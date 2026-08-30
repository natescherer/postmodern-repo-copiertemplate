# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich==15.0.0",
#     "tomlkit==0.15.1",
#     "watchdog==6.0.0",
# ]
# ///

"""Preview template/'s docs through a real zensical render.

A template project's docs can be gated by `{% if %}` conditionals both in their
path (e.g. `template/{% if is_template %}docs{% endif %}/`) and in their content
(a `.md.jinja` file with an `{% if is_public %}...{% endif %}` paragraph). Thus,
there's no single "correct" answer set to render the whole docs/ tree with.

So instead of picking one answer set, this renders the whole tree once per entry
in tests/answer_matrix.py's ANSWER_MATRIX (the same curated, valid combinations
the render-validation suite itself tests against), run in parallel: each entry's
a real `copier copy` subprocess call, releasing the GIL while it waits. Rather
than assume a fixed axis like this project's own project_type (a downstream
template can rename it, add values, or drop it), renders are grouped by what
they actually produced: any two whose docs/ end up with the exact same set of
files are the same "shape" and share one labeled top-level nav section, built
from that shape's own real nav (theme, CSS, JS unmodified); a page whose content
still differs *within* a shape gets its own nav entry expanded into labeled
sibling pages. This project's own Template and Standard project_types are one
example of two shapes, not an assumption baked into how shapes get found.

This script watches all *docs* source directories the whole time it runs and
re-renders on every save, so `zensical serve`'s own live-reload refreshes the
browser.

Run via `uv run` (its PEP 723 header above pulls in rich, tomlkit, and watchdog)
rather than plain `python`, since none of the three are otherwise a project
dependency.
"""

import argparse
import importlib.util
import re
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

# ty can't yet resolve a PEP 723 script's own inline deps (astral-sh/ty#4324), uv
# run installs these correctly at execution time regardless.
import tomlkit  # ty: ignore[unresolved-import]
from rich.console import Console  # ty: ignore[unresolved-import]
from watchdog.events import (  # ty: ignore[unresolved-import]
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer  # ty: ignore[unresolved-import]

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = REPO_ROOT / "template"
ANSWER_MATRIX_FILE = REPO_ROOT / "tests" / "answer_matrix.py"

console = Console()

IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", ".cache")

# How long the watched directories must go quiet before a save triggers a
# re-render, and how often the watch loop checks for that. Some editors fire more
# than one filesystem event per save (a write, then a rename for an atomic save):
# debouncing coalesces those into one re-render instead of several overlapping
# ones. Also long enough to collapse a burst of autosave-on-pause events while
# actively typing into one render, without making a single deliberate edit wait
# an unreasonably long time to see its result.
DEBOUNCE_SECONDS = 5.0
POLL_SECONDS = 0.1

# Matches a whole Jinja tag ("{% if is_template %}", "{% endif %}", "{# ... #}"),
# never a partial one: this template's own convention gates a whole path segment
# at a time, never part of a name, so stripping every tag leaves exactly the literal
# name a "true" render would produce.
JINJA_TAG = re.compile(r"\{[%#].*?[%#]\}")


class PreviewBuildError(Exception):
    """No ANSWER_MATRIX entry could render a usable preview."""


def run(
    *args: str, cwd: Path | None = None, capture: bool = False, quiet: bool = False
) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first unless `quiet`.

    Resolves argv[0] via shutil.which() first: some CLIs are wrapped in ways that
    subprocess with shell=False won't find from the bare name alone on every
    platform.

    Returns:
        The completed process, with captured stdout/stderr merged if `capture`.

    """
    if not quiet:
        console.print(f"$ {' '.join(args)}" + (f"  (in {cwd})" if cwd else ""))
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    stdout = subprocess.PIPE if capture else None
    stderr = subprocess.STDOUT if capture else None
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        resolved, check=True, cwd=cwd, stdout=stdout, stderr=stderr, text=True
    )


def load_answer_matrix() -> list[dict]:
    """Load ANSWER_MATRIX from tests/answer_matrix.py without touching sys.path.

    Returns:
        The list of curated, valid answer-matrix entries.

    Raises:
        SystemExit: if tests/answer_matrix.py can't be loaded at all.

    """
    spec = importlib.util.spec_from_file_location("answer_matrix", ANSWER_MATRIX_FILE)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load {ANSWER_MATRIX_FILE}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ANSWER_MATRIX


def find_docs_source_dirs() -> list[Path]:
    """Locate every docs source directory directly under template/.

    There can be more than one: this project's own template/ has a directory
    gated on is_template and a separate, much smaller one gated on is_standard for
    the other project_type. Matched purely by each directory's own name stripping
    down to "docs" once its Jinja conditional is removed (doesn't need to know
    what condition or axis is actually gating it, or what values it takes), so
    this generalizes to whatever a downstream template ends up using for the same
    purpose, not just this project's own project_type/is_template/is_standard.

    Returns:
        Every "docs"-shaped directory found.

    """
    return [
        child
        for child in TEMPLATE_DIR.iterdir()
        if child.is_dir() and JINJA_TAG.sub("", child.name) == "docs"
    ]


def render_variant(entry: dict, dest: Path) -> None:
    """Render template/ once using one ANSWER_MATRIX entry's answers, into `dest`.

    Mirrors tests/conftest.py's own `-d key=value` invocation for ANSWER_MATRIX
    entries, so this exercises the exact same copier invocation the render-
    validation suite already trusts.
    """
    src = Path(tempfile.mkdtemp(prefix="tdsrc-"))
    try:
        shutil.copytree(TEMPLATE_DIR, src / "template", ignore=IGNORE_PATTERNS)
        shutil.copy2(REPO_ROOT / "copier.yml", src / "copier.yml")
        data_args = [
            arg
            for key, value in entry.items()
            if key not in ("id", "_old_tag_overrides")
            for arg in ("-d", f"{key}={value}")
        ]
        run(
            "copier",
            "copy",
            "--trust",
            "--defaults",
            "--overwrite",
            "--skip-tasks",
            *data_args,
            str(src),
            str(dest),
            capture=True,
            quiet=True,
        )
    finally:
        shutil.rmtree(src, ignore_errors=True)


def render_all_variants() -> tuple[list[tuple[dict, Path]], list[str]]:
    """Render the whole template/ tree once per ANSWER_MATRIX entry, in parallel.

    Each render is a full site, kept around under its own temp dest; the caller
    is responsible for cleaning those up once it's done reading from them.

    Returns:
        (successful (entry, dest) pairs in ANSWER_MATRIX order, error messages from
        entries that failed to render at all).

    """
    matrix = load_answer_matrix()

    def _one(entry: dict) -> tuple[dict, Path] | str:
        """Render one entry.

        Returns:
            (entry, dest) on success, or an error string if the render failed.

        """
        dest = Path(tempfile.mkdtemp(prefix="tdvariant-"))
        try:
            render_variant(entry, dest)
        except subprocess.CalledProcessError as exc:
            shutil.rmtree(dest, ignore_errors=True)
            return f"{entry['id']}:\n{exc.output}"
        return (entry, dest)

    # map() yields results in matrix order regardless of completion order, which
    # keeps "the first applicable entry" (used to pick each section's primary
    # render) deterministic across runs rather than a race between the render
    # subprocesses.
    with ThreadPoolExecutor(max_workers=len(matrix)) as pool:
        results = list(pool.map(_one, matrix))

    renders = [r for r in results if isinstance(r, tuple)]
    errors = [r for r in results if isinstance(r, str)]
    return renders, errors


@dataclass
class Variant:
    """One ANSWER_MATRIX entry's rendered take on a target file."""

    entry: dict
    dest: Path
    content: str


def variants_for_path(
    renders: list[tuple[dict, Path]], docs_rel: Path
) -> list[Variant]:
    """Check `docs_rel` across every already-rendered tree, relative to render root.

    Returns:
        A Variant for each render that actually has this file.

    """
    variants = []
    for entry, render_dest in renders:
        target = render_dest / docs_rel
        if target.is_file():
            content = target.read_text(encoding="utf-8")
            variants.append(Variant(entry, render_dest, content))
    return variants


def dedupe_variants(variants: list[Variant]) -> list[list[Variant]]:
    """Group variants that rendered identically, in ANSWER_MATRIX order.

    Returns:
        Groups of variants sharing identical content, in the order their content
        was first seen.

    """
    groups: dict[str, list[Variant]] = {}
    order: list[str] = []
    for variant in variants:
        if variant.content not in groups:
            groups[variant.content] = []
            order.append(variant.content)
        groups[variant.content].append(variant)
    return [groups[key] for key in order]


def secondary_page_path(candidate_rel: Path, entry_id: str) -> Path:
    """Path for a non-primary variant's page, distinguished by matrix entry id.

    Returns:
        The distinguished path, alongside `candidate_rel` in the same directory.

    """
    return candidate_rel.with_name(
        f"{candidate_rel.stem}--{entry_id}{candidate_rel.suffix}"
    )


def collect_nav_leaves(nav_node: object, leaves: set[str]) -> None:
    """Collect every plain path string referenced anywhere in a nav structure."""
    if isinstance(nav_node, str):
        leaves.add(nav_node)
    elif isinstance(nav_node, list):
        for item in nav_node:
            collect_nav_leaves(item, leaves)
    elif isinstance(nav_node, dict):
        for value in nav_node.values():
            collect_nav_leaves(value, leaves)


def expand_nav_variants(
    nav_node: object, variant_pages: dict[str, list[dict[str, str]]]
) -> object:
    """Recursively rebuild `nav_node`, expanding any leaf path that has variants.

    A leaf whose path is a key in `variant_pages` is replaced by its list of
    `{label: path}` entries, spliced into the surrounding list in its place;
    everything else in the nav is left exactly as the primary render authored it.

    Returns:
        The rebuilt nav node.

    """
    if isinstance(nav_node, str):
        return variant_pages.get(nav_node, nav_node)
    if isinstance(nav_node, list):
        result: list[object] = []
        for item in nav_node:
            expanded = expand_nav_variants(item, variant_pages)
            if isinstance(expanded, list):
                result.extend(expanded)
            else:
                result.append(expanded)
        return result
    if isinstance(nav_node, dict):
        return {
            key: expand_nav_variants(value, variant_pages)
            for key, value in nav_node.items()
        }
    return nav_node


def read_nav(render_dest: Path) -> object:
    """Read a rendered site's own nav, straight from its own zensical.toml.

    Returns:
        The parsed nav array.

    """
    zensical_toml = render_dest / "zensical.toml"
    doc = tomlkit.parse(zensical_toml.read_text(encoding="utf-8"))
    return doc["project"]["nav"]


def prefix_nav_paths(nav_node: object, prefix: Path) -> object:
    """Recursively rebuild `nav_node` with every leaf path prefixed by `prefix`.

    Returns:
        The rebuilt nav node.

    """
    if isinstance(nav_node, str):
        return (prefix / nav_node).as_posix()
    if isinstance(nav_node, list):
        return [prefix_nav_paths(item, prefix) for item in nav_node]
    if isinstance(nav_node, dict):
        return {key: prefix_nav_paths(value, prefix) for key, value in nav_node.items()}
    return nav_node


def build_section(
    dest: Path, type_renders: list[tuple[dict, Path]], path_prefix: Path | None
) -> object:
    """Build one project_type's nav section, writing its pages under `path_prefix`.

    `type_renders` must already be filtered to a single project_type, in
    ANSWER_MATRIX order. `path_prefix` relocates every page under it (relative to
    docs_dir) so this section's pages don't collide with another section sharing
    the same `dest`; pass None only for the one section whose relative links
    were authored assuming they sit at docs_dir's own root: this template's own
    Template-type docs cross-reference each other extensively with plain relative
    links like "releasing.md" or "../index.md#..." (prefixing them without also
    rewriting every link target breaks every one of those, confirmed: zensical's
    own build reported "page does not exist" for exactly these links the first
    time every section got prefixed uniformly).

    Returns:
        This section's nav: the first applicable render's own real nav, prefixed
        if `path_prefix` is given, with any page that varies expanded into
        labeled sibling pages.

    """
    _primary_entry, primary_dest = type_renders[0]
    original_nav = read_nav(primary_dest)

    if path_prefix is None:
        shutil.copytree(primary_dest / "docs", dest / "docs", dirs_exist_ok=True)

    leaves: set[str] = set()
    collect_nav_leaves(original_nav, leaves)

    variant_pages: dict[str, list[dict[str, str]]] = {}
    for nav_path in leaves:
        docs_rel = Path("docs") / nav_path
        target_nav_path = (
            (path_prefix / nav_path).as_posix() if path_prefix else nav_path
        )
        groups = dedupe_variants(variants_for_path(type_renders, docs_rel))
        if not groups:
            continue  # Shouldn't happen: primary's own nav references it.
        if len(groups) == 1:
            if path_prefix is not None:
                # Nothing pre-populated `dest` at a prefixed location the way the
                # unprefixed case's copytree above already covers.
                page_rel = Path("docs") / target_nav_path
                (dest / page_rel).parent.mkdir(parents=True, exist_ok=True)
                (dest / page_rel).write_text(groups[0][0].content, encoding="utf-8")
            continue
        entries = []
        for group in groups:
            representative = group[0]
            if path_prefix is None and representative.dest == primary_dest:
                page_rel = docs_rel  # Already synced above.
            else:
                variant_rel = secondary_page_path(
                    Path(target_nav_path), representative.entry["id"]
                )
                page_rel = Path("docs") / variant_rel
                (dest / page_rel).parent.mkdir(parents=True, exist_ok=True)
                (dest / page_rel).write_text(representative.content, encoding="utf-8")
            entries.append(
                {representative.entry["id"]: page_rel.relative_to("docs").as_posix()}
            )
        variant_pages[target_nav_path] = entries

    nav = (
        original_nav
        if path_prefix is None
        else prefix_nav_paths(original_nav, path_prefix)
    )
    return expand_nav_variants(nav, variant_pages)


def docs_fingerprint(render_dest: Path) -> frozenset[str]:
    """Compute the set of relative paths under a render's docs/, its "shape".

    Returns:
        A hashable set of docs-relative paths (empty if there's no docs/ at all).

    """
    docs_dir = render_dest / "docs"
    if not docs_dir.is_dir():
        return frozenset()
    return frozenset(
        str(p.relative_to(docs_dir)) for p in docs_dir.rglob("*") if p.is_file()
    )


def group_by_docs_shape(
    renders: list[tuple[dict, Path]],
) -> list[list[tuple[dict, Path]]]:
    """Group renders whose docs/ trees have the exact same set of files.

    Different answer combinations can produce structurally different docs/ trees
    (this project's own template/ has an is_template docs source and a completely
    separate, smaller is_standard one); rather than hardcode which answer (e.g.
    project_type) drives that, or what its values are called, this groups purely
    by what each render actually produced. Whatever axis a downstream template
    ends up using for the same purpose (however many values, whatever they're
    named) falls out of this for free. Two renders sharing a shape but differing
    in per-page *content* still land in the same group here; that's exactly what
    build_section()'s own per-page variant expansion is for.

    Returns:
        Groups of (entry, dest) pairs sharing an identical docs/ file set, in the
        order each shape was first seen (ANSWER_MATRIX order).

    """
    groups: dict[frozenset[str], list[tuple[dict, Path]]] = {}
    order: list[frozenset[str]] = []
    for entry, render_dest in renders:
        shape = docs_fingerprint(render_dest)
        if shape not in groups:
            groups[shape] = []
            order.append(shape)
        groups[shape].append((entry, render_dest))
    return [groups[key] for key in order]


def section_label(type_renders: list[tuple[dict, Path]], index: int) -> str:
    """Build a human label for one docs-shape group's nav section.

    Returns:
        `"<project_type> Project"` if every render in this group agrees on a
        project_type answer (whatever it's actually called downstream), else a
        generic positional fallback for a template that doesn't have one.

    """
    types = {entry.get("project_type") for entry, _ in type_renders}
    if len(types) == 1:
        (project_type,) = types
        if project_type:
            return f"{project_type} Project"
    return f"Docs ({index + 1})"


def assemble_whole_tree(dest: Path, renders: list[tuple[dict, Path]]) -> None:
    """Build one nav section per distinct docs "shape" found in `renders`.

    The theme/CSS/JS/etc. from whichever render happens to be first becomes
    `dest`'s shared assets; those don't vary by shape. Each distinct shape gets
    its own labeled top-level nav group, built from that group's own real nav
    with any page whose content varies within the group expanded into labeled
    sibling pages (see group_by_docs_shape()'s docstring for why shape, not a
    hardcoded answer key, is what defines a section).

    The first shape found (ANSWER_MATRIX order) is left unprefixed, since this
    project's own docs cross-reference each other with plain relative links (see
    build_section()'s docstring) and prefixing breaks those; every other shape is
    prefixed to avoid colliding with it.
    """
    shutil.copytree(renders[0][1], dest, dirs_exist_ok=True)

    sections = []
    for index, shape_renders in enumerate(group_by_docs_shape(renders)):
        path_prefix = None if index == 0 else Path(f"docs-{index + 1}")
        section_nav = build_section(dest, shape_renders, path_prefix)
        sections.append({section_label(shape_renders, index): section_nav})

    zensical_toml = dest / "zensical.toml"
    doc = tomlkit.parse(zensical_toml.read_text(encoding="utf-8"))
    doc["project"]["nav"] = sections
    zensical_toml.write_text(tomlkit.dumps(doc), encoding="utf-8")


def build_whole_tree_preview(dest: Path) -> None:
    """Render the whole docs/ tree under every ANSWER_MATRIX entry into `dest`.

    Raises:
        PreviewBuildError: if every ANSWER_MATRIX entry failed to render outright.

    """
    renders, errors = render_all_variants()
    try:
        if not renders:
            detail = "\n".join(errors) if errors else "every entry failed to render."
            raise PreviewBuildError(f"Could not render any preview:\n{detail}")
        assemble_whole_tree(dest, renders)
    finally:
        for _, render_dest in renders:
            shutil.rmtree(render_dest, ignore_errors=True)


def render_with_status(dest: Path, label: str) -> bool:
    """Build the preview behind a spinner, printing a one-line pass/fail summary.

    Returns:
        True if the build succeeded. False if it failed, with the error output
        already printed; the caller decides whether that's fatal.

    """
    start = time.perf_counter()
    try:
        with console.status(f"{label} ..."):
            build_whole_tree_preview(dest)
    except (subprocess.CalledProcessError, PreviewBuildError) as exc:
        elapsed = time.perf_counter() - start
        console.print(f"[red]✗ FAILED:[/red] {label} (after {elapsed:.1f}s):")
        is_subprocess_error = isinstance(exc, subprocess.CalledProcessError)
        detail = exc.output if is_subprocess_error else str(exc)
        # markup=False: this can contain copier's own captured output, not trusted
        # text; it can contain literal "[...]" (e.g. "[Errno 2]") that isn't rich
        # markup.
        console.print(detail, markup=False)
        return False
    elapsed = time.perf_counter() - start
    console.print(f"[green]✓ OK:[/green] {label} ({elapsed:.1f}s)")
    return True


def start_zensical(dest: Path, extra_args: list[str]) -> subprocess.Popen:
    """Start `zensical serve` in the background against `dest`.

    Returns:
        The running process; the caller is responsible for terminating it.

    """
    args = ["zensical", "serve", *extra_args]
    console.print(f"$ {' '.join(args)}  (in {dest})")
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    # S603: fixed argv, no shell=True.
    return subprocess.Popen(resolved, cwd=dest)  # noqa: S603


class ChangeHandler(FileSystemEventHandler):
    """Records the time of the most recent change under any watched directory."""

    def __init__(self, watch_dirs: list[Path]) -> None:
        """Watch `watch_dirs`; start out with no change recorded."""
        super().__init__()
        self._dirs = watch_dirs
        self.last_change_at: float | None = None

    def on_any_event(self, event: FileSystemEvent) -> None:
        """Record a change, ignoring anything outside the watched directories."""
        if event.is_directory:
            return
        changed = Path(event.src_path).resolve()
        if any(changed.is_relative_to(watch_dir) for watch_dir in self._dirs):
            self.last_change_at = time.monotonic()


def watch_and_rerender(
    dest: Path, handler: ChangeHandler, stop: threading.Event
) -> None:
    """Rebuild `dest` on each settled change `handler` reports, until `stop` fires."""
    while not stop.is_set():
        changed_at = handler.last_change_at
        if changed_at is not None and time.monotonic() - changed_at >= DEBOUNCE_SECONDS:
            handler.last_change_at = None
            console.print("\n⟳ Change detected")
            render_with_status(dest, "Re-rendering")
        stop.wait(POLL_SECONDS)


def main() -> None:
    """Preview docs, live-reloading on every save, until stopped.

    Raises:
        SystemExit: with code 1, if the very first build fails; there's nothing
            to serve yet, so that's fatal (unlike a later rebuild triggered by a
            change, which just keeps serving the last good version).

    """
    # sys.stdout is typed as TextIO, which doesn't declare reconfigure(): it's a
    # real TextIOWrapper at runtime, though. Without this, Windows' default console
    # codepage (cp1252) can't encode the status glyphs below (rich hits the same
    # UnicodeEncodeError regardless of which internal render path it takes, since
    # both end up calling sys.stdout.write() directly). Assumes whoever runs this has
    # a Unicode-capable terminal.
    sys.stdout.reconfigure(encoding="utf-8")  # ty: ignore[unresolved-attribute]

    parser = argparse.ArgumentParser(
        description="Preview template/'s docs through a real zensical render."
    )
    _args, zensical_args = parser.parse_known_args()

    watch_dirs = find_docs_source_dirs()
    if not watch_dirs:
        raise SystemExit(f"Could not find a docs/ source dir under {TEMPLATE_DIR}.")
    for docs_dir in watch_dirs:
        console.print(f"Previewing {docs_dir.relative_to(TEMPLATE_DIR)}")

    dest = Path(tempfile.mkdtemp(prefix="tdout-"))
    if not render_with_status(dest, "Rendering initial preview"):
        shutil.rmtree(dest, ignore_errors=True)
        raise SystemExit(1)

    server = start_zensical(dest, zensical_args)

    handler = ChangeHandler(watch_dirs)
    observer = Observer()
    for watch_dir in watch_dirs:
        observer.schedule(handler, str(watch_dir), recursive=True)
    observer.start()

    stop = threading.Event()
    watcher = threading.Thread(
        target=watch_and_rerender, args=(dest, handler, stop), daemon=True
    )
    watcher.start()

    watched = ", ".join(str(watch_dir) for watch_dir in watch_dirs)
    console.print(
        f"\nWatching {watched}: saves re-render and live-reload automatically. "
        "Press Ctrl+C to stop.\n"
    )

    try:
        server.wait()
    except KeyboardInterrupt:
        console.print("\nStopping ...")
    finally:
        stop.set()
        watcher.join(timeout=2)
        observer.stop()
        observer.join(timeout=2)
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
        shutil.rmtree(dest, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

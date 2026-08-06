"""Renders this template across a boundary answer matrix and structurally validates it.

Generic by design: every check here operates on whatever actually got rendered (globbing
for file types, checking for known top-level files) rather than hardcoding this repo's
specific doc set or question values -- see answer_matrix.py for the repo-specific piece,
which a child template should edit alongside its own copier.yml changes.
"""

import io
import json
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import tarfile
from pathlib import Path

import jinja2
import pytest
import tomllib
import yaml
from answer_matrix import ANSWER_MATRIX
from jinja2_ansible_filters import AnsibleCoreFiltersExtension


def _find_repo_root() -> Path:
    """Walk upward from this file to find the directory containing a template/ folder.

    Deliberately not a fixed parents[N]: this file lives two levels below the repo root
    as template source (template/{% if is_template %}tests{% endif %}/...) but only one
    level below it once rendered into a consumer project (tests/...), so a fixed depth
    would be wrong in one of the two contexts.

    Returns:
        The repo root directory.

    Raises:
        RuntimeError: if no parent directory contains a template/ folder.

    """
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "template").is_dir():
            return candidate
    raise RuntimeError(
        "Could not find repo root (no template/ folder found in any parent directory)"
    )


REPO_ROOT = _find_repo_root()


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run subprocess.run with output always captured as UTF-8 text.

    Windows' default console encoding (cp1252) can't decode tool output containing
    e.g. emoji or box-drawing characters (lychee's summary, for one) -- that mismatch
    crashes the background reader thread and leaves stdout/stderr as None instead of
    raising cleanly.

    Returns:
        The completed subprocess, with UTF-8-decoded stdout/stderr.

    """
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    result = _run(["git", *args], cwd=cwd)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"git {' '.join(args)} failed:\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    return result


def _git_init_repo(path: Path) -> None:
    """Init a throwaway git repo at `path` with a fixed local identity.

    Needed because `copier update` requires both the source and the destination to be
    git repositories -- it records `_commit` from the source at copy time and uses git
    to detect local destination changes when applying an update.
    """
    path.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q"], path)
    _git(["config", "user.email", "template-tests@example.invalid"], path)
    _git(["config", "user.name", "Template Tests"], path)


def _git_commit_all(path: Path, message: str) -> None:
    _git(["add", "-A"], path)
    _git(["commit", "-q", "-m", message], path)


def _ignore_for_copy(directory, names):
    skip = {
        ".git",
        ".cache",
        ".venv",
        "__pycache__",
        "docs_site",
        ".ruff_cache",
        ".rumdl_cache",
    }
    return [n for n in names if n in skip]


def _assemble_source(repo_root: Path, dest: Path) -> None:
    """Build a copier source rooted at `dest` from the current `template/` contents.

    Deliberately does not copy this repo's own root copier.yml: that file is dogfooded
    output, refreshed only by an occasional `copier update`, so it lags behind
    uncommitted or just-committed edits under template/ -- exactly the edits this suite
    exists to catch. When template/ contains a self-hosting conditional copier.yml (a
    template that, like this one, supports generating child templates), that file's
    non-raw header is rendered with stub values -- nothing in these tests inspects
    parent_template_name/url -- while its `{% raw %}...{% endraw %}` body (the real
    question set) passes through unprocessed, exactly as Copier itself would render it
    into a child's copier.yml.
    """
    shutil.copytree(
        repo_root / "template",
        dest / "template",
        dirs_exist_ok=True,
        ignore=_ignore_for_copy,
    )

    conditional_copier_yml = (
        repo_root / "template" / "{% if is_template %}copier.yml{% endif %}.jinja"
    )
    if conditional_copier_yml.is_file():
        # S701: renders YAML, never HTML, so there's no XSS surface for autoescape.
        env = jinja2.Environment(extensions=[AnsibleCoreFiltersExtension])  # noqa: S701
        rendered = env.from_string(
            conditional_copier_yml.read_text(encoding="utf-8")
        ).render(
            project_name="Test Parent Template",
            using_github=True,
            using_azdo=False,
            github_repo_owner="test-owner",
            azdo_org="",
            azdo_project_encoded="",
            repo_name="test-parent-template",
        )
        (dest / "copier.yml").write_text(rendered, encoding="utf-8")
    else:
        shutil.copy2(repo_root / "copier.yml", dest / "copier.yml")


def _latest_tag(repo_root: Path) -> str | None:
    """Return this repo's most recent git tag by version sort.

    Returns:
        The latest tag name, or None if the repo has no tags yet (e.g. a brand-new
        template before its first release).

    """
    result = _run(["git", "tag", "--sort=-v:refname"], cwd=repo_root)
    tags = [line for line in result.stdout.splitlines() if line.strip()]
    return tags[0] if tags else None


def _assemble_update_scratch_repo(repo_root: Path, old_tag: str, dest: Path) -> None:
    """Build a 2-commit copier source for testing the update path: old_tag -> current.

    Commit 1 is `repo_root`'s real, historical state at `old_tag` (its actual root
    copier.yml as released, not synthesized) -- exactly what a real user updating from
    that release would have used as their template source. Commit 2 (HEAD) is the
    current on-disk template/ contents, assembled the same way _assemble_source builds
    it for the copy-only tests, so uncommitted edits are covered here too.

    Both states have to live at the same path across two commits, not two separate
    directories: `copier update` always re-reads `_src_path` from the destination's
    answers file and re-resolves *that same path* at update time, it can't be pointed
    at a different "new" source.
    """
    _git_init_repo(dest)

    # S603, S607: fixed args, no shell=True, resolved from PATH like every other tool
    # invocation in this file (actionlint, tombi, zensical, lychee).
    archive = subprocess.run(  # noqa: S603
        ["git", "archive", old_tag],  # noqa: S607
        cwd=repo_root,
        capture_output=True,
    )
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert archive.returncode == 0, f"git archive {old_tag} failed: {archive.stderr!r}"  # noqa: S101
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        tar.extractall(dest, filter="data")  # trusted content: this repo's own history
    _git_commit_all(dest, old_tag)
    _git(["tag", old_tag], dest)

    for child in dest.iterdir():
        if child.name == ".git":
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    _assemble_source(repo_root, dest)
    _git_commit_all(dest, "current")


@pytest.fixture(scope="session")
def template_source(tmp_path_factory):
    """Build a self-contained copier source fresh from the current template/ tree.

    Returns:
        Path to the fixture-scoped copier source directory.

    """
    src = tmp_path_factory.mktemp("template-source")
    _assemble_source(REPO_ROOT, src)
    return src


@pytest.fixture(scope="session")
def update_source(tmp_path_factory):
    """Build a 2-commit copier source (last tag -> current) for update-path testing.

    Skips dependent tests if this repo has no git tags yet.

    Returns:
        A (source_path, old_tag) tuple.

    """
    old_tag = _latest_tag(REPO_ROOT)
    if old_tag is None:
        pytest.skip("No git tags found -- nothing to update from yet.")
    src = tmp_path_factory.mktemp("update-source")
    _assemble_update_scratch_repo(REPO_ROOT, old_tag, src)
    return src, old_tag


def _render(source: Path, dest: Path, answers: dict, vcs_ref: str | None = None):
    args = ["copier", "copy", "--trust", "--defaults", "--skip-tasks"]
    if vcs_ref is not None:
        args.append(f"--vcs-ref={vcs_ref}")
    for key, value in answers.items():
        if key == "id":
            continue
        args.extend(["-d", f"{key}={value}"])
    args.extend([str(source), str(dest)])
    result = _run(args)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"copier copy failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )


# VS Code parses these specific files as JSONC (comments and trailing commas allowed),
# never as strict JSON -- see
# https://code.visualstudio.com/docs/languages/json#_json-with-comments.
_VSCODE_JSONC_FILES = {
    "settings.json",
    "extensions.json",
    "launch.json",
    "tasks.json",
    "keybindings.json",
}


def _check_structured_files(root: Path) -> list[str]:
    """Parse every TOML/JSON/YAML file in the render.

    Returns:
        One error string per file that failed to parse.

    """
    errors = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        try:
            if path.suffix == ".toml":
                tomllib.load(path.open("rb"))
            elif path.suffix == ".json":
                if path.parent.name == ".vscode" and path.name in _VSCODE_JSONC_FILES:
                    continue
                json.load(path.open(encoding="utf-8"))
            elif path.suffix in (".yml", ".yaml"):
                list(yaml.safe_load_all(path.open(encoding="utf-8")))
        except Exception as exc:  # noqa: BLE001 - collecting all errors, not just the first
            errors.append(f"{rel}: {exc}")
    return errors


def _check_actionlint(root: Path) -> list[str]:
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        return []
    # actionlint's zero-arg mode auto-finds .github/workflows by walking up to a git
    # repo root, which a bare rendered tmp dir isn't; passing files sidesteps that.
    files = [str(p) for p in workflows.glob("*.yml")] + [
        str(p) for p in workflows.glob("*.yaml")
    ]
    result = _run(["actionlint", *files], cwd=root)
    if result.returncode != 0:
        return [result.stdout.strip() or result.stderr.strip()]
    return []


def _check_tombi(root: Path) -> list[str]:
    toml_files = list(root.rglob("*.toml"))
    if not toml_files:
        return []
    result = _run(["tombi", "lint", *[str(p) for p in toml_files]], cwd=root)
    if result.returncode != 0:
        return [result.stdout.strip() or result.stderr.strip()]
    return []


def _check_zensical_build(root: Path) -> list[str]:
    if not (root / "zensical.toml").is_file():
        return []
    result = _run(["zensical", "build"], cwd=root)
    output = (
        result.stdout + result.stderr
    )  # zensical prints "No issues found" to stderr
    if result.returncode != 0 or "No issues found" not in output:
        return [output.strip()]
    return []


def _check_lychee(root: Path) -> list[str]:
    # Mirrors prek.toml's own lychee hook, which excludes docs_site: built HTML's
    # root-relative links (e.g. "/assets/...") resolve against the filesystem root
    # without a running server, producing bogus failures unrelated to the source
    # markdown this check is meant to validate.
    result = _run(
        ["lychee", "--no-progress", "--offline", "--exclude-path", "docs_site", "."],
        cwd=root,
    )
    if result.returncode != 0:
        return [result.stdout.strip() or result.stderr.strip()]
    return []


def _check_all(root: Path) -> list[str]:
    """Run every structural check against a rendered project.

    Returns:
        All collected error strings, each prefixed by which check produced it.

    """
    errors = []
    errors += [f"[structured-files] {e}" for e in _check_structured_files(root)]
    errors += [f"[actionlint] {e}" for e in _check_actionlint(root)]
    errors += [f"[tombi] {e}" for e in _check_tombi(root)]
    errors += [f"[zensical] {e}" for e in _check_zensical_build(root)]
    errors += [f"[lychee] {e}" for e in _check_lychee(root)]
    return errors


@pytest.mark.parametrize("answers", ANSWER_MATRIX, ids=lambda a: a["id"])
def test_render_combination(template_source, tmp_path, answers):
    """Render one answer_matrix.py combination and run every structural check on it."""
    dest = tmp_path / "out"
    _render(template_source, dest, answers)
    errors = _check_all(dest)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert not errors, "\n\n".join(errors)  # noqa: S101


@pytest.mark.parametrize("answers", ANSWER_MATRIX, ids=lambda a: a["id"])
def test_update_from_last_tag(update_source, tmp_path, answers):
    """Copy at this repo's last tag, update to current, and re-run every check.

    Covers the one class of bug the copy-only test above can't see: logic gated on
    `_copier_operation == 'update'` (e.g. the `project_initialized` locked-on-update
    question text, `current_release_please_version`) is never exercised by a fresh
    `copier copy`, since that operation is always `'copy'`.
    """
    source, old_tag = update_source
    dest = tmp_path / "out"
    _render(source, dest, answers, vcs_ref=old_tag)

    _git_init_repo(dest)
    _git_commit_all(dest, "initial render")

    result = _run(
        [
            "copier",
            "update",
            "--trust",
            "--defaults",
            "--skip-tasks",
            "--vcs-ref=HEAD",
            "-a",
            ".config/copier-answers.yml",
        ],
        cwd=dest,
    )
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"copier update failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    errors = _check_all(dest)
    assert not errors, "\n\n".join(errors)  # noqa: S101

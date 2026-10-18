"""Renders this template across a boundary answer matrix and structurally validates it.

Generic by design: every check here operates on whatever actually got rendered (globbing
for file types, checking for known top-level files) rather than hardcoding this repo's
specific doc set or question values; see answer_matrix.py for the repo-specific piece,
which a child template should edit alongside its own copier.yml changes.
"""

import json
import tomllib
from pathlib import Path

import pytest
import yaml
from answer_matrix import ANSWER_MATRIX
from conftest import _git_commit_all, _git_init_repo, _render, _run

# VS Code parses these specific files as JSONC (comments and trailing commas allowed),
# never as strict JSON; see
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
    # Mirrors prek.toml's own lychee hook, which excludes docs-site: built HTML's
    # root-relative links (e.g. "/assets/...") resolve against the filesystem root
    # without a running server, producing bogus failures unrelated to the source
    # markdown this check is meant to validate.
    result = _run(
        ["lychee", "--no-progress", "--offline", "--exclude-path", "docs-site", "."],
        cwd=root,
    )
    if result.returncode != 0:
        return [result.stdout.strip() or result.stderr.strip()]
    return []


def _check_all(root: Path, *, zensical: bool = True) -> list[str]:
    """Run every structural check against a rendered project.

    `zensical` is skippable: `test_update_from_last_tag` renders the same combo
    `test_render_combination` already builds docs for, just via `copier update`
    instead of a fresh copy; re-running the (comparatively slow) zensical build
    there would only re-confirm docs content that hasn't changed, not exercise
    anything update-path-specific.

    Returns:
        All collected error strings, each prefixed by which check produced it.

    """
    errors = []
    errors += [f"[structured-files] {e}" for e in _check_structured_files(root)]
    errors += [f"[actionlint] {e}" for e in _check_actionlint(root)]
    errors += [f"[tombi] {e}" for e in _check_tombi(root)]
    if zensical:
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
    `_copier_operation == 'update'` or on `project_initialized` (e.g. the `ask:`
    conditions that stop setup-only questions prompting, `current_knope_version`) is
    never exercised by a fresh `copier copy`, since that operation is always `'copy'`.
    Migrations only run on update too, so this also checks they did their job instead
    of only warning.
    """
    source, old_tag = update_source
    dest = tmp_path / "out"

    # The copy at the last release uses that release's question set, so an answer it
    # doesn't accept yet (a newly added or renamed choice value) would fail here. An
    # entry's `_old_tag_overrides` swaps in a value that release does accept, and the
    # update below passes the entry's real value back in.
    overrides = answers.get("_old_tag_overrides", {})
    _render(source, dest, {**answers, **overrides}, vcs_ref=old_tag)

    _git_init_repo(dest)
    _git_commit_all(dest, "initial render")

    real_values = [arg for key in overrides for arg in ("-d", f"{key}={answers[key]}")]
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
            *real_values,
        ],
        cwd=dest,
    )
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"copier update failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    output = result.stdout + result.stderr
    # A migration that can't do its job warns instead of failing the update.
    warnings = [line for line in output.splitlines() if line.startswith("Warning:")]
    assert not warnings, "\n".join(warnings)  # noqa: S101
    # The source's HEAD commit is a `feat:`, so the changeset migration writes one.
    assert list((dest / ".changeset").glob("template-update-*.md")), output  # noqa: S101
    if answers["lifecycle"] == "Stable":
        # current_knope_version reads the destination's version file, still 0.0.0,
        # so _message_after_update pins the first release to 1.0.0.
        override = json.loads(
            (dest / ".config/knope-release-override.json").read_text(encoding="utf-8")
        )
        assert override["version"] == "1.0.0", override  # noqa: S101

    errors = _check_all(dest, zensical=False)
    assert not errors, "\n\n".join(errors)  # noqa: S101


def _first_entry(**match) -> dict:
    return next(
        entry
        for entry in ANSWER_MATRIX
        if all(entry.get(key) == value for key, value in match.items())
    )


def test_nested_template(update_source, tmp_path):
    """Copy a Template child with its tasks, then copy a project from that child.

    The render tests skip tasks, so they never run `copy-template-files`, the task
    that gives a Template child its own copy of `template/`; without it, the child
    can't be copied from at all. This runs it (repo setup stays off, so nothing
    touches a remote) and then renders a grandchild from the result.
    """
    source, _ = update_source
    child_answers = _first_entry(project_type="Template", developer_platform="GitHub")
    child = tmp_path / "child"
    args = ["copier", "copy", "--trust", "--defaults", "--vcs-ref=HEAD"]
    for key, value in child_answers.items():
        if key not in ("id", "_old_tag_overrides"):
            args.extend(["-d", f"{key}={value}"])
    result = _run([*args, str(source), str(child)])
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"copier copy failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    def files(root: Path) -> dict[str, bytes]:
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    assert files(child / "template") == files(source / "template")  # noqa: S101

    grandchild = tmp_path / "grandchild"
    _render(child, grandchild, _first_entry(project_type="Standard"))
    errors = _check_all(grandchild, zensical=False)
    assert not errors, "\n\n".join(errors)  # noqa: S101

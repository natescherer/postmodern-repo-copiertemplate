"""Render this template across a boundary answer matrix and validate the output.

Generic by design: every check works on whatever was rendered (globbing for file types,
looking for known top-level files) instead of hardcoding this repo's docs or question
values. answer_matrix.py holds the repo-specific part, which a child template edits
along with its own copier.yml.
"""

import json
import shutil
import sys
import tomllib
from pathlib import Path

import pytest
import yaml
from conftest import (
    IS_LEAF,
    RENDERABLE_ANSWERS,
    _git_commit_all,
    _git_init_repo,
    _leaf_template,
    _render,
    _run,
)

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
    files = [str(p) for p in toml_files]
    errors = []
    # The tombi-format hook rewrites what `--check` flags, which fails the commit.
    for command in (["tombi", "lint"], ["tombi", "format", "--check", "--diff"]):
        result = _run([*command, *files], cwd=root)
        if result.returncode != 0:
            errors.append(result.stdout.strip() or result.stderr.strip())
    return errors


def _check_gh_settings(root: Path) -> list[str]:
    settings = root / ".github" / "settings.yml"
    if not settings.is_file():
        return []
    # The version the rendered project pins, run through `mise x`: this repo's own
    # mise.toml may not pin gh-settings yet.
    tools = tomllib.loads((root / "mise.toml").read_text(encoding="utf-8"))["tools"]
    version = tools.get("github:noirbizarre/gh-settings")
    if not version:
        return ["mise.toml doesn't pin gh-settings, which applies .github/settings.yml"]
    result = _run(
        [
            "mise",
            "x",
            f"github:noirbizarre/gh-settings@{version}",
            "--",
            "gh-settings",
            "validate",
            "--strict",
            "-c",
            str(settings),
        ],
        cwd=root,
    )
    if result.returncode != 0:
        return [result.stdout.strip() or result.stderr.strip()]
    return []


def _check_rumdl(root: Path) -> list[str]:
    result = _run(["rumdl", "check", "--no-cache", "."], cwd=root)
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
    # Excludes docs-site, like prek.toml's lychee hook: without a server, the built
    # HTML's root-relative links ("/assets/...") resolve against the filesystem root
    # and fail for reasons unrelated to the Markdown source.
    result = _run(
        ["lychee", "--no-progress", "--offline", "--exclude-path", "docs-site", "."],
        cwd=root,
    )
    if result.returncode != 0:
        return [result.stdout.strip() or result.stderr.strip()]
    return []


def _check_all(root: Path, *, zensical: bool = True) -> list[str]:
    """Run every structural check against a rendered project.

    `zensical` can be skipped: `test_update_from_last_tag` renders the same combination
    `test_render_combination` already builds docs for, only through `copier update`, so
    rebuilding the docs there would recheck unchanged content.

    Returns:
        All collected error strings, each prefixed by which check produced it.

    """
    errors = []
    errors += [f"[structured-files] {e}" for e in _check_structured_files(root)]
    errors += [f"[actionlint] {e}" for e in _check_actionlint(root)]
    errors += [f"[tombi] {e}" for e in _check_tombi(root)]
    errors += [f"[rumdl] {e}" for e in _check_rumdl(root)]
    errors += [f"[gh-settings] {e}" for e in _check_gh_settings(root)]
    if zensical:
        errors += [f"[zensical] {e}" for e in _check_zensical_build(root)]
    errors += [f"[lychee] {e}" for e in _check_lychee(root)]
    return errors


@pytest.mark.parametrize("answers", RENDERABLE_ANSWERS, ids=lambda a: a["id"])
def test_render_combination(template_source, tmp_path, answers):
    """Render one answer_matrix.py combination and run every structural check on it."""
    dest = tmp_path / "out"
    _render(template_source, dest, answers)
    errors = _check_all(dest)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert not errors, "\n\n".join(errors)  # noqa: S101


@pytest.mark.parametrize("answers", RENDERABLE_ANSWERS, ids=lambda a: a["id"])
def test_update_from_last_tag(update_source, tmp_path, answers):
    """Copy at this repo's last tag, update to current, and re-run every check.

    A fresh `copier copy` never exercises logic gated on `_copier_operation == 'update'`
    or on `project_initialized`, such as the `ask:` conditions that keep setup-only
    questions from prompting and `current_knope_version`. Migrations run only on update
    too, so this also checks that they did their job instead of only warning.
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


def _files(root: Path, skip: tuple[str, ...] = ()) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).as_posix() not in skip
    }


@pytest.mark.skipif(IS_LEAF, reason="A leaf template's template/ is already folded.")
@pytest.mark.parametrize(
    "answers",
    [entry for entry in RENDERABLE_ANSWERS if entry["project_type"] == "Standard"],
    ids=lambda a: a["id"],
)
def test_leaf_fold_keeps_output(template_source, tmp_path, answers):
    """Render a Standard project from a leaf template's folded template/, and compare.

    copy-template-files folds the project-type gates out of a leaf template's copy of
    template/ with fold_leaf_gates.py. A leaf's projects are always Standard, so every
    Standard project must render byte for byte the same from the folded copy.
    """
    folded = tmp_path / "folded"
    _leaf_template(template_source / "template", folded / "template")
    shutil.copy2(template_source / "copier.yml", folded / "copier.yml")
    _render(template_source, tmp_path / "original-out", answers)
    _render(folded, tmp_path / "folded-out", answers)
    # The answers file records each source's own path.
    skip = (".config/copier-answers.yml",)
    original = _files(tmp_path / "original-out", skip)
    assert _files(tmp_path / "folded-out", skip) == original  # noqa: S101


def _first_entry(**match) -> dict:
    return next(
        entry
        for entry in RENDERABLE_ANSWERS
        if all(entry.get(key) == value for key, value in match.items())
    )


@pytest.mark.skipif(IS_LEAF, reason="A leaf template's projects are never templates.")
@pytest.mark.parametrize("extensible", [True, False], ids=["extensible", "leaf"])
def test_nested_template(update_source, tmp_path, extensible):
    """Copy a Template child with its tasks, then copy a project from that child.

    The render tests skip tasks, so they never run `copy-template-files`, the task
    that gives a Template child its own copy of `template/`; without it, the child
    can't be copied from at all. This runs it (repo setup stays off, so nothing
    touches a remote), checks that a no-op `copier update` of the child succeeds,
    and then renders a grandchild from the result. An extensible
    template child gets the parent's whole `template/`. A leaf template child gets it
    without the paths gated on is_template or is_extensible and with the project-type
    gates folded out, its copier.yml has no project-type questions or
    copy-template-files task, and its own copy of this suite passes.
    """
    source, _ = update_source
    child_answers = {
        **_first_entry(project_type="Template", developer_platform="GitHub"),
        "extensible_template": extensible,
    }
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

    # HEAD is past the last tag, so the child records a `git describe` _commit, and
    # the update replays the task at that version first.
    _git_init_repo(child)
    _git_commit_all(child, "initial copy")
    result = _run(
        [
            "copier",
            "update",
            "--trust",
            "--defaults",
            "--skip-answered",
            "--vcs-ref=HEAD",
            "-a",
            ".config/copier-answers.yml",
        ],
        cwd=child,
    )
    assert result.returncode == 0, (  # noqa: S101
        f"copier update failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    expected = source / "template"
    if not extensible:
        expected = tmp_path / "leaf-template"
        _leaf_template(source / "template", expected)
    assert _files(child / "template") == _files(expected)  # noqa: S101

    # A leaf template's copier.yml drops what only a Template project uses.
    child_questions = yaml.safe_load((child / "copier.yml").read_text(encoding="utf-8"))
    project_type_keys = {
        "project_type",
        "extensible_template",
        "is_standard",
        "is_template",
        "is_extensible",
    }
    present = project_type_keys & child_questions.keys()
    assert present == (project_type_keys if extensible else set()), present  # noqa: S101
    copies_template = "template_only" in str(child_questions["_tasks"])
    assert copies_template == extensible  # noqa: S101

    grandchild = tmp_path / "grandchild"
    _render(child, grandchild, _first_entry(project_type="Standard"))
    errors = _check_all(grandchild, zensical=False)
    assert not errors, "\n\n".join(errors)  # noqa: S101

    if not extensible:
        # The leaf's own suite, run as its maintainers run it.
        result = _run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                f"--basetemp={tmp_path / 'suite'}",
            ],
            cwd=child,
        )
        assert result.returncode == 0, result.stdout[-10000:]  # noqa: S101

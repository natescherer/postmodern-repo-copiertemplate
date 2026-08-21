"""Checks content/config consistency in the rendered template, not the rendering itself.

Generic by design: every check here operates on whatever actually got rendered, rather
than hardcoding this repo's specific doc set -- see answer_matrix.py for the
repo-specific piece, which a child template should edit alongside its own copier.yml
changes.
"""

import re
from pathlib import Path

import pytest
import tomllib
import yaml
from answer_matrix import ANSWER_MATRIX
from conftest import _render


def _extract_nav_paths(nav: list) -> list[str]:
    """Recursively collect every doc path referenced in a zensical nav.

    Returns:
        Every path string found, however deeply nested under section titles.

    """
    paths = []
    for entry in nav:
        if isinstance(entry, str):
            paths.append(entry)
        elif isinstance(entry, dict):
            for value in entry.values():
                if isinstance(value, str):
                    paths.append(value)
                elif isinstance(value, list):
                    paths.extend(_extract_nav_paths(value))
    return paths


def _load_nav(root: Path) -> tuple[Path, list] | None:
    """Load zensical.toml's docs_dir and nav, if both are configured.

    Returns:
        A (docs_dir, nav) tuple, or None if there's no zensical.toml or no nav defined
        (an absent nav means every file under docs_dir is auto-included by default, so
        there's nothing for either completeness check below to verify).

    """
    zensical_toml = root / "zensical.toml"
    if not zensical_toml.is_file():
        return None
    project = tomllib.load(zensical_toml.open("rb")).get("project", {})
    nav = project.get("nav")
    if not nav:
        return None
    return root / project.get("docs_dir", "docs"), nav


def _check_nav_completeness(root: Path) -> list[str]:
    """Verify every path zensical.toml's nav references actually exists under docs_dir.

    Neither `zensical build` nor `lychee` catch this: a build with a nav entry pointing
    at a missing file produces no warning, and lychee only checks links *within*
    existing files, never the nav config itself.

    Returns:
        One error string per nav entry pointing at a missing file.

    """
    loaded = _load_nav(root)
    if loaded is None:
        return []
    docs_dir, nav = loaded
    return [
        f"nav entry {rel_path!r} does not exist at {docs_dir / rel_path}"
        for rel_path in _extract_nav_paths(nav)
        if not (docs_dir / rel_path).is_file()
    ]


def _check_docs_in_nav(root: Path) -> list[str]:
    """Verify every markdown file under docs_dir is reachable from zensical.toml's nav.

    The inverse of _check_nav_completeness: catches a doc page that got added but never
    wired into the nav, so it renders but nobody can navigate to it.

    Returns:
        One error string per markdown file missing from the nav.

    """
    loaded = _load_nav(root)
    if loaded is None:
        return []
    docs_dir, nav = loaded
    nav_paths = {Path(p) for p in _extract_nav_paths(nav)}
    return [
        f"{md_file.relative_to(docs_dir)} is not referenced anywhere in the nav"
        for md_file in docs_dir.rglob("*.md")
        if md_file.relative_to(docs_dir) not in nav_paths
    ]


@pytest.mark.parametrize("answers", ANSWER_MATRIX, ids=lambda a: a["id"])
def test_nav_completeness(template_source, tmp_path, answers):
    """Verify zensical.toml's nav and the rendered docs/ tree agree both ways."""
    dest = tmp_path / "out"
    _render(template_source, dest, answers)
    errors = _check_nav_completeness(dest) + _check_docs_in_nav(dest)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert not errors, "\n\n".join(errors)  # noqa: S101


def _entry_tool(entry: str) -> str | None:
    """Extract the tool name from a `mise x -- <tool> ...` prek hook entry.

    Returns:
        The tool name, or None if the entry doesn't follow that pattern (e.g. a hook
        that isn't backed by a mise-managed CLI at all).

    """
    prefix = "mise x -- "
    if not entry.startswith(prefix):
        return None
    return entry[len(prefix) :].split()[0]


def _check_hook_tools_available(prek_toml: Path, mise_toml: Path) -> list[str]:
    """Verify every local prek hook's tool is installed in mise.toml.

    prek.toml.jinja gates each hook behind the same conditions as its tool's entry in
    mise.toml.jinja (e.g. ruff-check/ruff-format and `is_template`, actionlint and
    `is_template or using_github`) specifically so this holds unconditionally for every
    hook that's actually present in a given render -- no need to guess whether a hook
    would find a matching file first. This is exactly the shape of bug that once let
    `actionlint` go missing from mise.toml for an Azure DevOps-hosted Template project.

    Returns:
        One error string per hook whose tool isn't installed.

    """
    if not prek_toml.is_file() or not mise_toml.is_file():
        return []
    prek_config = tomllib.load(prek_toml.open("rb"))
    mise_config = tomllib.load(mise_toml.open("rb"))

    # "aqua:owner/repo" / "pipx:name" / a plain tool name -> the leaf tool identifier,
    # matching what `mise x -- <tool>` actually invokes.
    installed_tools = {
        re.split(r"[:/]", name)[-1] for name in mise_config.get("tools", {})
    }

    errors = []
    for repo in prek_config.get("repos", []):
        if repo.get("repo") != "local":
            continue
        for hook in repo.get("hooks", []):
            tool = _entry_tool(hook.get("entry", ""))
            if tool is not None and tool not in installed_tools:
                errors.append(
                    f"hook {hook['id']!r} needs {tool!r}, which isn't in "
                    "mise.toml's [tools]"
                )
    return errors


@pytest.mark.parametrize("answers", ANSWER_MATRIX, ids=lambda a: a["id"])
def test_hook_tools_available(template_source, tmp_path, answers):
    """Verify every prek hook in the render has its tool installed."""
    dest = tmp_path / "out"
    _render(template_source, dest, answers)
    errors = _check_hook_tools_available(
        dest / ".config" / "prek.toml", dest / "mise.toml"
    )
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert not errors, "\n\n".join(errors)  # noqa: S101


def _task_command_text(task: dict | str) -> str:
    """Flatten one _tasks entry's command into a single searchable string.

    A `command:` value is either a plain string or a list of argv parts (Copier runs
    the latter with shell=False) -- either way, joining into one string is enough for
    substring checks, without needing to know which form a given task uses.

    Returns:
        The command flattened into one space-joined string.

    """
    command = task.get("command", "") if isinstance(task, dict) else task
    return " ".join(command) if isinstance(command, list) else str(command)


def _check_azdo_pipelines_registered(dest: Path) -> list[str]:
    """Verify every .azurepipelines/*.yml file has a matching az pipelines create task.

    copier.yml.jinja hardcodes one explicit `az pipelines create --yml-path
    .azurepipelines/<file>` _tasks entry per pipeline file -- a dynamic loop isn't
    possible in Copier's static _tasks list, so nothing else stops a newly-added
    pipeline file from silently never getting registered.

    Returns:
        One error string per pipeline file missing a matching _tasks entry.

    """
    pipelines_dir = dest / ".azurepipelines"
    copier_yml = dest / "copier.yml"
    if not pipelines_dir.is_dir() or not copier_yml.is_file():
        return []
    pipeline_files = sorted(
        f.name
        for f in pipelines_dir.glob("*.yml")
        if not f.name.startswith("template-")
    )
    data = yaml.safe_load(copier_yml.read_text(encoding="utf-8"))
    task_text = "\n".join(_task_command_text(task) for task in data.get("_tasks", []))
    return [
        f".azurepipelines/{name} has no matching 'az pipelines create --yml-path "
        f".azurepipelines/{name}' entry in _tasks"
        for name in pipeline_files
        if f".azurepipelines/{name}" not in task_text
    ]


@pytest.mark.parametrize("answers", ANSWER_MATRIX, ids=lambda a: a["id"])
def test_azdo_pipelines_registered(template_source, tmp_path, answers):
    """Verify every Azure Pipelines file in the render has a matching _tasks entry."""
    dest = tmp_path / "out"
    _render(template_source, dest, answers)
    errors = _check_azdo_pipelines_registered(dest)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert not errors, "\n\n".join(errors)  # noqa: S101

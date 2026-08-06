"""Checks content/config consistency in the rendered template, not the rendering itself.

Generic by design: every check here operates on whatever actually got rendered, rather
than hardcoding this repo's specific doc set -- see answer_matrix.py for the
repo-specific piece, which a child template should edit alongside its own copier.yml
changes.
"""

from pathlib import Path

import pytest
import tomllib
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

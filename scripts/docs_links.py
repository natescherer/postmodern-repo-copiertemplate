"""Resolve links to this project's own published docs pages.

Reads zensical.toml at runtime instead of hardcoding a URL, since scripts/ is
copied verbatim (not rendered) into every Template-type project, each with its own
docs location.
"""

import tomllib
from pathlib import Path


def _config_path() -> Path | None:
    """Find the project's zensical.toml in the nearest directory above this file.

    That's the parent for a project's scripts/, and the repo root for a template's own
    copy of them, whose parent (template/) has only zensical.toml.jinja.

    Returns:
        The file's path, or None if there's none.

    """
    for directory in Path(__file__).resolve().parents:
        if (directory / "zensical.toml").is_file():
            return directory / "zensical.toml"
    return None


def docs_page_url(page: str, *, version: str = "latest") -> str:
    """Return where docs page `page` is published.

    Args:
        page: The page's path under docs_dir, e.g. "reference/token-permissions.md".
        version: The mike version or alias to link, when the site has one: "latest"
            for the newest release, or "dev" for the docs built from main.

    Returns:
        The hosted URL when zensical.toml sets site_url (versioned via mike); otherwise
        the page's path in the committed site_dir. Falls back to the source path if
        there's no zensical.toml.

    """
    config_path = _config_path()
    if config_path is None:
        return f"docs/{page}"
    with config_path.open("rb") as config_file:
        project = tomllib.load(config_file).get("project", {})
    stem = page.removesuffix(".md")
    if site_url := project.get("site_url"):
        # Directory URLs: "a/b.md" is served at "a/b/", and "a/index.md" at "a/".
        is_index = stem == "index" or stem.endswith("/index")
        path = stem.removesuffix("index") if is_index else f"{stem}/"
        return f"{site_url.rstrip('/')}/{version}/{path}"
    return f"{project.get('site_dir', 'site')}/{stem}.html"

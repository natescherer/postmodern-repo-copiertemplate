"""Resolve links to this project's own published docs pages.

Reads zensical.toml at runtime instead of hardcoding a URL, since scripts/ is
copied verbatim (not rendered) into every Template-type project, each with its own
docs location.
"""

from pathlib import Path

import tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent


def docs_page_url(page: str) -> str:
    """Return where docs page `page` is published.

    Args:
        page: The page's path under docs_dir, e.g. "reference/token-permissions.md".

    Returns:
        The hosted URL when zensical.toml sets site_url (versioned via mike, so
        under its "latest" alias); otherwise the page's path in the committed
        site_dir. Falls back to the source path if there's no zensical.toml.

    """
    config_path = REPO_ROOT / "zensical.toml"
    if not config_path.is_file():
        return f"docs/{page}"
    with config_path.open("rb") as config_file:
        project = tomllib.load(config_file).get("project", {})
    stem = page.removesuffix(".md")
    if site_url := project.get("site_url"):
        # Directory URLs: "a/b.md" is served at "a/b/", and "a/index.md" at "a/".
        is_index = stem == "index" or stem.endswith("/index")
        path = stem.removesuffix("index") if is_index else f"{stem}/"
        return f"{site_url.rstrip('/')}/latest/{path}"
    return f"{project.get('site_dir', 'site')}/{stem}.html"

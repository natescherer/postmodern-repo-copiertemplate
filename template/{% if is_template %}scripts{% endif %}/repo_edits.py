"""File edits the integration test scripts merge into a test repo."""

import re
from pathlib import Path

# An old release of a tool Renovate's mise manager tracks. PR Validation checks only the
# files a PR changes, so pinning it doesn't change what the pin's own PR runs.
OLD_TYPOS = "1.50.3"


def let_renovate_bump_typos(repo: Path) -> None:
    """Lift Renovate's schedule and pin typos to an old release, for Renovate to bump.

    renovate.json otherwise lets Renovate open PRs only in its monthly window, so a run
    at any other time would have nothing to show.

    Raises:
        ValueError: if either file doesn't have the line it expects.

    """
    config = repo / "renovate.json"
    text, count = re.subn(
        r'"\* 0 1 \* \*"', '"at any time"', config.read_text(encoding="utf-8")
    )
    if count != 1:
        raise ValueError("renovate.json has no monthly schedule to lift")
    config.write_text(text, encoding="utf-8", newline="\n")

    tools = repo / "mise.toml"
    text, count = re.subn(
        r'(?m)^"aqua:crate-ci/typos" = "[^"]+"$',
        f'"aqua:crate-ci/typos" = "{OLD_TYPOS}"',
        tools.read_text(encoding="utf-8"),
    )
    if count != 1:
        raise ValueError("mise.toml has no typos pin to change")
    tools.write_text(text, encoding="utf-8", newline="\n")

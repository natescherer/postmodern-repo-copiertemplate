"""Changes the integration test scripts make to their test repos."""

import json
import os
import re
import shutil
import stat
import tempfile
from collections.abc import Callable
from pathlib import Path

from console import run, say

# An old release of a tool Renovate's mise manager tracks. PR Validation checks only the
# files a PR changes, so pinning it doesn't change what the pin's own PR runs.
OLD_TYPOS = "1.50.3"

# Repo B's branch for checking that the Copier Update Check detects a newer release.
OLDER_VERSION_BRANCH = "integration-test/older-recorded-version"


def local_clone_dir(repo_name: str) -> str:
    """Create the empty directory for a test repo's local clone, named after the repo.

    The name already carries the run's timestamp, so it's unique.

    Returns:
        `<temp directory>/<repo_name>`.

    """
    path = Path(tempfile.gettempdir(), repo_name)
    path.mkdir()
    return str(path)


# How older runs named clones: tempfile.mkdtemp(prefix="integration-test-").
_OLDER_CLONE_NAME = re.compile(r"integration-test-[a-z0-9_]{8}")


def local_clones(repo_name: re.Pattern[str], host: str) -> list[Path]:
    """Find the test repos' local clones for one platform in the temp directory.

    Both platforms name their repos alike, so a clone counts only if its origin is on
    `host`, or if it has no origin, which a run that stopped before pushing leaves.

    Returns:
        Each clone named after a test repo, or as older runs named them.

    """
    clones = []
    for path in Path(tempfile.gettempdir()).iterdir():
        named = repo_name.fullmatch(path.name) or _OLDER_CLONE_NAME.fullmatch(path.name)
        if not named or not path.is_dir():
            continue
        config = path / ".git" / "config"
        origin = config.read_text(encoding="utf-8") if config.is_file() else ""
        if host in origin or "url = " not in origin:
            clones.append(path)
    return sorted(clones)


def repo_b_clone(
    repo_prefix: str, host: str, local_path: str | None
) -> tuple[str, str]:
    """Find the Repo B clone to verify, and its origin URL.

    `--verify-update` uses it when you don't name Repo B, so verifying the newest run
    needs no arguments: its clone's origin names the repo. A run's repos carry its
    timestamp, so the newest clone is the highest one.

    Returns:
        The clone's path (`local_path`, or the newest Repo B clone on `host`), and its
        origin URL.

    Raises:
        SystemExit: if `local_path` has no origin on `host`, or there's no Repo B clone.

    """
    if local_path:
        clones = [Path(local_path)]
    else:
        pattern = re.compile(rf"{re.escape(repo_prefix)}-integration-test-(\d+)-b")
        clones = sorted(
            (c for c in local_clones(pattern, host) if pattern.fullmatch(c.name)),
            key=lambda c: int(pattern.fullmatch(c.name).group(1)),
            reverse=True,
        )
    for clone in clones:
        origin = run(
            "git",
            "remote",
            "get-url",
            "origin",
            cwd=str(clone),
            check=False,
            capture=True,
            echo=False,
        ).stdout.strip()
        if host in origin:
            return str(clone), origin
    if local_path:
        raise SystemExit(f"{local_path} has no origin on {host}.")
    raise SystemExit(
        f"No Repo B clone in {tempfile.gettempdir()}. Start a run first, or pass "
        "Repo B's --repo and --local-path."
    )


def remove_tree(path: Path) -> None:
    """Delete a directory tree, including a git clone's read-only files on Windows."""

    def clear_read_only(function: Callable, target: str, _error: BaseException) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(path, onexc=clear_read_only)


def remove_clones(clones: list[Path]) -> int:
    """Delete local clones, carrying on past any that can't be deleted.

    It skips the clone the current directory is in, whose files this run itself has
    open (its log, for one), and reports any other it can't delete, such as one an
    editor or terminal has open.

    Returns:
        How many it deleted.

    """
    here = Path.cwd().resolve()
    deleted = 0
    for clone in clones:
        if here.is_relative_to(clone.resolve()):
            say(
                f"Skipped {clone}: it's the current directory. Rerun cleanup from "
                "elsewhere."
            )
            continue
        try:
            remove_tree(clone)
        except OSError as error:
            say(
                f"Couldn't delete {clone}: {error.strerror}. Close whatever has it "
                "open, then rerun cleanup."
            )
        else:
            deleted += 1
    return deleted


def let_renovate_bump_typos(repo: Path) -> None:
    """Pin typos to an old release, and let Renovate bump it, and only it, at any time.

    renovate.json otherwise lets Renovate open PRs only in its monthly window, so a run
    at any other time would have nothing to show. Lifting the window for every
    dependency would open a PR for each one that has moved on, whose PR Validation runs
    then hold up the run's own PRs.

    Raises:
        ValueError: if mise.toml has no typos pin to change.

    """
    config_path = repo / "renovate.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["schedule"] = ["at any time"]
    config["packageRules"] = [
        *config.get("packageRules", []),
        {"matchPackageNames": ["/.*/"], "enabled": False},
        {"matchDepNames": ["aqua:crate-ci/typos"], "enabled": True},
    ]
    config_path.write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    tools = repo / "mise.toml"
    text, count = re.subn(
        r'(?m)^"aqua:crate-ci/typos" = "[^"]+"$',
        f'"aqua:crate-ci/typos" = "{OLD_TYPOS}"',
        tools.read_text(encoding="utf-8"),
    )
    if count != 1:
        raise ValueError("mise.toml has no typos pin to change")
    tools.write_text(text, encoding="utf-8", newline="\n")


def skip_template_docs_links(repo: Path, docs_root: str) -> None:
    """Have lychee skip links into the template's published docs.

    The template under test publishes its docs when it releases, so before then a link
    to one of its new pages 404s. The template's render tests check those links
    against its docs source instead.

    Raises:
        ValueError: if .config/lychee.toml has no `exclude` list.

    """
    config = repo / ".config" / "lychee.toml"
    entry = f"  '^{re.escape(docs_root)}', # The template under test, unpublished\n"
    text, count = re.subn(
        r"(?m)^exclude = \[\n",
        lambda match: match.group(0) + entry,
        config.read_text(encoding="utf-8"),
    )
    if count != 1:
        raise ValueError(".config/lychee.toml has no exclude list")
    config.write_text(text, encoding="utf-8", newline="\n")


# A minimal Cobertura report, covering the first line of README.md, which every project
# has. A fresh project has no tests that write one, so PR Validation's coverage step
# would have nothing to publish.
COVERAGE_FIXTURE = """<?xml version="1.0" ?>
<coverage version="1" timestamp="0" lines-valid="1" lines-covered="1" line-rate="1"
          branches-valid="0" branches-covered="0" branch-rate="0" complexity="0">
  <sources>
    <source>.</source>
  </sources>
  <packages>
    <package name="integration-test" line-rate="1" branch-rate="0" complexity="0">
      <classes>
        <class name="README" filename="README.md" line-rate="1" branch-rate="0"
               complexity="0">
          <methods/>
          <lines>
            <line number="1" hits="1"/>
          </lines>
        </class>
      </classes>
    </package>
  </packages>
</coverage>
"""


def add_coverage_fixture(repo: Path) -> None:
    """Commit a coverage.xml for PR Validation's coverage step to publish."""
    (repo / "coverage.xml").write_text(COVERAGE_FIXTURE, encoding="utf-8", newline="\n")


def template_docs_root(source: str) -> str | None:
    """Return where a GitHub-hosted template publishes its docs, as docs_base() does.

    Returns:
        `https://<owner>.github.io/<repo>/` for a github.com source, else None: a
        template elsewhere links its docs inside its own repo, which needs no release.

    """
    match = re.match(r"^gh:([^/\s]+)/([^/\s]+)$", source) or re.search(
        r"github\.com[:/]+([^/\s]+)/([^/\s.]+)", source
    )
    return f"https://{match[1]}.github.io/{match[2]}/" if match else None


def prepare_repo_a(source: str) -> Callable[[Path], None]:
    """Return the edit that sets Repo A up for the run's checks.

    Returns:
        A function that applies let_renovate_bump_typos(), add_coverage_fixture(),
        and, for a template that publishes its docs, skip_template_docs_links().

    """
    docs_root = template_docs_root(source)

    def edit(repo: Path) -> None:
        let_renovate_bump_typos(repo)
        add_coverage_fixture(repo)
        if docs_root:
            skip_template_docs_links(repo, docs_root)

    return edit


def prepare_repo_b(source: str) -> Callable[[Path], None] | None:
    """Return the edit that sets Repo B up for its update by hand, if it needs one.

    The update brings in links to the template's new docs pages, which the link check
    would reject until the template releases.

    Returns:
        A function that applies skip_template_docs_links(), or None for a template
        that doesn't publish its docs.

    """
    docs_root = template_docs_root(source)
    if not docs_root:
        return None
    return lambda repo: skip_template_docs_links(repo, docs_root)


def push_older_recorded_version(dest: str, source: str, tag: str) -> str:
    """Push a branch whose answers file records the commit just before `tag`.

    Copier reads a project's current version by running `git describe` on the
    template at the recorded commit, so on this branch the Copier Update Check finds
    `tag` newer: `<tag>~1` reads as the release before `tag` plus some commits, or as
    0.0.0 plus some commits if `tag` is the first release. Nothing at that commit is
    rendered.

    Returns:
        The branch's name.

    Raises:
        ValueError: if the answers file has no `_commit` line.

    """
    with tempfile.TemporaryDirectory() as clone:
        run(
            "git",
            "clone",
            "--quiet",
            "--filter=blob:none",
            "--no-checkout",
            source,
            clone,
        )
        commit = run(
            "git", "-C", clone, "rev-parse", f"{tag}~1", capture=True
        ).stdout.strip()
    answers = Path(dest, ".config", "copier-answers.yml")
    text, count = re.subn(
        r"(?m)^_commit: .*$", f"_commit: {commit}", answers.read_text(encoding="utf-8")
    )
    if count != 1:
        raise ValueError("the answers file has no _commit line")
    run("git", "switch", "-c", OLDER_VERSION_BRANCH, cwd=dest)
    answers.write_text(text, encoding="utf-8", newline="\n")
    run(
        "git",
        "commit",
        "-am",
        f"chore: record {tag}~1 as the template version",
        cwd=dest,
    )
    run("git", "push", "-u", "origin", OLDER_VERSION_BRANCH, cwd=dest)
    run("git", "switch", "main", cwd=dest)
    return OLDER_VERSION_BRANCH

"""Create two throwaway repos from this template and verify them.

Run via `mise run integration-test-gh` -- a human's own gh/GCM session, both repos
left in place afterward for inspection (delete them yourself when you're done). Not
templated itself; the caller passes this repo's own source URL and name as arguments,
so there's nothing here for Jinja to render.

Always runs against HEAD -- this is meant to verify a release candidate on main is
good before cutting a release, not to smoke-test an arbitrary branch. Covers both
scenarios every run: a plain `copier copy`, and a separate repo copied at the last
stable tag then updated to HEAD -- the only way to catch a bug gated on
`_copier_operation == 'update'` against a real remote, not just a local render (see
tests/test_render.py's `test_update_from_last_tag` for the render-only equivalent).
"""

import argparse
import json
import re
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tempfile
import time

# Default `gh auth login` scopes cover both -- see docs/token-permissions.md.
REQUIRED_SCOPES = ("repo", "workflow")

# Must match _tasks' project_description -d flag in create() below.
PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match .github/settings.yml.jinja's `labels:` list, sorted.
EXPECTED_LABELS = (
    "accessibility,awaiting pr,blocked,bug,documentation,duplicate,"
    "enhancement,good first issue,help wanted,invalid,question,wontfix"
)


def run(
    *args: str, check: bool = True, capture: bool = False, cwd: str | None = None
) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first.

    Resolves argv[0] via shutil.which() first: some CLIs (e.g. Azure CLI's `az`) are
    `.cmd` batch wrappers on Windows rather than real .exe files, and subprocess with
    shell=False (unlike cmd.exe's own PATH resolution) won't find those from the bare
    name alone, failing with `FileNotFoundError: [WinError 2]`. which() finds the
    actual resolvable path on any platform, sidestepping that gap without needing
    shell=True. gh/copier don't hit this today, but there's no downside to guarding
    every invocation here the same way.

    Returns:
        The completed process, with captured stdout/stderr if `capture` is True.

    """
    print(f"$ {' '.join(args)}" + (f"  (in {cwd})" if cwd else ""))
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        resolved, check=check, text=True, capture_output=capture, cwd=cwd
    )


def gh_value(*args: str) -> str:
    """Run `gh <args>` and return its trimmed stdout.

    Returns:
        The command's stdout, stripped of surrounding whitespace.

    """
    return run("gh", *args, capture=True).stdout.strip()


def check_gh_installed() -> None:
    """Verify the `gh` CLI is actually resolvable on PATH.

    Without this, a missing `gh` surfaces as a raw FileNotFoundError traceback from
    deep inside the first real `gh` call instead of a clear message up front.

    Raises:
        SystemExit: if `gh` can't be found.

    """
    if shutil.which("gh") is None:
        raise SystemExit(
            "GitHub CLI ('gh') not found on PATH. Install it: https://cli.github.com"
        )


def check_scopes() -> None:
    """Verify the active gh token has every scope this script needs.

    `gh auth status` reports a classic token's granted scopes (sourced from GitHub's
    own X-OAuth-Scopes API response) as a human-readable "Token scopes: 'a', 'b'" line
    -- there's no dedicated --json field for this, so this greps that line instead of
    querying the API directly a second time.

    Raises:
        SystemExit: if any of REQUIRED_SCOPES is missing.

    """
    status = run("gh", "auth", "status", check=False, capture=True)
    output = status.stdout + status.stderr
    missing = [scope for scope in REQUIRED_SCOPES if f"'{scope}'" not in output]
    if missing:
        raise SystemExit(
            f"Token is missing required scope(s): {', '.join(missing)}. See "
            "docs/token-permissions.md for what this token needs."
        )


def create(source: str, vcs_ref: str, repo_name: str, dest: str, owner: str) -> None:
    """Render+run the template to create the test repo.

    `github_username` is pinned to the already-resolved `owner` rather than left to
    auto-detect from local git config: copier.yml.jinja's `.github/settings.yml`
    content (e.g. `homepage`) is templated from `github_repo_owner`, which defaults to
    `github_username` -- letting that auto-detect could silently diverge from the
    account gh actually authenticated as, breaking verify() for reasons unrelated to
    what it's actually trying to test.

    `--defaults` falls back to each question's own default for anything not covered
    by an explicit -d below (currently github_org, author_name, zensical_target) --
    without it, copier drops into an interactive prompt for those. Explicit -d values
    below still take priority over --defaults regardless of order.
    """
    run(
        "copier",
        "copy",
        "--trust",
        "--defaults",
        f"--vcs-ref={vcs_ref}",
        "-d",
        f"repo_name={repo_name}",
        "-d",
        "repo_setup_actions=Create Repo",
        "-d",
        "developer_platform=GitHub",
        "-d",
        f"github_username={owner}",
        "-d",
        f"project_description={PROJECT_DESCRIPTION}",
        "-d",
        "project_type=Template",
        "-d",
        "project_name=Integration Test",
        "-d",
        "project_visibility=Public",
        "-d",
        "license=MIT",
        "-d",
        "lifecycle=Pre-Alpha",
        source,
        dest,
    )


def latest_stable_tag(source: str) -> str:
    """Find this template's most recent stable (non-prerelease) release tag.

    Uses `git ls-remote --tags` so it works directly against `source` without a local
    clone. Matches strict `vX.Y.Z` tags only (excluding prereleases like
    `v1.1.0-alpha.0`) and sorts by parsed version, not lexically -- a plain string
    sort would put `v0.7.9` after `v0.7.20`.

    Returns:
        The latest matching tag name, e.g. "v0.7.20".

    Raises:
        SystemExit: if no matching tag is found.

    """
    result = run("git", "ls-remote", "--tags", source, capture=True)
    versions = []
    for line in result.stdout.splitlines():
        match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", line.rsplit("refs/tags/", 1)[-1])
        if match:
            versions.append(tuple(int(g) for g in match.groups()))
    if not versions:
        raise SystemExit(f"No stable (vX.Y.Z) tags found at {source!r}")
    return "v" + ".".join(map(str, max(versions)))


def run_update(dest: str, new_ref: str) -> bool:
    """Update the throwaway repo in `dest` to `new_ref`.

    Deliberately not `--skip-tasks`: unlike the repo-creation/pipeline-registration
    _tasks (gated `_copier_operation == 'copy'`), the copy-template-files task that
    keeps a Template project's own template/ in sync with its parent isn't gated that
    way -- it's meant to run on update too, so this exercises that path for real.

    Returns:
        Whether the update produced any local changes to commit.

    """
    run(
        "copier",
        "update",
        "--trust",
        "--defaults",
        f"--vcs-ref={new_ref}",
        "-a",
        ".config/copier-answers.yml",
        cwd=dest,
    )
    status = run("git", "status", "--porcelain", capture=True, cwd=dest)
    return bool(status.stdout.strip())


def commit_and_push(dest: str) -> None:
    """Commit and push whatever `copier update` just changed in `dest`."""
    run("git", "add", "-A", cwd=dest)
    run("git", "commit", "-m", "chore: copier update", cwd=dest)
    run("git", "push", cwd=dest)


def settings_synced(repo: str, homepage: str) -> bool:
    """Check whether the Settings App has applied every part of .github/settings.yml.

    Covers the `repository`, `labels`, `rulesets`, and `environments` blocks -- every
    top-level key that file actually sets, not just a sample of them.

    Returns:
        True once every expected field/label/ruleset/environment is present.

    """
    repo_data_result = run("gh", "api", f"repos/{repo}", check=False, capture=True)
    if repo_data_result.returncode != 0:
        return False
    repo_data = json.loads(repo_data_result.stdout)
    if repo_data.get("description") != PROJECT_DESCRIPTION:
        return False
    if repo_data.get("homepage") != homepage:
        return False
    # allow_auto_merge isn't checked here: settings.yml.jinja only sets it when
    # zensical_repo is true, and this test always renders with the default
    # zensical_target (GitHub Pages), so it's never declared for this specific repo.
    if repo_data.get("delete_branch_on_merge") is not True:
        return False

    labels = run(
        "gh",
        "api",
        f"repos/{repo}/labels",
        "--jq",
        '[.[].name] | sort | join(",")',
        check=False,
        capture=True,
    )
    if labels.returncode != 0 or labels.stdout.strip() != EXPECTED_LABELS:
        return False

    rulesets = run(
        "gh",
        "api",
        f"repos/{repo}/rulesets",
        "--jq",
        ".[].name",
        check=False,
        capture=True,
    )
    if (
        rulesets.returncode != 0
        or "default-branch-protection" not in rulesets.stdout.split()
    ):
        return False

    # {"total_count": N, "environments": [...]} -- unlike labels/rulesets above, this
    # list endpoint wraps its array rather than returning it bare.
    environments = run(
        "gh",
        "api",
        f"repos/{repo}/environments",
        "--jq",
        "[.environments[].name]",
        check=False,
        capture=True,
    )
    return environments.returncode == 0 and "github-pages" in json.loads(
        environments.stdout or "[]"
    )


def verify(repo: str, homepage: str) -> None:
    """Assert the created repo's real remote state matches what repo setup should do.

    Raises:
        SystemExit: if any check fails or the Settings App never syncs in time.

    """
    print(f"Verifying {repo}...")
    visibility = gh_value(
        "repo", "view", repo, "--json", "visibility", "-q", ".visibility"
    )
    if visibility != "PUBLIC":
        raise SystemExit(f"Expected PUBLIC visibility, got {visibility!r}")

    pages_build_type = gh_value("api", f"repos/{repo}/pages", "-q", ".build_type")
    if pages_build_type != "workflow":
        raise SystemExit(
            f"Expected Pages build_type=workflow, got {pages_build_type!r}"
        )

    run("gh", "api", f"repos/{repo}/contents/.github/workflows", capture=True)

    # Labels and the branch ruleset come from .github/settings.yml, applied
    # asynchronously by the Settings GitHub App (https://github.com/apps/settings)
    # reacting to the push above -- not something this script sets directly, so this
    # polls rather than checking once. Requires that app be installed on the
    # authenticated account with access to all repositories (a new repo isn't
    # automatically visible to an app installed on "only select repositories") -- see
    # docs/token-permissions.md.
    for attempt in range(12):
        if settings_synced(repo, homepage):
            print(f"Settings App sync: OK (after {attempt * 10}s)")
            break
        if attempt == 11:
            raise SystemExit(
                "Settings App sync: not observed within 120s -- is it installed on "
                "this account with access to all repositories?"
            )
        time.sleep(10)
    print("All checks passed.")


def homepage_for(owner: str, repo_name: str) -> str:
    """Compute the GitHub Pages homepage verify() expects for a repo this script made.

    Returns:
        The homepage URL. project_visibility is always Public below, matching
        settings.yml.jinja's homepage logic (only set when is_public).

    """
    return f"https://{owner}.github.io/{repo_name}"


def main() -> None:
    """Create and verify two throwaway repos: a fresh copy, and an updated one.

    Both scenarios run every time, each against its own brand-new repo, always at
    HEAD (this tool exists to verify a release candidate on main is good before
    cutting a release, not to smoke-test an arbitrary branch): a plain `copier copy`,
    and a separate repo copied at the last stable tag then updated to HEAD -- the only
    way to catch a bug gated on `_copier_operation == 'update'` against a real remote,
    not just a local render (see tests/test_render.py's `test_update_from_last_tag`
    for the render-only equivalent). Both repos are left in place afterward for
    inspection.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Copier template source URL")
    parser.add_argument("--repo-prefix", required=True, help="This repo's own name")
    args = parser.parse_args()

    check_gh_installed()
    check_scopes()

    owner = gh_value("api", "user", "--jq", ".login")
    timestamp = int(time.time())

    print("=== Fresh copy at HEAD ===")
    fresh_repo_name = f"{args.repo_prefix}-integration-test-{timestamp}-fresh"
    fresh_dest = tempfile.mkdtemp(prefix="integration-test-")
    fresh_repo = f"{owner}/{fresh_repo_name}"
    create(args.source, "HEAD", fresh_repo_name, fresh_dest, owner)
    verify(fresh_repo, homepage_for(owner, fresh_repo_name))

    old_ref = latest_stable_tag(args.source)
    print(f"=== Update path: {old_ref} -> HEAD ===")
    update_repo_name = f"{args.repo_prefix}-integration-test-{timestamp}-update"
    update_dest = tempfile.mkdtemp(prefix="integration-test-")
    update_repo = f"{owner}/{update_repo_name}"
    update_homepage = homepage_for(owner, update_repo_name)
    create(args.source, old_ref, update_repo_name, update_dest, owner)
    verify(update_repo, update_homepage)
    if run_update(update_dest, "HEAD"):
        commit_and_push(update_dest)
        verify(update_repo, update_homepage)
    else:
        print("copier update produced no changes -- nothing to re-verify.")

    print(
        f"Leaving {fresh_repo} ({fresh_dest}) and {update_repo} ({update_dest}) in "
        "place -- delete them yourself when you're done."
    )


if __name__ == "__main__":
    sys.exit(main())

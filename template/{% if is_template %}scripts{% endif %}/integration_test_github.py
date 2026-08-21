"""Create a throwaway repo from this template, verify it, then optionally clean it up.

Shared by `mise run integration-test-gh` (a human's own gh/GCM session, repo left in
place by default so it can be inspected) and maint-integration_test.yml
(INTEGRATION_TEST_PAT, always passes --cleanup) -- not templated itself; both callers
pass this repo's own source URL and name as arguments, so there's nothing here for
Jinja to render.
"""

import argparse
import json

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tempfile
import time

# Must match docs/token_permissions.md's Integration Test PAT scope table.
REQUIRED_SCOPES = ("repo", "workflow", "delete_repo")

# Must match _tasks' project_description -d flag in create() below.
PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"


def run(
    *args: str, check: bool = True, capture: bool = False
) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first.

    Returns:
        The completed process, with captured stdout/stderr if `capture` is True.

    """
    print(f"$ {' '.join(args)}")
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        args, check=check, text=True, capture_output=capture
    )


def gh_value(*args: str) -> str:
    """Run `gh <args>` and return its trimmed stdout.

    Returns:
        The command's stdout, stripped of surrounding whitespace.

    """
    return run("gh", *args, capture=True).stdout.strip()


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
            "docs/token_permissions.md for what this token needs."
        )


def create(
    source: str, vcs_ref: str, repo_name: str, dest: str, owner: str, *, ci: bool
) -> None:
    """Render+run the template to create the test repo.

    `gh auth setup-git` is only run when `ci` is set -- it reconfigures git's *global*
    credential helper to route through gh, a real side effect on a human's own machine
    that a local run shouldn't impose. In CI it's required instead, since headless
    runners can't complete Git Credential Manager's interactive login (the human-run
    path this template's own _tasks otherwise rely on).

    `github_username` is pinned to the already-resolved `owner` rather than left to
    auto-detect from local git config: copier.yml.jinja's `.github/settings.yml`
    content (e.g. `homepage`) is templated from `github_repo_owner`, which defaults to
    `github_username` -- letting that auto-detect could silently diverge from the
    account gh actually authenticated as (especially in CI, where git config may have
    no user.email at all), breaking verify() for reasons unrelated to what it's
    actually trying to test.
    """
    if ci:
        run("gh", "auth", "setup-git")
    run(
        "copier",
        "copy",
        "--trust",
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
    if repo_data.get("allow_auto_merge") is not True:
        return False
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
    if labels.returncode != 0 or labels.stdout.strip() != "awaiting pr,blocked":
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

    workflow_perms = gh_value(
        "api",
        f"repos/{repo}/actions/permissions/workflow",
        "-q",
        ".can_approve_pull_request_reviews",
    )
    if workflow_perms != "true":
        raise SystemExit(
            f"Expected can_approve_pull_request_reviews=true, got {workflow_perms!r}"
        )

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
    # docs/token_permissions.md.
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


def cleanup(repo: str) -> None:
    """Delete the test repo."""
    run("gh", "repo", "delete", repo, "--yes")


def main() -> None:
    """Parse args, then create, verify, and (if requested) clean up a test repo."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Copier template source URL")
    parser.add_argument("--vcs-ref", default="HEAD")
    parser.add_argument("--repo-prefix", required=True, help="This repo's own name")
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Delete the repo when done (always used in CI)",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help=(
            "Reconfigure git's global credential helper via 'gh auth setup-git' "
            "(always used in CI; skipped locally since it would alter a human's own "
            "git config as a side effect)"
        ),
    )
    args = parser.parse_args()

    check_scopes()

    owner = gh_value("api", "user", "--jq", ".login")
    repo_name = f"{args.repo_prefix}-integration-test-{int(time.time())}"
    dest = tempfile.mkdtemp(prefix="integration-test-")
    repo = f"{owner}/{repo_name}"
    # project_visibility is always Public below, matching settings.yml.jinja's
    # homepage logic (only set when is_public).
    homepage = f"https://{owner}.github.io/{repo_name}"

    try:
        create(args.source, args.vcs_ref, repo_name, dest, owner, ci=args.ci)
        verify(repo, homepage)
    finally:
        if args.cleanup:
            cleanup(repo)
        else:
            print(
                f"Leaving {repo} in place ({dest}) -- pass --cleanup to delete "
                "it automatically."
            )


if __name__ == "__main__":
    sys.exit(main())

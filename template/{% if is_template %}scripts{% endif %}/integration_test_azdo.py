"""Create a throwaway repo from this template, verify it, then optionally clean it up.

Azure DevOps counterpart to integration_test_github.py -- see that file for the shared
shape (create/verify/cleanup, --cleanup/--ci flags). Diverges in a few real ways:

- No Settings App equivalent here, so nothing to poll for asynchronously.
- `az` has no scope-introspection command the way `gh auth status` does, so this does
  a basic access check (can the token see the target project at all) instead of
  asserting specific scopes.
- There's no az-native bridge from an authenticated session into git push credentials
  -- `az login`'s Entra session doesn't carry over to git the way `gh auth setup-git`
  does for GitHub. CI push auth here instead uses a PAT-based Basic-Auth header scoped
  to dev.azure.com specifically (Microsoft's own documented pattern for scripted git
  operations against Azure Repos: https://learn.microsoft.com/azure/devops/repos/git/auth-overview),
  not a stored credential helper.
- Repo and pipeline deletion both need az-resolved IDs, not just names, and pipeline
  definitions aren't confirmed to be cleaned up automatically when their repo is
  deleted, so this deletes them explicitly first rather than assuming they cascade.
"""

import argparse
import base64
import json
import os
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tempfile
import time

PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match the AZDO_INTEGRATION_TEST_ORG/AZDO_INTEGRATION_TEST_PROJECT placeholder
# values in test-auto-integration_test.yml's integration-test-azdo job -- there's no way
# to auto-detect which org/project a GitHub-hosted workflow should test against.
PLACEHOLDER = "CHANGE_ME"

# Must match template/{% if is_template %}copier.yml{% endif %}.jinja's hardcoded
# `az pipelines create --name "[<repo_name>] <name>"` _tasks entries. "Test (Auto):
# Integration Test" only registers because create() below passes
# integration_test_scheduled=true.
PIPELINE_DISPLAY_NAMES = (
    "Maint (Auto): Copier Update Check",
    "Docs (Auto): Zensical Build & Publish",
    "Test (Auto): PR Validation",
    "Release (Auto): Prepare/Publish Release",
    "Maint (Auto): Renovate",
    "Test (Auto): Integration Test",
)


def run(
    *args: str, check: bool = True, capture: bool = False
) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first.

    Resolves argv[0] via shutil.which() first: on Windows, `az` is an `az.cmd` batch
    wrapper rather than a real .exe, and subprocess with shell=False (unlike cmd.exe's
    own PATH resolution) won't find it from the bare name alone, failing with
    `FileNotFoundError: [WinError 2]`. which() finds the actual resolvable path on any
    platform, sidestepping that gap without needing shell=True.

    Returns:
        The completed process, with captured stdout/stderr if `capture` is True.

    """
    print(f"$ {' '.join(args)}")
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        resolved, check=check, text=True, capture_output=capture
    )


def az_value(*args: str) -> str:
    """Run `az <args>` and return its trimmed stdout.

    Returns:
        The command's stdout, stripped of surrounding whitespace.

    """
    return run("az", *args, capture=True).stdout.strip()


def check_az_installed() -> None:
    """Verify the `az` CLI is actually resolvable on PATH.

    Without this, a missing `az` surfaces as a raw FileNotFoundError traceback from
    deep inside the first real `az` call instead of a clear message up front.

    Raises:
        SystemExit: if `az` can't be found.

    """
    if shutil.which("az") is None:
        raise SystemExit(
            "Azure CLI ('az') not found on PATH. Install it: "
            "https://learn.microsoft.com/cli/azure/install-azure-cli"
        )


def check_azure_devops_extension() -> None:
    """Verify the azure-devops CLI extension is installed.

    `az devops`/`az repos`/`az pipelines` commands, if the extension isn't installed,
    prompt interactively to install it ("Do you want to install it now? (Y/n):") --
    which just hangs forever with no stdin attached (e.g. under `mise run` or in CI).
    Checking via `az extension list` first (a core command that doesn't itself need
    the extension) avoids ever triggering that prompt.

    Raises:
        SystemExit: if the extension isn't installed.

    """
    installed = az_value(
        "extension", "list", "--query", "[?name=='azure-devops'].name", "-o", "tsv"
    )
    if not installed:
        raise SystemExit(
            "Azure CLI extension 'azure-devops' is not installed. Install it: "
            "az extension add --name azure-devops"
        )


def check_access(org_url: str, project: str) -> None:
    """Verify the active az session can actually see the target project.

    Not a scope check (az has no equivalent to `gh auth status`'s scope list) -- just
    confirms the token/session is valid and has at least read access, so a bad
    AZURE_DEVOPS_EXT_PAT fails here with a clear message instead of deep inside
    `copier copy`.

    Raises:
        SystemExit: if the project isn't visible with the current credentials.

    """
    result = run(
        "az",
        "devops",
        "project",
        "show",
        "--org",
        org_url,
        "--project",
        project,
        check=False,
        capture=True,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"Can't see project {project!r} at {org_url} with the current az "
            "session. See docs/token_permissions.md for what this token needs."
        )


def configure_git_push_auth() -> None:
    """Scope a PAT-based Basic-Auth header to dev.azure.com for non-interactive push.

    See module docstring for why this is needed instead of a credential helper.
    """
    token = os.environ["AZURE_DEVOPS_EXT_PAT"]
    header = "Authorization: Basic " + base64.b64encode(f":{token}".encode()).decode()
    run(
        "git",
        "config",
        "--global",
        "http.https://dev.azure.com/.extraheader",
        header,
    )


def create(
    source: str,
    vcs_ref: str,
    repo_name: str,
    dest: str,
    org: str,
    project: str,
    *,
    ci: bool,
) -> None:
    """Render+run the template to create the test repo and register its pipelines.

    `--defaults` falls back to each question's own default for anything not covered
    by an explicit -d below (currently author_name, zensical_target) -- without it,
    copier drops into an interactive prompt for those, which just hangs in CI and
    adds unnecessary keypresses locally. Explicit -d values below still take priority
    over --defaults regardless of order.
    """
    if ci:
        configure_git_push_auth()
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
        "developer_platform=Azure DevOps",
        "-d",
        f"azdo_org={org}",
        "-d",
        f"azdo_project={project}",
        "-d",
        f"project_description={PROJECT_DESCRIPTION}",
        "-d",
        "project_type=Template",
        "-d",
        "integration_test_scheduled=true",
        "-d",
        "project_name=Integration Test",
        "-d",
        "project_visibility=Private",
        "-d",
        "license=None",
        "-d",
        "lifecycle=Pre-Alpha",
        source,
        dest,
    )


def check_pr_validation_policy(
    repo_id: str, pipelines: list[dict], org_url: str, project: str, repo_name: str
) -> None:
    """Assert the PR-validation build-validation policy was actually applied.

    Only checks the policy configuration itself (existence, blocking, enabled, and
    that it targets the pr_validation pipeline) -- not the Project Administrators
    bypass-permission grant alongside it. `az devops security permission`'s JSON
    output shape isn't documented clearly enough (no example response in Microsoft's
    own docs) to assert against confidently without a live org to verify against, so
    that half is left unverified here rather than risk a check that's confidently
    wrong in either direction.

    Raises:
        SystemExit: if no matching, enabled, blocking policy is found.

    """
    pr_validation_id = next(
        (
            p["id"]
            for p in pipelines
            if p["name"] == f"[{repo_name}] Test (Auto): PR Validation"
        ),
        None,
    )
    if pr_validation_id is None:
        raise SystemExit(
            "Can't check the PR-validation policy: pr_validation pipeline not found"
        )

    policies = json.loads(
        az_value(
            "repos",
            "policy",
            "list",
            "--repository-id",
            repo_id,
            "--branch",
            "main",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "[]"
    )
    build_policies = [
        p for p in policies if p.get("type", {}).get("displayName") == "Build"
    ]
    matching = [
        p
        for p in build_policies
        if p.get("settings", {}).get("buildDefinitionId") == pr_validation_id
    ]
    if not matching:
        raise SystemExit(
            "No build-validation policy on 'main' targets the pr_validation pipeline"
        )
    policy = matching[0]
    if not policy.get("isBlocking") or not policy.get("isEnabled"):
        raise SystemExit(
            f"Build-validation policy {policy.get('id')} exists but isn't both "
            "blocking and enabled"
        )


def verify(repo_name: str, org_url: str, project: str) -> None:
    """Assert the created repo, its pipelines, and its PR-validation policy exist.

    Raises:
        SystemExit: if the repo, any expected pipeline, or the policy is missing.

    """
    print(f"Verifying {org_url}{project}/{repo_name}...")
    repo_id = az_value(
        "repos",
        "show",
        "--repository",
        repo_name,
        "--org",
        org_url,
        "--project",
        project,
        "--query",
        "id",
        "-o",
        "tsv",
    )
    if not repo_id:
        raise SystemExit(f"Repo {repo_name!r} not found")

    pipelines = json.loads(
        az_value(
            "pipelines",
            "list",
            "--org",
            org_url,
            "--project",
            project,
            "--repository",
            repo_name,
            "--query",
            "[].{id: id, name: name}",
        )
        or "[]"
    )
    pipeline_names = {p["name"] for p in pipelines}
    expected = {f"[{repo_name}] {name}" for name in PIPELINE_DISPLAY_NAMES}
    missing = expected - pipeline_names
    if missing:
        raise SystemExit(f"Missing pipeline(s): {', '.join(sorted(missing))}")

    check_pr_validation_policy(repo_id, pipelines, org_url, project, repo_name)
    print("All checks passed.")


def cleanup(repo_name: str, org_url: str, project: str) -> None:
    """Delete the test repo's pipelines, then the repo itself.

    Pipeline definitions aren't confirmed to be cleaned up automatically when their
    repo is deleted, so this deletes them explicitly first rather than assume so.
    """
    pipeline_ids = json.loads(
        az_value(
            "pipelines",
            "list",
            "--org",
            org_url,
            "--project",
            project,
            "--repository",
            repo_name,
            "--query",
            "[].id",
        )
        or "[]"
    )
    for pipeline_id in pipeline_ids:
        run(
            "az",
            "pipelines",
            "delete",
            "--id",
            str(pipeline_id),
            "--org",
            org_url,
            "--project",
            project,
            "--yes",
            check=False,
        )

    repo_id = az_value(
        "repos",
        "show",
        "--repository",
        repo_name,
        "--org",
        org_url,
        "--project",
        project,
        "--query",
        "id",
        "-o",
        "tsv",
    )
    if repo_id:
        run(
            "az",
            "repos",
            "delete",
            "--id",
            repo_id,
            "--org",
            org_url,
            "--project",
            project,
            "--yes",
        )


def main() -> None:
    """Parse args, then create, verify, and (if requested) clean up a test repo.

    Raises:
        SystemExit: if `az` or its azure-devops extension aren't installed, or
            --org/--project are missing or left at their placeholder value.

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Copier template source URL")
    # usage_branch/usage_org/usage_project are set when this runs via `mise run
    # integration-test-azdo`, whose `usage` field defines matching flags (mise's own
    # arg-parsing, not this one) -- mise passes them through as real env vars rather
    # than templating them into the command line, so it works the same regardless of
    # the invoking shell/platform (unlike e.g. POSIX `${var}` expansion, which cmd.exe
    # can't parse).
    parser.add_argument("--vcs-ref", default=os.environ.get("usage_branch", "HEAD"))
    parser.add_argument("--repo-prefix", required=True, help="This repo's own name")
    parser.add_argument(
        "--org", default=os.environ.get("usage_org"), help="Azure DevOps organization"
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("usage_project"),
        help="Azure DevOps project",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Delete the repo/pipelines when done (always used in CI)",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help=(
            "Configure a PAT-based git push credential scoped to dev.azure.com "
            "(always used in CI; skipped locally since az login's session doesn't "
            "bridge into git credentials the way gh auth setup-git does for GitHub, "
            "so a human just gets Git Credential Manager's own interactive prompt)"
        ),
    )
    args = parser.parse_args()

    check_az_installed()
    check_azure_devops_extension()

    if not args.org or not args.project:
        raise SystemExit(
            "--org/--project are required. Pass them directly, or (when running "
            "via `mise run integration-test-azdo`) via "
            "`mise run integration-test-azdo -- --org X --project Y`."
        )

    if PLACEHOLDER in (args.org, args.project):
        raise SystemExit(
            f"--org/--project are still set to the placeholder {PLACEHOLDER!r}. If "
            "running via test-auto-integration_test.yml, edit the "
            "integration-test-azdo job's env block with your real Azure DevOps "
            "org/project. See docs/token_permissions.md."
        )

    org_url = f"https://dev.azure.com/{args.org}/"
    check_access(org_url, args.project)

    repo_name = f"{args.repo_prefix}-integration-test-{int(time.time())}"
    dest = tempfile.mkdtemp(prefix="integration-test-")

    try:
        create(
            args.source,
            args.vcs_ref,
            repo_name,
            dest,
            args.org,
            args.project,
            ci=args.ci,
        )
        verify(repo_name, org_url, args.project)
    finally:
        if args.cleanup:
            cleanup(repo_name, org_url, args.project)
        else:
            print(
                f"Leaving {repo_name} in place ({dest}) -- pass --cleanup to delete "
                "it automatically."
            )


if __name__ == "__main__":
    sys.exit(main())

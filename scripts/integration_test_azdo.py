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

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tempfile
import time

PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match the AZDO_INTEGRATION_TEST_ORG/AZDO_INTEGRATION_TEST_PROJECT placeholder
# values in maint-integration_test.yml's integration-test-azdo job -- there's no way
# to auto-detect which org/project a GitHub-hosted workflow should test against.
PLACEHOLDER = "CHANGE_ME"

# Must match template/{% if is_template %}copier.yml{% endif %}.jinja's hardcoded
# `az pipelines create --name "[<repo_name>] <file>"` _tasks entries. "integration_test"
# only registers because create() below passes integration_test_scheduled=true.
PIPELINE_FILE_STEMS = (
    "copier-update-check",
    "docs",
    "pr_validation",
    "release",
    "integration_test",
)


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


def az_value(*args: str) -> str:
    """Run `az <args>` and return its trimmed stdout.

    Returns:
        The command's stdout, stripped of surrounding whitespace.

    """
    return run("az", *args, capture=True).stdout.strip()


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
    """Render+run the template to create the test repo and register its pipelines."""
    if ci:
        configure_git_push_auth()
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


def verify(repo_name: str, org_url: str, project: str) -> None:
    """Assert the created repo and its registered pipelines actually exist.

    Raises:
        SystemExit: if the repo or any expected pipeline is missing.

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

    pipeline_names = json.loads(
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
            "[].name",
        )
        or "[]"
    )
    expected = {f"[{repo_name}] {stem}" for stem in PIPELINE_FILE_STEMS}
    missing = expected - set(pipeline_names)
    if missing:
        raise SystemExit(f"Missing pipeline(s): {', '.join(sorted(missing))}")
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
        SystemExit: if --org/--project are left at their placeholder value.

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Copier template source URL")
    parser.add_argument("--vcs-ref", default="HEAD")
    parser.add_argument("--repo-prefix", required=True, help="This repo's own name")
    parser.add_argument("--org", required=True, help="Azure DevOps organization")
    parser.add_argument("--project", required=True, help="Azure DevOps project")
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

    if PLACEHOLDER in (args.org, args.project):
        raise SystemExit(
            f"--org/--project are still set to the placeholder {PLACEHOLDER!r}. If "
            "running via maint-integration_test.yml, edit the integration-test-azdo "
            "job's env block with your real Azure DevOps org/project. See "
            "docs/token_permissions.md."
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

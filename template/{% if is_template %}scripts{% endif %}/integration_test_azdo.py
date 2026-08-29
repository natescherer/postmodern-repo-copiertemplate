"""Create two throwaway repos from this template and verify them.

Azure DevOps counterpart to integration_test_github.py -- see that file for the shared
shape (create/verify, both repos left in place afterward for you to delete yourself).
Diverges in a few real ways: no Settings App equivalent here, so nothing to poll for
asynchronously; `az` also has no scope-introspection command the way `gh auth status`
does, so this does a basic access check (can the token see the target project at all)
instead of asserting specific scopes; each repo gets a self-contained
cleanup_pipelines.py dropped into its local directory, since Azure DevOps (unlike
GitHub, where deleting the repo deletes everything registered against it) has no
bulk-delete UI for pipelines; and `az` has no cheap way to read a pipeline run's own
step-level output the way `gh run view --json jobs` does, so Maint (Auto) - Copier
Update Check is only checked for a successful run here, not whether it correctly
detected an update -- that nuance stays on the manual checklist for this platform.

Always runs against HEAD -- this is meant to verify a release candidate on main is
good before cutting a release, not to smoke-test an arbitrary branch. Creates two
repos every run, each covering a different scenario so a single run exercises more of
the answer space, not the same fixed answers twice: Repo A is a plain `copier copy`
with `code_coverage` on -- every automated check this script can run happens against
it. Repo B is copied at the last stable tag with `code_coverage` off, left there for
you to run `mise run copier-update` (then `mise run migrate-azdo-pipeline-names`)
against yourself -- deliberately not automated, see main()'s own docstring for why.

Every check this script runs prints its own PASS/FAIL line as it happens, plus a
summary per repo at the end -- it never stops at the first failure, so one run gives
the full picture. It only checks things that need a real Azure DevOps API call or a
real pipeline run; anything `tests/` already covers by rendering locally (structure,
Jinja/YAML validity, links, nav) isn't repeated here.
"""

import argparse
import json
import os
import re
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tempfile
import time
from pathlib import Path

PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match template/{% if is_template %}copier.yml{% endif %}.jinja's hardcoded
# `az pipelines create --name "[<repo_name>] <name>"` _tasks entries.
PIPELINE_DISPLAY_NAMES = (
    "Maint (Auto) - Copier Update Check",
    "Docs (Auto) - Zensical Build & Publish",
    "Test (Auto) - PR Validation",
    "Release (Auto) - Prepare & Publish Release",
    "Maint (Auto) - Renovate",
)

SCRATCH_FILE_CONTENT = "# Integration Test Scratch File\n\nSafe to ignore or delete.\n"


def run(
    *args: str, check: bool = True, capture: bool = False, cwd: str | None = None
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
    print(f"$ {' '.join(args)}" + (f"  (in {cwd})" if cwd else ""))
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        resolved, check=check, text=True, capture_output=capture, cwd=cwd
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
            "session. See docs/token-permissions.md for what this token needs."
        )


def check(failures: list[str], name: str, ok: bool, detail: str = "") -> None:
    """Record and print one named check's result immediately, without halting.

    Every automated check in this script goes through here so failures accumulate
    instead of stopping the run at the first one -- a full run reports the complete
    picture, not just whatever happened to fail first.
    """
    if ok:
        print(f"  [PASS] {name}")
    else:
        print(f"  [FAIL] {name}" + (f" -- {detail}" if detail else ""))
        failures.append(name)


def report(label: str, failures: list[str]) -> None:
    """Print a final summary of one repo's accumulated check results."""
    if failures:
        print(f"\n{label}: {len(failures)} check(s) failed:")
        for name in failures:
            print(f"  - {name}")
    else:
        print(f"\n{label}: all checks passed.")


def create(
    source: str,
    vcs_ref: str,
    repo_name: str,
    dest: str,
    org: str,
    project: str,
    *,
    code_coverage: bool,
) -> None:
    """Render+run the template to create the test repo and register its pipelines.

    `code_coverage` is explicit, not left to `--defaults`, so the two repos this
    script creates can cover both the on and off state instead of silently both
    getting the question's own (always off) default.

    `--defaults` falls back to each question's own default for anything not covered
    by an explicit -d below (currently author_name, zensical_target) -- without it,
    copier drops into an interactive prompt for those. Explicit -d values below still
    take priority over --defaults regardless of order.
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
        "project_name=Integration Test",
        "-d",
        "project_visibility=Private",
        "-d",
        "license=None",
        "-d",
        "lifecycle=Pre-Alpha",
        "-d",
        f"code_coverage={'true' if code_coverage else 'false'}",
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


def list_tags(org_url: str, project: str, repo_name: str) -> set[str]:
    """Return every tag currently pushed to this repo.

    Uses `az repos ref list` rather than `git ls-remote` so it reuses the same az
    session already authenticated against this org, with no separate git-credential
    concern for the repo's own URL.

    Returns:
        The set of tag names, without their `refs/tags/` prefix.

    """
    refs = json.loads(
        az_value(
            "repos",
            "ref",
            "list",
            "--repository",
            repo_name,
            "--filter",
            "tags/",
            "--org",
            org_url,
            "--project",
            project,
            "--query",
            "[].name",
        )
        or "[]"
    )
    return {r.removeprefix("refs/tags/") for r in refs}


CLEANUP_PIPELINES_SCRIPT = '''"""Delete every Azure Pipeline registered for {repo_name}.

Written by integration_test_azdo.py -- not part of the template itself, and never
committed to the repo it's dropped into. Azure DevOps has no bulk-delete UI for
pipelines; each one otherwise has to be removed by hand through its own settings page.
Run this before deleting {repo_name} itself.
"""

import json
import shutil
import subprocess  # noqa: S404
import sys

ORG = {org_url!r}
PROJECT = {project!r}
REPO_NAME = {repo_name!r}


def run(*args: str, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first."""
    print(f"$ {{' '.join(args)}}")
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    return subprocess.run(  # noqa: S603
        resolved, check=True, text=True, capture_output=capture
    )


def main() -> None:
    """Delete every pipeline registered for REPO_NAME in PROJECT."""
    pipeline_ids = json.loads(
        run(
            "az", "pipelines", "list",
            "--repository", REPO_NAME,
            "--org", ORG,
            "--project", PROJECT,
            "--query", "[].id",
            capture=True,
        ).stdout
        or "[]"
    )
    if not pipeline_ids:
        print(f"No pipelines registered for {{REPO_NAME}}.")
        return
    for pipeline_id in pipeline_ids:
        run(
            "az", "pipelines", "delete",
            "--id", str(pipeline_id),
            "--org", ORG,
            "--project", PROJECT,
            "--yes",
        )
    print(f"Deleted {{len(pipeline_ids)}} pipeline(s) for {{REPO_NAME}}.")


if __name__ == "__main__":
    sys.exit(main())
'''


def write_cleanup_script(dest: str, org_url: str, project: str, repo_name: str) -> None:
    """Drop a standalone script into `dest` that deletes every pipeline for this repo.

    Self-contained (no import from this module) so it still works after this process
    exits, whenever you're actually ready to delete the throwaway repo -- and never
    committed, since it has no reason to exist once the repo itself is gone.
    """
    Path(dest, "cleanup_pipelines.py").write_text(
        CLEANUP_PIPELINES_SCRIPT.format(
            org_url=org_url, project=project, repo_name=repo_name
        ),
        encoding="utf-8",
    )


def report_pr_validation_policy(
    repo_id: str,
    pipelines: list[dict],
    org_url: str,
    project: str,
    repo_name: str,
    failures: list[str],
) -> None:
    """Report whether the PR-validation build-validation policy was actually applied.

    Only checks the policy configuration itself (existence, blocking, enabled, and
    that it targets the pr_validation pipeline) -- not the Project Administrators
    bypass-permission grant alongside it. `az devops security permission`'s JSON
    output shape isn't documented clearly enough (no example response in Microsoft's
    own docs) to assert against confidently without a live org to verify against, so
    that half is left unverified here rather than risk a check that's confidently
    wrong in either direction.
    """
    pr_validation_id = next(
        (
            p["id"]
            for p in pipelines
            if p["name"] == f"[{repo_name}] Test (Auto) - PR Validation"
        ),
        None,
    )
    if pr_validation_id is None:
        check(
            failures,
            "PR-validation build policy targets the right pipeline",
            False,
            "pr_validation pipeline not found",
        )
        return

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
    check(
        failures,
        "a build-validation policy on 'main' targets the pr_validation pipeline",
        bool(matching),
    )
    if not matching:
        return
    policy = matching[0]
    check(
        failures,
        "the build-validation policy is blocking and enabled",
        bool(policy.get("isBlocking")) and bool(policy.get("isEnabled")),
        f"policy {policy.get('id')}",
    )


def verify(
    repo_name: str, org_url: str, project: str, failures: list[str]
) -> list[dict]:
    """Assert the created repo, its pipelines, and its PR-validation policy exist.

    Returns:
        The repo's registered pipelines (id/name), for callers that need to dispatch
        one by name without looking it up again.

    Raises:
        SystemExit: only if the repo itself can't be found -- every other assertion
            is recorded via check() instead, since a real value here doesn't prevent
            the rest of this script's checks from being meaningful.

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
        raise SystemExit(f"Repo {repo_name!r} not found -- did create() fail?")

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
    check(
        failures,
        "every expected pipeline is registered",
        expected <= pipeline_names,
        f"missing: {expected - pipeline_names}",
    )

    report_pr_validation_policy(
        repo_id, pipelines, org_url, project, repo_name, failures
    )
    return pipelines


def dispatch_pipeline(
    org_url: str,
    project: str,
    pipeline_name: str,
    *,
    parameters: dict[str, str] | None = None,
) -> str:
    """Run a pipeline by its full display name and return the new run's ID.

    Returns:
        The run ID.

    """
    args = [
        "pipelines",
        "run",
        "--name",
        pipeline_name,
        "--org",
        org_url,
        "--project",
        project,
        "--query",
        "id",
        "-o",
        "tsv",
    ]
    for key, value in (parameters or {}).items():
        args += ["--parameters", f"{key}={value}"]
    return az_value(*args)


def wait_for_pipeline_run(
    org_url: str, project: str, run_id: str, *, timeout: int = 900
) -> str:
    """Poll a pipeline run until it finishes and return its result.

    Returns:
        The run's result, e.g. "succeeded" or "failed" -- "timed out" if `timeout`
        seconds pass without the run completing.

    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        info = json.loads(
            az_value(
                "pipelines",
                "runs",
                "show",
                "--id",
                run_id,
                "--org",
                org_url,
                "--project",
                project,
            )
            or "{}"
        )
        if info.get("status") == "completed":
            return info.get("result", "unknown")
        time.sleep(10)
    return "timed out"


def pipeline_numeric_id(org_url: str, project: str, pipeline_name: str) -> str:
    """Resolve a pipeline's numeric ID from its full display name.

    Returns:
        The numeric ID as a string.

    """
    return az_value(
        "pipelines",
        "show",
        "--name",
        pipeline_name,
        "--org",
        org_url,
        "--project",
        project,
        "--query",
        "id",
        "-o",
        "tsv",
    )


def latest_pipeline_run_id(
    org_url: str, project: str, pipeline_numeric_id_: str
) -> str:
    """Return the most recent run's ID for a pipeline, or "" if none exist yet.

    Returns:
        The run ID as a string, or "".

    """
    return az_value(
        "pipelines",
        "runs",
        "list",
        "--org",
        org_url,
        "--project",
        project,
        "--pipeline-ids",
        pipeline_numeric_id_,
        "--top",
        "1",
        "--query",
        "[0].id",
        "-o",
        "tsv",
    )


def wait_for_new_pipeline_run(
    org_url: str,
    project: str,
    pipeline_numeric_id_: str,
    before_id: str,
    *,
    timeout: int = 180,
) -> str:
    """Poll for a new run of a pipeline to appear after `before_id`.

    A push-triggered Azure Pipeline run doesn't always register immediately --
    observed taking longer than a 60s budget in live testing, well before any
    step of the run itself even starts.

    Returns:
        The new run's ID.

    Raises:
        SystemExit: if no new run appears within `timeout` seconds.

    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = latest_pipeline_run_id(org_url, project, pipeline_numeric_id_)
        if current and current != before_id:
            return current
        time.sleep(5)
    raise SystemExit(
        f"Timed out waiting for a new run of pipeline {pipeline_numeric_id_}"
    )


def provision_test_secrets(org_url: str, project: str, repo_name: str) -> None:
    """Set a placeholder APPRISE_URL variable on every pipeline that requires it.

    Mirrors `mise run provision-secrets`'s own `az pipelines variable create` calls
    (see mise.toml.jinja) -- each pipeline needs its own copy, since Azure Pipelines
    variables are scoped per-pipeline, not project-wide the way GitHub secrets are.
    Points at a real, harmless HTTPS endpoint, not a fake host, so a pipeline that
    actually sends a notification doesn't fail on an unrelated delivery error.
    """
    for pipeline in (
        "Maint (Auto) - Copier Update Check",
        "Release (Auto) - Prepare & Publish Release",
        "Docs (Auto) - Zensical Build & Publish",
        "Maint (Auto) - Renovate",
    ):
        run(
            "az",
            "pipelines",
            "variable",
            "create",
            "--name",
            "APPRISE_URL",
            "--pipeline-name",
            f"[{repo_name}] {pipeline}",
            "--value",
            "json://httpbin.org/post",
            "--secret",
            "true",
            "--allow-override",
            "true",
            "--org",
            org_url,
            "--project",
            project,
        )


def check_copier_update_check(
    org_url: str, project: str, repo_name: str, failures: list[str]
) -> None:
    """Dispatch Maint (Auto) - Copier Update Check and confirm it runs successfully.

    Doesn't check whether it correctly detected an update either way -- see this
    module's own docstring for why that stays manual on this platform.
    """
    print("Checking Maint (Auto) - Copier Update Check...")
    run_id = dispatch_pipeline(
        org_url, project, f"[{repo_name}] Maint (Auto) - Copier Update Check"
    )
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(
        failures, "Copier Update Check pipeline succeeds", result == "succeeded", result
    )


def check_noop_update(dest: str, vcs_ref: str, failures: list[str]) -> None:
    """Run `copier update` against an already-current repo and confirm it's a no-op.

    `--defaults` is safe here specifically because nothing changed since this repo was
    copied -- there's no template diff to introduce a new question, so there's no risk
    of silently defaulting past a real prompt the way there would be for Repo B.

    `vcs_ref` must match whatever `create()` used for this repo: without an explicit
    ref, `copier update`/`check-update` falls back to resolving "the latest tag," and
    if there's no clean tag at the exact commit being tested, copier synthesizes a
    `git describe`-style pseudo-version string and then tries to `git clone --branch`
    using that same string as if it were a real ref -- which fails outright.
    """
    print("Checking `copier update` is a no-op on an already-current repo...")
    run(
        "copier",
        "update",
        "--answers-file",
        ".config/copier-answers.yml",
        "--skip-answered",
        "--trust",
        "--defaults",
        f"--vcs-ref={vcs_ref}",
        cwd=dest,
    )
    status = run("git", "status", "--porcelain", capture=True, cwd=dest)
    check(
        failures,
        "no-op `copier update` makes no changes",
        not status.stdout.strip(),
        status.stdout.strip(),
    )


def check_link_check(
    org_url: str, project: str, repo_name: str, failures: list[str]
) -> None:
    """Dispatch Maint (Auto) - Link Check and confirm it completes clean."""
    print("Checking Maint (Auto) - Link Check...")
    run_id = dispatch_pipeline(
        org_url, project, f"[{repo_name}] Maint (Auto) - Link Check"
    )
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(failures, "Link Check pipeline succeeds", result == "succeeded", result)


def check_renovate(
    org_url: str, project: str, repo_name: str, failures: list[str]
) -> None:
    """Dispatch Maint (Auto) - Renovate and confirm it authenticates successfully.

    GitHub's counterpart to this check doesn't exist: Renovate there runs as an
    external GitHub App on its own schedule, not a dispatchable workflow. Azure DevOps
    runs it as a self-hosted pipeline instead, so it's dispatchable here.
    """
    print("Checking Maint (Auto) - Renovate...")
    run_id = dispatch_pipeline(
        org_url, project, f"[{repo_name}] Maint (Auto) - Renovate"
    )
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(failures, "Renovate pipeline succeeds", result == "succeeded", result)


def wait_for_pr_policy(org_url: str, pr_id: str) -> str:
    """Poll a PR's build-validation policy until it settles past queued/running.

    `az repos pr policy list` takes no `--project` -- a PR ID is unique within the
    whole organization, not scoped per-project the way a repo name is.

    Returns:
        The joined set of distinct settled statuses (e.g. "approved" or "rejected"),
        or "unknown" if none ever left queued/running within the timeout.

    """
    for _ in range(24):
        evaluations = json.loads(
            az_value(
                "repos",
                "pr",
                "policy",
                "list",
                "--id",
                pr_id,
                "--org",
                org_url,
            )
            or "[]"
        )
        build_evals = [
            e
            for e in evaluations
            if e.get("configuration", {}).get("type", {}).get("displayName") == "Build"
        ]
        statuses = {e.get("status") for e in build_evals}
        if statuses and not statuses & {"queued", "running"}:
            return "/".join(sorted(statuses))
        time.sleep(10)
    return "unknown"


def assert_pr_blocked(
    org_url: str, pr_id: str, reason: str, failures: list[str]
) -> None:
    """Poll a PR's build-validation policy evaluation and assert it's blocked."""
    status = wait_for_pr_policy(org_url, pr_id)
    check(
        failures,
        f"PR Validation fails on {reason}",
        status == "rejected",
        f"policy status={status!r}",
    )


def open_pr_wait_and_merge(
    org_url: str,
    project: str,
    repo_name: str,
    dest: str,
    branch: str,
    commit_message: str,
    filename: str,
) -> None:
    """Open a normal, passing PR and merge it -- the only way real commits reach main.

    Branch protection rejects a direct `git push` to main outright, even for the
    project owner (confirmed the hard way: TF402455 "Pushes to this branch are not
    permitted"). This also mirrors how Release (Auto) - Prepare & Publish Release
    actually gets triggered in practice: by the push Azure DevOps generates when a PR
    completes, not by anyone pushing to main directly.

    Raises:
        SystemExit: if the PR's build-validation policy doesn't end up approved.

    """
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    run("git", "switch", "-c", branch, cwd=dest)
    Path(dest, filename).write_text(SCRATCH_FILE_CONTENT, newline="\n")
    run("git", "add", "-A", cwd=dest)
    run("git", "commit", "-m", commit_message, cwd=dest)
    run("git", "push", "-u", "origin", branch, cwd=dest)
    pr = json.loads(
        az_value(
            "repos",
            "pr",
            "create",
            "--repository",
            repo_name,
            "--source-branch",
            branch,
            "--target-branch",
            "main",
            "--title",
            commit_message,
            "--description",
            "Integration test.",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "{}"
    )
    pr_id = str(pr.get("pullRequestId"))
    status = wait_for_pr_policy(org_url, pr_id)
    if status != "approved":
        raise SystemExit(
            f"PR {pr_id} in {repo_name} didn't pass its policy: {status!r}"
        )
    run(
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        pr_id,
        "--status",
        "completed",
        "--squash",
        "true",
        # Without this, Azure DevOps writes a generic "Merge pull request N from
        # <branch> into main" squash commit message instead of the PR title -- unlike
        # GitHub, which defaults a squash merge's commit message to the PR title.
        # knope's PrepareRelease step parses Conventional Commits from real git commit
        # messages, so a squashed test commit that loses its "fix:"/"feat:" prefix this
        # way silently stops counting as a qualifying commit once a tag already exists
        # (confirmed live: after the first release, this caused knope's own
        # create-prerelease-via-knope workflow to fail with "No packages are ready to
        # release" even though a real fix commit had just been merged).
        "--merge-commit-message",
        commit_message,
        "--delete-source-branch",
        "true",
        "--org",
        org_url,
    )
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)


def check_bad_title_blocks_merge(
    org_url: str, project: str, repo_name: str, dest: str, failures: list[str]
) -> None:
    """Open a PR with a non-Conventional-Commit title and confirm it's blocked."""
    print("Checking a bad-title PR fails Test (Auto) - PR Validation...")
    run("git", "checkout", "main", cwd=dest)
    branch = "integration-test/bad-title"
    run("git", "switch", "-c", branch, cwd=dest)
    Path(dest, "INTEGRATION_TEST_BAD_TITLE.md").write_text(
        SCRATCH_FILE_CONTENT, newline="\n"
    )
    run("git", "add", "-A", cwd=dest)
    title = "this title is not a conventional commit"
    run("git", "commit", "-m", title, cwd=dest)
    run("git", "push", "-u", "origin", branch, cwd=dest)
    pr = json.loads(
        az_value(
            "repos",
            "pr",
            "create",
            "--repository",
            repo_name,
            "--source-branch",
            branch,
            "--target-branch",
            "main",
            "--title",
            title,
            "--description",
            "Integration test: expects PR Validation to fail on the title.",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "{}"
    )
    pr_id = str(pr.get("pullRequestId"))
    assert_pr_blocked(org_url, pr_id, "a bad PR title", failures)
    run(
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        pr_id,
        "--status",
        "abandoned",
        "--org",
        org_url,
    )


def check_failing_tests_block_merge(
    org_url: str, project: str, repo_name: str, dest: str, failures: list[str]
) -> None:
    """Open a PR with a deliberately failing test and confirm it's blocked."""
    print("Checking a PR with a failing test fails Test (Auto) - PR Validation...")
    run("git", "checkout", "main", cwd=dest)
    branch = "integration-test/failing-test"
    run("git", "switch", "-c", branch, cwd=dest)
    Path(dest, "tests", "test_integration_test_deliberate_failure.py").write_text(
        "def test_deliberately_fails():\n"
        '    assert False, "integration test: deliberate failure"\n',
        newline="\n",
    )
    run("git", "add", "-A", cwd=dest)
    title = "test: deliberately failing test for integration test"
    run("git", "commit", "-m", title, cwd=dest)
    run("git", "push", "-u", "origin", branch, cwd=dest)
    pr = json.loads(
        az_value(
            "repos",
            "pr",
            "create",
            "--repository",
            repo_name,
            "--source-branch",
            branch,
            "--target-branch",
            "main",
            "--title",
            title,
            "--description",
            "Integration test: expects PR Validation to fail on the test suite.",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "{}"
    )
    pr_id = str(pr.get("pullRequestId"))
    assert_pr_blocked(org_url, pr_id, "a failing test suite", failures)
    run(
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        pr_id,
        "--status",
        "abandoned",
        "--org",
        org_url,
    )


def knope_release_pr_title(org_url: str, project: str, repo_name: str) -> str | None:
    """Look up the open knope/release PR's title, if one is open.

    The title (e.g. "chore: prepare release 0.0.1") encodes the version knope
    computed -- unlike relying on "is a PR open at all" (one may already be open from
    the bootstrap-time v0.1.0 PR), it's the right signal for "did this merge actually
    change what's proposed."

    Returns:
        The PR title, or None if no such PR is currently open.

    """
    prs = json.loads(
        az_value(
            "repos",
            "pr",
            "list",
            "--repository",
            repo_name,
            "--source-branch",
            "knope/release",
            "--status",
            "active",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "[]"
    )
    return prs[0]["title"] if prs else None


def check_release_flow(
    org_url: str, project: str, repo_name: str, dest: str, failures: list[str]
) -> None:
    """Exercise the real release flow: a no-op merge, then a real release and tag.

    Azure DevOps has a single Release (Auto) - Prepare & Publish Release pipeline
    (unlike GitHub's split prepare/publish workflows) -- one pipeline handles both the
    push-to-main prepare step and the merge-triggered publish step, telling them apart
    via its own API check.
    """
    print("Checking Release (Auto) - Prepare & Publish Release...")
    pid = pipeline_numeric_id(
        org_url, project, f"[{repo_name}] Release (Auto) - Prepare & Publish Release"
    )

    # The bootstrap-time PR is prepared with an explicit --override-version; the
    # *first* automated run after that always recomputes the version from knope's own
    # default rules, changing the PR's content regardless of what triggered that run.
    # Absorb that one-time transition with a throwaway merge before testing that a
    # docs-only merge is a true no-op -- otherwise the correction gets misattributed
    # to whichever commit happens to trigger the first automated run.
    prepare_before = latest_pipeline_run_id(org_url, project, pid)
    open_pr_wait_and_merge(
        org_url,
        project,
        repo_name,
        dest,
        "integration-test/warmup",
        "chore: integration test warmup commit",
        "INTEGRATION_TEST_WARMUP.md",
    )
    warmup_run_id = wait_for_new_pipeline_run(org_url, project, pid, prepare_before)
    wait_for_pipeline_run(org_url, project, warmup_run_id)

    # A release PR may already be open here (e.g. the bootstrap-time v0.1.0 one), so
    # "no PR is open" isn't the right no-op signal -- what actually matters is that a
    # docs-only merge doesn't change what version it proposes.
    docs_noop_before = knope_release_pr_title(org_url, project, repo_name)
    prepare_before = latest_pipeline_run_id(org_url, project, pid)
    open_pr_wait_and_merge(
        org_url,
        project,
        repo_name,
        dest,
        "integration-test/docs-noop",
        "docs: integration test no-op commit",
        "INTEGRATION_TEST_DOCS.md",
    )
    run_id = wait_for_new_pipeline_run(org_url, project, pid, prepare_before)
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(
        failures,
        "a docs-only merge keeps the release pipeline green",
        # `az repos pr create` always fails with TF401179 ("an active pull request
        # ... already exists") once the first knope/release PR is open -- see the feat
        # merge check below for the full explanation. A docs-only commit that finds
        # nothing release-worthy can *also* legitimately surface as partiallySucceeded
        # (matching releasing.md's "shows a failed step but stays green overall" note
        # for the equivalent GitHub case), so either way this isn't a hard failure.
        result in ("succeeded", "partiallySucceeded"),
        result,
    )
    docs_noop_after = knope_release_pr_title(org_url, project, repo_name)
    check(
        failures,
        "a docs-only merge doesn't change the release PR's proposed version",
        docs_noop_after == docs_noop_before,
        f"before={docs_noop_before!r}, after={docs_noop_after!r}",
    )

    prepare_before = latest_pipeline_run_id(org_url, project, pid)
    open_pr_wait_and_merge(
        org_url,
        project,
        repo_name,
        dest,
        "integration-test/feat",
        "feat: integration test feature",
        "INTEGRATION_TEST_FEAT.md",
    )
    run_id = wait_for_new_pipeline_run(org_url, project, pid, prepare_before)
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(
        failures,
        "a feat merge's release pipeline succeeds",
        # `az repos pr create` always fails with TF401179 ("an active pull request
        # ... already exists") once the first knope/release PR is open -- every push
        # after the first hits this, regardless of commit type. Azure DevOps still
        # refreshes the PR's title from the new commit despite that failed step (the
        # final title -- and the eventual release -- come out correct), so this is a
        # real but non-blocking imperfection, not a failure worth hard-failing on.
        result in ("succeeded", "partiallySucceeded"),
        result,
    )
    release_prs = json.loads(
        az_value(
            "repos",
            "pr",
            "list",
            "--repository",
            repo_name,
            "--source-branch",
            "knope/release",
            "--status",
            "active",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "[]"
    )
    check(failures, "a feat commit opens a release PR", bool(release_prs))
    if not release_prs:
        return
    pr = release_prs[0]
    pr_id, pr_title = str(pr.get("pullRequestId")), pr.get("title", "")
    check(
        failures,
        "release PR title looks like a version bump",
        bool(re.search(r"prepare release v?\d+\.\d+\.\d+", pr_title)),
        pr_title,
    )

    before_tags = list_tags(org_url, project, repo_name)
    publish_before = latest_pipeline_run_id(org_url, project, pid)
    status = wait_for_pr_policy(org_url, pr_id)
    check(
        failures,
        "the release PR's build validation passes",
        status == "approved",
        status,
    )
    if status != "approved":
        return
    run(
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        pr_id,
        "--status",
        "completed",
        "--squash",
        "true",
        "--delete-source-branch",
        "true",
        "--org",
        org_url,
    )
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    publish_run_id = wait_for_new_pipeline_run(org_url, project, pid, publish_before)
    result = wait_for_pipeline_run(org_url, project, publish_run_id)
    check(
        failures,
        "merging the release PR publishes successfully",
        result == "succeeded",
        result,
    )
    new_tags = list_tags(org_url, project, repo_name) - before_tags
    check(
        failures,
        "merging the release PR creates a new tag",
        bool(new_tags),
        f"before={before_tags}",
    )


def check_prerelease_flow(
    org_url: str, project: str, repo_name: str, dest: str, failures: list[str]
) -> None:
    """Exercise Release (Manual) - Create Prerelease -- a label, a dup, a new label."""
    print("Checking Release (Manual) - Create Prerelease...")
    name = f"[{repo_name}] Release (Manual) - Create Prerelease"

    # PrepareRelease refuses to run with nothing to bump -- without a real commit
    # since the last release, every dispatch below would fail with knope's own
    # "No packages are ready to release", not the behavior this is meant to check.
    open_pr_wait_and_merge(
        org_url,
        project,
        repo_name,
        dest,
        "integration-test/prerelease-fix",
        "fix: integration test prerelease commit",
        "INTEGRATION_TEST_PRERELEASE.md",
    )

    before = list_tags(org_url, project, repo_name)
    run_id = dispatch_pipeline(org_url, project, name, parameters={"label": "alpha"})
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(
        failures,
        "dispatching an alpha prerelease succeeds",
        result == "succeeded",
        result,
    )
    after_alpha = list_tags(org_url, project, repo_name)
    new_alpha = after_alpha - before
    check(
        failures,
        "an alpha prerelease creates a matching tag",
        any(re.search(r"-alpha\.\d+$", t) for t in new_alpha),
        f"new tags: {new_alpha}",
    )

    run_id = dispatch_pipeline(org_url, project, name, parameters={"label": "alpha"})
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(
        failures,
        "re-dispatching the same label at the same commit is blocked",
        result == "failed",
        result,
    )

    run_id = dispatch_pipeline(org_url, project, name, parameters={"label": "beta"})
    result = wait_for_pipeline_run(org_url, project, run_id)
    check(
        failures,
        "dispatching a different label at the same commit succeeds",
        result == "succeeded",
        result,
    )
    new_beta = list_tags(org_url, project, repo_name) - after_alpha
    check(
        failures,
        "a beta prerelease creates a matching tag",
        any(re.search(r"-beta\.\d+$", t) for t in new_beta),
        f"new tags: {new_beta}",
    )


def check_post_update(
    org_url: str, project: str, repo_name: str, dest: str, failures: list[str]
) -> None:
    """Verify Repo B's state after a human has run `mise run copier-update` on it.

    This is the second entry point (`--verify-update`): the update itself happens by
    hand, on your own schedule, so this script can't chain straight from creating the
    repo into checking it -- see main()'s own docstring.
    """
    print(f"Checking {repo_name}'s update applied cleanly...")
    run("git", "fetch", cwd=dest)
    log = run(
        "git", "log", "--oneline", "-10", "origin/main", capture=True, cwd=dest
    ).stdout
    check(
        failures,
        "git log shows a copier update commit",
        "copier update" in log.lower(),
        log,
    )
    # Copier's own update conflicts come from `git merge-file`, so they use the same
    # markers as any other git conflict -- one grep catches both.
    grep = run(
        "git",
        "grep",
        "-lE",
        r"^<{7} |^={7}$|^>{7} ",
        "origin/main",
        "--",
        cwd=dest,
        check=False,
        capture=True,
    )
    check(
        failures,
        "no leftover conflict markers on main",
        grep.returncode != 0,
        grep.stdout,
    )

    pipeline_names = {
        p["name"]
        for p in json.loads(
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
    }
    expected = {f"[{repo_name}] {name}" for name in PIPELINE_DISPLAY_NAMES}
    check(
        failures,
        "every pipeline is registered only under its current name "
        "(migrate_pipeline_names.py ran)",
        expected <= pipeline_names,
        f"missing: {expected - pipeline_names}",
    )

    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    branch = "integration-test/post-update-check"
    run("git", "switch", "-c", branch, cwd=dest)
    Path(dest, "INTEGRATION_TEST_POST_UPDATE.md").write_text(
        SCRATCH_FILE_CONTENT, newline="\n"
    )
    run("git", "add", "-A", cwd=dest)
    title = "chore: integration test post-update check"
    run("git", "commit", "-m", title, cwd=dest)
    run("git", "push", "-u", "origin", branch, cwd=dest)
    pr = json.loads(
        az_value(
            "repos",
            "pr",
            "create",
            "--repository",
            repo_name,
            "--source-branch",
            branch,
            "--target-branch",
            "main",
            "--title",
            title,
            "--description",
            "Integration test: confirms PR Validation still works after `copier "
            "update`.",
            "--org",
            org_url,
            "--project",
            project,
        )
        or "{}"
    )
    pr_id = str(pr.get("pullRequestId"))
    status = wait_for_pr_policy(org_url, pr_id)
    check(
        failures,
        "PR Validation still triggers and passes after the update",
        status == "approved",
        status,
    )
    run(
        "az",
        "repos",
        "pr",
        "update",
        "--id",
        pr_id,
        "--status",
        "completed",
        "--squash",
        "true",
        "--delete-source-branch",
        "true",
        "--org",
        org_url,
    )


def main() -> None:
    """Create and verify two throwaway repos, each covering a different scenario.

    Both run every time, always at HEAD (this tool exists to verify a release
    candidate on main is good before cutting a release, not to smoke-test an
    arbitrary branch). Repo A is a plain `copier copy` with `code_coverage` on --
    every automated check this script can run happens against it. Repo B is copied at
    the last stable tag with `code_coverage` off, for you to run `mise run
    copier-update` (then `mise run migrate-azdo-pipeline-names`) against yourself --
    deliberately not automated: those are the exact commands, with the exact prompts,
    a real user gets, and running them by hand is the only way to see a new
    question's prompt land the way it actually would for them, not however this
    script happened to answer it. Both repos are left in place afterward for
    inspection.

    Once you've updated Repo B by hand, re-run this script with `--verify-update
    <repo> --local-path <path>` (also available as `mise run
    integration-test-verify-update-azdo`) to check it applied cleanly -- see
    docs/manual-verification-azdo.md's "Repo B" section.

    Raises:
        SystemExit: if `az` or its azure-devops extension aren't installed, if
            --org/--project are missing, or if any automated check failed (after
            printing every check's result -- see check()).

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Copier template source URL")
    parser.add_argument("--repo-prefix", help="This repo's own name")
    # usage_org/usage_project are set when this runs via `mise run
    # integration-test-azdo`, whose `usage` field defines matching flags (mise's own
    # arg-parsing, not this one) -- mise passes them through as real env vars rather
    # than templating them into the command line, so it works the same regardless of
    # the invoking shell/platform (unlike e.g. POSIX `${var}` expansion, which cmd.exe
    # can't parse).
    parser.add_argument(
        "--org", default=os.environ.get("usage_org"), help="Azure DevOps organization"
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("usage_project"),
        help="Azure DevOps project",
    )
    parser.add_argument(
        "--verify-update",
        metavar="REPO",
        default=os.environ.get("usage_repo"),
        help=(
            "Skip creating repos; instead verify REPO (repository name) after you've "
            "run `mise run copier-update` on it yourself. Requires --local-path."
        ),
    )
    parser.add_argument(
        "--local-path",
        default=os.environ.get("usage_local_path"),
        help="Local clone path for --verify-update (printed when Repo B was created).",
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

    org_url = f"https://dev.azure.com/{args.org}/"
    check_access(org_url, args.project)

    if args.verify_update:
        if not args.local_path:
            raise SystemExit("--verify-update requires --local-path too.")
        update_failures: list[str] = []
        check_post_update(
            org_url, args.project, args.verify_update, args.local_path, update_failures
        )
        report(f"Repo B ({args.verify_update})", update_failures)
        if update_failures:
            raise SystemExit(1)
        return

    if not args.source or not args.repo_prefix:
        raise SystemExit("--source and --repo-prefix are required.")

    timestamp = int(time.time())

    print("=== Repo A: fresh copy at HEAD (code_coverage: on) ===")
    repo_a_name = f"{args.repo_prefix}-integration-test-{timestamp}-a"
    dest_a = tempfile.mkdtemp(prefix="integration-test-")
    create(
        args.source,
        "HEAD",
        repo_a_name,
        dest_a,
        args.org,
        args.project,
        code_coverage=True,
    )
    failures_a: list[str] = []
    verify(repo_a_name, org_url, args.project, failures_a)
    provision_test_secrets(org_url, args.project, repo_a_name)
    check_copier_update_check(org_url, args.project, repo_a_name, failures_a)
    check_noop_update(dest_a, "HEAD", failures_a)
    check_link_check(org_url, args.project, repo_a_name, failures_a)
    check_renovate(org_url, args.project, repo_a_name, failures_a)
    check_bad_title_blocks_merge(org_url, args.project, repo_a_name, dest_a, failures_a)
    check_failing_tests_block_merge(
        org_url, args.project, repo_a_name, dest_a, failures_a
    )
    check_release_flow(org_url, args.project, repo_a_name, dest_a, failures_a)
    check_prerelease_flow(org_url, args.project, repo_a_name, dest_a, failures_a)
    # Dropped last: it's an untracked file never meant to be committed, and
    # check_noop_update() above requires a clean working tree.
    write_cleanup_script(dest_a, org_url, args.project, repo_a_name)
    report(f"Repo A ({repo_a_name})", failures_a)

    old_ref = latest_stable_tag(args.source)
    print(f"=== Repo B: {old_ref}, for you to update by hand (code_coverage: off) ===")
    repo_b_name = f"{args.repo_prefix}-integration-test-{timestamp}-b"
    dest_b = tempfile.mkdtemp(prefix="integration-test-")
    create(
        args.source,
        old_ref,
        repo_b_name,
        dest_b,
        args.org,
        args.project,
        code_coverage=False,
    )
    failures_b: list[str] = []
    verify(repo_b_name, org_url, args.project, failures_b)
    provision_test_secrets(org_url, args.project, repo_b_name)
    check_copier_update_check(org_url, args.project, repo_b_name, failures_b)
    # Dropped last: an untracked file, and dest_b is left for you to run a real
    # `mise run copier-update` against, which should start from a clean tree.
    write_cleanup_script(dest_b, org_url, args.project, repo_b_name)
    report(f"Repo B ({repo_b_name}, before updating)", failures_b)

    print(
        f"\nLeaving {repo_a_name} ({dest_a}) and {repo_b_name} ({dest_b}) in place. "
        "Run `python cleanup_pipelines.py` in each directory before deleting the "
        f"repos -- Azure DevOps has no bulk-delete UI for pipelines. {repo_b_name} "
        f"is still at {old_ref}; cd into {dest_b} and run `mise run copier-update` "
        "yourself to test the update path, then `mise run "
        f"integration-test-verify-update-azdo -- --repo {repo_b_name} --local-path "
        f'{dest_b}` to verify it applied cleanly (see "Repo B" in '
        "docs/manual-verification-azdo.md)."
    )

    if failures_a or failures_b:
        raise SystemExit(1)


if __name__ == "__main__":
    sys.exit(main())

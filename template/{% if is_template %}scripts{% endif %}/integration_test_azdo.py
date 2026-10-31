"""Create two throwaway repos from this template and verify them.

The Azure DevOps counterpart to integration_test_github.py, with the same shape: create,
then verify, leaving both repos for you to delete. It differs where the platforms do:

- No settings.yml equivalent, so there's nothing for gh-settings to apply.
- `az` can't list a token's scopes the way `gh auth status` can, so this checks only
  that it can see the target project.
- Deleting an Azure DevOps repo doesn't remove its pipelines, so `--cleanup` deletes
  those too.
- `az` can't easily read a run's step output the way `gh run view --json jobs` can, so
  Maint (Auto) - Monthly Maintenance's Copier Update Check job is checked only for a
  successful run. Whether it detected an update stays in this platform's runbook.

It always runs against HEAD, to verify a release candidate on main before a release.
Each run creates two repos with different answers, to cover more combinations. Repo A is
a `copier copy` with `code_coverage` on, and every automated check runs against it. Repo
B is a copy at the last stable tag with `code_coverage` off, left for you to update to
HEAD as the runbook's Repo B section says; main()'s docstring says why that's manual.

Each check prints a PASS or FAIL line as it runs, and each repo gets a summary at the
end. A failure doesn't stop the run. It checks only what needs a real Azure DevOps API
call or pipeline run; `tests/` covers what a local render can (structure, Jinja and YAML
validity, links, nav).
"""

import argparse
import json
import os
import re
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import time
import urllib.parse
from collections.abc import Callable
from pathlib import Path

from console import (
    RepoResult,
    ask,
    check,
    heading,
    run,
    save_log,
    say,
    start_log,
    step,
    summary,
)
from docs_links import docs_page_url
from repo_edits import (
    local_clone_dir,
    local_clones,
    prepare_repo_a,
    prepare_repo_b,
    push_older_recorded_version,
    remove_clones,
    repo_b_clone,
)

PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match template/{% if is_template %}copier.yml{% endif %}.jinja's hardcoded
# `az pipelines create --name "[<repo_name>] <name>"` _tasks entries.
PIPELINE_DISPLAY_NAMES = (
    "Maint (Auto) - Monthly Maintenance",
    "Docs (Auto) - Zensical Build & Commit",
    "Test (Auto) - PR Validation",
    "Release (Auto) - Prepare & Publish Release",
)
MONTHLY_MAINTENANCE = "Maint (Auto) - Monthly Maintenance"
RELEASE = "Release (Auto) - Prepare & Publish Release"

# The pipelines of a release before Monthly Maintenance merged the three Maint
# pipelines, Release took over Create Prerelease, and Docs was renamed to match
# GitHub's. Repo B starts at the last release, so it has these until you update it and
# run `mise run migrate-azdo-pipeline-names`. Remove once the last release has Monthly
# Maintenance.
LEGACY_PIPELINE_DISPLAY_NAMES = (
    "Maint (Auto) - Copier Update Check",
    "Maint (Auto) - Repo Health Check",
    "Maint (Auto) - Renovate",
    "Docs (Auto) - Zensical Build & Publish",
    "Test (Auto) - PR Validation",
    "Release (Auto) - Prepare & Publish Release",
    "Release (Manual) - Create Prerelease",
)

# Every pipeline, current or legacy, whose notifications need APPRISE_URL.
APPRISE_PIPELINES = {
    MONTHLY_MAINTENANCE,
    "Docs (Auto) - Zensical Build & Commit",
    "Docs (Auto) - Zensical Build & Publish",
    "Maint (Auto) - Copier Update Check",
    "Maint (Auto) - Renovate",
}


def pipeline_display_names(dest: str) -> tuple[str, ...]:
    """Return the pipelines a clone's own .azurepipelines/ calls for, current or legacy.

    Returns:
        PIPELINE_DISPLAY_NAMES, or LEGACY_PIPELINE_DISPLAY_NAMES for a clone without
        Monthly Maintenance.

    """
    current = Path(dest, ".azurepipelines", "maint-auto-monthlymaintenance.yml")
    return PIPELINE_DISPLAY_NAMES if current.exists() else LEGACY_PIPELINE_DISPLAY_NAMES


SCRATCH_FILE_CONTENT = "# Integration Test Scratch File\n\nSafe to ignore or delete.\n"

# Must match the bypass grant in the Set Repo Rules task of
# template/{% if is_template %}copier.yml{% endif %}.jinja.
GIT_REPOSITORIES_NAMESPACE = "2e9eb7ed-3c0a-47d4-87c1-0ffdd275fd87"
PULL_REQUEST_BYPASS_POLICY = 32768
# refs/heads/main, UTF-16LE hex-encoded per character: Azure DevOps's Git ACL token
# format for a branch.
MAIN_BRANCH_ACL_PATH = "refs/heads/6d00610069006e00"


def repo_url(org_url: str, project: str, repo_name: str) -> str:
    """Return a repo's web URL, for the run's summary.

    Returns:
        https://dev.azure.com/<org>/<project>/_git/<repo>, with the project encoded.

    """
    return f"{org_url}{urllib.parse.quote(project)}/_git/{repo_name}"


def setup_checklist(copy_output: str) -> list[str]:
    """Return the items of the setup checklist `copier copy` prints at the end.

    Returns:
        Each "- [ ] ..." line under "Setup checklist:", or an empty list.

    """
    lines = [line.strip() for line in copy_output.splitlines()]
    if "Setup checklist:" not in lines:
        return []
    items = []
    for line in lines[lines.index("Setup checklist:") + 1 :]:
        if not line.startswith("- [ ]"):
            break
        items.append(line)
    return items


def az_value(*args: str, echo: bool = True) -> str:
    """Run `az <args>` and return its trimmed stdout.

    Returns:
        The command's stdout, stripped of surrounding whitespace.

    """
    return run("az", *args, capture=True, echo=echo).stdout.strip()


def confirm(prompt: str, *, yes: bool) -> bool:
    """Ask a yes/no question, unless `yes` already answered it.

    With no terminal to answer from, the answer is no.

    Returns:
        True to go ahead.

    """
    if yes:
        return True
    try:
        return ask(f"{prompt} [y/N] ").strip().lower() == "y"
    except EOFError:
        return False


def test_repo_pattern(repo_prefix: str) -> re.Pattern[str]:
    """Match the names main() gives its test repos, and nothing else.

    Returns:
        A pattern for `<repo_prefix>-integration-test-<timestamp>-a` (or `-b`).

    """
    return re.compile(rf"{re.escape(repo_prefix)}-integration-test-\d+-[ab]")


def check_az_installed() -> None:
    """Verify the `az` CLI is resolvable on PATH.

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
    prompt interactively to install it ("Do you want to install it now? (Y/n):"),
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
    """Verify the active az session can see the target project.

    Not a scope check (az has no equivalent to `gh auth status`'s scope list); just
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
            f"session. See {docs_page_url('reference/token-permissions.md')} for what "
            "this token needs."
        )


def template_answers(*, leaf: bool) -> list[str]:
    """Return the -d flags that make a test repo a Template project.

    A leaf template's projects can't be templates, so a leaf template source gets none.
    Otherwise the repo is an extensible template, which exercises everything a template
    can be.

    Returns:
        Copier -d arguments.

    """
    if leaf:
        return []
    return ["-d", "project_type=Template", "-d", "extensible_template=true"]


def create(
    source: str,
    vcs_ref: str,
    repo_name: str,
    dest: str,
    org: str,
    project: str,
    *,
    code_coverage: bool,
    leaf: bool = False,
) -> list[str]:
    """Run the template to create the test repo and register its pipelines.

    `code_coverage` is explicit, so the two repos cover it on and off instead of both
    getting its default (off).

    `--defaults` covers the questions without an explicit -d below (author_name and
    zensical_target); without it, copier prompts for them. Explicit -d values take
    priority over --defaults.

    Returns:
        The setup checklist `copier copy` printed, which the summary repeats: on
        Azure DevOps it exists only in that output, long since scrolled away.

    """
    output = run(
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
        *template_answers(leaf=leaf),
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
    ).stdout
    return setup_checklist(output)


def latest_stable_tag(source: str) -> str:
    """Find this template's most recent stable (non-prerelease) release tag.

    Uses `git ls-remote --tags` so it works directly against `source` without a local
    clone. Matches strict `vX.Y.Z` tags only (excluding prereleases like
    `v1.1.0-alpha.0`) and sorts by parsed version, not lexically; a plain string
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


def cleanup(org_url: str, project: str, repo_prefix: str, *, yes: bool) -> None:
    """Delete every test repo main() created in `project`, and its pipelines.

    It finds them by name, so it covers runs that stopped partway, such as when the
    machine slept, as well as finished ones. Deleting an Azure DevOps repo leaves its
    pipelines behind, so this matches pipelines by their `[<repo>] ` name prefix too,
    including those of a repo that's already gone, and deletes them first.

    Raises:
        SystemExit: if a local clone can't be deleted.

    """
    pattern = test_repo_pattern(repo_prefix)
    scope = ("--org", org_url, "--project", project, "-o", "json")
    repos = sorted(
        (
            repo
            for repo in json.loads(
                az_value("repos", "list", *scope, "--query", "[].{id:id,name:name}")
            )
            if pattern.fullmatch(repo["name"])
        ),
        key=lambda repo: repo["name"],
    )
    pipeline_name = re.compile(rf"\[({pattern.pattern})\] ")
    pipelines = sorted(
        (
            pipeline
            for pipeline in json.loads(
                az_value("pipelines", "list", *scope, "--query", "[].{id:id,name:name}")
            )
            if pipeline_name.match(pipeline["name"])
        ),
        key=lambda pipeline: pipeline["name"],
    )
    clones = local_clones(pattern, "dev.azure.com")
    if not repos and not pipelines and not clones:
        say(f"No integration-test repos, pipelines, or local clones for {project}.")
        return
    say("Integration-test pipelines, repos, and local clones to delete:")
    for item in (*pipelines, *repos):
        say(f"  {item['name']}")
    for clone in clones:
        say(f"  {clone}")
    if not confirm(
        f"Delete these {len(pipelines)} pipeline(s), {len(repos)} repo(s), and "
        f"{len(clones)} local clone(s)?",
        yes=yes,
    ):
        say("Nothing deleted.")
        return
    for pipeline in pipelines:
        run(
            "az",
            "pipelines",
            "delete",
            "--id",
            str(pipeline["id"]),
            *scope[:4],
            "--yes",
        )
    for repo in repos:
        run("az", "repos", "delete", "--id", repo["id"], *scope[:4], "--yes")
    deleted = remove_clones(clones)
    say(
        f"Deleted {len(pipelines)} pipeline(s), {len(repos)} repo(s), and "
        f"{deleted} local clone(s)."
    )
    if deleted < len(clones):
        raise SystemExit(1)


def report_pr_validation_policy(
    repo_id: str,
    pipelines: list[dict],
    org_url: str,
    project: str,
    repo_name: str,
    failures: list[str],
) -> None:
    """Report whether the PR Validation build policy was applied.

    Checks the policy's configuration: that it exists, blocks, is enabled, and targets
    the pr_validation pipeline. report_bypass_permission() checks the bypass beside it.
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


def report_bypass_permission(
    repo_id: str, org_url: str, project: str, failures: list[str]
) -> None:
    """Report whether Project Administrators can bypass main's PR policies.

    Repo setup grants it explicitly, matching GitHub's admin bypass: allow bit 32768
    (PullRequestBypassPolicy) in the Git Repositories namespace, on main's ACL token,
    for the project's Project Administrators group. This reads that same entry.
    """
    project_id = az_value(
        "devops",
        "project",
        "show",
        "--project",
        project,
        "--org",
        org_url,
        "--query",
        "id",
        "-o",
        "tsv",
    )
    groups = json.loads(
        az_value(
            "devops",
            "security",
            "group",
            "list",
            "--org",
            org_url,
            "--project",
            project,
            "-o",
            "json",
        )
        or "{}"
    )
    descriptor = next(
        (
            group["descriptor"]
            for group in groups.get("graphGroups", [])
            if group.get("displayName") == "Project Administrators"
        ),
        None,
    )
    if descriptor is None:
        check(
            failures,
            "Project Administrators can bypass policies to complete PRs on 'main'",
            False,
            "Project Administrators group not found",
        )
        return
    entries = json.loads(
        az_value(
            "devops",
            "security",
            "permission",
            "show",
            "--namespace-id",
            GIT_REPOSITORIES_NAMESPACE,
            "--subject",
            descriptor,
            "--token",
            f"repoV2/{project_id}/{repo_id}/{MAIN_BRANCH_ACL_PATH}",
            "--org",
            org_url,
            "-o",
            "json",
        )
        or "[]"
    )
    aces = entries[0].get("acesDictionary", {}) if entries else {}
    ace = next(iter(aces.values()), {})
    allow, deny = ace.get("allow", 0), ace.get("deny", 0)
    check(
        failures,
        "Project Administrators can bypass policies to complete PRs on 'main'",
        bool(allow & PULL_REQUEST_BYPASS_POLICY)
        and not deny & PULL_REQUEST_BYPASS_POLICY,
        f"allow={allow}, deny={deny}",
    )


def verify(
    repo_name: str,
    org_url: str,
    project: str,
    failures: list[str],
    *,
    names: tuple[str, ...] = PIPELINE_DISPLAY_NAMES,
) -> list[dict]:
    """Assert the created repo, its pipelines, and its PR-validation policy exist.

    Returns:
        The repo's registered pipelines (id/name), for callers that need to dispatch
        one by name without looking it up again.

    Raises:
        SystemExit: only if the repo itself can't be found; every other assertion
            is recorded via check() instead, since a real value here doesn't prevent
            the rest of this script's checks from being meaningful.

    """
    step(f"Verifying {org_url}{project}/{repo_name}")
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
        raise SystemExit(f"Repo {repo_name!r} not found; did create() fail?")

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
    expected = {f"[{repo_name}] {name}" for name in names}
    check(
        failures,
        "every expected pipeline is registered",
        expected <= pipeline_names,
        f"missing: {expected - pipeline_names}",
    )

    report_pr_validation_policy(
        repo_id, pipelines, org_url, project, repo_name, failures
    )
    report_bypass_permission(repo_id, org_url, project, failures)
    return pipelines


def dispatch_pipeline(
    org_url: str,
    project: str,
    pipeline_name: str,
    *,
    parameters: dict[str, str] | None = None,
    branch: str | None = None,
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
    if branch:
        args += ["--branch", branch]
    return az_value(*args)


def wait_for_pipeline_run(
    org_url: str, project: str, run_id: str, *, timeout: int = 900
) -> str:
    """Poll a pipeline run until it finishes and return its result.

    Returns:
        The run's result, e.g. "succeeded" or "failed"; "timed out" if `timeout`
        seconds pass without the run completing.

    """
    print(f"Waiting for pipeline run {run_id}...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        info = json.loads(
            az_value(
                "pipelines", "runs", "show", "--id", run_id,
                "--org", org_url, "--project", project,
                echo=False,
            )
            or "{}"
        )  # fmt: skip
        if info.get("status") == "completed":
            save_pipeline_log(org_url, project, run_id)
            return info.get("result", "unknown")
        time.sleep(10)
    return "timed out"


def save_pipeline_log(org_url: str, project: str, run_id: str) -> None:
    """Save a finished pipeline run's log, every step's, to the run's log directory.

    Reads the build logs REST endpoint through `az devops invoke`; a pipeline run's
    ID is its build ID. A log that can't be read is noted, not fatal.
    """
    scope = (
        "--area", "build", "--resource", "logs", "--org", org_url,
        "--api-version", "7.1", "-o", "json",
    )  # fmt: skip
    route = ("--route-parameters", f"project={project}", f"buildId={run_id}")
    try:
        logs = json.loads(
            az_value("devops", "invoke", *scope, *route, echo=False) or "{}"
        ).get("value", [])
        parts = []
        for entry in logs:
            lines = json.loads(
                az_value(
                    "devops", "invoke", *scope, *route, f"logId={entry['id']}",
                    echo=False,
                )
                or "{}"
            ).get("value", [])  # fmt: skip
            parts.append(f"===== log {entry['id']} =====\n" + "\n".join(lines))
        save_log(f"pipeline-run-{run_id}.log", "\n".join(parts) + "\n")
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as error:
        print(f"Couldn't save the log for pipeline run {run_id}: {error}")


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

    A push-triggered Azure Pipeline run doesn't always register immediately:
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


def provision_test_secrets(
    org_url: str,
    project: str,
    repo_name: str,
    github_token: str,
    *,
    names: tuple[str, ...] = PIPELINE_DISPLAY_NAMES,
) -> None:
    """Set APPRISE_URL and GITHUB_COM_TOKEN on every pipeline that uses them.

    Mirrors `mise run provision-secrets`'s own `az pipelines variable create` calls
    (see mise.toml.jinja); each pipeline needs its own copy, since Azure Pipelines
    variables are scoped per-pipeline, not project-wide the way GitHub secrets are.
    APPRISE_URL points at a real, harmless HTTPS endpoint, not a fake host, so a
    pipeline that sends a notification doesn't fail on an unrelated delivery error.
    The token goes through az's AZURE_DEVOPS_EXT_PIPELINE_VAR_* environment variable,
    never the command line, so it's never echoed.
    """
    for pipeline in (name for name in names if name in APPRISE_PIPELINES):
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
    for pipeline in names:
        run(
            "az", "pipelines", "variable", "create",
            "--name", "GITHUB_COM_TOKEN",
            "--pipeline-name", f"[{repo_name}] {pipeline}",
            "--secret", "true",
            "--org", org_url,
            "--project", project,
            capture=True,
            env={"AZURE_DEVOPS_EXT_PIPELINE_VAR_GITHUB_COM_TOKEN": github_token},
        )  # fmt: skip


def run_monthly_maintenance_job(
    org_url: str,
    project: str,
    repo_name: str,
    job: str,
    *,
    names: tuple[str, ...] = PIPELINE_DISPLAY_NAMES,
    legacy: str = "",
    branch: str | None = None,
) -> str:
    """Run one of Monthly Maintenance's jobs alone, or the legacy pipeline it replaced.

    Returns:
        The run's result.

    """
    if MONTHLY_MAINTENANCE in names:
        pipeline, parameters = MONTHLY_MAINTENANCE, {"job": job}
    else:
        pipeline, parameters = legacy, None
    run_id = dispatch_pipeline(
        org_url,
        project,
        f"[{repo_name}] {pipeline}",
        parameters=parameters,
        branch=branch,
    )
    return wait_for_pipeline_run(org_url, project, run_id)


def check_copier_update_check(
    org_url: str,
    project: str,
    repo_name: str,
    failures: list[str],
    *,
    names: tuple[str, ...] = PIPELINE_DISPLAY_NAMES,
    branch: str | None = None,
) -> None:
    """Run Monthly Maintenance's Copier Update Check job and confirm it succeeds.

    Doesn't check whether it correctly detected an update either way; see this
    module's own docstring for why that stays manual on this platform.
    """
    on = f" on {branch}" if branch else ""
    step(f"Checking Maint (Auto) - Monthly Maintenance's Copier Update Check{on}")
    result = run_monthly_maintenance_job(
        org_url,
        project,
        repo_name,
        "copier_update_check",
        names=names,
        legacy="Maint (Auto) - Copier Update Check",
        branch=branch,
    )
    check(
        failures,
        f"Copier Update Check job succeeds{on}",
        result == "succeeded",
        result,
    )


def check_noop_update(dest: str, vcs_ref: str, failures: list[str]) -> None:
    """Run `copier update` against an already-current repo and confirm it's a no-op.

    `--defaults` is safe here: nothing changed since this repo was copied, so no
    template diff can add a question for it to answer silently, as it could for Repo B.

    `vcs_ref` must match what `create()` used. Without an explicit ref, `copier update`
    and `check-update` resolve the latest tag. With no tag at the commit under test,
    copier makes up a `git describe`-style version and passes it to `git clone --branch`
    as if it were a ref, which fails.
    """
    step("Checking `copier update` is a no-op on an already-current repo")
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


def check_repo_health_check(
    org_url: str, project: str, repo_name: str, failures: list[str]
) -> None:
    """Run Monthly Maintenance's Repo Health Check job and confirm it passes."""
    step("Checking Maint (Auto) - Monthly Maintenance's Repo Health Check")
    result = run_monthly_maintenance_job(
        org_url, project, repo_name, "repo_health_check"
    )
    check(failures, "Repo Health Check job succeeds", result == "succeeded", result)


def github_token() -> str:
    """Read the GitHub token a full run needs, before it creates anything.

    Every pipeline's mise install downloads tools from github.com, whose
    unauthenticated rate limit hosted agents share by IP, and Renovate skips every
    dependency hosted there without one.

    Returns:
        The GITHUB_COM_TOKEN environment variable's value, or else `gh auth token`'s.

    Raises:
        SystemExit: if neither gives a token.

    """
    token = os.environ.get("GITHUB_COM_TOKEN", "")
    if not token and shutil.which("gh"):
        token = run(
            "gh", "auth", "token", check=False, capture=True, secret=True
        ).stdout.strip()
    if not token:
        runbook = docs_page_url(
            "maintaining/integration-testing/runbook-azdo.md", version="dev"
        )
        raise SystemExit(
            "Set GITHUB_COM_TOKEN to a GitHub token with no scopes, or log in with "
            f"`gh auth login`, first; see Before You Start in {runbook}."
        )
    return token


def check_renovate(
    org_url: str, project: str, repo_name: str, failures: list[str]
) -> None:
    """Run Monthly Maintenance's Renovate job and confirm it bumps an old dependency.

    Repo A's setup PR already lifted its Renovate schedule and pinned an old typos, so
    Renovate has something to bump whenever this runs. GitHub's counterpart is a manual
    check: Renovate there runs as an external GitHub App on its own cadence, not a
    dispatchable workflow.
    """
    step("Checking Maint (Auto) - Monthly Maintenance's Renovate")
    result = run_monthly_maintenance_job(org_url, project, repo_name, "renovate")
    check(failures, "Renovate job succeeds", result == "succeeded", result)
    prs = json.loads(
        az_value(
            "repos",
            "pr",
            "list",
            "--repository",
            repo_name,
            "--status",
            "active",
            "--org",
            org_url,
            "--project",
            project,
            "--query",
            "[].{title: title, branch: sourceRefName}",
        )
        or "[]"
    )
    check(
        failures,
        "Renovate opens a PR bumping typos",
        any(
            pr["branch"].startswith("refs/heads/renovate/")
            and "typos" in pr["title"].lower()
            for pr in prs
        ),
        f"active PRs: {[pr['title'] for pr in prs]}",
    )


def wait_for_pr_policy(
    org_url: str, project: str, pr_id: str, *, timeout: int = 900
) -> str:
    """Poll a PR's build-validation policy until it settles past queued/running.

    The timeout matches wait_for_pipeline_run()'s: PR Validation can wait in the queue
    behind other runs, such as the ones a release merge starts, since a free Azure
    DevOps organization gets one parallel job. `az repos pr policy list` takes no
    `--project`; a PR ID is unique within the whole organization, not scoped
    per-project the way a repo name is.

    Returns:
        The joined set of distinct settled statuses (e.g. "approved" or "rejected").
        After `timeout` seconds, "timed out" and the last statuses seen, or "timed out
        (no build evaluation)" if PR Validation never started.

    """
    print(f"Waiting for PR {pr_id}'s build validation policy...")
    statuses: set[str] = set()
    deadline = time.time() + timeout
    while time.time() < deadline:
        evaluations = json.loads(
            az_value(
                "repos", "pr", "policy", "list", "--id", pr_id, "--org", org_url,
                echo=False,
            )
            or "[]"
        )  # fmt: skip
        build_evals = [
            e
            for e in evaluations
            if e.get("configuration", {}).get("type", {}).get("displayName") == "Build"
        ]
        statuses = {e.get("status") for e in build_evals}
        if statuses and not statuses & {"queued", "running"}:
            for build_id in {
                e.get("context", {}).get("buildId") for e in build_evals
            } - {None}:
                save_pipeline_log(org_url, project, str(build_id))
            return "/".join(sorted(statuses))
        time.sleep(10)
    if not statuses:
        return "timed out (no build evaluation)"
    return f"timed out ({'/'.join(sorted(statuses))})"


def assert_pr_blocked(
    org_url: str, project: str, pr_id: str, reason: str, failures: list[str]
) -> None:
    """Poll a PR's build-validation policy evaluation and assert it's blocked."""
    status = wait_for_pr_policy(org_url, project, pr_id)
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
    filename: str = "",
    *,
    edit: Callable[[Path], None] | None = None,
) -> None:
    """Open a passing PR and merge it, the only way commits reach main.

    The PR adds a scratch file named `filename`, or makes `edit`'s changes instead.

    The branch policy rejects a direct `git push` to main, even from the project owner
    (TF402455, "Pushes to this branch are not permitted"). Merging a PR also matches how
    Release (Auto) - Prepare & Publish Release starts in practice: from the push Azure
    DevOps makes when a PR completes.

    Raises:
        SystemExit: if the PR's build validation policy isn't approved.

    """
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    run("git", "switch", "-c", branch, cwd=dest)
    if edit is None:
        Path(dest, filename).write_text(SCRATCH_FILE_CONTENT, newline="\n")
    else:
        edit(Path(dest))
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
    status = wait_for_pr_policy(org_url, project, pr_id)
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
        # Without this, Azure DevOps squash-merges with a generic "Merge pull request N
        # from <branch> into main" message instead of the PR title, as GitHub uses.
        # Knope reads Conventional Commits from those messages, so the merged commit
        # would lose its "fix:" or "feat:" prefix and stop counting toward a release:
        # create-prerelease-via-knope then fails with "No packages are ready to
        # release".
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
    step("Checking a bad-title PR fails Test (Auto) - PR Validation")
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
    assert_pr_blocked(org_url, project, pr_id, "a bad PR title", failures)
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
    step("Checking a PR with a failing test fails Test (Auto) - PR Validation")
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
    assert_pr_blocked(org_url, project, pr_id, "a failing test suite", failures)
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
    computed; unlike relying on "is a PR open at all" (one may already be open from
    the bootstrap-time v0.1.0 PR), it's the right signal for "did this merge
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
    (unlike GitHub's split prepare/publish workflows); one pipeline handles both the
    push-to-main prepare step and the merge-triggered publish step, telling them apart
    via its own API check.
    """
    step("Checking Release (Auto) - Prepare & Publish Release")
    pid = pipeline_numeric_id(
        org_url, project, f"[{repo_name}] Release (Auto) - Prepare & Publish Release"
    )

    # Absorb any copy-time churn on the release PR (the first runs after copy may each
    # touch it) with a throwaway merge before testing that a docs-only merge is a true
    # no-op; otherwise that churn gets misattributed to the commit under test.
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
    # "no PR is open" isn't the right no-op signal; what matters is that a
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
        # Nothing to release is a normal outcome the pipeline handles, so it succeeds.
        result == "succeeded",
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
        # The pipeline updates the existing release PR instead of opening a second one.
        result == "succeeded",
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
    status = wait_for_pr_policy(org_url, project, pr_id)
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
    """Exercise the release pipeline's prerelease runs; a label, a dup, a new label."""
    step("Checking Release (Auto) - Prepare & Publish Release's prerelease runs")
    name = f"[{repo_name}] {RELEASE}"

    # PrepareRelease refuses to run with nothing to bump; without a real commit
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
    """Verify Repo B's state after a human has updated it to HEAD.

    This is the second entry point (`--verify-update`): the update itself happens by
    hand, on your own schedule, so this script can't chain straight from creating the
    repo into checking it; see main()'s own docstring.
    """
    step(f"Checking {repo_name}'s update applied cleanly")
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
    # markers as any other git conflict; one grep catches both.
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
    merged = {
        f"[{repo_name}] {name}"
        for name in LEGACY_PIPELINE_DISPLAY_NAMES
        if name not in PIPELINE_DISPLAY_NAMES
    }
    check(
        failures,
        "the merged pipelines' old registrations are gone",
        not merged & pipeline_names,
        f"still registered: {merged & pipeline_names}",
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
    status = wait_for_pr_policy(org_url, project, pr_id)
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


def verify_update_target(args: argparse.Namespace) -> tuple[str, str]:
    """Resolve the Repo B that `--verify-update` checks: the one named, or the newest.

    Found from its clone, Repo B also sets `args.org` and `args.project`, since its
    origin names the ones it's in, over any --org/--project default.

    Returns:
        Repo B's repository name, and its local clone's path.

    Raises:
        SystemExit: if REPO comes without --local-path, there's nothing to find Repo B
            by, or its clone's origin isn't an Azure DevOps repo.

    """
    repo, local_path = args.verify_update, args.local_path
    if repo:
        if not local_path:
            raise SystemExit("--verify-update REPO requires --local-path too.")
        return repo, local_path
    if not local_path and not args.repo_prefix:
        raise SystemExit("--verify-update without REPO requires --repo-prefix.")
    local_path, origin = repo_b_clone(args.repo_prefix, "dev.azure.com", local_path)
    match = re.search(r"dev\.azure\.com/([^/]+)/([^/]+)/_git/([^/?#]+)", origin)
    if not match:
        raise SystemExit(f"Can't read an Azure DevOps repo from {origin}.")
    args.org, project, repo = match.groups()
    args.project = urllib.parse.unquote(project)
    say(f"Verifying Repo B: {repo} in {args.org}/{args.project}, at {local_path}")
    return repo, local_path


def main() -> None:
    """Create and verify two throwaway repos, each covering a different scenario.

    Both run every time, at HEAD, to verify a release candidate on main before a
    release. Repo A is a `copier copy` with `code_coverage` on, and every automated
    check runs against it. Repo B is a copy at the last stable tag with `code_coverage`
    off, for you to update to HEAD as the runbook's Repo B section says, then run
    `mise run migrate-azdo-pipeline-names` once the update merges. That's manual on
    purpose: running the commands a real user runs, prompts included, is how a new
    question's prompt gets seen as they'll see it. Both repos stay for inspection.

    After updating Repo B, rerun this script with `--verify-update` (or `mise run
    integration-test-verify-update-azdo`) to check the update; see the "Repo B" section
    of the Azure DevOps runbook.

    Raises:
        SystemExit: if `az` or its azure-devops extension aren't installed, if
            --org/--project are missing, or if any automated check failed (after
            printing every check's result; see check()).

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Copier template source URL")
    parser.add_argument("--repo-prefix", help="This repo's own name")
    parser.add_argument(
        "--leaf",
        action="store_true",
        help="The source is a leaf template, whose projects can't be templates.",
    )
    # `mise run integration-test-azdo` sets usage_org and usage_project from the flags
    # its `usage` field defines. mise passes them as environment variables instead of
    # templating them into the command line, which works in any shell (cmd.exe can't
    # parse POSIX `${var}` expansion). Run directly, the script reads the variables
    # those flags fall back to itself.
    parser.add_argument(
        "--org",
        default=os.environ.get("usage_org")
        or os.environ.get("INTEGRATION_TEST_AZDO_ORG"),
        help="Azure DevOps organization",
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("usage_project")
        or os.environ.get("INTEGRATION_TEST_AZDO_PROJECT"),
        help="Azure DevOps project",
    )
    # `mise run integration-test-verify-update-azdo` passes a bare --verify-update, and
    # its --repo flag, if given, as usage_repo.
    parser.add_argument(
        "--verify-update",
        metavar="REPO",
        nargs="?",
        const=os.environ.get("usage_repo", ""),
        help=(
            "Skip creating repos; instead verify REPO (repository name) after you've "
            "updated it to HEAD yourself. Without REPO, it's read, with the org and "
            "project, from --local-path's origin, and without that, from the newest "
            "Repo B clone, which needs --repo-prefix."
        ),
    )
    parser.add_argument(
        "--local-path",
        default=os.environ.get("usage_local_path"),
        help="Local clone path for --verify-update (printed when Repo B was created).",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help=(
            "Skip creating repos; instead delete every test repo a run made (finished "
            "or not), after confirming. Requires --repo-prefix."
        ),
    )
    parser.add_argument(
        "--yes", action="store_true", help="Don't ask before --cleanup deletes."
    )
    args = parser.parse_args()
    log_dir = start_log("azdo")
    say(f"Logging this run to {log_dir}")

    check_az_installed()
    check_azure_devops_extension()

    if args.verify_update is not None:
        repo, local_path = verify_update_target(args)

    if not args.org or not args.project:
        raise SystemExit(
            "--org/--project are required. Pass them, or set "
            "INTEGRATION_TEST_AZDO_ORG and INTEGRATION_TEST_AZDO_PROJECT, such as in "
            "mise.local.toml's [env]."
        )

    org_url = f"https://dev.azure.com/{args.org}/"
    check_access(org_url, args.project)

    if args.cleanup:
        if not args.repo_prefix:
            raise SystemExit("--cleanup requires --repo-prefix.")
        cleanup(org_url, args.project, args.repo_prefix, yes=args.yes)
        return

    if args.verify_update is not None:
        update_failures: list[str] = []
        check_post_update(org_url, args.project, repo, local_path, update_failures)
        summary(
            [
                RepoResult(
                    "Repo B",
                    repo,
                    local_path,
                    update_failures,
                    url=repo_url(org_url, args.project, repo),
                )
            ]
        )
        if update_failures:
            raise SystemExit(1)
        return

    if not args.source or not args.repo_prefix:
        raise SystemExit("--source and --repo-prefix are required.")
    token = github_token()

    timestamp = int(time.time())

    heading("Repo A: a fresh copy at HEAD (code_coverage: on)")
    repo_a_name = f"{args.repo_prefix}-integration-test-{timestamp}-a"
    dest_a = local_clone_dir(repo_a_name)
    step(f"Creating {repo_a_name} at HEAD")
    checklist_a = create(
        args.source,
        "HEAD",
        repo_a_name,
        dest_a,
        args.org,
        args.project,
        code_coverage=True,
        leaf=args.leaf,
    )
    failures_a: list[str] = []
    verify(repo_a_name, org_url, args.project, failures_a)
    step("Setting test secrets")
    provision_test_secrets(org_url, args.project, repo_a_name, token)
    step("Merging Repo A's setup PR")
    # Before the checks that depend on it: the Renovate edits, and a lychee exclusion
    # for this template's docs, whose new pages publish only when it releases.
    open_pr_wait_and_merge(
        org_url,
        args.project,
        repo_a_name,
        dest_a,
        "integration-test/setup",
        "chore: set up Repo A for the integration test",
        edit=prepare_repo_a(args.source),
    )
    check_copier_update_check(org_url, args.project, repo_a_name, failures_a)
    check_noop_update(dest_a, "HEAD", failures_a)
    check_repo_health_check(org_url, args.project, repo_a_name, failures_a)
    check_bad_title_blocks_merge(org_url, args.project, repo_a_name, dest_a, failures_a)
    check_failing_tests_block_merge(
        org_url, args.project, repo_a_name, dest_a, failures_a
    )
    check_release_flow(org_url, args.project, repo_a_name, dest_a, failures_a)
    check_prerelease_flow(org_url, args.project, repo_a_name, dest_a, failures_a)
    # Last: Renovate's PR starts more PR Validation runs, which would queue ahead of
    # the checks above.
    check_renovate(org_url, args.project, repo_a_name, failures_a)

    old_ref = latest_stable_tag(args.source)
    heading(
        f"Repo B: a copy at {old_ref}, for you to update by hand (code_coverage: off)"
    )
    repo_b_name = f"{args.repo_prefix}-integration-test-{timestamp}-b"
    dest_b = local_clone_dir(repo_b_name)
    step(f"Creating {repo_b_name} at {old_ref}")
    checklist_b = create(
        args.source,
        old_ref,
        repo_b_name,
        dest_b,
        args.org,
        args.project,
        code_coverage=False,
        leaf=args.leaf,
    )
    failures_b: list[str] = []
    names_b = pipeline_display_names(dest_b)
    verify(repo_b_name, org_url, args.project, failures_b, names=names_b)
    step("Setting test secrets")
    provision_test_secrets(org_url, args.project, repo_b_name, token, names=names_b)
    if setup_b := prepare_repo_b(args.source):
        step("Merging Repo B's setup PR")
        open_pr_wait_and_merge(
            org_url,
            args.project,
            repo_b_name,
            dest_b,
            "integration-test/setup",
            "chore: set up Repo B for the integration test",
            edit=setup_b,
        )
    # Repo B is at the newest release, so main has no update; a branch recording
    # the commit before that release does. The runbook reads each run's result.
    check_copier_update_check(
        org_url, args.project, repo_b_name, failures_b, names=names_b
    )
    step("Pushing a branch that records an older template version")
    older = push_older_recorded_version(dest_b, args.source, old_ref)
    check_copier_update_check(
        org_url, args.project, repo_b_name, failures_b, names=names_b, branch=older
    )
    # The runbook as of main, which this run tests; latest is the last release's.
    runbook = docs_page_url(
        "maintaining/integration-testing/runbook-azdo.md", version="dev"
    )
    summary(
        [
            RepoResult(
                "Repo A",
                repo_a_name,
                dest_a,
                failures_a,
                checklist_a,
                url=repo_url(org_url, args.project, repo_a_name),
            ),
            RepoResult(
                f"Repo B (at {old_ref}, before updating)",
                repo_b_name,
                dest_b,
                failures_b,
                checklist_b,
                url=repo_url(org_url, args.project, repo_b_name),
            ),
        ],
        runbook,
    )

    if failures_a or failures_b:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit("\nStopped. Run cleanup to delete what this run created.")

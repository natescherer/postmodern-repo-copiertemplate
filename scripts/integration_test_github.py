"""Create two throwaway repos from this template and verify them.

Run it with `mise run integration-test-gh`. It works through your own gh and Git
Credential Manager sessions, and leaves both repos for you to inspect and delete. The
script itself isn't templated: the task passes this repo's source URL and name as
arguments.

It always runs against HEAD, to verify a release candidate on main before a release.
Each run creates two repos with different answers, to cover more combinations. Repo A
is a `copier copy` with `zensical_target: GitHub Pages` and `code_coverage` on. Repo B
is a copy at the last stable tag with `zensical_target: docs-site Directory in Repo`
and `code_coverage` off, left for you to update to HEAD as the runbook's Repo B
section says; main()'s docstring says why that's manual.

Each check prints a PASS or FAIL line as it runs, and each repo gets a summary at the
end. A failure doesn't stop the run. It checks only what needs a real GitHub API call
or workflow run; `tests/` covers what a local render can (structure, Jinja and YAML
validity, links, nav).
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
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

# Default `gh auth login` scopes cover both; see the Secrets and Tokens docs page.
REQUIRED_SCOPES = ("repo", "workflow")

MONTHLY_MAINTENANCE = "maint-auto-monthlymaintenance.yml"

# The workflow Monthly Maintenance's Copier Update Check job replaced. Repo B starts at
# the last release, so it has this until you update it. Remove once the last release
# has Monthly Maintenance.
LEGACY_COPIER_UPDATE_CHECK = "maint-auto-copierupdatecheck.yml"

# The status check settings.yml.jinja's ruleset requires before a PR can merge: PR
# Validation's `tests` job.
REQUIRED_CHECK = "tests"

# Must match _tasks' project_description -d flag in create() below.
PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match .github/settings.yml.jinja's `labels:` list. The repo also keeps
# GitHub's default labels, which settings.yml leaves alone.
EXPECTED_LABELS = frozenset({"awaiting pr", "blocked"})

SCRATCH_FILE_CONTENT = "# Integration Test Scratch File\n\nSafe to ignore or delete.\n"


def gh_value(*args: str, echo: bool = True) -> str:
    """Run `gh <args>` and return its trimmed stdout.

    Returns:
        The command's stdout, stripped of surrounding whitespace.

    """
    return run("gh", *args, capture=True, echo=echo).stdout.strip()


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


def check_gh_installed() -> None:
    """Verify the `gh` CLI is resolvable on PATH.

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
    own X-OAuth-Scopes API response) as a human-readable "Token scopes: 'a', 'b'" line;
    there's no dedicated --json field for this, so this greps that line instead of
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
            f"{docs_page_url('reference/token-permissions.md')} for what this token "
            "needs."
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
    owner: str,
    zensical_target: str,
    *,
    code_coverage: bool,
    leaf: bool = False,
) -> None:
    """Run the template to create the test repo.

    `github_username` is set to the resolved `owner` instead of auto-detected from local
    git config. copier.yml.jinja templates `.github/settings.yml` (such as `homepage`)
    from `github_repo_owner`, which defaults to `github_username`, so an auto-detected
    value that differs from the account gh is logged in as would break verify() for an
    unrelated reason.

    `zensical_target` and `code_coverage` are explicit, so the two repos can cover
    different values instead of both getting each question's default.

    `--defaults` covers the questions without an explicit -d below (github_org and
    author_name); without it, copier prompts for them. Explicit -d values take priority
    over --defaults.
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
        *template_answers(leaf=leaf),
        "-d",
        "project_name=Integration Test",
        "-d",
        "project_visibility=Public",
        "-d",
        "license=MIT",
        "-d",
        "lifecycle=Pre-Alpha",
        "-d",
        f"zensical_target={zensical_target}",
        "-d",
        f"code_coverage={'true' if code_coverage else 'false'}",
        source,
        dest,
    )


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


def list_tags(repo: str) -> set[str]:
    """Return every tag currently pushed to `repo`.

    Returns:
        The set of tag names (annotated tags' dereferenced `^{}` duplicates dropped).

    """
    result = run(
        "git", "ls-remote", "--tags", f"https://github.com/{repo}", capture=True
    )
    tags = set()
    for line in result.stdout.splitlines():
        ref = line.rsplit("refs/tags/", 1)[-1]
        if not ref.endswith("^{}"):
            tags.add(ref)
    return tags


def latest_run_id(repo: str, workflow_file: str, *, event: str) -> str:
    """Return the most recent run's ID for a workflow and event, or "" if none exist.

    Filtering by event matters for a workflow with more than one trigger, such as
    release-auto-preparereleasepr.yml: a push from a merge and a manual dispatch each
    start a run, and either can be the newest.

    Returns:
        The run ID as a string, or "".

    """
    return gh_value(
        "run",
        "list",
        "--repo",
        repo,
        "--workflow",
        workflow_file,
        "--event",
        event,
        "--limit",
        "1",
        "--json",
        "databaseId",
        "-q",
        '.[0].databaseId // ""',
    )


def wait_for_new_run(
    repo: str, workflow_file: str, before_id: str, *, event: str, timeout: int = 60
) -> int:
    """Poll for a new run of `workflow_file` to appear after `before_id`.

    GitHub takes a few seconds to create a run after a dispatch or push, and there's
    no API to wait for that directly, so this just polls `gh run list` for a change.

    Returns:
        The new run's ID.

    Raises:
        SystemExit: if no new run appears within `timeout` seconds.

    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = latest_run_id(repo, workflow_file, event=event)
        if current and current != before_id:
            return int(current)
        time.sleep(5)
    raise SystemExit(f"Timed out waiting for a new run of {workflow_file} in {repo}")


def dispatch_workflow(
    repo: str,
    workflow_file: str,
    *,
    inputs: dict[str, str] | None = None,
    ref: str | None = None,
) -> int:
    """Dispatch a workflow_dispatch workflow and return the resulting run's ID.

    Returns:
        The new run's ID.

    """
    before = latest_run_id(repo, workflow_file, event="workflow_dispatch")
    args = ["gh", "workflow", "run", workflow_file, "--repo", repo]
    if ref:
        args += ["--ref", ref]
    for key, value in (inputs or {}).items():
        args += ["-f", f"{key}={value}"]
    run(*args)
    return wait_for_new_run(repo, workflow_file, before, event="workflow_dispatch")


def open_pr_wait_and_merge(
    repo: str,
    dest: str,
    branch: str,
    commit_message: str,
    filename: str = "",
    *,
    edit: Callable[[Path], None] | None = None,
) -> str:
    """Open a passing PR and merge it, the only way commits reach main.

    The PR adds a scratch file named `filename`, or makes `edit`'s changes instead.

    Branch protection requires every change to go through a PR, even from the repo
    owner, so a direct `git push` to main is rejected. Merging a PR also matches how
    release-auto-preparereleasepr.yml starts in practice: from the push GitHub makes
    when a PR merges.

    Returns:
        The ID of the workflow run behind the PR's REQUIRED_CHECK.

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
    pr_url = gh_value(
        "pr",
        "create",
        "--repo",
        repo,
        "--head",
        branch,
        "--base",
        "main",
        "--title",
        commit_message,
        "--body",
        "Integration test.",
    )
    pr_number = pr_url.rstrip("/").rsplit("/", 1)[-1]
    checks = wait_for_pr_checks(repo, pr_number)
    merge_pr(repo, pr_number)
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    return next(
        match[1]
        for c in checks
        if c.get("name") == REQUIRED_CHECK
        and (match := re.search(r"/actions/runs/(\d+)/", c.get("detailsUrl") or ""))
    )


def wait_for_pr_checks(repo: str, pr_number: str) -> list[dict]:
    """Poll a PR's workflow checks until they all complete, and confirm they passed.

    Only GitHub Actions checks (those with a workflowName) count. Another app's checks,
    such as Codecov's, aren't required to merge and can stay in progress indefinitely,
    as Codecov's did on a new repo's setup PR. check_coverage_upload() covers the
    upload itself.

    Two force-pushes in quick succession can leave a `CANCELLED` entry beside the newer
    run for the same check name, since `test-auto-prvalidation.yml`'s concurrency group
    cancels the superseded run. Only each check name's latest entry reflects the PR, so
    older duplicates are dropped.

    That isn't enough on its own: a cancelled run can show as COMPLETED before its
    replacement even appears, and the two have completed within the same second. So an
    "all complete" result counts only once the same snapshot shows on two polls in a
    row, which gives a new replacement run time to appear. It also needs REQUIRED_CHECK
    among them: a run still queued for a runner hasn't reported yet, and the ruleset
    won't let the PR merge without it.

    Returns:
        Each check's latest status, as `gh pr view --json statusCheckRollup` gives it.

    Raises:
        SystemExit: if the checks don't all complete in time, or don't all pass.

    """
    print(f"Waiting for PR {pr_number}'s checks in {repo}...")
    latest: list[dict] = []
    stable = False
    for _ in range(90):
        rollup = json.loads(
            gh_value(
                "pr", "view", pr_number, "--repo", repo, "--json", "statusCheckRollup",
                echo=False,
            )
        )["statusCheckRollup"]  # fmt: skip
        latest_by_name: dict[str, dict] = {}
        for status_check in rollup:
            if not status_check.get("workflowName"):
                continue
            name = status_check.get("name")
            existing = latest_by_name.get(name)
            if existing is None or (status_check.get("completedAt") or "") >= (
                existing.get("completedAt") or ""
            ):
                latest_by_name[name] = status_check
        new_latest = list(latest_by_name.values())
        all_complete = any(c.get("name") == REQUIRED_CHECK for c in new_latest) and all(
            c.get("status") == "COMPLETED" for c in new_latest
        )
        if all_complete and stable and new_latest == latest:
            latest = new_latest
            break
        stable = all_complete
        latest = new_latest
        time.sleep(10)
    for run_id in {
        match[1]
        for c in latest
        if (match := re.search(r"/actions/runs/(\d+)/", c.get("detailsUrl") or ""))
    }:
        save_run_log(repo, run_id)
    if not latest or not all(c.get("conclusion") == "SUCCESS" for c in latest):
        raise SystemExit(f"PR {pr_number} in {repo} didn't pass its checks: {latest!r}")
    return latest


def merge_pr(repo: str, pr_number: str) -> None:
    """Squash-merge a PR whose checks passed.

    Raises:
        SystemExit: if GitHub refuses the merge, with its reason.

    """
    result = run(
        "gh", "pr", "merge", pr_number, "--repo", repo, "--squash", "--delete-branch",
        check=False, capture=True,
    )  # fmt: skip
    if result.returncode:
        reason = (result.stderr or result.stdout).strip()
        raise SystemExit(f"Couldn't merge PR {pr_number} in {repo}: {reason}")


def save_run_log(repo: str, run_id: int | str) -> None:
    """Save a finished workflow run's full log to the run's log directory."""
    log = run(
        "gh", "run", "view", str(run_id), "--repo", repo, "--log",
        check=False, capture=True, echo=False,
    )  # fmt: skip
    save_log(f"{repo.rsplit('/', 1)[-1]}-run-{run_id}.log", log.stdout)


def wait_for_run(repo: str, run_id: int, *, timeout: int = 1800) -> str:
    """Wait for a run to finish, save its log, and return its conclusion.

    Polls quietly instead of `gh run watch`, whose live display would flood the run's
    log. The caller decides which conclusion it wanted: some runs, such as a
    deliberately broken PR's, are meant to fail.

    Returns:
        The run's conclusion, e.g. "success" or "failure"; "timed out" if `timeout`
        seconds pass without the run completing.

    """
    print(f"Waiting for run {run_id} in {repo}...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        info = json.loads(
            gh_value(
                "run", "view", str(run_id), "--repo", repo,
                "--json", "status,conclusion",
                echo=False,
            )
            or "{}"
        )  # fmt: skip
        if info.get("status") == "completed":
            save_run_log(repo, run_id)
            return info.get("conclusion", "unknown")
        time.sleep(10)
    return "timed out"


def step_conclusion(repo: str, run_id: int, step_name: str) -> str | None:
    """Find one named step's conclusion across every job in a run.

    Returns:
        The step's conclusion (e.g. "success", "skipped"), or None if no step by that
        name is found.

    """
    jobs = json.loads(
        gh_value("run", "view", str(run_id), "--repo", repo, "--json", "jobs")
    )["jobs"]
    for job in jobs:
        for job_step in job["steps"]:
            if job_step["name"] == step_name:
                return job_step["conclusion"]
    return None


def report_settings_checks(
    repo: str, homepage: str, failures: list[str], *, zensical_ghpages: bool
) -> None:
    """Report each part of .github/settings.yml the copy should have applied.

    Covers the `repository`, `actions`, `labels`, `rulesets`, and `environments`
    blocks; every top-level key that file sets, not just a sample of them. verify()
    checks `pages`. The `github-pages` environment only exists when `zensical_ghpages`
    is true: settings.yml.jinja only declares it in that case.
    """
    repo_data = json.loads(
        run("gh", "api", f"repos/{repo}", check=False, capture=True).stdout or "{}"
    )
    check(
        failures,
        "repo description matches settings.yml",
        repo_data.get("description") == PROJECT_DESCRIPTION,
    )
    check(
        failures,
        "repo homepage matches settings.yml",
        (repo_data.get("homepage") or "") == homepage,
        f"got {repo_data.get('homepage')!r}, expected {homepage!r}",
    )
    check(
        failures,
        "delete_branch_on_merge is set",
        repo_data.get("delete_branch_on_merge") is True,
    )

    labels = run(
        "gh",
        "api",
        f"repos/{repo}/labels",
        "--jq",
        ".[].name",
        check=False,
        capture=True,
    )
    check(
        failures,
        "settings.yml's labels exist",
        EXPECTED_LABELS <= set(labels.stdout.splitlines()),
    )

    rulesets = run(
        "gh",
        "api",
        f"repos/{repo}/rulesets",
        "--jq",
        ".[].name",
        check=False,
        capture=True,
    )
    check(
        failures,
        "default-branch-protection ruleset exists",
        "default-branch-protection" in rulesets.stdout.split(),
    )

    workflow_permissions = json.loads(
        run(
            "gh",
            "api",
            f"repos/{repo}/actions/permissions/workflow",
            check=False,
            capture=True,
        ).stdout
        or "{}"
    )
    check(
        failures,
        "workflows can open pull requests",
        workflow_permissions.get("can_approve_pull_request_reviews") is True,
        f"got {workflow_permissions!r}",
    )

    if not zensical_ghpages:
        return
    environments = run(
        "gh",
        "api",
        f"repos/{repo}/environments",
        "--jq",
        "[.environments[].name]",
        check=False,
        capture=True,
    )
    check(
        failures,
        "github-pages environment exists",
        "github-pages" in json.loads(environments.stdout or "[]"),
    )


def verify(
    repo: str, dest: str, failures: list[str], *, zensical_ghpages: bool
) -> None:
    """Assert the created repo's real remote state matches what repo setup should do.

    `zensical_ghpages` gates the Pages-specific check: GitHub Pages is only enabled
    (and `/pages` only returns anything) when the repo was created with
    `zensical_target: GitHub Pages`. A copy at a release before gh-settings skips the
    settings checks: that release relied on the Settings GitHub App, which the upgrade
    guide has users remove, so check_post_update() checks them once
    `mise run sync-repo-settings` has applied the updated file.

    Raises:
        SystemExit: only if the repo itself can't be found; every other assertion
            is recorded via check() instead, since a real value here doesn't prevent
            the rest of this script's checks from being meaningful.

    """
    step(f"Verifying {repo}")
    repo_view = run(
        "gh", "repo", "view", repo, "--json", "visibility", check=False, capture=True
    )
    if repo_view.returncode != 0:
        raise SystemExit(f"Repo {repo!r} not found; did create() fail?")
    visibility = json.loads(repo_view.stdout)["visibility"]
    check(
        failures,
        "repo visibility is Public",
        visibility == "PUBLIC",
        f"got {visibility!r}",
    )

    if zensical_ghpages:
        pages_build_type = gh_value("api", f"repos/{repo}/pages", "-q", ".build_type")
        check(
            failures,
            "GitHub Pages build_type is workflow",
            pages_build_type == "workflow",
            f"got {pages_build_type!r}",
        )
        unrestricted = gh_value(
            "api",
            f"repos/{repo}/environments/github-pages",
            "-q",
            ".deployment_branch_policy == null",
        )
        check(
            failures,
            "github-pages environment has no deployment branch restriction",
            unrestricted == "true",
            f"got {unrestricted!r}",
        )

    run("gh", "api", f"repos/{repo}/contents/.github/workflows", capture=True)

    # The copy's gh-settings task applies .github/settings.yml before create() returns.
    if not uses_gh_settings(dest):
        say(
            "  [SKIP] settings.yml checks: this release applied it with the Settings "
            "GitHub App; they run after the update, once sync-repo-settings applies it"
        )
        return
    report_settings_checks(
        repo, settings_homepage(dest), failures, zensical_ghpages=zensical_ghpages
    )


def uses_gh_settings(dest: str) -> bool:
    """Check whether a repo's .github/settings.yml is in gh-settings' format.

    Releases before gh-settings wrote one for the Settings GitHub App instead; only
    gh-settings' format has a `version: 1` line.

    Returns:
        True if gh-settings applies the file.

    """
    text = Path(dest, ".github", "settings.yml").read_text(encoding="utf-8")
    return re.search(r"(?m)^version: 1$", text) is not None


def publishes_to_ghpages(dest: str) -> bool:
    """Check whether a repo was copied with `zensical_target: GitHub Pages`.

    Returns:
        True if its copier-answers.yml records that answer.

    """
    text = Path(dest, ".config", "copier-answers.yml").read_text(encoding="utf-8")
    return re.search(r"(?m)^zensical_target: GitHub Pages$", text) is not None


def settings_homepage(dest: str) -> str:
    """Read the homepage a repo's own .github/settings.yml sets.

    Reading it, not computing it, keeps verify() right for a repo copied at any
    release, since the template has changed what it sets.

    Returns:
        The homepage, or "" if settings.yml sets none.

    """
    text = Path(dest, ".github", "settings.yml").read_text(encoding="utf-8")
    match = re.search(r'(?m)^\s+homepage:\s*"?([^"\n]*?)"?\s*$', text)
    return match[1] if match else ""


def codecov_token() -> str:
    """Read the Codecov upload token a full run needs, before it creates anything.

    A new repo has no per-repo Codecov token yet, so this needs a Codecov global upload
    token.

    Returns:
        The CODECOV_TOKEN environment variable's value.

    Raises:
        SystemExit: if CODECOV_TOKEN isn't set.

    """
    token = os.environ.get("CODECOV_TOKEN", "")
    if not token:
        runbook = docs_page_url(
            "maintaining/integration-testing/runbook-github.md", version="dev"
        )
        raise SystemExit(
            "Set CODECOV_TOKEN to your Codecov global upload token first; see Before "
            f"You Start in {runbook}."
        )
    return token


def provide_codecov_token(repo: str, token: str) -> None:
    """Set the CODECOV_TOKEN secret on `repo`.

    The value goes to `gh secret set` on stdin, never its command line, and isn't
    logged.
    """
    run(
        "gh", "secret", "set", "CODECOV_TOKEN", "--repo", repo,
        capture=True, secret=True, stdin=token,
    )  # fmt: skip


def check_coverage_upload(repo: str, run_id: str, failures: list[str]) -> None:
    """Confirm a PR Validation run uploaded coverage.xml, and Codecov accepted it.

    The upload step runs only when coverage.xml exists, and Repo A's setup PR commits a
    fixture. The step passes even when Codecov rejects the upload, since it doesn't fail
    CI on an upload error, so acceptance is read from the uploader's own log line.
    """
    step("Checking PR Validation uploads coverage.xml")
    conclusion = step_conclusion(repo, int(run_id), "Upload Coverage to Codecov")
    check(
        failures,
        "PR Validation runs the Codecov upload",
        conclusion == "success",
        f"run {run_id}'s upload step conclusion was {conclusion!r}",
    )
    log = run(
        "gh", "run", "view", run_id, "--repo", repo, "--log",
        check=False, capture=True, echo=False,
    ).stdout  # fmt: skip
    check(
        failures,
        "Codecov accepts the upload",
        "Upload queued for processing complete" in log,
        f"run {run_id}'s log has no 'Upload queued for processing complete'",
    )


def provision_test_secrets(repo: str) -> None:
    """Set placeholder secrets so pipelines gated on their presence can run.

    APPRISE_URL: Monthly Maintenance's Copier Update Check requires it to exist before
    its own logic even runs (see .github/actions/require-secrets). Points at a real,
    harmless HTTPS endpoint, not a fake host, so the "Notify if Update is Available"
    step, when it does run, doesn't fail the whole workflow on an unrelated delivery
    error.
    """
    run(
        "gh",
        "secret",
        "set",
        "APPRISE_URL",
        "--repo",
        repo,
        "--body",
        "json://httpbin.org/post",
    )


def approve_pending_run(repo: str, branch: str, *, timeout: int = 60) -> None:
    """Approve a pull_request run on `branch` waiting in GitHub's action_required state.

    A push as the default GITHUB_TOKEN (github-actions[bot]) to a PR it opened or
    updated leaves that PR's pull_request runs waiting for approval in the Actions tab,
    as when Release (Auto): Prepare Release PR adds a commit to the release PR.
    Approving through the API does what a maintainer does by clicking "Approve and run
    workflow". It polls briefly, since the run may not exist yet when the push
    completes.

    Raises:
        SystemExit: if no action_required run appears on `branch` within `timeout`.

    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        runs = json.loads(
            gh_value(
                "run",
                "list",
                "--repo",
                repo,
                "--branch",
                branch,
                "--json",
                "databaseId,conclusion",
            )
            or "[]"
        )
        for r in runs:
            if r.get("conclusion") == "action_required":
                run(
                    "gh",
                    "api",
                    "-X",
                    "POST",
                    f"repos/{repo}/actions/runs/{r['databaseId']}/approve",
                )
                return
        time.sleep(3)
    raise SystemExit(
        f"Timed out waiting for an action_required run on {branch} in {repo}"
    )


def monthly_maintenance_run(
    repo: str, job: str, *, legacy: str = "", ref: str | None = None
) -> int:
    """Dispatch one of Monthly Maintenance's jobs alone, or the workflow it replaced.

    Returns:
        The run's ID.

    """
    if legacy:
        return dispatch_workflow(repo, legacy, ref=ref)
    return dispatch_workflow(repo, MONTHLY_MAINTENANCE, inputs={"job": job}, ref=ref)


def check_copier_update_check(
    repo: str,
    failures: list[str],
    *,
    expect_update_available: bool,
    ref: str | None = None,
    legacy: bool = False,
) -> None:
    """Run Monthly Maintenance's Copier Update Check job and verify it ran correctly.

    `legacy` runs the separate Copier Update Check workflow of a release before Monthly
    Maintenance instead, as Repo B has until it's updated.

    Whether it detected a pending update is read from whether the "Notify if Update is
    Available" step ran (its own `if:` is gated on that) rather than by scraping log
    text for the third-party action's own output, which isn't a contract this script
    should depend on.
    """
    on = f" on {ref}" if ref else ""
    step(f"Checking Maint (Auto): Monthly Maintenance's Copier Update Check{on}")
    run_id = monthly_maintenance_run(
        repo,
        "copier_update_check",
        legacy=LEGACY_COPIER_UPDATE_CHECK if legacy else "",
        ref=ref,
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        f"Copier Update Check job succeeds{on}",
        conclusion == "success",
        conclusion,
    )
    notify_step = step_conclusion(repo, run_id, "Notify if Update is Available")
    # Whether the step ran (its `if:` checks update_available), not whether delivery
    # succeeded, so a failed notification doesn't look like "no update detected".
    detected_available = notify_step not in (None, "skipped")
    check(
        failures,
        "Copier Update Check reports "
        + (
            "an update is available"
            if expect_update_available
            else "no update available"
        )
        + on,
        detected_available == expect_update_available,
        f"'Notify if Update is Available' step conclusion was {notify_step!r}",
    )


def check_noop_update(dest: str, vcs_ref: str, failures: list[str]) -> None:
    """Run `copier update` against an already-current repo and confirm it's a no-op.

    `--defaults` is safe here: nothing changed since this repo was copied, so no
    template diff can add a question for it to answer silently, as it could for Repo B.

    `vcs_ref` must match what `create()` used. Without `--vcs-ref`, `copier update`
    targets the latest release tag, not HEAD. When main has commits past the last
    release, as it normally does, that's earlier than the version this repo was created
    at, and copier can't update backward.
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


def check_repo_health_check(repo: str, failures: list[str]) -> None:
    """Run Monthly Maintenance's Repo Health Check job and confirm it completes clean.

    workflow-keepalive is gated `if: github.event_name == 'schedule'`, so a manual
    dispatch here only exercises the link check; that's covered by the overall
    run conclusion.
    """
    step("Checking Maint (Auto): Monthly Maintenance's Repo Health Check")
    run_id = monthly_maintenance_run(repo, "repo_health_check")
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "Repo Health Check job succeeds",
        conclusion == "success",
        conclusion,
    )


def assert_pr_blocked(repo: str, pr_url: str, reason: str, failures: list[str]) -> str:
    """Poll a PR's checks to completion, then assert they failed and merge is blocked.

    Returns:
        The PR number, so the caller can close it afterward.

    """
    pr_number = pr_url.rstrip("/").rsplit("/", 1)[-1]
    rollup: list[dict] = []
    for _ in range(24):
        rollup = json.loads(
            gh_value(
                "pr", "view", pr_number, "--repo", repo, "--json", "statusCheckRollup"
            )
        )["statusCheckRollup"]
        if rollup and all(c.get("status") == "COMPLETED" for c in rollup):
            break
        time.sleep(10)
    check(
        failures,
        f"PR Validation fails on {reason}",
        any(c.get("conclusion") == "FAILURE" for c in rollup),
        f"statusCheckRollup={rollup!r}",
    )
    mergeable_state = gh_value(
        "pr",
        "view",
        pr_number,
        "--repo",
        repo,
        "--json",
        "mergeStateStatus",
        "-q",
        ".mergeStateStatus",
    )
    check(
        failures,
        f"branch protection blocks merging a PR with {reason}",
        mergeable_state in ("BLOCKED", "DIRTY", "BEHIND"),
        f"mergeStateStatus={mergeable_state!r}",
    )
    return pr_number


def check_bad_title_blocks_merge(repo: str, dest: str, failures: list[str]) -> None:
    """Open a PR with a non-Conventional-Commit title and confirm it's blocked."""
    step("Checking a bad-title PR fails Test (Auto): PR Validation")
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
    pr_url = gh_value(
        "pr",
        "create",
        "--repo",
        repo,
        "--head",
        branch,
        "--base",
        "main",
        "--title",
        title,
        "--body",
        "Integration test: expects PR Validation to fail on the title.",
    )
    pr_number = assert_pr_blocked(repo, pr_url, "a bad PR title", failures)
    run("gh", "pr", "close", pr_number, "--repo", repo, "--delete-branch")


def check_failing_tests_block_merge(repo: str, dest: str, failures: list[str]) -> None:
    """Open a PR with a deliberately failing test and confirm it's blocked."""
    step("Checking a PR with a failing test fails Test (Auto): PR Validation")
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
    pr_url = gh_value(
        "pr",
        "create",
        "--repo",
        repo,
        "--head",
        branch,
        "--base",
        "main",
        "--title",
        title,
        "--body",
        "Integration test: expects PR Validation to fail on the test suite.",
    )
    pr_number = assert_pr_blocked(repo, pr_url, "a failing test suite", failures)
    run("gh", "pr", "close", pr_number, "--repo", repo, "--delete-branch")


def knope_release_pr_title(repo: str) -> str | None:
    """Look up the open knope/release PR's title, if one is open.

    The title (e.g. "chore: prepare release 0.0.1") encodes the version knope
    computed; unlike the PR's head commit SHA, it doesn't change just because
    `autoupdate-knope-pr` recreates the branch from a fresh main HEAD every run, so
    it's the right signal for "did this merge change what's proposed."

    Returns:
        The PR title, or None if no such PR is currently open.

    """
    prs = json.loads(
        gh_value(
            "pr",
            "list",
            "--repo",
            repo,
            "--head",
            "knope/release",
            "--state",
            "open",
            "--json",
            "title",
        )
        or "[]"
    )
    return prs[0]["title"] if prs else None


def check_release_flow(repo: str, dest: str, failures: list[str]) -> None:
    """Exercise the real release flow: a no-op merge, then a real release and tag."""
    step("Checking Release (Auto): Prepare/Publish Release")

    # Absorb any copy-time churn on the release PR (the first runs after copy may each
    # touch it) with a throwaway merge before testing that a docs-only merge is a true
    # no-op; otherwise that churn gets misattributed to the commit under test.
    prepare_before = latest_run_id(
        repo, "release-auto-preparereleasepr.yml", event="push"
    )
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/warmup",
        "chore: integration test warmup commit",
        "INTEGRATION_TEST_WARMUP.md",
    )
    warmup_run_id = wait_for_new_run(
        repo, "release-auto-preparereleasepr.yml", prepare_before, event="push"
    )
    wait_for_run(repo, warmup_run_id)

    # A release PR may already be open here (e.g. the bootstrap-time v0.1.0 one), so
    # "no PR is open" isn't the right no-op signal; what matters is that a
    # docs-only merge doesn't change what version it proposes.
    docs_noop_before = knope_release_pr_title(repo)
    prepare_before = latest_run_id(
        repo, "release-auto-preparereleasepr.yml", event="push"
    )
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/docs-noop",
        "docs: integration test no-op commit",
        "INTEGRATION_TEST_DOCS.md",
    )
    run_id = wait_for_new_run(
        repo, "release-auto-preparereleasepr.yml", prepare_before, event="push"
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "a docs-only merge keeps the release workflow green",
        conclusion == "success",
        conclusion,
    )
    docs_noop_after = knope_release_pr_title(repo)
    check(
        failures,
        "a docs-only merge doesn't change the release PR's proposed version",
        docs_noop_after == docs_noop_before,
        f"before={docs_noop_before!r}, after={docs_noop_after!r}",
    )

    prepare_before = latest_run_id(
        repo, "release-auto-preparereleasepr.yml", event="push"
    )
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/feat",
        "feat: integration test feature",
        "INTEGRATION_TEST_FEAT.md",
    )
    run_id = wait_for_new_run(
        repo, "release-auto-preparereleasepr.yml", prepare_before, event="push"
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "a feat merge's release workflow succeeds",
        conclusion == "success",
        conclusion,
    )
    release_prs = json.loads(
        gh_value(
            "pr",
            "list",
            "--repo",
            repo,
            "--head",
            "knope/release",
            "--state",
            "open",
            "--json",
            "number,title",
        )
        or "[]"
    )
    check(failures, "a feat commit opens a release PR", bool(release_prs))
    if not release_prs:
        return
    pr_number, pr_title = release_prs[0]["number"], release_prs[0]["title"]
    check(
        failures,
        "release PR title looks like a version bump",
        bool(re.search(r"prepare release v?\d+\.\d+\.\d+", pr_title)),
        pr_title,
    )

    before_tags = list_tags(repo)
    publish_before = latest_run_id(
        repo, "release-auto-publishrelease.yml", event="pull_request"
    )
    zensical_before = latest_run_id(
        repo, "docs-auto-zensical.yml", event="workflow_dispatch"
    )
    approve_pending_run(repo, "knope/release")
    wait_for_pr_checks(repo, str(pr_number))
    merge_pr(repo, str(pr_number))
    run("git", "pull", cwd=dest)
    publish_run_id = wait_for_new_run(
        repo, "release-auto-publishrelease.yml", publish_before, event="pull_request"
    )
    conclusion = wait_for_run(repo, publish_run_id)
    check(
        failures,
        "merging the release PR publishes successfully",
        conclusion == "success",
        conclusion,
    )
    new_tags = list_tags(repo) - before_tags
    check(
        failures,
        "merging the release PR creates a new tag",
        bool(new_tags),
        f"before={before_tags}",
    )
    if new_tags:
        release_view = run(
            "gh",
            "release",
            "view",
            sorted(new_tags)[-1],
            "--repo",
            repo,
            check=False,
            capture=True,
        )
        check(
            failures,
            "a GitHub Release exists for the new tag",
            release_view.returncode == 0,
        )

        # Publish Release dispatches docs-auto-zensical.yml with the new tag (it
        # publishes the "latest" Pages docs alias): a release made with GITHUB_TOKEN
        # fires no `release` event. Wait for that run here so check_repo_health_check(),
        # which runs later, isn't racing a Pages deployment that hasn't happened yet.
        zensical_run_id = wait_for_new_run(
            repo, "docs-auto-zensical.yml", zensical_before, event="workflow_dispatch"
        )
        conclusion = wait_for_run(repo, zensical_run_id)
        check(
            failures,
            "publishing a release triggers the Pages docs deploy",
            conclusion == "success",
            conclusion,
        )


def check_prerelease_flow(repo: str, dest: str, failures: list[str]) -> None:
    """Exercise Prepare Release PR's prerelease runs; a label, a dup, a new label."""
    step("Checking Release (Auto): Prepare Release PR's prerelease runs")

    # PrepareRelease refuses to run with nothing to bump; without a real commit
    # since the last release, every dispatch below would fail with knope's own
    # "No packages are ready to release", not the behavior this is meant to check.
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/prerelease-fix",
        "fix: integration test prerelease commit",
        "INTEGRATION_TEST_PRERELEASE.md",
    )

    before = list_tags(repo)
    run_id = dispatch_workflow(
        repo, "release-auto-preparereleasepr.yml", inputs={"label": "alpha"}
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "dispatching an alpha prerelease succeeds",
        conclusion == "success",
        conclusion,
    )
    after_alpha = list_tags(repo)
    new_alpha = after_alpha - before
    check(
        failures,
        "an alpha prerelease creates a matching tag",
        any(re.search(r"-alpha\.\d+$", t) for t in new_alpha),
        f"new tags: {new_alpha}",
    )

    run_id = dispatch_workflow(
        repo, "release-auto-preparereleasepr.yml", inputs={"label": "alpha"}
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "re-dispatching the same label at the same commit is blocked",
        conclusion == "failure",
        conclusion,
    )

    run_id = dispatch_workflow(
        repo, "release-auto-preparereleasepr.yml", inputs={"label": "beta"}
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "dispatching a different label at the same commit succeeds",
        conclusion == "success",
        conclusion,
    )
    new_beta = list_tags(repo) - after_alpha
    check(
        failures,
        "a beta prerelease creates a matching tag",
        any(re.search(r"-beta\.\d+$", t) for t in new_beta),
        f"new tags: {new_beta}",
    )


def check_post_update(repo: str, dest: str, failures: list[str]) -> None:
    """Verify Repo B's state after a human has updated it to HEAD.

    This is the second entry point (`--verify-update`): the update itself happens by
    hand, on your own schedule, so this script can't chain straight from creating the
    repo into checking it; see main()'s own docstring.
    """
    step(f"Checking {repo}'s update applied cleanly")
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

    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    # The runbook has you run `mise run sync-repo-settings` once the update merges, as
    # the upgrade guide does: copy tasks don't run on update.
    report_settings_checks(
        repo,
        settings_homepage(dest),
        failures,
        zensical_ghpages=publishes_to_ghpages(dest),
    )
    branch = "integration-test/post-update-check"
    run("git", "switch", "-c", branch, cwd=dest)
    Path(dest, "INTEGRATION_TEST_POST_UPDATE.md").write_text(
        SCRATCH_FILE_CONTENT, newline="\n"
    )
    run("git", "add", "-A", cwd=dest)
    title = "chore: integration test post-update check"
    run("git", "commit", "-m", title, cwd=dest)
    run("git", "push", "-u", "origin", branch, cwd=dest)
    pr_url = gh_value(
        "pr",
        "create",
        "--repo",
        repo,
        "--head",
        branch,
        "--base",
        "main",
        "--title",
        title,
        "--body",
        "Integration test: confirms PR Validation still works after `copier update`.",
    )
    pr_number = pr_url.rstrip("/").rsplit("/", 1)[-1]
    rollup: list[dict] = []
    for _ in range(24):
        rollup = json.loads(
            gh_value(
                "pr", "view", pr_number, "--repo", repo, "--json", "statusCheckRollup"
            )
        )["statusCheckRollup"]
        if rollup and all(c.get("status") == "COMPLETED" for c in rollup):
            break
        time.sleep(10)
    check(
        failures,
        "PR Validation still triggers and passes after the update",
        bool(rollup) and all(c.get("conclusion") == "SUCCESS" for c in rollup),
        f"statusCheckRollup={rollup!r}",
    )
    merge_pr(repo, pr_number)


def cleanup(owner: str, repo_prefix: str, *, yes: bool) -> None:
    """Delete every test repo main() created under `owner`, and its local clone.

    It finds them by name, so it covers runs that stopped partway, such as when the
    machine slept, as well as finished ones. Deleting a GitHub repo removes its
    workflows too. It lists everything, then asks before deleting anything.

    Raises:
        SystemExit: if the gh token lacks the delete_repo scope, or a local
            clone can't be deleted.

    """
    pattern = test_repo_pattern(repo_prefix)
    repos = json.loads(
        gh_value("repo", "list", owner, "--limit", "1000", "--json", "name")
    )
    names = sorted(r["name"] for r in repos if pattern.fullmatch(r["name"]))
    clones = local_clones(pattern, "github.com")
    if not names and not clones:
        say(f"No integration-test repos under {owner}, and no local clones.")
        return
    say("Integration-test repos and local clones to delete:")
    for name in names:
        say(f"  {owner}/{name}")
    for clone in clones:
        say(f"  {clone}")
    if names:
        status = run("gh", "auth", "status", check=False, capture=True)
        if "'delete_repo'" not in status.stdout + status.stderr:
            raise SystemExit(
                "Deleting repos needs the delete_repo scope. Add it with "
                "`gh auth refresh -h github.com -s delete_repo`, then rerun."
            )
    if not confirm(
        f"Delete these {len(names)} repo(s) and {len(clones)} local clone(s)?", yes=yes
    ):
        say("Nothing deleted.")
        return
    for name in names:
        run("gh", "repo", "delete", f"{owner}/{name}", "--yes")
    deleted = remove_clones(clones)
    say(f"Deleted {len(names)} repo(s) and {deleted} local clone(s).")
    if deleted < len(clones):
        raise SystemExit(1)


def verify_update_target(args: argparse.Namespace) -> tuple[str, str]:
    """Resolve the Repo B that `--verify-update` checks: the one named, or the newest.

    Returns:
        Repo B's `owner/name`, and its local clone's path.

    Raises:
        SystemExit: if REPO comes without --local-path, there's nothing to find Repo B
            by, or its clone's origin isn't a GitHub repo.

    """
    repo, local_path = args.verify_update, args.local_path
    if repo:
        if not local_path:
            raise SystemExit("--verify-update REPO requires --local-path too.")
        return repo, local_path
    if not local_path and not args.repo_prefix:
        raise SystemExit("--verify-update without REPO requires --repo-prefix.")
    local_path, origin = repo_b_clone(args.repo_prefix, "github.com", local_path)
    match = re.search(r"github\.com[/:]([^/]+/[^/]+?)(?:\.git)?/?$", origin)
    if not match:
        raise SystemExit(f"Can't read a GitHub repo from {origin}.")
    say(f"Verifying Repo B: {match.group(1)}, cloned at {local_path}")
    return match.group(1), local_path


def main() -> None:
    """Create and verify two throwaway repos, each covering a different scenario.

    Both run every time, at HEAD, to verify a release candidate on main before a
    release. Repo A is a `copier copy` with `zensical_target: GitHub Pages` and
    `code_coverage` on, and every automated check runs against it. Repo B is a copy at
    the last stable tag with `zensical_target: docs-site Directory in Repo` and
    `code_coverage` off, for you to update to HEAD as the runbook's Repo B section says.
    That's manual on purpose: running the command a real user runs, prompts included,
    is how a new question's prompt gets seen as they'll see it. Both repos stay for
    inspection.

    After updating Repo B, rerun this script with `--verify-update` (or `mise run
    integration-test-verify-update-gh`) to check the update; see the "Repo B" section
    of the GitHub runbook.

    Raises:
        SystemExit: if required arguments are missing, or if any automated check
            failed (after printing every check's result; see check()).

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Copier template source URL")
    parser.add_argument("--repo-prefix", help="This repo's own name")
    parser.add_argument(
        "--leaf",
        action="store_true",
        help="The source is a leaf template, whose projects can't be templates.",
    )
    # `mise run integration-test-verify-update-gh` passes a bare --verify-update, and
    # its --repo flag, if given, as usage_repo.
    parser.add_argument(
        "--verify-update",
        metavar="REPO",
        nargs="?",
        const=os.environ.get("usage_repo", ""),
        help=(
            "Skip creating repos; instead verify REPO (owner/name) after you've "
            "updated it to HEAD yourself. Without REPO, it's read from --local-path's "
            "origin, and without that, from the newest Repo B clone, which needs "
            "--repo-prefix."
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
    log_dir = start_log("github")
    say(f"Logging this run to {log_dir}")

    check_gh_installed()
    check_scopes()

    if args.cleanup:
        if not args.repo_prefix:
            raise SystemExit("--cleanup requires --repo-prefix.")
        cleanup(
            gh_value("api", "user", "--jq", ".login"), args.repo_prefix, yes=args.yes
        )
        return

    if args.verify_update is not None:
        repo, local_path = verify_update_target(args)
        update_failures: list[str] = []
        check_post_update(repo, local_path, update_failures)
        summary(
            [
                RepoResult(
                    "Repo B",
                    repo,
                    local_path,
                    update_failures,
                    url=f"https://github.com/{repo}",
                )
            ]
        )
        if update_failures:
            raise SystemExit(1)
        return

    if not args.source or not args.repo_prefix:
        raise SystemExit("--source and --repo-prefix are required.")
    token = codecov_token()

    owner = gh_value("api", "user", "--jq", ".login")
    timestamp = int(time.time())

    heading(
        "Repo A: a fresh copy at HEAD "
        "(zensical_target: GitHub Pages, code_coverage: on)"
    )
    repo_a_name = f"{args.repo_prefix}-integration-test-{timestamp}-a"
    dest_a = local_clone_dir(repo_a_name)
    repo_a = f"{owner}/{repo_a_name}"
    step(f"Creating {repo_a} at HEAD")
    create(
        args.source,
        "HEAD",
        repo_a_name,
        dest_a,
        owner,
        "GitHub Pages",
        code_coverage=True,
        leaf=args.leaf,
    )
    failures_a: list[str] = []
    step("Setting test secrets")
    provision_test_secrets(repo_a)
    provide_codecov_token(repo_a, token)
    verify(repo_a, dest_a, failures_a, zensical_ghpages=True)
    step("Merging Repo A's setup PR")
    # Before the checks that depend on it: the Renovate edits, and a lychee exclusion
    # for this template's docs, whose new pages publish only when it releases.
    setup_run = open_pr_wait_and_merge(
        repo_a,
        dest_a,
        "integration-test/setup",
        "chore: set up Repo A for the integration test",
        edit=prepare_repo_a(args.source),
    )
    check_coverage_upload(repo_a, setup_run, failures_a)
    check_copier_update_check(repo_a, failures_a, expect_update_available=False)
    check_noop_update(dest_a, "HEAD", failures_a)
    check_bad_title_blocks_merge(repo_a, dest_a, failures_a)
    check_failing_tests_block_merge(repo_a, dest_a, failures_a)
    check_release_flow(repo_a, dest_a, failures_a)
    # Run last: a GitHub Pages repo's homepage link in README.md returns 404 until the
    # first Pages deployment propagates, which it has by this point.
    check_repo_health_check(repo_a, failures_a)
    check_prerelease_flow(repo_a, dest_a, failures_a)

    old_ref = latest_stable_tag(args.source)
    heading(
        f"Repo B: a copy at {old_ref}, for you to update by hand (zensical_target: "
        "docs-site Directory in Repo, code_coverage: off)"
    )
    repo_b_name = f"{args.repo_prefix}-integration-test-{timestamp}-b"
    dest_b = local_clone_dir(repo_b_name)
    repo_b = f"{owner}/{repo_b_name}"
    step(f"Creating {repo_b} at {old_ref}")
    create(
        args.source,
        old_ref,
        repo_b_name,
        dest_b,
        owner,
        "docs-site Directory in Repo",
        code_coverage=False,
        leaf=args.leaf,
    )
    step("Setting test secrets")
    provision_test_secrets(repo_b)
    failures_b: list[str] = []
    verify(repo_b, dest_b, failures_b, zensical_ghpages=False)
    if setup_b := prepare_repo_b(args.source):
        step("Merging Repo B's setup PR")
        open_pr_wait_and_merge(
            repo_b,
            dest_b,
            "integration-test/setup",
            "chore: set up Repo B for the integration test",
            edit=setup_b,
        )
    # Repo B is at the newest release, so main has no update; a branch recording
    # the commit before that release does.
    legacy_b = not Path(dest_b, ".github", "workflows", MONTHLY_MAINTENANCE).exists()
    check_copier_update_check(
        repo_b, failures_b, expect_update_available=False, legacy=legacy_b
    )
    step("Pushing a branch that records an older template version")
    older = push_older_recorded_version(dest_b, args.source, old_ref)
    check_copier_update_check(
        repo_b, failures_b, expect_update_available=True, ref=older, legacy=legacy_b
    )
    # The runbook as of main, which this run tests; latest is the last release's.
    runbook = docs_page_url(
        "maintaining/integration-testing/runbook-github.md", version="dev"
    )
    summary(
        [
            RepoResult(
                "Repo A", repo_a, dest_a, failures_a, url=f"https://github.com/{repo_a}"
            ),
            RepoResult(
                f"Repo B (at {old_ref}, before updating)",
                repo_b,
                dest_b,
                failures_b,
                url=f"https://github.com/{repo_b}",
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

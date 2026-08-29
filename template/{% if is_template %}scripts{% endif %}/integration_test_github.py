"""Create two throwaway repos from this template and verify them.

Run via `mise run integration-test-gh` -- a human's own gh/GCM session, both repos
left in place afterward for inspection (delete them yourself when you're done). Not
templated itself; the caller passes this repo's own source URL and name as arguments,
so there's nothing here for Jinja to render.

Always runs against HEAD -- this is meant to verify a release candidate on main is
good before cutting a release, not to smoke-test an arbitrary branch. Creates two
repos every run, each covering a different scenario so a single run exercises more of
the answer space, not the same fixed answers twice: Repo A is a plain `copier copy`
with `zensical_target: GitHub Pages` and `code_coverage` on; Repo B is copied at the
last stable tag with `zensical_target: docs-site Directory in Repo` and
`code_coverage` off, left there for you to run `mise run copier-update` against
yourself -- deliberately not automated, see main()'s own docstring for why.

Every check this script runs prints its own PASS/FAIL line as it happens, plus a
summary per repo at the end -- it never stops at the first failure, so one run gives
the full picture. It only checks things that need a real GitHub API call or a real
pipeline run; anything `tests/` already covers by rendering locally (structure,
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

# Default `gh auth login` scopes cover both -- see docs/token-permissions.md.
REQUIRED_SCOPES = ("repo", "workflow")

# Must match _tasks' project_description -d flag in create() below.
PROJECT_DESCRIPTION = "Integration Test - NOT FOR PUBLIC USE, safe to delete"

# Must match .github/settings.yml.jinja's `labels:` list, sorted.
EXPECTED_LABELS = (
    "accessibility,awaiting pr,blocked,bug,documentation,duplicate,"
    "enhancement,good first issue,help wanted,invalid,question,wontfix"
)

SCRATCH_FILE_CONTENT = "# Integration Test Scratch File\n\nSafe to ignore or delete.\n"


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
    owner: str,
    zensical_target: str,
    *,
    code_coverage: bool,
) -> None:
    """Render+run the template to create the test repo.

    `github_username` is pinned to the already-resolved `owner` rather than left to
    auto-detect from local git config: copier.yml.jinja's `.github/settings.yml`
    content (e.g. `homepage`) is templated from `github_repo_owner`, which defaults to
    `github_username` -- letting that auto-detect could silently diverge from the
    account gh actually authenticated as, breaking verify() for reasons unrelated to
    what it's actually trying to test.

    `zensical_target` and `code_coverage` are explicit, not left to `--defaults`, so
    the two repos this script creates can each cover a different value instead of
    silently both getting whatever the question's own default is.

    `--defaults` falls back to each question's own default for anything not covered
    by an explicit -d below (currently github_org, author_name) -- without it, copier
    drops into an interactive prompt for those. Explicit -d values below still take
    priority over --defaults regardless of order.
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


def latest_run_id(repo: str, workflow_file: str) -> str:
    """Return the most recent run's ID for a workflow, or "" if none exist yet.

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
        "--limit",
        "1",
        "--json",
        "databaseId",
        "-q",
        '.[0].databaseId // ""',
    )


def wait_for_new_run(
    repo: str, workflow_file: str, before_id: str, *, timeout: int = 60
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
        current = latest_run_id(repo, workflow_file)
        if current and current != before_id:
            return int(current)
        time.sleep(5)
    raise SystemExit(f"Timed out waiting for a new run of {workflow_file} in {repo}")


def dispatch_workflow(
    repo: str, workflow_file: str, *, inputs: dict[str, str] | None = None
) -> int:
    """Dispatch a workflow_dispatch workflow and return the resulting run's ID.

    Returns:
        The new run's ID.

    """
    before = latest_run_id(repo, workflow_file)
    args = ["gh", "workflow", "run", workflow_file, "--repo", repo]
    for key, value in (inputs or {}).items():
        args += ["-f", f"{key}={value}"]
    run(*args)
    return wait_for_new_run(repo, workflow_file, before)


def open_pr_wait_and_merge(
    repo: str, dest: str, branch: str, commit_message: str, filename: str
) -> None:
    """Open a normal, passing PR and merge it -- the only way real commits reach main.

    Branch protection requires every change to go through a PR, even for the repo
    owner -- a direct `git push` to main is rejected outright once the ruleset is
    live (confirmed the hard way: an earlier version of this script tried exactly
    that). This also mirrors how release-auto-preparereleasepr.yml actually gets
    triggered in practice: by the push GitHub generates when a PR merges, not by
    anyone pushing to main directly.

    """
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)
    run("git", "switch", "-c", branch, cwd=dest)
    Path(dest, filename).write_text(SCRATCH_FILE_CONTENT, newline="\n")
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
    wait_for_pr_checks(repo, pr_number)
    run("gh", "pr", "merge", pr_number, "--repo", repo, "--squash", "--delete-branch")
    run("git", "checkout", "main", cwd=dest)
    run("git", "pull", cwd=dest)


def wait_for_pr_checks(repo: str, pr_number: str) -> None:
    """Poll a PR's status checks until they all complete, and confirm they passed.

    A force-push in quick succession (e.g. a branch updated twice back-to-back) can
    leave a stale `CANCELLED` entry alongside the newer run's result for the same
    check name -- `test-auto-prvalidation.yml`'s own concurrency group cancels the
    superseded run. Only the most recent entry per check name reflects the PR's
    actual current state, so older duplicates are dropped before evaluating success.

    A dedupe pass alone isn't enough: a check can be observed as COMPLETED
    (cancelled) in the brief window before its superseding run has even been
    created, let alone registered in the rollup -- a cancelled run and its
    replacement's SUCCESS have been observed completing within the same second. So
    this only accepts an "all complete" result once the exact same snapshot is
    observed on two consecutive polls, giving a just-created superseding run a
    chance to show up first.

    Raises:
        SystemExit: if the checks don't all complete in time, or don't all pass.

    """
    latest: list[dict] = []
    stable = False
    for _ in range(24):
        rollup = json.loads(
            gh_value(
                "pr", "view", pr_number, "--repo", repo, "--json", "statusCheckRollup"
            )
        )["statusCheckRollup"]
        latest_by_name: dict[str, dict] = {}
        for check in rollup:
            name = check.get("name")
            existing = latest_by_name.get(name)
            if existing is None or (check.get("completedAt") or "") >= (
                existing.get("completedAt") or ""
            ):
                latest_by_name[name] = check
        new_latest = list(latest_by_name.values())
        all_complete = bool(new_latest) and all(
            c.get("status") == "COMPLETED" for c in new_latest
        )
        if all_complete and stable and new_latest == latest:
            latest = new_latest
            break
        stable = all_complete
        latest = new_latest
        time.sleep(10)
    if not latest or not all(c.get("conclusion") == "SUCCESS" for c in latest):
        raise SystemExit(f"PR {pr_number} in {repo} didn't pass its checks: {latest!r}")


def wait_for_run(repo: str, run_id: int) -> str:
    """Wait for a run to finish and return its conclusion.

    `check=False`: a failing run makes `gh run watch --exit-status` exit non-zero,
    which is an expected outcome for some callers (e.g. a deliberately-broken PR), not
    a bug in this script -- the caller decides what conclusion was actually wanted.

    Returns:
        The run's conclusion, e.g. "success" or "failure".

    """
    run("gh", "run", "watch", str(run_id), "--repo", repo, "--exit-status", check=False)
    return gh_value(
        "run",
        "view",
        str(run_id),
        "--repo",
        repo,
        "--json",
        "conclusion",
        "-q",
        ".conclusion",
    )


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
        for step in job["steps"]:
            if step["name"] == step_name:
                return step["conclusion"]
    return None


def report_settings_checks(
    repo: str, homepage: str, failures: list[str], *, zensical_ghpages: bool
) -> None:
    """Report each part of .github/settings.yml the Settings App should have applied.

    Covers the `repository`, `labels`, `rulesets`, and `environments` blocks -- every
    top-level key that file actually sets, not just a sample of them. The
    `github-pages` environment only exists when `zensical_ghpages` is true --
    settings.yml.jinja only declares it in that case.
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
        repo_data.get("homepage") == homepage,
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
        '[.[].name] | sort | join(",")',
        check=False,
        capture=True,
    )
    check(
        failures, "labels match settings.yml", labels.stdout.strip() == EXPECTED_LABELS
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


def settings_synced(repo: str, homepage: str, *, zensical_ghpages: bool) -> bool:
    """Check whether the Settings App has applied every part of .github/settings.yml.

    Used only to decide when the polling loop in verify() can stop -- the actual
    per-field results get reported once, afterward, by report_settings_checks().

    Returns:
        True once every expected field/label/ruleset/(conditionally) environment is
        present.

    """
    repo_data_result = run("gh", "api", f"repos/{repo}", check=False, capture=True)
    if repo_data_result.returncode != 0:
        return False
    repo_data = json.loads(repo_data_result.stdout)
    if repo_data.get("description") != PROJECT_DESCRIPTION:
        return False
    if repo_data.get("homepage") != homepage:
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

    if not zensical_ghpages:
        return True

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


def verify(
    repo: str, homepage: str, failures: list[str], *, zensical_ghpages: bool
) -> None:
    """Assert the created repo's real remote state matches what repo setup should do.

    `zensical_ghpages` gates the Pages-specific check: GitHub Pages is only enabled
    (and `/pages` only returns anything) when the repo was created with
    `zensical_target: GitHub Pages`.

    Raises:
        SystemExit: only if the repo itself can't be found -- every other assertion
            is recorded via check() instead, since a real value here doesn't prevent
            the rest of this script's checks from being meaningful.

    """
    print(f"Verifying {repo}...")
    repo_view = run(
        "gh", "repo", "view", repo, "--json", "visibility", check=False, capture=True
    )
    if repo_view.returncode != 0:
        raise SystemExit(f"Repo {repo!r} not found -- did create() fail?")
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

    run("gh", "api", f"repos/{repo}/contents/.github/workflows", capture=True)

    # Labels and the branch ruleset come from .github/settings.yml, applied
    # asynchronously by the Settings GitHub App (https://github.com/apps/settings)
    # reacting to the push above -- not something this script sets directly, so this
    # polls rather than checking once. Requires that app be installed on the
    # authenticated account with access to all repositories (a new repo isn't
    # automatically visible to an app installed on "only select repositories") -- see
    # docs/token-permissions.md.
    for attempt in range(12):
        if settings_synced(repo, homepage, zensical_ghpages=zensical_ghpages):
            print(f"Settings App sync: OK (after {attempt * 10}s)")
            break
        time.sleep(10)
    else:
        print(
            "Settings App sync: not observed within 120s -- is it installed on this "
            "account with access to all repositories?"
        )
    report_settings_checks(repo, homepage, failures, zensical_ghpages=zensical_ghpages)


def homepage_for(owner: str, repo_name: str) -> str:
    """Compute the GitHub Pages homepage verify() expects for a repo this script made.

    Returns:
        The homepage URL. project_visibility is always Public below, matching
        settings.yml.jinja's homepage logic (only set when is_public).

    """
    return f"https://{owner}.github.io/{repo_name}"


def provision_test_secrets(repo: str) -> None:
    """Set placeholder secrets so pipelines gated on their presence can actually run.

    APPRISE_URL: Maint (Auto): Copier Update Check requires it to exist before its own
    logic even runs (see .github/actions/require-secrets). Points at a real, harmless
    HTTPS endpoint, not a fake host, so the "Notify if Update is Available" step, when
    it does run, doesn't fail the whole workflow on an unrelated delivery error.

    REPO_MAINTENANCE_PAT: Release (Auto): Prepare Release PR pushes to `knope/release`
    and opens/updates a PR against it. A push authenticated as the default
    `GITHUB_TOKEN` (i.e. actor `github-actions[bot]`) leaves that PR's required `tests`
    status check permanently stuck in GitHub's `action_required` state -- pending a
    human manually approving the run in the Actions tab -- which blocks branch
    protection from ever letting it merge. Reuses this script's own `gh` auth token
    (the same real-user identity already pushing the other test branches, which never
    hit this gate) so the release flow can be exercised the same way a real repo's own
    REPO_MAINTENANCE_PAT would behave.
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
    pat = gh_value("auth", "token")
    run("gh", "secret", "set", "REPO_MAINTENANCE_PAT", "--repo", repo, "--body", pat)


def check_copier_update_check(
    repo: str, failures: list[str], *, expect_update_available: bool
) -> None:
    """Dispatch Maint (Auto): Copier Update Check and verify it ran correctly.

    Whether it detected a pending update is read from whether the "Notify if Update is
    Available" step ran (its own `if:` is gated on that) rather than by scraping log
    text for the third-party action's own output, which isn't a contract this script
    should depend on.
    """
    print("Checking Maint (Auto): Copier Update Check...")
    run_id = dispatch_workflow(repo, "maint-auto-copierupdatecheck.yml")
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "Copier Update Check workflow succeeds",
        conclusion == "success",
        conclusion,
    )
    notify_step = step_conclusion(repo, run_id, "Notify if Update is Available")
    # Whether the step *ran* (its `if:` is gated on update_available), not whether
    # its own delivery succeeded -- a real notification failure (bad endpoint, etc.)
    # would otherwise look identical to "no update was detected".
    detected_available = notify_step not in (None, "skipped")
    check(
        failures,
        "Copier Update Check reports "
        + (
            "an update is available"
            if expect_update_available
            else "no update available"
        ),
        detected_available == expect_update_available,
        f"'Notify if Update is Available' step conclusion was {notify_step!r}",
    )


def check_noop_update(dest: str, vcs_ref: str, failures: list[str]) -> None:
    """Run `copier update` against an already-current repo and confirm it's a no-op.

    `--defaults` is safe here specifically because nothing changed since this repo was
    copied -- there's no template diff to introduce a new question, so there's no risk
    of silently defaulting past a real prompt the way there would be for Repo B.

    `vcs_ref` must match whatever `create()` used for this repo: without an explicit
    `--vcs-ref`, `copier update` targets the latest release *tag*, not HEAD -- if
    main has commits past the last release (the normal case), that's an earlier point
    than what this repo was actually created at, and copier has no sane way to
    "update" backwards to it.
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


def check_repo_health_check(repo: str, failures: list[str]) -> None:
    """Dispatch Maint (Auto): Repo Health Check and confirm it completes clean.

    Covers both jobs (link-check and the REPO_MAINTENANCE_PAT expiration check) via
    the overall run conclusion -- a real near-expiry PAT to exercise the actual
    warning/notification path isn't something this throwaway repo has, so that part
    stays on the manual verification checklist.
    """
    print("Checking Maint (Auto): Repo Health Check...")
    run_id = dispatch_workflow(repo, "maint-auto-repohealthcheck.yml")
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "Repo Health Check workflow succeeds",
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
    print("Checking a bad-title PR fails Test (Auto): PR Validation...")
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
    print("Checking a PR with a failing test fails Test (Auto): PR Validation...")
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
    computed -- unlike the PR's head commit SHA, it doesn't change just because
    `autoupdate-knope-pr` recreates the branch from a fresh main HEAD every run, so
    it's the right signal for "did this merge actually change what's proposed."

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
    print("Checking Release (Auto): Prepare/Publish Release...")

    # The bootstrap-time PR is prepared with an explicit --override-version; the
    # *first* automated run after that always recomputes the version from knope's own
    # default rules, changing the PR's content regardless of what triggered that run.
    # Absorb that one-time transition with a throwaway merge before testing that a
    # docs-only merge is a true no-op -- otherwise the correction gets misattributed
    # to whichever commit happens to trigger the first automated run.
    prepare_before = latest_run_id(repo, "release-auto-preparereleasepr.yml")
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/warmup",
        "chore: integration test warmup commit",
        "INTEGRATION_TEST_WARMUP.md",
    )
    warmup_run_id = wait_for_new_run(
        repo, "release-auto-preparereleasepr.yml", prepare_before
    )
    wait_for_run(repo, warmup_run_id)

    # A release PR may already be open here (e.g. the bootstrap-time v0.1.0 one), so
    # "no PR is open" isn't the right no-op signal -- what actually matters is that a
    # docs-only merge doesn't change what version it proposes.
    docs_noop_before = knope_release_pr_title(repo)
    prepare_before = latest_run_id(repo, "release-auto-preparereleasepr.yml")
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/docs-noop",
        "docs: integration test no-op commit",
        "INTEGRATION_TEST_DOCS.md",
    )
    run_id = wait_for_new_run(repo, "release-auto-preparereleasepr.yml", prepare_before)
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

    prepare_before = latest_run_id(repo, "release-auto-preparereleasepr.yml")
    open_pr_wait_and_merge(
        repo,
        dest,
        "integration-test/feat",
        "feat: integration test feature",
        "INTEGRATION_TEST_FEAT.md",
    )
    run_id = wait_for_new_run(repo, "release-auto-preparereleasepr.yml", prepare_before)
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
    publish_before = latest_run_id(repo, "release-auto-publishrelease.yml")
    zensical_before = latest_run_id(repo, "docs-auto-zensical.yml")
    wait_for_pr_checks(repo, str(pr_number))
    run(
        "gh",
        "pr",
        "merge",
        str(pr_number),
        "--repo",
        repo,
        "--squash",
        "--delete-branch",
    )
    run("git", "pull", cwd=dest)
    publish_run_id = wait_for_new_run(
        repo, "release-auto-publishrelease.yml", publish_before
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

        # Publishing a release fires a `release: published` event that
        # docs-auto-zensical.yml listens for (it publishes the "latest" Pages docs
        # alias) -- wait for it here so check_repo_health_check(), which runs later,
        # isn't racing a Pages deployment that hasn't happened yet.
        zensical_run_id = wait_for_new_run(
            repo, "docs-auto-zensical.yml", zensical_before
        )
        conclusion = wait_for_run(repo, zensical_run_id)
        check(
            failures,
            "publishing a release triggers the Pages docs deploy",
            conclusion == "success",
            conclusion,
        )


def check_prerelease_flow(repo: str, dest: str, failures: list[str]) -> None:
    """Exercise Release (Manual): Create Prerelease -- a label, a dup, a new label."""
    print("Checking Release (Manual): Create Prerelease...")

    # PrepareRelease refuses to run with nothing to bump -- without a real commit
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
        repo, "release-manual-createprerelease.yml", inputs={"label": "alpha"}
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
        repo, "release-manual-createprerelease.yml", inputs={"label": "alpha"}
    )
    conclusion = wait_for_run(repo, run_id)
    check(
        failures,
        "re-dispatching the same label at the same commit is blocked",
        conclusion == "failure",
        conclusion,
    )

    run_id = dispatch_workflow(
        repo, "release-manual-createprerelease.yml", inputs={"label": "beta"}
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
    """Verify Repo B's state after a human has run `mise run copier-update` on it.

    This is the second entry point (`--verify-update`): the update itself happens by
    hand, on your own schedule, so this script can't chain straight from creating the
    repo into checking it -- see main()'s own docstring.
    """
    print(f"Checking {repo}'s update applied cleanly...")
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
    run("gh", "pr", "merge", pr_number, "--repo", repo, "--squash", "--delete-branch")


def main() -> None:
    """Create and verify two throwaway repos, each covering a different scenario.

    Both run every time, always at HEAD (this tool exists to verify a release
    candidate on main is good before cutting a release, not to smoke-test an
    arbitrary branch). Repo A is a plain `copier copy` with `zensical_target: GitHub
    Pages` and `code_coverage` on -- every automated check this script can run
    happens against it. Repo B is copied at the last stable tag with
    `zensical_target: docs-site Directory in Repo` and `code_coverage` off, for you to
    run `mise run copier-update` against yourself -- deliberately not automated:
    that's the exact command, with the exact prompts, a real user gets, and running it
    by hand is the only way to see a new question's prompt land the way it actually
    would for them, not however this script happened to answer it. Both repos are
    left in place afterward for inspection.

    Once you've updated Repo B by hand, re-run this script with `--verify-update
    <repo> --local-path <path>` (also available as `mise run
    integration-test-verify-update-gh`) to check it applied cleanly -- see
    docs/manual-verification-github.md's "Repo B" section.

    Raises:
        SystemExit: if required arguments are missing, or if any automated check
            failed (after printing every check's result -- see check()).

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Copier template source URL")
    parser.add_argument("--repo-prefix", help="This repo's own name")
    parser.add_argument(
        "--verify-update",
        metavar="REPO",
        default=os.environ.get("usage_repo"),
        help=(
            "Skip creating repos; instead verify REPO (owner/name) after you've run "
            "`mise run copier-update` on it yourself. Requires --local-path."
        ),
    )
    parser.add_argument(
        "--local-path",
        default=os.environ.get("usage_local_path"),
        help="Local clone path for --verify-update (printed when Repo B was created).",
    )
    args = parser.parse_args()

    check_gh_installed()
    check_scopes()

    if args.verify_update:
        if not args.local_path:
            raise SystemExit("--verify-update requires --local-path too.")
        update_failures: list[str] = []
        check_post_update(args.verify_update, args.local_path, update_failures)
        report(f"Repo B ({args.verify_update})", update_failures)
        if update_failures:
            raise SystemExit(1)
        return

    if not args.source or not args.repo_prefix:
        raise SystemExit("--source and --repo-prefix are required.")

    owner = gh_value("api", "user", "--jq", ".login")
    timestamp = int(time.time())

    print(
        "=== Repo A: fresh copy at HEAD "
        "(zensical_target: GitHub Pages, code_coverage: on) ==="
    )
    repo_a_name = f"{args.repo_prefix}-integration-test-{timestamp}-a"
    dest_a = tempfile.mkdtemp(prefix="integration-test-")
    repo_a = f"{owner}/{repo_a_name}"
    create(
        args.source,
        "HEAD",
        repo_a_name,
        dest_a,
        owner,
        "GitHub Pages",
        code_coverage=True,
    )
    provision_test_secrets(repo_a)
    failures_a: list[str] = []
    verify(repo_a, homepage_for(owner, repo_a_name), failures_a, zensical_ghpages=True)
    check_copier_update_check(repo_a, failures_a, expect_update_available=False)
    check_noop_update(dest_a, "HEAD", failures_a)
    check_bad_title_blocks_merge(repo_a, dest_a, failures_a)
    check_failing_tests_block_merge(repo_a, dest_a, failures_a)
    check_release_flow(repo_a, dest_a, failures_a)
    # Run last: a GitHub Pages repo's own homepage link (in README.md) 404s until the
    # first Pages deployment finishes propagating -- by now enough real wall-clock
    # time and several PR/merge cycles have passed for that to be reliably live,
    # rather than racing it right after repo creation.
    check_repo_health_check(repo_a, failures_a)
    check_prerelease_flow(repo_a, dest_a, failures_a)
    report(f"Repo A ({repo_a})", failures_a)

    old_ref = latest_stable_tag(args.source)
    print(
        f"=== Repo B: {old_ref}, for you to update by hand (zensical_target: "
        "docs-site Directory in Repo, code_coverage: off) ==="
    )
    repo_b_name = f"{args.repo_prefix}-integration-test-{timestamp}-b"
    dest_b = tempfile.mkdtemp(prefix="integration-test-")
    repo_b = f"{owner}/{repo_b_name}"
    create(
        args.source,
        old_ref,
        repo_b_name,
        dest_b,
        owner,
        "docs-site Directory in Repo",
        code_coverage=False,
    )
    provision_test_secrets(repo_b)
    failures_b: list[str] = []
    verify(repo_b, homepage_for(owner, repo_b_name), failures_b, zensical_ghpages=False)
    check_copier_update_check(repo_b, failures_b, expect_update_available=True)
    report(f"Repo B ({repo_b}, before updating)", failures_b)

    print(
        f"\nLeaving {repo_a} ({dest_a}) and {repo_b} ({dest_b}) in place -- delete "
        f"them yourself when you're done. {repo_b} is still at {old_ref}; cd into "
        f"{dest_b} and run `mise run copier-update` yourself to test the update path, "
        "then `mise run integration-test-verify-update-gh -- --repo "
        f"{repo_b} --local-path {dest_b}` to verify it applied cleanly "
        '(see "Repo B" in docs/manual-verification-github.md).'
    )

    if failures_a or failures_b:
        raise SystemExit(1)


if __name__ == "__main__":
    sys.exit(main())

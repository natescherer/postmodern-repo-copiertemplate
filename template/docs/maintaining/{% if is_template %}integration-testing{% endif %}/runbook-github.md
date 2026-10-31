# Integration Test Runbook (GitHub)

Every step of a GitHub integration test run, from setup to cleanup, as the last step before a
release. See [Integration Testing](index.md) for what the run does and why.

The commands use these values from each repo's entry in the run's summary: its **Local clone**
for `<repo-a-path>` and `<repo-b-path>`. Each entry's **Web** link opens that repo on GitHub. `<template-repo-path>` is this template's own clone.

!!! bug "Checkbox state isn't saved"
    You can tick the boxes as you go, but reloading or leaving the page clears them. Finish the
    list in one sitting.

## Before You Start

- [ ] The GitHub [Prerequisites](../../getting-started/prerequisites.md) are in place for your
  account: all four GitHub apps, including the optional ones, each with access to all
  repositories, since the test repos are public with `code_coverage` on; and the GitHub CLI,
  logged in, with Git authentication set up.
- [ ] Give the GitHub CLI the scopes the run and its cleanup need:

    ```sh
    gh auth refresh -h github.com -s repo,workflow,delete_repo
    ```

- [ ] Set the `CODECOV_TOKEN` environment variable to your Codecov account's global upload
  token, which the run stores as Repo A's secret; a new repo has no per-repo token yet. The
  run requires it, and stops before creating anything without it.

## Running the Test

- [ ] Start the run:

    ```sh
    cd <template-repo-path>
    mise run integration-test-gh
    ```

- [ ] When it finishes, its summary says "all checks passed" for both repos. If a check failed,
  find out why in the run's log directory, which the run prints at its start and end:
  `<template-repo-path>/.cache/integration-test/<timestamp>-github/`. Its `run.log` holds
  everything the run printed and every command's output, and each workflow run the script waited
  on has its own log beside it. Fix the cause, clean up (see [Cleaning Up](#cleaning-up)), and
  start again.

## Repo A

A copy at `HEAD`, with `zensical_target: GitHub Pages` and `code_coverage` on. Its docs site is
its homepage, `https://<owner>.github.io/<repo>/`.

### After First Setup

*Automated: a bad PR title fails PR Validation, and branch protection blocks merging it.*

- [ ] Each item in the **Template Setup Checklist** issue applies to a GitHub project, and each
  link in it opens.
- [ ] The badges at the top of README.md render, with no broken images.
- [ ] README.md shows `docs/assets/images/readme-logo.png` and
  `docs/assets/images/readme-screenshot.png`.

### Maint (Auto): Monthly Maintenance

*Automated: the run starts each of the workflow's two jobs alone, through its **Job to run**
input. The Copier Update Check job completes and reports no update available, and the Repo
Health Check job completes clean.*

- [ ] Run the Repo Health Check job on a branch with a broken link:

    ```sh
    cd <repo-a-path>
    git switch main
    git pull
    git switch -c integration-test/broken-link
    echo "[Broken link](https://httpbin.org/status/404)" >> README.md
    git commit -am "docs: add a broken link"
    git push -u origin integration-test/broken-link
    gh workflow run maint-auto-monthlymaintenance.yml --ref integration-test/broken-link -f job=repo_health_check
    ```

    The run fails, and its **Check for Broken Links** step names `https://httpbin.org/status/404`.

### Maint (Auto): Renovate

On GitHub, Renovate runs as the [Renovate GitHub App](https://github.com/apps/renovate), outside
this repo's CI, so there's nothing to dispatch.

- [ ] Repo A's **Settings > GitHub Apps** lists Renovate.
- [ ] Renovate opens a **Dependency Dashboard** issue in Repo A.
- [ ] Renovate opens a PR bumping typos. The run's last merge, `chore: let Renovate bump an old
  typos`, lifted Repo A's Renovate schedule and pinned typos to an old release.

### Maint (Auto): All Contributors

- [ ] Comment `@all-contributors please add @<your GitHub username> for doc` on the
  **Template Setup Checklist** issue. The bot opens a PR adding you to README.md's
  Contributors section.

### Docs (Auto): Zensical Publish to GitHub Pages

- [ ] Merge a docs change through a PR:

    ```sh
    cd <repo-a-path>
    git switch main
    git pull
    git switch -c integration-test/docs-change
    echo "Integration test docs change." >> docs/index.md
    git commit -am "docs: integration test docs change"
    git push -u origin integration-test/docs-change
    gh pr create --title "docs: integration test docs change" --body "Integration test."
    gh pr merge --squash --auto --delete-branch
    ```

- [ ] Once that PR merges, the site's `dev` version (`.../dev/`) shows "Integration test docs
  change." on its home page.
- [ ] The site's version selector lists the release the run published, `latest` points at it,
  and the site root serves it.

### Test (Auto): PR Validation

*Automated: a bad PR title fails, a failing test suite fails and blocks the merge, and the
**Upload Coverage to Codecov** step uploads the `coverage.xml` that Repo A's setup PR commits,
which Codecov accepts.*

- [ ] Repo A's page on Codecov, `https://app.codecov.io/gh/` followed by Repo A's **Name** from
  the summary, shows a report for `README.md` on the `integration-test/setup` branch: Codecov
  processed the upload it accepted. PR Validation uploads only from PRs, so `main`, the page's
  default branch, has no report.

### Release (Auto): Prepare/Publish Release

*Automated: a docs-only commit releases nothing, a `feat:` commit opens a release PR with the
bumped version in its title, and merging that PR creates a tag and a GitHub Release.*

Nothing left to check for Repo A.

### Release (Auto): Prepare Release PR: Prereleases

*Automated: a manual run with each prerelease label produces a matching tag, the same label at
the same commit is blocked, and a different label at the same commit is allowed.*

Nothing left to check for Repo A.

## Repo B

A copy at the last stable release tag, with `zensical_target: docs-site Directory in Repo` and
`code_coverage` off. It stays at that tag until you update it.

### Before Updating

*Automated, before you update anything: Maint (Auto): Monthly Maintenance's Copier Update
Check job reports no update available on `main`, since Repo B is at the newest release. On the
`integration-test/older-recorded-version` branch, whose answers record the commit just before
that release, it detects the release.*

- [ ] The branch run's **Notify if Update is Available** step succeeds.

### Running the Update

- [ ] Update on a branch to this template's `HEAD`, the release candidate, pressing Enter at
  each prompt to accept the default:

    ```sh
    cd <repo-b-path>
    git switch -C integration-test/copier-update
    mise x -- uvx --refresh --from copier@latest --with jinja2-shell-extension copier update --answers-file .config/copier-answers.yml --skip-answered --trust --vcs-ref=HEAD
    ```

    This is the [upgrade guide](../upgrading-from-0x.md)'s command, not Repo B's
    `copier-update` task: Repo B starts at a 0.x release, whose task runs a Copier older than
    this template's `_min_copier_version`.

- [ ] The update finishes without an error. Then commit it and open its PR:

    ```sh
    git add -A
    git commit -m "chore: copier update"
    git push -u origin integration-test/copier-update
    gh pr create --title "chore: copier update" --body "Integration test."
    gh pr merge --squash --auto --delete-branch
    ```

### After Updating

- [ ] Once the update's PR merges, apply its `.github/settings.yml` with gh-settings, as the
  [upgrade guide](../upgrading-from-0x.md) has a 0.x project do, and answer yes when it asks:

    ```sh
    cd <repo-b-path>
    git switch main
    git pull
    mise run sync-repo-settings
    ```

    A Repo B copied at a release before gh-settings has none of its settings applied until now,
    so the run shows its settings checks as `[SKIP]`.

- [ ] Verify the update:

    ```sh
    cd <template-repo-path>
    mise run integration-test-verify-update-gh
    ```

    It finds the newest run's Repo B from its local clone. It checks that the update brought in
    current content, left no conflict markers, and applied `.github/settings.yml`, and that
    `Test (Auto): PR Validation` triggers and passes on a new PR. Every check prints `[PASS]`.

## Cleaning Up

- [ ] Delete the test repos, and confirm when it asks:

    ```sh
    cd <template-repo-path>
    mise run integration-test-cleanup-gh
    ```

    It deletes every integration-test repo under your account, and their local clones,
    including any left by a run that stopped partway.

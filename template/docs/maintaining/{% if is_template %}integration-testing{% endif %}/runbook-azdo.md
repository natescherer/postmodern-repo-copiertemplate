# Integration Test Runbook (Azure DevOps)

Every step of an Azure DevOps integration test run, from setup to cleanup, as the last step
before a release. See [Integration Testing](index.md) for what the run does and why.

The steps use these values from each repo's entry in the run's summary: Repo A's **Name** for
`<repo-a>`, and each repo's **Local clone** for `<repo-a-path>` and `<repo-b-path>`. Each
entry's **Web** link opens that repo in Azure DevOps. `<template-repo-path>` is this template's
own clone, and `<org>` and `<project>` are the Azure DevOps organization and project the test
repos go in.

!!! bug "Checkbox state isn't saved"
    You can tick the boxes as you go, but reloading or leaving the page clears them. Finish the
    list in one sitting.

## Before You Start

- [ ] The Azure DevOps [Prerequisites](../../getting-started/prerequisites.md) are in place for
  `<project>`: the project settings, the build service permissions, and the Azure CLI with its
  Azure DevOps extension, logged in.
- [ ] A GitHub token is available: log in with `gh auth login`, or set the `GITHUB_COM_TOKEN`
  environment variable to a GitHub token with no scopes. The run sets it on every pipeline, for
  mise's tool downloads and Renovate's lookups on github.com, and stops before creating anything
  without one.
- [ ] `<org>` and `<project>` are set for the integration-test tasks, once per machine, in
  `<template-repo-path>/mise.local.toml`, which git ignores:

    ```toml
    [env]
    INTEGRATION_TEST_AZDO_ORG = "<org>"
    INTEGRATION_TEST_AZDO_PROJECT = "<project>"
    ```

    A template hosted on Azure DevOps defaults to its own org and project, so it needs this only
    to test somewhere else. Passing `--org` and `--project` to a task overrides either.

## Running the Test

- [ ] Start the run:

    ```sh
    cd <template-repo-path>
    mise run integration-test-azdo
    ```

- [ ] When it finishes, its summary says "all checks passed" for both repos. If a check failed,
  find out why in the run's log directory, which the run prints at its start and end:
  `<template-repo-path>/.cache/integration-test/<timestamp>-azdo/`. Its `run.log` holds
  everything the run printed and every command's output, and each pipeline run the script waited
  on has its own log beside it. Fix the cause, clean up (see [Cleaning Up](#cleaning-up)), and
  start again.

## Repo A

A copy at `HEAD`, with `code_coverage` on.

### After First Setup

*Automated: a bad PR title fails PR Validation, the branch policy blocks completing it, and
Project Administrators can bypass the policy.*

- [ ] Each item in the setup checklist (repeated under Repo A in the run's summary) applies to
  an Azure DevOps project, and each link in it opens.
- [ ] The badges at the top of README.md render, with no broken images.
- [ ] README.md shows `docs/assets/images/readme-logo.png` and
  `docs/assets/images/readme-screenshot.png`.

### Maint (Auto) - Monthly Maintenance

*Automated: the run starts each of the pipeline's three jobs alone, through its **Job to run**
parameter, and each succeeds. The Copier Update Check job completes; what it reports isn't
checked, since `az` can't easily read a run's step output (see the script's module docstring).
The Repo Health Check job completes clean. The Renovate job, with Repo A's Renovate schedule
lifted, typos pinned to an old release, and your GitHub token set as `GITHUB_COM_TOKEN`, opens
a PR bumping typos.*

- [ ] The Copier Update Check job's **Check for Template Updates** step reports no update
  available, since this repo is at `HEAD`.
- [ ] Push a branch with a broken link:

    ```sh
    cd <repo-a-path>
    git switch main
    git pull
    git switch -c integration-test/broken-link
    echo "[Broken link](https://httpbin.org/status/404)" >> README.md
    git commit -am "docs: add a broken link"
    git push -u origin integration-test/broken-link
    ```

- [ ] In `<project>`'s **Pipelines**, run `[<repo-a>] Maint (Auto) - Monthly Maintenance` on
  that branch (**Run pipeline**, then **Branch/tag**: `integration-test/broken-link` and **Job to
  run**: `repo_health_check`). The run fails, and its log names `https://httpbin.org/status/404`.

### Docs (Auto) - Zensical Build & Commit

- [ ] Merge a docs change through a PR:

    ```sh
    cd <repo-a-path>
    git switch main
    git pull
    git switch -c integration-test/docs-change
    echo "Integration test docs change." >> docs/index.md
    git commit -am "docs: integration test docs change"
    git push -u origin integration-test/docs-change
    az repos pr create --source-branch integration-test/docs-change --target-branch main --title "docs: integration test docs change" --merge-commit-message "docs: integration test docs change" --auto-complete true --squash true --delete-source-branch true
    ```

- [ ] Once that PR completes, `[<repo-a>] Docs (Auto) - Zensical Build & Commit` runs, opens
  a PR from `zensical-build`, and completes it. `docs-site/index.html` on `main` then contains
  "Integration test docs change."

### Test (Auto) - PR Validation

*Automated: a bad PR title fails, and a failing test suite fails and blocks completing the PR.*

- [ ] The PR Validation run for the docs-change PR has a **Code Coverage** tab showing the
  results of the `coverage.xml` that Repo A's setup PR commits.
- [ ] Open a PR from the broken-link branch, then push one more commit to it:

    ```sh
    cd <repo-a-path>
    git switch integration-test/broken-link
    az repos pr create --source-branch integration-test/broken-link --target-branch main --title "docs: add a broken link"
    git commit --allow-empty -m "docs: push again"
    git push
    ```

    The PR shows a second PR Validation run, started by the push. Azure Repos has no PR trigger,
    so only the build validation policy starts this pipeline.

### Release (Auto) - Prepare & Publish Release

*Automated: a docs-only commit releases nothing, a `feat:` commit opens a release PR with the
bumped version in its title, and merging that PR creates a tag.*

- [ ] Repo A has exactly one tag without a prerelease suffix (`-alpha` or `-beta`): the release
  from the `feat:` merge. The run merged `fix: integration test prerelease commit` right after
  that release, and the pipeline tells that merge apart from the release PR's own through an API
  check, not a native trigger, so it mustn't have published again.

### Release (Auto) - Prepare & Publish Release: Prereleases

*Automated: a manual run with each prerelease label produces a matching tag, the same label at
the same commit is blocked, and a different label at the same commit is allowed.*

Nothing left to check for Repo A.

## Repo B

A copy at the last stable release tag, with `code_coverage` off. It stays at that tag until you
update it.

### Before Updating

*Automated, before you update anything: Maint (Auto) - Monthly Maintenance's Copier Update
Check job runs and completes, on `main` and on the `integration-test/older-recorded-version`
branch, whose answers record the commit just before the newest release.*

- [ ] The `main` run's **Check for Template Updates** step reports no update available, since
  Repo B is at the newest release.
- [ ] The branch run's **Check for Template Updates** step reports the newest release and sends
  the notification without an error.

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
    az repos pr create --source-branch integration-test/copier-update --target-branch main --title "chore: copier update" --merge-commit-message "chore: copier update" --auto-complete true --squash true --delete-source-branch true
    ```

    Without `--merge-commit-message`, Azure DevOps squash-merges with a generic "Merge pull
    request N" message instead of the PR title.

### After Updating

- [ ] Once the update's PR completes, repoint or delete any pipeline registrations it renamed
  or merged:

    ```sh
    cd <repo-b-path>
    git switch main
    git pull
    mise run migrate-azdo-pipeline-names
    ```

- [ ] Verify the update:

    ```sh
    cd <template-repo-path>
    mise run integration-test-verify-update-azdo
    ```

    It finds the newest run's Repo B, with its org and project, from its local clone. It checks
    that the update brought in current content, left no conflict markers, registered
    each pipeline only under its current name, removed the merged pipelines' old registrations,
    and that `Test (Auto) - PR Validation` triggers and passes on a new PR. Every check prints
    `[PASS]`.

## Cleaning Up

- [ ] Delete the test repos and their pipelines, and confirm when it asks:

    ```sh
    cd <template-repo-path>
    mise run integration-test-cleanup-azdo
    ```

    It deletes every integration-test repo and pipeline in the project, and their local clones,
    including any left by a run that stopped partway.

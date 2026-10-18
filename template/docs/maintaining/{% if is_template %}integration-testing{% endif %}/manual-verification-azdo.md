# Manual Verification Checklist (Azure DevOps)

Work through this whole list by hand as the last step before a release. It covers only what
`mise run integration-test-azdo` can't check; each `integration-test-*-azdo` task prints its
own `[PASS]` or `[FAIL]` per check and a summary. See [Integration Testing](index.md) for what
the run creates and why Repo B's update is manual.

Run each command from the repo's local clone, at the path the run's summary prints for it.

!!! bug "Checkbox state isn't saved"
    You can tick the boxes as you go, but reloading or leaving the page clears them. Finish the
    list in one sitting.

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

### Maint (Auto) - Copier Update Check

*Automated: it runs and completes. What it reports isn't, since `az` can't easily read a run's
step output; see the script's module docstring.*

- [ ] Its run's **Check for Template Updates** step reports no update available, since this
  repo is at `HEAD`.

### Maint (Auto) - Repo Health Check

*Automated: it runs and completes clean.*

- [ ] Push a branch with a broken link:

    ```sh
    git switch main
    git pull
    git switch -c integration-test/broken-link
    echo "[Broken link](https://example.invalid/)" >> README.md
    git commit -am "docs: add a broken link"
    git push -u origin integration-test/broken-link
    ```

- [ ] Run **Maint (Auto) - Repo Health Check** on that branch (**Run pipeline**, then
  **Branch/tag**: `integration-test/broken-link`). The run fails, and its log names
  `https://example.invalid/`.

### Maint (Auto) - Renovate

*Automated: with Repo A's Renovate schedule lifted, typos pinned to an old release, and your
GitHub token set as `GITHUB_COM_TOKEN`, it runs and opens a PR bumping typos.*

Nothing left to check for Repo A.

### Docs (Auto) - Zensical Build & Publish

- [ ] Merge a docs change through a PR:

    ```sh
    git switch main
    git pull
    git switch -c integration-test/docs-change
    echo "Integration test docs change." >> docs/index.md
    git commit -am "docs: integration test docs change"
    git push -u origin integration-test/docs-change
    az repos pr create --source-branch integration-test/docs-change --target-branch main --title "docs: integration test docs change" --auto-complete true --squash true --delete-source-branch true
    ```

- [ ] Once that PR completes, **Docs (Auto) - Zensical Build & Publish** runs, opens a PR from
  `zensical-build`, and completes it. `docs-site/index.html` on `main` then contains
  "Integration test docs change."

### Test (Auto) - PR Validation

*Automated: a bad PR title fails, and a failing test suite fails and blocks completing the PR.*

- [ ] The PR Validation run for the docs-change PR has a **Code Coverage** tab showing
  `coverage.xml`'s results (`code_coverage` is on for this repo).
- [ ] Open a PR from the broken-link branch, then push one more commit to it:

    ```sh
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

### Release (Manual) - Create Prerelease

*Automated: each label produces a matching tag, the same label at the same commit is blocked,
and a different label at the same commit is allowed.*

Nothing left to check for Repo A.

## Repo B

A copy at the last stable release tag, with `code_coverage` off. It stays at that tag until you
update it.

### Before Updating

*Automated, before you update anything: Maint (Auto) - Copier Update Check runs and completes.*

- [ ] Its run's **Check for Template Updates** step reports the newer version and sends the
  notification without an error.

### Running the Update

- [ ] Update on a branch, pressing Enter at each prompt to accept the default:

    ```sh
    git switch -c integration-test/copier-update
    mise run copier-update
    git add -A
    git commit -m "chore: copier update"
    git push -u origin integration-test/copier-update
    az repos pr create --source-branch integration-test/copier-update --target-branch main --title "chore: copier update" --auto-complete true --squash true --delete-source-branch true
    ```

### After Updating

Once the update's PR completes, run the commands in step 2 of the run's summary. They rename any
pipeline registrations the update renamed, then check that the update brought in current
content, left no conflict markers, registered each pipeline only under its current name, and
that `Test (Auto) - PR Validation` triggers and passes on a new PR.

## Cleaning Up

- [ ] Run the cleanup command in the run's summary, and confirm. It deletes every
  integration-test repo and pipeline in the project, including any left by a run that stopped
  partway.

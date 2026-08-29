# Manual Verification Checklist (Azure DevOps)

Run through this **in full**, by hand, as the last step before cutting a release. See [Integration Testing](integration-testing.md) for what `mise run integration-test-azdo` creates and why the update step below isn't automated. Most of Repo A's checks are now automated -- each `mise run integration-test-*-azdo` invocation prints its own PASS/FAIL per check, plus a summary; what's below is what's left for a human.

!!! bug "Checkbox state isn't saved"
    Boxes on this page are clickable so you can tick items off as you go, but nothing
    persists that -- reloading or leaving the page resets every box to unchecked. Treat
    it as a scratchpad for one sitting, not a record you can come back to.

## Repo A

Fresh copy at `HEAD`, `code_coverage` on.

### After First Setup

*Branch protection actually blocking a bad PR is automated -- see "a bad-title PR fails Test (Auto) - PR Validation" and its blocked-merge counterpart in the script's own output.*

- [ ] The setup checklist (printed to the console at the end of `copier copy`) exists and every item on it has been addressed.
- [ ] Badges at the top of README.md render correctly (no broken image icons).
- [ ] `docs/images/readme-logo.png` and `docs/images/readme-screenshot.png` display correctly in README.md, or that section has been removed if unused.
- [ ] Required secrets/pipeline variables are provisioned (`mise run provision-secrets`, or see [Token Permissions](token-permissions.md)) -- confirmed by the pipelines below not failing with authentication errors.

### Maint (Auto) - Copier Update Check

*Dispatching it and confirming it completes without error are automated. Whether it correctly reports no update available isn't -- `az` has no cheap way to read a pipeline run's own step output, see the script's own module docstring for why.*

- [ ] Confirm it correctly reports **no update available** -- this repo is already at `HEAD`.

### Maint (Auto) - Repo Health Check

*Dispatching it and confirming it completes clean is automated.*

- [ ] Temporarily introduce a broken link (e.g. a typo'd URL in a doc) and confirm the next run catches it, then revert.

### Maint (Auto) - Renovate

*Dispatching it and confirming it authenticates successfully are automated.*

- [ ] With at least one outdated dependency present, confirm it opens (or updates) a real pull request proposing the bump.
- [ ] Confirm the one-time **Project Collection Build Service** permission grant described in [Azure DevOps Limitations](platform-notes/azure-devops.md) is actually in place -- a missing grant surfaces as a push/PR-creation failure here, not a clear permissions error.

### Docs (Auto) - Zensical Build & Publish

- [ ] Push a docs change to `main` and confirm `docs-site/` is committed back to the repo with the freshly built HTML.

### Test (Auto) - PR Validation

*A bad-title PR failing, and a PR with a failing test suite failing and being blocked from merging, are both automated.*

- [ ] Confirm `coverage.xml` publishes successfully and shows up on the build -- `code_coverage` is on for this repo.
- [ ] Azure Repos has no native PR-triggered pipeline run -- this pipeline is triggered solely by the build-validation branch policy. Confirm pushing a new commit to an open PR actually kicks off a fresh run (not just the PR's initial creation).

### Release (Auto) - Prepare & Publish Release

*The full flow is automated: a docs-only commit staying a no-op, a feat commit opening a release PR with a version-bump title, and merging that PR publishing a tag.*

- [ ] Confirm the pipeline correctly tells "a normal push to `main`" apart from "this push is the release PR's own merge" -- it does this via an API check, not a native trigger, so push a second, unrelated commit right after a release and confirm it doesn't also try to publish.

### Release (Manual) - Create Prerelease

*The full flow is automated: dispatching each label produces a matching tag, re-dispatching the same label at the same commit is blocked, and dispatching a different label at the same commit is allowed.*

Nothing left here for Repo A.

## Repo B

Copied at the last stable release tag, `code_coverage` off. Still at that tag -- nothing here has been updated for you.

### Before Updating

*Dispatching Maint (Auto) - Copier Update Check and confirming it completes without error are automated (part of `mise run integration-test-azdo`, before you update anything).*

- [ ] Confirm it correctly detects a newer version is available and the Apprise notification actually arrives at `APPRISE_URL`.

### Running the Update

- [ ] `cd` into the repo and run `mise run copier-update` yourself. If it prompts for a new question, answer it the way you'd want a real user updating from the last release to answer it, not whatever's quickest.
- [ ] Commit and push the result.
- [ ] Run `mise run migrate-azdo-pipeline-names` to repoint any renamed pipeline registrations.

### After Updating

Run `mise run integration-test-verify-update-azdo -- --repo <repo> --local-path <path>` (the repo/path are printed at the end of the original `mise run integration-test-azdo` run). It automates everything that needs checking here: the update actually pulled in current content, applied with no leftover conflict markers, every pipeline is registered only under its current name (not left duplicated under the old one), and `Test (Auto) - PR Validation` still triggers and passes on a fresh PR against the updated repo.

## Cleaning Up

- [ ] Run `python cleanup_pipelines.py` in each throwaway repo's local directory (left there by the integration test, next to the repo's own files) before deleting the repos -- Azure DevOps has no bulk-delete UI for pipelines, so skipping this means removing each one by hand through its own settings page.
- [ ] Delete both repos (Project Settings > Repositories, or `az repos delete`).

# Manual Verification Checklist (Azure DevOps)

Run through this **in full**, by hand, against the repos `mise run integration-test-azdo` just created, as the last step before cutting a release -- see [Integration Testing](integration-testing.md) for what that command does and doesn't check on its own.

!!! bug "Checkbox state isn't saved"
    Boxes on this page are clickable so you can tick items off as you go, but nothing
    persists that -- reloading or leaving the page resets every box to unchecked. Treat
    it as a scratchpad for one sitting, not a record you can come back to.

## After First Setup

- [ ] The setup checklist (printed to the console at the end of `copier copy`) exists and every item on it has been addressed.
- [ ] Badges at the top of README.md render correctly (no broken image icons).
- [ ] `docs/images/readme-logo.png` and `docs/images/readme-screenshot.png` display correctly in README.md, or that section has been removed if unused.
- [ ] Required secrets/pipeline variables are provisioned (`mise run provision-secrets`, or see [Token Permissions](token-permissions.md)) -- confirmed by the pipelines below not failing with authentication errors.
- [ ] Branch protection actually **blocks** a bad PR, not just that the policy exists: open a throwaway PR with a failing check (e.g. a non-Conventional-Commit title) and confirm the merge button is disabled, not just that a check shows red.

## Maint (Auto): Copier Update Check

- [ ] Manually run the pipeline and confirm it completes without error.
- [ ] If a newer template version genuinely exists, confirm the Apprise notification actually arrives at the endpoint configured in `APPRISE_URL`.

## Maint (Auto): Link Check

- [ ] Manually run the pipeline and confirm it completes clean.
- [ ] Temporarily introduce a broken link (e.g. a typo'd URL in a doc) and confirm the next run catches it, then revert.

## Maint (Auto): Renovate

- [ ] Manually run the pipeline and confirm it authenticates successfully (no permission/token errors in the log).
- [ ] With at least one outdated dependency present, confirm it opens (or updates) a real pull request proposing the bump.
- [ ] Confirm the one-time **Project Collection Build Service** permission grant described in [Azure DevOps Limitations](platform-notes/azure-devops.md) is actually in place -- a missing grant surfaces as a push/PR-creation failure here, not a clear permissions error.

## Docs (Auto): Zensical Build & Publish

- [ ] Push a docs change to `main` and confirm `docs-site/` is committed back to the repo with the freshly built HTML.

## Test (Auto): PR Validation

- [ ] Open a PR with a non-Conventional-Commit title and confirm the check fails.
- [ ] Open a PR that fails `prek` or the test suite and confirm the required check fails, and that the branch policy above actually blocks merging it.
- [ ] With `code_coverage` on: confirm `coverage.xml` uploads to Codecov successfully and the report/badge reflects it.
- [ ] Azure Repos has no native PR-triggered pipeline run -- this pipeline is triggered solely by the build-validation branch policy. Confirm pushing a new commit to an open PR actually kicks off a fresh run (not just the PR's initial creation).

## Release (Auto): Prepare/Publish Release

- [ ] Push a `feat:` or `fix:` commit to `main` and confirm the `knope/release` PR opens (or updates) with the expected version bump and a correctly generated changelog entry.
- [ ] Push a `docs:`- or `chore:`-only commit and confirm no PR is opened/updated (the run stays green overall even though one step reports nothing to do -- see [Releasing](releasing.md)).
- [ ] Merge the release PR and confirm the tag and release notes get created correctly.
- [ ] Confirm the pipeline correctly tells "a normal push to `main`" apart from "this push is the release PR's own merge" -- it does this via an API check, not a native trigger, so push a second, unrelated commit right after a release and confirm it doesn't also try to publish.

## Release (Manual): Create Prerelease

- [ ] Manually dispatch with each label (`alpha`, `beta`, `rc`) and confirm each produces the expected version (e.g. `1.1.0-alpha.0`).
- [ ] Dispatch the same label again at the same commit and confirm it's blocked; push a new commit and confirm it's then allowed.
- [ ] Dispatch a different label (e.g. `alpha` to `beta`) at the same commit and confirm it's allowed without needing a new commit first.

## Cleaning Up

- [ ] Run `python cleanup_pipelines.py` in each throwaway repo's local directory (left there by the integration test, next to the repo's own files) before deleting the repos -- Azure DevOps has no bulk-delete UI for pipelines, so skipping this means removing each one by hand through its own settings page.
- [ ] Delete both repos (Project Settings > Repositories, or `az repos delete`).

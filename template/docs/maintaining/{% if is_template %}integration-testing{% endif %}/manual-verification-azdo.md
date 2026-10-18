# Manual Verification Checklist (Azure DevOps)

Work through this whole list by hand as the last step before a release. It covers only what
`mise run integration-test-azdo` can't check; each `integration-test-*-azdo` task prints its
own `[PASS]` or `[FAIL]` per check and a summary. See [Integration Testing](index.md) for what
the run creates and why Repo B's update is manual.

!!! bug "Checkbox state isn't saved"
    You can tick the boxes as you go, but reloading or leaving the page clears them. Finish the
    list in one sitting.

## Repo A

A copy at `HEAD`, with `code_coverage` on.

### After First Setup

*Automated: a bad PR title fails PR Validation, and the branch policy blocks completing it.*

- [ ] The setup checklist (printed at the end of `copier copy`) exists, and every item on it is
  done.
- [ ] The badges at the top of README.md render, with no broken images.
- [ ] `docs/assets/images/readme-logo.png` and `docs/assets/images/readme-screenshot.png`
  display in README.md, or that section is removed.
- [ ] The required pipeline variables are set (`mise run provision-secrets`, or see
  [Secrets and Tokens](../../reference/token-permissions.md)): none of the pipelines below fails
  on authentication.

### Maint (Auto) - Copier Update Check

*Automated: it runs and completes. Whether it reports no update available isn't, since `az`
can't easily read a run's step output; see the script's module docstring.*

- [ ] It reports **no update available**, since this repo is at `HEAD`.

### Maint (Auto) - Repo Health Check

*Automated: it runs and completes clean.*

- [ ] Add a broken link (a mistyped URL in a doc), confirm the next run reports it, then
  revert.

### Maint (Auto) - Renovate

*Automated: it runs and authenticates.*

- [ ] With an outdated dependency present, it opens or updates a PR for the bump.
- [ ] The build service has the permissions listed in
  [Prerequisites](../../getting-started/prerequisites.md). Without them, this pipeline fails to
  push or open its PR, with no clear permissions error.

### Docs (Auto) - Zensical Build & Publish

- [ ] Push a docs change to `main`, and confirm `docs-site/` is committed back with the new
  HTML.

### Test (Auto) - PR Validation

*Automated: a bad PR title fails, and a failing test suite fails and blocks completing the PR.*

- [ ] `coverage.xml` publishes and shows on the build (`code_coverage` is on for this repo).
- [ ] Pushing a new commit to an open PR starts a new run. Azure Repos has no PR trigger, so
  only the build validation policy starts this pipeline.

### Release (Auto) - Prepare & Publish Release

*Automated: a docs-only commit releases nothing, a `feat:` commit opens a release PR with the
bumped version in its title, and merging that PR creates a tag.*

- [ ] Right after a release, push an unrelated commit and confirm the pipeline doesn't publish
  again. It tells the release PR's own merge from a normal push through an API check, not a
  native trigger.

### Release (Manual) - Create Prerelease

*Automated: each label produces a matching tag, the same label at the same commit is blocked,
and a different label at the same commit is allowed.*

Nothing left to check for Repo A.

## Repo B

A copy at the last stable release tag, with `code_coverage` off. It stays at that tag until you
update it.

### Before Updating

*Automated, before you update anything: Maint (Auto) - Copier Update Check runs and completes.*

- [ ] It detects the newer version, and the Apprise notification arrives at `APPRISE_URL`.

### Running the Update

- [ ] In the repo, run `mise run copier-update`. Answer any new question the way a real user
  updating from the last release would.
- [ ] Commit and push the result.
- [ ] Run `mise run migrate-azdo-pipeline-names` to repoint any renamed pipeline registrations.

### After Updating

Run `mise run integration-test-verify-update-azdo -- --repo <repo> --local-path <path>`, with
the repo and path printed at the end of the original `mise run integration-test-azdo` run. It
checks that the update brought in current content, left no conflict markers, registered each
pipeline only under its current name, and that `Test (Auto) - PR Validation` triggers and
passes on a new PR.

## Cleaning Up

- [ ] Run `mise run integration-test-cleanup-azdo -- --org <org> --project <project>`. It lists
  every integration-test repo and pipeline in the project, including any left by a run that
  stopped partway, and deletes them once you confirm. Deleting a repo by hand leaves its
  pipelines behind, which this also finds.

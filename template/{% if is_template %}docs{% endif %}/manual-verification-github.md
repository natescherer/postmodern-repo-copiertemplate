# Manual Verification Checklist (GitHub)

Run through this **in full**, by hand, against the repos `mise run integration-test-gh` just created, as the last step before cutting a release -- see [Integration Testing](integration-testing.md) for what that command does and doesn't check on its own.

!!! bug "Checkbox state isn't saved"
    Boxes on this page are clickable so you can tick items off as you go, but nothing
    persists that -- reloading or leaving the page resets every box to unchecked. Treat
    it as a scratchpad for one sitting, not a record you can come back to.

## After First Setup

- [ ] The setup checklist (a GitHub Issue titled "Post-Setup Checklist," opened automatically on first copy) exists and every item on it has been addressed.
- [ ] Badges at the top of README.md render correctly (no broken image icons).
- [ ] `docs/images/readme-logo.png` and `docs/images/readme-screenshot.png` display correctly in README.md, or that section has been removed if unused.
- [ ] Required secrets/pipeline variables are provisioned (`mise run provision-secrets`, or see [Token Permissions](token-permissions.md)) -- confirmed by the pipelines below not failing with authentication errors.
- [ ] Branch protection actually **blocks** a bad PR, not just that the policy exists: open a throwaway PR with a failing check (e.g. a non-Conventional-Commit title) and confirm the merge button is disabled, not just that a check shows red.

## Maint (Auto): Copier Update Check

- [ ] Manually dispatch the workflow and confirm it completes without error.
- [ ] If a newer template version genuinely exists, confirm the Apprise notification actually arrives at the endpoint configured in `APPRISE_URL`.

## Maint (Auto): Link Check

- [ ] Manually dispatch the workflow and confirm it completes clean.
- [ ] Temporarily introduce a broken link (e.g. a typo'd URL in a doc) and confirm the next run catches it, then revert.

## Maint (Auto): Renovate

- [ ] Manually dispatch the workflow and confirm it authenticates successfully (no permission/token errors in the log).
- [ ] With at least one outdated dependency present, confirm it opens (or updates) a real pull request proposing the bump.

## Maint (Auto): All Contributors

(Public repos only.)

- [ ] Comment `@all-contributors please add @<username> for <contribution>` on an issue or PR, and confirm the bot opens a PR adding that person to the Contributors section of README.md.

## Docs (Auto): Zensical Publish to GitHub Pages

(`zensical_target: GitHub Pages` projects only.)

- [ ] Push a docs change to `main` and confirm the `dev` version of the docs site updates at `.../dev/`.
- [ ] Publish a release and confirm a new versioned copy is published, `latest` updates to point at it, and it becomes the default version served at the site root.

## Docs (Auto): Zensical Build & Publish

(`zensical_target: docs-site Directory in Repo` projects only.)

- [ ] Push a docs change to `main` and confirm `docs-site/` is committed back to the repo with the freshly built HTML.

## Test (Auto): PR Validation

- [ ] Open a PR with a non-Conventional-Commit title and confirm the check fails.
- [ ] Open a PR that fails `prek` or the test suite and confirm the required check fails, and that the branch policy above actually blocks merging it.
- [ ] With `code_coverage` on: confirm `coverage.xml` uploads to Codecov successfully and the report/badge reflects it.

## Release (Auto): Prepare/Publish Release

- [ ] Push a `feat:` or `fix:` commit to `main` and confirm the `knope/release` PR opens (or updates) with the expected version bump and a correctly generated changelog entry.
- [ ] Push a `docs:`- or `chore:`-only commit and confirm no PR is opened/updated (the run stays green overall even though one step reports nothing to do -- see [Releasing](releasing.md)).
- [ ] Merge the release PR and confirm the tag, GitHub Release, and its notes get created correctly.

## Release (Manual): Create Prerelease

- [ ] Manually dispatch with each label (`alpha`, `beta`, `rc`) and confirm each produces the expected version (e.g. `1.1.0-alpha.0`).
- [ ] Dispatch the same label again at the same commit and confirm it's blocked; push a new commit and confirm it's then allowed.
- [ ] Dispatch a different label (e.g. `alpha` to `beta`) at the same commit and confirm it's allowed without needing a new commit first.

## Cleaning Up

- [ ] Delete both throwaway repos (`gh repo delete <repo> --yes`, or via the web UI) -- deleting a GitHub repo removes everything registered against it, workflows included.

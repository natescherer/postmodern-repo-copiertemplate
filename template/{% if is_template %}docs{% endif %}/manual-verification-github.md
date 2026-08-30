# Manual Verification Checklist (GitHub)

Run through this **in full**, by hand, as the last step before cutting a release. See [Integration Testing](integration-testing.md) for what `mise run integration-test-gh` creates and why the update step below isn't automated. Most of Repo A's checks are now automated; each `mise run integration-test-*-gh` invocation prints its own PASS/FAIL per check, plus a summary; what's below is what's left for a human.

!!! bug "Checkbox state isn't saved"
    Boxes on this page are clickable so you can tick items off as you go, but nothing
    persists that; reloading or leaving the page resets every box to unchecked. Treat
    it as a scratchpad for one sitting, not a record you can come back to.

## Repo A

Fresh copy at `HEAD`, `zensical_target: GitHub Pages`, `code_coverage` on.

### After First Setup

*Branch protection actually blocking a bad PR is automated; see "a bad-title PR fails Test (Auto): PR Validation" and "branch protection blocks merging a PR with a bad PR title" in the script's own output.*

- [ ] The setup checklist (a GitHub Issue titled "Post-Setup Checklist," opened automatically on first copy) exists and every item on it has been addressed.
- [ ] Badges at the top of README.md render correctly (no broken image icons).
- [ ] `docs/images/readme-logo.png` and `docs/images/readme-screenshot.png` display correctly in README.md, or that section has been removed if unused.
- [ ] Required secrets/pipeline variables are provisioned (`mise run provision-secrets`, or see [Token Permissions](token-permissions.md)); confirmed by the pipelines below not failing with authentication errors.

### Maint (Auto): Copier Update Check

*Dispatching it, confirming it completes without error, and confirming it correctly reports no update available are all automated.*

Nothing left here for Repo A.

### Maint (Auto): Repo Health Check

*Dispatching it and confirming it completes clean is automated.*

- [ ] Temporarily introduce a broken link (e.g. a typo'd URL in a doc) and confirm the next run catches it, then revert.

### Maint (Auto): Renovate

Renovate on GitHub runs as the externally-hosted [Renovate GitHub App](https://github.com/apps/renovate), not a workflow in this repo; there's nothing to dispatch or verify from inside this repo's own CI.

- [ ] Confirm the app is installed with access to this repo (Settings > Integrations, or your account/org's installed GitHub Apps).
- [ ] Wait for its own schedule (or check its dashboard for how to trigger an out-of-schedule run) and confirm it authenticates successfully.
- [ ] With at least one outdated dependency present, confirm it opens (or updates) a real pull request proposing the bump.

### Maint (Auto): All Contributors

(Public repos only; both repos are Public, so either would do; this repo is as good a place as any.)

- [ ] Comment `@all-contributors please add @<username> for <contribution>` on an issue or PR, and confirm the bot opens a PR adding that person to the Contributors section of README.md.

### Docs (Auto): Zensical Publish to GitHub Pages

- [ ] Push a docs change to `main` and confirm the `dev` version of the docs site updates at `.../dev/`.
- [ ] Publish a release and confirm a new versioned copy is published, `latest` updates to point at it, and it becomes the default version served at the site root.

### Test (Auto): PR Validation

*A bad-title PR failing, and a PR with a failing test suite failing and being blocked from merging, are both automated.*

- [ ] Confirm `coverage.xml` uploads to Codecov successfully and the report/badge reflects it; `code_coverage` is on for this repo.

### Release (Auto): Prepare/Publish Release

*The full flow is automated: a docs-only commit staying a no-op, a feat commit opening a release PR with a version-bump title, and merging that PR creating a tag and a GitHub Release.*

Nothing left here for Repo A.

### Release (Manual): Create Prerelease

*The full flow is automated: dispatching each label produces a matching tag, re-dispatching the same label at the same commit is blocked, and dispatching a different label at the same commit is allowed.*

Nothing left here for Repo A.

## Repo B

Copied at the last stable release tag, `zensical_target: docs-site Directory in Repo`, `code_coverage` off. Still at that tag; nothing here has been updated for you.

### Before Updating

*Dispatching Maint (Auto): Copier Update Check, confirming it completes without error, and confirming it correctly detects a newer version is available are all automated (part of `mise run integration-test-gh`, before you update anything).*

- [ ] Confirm the Apprise notification actually arrives at the endpoint configured in `APPRISE_URL`.

### Running the Update

- [ ] `cd` into the repo and run `mise run copier-update` yourself. If it prompts for a new question, answer it the way you'd want a real user updating from the last release to answer it, not whatever's quickest.
- [ ] Commit and push the result.

### After Updating

Run `mise run integration-test-verify-update-gh -- --repo <repo> --local-path <path>` (the repo/path are printed at the end of the original `mise run integration-test-gh` run). It automates everything that needs checking here: the update actually pulled in current content, applied with no leftover conflict markers, and `Test (Auto): PR Validation` still triggers and passes on a fresh PR against the updated repo.

## Cleaning Up

- [ ] Delete both throwaway repos (`gh repo delete <repo> --yes`, or via the web UI); deleting a GitHub repo removes everything registered against it, workflows included.

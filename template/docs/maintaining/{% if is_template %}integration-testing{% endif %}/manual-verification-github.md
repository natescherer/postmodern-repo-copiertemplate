# Manual Verification Checklist (GitHub)

Work through this whole list by hand as the last step before a release. It covers only what
`mise run integration-test-gh` can't check; each `integration-test-*-gh` task prints its own
`[PASS]` or `[FAIL]` per check and a summary. See [Integration Testing](index.md) for what the
run creates and why Repo B's update is manual.

!!! bug "Checkbox state isn't saved"
    You can tick the boxes as you go, but reloading or leaving the page clears them. Finish the
    list in one sitting.

## Repo A

A copy at `HEAD`, with `zensical_target: GitHub Pages` and `code_coverage` on.

### After First Setup

*Automated: a bad PR title fails PR Validation, and branch protection blocks merging it.*

- [ ] The setup checklist (the "Template Setup Checklist" issue, opened on first copy) exists,
  and every item on it is done.
- [ ] The badges at the top of README.md render, with no broken images.
- [ ] `docs/assets/images/readme-logo.png` and `docs/assets/images/readme-screenshot.png`
  display in README.md, or that section is removed.
- [ ] The required secrets are set (`mise run provision-secrets`, or see
  [Secrets and Tokens](../../reference/token-permissions.md)): none of the workflows below fails
  on authentication.

### Maint (Auto): Copier Update Check

*Automated: it runs, completes, and reports no update available.*

Nothing left to check for Repo A.

### Maint (Auto): Repo Health Check

*Automated: it runs and completes clean.*

- [ ] Add a broken link (a mistyped URL in a doc), confirm the next run reports it, then
  revert.

### Maint (Auto): Renovate

On GitHub, Renovate runs as the [Renovate GitHub App](https://github.com/apps/renovate), outside
this repo's CI, so there's nothing to dispatch.

- [ ] The app is installed with access to this repo (**Settings > Integrations**, or the
  account's or org's installed apps).
- [ ] On its next scheduled run (or a manual run from its dashboard), it authenticates.
- [ ] With an outdated dependency present, it opens or updates a PR for the bump.

### Maint (Auto): All Contributors

Public repos only. Both repos are public; use this one.

- [ ] Comment `@all-contributors please add @<username> for <contribution>` on an issue or PR,
  and confirm the bot opens a PR adding them to README.md's Contributors section.

### Docs (Auto): Zensical Publish to GitHub Pages

- [ ] Push a docs change to `main`, and confirm the site's `dev` version updates at `.../dev/`.
- [ ] Publish a release, and confirm a new version is published, `latest` points at it, and the
  site root serves it.

### Test (Auto): PR Validation

*Automated: a bad PR title fails, and a failing test suite fails and blocks the merge.*

- [ ] `coverage.xml` uploads to Codecov, and the report and badge reflect it (`code_coverage`
  is on for this repo).

### Release (Auto): Prepare/Publish Release

*Automated: a docs-only commit releases nothing, a `feat:` commit opens a release PR with the
bumped version in its title, and merging that PR creates a tag and a GitHub Release.*

Nothing left to check for Repo A.

### Release (Manual): Create Prerelease

*Automated: each label produces a matching tag, the same label at the same commit is blocked,
and a different label at the same commit is allowed.*

Nothing left to check for Repo A.

## Repo B

A copy at the last stable release tag, with `zensical_target: docs-site Directory in Repo` and
`code_coverage` off. It stays at that tag until you update it.

### Before Updating

*Automated, before you update anything: Maint (Auto): Copier Update Check runs, completes, and
detects the newer version.*

- [ ] The Apprise notification arrives at the endpoint in `APPRISE_URL`.

### Running the Update

- [ ] In the repo, run `mise run copier-update`. Answer any new question the way a real user
  updating from the last release would.
- [ ] Commit and push the result.

### After Updating

Run `mise run integration-test-verify-update-gh -- --repo <repo> --local-path <path>`, with the
repo and path printed at the end of the original `mise run integration-test-gh` run. It checks
that the update brought in current content, left no conflict markers, and that
`Test (Auto): PR Validation` triggers and passes on a new PR.

## Cleaning Up

- [ ] Delete both repos (`gh repo delete <repo> --yes`, or the web UI). Deleting a GitHub repo
  removes its workflows too.

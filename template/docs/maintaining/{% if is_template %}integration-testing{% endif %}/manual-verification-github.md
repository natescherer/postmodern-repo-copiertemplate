# Manual Verification Checklist (GitHub)

Work through this whole list by hand as the last step before a release. It covers only what
`mise run integration-test-gh` can't check; each `integration-test-*-gh` task prints its own
`[PASS]` or `[FAIL]` per check and a summary. See [Integration Testing](index.md) for what the
run creates and why Repo B's update is manual.

Run each command from the repo's local clone, at the path the run's summary prints for it.

!!! bug "Checkbox state isn't saved"
    You can tick the boxes as you go, but reloading or leaving the page clears them. Finish the
    list in one sitting.

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

### Maint (Auto): Copier Update Check

*Automated: it runs, completes, and reports no update available.*

Nothing left to check for Repo A.

### Maint (Auto): Repo Health Check

*Automated: it runs and completes clean.*

- [ ] Run it on a branch with a broken link:

    ```sh
    git switch main
    git pull
    git switch -c integration-test/broken-link
    echo "[Broken link](https://example.invalid/)" >> README.md
    git commit -am "docs: add a broken link"
    git push -u origin integration-test/broken-link
    gh workflow run maint-auto-repohealthcheck.yml --ref integration-test/broken-link
    ```

    The run fails, and its **Check for Broken Links** step names `https://example.invalid/`.

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

*Automated: a bad PR title fails, and a failing test suite fails and blocks the merge.*

- [ ] The PR Validation run for the docs-change PR uploads `coverage.xml` (its
  **Upload Coverage to Codecov** step succeeds), and the coverage badge in README.md shows a
  percentage (`code_coverage` is on for this repo).

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

- [ ] Its run's **Notify if Update is Available** step succeeds.

### Running the Update

- [ ] Update on a branch, pressing Enter at each prompt to accept the default:

    ```sh
    git switch -c integration-test/copier-update
    mise run copier-update
    git add -A
    git commit -m "chore: copier update"
    git push -u origin integration-test/copier-update
    gh pr create --title "chore: copier update" --body "Integration test."
    gh pr merge --squash --auto --delete-branch
    ```

### After Updating

Once the update's PR merges, run the verify command in step 2 of the run's summary. It checks
that the update brought in current content, left no conflict markers, and that
`Test (Auto): PR Validation` triggers and passes on a new PR.

## Cleaning Up

- [ ] Run the cleanup command in the run's summary, and confirm. It deletes every
  integration-test repo under your account, including any left by a run that stopped partway.
  It needs the `delete_repo` scope: `gh auth refresh -h github.com -s delete_repo`.

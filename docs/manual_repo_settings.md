# Manual Repo Settings

When you use the [Settings GitHub App](https://github.com/apps/settings), it syncs the repo
settings, labels, and branch protection ruleset described below from the committed
`.github/settings.yml` automatically. If you don't want to install that app (or can't, e.g. it's
not been approved for your organization), here's how to apply the same configuration by hand
through the GitHub UI. `.github/settings.yml` is the source of truth for the exact values below --
if the two ever disagree, trust the file.

## Labels

Under the repo's **Issues** tab, open **Labels**, and create:

| Name | Color | Description |
| --- | --- | --- |
| `awaiting pr` | `#668F04` | Awaiting completion of a PR from a contributor |
| `blocked` | `#B60205` | Blocked by an external dependency |

## Merge Options

Under **Settings > General > Pull Requests**, enable:

- **Allow auto-merge**
- **Automatically delete head branches**

## Branch Protection

Under **Settings > Rules > Rulesets**, create a new ruleset:

- Name: `default-branch-protection`
- Enforcement status: **Active**
- Target branches: **Default branch**
- Rules:
    - **Restrict deletions**
    - **Block force pushes**
    - **Require a pull request before merging**, with:
        - Required approvals: `0`
        - Dismiss stale pull request approvals when new commits are pushed: off
        - Require review from Code Owners: off
        - Require approval of the most recent reviewable push: off
        - Require conversation resolution before merging: off
    - **Require status checks to pass**, with:
        - Require branches to be up to date before merging: on
        - Status check: `tests` (the job in `[Test] PR Validation`)
- Bypass list: add **Repository admin**, with bypass mode **Pull requests only** -- this lets
  repo admins use the "Merge without waiting for requirements to be met" button instead of being
  blocked entirely.

## GitHub Pages Environment

After the first successful Pages deployment, an environment named `github-pages` will exist under
**Settings > Environments**. Open it and ensure **Deployment branches and tags** is set to
**All branches** (no restriction).

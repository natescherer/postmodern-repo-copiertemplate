# Azure DevOps Limitations

**Azure DevOps support is deprecated and will eventually be removed.** It's kept around for
existing organizational needs, not as a recommendation -- prefer GitHub for new projects unless
you specifically need Azure DevOps.

Support for Azure DevOps is provided on a best-effort basis and has some limitations compared to GitHub.

- Public projects not supported
  - It is assumed that if you are using Azure DevOps, it is due to organizational requirements.
- GitHub-specific features not implemented
  - Custom Issue tags
- Branch protection is partial
  - When `repo_setup_actions` triggers setup, a required PR-validation build policy is created
    automatically on the default branch (the `pr_validation` pipeline must pass before a PR can
    complete), along with a **Project Administrators** bypass permission mirroring GitHub's
    admin `bypass_actors` entry. Unlike GitHub's ruleset, force-push and branch deletion on the
    default branch are **not** blocked -- this is a known, currently-accepted gap. If you chose
    `repo_setup_actions: None`, see [Manual Repo Settings](../manual_repo_settings.md) for how to
    set this up by hand.
- `zensical_target` is always `docs_site Directory in Repo`
  - `GitHub Pages` isn't offered, so Azure DevOps projects never get the release-versioned docs
    site that target provides — see [Getting Started](../index.md#documentation)
- Renovate needs a one-time manual permission grant
  - Unlike GitHub (which uses the Renovate GitHub App), Renovate runs here as a self-hosted
    scheduled pipeline (`.azurepipelines/renovate.yml`), authenticated via the pipeline's own
    `$(System.AccessToken)` rather than a stored secret. For it to push branches and open PRs,
    grant the **Project Collection Build Service** account **Contribute**, **Create branch**,
    and **Contribute to pull requests** on this repo (Project Settings > Repositories > this
    repo > Security) -- this is normally a one-time, org-wide grant, not something you need to
    repeat per repo.
- `release` pipeline is manually queued
  - Unlike GitHub's Release Please, which reacts to every push to `main`, this pipeline has no
    trigger and must be run by hand (Pipelines > select the pipeline > Run) whenever you want a
    release. This is intentional, not a missing-automation gap: `cz bump` (commitizen) computes
    the next version and changelog directly against whatever commits already exist on `main` at
    queue time, so there's no equivalent to release-please's own PR-tracking state that would
    need a push trigger to stay current.
- Can't test (or otherwise create) a GitHub-target repo from Azure DevOps-hosted CI
  - `.azurepipelines/integration_test.yml` only ever creates and verifies an Azure DevOps-hosted
    throwaway repo -- it has no `gh` CLI setup or GitHub token, so it can't scaffold a
    GitHub-target child the way GitHub's own integration test workflow scaffolds an Azure
    DevOps-target one (it already has `AZURE_DEVOPS_EXT_PAT` wired up for exactly that). This is
    an intentional, accepted asymmetry, not a gap to close: a regression in GitHub-target
    scaffolding is still caught, just only by GitHub-hosted CI.

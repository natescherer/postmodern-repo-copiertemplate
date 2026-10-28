# Azure DevOps Limitations

**Azure DevOps support is deprecated and will be removed in a future major version.** It stays
for organizations that require it; use GitHub for new projects unless you need Azure DevOps.

Azure DevOps support is best-effort, and differs from GitHub in these ways:

- **No public projects.** Azure DevOps projects are assumed to exist for organizational
  requirements.
- **No GitHub-only features,** such as custom issue labels.
- **Partial branch protection.** Repo setup creates a required build validation policy on the
  default branch (`Test (Auto) - PR Validation` must pass before a PR completes), plus a
  **Project Administrators** bypass permission that matches GitHub's admin bypass. Unlike
  GitHub's ruleset, it doesn't block force pushes or deleting the default branch. With
  `repo_setup_actions: None`, set it up by hand with [Manual Repo Settings](manual-repo-settings.md).
- **`zensical_target` is always `docs-site Directory in Repo`.** `GitHub Pages` isn't offered,
  so there's no release-versioned docs site; see [Features](features.md#documentation).
- **Renovate runs as a pipeline job, not an app.** The Renovate job in
  `.azurepipelines/maint-auto-monthlymaintenance.yml` runs on a schedule and authenticates with the pipeline's own `$(System.AccessToken)`, not a stored
  secret. It pushes branches and opens PRs as the build service identity, so it needs the same
  permissions as the release and docs pipelines; see
  [Prerequisites](../getting-started/prerequisites.md).
- **The release pipeline detects PR merges through the API.** The release flow matches GitHub's:
  every push to `main` opens or updates the `knope/release` PR, and merging it publishes the
  release; see [Releasing](../maintaining/releasing.md). Azure Pipelines has no "PR completed"
  trigger, only push triggers, so `Release (Auto) - Prepare & Publish Release` checks whether
  the last completed PR from `knope/release` into `main` matches the commit that started the
  run. A prerelease is a manual run of the same pipeline (**Pipelines**, select it, **Run**)
  with a prerelease label instead of `none`.
- **No semantic linter for pipeline YAML.** `ryl` checks `.azurepipelines/*.yml` as YAML, but
  no standalone tool checks Azure Pipelines schemas the way `actionlint` checks GitHub Actions
  workflows.

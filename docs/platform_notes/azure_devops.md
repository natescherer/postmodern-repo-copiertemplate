# Azure DevOps Limitations

Support for Azure DevOps is provided on a best-effort basis and has some limitations compared to GitHub.

- Public projects not supported
  - It is assumed that if you are using Azure DevOps, it is due to organizational requirements.
- GitHub-specific features not implemented
  - Custom Issue tags
  - Renovate
- Branch protection policies not set
  - It is assumed that your organization will be enforcing this at the project level
- `zensical_target` is always `docs_site Directory in Repo`
  - `GitHub Pages` isn't offered, so Azure DevOps projects never get the release-versioned docs
    site that target provides — see [Getting Started](../index.md#documentation)

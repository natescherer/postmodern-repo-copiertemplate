# Compatibility

## Workstations

Windows, macOS, and Linux are all supported. `mise run` tasks and Git hooks work from any shell
mise is activated in, including PowerShell, Bash, and zsh.

## Tools

mise installs every tool this project uses, at the version pinned in `mise.toml`. Two minimums
apply on top of that, and Renovate keeps both current:

- **mise itself** must be at least the `min_version` in `mise.toml`. An older mise refuses to
  run and says so; `mise self-update` fixes it.
- **Copier** must be at least the parent template's `_min_copier_version`. `mise run
  copier-update` runs the newest Copier, so this only matters if you run Copier some other
  way, which also needs Python 3.11 or later for the template's migrations.

## CI

GitHub Actions workflows and Azure Pipelines both run on hosted `ubuntu-latest` runners. A
self-hosted runner needs Linux with Bash, Git, and curl, plus PowerShell 7 and jq on
Azure DevOps; mise installs everything else.

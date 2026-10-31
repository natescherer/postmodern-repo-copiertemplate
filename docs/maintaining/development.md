# Development

## Setup

1. Complete the [workstation prerequisites](../getting-started/prerequisites.md#workstation-prerequisites).
1. Clone the repo and, from its root, run:

    ```bash
    mise trust
    mise install
    ```

`mise install` installs every tool this project uses at its pinned version, then installs
[prek](https://prek.j178.dev/)'s Git hooks: linters and formatters run on each commit, and
[committed](https://github.com/crate-ci/committed) checks each commit message. To run every
hook against the whole repo:

```bash
mise x -- prek run -c .config/prek.toml --all-files
```

## Branching

This project uses [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow):
one long-lived branch, `main`, plus a short-lived branch for each change.

- **`main` is always releasable.** Everything on it has passed PR Validation, and any push to
  it can become the next release; see [Releasing](releasing.md). Nothing lands on `main` except
  through a pull request; branch protection on GitHub and branch policies on
  Azure DevOps enforce that.
- **One change per branch, branched from the latest `main`.** Keep it short-lived: open the pull
  request early, merge it once it's green, and delete the branch.
- **Branches stay independent.** Branch from `main`, not from another unmerged branch, so pull
  requests can merge in any order. If `main` moves on, rebase onto it.
- **There are no `develop`, release, or hotfix branches.** A fix for something already released
  is just another branch from `main`, and the release PR picks up whatever has merged since the
  last release.

## Commits and Pull Requests

Commit messages and PR titles follow [Conventional Commits](https://www.conventionalcommits.org/)
(`type: summary`). The type decides the next version bump; see [Releasing](releasing.md).

PR Validation checks that the PR title is a Conventional Commit and runs the prek hooks against
every file the PR changes. On GitHub, PRs are squash-merged, so the PR title becomes the
commit message on `main`.

## Tasks

Run any of these with `mise run <task>`.

| Task | What it does |
| ---- | ------------ |
| `copier-update` | Pulls in the latest parent template changes; see [Updating from the Parent Template](updating-from-template.md) |
| `set-lifecycle` | Changes only the `lifecycle` answer, without pulling in a template update |
| `docs-server` | Serves these docs locally with live reload |
| `provision-secrets` | Sets the secrets CI needs, via masked prompts; see [Secrets and Tokens](../reference/token-permissions.md) |
| `renovate-lookup` | Runs Renovate locally in dry-run mode to show what it detects, without pushing anything; see [Adding a Dependency or Tool](#adding-a-dependency-or-tool) |
| `migrate-azdo-pipeline-names` | (Azure DevOps only) Brings existing pipeline registrations in line after a template update renames or merges their files |
| `test` | Runs the render-validation test suite |
| `template-docs-server` | Previews the template's docs rendered under every answer combination |
| `integration-test-gh` / `integration-test-azdo` | Creates real throwaway repos from this template and checks them; see [Integration Testing](integration-testing/index.md) |
| `integration-test-verify-update-gh` / `integration-test-verify-update-azdo` | Verifies a manually updated integration-test repo |
| `integration-test-cleanup-gh` / `integration-test-cleanup-azdo` | Deletes every integration-test repo (and, on Azure DevOps, pipeline), including those of a run that stopped partway |

## Adding a Dependency or Tool

Pin every dependency to an exact version, never a range, `latest`, or an unversioned install
script, so every contributor and CI run gets the same one and Renovate can propose each bump.
Where it goes depends on what it is:

- **Command-line tools** (linters, formatters, build and release tools): add them to `mise.toml`,
  or `mise.ci.toml` if only CI needs them. A pin in a `.jinja` file under
  `template/` also needs a `{#- renovate: datasource=... depName=... #}` comment above it, which
  this repo's custom managers match.
- **Libraries and packages**: declare them in the language's own manifest or lockfile. Renovate
  detects [many of these](https://docs.renovatebot.com/modules/manager/) natively, but not every
  ecosystem or file format.

Then:

1. **Confirm Renovate detects it.** Run `mise run renovate-lookup` and check that the dependency
   appears, with the right version, in the `packageFiles with updates` log entry. Renovate skips
   an unsupported manifest, and a custom manager regex that captures too much, without an error.
1. **Add a custom manager if it doesn't.** A regex entry under `customManagers` in
   `renovate.json` can track a version Renovate can't find on its own, such as one inside a
   script.
1. **Group duplicates.** If one dependency is pinned under two names (for example, as a mise tool
   and as a CI step), a `packageRules` entry with a shared `groupName` bumps both in one PR.
1. **Explain any gap.** If a dependency has no trackable version source at all, say why in a
   comment next to where it's installed.

## Documentation

Docs live in `docs/` and are built with [Zensical](https://zensical.org/). Add every new page to
`nav` in `zensical.toml`; the render-validation tests fail on a page missing from it.

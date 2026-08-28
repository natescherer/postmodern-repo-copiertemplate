# Template Questions

This page walks through what each Copier question controls, and what it triggers behind the
scenes. Questions not listed here (`repo_name`, `author_name`, `project_name`,
`project_description`) are self-explanatory and only affect their own value. Neither platform
prompts for a token anymore — repo setup uses `gh auth login` (GitHub) or `az login` (Azure
DevOps) instead — see [Prerequisites](prerequisites.md) and [Token Permissions](token-permissions.md).

## `developer_platform`: GitHub / Azure DevOps

Determines which platform-specific files get generated: GitHub gets `.github/workflows/`,
Azure DevOps gets `.azurepipelines/`. This choice also locks out some other options — Azure DevOps
projects can't use `GitHub Pages` for `zensical_target`, and `project_visibility` defaults to
`Private` since Azure DevOps doesn't support public projects the same way. See
[Azure DevOps Limitations](platform-notes/azure-devops.md) for platform-specific details.

**Azure DevOps support is deprecated** and will eventually be removed from this template
entirely. Prefer GitHub for new projects unless you specifically need Azure DevOps.

## `repo_setup_actions`: Create Repo / Set Repo Rules / None

Controls which setup automation runs after the template is copied. `.github/settings.yml` (GitHub
only) is always generated regardless of this answer -- see below. Choosing anything but `None`
triggers this question's validator, which checks the relevant platform CLI (`gh` or `az`) is
installed and authenticated *before* letting you proceed -- see [Prerequisites](prerequisites.md).

- **Create Repo** — creates the remote repo; on GitHub also sets Actions workflow permissions,
  sets up GitHub Pages if applicable, and (for public repos) enables CodeQL code scanning's
  default setup and private vulnerability reporting; on Azure DevOps also registers pipelines for
  each file under `.azurepipelines/`.
- **Set Repo Rules** — skips repo creation (for an existing repo) but still applies the other
  automation above.
- **None** — skips all of it; you're on your own for repo creation and settings.

Whichever you choose, GitHub projects still get a generated `.github/settings.yml`, applied
automatically if you've installed the [Settings GitHub App](https://github.com/apps/settings) (see
[Prerequisites](prerequisites.md)) or by hand per [Manual Repo Settings](manual-repo-settings.md)
if you haven't. Choosing `None` prints a reminder about this at the end of the run.

## `project_type`: Standard / Template

**Standard** generates a normal project repo. **Template** additionally generates a `copier.yml`
of its own (so your project can itself be used as a Copier template — this is how this repo
works), a fuller `docs/` set explaining the template's own features, and template-authoring tasks
like `mise run integration-test-gh`/`integration-test-azdo`.

## `project_visibility`: Public / Private

Public repos get contributor-facing files that don't make sense for private code: the
`CONTRIBUTING.md` "Ground Rules" section, `.all-contributorsrc`, and the All Contributors
workflow. See [Public vs Private Repos](public-vs-private-repos.md) for the full breakdown.

## `license`: MIT / None

Controls whether a `LICENSE` file is generated and whether the README claims MIT licensing. If you
pick `None` on a Public repo, the README instead shows a notice that the project currently has no
license set (meaning nobody may legally use, copy, or contribute to it without your permission) —
see [Public vs Private Repos](public-vs-private-repos.md#support-files). `MIT` isn't offered for Private
repos, since a license only matters once code is visible to others.

## `zensical_target`: GitHub Pages / docs-site Directory in Repo

Chooses where rendered documentation ends up:

- **GitHub Pages** — deploys via `docs-auto-zensical.yml`, using `mike` to keep a version-aliased
  history (`latest`, `dev`, and per-release versions) of the docs site.
- **docs-site Directory in Repo** — builds via `docs-auto-mkdocs.yml` into a `docs-site/` folder
  committed to the repo, always reflecting the latest `main`, with no version history. This is the
  only option for Azure DevOps projects.

## `lifecycle`: Pre-Alpha / Alpha / Beta / Stable / Inactive

Controls the status banner shown at the top of the README, and (for GitHub projects moving to
Stable) prompts a one-time command to open a pull request bumping the version to `1.0.0`. See
[Lifecycle Management](lifecycle-management.md) for the full behavior.

## `agent_instructions`: Yes / No

Whether to generate `AGENTS.md` (repo conventions for AI coding agents) and `CLAUDE.md` (a
one-line `@AGENTS.md` import, so Claude Code picks up the same content). Choosing `No` skips
both files entirely.

## `code_coverage`: Yes / No

Whether to wire up code coverage reporting: the Codecov GitHub Action on GitHub, or Azure
Pipelines' built-in coverage publishing on Azure DevOps. This only plumbs the upload/publish
step -- it expects a `coverage.xml` (Cobertura format) at the repo root, and doesn't produce
one itself. Your own test command (or a language-specific child template built from this one)
needs to actually generate that file, e.g. `pytest-cov`'s `--cov-report=xml` for Python or
Pester's `-CodeCoverage` for PowerShell.

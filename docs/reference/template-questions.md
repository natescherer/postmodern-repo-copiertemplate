# Template Questions

This page covers what each Copier question controls and what it sets up. The questions not
listed (`repo_name`, `author_name`, `project_name`, `project_description`) only set their own
value. Repo setup authenticates through your `gh auth login` or `az login` session, not a
token; see [Prerequisites](../getting-started/prerequisites.md) and
[Secrets and Tokens](token-permissions.md).

Questions marked as fixed after the first copy aren't asked again on update; Copier keeps the
recorded answer.

## `developer_platform`: GitHub / Azure DevOps

Decides which platform's files are generated: `.github/workflows/` for GitHub, or
`.azurepipelines/` for Azure DevOps. It also limits other answers: Azure DevOps projects can't
use `GitHub Pages` for `zensical_target`, and `project_visibility` defaults to `Private`. See
[Azure DevOps Limitations](azure-devops.md). Fixed after the first copy.

**Azure DevOps support is deprecated** and will be removed in a future major version. Use
GitHub for new projects unless you need Azure DevOps.

## `repo_setup_actions`: Create Repo / Set Repo Rules / None

Controls which setup runs after the copy. Choosing anything but `None` runs a check that the
platform CLI (`gh` or `az`) is installed and logged in before Copier continues; see
[Prerequisites](../getting-started/prerequisites.md). Fixed after the first copy.

- **Create Repo** creates the remote repo. On GitHub, it also sets Actions workflow permissions,
  sets up GitHub Pages when used, and, for public repos, enables CodeQL default setup and
  private vulnerability reporting. On Azure DevOps, it also registers a pipeline for each `.yml`
  file directly in `.azurepipelines/`.
- **Set Repo Rules** (GitHub only) applies the same settings to an existing repo without
  creating one. Azure DevOps registers pipelines from YAML on the remote repo, which an existing
  project hasn't pushed at copy time, so choose `None` there and follow
  [Manual Repo Settings](manual-repo-settings.md).
- **None** skips all of it; create the repo and apply its settings yourself.

GitHub projects get `.github/settings.yml` whatever you choose. Create Repo and Set Repo Rules
apply it with [gh-settings](https://github.com/noirbizarre/gh-settings); with None, run `mise run
sync-repo-settings` once the repo exists, or apply it by hand with
[Manual Repo Settings](manual-repo-settings.md).

## Repo location: `github_username` / `github_org` / `azdo_org` / `azdo_project`

Where the repo lives. Copier asks only the pair for your `developer_platform`. Fixed after the
first copy.

- **`github_username`**: your GitHub username. It defaults to the username in a GitHub noreply
  `user.email` (`12345+username@users.noreply.github.com`); with any other email, check the
  default before accepting it.
- **`github_org`**: the organization that owns the repo. Leave it as `None` to create the repo
  under `github_username`.
- **`azdo_org`** / **`azdo_project`**: the Azure DevOps organization and project the repo is
  created in. The project name can contain spaces.

## `project_type`: Standard / Template

The other foundational decision, with `developer_platform`; see
[the home page](../index.md#the-big-decision). Fixed after the first copy.

**Standard** generates a project repo, a starting point for whatever the project is for.
**Template** also generates:

- its own `copier.yml`, so the project can be used as a Copier template, as this repo is;
- fuller docs about the template's own features, including this page;
- template-authoring tasks such as `mise run integration-test-gh` and `integration-test-azdo`.

See [Extending This Template](../maintaining/extending-the-template.md) for what comes next:
whether your template will be extended in turn, and checklists for adding to it.

## `extensible_template`: Yes / No

Asked only for `Template`: whether other Copier templates will be built from this one.

- **No** (the default for a new copy) makes a leaf template. Its projects are always
  Standard, so its copy of `template/` leaves out the template-only files (the child
  `copier.yml`, tests, scripts, and template docs) and has the `is_template`,
  `is_standard`, and `is_extensible` conditions folded out of the files it keeps. Its own
  `copier.yml` doesn't ask `project_type`. Most templates, such as a company's internal deployment template, are
  leaf templates.
- **Yes** makes an extensible template. It keeps the whole `template/`, so its projects
  can be templates too, as this template's are.

An existing Template project is asked once on its next update, with yes preselected, which
keeps its current behavior. Answering no then removes the template-only files from its
`template/`. See [Extending This Template](../maintaining/extending-the-template.md#start-here-will-other-templates-build-on-yours).

## `project_visibility`: Public / Private

A Public repo is an open-source project: visible to anyone and open to contributions. A Private
repo is closed-source and requires authentication to access. Fixed after the first copy.
Private repos omit what only public code needs:

- **All Contributors**: `.all-contributorsrc` and its workflow, which credit contributors in the
  README.
- **`CODE_OF_CONDUCT.md`** and **`CONTRIBUTING.md`**. Add your own if you want them; template
  updates leave files the template doesn't generate alone.
- **`LICENSE`**: see `license` below.
- **GitHub security scanning**: CodeQL default setup, private vulnerability reporting, and
  secret scanning with push protection. These are free on public repos and need a paid GitHub
  Advanced Security license on private ones; see [Manual Repo Settings](manual-repo-settings.md)
  to enable secret scanning by hand.

## `license`: MIT / None

Controls whether a `LICENSE` file is generated and whether the README states MIT licensing. It
defaults to `MIT` for public repos and `None` for private ones, which can't choose `MIT`: a
license only matters once others can see the code. With `None` on a public repo, the setup
checklist reminds you to add a license; without one, nobody may legally use, copy, or
contribute to the code.

## `zensical_target`: GitHub Pages / docs-site Directory in Repo

Chooses where the built docs go. Fixed after the first copy.

- **GitHub Pages**: `.github/workflows/docs-auto-zensical.yml` deploys them, using `mike` to keep
  versions (`latest`, `dev`, and one per release).
- **docs-site Directory in Repo**: `.github/workflows/docs-auto-zensicalcommit.yml` (GitHub) or
  `.azurepipelines/docs-auto-zensicalcommit.yml` (Azure DevOps) builds them into a committed
  `docs-site/` folder, rebuilt from the latest `main`, with no version history. Azure DevOps
  projects can only use this option.

## `lifecycle`: Pre-Alpha / Alpha / Beta / Stable / Inactive

Controls the status notice at the top of the README. Change it with `mise run set-lifecycle`,
which updates or removes the notice:

- **Pre-Alpha** / **Alpha**: not ready for public use.
- **Beta**: use with caution.
- **Stable**: production-ready; no notice.
- **Inactive**: no longer under active development.

Moving to Stable for the first time pins the next release to `1.0.0` in
`.config/knope-release-override.json`; see [Releasing](../maintaining/releasing.md#graduating-to-100).

## `agent_instructions`: Yes / No

Whether to generate `AGENTS.md`, the repo's conventions for AI coding agents.

## `code_coverage`: Yes / No

Whether to publish code coverage: through the Codecov GitHub Action on GitHub, or Azure
Pipelines' built-in coverage publishing on Azure DevOps. It publishes a Cobertura `coverage.xml`
from the repo root but doesn't generate one. Your test command, or a language-specific child
template, produces it: for example `pytest-cov`'s `--cov-report=xml` for Python, or Pester's
`-CodeCoverage` for PowerShell.

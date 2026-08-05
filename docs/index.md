# Getting Started

Documentation is currently being improved, but here is the short version to use this template:

1. Ensure you have [mise](https://mise.jdx.dev/getting-started.html) installed on your workstation (Linux/macOS/Windows are all supported).
1. Clone this repository and open it in your terminal
1. Run the following to install needed dependencies to use the template:

```bash
mise trust
mise install
```

1. Run the following to create the template, making sure set the path at the end as appropriate

```bash
mise x "--" copier copy --trust https://github.com/natescherer/postmodern-repo-copiertemplate ~/local-repo-path-here
```

## Stuff from old README

### Core

#### Support for Multiple CI/CD Platforms

- GitHub **Recommended**
  - Creating repos under both users and orgs is supported
  - See [GitHub Org Limitations](docs/github_org_limitations.md) for details about template features excluded for Orgs
- Azure DevOps
  - See [Azure DevOps Limitations](docs/azure_devops_limitations.md) for details about features missing for AzDO

#### Support for Public (Open-Source) and Private (Closed-Source) Repositories

This template fully supports both public/open-source and private/closed-source repositories. See [Public vs Private Repos](docs/public_vs_private_repos.md) for the difference.

#### Support for Existing Projects

Postmodern templates are designed to allow either the creation of new templates from scratch or adoption for existing projects with existing code repos.

#### Support for Template Updates

Keeping projects in sync with their parent template is a core feature of [Copier](https://github.com/copier-org/copier), and this template will deploy a GitHub Actions Workflow/Azure DevOps Pipeline that will automate the update process.

#### Support for Child/Recursive Templates

It is highly encouraged for you to take this template and make your own child template that meets your needs. Your child template can (optionally) receive updates from this template.

### Repository Management

- Creation of new repos and branches
- Setting of repo settings & branch protection rules
- Creation of useful non-default issue labels: `awaiting pr` and `blocked`
- Contributor management and crediting via [All Contributors](https://allcontributors.org/)
- Dependency updates via [Renovate](https://github.com/marketplace/renovate/)
- Scheduled checks for updates from parent template

### Documentation

Rich Markdown documentation is pre-configured using [Zensical](https://zensical.org/), the successor to the extremely popular (but end of life) [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

- Documentation is automatically built for each version of your project that is released, with old versions maintained
- Multiple choices of documentation target:
  - GitHub Pages
  - A `docs_site` folder in your repo containing rendered HTML suitable for offline use

### Code Management and Formatting

- Automatic, repository-local dev tool installation via [mise](https://github.com/jdx/mise)
- Automatic code linting and formatting via [prek](https://prek.j178.dev/):
  - Commit message linting via [committed](https://github.com/crate-ci/committed)
  - GitHub Actions linting via [actionlint](https://github.com/rhysd/actionlint)
  - Markdown linting via [rumdl](https://github.com/rvben/rumdl)
  - Python linting and formatting via [Ruff](https://github.com/astral-sh/ruff)
  - Spell checking via [typos](https://github.com/crate-ci/typos)
  - TOML linting and formatting via [Tombi](https://github.com/tombi-toml/tombi)
  - YAML formatting via [yamlfmt](https://github.com/google/yamlfmt)

### CI/CD

- Version number calculation, Changelog updating, releasing, and tagging via [Release Please](https://github.com/googleapis/release-please)
- Simple/example release workflow via GitHub Actions

### Support Files

- `.gitignore`, set to ignore macOS `.DS_Store` files and Windows `Thumbs.db` files
- `CODE_OF_CONDUCT.md`, derived from [The Contributor Covenant](https://www.contributor-covenant.org/)
- `CONTRIBUTING.md`, designed help novices to make their first contribution
- `LICENSE`, a copy of the [MIT License](https://choosealicense.com/licenses/mit/)
- `README.md`, designed for general products

### Editor Configuration

Optimal settings and plugin recommendations are included for [Visual Studio Code](http://code.visualstudio.com/).

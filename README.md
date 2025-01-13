# Postmodern Repo Copier Template

[![All Contributors](https://img.shields.io/github/all-contributors/natescherer/postmodern-repo-copiertemplate?color=ee8449&style=flat-square)](#contributors)

| :exclamation: Notice: This project is currently in a Pre-Alpha state and is not ready for public use. |
| ----------------------------------------------------------------------------------------------------- |

A [Copier](https://github.com/copier-org/copier) template for creating a basic repository with full, all-the-bells-and-whistles CI/CD. (And for creating other templates!)

This template is heavily inspired by the [Hypermodern Python Cookiecutter](https://cookiecutter-hypermodern-python.readthedocs.io).

Why Postmodern? Besides being a cheeky homage to this template's inspiration, I think that Postmodern philosophy's idea of the relativity of truth applies very well to software. There's no objectively best way to do CI/CD, this is just one way that works, and it might work for you too!

## Included Features

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

### Code Management and Formatting

- Automatic code linting and formatting via [Trunk](https://trunk.io):
  - GitHub Actions linting via [actionlint](https://github.com/rhysd/actionlint)
  - Markdown link health checking via [markdown-link-check](https://github.com/tcort/markdown-link-check)
  - Markdown formatting via [Prettier](https://prettier.io/)
  - Markdown linting via [markdownlint](https://github.com/DavidAnson/markdownlint)
  - Python linting and formatting via [Ruff](https://github.com/astral-sh/ruff)
  - Spell checking via [cSpell](https://cspell.org/)
<<<<<<< before updating
=======
  - TOML linting via [taplo](https://github.com/tamasfe/taplo)
>>>>>>> after updating
  - YAML formatting via [Prettier](https://prettier.io/)
  - YAML linting via [yamllint](https://github.com/adrienverge/yamllint)

### CI/CD

- Version number calculation, Changelog updating, releasing, and tagging via [Release Please](https://github.com/googleapis/release-please)
- Simple/example release workflow via GitHub Actions

### Support Files

- `.gitignore`, set to ignore macOS `.DS_Store` files and Windows `Thumbs.db` files
- `CODE_OF_CONDUCT.md`, derived from [The Contributor Covenant](https://www.contributor-covenant.org/)
- `CONTRIBUTING.md`, designed help novices to make their first contribution
- `LICENSE`, a copy of the [MIT License](https://choosealicense.com/licenses/mit/)
- `README.md`, designed for general products

## Getting started

Intersted in using this template (or just learning more about it)? Check out [Getting Started](docs/getting_started.md).

## Questions/Comments

If you have questions, comments, etc, please enter a GitHub Issue with the "question" tag.

## Contributing/Bug Reporting

Contributions and bug reports are gladly accepted! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Contributors

<!-- spell-checker:disable -->
<!-- markdown-link-check-disable -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/natescherer"><img src="https://avatars.githubusercontent.com/u/376408?v=4?s=100" width="100px;" alt="Nate Scherer"/><br /><sub><b>Nate Scherer</b></sub></a><br /><a href="#code-natescherer" title="Code">💻</a> <a href="#maintenance-natescherer" title="Maintenance">🚧</a> <a href="#doc-natescherer" title="Documentation">📖</a> <a href="#infra-natescherer" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- markdown-link-check-enable -->
<!-- spell-checker:enable -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!

## License

This project is licensed under The MIT License - see [LICENSE](LICENSE) for details.

## Repository Template

This repository is based on the template of itself. Neat, huh?

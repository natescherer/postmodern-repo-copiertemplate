# cookiecutter-postmodern-repo

A [Cookiecutter][cookiecutter] template for creating a basic GitHub repository. (And for creating other cookiecutters!)

<!-- Add additional data after this line -->

This template is heavily inspired by the [Hypermodern Python Cookiecutter](https://github.com/cjolowicz/cookiecutter-hypermodern-python).

Why Postmodern? Besides being a cheeky homage to this template's inspiration, I think that Postmodern philosophy's idea of the relativity of truth applies very well to software. There's no objectively best way to do CI/CD, this is just one way that works, and it might work for you too!

## Included Features

### Repository Management

- Creation of GitHub repo and `feature/initial` branch via git and [GitHub CLI][github-cli]
- Setting of default repo settings & main branch protection ruleset via [GitHub CLI][github-cli]
- Creation of useful non-default issue/pr labels via [GitHub CLI][github-cli] script: `awaiting pr` and `blocked`
- Contributor management and crediting via [All Contributors][all-contributors]
- GitHub Actions dependency updating via [Dependabot][dependabot]
- Synchronization with updates to this template via [cruft][cruft]

### CI/CD

- [SemVer][semver] version number calculation via [GitVersion][gitversion]
- Changelog creation and upkeep in [Keep a Changelog][keep-a-changelog] format
- Simple/example release workflow via GitHub Actions

### Support Files

- `.gitignore`, set to ignore macOS `.DS_Store` files
- `CODE_OF_CONDUCT.md`, derived from [The Contributor Covenant][contributor-covenant]
- `CONTRIBUTING.md`, designed help novices to make their first contribution
- `LICENSE`, a copy of the [MIT License][mit-license]
- `README.md`, designed for general products

## Prerequisites

### Your Machine

1. Ensure you have a [supported version][eol-python] of Python installed.
    - You can check if Python is installed by running `python --version` in your shell. If you get an error, it is not installed.
    - Need to install Python? See [Installing Python](docs/installing_python.md) for help.
1. Ensure you have the [pipx][pipx] Python package manger installed.
    - You can check by running `pipx --version` in your shell. If you get an error, it is not installed.
    - Need to install pipx? See [Installing pipx](docs/installing_pipx.md) for help.
1. Install `Cookiecutter` & `cruft`

    ``` bash
    pipx install cookiecutter
    pipx install cruft
    ```

    - If you plan on using Cookiecutters often, consider setting up a user config file to specify default values so you don't have to type them in for every template. If you want to do this, see [Cookiecutter Defaults](docs/cookiecutter_defaults.md).

1. Ensure you have the [GitHub CLI][github-cli] (aka gh) installed
    - You can check by running `gh --version` in your shell. If you get an error, it is not installed.
    - Need to install gh? See [their instructions][github-cli-instructions] for help.

### GitHub

1. Install the [AllContributors GitHub App][all-contributors-app] for your user or organization.
    - You can either give it access to all your repositories, which means you only need to do this step once, or you can select repositories individually, in which case you will need to do this for each new repo you create.
1. Ensure `Private vulnerability reporting > Automatically enable for new public repositories` is checked [here](https://github.com/settings/security_analysis).
    - This only needs done once for all repositories

## Using this Cookiecutter

1. Open a terminal to the parent directory where you want the repo subdirectory to be created
1. Run the following to initialize the template (and the linked GitHub repo):

    ``` bash
    cruft create https://github.com/natescherer/cookiecutter-base
    ```

## Repository Template

This repository is based on the template of itself via [cruft][cruft]. Neat, huh?

[all-contributors]: https://allcontributors.org/
[all-contributors-app]: https://github.com/apps/allcontributors/installations/new
[cookiecutter]: https://www.cookiecutter.io/
[contributor-covenant]: https://www.contributor-covenant.org/
[cruft]: https://cruft.github.io/cruft/
[dependabot]: https://docs.github.com/en/code-security/getting-started/dependabot-quickstart-guide
[eol-python]: https://endoflife.date/python
[github-cli]: https://cli.github.com/
[github-cli-instructions]: https://github.com/cli/cli#installation
[gitversion]: https://gitversion.net/
[keep-a-changelog]: https://keepachangelog.com/en/1.1.0/
[mit-license]: https://choosealicense.com/licenses/mit/
[pipx]: https://github.com/pypa/pipx
[semver]: https://semver.org/

# {{cookiecutter.repo_name}}

[![All Contributors][all-contributors-badge]](#contributors)

{{cookiecutter.short_description}}

## Included Features

### Repository Management

- Setting of default repo settings & main branch protection ruleset via [GitHub CLI][github-cli] script
- Creation of useful non-default issue/pr labels via [GitHub CLI][github-cli] script: `awaiting pr` and `blocked`
- Contributor management and crediting via [All Contributors][all-contributors]
- GitHub Actions dependency updating via [Dependabot][dependabot]
- Synchronization with template updates via [cruft][cruft]

### CI/CD

- [SemVer][semver] version number calculation via [GitVersion][gitversion]
- Changelog creation and upkeep in [Keep a Changelog][keep-a-changelog] format
- Release workflow via GitHub Actions

### Support Files

- `.gitattributes`, set to force LF line endings on all platforms
- `.gitignore`, set to general defaults
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

## Using this Cookiecutter

### Repo Creation and Template Initialization

1. Create a new repo in GitHub, choosing to create a README to initialize it.
1. Clone that repo to your local machine, but don't cd into it yet.
1. Run the following to install the template via cruft:

    ``` bash
    cruft create https://github.com/natescherer/cookiecutter-basic -f
    ```

### Configuration Tasks

1. In order to configure GitHub repository settings, a script that leverages the GitHub CLI is included and should be run after the template is initialized. Syntax is slightly different based on your platform:
    - macOS/Linux

        ``` bash
        cd .github
        chmod +x set-repo-settings.sh
        ./set-repo-settings.sh
        ```

    - Windows (in PowerShell)

        ``` PowerShell
        & {Invoke-Expression (Get-Content -Raw .github\set-repo-settings.sh)}
        ```

## Repository Template

This repository is based on the template of itself via [cruft][cruft]. Neat, huh?

[all-contributors]: https://allcontributors.org/
[all-contributors-app]: https://github.com/apps/allcontributors/installations/new
[all-contributors-badge]: https://img.shields.io/github/all-contributors/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}}?color=ee8449&style=flat-square
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

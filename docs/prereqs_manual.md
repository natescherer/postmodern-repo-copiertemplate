# Manual Prerequisite Installation

1. Ensure you have a [supported version][eol-python] of Python installed.
   - You can check if Python is installed by running `python --version` in your shell. If you get an error, it is not installed.
   - Need to install Python? See [Installing Python](docs/installing_python.md) for help.
1. Ensure you have the [pipx][pipx] Python package manger installed.
   - You can check by running `pipx --version` in your shell. If you get an error, it is not installed.
   - Need to install pipx? See [Installing pipx](docs/installing_pipx.md) for help.
1. Install `copier` and the requirements for this template

   ```bash
   pipx install copier
   pipx inject copier -r PATH-TO-REPO-HERE/.devcontainer/requirements.txt
   ```

1. Ensure you have the [GitHub CLI][github-cli] (aka gh) installed
   - You can check by running `gh --version` in your shell. If you get an error, it is not installed.
   - Need to install gh? See [their instructions][github-cli-instructions] for help.

[eol-python]: https://endoflife.date/python
[github-cli]: https://cli.github.com/
[github-cli-instructions]: https://github.com/cli/cli#installation
[pipx]: https://github.com/pypa/pipx
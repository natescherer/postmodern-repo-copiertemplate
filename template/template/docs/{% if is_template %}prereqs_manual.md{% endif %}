# Manual Prerequisite Installation

1. Ensure sure you have Git Credential Manager installed via [their instructions][gcm-install].
1. Ensure you have a [supported version][eol-python] of Python installed.
   - You can check if Python is installed by running `python --version` in your shell. If you get an error, it is not installed.
   - Need to install Python? See [Installing Python](docs/installing_python.md) for help.
1. Ensure you have the [pipx][pipx] Python package manger installed.
   - You can check by running `pipx --version` in your shell. If you get an error, it is not installed.
   - Need to install pipx? See [Installing pipx](docs/installing_pipx.md) for help.
1. Install `copier` and the requirements for this template

   1. Download [../.devcontainer/library/requirements.txt](../.devcontainer/library/requirements.txt)

   ```bash
   pipx install copier
   pipx inject copier -r PATH-TO-DOWNLOAD-FOLDER-HERE/requirements.txt
   ```

1. Ensure you have the [GitHub CLI][github-cli] (aka gh) installed
   - You can check by running `gh --version` in your shell. If you get an error, it is not installed.
   - Need to install gh? See [their instructions][github-cli-instructions] for help.

[eol-python]: https://endoflife.date/python
[gcm-install]: https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md
[github-cli]: https://cli.github.com/
[github-cli-instructions]: https://github.com/cli/cli#installation
[pipx]: https://github.com/pypa/pipx
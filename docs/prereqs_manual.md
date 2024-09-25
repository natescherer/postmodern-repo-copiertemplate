# Manual Prerequisite Installation

1. Ensure sure you have Git Credential Manager installed via [their instructions][gcm-install].
1. Ensure you have a [supported version][eol-python] of Python installed.
   - You can check if Python is installed by running `python --version` in your shell. If you get an error, it is not installed.
   - Need to install Python? See [Installing Python](installing_python.md) for help.
1. Ensure you have the [pipx][pipx] Python package manger installed.
   - You can check by running `pipx --version` in your shell. If you get an error, it is not installed.
   - Need to install pipx? See [Installing pipx](installing_pipx.md) for help.
1. Install `copier` and the requirements for this template

   1. Download [../.devcontainer/library/requirements.txt](../.devcontainer/library/requirements.txt)

   ```bash
   pipx install copier
   pipx inject copier -r PATH-TO-DOWNLOAD-FOLDER-HERE/requirements.txt
   ```

[eol-python]: https://endoflife.date/python
[gcm-install]: https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md
[pipx]: https://github.com/pypa/pipx

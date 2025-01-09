# Manual Prerequisite Installation

1. In order to make sure you can authenticate Git with GitHub and/or Azure DevOps, ensure you have Git Credential Manager installed on your machine via [their instructions](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md).
1. Ensure you have a [supported version](https://endoflife.date/python) of Python installed.
   - You can check if Python is installed by running `python --version` in your shell. If you get an error, it is not installed.
   - Need to install Python? See [Installing Python](installing_python.md) for help.
1. Ensure you have the [pipx](https://github.com/pypa/pipx) Python package manger installed.
   - You can check by running `pipx --version` in your shell. If you get an error, it is not installed.
   - Need to install pipx? See [Installing pipx](installing_pipx.md) for help.
1. Install `copier` and the requirements for this template

   1. Download [https://github.com/natescherer/postmodern-tools-container/blob/main/src/requirements.txt](https://github.com/natescherer/postmodern-tools-container/blob/main/src/requirements.txt)

   ```bash
   pipx install copier
   pipx inject copier -r requirements.txt
   ```

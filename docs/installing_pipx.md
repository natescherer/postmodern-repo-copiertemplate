# Installing pipx

`pipx` is a package manager for Python that is designed to install command-line applications like `copier`.

## Linux

Installation on Linux is done via `pip`.

1. Run the following in your shell of choice:

    ``` bash
    pip install --user pipx
    pipx ensurepath
    ```

1. Close and reopen your shell

## macOS

Installation on macOS is down via `Homebrew`.

1. Run the following in Terminal:

    ``` bash
    brew update
    brew install pipx
    pipx ensurepath
    ```

1. Close and reopen Terminal

## Windows

Installation on Windows is done via `pip`.

1. Run the following in PowerShell:

    ``` PowerShell
    pip install --user pipx
    ```

1. Confirm `pipx` is properly installed by running `pipx --version`
    1. If a version number was returned:
        1. Run the following in PowerShell:

            ``` PowerShell
            pipx ensurepath
            ```

        1. Close and reopen PowerShell

    1. If you got an error:
        1. Run the following in PowerShell:

            ``` PowerShell
            cd $(python -c "import os,sysconfig;print(sysconfig.get_path('scripts',f'{os.name}_user'))")
            .\pipx.exe ensurepath
            ```

        1. Close and reopen PowerShell
        1. Run `pipx --version` again and a version number should be returned

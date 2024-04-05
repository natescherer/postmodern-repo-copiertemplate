# Prerequisites via Devcontainer

In order to make sure you can authenticate Git with GitHub and/or Azure DevOps, you will need to make sure you have Git Credential Manager installed on your host machine via [their instructions][gcm-install].

There are many different tools that use Devcontainers, but, if you are starting out, I recommend you use Visual Studio Code's integration with them.

First off, follow [their tutorial][vscode-devcontainer-tutorial] to get set up. Running the sample container they recommend is optional.

Once that is done, clone this repository into VSCode, then go to `View > Command Palette` and type in `rebuild and reopen`. The item `Dev Containers: Rebuild and Reopen in Container` should be selected. Hit Enter, and the devcontainer will be built, and VSCode will reopen with a terminal running inside the container with all needed tools.

Note that home folder of the computer where you are running Docker will be mounted at `/host-home`.

[gcm-install]: https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md
[vscode-devcontainer-tutorial]: https://code.visualstudio.com/docs/devcontainers/tutorial
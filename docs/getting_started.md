# Getting Started

## Prerequisites

### Your Machine

There are several tools needed on your local machine to use this template, and three main options to install them:

[Prerequisites via Docker Container](prereqs/docker/prereqs_docker.md)

- Recommended for most applications

[Prerequisites via Devcontainer](prereqs/devcontainer/prereqs_devcontainer.md)

- Recommended if you are using a template from a Git repo that requires authentication, which the Docker method doesn't support

[Prerequisites via Manual Installation](prereqs/manual/prereqs_manual.md)

- Works, but not recommended

### GitHub

### One-Time Actions Per GitHub User/Organization

1. Install the [AllContributors GitHub App](https://github.com/apps/allcontributors/installations/new) for your user or organization.
    - This app provides automatic README crediting when other people contribute to your project
    - If you know you are only going to be making Private projects, you can skip installing this app
    - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
1. Install the [Renovate GitHub App](https://github.com/apps/renovate) for your user or organization.
    - This app provides automatic dependency updates for your project
    - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
1. Ensure `Private vulnerability reporting > Automatically enable for new public repositories` is checked [in the repo settings](https://github.com/settings/security_analysis).

## Using this template

### Docker

1. In your terminal, create a folder with the name of the repo you wish to create, and cd into it.
1. Run the appropriate command for your OS:

   *macOS/Linux*

   ```bash
   docker run -v .:/mnt/${PWD##*/} -w /mnt/${PWD##*/} -v ~/.gitconfig:/root/.gitconfig:ro -it --pull always --rm ghcr.io/natescherer/postmodern-tools-container:latest copier copy --trust gh:natescherer/postmodern-repo-copiertemplate .
   ```

   *Windows*

   ```PowerShell
   coming soon
   ```

### Devcontainer

1. Ensure you are running inside the Devcontainer
1. Inside of `/mnt/host-home` (which is the home directory of your host machine), create a folder with the name of the repo you wish to create, and cd into it
1. Run the following to initialize the template:

   ```bash
   copier copy --trust gh:natescherer/postmodern-repo-copiertemplate .
   ```

### Manual

1. Create a folder with the name of the repo you wish to create, and cd into it
1. Run the following to initialize the template:

   ```bash
   copier copy --trust gh:natescherer/postmodern-repo-copiertemplate .
   ```

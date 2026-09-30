# Prerequisites

## Platform-Level Prerequisites

=== "GitHub"

    ### One-Time Actions Per GitHub User/Organization

    1. Install the [Renovate GitHub App](https://github.com/apps/renovate) for your user or organization.
        - This app provides automatic dependency updates for your project
        - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
    1. **[Optional for Private Repos]** Install the [Settings GitHub App](https://github.com/apps/settings) for your user or organization.
        - This app syncs repo settings (labels, merge options, branch protection) from `.github/settings.yml`, allowing you to manage (most) GitHub repo settings in code.
        - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
        - If you don't want to use the settings app, manual settings workflow is documented and will be provided during the course of template setup.
    1. **[Optional if you don't want Code Coverage]** Install the [Codecov GitHub App](https://github.com/apps/codecov) for your user or organization.
        - This app powers Codecov's PR comments/checks and connects your repo to codecov.io for uploads
        - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
    1. **[Skip for Private Repos]** Install the [AllContributors GitHub App](https://github.com/apps/allcontributors/installations/new) for your user or organization.
        - This app provides automatic README crediting when other people contribute to your project
        - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.

=== "Azure DevOps"

    ### One-Time Actions per Azure DevOps Project

    In order to support the proper parsing of Conventional Commits, the following settings must be set:

    - `Project settings`
        - `Repositories`
            - `Settings` tab
                - `All Repositories Settings` section
                    - Ensure `Include PR ID in the completion commit message title by default` is set to `Off`

    In order to support Knope/Zensical workflows, the following permissions must be granted:

    - `Project settings`
        - `Repositories`
            - `Security` tab
                - `PROJECTNAME Build Service (PROJECTNAME)`
                    - Set these to `Allow`:
                        - `Contribute`
                        - `Contribute to pull requests`
                        - `Create branch`

## Workstation Prerequisites

### Universal

1. Install [mise](https://mise.jdx.dev/getting-started.html), the dependency manager for this project.
1. Ensure you have followed the steps to [activate mise in your shell](https://mise.jdx.dev/getting-started.html#activate-mise).
1. **[Optional]** It is recommended to install [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager) to handle your git authentication to GitHub/Azure DevOps.
    - This comes bundled with Git for Windows, but is a separate install for macOS and Linux. See the link above for installation options.
    - You're welcome to use SSH or another way of authenticating Git, but GCM gives you a nice web-based login experience.

### Platform-Specific

=== "GitHub"

    1. Install the [GitHub CLI](https://cli.github.com)
        - The template uses the GitHub CLI to create your repo and configure the settings that the Settings App is unable to.
    1. Run the below to authenticate:
        ```
        gh auth login
        ```

=== "Azure DevOps"

    1. Install the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
    1. Run the below to install the Azure DevOps extension and authenticate:
        ```
        az extension add --name azure-devops
        az login
        ```

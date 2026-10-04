# Prerequisites

## Platform-Level Prerequisites

=== "GitHub"

    ### One-Time Actions Per GitHub User/Organization

    #### GitHub App Installations

    Each of these apps should be installed for the user or organization where you plan to create your repo. It is recommended that you give each app access to all your repositories, which means you only need to do this step once rather than for each new repo.

    1. [Renovate GitHub App](https://github.com/apps/renovate)
        - This app provides automatic dependency updates for your project
    1. **[Optional]** [Settings GitHub App](https://github.com/apps/settings)
        - This app syncs repo settings (labels, merge options, branch protection, etc) from `.github/settings.yml`, allowing you to manage (most) GitHub repo settings in code.
        - If you don't want to use the settings app, manual settings workflow is documented and will be provided during the course of template setup.
    1. **[Optional]** [Codecov GitHub App](https://github.com/apps/codecov)
        - This app powers Codecov's PR comments/checks and connects your repo to codecov.io for uploads
        - If you don't want code coverage, skip installing and say no to code coverage when setting up the template
    1. **[Skip for Private Repos]** [AllContributors GitHub App](https://github.com/apps/allcontributors/installations/new)
        - This app provides automatic README crediting when other people contribute to your project

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

### Platform-Specific

=== "GitHub"

    1. Install the [GitHub CLI](https://cli.github.com)
        - The template uses the GitHub CLI to create your repo and configure the settings that the Settings App is unable to.
    1. Run the below to authenticate the GitHub CLI:
        ```
        gh auth login
        ```
    1. Set up Git authentication for HTTPS. Either option works:
        - Run `gh auth setup-git` to let Git reuse the GitHub CLI's credentials.
        - Install [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager), which also handles Azure DevOps if you use both. It comes bundled with Git for Windows; on macOS and Linux it's a separate install (see the link above).

=== "Azure DevOps"

    1. Install the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
    1. Run the below to install the Azure DevOps extension and authenticate:
        ```
        az extension add --name azure-devops
        az login
        ```
    1. Install [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager) to authenticate git over HTTPS
        - Git Credential Manager comes bundled with Git for Windows; on macOS and Linux it's a separate install (see the link above).

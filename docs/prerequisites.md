# Prerequisites

## GitHub

### One-Time Actions Per GitHub User/Organization

1. Install the [AllContributors GitHub App](https://github.com/apps/allcontributors/installations/new) for your user or organization.
    - This app provides automatic README crediting when other people contribute to your project
    - If you know you are only going to be making Private projects, you can skip installing this app
    - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
1. Install the [Renovate GitHub App](https://github.com/apps/renovate) for your user or organization.
    - This app provides automatic dependency updates for your project
    - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
1. Ensure `Private vulnerability reporting > Automatically enable for new public repositories` is checked [in the repo settings](https://github.com/settings/security_analysis).

## Personal Access Tokens

Unless you choose `None` for the `repo_setup_actions` question, Copier will prompt you for a
Personal Access Token part-way through the run. See [Token Permissions](token_permissions.md) for
the minimum scopes needed and why.

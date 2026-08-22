# Prerequisites

## GitHub

### One-Time Actions Per GitHub User/Organization

1. Install the [GitHub CLI](https://cli.github.com) (`gh`) and run `gh auth login` (default
   scopes are enough). Unless you choose `None` for the `repo_setup_actions` question, this is
   used instead of a Personal Access Token to create/configure your repo. The `repo_setup_actions`
   question's validator checks that `gh` is installed and authenticated before letting you
   proceed.
1. Make sure [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager) is
   installed (bundled with Git for Windows if you enabled it during install; a separate install on
   macOS/Linux). `gh auth login`'s default scopes don't cover pushing `.github/workflows/` files --
   see [Token Permissions](token_permissions.md#gh-auth-login-scopes) for why -- so GCM handles the
   initial push with its own (separate) interactive GitHub sign-in the first time.
1. Install the [AllContributors GitHub App](https://github.com/apps/allcontributors/installations/new) for your user or organization.
    - This app provides automatic README crediting when other people contribute to your project
    - If you know you are only going to be making Private projects, you can skip installing this app
    - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
1. Install the [Renovate GitHub App](https://github.com/apps/renovate) for your user or organization.
    - This app provides automatic dependency updates for your project
    - It is recommended that you give it access to all your repositories, which means you only need to do this step once rather than for each new repo.
1. Install the [Settings GitHub App](https://github.com/apps/settings) for your user or organization.
    - This app syncs repo settings (labels, merge options, branch protection) from the committed `.github/settings.yml`, which is always generated for GitHub projects
    - It must have access to a repo *before* that repo is created for its settings to apply, so grant it access to all your repositories up front, same as the apps above
    - Skipping this is fine -- see [Manual Repo Settings](manual_repo_settings.md) for how to apply the same configuration by hand instead
1. Ensure `Private vulnerability reporting > Automatically enable for new public repositories` is checked [in the repo settings](https://github.com/settings/security_analysis).

## Personal Access Tokens

GitHub no longer needs one for repo setup -- see the `gh auth login` step above. See
[Token Permissions](token_permissions.md) for the separate, ongoing **Repo Maintenance PAT** used
by this project's own GitHub Actions workflows.

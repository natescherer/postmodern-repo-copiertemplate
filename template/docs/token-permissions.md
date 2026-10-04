# Token Permissions

This doc details the credentials needed to use this template, along with reasons why. No
workflow or pipeline needs a Personal Access Token: CI runs under each platform's own built-in
identity (`GITHUB_TOKEN` / `$(System.AccessToken)`), and repo setup uses your own CLI session.

## CLI Session

=== "GitHub"

    Repo setup and the integration test scripts run as whoever is logged in via `gh auth login`.
    That session needs the `repo` and `workflow` scopes, which `gh auth login` grants by default.
    Check with `gh auth status`.

=== "Azure DevOps"

    Repo setup and the integration test scripts run as whoever is logged in via `az login`. That
    account needs access to the target Azure DevOps project, plus permission to create repos,
    pipelines, and branch policies in it.

## Secrets

Once you've created each secret below, run `mise run provision-secrets`: each value is entered
via that platform's own CLI prompt (`gh secret set` / `az pipelines variable create`), masked as
you type and never passed as a command-line argument. It's opt-in and safe to re-run any time,
e.g. to rotate a value.

### APPRISE_URL

Both platforms' Copier update-check job needs a secret/variable called **APPRISE_URL**. Azure
DevOps additionally needs it for the Renovate pipeline and the release/docs pipelines, since
those merge without a human in the loop and notify on both successful auto-merge and on PR
validation failing to pass. It's an [Apprise](https://github.com/caronc/apprise) notification URL
pointing at wherever you want these notifications sent (email, Slack, Discord, ntfy, Pushover,
and 80+ others; see Apprise's own docs for the URL format for your service of choice).

### CODECOV_TOKEN

(GitHub with `code_coverage` only.) The PR validation workflow uploads `coverage.xml` to
[Codecov](https://codecov.io/) with this token. Copy it from the repo's settings page on
codecov.io after installing the Codecov GitHub App (see [Prerequisites](prerequisites.md)).

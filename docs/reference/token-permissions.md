# Secrets and Tokens

This page lists the credentials this project needs and why. No workflow or pipeline needs a
Personal Access Token: CI runs as each platform's built-in identity (`GITHUB_TOKEN` /
`$(System.AccessToken)`), and repo setup uses your own CLI session.

## CLI Session

=== "GitHub"

    Repo setup (and, in Template projects, the integration test scripts) runs as whoever is
    logged in via `gh auth login`. That session needs the `repo` and `workflow` scopes, which
    `gh auth login` grants by default. Check with `gh auth status`.

=== "Azure DevOps"

    Repo setup (and, in Template projects, the integration test scripts) runs as whoever is
    logged in via `az login`. That account needs access to the target Azure DevOps project, plus
    permission to create repos, pipelines, and branch policies in it.

## Secrets

Once you have each value below, run `mise run provision-secrets`. It prompts for each one
through the platform's CLI (`gh secret set` / `az pipelines variable create`), masked as you
type and never passed as a command-line argument. Rerun it any time, for example to rotate a
value.

### APPRISE_URL

The Copier update check on both platforms needs a secret or variable named **APPRISE_URL**.
On Azure DevOps, that check is a job in the Monthly Maintenance pipeline, whose Renovate job
also notifies when it opens PRs; the docs pipeline needs it too, since it merges its own PR and
notifies when that succeeds or PR validation fails.
It's an [Apprise](https://github.com/caronc/apprise) URL for wherever the notifications should go:
email, Slack, Discord, ntfy, Pushover, or one of 80+ other services. Apprise's docs give each
service's URL format.

### GITHUB_COM_TOKEN

(Azure DevOps only.) Renovate looks up most dependency versions on github.com, and skips every
dependency hosted there without a token, so Monthly Maintenance's Renovate job fails without
one. Every pipeline uses it when it's set: mise downloads tools from github.com, and the Repo
Health Check job checks github.com links, and Microsoft-hosted agents share github.com's
unauthenticated rate limit by IP, so a run without a token can fail on a 403. Create a
[personal access token](https://github.com/settings/tokens) with **no scopes** on any GitHub
account, then add it to each pipeline (`mise run provision-secrets` does this, asking for the
value once per pipeline):

```bash
az pipelines variable create --name GITHUB_COM_TOKEN --pipeline-name "[<repo>] <pipeline>" --secret true
```

Run that for each of the four pipelines: Maint (Auto) - Monthly Maintenance, Docs (Auto) -
Zensical Build & Commit, Release (Auto) - Prepare & Publish Release, and Test (Auto) - PR
Validation.

### CODECOV_TOKEN

(GitHub with `code_coverage` only.) The PR validation workflow uploads `coverage.xml` to
[Codecov](https://codecov.io/) with this token. Copy it from the repo's settings page on
codecov.io after installing the Codecov GitHub App (see [Prerequisites](../getting-started/prerequisites.md)).

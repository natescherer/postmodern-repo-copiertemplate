# Token Permissions

This doc details the minimum scopes/permissions needed to use this template, along with reasons
why. Neither platform requires a prompted Personal Access Token for repo setup anymore; both use
the platform's own CLI session instead (`gh auth login` / `az login`).

Once you've created each secret/token below, run `mise run provision-secrets`: each value is
entered via that platform's own CLI prompt (`gh secret set` / `az pipelines variable create`),
masked as you type and never passed as a command-line argument. It's opt-in and safe to re-run
any time, e.g. to rotate a token.

## Notifications

Both platforms' Copier update-check job needs a secret/variable called **APPRISE_URL**. Azure
DevOps additionally needs it for the Renovate pipeline and the release/docs pipelines, since
those merge without a human in the loop and notify on both successful auto-merge and on PR
validation failing to pass. Unlike the tokens below, it isn't a scope to grant; it's an
[Apprise](https://github.com/caronc/apprise) notification URL pointing at wherever you want these
notifications sent (email, Slack, Discord, ntfy, Pushover, and 80+ others; see Apprise's own
docs for the URL format for your service of choice).

=== "GitHub"

    ### Repo Maintenance PAT (Classic Token)

    Due to GitHub security policies, a PAT must be provided to several workflows in order for them to execute properly.

    The primary blocker is [detailed here](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow#triggering-a-workflow-from-a-workflow), namely that pull requests opened under GitHub Actions's default auth will never trigger another workflow. This breaks Knope's PR-based release flow, as Knope PRs need to trigger the `release-auto-publishrelease.yml` workflow which does the actual release work.

    No other flows are blocked per se, but since the token must exist for `release-auto-publishrelease.yml`, we also use it to reduce friction in other workflows, such as bypassing the human approval that would be needed for tests to run on workflow-created PRs.

    **Repository Access**: All repositories

    | **Scope** | **Reason**                        |
    | --------- | ---------------------------------- |
    | `repo`    | Needed for Knope and Zensical workflows   |

    !!! note
        Fine-grained tokens are specifically **not** used, since they cannot open pull requests.
        This can be changed once [this issue](https://github.com/github/roadmap/issues/600) is
        implemented by GitHub.

=== "Azure DevOps"

    Nothing currently.

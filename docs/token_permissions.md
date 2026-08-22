# Token Permissions

This doc details the minimum scopes/permissions needed to use this template, along with reasons
why. Neither platform requires a prompted Personal Access Token for repo setup anymore -- both use
the platform's own CLI session instead (`gh auth login` / `az login`).

## GitHub

### `gh auth login` Scopes

Repo creation and configuration (labels, merge options, branch protection, Actions permissions,
Pages) uses the [GitHub CLI](https://cli.github.com)'s own authenticated session rather than a
prompted Personal Access Token -- see [Prerequisites](prerequisites.md). Default scopes (`repo`
among them) are enough; no need for `gh auth login --scopes ...`. The initial `git push` is a
separate matter -- `gh auth login`'s scopes don't cover pushing `.github/workflows/` files
regardless, so that step uses Git Credential Manager's own login instead, not `gh`'s.

### Repo Maintenance PAT (Classic Token)

For best security, create this token via [this link](https://github.com/settings/personal-access-tokens/new)
and save it as a GitHub Actions secret on the repository called **REPO_MAINTENANCE_PAT**. This is
separate from `gh auth login` above -- it's used on an ongoing basis by this project's own GitHub
Actions workflows (Copier update checks, Release Please), not just at setup time.

**Repository Access**: All repositories

| **Scope**                     | **Reason**                                 |
| ----------------------------- | ------------------------------------------ |
| repo                          | Needed for Copier/Release Please workflows |

NOTE: Fine-grained tokens are specifically **not** used, as they cannot open pull requests. This can be changed once [this issue](https://github.com/github/roadmap/issues/600) is implemented by GitHub.

### Integration Test PAT (Classic Token)

Create this token the same way as the Repo Maintenance PAT above and save it as a GitHub Actions
secret called **INTEGRATION_TEST_PAT**. Used by `maint-integration_test.yml`, which creates a
real, throwaway repo on a schedule to verify repo setup actually works end to end, then deletes
it -- `delete_repo` is needed specifically for that cleanup step and isn't part of any other
token this project uses.

**Repository Access**: All repositories

| **Scope**   | **Reason**                                                  |
| ----------- | ------------------------------------------------------------ |
| repo        | Needed to create the test repo and read back its settings   |
| workflow    | Needed to push the test repo's initial commit (includes `.github/workflows/`) |
| delete_repo | Needed to delete the test repo during cleanup                |

The account this token belongs to also needs the [Settings GitHub App](https://github.com/apps/settings)
installed with access to **all** repositories, not just selected ones -- the workflow's
verification step checks that the app actually synced `.github/settings.yml` (labels, branch
ruleset) to the freshly-created test repo, and an app installed on "only select repositories"
never automatically gains access to a repo created after the fact.

### Integration Test PAT for Azure DevOps

`maint-integration_test.yml` also runs a second job that creates a throwaway repo with
`developer_platform=Azure DevOps` to verify that path end to end, regardless of which platform
this project itself uses. Create an Azure DevOps PAT covering **Code (Full)** and **Build (Read &
execute)** for the target org/project -- the same permissions a signed-in `az login` session would
need for repo/pipeline creation, just via a PAT since CI can't do an interactive login -- and save
it as a GitHub Actions secret called **AZURE_DEVOPS_EXT_PAT** -- this exact name is what the `azure-devops` `az` CLI
extension auto-detects for non-interactive auth, so it's reused as-is for both `az` calls and the
test repo's initial `git push`. There's no way to auto-detect which Azure DevOps org/project the
throwaway repo should be created in (unlike the AzDO-hosted pipeline below, which reads that from
its own pipeline variables), so also edit the `integration-test-azdo` job's `env:` block directly
in `maint-integration_test.yml`, replacing the `AZDO_INTEGRATION_TEST_ORG`/`AZDO_INTEGRATION_TEST_PROJECT`
placeholder values with your real org/project -- left as placeholders, the job fails fast with an
explanatory error instead of a confusing `az` CLI one.

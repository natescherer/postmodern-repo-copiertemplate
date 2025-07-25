# Token Permissions

This doc details the minimum scopes/permissions needed for GitHub/Azure DevOps tokens needed to use this template, along with reasons why.

## GitHub

For best security, you should create two GitHub Personal Access tokens via [this link](https://github.com/settings/personal-access-tokens/new), a **Repo Setup PAT** and a **Repo Maintenance PAT**, permissions of which are detailed below.

The **Repo Setup PAT** can be stored in your password vault of choice, as you will only need it when you are creating a new repo via this template.

The **Repo Maintenance PAT** should be saved as a GitHub Actions secret on the repository called **REPO_MAINTENANCE_PAT**. This can be done manually or via Infisical.

### Repo Setup PAT (Fine-grained token)

**Repository Access**: All Repositories

| **Permission**                 | **Reason**                                         |
| ------------------------------ | -------------------------------------------------- |
| Administration: Read and Write | Needed to create repo & set its settings           |
| Contents: Read and Write       | Needed to commit code                              |
| Issues: Read and Write         | Needed to create custom labels                     |
| Workflows: Read and Write      | Needed to allow template tasks to commit workflows |

### Repo Maintenance PAT (Classic token)

NOTE: The newer Fine-Grained Tokens can't make PRs inside GitHub Organizations, classic tokens will be recommended until this functionality is added. See [https://github.com/orgs/community/discussions/106661](https://github.com/orgs/community/discussions/106661)

| **Scope**                     | **Reason**                                 |
| ----------------------------- | ------------------------------------------ |
| repo                          | Needed for Release Please workflow        |

## Azure DevOps

| **Scope**             | **Reason**                               |
| --------------------- | ---------------------------------------- |
| Build: Read & Execute | Needed to allow creating Azure Pipelines |
| Code: Full            | Needed to create repo                    |

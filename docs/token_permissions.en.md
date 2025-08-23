# Token Permissions

This doc details the minimum scopes/permissions needed for GitHub/Azure DevOps tokens needed to use this template, along with reasons why.

## GitHub

For best security, you should create two GitHub Personal Access tokens via [this link](https://github.com/settings/personal-access-tokens/new), a **Repo Setup PAT** and a **Repo Maintenance PAT**, permissions of which are detailed below.

The **Repo Setup PAT** can be stored in your password vault of choice, as you will only need it when you are creating a new repo via this template.

The **Repo Maintenance PAT** should be saved as a GitHub Actions secret on the repository called **REPO_MAINTENANCE_PAT**.

NOTE: Fine-grained tokens are specific NOT used, as they cannot open pull requests. This can be changed once [this issue](https://github.com/github/roadmap/issues/600) is implemented by GitHub.

### Repo Setup PAT (Classic Token)

**Repository Access**: All repositories

| **Scope**                      | **Reason**                                         |
| ------------------------------ | -------------------------------------------------- |
| repo                           | Needed to create repo & set its settings           |
| workflow                       | Needed to commit GitHub Actions workflows          |

### Repo Maintenance PAT (Classic Token)

**Repository Access**: All repositories

| **Scope**                     | **Reason**                                 |
| ----------------------------- | ------------------------------------------ |
| repo                          | Needed for Copier/Release Please workflows |

## Azure DevOps

| **Scope**             | **Reason**                               |
| --------------------- | ---------------------------------------- |
| Build: Read & Execute | Needed to allow creating Azure Pipelines |
| Code: Full            | Needed to create repo                    |

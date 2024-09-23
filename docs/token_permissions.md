# Token Permissions

This doc details the minimum scopes/permissions needed for GitHub/Azure DevOps tokens needed to use this template, along with reasons why.

## GitHub

### Personal Access Tokens (classic)

**Scope** | **Reason**
---|---
repo | Needed to create repo & set its settings
workflow | Needed to allow template tasks to commit workflows

### Fine-grained tokens

**Permission** | **Reason**
---|---
Repository > Administration: Read & Write | Needed to create repo & set its settings
Repository > Issues: Read & Write | Needed to create custom labels
Repository > Workflows: Read & Write | Needed to allow template tasks to commit workflows

## Azure DevOps

**Scope** | **Reason**
---|---
Build: Read & Execute | Needed to allow creating Azure Pipelines
Code: Full | Needed to create repo

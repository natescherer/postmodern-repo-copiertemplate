# Public vs Private Repos

In order to increase the usefulness of the Postmodern template ecosystem, full support for both Public and Private repositories are included.

## What is Public?

For the purposes of this template, a Public repo is an open-source project that is visible to the internet and encourages contributions.

## What is Private?

For the purposes of this template, a Private repo is a closed-source project that requires authentication to access.

## Differences

Private repos omit the following features that would not be relevant to them, with reasoning for each:

### Repository Management

- Contributor management and crediting via All Contributors
    - Irrelevant on non-public projects

### Support Files

- `CODE_OF_CONDUCT.md`
    - Irrelevant on non-public projects
- `CONTRIBUTING.md`
    - Likely not needed for a private project, but you can always provide your own custom file which will be ignored by template updates
- `LICENSE`
    - No need to license something not available to others, but you can always provide your own custom file which will be ignored by template updates

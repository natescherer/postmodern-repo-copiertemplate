# Troubleshooting

## Setup

**mise says the config isn't trusted.** mise won't read a `mise.toml` it hasn't been told to
trust. Run `mise trust` from the repo root, then `mise install`.

**Copier stops at the Repo Setup Actions question.** That question's validator checks the
platform CLI before anything runs, and its message says what's missing: install `gh` or `az`,
run `gh auth login` or `az login`, add the Azure DevOps extension with
`az extension add --name azure-devops`, or (for Create Repo) put `knope` on your `PATH`. See
[Prerequisites](../getting-started/prerequisites.md). Choosing `None` skips the check, and the
setup it guards.

**Copier says the destination repository is dirty.** Copier won't copy over or update
uncommitted changes. Commit or stash them, then run it again.

## Releases

**No release PR opens.** In order of likelihood:

- Nothing since the last release bumps the version: `docs:` commits don't, and neither do
  `chore:` commits other than Renovate's. That's expected; see
  [Releasing](releasing.md).
- On GitHub, Actions isn't allowed to open pull requests. Enable **Allow GitHub
  Actions to create and approve pull requests**; see
  [Manual Repo Settings](../reference/manual-repo-settings.md).
- On Azure DevOps, the build service identity can't push branches or open pull
  requests. Grant it the repository permissions in
  [Prerequisites](../getting-started/prerequisites.md).

**The release PR can't merge because its check never runs.** On GitHub, each
push a bot makes to the release PR waits for someone to click **Approve and run workflow**; see
[Releasing](releasing.md).

## Dependencies

**Renovate doesn't update a dependency.** Run `mise run renovate-lookup` and check whether the
dependency appears, with the right version, in the `packageFiles with updates` log entry. If it
doesn't, Renovate can't see it; see
[Adding a Dependency or Tool](development.md#adding-a-dependency-or-tool). If it does, on GitHub check
that the Renovate app has access to this repo.

## Template updates

**`copier update` fails while rendering your project's old version.** See
[Updating from the Parent Template](updating-from-template.md#troubleshooting).

# Stability Policy

This template follows [Semantic Versioning](https://semver.org/). Its public interface is
everything a project generated from it depends on: the questions and what their answers do, the
files it generates and where they live, and the URLs of these docs.

## What counts as breaking

A release is a **major** version when a project already generated from the template needs
manual action after `copier update` to keep working the way it did. That includes:

- Removing or renaming a question, or changing what an existing answer does.
- Moving, renaming, or removing a generated file that projects commonly reference or customize,
  such as a workflow or pipeline file, or a CI job whose name a branch protection rule or
  required check points at.
- Removing a supported option, such as a `developer_platform`.
- Moving or removing a page in these docs, since generated projects' docs link into them.

A change that a `_migrations` step in `copier.yml` handles completely, with nothing left for
the project to do, isn't breaking.

## Minor and patch releases

- **Minor** (`feat:`): new questions with a default, new generated files, new features, and
  newly deprecated options.
- **Patch**: bug fixes (`fix:`), dependency bumps, and changes that leave a correctly working
  project's output unchanged.

Docs-only changes don't trigger a release on their own; see
[Releasing](../maintaining/releasing.md).

## Deprecations

Something slated for removal is deprecated first, in a minor release: the question's help text,
these docs, and the changelog say so. It keeps working for the rest of that major version and is
removed in the next one.

Azure DevOps support is deprecated (see
[`developer_platform`](template-questions.md#developer_platform-github-azure-devops)). It stays
supported for every 1.x release and is removed in 2.0.0.

## Updating across a major version

`copier update` moves to the latest release, including across a major version. Before an update
that crosses one, read that release's **Breaking Changes** in the changelog and follow its steps
as part of the same update.

To stay on the current major for now, pass the newest tag in that major explicitly:

```bash
mise run copier-update --vcs-ref=<tag>
```

# Updating from the Parent Template

This project was generated from the [Postmodern Repo Copier Template](https://github.com/natescherer/postmodern-repo-copiertemplate)
[Copier](https://copier.readthedocs.io/) template. On the 1st of each month, the Monthly Maintenance
workflow/pipeline's Copier Update Check job checks for a new template release and sends a notification to
`APPRISE_URL` when one is available; see [Secrets and Tokens](../reference/token-permissions.md#apprise_url).

To pull in its latest changes:

1. Start from a clean working tree on a new branch; Copier won't update over uncommitted
   changes.
1. If the update crosses a major version, read that release's **Breaking Changes** in the
   template's changelog first; see its [Stability Policy](https://natescherer.github.io/postmodern-repo-copiertemplate/latest/reference/stability-policy/).
1. Run `mise run copier-update`. It reuses your recorded answers and asks only the questions
   added since your last update.
1. Resolve any conflicts where your own edits overlap a template change; Copier marks
   them inline.
1. Review the new files in `.changeset/`, one per relevant upstream change, and delete the
   ones that don't apply to your project. Each links to the upstream PR it came from.
1. Commit and open a pull request as usual. The remaining changesets go into your
   [next release](releasing.md) with your own commits.
1. On Azure DevOps, if the update renamed, merged, or removed files under
   `.azurepipelines/`, run `mise run migrate-azdo-pipeline-names` once the pull request has
   merged to `main`. It repoints an existing registration at each new name, keeping its run
   history and variables, and deletes the registrations of pipelines merged into another.
   Wait for the merge: Azure DevOps reads pipeline YAML from `main`, so repointing earlier
   breaks every run until the new files get there. It's safe to run when nothing needs
   migrating.

## Troubleshooting

If `copier update` fails while rendering your project's *old* template version (for example,
because that version depends on something that no longer exists), re-apply the current template
over the project:

1. Copy `.config/copier-answers.yml` to a temporary file outside the repo and delete every key
   that starts with `_` from the copy.
1. Run:

    ```bash
    mise x -- copier copy --trust --overwrite --data-file <temporary-answers-file> https://github.com/natescherer/postmodern-repo-copiertemplate .
    ```

1. Unlike `copier update`, this overwrites your own edits. Review every changed file with
   `git diff`, and restore what you'd customized before committing.

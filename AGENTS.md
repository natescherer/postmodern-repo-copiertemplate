# Notes for AI Agents

## Git workflow

- Write commit messages as `type: summary` (Conventional Commits, enforced by
  `.config/committed.toml`), with the subject at most 72 characters. Add a short body only
  when it explains rationale the diff doesn't show.
- Never push a git tag to this repo without the user's approval for that specific tag, and
  never push one shaped like a version number (such as `v99.0.0`), even as a testing
  workaround. Projects that copy from this repo can see its tags, and a stray one could resolve
  as a real release. A local testing tag that isn't version-shaped needs no approval; delete
  it as soon as the test is done.

## Render-validation test suite

The suite lives in `template/{% if is_template %}tests{% endif %}/`. Run it with:

```sh
mise x -- pytest "template/{% if is_template %}tests{% endif %}/"
```

- `conftest.py`: shared fixtures.
- `test_render.py`: renders every `ANSWER_MATRIX` entry in `answer_matrix.py` and checks the
  output, including an update from the last tag and a copy from a Template child.
- `test_content.py`: config and content consistency, such as nav completeness and hook-tool
  availability.
- `test_validators.py`: checks that `copier.yml.jinja`'s `validator:` blocks reject each
  `INVALID_ANSWER_MATRIX` entry.
- `test_answer_matrix_coverage.py`: audits `answer_matrix.py` against the real question set.

Keep `answer_matrix.py` in step with `copier.yml.jinja` in the same change:

- **New question or new choice value:** use every value in at least one
  `ANSWER_MATRIX` entry, respecting the question's `when:` and any `validator:`.
  Prefer changing an existing entry over adding one, since each entry costs a
  full render. `test_answer_matrix_coverage.py` catches a missing `choices:`
  value, but not a missing yes/no value, so cover both of those by hand.
- **A value the last release doesn't accept** (new or renamed): the
  update-path test copies each entry at that release first, so give the entry
  `"_old_tag_overrides": {"<question>": "<value that release accepts>"}` until
  the next release ships, then remove it.
- **New `validator:` constraint:** add a combination it should reject to
  `INVALID_ANSWER_MATRIX`, with an `expected_error` substring of its message.
- **Renamed or removed question or value:** update every entry that uses it.

The suite has a second copy in root `tests/`, which PR Validation runs; descendant templates
inherit the `template/` copy. Add each new or changed test to both, unless descendants
shouldn't inherit it; then add it to root `tests/` only. Run each copy before committing: the
`template/` copy with the command above, and root's with `mise x -- pytest tests/`.

A hook's tool entry in `mise.toml.jinja` and its gate in `prek.toml.jinja` must use the same
condition. `test_hook_tools_available` checks that every local prek hook's tool is installed
for each answer combination, and relies on that match. `actionlint` needs
`is_template or using_github`, not `using_github` alone: `copy-template-files` copies all of
`template/`, workflows included, into every Template project, so an Azure DevOps Template
project still runs actionlint.

## Setup checklist

`setup_checklist` in `copier.yml.jinja` lists what a new project's owner has to finish by hand;
`copier copy` opens it as a GitHub Issue or prints it. **Add to it whenever a new feature needs
the user to configure, replace, or complete something after copying.**

## Integration test runbooks

The `runbook-*.md` pages in `docs/maintaining/integration-testing/` hold every step of an
integration test run, including what a `copier copy` can't verify: whether a workflow or
pipeline authenticates, triggers, and does its job. Both are static and unconditional, since a
template author tests every feature on both platforms, and each step is exact, the same on
every run. **Add to the relevant one whenever a new or changed workflow or pipeline needs its
behavior checked by hand.**

## Renovate `schedule` cron syntax is not standard cron

Renovate's `schedule` option (in `renovate.json` and `template/renovate.json.jinja`)
looks like 5-field cron, but Renovate reads it differently on every platform:

- The minutes field **must** be `*`. Renovate has no minute-level granularity, and a schedule
  that restricts minutes is invalid.
- A schedule defines an allowed **time window**, not a trigger time. Renovate runs on its own
  polling cadence, outside this project, and acts only inside the window.

So `"* 18 1 * *"` is the correct form for "once a month, on the 1st, during hour 18". Don't
change it to `"0 18 1 * *"`: that restricts the minutes field, which Renovate rejects.

Reference: <https://docs.renovatebot.com/key-concepts/scheduling/>

## Tooling

`mise.toml` pins every dev tool; run them as `mise x -- <tool>`, not from `PATH`. prek's Git
hooks (`.config/prek.toml`) run the linters and formatters on every commit and check the commit
message. Fix what they report instead of bypassing them with `--no-verify`.

## Managed files

Tooling writes these; don't edit them by hand:

- `.config/copier-answers.yml`: Copier's record of this project's answers.
- `CHANGELOG.md` and `.config/knope-current-version.json`: Knope updates both when it prepares
  a release.
- The README's lifecycle notice: set by the `lifecycle` answer; change it with
  `mise run set-lifecycle`.
- `docs-site/` (when docs are built into the repo): CI rebuilds
  it from `docs/` whenever docs change on `main`.

Files from the parent template change through `mise run copier-update`. A local edit to one is
kept, but every later update has to merge around it.

## Documentation

Docs live in `docs/` and are built with Zensical. Add every new page to `nav` in
`zensical.toml`.

## Dogfooding architecture

This section is hand-maintained, not templated: `template/AGENTS.md.jinja` doesn't carry it,
since dogfooding applies only to this repo. Like the root `copier.yml` exception, it's a
permanent addendum that a `copier update` must not remove.

This repo is a Copier template (source of truth under `template/`) and, through dogfooding, a
rendered instance of that template (`project_type: Template` in `.config/copier-answers.yml`).
Root-level files such as `mise.toml`, `README.md`, `docs/`, and `.github/workflows/` are
**rendered output**. They lag behind `template/` until a `copier update` re-renders them.
**Never hand-edit a root-level dogfooded file; edit its `template/` source instead.**

That includes root `tests/`, so the render-validation suite's rule of adding each test to both
copies doesn't apply here: add it to `template/`'s copy only, and run that copy with the
`template/` command. Root `tests/` holds the last-synced suite, so a new or edited test runs
from root only after the next `copier update`.

Two exceptions:

- **Root `copier.yml`** must stay in sync **immediately**, in the same change as any edit to
  the raw-block body of `template/{% if is_template %}copier.yml{% endif %}.jinja`. Copier reads
  root `copier.yml` when this repo is the source, so a stale copy breaks real use. To sync it,
  render `copier.yml` from the updated template with this repo's recorded answers, confirm the
  diff against the current root file is exactly the intended edit, then replace the file. Render
  from a plain-directory copy of `template/` plus root `copier.yml`, not from this repo's `.git`:
  a git-source render reads HEAD and ignores uncommitted edits.
- **Root files something reads directly.** When staleness causes a problem now, not just a
  missing feature until the next update, sync the root file as a deliberate, flagged exception.
  `renovate.json` is one: Renovate reads it on its own schedule. Root `knope.toml` is another,
  for any workflow a `copier.yml` migration runs by cloning this repo (such as
  `compute-upstream-bump`): the clone gets root `knope.toml`, not `template/knope.toml.jinja`,
  so a workflow defined only in the template fails with "unrecognized subcommand" in every
  child's migration until root catches up.

To test template changes, render from `template/`, or run `copier update --vcs-ref=HEAD` on
root first; never use the stale root as a Copier source. A git-source render reads HEAD, not
the working tree, so to include uncommitted edits, render from a plain-directory copy (with
`.git` removed) or commit first.

If `copier update` can't render an old baseline (for example, the old version needs a Jinja
extension or `invoke` task that no longer exists), update once with that version's extensions
installed and `--skip-tasks`, as the Upgrading from 0.x guide shows. Use
`copier copy --overwrite --data-file <answers without _ keys> --vcs-ref=HEAD <source> .` only as
a last resort: it overwrites local edits, so diff every changed file against `HEAD` before
staging.

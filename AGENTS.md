# Notes for AI Agents

## Git workflow

- Commit message style: `type: summary` as the first line (Conventional
  Commits, enforced by `.config/committed.toml`; keep the subject at or
  under 72 characters). A short body paragraph explaining non-obvious
  rationale is fine when it adds real context; don't pad a trivial change with
  one just to have one.
- Never push a git tag to this repo without explicit user approval for that
  specific tag, and never push one shaped like a version number (e.g.
  `v99.0.0`) even as a throwaway testing workaround; this repo's tags are
  visible to any downstream project that copies from it, and a real one could
  resolve against a stray tag. A non-version-shaped tag for local testing is
  fine to create without asking, but delete it immediately once the test that
  needed it is done.

## Render-validation test suite

Location: `template/{% if is_template %}tests{% endif %}/`. Run via:

```sh
mise x -- pytest "template/{% if is_template %}tests{% endif %}/"
```

Files: `conftest.py` (shared fixtures), `test_render.py` (structural
validation across `answer_matrix.py`'s `ANSWER_MATRIX`, including an
update-from-last-tag path), `test_content.py` (config/content consistency,
e.g. nav completeness, hook-tool availability), `test_validators.py` (asserts
`copier.yml.jinja`'s `validator:` blocks actually reject what they claim to,
via `INVALID_ANSWER_MATRIX`), `test_answer_matrix_coverage.py` (audits
`answer_matrix.py` itself against the real question set). **Update
`answer_matrix.py` whenever a Copier question is added, removed, or renamed,
or a new `validator:` constraint is added.**

Always run it via the command above (against `template/`'s own source), never
`pytest tests/` from the repo root: root's `tests/` is a dogfooded, rendered
copy of this same suite (see Dogfooding architecture below), so a newly added
or edited test *function* only exists under `template/` and silently never
runs from root until the next full sync, even though root's copy still
executes without error.

A hook's `mise.toml.jinja` tool entry and its `prek.toml.jinja` gating
condition must match exactly: `test_hook_tools_available` verifies every
local prek hook's tool is installed for that answer combination, and it only
works because each hook is gated behind the identical condition as its tool.
`actionlint` specifically needs `is_template or using_github`, not just
`using_github`: `copy-template-files` embeds a full, unrendered copy of
`template/` (workflows included) into every Template-type project regardless
of *that* project's own `developer_platform`, so an Azure DevOps-hosted
Template project still needs actionlint available. Narrowing that condition
to just `using_github` is a real regression this repo has hit before.

## Renovate `schedule` cron syntax is not standard cron

Renovate's `schedule` option (see `renovate.json` / `template/renovate.json.jinja`)
looks like 5-field cron but isn't interpreted the same way:

- The minutes field **must** be `*`: Renovate doesn't support minute-level
  granularity, and a schedule that restricts it is invalid.
- A cron schedule defines an allowed **time window**, not an exact trigger
  instant: Renovate itself runs on its own polling cadence (external to
  this repo) and only acts during the window the schedule describes.

So `"* 0 1 * *"` is the *correct* idiomatic form for "once a month, on the
1st, during hour 0"; it is not a bug, even though it looks like a broken
"every minute" cron at a glance. Do not change it to `"0 0 1 * *"` (a
standard-cron-style fix): that's invalid for Renovate specifically, since it
constrains the minutes field.

Reference: <https://docs.renovatebot.com/key-concepts/scheduling/>

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

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

This section is hand-maintained, not templated; `template/AGENTS.md.jinja` doesn't
carry it, since dogfooding is specific to this repo and never applies to a generated
child. Treat it like the root `copier.yml` exception: a deliberate, permanent addendum,
not something a future `copier update` should reconcile away.

This repo is both a Copier template (source of truth under `template/`) and,
via dogfooding, a rendered instance of that same template
(`project_type: Template` in `.config/copier-answers.yml`). Root-level files
like `mise.toml`, `README.md`, `docs/`, and `.github/workflows/` are
**rendered output**, not hand-maintained; they lag behind `template/` until
an explicit `copier update` (or a new release) re-renders them. **Never
hand-edit a root-level dogfooded file; edit the matching `template/` source
instead.**

Two exceptions:

- **Root `copier.yml`** must be kept in sync **immediately**, in the same
  turn as any edit to `template/{% if is_template %}copier.yml{% endif %}.jinja`'s
  raw-block body. Copier reads root `copier.yml` directly (not from inside
  `template/`) when this repo is used as a Copier source, so a stale root
  copy breaks real usage, not just documentation. Safe method: render just
  `copier.yml` from the updated template against this repo's own recorded
  answers, diff against the current root file to confirm the delta is exactly
  the intended edit, then replace it wholesale. Render from a plain-directory
  copy of `template/` plus root `copier.yml` (not this repo's `.git` source
  directly): a git-source render reads from HEAD, so it silently ignores any
  edit that isn't committed yet.
- Occasionally another root file is operationally load-bearing enough that
  staleness causes an active problem right now (not just "missing a new
  feature until the next update"); e.g. `renovate.json`, which Renovate
  reads directly on its own schedule regardless of `copier update`. Treat
  syncing those as a deliberate, flagged exception, not the default. Root
  `knope.toml` joins this list specifically for any workflow that
  `copier.yml`'s `_migrations` scripts invoke by cloning this repo (e.g.
  `compute-upstream-bump`); that clone gets whatever's actually committed to
  root `knope.toml`, not `template/knope.toml.jinja`, so a workflow that only
  exists in the template source silently fails with "unrecognized subcommand"
  in every child's migration until root catches up.

When validating template changes (e.g. testing uncommitted edits), don't copy
this repo's root as a Copier source; either render fresh from `template/` or
run a real `copier update --vcs-ref=HEAD` first, since the root will be stale.
A git-source render (unlike a plain local-directory source) reads from git
HEAD, not the working tree, so even a fresh `template/` checkout won't pick up
*uncommitted* edits unless the source is a plain directory copy (strip `.git`
so Copier treats it as files, not a repo to check out from) or the edits are
committed first.

If `copier update`/`copier recopy` ever deadlocks trying to render an old
baseline tag (e.g. a removed extension module the old tag still references),
`copier copy --overwrite --data-file <answers-file-with-underscore-keys-stripped>
--vcs-ref=HEAD gh:<owner>/<repo> .` is the escape hatch, but it has no
"preserve unless template changed" diffing, so treat its output as a rough
draft and diff every changed file against the pre-copy `HEAD` before staging.

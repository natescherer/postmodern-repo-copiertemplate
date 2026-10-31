# Extending This Template

This template supplies what any Git-tracked project needs, whatever it contains: repo settings,
CI/CD, release automation, and repo hygiene. It's meant as a common ancestor. A Python library
template, a PowerShell module template, or a Terraform template starts from a `copier copy` of
this one with `project_type: Template`, which gives it its own copy of `template/` to build on,
and then adds what its domain needs.

What keeps this template correct has to carry over to yours. The render tests, Renovate
coverage, CI on both platforms, and migrations for existing projects are all generic. This page
covers applying them to what you add, starting with the decision that shapes the rest.

## Start here: will other templates build on yours?

Decide this first; it sets how much of this page applies to you. The
[`extensible_template`](../reference/template-questions.md#extensible_template-yes-no) question
records the answer.

=== "Leaf template (most common)"

    Your template produces finished projects, and nothing copies from it again. This is the
    lower-maintenance path, and the right default unless you know otherwise. Answer no to
    `extensible_template`, and the template handles the rest:

    - Your `template/` leaves out this template's template-only files (its `copier.yml`,
      tests, scripts, and template docs), so you only maintain what your projects use.
    - The files it keeps have no `is_template`, `is_standard`, or `is_extensible`
      conditions: each update folds them out, so only the conditions that still vary remain.
    - Your `copier.yml` has no project-type questions or `copy-template-files` task; every
      project it creates is Standard.
    - The obligations below about your own template's extensibility don't apply.

=== "Extensible template"

    Your template can itself be copied with `project_type: Template`, the relationship this
    repo has to yours. Answer yes to `extensible_template`. That costs maintenance for as long
    as the template exists:

    - Your `copier.yml` keeps `project_type` and `extensible_template`, so your projects can be
      templates too.
    - Your `template/` keeps the whole `is_template`-gated subtree, to carry forward.
    - Write a guide like this page for whoever extends your template. Adapt this one: most of
      it (dependency pinning, Renovate coverage, the CI checklist, the testing layers) applies
      to any Copier template.

!!! tip "When a leaf template is the right call"
    An internal, single-company template is usually a leaf template. Nobody will fork
    it, and the `Template`/`Standard` branch costs its maintainers indefinitely: an extra
    question to explain, extra conditionals, and extra answer combinations for the
    render-validation suite. Choose an extensible template when you know another template
    will build on yours.

## The mental model

Everything in this template varies along a few axes. Every question, file, and check either
applies to all combinations or is gated to the ones it belongs to:

- **`developer_platform`** (`GitHub` / `Azure DevOps`): most capabilities exist on both
  platforms. A GitHub Actions workflow has an Azure Pipelines counterpart, a GitHub secret has
  a pipeline variable, and so on. `using_github` and `using_azdo` gate the differences.
- **`project_type`** (`Template` / `Standard`): `is_template` gates what only a Copier template
  needs (the `template/` subtree, the integration test scripts, this page), and `is_standard`
  is its complement. Whether your template keeps this axis is the decision above.
- **Your own axes.** A Python library template might add a `package_manager` question (`uv` /
  `poetry`); a Terraform template might add `terraform` / `opentofu`. The render-validation
  suite has to exercise each answer and each combination of answers; see
  [Testing what you add](#testing-what-you-add).

Each new axis multiplies the combinations everything else has to work for. When two ideas are
close, add an option to an existing axis instead of a new axis.

## Workflow: extending the template

Use the checklist below that matches your change. Most changes need one; a larger change, such
as a new tool that also needs a secret and a CI check, works through several in turn.

### Adding a new versioned dependency or tool

Follow [Adding a Dependency or Tool](development.md#adding-a-dependency-or-tool). It covers the
`renovate:` comments that pins under `template/` need, and how to check that Renovate detects
them.

### Adding a new Copier question

1. Add the question to `copier.yml`, with a `when:` or `validator:` if it's conditional or
   constrained.
1. Use each of its values in some `ANSWER_MATRIX` entry in `answer_matrix.py` (in each copy of
   the suite; see [Template-level tests](#template-level-tests)), and add a
   combination each new `validator:` should reject to `INVALID_ANSWER_MATRIX`. `AGENTS.md`
   lists the rules, including `_old_tag_overrides` for a value the last release doesn't
   accept; `test_answer_matrix_coverage.py` catches a missed `choices:` value.
1. If the question changes what a fresh `copier copy` sets up, update `_message_after_copy` and
   the template-questions reference in `docs/` to match.

### Adding a new CI workflow or pipeline

1. Build both platform variants together; a gap left for later tends to stay. Follow the naming
   convention: `Category (Auto/Manual): Name` on GitHub, `Category (Auto/Manual) - Name` on
   Azure DevOps.
1. Register it on Azure DevOps. Pipelines there are registered objects, not just files, so add
   it to the `az pipelines create` tasks in `_tasks`.
1. Add a check to the integration test scripts: a `check_*()` function, and on Azure DevOps the
   pipeline's display name in `PIPELINE_DISPLAY_NAMES` in `integration_test_azdo.py`.
1. Add what can't be automated to the integration test runbooks
   (`docs/maintaining/integration-testing/runbook-github.md` and `runbook-azdo.md`) as exact
   steps, such as checking a third-party bot's response.
1. If it needs a secret, work through the next checklist too.
1. Put any new SHA-pinned action, Azure Pipelines task version, or embedded tool version
   through the dependency checklist above.

### Adding a new secret or credential

1. Document its purpose and required scopes in `docs/reference/token-permissions.md`.
1. Add it to the `provision-secrets` task (`gh secret set` or `az pipelines variable create`),
   so setup stays one guided step.
1. Check for it in every workflow or pipeline that uses it: the `require-secrets` composite
   action on GitHub, or the equivalent guard step on Azure DevOps. A missing secret then fails
   with a clear message instead of a confusing error later.
1. Add it to the "Before CI works" secrets list in `_message_after_copy` for each platform that
   needs it.
1. If it can expire, consider an expiration check, for example in the monthly repo health
   check: authenticate as the credential, read the expiration date the platform's API reports,
   and notify before it lapses.

### Renaming or removing something

A rename has to reach every project that already has the old name. A plain file rename or
removal needs nothing extra: `copier update` deletes what the template dropped and adds what
it gained, like any other change.

1. Update every reference to the old name: the integration test scripts, the manual
   verification checklists, and any list that enumerates things by name, such as
   `PIPELINE_DISPLAY_NAMES`. Those lists are the easiest reference to miss.
1. If existing content has to change shape (reformatting a file so a tool can parse it, or
   converting old data), add a `_migrations` entry. Don't give it a `version:`: Copier checks
   that against the version of the template a project updates from, which in a child
   template's projects is the child's own version. Make it safe to rerun, a no-op once its work
   is done, and let it run on every update.

!!! warning "Live registered objects aren't files"
    Copier's diff only reaches files. An Azure DevOps pipeline registration exists only as a
    remote API object, and `_tasks` runs only on `copier copy`, so renaming a pipeline's file
    leaves its registration pointing at the old path. `migrate_pipeline_names.py` repoints the
    registration in place, keeping its ID, run history, and variables; see its docstring.

### Testing what you add

Two things need testing separately: whether the template renders correctly, and whether what it
produces works.

#### Template-level tests

These test the Copier mechanics (questions, conditionals, CI/CD scaffolding), independent of
your domain content, in three layers:

- **`pytest tests/`** runs locally and on every PR, with no external side effects. It renders
  every answer combination and checks for valid Jinja, YAML, and JSON, working internal links,
  and consistent config. New `ANSWER_MATRIX` entries and `validator:` constraints get exercised
  here.
- **Integration testing** (`integration_test_github.py` and `integration_test_azdo.py`) creates
  real repos and runs real workflows and pipelines against them. It catches regressions that
  need a real API call, a running pipeline, or an external system. Run it before each release.
- **The integration test runbooks** hold every step of a run, and their manual steps cover
  the rest: human judgment, and systems the scripts can't inspect, such as whether a bot
  responded.

A CI/CD change tested only by the first layer is untested where it's most likely to break.
Verify it on a real platform.

An extensible template has two copies of the suite. PR Validation runs root `tests/`, and the
templates built on yours inherit `template/{% if is_template %}tests{% endif %}/`. Add each new
or changed test to both, so your CI runs it and your descendants get it. A test they shouldn't
inherit goes in root `tests/` only. `copier update` keeps the test files you add to root
`tests/` and merges your edits into this template's, such as `answer_matrix.py`. A leaf
template's `template/` has no tests, so its tests go in root `tests/`.

#### Tests for what the template produces

This template is pure scaffolding with no workload of its own; yours has one. A Python library
template produces Python libraries, and a Terraform template produces Terraform configs. That
content needs its own checks on top of the template-level layers:

- **Starter or example code** (a sample module, a sample stack) should pass its own test
  suite, linter, and type checker. Starter code that renders but doesn't work passes every
  template-level test and fails the first time a user runs it.
- **CI that tests the workload** (the generated project's tests, linting, `terraform validate`)
  goes through the same [Adding a new CI workflow or pipeline](#adding-a-new-ci-workflow-or-pipeline)
  checklist as any other workflow.
- **The domain's own dependencies and tools** (a package manager, a linter, a language server)
  go through the [Adding a new versioned dependency or tool](#adding-a-new-versioned-dependency-or-tool)
  checklist; Renovate coverage includes them too.

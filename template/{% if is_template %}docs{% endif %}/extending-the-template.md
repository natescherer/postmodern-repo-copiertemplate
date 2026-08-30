# Extending This Template

This template is deliberately universal: it provides the settings, CI/CD, release automation, and repo hygiene that apply to *any* Git-tracked project, regardless of what's actually in it. It's meant to be a common ancestor: a Python library template, a PowerShell module template, a Terraform-config template, and others all start from a `copier copy` of this one (with `project_type: Template`, which gives you your own copy of `template/` to build on) and then add whatever's specific to their own domain.

That inheritance is the whole point, but it also means the discipline that keeps *this* template correct has to travel with you. Every mechanism this template relies on (the render tests, Renovate coverage, dual-platform CI, the migration story for existing downstream projects) is generic. None of it is specific to what this template happens to contain today. This page walks through applying that same discipline to whatever *you* add, starting with the one decision that shapes everything else.

## Start here: will other templates build on yours?

Resolve this before anything else: it decides how much of the rest of this page even applies to you.

=== "Leaf template (most common)"

    Your template produces finished projects and nothing ever copies *from* it again: it's the end of the chain. This is the lower-maintenance path, and the right default unless you specifically know otherwise:

    - Drop the `project_type` axis from your own `copier.yml` (or hardcode it to whatever your one output shape is): there's no `Template` branch to carry if nothing downstream of you will ever itself be a template.
    - Skip the `template/`-subtree-gated-by-`is_template` convention entirely. You have exactly one branch, not two.
    - None of the obligations below about *your own* extensibility apply: you're not handing anyone else a template to extend.

=== "Extensible template"

    Your template can itself be copied with `project_type: Template` to become the parent of a further template, exactly the relationship this repo has to yours. That inheritance keeps costing you maintenance for as long as the template exists:

    - Keep `project_type` (or your own equivalent axis) so children can choose `Template` vs `Standard`.
    - Carry your own `template/` subtree convention forward, gated the same way this one is.
    - You inherit the obligation this page is discharging right now: a "what touches what" guide of your own, for whoever extends *you* next. Adapt this page rather than starting from a blank one: most of it (dependency pinning, Renovate coverage, the CI checklist, the testing layers) is generic to *any* Copier template, not specific to this one.

!!! tip "When leaf is the right call"
    An internal, single-company template usually doesn't need the extensible path: there's no third party waiting to fork it, and carrying the `Template`/`Standard` branch (the extra axis, the extra conditionals, the extra questions to explain, the extra answer combinations the render-validation suite has to exercise) is dead weight your maintainers pay for indefinitely with no one ever spending it. Choose extensible because you *know* another template will sit on top of yours, not because it seems more flexible to leave the door open.

## The mental model

Everything in this template varies along a small number of axes, and every question, file, and check either applies to all combinations or is explicitly gated to the ones it belongs to:

- **`developer_platform`** (`GitHub` / `Azure DevOps`): most capabilities exist in parallel on both platforms, a GitHub Actions workflow has an Azure Pipelines counterpart, a GitHub secret has an Azure Pipeline variable, and so on. `using_github`/`using_azdo` gate the difference.
- **`project_type`** (`Template` / `Standard`): `is_template` gates everything that only makes sense for a project that is itself a Copier template (the `template/` subtree, integration test scripts, this very page). `is_standard` is its complement. Whether *your* template keeps this axis at all is the fork you just resolved above.
- Whatever new axis *you* introduce. A Python library template might add a `package_manager` question (`uv` / `poetry`); a Terraform template might add one for `terraform` / `opentofu`. Each answer (and, more importantly, each *combination* of answers) is something the render-validation suite has to actually exercise (see [Testing what you add](#testing-what-you-add)).

Adding a new axis is a real decision, not a casual one: it multiplies the combinations everything else needs to keep working for. Prefer extending an existing axis's *options* over introducing a wholly new axis when the two are conceptually close.

## Workflow: extending the template

Once you know which fork you're on, everything else is the same kind of work repeated for whatever you're adding. Work through whichever checklist below matches what you're touching: most changes only need one, and a bigger change (a new tool that also needs a secret and a CI check) just means working through more than one in sequence.

### Adding a new versioned dependency or tool

This is the exercise that prompted this page; see [Token Permissions](token-permissions.md) and this template's own `renovate.json` for the concrete patterns referenced below.

1. **Pin it.** A floating tag, `latest`, or an unversioned install script is a reproducibility gap. If you genuinely can't find a trackable version source for something (rare, but it happens), document *why* in a comment next to the install step rather than leaving a silent gap.
2. **Wire it into `mise.toml`/`mise.ci.toml`** (or your own analog) with an exact version, not a range.
3. **Make sure Renovate can actually see it.** Check `renovate.json`'s existing `customManagers` for a manager that already covers the shape of what you're adding (a `# renovate: datasource=... depName=...` comment above an inline `key = "value"` pin covers most simple cases). If nothing fits, you'll likely need a new custom regex manager.
4. **Group related packages** if the same underlying dependency shows up under more than one name across ecosystems (e.g. a tool that's both a mise tool `depName` and a GitHub Action `depName`): a `packageRules` entry with a shared `groupName` keeps Renovate from opening two PRs for the same bump.

!!! warning "Verify it, don't assume it"
    A regex manager that looks right can still fail silently: a captured version string that includes trailing garbage (a Jinja tag with no space before it, a stray quote) won't error, it'll just get quietly dropped by Renovate during its own parsing. The reliable way to check: after `git push`, open the repo's **Dependency Dashboard** issue (Renovate creates one automatically) and confirm your dependency actually appears under **Detected Dependencies**, with the version you expect, not garbled, not missing. If you want to check a specific regex's matching behavior before pushing at all, test it directly against the real file content with a same-language regex engine (Renovate itself uses JS `RegExp` semantics) rather than reasoning about it by eye.

### Adding a new Copier question

1. Add the question to `copier.yml`, with a `when:`/`validator:` if it's conditional or constrained.
2. Add real, reachable combinations to `answer_matrix.py`'s `ANSWER_MATRIX`; if you added a `validator:`, also add a combination it's supposed to reject to `INVALID_ANSWER_MATRIX`. `test_answer_matrix_coverage.py` audits `answer_matrix.py` itself against the real question set, so a forgotten entry won't pass silently.
3. Decide whether the question needs representation in **every** existing answer combination, or just some; make sure `ANSWER_MATRIX`'s existing entries reflect that (a new axis usually means revisiting entries that predate it).
4. If it changes what a fresh `copier copy` sets up, consider whether `_message_after_copy` needs a line about it, and whether `docs/` (particularly a template-questions-style reference) needs updating.

### Adding a new CI workflow or pipeline

1. Build **both** platform variants together, not one now and the other "later": a platform gap tends to stay a gap. Match the established naming convention (`Category (Auto/Manual): Name` on GitHub, `Category (Auto/Manual) - Name` on Azure DevOps).
2. On Azure DevOps, pipelines are live registered objects, not just files; wire the new one into the `_tasks` `az pipelines create` bootstrap so a fresh `copier copy` registers it.
3. Add a check for it to the integration test scripts (a `check_X()` function, plus the pipeline's display name in whatever coverage list `integration_test_azdo.py` maintains) so a real run actually exercises it, not just a local render.
4. Add whatever can't be automated to the manual verification checklists (`docs/manual-verification-github.md` / `-azdo.md`): anything that depends on an external system's own behavior (a real notification landing, a third-party bot responding) belongs there, not in the automated scripts.
5. If it needs a secret, work through the next checklist too.
6. Any new SHA-pinned action, `az pipelines create`d task version, or embedded tool version this workflow introduces goes through the dependency checklist above too.

### Adding a new secret or credential

1. Document what it's for and what scope/permissions it needs in `docs/token-permissions.md`.
2. Add it to the `provision-secrets` task (masked-prompt entry via `gh secret set` / `az pipelines variable create`) so setup stays a single guided step.
3. Validate its presence in every consuming workflow/pipeline (the `require-secrets`-composite-action pattern on GitHub; an equivalent guard step on Azure DevOps) so a missing secret fails with a clear message instead of a confusing downstream error.
4. Add it to `_message_after_copy`'s setup checklist.
5. Consider whether it can expire, and if so, whether an expiration check belongs somewhere (e.g. the monthly repo health check): authenticate as the credential itself, read whatever the platform's API reports about its expiration, and notify ahead of time rather than letting it fail silently later.

### Renaming or removing something

The tricky part isn't the rename itself: it's everyone who already copied the *old* name. A plain file rename or removal doesn't need anything special: Copier's own diff-based `update` already deletes what's gone and adds what's new in the current template, the same way it applies any other change.

1. Update every place that referenced the old name: integration test scripts, manual verification checklists, any coverage list that enumerates things by name (these are exactly the kind of cross-reference that's easy to miss: this template's own `PIPELINE_DISPLAY_NAMES` list has had real, found-after-the-fact gaps from renames that touched every *other* reference but that one).
2. If the value itself needs transforming (not just diffed away and re-added), a `_migrations` entry is the place for that: reformatting existing content in a file so a downstream tool can parse it, or converting old data into a new shape. Give it no `version:` if it should run on every update, or a specific one for a one-time fixup.

!!! warning "Live registered objects aren't files"
    Copier's diffing can only ever touch what's on disk. Azure Pipeline registrations are the concrete example here: `_tasks` only ever runs on a fresh `copier copy`, never on `update`, and no amount of file-diffing reaches something that only exists as a remote API object. Rename the file and the ordinary template-diff handles it correctly, but the *registration* in Azure DevOps has no idea that happened, and needs a dedicated migration script (see `migrate_pipeline_names.py`'s own docstring for the full reasoning) that repoints the existing registration in place (preserving its ID, run history, and any manually-set variables) rather than losing them to a delete-and-recreate.

### Testing what you add

Two different things need testing, and conflating them hides gaps: does the *template* render correctly, and does the *thing it produces* actually work?

#### Template-level tests

These validate the Copier mechanics themselves (the questions, the conditionals, the CI/CD scaffolding), independent of whatever domain-specific content you've layered on top. Three layers, each catching a different class of problem:

- **`pytest tests/`** (fast, local, no external side effects): structural validation across the whole answer matrix: valid Jinja/YAML/JSON, no broken internal links, config/content consistency. Runs on every PR. This is where a new `ANSWER_MATRIX` entry or a new `validator:` gets exercised.
- **Live integration testing** (`integration_test_github.py`/`-azdo.py` equivalents): actually creates a real throwaway repo and runs real pipelines/workflows against it. This is the only way to catch a regression in anything that needs a real API call, a real running pipeline, or a real external system's behavior, exactly the class of thing a local render can't exercise. Run before cutting a release, not on every PR.
- **Manual verification checklists**: what's left after both of the above; human judgment (does this actually look right) and systems that can't be inspected programmatically (did a notification actually land at the configured endpoint, did a third-party bot actually respond).

A change that only touches the first layer is untested in the ways that matter most for CI/CD scaffolding; prefer verifying against a real platform whenever what you're touching can plausibly break there.

#### Tests for what the template produces

This template has no workload of its own to test: it's pure scaffolding. Yours does: a Python library template produces Python libraries, a Terraform template produces Terraform configs, and whatever domain-specific content you add needs its own kind of verification, on top of (not instead of) the template-level layers above:

- If the template ships starter or example code (a sample module, a sample stack), that code should pass its own domain's normal checks: run its actual test suite, linter, and type checker, not just confirm the files rendered without a Jinja error. A render that produces syntactically valid but broken starter code will sail through every template-level test and still hand a new user a project that fails on first run.
- Any CI workflow or pipeline you add to exercise the workload itself (running the generated project's test suite, linting, `terraform validate`, etc.) goes through the same [Adding a new CI workflow or pipeline](#adding-a-new-ci-workflow-or-pipeline) checklist as anything else; it just validates the produced code instead of the template.
- Where the domain has its own dependency or tooling ecosystem (a language's package manager, a linter, a language server), the [Adding a new versioned dependency or tool](#adding-a-new-versioned-dependency-or-tool) checklist applies there too; Renovate coverage doesn't stop at the template's own tooling.

# Integration Testing

Integration testing is the last check before every release. It creates real repos from the
current template source and exercises them on GitHub and Azure DevOps, which catches the
regressions a local render can't: repo creation, pipeline registration, and workflow runs. The
template ships for both platforms, so a release is tested on both, whichever platform this repo
uses.

## Repo A and Repo B

Each run creates two repos per platform, named `<prefix>-integration-test-<timestamp>-a` and
`...-b`, with different answers, so one run covers more of the answer space.

- **Repo A** is a copy at `HEAD`. The script runs every automated check against it: it
  dispatches pipelines, opens PRs, and cuts a release and a prerelease.
- **Repo B** is a copy at the last stable release tag, left at that tag for a person to update.
  Running the update the way a real user does, prompts included, shows each new question as users
  will see it. A second entry point to the script then checks that the update applied cleanly.

The two repos also split each either/or answer: `code_coverage` is on for Repo A and off for
Repo B on both platforms, and on GitHub, `zensical_target` is `GitHub Pages` for Repo A and
`docs-site Directory in Repo` for Repo B.

## Automated and Manual Checks

The scripts automate every check they can: they dispatch pipelines and wait for them, open PRs
and confirm they're blocked or pass, push commits and confirm the release flow responds, and cut
a release and a prerelease. A failure doesn't stop the run, so one run reports everything.

Two setup steps keep the checks independent of timing. Repo A first merges a setup PR that
pins an old dependency and lifts Renovate's schedule for it alone, so Renovate has one PR to
open on any day; commits a minimal `coverage.xml`, so PR Validation's coverage step has a report
to publish; and has its link check skip this template's published docs, whose new pages exist
only once this release publishes them. Repo B merges a setup PR with the same link check skip,
since the update brings in links to those pages. At the newest release, it records the commit
just before that release on a branch, so the update check finds a newer release there without
rendering any other version.

The terminal shows only an outline of a run: each step and each check's `[PASS]` or `[FAIL]`,
with timestamps, a spinner under the step in progress, and a summary at the end. Everything
else goes to the run's log under `.cache/integration-test/`, for analysis after the fact: every
command and its output, timestamped, and the log of every workflow or pipeline run it waited
on.

The runbooks' manual steps cover the rest, as fixed steps that are the same on every run:
anything that needs human judgment (whether a badge renders, whether each setup checklist item
applies) and anything the scripts can't read (a pipeline step's log on Azure DevOps, or whether
the Renovate and All Contributors apps responded on GitHub).

The scripts find test repos by name, so their cleanup also removes what a run that stopped
partway left behind. Each repo's local clone is named after it too, so cleanup deletes those,
and keeps the temp directory from filling up with old runs. On Azure DevOps, deleting a repo
leaves its pipelines registered, so the cleanup deletes those as well.

## How It Differs from `pytest tests/`

`pytest tests/` (`mise run test`, and CI on every PR) checks the template locally: it renders
into a temporary directory, never contacts GitHub or Azure DevOps, and runs no repo setup tasks.
It catches broken Jinja, invalid YAML and JSON, dead links, and update-path bugs, including a
real `copier update` against a git history (`test_update_from_last_tag`). Integration testing
covers what needs a real API call, a running pipeline, or an external system.

## Runbooks

Each platform's runbook holds every step of a run, from setup to cleanup:

- [Integration Test Runbook (GitHub)](runbook-github.md)
- [Integration Test Runbook (Azure DevOps)](runbook-azdo.md)

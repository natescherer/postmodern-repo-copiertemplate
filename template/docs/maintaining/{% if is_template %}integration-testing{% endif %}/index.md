# Integration Testing

Run the integration tests as the last step before every release. They create real repos from the
current template source and exercise them on GitHub and Azure DevOps, which catches the
regressions a local render can't: repo creation, pipeline registration, and workflow runs.

## Running It

- `mise run integration-test-gh` creates two GitHub repos from this template, named
  `<prefix>-integration-test-<timestamp>-a` and `...-b`.
- `mise run integration-test-azdo` does the same on Azure DevOps. Pass `--org` and `--project`,
  or let them default to this project's own when it uses Azure DevOps. It also needs a GitHub
  token for Renovate, which skips every dependency hosted on github.com without one: set
  `GITHUB_COM_TOKEN`, or log in with `gh auth login`.

Run both before a release, whichever platform this repo uses: the template ships for both.

## Repo A and Repo B

Each run creates two repos with different answers, so one run covers more of the answer space.
Each checklist has a section for each repo.

- **Repo A** is a `copier copy` at `HEAD`. The script runs every automated check against it
  before returning: it dispatches pipelines, opens PRs, and cuts a release.
- **Repo B** is a `copier copy` at the last stable release tag, left there for you to update by
  hand with the commands in its checklist section. Running the command a real user runs, prompts
  included, shows each new question the way they'll see it. Afterward,
  `mise run integration-test-verify-update-gh` or `integration-test-verify-update-azdo` checks
  that the update applied cleanly.

The two repos also split each either/or answer: `code_coverage` is on for Repo A and off for
Repo B on both platforms, and on GitHub, `zensical_target` is `GitHub Pages` for Repo A and
`docs-site Directory in Repo` for Repo B.

## What It Checks

The scripts automate every check they can: they dispatch pipelines and wait for them, open PRs
and confirm they're blocked or pass, push commits and confirm the release flow responds, and cut
a release and a prerelease. Each check prints a `[PASS]` or `[FAIL]` line as it runs, and a
summary at the end; a failure doesn't stop the run, so one run reports everything.

The manual checklists cover the rest, as fixed steps that are the same on every run: anything
that needs human judgment (whether a badge renders, whether each setup checklist item applies)
and anything the scripts can't read (a pipeline step's log on Azure DevOps, or whether Renovate
or All Contributors responded). Each checklist lists only those steps, and notes where a nearby
check is already automated.

## How It Differs from `pytest tests/`

`pytest tests/` (`mise run test`, and CI on every PR) checks the template locally: it renders
into a temporary directory, never contacts GitHub or Azure DevOps, and runs no repo setup tasks.
It catches broken Jinja, invalid YAML and JSON, dead links, and update-path bugs, including a
real `copier update` against a git history (`test_update_from_last_tag`). Integration testing
covers what needs a real API call, a running pipeline, or an external system.

Work through the checklist for each platform, by hand, against the repos the run just created:

- [Manual Verification Checklist (GitHub)](manual-verification-github.md)
- [Manual Verification Checklist (Azure DevOps)](manual-verification-azdo.md)

Each checklist ends with cleaning up the test repos. When a run stops partway (for example,
because the machine slept), `mise run integration-test-cleanup-gh` or
`integration-test-cleanup-azdo` still finds and deletes what it created.

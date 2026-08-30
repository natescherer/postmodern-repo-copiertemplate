# Integration Testing

**Run this as the last step before cutting every release.** It's the only way to catch a real regression in this template's own scaffolding; a local render can't create a repo, register a pipeline, or trigger a workflow, and those are exactly the things a release needs to still work.

Integration testing means actually running the template: creating a real throwaway repo from the current template source and confirming the result holds up, not just inspecting a local render.

## Running It

- `mise run integration-test-gh`: creates two real GitHub repos from this template, named `<prefix>-integration-test-<timestamp>-a` and `...-b`.
- `mise run integration-test-azdo`: the same shape, on Azure DevOps (pass `--org`/`--project`, or let them default to this project's own if it already uses Azure DevOps).

Run both, regardless of which platform this template's own repo happens to use; a release has to be good for every platform this template supports, not just the one you personally host on.

## Repo A and Repo B

Each run creates two repos with deliberately different answers, so between them a single run covers more of the answer space instead of exercising the same fixed answers twice. Each checklist below has a matching section per repo.

- **Repo A** is a plain `copier copy` at `HEAD`, ready to check immediately; both `mise run integration-test-gh`/`integration-test-azdo` run every automated check they can against it directly (dispatching pipelines, opening real PRs, cutting a real release) before returning.
- **Repo B** is copied at the last stable release tag and left there; it does *not* get updated for you. Applying that update is deliberately a manual step, spelled out in each checklist's own Repo B section: running the exact command a real user runs, prompts included, is the only way to see a new question land the way it actually would for them, not however a script might have answered it. Once you've updated it by hand, `mise run integration-test-verify-update-gh`/`integration-test-verify-update-azdo` automates checking that it applied cleanly.

The two repos also split every other either/or answer this template offers, so both branches get exercised somewhere: `code_coverage` is on for Repo A and off for Repo B on both platforms; on GitHub, `zensical_target` is `GitHub Pages` for Repo A and `docs-site Directory in Repo` for Repo B.

## What It Checks, and What It Doesn't

Both scripts check as much as is feasible for them to automatically: they dispatch real pipelines and wait for them to finish, open real PRs and confirm they're blocked or pass, push real commits and confirm the release flow reacts correctly, and cut a real release and prerelease. Every check prints its own `[PASS]`/`[FAIL]` line as it runs, plus a summary at the end; nothing stops at the first failure, so one run gives the full picture.

What's still out of reach: anything that depends on a human's judgment (does a badge actually look right, was the setup checklist genuinely addressed) or an external system this script can't inspect (whether an Apprise notification actually landed at your configured endpoint, whether a third-party bot like Renovate or All Contributors responded). That's what the checklists are for; each one only lists what's actually left for a human, with a note wherever a check nearby is already automated.

## vs. `pytest tests/`

`pytest tests/` (`mise run test`; CI runs the same command directly on every PR) already covers a lot of this template's own correctness, including an update-path check (`test_update_from_last_tag`) that runs a real `copier update` against a real git history, but entirely locally: it renders into a temp directory, never touches GitHub or Azure DevOps, and skips every `_tasks` entry (`--skip-tasks`), so it can't create a repo, register a pipeline, or apply a branch policy for real. It's what catches broken Jinja, invalid YAML/JSON, dead links, and template-diff bugs, fast and on every PR, with no external side effects.

Integration testing picks up exactly where that stops: anything gated on a real API call, a real running pipeline, or an external system's own behavior; none of which a local render can exercise, which is why this has to be a manual, pre-release step rather than something CI runs on every PR.

Run through **all of** the relevant checklist, by hand, against the repos the integration test just created:

- [Manual Verification Checklist (GitHub)](manual-verification-github.md)
- [Manual Verification Checklist (Azure DevOps)](manual-verification-azdo.md)

Each checklist ends with its own cleanup steps for tearing the throwaway repos back down once you're done.

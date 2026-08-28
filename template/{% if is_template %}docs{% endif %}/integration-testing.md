# Integration Testing

**Run this as the last step before cutting every release.** It's the only way to catch a real regression in this template's own scaffolding -- a local render can't create a repo, register a pipeline, or trigger a workflow, and those are exactly the things a release needs to still work.

Integration testing means actually running the template: creating a real throwaway repo from the current template source and confirming the result holds up, not just inspecting a local render.

## Running It

- `mise run integration-test-gh` -- creates two real GitHub repos from this template: a fresh copy at `HEAD`, and a second copied at the last stable release tag then updated to `HEAD`, exercising the `copier update` path against a real repo.
- `mise run integration-test-azdo` -- the same shape, on Azure DevOps (pass `--org`/`--project`, or let them default to this project's own if it already uses Azure DevOps).

Run both, regardless of which platform this template's own repo happens to use -- a release has to be good for every platform this template supports, not just the one you personally host on.

## What It Checks, and What It Doesn't

Both scripts only check *structure*: that each repo, its pipelines/workflows, and its branch policy exist with the right names. They never trigger most of what they create, so they can't tell you whether a pipeline actually authenticates, opens a PR, blocks a bad merge, or publishes a release correctly -- and each run only ever exercises one fixed set of answers, so it can't cover every feature this template offers either.

That's what the checklists below are for. Run through **all of** the relevant one, by hand, against the repos the integration test just created:

- [Manual Verification Checklist (GitHub)](manual-verification-github.md)
- [Manual Verification Checklist (Azure DevOps)](manual-verification-azdo.md)

Each checklist ends with its own cleanup steps for tearing the throwaway repos back down once you're done.

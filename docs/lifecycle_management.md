# Lifecycle Management

This doc explains what the `lifecycle` question controls and how your project's status is
communicated as it changes over time.

## Choices

- **Pre-Alpha** / **Alpha** — The README displays a notice that the project is not ready for
  public use.
- **Beta** — The README displays a notice that the project should be used with caution.
- **Stable** — No notice is shown; the project is considered production-ready.
- **Inactive** — The README displays a notice that the project is no longer under active
  development.

Changing `lifecycle` via `copier update` updates this notice (or removes it, for Stable)
automatically.

## Moving to Stable for the First Time

While `lifecycle` is Pre-Alpha, Alpha, or Beta, Release Please keeps your version below `1.0.0`,
bumping the minor/patch component for `feat`/`fix` commits instead of the usual major/minor bump.
Release Please won't cross the `1.0.0` line on its own — that requires an explicit
`Release-As: 1.0.0` commit trailer.

To make this easy, once you set `lifecycle` to `Stable` on a GitHub project and run
`copier update`, if the version Release Please last tracked is still below `1.0.0`, you'll see a
message with a ready-to-run command:

```bash
git commit --allow-empty -m "chore: bump version to v1.0.0" -m "Release-As: 1.0.0"
```

Merge that commit to `main` and Release Please's next run will bump the version to `1.0.0`. The
message stops appearing automatically once that's done.

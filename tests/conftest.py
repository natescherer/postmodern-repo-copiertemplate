"""Shared fixtures and helpers for rendering this template against real Copier.

Generic by design: nothing here hardcodes this repo's specific doc set or question
values; see answer_matrix.py for the repo-specific piece, which a child template
should edit alongside its own copier.yml changes.
"""

import io
import os
import shutil

# S404: drives real CLI tools below; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import tarfile
from pathlib import Path

import jinja2
import pytest
from answer_matrix import ANSWER_MATRIX
from jinja2_ansible_filters import AnsibleCoreFiltersExtension


def _find_repo_root() -> Path:
    """Walk upward from this file to find the directory containing a template/ folder.

    A fixed parents[N] would be wrong in one context: as template source, this file is
    two levels below the repo root (template/{% if is_template %}tests{% endif %}/...),
    and rendered into a project, it's one level below (tests/...).

    Returns:
        The repo root directory.

    Raises:
        RuntimeError: if no parent directory contains a template/ folder.

    """
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "template").is_dir():
            return candidate
    raise RuntimeError(
        "Could not find repo root (no template/ folder found in any parent directory)"
    )


REPO_ROOT = _find_repo_root()

# copy-template-files leaves copier.yml.jinja out of a leaf template's template/,
# and the leaf's copier.yml makes every project Standard.
IS_LEAF = not (
    REPO_ROOT / "template" / "{% if is_template %}copier.yml{% endif %}.jinja"
).is_file()

# copy-template-files leaves paths carrying these gates out of a leaf template's
# template/, and folds the project-type gates out of the files it keeps.
TEMPLATE_ONLY_GATES = ("{% if is_template %}", "{% if is_extensible %}")
FOLD_SCRIPT = (
    REPO_ROOT
    / "template"
    / "{% if is_template %}scripts{% endif %}"
    / "{% if is_extensible %}fold_leaf_gates.py{% endif %}"
)

# The ANSWER_MATRIX entries this source can render: a leaf template renders only its
# Standard ones.
RENDERABLE_ANSWERS = [
    entry
    for entry in ANSWER_MATRIX
    if not (IS_LEAF and entry["project_type"] == "Template")
]


# Git can run maintenance in a detached background process after commands such as
# commit. One still writing into a temporary repo while Copier deletes it fails the
# update with "Directory not empty". Turning automatic maintenance off for every git
# these tests start, Copier's own calls included, rules that out.
_GIT_NO_BACKGROUND_MAINTENANCE = (("gc.auto", "0"), ("maintenance.auto", "false"))


def _subprocess_env() -> dict[str, str]:
    """Return os.environ plus git settings that disable background maintenance.

    Appends to any GIT_CONFIG_COUNT entries already set instead of replacing them.

    Returns:
        A copy of the environment for subprocess.run.

    """
    env = dict(os.environ)
    count = int(env.get("GIT_CONFIG_COUNT") or 0)
    for key, value in _GIT_NO_BACKGROUND_MAINTENANCE:
        env[f"GIT_CONFIG_KEY_{count}"] = key
        env[f"GIT_CONFIG_VALUE_{count}"] = value
        count += 1
    env["GIT_CONFIG_COUNT"] = str(count)
    return env


def _run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run subprocess.run with output always captured as UTF-8 text.

    Windows' default console encoding (cp1252) can't decode tool output containing
    e.g. emoji or box-drawing characters (lychee's summary, for one); that mismatch
    crashes the background reader thread and leaves stdout/stderr as None instead of
    raising cleanly.

    Returns:
        The completed subprocess, with UTF-8-decoded stdout/stderr.

    """
    # S603: args are always a fixed list built by this module; no shell=True.
    return subprocess.run(  # noqa: S603
        args,
        cwd=cwd,
        env=_subprocess_env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    result = _run(["git", *args], cwd=cwd)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"git {' '.join(args)} failed:\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    return result


def _git_init_repo(path: Path) -> None:
    """Init a throwaway git repo at `path` with a fixed local identity.

    Needed because `copier update` requires both the source and the destination to be
    git repositories; it records `_commit` from the source at copy time and uses git
    to detect local destination changes when applying an update.
    """
    path.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q"], path)
    _git(["config", "user.email", "template-tests@example.invalid"], path)
    _git(["config", "user.name", "Template Tests"], path)


def _git_commit_all(path: Path, message: str) -> None:
    _git(["add", "-A"], path)
    _git(["commit", "-q", "-m", message], path)


def _ignore_for_copy(directory, names):
    skip = {
        ".git",
        ".cache",
        ".venv",
        "__pycache__",
        "docs-site",
        ".ruff_cache",
        ".rumdl_cache",
    }
    return [n for n in names if n in skip]


def _assemble_source(repo_root: Path, dest: Path) -> None:
    """Build a copier source rooted at `dest` from the current `template/` contents.

    It doesn't copy this repo's root copier.yml: that's dogfooded output, refreshed only
    by a `copier update`, so it lags behind the uncommitted and just-committed edits
    under template/ that this suite exists to check. When template/ has a self-hosting
    conditional copier.yml (as a template that generates child templates does), its
    non-raw header renders with stub values, which no test inspects, and its `{% raw
    %}...{% endraw %}` body, the real question set, passes through unchanged, as Copier
    renders it into a child's copier.yml.
    """
    shutil.copytree(
        repo_root / "template",
        dest / "template",
        dirs_exist_ok=True,
        ignore=_ignore_for_copy,
    )

    conditional_copier_yml = (
        repo_root / "template" / "{% if is_template %}copier.yml{% endif %}.jinja"
    )
    if conditional_copier_yml.is_file():
        # S701: renders YAML, never HTML, so there's no XSS surface for autoescape.
        env = jinja2.Environment(extensions=[AnsibleCoreFiltersExtension])  # noqa: S701
        rendered = env.from_string(
            conditional_copier_yml.read_text(encoding="utf-8")
        ).render(
            project_name="Test Parent Template",
            using_github=True,
            using_azdo=False,
            github_repo_owner="test-owner",
            azdo_org="",
            azdo_project_encoded="",
            repo_name="test-parent-template",
            # The test source is an extensible template, so it asks project_type.
            is_extensible=True,
        )
        (dest / "copier.yml").write_text(rendered, encoding="utf-8")
    else:
        shutil.copy2(repo_root / "copier.yml", dest / "copier.yml")


def _latest_tag(repo_root: Path) -> str | None:
    """Return this repo's most recent git tag by version sort.

    Returns:
        The latest tag name, or None if the repo has no tags yet (e.g. a brand-new
        template before its first release).

    """
    result = _run(["git", "tag", "--sort=-v:refname"], cwd=repo_root)
    tags = [line for line in result.stdout.splitlines() if line.strip()]
    return tags[0] if tags else None


UPDATE_SOURCE_ROOT_FILES = (
    "knope.toml",
    "mise.toml",
    ".config/knope-current-version.json",
)


def _assemble_update_scratch_repo(repo_root: Path, old_tag: str, dest: Path) -> None:
    """Build a 2-commit copier source for testing the update path: old_tag -> current.

    Commit 1 is `repo_root` as it was at `old_tag`, its released root copier.yml
    included: the source a real user updating from that release had. Commit 2 (HEAD) is
    the current template/, assembled the way _assemble_source() does it, so uncommitted
    edits are covered too.

    Both states have to live at one path, in two commits: `copier update` reads
    `_src_path` from the destination's answers file and resolves that same path, so it
    can't be pointed at a different source for the new version.
    """
    _git_init_repo(dest)

    # S603, S607: fixed args, no shell=True, resolved from PATH like every other tool
    # invocation in this file (actionlint, tombi, zensical, lychee).
    archive = subprocess.run(  # noqa: S603
        ["git", "archive", old_tag],  # noqa: S607
        cwd=repo_root,
        capture_output=True,
    )
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert archive.returncode == 0, f"git archive {old_tag} failed: {archive.stderr!r}"  # noqa: S101
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        tar.extractall(dest, filter="data")  # trusted content: this repo's own history
    _git_commit_all(dest, old_tag)
    _git(["tag", old_tag], dest)

    for child in dest.iterdir():
        if child.name == ".git":
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    _assemble_source(repo_root, dest)
    # The changeset migration clones the source and runs `knope compute-upstream-bump`
    # at its root, the way a real one (this repo) has these files. The `feat:` subject
    # gives Knope something release-worthy, so the migration writes a changeset.
    for rel in UPDATE_SOURCE_ROOT_FILES:
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo_root / rel, dest / rel)
    _git_commit_all(dest, "feat: current template")


@pytest.fixture(scope="session")
def template_source(tmp_path_factory):
    """Build a self-contained copier source fresh from the current template/ tree.

    Returns:
        Path to the fixture-scoped copier source directory.

    """
    src = tmp_path_factory.mktemp("template-source")
    _assemble_source(REPO_ROOT, src)
    return src


@pytest.fixture(scope="session")
def update_source(tmp_path_factory):
    """Build a 2-commit copier source (last tag -> current) for update-path testing.

    Skips dependent tests if this repo has no git tags yet.

    Returns:
        A (source_path, old_tag) tuple.

    """
    old_tag = _latest_tag(REPO_ROOT)
    if old_tag is None:
        pytest.skip("No git tags found; nothing to update from yet.")
    src = tmp_path_factory.mktemp("update-source")
    _assemble_update_scratch_repo(REPO_ROOT, old_tag, src)
    return src, old_tag


def _leaf_template(template_dir: Path, dest: Path) -> None:
    """Copy `template_dir` to `dest` the way copy-template-files does for a leaf."""
    shutil.copytree(
        template_dir,
        dest,
        ignore=lambda _directory, names: [
            name for name in names if any(gate in name for gate in TEMPLATE_ONLY_GATES)
        ],
    )
    result = _run([sys.executable, str(FOLD_SCRIPT), str(dest)])
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, result.stderr  # noqa: S101


def _render(source: Path, dest: Path, answers: dict, vcs_ref: str | None = None):
    args = ["copier", "copy", "--trust", "--defaults", "--skip-tasks"]
    if vcs_ref is not None:
        args.append(f"--vcs-ref={vcs_ref}")
    for key, value in answers.items():
        if key in ("id", "_old_tag_overrides"):
            continue
        args.extend(["-d", f"{key}={value}"])
    args.extend([str(source), str(dest)])
    result = _run(args)
    # S101: `assert` is the normal, expected way to fail a pytest test.
    assert result.returncode == 0, (  # noqa: S101
        f"copier copy failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

import json
import os
import shutil
import subprocess


class color:
    PURPLE = "\033[1;35;48m"
    CYAN = "\033[1;36;48m"
    BOLD = "\033[1;37;48m"
    BLUE = "\033[1;34;48m"
    GREEN = "\033[1;32;48m"
    YELLOW = "\033[1;33;48m"
    RED = "\033[1;31;48m"
    BLACK = "\033[1;30;48m"
    UNDERLINE = "\033[4;37;48m"
    END = "\033[1;37;0m"


print(color.GREEN + "*** PRE-GEN PROJECT HOOK START ***" + color.END)

print(color.CYAN + "Verifying GitHub CLI is installed..." + color.END)
if not shutil.which("gh"):
    raise FileNotFoundError("GitHub CLI is required and is not installed!")

print(color.CYAN + "Verifying you are logged in to GitHub CLI..." + color.END)
try:
    subprocess.run(["gh", "auth", "status"], capture_output=True, check=True)
except subprocess.CalledProcessError as exc:
    raise Exception("You are not logged into gh cli, run gh auth login") from exc

if "{{cookiecutter.new_project}}" == "Yes":
    print(color.CYAN + "Creating & Cloning GitHub repo..." + color.END)
    gh_repo_create = subprocess.run(
        ["gh", "repo", "create", "{{cookiecutter.repo_name}}", "--public", "--clone"],
        capture_output=True,
        check=True,
        cwd="..",
    )

print(color.CYAN + "Setting GitHub repo settings..." + color.END)
repo_settings = {
    "description": "{{cookiecutter.short_description}}",
    "homepage": "{{cookiecutter.project_website}}",
    "allow_auto_merge": True,
    "delete_branch_on_merge": True,
}
gh_api_repos = subprocess.run(
    [
        "gh",
        "api",
        "/repos/{owner}/{repo}",
        "--method",
        "PATCH",
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        "X-GitHub-Api-Version: 2022-11-28",
        "--input",
        "-",
    ],
    capture_output=True,
    check=True,
    input=json.dumps(repo_settings).encode(),
)

print(color.CYAN + "Adding GitHub Labels..." + color.END)
gh_label_create_awaiting_pr = subprocess.run(
    [
        "gh",
        "label",
        "create",
        "awaiting pr",
        "-d",
        "Awaiting completion of a PR from a contributor",
        "-c",
        "668F04",
        "-f",
    ],
    capture_output=True,
    check=True,
)
gh_label_create_awaiting_pr = subprocess.run(
    [
        "gh",
        "label",
        "create",
        "blocked",
        "-d",
        "Blocked by an external dependency",
        "-c",
        "B60205",
        "-f",
    ],
    capture_output=True,
    check=True,
)

print(color.CYAN + "Setting GitHub branch protection ruleset..." + color.END)
repo_ruleset = {
    "name": "default-branch-protection",
    "enforcement": "active",
    "target": "branch",
    "bypass_actors": [],
    "conditions": {"ref_name": {"exclude": [], "include": ["~DEFAULT_BRANCH"]}},
    "rules": [
        {"type": "deletion"},
        {"type": "non_fast_forward"},
        {
            "type": "pull_request",
            "dismiss_stale_reviews_on_push": False,
            "require_code_owner_review": False,
            "require_last_push_approval": False,
            "required_approving_review_count": 0,
            "required_review_thread_resolution": False,
        },
    ],
}
gh_api_repos_rulesets = subprocess.run(
    [
        "gh",
        "api",
        "/repos/{owner}/{repo}/rulesets",
        "--method",
        "POST",
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        "X-GitHub-Api-Version: 2022-11-28",
        "--input",
        "-",
    ],
    capture_output=True,
    check=True,
    input=json.dumps(repo_ruleset).encode(),
)

# Choose correct files based on project type
PROJECT = "{{cookiecutter.project_type}}"
if PROJECT == "Cookiecutter":
    print(color.CYAN + "Duplicating files for cookiecutter project type..." + color.END)
    os.mkdir("cookiecutter")
    os.mkdir("cookiecutter/.github")
    os.mkdir("cookiecutter/.github/workflows")
    os.mkdir("cookiecutter/docs")
    CC_FILES = [
        ".github/workflows/AllContributorsAutomation.yml",
        ".github/workflows/BotAutoMerge.yml",
        ".github/workflows/Release-cookiecutter.yml",
        ".github/dependabot.yml",
        "docs/cookiecutter_defaults.md",
        "docs/installing_pipx.md",
        "docs/installing_python.md",
        ".all-contributorsrc",
        ".gitattributes",
        ".gitignore",
        "CHANGELOG.md",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "cookiecutter.json",
        "GitVersion.yml",
        "LICENSE",
    ]
    for path in CC_FILES:
        shutil.copy2(path, "cookiecutter")

print(color.GREEN + "*** PRE-GEN PROJECT HOOK END ***" + color.END)

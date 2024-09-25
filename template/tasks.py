"""Postmodern template tasks.

This file is to be executed with https://www.pyinvoke.org/ in Python 3.6+.
"""

import json
import os
import shutil
import tempfile

import copier.vcs
import githubkit
import requests
from invoke import task
from rich import print


@task
def copy_template_files(c, answers_json):
    """Pull down an additional copy of template files."""
    print("[bold green]*** 'copy-template-files' task start ***[/bold green]")
    answers = json.loads(answers_json)
    source = answers["_src_path"]
    ref = answers["_commit"]
    source_url = copier.vcs.get_repo(source)

    with tempfile.TemporaryDirectory() as tmpdir:
        if ref != "HEAD" and ref is not None:
            c.run(
                f"cd {tmpdir}; git -c advice.detachedHead=false clone -q --depth 1 --branch {ref} {source_url} ."
            )
        else:
            c.run(
                f"cd {tmpdir}; git -c advice.detachedHead=false clone -q --depth 1 {source_url} ."
            )
        shutil.copytree(f"{tmpdir}/template", "template", dirs_exist_ok=True)
    print("[bold green]*** 'copy-template-files' task end ***[/bold green]")


@task
def create_repo_github(c, answers_json):
    """Create a GitHub repo."""
    print("[bold green]*** 'create-repo-github' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    repo_data = {
        "name": answers["repo_name"],
        "description": answers["project_short_description"],
        "homepage": answers["project_website"],
        "private": True if answers["project_visibility"] == "Private" else False,
    }
    if answers["github_org"]:
        print("[cyan]Creating repo in GitHub organization...[/cyan]")
        github.rest.repos.create_in_org(answers["github_org"], data=repo_data)
    else:
        repo_data.update({"allow_auto_merge": True, "delete_branch_on_merge": True})
        print("[cyan]Creating repo in GitHub user account...[/cyan]")
        github.rest.repos.create_for_authenticated_user(data=repo_data)
    print("[bold green]*** 'create-repo-github' task end ***[/bold green]")


@task
def create_repo_azdo(c, answers_json):
    """Create an Azure DevOps repo."""
    print("[bold green]*** 'create-repo-azdo' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    repo_data = {"name": answers["repo_name"]}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    encoded_project = answers["azdo_project"].replace(" ", "%20")
    print("[cyan]Creating repo in Azure DevOps...[/cyan]")
    response = requests.post(
        f"https://dev.azure.com/{answers['azdo_org']}/{encoded_project}/_apis/git/repositories?api-version=7.2-preview.1",
        data=json.dumps(repo_data),
        auth=("", token),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    print("[bold green]*** 'create-repo-azdo' task end ***[/bold green]")


@task
def set_repo_settings_github(c, answers_json):
    """Set settings on a GitHub repo."""
    print("[bold green]*** 'set-repo-settings-github' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]
    owner = answers.get("github_org") or answers.get("github_username")

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))

    # Auto-merge and delete branch on merge
    if not answers["github_org"]:
        repo_data = {"allow_auto_merge": True, "delete_branch_on_merge": True}
        github.rest.repos.update(owner=owner, repo=answers["repo_name"], data=repo_data)

    # Labels
    current_label_content = github.rest.issues.list_labels_for_repo(
        owner=owner, repo=answers["repo_name"]
    )
    current_labels = [x.name for x in current_label_content.parsed_data]

    if "awaiting pr" not in current_labels:
        awaiting_pr_label_data = {
            "name": "awaiting pr",
            "color": "668F04",
            "description": "Awaiting completion of a PR from a contributor",
        }
        print("[cyan]Creating 'awaiting pr' label...[/cyan]")
        github.rest.issues.create_label(
            owner=owner, repo=answers["repo_name"], data=awaiting_pr_label_data
        )
    else:
        print("[yellow]Label 'awaiting pr' already exists, skipping creation.[/yellow]")
    if "blocked" not in current_labels:
        blocked_label_data = {
            "name": "blocked",
            "color": "B60205",
            "description": "Blocked by an external dependency",
        }
        print("[cyan]Creating 'blocked' label...[/cyan]")
        github.rest.issues.create_label(
            owner=owner, repo=answers["repo_name"], data=blocked_label_data
        )
    else:
        print("[yellow]Label 'blocked' already exists, skipping creation.[/yellow]")

    # Workflow Permissions
    workflow_perm_data = {"can_approve_pull_request_reviews": True}
    print("[cyan]Setting Actions workflow settings...[/cyan]")
    github.rest.actions.set_github_actions_default_workflow_permissions_repository(
        owner=owner, repo=answers["repo_name"], data=workflow_perm_data
    )
    print("[bold green]*** 'set-repo-settings-github' task end ***[/bold green]")


@task
def set_branch_protection_ruleset_github(c, answers_json):
    """Set branch protection ruleset on a GitHub repo."""
    print(
        "[bold green]*** 'set-branch-protection-ruleset-github' task start ***[/bold green]"
    )
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]
    owner = answers.get("github_org") or answers.get("github_username")

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    rulesets_content = github.rest.repos.get_repo_rulesets(
        owner=owner, repo=answers["repo_name"]
    )
    rulesets = [x.name for x in rulesets_content.parsed_data]
    if "default-branch-protection" not in rulesets:
        ruleset_data = {
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
                    "parameters": {
                        "dismiss_stale_reviews_on_push": False,
                        "require_code_owner_review": False,
                        "require_last_push_approval": False,
                        "required_approving_review_count": 0,
                        "required_review_thread_resolution": False,
                    },
                },
            ],
        }
        print("[cyan]Creating branch protection ruleset...[/cyan]")
        github.rest.repos.create_repo_ruleset(
            owner=owner, repo=answers["repo_name"], data=ruleset_data
        )
    else:
        print(
            "[yellow]Repo ruleset 'default-branch-protection' already exists, skipping creation. Please verify this ruleset was made by this template or GitHub Actions workflows might not work correctly![/yellow]"
        )
    print(
        "[bold green]*** 'set-branch-protection-ruleset-github' task end ***[/bold green]"
    )


@task
def initialize_repo_and_commit_files(c, answers_json):
    """Create an initial branch and commit files."""
    print(
        "[bold green]*** 'initialize-repo-and-commit-files' task start ***[/bold green]"
    )
    answers = json.loads(answers_json)
    owner = answers.get("github_org") or answers.get("github_username")
    if answers["lifecycle"] in ["Pre-Alpha", "Alpha", "Beta"]:
        first_version = "0.1.0"
    else:
        first_version = "1.0.0"

    print("[cyan]Initializing git repo with 'main' branch...[/cyan]")
    c.run("git init -b main")
    print("[cyan]Adding files to commit...[/cyan]")
    c.run("git add --all -- ':!tasks.py' ':!token.json' ':!template_copy.tar.gz'")
    print("[cyan]Committing...[/cyan]")
    commit_message = "git commit -m 'feat: initialize project'"
    if answers["developer_platform"] == "GitHub":
        commit_message += f" -m 'Release-As: {first_version}'"
    c.run(commit_message)
    if answers["developer_platform"] == "GitHub":
        remote_url = f"https://github.com/{owner}/{answers['repo_name']}.git"
    elif answers["developer_platform"] == "Azure DevOps":
        encoded_project = answers["azdo_project"].replace(" ", "%20")
        remote_url = f"https://{answers['azdo_org']}@dev.azure.com/{answers['azdo_org']}/{encoded_project}/_git/{answers['repo_name']}"
        print("[cyan]Setting 'git config credential.useHttpPath true'...[/cyan]")
        c.run("git config credential.useHttpPath true")
    print(f"[cyan]Adding remote {remote_url}...[/cyan]")
    c.run(f"git remote add origin {remote_url}")
    print("[cyan]Pushing to remote...[/cyan]")
    c.run("git push -u origin --all")
    print(
        "[bold green]*** 'initialize-repo-and-commit-files' task end ***[/bold green]"
    )


@task
def create_pipelines_azdo(c, answers_json):
    """Register pipeline for an Azure DevOps repo."""
    print("[bold green]*** 'create-pipelines-azdo' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    pipeline_data = {
        "name": answers["repo_name"],
        "repository": {"name": answers["repo_name"], "type": "TfsGit"},
        "process": {"yamlFilename": ".azurepipelines/azure-pipelines.yml", "type": 2},
        "path": "\\",
        "queue": {"name": "Azure Pipelines"},
        "triggers": [{"settingsSourceType": 2, "triggerType": "continuousIntegration"}],
        "type": "build",
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    encoded_project = answers["azdo_project"].replace(" ", "%20")
    print("[cyan]Creating pipeline in Azure DevOps...[/cyan]")
    response = requests.post(
        f"https://dev.azure.com/{answers['azdo_org']}/{encoded_project}/_apis/build/definitions?api-version=7.1-preview.7",
        data=json.dumps(pipeline_data),
        auth=("", token),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    print("[bold green]*** 'create-pipelines-azdo' task end ***[/bold green]")


@task
def delete_unneeded_template_files(c):
    """Delete files used only in the template build process, including this tasks.py file."""
    print(
        "[bold green]*** 'delete-unneeded-template-files' task start ***[/bold green]"
    )
    os.remove("token.json")
    os.remove(__file__)
    print("[bold green]*** 'delete-unneeded-template-files' task end ***[/bold green]")

"""Postmodern template tasks.

This file is to be executed with https://www.pyinvoke.org/ in Python 3.6+.
"""
import json
import os
import shutil
import urllib.parse
import githubkit
from azure.devops.connection import Connection
from azure.devops.exceptions import AzureDevOpsServiceError
from msrest.authentication import BasicAuthentication
from invoke import task
from rich import print

@task
def unpack_and_delete_template_zip(c):
    """For project_type == 'Template', unpack and delete template/clean_template.zip"""
    print("[bold green]*** 'unpack_and_delete_template_zip' task start ***[/bold green]")
    shutil.unpack_archive("template_copy.zip", ".")
    print("[bold green]*** 'unpack_and_delete_template_zip' task end ***[/bold green]")

@task
def repo_create_github(c, answers_json):
    """Create a GitHub repo"""
    print("[bold green]*** 'repo-create-github' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    repo_data = {
        "name": answers["repo_name"],
        "description": answers["project_short_description"],
        "homepage": answers["project_website"],
        "private": True if answers["project_visibility"] == "private" else False
    }
    if answers["github_org"]:
        print("[cyan]Creating repo in GitHub organization...[/cyan]")
        github.rest.repos.create_in_org(answers["github_org"],data=repo_data)
    else:
        repo_data.update(
            {
                "allow_auto_merge": True,
                "delete_branch_on_merge": True
            }
        )
        print("[cyan]Creating repo in GitHub user account...[/cyan]")
        github.rest.repos.create_for_authenticated_user(data=repo_data)
    print("[bold green]*** 'repo-create-github' task end ***[/bold green]")

@task
def repo_create_azdo(c, answers_json):
    """Create an Azure DevOps repo"""
    print("[bold green]*** 'repo-create-azdo' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to Azure DevOps...[/cyan]")
    credentials = BasicAuthentication('', token)
    connection = Connection(base_url=f"https://dev.azure.com/{answers['azdo_org']}", creds=credentials)
    git_client = connection.clients_v5_1.get_git_client()
    repo_data = {
        "name": answers["repo_name"],
    }
    print("[cyan]Creating repo in Azure DevOps...[/cyan]")
    git_client.create_repository(repo_data, project=answers["azdo_project"])
    print("[bold green]*** 'repo-create-github' task end ***[/bold green]")

@task
def repo_settings_github(c, answers_json):
    """Set settings on a GitHub repo"""
    print("[bold green]*** 'repo-settings-github' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]
    owner = answers.get("github_org") or answers.get("github_username")

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))

    # Auto-merge and delete branch on merge
    if not answers["github_org"]:
        repo_data = {
            "allow_auto_merge": True,
            "delete_branch_on_merge": True
        }
        github.rest.repos.update(owner=owner, repo=answers["repo_name"], data=repo_data)

    # Labels
    current_label_content = github.rest.issues.list_labels_for_repo(owner=owner, repo=answers["repo_name"])
    current_labels = [x.name for x in current_label_content.parsed_data]

    if "awaiting pr" not in current_labels: 
        awaiting_pr_label_data = {
            "name": "awaiting pr",
            "color": "668F04",
            "description": "Awaiting completion of a PR from a contributor"
        }
        print("[cyan]Creating 'awaiting pr' label...[/cyan]")
        github.rest.issues.create_label(owner=owner, repo=answers["repo_name"], data=awaiting_pr_label_data)
    else:
        print("[yellow]Label 'awaiting pr' already exists, skipping creation.[/yellow]")
    if "blocked" not in current_labels:
        blocked_label_data = {
            "name": "blocked",
            "color": "B60205",
            "description": "Blocked by an external dependency"
        }
        print("[cyan]Creating 'blocked' label...[/cyan]")
        github.rest.issues.create_label(owner=owner, repo=answers["repo_name"], data=blocked_label_data)
    else:
        print("[yellow]Label 'blocked' already exists, skipping creation.[/yellow]")

    # Workflow Permissions
    workflow_perm_data = {
        "can_approve_pull_request_reviews": True
    }
    print("[cyan]Setting Actions workflow settings...[/cyan]")
    github.rest.actions.set_github_actions_default_workflow_permissions_repository(owner=owner, repo=answers["repo_name"], data=workflow_perm_data)
    print("[bold green]*** 'repo-settings-github' task end ***[/bold green]")

@task
def branch_protection_ruleset_github(c, answers_json):
    """Set branch protection ruleset on a GitHub repo"""
    print("[bold green]*** 'branch_protection_ruleset_github' task start ***[/bold green]")
    answers = json.loads(answers_json)
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]
    owner = answers.get("github_org") or answers.get("github_username")

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    rulesets_content = github.rest.repos.get_repo_rulesets(owner=owner, repo=answers["repo_name"])
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
                    "dismiss_stale_reviews_on_push": False,
                    "require_code_owner_review": False,
                    "require_last_push_approval": False,
                    "required_approving_review_count": 0,
                    "required_review_thread_resolution": False
                },
                {
                "type": "required_status_checks",
                    "parameters": {
                        "strict_required_status_checks_policy": False,
                        "required_status_checks": [
                            {
                                "context": "status_checks_pr"
                            }
                        ]
                    }
                }
            ]
        }
        print("[cyan]Creating branch protection ruleset...[/cyan]")
        github.rest.repos.create_repo_ruleset(owner=owner, repo=answers["repo_name"], data=ruleset_data)
    else:
        print("[yellow]Repo ruleset 'default-branch-protection' already exists, skipping creation. Please verify this ruleset was made by this template or GitHub Actions workflows might not work correctly![/yellow]")
    print("[bold green]*** 'branch_protection_ruleset_github' task end ***[/bold green]")

@task
def initialize_and_commit(c, answers_json):
    """Create an initial branch and commit files"""
    print("[bold green]*** 'initialize_and_commit' task start ***[/bold green]")
    answers = json.loads(answers_json)
    owner = answers.get("github_org") or answers.get("github_username")

    print("[cyan]Initializing git repo with 'main' branch...[/cyan]")
    c.run("git init -b main")
    print("[cyan]Adding files to commit...[/cyan]")
    c.run("git add --all -- ':!tasks.py' ':!token.json' ':!template_copy.zip'")
    print("[cyan]Committing...[/cyan]")
    c.run("git commit -m 'feat: initialize project'")
    if answers["developer_platform"] == "GitHub":
        remote_url = f"https://github.com/{owner}/{answers['repo_name']}.git"
    elif answers["developer_platform"] == "Azure DevOps":
        encoded_project = urllib.parse.quote_plus(answers["azdo_project"])
        remote_url = f"https://{answers['azdo_org']}@dev.azure.com/{answers['azdo_org']}/{encoded_project}/_git/{answers['repo_name']}"
        print(f"[cyan]Setting 'git config credential.useHttpPath true'...[/cyan]")
        c.run("git config credential.useHttpPath true")
    print(f"[cyan]Adding remote {remote_url}...[/cyan]")
    c.run(f"git remote add origin {remote_url}")
    print("[cyan]Pushing to remote...[/cyan]")
    c.run(f"git push -u origin --all")
    print("[bold green]*** 'initialize_and_commit' task end ***[/bold green]")

@task
def delete_files(c):
    """Delete files used only in the template build process, including this tasks.py file"""
    print("[bold green]*** 'delete_files' task start ***[/bold green]")
    os.remove("template_copy.zip")
    os.remove("token.json")
    os.remove(__file__)
    print("[bold green]*** 'delete_files' task end ***[/bold green]")

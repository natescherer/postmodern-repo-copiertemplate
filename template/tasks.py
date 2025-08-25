"""Postmodern template tasks.

This file is to be executed with https://www.pyinvoke.org/ in Python 3.6+.
"""

import json
import os
import shutil
import tempfile
import time
from pathlib import Path

import githubkit
import requests
from invoke import task
from rich import print


@task(optional=["vcs_ref"])
def copy_template_files(c, src_path, vcs_ref=None):
    """Pull down an additional copy of template files."""
    print("[bold green]*** 'copy-template-files' task start ***[/bold green]")

    with tempfile.TemporaryDirectory() as tmpdir:
        if vcs_ref != "HEAD" and vcs_ref is not None:
            time.sleep(5)
            c.run(
                f"git -c advice.detachedHead=false clone --quiet "
                f"--branch {vcs_ref} {src_path} {tmpdir}"
            )
        else:
            c.run(f"git -c advice.detachedHead=false clone --quiet {src_path} {tmpdir}")
        shutil.copytree(f"{tmpdir}/template", "template", dirs_exist_ok=True)
    print("[bold green]*** 'copy-template-files' task end ***[/bold green]")


@task(optional=["github_org"])
def create_repo_github(
    c, repo_name, github_repo_description, github_repo_owner, is_public, github_org=None
):
    """Create a GitHub repo."""
    print("[bold green]*** 'create-repo-github' task start ***[/bold green]")
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    repo_data = {
        "name": repo_name,
        "description": github_repo_description,
        "homepage": f"https://{github_repo_owner}.github.io/{repo_name}"
        if is_public
        else "",
        "private": True if not is_public else False,
    }
    if github_org:
        print("[cyan]Creating repo in GitHub organization...[/cyan]")
        github.rest.repos.create_in_org(github_org, data=repo_data)
    else:
        repo_data.update({"allow_auto_merge": True, "delete_branch_on_merge": True})
        print("[cyan]Creating repo in GitHub user account...[/cyan]")
        github.rest.repos.create_for_authenticated_user(data=repo_data)
    print("[bold green]*** 'create-repo-github' task end ***[/bold green]")


@task
def create_repo_azdo(c, repo_name, azdo_project, azdo_org):
    """Create an Azure DevOps repo."""
    print("[bold green]*** 'create-repo-azdo' task start ***[/bold green]")
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    repo_data = {"name": repo_name}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    encoded_project = azdo_project.replace(" ", "%20")
    print("[cyan]Creating repo in Azure DevOps...[/cyan]")
    response = requests.post(
        f"https://dev.azure.com/{azdo_org}/{encoded_project}/_apis/git/repositories?api-version=7.2-preview.1",
        data=json.dumps(repo_data),
        auth=("", token),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    print("[bold green]*** 'create-repo-azdo' task end ***[/bold green]")


@task(optional=["github_org"])
def set_repo_settings_github(
    c, github_repo_owner, repo_name, is_public, github_org=None
):
    """Set settings on a GitHub repo."""
    print("[bold green]*** 'set-repo-settings-github' task start ***[/bold green]")
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))

    # Auto-merge and delete branch on merge
    if not github_org:
        repo_data = {"allow_auto_merge": True, "delete_branch_on_merge": True}
        github.rest.repos.update(
            owner=github_repo_owner, repo=repo_name, data=repo_data
        )

    # Labels
    current_label_content = github.rest.issues.list_labels_for_repo(
        owner=github_repo_owner, repo=repo_name
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
            owner=github_repo_owner, repo=repo_name, data=awaiting_pr_label_data
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
            owner=github_repo_owner, repo=repo_name, data=blocked_label_data
        )
    else:
        print("[yellow]Label 'blocked' already exists, skipping creation.[/yellow]")

    # Workflow Permissions
    workflow_perm_data = {"can_approve_pull_request_reviews": True}
    print("[cyan]Setting Actions workflow settings...[/cyan]")
    github.rest.actions.set_github_actions_default_workflow_permissions_repository(
        owner=github_repo_owner, repo=repo_name, data=workflow_perm_data
    )

    print("[bold green]*** 'set-repo-settings-github' task end ***[/bold green]")


@task
def set_branch_protection_ruleset_github(c, github_repo_owner, repo_name):
    """Set branch protection ruleset on a GitHub repo."""
    print(
        "[bold green]"
        "*** 'set-branch-protection-ruleset-github' task start ***"
        "[/bold green]"
    )
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    rulesets_content = github.rest.repos.get_repo_rulesets(
        owner=github_repo_owner, repo=repo_name
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
            owner=github_repo_owner, repo=repo_name, data=ruleset_data
        )
    else:
        print(
            "[yellow]Repo ruleset 'default-branch-protection' already exists, "
            "skipping creation. Please verify this ruleset was made by this "
            "template or GitHub Actions workflows might not work correctly![/yellow]"
        )
    print(
        "[bold green]"
        "*** 'set-branch-protection-ruleset-github' task end ***"
        "[/bold green]"
    )


@task(optional=["github_username", "github_repo_owner", "azdo_org", "azdo_project"])
def initialize_repo_and_commit_files(
    c,
    lifecycle,
    developer_platform,
    repo_name,
    github_username=None,
    github_repo_owner=None,
    azdo_org=None,
    azdo_project=None,
):
    """Create an initial branch and commit files."""
    print(
        "[bold green]*** 'initialize-repo-and-commit-files' task start ***[/bold green]"
    )
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]
    if lifecycle in ["Pre-Alpha", "Alpha", "Beta"]:
        first_version = "0.1.0"
    else:
        first_version = "1.0.0"

    print("[cyan]Initializing git repo with 'main' branch...[/cyan]")
    c.run("git init -b main")
    print("[cyan]Adding files to commit...[/cyan]")
    c.run('git add --all -- ":!tasks.py" ":!token.json" ":!mise.init.toml"')
    print("[cyan]Committing...[/cyan]")
    commit_cmd = 'git commit -m "feat: initialize project"'
    if developer_platform == "GitHub":
        commit_cmd += f' -m "Release-As: {first_version}"'
    c.run(commit_cmd)
    print("[cyan]Adding remote...[/cyan]")
    if developer_platform == "GitHub":
        remote_url = f"https://github.com/{github_repo_owner}/{repo_name}.git"
        gcm_dir = f"{str(Path.home())}/.gcm/store/git/https/github.com"
        gcm_file = f"{github_username}.credential"
        gcm_service = "https://github.com"
        gcm_account = github_username
    elif developer_platform == "Azure DevOps":
        encoded_project = azdo_project.replace(" ", "%20")
        remote_url = f"https://{azdo_org}@dev.azure.com/{azdo_org}/{encoded_project}/_git/{repo_name}"
        gcm_dir = f"{str(Path.home())}/.gcm/store/git/https/dev.azure.com/{azdo_org}"
        gcm_file = "copier.credential"
        gcm_service = f"https://dev.azure.com/{azdo_org}"
        gcm_account = "copier"
        print("[cyan]Temporarily setting git config options for AzDO...[/cyan]")
        c.run("git config credential.useHttpPath true")
    c.run(f"git remote add origin {remote_url}")
    print("[cyan]Setting up Git credentials...[/cyan]")
    print(
        "[cyan]Temporarily enabling plaintext git credentials for first push...[/cyan]"
    )
    c.run("git config credential.credentialStore plaintext")
    print(
        "[cyan]Creating credentials file that will be cleaned up after push...[/cyan]"
    )
    Path(gcm_dir).mkdir(parents=True, exist_ok=True)
    with open(f"{gcm_dir}/{gcm_file}", "w+") as cred_file:
        cred_file.writelines(
            [f"{token}\n", f"service={gcm_service}\n", f"account={gcm_account}"]
        )
    print("[cyan]Pushing to remote...[/cyan]")
    c.run("git push -u origin --all")
    if developer_platform == "Azure DevOps":
        print("[cyan]Unsetting git config options for AzDO...[/cyan]")
        c.run("git config --unset credential.useHttpPath")
    print("[cyan]Disabling plaintext git credentials...[/cyan]")
    c.run("git config --unset credential.credentialStore")
    print("[cyan]Deleting credentials file...[/cyan]")
    os.remove(f"{gcm_dir}/{gcm_file}")
    print(
        "[bold green]*** 'initialize-repo-and-commit-files' task end ***[/bold green]"
    )


@task
def create_pipelines_azdo(c, repo_name, azdo_project, azdo_org):
    """Register pipelines for an Azure DevOps repo."""
    print("[bold green]*** 'create-pipelines-azdo' task start ***[/bold green]")
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    for entry in os.scandir(".azurepipelines"):
        if entry.name.endswith(".yml") and not entry.name.startswith("template-"):
            pipeline_data = {
                "name": f"[{repo_name}] {Path(entry.name).with_suffix('')}",
                "repository": {
                    "name": repo_name,
                    "type": "TfsGit",
                },
                "process": {"yamlFilename": f".azurepipelines/{entry.name}", "type": 2},
                "path": "\\",
                "queue": {"name": "Azure Pipelines"},
                "triggers": [
                    {"settingsSourceType": 2, "triggerType": "continuousIntegration"}
                ],
                "type": "build",
            }
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            encoded_project = azdo_project.replace(" ", "%20")
            print(
                f"[cyan]"
                f"Creating pipeline for '.azurepipelines/{entry.name}' in "
                "Azure DevOps...[/cyan]"
            )
            response = requests.post(
                f"https://dev.azure.com/{azdo_org}/{encoded_project}/_apis/build/definitions?api-version=7.1-preview.7",
                data=json.dumps(pipeline_data),
                auth=("", token),
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
    print("[bold green]*** 'create-pipelines-azdo' task end ***[/bold green]")


@task
def setup_mkdocs_ghpages(c, github_repo_owner, repo_name):
    """Perform initial setup for mkdocs on GitHub."""
    print("[bold green]*** 'setup-mkdocs' task start ***[/bold green]")

    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    print("[cyan]Authenticating to GitHub...[/cyan]")
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))

    # Enable Pages
    github.rest.repos.create_pages_site(
        owner=github_repo_owner, repo=repo_name, data={"build_type": "workflow"}
    )

    github.rest.repos.create_or_update_environment(
        owner=github_repo_owner,
        repo=repo_name,
        environment_name="github-pages",
        data={"deployment_branch_policy": None},
    )
    print("[bold green]*** 'setup-mkdocs' task end ***[/bold green]")


@task
def delete_unneeded_template_files(c):
    """Delete files used only in the template process, including this tasks.py file."""
    print(
        "[bold green]*** 'delete-unneeded-template-files' task start ***[/bold green]"
    )
    os.remove("token.json")
    os.remove(__file__)
    print("[bold green]*** 'delete-unneeded-template-files' task end ***[/bold green]")

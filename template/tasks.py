"""Postmodern template tasks.

This file is to be executed with https://www.pyinvoke.org/ in Python 3.6+.
"""

import json
import os
import shutil
import tempfile
import time
from pathlib import Path

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


@task
def create_repo_azdo(c, repo_name, azdo_project, azdo_org):
    """Create an Azure DevOps repo."""
    print("[bold green]*** 'create-repo-azdo' task start ***[/bold green]")
    with open("token.json") as token_file:
        token = json.loads(token_file.read())["token"]

    repo_data = {"name": repo_name}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    print("[cyan]Creating repo in Azure DevOps...[/cyan]")
    response = requests.post(
        f"https://dev.azure.com/{azdo_org}/{azdo_project}/_apis/git/repositories?api-version=7.2-preview.1",
        data=json.dumps(repo_data),
        auth=("", token),
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    print("[bold green]*** 'create-repo-azdo' task end ***[/bold green]")


@task(optional=["github_repo_owner", "azdo_org", "azdo_project"])
def initialize_repo_and_commit_files(
    c,
    lifecycle,
    developer_platform,
    repo_name,
    github_repo_owner=None,
    azdo_org=None,
    azdo_project=None,
):
    """Create an initial branch and commit files."""
    print(
        "[bold green]*** 'initialize-repo-and-commit-files' task start ***[/bold green]"
    )
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
        # Auth for the push below is handled by 'gh auth setup-git', run earlier in
        # _tasks -- no credential file needed here, unlike the Azure DevOps branch.
        remote_url = f"https://github.com/{github_repo_owner}/{repo_name}.git"
        c.run(f"git remote add origin {remote_url}")
        print("[cyan]Pushing to remote...[/cyan]")
        c.run("git push -u origin --all")
    elif developer_platform == "Azure DevOps":
        with open("token.json") as token_file:
            token = json.loads(token_file.read())["token"]
        remote_url = f"https://{azdo_org}@dev.azure.com/{azdo_org}/{azdo_project}/_git/{repo_name}"
        gcm_dir = f"{str(Path.home())}/.gcm/store/git/https/dev.azure.com/{azdo_org}"
        gcm_file = "copier.credential"
        gcm_service = f"https://dev.azure.com/{azdo_org}"
        gcm_account = "copier"
        print("[cyan]Temporarily setting git config options for AzDO...[/cyan]")
        c.run("git config credential.useHttpPath true")
        c.run(f"git remote add origin {remote_url}")
        print("[cyan]Setting up Git credentials...[/cyan]")
        print(
            "[cyan]Temporarily enabling plaintext git credentials for first "
            "push...[/cyan]"
        )
        c.run("git config credential.credentialStore plaintext")
        print(
            "[cyan]Creating credentials file that will be cleaned up after "
            "push...[/cyan]"
        )
        Path(gcm_dir).mkdir(parents=True, exist_ok=True)
        with open(f"{gcm_dir}/{gcm_file}", "w+") as cred_file:
            cred_file.writelines(
                [f"{token}\n", f"service={gcm_service}\n", f"account={gcm_account}"]
            )
        print("[cyan]Pushing to remote...[/cyan]")
        c.run("git push -u origin --all")
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
            print(
                f"[cyan]"
                f"Creating pipeline for '.azurepipelines/{entry.name}' in "
                "Azure DevOps...[/cyan]"
            )
            response = requests.post(
                f"https://dev.azure.com/{azdo_org}/{azdo_project}/_apis/build/definitions?api-version=7.1-preview.7",
                data=json.dumps(pipeline_data),
                auth=("", token),
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
    print("[bold green]*** 'create-pipelines-azdo' task end ***[/bold green]")


@task
def delete_unneeded_template_files(c):
    """Delete files used only in the template process, including this tasks.py file."""
    print(
        "[bold green]*** 'delete-unneeded-template-files' task start ***[/bold green]"
    )
    Path("token.json").unlink(missing_ok=True)
    os.remove(__file__)
    print("[bold green]*** 'delete-unneeded-template-files' task end ***[/bold green]")

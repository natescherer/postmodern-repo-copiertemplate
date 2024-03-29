import requests
from azure.devops.connection import Connection
from azure.devops.exceptions import AzureDevOpsServiceError
from msrest.authentication import BasicAuthentication
from jinja2.ext import Extension

def extant_azdo_org(org):
    """
    Checks if Azure DevOps organization exists.
    """
    r = requests.get(f"https://dev.azure.com/{org}")
    if r.status_code == 203:
        return True
    else:
        return False

def valid_azdo_token_for_org(token, org):
    """
    Checks if Azure DevOps token is valid.
    """
    credentials = BasicAuthentication('', token)
    connection = Connection(base_url=f"https://dev.azure.com/{org}", creds=credentials)
    core_client = connection.clients.get_core_client()
    try:
        core_client.get_projects()
        return True
    except AzureDevOpsServiceError:
        return False

def valid_azdo_project_for_token_and_org(project, token, org):
    """
    Checks if Azure DevOps project exists for a given organization.
    """
    credentials = BasicAuthentication('', token)
    connection = Connection(base_url=f"https://dev.azure.com/{org}", creds=credentials)
    core_client = connection.clients_v5_1.get_core_client()
    get_projects_response = core_client.get_projects()
    index = 0
    projects = []
    while get_projects_response is not None:
        for item in get_projects_response.value:
            projects.append(item.name)
            index += 1
        if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
            get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
        else:
            get_projects_response = None
    if project in projects:
        return True
    else:
        return False

def available_azdo_repo_name_for_token_and_org_and_project(repo, token, org, project):
    """
    Checks if an Azure DevOps repo name is available.
    """
    credentials = BasicAuthentication('', token)
    connection = Connection(base_url=f"https://dev.azure.com/{org}", creds=credentials)
    git_client = connection.clients_v5_1.get_git_client()
    get_repos_response = git_client.get_repositories(project)
    repos = []
    for item in get_repos_response:
        repos.append(item.name)
    if repo not in repos:
        return True
    else:
        return False


class AzureDevOpsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.tests["extant_azdo_org"] = extant_azdo_org
        environment.tests["valid_azdo_token_for_org"] = valid_azdo_token_for_org
        environment.tests["valid_azdo_project_for_token_and_org"] = valid_azdo_project_for_token_and_org
        environment.tests["available_azdo_repo_name_for_token_and_org_and_project"] = available_azdo_repo_name_for_token_and_org_and_project

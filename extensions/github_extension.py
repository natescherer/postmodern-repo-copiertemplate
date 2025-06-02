"""Provide extension for GitHub projects."""

import githubkit
from jinja2.ext import Extension


def valid_gh_token(token):
    """Check if GitHub token is valid.

    Returns:
        True or False.

    """
    github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
    try:
        github.rest.users.get_authenticated()
        return True
    except Exception:
        return False


# Disabled as not currently in use, may eventually delete
# def same_as_gh_token_user(user, token):
#     """
#     Checks if a provided user matches the user associated with a GitHub token.
#     """
#     github = githubkit.GitHub(githubkit.TokenAuthStrategy(token))
#     response = github.rest.users.get_authenticated()
#     return user == response.parsed_data.login


def available_gh_repo_name_for_owner(repo, owner):
    """Check if a GitHub repo name is available.

    Returns:
        True or False.

    """
    github = githubkit.GitHub(githubkit.UnauthAuthStrategy())
    try:
        github.rest.repos.get(owner, repo)
        return False
    except githubkit.exception.RequestFailed:
        # This is what you want, i.e. a 404 when it tries to find the repo
        return True


class GitHubExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.tests["valid_gh_token"] = valid_gh_token
        # environment.tests["same_as_gh_token_user"] = same_as_gh_token_user
        environment.tests["available_gh_repo_name_for_owner"] = (
            available_gh_repo_name_for_owner
        )

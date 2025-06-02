"""Provide extensions relating to paths."""

import os

from jinja2.ext import Extension

try:
    from jinja2 import pass_eval_context as eval_context
except ImportError:
    from jinja2 import evalcontextfilter as eval_context


def path_exists(path):
    """Check if a path exists, and return True if it does and nothing if it doesn't.

    Returns:
        True or None.

    """
    if os.path.exists(path):
        return True


def path_missing(path):
    """Check if a path exists, and return True if it does NOT and nothing if it does.

    Returns:
        True or None.

    """
    if not os.path.exists(path):
        return True


@eval_context
def cwd_name(eval_ctx, value):
    """Return the name of the current working directory.

    Returns:
        Working directory name.

    """
    return os.path.basename(os.getcwd())


class PathExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["path_exists"] = path_exists
        environment.filters["path_missing"] = path_missing
        environment.filters["cwd_name"] = cwd_name

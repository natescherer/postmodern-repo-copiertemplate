"""Provide extensions relating to paths."""

import os

from jinja2.ext import Extension


def path_exists(path):
    """Check if a path exists, and return True if it does and nothing if it doesn't."""
    if os.path.exists(path):
        return True


def path_missing(path):
    """Check if a path exists, and return True if it does NOT and nothing if it does."""
    if not os.path.exists(path):
        return True


class PathExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["path_exists"] = path_exists
        environment.filters["path_missing"] = path_missing

    def _cwd_name(self):
        """Return the name of the current working directory."""
        return os.path.basename(os.getcwd())

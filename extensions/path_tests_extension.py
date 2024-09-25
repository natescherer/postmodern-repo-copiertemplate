"""Provide extension for testing path validity."""

import os

from jinja2.ext import Extension


def path_exists(path):
    """Check if a path exists, and returns True if it does and nothing if it doesn't."""
    if os.path.exists(path):
        return True


def path_missing(path):
    """Check if a path exists, and returns True if it does NOT and nothing if it does."""
    if not os.path.exists(path):
        return True


class PathTestsExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["path_exists"] = path_exists
        environment.filters["path_missing"] = path_missing

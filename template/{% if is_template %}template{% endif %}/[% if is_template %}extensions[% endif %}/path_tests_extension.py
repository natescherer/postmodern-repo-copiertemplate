import os

from jinja2.ext import Extension


def path_exists(path):
    """
    Checks if a path exists, and returns True if it does and nothing if it doesn't.
    """
    if os.path.exists(path):
        return True

def path_missing(path):
    """
    Checks if a path exists, and returns True if it does NOT and nothing if it does.
    """
    if not os.path.exists(path):
        return True


class PathTestsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["path_exists"] = path_exists
        environment.filters["path_missing"] = path_missing

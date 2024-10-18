"""Provide extension for checking current version."""

import json

from jinja2.ext import Extension
from packaging.version import Version


def current_release_please_version_is_pre_1():
    """Check the current version in .release-please-manifest.json and returns True if it is less than 1.0.0."""
    with open(".release-please-manifest.json") as file:
        data = json.load(file)
    if Version(data["."]) < Version("1.0.0"):
        return True
    else:
        return False


class VersionExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["current_release_please_version_is_pre_1"] = (
            current_release_please_version_is_pre_1
        )

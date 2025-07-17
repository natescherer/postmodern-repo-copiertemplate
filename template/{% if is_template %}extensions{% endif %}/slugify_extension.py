"""Provide extension for slugify-ing values."""

from jinja2.ext import Extension
from slugify import slugify


def slugify_function(string):
    """Slugify given input string.

    Returns:
        Slug version of input string.

    """
    return slugify(string)


class SlugifyExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["slugify"] = slugify_function

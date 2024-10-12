"""Provide extension for slugify-ing values."""

from jinja2.ext import Extension
from slugify import slugify as unicode_slugify


def slugify(string):
    """Slugify given input string."""
    return unicode_slugify(string, only_ascii=True)


class SlugifyExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["slugify"] = slugify

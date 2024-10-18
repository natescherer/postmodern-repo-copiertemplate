"""Provides a filter that will add single quotes to a string if needed for YAML."""

from jinja2.ext import Extension


def quote_for_yaml(string):
    """Return a string wrapped in single-quotes if it contains YAML special characters."""
    if any(
        x in string
        for x in (
            ":",
            "{",
            "}",
            "[",
            "]",
            ",",
            "&",
            "*",
            "#",
            "?",
            "|",
            "-",
            "<",
            ">",
            "=",
            "!",
            "%",
            "@",
        )
    ):
        return f"'{string}'"
    else:
        return string


class YamlQuoteExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.filters["quote_for_yaml"] = quote_for_yaml

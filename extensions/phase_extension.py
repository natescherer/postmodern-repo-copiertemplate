"""Provide extension for exposing update phase."""

from pathlib import Path

from jinja2.ext import Extension


class PhaseExtension(Extension):
    """Export for use by Jinja."""

    def __init__(self, environment):
        """Export for use by Jinja."""
        super().__init__(environment)
        environment.globals["is_copier_update"] = Path(".copier-answers.yml").exists()

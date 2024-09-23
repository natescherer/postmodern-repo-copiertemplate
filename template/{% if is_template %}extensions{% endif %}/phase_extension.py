from jinja2.ext import Extension
from pathlib import Path

class PhaseExtension(Extension):
    def __init__(self, environment):
          super().__init__(environment)
          environment.globals["is_copier_update"] = Path(".copier-answers.yml").exists()
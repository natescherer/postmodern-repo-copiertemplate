import subprocess
import git

from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        new_context = {}
        new_context["gitconfig-username"] = git.config.GitConfigParser().get_value("user", "name")
        new_context["gitconfig-useremail"] = git.config.GitConfigParser().get_value("user", "email")
        return new_context

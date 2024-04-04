import shutil
from jinja2.ext import Extension

def template_then_make_zip_and_return_true(project_type):
    """
    Dirty hack to zip the contents of template/ into template/template.zip when
    the project_type is Template.
    """
    if project_type == "Template":
        shutil.make_archive("clean_template", "zip", "template")
        shutil.move("clean_template.zip", "template/clean_template.zip")
        return True
    else:
        return False

class PreRenderFunctionsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.tests["template_then_make_zip_and_return_true"] = template_then_make_zip_and_return_true

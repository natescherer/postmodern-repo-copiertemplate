import glob
import os
import shutil
import subprocess


class color:
    PURPLE = "\033[1;35;48m"
    CYAN = "\033[1;36;48m"
    BOLD = "\033[1;37;48m"
    BLUE = "\033[1;34;48m"
    GREEN = "\033[1;32;48m"
    YELLOW = "\033[1;33;48m"
    RED = "\033[1;31;48m"
    BLACK = "\033[1;30;48m"
    UNDERLINE = "\033[4;37;48m"
    END = "\033[1;37;0m"


print(color.GREEN + "*** POST-GEN PROJECT HOOK START ***" + color.END)

# Choose correct files based on project type
PROJECT = "{{cookiecutter.project_type}}"
if PROJECT == "Cookiecutter":
    os.rename("README-cookiecutter.md", "README.md")
    os.rename(".github/dependabot-cookiecutter.yml", ".github/dependabot.yml")
    os.rename(
        ".github/workflows/Release-cookiecutter.yml", ".github/workflows/Release.yml"
    )
    os.rename("cookiecutter", "{{'{{cookiecutter.repo_name}}'}}")
elif PROJECT == "Basic":
    os.rename("README-basic.md", "README.md")
    os.rename(".github/dependabot-basic.yml", ".github/dependabot.yml")
    os.rename(".github/workflows/Release-basic.yml", ".github/workflows/Release.yml")
unneeded_readmes = glob.glob("README-*")
for readme in unneeded_readmes:
    os.unlink(readme)
unneeded_dependabot_yamls = glob.glob(".github/dependabot-*")
for workflow in unneeded_dependabot_yamls:
    os.unlink(workflow)
unneeded_release_workflows = glob.glob(".github/workflows/Release-*")
for workflow in unneeded_release_workflows:
    os.unlink(workflow)

# Remove unneeded files based on options
REMOVE_PATHS = [
    '{% if cookiecutter.include_python_install_doc == "No" %}docs/installing_python.md{% endif %}',
    '{% if cookiecutter.include_python_install_doc == "No" %}docs/installing_pipx.md{% endif %}',
    '{% if cookiecutter.project_type != "Cookiecutter" %}docs/cookiecutter_defaults.md{% endif %}',
    '{% if cookiecutter.project_type != "Cookiecutter" %}cookiecutter.json{% endif %}',
]
print(color.CYAN + "Removing unneeded files..." + color.END)
for path in REMOVE_PATHS:
    CLEAN_PATH = path.strip()
    if CLEAN_PATH and os.path.exists(CLEAN_PATH):
        if os.path.isfile(CLEAN_PATH):
            os.unlink(CLEAN_PATH)
        else:
            shutil.rmtree(CLEAN_PATH)

if os.environ.get("CI") != "true":
    print(color.CYAN + "Creating initial branch..." + color.END)
    subprocess.run(
        ["git", "checkout", "-b", "feature/initial"], capture_output=True, check=True
    )
else:
    print(
        color.YELLOW
        + "Skipping creating intial branch as script appears to be running in GitHub Actions."
        + color.END
    )

if os.environ.get("CI") != "true":
    print(
        color.YELLOW
        + "If you are using Doppler, set up your sync for this repo now!"
        + color.END
    )

    print(
        color.PURPLE
        + "Template complete! If you want to open in VSCode: code {{cookiecutter.repo_name}}"
        + color.END
    )
else:
    print(
        color.YELLOW
        + "Skipping post-gen reminders as script appears to be running in GitHub Actions."
        + color.END
    )

print(color.GREEN + "*** POST-GEN PROJECT HOOK END ***" + color.END)

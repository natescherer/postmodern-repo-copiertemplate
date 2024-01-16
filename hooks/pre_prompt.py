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


print(color.GREEN + "*** PRE-PROMPT HOOK START ***" + color.END)

print(color.CYAN + "Verifying GitHub CLI is installed..." + color.END)
if not shutil.which("gh"):
    raise FileNotFoundError("GitHub CLI is required and is not installed!")

print(color.CYAN + "Verifying you are logged in to GitHub CLI..." + color.END)
gh_auth_status = subprocess.run(
    ["gh", "auth", "status"], capture_output=True, check=True
)

print(color.GREEN + "*** PRE-PROMPT HOOK END ***" + color.END)

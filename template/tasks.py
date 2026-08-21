"""Postmodern template tasks.

This file is to be executed with https://www.pyinvoke.org/ in Python 3.6+.
"""

import os
import shutil
import tempfile
import time

from invoke import task
from rich import print


@task(optional=["vcs_ref"])
def copy_template_files(c, src_path, vcs_ref=None):
    """Pull down an additional copy of template files."""
    print("[bold green]*** 'copy-template-files' task start ***[/bold green]")

    with tempfile.TemporaryDirectory() as tmpdir:
        if vcs_ref != "HEAD" and vcs_ref is not None:
            time.sleep(5)
            c.run(
                f"git -c advice.detachedHead=false clone --quiet "
                f"--branch {vcs_ref} {src_path} {tmpdir}"
            )
        else:
            c.run(f"git -c advice.detachedHead=false clone --quiet {src_path} {tmpdir}")
        shutil.copytree(f"{tmpdir}/template", "template", dirs_exist_ok=True)
    print("[bold green]*** 'copy-template-files' task end ***[/bold green]")


@task
def delete_unneeded_template_files(c):
    """Delete files used only in the template process, including this tasks.py file."""
    print(
        "[bold green]*** 'delete-unneeded-template-files' task start ***[/bold green]"
    )
    os.remove(__file__)
    print("[bold green]*** 'delete-unneeded-template-files' task end ***[/bold green]")

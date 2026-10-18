"""Terminal output shared by the integration test scripts.

Colors apply only when stdout is a terminal and NO_COLOR (https://no-color.org) isn't
set.
"""

import os
import sys
from dataclasses import dataclass, field


def _ansi_supported() -> bool:
    if not sys.stdout.isatty() or "NO_COLOR" in os.environ:
        return False
    if os.name != "nt":
        return True
    # Windows consoles interpret ANSI codes only once a program turns that on.
    import ctypes  # noqa: PLC0415

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    mode = ctypes.c_uint32()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return False
    enable_virtual_terminal_processing = 0x0004
    return bool(
        kernel32.SetConsoleMode(handle, mode.value | enable_virtual_terminal_processing)
    )


_ANSI = _ansi_supported()


def _style(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _ANSI else text


def _bold(text: str) -> str:
    return _style(text, "1")


def _green(text: str) -> str:
    return _style(text, "32")


def _red(text: str) -> str:
    return _style(text, "31")


def _cyan(text: str) -> str:
    return _style(text, "36")


def heading(text: str) -> None:
    """Print a section heading, set off by a blank line."""
    print(f"\n{_bold(text)}")


def check(failures: list[str], name: str, ok: bool, detail: str = "") -> None:
    """Record and print one named check's result immediately, without halting.

    Every automated check goes through here, so failures accumulate instead of
    stopping the run at the first one, and a full run reports the complete picture.
    """
    if ok:
        print(f"  {_green('[PASS]')} {name}")
    else:
        print(f"  {_red('[FAIL]')} {name}" + (f": {detail}" if detail else ""))
        failures.append(name)


@dataclass
class RepoResult:
    """One test repo's outcome, for summary()."""

    label: str
    repo: str
    local_path: str
    failures: list[str] = field(default_factory=list)
    setup_checklist: list[str] = field(default_factory=list)


@dataclass
class Step:
    """One next step for summary(): what to do, then the commands that do it."""

    text: str
    commands: list[str] = field(default_factory=list)


def summary(results: list[RepoResult], steps: list[Step] = ()) -> None:
    """Print each repo's result, then numbered next steps, at the end of a run."""
    heading("Summary")
    for result in results:
        if result.failures:
            outcome = _red(f"{len(result.failures)} check(s) failed")
        else:
            outcome = _green("all checks passed")
        print(f"\n  {_bold(result.label)}: {outcome}")
        print(f"    {result.repo}")
        print(f"    {result.local_path}")
        for name in result.failures:
            print(f"    {_red('-')} {name}")
        if result.setup_checklist:
            print("    Setup checklist, from copier copy:")
            for item in result.setup_checklist:
                print(f"      {item}")
    if steps:
        heading("Next steps")
        for number, step in enumerate(steps, 1):
            print(f"\n  {number}. {step.text}")
            for command in step.commands:
                print(f"       {_cyan(command)}")

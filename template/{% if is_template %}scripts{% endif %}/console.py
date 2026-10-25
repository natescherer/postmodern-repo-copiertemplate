"""Terminal output and logging shared by the integration test scripts.

Colors apply only when stdout is a terminal and NO_COLOR (https://no-color.org) isn't
set. Once start_log() runs, everything printed, and every command's output, also goes
to a log directory for later analysis.
"""

import os
import re
import shutil

# S404: drives real CLI tools; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TextIO

_ANSI_CODE = re.compile(r"\033\[[0-9;]*m")
_log_file: TextIO | None = None
log_dir: Path | None = None


class _Tee:
    """A text stream that also writes to the log file, minus color codes."""

    def __init__(self, stream: TextIO, file: TextIO) -> None:
        self._stream, self._file = stream, file

    def write(self, text: str) -> int:
        self._stream.write(text)
        self._file.write(_ANSI_CODE.sub("", text))
        return len(text)

    def flush(self) -> None:
        self._stream.flush()
        self._file.flush()

    def __getattr__(self, name: str) -> object:
        return getattr(self._stream, name)


def start_log(platform: str) -> Path:
    """Copy everything this run prints into a new log directory.

    Returns:
        The directory: .cache/integration-test/<timestamp>-<platform>/, under the
        current directory.

    """
    global _log_file, log_dir  # noqa: PLW0603
    log_dir = (
        Path.cwd()
        / ".cache"
        / "integration-test"
        / f"{time.strftime('%Y%m%d-%H%M%S')}-{platform}"
    )
    log_dir.mkdir(parents=True)
    _log_file = (log_dir / "run.log").open("w", encoding="utf-8", newline="\n")
    sys.stdout = _Tee(sys.stdout, _log_file)
    sys.stderr = _Tee(sys.stderr, _log_file)
    return log_dir


def _log_only(text: str) -> None:
    if _log_file and text:
        _log_file.write(
            _ANSI_CODE.sub("", text) + ("" if text.endswith("\n") else "\n")
        )
        _log_file.flush()


def save_log(name: str, text: str) -> None:
    """Write `text` to file `name` in the run's log directory, if there is one."""
    if log_dir:
        (log_dir / name).write_text(text, encoding="utf-8", newline="\n")


def run(
    *args: str,
    check: bool = True,
    capture: bool = False,
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    echo: bool = True,
    secret: bool = False,
) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first, and log its output.

    Resolves argv[0] with shutil.which() first. Some CLIs, such as the Azure CLI's `az`,
    are `.cmd` batch wrappers on Windows, which subprocess without a shell can't find by
    bare name (`FileNotFoundError: [WinError 2]`). which() resolves the path on any
    platform without shell=True.

    Without `capture`, the output streams to the terminal as the command runs. Either
    way, the log gets it, unless `secret`. `echo=False` logs the command line without
    printing it, for polls.

    Returns:
        The completed process, with its stdout (and stderr, if captured).

    Raises:
        subprocess.CalledProcessError: if the command exits nonzero and `check`.

    """
    line = f"$ {' '.join(args)}" + (f"  (in {cwd})" if cwd else "")
    if echo:
        print(line)
    else:
        _log_only(line)
    resolved = (shutil.which(args[0]) or args[0], *args[1:])
    # Python tools such as Copier write UTF-8 to a pipe only when told to.
    full_env = {**os.environ, "PYTHONIOENCODING": "utf-8", **(env or {})}
    options = {"text": True, "encoding": "utf-8", "errors": "replace", "cwd": cwd}
    if capture:
        # S603: args are always a fixed list built by the caller; no shell=True.
        result = subprocess.run(  # noqa: S603
            resolved, check=False, capture_output=True, env=full_env, **options
        )
        if not secret:
            _log_only(result.stdout + result.stderr)
    else:
        lines: list[str] = []
        # S603: as above.
        with subprocess.Popen(  # noqa: S603
            resolved,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=full_env,
            **options,
        ) as process:
            for output in process.stdout:
                print(output, end="")
                lines.append(output)
        result = subprocess.CompletedProcess(
            resolved, process.returncode, "".join(lines), ""
        )
    if check and result.returncode:
        raise subprocess.CalledProcessError(
            result.returncode, resolved, result.stdout, result.stderr
        )
    return result


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
    if log_dir:
        print(f"\n  Logs for this run: {log_dir}")

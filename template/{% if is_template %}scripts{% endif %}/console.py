"""Terminal output and logging shared by the integration test scripts.

Once start_log() runs, the terminal shows only an outline of the run: section headings,
each step and check with a timestamp, a spinner under the current step, and the
summary. Everything else, including every command and its output, goes to a log
directory for later analysis, with a timestamp on every line. Errors still reach the
terminal.

Colors apply only when stdout is a terminal and NO_COLOR (https://no-color.org) isn't
set.
"""

import os
import re
import shutil

# S404: drives real CLI tools; no untrusted input, no shell=True.
import subprocess  # noqa: S404
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TextIO

_ANSI_CODE = re.compile(r"\033\[[0-9;]*m")
_terminal: TextIO = sys.stdout
_lock = threading.RLock()
_log_file: TextIO | None = None
_log_at_line_start = True
log_dir: Path | None = None


def _clock() -> str:
    return time.strftime("%H:%M:%S")


def _log_write(text: str) -> None:
    """Append `text` to the log, minus color codes, with a timestamp on each line."""
    global _log_at_line_start  # noqa: PLW0603
    if not _log_file or not text:
        return
    with _lock:
        for line in _ANSI_CODE.sub("", text).splitlines(keepends=True):
            if _log_at_line_start:
                _log_file.write(f"[{_clock()}] ")
            _log_file.write(line)
            _log_at_line_start = line.endswith("\n")
        _log_file.flush()


class _LogStream:
    """What print() writes to once start_log() runs: the log file only."""

    def write(self, text: str) -> int:
        _log_write(text)
        return len(text)

    def flush(self) -> None:
        if _log_file:
            _log_file.flush()

    def isatty(self) -> bool:
        return False


class _ErrorStream:
    """What stderr becomes once start_log() runs: the terminal and the log file."""

    def __init__(self, stream: TextIO) -> None:
        self._stream = stream

    def write(self, text: str) -> int:
        with _lock:
            _spinner.clear()
            self._stream.write(text)
            self._stream.flush()
        _log_write(text)
        return len(text)

    def flush(self) -> None:
        self._stream.flush()

    def __getattr__(self, name: str) -> object:
        return getattr(self._stream, name)


class _Spinner:
    """A line under the current step that shows it's still running, and for how long."""

    _FRAMES = "|/-\\"

    def __init__(self) -> None:
        self._started: float | None = None
        self._drawn = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if not _terminal.isatty():
            return
        with _lock:
            self._started = time.monotonic()
            if self._thread is None:
                self._thread = threading.Thread(target=self._spin, daemon=True)
                self._thread.start()

    def stop(self) -> None:
        with _lock:
            self.clear()
            self._started = None

    def clear(self) -> None:
        """Erase the spinner's line, so other output can take its place."""
        with _lock:
            if self._drawn:
                width = shutil.get_terminal_size().columns - 1
                _terminal.write("\r" + " " * width + "\r")
                _terminal.flush()
                self._drawn = False

    def _spin(self) -> None:
        frame = 0
        while True:
            with _lock:
                if self._started is not None:
                    elapsed = int(time.monotonic() - self._started)
                    minutes, seconds = divmod(elapsed, 60)
                    frame_char = self._FRAMES[frame % len(self._FRAMES)]
                    _terminal.write(f"\r  {frame_char} {minutes}:{seconds:02d}")
                    _terminal.flush()
                    self._drawn = True
            frame += 1
            time.sleep(0.25)


_spinner = _Spinner()


def start_log(platform: str) -> Path:
    """Send everything this run prints to a new log directory, not the terminal.

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
    sys.stdout = _LogStream()
    sys.stderr = _ErrorStream(sys.stderr)
    return log_dir


def say(text: str = "", *, timestamped: bool = False) -> None:
    """Show `text` on the terminal, and log it.

    `timestamped` puts the time in front of it on the terminal; the log has a timestamp
    on every line already.
    """
    with _lock:
        _spinner.clear()
        _terminal.write((f"{_dim(_clock())} " if timestamped else "") + text + "\n")
        _terminal.flush()
    _log_write(text + "\n")


def ask(prompt: str) -> str:
    """Show `prompt` on the terminal and read the answer typed after it.

    With no terminal to answer from, input() raises EOFError, which the caller handles.

    Returns:
        The line typed, without its newline.

    """
    with _lock:
        _spinner.stop()
        _terminal.write(prompt)
        _terminal.flush()
    answer = input()
    _log_write(prompt + answer + "\n")
    return answer


def _log_only(text: str) -> None:
    if text:
        _log_write(text if text.endswith("\n") else text + "\n")


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
    stdin: str | None = None,
) -> subprocess.CompletedProcess:
    """Run a CLI command, echoing it first, and log its output.

    Resolves argv[0] with shutil.which() first. Some CLIs, such as the Azure CLI's `az`,
    are `.cmd` batch wrappers on Windows, which subprocess without a shell can't find by
    bare name (`FileNotFoundError: [WinError 2]`). which() resolves the path on any
    platform without shell=True.

    Without `capture`, the output streams as the command runs; once start_log() runs,
    that's to the log. Either way, the log gets it, unless `secret`. `echo=False` logs
    the command line without printing it, for polls. `stdin` feeds a captured command
    its input, such as a secret that mustn't appear in its arguments.

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
            resolved,
            check=False,
            capture_output=True,
            env=full_env,
            input=stdin,
            **options,
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
    if not _terminal.isatty() or "NO_COLOR" in os.environ:
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


def _dim(text: str) -> str:
    return _style(text, "2")


def _green(text: str) -> str:
    return _style(text, "32")


def _red(text: str) -> str:
    return _style(text, "31")


def _cyan(text: str) -> str:
    return _style(text, "36")


def heading(text: str) -> None:
    """Show a section heading, set off by a blank line."""
    _spinner.stop()
    say(f"\n{_bold(text)}")


def step(text: str) -> None:
    """Show the step that's starting, with a timestamp, and spin until the next one."""
    say(text, timestamped=True)
    _spinner.start()


def check(failures: list[str], name: str, ok: bool, detail: str = "") -> None:
    """Record and show one named check's result immediately, without halting.

    Every automated check goes through here, so failures accumulate instead of
    stopping the run at the first one, and a full run reports the complete picture.
    """
    if ok:
        say(f"  {_green('[PASS]')} {name}", timestamped=True)
    else:
        say(
            f"  {_red('[FAIL]')} {name}" + (f": {detail}" if detail else ""),
            timestamped=True,
        )
        failures.append(name)


@dataclass
class RepoResult:
    """One test repo's outcome, for summary()."""

    label: str
    repo: str
    local_path: str
    failures: list[str] = field(default_factory=list)
    setup_checklist: list[str] = field(default_factory=list)
    url: str = ""


def _show_result(result: RepoResult) -> None:
    if result.failures:
        outcome = _red(f"{len(result.failures)} check(s) failed")
    else:
        outcome = _green("all checks passed")
    say(f"\n  {_bold(result.label)}: {outcome}")
    say(f"    Name:        {result.repo}")
    if result.url:
        say(f"    Web:         {_cyan(result.url)}")
    say(f"    Local clone: {_cyan(result.local_path)}")
    for name in result.failures:
        say(f"    {_red('-')} {name}")
    if result.setup_checklist:
        say("    Setup checklist, from copier copy:")
        for item in result.setup_checklist:
            say(f"      {item}")


def summary(results: list[RepoResult], runbook: str = "") -> None:
    """Show each repo's result at the end of a run, then the runbook to follow."""
    heading("Summary")
    for result in results:
        _show_result(result)
    if runbook:
        say(f"\n  Next, follow the rest of the runbook: {_cyan(runbook)}")
    if log_dir:
        say(f"\n  Logs for this run: {log_dir}")

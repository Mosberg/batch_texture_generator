from __future__ import annotations

import queue
import subprocess
import threading
from dataclasses import dataclass
from typing import Callable, Optional, Sequence


LogSink = Callable[[str], None]
ExitSink = Callable[[int], None]


@dataclass
class ProcState:
    popen: Optional[subprocess.Popen[str]] = None
    thread: Optional[threading.Thread] = None


class ProcessRunner:
    def __init__(self, *, on_log: LogSink, on_exit: ExitSink) -> None:
        self._on_log = on_log
        self._on_exit = on_exit
        self._q: "queue.Queue[str]" = queue.Queue()
        self._state = ProcState()

    def is_running(self) -> bool:
        p = self._state.popen
        return p is not None and p.poll() is None

    def start(self, cmd: Sequence[str], *, cwd: str) -> None:
        if self.is_running():
            raise RuntimeError("A process is already running")

        p = subprocess.Popen(
            list(cmd),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )
        self._state.popen = p

        t = threading.Thread(target=self._reader_thread, daemon=True)
        self._state.thread = t
        t.start()

    def stop(self) -> None:
        p = self._state.popen
        if p is None:
            return
        if p.poll() is not None:
            return
        try:
            p.terminate()
        except Exception:
            pass

    def poll_logs(self) -> None:
        # Drain queued logs
        while True:
            try:
                line = self._q.get_nowait()
            except queue.Empty:
                break
            self._on_log(line)

    def _reader_thread(self) -> None:
        p = self._state.popen
        if p is None:
            return

        try:
            assert p.stdout is not None
            for line in p.stdout:
                self._q.put(line.rstrip("\n"))
        finally:
            code = p.wait()
            self._q.put(f"\n[process exited: {code}]\n")
            self._on_exit(int(code))
            self._state = ProcState()

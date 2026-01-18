from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional


def is_windows() -> bool:
    return os.name == "nt"


def now_ts() -> str:
    t = time.localtime()
    return f"{t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"


def normalize_path_str(p: str) -> str:
    return str(p).strip().replace("\\\\", "/")


def try_rel(repo: Path, p: Path) -> str:
    try:
        return p.resolve().relative_to(repo.resolve()).as_posix()
    except Exception:
        return p.resolve().as_posix()


def find_repo_root(start: Path) -> Path:
    """Best-effort repo root detection by walking upward until `.git` is found."""

    p = start.resolve()
    for _ in range(50):
        if (p / ".git").exists():
            return p
        if p.parent == p:
            return start.resolve()
        p = p.parent
    return start.resolve()


def default_btg_candidates(repo_root: Path) -> List[Path]:
    here = Path(__file__).resolve().parent
    return [
        (repo_root / "tools" / "btg.py"),
        (here.parent / "btg.py"),
        (repo_root / "btg.py"),
        (repo_root / "tools" / "btg.py"),
    ]


def guess_btg_script(repo_root: Path) -> Optional[Path]:
    for c in default_btg_candidates(repo_root):
        if c.exists() and c.is_file():
            return c.resolve()
    return None


def open_in_file_manager(path: Path) -> None:
    path = path.resolve()
    if is_windows():
        os.startfile(str(path))  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
        return
    subprocess.Popen(["xdg-open", str(path)])

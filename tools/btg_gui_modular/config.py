from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from .constants import HOME_CONFIG_NAME, REPO_CONFIG_NAME


@dataclass
class ProjectConfig:
    repo_root: str
    btg_script: str
    python_exe: str
    log_level: str
    dry_run: bool


def _config_path_repo(repo_root: Path) -> Path:
    return repo_root / REPO_CONFIG_NAME


def _config_path_home() -> Path:
    return Path.home() / HOME_CONFIG_NAME


def pick_config_path_for_save(repo_root: Path) -> Path:
    repo_cfg = _config_path_repo(repo_root)
    try:
        if repo_root.exists():
            if repo_cfg.exists() or os.access(str(repo_root), os.W_OK):
                return repo_cfg
    except Exception:
        pass
    return _config_path_home()


def load_config_best_effort(repo_root: Path) -> Dict[str, Any]:
    for p in (_config_path_repo(repo_root), _config_path_home()):
        try:
            if p.exists():
                data = json.loads(p.read_text(encoding="utf-8"))
                return data if isinstance(data, dict) else {}
        except Exception:
            continue
    return {}


def save_config(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

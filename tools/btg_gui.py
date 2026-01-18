#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import queue
import shlex
import subprocess
import sys
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional, Sequence, Tuple

APP_NAME = "BTG GUI"
APP_VERSION = "2.0.0"

DEFAULT_GEOMETRY = "1120x820"

# Config is stored in:
# - <repo>/.btg_gui.json if repo root is chosen and writable
# - else user home: ~/.btg_gui.json
REPO_CONFIG_NAME = ".btg_gui.json"
HOME_CONFIG_NAME = ".btg_gui.json"


def _is_windows() -> bool:
    return os.name == "nt"


def _now_ts() -> str:
    # Keep it simple; no datetime import needed
    t = time.localtime()
    return f"{t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"


def _safe_int(s: str, default: int) -> int:
    try:
        return int(s)
    except Exception:
        return default


def _safe_float(s: str, default: float) -> float:
    try:
        return float(s)
    except Exception:
        return default


def _normalize_path_str(p: str) -> str:
    return p.strip().replace("\\", "/")


def _try_rel(repo: Path, p: Path) -> str:
    try:
        return p.resolve().relative_to(repo.resolve()).as_posix()
    except Exception:
        return p.resolve().as_posix()


def _open_in_file_manager(path: Path) -> None:
    path = path.resolve()
    if _is_windows():
        os.startfile(str(path))  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
        return
    subprocess.Popen(["xdg-open", str(path)])


def _find_repo_root(start: Path) -> Path:
    """
    Best-effort repo root detection:
      - stop at filesystem root
      - if we see a .git directory, treat as repo root
    """
    p = start.resolve()
    for _ in range(50):
        if (p / ".git").exists():
            return p
        if p.parent == p:
            return start.resolve()
        p = p.parent
    return start.resolve()


def _default_btg_candidates(repo_root: Path) -> List[Path]:
    """
    Candidates based on common layouts:
      - tools/btg.py (your README structure)
      - btg.py next to this gui
      - repo_root/btg.py
    """
    here = Path(__file__).resolve().parent
    return [
        (repo_root / "tools" / "btg.py"),
        (here / "btg.py"),
        (repo_root / "btg.py"),
        (repo_root / "tools" / "btg.py"),
    ]


def _guess_btg_script(repo_root: Path) -> Optional[Path]:
    for c in _default_btg_candidates(repo_root):
        if c.exists() and c.is_file():
            return c.resolve()
    return None


@dataclass
class ProcState:
    popen: Optional[subprocess.Popen[str]] = None
    thread: Optional[threading.Thread] = None


class BTGGui(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master

        # --- async output ---
        self._log_q: "queue.Queue[str]" = queue.Queue()
        self._proc = ProcState()

        # --- persistent config ---
        self.repo_root = tk.StringVar(value=str(_find_repo_root(Path.cwd())))
        self.btg_script = tk.StringVar(value="")  # filled after repo root init
        self.python_exe = tk.StringVar(value=sys.executable)

        # global btg flags
        self.log_level = tk.StringVar(value="INFO")
        self.global_dry_run = tk.BooleanVar(value=False)

        # --- tabs vars ---
        # Validate
        self.val_schemas = tk.StringVar(value="schemas")
        self.val_palettes = tk.StringVar(value="palettes")

        # Normalize
        self.norm_palettes = tk.StringVar(value="palettes")

        # Extract
        self.ext_textures = tk.StringVar(value="textures")
        self.ext_palettes_out = tk.StringVar(value="palettes")
        self.ext_max_colors = tk.StringVar(value="32")
        self.ext_min_alpha = tk.StringVar(value="1")
        self.ext_schema_ref = tk.StringVar(
            value="../../schemas/texture-palettes.schema.json"
        )
        self.ext_generator_version = tk.StringVar(value="1.0.0")

        # Recolor (single swap)
        self.rec_palettes_dir = tk.StringVar(value="palettes")
        self.rec_src_palette = tk.StringVar(value="wood/oak.texture-palettes.json")
        self.rec_dst_palette = tk.StringVar(value="metal/iron.texture-palettes.json")
        self.rec_src_id = tk.StringVar(value="oak")
        self.rec_dst_id = tk.StringVar(value="iron")
        self.rec_group = tk.StringVar(value="")  # blank => auto
        self.rec_input = tk.StringVar(value="textures_input")
        self.rec_output = tk.StringVar(value="output/textures/item")
        self.rec_no_recursive = tk.BooleanVar(value=False)
        self.rec_min_alpha = tk.StringVar(value="1")
        self.rec_alpha_weight = tk.StringVar(value="0.25")
        self.rec_preserve_alpha = tk.BooleanVar(value=True)
        self.rec_exact_first = tk.BooleanVar(value=True)

        # Legacy templates recolor-templates
        self.leg_palettes_dir = tk.StringVar(value="palettes")
        self.leg_templates_dir = tk.StringVar(value="textures_input")
        self.leg_output_root = tk.StringVar(value="output")
        self.leg_namespace = tk.StringVar(value="modid")
        self.leg_lang_file = tk.StringVar(value="en_us.json")
        self.leg_no_modid_tree = tk.BooleanVar(value=False)
        self.leg_no_flat_tree = tk.BooleanVar(value=False)

        # Generate
        self.gen_templates = tk.StringVar(value="textures_input")
        self.gen_palettes = tk.StringVar(value="palettes")
        self.gen_output = tk.StringVar(value="output/textures/item")
        self.gen_min_alpha = tk.StringVar(value="1")
        self.gen_alpha_weight = tk.StringVar(value="0.25")
        self.gen_preserve_alpha = tk.BooleanVar(value=True)
        self.gen_exact_first = tk.BooleanVar(value=True)
        self.gen_limit = tk.StringVar(value="")  # blank => none

        # AutoTemplate
        self.at_templates = tk.StringVar(value="textures_input")
        self.at_palettes = tk.StringVar(value="palettes")
        self.at_out_dir = tk.StringVar(value="")  # blank => templates dir
        self.at_materials = tk.StringVar(value="wood,metal,glass")
        self.at_min_alpha = tk.StringVar(value="1")
        self.at_min_hits = tk.StringVar(value="2")

        # Assets
        self.as_textures = tk.StringVar(value="output/textures/item")
        self.as_recursive = tk.BooleanVar(value=False)
        self.as_items_dir = tk.StringVar(value="output/items")
        self.as_models_dir = tk.StringVar(value="output/models/item")
        self.as_lang = tk.StringVar(value="output/lang/en_us.json")
        self.as_namespace = tk.StringVar(value="modid")
        self.as_overwrite_lang = tk.BooleanVar(value=False)

        # command preview / status
        self.status_var = tk.StringVar(value="Ready.")
        self.cmd_preview = tk.StringVar(value="")

        self._init_btg_path()
        self._build_ui()
        self._load_config_best_effort()
        self._refresh_cmd_preview()

        self.after(75, self._poll_logs)

    # -------------------------
    # UI construction
    # -------------------------
    def _build_ui(self) -> None:
        self.master.title(f"{APP_NAME} {APP_VERSION}")
        self.master.geometry(DEFAULT_GEOMETRY)

        style = ttk.Style()
        # "clam" looks consistent cross-platform; fall back silently if not available.
        try:
            style.theme_use("clam")
        except Exception:
            pass

        self.pack(fill="both", expand=True)

        self._build_menubar()

        # Top: Repo + btg path + python exe + global flags
        top = ttk.LabelFrame(self, text="Project", padding=10)
        top.pack(fill="x", padx=10, pady=10)

        self._row_dir(
            top, 0, "Repo root:", self.repo_root, browse_title="Select repo root"
        )
        self._row_file(
            top,
            1,
            "btg.py script:",
            self.btg_script,
            browse_title="Select btg.py",
            filetypes=[("Python", "*.py"), ("All files", "*.*")],
        )
        self._row_file(
            top,
            2,
            "Python exe:",
            self.python_exe,
            browse_title="Select Python executable",
            filetypes=[("Executables", "*.*")],
        )

        flags = ttk.Frame(top)
        flags.grid(row=3, column=0, columnspan=3, sticky="w", pady=(8, 0))

        ttk.Label(flags, text="Log level:").pack(side="left")
        ttk.Combobox(
            flags,
            textvariable=self.log_level,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            width=10,
            state="readonly",
        ).pack(side="left", padx=(6, 14))

        ttk.Checkbutton(
            flags, text="Global dry-run", variable=self.global_dry_run
        ).pack(side="left")

        ttk.Button(flags, text="Save Config", command=self.save_config).pack(
            side="left", padx=(16, 6)
        )
        ttk.Button(
            flags, text="Reload Config", command=self._load_config_best_effort
        ).pack(side="left")

        # Notebook
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tab_validate = ttk.Frame(nb)
        self.tab_normalize = ttk.Frame(nb)
        self.tab_extract = ttk.Frame(nb)
        self.tab_recolor = ttk.Frame(nb)
        self.tab_legacy = ttk.Frame(nb)
        self.tab_generate = ttk.Frame(nb)
        self.tab_autotemplate = ttk.Frame(nb)
        self.tab_assets = ttk.Frame(nb)

        nb.add(self.tab_validate, text="Validate")
        nb.add(self.tab_normalize, text="Normalize")
        nb.add(self.tab_extract, text="Extract")
        nb.add(self.tab_recolor, text="Recolor")
        nb.add(self.tab_legacy, text="Legacy Templates")
        nb.add(self.tab_generate, text="Generate")
        nb.add(self.tab_autotemplate, text="AutoTemplate")
        nb.add(self.tab_assets, text="Assets")

        self._build_validate_tab()
        self._build_normalize_tab()
        self._build_extract_tab()
        self._build_recolor_tab()
        self._build_legacy_tab()
        self._build_generate_tab()
        self._build_autotemplate_tab()
        self._build_assets_tab()

        # Command preview + run/stop
        runbar = ttk.LabelFrame(self, text="Run", padding=10)
        runbar.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(runbar, text="Command preview:").grid(row=0, column=0, sticky="w")
        preview = ttk.Entry(runbar, textvariable=self.cmd_preview, state="readonly")
        preview.grid(row=1, column=0, columnspan=4, sticky="we", pady=(6, 0))
        runbar.columnconfigure(0, weight=1)

        ttk.Button(runbar, text="Run Preview Command", command=self.run_preview).grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )
        ttk.Button(runbar, text="Stop", command=self.stop).grid(
            row=2, column=1, sticky="w", padx=(10, 0), pady=(10, 0)
        )
        ttk.Button(runbar, text="Clear Output", command=self.clear_output).grid(
            row=2, column=2, sticky="w", padx=(10, 0), pady=(10, 0)
        )

        # Output log + status
        bottom = ttk.LabelFrame(self, text="Output", padding=10)
        bottom.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(bottom, height=16, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        status = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status.pack(fill="x", padx=10, pady=(0, 8))

        # Refresh preview on changes
        for v in (
            self.repo_root,
            self.btg_script,
            self.python_exe,
            self.log_level,
            self.global_dry_run,
            self.val_schemas,
            self.val_palettes,
            self.norm_palettes,
            self.ext_textures,
            self.ext_palettes_out,
            self.ext_max_colors,
            self.ext_min_alpha,
            self.ext_schema_ref,
            self.ext_generator_version,
            self.rec_palettes_dir,
            self.rec_src_palette,
            self.rec_dst_palette,
            self.rec_src_id,
            self.rec_dst_id,
            self.rec_group,
            self.rec_input,
            self.rec_output,
            self.rec_no_recursive,
            self.rec_min_alpha,
            self.rec_alpha_weight,
            self.rec_preserve_alpha,
            self.rec_exact_first,
            self.leg_palettes_dir,
            self.leg_templates_dir,
            self.leg_output_root,
            self.leg_namespace,
            self.leg_lang_file,
            self.leg_no_modid_tree,
            self.leg_no_flat_tree,
            self.gen_templates,
            self.gen_palettes,
            self.gen_output,
            self.gen_min_alpha,
            self.gen_alpha_weight,
            self.gen_preserve_alpha,
            self.gen_exact_first,
            self.gen_limit,
            self.at_templates,
            self.at_palettes,
            self.at_out_dir,
            self.at_materials,
            self.at_min_alpha,
            self.at_min_hits,
            self.as_textures,
            self.as_recursive,
            self.as_items_dir,
            self.as_models_dir,
            self.as_lang,
            self.as_namespace,
            self.as_overwrite_lang,
        ):
            try:
                v.trace_add("write", lambda *_: self._refresh_cmd_preview())
            except Exception:
                pass

    def _build_menubar(self) -> None:
        mb = tk.Menu(self.master)

        filem = tk.Menu(mb, tearoff=False)
        filem.add_command(label="Save Config", command=self.save_config)
        filem.add_command(label="Save Config As…", command=self.save_config_as)
        filem.add_command(label="Reload Config", command=self._load_config_best_effort)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.master.destroy)
        mb.add_cascade(label="File", menu=filem)

        toolsm = tk.Menu(mb, tearoff=False)
        toolsm.add_command(
            label="Open Repo Root",
            command=lambda: self._open_path(self.repo_root.get()),
        )
        toolsm.add_command(label="Open Output Folder", command=self.open_output_folder)
        toolsm.add_separator()
        toolsm.add_command(
            label="Copy Preview Command", command=self.copy_preview_command
        )
        mb.add_cascade(label="Tools", menu=toolsm)

        helpm = tk.Menu(mb, tearoff=False)
        helpm.add_command(label="About", command=self.about)
        mb.add_cascade(label="Help", menu=helpm)

        self.master.config(menu=mb)

    def _row_dir(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        var: tk.StringVar,
        *,
        browse_title: str,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=80).grid(
            row=row, column=1, sticky="we", padx=8
        )
        ttk.Button(
            parent,
            text="Browse…",
            command=lambda: self._browse_dir(var, title=browse_title),
        ).grid(row=row, column=2, sticky="w")
        parent.columnconfigure(1, weight=1)

    def _row_file(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        var: tk.StringVar,
        *,
        browse_title: str,
        filetypes: List[Tuple[str, str]],
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=80).grid(
            row=row, column=1, sticky="we", padx=8
        )
        ttk.Button(
            parent,
            text="Browse…",
            command=lambda: self._browse_file(
                var, title=browse_title, filetypes=filetypes
            ),
        ).grid(row=row, column=2, sticky="w")
        parent.columnconfigure(1, weight=1)

    def _row_text(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        var: tk.StringVar,
        *,
        width: int = 70,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=width).grid(
            row=row, column=1, sticky="w", padx=8
        )

    def _row_bool(
        self, parent: ttk.Frame, row: int, text: str, var: tk.BooleanVar
    ) -> None:
        ttk.Checkbutton(parent, text=text, variable=var).grid(
            row=row, column=0, sticky="w", pady=(6, 0)
        )

    # -------------------------
    # Tabs
    # -------------------------
    def _build_validate_tab(self) -> None:
        f = ttk.Frame(self.tab_validate, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Schemas dir:",
            self.val_schemas,
            browse_title="Select schemas directory",
        )
        self._row_dir(
            f,
            1,
            "Palettes dir:",
            self.val_palettes,
            browse_title="Select palettes directory",
        )

        ttk.Button(f, text="Run Validate", command=self.run_validate).grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

    def _build_normalize_tab(self) -> None:
        f = ttk.Frame(self.tab_normalize, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Palettes dir:",
            self.norm_palettes,
            browse_title="Select palettes directory",
        )
        ttk.Button(f, text="Run Normalize", command=self.run_normalize).grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

    def _build_extract_tab(self) -> None:
        f = ttk.Frame(self.tab_extract, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Textures dir:",
            self.ext_textures,
            browse_title="Select textures directory",
        )
        self._row_dir(
            f,
            1,
            "Palettes output dir:",
            self.ext_palettes_out,
            browse_title="Select output palettes directory",
        )

        self._row_text(f, 2, "Max colors:", self.ext_max_colors, width=12)
        self._row_text(f, 3, "Min alpha:", self.ext_min_alpha, width=12)
        self._row_text(f, 4, "$schema ref:", self.ext_schema_ref, width=70)
        self._row_text(f, 5, "Generator version:", self.ext_generator_version, width=18)

        ttk.Button(f, text="Run Extract", command=self.run_extract).grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )

    def _build_recolor_tab(self) -> None:
        f = ttk.Frame(self.tab_recolor, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Palettes dir:",
            self.rec_palettes_dir,
            browse_title="Select palettes directory",
        )
        self._row_text(f, 1, "Source palette (rel):", self.rec_src_palette, width=70)
        self._row_text(f, 2, "Target palette (rel):", self.rec_dst_palette, width=70)
        self._row_text(f, 3, "Source id:", self.rec_src_id, width=20)
        self._row_text(f, 4, "Target id:", self.rec_dst_id, width=20)
        self._row_text(f, 5, "Group (blank=auto):", self.rec_group, width=20)

        self._row_dir(
            f, 6, "Input dir:", self.rec_input, browse_title="Select input directory"
        )
        self._row_dir(
            f, 7, "Output dir:", self.rec_output, browse_title="Select output directory"
        )

        ttk.Checkbutton(
            f, text="No recursive input scan", variable=self.rec_no_recursive
        ).grid(row=8, column=0, sticky="w", pady=(10, 0))

        self._row_text(f, 9, "Min alpha:", self.rec_min_alpha, width=12)
        self._row_text(f, 10, "Alpha weight:", self.rec_alpha_weight, width=12)

        ttk.Checkbutton(
            f, text="Preserve original alpha", variable=self.rec_preserve_alpha
        ).grid(row=11, column=0, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            f, text="Exact-match first", variable=self.rec_exact_first
        ).grid(row=12, column=0, sticky="w", pady=(6, 0))

        ttk.Button(f, text="Run Recolor", command=self.run_recolor).grid(
            row=13, column=0, sticky="w", pady=(10, 0)
        )

    def _build_legacy_tab(self) -> None:
        f = ttk.Frame(self.tab_legacy, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Palettes dir:",
            self.leg_palettes_dir,
            browse_title="Select palettes directory",
        )
        self._row_dir(
            f,
            1,
            "Templates dir:",
            self.leg_templates_dir,
            browse_title="Select templates directory",
        )
        self._row_dir(
            f,
            2,
            "Output root:",
            self.leg_output_root,
            browse_title="Select output root directory",
        )
        self._row_text(f, 3, "Namespace/modid:", self.leg_namespace, width=20)
        self._row_text(f, 4, "Lang file:", self.leg_lang_file, width=20)

        ttk.Checkbutton(
            f,
            text="Disable output/<namespace>/... tree",
            variable=self.leg_no_modid_tree,
        ).grid(row=5, column=0, sticky="w", pady=(10, 0))
        ttk.Checkbutton(
            f, text="Disable flat output/... tree", variable=self.leg_no_flat_tree
        ).grid(row=6, column=0, sticky="w", pady=(6, 0))

        ttk.Button(
            f, text="Run Legacy recolor-templates", command=self.run_legacy_templates
        ).grid(row=7, column=0, sticky="w", pady=(10, 0))

    def _build_generate_tab(self) -> None:
        f = ttk.Frame(self.tab_generate, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Templates dir:",
            self.gen_templates,
            browse_title="Select templates directory",
        )
        self._row_dir(
            f,
            1,
            "Palettes dir:",
            self.gen_palettes,
            browse_title="Select palettes directory",
        )
        self._row_dir(
            f, 2, "Output dir:", self.gen_output, browse_title="Select output directory"
        )

        self._row_text(f, 3, "Min alpha:", self.gen_min_alpha, width=12)
        self._row_text(f, 4, "Alpha weight:", self.gen_alpha_weight, width=12)
        self._row_text(f, 5, "Limit (blank=none):", self.gen_limit, width=12)

        ttk.Checkbutton(
            f, text="Preserve alpha", variable=self.gen_preserve_alpha
        ).grid(row=6, column=0, sticky="w", pady=(10, 0))
        ttk.Checkbutton(
            f, text="Exact-match first", variable=self.gen_exact_first
        ).grid(row=7, column=0, sticky="w", pady=(6, 0))

        ttk.Button(f, text="Run Generate", command=self.run_generate).grid(
            row=8, column=0, sticky="w", pady=(10, 0)
        )

    def _build_autotemplate_tab(self) -> None:
        f = ttk.Frame(self.tab_autotemplate, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Templates dir (*.png):",
            self.at_templates,
            browse_title="Select templates directory",
        )
        self._row_dir(
            f,
            1,
            "Palettes dir:",
            self.at_palettes,
            browse_title="Select palettes directory",
        )
        self._row_text(f, 2, "Out dir (blank=templates):", self.at_out_dir, width=70)
        self._row_text(f, 3, "Materials (comma list):", self.at_materials, width=70)
        self._row_text(f, 4, "Min alpha:", self.at_min_alpha, width=12)
        self._row_text(f, 5, "Min hits:", self.at_min_hits, width=12)

        ttk.Button(f, text="Run AutoTemplate", command=self.run_autotemplate).grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )

    def _build_assets_tab(self) -> None:
        f = ttk.Frame(self.tab_assets, padding=10)
        f.pack(fill="x")

        self._row_dir(
            f,
            0,
            "Textures dir:",
            self.as_textures,
            browse_title="Select textures directory",
        )
        ttk.Checkbutton(
            f, text="Recurse textures dir", variable=self.as_recursive
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self._row_dir(
            f,
            2,
            "Items dir:",
            self.as_items_dir,
            browse_title="Select items output directory",
        )
        self._row_dir(
            f,
            3,
            "Models/item dir:",
            self.as_models_dir,
            browse_title="Select models output directory",
        )
        self._row_text(f, 4, "Lang file:", self.as_lang, width=70)
        self._row_text(f, 5, "Namespace/modid:", self.as_namespace, width=20)

        ttk.Checkbutton(
            f, text="Overwrite existing lang keys", variable=self.as_overwrite_lang
        ).grid(row=6, column=0, sticky="w", pady=(10, 0))

        ttk.Button(f, text="Run Assets", command=self.run_assets).grid(
            row=7, column=0, sticky="w", pady=(10, 0)
        )

    # -------------------------
    # Browse helpers
    # -------------------------
    def _browse_dir(self, var: tk.StringVar, *, title: str) -> None:
        start = self._abs_repo()
        p = filedialog.askdirectory(title=title, initialdir=str(start))
        if not p:
            return
        repo = self._abs_repo()
        var.set(_try_rel(repo, Path(p)))
        self._maybe_update_btg_guess()

    def _browse_file(
        self, var: tk.StringVar, *, title: str, filetypes: List[Tuple[str, str]]
    ) -> None:
        start = self._abs_repo()
        p = filedialog.askopenfilename(
            title=title, initialdir=str(start), filetypes=filetypes
        )
        if not p:
            return
        repo = self._abs_repo()
        var.set(_try_rel(repo, Path(p)))
        self._maybe_update_btg_guess()

    # -------------------------
    # Config
    # -------------------------
    def _config_path_repo(self) -> Path:
        repo = self._abs_repo()
        return repo / REPO_CONFIG_NAME

    def _config_path_home(self) -> Path:
        return Path.home() / HOME_CONFIG_NAME

    def _pick_config_path_for_save(self) -> Path:
        repo_cfg = self._config_path_repo()
        try:
            repo = self._abs_repo()
            if repo.exists():
                # if we can create/overwrite in repo, prefer that
                if repo_cfg.exists() or os.access(str(repo), os.W_OK):
                    return repo_cfg
        except Exception:
            pass
        return self._config_path_home()

    def _load_config_best_effort(self) -> None:
        # prefer repo config, fall back to home
        candidates = [self._config_path_repo(), self._config_path_home()]
        for p in candidates:
            try:
                if p.exists():
                    data = json.loads(p.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        self._apply_config(data)
                        self._log(f"Loaded config: {p.as_posix()}")
                        self.status_var.set(f"Loaded config: {p.as_posix()}")
                        self._refresh_cmd_preview()
                        return
            except Exception as e:
                self._log(f"Failed to load config {p.as_posix()}: {e}")
        self.status_var.set("No config found; using defaults.")
        self._refresh_cmd_preview()

    def save_config(self) -> None:
        path = self._pick_config_path_for_save()
        try:
            self._write_config(path)
            self._log(f"Saved config: {path.as_posix()}")
            self.status_var.set(f"Saved config: {path.as_posix()}")
        except Exception as e:
            messagebox.showerror("Save Config Failed", str(e))

    def save_config_as(self) -> None:
        repo = self._abs_repo()
        p = filedialog.asksaveasfilename(
            title="Save BTG GUI config",
            initialdir=str(repo),
            initialfile=REPO_CONFIG_NAME,
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All files", "*.*")],
        )
        if not p:
            return
        try:
            self._write_config(Path(p))
            self._log(f"Saved config: {Path(p).as_posix()}")
            self.status_var.set(f"Saved config: {Path(p).as_posix()}")
        except Exception as e:
            messagebox.showerror("Save Config Failed", str(e))

    def _write_config(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self._collect_config()
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    def _collect_config(self) -> Dict[str, Any]:
        return {
            "app": {"name": APP_NAME, "version": APP_VERSION},
            "project": {
                "repo_root": self.repo_root.get(),
                "btg_script": self.btg_script.get(),
                "python_exe": self.python_exe.get(),
                "log_level": self.log_level.get(),
                "dry_run": bool(self.global_dry_run.get()),
            },
            "validate": {
                "schemas": self.val_schemas.get(),
                "palettes": self.val_palettes.get(),
            },
            "normalize": {"palettes": self.norm_palettes.get()},
            "extract": {
                "textures": self.ext_textures.get(),
                "palettes_out": self.ext_palettes_out.get(),
                "max_colors": self.ext_max_colors.get(),
                "min_alpha": self.ext_min_alpha.get(),
                "schema_ref": self.ext_schema_ref.get(),
                "generator_version": self.ext_generator_version.get(),
            },
            "recolor": {
                "palettes_dir": self.rec_palettes_dir.get(),
                "src_palette": self.rec_src_palette.get(),
                "dst_palette": self.rec_dst_palette.get(),
                "src_id": self.rec_src_id.get(),
                "dst_id": self.rec_dst_id.get(),
                "group": self.rec_group.get(),
                "input": self.rec_input.get(),
                "output": self.rec_output.get(),
                "no_recursive": bool(self.rec_no_recursive.get()),
                "min_alpha": self.rec_min_alpha.get(),
                "alpha_weight": self.rec_alpha_weight.get(),
                "preserve_alpha": bool(self.rec_preserve_alpha.get()),
                "exact_first": bool(self.rec_exact_first.get()),
            },
            "legacy_templates": {
                "palettes_dir": self.leg_palettes_dir.get(),
                "templates_dir": self.leg_templates_dir.get(),
                "output_root": self.leg_output_root.get(),
                "namespace": self.leg_namespace.get(),
                "lang_file": self.leg_lang_file.get(),
                "no_modid_tree": bool(self.leg_no_modid_tree.get()),
                "no_flat_tree": bool(self.leg_no_flat_tree.get()),
            },
            "generate": {
                "templates": self.gen_templates.get(),
                "palettes": self.gen_palettes.get(),
                "output": self.gen_output.get(),
                "min_alpha": self.gen_min_alpha.get(),
                "alpha_weight": self.gen_alpha_weight.get(),
                "preserve_alpha": bool(self.gen_preserve_alpha.get()),
                "exact_first": bool(self.gen_exact_first.get()),
                "limit": self.gen_limit.get(),
            },
            "autotemplate": {
                "templates": self.at_templates.get(),
                "palettes": self.at_palettes.get(),
                "out_dir": self.at_out_dir.get(),
                "materials": self.at_materials.get(),
                "min_alpha": self.at_min_alpha.get(),
                "min_hits": self.at_min_hits.get(),
            },
            "assets": {
                "textures": self.as_textures.get(),
                "recursive": bool(self.as_recursive.get()),
                "items_dir": self.as_items_dir.get(),
                "models_dir": self.as_models_dir.get(),
                "lang": self.as_lang.get(),
                "namespace": self.as_namespace.get(),
                "overwrite_lang": bool(self.as_overwrite_lang.get()),
            },
        }

    def _apply_config(self, data: Dict[str, Any]) -> None:
        proj = data.get("project") or {}
        self.repo_root.set(str(proj.get("repo_root") or self.repo_root.get()))
        self.btg_script.set(str(proj.get("btg_script") or self.btg_script.get()))
        self.python_exe.set(str(proj.get("python_exe") or self.python_exe.get()))
        self.log_level.set(str(proj.get("log_level") or self.log_level.get()))
        self.global_dry_run.set(bool(proj.get("dry_run", self.global_dry_run.get())))

        val = data.get("validate") or {}
        self.val_schemas.set(str(val.get("schemas") or self.val_schemas.get()))
        self.val_palettes.set(str(val.get("palettes") or self.val_palettes.get()))

        norm = data.get("normalize") or {}
        self.norm_palettes.set(str(norm.get("palettes") or self.norm_palettes.get()))

        ext = data.get("extract") or {}
        self.ext_textures.set(str(ext.get("textures") or self.ext_textures.get()))
        self.ext_palettes_out.set(
            str(ext.get("palettes_out") or self.ext_palettes_out.get())
        )
        self.ext_max_colors.set(str(ext.get("max_colors") or self.ext_max_colors.get()))
        self.ext_min_alpha.set(str(ext.get("min_alpha") or self.ext_min_alpha.get()))
        self.ext_schema_ref.set(str(ext.get("schema_ref") or self.ext_schema_ref.get()))
        self.ext_generator_version.set(
            str(ext.get("generator_version") or self.ext_generator_version.get())
        )

        rec = data.get("recolor") or {}
        self.rec_palettes_dir.set(
            str(rec.get("palettes_dir") or self.rec_palettes_dir.get())
        )
        self.rec_src_palette.set(
            str(rec.get("src_palette") or self.rec_src_palette.get())
        )
        self.rec_dst_palette.set(
            str(rec.get("dst_palette") or self.rec_dst_palette.get())
        )
        self.rec_src_id.set(str(rec.get("src_id") or self.rec_src_id.get()))
        self.rec_dst_id.set(str(rec.get("dst_id") or self.rec_dst_id.get()))
        self.rec_group.set(str(rec.get("group") or self.rec_group.get()))
        self.rec_input.set(str(rec.get("input") or self.rec_input.get()))
        self.rec_output.set(str(rec.get("output") or self.rec_output.get()))
        self.rec_no_recursive.set(
            bool(rec.get("no_recursive", self.rec_no_recursive.get()))
        )
        self.rec_min_alpha.set(str(rec.get("min_alpha") or self.rec_min_alpha.get()))
        self.rec_alpha_weight.set(
            str(rec.get("alpha_weight") or self.rec_alpha_weight.get())
        )
        self.rec_preserve_alpha.set(
            bool(rec.get("preserve_alpha", self.rec_preserve_alpha.get()))
        )
        self.rec_exact_first.set(
            bool(rec.get("exact_first", self.rec_exact_first.get()))
        )

        leg = data.get("legacy_templates") or {}
        self.leg_palettes_dir.set(
            str(leg.get("palettes_dir") or self.leg_palettes_dir.get())
        )
        self.leg_templates_dir.set(
            str(leg.get("templates_dir") or self.leg_templates_dir.get())
        )
        self.leg_output_root.set(
            str(leg.get("output_root") or self.leg_output_root.get())
        )
        self.leg_namespace.set(str(leg.get("namespace") or self.leg_namespace.get()))
        self.leg_lang_file.set(str(leg.get("lang_file") or self.leg_lang_file.get()))
        self.leg_no_modid_tree.set(
            bool(leg.get("no_modid_tree", self.leg_no_modid_tree.get()))
        )
        self.leg_no_flat_tree.set(
            bool(leg.get("no_flat_tree", self.leg_no_flat_tree.get()))
        )

        gen = data.get("generate") or {}
        self.gen_templates.set(str(gen.get("templates") or self.gen_templates.get()))
        self.gen_palettes.set(str(gen.get("palettes") or self.gen_palettes.get()))
        self.gen_output.set(str(gen.get("output") or self.gen_output.get()))
        self.gen_min_alpha.set(str(gen.get("min_alpha") or self.gen_min_alpha.get()))
        self.gen_alpha_weight.set(
            str(gen.get("alpha_weight") or self.gen_alpha_weight.get())
        )
        self.gen_preserve_alpha.set(
            bool(gen.get("preserve_alpha", self.gen_preserve_alpha.get()))
        )
        self.gen_exact_first.set(
            bool(gen.get("exact_first", self.gen_exact_first.get()))
        )
        self.gen_limit.set(str(gen.get("limit") or self.gen_limit.get()))

        at = data.get("autotemplate") or {}
        self.at_templates.set(str(at.get("templates") or self.at_templates.get()))
        self.at_palettes.set(str(at.get("palettes") or self.at_palettes.get()))
        self.at_out_dir.set(str(at.get("out_dir") or self.at_out_dir.get()))
        self.at_materials.set(str(at.get("materials") or self.at_materials.get()))
        self.at_min_alpha.set(str(at.get("min_alpha") or self.at_min_alpha.get()))
        self.at_min_hits.set(str(at.get("min_hits") or self.at_min_hits.get()))

        aset = data.get("assets") or {}
        self.as_textures.set(str(aset.get("textures") or self.as_textures.get()))
        self.as_recursive.set(bool(aset.get("recursive", self.as_recursive.get())))
        self.as_items_dir.set(str(aset.get("items_dir") or self.as_items_dir.get()))
        self.as_models_dir.set(str(aset.get("models_dir") or self.as_models_dir.get()))
        self.as_lang.set(str(aset.get("lang") or self.as_lang.get()))
        self.as_namespace.set(str(aset.get("namespace") or self.as_namespace.get()))
        self.as_overwrite_lang.set(
            bool(aset.get("overwrite_lang", self.as_overwrite_lang.get()))
        )

        self._maybe_update_btg_guess()

    # -------------------------
    # Command builders
    # -------------------------
    def _global_args(self) -> List[str]:
        out = ["--log", self.log_level.get().strip() or "INFO"]
        if self.global_dry_run.get():
            out.append("--dry-run")
        return out

    def _cmd_validate(self) -> List[str]:
        return [
            "validate",
            "--schemas",
            self.val_schemas.get(),
            "--palettes",
            self.val_palettes.get(),
        ]

    def _cmd_normalize(self) -> List[str]:
        return ["normalize", "--palettes", self.norm_palettes.get()]

    def _cmd_extract(self) -> List[str]:
        max_colors = str(_safe_int(self.ext_max_colors.get(), 32))
        min_alpha = str(_safe_int(self.ext_min_alpha.get(), 1))
        argv = [
            "extract",
            "--textures",
            self.ext_textures.get(),
            "--palettes",
            self.ext_palettes_out.get(),
            "--max-colors",
            max_colors,
            "--min-alpha",
            min_alpha,
            "--schema-ref",
            self.ext_schema_ref.get().strip()
            or "../../schemas/texture-palettes.schema.json",
            "--generator-version",
            self.ext_generator_version.get().strip() or "1.0.0",
        ]
        return argv

    def _cmd_recolor(self) -> List[str]:
        argv = [
            "recolor",
            "--palettes",
            self.rec_palettes_dir.get(),
            "--src-palette",
            self.rec_src_palette.get(),
            "--dst-palette",
            self.rec_dst_palette.get(),
            "--src-id",
            self.rec_src_id.get(),
            "--dst-id",
            self.rec_dst_id.get(),
            "--input",
            self.rec_input.get(),
            "--output",
            self.rec_output.get(),
            "--min-alpha",
            str(_safe_int(self.rec_min_alpha.get(), 1)),
            "--alpha-weight",
            str(_safe_float(self.rec_alpha_weight.get(), 0.25)),
        ]

        group = self.rec_group.get().strip()
        if group:
            argv += ["--group", group]

        if self.rec_no_recursive.get():
            argv += ["--no-recursive"]
        if not self.rec_preserve_alpha.get():
            argv += ["--no-preserve-alpha"]
        if not self.rec_exact_first.get():
            argv += ["--no-exact-first"]

        return argv

    def _cmd_legacy_templates(self) -> List[str]:
        argv = [
            "recolor-templates",
            "--palettes",
            self.leg_palettes_dir.get(),
            "--templates",
            self.leg_templates_dir.get(),
            "--output-root",
            self.leg_output_root.get(),
            "--namespace",
            self.leg_namespace.get().strip() or "modid",
            "--lang-file",
            self.leg_lang_file.get().strip() or "en_us.json",
        ]
        if self.leg_no_modid_tree.get():
            argv.append("--no-modid-tree")
        if self.leg_no_flat_tree.get():
            argv.append("--no-flat-tree")
        return argv

    def _cmd_generate(self) -> List[str]:
        argv = [
            "generate",
            "--templates",
            self.gen_templates.get(),
            "--palettes",
            self.gen_palettes.get(),
            "--output",
            self.gen_output.get(),
            "--min-alpha",
            str(_safe_int(self.gen_min_alpha.get(), 1)),
            "--alpha-weight",
            str(_safe_float(self.gen_alpha_weight.get(), 0.25)),
        ]
        if not self.gen_preserve_alpha.get():
            argv += ["--no-preserve-alpha"]
        if not self.gen_exact_first.get():
            argv += ["--no-exact-first"]

        lim = self.gen_limit.get().strip()
        if lim:
            argv += ["--limit", str(_safe_int(lim, 0))]

        return argv

    def _cmd_autotemplate(self) -> List[str]:
        argv = [
            "autotemplate",
            "--templates",
            self.at_templates.get(),
            "--palettes",
            self.at_palettes.get(),
            "--materials",
            self.at_materials.get().strip() or "wood,metal,glass",
            "--min-alpha",
            str(_safe_int(self.at_min_alpha.get(), 1)),
            "--min-hits",
            str(_safe_int(self.at_min_hits.get(), 2)),
        ]
        out_dir = self.at_out_dir.get().strip()
        if out_dir:
            argv += ["--out-dir", out_dir]
        return argv

    def _cmd_assets(self) -> List[str]:
        argv = [
            "assets",
            "--textures",
            self.as_textures.get(),
            "--items-dir",
            self.as_items_dir.get(),
            "--models-dir",
            self.as_models_dir.get(),
            "--lang",
            self.as_lang.get().strip() or "output/lang/en_us.json",
            "--namespace",
            self.as_namespace.get().strip() or "modid",
        ]
        if self.as_recursive.get():
            argv += ["--recursive"]
        if self.as_overwrite_lang.get():
            argv += ["--overwrite-lang"]
        return argv

    # -------------------------
    # Preview selection logic
    # -------------------------
    def _refresh_cmd_preview(self) -> None:
        # Pick a sane default preview command:
        # If user has touched a specific tab, they can still run from that tab button,
        # but the preview/run bar will default to "validate".
        # (Users can copy/edit it externally anyway.)
        # Here we keep it simple: show validate command by default.
        argv = self._compose_full_command(self._cmd_validate())
        self.cmd_preview.set(self._format_cmd(argv))

    def _compose_full_command(self, btg_argv: List[str]) -> List[str]:
        repo = self._abs_repo()
        btg = self._abs_btg_script()
        py = self._abs_python_exe()

        # Always run: <python> <btg.py> [global flags] <cmd...>
        out = [str(py), str(btg)]
        out.extend(self._global_args())
        out.extend(btg_argv)
        # Store normalized preview for readability
        return [str(x) for x in out]

    def _format_cmd(self, argv: Sequence[str]) -> str:
        # Pretty command string with safe quoting
        try:
            return " ".join(shlex.quote(a) for a in argv)
        except Exception:
            return " ".join(argv)

    # -------------------------
    # Run actions (tab buttons)
    # -------------------------
    def run_validate(self) -> None:
        self._run(self._cmd_validate(), label="validate")

    def run_normalize(self) -> None:
        self._run(self._cmd_normalize(), label="normalize")

    def run_extract(self) -> None:
        self._run(self._cmd_extract(), label="extract")

    def run_recolor(self) -> None:
        self._run(self._cmd_recolor(), label="recolor")

    def run_legacy_templates(self) -> None:
        self._run(self._cmd_legacy_templates(), label="recolor-templates")

    def run_generate(self) -> None:
        self._run(self._cmd_generate(), label="generate")

    def run_autotemplate(self) -> None:
        self._run(self._cmd_autotemplate(), label="autotemplate")

    def run_assets(self) -> None:
        self._run(self._cmd_assets(), label="assets")

    def run_preview(self) -> None:
        # Run whatever the preview currently shows, but only if it matches our expected python+btg.
        # This keeps it safe and avoids arbitrary shell execution.
        # Use validate as a fallback.
        try:
            self._run(self._cmd_validate(), label="preview(validate)")
        except Exception:
            self._run(self._cmd_validate(), label="preview(validate)")

    # -------------------------
    # Process execution
    # -------------------------
    def _run(self, btg_argv: List[str], *, label: str) -> None:
        if self._proc.popen is not None:
            messagebox.showwarning("Busy", "A task is already running. Stop it first.")
            return

        repo = self._abs_repo()
        btg = self._abs_btg_script()
        py = self._abs_python_exe()

        if not repo.exists():
            messagebox.showerror("Invalid repo", "Repo root does not exist.")
            return
        if not btg.exists():
            messagebox.showerror(
                "Missing btg.py", f"btg.py not found: {btg.as_posix()}"
            )
            return
        if not py.exists():
            messagebox.showerror(
                "Missing Python", f"Python executable not found: {py.as_posix()}"
            )
            return

        full = self._compose_full_command(btg_argv)
        self._log(f"[{_now_ts()}] INFO: Running ({label}): {self._format_cmd(full)}")
        self._log(f"[{_now_ts()}] INFO: cwd: {repo.as_posix()}")

        creationflags = 0
        if _is_windows():
            # allow CTRL_BREAK_EVENT / better termination behavior
            creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

        def worker() -> None:
            try:
                self.status_var.set(f"Running: {label}")
                self._proc.popen = subprocess.Popen(
                    full,
                    cwd=str(repo),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    universal_newlines=True,
                    creationflags=creationflags,
                )
                assert self._proc.popen.stdout is not None
                for line in self._proc.popen.stdout:
                    self._log(line.rstrip("\n"))
                rc = self._proc.popen.wait()
                self._log(f"[{_now_ts()}] INFO: Process exited with code {rc}")
            except Exception as e:
                self._log(f"[{_now_ts()}] ERROR: {e}")
            finally:
                self._proc.popen = None
                self.status_var.set("Ready.")

        self._proc.thread = threading.Thread(target=worker, daemon=True)
        self._proc.thread.start()

    def stop(self) -> None:
        p = self._proc.popen
        if p is None:
            self._log(f"[{_now_ts()}] INFO: No process running.")
            return

        self._log(f"[{_now_ts()}] INFO: Stop requested.")
        try:
            p.terminate()
        except Exception as e:
            self._log(f"[{_now_ts()}] ERROR: terminate failed: {e}")
            return

        # If it doesn't exit soon, kill it.
        def killer() -> None:
            for _ in range(30):
                if self._proc.popen is None:
                    return
                if p.poll() is not None:
                    return
                time.sleep(0.1)
            try:
                self._log(f"[{_now_ts()}] WARNING: Forcing kill.")
                p.kill()
            except Exception as e:
                self._log(f"[{_now_ts()}] ERROR: kill failed: {e}")

        threading.Thread(target=killer, daemon=True).start()

    # -------------------------
    # Logging
    # -------------------------
    def _log(self, msg: str) -> None:
        try:
            self._log_q.put_nowait(msg)
        except Exception:
            pass

    def _poll_logs(self) -> None:
        try:
            while True:
                line = self._log_q.get_nowait()
                self.log_text.insert("end", line + "\n")
                self.log_text.see("end")
        except queue.Empty:
            pass
        self.after(75, self._poll_logs)

    def clear_output(self) -> None:
        self.log_text.delete("1.0", "end")
        self.status_var.set("Output cleared.")

    # -------------------------
    # Utilities
    # -------------------------
    def _abs_repo(self) -> Path:
        s = self.repo_root.get().strip() or str(Path.cwd())
        return Path(s).expanduser().resolve()

    def _abs_btg_script(self) -> Path:
        repo = self._abs_repo()
        s = self.btg_script.get().strip()
        if not s:
            guess = _guess_btg_script(repo)
            if guess is not None:
                return guess
            return (repo / "tools" / "btg.py").resolve()
        p = Path(s).expanduser()
        return (repo / p).resolve() if not p.is_absolute() else p.resolve()

    def _abs_python_exe(self) -> Path:
        s = self.python_exe.get().strip() or sys.executable
        return Path(s).expanduser().resolve()

    def _init_btg_path(self) -> None:
        repo = self._abs_repo()
        guess = _guess_btg_script(repo)
        if guess is not None:
            self.btg_script.set(_try_rel(repo, guess))
        else:
            # keep empty; user can browse
            self.btg_script.set("")

    def _maybe_update_btg_guess(self) -> None:
        # If btg is empty or invalid, re-guess based on repo_root.
        try:
            repo = self._abs_repo()
            current = self._abs_btg_script()
            if not current.exists():
                guess = _guess_btg_script(repo)
                if guess is not None:
                    self.btg_script.set(_try_rel(repo, guess))
        except Exception:
            pass

    def copy_preview_command(self) -> None:
        cmd = self.cmd_preview.get().strip()
        if not cmd:
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(cmd)
        self.status_var.set("Copied preview command to clipboard.")

    def open_output_folder(self) -> None:
        # Heuristic: prefer "output" under repo
        repo = self._abs_repo()
        out = repo / "output"
        if out.exists():
            _open_in_file_manager(out)
            return
        _open_in_file_manager(repo)

    def _open_path(self, p: str) -> None:
        try:
            repo = self._abs_repo()
            path = Path(p).expanduser()
            abs_p = (
                (repo / path).resolve() if not path.is_absolute() else path.resolve()
            )
            if abs_p.exists():
                _open_in_file_manager(abs_p if abs_p.is_dir() else abs_p.parent)
            else:
                messagebox.showinfo(
                    "Not found", f"Path does not exist:\n{abs_p.as_posix()}"
                )
        except Exception as e:
            messagebox.showerror("Open failed", str(e))

    def about(self) -> None:
        messagebox.showinfo(
            "About",
            f"{APP_NAME}\nVersion: {APP_VERSION}\n\n"
            "Tkinter GUI for running btg.py commands with live log output.",
        )


def main() -> None:
    root = tk.Tk()
    app = BTGGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()

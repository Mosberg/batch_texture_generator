from __future__ import annotations

import shlex
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, Optional

from . import commands
from .commands import Project
from .config import load_config_best_effort, pick_config_path_for_save, save_config
from .constants import APP_NAME, APP_VERSION, DEFAULT_GEOMETRY
from .paths import find_repo_root, guess_btg_script, open_in_file_manager, try_rel
from .runner import ProcessRunner


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


class BTGGuiApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master

        self.repo_root = tk.StringVar(value=str(find_repo_root(Path.cwd())))
        self.btg_script = tk.StringVar(value="")
        self.python_exe = tk.StringVar(value=sys.executable)
        self.log_level = tk.StringVar(value="INFO")
        self.global_dry_run = tk.BooleanVar(value=False)

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
        self.ext_schema_ref = tk.StringVar(value="../../schemas/texture-palettes.schema.json")
        self.ext_generator_version = tk.StringVar(value="1.0.0")

        # Recolor
        self.rec_palettes_dir = tk.StringVar(value="palettes")
        self.rec_src_palette = tk.StringVar(value="wood/oak.texture-palettes.json")
        self.rec_dst_palette = tk.StringVar(value="metal/iron.texture-palettes.json")
        self.rec_src_id = tk.StringVar(value="oak")
        self.rec_dst_id = tk.StringVar(value="iron")
        self.rec_group = tk.StringVar(value="")
        self.rec_input = tk.StringVar(value="textures_input")
        self.rec_output = tk.StringVar(value="output/textures/item")
        self.rec_no_recursive = tk.BooleanVar(value=False)
        self.rec_min_alpha = tk.StringVar(value="1")
        self.rec_alpha_weight = tk.StringVar(value="0.25")
        self.rec_preserve_alpha = tk.BooleanVar(value=True)
        self.rec_exact_first = tk.BooleanVar(value=True)

        # Legacy templates
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
        self.gen_limit = tk.StringVar(value="")

        # AutoTemplate
        self.at_templates = tk.StringVar(value="textures_input")
        self.at_palettes = tk.StringVar(value="palettes")
        self.at_out_dir = tk.StringVar(value="")
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

        self.cmd_preview = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="Ready.")

        self._last_cmd: Optional[list[str]] = None

        self._init_btg_path()

        self._runner = ProcessRunner(on_log=self._log, on_exit=self._on_exit)

        self._build_ui()
        self._load_config()
        self._update_preview()

        self.after(75, self._tick)

    # -------------------------
    # Lifecycle
    # -------------------------
    def _init_btg_path(self) -> None:
        repo = Path(self.repo_root.get())
        guess = guess_btg_script(repo)
        if guess is not None:
            self.btg_script.set(try_rel(repo, guess))

    def _tick(self) -> None:
        self._runner.poll_logs()
        self.after(75, self._tick)

    def _project(self) -> Project:
        repo_root = Path(self.repo_root.get()).resolve()
        btg = Path(self.btg_script.get())
        if not btg.is_absolute():
            btg = (repo_root / btg).resolve()
        py = Path(self.python_exe.get()).resolve()

        return Project(
            repo_root=repo_root,
            btg_script=btg,
            python_exe=py,
            log_level=self.log_level.get(),
            dry_run=bool(self.global_dry_run.get()),
        )

    def _cwd(self) -> str:
        return str(Path(self.repo_root.get()).resolve())

    # -------------------------
    # UI
    # -------------------------
    def _build_ui(self) -> None:
        self.master.title(f"{APP_NAME} {APP_VERSION}")
        self.master.geometry(DEFAULT_GEOMETRY)

        try:
            ttk.Style().theme_use("clam")
        except Exception:
            pass

        self.pack(fill="both", expand=True)

        self._build_menubar()

        top = ttk.LabelFrame(self, text="Project", padding=10)
        top.pack(fill="x", padx=10, pady=10)

        self._row_dir(top, 0, "Repo root:", self.repo_root, "Select repo root")
        self._row_file(
            top,
            1,
            "btg.py script:",
            self.btg_script,
            "Select btg.py",
            [("Python", "*.py"), ("All files", "*.*")],
        )
        self._row_file(
            top,
            2,
            "Python exe:",
            self.python_exe,
            "Select Python executable",
            [("All files", "*.*")],
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

        ttk.Checkbutton(flags, text="Global dry-run", variable=self.global_dry_run).pack(
            side="left"
        )

        ttk.Button(flags, text="Save Config", command=self.save_config).pack(
            side="left", padx=(16, 6)
        )
        ttk.Button(flags, text="Reload Config", command=self._load_config).pack(
            side="left"
        )

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

        bottom = ttk.LabelFrame(self, text="Output", padding=10)
        bottom.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(bottom, height=16, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        status = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status.pack(fill="x", padx=10, pady=(0, 8))

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
                v.trace_add("write", lambda *_: self._update_preview())
            except Exception:
                pass

    def _build_menubar(self) -> None:
        mb = tk.Menu(self.master)

        filem = tk.Menu(mb, tearoff=False)
        filem.add_command(label="Save Config", command=self.save_config)
        filem.add_command(label="Reload Config", command=self._load_config)
        filem.add_separator()
        filem.add_command(label="Exit", command=self.master.destroy)
        mb.add_cascade(label="File", menu=filem)

        toolsm = tk.Menu(mb, tearoff=False)
        toolsm.add_command(label="Open Repo Root", command=self.open_repo_root)
        toolsm.add_command(label="Open Output Folder", command=self.open_output_folder)
        toolsm.add_separator()
        toolsm.add_command(label="Copy Preview Command", command=self.copy_preview_command)
        mb.add_cascade(label="Tools", menu=toolsm)

        helpm = tk.Menu(mb, tearoff=False)
        helpm.add_command(label="About", command=self.about)
        mb.add_cascade(label="Help", menu=helpm)

        self.master.config(menu=mb)

    def _row_dir(
        self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar, title: str
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=80).grid(
            row=row, column=1, sticky="we", padx=8
        )
        ttk.Button(
            parent, text="Browse…", command=lambda: self._browse_dir(var, title)
        ).grid(row=row, column=2, sticky="w")
        parent.columnconfigure(1, weight=1)

    def _row_file(
        self,
        parent: ttk.Frame,
        row: int,
        label: str,
        var: tk.StringVar,
        title: str,
        filetypes,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=80).grid(
            row=row, column=1, sticky="we", padx=8
        )
        ttk.Button(
            parent,
            text="Browse…",
            command=lambda: self._browse_file(var, title, filetypes),
        ).grid(row=row, column=2, sticky="w")
        parent.columnconfigure(1, weight=1)

    def _row_text(
        self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar, width: int = 70
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=width).grid(
            row=row, column=1, sticky="w", padx=8
        )

    # -------------------------
    # Tabs
    # -------------------------
    def _build_validate_tab(self) -> None:
        f = ttk.Frame(self.tab_validate, padding=10)
        f.pack(fill="x")

        self._row_dir(f, 0, "Schemas dir:", self.val_schemas, "Select schemas directory")
        self._row_dir(
            f, 1, "Palettes dir:", self.val_palettes, "Select palettes directory"
        )

        ttk.Button(f, text="Run Validate", command=self.run_validate).grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

    def _build_normalize_tab(self) -> None:
        f = ttk.Frame(self.tab_normalize, padding=10)
        f.pack(fill="x")
        self._row_dir(f, 0, "Palettes dir:", self.norm_palettes, "Select palettes directory")
        ttk.Button(f, text="Run Normalize", command=self.run_normalize).grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

    def _build_extract_tab(self) -> None:
        f = ttk.Frame(self.tab_extract, padding=10)
        f.pack(fill="x")

        self._row_dir(f, 0, "Textures dir:", self.ext_textures, "Select textures directory")
        self._row_dir(
            f, 1, "Palettes output dir:", self.ext_palettes_out, "Select output palettes directory"
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

        self._row_dir(f, 0, "Palettes dir:", self.rec_palettes_dir, "Select palettes directory")
        self._row_text(f, 1, "Source palette (rel):", self.rec_src_palette, width=70)
        self._row_text(f, 2, "Target palette (rel):", self.rec_dst_palette, width=70)
        self._row_text(f, 3, "Source id:", self.rec_src_id, width=20)
        self._row_text(f, 4, "Target id:", self.rec_dst_id, width=20)
        self._row_text(f, 5, "Group (blank=auto):", self.rec_group, width=20)

        self._row_dir(f, 6, "Input dir:", self.rec_input, "Select input directory")
        self._row_dir(f, 7, "Output dir:", self.rec_output, "Select output directory")

        ttk.Checkbutton(f, text="No recursive input scan", variable=self.rec_no_recursive).grid(
            row=8, column=0, sticky="w", pady=(10, 0)
        )

        self._row_text(f, 9, "Min alpha:", self.rec_min_alpha, width=12)
        self._row_text(f, 10, "Alpha weight:", self.rec_alpha_weight, width=12)

        ttk.Checkbutton(f, text="Preserve original alpha", variable=self.rec_preserve_alpha).grid(
            row=11, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Checkbutton(f, text="Exact-match first", variable=self.rec_exact_first).grid(
            row=12, column=0, sticky="w", pady=(6, 0)
        )

        ttk.Button(f, text="Run Recolor", command=self.run_recolor).grid(
            row=13, column=0, sticky="w", pady=(10, 0)
        )

    def _build_legacy_tab(self) -> None:
        f = ttk.Frame(self.tab_legacy, padding=10)
        f.pack(fill="x")

        self._row_dir(f, 0, "Palettes dir:", self.leg_palettes_dir, "Select palettes directory")
        self._row_dir(f, 1, "Templates dir:", self.leg_templates_dir, "Select templates directory")
        self._row_dir(f, 2, "Output root:", self.leg_output_root, "Select output root directory")
        self._row_text(f, 3, "Namespace/modid:", self.leg_namespace, width=20)
        self._row_text(f, 4, "Lang file:", self.leg_lang_file, width=20)

        ttk.Checkbutton(
            f, text="Disable output/<namespace>/... tree", variable=self.leg_no_modid_tree
        ).grid(row=5, column=0, sticky="w", pady=(10, 0))
        ttk.Checkbutton(f, text="Disable flat output/... tree", variable=self.leg_no_flat_tree).grid(
            row=6, column=0, sticky="w", pady=(6, 0)
        )

        ttk.Button(f, text="Run Legacy recolor-templates", command=self.run_legacy_templates).grid(
            row=7, column=0, sticky="w", pady=(10, 0)
        )

    def _build_generate_tab(self) -> None:
        f = ttk.Frame(self.tab_generate, padding=10)
        f.pack(fill="x")

        self._row_dir(f, 0, "Templates dir:", self.gen_templates, "Select templates directory")
        self._row_dir(f, 1, "Palettes dir:", self.gen_palettes, "Select palettes directory")
        self._row_dir(f, 2, "Output dir:", self.gen_output, "Select output directory")

        self._row_text(f, 3, "Min alpha:", self.gen_min_alpha, width=12)
        self._row_text(f, 4, "Alpha weight:", self.gen_alpha_weight, width=12)
        self._row_text(f, 5, "Limit (blank=none):", self.gen_limit, width=12)

        ttk.Checkbutton(f, text="Preserve alpha", variable=self.gen_preserve_alpha).grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )
        ttk.Checkbutton(f, text="Exact-match first", variable=self.gen_exact_first).grid(
            row=7, column=0, sticky="w", pady=(6, 0)
        )

        ttk.Button(f, text="Run Generate", command=self.run_generate).grid(
            row=8, column=0, sticky="w", pady=(10, 0)
        )

    def _build_autotemplate_tab(self) -> None:
        f = ttk.Frame(self.tab_autotemplate, padding=10)
        f.pack(fill="x")

        self._row_dir(f, 0, "Templates dir (*.png):", self.at_templates, "Select templates directory")
        self._row_dir(f, 1, "Palettes dir:", self.at_palettes, "Select palettes directory")
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

        self._row_dir(f, 0, "Textures dir:", self.as_textures, "Select textures directory")
        ttk.Checkbutton(f, text="Recurse textures dir", variable=self.as_recursive).grid(
            row=1, column=0, sticky="w", pady=(6, 0)
        )
        self._row_dir(f, 2, "Items dir:", self.as_items_dir, "Select items output directory")
        self._row_dir(f, 3, "Models/item dir:", self.as_models_dir, "Select models output directory")
        self._row_text(f, 4, "Lang file:", self.as_lang, width=70)
        self._row_text(f, 5, "Namespace/modid:", self.as_namespace, width=20)

        ttk.Checkbutton(f, text="Overwrite existing lang keys", variable=self.as_overwrite_lang).grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )

        ttk.Button(f, text="Run Assets", command=self.run_assets).grid(
            row=7, column=0, sticky="w", pady=(10, 0)
        )

    # -------------------------
    # Browse helpers
    # -------------------------
    def _browse_dir(self, var: tk.StringVar, title: str) -> None:
        repo = Path(self.repo_root.get()).resolve()
        p = filedialog.askdirectory(title=title, initialdir=str(repo))
        if not p:
            return
        var.set(try_rel(repo, Path(p)))
        self._update_preview()

    def _browse_file(self, var: tk.StringVar, title: str, filetypes) -> None:
        repo = Path(self.repo_root.get()).resolve()
        p = filedialog.askopenfilename(title=title, initialdir=str(repo), filetypes=filetypes)
        if not p:
            return
        var.set(try_rel(repo, Path(p)))
        self._update_preview()

    # -------------------------
    # Commands
    # -------------------------
    def _update_preview(self) -> None:
        # Show the last selected command if available, otherwise default to validate.
        if self._last_cmd is None:
            self._last_cmd = self._build_validate_cmd()
        self.cmd_preview.set(commands.format_command_for_preview(self._last_cmd, Path(self.repo_root.get()).resolve()))

    def _run(self, cmd: list[str]) -> None:
        self._last_cmd = cmd
        self._update_preview()

        try:
            self._runner.start(cmd, cwd=self._cwd())
            self.status_var.set("Running…")
        except Exception as e:
            messagebox.showerror("Run failed", str(e))

    def run_preview(self) -> None:
        if self._last_cmd is None:
            self._update_preview()
        if self._last_cmd is None:
            return
        self._run(self._last_cmd)

    def stop(self) -> None:
        self._runner.stop()
        self.status_var.set("Stopping…")

    def clear_output(self) -> None:
        self.log_text.delete("1.0", "end")

    def _build_validate_cmd(self) -> list[str]:
        proj = self._project()
        return commands.cmd_validate(
            proj,
            schemas=self.val_schemas.get(),
            palettes=self.val_palettes.get(),
        )

    def run_validate(self) -> None:
        self._run(self._build_validate_cmd())

    def run_normalize(self) -> None:
        proj = self._project()
        cmd = commands.cmd_normalize(proj, palettes=self.norm_palettes.get())
        self._run(cmd)

    def run_extract(self) -> None:
        proj = self._project()
        cmd = commands.cmd_extract(
            proj,
            textures=self.ext_textures.get(),
            palettes_out=self.ext_palettes_out.get(),
            max_colors=_safe_int(self.ext_max_colors.get(), 32),
            min_alpha=_safe_int(self.ext_min_alpha.get(), 1),
            schema_ref=self.ext_schema_ref.get(),
            generator_version=self.ext_generator_version.get(),
        )
        self._run(cmd)

    def run_recolor(self) -> None:
        proj = self._project()
        group = self.rec_group.get().strip() or None
        cmd = commands.cmd_recolor(
            proj,
            palettes_dir=self.rec_palettes_dir.get(),
            src_palette=self.rec_src_palette.get(),
            dst_palette=self.rec_dst_palette.get(),
            src_id=self.rec_src_id.get(),
            dst_id=self.rec_dst_id.get(),
            group=group,
            input_dir=self.rec_input.get(),
            output_dir=self.rec_output.get(),
            recursive=not bool(self.rec_no_recursive.get()),
            min_alpha=_safe_int(self.rec_min_alpha.get(), 1),
            alpha_weight=_safe_float(self.rec_alpha_weight.get(), 0.25),
            preserve_alpha=bool(self.rec_preserve_alpha.get()),
            exact_first=bool(self.rec_exact_first.get()),
        )
        self._run(cmd)

    def run_legacy_templates(self) -> None:
        proj = self._project()
        cmd = commands.cmd_recolor_templates(
            proj,
            palettes_dir=self.leg_palettes_dir.get(),
            templates_dir=self.leg_templates_dir.get(),
            output_root=self.leg_output_root.get(),
            namespace=self.leg_namespace.get(),
            lang_file=self.leg_lang_file.get(),
            write_modid_tree=not bool(self.leg_no_modid_tree.get()),
            write_flat_tree=not bool(self.leg_no_flat_tree.get()),
        )
        self._run(cmd)

    def run_generate(self) -> None:
        proj = self._project()
        limit_s = self.gen_limit.get().strip()
        limit = _safe_int(limit_s, 0) if limit_s else None
        if limit is not None and limit <= 0:
            limit = None
        cmd = commands.cmd_generate(
            proj,
            templates_dir=self.gen_templates.get(),
            palettes_dir=self.gen_palettes.get(),
            output_dir=self.gen_output.get(),
            min_alpha=_safe_int(self.gen_min_alpha.get(), 1),
            alpha_weight=_safe_float(self.gen_alpha_weight.get(), 0.25),
            preserve_alpha=bool(self.gen_preserve_alpha.get()),
            exact_first=bool(self.gen_exact_first.get()),
            limit=limit,
        )
        self._run(cmd)

    def run_autotemplate(self) -> None:
        proj = self._project()
        cmd = commands.cmd_autotemplate(
            proj,
            templates_dir=self.at_templates.get(),
            palettes_dir=self.at_palettes.get(),
            out_dir=self.at_out_dir.get().strip(),
            materials=self.at_materials.get(),
            min_alpha=_safe_int(self.at_min_alpha.get(), 1),
            min_hits=_safe_int(self.at_min_hits.get(), 2),
        )
        self._run(cmd)

    def run_assets(self) -> None:
        proj = self._project()
        cmd = commands.cmd_assets(
            proj,
            textures_dir=self.as_textures.get(),
            recursive=bool(self.as_recursive.get()),
            items_dir=self.as_items_dir.get(),
            models_dir=self.as_models_dir.get(),
            lang_file=self.as_lang.get(),
            namespace=self.as_namespace.get(),
            overwrite_lang=bool(self.as_overwrite_lang.get()),
        )
        self._run(cmd)

    # -------------------------
    # Config
    # -------------------------
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
            "validate": {"schemas": self.val_schemas.get(), "palettes": self.val_palettes.get()},
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
        self.ext_palettes_out.set(str(ext.get("palettes_out") or self.ext_palettes_out.get()))
        self.ext_max_colors.set(str(ext.get("max_colors") or self.ext_max_colors.get()))
        self.ext_min_alpha.set(str(ext.get("min_alpha") or self.ext_min_alpha.get()))
        self.ext_schema_ref.set(str(ext.get("schema_ref") or self.ext_schema_ref.get()))
        self.ext_generator_version.set(str(ext.get("generator_version") or self.ext_generator_version.get()))

        rec = data.get("recolor") or {}
        self.rec_palettes_dir.set(str(rec.get("palettes_dir") or self.rec_palettes_dir.get()))
        self.rec_src_palette.set(str(rec.get("src_palette") or self.rec_src_palette.get()))
        self.rec_dst_palette.set(str(rec.get("dst_palette") or self.rec_dst_palette.get()))
        self.rec_src_id.set(str(rec.get("src_id") or self.rec_src_id.get()))
        self.rec_dst_id.set(str(rec.get("dst_id") or self.rec_dst_id.get()))
        self.rec_group.set(str(rec.get("group") or self.rec_group.get()))
        self.rec_input.set(str(rec.get("input") or self.rec_input.get()))
        self.rec_output.set(str(rec.get("output") or self.rec_output.get()))
        self.rec_no_recursive.set(bool(rec.get("no_recursive", self.rec_no_recursive.get())))
        self.rec_min_alpha.set(str(rec.get("min_alpha") or self.rec_min_alpha.get()))
        self.rec_alpha_weight.set(str(rec.get("alpha_weight") or self.rec_alpha_weight.get()))
        self.rec_preserve_alpha.set(bool(rec.get("preserve_alpha", self.rec_preserve_alpha.get())))
        self.rec_exact_first.set(bool(rec.get("exact_first", self.rec_exact_first.get())))

        leg = data.get("legacy_templates") or {}
        self.leg_palettes_dir.set(str(leg.get("palettes_dir") or self.leg_palettes_dir.get()))
        self.leg_templates_dir.set(str(leg.get("templates_dir") or self.leg_templates_dir.get()))
        self.leg_output_root.set(str(leg.get("output_root") or self.leg_output_root.get()))
        self.leg_namespace.set(str(leg.get("namespace") or self.leg_namespace.get()))
        self.leg_lang_file.set(str(leg.get("lang_file") or self.leg_lang_file.get()))
        self.leg_no_modid_tree.set(bool(leg.get("no_modid_tree", self.leg_no_modid_tree.get())))
        self.leg_no_flat_tree.set(bool(leg.get("no_flat_tree", self.leg_no_flat_tree.get())))

        gen = data.get("generate") or {}
        self.gen_templates.set(str(gen.get("templates") or self.gen_templates.get()))
        self.gen_palettes.set(str(gen.get("palettes") or self.gen_palettes.get()))
        self.gen_output.set(str(gen.get("output") or self.gen_output.get()))
        self.gen_min_alpha.set(str(gen.get("min_alpha") or self.gen_min_alpha.get()))
        self.gen_alpha_weight.set(str(gen.get("alpha_weight") or self.gen_alpha_weight.get()))
        self.gen_preserve_alpha.set(bool(gen.get("preserve_alpha", self.gen_preserve_alpha.get())))
        self.gen_exact_first.set(bool(gen.get("exact_first", self.gen_exact_first.get())))
        self.gen_limit.set(str(gen.get("limit") or self.gen_limit.get()))

        at = data.get("autotemplate") or {}
        self.at_templates.set(str(at.get("templates") or self.at_templates.get()))
        self.at_palettes.set(str(at.get("palettes") or self.at_palettes.get()))
        self.at_out_dir.set(str(at.get("out_dir") or self.at_out_dir.get()))
        self.at_materials.set(str(at.get("materials") or self.at_materials.get()))
        self.at_min_alpha.set(str(at.get("min_alpha") or self.at_min_alpha.get()))
        self.at_min_hits.set(str(at.get("min_hits") or self.at_min_hits.get()))

        ax = data.get("assets") or {}
        self.as_textures.set(str(ax.get("textures") or self.as_textures.get()))
        self.as_recursive.set(bool(ax.get("recursive", self.as_recursive.get())))
        self.as_items_dir.set(str(ax.get("items_dir") or self.as_items_dir.get()))
        self.as_models_dir.set(str(ax.get("models_dir") or self.as_models_dir.get()))
        self.as_lang.set(str(ax.get("lang") or self.as_lang.get()))
        self.as_namespace.set(str(ax.get("namespace") or self.as_namespace.get()))
        self.as_overwrite_lang.set(bool(ax.get("overwrite_lang", self.as_overwrite_lang.get())))

    def _load_config(self) -> None:
        data = load_config_best_effort(Path(self.repo_root.get()).resolve())
        if data:
            self._apply_config(data)
            self._log("Loaded config.")
            self.status_var.set("Loaded config.")
        else:
            self.status_var.set("No config found; using defaults.")
        self._update_preview()

    def save_config(self) -> None:
        repo = Path(self.repo_root.get()).resolve()
        path = pick_config_path_for_save(repo)
        try:
            save_config(path, self._collect_config())
            self._log(f"Saved config: {path.as_posix()}")
            self.status_var.set(f"Saved config: {path.as_posix()}")
        except Exception as e:
            messagebox.showerror("Save Config Failed", str(e))

    # -------------------------
    # Tools / menu actions
    # -------------------------
    def copy_preview_command(self) -> None:
        cmd = self.cmd_preview.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(cmd)
        self.status_var.set("Copied preview command to clipboard.")

    def open_repo_root(self) -> None:
        open_in_file_manager(Path(self.repo_root.get()))

    def open_output_folder(self) -> None:
        # Prefer a configured output folder; fall back to repo root.
        out = self.gen_output.get().strip() or "output"
        open_in_file_manager(Path(self.repo_root.get()) / out)

    def about(self) -> None:
        messagebox.showinfo(
            "About",
            f"{APP_NAME} {APP_VERSION}\n\n"
            "A modular tkinter GUI for tools/btg.py.\n"
            "Config is stored as .btg_gui.json (repo) or ~/.btg_gui.json (home).",
        )

    # -------------------------
    # Logging / runner callbacks
    # -------------------------
    def _log(self, line: str) -> None:
        self.log_text.insert("end", line + "\n")
        self.log_text.see("end")

    def _on_exit(self, code: int) -> None:
        self.status_var.set(f"Done (exit code {code}).")

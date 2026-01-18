from __future__ import annotations

import os
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import List, Optional

import btg_v3 as btg


class TkLogHandler(btg.logging.Handler):
    def __init__(self, q: "queue.Queue[str]") -> None:
        super().__init__()
        self._q = q

    def emit(self, record: btg.logging.LogRecord) -> None:
        try:
            self._q.put_nowait(self.format(record))
        except Exception:
            pass


def _browse_dir(var: tk.StringVar, *, title: str) -> None:
    from tkinter import filedialog

    p = filedialog.askdirectory(title=title)
    if p:
        var.set(p)


class App(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.log_q: "queue.Queue[str]" = queue.Queue()
        self._worker: Optional[threading.Thread] = None

        self._setup_logging()
        self.pack(fill="both", expand=True)
        self._build_ui()
        self._poll_logs()

    def _setup_logging(self) -> None:
        handler = TkLogHandler(self.log_q)
        handler.setFormatter(btg.logging.Formatter("%(levelname)s: %(message)s"))

        btg.LOG.setLevel(btg.logging.INFO)
        btg.LOG.handlers.clear()
        btg.LOG.addHandler(handler)

        root = btg.logging.getLogger()
        root.setLevel(btg.logging.INFO)
        root.handlers.clear()
        root.addHandler(handler)

    def _build_ui(self) -> None:
        self.master.title("Batch Texture Generator (btg)")
        self.master.geometry("1020x760")

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.repo_var = tk.StringVar(value=str(Path.cwd()))
        ttk.Label(top, text="Repo root:").pack(side="left")
        ttk.Entry(top, textvariable=self.repo_var, width=80).pack(side="left", padx=8)
        ttk.Button(
            top,
            text="Browse…",
            command=lambda: _browse_dir(self.repo_var, title="Select repo root"),
        ).pack(side="left")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tab_validate = ttk.Frame(nb)
        self.tab_normalize = ttk.Frame(nb)
        self.tab_extract = ttk.Frame(nb)
        self.tab_recolor = ttk.Frame(nb)
        self.tab_generate = ttk.Frame(nb)
        self.tab_autotemplate = ttk.Frame(nb)
        self.tab_assets = ttk.Frame(nb)

        nb.add(self.tab_validate, text="Validate")
        nb.add(self.tab_normalize, text="Normalize")
        nb.add(self.tab_extract, text="Extract")
        nb.add(self.tab_recolor, text="Recolor")
        nb.add(self.tab_generate, text="Generate")
        nb.add(self.tab_autotemplate, text="AutoTemplate")
        nb.add(self.tab_assets, text="Assets")

        self._build_validate_tab()
        self._build_normalize_tab()
        self._build_extract_tab()
        self._build_recolor_tab()
        self._build_generate_tab()
        self._build_autotemplate_tab()
        self._build_assets_tab()

        bottom = ttk.Frame(self)
        bottom.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ttk.Label(bottom, text="Output:").pack(anchor="w")
        self.log_text = tk.Text(bottom, height=16, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        btns = ttk.Frame(bottom)
        btns.pack(fill="x", pady=(6, 0))
        ttk.Button(
            btns,
            text="Clear Output",
            command=lambda: self.log_text.delete("1.0", "end"),
        ).pack(side="left")

    def _poll_logs(self) -> None:
        try:
            while True:
                line = self.log_q.get_nowait()
                self.log_text.insert("end", line + "\n")
                self.log_text.see("end")
        except queue.Empty:
            pass

        self.after(100, self._poll_logs)

    def _run_in_thread(self, argv: List[str]) -> None:
        if self._worker and self._worker.is_alive():
            messagebox.showwarning("Busy", "A task is already running.")
            return

        repo = Path(self.repo_var.get()).resolve()
        if not repo.exists():
            messagebox.showerror("Invalid repo", "Repo root does not exist.")
            return

        def work() -> None:
            try:
                self.log_q.put_nowait(f"INFO: Running: btg {' '.join(argv)}")
                old = Path.cwd()
                os.chdir(repo)
                try:
                    btg.main(argv)
                finally:
                    os.chdir(old)
            except Exception as e:
                self.log_q.put_nowait(f"ERROR: {e}")

        self._worker = threading.Thread(target=work, daemon=True)
        self._worker.start()

    # ---- UI helpers ----
    def _row_dir(
        self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=70).grid(
            row=row, column=1, sticky="w", padx=8
        )
        ttk.Button(
            parent,
            text="Browse…",
            command=lambda v=var: _browse_dir(v, title=label),
        ).grid(row=row, column=2, sticky="w")

    def _row_text(
        self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=70).grid(
            row=row, column=1, sticky="w", padx=8
        )

    # ---- Tabs ----
    def _build_validate_tab(self) -> None:
        f = ttk.Frame(self.tab_validate)
        f.pack(fill="x", padx=10, pady=10)

        self.val_schemas = tk.StringVar(value="schemas")
        self.val_palettes = tk.StringVar(value="palettes")

        self._row_dir(f, 0, "Schemas dir:", self.val_schemas)
        self._row_dir(f, 1, "Palettes dir:", self.val_palettes)

        ttk.Button(
            f,
            text="Run Validate",
            command=lambda: self._run_in_thread(
                [
                    "validate",
                    "--schemas",
                    self.val_schemas.get(),
                    "--palettes",
                    self.val_palettes.get(),
                ]
            ),
        ).grid(row=2, column=0, sticky="w", pady=(10, 0))

    def _build_normalize_tab(self) -> None:
        f = ttk.Frame(self.tab_normalize)
        f.pack(fill="x", padx=10, pady=10)

        self.norm_palettes = tk.StringVar(value="palettes")
        self._row_dir(f, 0, "Palettes dir:", self.norm_palettes)

        ttk.Button(
            f,
            text="Run Normalize",
            command=lambda: self._run_in_thread(
                ["normalize", "--palettes", self.norm_palettes.get()]
            ),
        ).grid(row=1, column=0, sticky="w", pady=(10, 0))

    def _build_extract_tab(self) -> None:
        f = ttk.Frame(self.tab_extract)
        f.pack(fill="x", padx=10, pady=10)

        self.ext_textures = tk.StringVar(value="textures")
        self.ext_palettes = tk.StringVar(value="palettes")
        self.ext_max_colors = tk.IntVar(value=32)
        self.ext_min_alpha = tk.IntVar(value=1)

        self._row_dir(f, 0, "Textures dir:", self.ext_textures)
        self._row_dir(f, 1, "Palettes output dir:", self.ext_palettes)

        ttk.Label(f, text="Max colors:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Spinbox(f, from_=1, to=256, textvariable=self.ext_max_colors, width=8).grid(
            row=2, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(f, text="Min alpha:").grid(row=3, column=0, sticky="w")
        ttk.Spinbox(f, from_=0, to=255, textvariable=self.ext_min_alpha, width=8).grid(
            row=3, column=1, sticky="w"
        )

        ttk.Button(
            f,
            text="Run Extract",
            command=lambda: self._run_in_thread(
                [
                    "extract",
                    "--textures",
                    self.ext_textures.get(),
                    "--palettes",
                    self.ext_palettes.get(),
                    "--max-colors",
                    str(self.ext_max_colors.get()),
                    "--min-alpha",
                    str(self.ext_min_alpha.get()),
                ]
            ),
        ).grid(row=4, column=0, sticky="w", pady=(10, 0))

    def _build_recolor_tab(self) -> None:
        f = ttk.Frame(self.tab_recolor)
        f.pack(fill="x", padx=10, pady=10)

        self.rec_palettes_dir = tk.StringVar(value="palettes")
        self.rec_src_palette = tk.StringVar(value="wood/oak.texture-palettes.json")
        self.rec_dst_palette = tk.StringVar(value="metal/iron.texture-palettes.json")
        self.rec_src_id = tk.StringVar(value="oak")
        self.rec_dst_id = tk.StringVar(value="iron")
        self.rec_group = tk.StringVar(value="base")
        self.rec_input = tk.StringVar(value="textures_input")
        self.rec_output = tk.StringVar(value="output/textures/item")
        self.rec_min_alpha = tk.IntVar(value=1)
        self.rec_alpha_weight = tk.DoubleVar(value=0.25)
        self.rec_preserve_alpha = tk.BooleanVar(value=True)
        self.rec_exact_first = tk.BooleanVar(value=True)

        self._row_dir(f, 0, "Palettes dir:", self.rec_palettes_dir)
        self._row_text(
            f, 1, "Source palette (relative to palettes/):", self.rec_src_palette
        )
        self._row_text(
            f, 2, "Target palette (relative to palettes/):", self.rec_dst_palette
        )
        self._row_text(f, 3, "Source id:", self.rec_src_id)
        self._row_text(f, 4, "Target id:", self.rec_dst_id)
        self._row_text(f, 5, "Group (or blank for auto):", self.rec_group)
        self._row_dir(f, 6, "Input dir:", self.rec_input)
        self._row_dir(f, 7, "Output dir:", self.rec_output)

        ttk.Label(f, text="Min alpha:").grid(row=8, column=0, sticky="w", pady=(10, 0))
        ttk.Spinbox(f, from_=0, to=255, textvariable=self.rec_min_alpha, width=8).grid(
            row=8, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(f, text="Alpha weight:").grid(row=9, column=0, sticky="w")
        ttk.Spinbox(
            f,
            from_=0.0,
            to=5.0,
            increment=0.05,
            textvariable=self.rec_alpha_weight,
            width=8,
        ).grid(row=9, column=1, sticky="w")

        ttk.Checkbutton(
            f, text="Preserve original alpha", variable=self.rec_preserve_alpha
        ).grid(row=10, column=0, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            f, text="Exact-match first", variable=self.rec_exact_first
        ).grid(row=10, column=1, sticky="w", pady=(8, 0))

        def run() -> None:
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
                str(self.rec_min_alpha.get()),
                "--alpha-weight",
                str(self.rec_alpha_weight.get()),
            ]

            group = self.rec_group.get().strip()
            if group:
                argv += ["--group", group]

            if not self.rec_preserve_alpha.get():
                argv += ["--no-preserve-alpha"]
            if not self.rec_exact_first.get():
                argv += ["--no-exact-first"]

            self._run_in_thread(argv)

        ttk.Button(f, text="Run Recolor", command=run).grid(
            row=11, column=0, sticky="w", pady=(10, 0)
        )

    def _build_generate_tab(self) -> None:
        f = ttk.Frame(self.tab_generate)
        f.pack(fill="x", padx=10, pady=10)

        self.gen_templates = tk.StringVar(value="textures_input")
        self.gen_palettes = tk.StringVar(value="palettes")
        self.gen_output = tk.StringVar(value="output/textures/item")
        self.gen_min_alpha = tk.IntVar(value=1)
        self.gen_alpha_weight = tk.DoubleVar(value=0.25)
        self.gen_preserve_alpha = tk.BooleanVar(value=True)
        self.gen_exact_first = tk.BooleanVar(value=True)
        self.gen_dry_run = tk.BooleanVar(value=False)
        self.gen_limit = tk.StringVar(value="")

        self._row_dir(
            f, 0, "Templates dir (*.btg-template.json + PNG):", self.gen_templates
        )
        self._row_dir(f, 1, "Palettes dir:", self.gen_palettes)
        self._row_dir(f, 2, "Output dir:", self.gen_output)

        ttk.Label(f, text="Min alpha:").grid(row=3, column=0, sticky="w", pady=(10, 0))
        ttk.Spinbox(f, from_=0, to=255, textvariable=self.gen_min_alpha, width=8).grid(
            row=3, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(f, text="Alpha weight:").grid(row=4, column=0, sticky="w")
        ttk.Spinbox(
            f,
            from_=0.0,
            to=5.0,
            increment=0.05,
            textvariable=self.gen_alpha_weight,
            width=8,
        ).grid(row=4, column=1, sticky="w")

        ttk.Label(f, text="Limit (optional):").grid(
            row=5, column=0, sticky="w", pady=(10, 0)
        )
        ttk.Entry(f, textvariable=self.gen_limit, width=12).grid(
            row=5, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Checkbutton(
            f, text="Preserve alpha", variable=self.gen_preserve_alpha
        ).grid(row=6, column=0, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            f, text="Exact-match first", variable=self.gen_exact_first
        ).grid(row=6, column=1, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            f, text="Dry run (no files written)", variable=self.gen_dry_run
        ).grid(row=7, column=0, sticky="w", pady=(8, 0))

        def run() -> None:
            argv = [
                "generate",
                "--templates",
                self.gen_templates.get(),
                "--palettes",
                self.gen_palettes.get(),
                "--output",
                self.gen_output.get(),
                "--min-alpha",
                str(self.gen_min_alpha.get()),
                "--alpha-weight",
                str(self.gen_alpha_weight.get()),
            ]

            if not self.gen_preserve_alpha.get():
                argv += ["--no-preserve-alpha"]
            if not self.gen_exact_first.get():
                argv += ["--no-exact-first"]
            if self.gen_dry_run.get():
                argv += ["--dry-run"]

            limit = self.gen_limit.get().strip()
            if limit:
                argv += ["--limit", limit]

            self._run_in_thread(argv)

        ttk.Button(f, text="Run Generate", command=run).grid(
            row=8, column=0, sticky="w", pady=(10, 0)
        )

    def _build_autotemplate_tab(self) -> None:
        f = ttk.Frame(self.tab_autotemplate)
        f.pack(fill="x", padx=10, pady=10)

        self.at_templates = tk.StringVar(value="textures_input")
        self.at_palettes = tk.StringVar(value="palettes")
        self.at_out_dir = tk.StringVar(value="")
        self.at_materials = tk.StringVar(value="wood,metal,glass")
        self.at_min_alpha = tk.IntVar(value=1)
        self.at_min_hits = tk.IntVar(value=2)
        self.at_dry_run = tk.BooleanVar(value=False)

        self._row_dir(f, 0, "Templates dir (*.png):", self.at_templates)
        self._row_dir(f, 1, "Palettes dir:", self.at_palettes)
        self._row_text(f, 2, "Output dir (blank = templates dir):", self.at_out_dir)
        self._row_text(f, 3, "Materials (comma list):", self.at_materials)

        ttk.Label(f, text="Min alpha:").grid(row=4, column=0, sticky="w", pady=(10, 0))
        ttk.Spinbox(f, from_=0, to=255, textvariable=self.at_min_alpha, width=8).grid(
            row=4, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(f, text="Min hits:").grid(row=5, column=0, sticky="w")
        ttk.Spinbox(f, from_=0, to=999, textvariable=self.at_min_hits, width=8).grid(
            row=5, column=1, sticky="w"
        )

        ttk.Checkbutton(
            f, text="Dry run (no files written)", variable=self.at_dry_run
        ).grid(row=6, column=0, sticky="w", pady=(8, 0))

        def run() -> None:
            argv = [
                "autotemplate",
                "--templates",
                self.at_templates.get(),
                "--palettes",
                self.at_palettes.get(),
                "--materials",
                self.at_materials.get(),
                "--min-alpha",
                str(self.at_min_alpha.get()),
                "--min-hits",
                str(self.at_min_hits.get()),
            ]

            out_dir = self.at_out_dir.get().strip()
            if out_dir:
                argv += ["--out-dir", out_dir]
            if self.at_dry_run.get():
                argv += ["--dry-run"]

            self._run_in_thread(argv)

        ttk.Button(f, text="Run AutoTemplate", command=run).grid(
            row=7, column=0, sticky="w", pady=(10, 0)
        )

    def _build_assets_tab(self) -> None:
        f = ttk.Frame(self.tab_assets)
        f.pack(fill="x", padx=10, pady=10)

        self.as_textures = tk.StringVar(value="output/textures/item")
        self.as_items_dir = tk.StringVar(value="output/items")
        self.as_models_dir = tk.StringVar(value="output/models/item")
        self.as_lang = tk.StringVar(value="output/lang/en_us.json")
        self.as_namespace = tk.StringVar(value="modid")
        self.as_overwrite_lang = tk.BooleanVar(value=False)
        self.as_dry_run = tk.BooleanVar(value=False)

        self._row_dir(f, 0, "Textures dir (output/textures/item):", self.as_textures)
        self._row_dir(f, 1, "Items dir:", self.as_items_dir)
        self._row_dir(f, 2, "Models/item dir:", self.as_models_dir)
        self._row_text(f, 3, "Lang file (relative path):", self.as_lang)
        self._row_text(f, 4, "Namespace/modid:", self.as_namespace)

        ttk.Checkbutton(
            f, text="Overwrite existing lang keys", variable=self.as_overwrite_lang
        ).grid(row=5, column=0, sticky="w", pady=(8, 0))
        ttk.Checkbutton(
            f, text="Dry run (no files written)", variable=self.as_dry_run
        ).grid(row=6, column=0, sticky="w", pady=(8, 0))

        def run() -> None:
            argv = [
                "assets",
                "--textures",
                self.as_textures.get(),
                "--items-dir",
                self.as_items_dir.get(),
                "--models-dir",
                self.as_models_dir.get(),
                "--lang",
                self.as_lang.get().strip(),
                "--namespace",
                self.as_namespace.get().strip() or "modid",
            ]
            if self.as_overwrite_lang.get():
                argv += ["--overwrite-lang"]
            if self.as_dry_run.get():
                argv += ["--dry-run"]

            self._run_in_thread(argv)

        ttk.Button(f, text="Run Assets", command=run).grid(
            row=7, column=0, sticky="w", pady=(10, 0)
        )


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

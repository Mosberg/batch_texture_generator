from __future__ import annotations

import os
import queue
import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

import tools.btg_v1 as btg_v1  # tools/btg.py

# ----------------------------
# Logging bridge to Tk
# ----------------------------


class TkLogHandler(btg_v1.logging.Handler):
    def __init__(self, q: "queue.Queue[str]") -> None:
        super().__init__()
        self._q = q

    def emit(self, record: btg_v1.logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self._q.put_nowait(msg)
        except Exception:
            pass


# ----------------------------
# GUI helpers
# ----------------------------


def _browse_dir(var: tk.StringVar, *, title: str) -> None:
    p = filedialog.askdirectory(title=title)
    if p:
        var.set(p)


def _browse_file(
    var: tk.StringVar, *, title: str, initialdir: Optional[str] = None
) -> None:
    p = filedialog.askopenfilename(
        title=title,
        initialdir=initialdir,
        filetypes=[("Palette JSON", "*.json"), ("All files", "*.*")],
    )
    if p:
        var.set(p)


@dataclass(slots=True)
class RecolorConfig:
    palettes_dir: str
    src_palette_rel: str
    dst_palette_rel: str
    src_id: str
    dst_id: str
    group: str
    input_dir: str
    output_dir: str
    min_alpha: int
    alpha_weight: float
    preserve_alpha: bool
    exact_first: bool


class App(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master

        self.log_q: "queue.Queue[str]" = queue.Queue()
        self._worker: Optional[threading.Thread] = None

        self._setup_logging()

        self.repo_root = Path.cwd()
        self._build_ui()
        self._poll_logs()

    def _setup_logging(self) -> None:
        handler = TkLogHandler(self.log_q)
        handler.setFormatter(btg_v1.logging.Formatter("%(levelname)s: %(message)s"))

        # Attach to btg logger
        btg_v1.LOG.setLevel(btg_v1.logging.INFO)
        btg_v1.LOG.handlers.clear()
        btg_v1.LOG.addHandler(handler)

        # Also route root logger (argparse/main may use it)
        root = btg_v1.logging.getLogger()
        root.setLevel(btg_v1.logging.INFO)
        root.handlers.clear()
        root.addHandler(handler)

    def _build_ui(self) -> None:
        self.master.title("Batch Texture Generator (btg)")
        self.master.geometry("1000x700")

        self.pack(fill="both", expand=True)

        # Top: repo root chooser
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        self.repo_var = tk.StringVar(value=str(self.repo_root))
        ttk.Label(top, text="Repo root:").pack(side="left")
        ttk.Entry(top, textvariable=self.repo_var, width=80).pack(side="left", padx=8)
        ttk.Button(
            top,
            text="Browse…",
            command=lambda: _browse_dir(self.repo_var, title="Select repo root"),
        ).pack(side="left")

        # Tabs
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tab_validate = ttk.Frame(nb)
        self.tab_normalize = ttk.Frame(nb)
        self.tab_extract = ttk.Frame(nb)
        self.tab_recolor = ttk.Frame(nb)
        nb.add(self.tab_validate, text="Validate")
        nb.add(self.tab_normalize, text="Normalize")
        nb.add(self.tab_extract, text="Extract")
        nb.add(self.tab_recolor, text="Recolor")

        self._build_validate_tab()
        self._build_normalize_tab()
        self._build_extract_tab()
        self._build_recolor_tab()

        # Bottom: log output
        bottom = ttk.Frame(self)
        bottom.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ttk.Label(bottom, text="Output:").pack(anchor="w")
        self.log_text = tk.Text(bottom, height=14, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        btns = ttk.Frame(bottom)
        btns.pack(fill="x", pady=(6, 0))
        ttk.Button(btns, text="Clear Output", command=self._clear_log).pack(side="left")
        ttk.Button(btns, text="Stop (best-effort)", command=self._stop_worker).pack(
            side="left", padx=8
        )

    def _build_validate_tab(self) -> None:
        f = ttk.Frame(self.tab_validate)
        f.pack(fill="x", padx=10, pady=10)

        self.val_schemas = tk.StringVar(value="schemas")
        self.val_palettes = tk.StringVar(value="palettes")

        self._row_dir(f, 0, "Schemas dir (relative to repo):", self.val_schemas)
        self._row_dir(f, 1, "Palettes dir (relative to repo):", self.val_palettes)

        ttk.Button(f, text="Run Validate", command=self._run_validate).grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

    def _build_normalize_tab(self) -> None:
        f = ttk.Frame(self.tab_normalize)
        f.pack(fill="x", padx=10, pady=10)

        self.norm_palettes = tk.StringVar(value="palettes")
        self._row_dir(f, 0, "Palettes dir (relative to repo):", self.norm_palettes)

        ttk.Button(f, text="Run Normalize", command=self._run_normalize).grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

    def _build_extract_tab(self) -> None:
        f = ttk.Frame(self.tab_extract)
        f.pack(fill="x", padx=10, pady=10)

        self.ext_textures = tk.StringVar(value="textures")
        self.ext_palettes = tk.StringVar(value="palettes")
        self.ext_max_colors = tk.IntVar(value=32)
        self.ext_min_alpha = tk.IntVar(value=1)

        self._row_dir(f, 0, "Textures dir (relative to repo):", self.ext_textures)
        self._row_dir(
            f, 1, "Palettes output dir (relative to repo):", self.ext_palettes
        )

        ttk.Label(f, text="Max colors:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Spinbox(f, from_=1, to=256, textvariable=self.ext_max_colors, width=8).grid(
            row=2, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(f, text="Min alpha:").grid(row=3, column=0, sticky="w")
        ttk.Spinbox(f, from_=0, to=255, textvariable=self.ext_min_alpha, width=8).grid(
            row=3, column=1, sticky="w"
        )

        ttk.Button(f, text="Run Extract", command=self._run_extract).grid(
            row=4, column=0, sticky="w", pady=(10, 0)
        )

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

        self._row_dir(f, 0, "Palettes dir (relative):", self.rec_palettes_dir)

        self._row_text(
            f, 1, "Source palette (relative to palettes/):", self.rec_src_palette
        )
        self._row_text(
            f, 2, "Target palette (relative to palettes/):", self.rec_dst_palette
        )

        self._row_text(f, 3, "Source id:", self.rec_src_id)
        self._row_text(f, 4, "Target id:", self.rec_dst_id)
        self._row_text(f, 5, "Group (blank = auto):", self.rec_group)

        self._row_dir(f, 6, "Input textures dir (relative):", self.rec_input)
        self._row_dir(f, 7, "Output textures dir (relative):", self.rec_output)

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

        ttk.Button(f, text="Run Recolor", command=self._run_recolor).grid(
            row=11, column=0, sticky="w", pady=(10, 0)
        )

    def _row_dir(
        self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=70).grid(
            row=row, column=1, sticky="w", padx=8
        )
        ttk.Button(
            parent, text="Browse…", command=lambda v=var: _browse_dir(v, title=label)
        ).grid(row=row, column=2, sticky="w")

    def _row_text(
        self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        ttk.Entry(parent, textvariable=var, width=70).grid(
            row=row, column=1, sticky="w", padx=8
        )
        ttk.Label(parent, text="").grid(row=row, column=2, sticky="w")

    def _clear_log(self) -> None:
        self.log_text.delete("1.0", "end")

    def _stop_worker(self) -> None:
        # Best-effort: we don’t forcibly kill threads; we just notify.
        if self._worker and self._worker.is_alive():
            messagebox.showinfo(
                "Stop",
                "Stop requested.\nThis is best-effort; current operation may finish first.",
            )

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
                old_cwd = Path.cwd()
                os.chdir(repo)
                try:
                    btg_v1.main(argv)
                finally:
                    os.chdir(old_cwd)
            except Exception as e:
                self.log_q.put_nowait(f"ERROR: {e}")

        self._worker = threading.Thread(target=work, daemon=True)
        self._worker.start()

    # ---- actions ----

    def _run_validate(self) -> None:
        self._run_in_thread(
            [
                "validate",
                "--schemas",
                self.val_schemas.get(),
                "--palettes",
                self.val_palettes.get(),
            ]
        )

    def _run_normalize(self) -> None:
        self._run_in_thread(
            [
                "normalize",
                "--palettes",
                self.norm_palettes.get(),
            ]
        )

    def _run_extract(self) -> None:
        self._run_in_thread(
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
        )

    def _run_recolor(self) -> None:
        group = self.rec_group.get().strip()
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
        if group:
            argv += ["--group", group]
        if not self.rec_preserve_alpha.get():
            argv += ["--no-preserve-alpha"]
        if not self.rec_exact_first.get():
            argv += ["--no-exact-first"]

        self._run_in_thread(argv)


def main() -> None:
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

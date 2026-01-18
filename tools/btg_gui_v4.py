#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import threading
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, ttk


@dataclass
class SwapRow:
    src_palette: tk.StringVar
    src_id: tk.StringVar
    dst_palette: tk.StringVar
    dst_id: tk.StringVar


class BTGGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Batch Texture Generator (BTG)")
        self.geometry("980x720")

        self.project_root = tk.StringVar(value=str(Path.cwd()))
        self.namespace = tk.StringVar(value="modid")
        self.output_dir = tk.StringVar(value="output")
        self.lang_file = tk.StringVar(value="en_us.json")

        self.palettes_dir = tk.StringVar(value="palettes")
        self.textures_dir = tk.StringVar(value="textures")
        self.extract_out_dir = tk.StringVar(value="palettes_extracted")
        self.max_colors = tk.IntVar(value=32)

        self.input_dir = tk.StringVar(value="textures_input")
        self.templates_dir = tk.StringVar(value="textures_input")

        self.generate_json = tk.BooleanVar(value=False)
        self.no_modid_tree = tk.BooleanVar(value=False)
        self.no_flat_tree = tk.BooleanVar(value=False)

        self.swaps: list[SwapRow] = []
        self._proc: subprocess.Popen[str] | None = None

        self._build_ui()

    # --------------
    # UI
    # --------------
    def _build_ui(self) -> None:
        root_frame = ttk.Frame(self, padding=10)
        root_frame.pack(fill="both", expand=True)

        # Top: project root + namespace/output
        top = ttk.LabelFrame(root_frame, text="Project", padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Project root:").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.project_root, width=70).grid(
            row=0, column=1, sticky="we", padx=6
        )
        ttk.Button(top, text="Browse...", command=self._browse_project_root).grid(
            row=0, column=2, sticky="e"
        )

        ttk.Label(top, text="Namespace:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(top, textvariable=self.namespace, width=20).grid(
            row=1, column=1, sticky="w", pady=(8, 0)
        )

        ttk.Label(top, text="Output dir:").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(top, textvariable=self.output_dir, width=20).grid(
            row=2, column=1, sticky="w", pady=(8, 0)
        )

        ttk.Label(top, text="Lang file:").grid(row=3, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(top, textvariable=self.lang_file, width=20).grid(
            row=3, column=1, sticky="w", pady=(8, 0)
        )

        top.columnconfigure(1, weight=1)

        # Tabs
        tabs = ttk.Notebook(root_frame)
        tabs.pack(fill="both", expand=True, pady=(10, 0))

        self.tab_norm = ttk.Frame(tabs, padding=10)
        self.tab_val = ttk.Frame(tabs, padding=10)
        self.tab_ext = ttk.Frame(tabs, padding=10)
        self.tab_rec = ttk.Frame(tabs, padding=10)

        tabs.add(self.tab_norm, text="Normalize")
        tabs.add(self.tab_val, text="Validate")
        tabs.add(self.tab_ext, text="Extract")
        tabs.add(self.tab_rec, text="Recolor")

        self._build_tab_normalize()
        self._build_tab_validate()
        self._build_tab_extract()
        self._build_tab_recolor()

        # Log
        log_frame = ttk.LabelFrame(root_frame, text="Log", padding=10)
        log_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.log = tk.Text(log_frame, height=14, wrap="word")
        self.log.pack(fill="both", expand=True)
        self._log_line("Ready.")

    def _build_tab_normalize(self) -> None:
        f = self.tab_norm
        ttk.Label(f, text="Palettes dir (relative to project root):").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Entry(f, textvariable=self.palettes_dir, width=40).grid(
            row=0, column=1, sticky="w", padx=6
        )
        ttk.Button(f, text="Run normalize", command=self.run_normalize).grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

    def _build_tab_validate(self) -> None:
        f = self.tab_val
        ttk.Label(f, text="Palettes dir (relative to project root):").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Entry(f, textvariable=self.palettes_dir, width=40).grid(
            row=0, column=1, sticky="w", padx=6
        )
        ttk.Button(f, text="Run validate", command=self.run_validate).grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

    def _build_tab_extract(self) -> None:
        f = self.tab_ext
        ttk.Label(f, text="Textures dir (relative to project root):").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Entry(f, textvariable=self.textures_dir, width=40).grid(
            row=0, column=1, sticky="w", padx=6
        )

        ttk.Label(f, text="Output dir (relative to project root):").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Entry(f, textvariable=self.extract_out_dir, width=40).grid(
            row=1, column=1, sticky="w", padx=6, pady=(8, 0)
        )

        ttk.Label(f, text="Max colors:").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(f, textvariable=self.max_colors, width=8).grid(
            row=2, column=1, sticky="w", padx=6, pady=(8, 0)
        )

        ttk.Button(f, text="Run extract", command=self.run_extract).grid(
            row=3, column=0, sticky="w", pady=(10, 0)
        )

    def _build_tab_recolor(self) -> None:
        f = self.tab_rec

        mode = ttk.LabelFrame(f, text="Mode", padding=10)
        mode.grid(row=0, column=0, sticky="we")
        f.columnconfigure(0, weight=1)

        self.recolor_mode = tk.StringVar(value="templates")
        ttk.Radiobutton(
            mode,
            text="Templates batch (--templates-dir)",
            variable=self.recolor_mode,
            value="templates",
        ).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            mode,
            text="Manual swaps (--swap ...)",
            variable=self.recolor_mode,
            value="manual",
        ).grid(row=0, column=1, sticky="w", padx=(12, 0))

        # Templates
        tf = ttk.LabelFrame(f, text="Templates", padding=10)
        tf.grid(row=1, column=0, sticky="we", pady=(10, 0))
        ttk.Label(tf, text="Templates dir:").grid(row=0, column=0, sticky="w")
        ttk.Entry(tf, textvariable=self.templates_dir, width=50).grid(
            row=0, column=1, sticky="we", padx=6
        )
        ttk.Button(tf, text="Browse...", command=self._browse_templates_dir).grid(
            row=0, column=2, sticky="e"
        )
        tf.columnconfigure(1, weight=1)

        # Manual swaps
        mf = ttk.LabelFrame(f, text="Manual swaps", padding=10)
        mf.grid(row=2, column=0, sticky="we", pady=(10, 0))
        ttk.Label(mf, text="Input dir:").grid(row=0, column=0, sticky="w")
        ttk.Entry(mf, textvariable=self.input_dir, width=50).grid(
            row=0, column=1, sticky="we", padx=6
        )
        ttk.Button(mf, text="Browse...", command=self._browse_input_dir).grid(
            row=0, column=2, sticky="e"
        )
        mf.columnconfigure(1, weight=1)

        self.swaps_frame = ttk.Frame(mf)
        self.swaps_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=(10, 0))

        ttk.Button(mf, text="Add swap", command=self._add_swap_row).grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )
        ttk.Button(mf, text="Clear swaps", command=self._clear_swaps).grid(
            row=2, column=1, sticky="w", pady=(10, 0)
        )

        # Options
        opt = ttk.LabelFrame(f, text="Options", padding=10)
        opt.grid(row=3, column=0, sticky="we", pady=(10, 0))

        ttk.Checkbutton(
            opt,
            text="Generate basic item JSON/model/lang (manual mode)",
            variable=self.generate_json,
        ).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(
            opt, text="Disable output/<modid>/... tree", variable=self.no_modid_tree
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Checkbutton(
            opt,
            text="Disable flat output/textures/... tree",
            variable=self.no_flat_tree,
        ).grid(row=2, column=0, sticky="w", pady=(6, 0))

        # Run buttons
        run = ttk.Frame(f)
        run.grid(row=4, column=0, sticky="we", pady=(10, 0))
        ttk.Button(run, text="Run recolor", command=self.run_recolor).pack(side="left")
        ttk.Button(run, text="Stop", command=self.stop_process).pack(
            side="left", padx=(10, 0)
        )

        # Pre-add one swap row for convenience
        self._add_swap_row()

    # --------------
    # Browsers
    # --------------
    def _browse_project_root(self) -> None:
        d = filedialog.askdirectory(
            initialdir=self.project_root.get() or str(Path.cwd())
        )
        if d:
            self.project_root.set(d)

    def _browse_templates_dir(self) -> None:
        d = filedialog.askdirectory(initialdir=str(Path(self.project_root.get())))
        if d:
            # store as relative if possible
            self.templates_dir.set(self._rel_to_project(Path(d)))

    def _browse_input_dir(self) -> None:
        d = filedialog.askdirectory(initialdir=str(Path(self.project_root.get())))
        if d:
            self.input_dir.set(self._rel_to_project(Path(d)))

    def _browse_palette_file(self, var: tk.StringVar) -> None:
        d = Path(self.project_root.get())
        p = filedialog.askopenfilename(
            initialdir=str(d),
            filetypes=[("Texture palette JSON", "*.json"), ("All files", "*.*")],
        )
        if p:
            var.set(self._rel_to_project(Path(p)))

    # --------------
    # Swap rows
    # --------------
    def _clear_swaps(self) -> None:
        for child in list(self.swaps_frame.winfo_children()):
            child.destroy()
        self.swaps.clear()

    def _add_swap_row(self) -> None:
        row = SwapRow(
            src_palette=tk.StringVar(value=""),
            src_id=tk.StringVar(value=""),
            dst_palette=tk.StringVar(value=""),
            dst_id=tk.StringVar(value=""),
        )
        self.swaps.append(row)

        r = len(self.swaps) - 1
        line = ttk.Frame(self.swaps_frame)
        line.grid(row=r, column=0, sticky="we", pady=2)
        self.swaps_frame.columnconfigure(0, weight=1)

        ttk.Label(line, text="SRC palette:").grid(row=0, column=0, sticky="w")
        ttk.Entry(line, textvariable=row.src_palette, width=28).grid(
            row=0, column=1, sticky="w", padx=4
        )
        ttk.Button(
            line,
            text="...",
            width=3,
            command=lambda: self._browse_palette_file(row.src_palette),
        ).grid(row=0, column=2, sticky="w")
        ttk.Label(line, text="SRC id:").grid(row=0, column=3, sticky="w", padx=(10, 0))
        ttk.Entry(line, textvariable=row.src_id, width=14).grid(
            row=0, column=4, sticky="w", padx=4
        )

        ttk.Label(line, text="DST palette:").grid(row=1, column=0, sticky="w")
        ttk.Entry(line, textvariable=row.dst_palette, width=28).grid(
            row=1, column=1, sticky="w", padx=4
        )
        ttk.Button(
            line,
            text="...",
            width=3,
            command=lambda: self._browse_palette_file(row.dst_palette),
        ).grid(row=1, column=2, sticky="w")
        ttk.Label(line, text="DST id:").grid(row=1, column=3, sticky="w", padx=(10, 0))
        ttk.Entry(line, textvariable=row.dst_id, width=14).grid(
            row=1, column=4, sticky="w", padx=4
        )

    # --------------
    # Run helpers
    # --------------
    def _btg_path(self) -> Path:
        # btg.py is assumed to live next to this gui script
        return Path(__file__).with_name("btg_v4.py")

    def _rel_to_project(self, p: Path) -> str:
        try:
            pr = Path(self.project_root.get()).resolve()
            return str(p.resolve().relative_to(pr))
        except Exception:
            return str(p)

    def _run_btg(self, args: list[str]) -> None:
        if self._proc is not None:
            self._log_line("A process is already running. Stop it first.")
            return

        btg = self._btg_path()
        if not btg.exists():
            self._log_line(f"btg_v4.py not found next to GUI: {btg}")
            return

        cwd = Path(self.project_root.get())
        cmd = [sys.executable, str(btg), *args]

        self._log_line("Running: " + " ".join(cmd))
        self._log_line(f"cwd: {cwd}")

        def worker() -> None:
            try:
                self._proc = subprocess.Popen(
                    cmd,
                    cwd=str(cwd),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    universal_newlines=True,
                )
                assert self._proc.stdout is not None
                for line in self._proc.stdout:
                    self._log_line(line.rstrip("\n"))
                rc = self._proc.wait()
                self._log_line(f"Process exited with code: {rc}")
            except Exception as e:
                self._log_line(f"Error: {e}")
            finally:
                self._proc = None

        threading.Thread(target=worker, daemon=True).start()

    def stop_process(self) -> None:
        if self._proc is None:
            self._log_line("No process running.")
            return
        try:
            self._proc.terminate()
            self._log_line("Terminate requested.")
        except Exception as e:
            self._log_line(f"Terminate failed: {e}")

    # --------------
    # Commands
    # --------------
    def run_normalize(self) -> None:
        self._run_btg(["normalize", "--palettes-dir", self.palettes_dir.get()])

    def run_validate(self) -> None:
        self._run_btg(["validate", "--palettes-dir", self.palettes_dir.get()])

    def run_extract(self) -> None:
        self._run_btg(
            [
                "extract",
                "--textures-dir",
                self.textures_dir.get(),
                "--output-dir",
                self.extract_out_dir.get(),
                "--max-colors",
                str(self.max_colors.get()),
            ]
        )

    def run_recolor(self) -> None:
        args = [
            "recolor",
            "--namespace",
            self.namespace.get(),
            "--output-dir",
            self.output_dir.get(),
            "--lang-file",
            self.lang_file.get(),
        ]
        if self.no_modid_tree.get():
            args.append("--no-modid-tree")
        if self.no_flat_tree.get():
            args.append("--no-flat-tree")

        if self.recolor_mode.get() == "templates":
            args.extend(["--templates-dir", self.templates_dir.get()])
        else:
            args.extend(["--input-dir", self.input_dir.get()])
            if self.generate_json.get():
                args.append("--generate-json")
            for s in self.swaps:
                sp = s.src_palette.get().strip()
                si = s.src_id.get().strip()
                dp = s.dst_palette.get().strip()
                di = s.dst_id.get().strip()
                if not (sp and si and dp and di):
                    continue
                args.extend(["--swap", sp, si, dp, di])

        self._run_btg(args)

    # --------------
    # Logging
    # --------------
    def _log_line(self, s: str) -> None:
        self.log.insert("end", s + "\n")
        self.log.see("end")


def main() -> None:
    app = BTGGui()
    app.mainloop()


if __name__ == "__main__":
    main()

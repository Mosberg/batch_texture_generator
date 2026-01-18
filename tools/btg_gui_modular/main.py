from __future__ import annotations

import tkinter as tk

from .ui import BTGGuiApp


def main() -> int:
    root = tk.Tk()
    BTGGuiApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Backward-compatible entrypoint.

This file used to contain the full GUI implementation.
It now forwards to the modular implementation in `tools/btg_gui_modular/`.
"""

from __future__ import annotations

from btg_gui_modular.main import main


if __name__ == "__main__":
    raise SystemExit(main())

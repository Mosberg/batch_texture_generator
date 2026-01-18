# Copilot Instructions

## Project goals

- Batch Texture Generator: validate palettes, extract palettes from textures, recolor textures deterministically.

## Non-negotiable conventions

- Python 3.14.
- Prefer small pure functions; type hints for all public functions.
- Palette colors are **8-digit RGBA hex** only: `#RRGGBBAA`.
- Validate JSON using local schemas in `schemas/` (Draft 2020-12).

## Repository layout

- Schemas: `schemas/common.schema.json`, `schemas/texture-palettes.schema.json`
- Palettes: `palettes/**/**.texture-palettes.json`
- Source textures: `textures/<material>/*.png`
- Inputs to recolor: `textures_input/**/*.png`
- Outputs: `textures_output/**/*.png`
- Tooling: `tools/btg.py`

## CLI expectations

When adding features to `tools/btg.py`, keep commands stable:

- `python tools/btg.py validate`
- `python tools/btg.py extract ...`
- `python tools/btg.py recolor ...`
- `python tools/btg.py normalize ...` (upgrade old palettes to RGBA)

## Quality bar

- Format: `black`
- Lint: `flake8`
- Add clear errors (include file path + JSON pointer path for schema errors).
- Avoid silent fallbacks; prefer explicit options and deterministic output.

## Remote indexing:

- Use [Remote Index](REMOTE-INDEX.md) for large codebases.

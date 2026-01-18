# Batch Texture Generator

## Setup

```bash
python -m venv .btg
.btg\Scripts\python.exe -m pip install -r requirements.txt
```

## Commands

### 1) Normalize palettes to RGBA

Converts any `#RRGGBB` colors to `#RRGGBBff` and normalizes casing.

```bash
python tools/btg.py normalize
```

### 2) Validate palettes

```bash
python tools/btg.py validate
```

### 3) Extract RGBA palettes from textures/

```bash
python tools/btg.py extract --max-colors 32
```

### 4) Recolor textures_input/ using palette swap

```bash
python tools/btg.py recolor ^
  --src-palette wood/oak.texture-palettes.json --src-id oak ^
  --dst-palette metal/iron.texture-palettes.json --dst-id iron ^
  --output textures_output
```

## Notes

- Palettes must use 8-digit RGBA hex: `#RRGGBBAA`.
- Schemas live in `schemas/` and are mapped in `.vscode/settings.json`.

## Project Structure

```plaintext
batch_texture_generator/               # Root directory
├─ .github/
│  ├─ REMOTE-INDEX.md                  # Remote index for large codebases
│  └─ copilot-instructions.md          # GitHub Copilot instructions
├─ .vscode/
│  └─ settings.json                    # VSCode settings
├─ palettes/                           # JSON palette directory
│  ├─ glass
│  │  ├─ black_stained_glass.texture-palettes.json
│  │  ├─ blue_stained_glass.texture-palettes.json
│  │  ├─ brown_stained_glass.texture-palettes.json
│  │  ├─ cyan_stained_glass.texture-palettes.json
│  │  ├─ glass.texture-palettes.json
│  │  ├─ gray_stained_glass.texture-palettes.json
│  │  ├─ green_stained_glass.texture-palettes.json
│  │  ├─ light_blue_stained_glass.texture-palettes.json
│  │  ├─ light_gray_stained_glass.texture-palettes.json
│  │  ├─ lime_stained_glass.texture-palettes.json
│  │  ├─ magenta_stained_glass.texture-palettes.json
│  │  ├─ orange_stained_glass.texture-palettes.json
│  │  ├─ pink_stained_glass.texture-palettes.json
│  │  ├─ purple_stained_glass.texture-palettes.json
│  │  ├─ red_stained_glass.texture-palettes.json
│  │  ├─ tinted_glass.texture-palettes.json
│  │  ├─ white_stained_glass.texture-palettes.json
│  │  └─ yellow_stained_glass.texture-palettes.json
│  ├─ metal
│  │  ├─ copper.texture-palettes.json
│  │  ├─ copper_exposed.texture-palettes.json
│  │  ├─ copper_oxidized.texture-palettes.json
│  │  ├─ copper_weathered.texture-palettes.json
│  │  ├─ gold.texture-palettes.json
│  │  ├─ iron.texture-palettes.json
│  │  └─ netherite.texture-palettes.json
│  └─ wood
│     ├─ acacia.texture-palettes.json
│     ├─ bamboo.texture-palettes.json
│     ├─ birch.texture-palettes.json
│     ├─ cherry.texture-palettes.json
│     ├─ crimson.texture-palettes.json
│     ├─ dark_oak.texture-palettes.json
│     ├─ jungle.texture-palettes.json
│     ├─ mangrove.texture-palettes.json
│     ├─ oak.texture-palettes.json
│     ├─ pale_oak.texture-palettes.json
│     ├─ spruce.texture-palettes.json
│     └─ warped.texture-palettes.json
├─ README.md
├─ requirements.txt
├─ schemas/                            # JSON schema directory
│  ├─ common.schema.json
│  └─ texture-palettes.schema.json
├─ textures/                           # Material PNG directory
│  ├─ glass/
│  │  ├─ black_stained_glass.png
│  │  ├─ blue_stained_glass.png
│  │  ├─ brown_stained_glass.png
│  │  ├─ cyan_stained_glass.png
│  │  ├─ glass.png
│  │  ├─ gray_stained_glass.png
│  │  ├─ green_stained_glass.png
│  │  ├─ light_blue_stained_glass.png
│  │  ├─ light_gray_stained_glass.png
│  │  ├─ lime_stained_glass.png
│  │  ├─ magenta_stained_glass.png
│  │  ├─ orange_stained_glass.png
│  │  ├─ pink_stained_glass.png
│  │  ├─ purple_stained_glass.png
│  │  ├─ red_stained_glass.png
│  │  ├─ tinted_glass.png
│  │  ├─ white_stained_glass.png
│  │  └─ yellow_stained_glass.png
│  ├─ metal/
│  │  ├─ copper.png
│  │  ├─ copper_exposed.png
│  │  ├─ copper_oxidized.png
│  │  ├─ copper_weathered.png
│  │  ├─ gold.png
│  │  ├─ iron.png
│  │  └─ netherite.png
│  └─ wood/
│     ├─ acacia.png
│     ├─ bamboo.png
│     ├─ birch.png
│     ├─ cherry.png
│     ├─ crimson.png
│     ├─ dark_oak.png
│     ├─ jungle.png
│     ├─ mangrove.png
│     ├─ oak.png
│     ├─ pale_oak.png
│     ├─ spruce.png
│     └─ warped.png
├─ textures_input/                     # Texture PNG's which needs recoloring
│  ├─ barrel.png
│  ├─ barrel.texture-palettes.json
│  ├─ big_flask.png
│  ├─ big_flask.texture-palettes.json
│  ├─ keg.png
│  ├─ keg.texture-palettes.json
│  ├─ medium_flask.png
│  ├─ medium_flask.texture-palettes.json
│  ├─ small_flask.png
│  └─ small_flask.texture-palettes.json
├─ textures_output/                    # Texture PNG's which have been recolored
└─ tools/
   ├─ btg.py                           # Main script for batch texture generation
   └─ btg_gui.py                       # GUI script for batch texture generation

```

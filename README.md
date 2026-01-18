# Batch Texture Generator

## Usage

# Validate all palette JSON files

```bash
python tools/btg.py validate
```

# Extract palettes from textures/_/_.png

```bash
python tools/btg.py extract --max-colors 32 --method quantize
```

# Recolor everything in textures_input/ from oak->iron using group "base"

```bash
python tools/btg.py recolor --src-palette wood/oak.texture-palettes.json --src-id oak --dst-palette metal/iron.texture-palettes.json --dst-id iron
```

## Project Structure

```plaintext
batch_texture_generator/               # Root directory
├─ .github/
│  ├─ REMOTE-INDEX.md                  # Remote index for large codebases
│  └─ copilot-instructions.md          # GitHub Copilot instructions
├─ .vscode/
│  └─ settings.json                    # VSCode settings
├─ palettes/                           # JSON palette directory
│  ├─ glass/
│  │  └─ glass.texture-palettes.json
│  ├─ metal/
│  │  └─ iron.texture-palettes.json
│  └─ wood/
│     └─ oak.texture-palettes.json
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
├─ textures_output/                    # Texture PNG's which have been recolored
└─ tools/
   └─ btg.py                           # Main script for batch texture generation

```

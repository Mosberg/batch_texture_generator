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
  --output output/textures/item
```

## Notes

- Palettes must use 8-digit RGBA hex: `#RRGGBBAA`.
- Schemas live in `schemas/` and are mapped in `.vscode/settings.json`.

## Output

- Recolored textures are saved to `output/textures/item/`.
- Generated item models are saved to `output/models/item/`.
- Generated item JSONs are saved to `output/items/`.
- Language entries are saved to `output/lang/en_us.json`.

### output/items/

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/acacia_copper_barrel"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/big_acacia_black_stained_glass_flask"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/copper_keg"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/medium_acacia_black_stained_glass_flask"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/small_acacia_black_stained_glass_flask"
  }
}
```

### output/models/item/

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/acacia_copper_barrel"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/big_acacia_black_stained_glass_flask"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/copper_keg"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/medium_acacia_black_stained_glass_flask"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/small_acacia_black_stained_glass_flask"
  }
}
```

### output/lang/en_us.json

```json
{
  "item.modid.acacia_copper_barrel": "Acacia Copper Barrel",

  "item.modid.copper_keg": "Copper Keg",

  "item.modid.small_acacia_black_stained_glass_flask": "Small Acacia Black Stained Glass Flask",

  "item.modid.medium_acacia_black_stained_glass_flask": "Medium Acacia Black Stained Glass Flask",

  "item.modid.big_acacia_black_stained_glass_flask": "Big Acacia Black Stained Glass Flask"
}
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
├─ output/                             # Texture PNG's which have been generated + models/item/ JSON's + items/ JSON's + lang/en_us.json for Minecraft
│  ├─ items/
│  │  ├─ acacia_copper_barrel.json
│  │  ├─ big_acacia_black_stained_glass_flask.json
│  │  ├─ copper_keg.json
│  │  ├─ medium_acacia_black_stained_glass_flask.json
│  │  └─ small_acacia_black_stained_glass_flask.json
│  ├─ lang/
│  │  └─ en_us.json
│  ├─ models/
│  │  └─ item/
│  │     ├─ acacia_copper_barrel.json
│  │     ├─ big_acacia_black_stained_glass_flask.json
│  │     ├─ copper_keg.json
│  │     ├─ medium_acacia_black_stained_glass_flask.json
│  │     └─ small_acacia_black_stained_glass_flask.json
│  └─ textures
│     └─ item/
│        ├─ acacia_copper_barrel.png
│        ├─ acacia_copper_exposed_barrel.png
│        ├─ acacia_copper_oxidized_barrel.png
│        ├─ acacia_copper_weathered_barrel.png
│        ├─ acacia_gold_barrel.png
│        ├─ acacia_iron_barrel.png
│        ├─ acacia_netherite_barrel.png
│        ├─ bamboo_copper_barrel.png
│        ├─ bamboo_copper_exposed_barrel.png
│        ├─ bamboo_copper_oxidized_barrel.png
│        ├─ bamboo_copper_weathered_barrel.png
│        ├─ bamboo_gold_barrel.png
│        ├─ bamboo_iron_barrel.png
│        ├─ bamboo_netherite_barrel.png
│        ├─ big_acacia_black_stained_glass_flask.png
│        ├─ big_acacia_blue_stained_glass_flask.png
│        ├─ big_acacia_brown_stained_glass_flask.png
│        ├─ big_acacia_cyan_stained_glass_flask.png
│        ├─ big_acacia_glass_flask.png
│        ├─ big_acacia_gray_stained_glass_flask.png
│        ├─ big_acacia_green_stained_glass_flask.png
│        ├─ big_acacia_light_blue_stained_glass_flask.png
│        ├─ big_acacia_light_gray_stained_glass_flask.png
│        ├─ big_acacia_lime_stained_glass_flask.png
│        ├─ big_acacia_magenta_stained_glass_flask.png
│        ├─ big_acacia_orange_stained_glass_flask.png
│        ├─ big_acacia_pink_stained_glass_flask.png
│        ├─ big_acacia_purple_stained_glass_flask.png
│        ├─ big_acacia_red_stained_glass_flask.png
│        ├─ big_acacia_tinted_glass_flask.png
│        ├─ big_acacia_white_stained_glass_flask.png
│        ├─ big_acacia_yellow_stained_glass_flask.png
│        ├─ big_bamboo_black_stained_glass_flask.png
│        ├─ big_bamboo_blue_stained_glass_flask.png
│        ├─ big_bamboo_brown_stained_glass_flask.png
│        ├─ big_bamboo_cyan_stained_glass_flask.png
│        ├─ big_bamboo_glass_flask.png
│        ├─ big_bamboo_gray_stained_glass_flask.png
│        ├─ big_bamboo_green_stained_glass_flask.png
│        ├─ big_bamboo_light_blue_stained_glass_flask.png
│        ├─ big_bamboo_light_gray_stained_glass_flask.png
│        ├─ big_bamboo_lime_stained_glass_flask.png
│        ├─ big_bamboo_magenta_stained_glass_flask.png
│        ├─ big_bamboo_orange_stained_glass_flask.png
│        ├─ big_bamboo_pink_stained_glass_flask.png
│        ├─ big_bamboo_purple_stained_glass_flask.png
│        ├─ big_bamboo_red_stained_glass_flask.png
│        ├─ big_bamboo_tinted_glass_flask.png
│        ├─ big_bamboo_white_stained_glass_flask.png
│        ├─ big_bamboo_yellow_stained_glass_flask.png
│        ├─ big_birch_black_stained_glass_flask.png
│        ├─ big_birch_blue_stained_glass_flask.png
│        ├─ big_birch_brown_stained_glass_flask.png
│        ├─ big_birch_cyan_stained_glass_flask.png
│        ├─ big_birch_glass_flask.png
│        ├─ big_birch_gray_stained_glass_flask.png
│        ├─ big_birch_green_stained_glass_flask.png
│        ├─ big_birch_light_blue_stained_glass_flask.png
│        ├─ big_birch_light_gray_stained_glass_flask.png
│        ├─ big_birch_lime_stained_glass_flask.png
│        ├─ big_birch_magenta_stained_glass_flask.png
│        ├─ big_birch_orange_stained_glass_flask.png
│        ├─ big_birch_pink_stained_glass_flask.png
│        ├─ big_birch_purple_stained_glass_flask.png
│        ├─ big_birch_red_stained_glass_flask.png
│        ├─ big_birch_tinted_glass_flask.png
│        ├─ big_birch_white_stained_glass_flask.png
│        ├─ big_birch_yellow_stained_glass_flask.png
│        ├─ big_cherry_black_stained_glass_flask.png
│        ├─ big_cherry_blue_stained_glass_flask.png
│        ├─ big_cherry_brown_stained_glass_flask.png
│        ├─ big_cherry_cyan_stained_glass_flask.png
│        ├─ big_cherry_glass_flask.png
│        ├─ big_cherry_gray_stained_glass_flask.png
│        ├─ big_cherry_green_stained_glass_flask.png
│        ├─ big_cherry_light_blue_stained_glass_flask.png
│        ├─ big_cherry_light_gray_stained_glass_flask.png
│        ├─ big_cherry_lime_stained_glass_flask.png
│        ├─ big_cherry_magenta_stained_glass_flask.png
│        ├─ big_cherry_orange_stained_glass_flask.png
│        ├─ big_cherry_pink_stained_glass_flask.png
│        ├─ big_cherry_purple_stained_glass_flask.png
│        ├─ big_cherry_red_stained_glass_flask.png
│        ├─ big_cherry_tinted_glass_flask.png
│        ├─ big_cherry_white_stained_glass_flask.png
│        ├─ big_cherry_yellow_stained_glass_flask.png
│        ├─ big_crimson_black_stained_glass_flask.png
│        ├─ big_crimson_blue_stained_glass_flask.png
│        ├─ big_crimson_brown_stained_glass_flask.png
│        ├─ big_crimson_cyan_stained_glass_flask.png
│        ├─ big_crimson_glass_flask.png
│        ├─ big_crimson_gray_stained_glass_flask.png
│        ├─ big_crimson_green_stained_glass_flask.png
│        ├─ big_crimson_light_blue_stained_glass_flask.png
│        ├─ big_crimson_light_gray_stained_glass_flask.png
│        ├─ big_crimson_lime_stained_glass_flask.png
│        ├─ big_crimson_magenta_stained_glass_flask.png
│        ├─ big_crimson_orange_stained_glass_flask.png
│        ├─ big_crimson_pink_stained_glass_flask.png
│        ├─ big_crimson_purple_stained_glass_flask.png
│        ├─ big_crimson_red_stained_glass_flask.png
│        ├─ big_crimson_tinted_glass_flask.png
│        ├─ big_crimson_white_stained_glass_flask.png
│        ├─ big_crimson_yellow_stained_glass_flask.png
│        ├─ big_dark_oak_black_stained_glass_flask.png
│        ├─ big_dark_oak_blue_stained_glass_flask.png
│        ├─ big_dark_oak_brown_stained_glass_flask.png
│        ├─ big_dark_oak_cyan_stained_glass_flask.png
│        ├─ big_dark_oak_glass_flask.png
│        ├─ big_dark_oak_gray_stained_glass_flask.png
│        ├─ big_dark_oak_green_stained_glass_flask.png
│        ├─ big_dark_oak_light_blue_stained_glass_flask.png
│        ├─ big_dark_oak_light_gray_stained_glass_flask.png
│        ├─ big_dark_oak_lime_stained_glass_flask.png
│        ├─ big_dark_oak_magenta_stained_glass_flask.png
│        ├─ big_dark_oak_orange_stained_glass_flask.png
│        ├─ big_dark_oak_pink_stained_glass_flask.png
│        ├─ big_dark_oak_purple_stained_glass_flask.png
│        ├─ big_dark_oak_red_stained_glass_flask.png
│        ├─ big_dark_oak_tinted_glass_flask.png
│        ├─ big_dark_oak_white_stained_glass_flask.png
│        ├─ big_dark_oak_yellow_stained_glass_flask.png
│        ├─ big_jungle_black_stained_glass_flask.png
│        ├─ big_jungle_blue_stained_glass_flask.png
│        ├─ big_jungle_brown_stained_glass_flask.png
│        ├─ big_jungle_cyan_stained_glass_flask.png
│        ├─ big_jungle_glass_flask.png
│        ├─ big_jungle_gray_stained_glass_flask.png
│        ├─ big_jungle_green_stained_glass_flask.png
│        ├─ big_jungle_light_blue_stained_glass_flask.png
│        ├─ big_jungle_light_gray_stained_glass_flask.png
│        ├─ big_jungle_lime_stained_glass_flask.png
│        ├─ big_jungle_magenta_stained_glass_flask.png
│        ├─ big_jungle_orange_stained_glass_flask.png
│        ├─ big_jungle_pink_stained_glass_flask.png
│        ├─ big_jungle_purple_stained_glass_flask.png
│        ├─ big_jungle_red_stained_glass_flask.png
│        ├─ big_jungle_tinted_glass_flask.png
│        ├─ big_jungle_white_stained_glass_flask.png
│        ├─ big_jungle_yellow_stained_glass_flask.png
│        ├─ big_mangrove_black_stained_glass_flask.png
│        ├─ big_mangrove_blue_stained_glass_flask.png
│        ├─ big_mangrove_brown_stained_glass_flask.png
│        ├─ big_mangrove_cyan_stained_glass_flask.png
│        ├─ big_mangrove_glass_flask.png
│        ├─ big_mangrove_gray_stained_glass_flask.png
│        ├─ big_mangrove_green_stained_glass_flask.png
│        ├─ big_mangrove_light_blue_stained_glass_flask.png
│        ├─ big_mangrove_light_gray_stained_glass_flask.png
│        ├─ big_mangrove_lime_stained_glass_flask.png
│        ├─ big_mangrove_magenta_stained_glass_flask.png
│        ├─ big_mangrove_orange_stained_glass_flask.png
│        ├─ big_mangrove_pink_stained_glass_flask.png
│        ├─ big_mangrove_purple_stained_glass_flask.png
│        ├─ big_mangrove_red_stained_glass_flask.png
│        ├─ big_mangrove_tinted_glass_flask.png
│        ├─ big_mangrove_white_stained_glass_flask.png
│        ├─ big_mangrove_yellow_stained_glass_flask.png
│        ├─ big_oak_black_stained_glass_flask.png
│        ├─ big_oak_blue_stained_glass_flask.png
│        ├─ big_oak_brown_stained_glass_flask.png
│        ├─ big_oak_cyan_stained_glass_flask.png
│        ├─ big_oak_glass_flask.png
│        ├─ big_oak_gray_stained_glass_flask.png
│        ├─ big_oak_green_stained_glass_flask.png
│        ├─ big_oak_light_blue_stained_glass_flask.png
│        ├─ big_oak_light_gray_stained_glass_flask.png
│        ├─ big_oak_lime_stained_glass_flask.png
│        ├─ big_oak_magenta_stained_glass_flask.png
│        ├─ big_oak_orange_stained_glass_flask.png
│        ├─ big_oak_pink_stained_glass_flask.png
│        ├─ big_oak_purple_stained_glass_flask.png
│        ├─ big_oak_red_stained_glass_flask.png
│        ├─ big_oak_tinted_glass_flask.png
│        ├─ big_oak_white_stained_glass_flask.png
│        ├─ big_oak_yellow_stained_glass_flask.png
│        ├─ big_pale_oak_black_stained_glass_flask.png
│        ├─ big_pale_oak_blue_stained_glass_flask.png
│        ├─ big_pale_oak_brown_stained_glass_flask.png
│        ├─ big_pale_oak_cyan_stained_glass_flask.png
│        ├─ big_pale_oak_glass_flask.png
│        ├─ big_pale_oak_gray_stained_glass_flask.png
│        ├─ big_pale_oak_green_stained_glass_flask.png
│        ├─ big_pale_oak_light_blue_stained_glass_flask.png
│        ├─ big_pale_oak_light_gray_stained_glass_flask.png
│        ├─ big_pale_oak_lime_stained_glass_flask.png
│        ├─ big_pale_oak_magenta_stained_glass_flask.png
│        ├─ big_pale_oak_orange_stained_glass_flask.png
│        ├─ big_pale_oak_pink_stained_glass_flask.png
│        ├─ big_pale_oak_purple_stained_glass_flask.png
│        ├─ big_pale_oak_red_stained_glass_flask.png
│        ├─ big_pale_oak_tinted_glass_flask.png
│        ├─ big_pale_oak_white_stained_glass_flask.png
│        ├─ big_pale_oak_yellow_stained_glass_flask.png
│        ├─ big_spruce_black_stained_glass_flask.png
│        ├─ big_spruce_blue_stained_glass_flask.png
│        ├─ big_spruce_brown_stained_glass_flask.png
│        ├─ big_spruce_cyan_stained_glass_flask.png
│        ├─ big_spruce_glass_flask.png
│        ├─ big_spruce_gray_stained_glass_flask.png
│        ├─ big_spruce_green_stained_glass_flask.png
│        ├─ big_spruce_light_blue_stained_glass_flask.png
│        ├─ big_spruce_light_gray_stained_glass_flask.png
│        ├─ big_spruce_lime_stained_glass_flask.png
│        ├─ big_spruce_magenta_stained_glass_flask.png
│        ├─ big_spruce_orange_stained_glass_flask.png
│        ├─ big_spruce_pink_stained_glass_flask.png
│        ├─ big_spruce_purple_stained_glass_flask.png
│        ├─ big_spruce_red_stained_glass_flask.png
│        ├─ big_spruce_tinted_glass_flask.png
│        ├─ big_spruce_white_stained_glass_flask.png
│        ├─ big_spruce_yellow_stained_glass_flask.png
│        ├─ big_warped_black_stained_glass_flask.png
│        ├─ big_warped_blue_stained_glass_flask.png
│        ├─ big_warped_brown_stained_glass_flask.png
│        ├─ big_warped_cyan_stained_glass_flask.png
│        ├─ big_warped_glass_flask.png
│        ├─ big_warped_gray_stained_glass_flask.png
│        ├─ big_warped_green_stained_glass_flask.png
│        ├─ big_warped_light_blue_stained_glass_flask.png
│        ├─ big_warped_light_gray_stained_glass_flask.png
│        ├─ big_warped_lime_stained_glass_flask.png
│        ├─ big_warped_magenta_stained_glass_flask.png
│        ├─ big_warped_orange_stained_glass_flask.png
│        ├─ big_warped_pink_stained_glass_flask.png
│        ├─ big_warped_purple_stained_glass_flask.png
│        ├─ big_warped_red_stained_glass_flask.png
│        ├─ big_warped_tinted_glass_flask.png
│        ├─ big_warped_white_stained_glass_flask.png
│        ├─ big_warped_yellow_stained_glass_flask.png
│        ├─ birch_copper_barrel.png
│        ├─ birch_copper_exposed_barrel.png
│        ├─ birch_copper_oxidized_barrel.png
│        ├─ birch_copper_weathered_barrel.png
│        ├─ birch_gold_barrel.png
│        ├─ birch_iron_barrel.png
│        ├─ birch_netherite_barrel.png
│        ├─ cherry_copper_barrel.png
│        ├─ cherry_copper_exposed_barrel.png
│        ├─ cherry_copper_oxidized_barrel.png
│        ├─ cherry_copper_weathered_barrel.png
│        ├─ cherry_gold_barrel.png
│        ├─ cherry_iron_barrel.png
│        ├─ cherry_netherite_barrel.png
│        ├─ copper_exposed_keg.png
│        ├─ copper_keg.png
│        ├─ copper_oxidized_keg.png
│        ├─ copper_weathered_keg.png
│        ├─ crimson_copper_barrel.png
│        ├─ crimson_copper_exposed_barrel.png
│        ├─ crimson_copper_oxidized_barrel.png
│        ├─ crimson_copper_weathered_barrel.png
│        ├─ crimson_gold_barrel.png
│        ├─ crimson_iron_barrel.png
│        ├─ crimson_netherite_barrel.png
│        ├─ dark_oak_copper_barrel.png
│        ├─ dark_oak_copper_exposed_barrel.png
│        ├─ dark_oak_copper_oxidized_barrel.png
│        ├─ dark_oak_copper_weathered_barrel.png
│        ├─ dark_oak_gold_barrel.png
│        ├─ dark_oak_iron_barrel.png
│        ├─ dark_oak_netherite_barrel.png
│        ├─ gold_keg.png
│        ├─ iron_keg.png
│        ├─ jungle_copper_barrel.png
│        ├─ jungle_copper_exposed_barrel.png
│        ├─ jungle_copper_oxidized_barrel.png
│        ├─ jungle_copper_weathered_barrel.png
│        ├─ jungle_gold_barrel.png
│        ├─ jungle_iron_barrel.png
│        ├─ jungle_netherite_barrel.png
│        ├─ mangrove_copper_barrel.png
│        ├─ mangrove_copper_exposed_barrel.png
│        ├─ mangrove_copper_oxidized_barrel.png
│        ├─ mangrove_copper_weathered_barrel.png
│        ├─ mangrove_gold_barrel.png
│        ├─ mangrove_iron_barrel.png
│        ├─ mangrove_netherite_barrel.png
│        ├─ medium_acacia_black_stained_glass_flask.png
│        ├─ medium_acacia_blue_stained_glass_flask.png
│        ├─ medium_acacia_brown_stained_glass_flask.png
│        ├─ medium_acacia_cyan_stained_glass_flask.png
│        ├─ medium_acacia_glass_flask.png
│        ├─ medium_acacia_gray_stained_glass_flask.png
│        ├─ medium_acacia_green_stained_glass_flask.png
│        ├─ medium_acacia_light_blue_stained_glass_flask.png
│        ├─ medium_acacia_light_gray_stained_glass_flask.png
│        ├─ medium_acacia_lime_stained_glass_flask.png
│        ├─ medium_acacia_magenta_stained_glass_flask.png
│        ├─ medium_acacia_orange_stained_glass_flask.png
│        ├─ medium_acacia_pink_stained_glass_flask.png
│        ├─ medium_acacia_purple_stained_glass_flask.png
│        ├─ medium_acacia_red_stained_glass_flask.png
│        ├─ medium_acacia_tinted_glass_flask.png
│        ├─ medium_acacia_white_stained_glass_flask.png
│        ├─ medium_acacia_yellow_stained_glass_flask.png
│        ├─ medium_bamboo_black_stained_glass_flask.png
│        ├─ medium_bamboo_blue_stained_glass_flask.png
│        ├─ medium_bamboo_brown_stained_glass_flask.png
│        ├─ medium_bamboo_cyan_stained_glass_flask.png
│        ├─ medium_bamboo_glass_flask.png
│        ├─ medium_bamboo_gray_stained_glass_flask.png
│        ├─ medium_bamboo_green_stained_glass_flask.png
│        ├─ medium_bamboo_light_blue_stained_glass_flask.png
│        ├─ medium_bamboo_light_gray_stained_glass_flask.png
│        ├─ medium_bamboo_lime_stained_glass_flask.png
│        ├─ medium_bamboo_magenta_stained_glass_flask.png
│        ├─ medium_bamboo_orange_stained_glass_flask.png
│        ├─ medium_bamboo_pink_stained_glass_flask.png
│        ├─ medium_bamboo_purple_stained_glass_flask.png
│        ├─ medium_bamboo_red_stained_glass_flask.png
│        ├─ medium_bamboo_tinted_glass_flask.png
│        ├─ medium_bamboo_white_stained_glass_flask.png
│        ├─ medium_bamboo_yellow_stained_glass_flask.png
│        ├─ medium_birch_black_stained_glass_flask.png
│        ├─ medium_birch_blue_stained_glass_flask.png
│        ├─ medium_birch_brown_stained_glass_flask.png
│        ├─ medium_birch_cyan_stained_glass_flask.png
│        ├─ medium_birch_glass_flask.png
│        ├─ medium_birch_gray_stained_glass_flask.png
│        ├─ medium_birch_green_stained_glass_flask.png
│        ├─ medium_birch_light_blue_stained_glass_flask.png
│        ├─ medium_birch_light_gray_stained_glass_flask.png
│        ├─ medium_birch_lime_stained_glass_flask.png
│        ├─ medium_birch_magenta_stained_glass_flask.png
│        ├─ medium_birch_orange_stained_glass_flask.png
│        ├─ medium_birch_pink_stained_glass_flask.png
│        ├─ medium_birch_purple_stained_glass_flask.png
│        ├─ medium_birch_red_stained_glass_flask.png
│        ├─ medium_birch_tinted_glass_flask.png
│        ├─ medium_birch_white_stained_glass_flask.png
│        ├─ medium_birch_yellow_stained_glass_flask.png
│        ├─ medium_cherry_black_stained_glass_flask.png
│        ├─ medium_cherry_blue_stained_glass_flask.png
│        ├─ medium_cherry_brown_stained_glass_flask.png
│        ├─ medium_cherry_cyan_stained_glass_flask.png
│        ├─ medium_cherry_glass_flask.png
│        ├─ medium_cherry_gray_stained_glass_flask.png
│        ├─ medium_cherry_green_stained_glass_flask.png
│        ├─ medium_cherry_light_blue_stained_glass_flask.png
│        ├─ medium_cherry_light_gray_stained_glass_flask.png
│        ├─ medium_cherry_lime_stained_glass_flask.png
│        ├─ medium_cherry_magenta_stained_glass_flask.png
│        ├─ medium_cherry_orange_stained_glass_flask.png
│        ├─ medium_cherry_pink_stained_glass_flask.png
│        ├─ medium_cherry_purple_stained_glass_flask.png
│        ├─ medium_cherry_red_stained_glass_flask.png
│        ├─ medium_cherry_tinted_glass_flask.png
│        ├─ medium_cherry_white_stained_glass_flask.png
│        ├─ medium_cherry_yellow_stained_glass_flask.png
│        ├─ medium_crimson_black_stained_glass_flask.png
│        ├─ medium_crimson_blue_stained_glass_flask.png
│        ├─ medium_crimson_brown_stained_glass_flask.png
│        ├─ medium_crimson_cyan_stained_glass_flask.png
│        ├─ medium_crimson_glass_flask.png
│        ├─ medium_crimson_gray_stained_glass_flask.png
│        ├─ medium_crimson_green_stained_glass_flask.png
│        ├─ medium_crimson_light_blue_stained_glass_flask.png
│        ├─ medium_crimson_light_gray_stained_glass_flask.png
│        ├─ medium_crimson_lime_stained_glass_flask.png
│        ├─ medium_crimson_magenta_stained_glass_flask.png
│        ├─ medium_crimson_orange_stained_glass_flask.png
│        ├─ medium_crimson_pink_stained_glass_flask.png
│        ├─ medium_crimson_purple_stained_glass_flask.png
│        ├─ medium_crimson_red_stained_glass_flask.png
│        ├─ medium_crimson_tinted_glass_flask.png
│        ├─ medium_crimson_white_stained_glass_flask.png
│        ├─ medium_crimson_yellow_stained_glass_flask.png
│        ├─ medium_dark_oak_black_stained_glass_flask.png
│        ├─ medium_dark_oak_blue_stained_glass_flask.png
│        ├─ medium_dark_oak_brown_stained_glass_flask.png
│        ├─ medium_dark_oak_cyan_stained_glass_flask.png
│        ├─ medium_dark_oak_glass_flask.png
│        ├─ medium_dark_oak_gray_stained_glass_flask.png
│        ├─ medium_dark_oak_green_stained_glass_flask.png
│        ├─ medium_dark_oak_light_blue_stained_glass_flask.png
│        ├─ medium_dark_oak_light_gray_stained_glass_flask.png
│        ├─ medium_dark_oak_lime_stained_glass_flask.png
│        ├─ medium_dark_oak_magenta_stained_glass_flask.png
│        ├─ medium_dark_oak_orange_stained_glass_flask.png
│        ├─ medium_dark_oak_pink_stained_glass_flask.png
│        ├─ medium_dark_oak_purple_stained_glass_flask.png
│        ├─ medium_dark_oak_red_stained_glass_flask.png
│        ├─ medium_dark_oak_tinted_glass_flask.png
│        ├─ medium_dark_oak_white_stained_glass_flask.png
│        ├─ medium_dark_oak_yellow_stained_glass_flask.png
│        ├─ medium_jungle_black_stained_glass_flask.png
│        ├─ medium_jungle_blue_stained_glass_flask.png
│        ├─ medium_jungle_brown_stained_glass_flask.png
│        ├─ medium_jungle_cyan_stained_glass_flask.png
│        ├─ medium_jungle_glass_flask.png
│        ├─ medium_jungle_gray_stained_glass_flask.png
│        ├─ medium_jungle_green_stained_glass_flask.png
│        ├─ medium_jungle_light_blue_stained_glass_flask.png
│        ├─ medium_jungle_light_gray_stained_glass_flask.png
│        ├─ medium_jungle_lime_stained_glass_flask.png
│        ├─ medium_jungle_magenta_stained_glass_flask.png
│        ├─ medium_jungle_orange_stained_glass_flask.png
│        ├─ medium_jungle_pink_stained_glass_flask.png
│        ├─ medium_jungle_purple_stained_glass_flask.png
│        ├─ medium_jungle_red_stained_glass_flask.png
│        ├─ medium_jungle_tinted_glass_flask.png
│        ├─ medium_jungle_white_stained_glass_flask.png
│        ├─ medium_jungle_yellow_stained_glass_flask.png
│        ├─ medium_mangrove_black_stained_glass_flask.png
│        ├─ medium_mangrove_blue_stained_glass_flask.png
│        ├─ medium_mangrove_brown_stained_glass_flask.png
│        ├─ medium_mangrove_cyan_stained_glass_flask.png
│        ├─ medium_mangrove_glass_flask.png
│        ├─ medium_mangrove_gray_stained_glass_flask.png
│        ├─ medium_mangrove_green_stained_glass_flask.png
│        ├─ medium_mangrove_light_blue_stained_glass_flask.png
│        ├─ medium_mangrove_light_gray_stained_glass_flask.png
│        ├─ medium_mangrove_lime_stained_glass_flask.png
│        ├─ medium_mangrove_magenta_stained_glass_flask.png
│        ├─ medium_mangrove_orange_stained_glass_flask.png
│        ├─ medium_mangrove_pink_stained_glass_flask.png
│        ├─ medium_mangrove_purple_stained_glass_flask.png
│        ├─ medium_mangrove_red_stained_glass_flask.png
│        ├─ medium_mangrove_tinted_glass_flask.png
│        ├─ medium_mangrove_white_stained_glass_flask.png
│        ├─ medium_mangrove_yellow_stained_glass_flask.png
│        ├─ medium_oak_black_stained_glass_flask.png
│        ├─ medium_oak_blue_stained_glass_flask.png
│        ├─ medium_oak_brown_stained_glass_flask.png
│        ├─ medium_oak_cyan_stained_glass_flask.png
│        ├─ medium_oak_glass_flask.png
│        ├─ medium_oak_gray_stained_glass_flask.png
│        ├─ medium_oak_green_stained_glass_flask.png
│        ├─ medium_oak_light_blue_stained_glass_flask.png
│        ├─ medium_oak_light_gray_stained_glass_flask.png
│        ├─ medium_oak_lime_stained_glass_flask.png
│        ├─ medium_oak_magenta_stained_glass_flask.png
│        ├─ medium_oak_orange_stained_glass_flask.png
│        ├─ medium_oak_pink_stained_glass_flask.png
│        ├─ medium_oak_purple_stained_glass_flask.png
│        ├─ medium_oak_red_stained_glass_flask.png
│        ├─ medium_oak_tinted_glass_flask.png
│        ├─ medium_oak_white_stained_glass_flask.png
│        ├─ medium_oak_yellow_stained_glass_flask.png
│        ├─ medium_pale_oak_black_stained_glass_flask.png
│        ├─ medium_pale_oak_blue_stained_glass_flask.png
│        ├─ medium_pale_oak_brown_stained_glass_flask.png
│        ├─ medium_pale_oak_cyan_stained_glass_flask.png
│        ├─ medium_pale_oak_glass_flask.png
│        ├─ medium_pale_oak_gray_stained_glass_flask.png
│        ├─ medium_pale_oak_green_stained_glass_flask.png
│        ├─ medium_pale_oak_light_blue_stained_glass_flask.png
│        ├─ medium_pale_oak_light_gray_stained_glass_flask.png
│        ├─ medium_pale_oak_lime_stained_glass_flask.png
│        ├─ medium_pale_oak_magenta_stained_glass_flask.png
│        ├─ medium_pale_oak_orange_stained_glass_flask.png
│        ├─ medium_pale_oak_pink_stained_glass_flask.png
│        ├─ medium_pale_oak_purple_stained_glass_flask.png
│        ├─ medium_pale_oak_red_stained_glass_flask.png
│        ├─ medium_pale_oak_tinted_glass_flask.png
│        ├─ medium_pale_oak_white_stained_glass_flask.png
│        ├─ medium_pale_oak_yellow_stained_glass_flask.png
│        ├─ medium_spruce_black_stained_glass_flask.png
│        ├─ medium_spruce_blue_stained_glass_flask.png
│        ├─ medium_spruce_brown_stained_glass_flask.png
│        ├─ medium_spruce_cyan_stained_glass_flask.png
│        ├─ medium_spruce_glass_flask.png
│        ├─ medium_spruce_gray_stained_glass_flask.png
│        ├─ medium_spruce_green_stained_glass_flask.png
│        ├─ medium_spruce_light_blue_stained_glass_flask.png
│        ├─ medium_spruce_light_gray_stained_glass_flask.png
│        ├─ medium_spruce_lime_stained_glass_flask.png
│        ├─ medium_spruce_magenta_stained_glass_flask.png
│        ├─ medium_spruce_orange_stained_glass_flask.png
│        ├─ medium_spruce_pink_stained_glass_flask.png
│        ├─ medium_spruce_purple_stained_glass_flask.png
│        ├─ medium_spruce_red_stained_glass_flask.png
│        ├─ medium_spruce_tinted_glass_flask.png
│        ├─ medium_spruce_white_stained_glass_flask.png
│        ├─ medium_spruce_yellow_stained_glass_flask.png
│        ├─ medium_warped_black_stained_glass_flask.png
│        ├─ medium_warped_blue_stained_glass_flask.png
│        ├─ medium_warped_brown_stained_glass_flask.png
│        ├─ medium_warped_cyan_stained_glass_flask.png
│        ├─ medium_warped_glass_flask.png
│        ├─ medium_warped_gray_stained_glass_flask.png
│        ├─ medium_warped_green_stained_glass_flask.png
│        ├─ medium_warped_light_blue_stained_glass_flask.png
│        ├─ medium_warped_light_gray_stained_glass_flask.png
│        ├─ medium_warped_lime_stained_glass_flask.png
│        ├─ medium_warped_magenta_stained_glass_flask.png
│        ├─ medium_warped_orange_stained_glass_flask.png
│        ├─ medium_warped_pink_stained_glass_flask.png
│        ├─ medium_warped_purple_stained_glass_flask.png
│        ├─ medium_warped_red_stained_glass_flask.png
│        ├─ medium_warped_tinted_glass_flask.png
│        ├─ medium_warped_white_stained_glass_flask.png
│        ├─ medium_warped_yellow_stained_glass_flask.png
│        ├─ netherite_keg.png
│        ├─ oak_copper_barrel.png
│        ├─ oak_copper_exposed_barrel.png
│        ├─ oak_copper_oxidized_barrel.png
│        ├─ oak_copper_weathered_barrel.png
│        ├─ oak_gold_barrel.png
│        ├─ oak_iron_barrel.png
│        ├─ oak_netherite_barrel.png
│        ├─ pale_oak_copper_barrel.png
│        ├─ pale_oak_copper_exposed_barrel.png
│        ├─ pale_oak_copper_oxidized_barrel.png
│        ├─ pale_oak_copper_weathered_barrel.png
│        ├─ pale_oak_gold_barrel.png
│        ├─ pale_oak_iron_barrel.png
│        ├─ pale_oak_netherite_barrel.png
│        ├─ small_acacia_black_stained_glass_flask.png
│        ├─ small_acacia_blue_stained_glass_flask.png
│        ├─ small_acacia_brown_stained_glass_flask.png
│        ├─ small_acacia_cyan_stained_glass_flask.png
│        ├─ small_acacia_glass_flask.png
│        ├─ small_acacia_gray_stained_glass_flask.png
│        ├─ small_acacia_green_stained_glass_flask.png
│        ├─ small_acacia_light_blue_stained_glass_flask.png
│        ├─ small_acacia_light_gray_stained_glass_flask.png
│        ├─ small_acacia_lime_stained_glass_flask.png
│        ├─ small_acacia_magenta_stained_glass_flask.png
│        ├─ small_acacia_orange_stained_glass_flask.png
│        ├─ small_acacia_pink_stained_glass_flask.png
│        ├─ small_acacia_purple_stained_glass_flask.png
│        ├─ small_acacia_red_stained_glass_flask.png
│        ├─ small_acacia_tinted_glass_flask.png
│        ├─ small_acacia_white_stained_glass_flask.png
│        ├─ small_acacia_yellow_stained_glass_flask.png
│        ├─ small_bamboo_black_stained_glass_flask.png
│        ├─ small_bamboo_blue_stained_glass_flask.png
│        ├─ small_bamboo_brown_stained_glass_flask.png
│        ├─ small_bamboo_cyan_stained_glass_flask.png
│        ├─ small_bamboo_glass_flask.png
│        ├─ small_bamboo_gray_stained_glass_flask.png
│        ├─ small_bamboo_green_stained_glass_flask.png
│        ├─ small_bamboo_light_blue_stained_glass_flask.png
│        ├─ small_bamboo_light_gray_stained_glass_flask.png
│        ├─ small_bamboo_lime_stained_glass_flask.png
│        ├─ small_bamboo_magenta_stained_glass_flask.png
│        ├─ small_bamboo_orange_stained_glass_flask.png
│        ├─ small_bamboo_pink_stained_glass_flask.png
│        ├─ small_bamboo_purple_stained_glass_flask.png
│        ├─ small_bamboo_red_stained_glass_flask.png
│        ├─ small_bamboo_tinted_glass_flask.png
│        ├─ small_bamboo_white_stained_glass_flask.png
│        ├─ small_bamboo_yellow_stained_glass_flask.png
│        ├─ small_birch_black_stained_glass_flask.png
│        ├─ small_birch_blue_stained_glass_flask.png
│        ├─ small_birch_brown_stained_glass_flask.png
│        ├─ small_birch_cyan_stained_glass_flask.png
│        ├─ small_birch_glass_flask.png
│        ├─ small_birch_gray_stained_glass_flask.png
│        ├─ small_birch_green_stained_glass_flask.png
│        ├─ small_birch_light_blue_stained_glass_flask.png
│        ├─ small_birch_light_gray_stained_glass_flask.png
│        ├─ small_birch_lime_stained_glass_flask.png
│        ├─ small_birch_magenta_stained_glass_flask.png
│        ├─ small_birch_orange_stained_glass_flask.png
│        ├─ small_birch_pink_stained_glass_flask.png
│        ├─ small_birch_purple_stained_glass_flask.png
│        ├─ small_birch_red_stained_glass_flask.png
│        ├─ small_birch_tinted_glass_flask.png
│        ├─ small_birch_white_stained_glass_flask.png
│        ├─ small_birch_yellow_stained_glass_flask.png
│        ├─ small_cherry_black_stained_glass_flask.png
│        ├─ small_cherry_blue_stained_glass_flask.png
│        ├─ small_cherry_brown_stained_glass_flask.png
│        ├─ small_cherry_cyan_stained_glass_flask.png
│        ├─ small_cherry_glass_flask.png
│        ├─ small_cherry_gray_stained_glass_flask.png
│        ├─ small_cherry_green_stained_glass_flask.png
│        ├─ small_cherry_light_blue_stained_glass_flask.png
│        ├─ small_cherry_light_gray_stained_glass_flask.png
│        ├─ small_cherry_lime_stained_glass_flask.png
│        ├─ small_cherry_magenta_stained_glass_flask.png
│        ├─ small_cherry_orange_stained_glass_flask.png
│        ├─ small_cherry_pink_stained_glass_flask.png
│        ├─ small_cherry_purple_stained_glass_flask.png
│        ├─ small_cherry_red_stained_glass_flask.png
│        ├─ small_cherry_tinted_glass_flask.png
│        ├─ small_cherry_white_stained_glass_flask.png
│        ├─ small_cherry_yellow_stained_glass_flask.png
│        ├─ small_crimson_black_stained_glass_flask.png
│        ├─ small_crimson_blue_stained_glass_flask.png
│        ├─ small_crimson_brown_stained_glass_flask.png
│        ├─ small_crimson_cyan_stained_glass_flask.png
│        ├─ small_crimson_glass_flask.png
│        ├─ small_crimson_gray_stained_glass_flask.png
│        ├─ small_crimson_green_stained_glass_flask.png
│        ├─ small_crimson_light_blue_stained_glass_flask.png
│        ├─ small_crimson_light_gray_stained_glass_flask.png
│        ├─ small_crimson_lime_stained_glass_flask.png
│        ├─ small_crimson_magenta_stained_glass_flask.png
│        ├─ small_crimson_orange_stained_glass_flask.png
│        ├─ small_crimson_pink_stained_glass_flask.png
│        ├─ small_crimson_purple_stained_glass_flask.png
│        ├─ small_crimson_red_stained_glass_flask.png
│        ├─ small_crimson_tinted_glass_flask.png
│        ├─ small_crimson_white_stained_glass_flask.png
│        ├─ small_crimson_yellow_stained_glass_flask.png
│        ├─ small_dark_oak_black_stained_glass_flask.png
│        ├─ small_dark_oak_blue_stained_glass_flask.png
│        ├─ small_dark_oak_brown_stained_glass_flask.png
│        ├─ small_dark_oak_cyan_stained_glass_flask.png
│        ├─ small_dark_oak_glass_flask.png
│        ├─ small_dark_oak_gray_stained_glass_flask.png
│        ├─ small_dark_oak_green_stained_glass_flask.png
│        ├─ small_dark_oak_light_blue_stained_glass_flask.png
│        ├─ small_dark_oak_light_gray_stained_glass_flask.png
│        ├─ small_dark_oak_lime_stained_glass_flask.png
│        ├─ small_dark_oak_magenta_stained_glass_flask.png
│        ├─ small_dark_oak_orange_stained_glass_flask.png
│        ├─ small_dark_oak_pink_stained_glass_flask.png
│        ├─ small_dark_oak_purple_stained_glass_flask.png
│        ├─ small_dark_oak_red_stained_glass_flask.png
│        ├─ small_dark_oak_tinted_glass_flask.png
│        ├─ small_dark_oak_white_stained_glass_flask.png
│        ├─ small_dark_oak_yellow_stained_glass_flask.png
│        ├─ small_jungle_black_stained_glass_flask.png
│        ├─ small_jungle_blue_stained_glass_flask.png
│        ├─ small_jungle_brown_stained_glass_flask.png
│        ├─ small_jungle_cyan_stained_glass_flask.png
│        ├─ small_jungle_glass_flask.png
│        ├─ small_jungle_gray_stained_glass_flask.png
│        ├─ small_jungle_green_stained_glass_flask.png
│        ├─ small_jungle_light_blue_stained_glass_flask.png
│        ├─ small_jungle_light_gray_stained_glass_flask.png
│        ├─ small_jungle_lime_stained_glass_flask.png
│        ├─ small_jungle_magenta_stained_glass_flask.png
│        ├─ small_jungle_orange_stained_glass_flask.png
│        ├─ small_jungle_pink_stained_glass_flask.png
│        ├─ small_jungle_purple_stained_glass_flask.png
│        ├─ small_jungle_red_stained_glass_flask.png
│        ├─ small_jungle_tinted_glass_flask.png
│        ├─ small_jungle_white_stained_glass_flask.png
│        ├─ small_jungle_yellow_stained_glass_flask.png
│        ├─ small_mangrove_black_stained_glass_flask.png
│        ├─ small_mangrove_blue_stained_glass_flask.png
│        ├─ small_mangrove_brown_stained_glass_flask.png
│        ├─ small_mangrove_cyan_stained_glass_flask.png
│        ├─ small_mangrove_glass_flask.png
│        ├─ small_mangrove_gray_stained_glass_flask.png
│        ├─ small_mangrove_green_stained_glass_flask.png
│        ├─ small_mangrove_light_blue_stained_glass_flask.png
│        ├─ small_mangrove_light_gray_stained_glass_flask.png
│        ├─ small_mangrove_lime_stained_glass_flask.png
│        ├─ small_mangrove_magenta_stained_glass_flask.png
│        ├─ small_mangrove_orange_stained_glass_flask.png
│        ├─ small_mangrove_pink_stained_glass_flask.png
│        ├─ small_mangrove_purple_stained_glass_flask.png
│        ├─ small_mangrove_red_stained_glass_flask.png
│        ├─ small_mangrove_tinted_glass_flask.png
│        ├─ small_mangrove_white_stained_glass_flask.png
│        ├─ small_mangrove_yellow_stained_glass_flask.png
│        ├─ small_oak_black_stained_glass_flask.png
│        ├─ small_oak_blue_stained_glass_flask.png
│        ├─ small_oak_brown_stained_glass_flask.png
│        ├─ small_oak_cyan_stained_glass_flask.png
│        ├─ small_oak_glass_flask.png
│        ├─ small_oak_gray_stained_glass_flask.png
│        ├─ small_oak_green_stained_glass_flask.png
│        ├─ small_oak_light_blue_stained_glass_flask.png
│        ├─ small_oak_light_gray_stained_glass_flask.png
│        ├─ small_oak_lime_stained_glass_flask.png
│        ├─ small_oak_magenta_stained_glass_flask.png
│        ├─ small_oak_orange_stained_glass_flask.png
│        ├─ small_oak_pink_stained_glass_flask.png
│        ├─ small_oak_purple_stained_glass_flask.png
│        ├─ small_oak_red_stained_glass_flask.png
│        ├─ small_oak_tinted_glass_flask.png
│        ├─ small_oak_white_stained_glass_flask.png
│        ├─ small_oak_yellow_stained_glass_flask.png
│        ├─ small_pale_oak_black_stained_glass_flask.png
│        ├─ small_pale_oak_blue_stained_glass_flask.png
│        ├─ small_pale_oak_brown_stained_glass_flask.png
│        ├─ small_pale_oak_cyan_stained_glass_flask.png
│        ├─ small_pale_oak_glass_flask.png
│        ├─ small_pale_oak_gray_stained_glass_flask.png
│        ├─ small_pale_oak_green_stained_glass_flask.png
│        ├─ small_pale_oak_light_blue_stained_glass_flask.png
│        ├─ small_pale_oak_light_gray_stained_glass_flask.png
│        ├─ small_pale_oak_lime_stained_glass_flask.png
│        ├─ small_pale_oak_magenta_stained_glass_flask.png
│        ├─ small_pale_oak_orange_stained_glass_flask.png
│        ├─ small_pale_oak_pink_stained_glass_flask.png
│        ├─ small_pale_oak_purple_stained_glass_flask.png
│        ├─ small_pale_oak_red_stained_glass_flask.png
│        ├─ small_pale_oak_tinted_glass_flask.png
│        ├─ small_pale_oak_white_stained_glass_flask.png
│        ├─ small_pale_oak_yellow_stained_glass_flask.png
│        ├─ small_spruce_black_stained_glass_flask.png
│        ├─ small_spruce_blue_stained_glass_flask.png
│        ├─ small_spruce_brown_stained_glass_flask.png
│        ├─ small_spruce_cyan_stained_glass_flask.png
│        ├─ small_spruce_glass_flask.png
│        ├─ small_spruce_gray_stained_glass_flask.png
│        ├─ small_spruce_green_stained_glass_flask.png
│        ├─ small_spruce_light_blue_stained_glass_flask.png
│        ├─ small_spruce_light_gray_stained_glass_flask.png
│        ├─ small_spruce_lime_stained_glass_flask.png
│        ├─ small_spruce_magenta_stained_glass_flask.png
│        ├─ small_spruce_orange_stained_glass_flask.png
│        ├─ small_spruce_pink_stained_glass_flask.png
│        ├─ small_spruce_purple_stained_glass_flask.png
│        ├─ small_spruce_red_stained_glass_flask.png
│        ├─ small_spruce_tinted_glass_flask.png
│        ├─ small_spruce_white_stained_glass_flask.png
│        ├─ small_spruce_yellow_stained_glass_flask.png
│        ├─ small_warped_black_stained_glass_flask.png
│        ├─ small_warped_blue_stained_glass_flask.png
│        ├─ small_warped_brown_stained_glass_flask.png
│        ├─ small_warped_cyan_stained_glass_flask.png
│        ├─ small_warped_glass_flask.png
│        ├─ small_warped_gray_stained_glass_flask.png
│        ├─ small_warped_green_stained_glass_flask.png
│        ├─ small_warped_light_blue_stained_glass_flask.png
│        ├─ small_warped_light_gray_stained_glass_flask.png
│        ├─ small_warped_lime_stained_glass_flask.png
│        ├─ small_warped_magenta_stained_glass_flask.png
│        ├─ small_warped_orange_stained_glass_flask.png
│        ├─ small_warped_pink_stained_glass_flask.png
│        ├─ small_warped_purple_stained_glass_flask.png
│        ├─ small_warped_red_stained_glass_flask.png
│        ├─ small_warped_tinted_glass_flask.png
│        ├─ small_warped_white_stained_glass_flask.png
│        ├─ small_warped_yellow_stained_glass_flask.png
│        ├─ spruce_copper_barrel.png
│        ├─ spruce_copper_exposed_barrel.png
│        ├─ spruce_copper_oxidized_barrel.png
│        ├─ spruce_copper_weathered_barrel.png
│        ├─ spruce_gold_barrel.png
│        ├─ spruce_iron_barrel.png
│        ├─ spruce_netherite_barrel.png
│        ├─ warped_copper_barrel.png
│        ├─ warped_copper_exposed_barrel.png
│        ├─ warped_copper_oxidized_barrel.png
│        ├─ warped_copper_weathered_barrel.png
│        ├─ warped_gold_barrel.png
│        ├─ warped_iron_barrel.png
│        └─ warped_netherite_barrel.png
└─ tools/
   ├─ btg.py                           # Main script for batch texture generation
   └─ btg_gui.py                       # GUI script for batch texture generation
```

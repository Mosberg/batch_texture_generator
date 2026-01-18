# Batch Textures and Assets Generator

**Generate several \*.py modules which all can be controlled from a main script and tkinter gui.**
**Split into several modules for better maintainability.**

## Features

- Validate
  - Check for missing files
  - Check for incorrect formats
- Normalize
  - Resize images
  - Standardize naming conventions
- Extract
  - Pull textures from source files
  - Separate assets into categories
- Recolor
  - Apply color palettes
  - Generate variations
- Legacy Templates
  - Convert old templates to new format
  - Update metadata
- Generate
  - Create new textures based on parameters
  - Batch process multiple files
- AutoTemplate
  - Automatically generate templates from existing assets
  - Suggest improvements based on asset analysis
- ItemAssets
  - Process item-specific textures
  - Create item previews
- BlockAssets
  - Handle block-specific textures
  - Generate block models and previews
- GUI
  - User-friendly interface for batch operations
  - Real-time progress updates
- Configuration management
  - Load and save user settings
  - Support for multiple configuration profiles
- Logging and error handling
  - Detailed logs for each operation
  - Graceful error recovery
- Multi-threading support
  - Parallel processing for faster execution
  - Efficient resource management

## Notes

- Palettes must use 8-digit RGBA hex: `#RRGGBBAA`.
- Schemas live in `schemas/` and are mapped in `.vscode/settings.json`.
- Input files should be placed in `input/modid/` where `modid` is your mod's identifier.

## Output

- Recolored textures are saved to `output/modid/textures/item/`.
- Generated item models are saved to `output/modid/models/item/`.
- Generated item JSONs are saved to `output/modid/items/`.
- Language entries are saved to `output/modid/lang/en_us.json`.
- Block models and blockstates are saved to `output/modid/models/block/` and `output/modid/blockstates/`.

## Examples

### examples/modid/blockstates/

```json
{
  "variants": {
    "normal": { "model": "modid:block/iron_keg_block" },
    "facing=north,open=false": {
      "model": "modid:block/iron_keg_block",
      "y": 0
    },
    "facing=east,open=false": {
      "model": "modid:block/iron_keg_block",
      "y": 90
    },
    "facing=south,open=false": {
      "model": "modid:block/iron_keg_block",
      "y": 180
    },
    "facing=west,open=false": {
      "model": "modid:block/iron_keg_block",
      "y": 270
    }
  }
}
```

```json
{
  "variants": {
    "normal": { "model": "modid:block/oak_iron_barrel_block" },
    "facing=north,open=false": {
      "model": "modid:block/oak_iron_barrel_block",
      "y": 0
    },
    "facing=east,open=false": {
      "model": "modid:block/oak_iron_barrel_block",
      "y": 90
    },
    "facing=south,open=false": {
      "model": "modid:block/oak_iron_barrel_block",
      "y": 180
    },
    "facing=west,open=false": {
      "model": "modid:block/oak_iron_barrel_block",
      "y": 270
    }
  }
}
```

### examples/modid/items/

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/big_oak_glass_flask"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/iron_keg"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/medium_oak_glass_flask"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/oak_iron_barrel"
  }
}
```

```json
{
  "model": {
    "type": "minecraft:model",
    "model": "modid:item/small_oak_glass_flask"
  }
}
```

### examples/modid/models/block/

```json
{
  "format_version": "1.21.11",
  "credit": "Made by Mosberg with Blockbench",
  "texture_size": [32, 32],
  "textures": {
    "0": "modid:block/iron_keg_block",
    "particle": "modid:block/iron_keg_block"
  },
  "elements": [
    {
      "from": [4, 0, 4],
      "to": [12, 1, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 0, 7] },
      "faces": {
        "north": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "east": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "south": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "west": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "up": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" },
        "down": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [5, 0, 3],
      "to": [11, 1, 4],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 0, 6] },
      "faces": {
        "north": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "east": { "uv": [14.5, 4.5, 15, 5], "texture": "#0" },
        "south": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "west": { "uv": [12, 4.5, 12.5, 5], "texture": "#0" },
        "up": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "down": { "uv": [12, 4.5, 15, 5], "texture": "#0" }
      }
    },
    {
      "from": [5, 0, 12],
      "to": [11, 1, 13],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 0, 15] },
      "faces": {
        "north": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "east": { "uv": [12, 0, 12.5, 0.5], "texture": "#0" },
        "south": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "west": { "uv": [14.5, 0, 15, 0.5], "texture": "#0" },
        "up": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "down": { "uv": [12, 0, 15, 0.5], "texture": "#0" }
      }
    },
    {
      "from": [12, 0, 5],
      "to": [13, 1, 11],
      "rotation": { "angle": 0, "axis": "y", "origin": [9, 0, 14] },
      "faces": {
        "north": { "uv": [11, 3.5, 11.5, 4], "texture": "#0" },
        "east": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "south": { "uv": [11, 1, 11.5, 1.5], "texture": "#0" },
        "west": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "up": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "down": { "uv": [11, 1, 11.5, 4], "texture": "#0" }
      }
    },
    {
      "from": [3, 0, 5],
      "to": [4, 1, 11],
      "rotation": { "angle": 0, "axis": "y", "origin": [0, 0, 14] },
      "faces": {
        "north": { "uv": [15.5, 3.5, 16, 4], "texture": "#0" },
        "east": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "south": { "uv": [15.5, 1, 16, 1.5], "texture": "#0" },
        "west": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "up": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "down": { "uv": [15.5, 1, 16, 4], "texture": "#0" }
      }
    },
    {
      "from": [3, 1, 3],
      "to": [13, 15, 13],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 1, 7] },
      "faces": {
        "north": { "uv": [5, 0.5, 11, 7.5], "texture": "#0" },
        "east": { "uv": [5, 0.5, 11, 7.5], "texture": "#0" },
        "south": { "uv": [5, 0.5, 11, 7.5], "texture": "#0" },
        "west": { "uv": [5, 0.5, 11, 7.5], "texture": "#0" },
        "up": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" },
        "down": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [4, 1, 2],
      "to": [12, 15, 3],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 1, 6] },
      "faces": {
        "north": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "east": { "uv": [10, 0.5, 10.5, 7.5], "texture": "#0" },
        "south": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "west": { "uv": [5.5, 0.5, 6, 7.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 7.5, 10, 8], "texture": "#0" }
      }
    },
    {
      "from": [4, 1, 13],
      "to": [12, 15, 14],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 1, 15] },
      "faces": {
        "north": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "east": { "uv": [10, 0.5, 10.5, 7.5], "texture": "#0" },
        "south": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "west": { "uv": [5.5, 0.5, 6, 7.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 7.5, 10, 8], "texture": "#0" }
      }
    },
    {
      "from": [13, 1, 4],
      "to": [14, 15, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [9, 1, 14] },
      "faces": {
        "north": { "uv": [10, 0.5, 10.5, 7.5], "texture": "#0" },
        "east": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "south": { "uv": [5.5, 0.5, 6, 7.5], "texture": "#0" },
        "west": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 7.5, 10, 8], "texture": "#0" }
      }
    },
    {
      "from": [2, 1, 4],
      "to": [3, 15, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [0, 1, 14] },
      "faces": {
        "north": { "uv": [10, 0.5, 10.5, 7.5], "texture": "#0" },
        "east": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "south": { "uv": [5.5, 0.5, 6, 7.5], "texture": "#0" },
        "west": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 7.5, 10, 8], "texture": "#0" }
      }
    },
    {
      "from": [7, 15, 7],
      "to": [9, 16, 9],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 15, 7] },
      "faces": {
        "north": { "uv": [2, 2.5, 3, 3], "texture": "#0" },
        "east": { "uv": [2, 2, 3, 2.5], "texture": "#0" },
        "south": { "uv": [2, 2.5, 3, 3], "texture": "#0" },
        "west": { "uv": [2, 2, 3, 2.5], "texture": "#0" },
        "up": { "uv": [2, 2, 3, 3], "texture": "#0" },
        "down": { "uv": [2, 2, 3, 3], "texture": "#0" }
      }
    },
    {
      "from": [4, 15, 3],
      "to": [12, 16, 4],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 15, 6] },
      "faces": {
        "north": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "east": { "uv": [10, 0, 10.5, 0.5], "texture": "#0" },
        "south": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "west": { "uv": [5.5, 0, 6, 0.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 0, 10, 0.5], "texture": "#0" }
      }
    },
    {
      "from": [4, 15, 12],
      "to": [12, 16, 13],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 15, 15] },
      "faces": {
        "north": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "east": { "uv": [6, 0, 6.5, 0.5], "texture": "#0" },
        "south": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "west": { "uv": [6, 0, 6.5, 0.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 0, 10, 0.5], "texture": "#0" }
      }
    },
    {
      "from": [12, 15, 4],
      "to": [13, 16, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [9, 15, 14] },
      "faces": {
        "north": { "uv": [6, 0, 6.5, 0.5], "texture": "#0" },
        "east": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "south": { "uv": [6, 0, 6.5, 0.5], "texture": "#0" },
        "west": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 0, 10, 0.5], "texture": "#0" }
      }
    },
    {
      "from": [3, 15, 4],
      "to": [4, 16, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [0, 15, 14] },
      "faces": {
        "north": { "uv": [6, 0, 6.5, 0.5], "texture": "#0" },
        "east": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "south": { "uv": [6, 0, 6.5, 0.5], "texture": "#0" },
        "west": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 0, 10, 0.5], "texture": "#0" }
      }
    }
  ]
}
```

````json
{
  "format_version": "1.21.11",
  "credit": "Made by Mosberg with Blockbench",
  "texture_size": [32, 32],
  "textures": {
    "0": "modid:block/oak_iron_barrel_block",
    "particle": "modid:block/oak_iron_barrel_block"
  },
  "elements": [
    {
      "from": [4, 0, 4],
      "to": [12, 1, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 0, 7] },
      "faces": {
        "north": { "uv": [11.5, 4, 15.5, 4.5], "texture": "#0" },
        "east": { "uv": [11.5, 0.5, 15.5, 1], "texture": "#0" },
        "south": { "uv": [11.5, 0.5, 15.5, 1], "texture": "#0" },
        "west": { "uv": [11.5, 4, 15.5, 4.5], "texture": "#0" },
        "up": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" },
        "down": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [5, 0, 3],
      "to": [11, 1, 4],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 0, 6] },
      "faces": {
        "north": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "east": { "uv": [14.5, 4.5, 15, 5], "texture": "#0" },
        "south": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "west": { "uv": [12, 4.5, 12.5, 5], "texture": "#0" },
        "up": { "uv": [12, 4.5, 15, 5], "texture": "#0" },
        "down": { "uv": [12, 4.5, 15, 5], "texture": "#0" }
      }
    },
    {
      "from": [5, 0, 12],
      "to": [11, 1, 13],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 0, 15] },
      "faces": {
        "north": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "east": { "uv": [14.5, 0, 15, 0.5], "texture": "#0" },
        "south": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "west": { "uv": [12, 0, 12.5, 0.5], "texture": "#0" },
        "up": { "uv": [12, 0, 15, 0.5], "texture": "#0" },
        "down": { "uv": [12, 0, 15, 0.5], "texture": "#0" }
      }
    },
    {
      "from": [12, 0, 5],
      "to": [13, 1, 11],
      "rotation": { "angle": 0, "axis": "y", "origin": [9, 0, 14] },
      "faces": {
        "north": { "uv": [15.5, 1, 16, 1.5], "texture": "#0" },
        "east": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "south": { "uv": [15.5, 3.5, 16, 4], "texture": "#0" },
        "west": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "up": { "uv": [15.5, 1, 16, 4], "texture": "#0" },
        "down": { "uv": [15.5, 1, 16, 4], "texture": "#0" }
      }
    },
    {
      "from": [3, 0, 5],
      "to": [4, 1, 11],
      "rotation": { "angle": 0, "axis": "y", "origin": [0, 0, 14] },
      "faces": {
        "north": { "uv": [11, 1, 11.5, 1.5], "texture": "#0" },
        "east": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "south": { "uv": [11, 3.5, 11.5, 4], "texture": "#0" },
        "west": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "up": { "uv": [11, 1, 11.5, 4], "texture": "#0" },
        "down": { "uv": [11, 1, 11.5, 4], "texture": "#0" }
      }
    },
    {
      "from": [3, 1, 3],
      "to": [13, 15, 13],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 1, 7] },
      "faces": {
        "north": { "uv": [5.5, 0.5, 10.5, 7.5], "texture": "#0" },
        "east": { "uv": [5.5, 0.5, 10.5, 7.5], "texture": "#0" },
        "south": { "uv": [5.5, 0.5, 10.5, 7.5], "texture": "#0" },
        "west": { "uv": [5.5, 0.5, 10.5, 7.5], "texture": "#0" },
        "up": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" },
        "down": { "uv": [11.5, 0.5, 15.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [4, 1, 2],
      "to": [12, 15, 3],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 1, 6] },
      "faces": {
        "north": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "east": { "uv": [10.5, 0.5, 11, 7.5], "texture": "#0" },
        "south": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "west": { "uv": [5, 0.5, 5.5, 7.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 7.5, 10, 8], "texture": "#0" }
      }
    },
    {
      "from": [4, 1, 13],
      "to": [12, 15, 14],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 1, 15] },
      "faces": {
        "north": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "east": { "uv": [10.5, 0.5, 11, 7.5], "texture": "#0" },
        "south": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "west": { "uv": [5, 0.5, 5.5, 7.5], "texture": "#0" },
        "up": { "uv": [6, 0, 10, 0.5], "texture": "#0" },
        "down": { "uv": [6, 7.5, 10, 8], "texture": "#0" }
      }
    },
    {
      "from": [13, 1, 4],
      "to": [14, 15, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [9, 1, 14] },
      "faces": {
        "north": { "uv": [10.5, 0.5, 11, 7.5], "texture": "#0" },
        "east": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "south": { "uv": [5, 0.5, 5.5, 7.5], "texture": "#0" },
        "west": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "up": { "uv": [11.5, 0.5, 12, 4.5], "texture": "#0" },
        "down": { "uv": [15, 0.5, 15.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [2, 1, 4],
      "to": [3, 15, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [0, 1, 14] },
      "faces": {
        "north": { "uv": [5, 0.5, 5.5, 7.5], "texture": "#0" },
        "east": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "south": { "uv": [10.5, 0.5, 11, 7.5], "texture": "#0" },
        "west": { "uv": [6, 0.5, 10, 7.5], "texture": "#0" },
        "up": { "uv": [11.5, 0.5, 12, 4.5], "texture": "#0" },
        "down": { "uv": [15, 0.5, 15.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [4, 15, 4],
      "to": [12, 16, 12],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 15, 7] },
      "faces": {
        "north": { "uv": [0.5, 0.5, 4.5, 1], "texture": "#0" },
        "east": { "uv": [0.5, 4, 4.5, 4.5], "texture": "#0" },
        "south": { "uv": [0.5, 4, 4.5, 4.5], "texture": "#0" },
        "west": { "uv": [0.5, 0.5, 4.5, 1], "texture": "#0" },
        "up": { "uv": [0.5, 0.5, 4.5, 4.5], "texture": "#0" },
        "down": { "uv": [0.5, 0.5, 4.5, 4.5], "texture": "#0" }
      }
    },
    {
      "from": [5, 15, 3],
      "to": [11, 16, 4],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 15, 6] },
      "faces": {
        "north": { "uv": [1, 4.5, 4, 5], "texture": "#0" },
        "east": { "uv": [3.5, 0, 4, 0.5], "texture": "#0" },
        "south": { "uv": [1, 0, 4, 0.5], "texture": "#0" },
        "west": { "uv": [1, 0, 1.5, 0.5], "texture": "#0" },
        "up": { "uv": [1, 0, 4, 0.5], "texture": "#0" },
        "down": { "uv": [1, 4.5, 4, 5], "texture": "#0" }
      }
    },
    {
      "from": [5, 15, 12],
      "to": [11, 16, 13],
      "rotation": { "angle": 0, "axis": "y", "origin": [7, 15, 15] },
      "faces": {
        "north": { "uv": [1, 0, 4, 0.5], "texture": "#0" },
        "east": { "uv": [3.5, 0, 4, 0.5], "texture": "#0" },
        "south": { "uv": [1, 4.5, 4, 5], "texture": "#0" },
        "west": { "uv": [1, 0, 1.5, 0.5], "texture": "#0" },
        "up": { "uv": [1, 0, 4, 0.5], "texture": "#0" },
        "down": { "uv": [1, 4.5, 4, 5], "texture": "#0" }
      }
    },
    {
      "from": [12, 15, 5],
      "to": [13, 16, 11],
      "rotation": { "angle": 0, "axis": "y", "origin": [9, 15, 14] },
      "faces": {
        "north": { "uv": [3.5, 0, 4, 0.5], "texture": "#0" },
        "east": { "uv": [1, 4.5, 4, 5], "texture": "#0" },
        "south": { "uv": [1, 0, 1.5, 0.5], "texture": "#0" },
        "west": { "uv": [1, 0, 4, 0.5], "texture": "#0" },
        "up": { "uv": [0, 1, 0.5, 4], "texture": "#0" },
        "down": { "uv": [4.5, 1, 5, 4], "texture": "#0" }
      }
    },
    {
      "from": [3, 15, 5],
      "to": [4, 16, 11],
      "rotation": { "angle": 0, "axis": "y", "origin": [0, 15, 14] },
      "faces": {
        "north": { "uv": [1, 0, 1.5, 0.5], "texture": "#0" },
        "east": { "uv": [1, 4.5, 4, 5], "texture": "#0" },
        "south": { "uv": [3.5, 0, 4, 0.5], "texture": "#0" },
        "west": { "uv": [1, 0, 4, 0.5], "texture": "#0" },
        "up": { "uv": [4.5, 1, 5, 4], "texture": "#0" },
        "down": { "uv": [0, 1, 0.5, 4], "texture": "#0" }
      }
    }
  ]
}```

### examples/modid/models/item/

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/big_oak_glass_flask"
  }
}
````

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/iron_keg"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/medium_oak_glass_flask"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/oak_iron_barrel"
  }
}
```

```json
{
  "parent": "item/generated",
  "textures": {
    "layer0": "modid:item/small_oak_glass_flask"
  }
}
```

### examples/modid/lang/en_us.json

```json
{
  "itemGroup.modid.barrels": "Barrels",
  "itemGroup.modid.kegs": "Kegs",
  "itemGroup.modid.smallflasks": "Small Flasks",
  "itemGroup.modid.mediumflasks": "Medium Flasks",
  "itemGroup.modid.bigflasks": "Big Flasks",

  "block.modid.oak_iron_barrel": "Oak Iron Barrel",
  "block.modid.iron_keg": "Iron Keg",

  "item.modid.oak_iron_barrel": "Oak Iron Barrel",
  "item.modid.iron_keg": "Iron Keg",
  "item.modid.small_oak_glass_flask": "Small Oak Glass Flask",
  "item.modid.medium_oak_glass_flask": "Medium Oak Glass Flask",
  "item.modid.big_oak_glass_flask": "Big Oak Glass Flask"
}
```

## Project Structure

```
batch_texture_generator
├─ examples                                   # Example files demonstrating input and output structure
│  └─ modid
│     ├─ blockstates                          # Blockstate JSON files
│     ├─ items                                # Item JSON files
│     ├─ lang                                 # Language files
│     ├─ models                               # Model JSON files
│     │  ├─ block                             # Block model JSON files
│     │  └─ item                              # Item model JSON files
│     └─ textures                             # Texture image files
│        ├─ block                             # Block texture image files
│        └─ item                              # Item texture image files
├─ input                                      # Input textures for processing
│  ├─ block                                   # Block input textures
│  └─ item                                    # Item input textures
├─ output                                     # Output files generated after processing
│  └─ modid
│     ├─ blockstates                          # Blockstate JSON files
│     ├─ items                                # Item JSON files
│     ├─ lang                                 # Language files
│     ├─ models                               # Model JSON files
│     │  ├─ block                             # Block model JSON files
│     │  └─ item                              # Item model JSON files
│     └─ textures                             # Texture image files
│        ├─ block                             # Block texture image files
│        └─ item                              # Item texture image files
├─ palettes                                   # Color palettes for texture variations
│  ├─ glass                                   # Glass texture palettes
│  ├─ metal                                   # Metal texture palettes
│  └─ wood                                    # Wood texture palettes
├─ README.md                                 # Project documentation and overview
├─ requirements.txt                          # Python dependencies
├─ schemas                                   # JSON schema definitions
│  ├─ common.schema.json                     # Common schema definitions
│  └─ texture-palettes.schema.json           # Texture palettes schema definition
├─ templates                                 # Model templates for blocks and items
│  ├─ block                                  # Block model templates
│  └─ item                                   # Item model templates
├─ textures                                  # Texture image files for palette generation
│  ├─ glass                                  # Glass texture image files
│  ├─ metal                                   # Metal texture image files
│  └─ wood                                    # Wood texture image files
└─ tools
   ├─ btg.py                                  # Main script for batch texture generation
   └─ btg_gui.py                              # GUI script for batch texture generation

```

```
batch_texture_generator
├─ .btg_gui.json
├─ BLOCK-ASSETS.md
├─ examples
│  └─ modid
│     ├─ blockstates
│     │  ├─ iron_keg_block.json
│     │  └─ oak_iron_barrel_block.json
│     ├─ items
│     │  ├─ big_oak_glass_flask.json
│     │  ├─ iron_keg.json
│     │  ├─ medium_oak_glass_flask.json
│     │  ├─ oak_iron_barrel.json
│     │  └─ small_oak_glass_flask.json
│     ├─ lang
│     │  └─ en_us.json
│     ├─ models
│     │  ├─ block
│     │  │  ├─ iron_keg_block.json
│     │  │  └─ oak_iron_barrel_block.json
│     │  └─ item
│     │     ├─ big_oak_glass_flask.json
│     │     ├─ iron_keg.json
│     │     ├─ medium_oak_glass_flask.json
│     │     ├─ oak_iron_barrel.json
│     │     └─ small_oak_glass_flask.json
│     └─ textures
│        ├─ block
│        │  ├─ iron_keg_block.png
│        │  └─ oak_iron_barrel_block.png
│        └─ item
│           ├─ big_oak_glass_flask.png
│           ├─ iron_keg.png
│           ├─ medium_oak_glass_flask.png
│           ├─ oak_iron_barrel.png
│           └─ small_oak_glass_flask.png
├─ output
│  └─ modid
│     ├─ blockstates
│     │  ├─ iron_keg_block.json
│     │  └─ oak_iron_barrel_block.json
│     ├─ items
│     │  ├─ acacia_copper_barrel.json
│     │  ├─ acacia_copper_barrel_block.json
│     │  ├─ acacia_copper_exposed_barrel.json
│     │  ├─ acacia_copper_exposed_barrel_block.json
│     │  ├─ acacia_copper_oxidized_barrel.json
│     │  ├─ acacia_copper_oxidized_barrel_block.json
│     │  ├─ acacia_copper_weathered_barrel.json
│     │  ├─ acacia_copper_weathered_barrel_block.json
│     │  ├─ acacia_gold_barrel.json
│     │  ├─ acacia_gold_barrel_block.json
│     │  ├─ acacia_iron_barrel.json
│     │  ├─ acacia_iron_barrel_block.json
│     │  ├─ acacia_netherite_barrel.json
│     │  ├─ acacia_netherite_barrel_block.json
│     │  ├─ bamboo_copper_barrel.json
│     │  ├─ bamboo_copper_barrel_block.json
│     │  ├─ bamboo_copper_exposed_barrel.json
│     │  ├─ bamboo_copper_exposed_barrel_block.json
│     │  ├─ bamboo_copper_oxidized_barrel.json
│     │  ├─ bamboo_copper_oxidized_barrel_block.json
│     │  ├─ bamboo_copper_weathered_barrel.json
│     │  ├─ bamboo_copper_weathered_barrel_block.json
│     │  ├─ bamboo_gold_barrel.json
│     │  ├─ bamboo_gold_barrel_block.json
│     │  ├─ bamboo_iron_barrel.json
│     │  ├─ bamboo_iron_barrel_block.json
│     │  ├─ bamboo_netherite_barrel.json
│     │  ├─ bamboo_netherite_barrel_block.json
│     │  ├─ big_acacia_black_stained_glass_flask.json
│     │  ├─ big_acacia_blue_stained_glass_flask.json
│     │  ├─ big_acacia_brown_stained_glass_flask.json
│     │  ├─ big_acacia_cyan_stained_glass_flask.json
│     │  ├─ big_acacia_glass_flask.json
│     │  ├─ big_acacia_gray_stained_glass_flask.json
│     │  ├─ big_acacia_green_stained_glass_flask.json
│     │  ├─ big_acacia_light_blue_stained_glass_flask.json
│     │  ├─ big_acacia_light_gray_stained_glass_flask.json
│     │  ├─ big_acacia_lime_stained_glass_flask.json
│     │  ├─ big_acacia_magenta_stained_glass_flask.json
│     │  ├─ big_acacia_orange_stained_glass_flask.json
│     │  ├─ big_acacia_pink_stained_glass_flask.json
│     │  ├─ big_acacia_purple_stained_glass_flask.json
│     │  ├─ big_acacia_red_stained_glass_flask.json
│     │  ├─ big_acacia_tinted_glass_flask.json
│     │  ├─ big_acacia_white_stained_glass_flask.json
│     │  ├─ big_acacia_yellow_stained_glass_flask.json
│     │  ├─ big_bamboo_black_stained_glass_flask.json
│     │  ├─ big_bamboo_blue_stained_glass_flask.json
│     │  ├─ big_bamboo_brown_stained_glass_flask.json
│     │  ├─ big_bamboo_cyan_stained_glass_flask.json
│     │  ├─ big_bamboo_glass_flask.json
│     │  ├─ big_bamboo_gray_stained_glass_flask.json
│     │  ├─ big_bamboo_green_stained_glass_flask.json
│     │  ├─ big_bamboo_light_blue_stained_glass_flask.json
│     │  ├─ big_bamboo_light_gray_stained_glass_flask.json
│     │  ├─ big_bamboo_lime_stained_glass_flask.json
│     │  ├─ big_bamboo_magenta_stained_glass_flask.json
│     │  ├─ big_bamboo_orange_stained_glass_flask.json
│     │  ├─ big_bamboo_pink_stained_glass_flask.json
│     │  ├─ big_bamboo_purple_stained_glass_flask.json
│     │  ├─ big_bamboo_red_stained_glass_flask.json
│     │  ├─ big_bamboo_tinted_glass_flask.json
│     │  ├─ big_bamboo_white_stained_glass_flask.json
│     │  ├─ big_bamboo_yellow_stained_glass_flask.json
│     │  ├─ big_birch_black_stained_glass_flask.json
│     │  ├─ big_birch_blue_stained_glass_flask.json
│     │  ├─ big_birch_brown_stained_glass_flask.json
│     │  ├─ big_birch_cyan_stained_glass_flask.json
│     │  ├─ big_birch_glass_flask.json
│     │  ├─ big_birch_gray_stained_glass_flask.json
│     │  ├─ big_birch_green_stained_glass_flask.json
│     │  ├─ big_birch_light_blue_stained_glass_flask.json
│     │  ├─ big_birch_light_gray_stained_glass_flask.json
│     │  ├─ big_birch_lime_stained_glass_flask.json
│     │  ├─ big_birch_magenta_stained_glass_flask.json
│     │  ├─ big_birch_orange_stained_glass_flask.json
│     │  ├─ big_birch_pink_stained_glass_flask.json
│     │  ├─ big_birch_purple_stained_glass_flask.json
│     │  ├─ big_birch_red_stained_glass_flask.json
│     │  ├─ big_birch_tinted_glass_flask.json
│     │  ├─ big_birch_white_stained_glass_flask.json
│     │  ├─ big_birch_yellow_stained_glass_flask.json
│     │  ├─ big_cherry_black_stained_glass_flask.json
│     │  ├─ big_cherry_blue_stained_glass_flask.json
│     │  ├─ big_cherry_brown_stained_glass_flask.json
│     │  ├─ big_cherry_cyan_stained_glass_flask.json
│     │  ├─ big_cherry_glass_flask.json
│     │  ├─ big_cherry_gray_stained_glass_flask.json
│     │  ├─ big_cherry_green_stained_glass_flask.json
│     │  ├─ big_cherry_light_blue_stained_glass_flask.json
│     │  ├─ big_cherry_light_gray_stained_glass_flask.json
│     │  ├─ big_cherry_lime_stained_glass_flask.json
│     │  ├─ big_cherry_magenta_stained_glass_flask.json
│     │  ├─ big_cherry_orange_stained_glass_flask.json
│     │  ├─ big_cherry_pink_stained_glass_flask.json
│     │  ├─ big_cherry_purple_stained_glass_flask.json
│     │  ├─ big_cherry_red_stained_glass_flask.json
│     │  ├─ big_cherry_tinted_glass_flask.json
│     │  ├─ big_cherry_white_stained_glass_flask.json
│     │  ├─ big_cherry_yellow_stained_glass_flask.json
│     │  ├─ big_crimson_black_stained_glass_flask.json
│     │  ├─ big_crimson_blue_stained_glass_flask.json
│     │  ├─ big_crimson_brown_stained_glass_flask.json
│     │  ├─ big_crimson_cyan_stained_glass_flask.json
│     │  ├─ big_crimson_glass_flask.json
│     │  ├─ big_crimson_gray_stained_glass_flask.json
│     │  ├─ big_crimson_green_stained_glass_flask.json
│     │  ├─ big_crimson_light_blue_stained_glass_flask.json
│     │  ├─ big_crimson_light_gray_stained_glass_flask.json
│     │  ├─ big_crimson_lime_stained_glass_flask.json
│     │  ├─ big_crimson_magenta_stained_glass_flask.json
│     │  ├─ big_crimson_orange_stained_glass_flask.json
│     │  ├─ big_crimson_pink_stained_glass_flask.json
│     │  ├─ big_crimson_purple_stained_glass_flask.json
│     │  ├─ big_crimson_red_stained_glass_flask.json
│     │  ├─ big_crimson_tinted_glass_flask.json
│     │  ├─ big_crimson_white_stained_glass_flask.json
│     │  ├─ big_crimson_yellow_stained_glass_flask.json
│     │  ├─ big_dark_oak_black_stained_glass_flask.json
│     │  ├─ big_dark_oak_blue_stained_glass_flask.json
│     │  ├─ big_dark_oak_brown_stained_glass_flask.json
│     │  ├─ big_dark_oak_cyan_stained_glass_flask.json
│     │  ├─ big_dark_oak_glass_flask.json
│     │  ├─ big_dark_oak_gray_stained_glass_flask.json
│     │  ├─ big_dark_oak_green_stained_glass_flask.json
│     │  ├─ big_dark_oak_light_blue_stained_glass_flask.json
│     │  ├─ big_dark_oak_light_gray_stained_glass_flask.json
│     │  ├─ big_dark_oak_lime_stained_glass_flask.json
│     │  ├─ big_dark_oak_magenta_stained_glass_flask.json
│     │  ├─ big_dark_oak_orange_stained_glass_flask.json
│     │  ├─ big_dark_oak_pink_stained_glass_flask.json
│     │  ├─ big_dark_oak_purple_stained_glass_flask.json
│     │  ├─ big_dark_oak_red_stained_glass_flask.json
│     │  ├─ big_dark_oak_tinted_glass_flask.json
│     │  ├─ big_dark_oak_white_stained_glass_flask.json
│     │  ├─ big_dark_oak_yellow_stained_glass_flask.json
│     │  ├─ big_jungle_black_stained_glass_flask.json
│     │  ├─ big_jungle_blue_stained_glass_flask.json
│     │  ├─ big_jungle_brown_stained_glass_flask.json
│     │  ├─ big_jungle_cyan_stained_glass_flask.json
│     │  ├─ big_jungle_glass_flask.json
│     │  ├─ big_jungle_gray_stained_glass_flask.json
│     │  ├─ big_jungle_green_stained_glass_flask.json
│     │  ├─ big_jungle_light_blue_stained_glass_flask.json
│     │  ├─ big_jungle_light_gray_stained_glass_flask.json
│     │  ├─ big_jungle_lime_stained_glass_flask.json
│     │  ├─ big_jungle_magenta_stained_glass_flask.json
│     │  ├─ big_jungle_orange_stained_glass_flask.json
│     │  ├─ big_jungle_pink_stained_glass_flask.json
│     │  ├─ big_jungle_purple_stained_glass_flask.json
│     │  ├─ big_jungle_red_stained_glass_flask.json
│     │  ├─ big_jungle_tinted_glass_flask.json
│     │  ├─ big_jungle_white_stained_glass_flask.json
│     │  ├─ big_jungle_yellow_stained_glass_flask.json
│     │  ├─ big_mangrove_black_stained_glass_flask.json
│     │  ├─ big_mangrove_blue_stained_glass_flask.json
│     │  ├─ big_mangrove_brown_stained_glass_flask.json
│     │  ├─ big_mangrove_cyan_stained_glass_flask.json
│     │  ├─ big_mangrove_glass_flask.json
│     │  ├─ big_mangrove_gray_stained_glass_flask.json
│     │  ├─ big_mangrove_green_stained_glass_flask.json
│     │  ├─ big_mangrove_light_blue_stained_glass_flask.json
│     │  ├─ big_mangrove_light_gray_stained_glass_flask.json
│     │  ├─ big_mangrove_lime_stained_glass_flask.json
│     │  ├─ big_mangrove_magenta_stained_glass_flask.json
│     │  ├─ big_mangrove_orange_stained_glass_flask.json
│     │  ├─ big_mangrove_pink_stained_glass_flask.json
│     │  ├─ big_mangrove_purple_stained_glass_flask.json
│     │  ├─ big_mangrove_red_stained_glass_flask.json
│     │  ├─ big_mangrove_tinted_glass_flask.json
│     │  ├─ big_mangrove_white_stained_glass_flask.json
│     │  ├─ big_mangrove_yellow_stained_glass_flask.json
│     │  ├─ big_oak_black_stained_glass_flask.json
│     │  ├─ big_oak_blue_stained_glass_flask.json
│     │  ├─ big_oak_brown_stained_glass_flask.json
│     │  ├─ big_oak_cyan_stained_glass_flask.json
│     │  ├─ big_oak_glass_flask.json
│     │  ├─ big_oak_gray_stained_glass_flask.json
│     │  ├─ big_oak_green_stained_glass_flask.json
│     │  ├─ big_oak_light_blue_stained_glass_flask.json
│     │  ├─ big_oak_light_gray_stained_glass_flask.json
│     │  ├─ big_oak_lime_stained_glass_flask.json
│     │  ├─ big_oak_magenta_stained_glass_flask.json
│     │  ├─ big_oak_orange_stained_glass_flask.json
│     │  ├─ big_oak_pink_stained_glass_flask.json
│     │  ├─ big_oak_purple_stained_glass_flask.json
│     │  ├─ big_oak_red_stained_glass_flask.json
│     │  ├─ big_oak_tinted_glass_flask.json
│     │  ├─ big_oak_white_stained_glass_flask.json
│     │  ├─ big_oak_yellow_stained_glass_flask.json
│     │  ├─ big_pale_oak_black_stained_glass_flask.json
│     │  ├─ big_pale_oak_blue_stained_glass_flask.json
│     │  ├─ big_pale_oak_brown_stained_glass_flask.json
│     │  ├─ big_pale_oak_cyan_stained_glass_flask.json
│     │  ├─ big_pale_oak_glass_flask.json
│     │  ├─ big_pale_oak_gray_stained_glass_flask.json
│     │  ├─ big_pale_oak_green_stained_glass_flask.json
│     │  ├─ big_pale_oak_light_blue_stained_glass_flask.json
│     │  ├─ big_pale_oak_light_gray_stained_glass_flask.json
│     │  ├─ big_pale_oak_lime_stained_glass_flask.json
│     │  ├─ big_pale_oak_magenta_stained_glass_flask.json
│     │  ├─ big_pale_oak_orange_stained_glass_flask.json
│     │  ├─ big_pale_oak_pink_stained_glass_flask.json
│     │  ├─ big_pale_oak_purple_stained_glass_flask.json
│     │  ├─ big_pale_oak_red_stained_glass_flask.json
│     │  ├─ big_pale_oak_tinted_glass_flask.json
│     │  ├─ big_pale_oak_white_stained_glass_flask.json
│     │  ├─ big_pale_oak_yellow_stained_glass_flask.json
│     │  ├─ big_spruce_black_stained_glass_flask.json
│     │  ├─ big_spruce_blue_stained_glass_flask.json
│     │  ├─ big_spruce_brown_stained_glass_flask.json
│     │  ├─ big_spruce_cyan_stained_glass_flask.json
│     │  ├─ big_spruce_glass_flask.json
│     │  ├─ big_spruce_gray_stained_glass_flask.json
│     │  ├─ big_spruce_green_stained_glass_flask.json
│     │  ├─ big_spruce_light_blue_stained_glass_flask.json
│     │  ├─ big_spruce_light_gray_stained_glass_flask.json
│     │  ├─ big_spruce_lime_stained_glass_flask.json
│     │  ├─ big_spruce_magenta_stained_glass_flask.json
│     │  ├─ big_spruce_orange_stained_glass_flask.json
│     │  ├─ big_spruce_pink_stained_glass_flask.json
│     │  ├─ big_spruce_purple_stained_glass_flask.json
│     │  ├─ big_spruce_red_stained_glass_flask.json
│     │  ├─ big_spruce_tinted_glass_flask.json
│     │  ├─ big_spruce_white_stained_glass_flask.json
│     │  ├─ big_spruce_yellow_stained_glass_flask.json
│     │  ├─ big_warped_black_stained_glass_flask.json
│     │  ├─ big_warped_blue_stained_glass_flask.json
│     │  ├─ big_warped_brown_stained_glass_flask.json
│     │  ├─ big_warped_cyan_stained_glass_flask.json
│     │  ├─ big_warped_glass_flask.json
│     │  ├─ big_warped_gray_stained_glass_flask.json
│     │  ├─ big_warped_green_stained_glass_flask.json
│     │  ├─ big_warped_light_blue_stained_glass_flask.json
│     │  ├─ big_warped_light_gray_stained_glass_flask.json
│     │  ├─ big_warped_lime_stained_glass_flask.json
│     │  ├─ big_warped_magenta_stained_glass_flask.json
│     │  ├─ big_warped_orange_stained_glass_flask.json
│     │  ├─ big_warped_pink_stained_glass_flask.json
│     │  ├─ big_warped_purple_stained_glass_flask.json
│     │  ├─ big_warped_red_stained_glass_flask.json
│     │  ├─ big_warped_tinted_glass_flask.json
│     │  ├─ big_warped_white_stained_glass_flask.json
│     │  ├─ big_warped_yellow_stained_glass_flask.json
│     │  ├─ birch_copper_barrel.json
│     │  ├─ birch_copper_barrel_block.json
│     │  ├─ birch_copper_exposed_barrel.json
│     │  ├─ birch_copper_exposed_barrel_block.json
│     │  ├─ birch_copper_oxidized_barrel.json
│     │  ├─ birch_copper_oxidized_barrel_block.json
│     │  ├─ birch_copper_weathered_barrel.json
│     │  ├─ birch_copper_weathered_barrel_block.json
│     │  ├─ birch_gold_barrel.json
│     │  ├─ birch_gold_barrel_block.json
│     │  ├─ birch_iron_barrel.json
│     │  ├─ birch_iron_barrel_block.json
│     │  ├─ birch_netherite_barrel.json
│     │  ├─ birch_netherite_barrel_block.json
│     │  ├─ cherry_copper_barrel.json
│     │  ├─ cherry_copper_barrel_block.json
│     │  ├─ cherry_copper_exposed_barrel.json
│     │  ├─ cherry_copper_exposed_barrel_block.json
│     │  ├─ cherry_copper_oxidized_barrel.json
│     │  ├─ cherry_copper_oxidized_barrel_block.json
│     │  ├─ cherry_copper_weathered_barrel.json
│     │  ├─ cherry_copper_weathered_barrel_block.json
│     │  ├─ cherry_gold_barrel.json
│     │  ├─ cherry_gold_barrel_block.json
│     │  ├─ cherry_iron_barrel.json
│     │  ├─ cherry_iron_barrel_block.json
│     │  ├─ cherry_netherite_barrel.json
│     │  ├─ cherry_netherite_barrel_block.json
│     │  ├─ copper_exposed_keg.json
│     │  ├─ copper_exposed_keg_block.json
│     │  ├─ copper_keg.json
│     │  ├─ copper_keg_block.json
│     │  ├─ copper_oxidized_keg.json
│     │  ├─ copper_oxidized_keg_block.json
│     │  ├─ copper_weathered_keg.json
│     │  ├─ copper_weathered_keg_block.json
│     │  ├─ crimson_copper_barrel.json
│     │  ├─ crimson_copper_barrel_block.json
│     │  ├─ crimson_copper_exposed_barrel.json
│     │  ├─ crimson_copper_exposed_barrel_block.json
│     │  ├─ crimson_copper_oxidized_barrel.json
│     │  ├─ crimson_copper_oxidized_barrel_block.json
│     │  ├─ crimson_copper_weathered_barrel.json
│     │  ├─ crimson_copper_weathered_barrel_block.json
│     │  ├─ crimson_gold_barrel.json
│     │  ├─ crimson_gold_barrel_block.json
│     │  ├─ crimson_iron_barrel.json
│     │  ├─ crimson_iron_barrel_block.json
│     │  ├─ crimson_netherite_barrel.json
│     │  ├─ crimson_netherite_barrel_block.json
│     │  ├─ dark_oak_copper_barrel.json
│     │  ├─ dark_oak_copper_barrel_block.json
│     │  ├─ dark_oak_copper_exposed_barrel.json
│     │  ├─ dark_oak_copper_exposed_barrel_block.json
│     │  ├─ dark_oak_copper_oxidized_barrel.json
│     │  ├─ dark_oak_copper_oxidized_barrel_block.json
│     │  ├─ dark_oak_copper_weathered_barrel.json
│     │  ├─ dark_oak_copper_weathered_barrel_block.json
│     │  ├─ dark_oak_gold_barrel.json
│     │  ├─ dark_oak_gold_barrel_block.json
│     │  ├─ dark_oak_iron_barrel.json
│     │  ├─ dark_oak_iron_barrel_block.json
│     │  ├─ dark_oak_netherite_barrel.json
│     │  ├─ dark_oak_netherite_barrel_block.json
│     │  ├─ gold_keg.json
│     │  ├─ gold_keg_block.json
│     │  ├─ iron_keg.json
│     │  ├─ iron_keg_block.json
│     │  ├─ jungle_copper_barrel.json
│     │  ├─ jungle_copper_barrel_block.json
│     │  ├─ jungle_copper_exposed_barrel.json
│     │  ├─ jungle_copper_exposed_barrel_block.json
│     │  ├─ jungle_copper_oxidized_barrel.json
│     │  ├─ jungle_copper_oxidized_barrel_block.json
│     │  ├─ jungle_copper_weathered_barrel.json
│     │  ├─ jungle_copper_weathered_barrel_block.json
│     │  ├─ jungle_gold_barrel.json
│     │  ├─ jungle_gold_barrel_block.json
│     │  ├─ jungle_iron_barrel.json
│     │  ├─ jungle_iron_barrel_block.json
│     │  ├─ jungle_netherite_barrel.json
│     │  ├─ jungle_netherite_barrel_block.json
│     │  ├─ mangrove_copper_barrel.json
│     │  ├─ mangrove_copper_barrel_block.json
│     │  ├─ mangrove_copper_exposed_barrel.json
│     │  ├─ mangrove_copper_exposed_barrel_block.json
│     │  ├─ mangrove_copper_oxidized_barrel.json
│     │  ├─ mangrove_copper_oxidized_barrel_block.json
│     │  ├─ mangrove_copper_weathered_barrel.json
│     │  ├─ mangrove_copper_weathered_barrel_block.json
│     │  ├─ mangrove_gold_barrel.json
│     │  ├─ mangrove_gold_barrel_block.json
│     │  ├─ mangrove_iron_barrel.json
│     │  ├─ mangrove_iron_barrel_block.json
│     │  ├─ mangrove_netherite_barrel.json
│     │  ├─ mangrove_netherite_barrel_block.json
│     │  ├─ medium_acacia_black_stained_glass_flask.json
│     │  ├─ medium_acacia_blue_stained_glass_flask.json
│     │  ├─ medium_acacia_brown_stained_glass_flask.json
│     │  ├─ medium_acacia_cyan_stained_glass_flask.json
│     │  ├─ medium_acacia_glass_flask.json
│     │  ├─ medium_acacia_gray_stained_glass_flask.json
│     │  ├─ medium_acacia_green_stained_glass_flask.json
│     │  ├─ medium_acacia_light_blue_stained_glass_flask.json
│     │  ├─ medium_acacia_light_gray_stained_glass_flask.json
│     │  ├─ medium_acacia_lime_stained_glass_flask.json
│     │  ├─ medium_acacia_magenta_stained_glass_flask.json
│     │  ├─ medium_acacia_orange_stained_glass_flask.json
│     │  ├─ medium_acacia_pink_stained_glass_flask.json
│     │  ├─ medium_acacia_purple_stained_glass_flask.json
│     │  ├─ medium_acacia_red_stained_glass_flask.json
│     │  ├─ medium_acacia_tinted_glass_flask.json
│     │  ├─ medium_acacia_white_stained_glass_flask.json
│     │  ├─ medium_acacia_yellow_stained_glass_flask.json
│     │  ├─ medium_bamboo_black_stained_glass_flask.json
│     │  ├─ medium_bamboo_blue_stained_glass_flask.json
│     │  ├─ medium_bamboo_brown_stained_glass_flask.json
│     │  ├─ medium_bamboo_cyan_stained_glass_flask.json
│     │  ├─ medium_bamboo_glass_flask.json
│     │  ├─ medium_bamboo_gray_stained_glass_flask.json
│     │  ├─ medium_bamboo_green_stained_glass_flask.json
│     │  ├─ medium_bamboo_light_blue_stained_glass_flask.json
│     │  ├─ medium_bamboo_light_gray_stained_glass_flask.json
│     │  ├─ medium_bamboo_lime_stained_glass_flask.json
│     │  ├─ medium_bamboo_magenta_stained_glass_flask.json
│     │  ├─ medium_bamboo_orange_stained_glass_flask.json
│     │  ├─ medium_bamboo_pink_stained_glass_flask.json
│     │  ├─ medium_bamboo_purple_stained_glass_flask.json
│     │  ├─ medium_bamboo_red_stained_glass_flask.json
│     │  ├─ medium_bamboo_tinted_glass_flask.json
│     │  ├─ medium_bamboo_white_stained_glass_flask.json
│     │  ├─ medium_bamboo_yellow_stained_glass_flask.json
│     │  ├─ medium_birch_black_stained_glass_flask.json
│     │  ├─ medium_birch_blue_stained_glass_flask.json
│     │  ├─ medium_birch_brown_stained_glass_flask.json
│     │  ├─ medium_birch_cyan_stained_glass_flask.json
│     │  ├─ medium_birch_glass_flask.json
│     │  ├─ medium_birch_gray_stained_glass_flask.json
│     │  ├─ medium_birch_green_stained_glass_flask.json
│     │  ├─ medium_birch_light_blue_stained_glass_flask.json
│     │  ├─ medium_birch_light_gray_stained_glass_flask.json
│     │  ├─ medium_birch_lime_stained_glass_flask.json
│     │  ├─ medium_birch_magenta_stained_glass_flask.json
│     │  ├─ medium_birch_orange_stained_glass_flask.json
│     │  ├─ medium_birch_pink_stained_glass_flask.json
│     │  ├─ medium_birch_purple_stained_glass_flask.json
│     │  ├─ medium_birch_red_stained_glass_flask.json
│     │  ├─ medium_birch_tinted_glass_flask.json
│     │  ├─ medium_birch_white_stained_glass_flask.json
│     │  ├─ medium_birch_yellow_stained_glass_flask.json
│     │  ├─ medium_cherry_black_stained_glass_flask.json
│     │  ├─ medium_cherry_blue_stained_glass_flask.json
│     │  ├─ medium_cherry_brown_stained_glass_flask.json
│     │  ├─ medium_cherry_cyan_stained_glass_flask.json
│     │  ├─ medium_cherry_glass_flask.json
│     │  ├─ medium_cherry_gray_stained_glass_flask.json
│     │  ├─ medium_cherry_green_stained_glass_flask.json
│     │  ├─ medium_cherry_light_blue_stained_glass_flask.json
│     │  ├─ medium_cherry_light_gray_stained_glass_flask.json
│     │  ├─ medium_cherry_lime_stained_glass_flask.json
│     │  ├─ medium_cherry_magenta_stained_glass_flask.json
│     │  ├─ medium_cherry_orange_stained_glass_flask.json
│     │  ├─ medium_cherry_pink_stained_glass_flask.json
│     │  ├─ medium_cherry_purple_stained_glass_flask.json
│     │  ├─ medium_cherry_red_stained_glass_flask.json
│     │  ├─ medium_cherry_tinted_glass_flask.json
│     │  ├─ medium_cherry_white_stained_glass_flask.json
│     │  ├─ medium_cherry_yellow_stained_glass_flask.json
│     │  ├─ medium_crimson_black_stained_glass_flask.json
│     │  ├─ medium_crimson_blue_stained_glass_flask.json
│     │  ├─ medium_crimson_brown_stained_glass_flask.json
│     │  ├─ medium_crimson_cyan_stained_glass_flask.json
│     │  ├─ medium_crimson_glass_flask.json
│     │  ├─ medium_crimson_gray_stained_glass_flask.json
│     │  ├─ medium_crimson_green_stained_glass_flask.json
│     │  ├─ medium_crimson_light_blue_stained_glass_flask.json
│     │  ├─ medium_crimson_light_gray_stained_glass_flask.json
│     │  ├─ medium_crimson_lime_stained_glass_flask.json
│     │  ├─ medium_crimson_magenta_stained_glass_flask.json
│     │  ├─ medium_crimson_orange_stained_glass_flask.json
│     │  ├─ medium_crimson_pink_stained_glass_flask.json
│     │  ├─ medium_crimson_purple_stained_glass_flask.json
│     │  ├─ medium_crimson_red_stained_glass_flask.json
│     │  ├─ medium_crimson_tinted_glass_flask.json
│     │  ├─ medium_crimson_white_stained_glass_flask.json
│     │  ├─ medium_crimson_yellow_stained_glass_flask.json
│     │  ├─ medium_dark_oak_black_stained_glass_flask.json
│     │  ├─ medium_dark_oak_blue_stained_glass_flask.json
│     │  ├─ medium_dark_oak_brown_stained_glass_flask.json
│     │  ├─ medium_dark_oak_cyan_stained_glass_flask.json
│     │  ├─ medium_dark_oak_glass_flask.json
│     │  ├─ medium_dark_oak_gray_stained_glass_flask.json
│     │  ├─ medium_dark_oak_green_stained_glass_flask.json
│     │  ├─ medium_dark_oak_light_blue_stained_glass_flask.json
│     │  ├─ medium_dark_oak_light_gray_stained_glass_flask.json
│     │  ├─ medium_dark_oak_lime_stained_glass_flask.json
│     │  ├─ medium_dark_oak_magenta_stained_glass_flask.json
│     │  ├─ medium_dark_oak_orange_stained_glass_flask.json
│     │  ├─ medium_dark_oak_pink_stained_glass_flask.json
│     │  ├─ medium_dark_oak_purple_stained_glass_flask.json
│     │  ├─ medium_dark_oak_red_stained_glass_flask.json
│     │  ├─ medium_dark_oak_tinted_glass_flask.json
│     │  ├─ medium_dark_oak_white_stained_glass_flask.json
│     │  ├─ medium_dark_oak_yellow_stained_glass_flask.json
│     │  ├─ medium_jungle_black_stained_glass_flask.json
│     │  ├─ medium_jungle_blue_stained_glass_flask.json
│     │  ├─ medium_jungle_brown_stained_glass_flask.json
│     │  ├─ medium_jungle_cyan_stained_glass_flask.json
│     │  ├─ medium_jungle_glass_flask.json
│     │  ├─ medium_jungle_gray_stained_glass_flask.json
│     │  ├─ medium_jungle_green_stained_glass_flask.json
│     │  ├─ medium_jungle_light_blue_stained_glass_flask.json
│     │  ├─ medium_jungle_light_gray_stained_glass_flask.json
│     │  ├─ medium_jungle_lime_stained_glass_flask.json
│     │  ├─ medium_jungle_magenta_stained_glass_flask.json
│     │  ├─ medium_jungle_orange_stained_glass_flask.json
│     │  ├─ medium_jungle_pink_stained_glass_flask.json
│     │  ├─ medium_jungle_purple_stained_glass_flask.json
│     │  ├─ medium_jungle_red_stained_glass_flask.json
│     │  ├─ medium_jungle_tinted_glass_flask.json
│     │  ├─ medium_jungle_white_stained_glass_flask.json
│     │  ├─ medium_jungle_yellow_stained_glass_flask.json
│     │  ├─ medium_mangrove_black_stained_glass_flask.json
│     │  ├─ medium_mangrove_blue_stained_glass_flask.json
│     │  ├─ medium_mangrove_brown_stained_glass_flask.json
│     │  ├─ medium_mangrove_cyan_stained_glass_flask.json
│     │  ├─ medium_mangrove_glass_flask.json
│     │  ├─ medium_mangrove_gray_stained_glass_flask.json
│     │  ├─ medium_mangrove_green_stained_glass_flask.json
│     │  ├─ medium_mangrove_light_blue_stained_glass_flask.json
│     │  ├─ medium_mangrove_light_gray_stained_glass_flask.json
│     │  ├─ medium_mangrove_lime_stained_glass_flask.json
│     │  ├─ medium_mangrove_magenta_stained_glass_flask.json
│     │  ├─ medium_mangrove_orange_stained_glass_flask.json
│     │  ├─ medium_mangrove_pink_stained_glass_flask.json
│     │  ├─ medium_mangrove_purple_stained_glass_flask.json
│     │  ├─ medium_mangrove_red_stained_glass_flask.json
│     │  ├─ medium_mangrove_tinted_glass_flask.json
│     │  ├─ medium_mangrove_white_stained_glass_flask.json
│     │  ├─ medium_mangrove_yellow_stained_glass_flask.json
│     │  ├─ medium_oak_black_stained_glass_flask.json
│     │  ├─ medium_oak_blue_stained_glass_flask.json
│     │  ├─ medium_oak_brown_stained_glass_flask.json
│     │  ├─ medium_oak_cyan_stained_glass_flask.json
│     │  ├─ medium_oak_glass_flask.json
│     │  ├─ medium_oak_gray_stained_glass_flask.json
│     │  ├─ medium_oak_green_stained_glass_flask.json
│     │  ├─ medium_oak_light_blue_stained_glass_flask.json
│     │  ├─ medium_oak_light_gray_stained_glass_flask.json
│     │  ├─ medium_oak_lime_stained_glass_flask.json
│     │  ├─ medium_oak_magenta_stained_glass_flask.json
│     │  ├─ medium_oak_orange_stained_glass_flask.json
│     │  ├─ medium_oak_pink_stained_glass_flask.json
│     │  ├─ medium_oak_purple_stained_glass_flask.json
│     │  ├─ medium_oak_red_stained_glass_flask.json
│     │  ├─ medium_oak_tinted_glass_flask.json
│     │  ├─ medium_oak_white_stained_glass_flask.json
│     │  ├─ medium_oak_yellow_stained_glass_flask.json
│     │  ├─ medium_pale_oak_black_stained_glass_flask.json
│     │  ├─ medium_pale_oak_blue_stained_glass_flask.json
│     │  ├─ medium_pale_oak_brown_stained_glass_flask.json
│     │  ├─ medium_pale_oak_cyan_stained_glass_flask.json
│     │  ├─ medium_pale_oak_glass_flask.json
│     │  ├─ medium_pale_oak_gray_stained_glass_flask.json
│     │  ├─ medium_pale_oak_green_stained_glass_flask.json
│     │  ├─ medium_pale_oak_light_blue_stained_glass_flask.json
│     │  ├─ medium_pale_oak_light_gray_stained_glass_flask.json
│     │  ├─ medium_pale_oak_lime_stained_glass_flask.json
│     │  ├─ medium_pale_oak_magenta_stained_glass_flask.json
│     │  ├─ medium_pale_oak_orange_stained_glass_flask.json
│     │  ├─ medium_pale_oak_pink_stained_glass_flask.json
│     │  ├─ medium_pale_oak_purple_stained_glass_flask.json
│     │  ├─ medium_pale_oak_red_stained_glass_flask.json
│     │  ├─ medium_pale_oak_tinted_glass_flask.json
│     │  ├─ medium_pale_oak_white_stained_glass_flask.json
│     │  ├─ medium_pale_oak_yellow_stained_glass_flask.json
│     │  ├─ medium_spruce_black_stained_glass_flask.json
│     │  ├─ medium_spruce_blue_stained_glass_flask.json
│     │  ├─ medium_spruce_brown_stained_glass_flask.json
│     │  ├─ medium_spruce_cyan_stained_glass_flask.json
│     │  ├─ medium_spruce_glass_flask.json
│     │  ├─ medium_spruce_gray_stained_glass_flask.json
│     │  ├─ medium_spruce_green_stained_glass_flask.json
│     │  ├─ medium_spruce_light_blue_stained_glass_flask.json
│     │  ├─ medium_spruce_light_gray_stained_glass_flask.json
│     │  ├─ medium_spruce_lime_stained_glass_flask.json
│     │  ├─ medium_spruce_magenta_stained_glass_flask.json
│     │  ├─ medium_spruce_orange_stained_glass_flask.json
│     │  ├─ medium_spruce_pink_stained_glass_flask.json
│     │  ├─ medium_spruce_purple_stained_glass_flask.json
│     │  ├─ medium_spruce_red_stained_glass_flask.json
│     │  ├─ medium_spruce_tinted_glass_flask.json
│     │  ├─ medium_spruce_white_stained_glass_flask.json
│     │  ├─ medium_spruce_yellow_stained_glass_flask.json
│     │  ├─ medium_warped_black_stained_glass_flask.json
│     │  ├─ medium_warped_blue_stained_glass_flask.json
│     │  ├─ medium_warped_brown_stained_glass_flask.json
│     │  ├─ medium_warped_cyan_stained_glass_flask.json
│     │  ├─ medium_warped_glass_flask.json
│     │  ├─ medium_warped_gray_stained_glass_flask.json
│     │  ├─ medium_warped_green_stained_glass_flask.json
│     │  ├─ medium_warped_light_blue_stained_glass_flask.json
│     │  ├─ medium_warped_light_gray_stained_glass_flask.json
│     │  ├─ medium_warped_lime_stained_glass_flask.json
│     │  ├─ medium_warped_magenta_stained_glass_flask.json
│     │  ├─ medium_warped_orange_stained_glass_flask.json
│     │  ├─ medium_warped_pink_stained_glass_flask.json
│     │  ├─ medium_warped_purple_stained_glass_flask.json
│     │  ├─ medium_warped_red_stained_glass_flask.json
│     │  ├─ medium_warped_tinted_glass_flask.json
│     │  ├─ medium_warped_white_stained_glass_flask.json
│     │  ├─ medium_warped_yellow_stained_glass_flask.json
│     │  ├─ netherite_keg.json
│     │  ├─ netherite_keg_block.json
│     │  ├─ oak_copper_barrel.json
│     │  ├─ oak_copper_barrel_block.json
│     │  ├─ oak_copper_exposed_barrel.json
│     │  ├─ oak_copper_exposed_barrel_block.json
│     │  ├─ oak_copper_oxidized_barrel.json
│     │  ├─ oak_copper_oxidized_barrel_block.json
│     │  ├─ oak_copper_weathered_barrel.json
│     │  ├─ oak_copper_weathered_barrel_block.json
│     │  ├─ oak_gold_barrel.json
│     │  ├─ oak_gold_barrel_block.json
│     │  ├─ oak_iron_barrel.json
│     │  ├─ oak_iron_barrel_block.json
│     │  ├─ oak_netherite_barrel.json
│     │  ├─ oak_netherite_barrel_block.json
│     │  ├─ pale_oak_copper_barrel.json
│     │  ├─ pale_oak_copper_barrel_block.json
│     │  ├─ pale_oak_copper_exposed_barrel.json
│     │  ├─ pale_oak_copper_exposed_barrel_block.json
│     │  ├─ pale_oak_copper_oxidized_barrel.json
│     │  ├─ pale_oak_copper_oxidized_barrel_block.json
│     │  ├─ pale_oak_copper_weathered_barrel.json
│     │  ├─ pale_oak_copper_weathered_barrel_block.json
│     │  ├─ pale_oak_gold_barrel.json
│     │  ├─ pale_oak_gold_barrel_block.json
│     │  ├─ pale_oak_iron_barrel.json
│     │  ├─ pale_oak_iron_barrel_block.json
│     │  ├─ pale_oak_netherite_barrel.json
│     │  ├─ pale_oak_netherite_barrel_block.json
│     │  ├─ small_acacia_black_stained_glass_flask.json
│     │  ├─ small_acacia_blue_stained_glass_flask.json
│     │  ├─ small_acacia_brown_stained_glass_flask.json
│     │  ├─ small_acacia_cyan_stained_glass_flask.json
│     │  ├─ small_acacia_glass_flask.json
│     │  ├─ small_acacia_gray_stained_glass_flask.json
│     │  ├─ small_acacia_green_stained_glass_flask.json
│     │  ├─ small_acacia_light_blue_stained_glass_flask.json
│     │  ├─ small_acacia_light_gray_stained_glass_flask.json
│     │  ├─ small_acacia_lime_stained_glass_flask.json
│     │  ├─ small_acacia_magenta_stained_glass_flask.json
│     │  ├─ small_acacia_orange_stained_glass_flask.json
│     │  ├─ small_acacia_pink_stained_glass_flask.json
│     │  ├─ small_acacia_purple_stained_glass_flask.json
│     │  ├─ small_acacia_red_stained_glass_flask.json
│     │  ├─ small_acacia_tinted_glass_flask.json
│     │  ├─ small_acacia_white_stained_glass_flask.json
│     │  ├─ small_acacia_yellow_stained_glass_flask.json
│     │  ├─ small_bamboo_black_stained_glass_flask.json
│     │  ├─ small_bamboo_blue_stained_glass_flask.json
│     │  ├─ small_bamboo_brown_stained_glass_flask.json
│     │  ├─ small_bamboo_cyan_stained_glass_flask.json
│     │  ├─ small_bamboo_glass_flask.json
│     │  ├─ small_bamboo_gray_stained_glass_flask.json
│     │  ├─ small_bamboo_green_stained_glass_flask.json
│     │  ├─ small_bamboo_light_blue_stained_glass_flask.json
│     │  ├─ small_bamboo_light_gray_stained_glass_flask.json
│     │  ├─ small_bamboo_lime_stained_glass_flask.json
│     │  ├─ small_bamboo_magenta_stained_glass_flask.json
│     │  ├─ small_bamboo_orange_stained_glass_flask.json
│     │  ├─ small_bamboo_pink_stained_glass_flask.json
│     │  ├─ small_bamboo_purple_stained_glass_flask.json
│     │  ├─ small_bamboo_red_stained_glass_flask.json
│     │  ├─ small_bamboo_tinted_glass_flask.json
│     │  ├─ small_bamboo_white_stained_glass_flask.json
│     │  ├─ small_bamboo_yellow_stained_glass_flask.json
│     │  ├─ small_birch_black_stained_glass_flask.json
│     │  ├─ small_birch_blue_stained_glass_flask.json
│     │  ├─ small_birch_brown_stained_glass_flask.json
│     │  ├─ small_birch_cyan_stained_glass_flask.json
│     │  ├─ small_birch_glass_flask.json
│     │  ├─ small_birch_gray_stained_glass_flask.json
│     │  ├─ small_birch_green_stained_glass_flask.json
│     │  ├─ small_birch_light_blue_stained_glass_flask.json
│     │  ├─ small_birch_light_gray_stained_glass_flask.json
│     │  ├─ small_birch_lime_stained_glass_flask.json
│     │  ├─ small_birch_magenta_stained_glass_flask.json
│     │  ├─ small_birch_orange_stained_glass_flask.json
│     │  ├─ small_birch_pink_stained_glass_flask.json
│     │  ├─ small_birch_purple_stained_glass_flask.json
│     │  ├─ small_birch_red_stained_glass_flask.json
│     │  ├─ small_birch_tinted_glass_flask.json
│     │  ├─ small_birch_white_stained_glass_flask.json
│     │  ├─ small_birch_yellow_stained_glass_flask.json
│     │  ├─ small_cherry_black_stained_glass_flask.json
│     │  ├─ small_cherry_blue_stained_glass_flask.json
│     │  ├─ small_cherry_brown_stained_glass_flask.json
│     │  ├─ small_cherry_cyan_stained_glass_flask.json
│     │  ├─ small_cherry_glass_flask.json
│     │  ├─ small_cherry_gray_stained_glass_flask.json
│     │  ├─ small_cherry_green_stained_glass_flask.json
│     │  ├─ small_cherry_light_blue_stained_glass_flask.json
│     │  ├─ small_cherry_light_gray_stained_glass_flask.json
│     │  ├─ small_cherry_lime_stained_glass_flask.json
│     │  ├─ small_cherry_magenta_stained_glass_flask.json
│     │  ├─ small_cherry_orange_stained_glass_flask.json
│     │  ├─ small_cherry_pink_stained_glass_flask.json
│     │  ├─ small_cherry_purple_stained_glass_flask.json
│     │  ├─ small_cherry_red_stained_glass_flask.json
│     │  ├─ small_cherry_tinted_glass_flask.json
│     │  ├─ small_cherry_white_stained_glass_flask.json
│     │  ├─ small_cherry_yellow_stained_glass_flask.json
│     │  ├─ small_crimson_black_stained_glass_flask.json
│     │  ├─ small_crimson_blue_stained_glass_flask.json
│     │  ├─ small_crimson_brown_stained_glass_flask.json
│     │  ├─ small_crimson_cyan_stained_glass_flask.json
│     │  ├─ small_crimson_glass_flask.json
│     │  ├─ small_crimson_gray_stained_glass_flask.json
│     │  ├─ small_crimson_green_stained_glass_flask.json
│     │  ├─ small_crimson_light_blue_stained_glass_flask.json
│     │  ├─ small_crimson_light_gray_stained_glass_flask.json
│     │  ├─ small_crimson_lime_stained_glass_flask.json
│     │  ├─ small_crimson_magenta_stained_glass_flask.json
│     │  ├─ small_crimson_orange_stained_glass_flask.json
│     │  ├─ small_crimson_pink_stained_glass_flask.json
│     │  ├─ small_crimson_purple_stained_glass_flask.json
│     │  ├─ small_crimson_red_stained_glass_flask.json
│     │  ├─ small_crimson_tinted_glass_flask.json
│     │  ├─ small_crimson_white_stained_glass_flask.json
│     │  ├─ small_crimson_yellow_stained_glass_flask.json
│     │  ├─ small_dark_oak_black_stained_glass_flask.json
│     │  ├─ small_dark_oak_blue_stained_glass_flask.json
│     │  ├─ small_dark_oak_brown_stained_glass_flask.json
│     │  ├─ small_dark_oak_cyan_stained_glass_flask.json
│     │  ├─ small_dark_oak_glass_flask.json
│     │  ├─ small_dark_oak_gray_stained_glass_flask.json
│     │  ├─ small_dark_oak_green_stained_glass_flask.json
│     │  ├─ small_dark_oak_light_blue_stained_glass_flask.json
│     │  ├─ small_dark_oak_light_gray_stained_glass_flask.json
│     │  ├─ small_dark_oak_lime_stained_glass_flask.json
│     │  ├─ small_dark_oak_magenta_stained_glass_flask.json
│     │  ├─ small_dark_oak_orange_stained_glass_flask.json
│     │  ├─ small_dark_oak_pink_stained_glass_flask.json
│     │  ├─ small_dark_oak_purple_stained_glass_flask.json
│     │  ├─ small_dark_oak_red_stained_glass_flask.json
│     │  ├─ small_dark_oak_tinted_glass_flask.json
│     │  ├─ small_dark_oak_white_stained_glass_flask.json
│     │  ├─ small_dark_oak_yellow_stained_glass_flask.json
│     │  ├─ small_jungle_black_stained_glass_flask.json
│     │  ├─ small_jungle_blue_stained_glass_flask.json
│     │  ├─ small_jungle_brown_stained_glass_flask.json
│     │  ├─ small_jungle_cyan_stained_glass_flask.json
│     │  ├─ small_jungle_glass_flask.json
│     │  ├─ small_jungle_gray_stained_glass_flask.json
│     │  ├─ small_jungle_green_stained_glass_flask.json
│     │  ├─ small_jungle_light_blue_stained_glass_flask.json
│     │  ├─ small_jungle_light_gray_stained_glass_flask.json
│     │  ├─ small_jungle_lime_stained_glass_flask.json
│     │  ├─ small_jungle_magenta_stained_glass_flask.json
│     │  ├─ small_jungle_orange_stained_glass_flask.json
│     │  ├─ small_jungle_pink_stained_glass_flask.json
│     │  ├─ small_jungle_purple_stained_glass_flask.json
│     │  ├─ small_jungle_red_stained_glass_flask.json
│     │  ├─ small_jungle_tinted_glass_flask.json
│     │  ├─ small_jungle_white_stained_glass_flask.json
│     │  ├─ small_jungle_yellow_stained_glass_flask.json
│     │  ├─ small_mangrove_black_stained_glass_flask.json
│     │  ├─ small_mangrove_blue_stained_glass_flask.json
│     │  ├─ small_mangrove_brown_stained_glass_flask.json
│     │  ├─ small_mangrove_cyan_stained_glass_flask.json
│     │  ├─ small_mangrove_glass_flask.json
│     │  ├─ small_mangrove_gray_stained_glass_flask.json
│     │  ├─ small_mangrove_green_stained_glass_flask.json
│     │  ├─ small_mangrove_light_blue_stained_glass_flask.json
│     │  ├─ small_mangrove_light_gray_stained_glass_flask.json
│     │  ├─ small_mangrove_lime_stained_glass_flask.json
│     │  ├─ small_mangrove_magenta_stained_glass_flask.json
│     │  ├─ small_mangrove_orange_stained_glass_flask.json
│     │  ├─ small_mangrove_pink_stained_glass_flask.json
│     │  ├─ small_mangrove_purple_stained_glass_flask.json
│     │  ├─ small_mangrove_red_stained_glass_flask.json
│     │  ├─ small_mangrove_tinted_glass_flask.json
│     │  ├─ small_mangrove_white_stained_glass_flask.json
│     │  ├─ small_mangrove_yellow_stained_glass_flask.json
│     │  ├─ small_oak_black_stained_glass_flask.json
│     │  ├─ small_oak_blue_stained_glass_flask.json
│     │  ├─ small_oak_brown_stained_glass_flask.json
│     │  ├─ small_oak_cyan_stained_glass_flask.json
│     │  ├─ small_oak_glass_flask.json
│     │  ├─ small_oak_gray_stained_glass_flask.json
│     │  ├─ small_oak_green_stained_glass_flask.json
│     │  ├─ small_oak_light_blue_stained_glass_flask.json
│     │  ├─ small_oak_light_gray_stained_glass_flask.json
│     │  ├─ small_oak_lime_stained_glass_flask.json
│     │  ├─ small_oak_magenta_stained_glass_flask.json
│     │  ├─ small_oak_orange_stained_glass_flask.json
│     │  ├─ small_oak_pink_stained_glass_flask.json
│     │  ├─ small_oak_purple_stained_glass_flask.json
│     │  ├─ small_oak_red_stained_glass_flask.json
│     │  ├─ small_oak_tinted_glass_flask.json
│     │  ├─ small_oak_white_stained_glass_flask.json
│     │  ├─ small_oak_yellow_stained_glass_flask.json
│     │  ├─ small_pale_oak_black_stained_glass_flask.json
│     │  ├─ small_pale_oak_blue_stained_glass_flask.json
│     │  ├─ small_pale_oak_brown_stained_glass_flask.json
│     │  ├─ small_pale_oak_cyan_stained_glass_flask.json
│     │  ├─ small_pale_oak_glass_flask.json
│     │  ├─ small_pale_oak_gray_stained_glass_flask.json
│     │  ├─ small_pale_oak_green_stained_glass_flask.json
│     │  ├─ small_pale_oak_light_blue_stained_glass_flask.json
│     │  ├─ small_pale_oak_light_gray_stained_glass_flask.json
│     │  ├─ small_pale_oak_lime_stained_glass_flask.json
│     │  ├─ small_pale_oak_magenta_stained_glass_flask.json
│     │  ├─ small_pale_oak_orange_stained_glass_flask.json
│     │  ├─ small_pale_oak_pink_stained_glass_flask.json
│     │  ├─ small_pale_oak_purple_stained_glass_flask.json
│     │  ├─ small_pale_oak_red_stained_glass_flask.json
│     │  ├─ small_pale_oak_tinted_glass_flask.json
│     │  ├─ small_pale_oak_white_stained_glass_flask.json
│     │  ├─ small_pale_oak_yellow_stained_glass_flask.json
│     │  ├─ small_spruce_black_stained_glass_flask.json
│     │  ├─ small_spruce_blue_stained_glass_flask.json
│     │  ├─ small_spruce_brown_stained_glass_flask.json
│     │  ├─ small_spruce_cyan_stained_glass_flask.json
│     │  ├─ small_spruce_glass_flask.json
│     │  ├─ small_spruce_gray_stained_glass_flask.json
│     │  ├─ small_spruce_green_stained_glass_flask.json
│     │  ├─ small_spruce_light_blue_stained_glass_flask.json
│     │  ├─ small_spruce_light_gray_stained_glass_flask.json
│     │  ├─ small_spruce_lime_stained_glass_flask.json
│     │  ├─ small_spruce_magenta_stained_glass_flask.json
│     │  ├─ small_spruce_orange_stained_glass_flask.json
│     │  ├─ small_spruce_pink_stained_glass_flask.json
│     │  ├─ small_spruce_purple_stained_glass_flask.json
│     │  ├─ small_spruce_red_stained_glass_flask.json
│     │  ├─ small_spruce_tinted_glass_flask.json
│     │  ├─ small_spruce_white_stained_glass_flask.json
│     │  ├─ small_spruce_yellow_stained_glass_flask.json
│     │  ├─ small_warped_black_stained_glass_flask.json
│     │  ├─ small_warped_blue_stained_glass_flask.json
│     │  ├─ small_warped_brown_stained_glass_flask.json
│     │  ├─ small_warped_cyan_stained_glass_flask.json
│     │  ├─ small_warped_glass_flask.json
│     │  ├─ small_warped_gray_stained_glass_flask.json
│     │  ├─ small_warped_green_stained_glass_flask.json
│     │  ├─ small_warped_light_blue_stained_glass_flask.json
│     │  ├─ small_warped_light_gray_stained_glass_flask.json
│     │  ├─ small_warped_lime_stained_glass_flask.json
│     │  ├─ small_warped_magenta_stained_glass_flask.json
│     │  ├─ small_warped_orange_stained_glass_flask.json
│     │  ├─ small_warped_pink_stained_glass_flask.json
│     │  ├─ small_warped_purple_stained_glass_flask.json
│     │  ├─ small_warped_red_stained_glass_flask.json
│     │  ├─ small_warped_tinted_glass_flask.json
│     │  ├─ small_warped_white_stained_glass_flask.json
│     │  ├─ small_warped_yellow_stained_glass_flask.json
│     │  ├─ spruce_copper_barrel.json
│     │  ├─ spruce_copper_barrel_block.json
│     │  ├─ spruce_copper_exposed_barrel.json
│     │  ├─ spruce_copper_exposed_barrel_block.json
│     │  ├─ spruce_copper_oxidized_barrel.json
│     │  ├─ spruce_copper_oxidized_barrel_block.json
│     │  ├─ spruce_copper_weathered_barrel.json
│     │  ├─ spruce_copper_weathered_barrel_block.json
│     │  ├─ spruce_gold_barrel.json
│     │  ├─ spruce_gold_barrel_block.json
│     │  ├─ spruce_iron_barrel.json
│     │  ├─ spruce_iron_barrel_block.json
│     │  ├─ spruce_netherite_barrel.json
│     │  ├─ spruce_netherite_barrel_block.json
│     │  ├─ warped_copper_barrel.json
│     │  ├─ warped_copper_barrel_block.json
│     │  ├─ warped_copper_exposed_barrel.json
│     │  ├─ warped_copper_exposed_barrel_block.json
│     │  ├─ warped_copper_oxidized_barrel.json
│     │  ├─ warped_copper_oxidized_barrel_block.json
│     │  ├─ warped_copper_weathered_barrel.json
│     │  ├─ warped_copper_weathered_barrel_block.json
│     │  ├─ warped_gold_barrel.json
│     │  ├─ warped_gold_barrel_block.json
│     │  ├─ warped_iron_barrel.json
│     │  ├─ warped_iron_barrel_block.json
│     │  ├─ warped_netherite_barrel.json
│     │  └─ warped_netherite_barrel_block.json
│     ├─ lang
│     │  └─ en_us.json
│     ├─ models
│     │  ├─ block
│     │  │  ├─ iron_keg_block.json
│     │  │  └─ oak_iron_barrel_block.json
│     │  └─ item
│     │     ├─ acacia_copper_barrel.json
│     │     ├─ acacia_copper_exposed_barrel.json
│     │     ├─ acacia_copper_oxidized_barrel.json
│     │     ├─ acacia_copper_weathered_barrel.json
│     │     ├─ acacia_gold_barrel.json
│     │     ├─ acacia_iron_barrel.json
│     │     ├─ acacia_netherite_barrel.json
│     │     ├─ bamboo_copper_barrel.json
│     │     ├─ bamboo_copper_exposed_barrel.json
│     │     ├─ bamboo_copper_oxidized_barrel.json
│     │     ├─ bamboo_copper_weathered_barrel.json
│     │     ├─ bamboo_gold_barrel.json
│     │     ├─ bamboo_iron_barrel.json
│     │     ├─ bamboo_netherite_barrel.json
│     │     ├─ big_acacia_black_stained_glass_flask.json
│     │     ├─ big_acacia_blue_stained_glass_flask.json
│     │     ├─ big_acacia_brown_stained_glass_flask.json
│     │     ├─ big_acacia_cyan_stained_glass_flask.json
│     │     ├─ big_acacia_glass_flask.json
│     │     ├─ big_acacia_gray_stained_glass_flask.json
│     │     ├─ big_acacia_green_stained_glass_flask.json
│     │     ├─ big_acacia_light_blue_stained_glass_flask.json
│     │     ├─ big_acacia_light_gray_stained_glass_flask.json
│     │     ├─ big_acacia_lime_stained_glass_flask.json
│     │     ├─ big_acacia_magenta_stained_glass_flask.json
│     │     ├─ big_acacia_orange_stained_glass_flask.json
│     │     ├─ big_acacia_pink_stained_glass_flask.json
│     │     ├─ big_acacia_purple_stained_glass_flask.json
│     │     ├─ big_acacia_red_stained_glass_flask.json
│     │     ├─ big_acacia_tinted_glass_flask.json
│     │     ├─ big_acacia_white_stained_glass_flask.json
│     │     ├─ big_acacia_yellow_stained_glass_flask.json
│     │     ├─ big_bamboo_black_stained_glass_flask.json
│     │     ├─ big_bamboo_blue_stained_glass_flask.json
│     │     ├─ big_bamboo_brown_stained_glass_flask.json
│     │     ├─ big_bamboo_cyan_stained_glass_flask.json
│     │     ├─ big_bamboo_glass_flask.json
│     │     ├─ big_bamboo_gray_stained_glass_flask.json
│     │     ├─ big_bamboo_green_stained_glass_flask.json
│     │     ├─ big_bamboo_light_blue_stained_glass_flask.json
│     │     ├─ big_bamboo_light_gray_stained_glass_flask.json
│     │     ├─ big_bamboo_lime_stained_glass_flask.json
│     │     ├─ big_bamboo_magenta_stained_glass_flask.json
│     │     ├─ big_bamboo_orange_stained_glass_flask.json
│     │     ├─ big_bamboo_pink_stained_glass_flask.json
│     │     ├─ big_bamboo_purple_stained_glass_flask.json
│     │     ├─ big_bamboo_red_stained_glass_flask.json
│     │     ├─ big_bamboo_tinted_glass_flask.json
│     │     ├─ big_bamboo_white_stained_glass_flask.json
│     │     ├─ big_bamboo_yellow_stained_glass_flask.json
│     │     ├─ big_birch_black_stained_glass_flask.json
│     │     ├─ big_birch_blue_stained_glass_flask.json
│     │     ├─ big_birch_brown_stained_glass_flask.json
│     │     ├─ big_birch_cyan_stained_glass_flask.json
│     │     ├─ big_birch_glass_flask.json
│     │     ├─ big_birch_gray_stained_glass_flask.json
│     │     ├─ big_birch_green_stained_glass_flask.json
│     │     ├─ big_birch_light_blue_stained_glass_flask.json
│     │     ├─ big_birch_light_gray_stained_glass_flask.json
│     │     ├─ big_birch_lime_stained_glass_flask.json
│     │     ├─ big_birch_magenta_stained_glass_flask.json
│     │     ├─ big_birch_orange_stained_glass_flask.json
│     │     ├─ big_birch_pink_stained_glass_flask.json
│     │     ├─ big_birch_purple_stained_glass_flask.json
│     │     ├─ big_birch_red_stained_glass_flask.json
│     │     ├─ big_birch_tinted_glass_flask.json
│     │     ├─ big_birch_white_stained_glass_flask.json
│     │     ├─ big_birch_yellow_stained_glass_flask.json
│     │     ├─ big_cherry_black_stained_glass_flask.json
│     │     ├─ big_cherry_blue_stained_glass_flask.json
│     │     ├─ big_cherry_brown_stained_glass_flask.json
│     │     ├─ big_cherry_cyan_stained_glass_flask.json
│     │     ├─ big_cherry_glass_flask.json
│     │     ├─ big_cherry_gray_stained_glass_flask.json
│     │     ├─ big_cherry_green_stained_glass_flask.json
│     │     ├─ big_cherry_light_blue_stained_glass_flask.json
│     │     ├─ big_cherry_light_gray_stained_glass_flask.json
│     │     ├─ big_cherry_lime_stained_glass_flask.json
│     │     ├─ big_cherry_magenta_stained_glass_flask.json
│     │     ├─ big_cherry_orange_stained_glass_flask.json
│     │     ├─ big_cherry_pink_stained_glass_flask.json
│     │     ├─ big_cherry_purple_stained_glass_flask.json
│     │     ├─ big_cherry_red_stained_glass_flask.json
│     │     ├─ big_cherry_tinted_glass_flask.json
│     │     ├─ big_cherry_white_stained_glass_flask.json
│     │     ├─ big_cherry_yellow_stained_glass_flask.json
│     │     ├─ big_crimson_black_stained_glass_flask.json
│     │     ├─ big_crimson_blue_stained_glass_flask.json
│     │     ├─ big_crimson_brown_stained_glass_flask.json
│     │     ├─ big_crimson_cyan_stained_glass_flask.json
│     │     ├─ big_crimson_glass_flask.json
│     │     ├─ big_crimson_gray_stained_glass_flask.json
│     │     ├─ big_crimson_green_stained_glass_flask.json
│     │     ├─ big_crimson_light_blue_stained_glass_flask.json
│     │     ├─ big_crimson_light_gray_stained_glass_flask.json
│     │     ├─ big_crimson_lime_stained_glass_flask.json
│     │     ├─ big_crimson_magenta_stained_glass_flask.json
│     │     ├─ big_crimson_orange_stained_glass_flask.json
│     │     ├─ big_crimson_pink_stained_glass_flask.json
│     │     ├─ big_crimson_purple_stained_glass_flask.json
│     │     ├─ big_crimson_red_stained_glass_flask.json
│     │     ├─ big_crimson_tinted_glass_flask.json
│     │     ├─ big_crimson_white_stained_glass_flask.json
│     │     ├─ big_crimson_yellow_stained_glass_flask.json
│     │     ├─ big_dark_oak_black_stained_glass_flask.json
│     │     ├─ big_dark_oak_blue_stained_glass_flask.json
│     │     ├─ big_dark_oak_brown_stained_glass_flask.json
│     │     ├─ big_dark_oak_cyan_stained_glass_flask.json
│     │     ├─ big_dark_oak_glass_flask.json
│     │     ├─ big_dark_oak_gray_stained_glass_flask.json
│     │     ├─ big_dark_oak_green_stained_glass_flask.json
│     │     ├─ big_dark_oak_light_blue_stained_glass_flask.json
│     │     ├─ big_dark_oak_light_gray_stained_glass_flask.json
│     │     ├─ big_dark_oak_lime_stained_glass_flask.json
│     │     ├─ big_dark_oak_magenta_stained_glass_flask.json
│     │     ├─ big_dark_oak_orange_stained_glass_flask.json
│     │     ├─ big_dark_oak_pink_stained_glass_flask.json
│     │     ├─ big_dark_oak_purple_stained_glass_flask.json
│     │     ├─ big_dark_oak_red_stained_glass_flask.json
│     │     ├─ big_dark_oak_tinted_glass_flask.json
│     │     ├─ big_dark_oak_white_stained_glass_flask.json
│     │     ├─ big_dark_oak_yellow_stained_glass_flask.json
│     │     ├─ big_jungle_black_stained_glass_flask.json
│     │     ├─ big_jungle_blue_stained_glass_flask.json
│     │     ├─ big_jungle_brown_stained_glass_flask.json
│     │     ├─ big_jungle_cyan_stained_glass_flask.json
│     │     ├─ big_jungle_glass_flask.json
│     │     ├─ big_jungle_gray_stained_glass_flask.json
│     │     ├─ big_jungle_green_stained_glass_flask.json
│     │     ├─ big_jungle_light_blue_stained_glass_flask.json
│     │     ├─ big_jungle_light_gray_stained_glass_flask.json
│     │     ├─ big_jungle_lime_stained_glass_flask.json
│     │     ├─ big_jungle_magenta_stained_glass_flask.json
│     │     ├─ big_jungle_orange_stained_glass_flask.json
│     │     ├─ big_jungle_pink_stained_glass_flask.json
│     │     ├─ big_jungle_purple_stained_glass_flask.json
│     │     ├─ big_jungle_red_stained_glass_flask.json
│     │     ├─ big_jungle_tinted_glass_flask.json
│     │     ├─ big_jungle_white_stained_glass_flask.json
│     │     ├─ big_jungle_yellow_stained_glass_flask.json
│     │     ├─ big_mangrove_black_stained_glass_flask.json
│     │     ├─ big_mangrove_blue_stained_glass_flask.json
│     │     ├─ big_mangrove_brown_stained_glass_flask.json
│     │     ├─ big_mangrove_cyan_stained_glass_flask.json
│     │     ├─ big_mangrove_glass_flask.json
│     │     ├─ big_mangrove_gray_stained_glass_flask.json
│     │     ├─ big_mangrove_green_stained_glass_flask.json
│     │     ├─ big_mangrove_light_blue_stained_glass_flask.json
│     │     ├─ big_mangrove_light_gray_stained_glass_flask.json
│     │     ├─ big_mangrove_lime_stained_glass_flask.json
│     │     ├─ big_mangrove_magenta_stained_glass_flask.json
│     │     ├─ big_mangrove_orange_stained_glass_flask.json
│     │     ├─ big_mangrove_pink_stained_glass_flask.json
│     │     ├─ big_mangrove_purple_stained_glass_flask.json
│     │     ├─ big_mangrove_red_stained_glass_flask.json
│     │     ├─ big_mangrove_tinted_glass_flask.json
│     │     ├─ big_mangrove_white_stained_glass_flask.json
│     │     ├─ big_mangrove_yellow_stained_glass_flask.json
│     │     ├─ big_oak_black_stained_glass_flask.json
│     │     ├─ big_oak_blue_stained_glass_flask.json
│     │     ├─ big_oak_brown_stained_glass_flask.json
│     │     ├─ big_oak_cyan_stained_glass_flask.json
│     │     ├─ big_oak_glass_flask.json
│     │     ├─ big_oak_gray_stained_glass_flask.json
│     │     ├─ big_oak_green_stained_glass_flask.json
│     │     ├─ big_oak_light_blue_stained_glass_flask.json
│     │     ├─ big_oak_light_gray_stained_glass_flask.json
│     │     ├─ big_oak_lime_stained_glass_flask.json
│     │     ├─ big_oak_magenta_stained_glass_flask.json
│     │     ├─ big_oak_orange_stained_glass_flask.json
│     │     ├─ big_oak_pink_stained_glass_flask.json
│     │     ├─ big_oak_purple_stained_glass_flask.json
│     │     ├─ big_oak_red_stained_glass_flask.json
│     │     ├─ big_oak_tinted_glass_flask.json
│     │     ├─ big_oak_white_stained_glass_flask.json
│     │     ├─ big_oak_yellow_stained_glass_flask.json
│     │     ├─ big_pale_oak_black_stained_glass_flask.json
│     │     ├─ big_pale_oak_blue_stained_glass_flask.json
│     │     ├─ big_pale_oak_brown_stained_glass_flask.json
│     │     ├─ big_pale_oak_cyan_stained_glass_flask.json
│     │     ├─ big_pale_oak_glass_flask.json
│     │     ├─ big_pale_oak_gray_stained_glass_flask.json
│     │     ├─ big_pale_oak_green_stained_glass_flask.json
│     │     ├─ big_pale_oak_light_blue_stained_glass_flask.json
│     │     ├─ big_pale_oak_light_gray_stained_glass_flask.json
│     │     ├─ big_pale_oak_lime_stained_glass_flask.json
│     │     ├─ big_pale_oak_magenta_stained_glass_flask.json
│     │     ├─ big_pale_oak_orange_stained_glass_flask.json
│     │     ├─ big_pale_oak_pink_stained_glass_flask.json
│     │     ├─ big_pale_oak_purple_stained_glass_flask.json
│     │     ├─ big_pale_oak_red_stained_glass_flask.json
│     │     ├─ big_pale_oak_tinted_glass_flask.json
│     │     ├─ big_pale_oak_white_stained_glass_flask.json
│     │     ├─ big_pale_oak_yellow_stained_glass_flask.json
│     │     ├─ big_spruce_black_stained_glass_flask.json
│     │     ├─ big_spruce_blue_stained_glass_flask.json
│     │     ├─ big_spruce_brown_stained_glass_flask.json
│     │     ├─ big_spruce_cyan_stained_glass_flask.json
│     │     ├─ big_spruce_glass_flask.json
│     │     ├─ big_spruce_gray_stained_glass_flask.json
│     │     ├─ big_spruce_green_stained_glass_flask.json
│     │     ├─ big_spruce_light_blue_stained_glass_flask.json
│     │     ├─ big_spruce_light_gray_stained_glass_flask.json
│     │     ├─ big_spruce_lime_stained_glass_flask.json
│     │     ├─ big_spruce_magenta_stained_glass_flask.json
│     │     ├─ big_spruce_orange_stained_glass_flask.json
│     │     ├─ big_spruce_pink_stained_glass_flask.json
│     │     ├─ big_spruce_purple_stained_glass_flask.json
│     │     ├─ big_spruce_red_stained_glass_flask.json
│     │     ├─ big_spruce_tinted_glass_flask.json
│     │     ├─ big_spruce_white_stained_glass_flask.json
│     │     ├─ big_spruce_yellow_stained_glass_flask.json
│     │     ├─ big_warped_black_stained_glass_flask.json
│     │     ├─ big_warped_blue_stained_glass_flask.json
│     │     ├─ big_warped_brown_stained_glass_flask.json
│     │     ├─ big_warped_cyan_stained_glass_flask.json
│     │     ├─ big_warped_glass_flask.json
│     │     ├─ big_warped_gray_stained_glass_flask.json
│     │     ├─ big_warped_green_stained_glass_flask.json
│     │     ├─ big_warped_light_blue_stained_glass_flask.json
│     │     ├─ big_warped_light_gray_stained_glass_flask.json
│     │     ├─ big_warped_lime_stained_glass_flask.json
│     │     ├─ big_warped_magenta_stained_glass_flask.json
│     │     ├─ big_warped_orange_stained_glass_flask.json
│     │     ├─ big_warped_pink_stained_glass_flask.json
│     │     ├─ big_warped_purple_stained_glass_flask.json
│     │     ├─ big_warped_red_stained_glass_flask.json
│     │     ├─ big_warped_tinted_glass_flask.json
│     │     ├─ big_warped_white_stained_glass_flask.json
│     │     ├─ big_warped_yellow_stained_glass_flask.json
│     │     ├─ birch_copper_barrel.json
│     │     ├─ birch_copper_exposed_barrel.json
│     │     ├─ birch_copper_oxidized_barrel.json
│     │     ├─ birch_copper_weathered_barrel.json
│     │     ├─ birch_gold_barrel.json
│     │     ├─ birch_iron_barrel.json
│     │     ├─ birch_netherite_barrel.json
│     │     ├─ cherry_copper_barrel.json
│     │     ├─ cherry_copper_exposed_barrel.json
│     │     ├─ cherry_copper_oxidized_barrel.json
│     │     ├─ cherry_copper_weathered_barrel.json
│     │     ├─ cherry_gold_barrel.json
│     │     ├─ cherry_iron_barrel.json
│     │     ├─ cherry_netherite_barrel.json
│     │     ├─ copper_exposed_keg.json
│     │     ├─ copper_keg.json
│     │     ├─ copper_oxidized_keg.json
│     │     ├─ copper_weathered_keg.json
│     │     ├─ crimson_copper_barrel.json
│     │     ├─ crimson_copper_exposed_barrel.json
│     │     ├─ crimson_copper_oxidized_barrel.json
│     │     ├─ crimson_copper_weathered_barrel.json
│     │     ├─ crimson_gold_barrel.json
│     │     ├─ crimson_iron_barrel.json
│     │     ├─ crimson_netherite_barrel.json
│     │     ├─ dark_oak_copper_barrel.json
│     │     ├─ dark_oak_copper_exposed_barrel.json
│     │     ├─ dark_oak_copper_oxidized_barrel.json
│     │     ├─ dark_oak_copper_weathered_barrel.json
│     │     ├─ dark_oak_gold_barrel.json
│     │     ├─ dark_oak_iron_barrel.json
│     │     ├─ dark_oak_netherite_barrel.json
│     │     ├─ gold_keg.json
│     │     ├─ iron_keg.json
│     │     ├─ jungle_copper_barrel.json
│     │     ├─ jungle_copper_exposed_barrel.json
│     │     ├─ jungle_copper_oxidized_barrel.json
│     │     ├─ jungle_copper_weathered_barrel.json
│     │     ├─ jungle_gold_barrel.json
│     │     ├─ jungle_iron_barrel.json
│     │     ├─ jungle_netherite_barrel.json
│     │     ├─ mangrove_copper_barrel.json
│     │     ├─ mangrove_copper_exposed_barrel.json
│     │     ├─ mangrove_copper_oxidized_barrel.json
│     │     ├─ mangrove_copper_weathered_barrel.json
│     │     ├─ mangrove_gold_barrel.json
│     │     ├─ mangrove_iron_barrel.json
│     │     ├─ mangrove_netherite_barrel.json
│     │     ├─ medium_acacia_black_stained_glass_flask.json
│     │     ├─ medium_acacia_blue_stained_glass_flask.json
│     │     ├─ medium_acacia_brown_stained_glass_flask.json
│     │     ├─ medium_acacia_cyan_stained_glass_flask.json
│     │     ├─ medium_acacia_glass_flask.json
│     │     ├─ medium_acacia_gray_stained_glass_flask.json
│     │     ├─ medium_acacia_green_stained_glass_flask.json
│     │     ├─ medium_acacia_light_blue_stained_glass_flask.json
│     │     ├─ medium_acacia_light_gray_stained_glass_flask.json
│     │     ├─ medium_acacia_lime_stained_glass_flask.json
│     │     ├─ medium_acacia_magenta_stained_glass_flask.json
│     │     ├─ medium_acacia_orange_stained_glass_flask.json
│     │     ├─ medium_acacia_pink_stained_glass_flask.json
│     │     ├─ medium_acacia_purple_stained_glass_flask.json
│     │     ├─ medium_acacia_red_stained_glass_flask.json
│     │     ├─ medium_acacia_tinted_glass_flask.json
│     │     ├─ medium_acacia_white_stained_glass_flask.json
│     │     ├─ medium_acacia_yellow_stained_glass_flask.json
│     │     ├─ medium_bamboo_black_stained_glass_flask.json
│     │     ├─ medium_bamboo_blue_stained_glass_flask.json
│     │     ├─ medium_bamboo_brown_stained_glass_flask.json
│     │     ├─ medium_bamboo_cyan_stained_glass_flask.json
│     │     ├─ medium_bamboo_glass_flask.json
│     │     ├─ medium_bamboo_gray_stained_glass_flask.json
│     │     ├─ medium_bamboo_green_stained_glass_flask.json
│     │     ├─ medium_bamboo_light_blue_stained_glass_flask.json
│     │     ├─ medium_bamboo_light_gray_stained_glass_flask.json
│     │     ├─ medium_bamboo_lime_stained_glass_flask.json
│     │     ├─ medium_bamboo_magenta_stained_glass_flask.json
│     │     ├─ medium_bamboo_orange_stained_glass_flask.json
│     │     ├─ medium_bamboo_pink_stained_glass_flask.json
│     │     ├─ medium_bamboo_purple_stained_glass_flask.json
│     │     ├─ medium_bamboo_red_stained_glass_flask.json
│     │     ├─ medium_bamboo_tinted_glass_flask.json
│     │     ├─ medium_bamboo_white_stained_glass_flask.json
│     │     ├─ medium_bamboo_yellow_stained_glass_flask.json
│     │     ├─ medium_birch_black_stained_glass_flask.json
│     │     ├─ medium_birch_blue_stained_glass_flask.json
│     │     ├─ medium_birch_brown_stained_glass_flask.json
│     │     ├─ medium_birch_cyan_stained_glass_flask.json
│     │     ├─ medium_birch_glass_flask.json
│     │     ├─ medium_birch_gray_stained_glass_flask.json
│     │     ├─ medium_birch_green_stained_glass_flask.json
│     │     ├─ medium_birch_light_blue_stained_glass_flask.json
│     │     ├─ medium_birch_light_gray_stained_glass_flask.json
│     │     ├─ medium_birch_lime_stained_glass_flask.json
│     │     ├─ medium_birch_magenta_stained_glass_flask.json
│     │     ├─ medium_birch_orange_stained_glass_flask.json
│     │     ├─ medium_birch_pink_stained_glass_flask.json
│     │     ├─ medium_birch_purple_stained_glass_flask.json
│     │     ├─ medium_birch_red_stained_glass_flask.json
│     │     ├─ medium_birch_tinted_glass_flask.json
│     │     ├─ medium_birch_white_stained_glass_flask.json
│     │     ├─ medium_birch_yellow_stained_glass_flask.json
│     │     ├─ medium_cherry_black_stained_glass_flask.json
│     │     ├─ medium_cherry_blue_stained_glass_flask.json
│     │     ├─ medium_cherry_brown_stained_glass_flask.json
│     │     ├─ medium_cherry_cyan_stained_glass_flask.json
│     │     ├─ medium_cherry_glass_flask.json
│     │     ├─ medium_cherry_gray_stained_glass_flask.json
│     │     ├─ medium_cherry_green_stained_glass_flask.json
│     │     ├─ medium_cherry_light_blue_stained_glass_flask.json
│     │     ├─ medium_cherry_light_gray_stained_glass_flask.json
│     │     ├─ medium_cherry_lime_stained_glass_flask.json
│     │     ├─ medium_cherry_magenta_stained_glass_flask.json
│     │     ├─ medium_cherry_orange_stained_glass_flask.json
│     │     ├─ medium_cherry_pink_stained_glass_flask.json
│     │     ├─ medium_cherry_purple_stained_glass_flask.json
│     │     ├─ medium_cherry_red_stained_glass_flask.json
│     │     ├─ medium_cherry_tinted_glass_flask.json
│     │     ├─ medium_cherry_white_stained_glass_flask.json
│     │     ├─ medium_cherry_yellow_stained_glass_flask.json
│     │     ├─ medium_crimson_black_stained_glass_flask.json
│     │     ├─ medium_crimson_blue_stained_glass_flask.json
│     │     ├─ medium_crimson_brown_stained_glass_flask.json
│     │     ├─ medium_crimson_cyan_stained_glass_flask.json
│     │     ├─ medium_crimson_glass_flask.json
│     │     ├─ medium_crimson_gray_stained_glass_flask.json
│     │     ├─ medium_crimson_green_stained_glass_flask.json
│     │     ├─ medium_crimson_light_blue_stained_glass_flask.json
│     │     ├─ medium_crimson_light_gray_stained_glass_flask.json
│     │     ├─ medium_crimson_lime_stained_glass_flask.json
│     │     ├─ medium_crimson_magenta_stained_glass_flask.json
│     │     ├─ medium_crimson_orange_stained_glass_flask.json
│     │     ├─ medium_crimson_pink_stained_glass_flask.json
│     │     ├─ medium_crimson_purple_stained_glass_flask.json
│     │     ├─ medium_crimson_red_stained_glass_flask.json
│     │     ├─ medium_crimson_tinted_glass_flask.json
│     │     ├─ medium_crimson_white_stained_glass_flask.json
│     │     ├─ medium_crimson_yellow_stained_glass_flask.json
│     │     ├─ medium_dark_oak_black_stained_glass_flask.json
│     │     ├─ medium_dark_oak_blue_stained_glass_flask.json
│     │     ├─ medium_dark_oak_brown_stained_glass_flask.json
│     │     ├─ medium_dark_oak_cyan_stained_glass_flask.json
│     │     ├─ medium_dark_oak_glass_flask.json
│     │     ├─ medium_dark_oak_gray_stained_glass_flask.json
│     │     ├─ medium_dark_oak_green_stained_glass_flask.json
│     │     ├─ medium_dark_oak_light_blue_stained_glass_flask.json
│     │     ├─ medium_dark_oak_light_gray_stained_glass_flask.json
│     │     ├─ medium_dark_oak_lime_stained_glass_flask.json
│     │     ├─ medium_dark_oak_magenta_stained_glass_flask.json
│     │     ├─ medium_dark_oak_orange_stained_glass_flask.json
│     │     ├─ medium_dark_oak_pink_stained_glass_flask.json
│     │     ├─ medium_dark_oak_purple_stained_glass_flask.json
│     │     ├─ medium_dark_oak_red_stained_glass_flask.json
│     │     ├─ medium_dark_oak_tinted_glass_flask.json
│     │     ├─ medium_dark_oak_white_stained_glass_flask.json
│     │     ├─ medium_dark_oak_yellow_stained_glass_flask.json
│     │     ├─ medium_jungle_black_stained_glass_flask.json
│     │     ├─ medium_jungle_blue_stained_glass_flask.json
│     │     ├─ medium_jungle_brown_stained_glass_flask.json
│     │     ├─ medium_jungle_cyan_stained_glass_flask.json
│     │     ├─ medium_jungle_glass_flask.json
│     │     ├─ medium_jungle_gray_stained_glass_flask.json
│     │     ├─ medium_jungle_green_stained_glass_flask.json
│     │     ├─ medium_jungle_light_blue_stained_glass_flask.json
│     │     ├─ medium_jungle_light_gray_stained_glass_flask.json
│     │     ├─ medium_jungle_lime_stained_glass_flask.json
│     │     ├─ medium_jungle_magenta_stained_glass_flask.json
│     │     ├─ medium_jungle_orange_stained_glass_flask.json
│     │     ├─ medium_jungle_pink_stained_glass_flask.json
│     │     ├─ medium_jungle_purple_stained_glass_flask.json
│     │     ├─ medium_jungle_red_stained_glass_flask.json
│     │     ├─ medium_jungle_tinted_glass_flask.json
│     │     ├─ medium_jungle_white_stained_glass_flask.json
│     │     ├─ medium_jungle_yellow_stained_glass_flask.json
│     │     ├─ medium_mangrove_black_stained_glass_flask.json
│     │     ├─ medium_mangrove_blue_stained_glass_flask.json
│     │     ├─ medium_mangrove_brown_stained_glass_flask.json
│     │     ├─ medium_mangrove_cyan_stained_glass_flask.json
│     │     ├─ medium_mangrove_glass_flask.json
│     │     ├─ medium_mangrove_gray_stained_glass_flask.json
│     │     ├─ medium_mangrove_green_stained_glass_flask.json
│     │     ├─ medium_mangrove_light_blue_stained_glass_flask.json
│     │     ├─ medium_mangrove_light_gray_stained_glass_flask.json
│     │     ├─ medium_mangrove_lime_stained_glass_flask.json
│     │     ├─ medium_mangrove_magenta_stained_glass_flask.json
│     │     ├─ medium_mangrove_orange_stained_glass_flask.json
│     │     ├─ medium_mangrove_pink_stained_glass_flask.json
│     │     ├─ medium_mangrove_purple_stained_glass_flask.json
│     │     ├─ medium_mangrove_red_stained_glass_flask.json
│     │     ├─ medium_mangrove_tinted_glass_flask.json
│     │     ├─ medium_mangrove_white_stained_glass_flask.json
│     │     ├─ medium_mangrove_yellow_stained_glass_flask.json
│     │     ├─ medium_oak_black_stained_glass_flask.json
│     │     ├─ medium_oak_blue_stained_glass_flask.json
│     │     ├─ medium_oak_brown_stained_glass_flask.json
│     │     ├─ medium_oak_cyan_stained_glass_flask.json
│     │     ├─ medium_oak_glass_flask.json
│     │     ├─ medium_oak_gray_stained_glass_flask.json
│     │     ├─ medium_oak_green_stained_glass_flask.json
│     │     ├─ medium_oak_light_blue_stained_glass_flask.json
│     │     ├─ medium_oak_light_gray_stained_glass_flask.json
│     │     ├─ medium_oak_lime_stained_glass_flask.json
│     │     ├─ medium_oak_magenta_stained_glass_flask.json
│     │     ├─ medium_oak_orange_stained_glass_flask.json
│     │     ├─ medium_oak_pink_stained_glass_flask.json
│     │     ├─ medium_oak_purple_stained_glass_flask.json
│     │     ├─ medium_oak_red_stained_glass_flask.json
│     │     ├─ medium_oak_tinted_glass_flask.json
│     │     ├─ medium_oak_white_stained_glass_flask.json
│     │     ├─ medium_oak_yellow_stained_glass_flask.json
│     │     ├─ medium_pale_oak_black_stained_glass_flask.json
│     │     ├─ medium_pale_oak_blue_stained_glass_flask.json
│     │     ├─ medium_pale_oak_brown_stained_glass_flask.json
│     │     ├─ medium_pale_oak_cyan_stained_glass_flask.json
│     │     ├─ medium_pale_oak_glass_flask.json
│     │     ├─ medium_pale_oak_gray_stained_glass_flask.json
│     │     ├─ medium_pale_oak_green_stained_glass_flask.json
│     │     ├─ medium_pale_oak_light_blue_stained_glass_flask.json
│     │     ├─ medium_pale_oak_light_gray_stained_glass_flask.json
│     │     ├─ medium_pale_oak_lime_stained_glass_flask.json
│     │     ├─ medium_pale_oak_magenta_stained_glass_flask.json
│     │     ├─ medium_pale_oak_orange_stained_glass_flask.json
│     │     ├─ medium_pale_oak_pink_stained_glass_flask.json
│     │     ├─ medium_pale_oak_purple_stained_glass_flask.json
│     │     ├─ medium_pale_oak_red_stained_glass_flask.json
│     │     ├─ medium_pale_oak_tinted_glass_flask.json
│     │     ├─ medium_pale_oak_white_stained_glass_flask.json
│     │     ├─ medium_pale_oak_yellow_stained_glass_flask.json
│     │     ├─ medium_spruce_black_stained_glass_flask.json
│     │     ├─ medium_spruce_blue_stained_glass_flask.json
│     │     ├─ medium_spruce_brown_stained_glass_flask.json
│     │     ├─ medium_spruce_cyan_stained_glass_flask.json
│     │     ├─ medium_spruce_glass_flask.json
│     │     ├─ medium_spruce_gray_stained_glass_flask.json
│     │     ├─ medium_spruce_green_stained_glass_flask.json
│     │     ├─ medium_spruce_light_blue_stained_glass_flask.json
│     │     ├─ medium_spruce_light_gray_stained_glass_flask.json
│     │     ├─ medium_spruce_lime_stained_glass_flask.json
│     │     ├─ medium_spruce_magenta_stained_glass_flask.json
│     │     ├─ medium_spruce_orange_stained_glass_flask.json
│     │     ├─ medium_spruce_pink_stained_glass_flask.json
│     │     ├─ medium_spruce_purple_stained_glass_flask.json
│     │     ├─ medium_spruce_red_stained_glass_flask.json
│     │     ├─ medium_spruce_tinted_glass_flask.json
│     │     ├─ medium_spruce_white_stained_glass_flask.json
│     │     ├─ medium_spruce_yellow_stained_glass_flask.json
│     │     ├─ medium_warped_black_stained_glass_flask.json
│     │     ├─ medium_warped_blue_stained_glass_flask.json
│     │     ├─ medium_warped_brown_stained_glass_flask.json
│     │     ├─ medium_warped_cyan_stained_glass_flask.json
│     │     ├─ medium_warped_glass_flask.json
│     │     ├─ medium_warped_gray_stained_glass_flask.json
│     │     ├─ medium_warped_green_stained_glass_flask.json
│     │     ├─ medium_warped_light_blue_stained_glass_flask.json
│     │     ├─ medium_warped_light_gray_stained_glass_flask.json
│     │     ├─ medium_warped_lime_stained_glass_flask.json
│     │     ├─ medium_warped_magenta_stained_glass_flask.json
│     │     ├─ medium_warped_orange_stained_glass_flask.json
│     │     ├─ medium_warped_pink_stained_glass_flask.json
│     │     ├─ medium_warped_purple_stained_glass_flask.json
│     │     ├─ medium_warped_red_stained_glass_flask.json
│     │     ├─ medium_warped_tinted_glass_flask.json
│     │     ├─ medium_warped_white_stained_glass_flask.json
│     │     ├─ medium_warped_yellow_stained_glass_flask.json
│     │     ├─ netherite_keg.json
│     │     ├─ oak_copper_barrel.json
│     │     ├─ oak_copper_exposed_barrel.json
│     │     ├─ oak_copper_oxidized_barrel.json
│     │     ├─ oak_copper_weathered_barrel.json
│     │     ├─ oak_gold_barrel.json
│     │     ├─ oak_iron_barrel.json
│     │     ├─ oak_netherite_barrel.json
│     │     ├─ pale_oak_copper_barrel.json
│     │     ├─ pale_oak_copper_exposed_barrel.json
│     │     ├─ pale_oak_copper_oxidized_barrel.json
│     │     ├─ pale_oak_copper_weathered_barrel.json
│     │     ├─ pale_oak_gold_barrel.json
│     │     ├─ pale_oak_iron_barrel.json
│     │     ├─ pale_oak_netherite_barrel.json
│     │     ├─ small_acacia_black_stained_glass_flask.json
│     │     ├─ small_acacia_blue_stained_glass_flask.json
│     │     ├─ small_acacia_brown_stained_glass_flask.json
│     │     ├─ small_acacia_cyan_stained_glass_flask.json
│     │     ├─ small_acacia_glass_flask.json
│     │     ├─ small_acacia_gray_stained_glass_flask.json
│     │     ├─ small_acacia_green_stained_glass_flask.json
│     │     ├─ small_acacia_light_blue_stained_glass_flask.json
│     │     ├─ small_acacia_light_gray_stained_glass_flask.json
│     │     ├─ small_acacia_lime_stained_glass_flask.json
│     │     ├─ small_acacia_magenta_stained_glass_flask.json
│     │     ├─ small_acacia_orange_stained_glass_flask.json
│     │     ├─ small_acacia_pink_stained_glass_flask.json
│     │     ├─ small_acacia_purple_stained_glass_flask.json
│     │     ├─ small_acacia_red_stained_glass_flask.json
│     │     ├─ small_acacia_tinted_glass_flask.json
│     │     ├─ small_acacia_white_stained_glass_flask.json
│     │     ├─ small_acacia_yellow_stained_glass_flask.json
│     │     ├─ small_bamboo_black_stained_glass_flask.json
│     │     ├─ small_bamboo_blue_stained_glass_flask.json
│     │     ├─ small_bamboo_brown_stained_glass_flask.json
│     │     ├─ small_bamboo_cyan_stained_glass_flask.json
│     │     ├─ small_bamboo_glass_flask.json
│     │     ├─ small_bamboo_gray_stained_glass_flask.json
│     │     ├─ small_bamboo_green_stained_glass_flask.json
│     │     ├─ small_bamboo_light_blue_stained_glass_flask.json
│     │     ├─ small_bamboo_light_gray_stained_glass_flask.json
│     │     ├─ small_bamboo_lime_stained_glass_flask.json
│     │     ├─ small_bamboo_magenta_stained_glass_flask.json
│     │     ├─ small_bamboo_orange_stained_glass_flask.json
│     │     ├─ small_bamboo_pink_stained_glass_flask.json
│     │     ├─ small_bamboo_purple_stained_glass_flask.json
│     │     ├─ small_bamboo_red_stained_glass_flask.json
│     │     ├─ small_bamboo_tinted_glass_flask.json
│     │     ├─ small_bamboo_white_stained_glass_flask.json
│     │     ├─ small_bamboo_yellow_stained_glass_flask.json
│     │     ├─ small_birch_black_stained_glass_flask.json
│     │     ├─ small_birch_blue_stained_glass_flask.json
│     │     ├─ small_birch_brown_stained_glass_flask.json
│     │     ├─ small_birch_cyan_stained_glass_flask.json
│     │     ├─ small_birch_glass_flask.json
│     │     ├─ small_birch_gray_stained_glass_flask.json
│     │     ├─ small_birch_green_stained_glass_flask.json
│     │     ├─ small_birch_light_blue_stained_glass_flask.json
│     │     ├─ small_birch_light_gray_stained_glass_flask.json
│     │     ├─ small_birch_lime_stained_glass_flask.json
│     │     ├─ small_birch_magenta_stained_glass_flask.json
│     │     ├─ small_birch_orange_stained_glass_flask.json
│     │     ├─ small_birch_pink_stained_glass_flask.json
│     │     ├─ small_birch_purple_stained_glass_flask.json
│     │     ├─ small_birch_red_stained_glass_flask.json
│     │     ├─ small_birch_tinted_glass_flask.json
│     │     ├─ small_birch_white_stained_glass_flask.json
│     │     ├─ small_birch_yellow_stained_glass_flask.json
│     │     ├─ small_cherry_black_stained_glass_flask.json
│     │     ├─ small_cherry_blue_stained_glass_flask.json
│     │     ├─ small_cherry_brown_stained_glass_flask.json
│     │     ├─ small_cherry_cyan_stained_glass_flask.json
│     │     ├─ small_cherry_glass_flask.json
│     │     ├─ small_cherry_gray_stained_glass_flask.json
│     │     ├─ small_cherry_green_stained_glass_flask.json
│     │     ├─ small_cherry_light_blue_stained_glass_flask.json
│     │     ├─ small_cherry_light_gray_stained_glass_flask.json
│     │     ├─ small_cherry_lime_stained_glass_flask.json
│     │     ├─ small_cherry_magenta_stained_glass_flask.json
│     │     ├─ small_cherry_orange_stained_glass_flask.json
│     │     ├─ small_cherry_pink_stained_glass_flask.json
│     │     ├─ small_cherry_purple_stained_glass_flask.json
│     │     ├─ small_cherry_red_stained_glass_flask.json
│     │     ├─ small_cherry_tinted_glass_flask.json
│     │     ├─ small_cherry_white_stained_glass_flask.json
│     │     ├─ small_cherry_yellow_stained_glass_flask.json
│     │     ├─ small_crimson_black_stained_glass_flask.json
│     │     ├─ small_crimson_blue_stained_glass_flask.json
│     │     ├─ small_crimson_brown_stained_glass_flask.json
│     │     ├─ small_crimson_cyan_stained_glass_flask.json
│     │     ├─ small_crimson_glass_flask.json
│     │     ├─ small_crimson_gray_stained_glass_flask.json
│     │     ├─ small_crimson_green_stained_glass_flask.json
│     │     ├─ small_crimson_light_blue_stained_glass_flask.json
│     │     ├─ small_crimson_light_gray_stained_glass_flask.json
│     │     ├─ small_crimson_lime_stained_glass_flask.json
│     │     ├─ small_crimson_magenta_stained_glass_flask.json
│     │     ├─ small_crimson_orange_stained_glass_flask.json
│     │     ├─ small_crimson_pink_stained_glass_flask.json
│     │     ├─ small_crimson_purple_stained_glass_flask.json
│     │     ├─ small_crimson_red_stained_glass_flask.json
│     │     ├─ small_crimson_tinted_glass_flask.json
│     │     ├─ small_crimson_white_stained_glass_flask.json
│     │     ├─ small_crimson_yellow_stained_glass_flask.json
│     │     ├─ small_dark_oak_black_stained_glass_flask.json
│     │     ├─ small_dark_oak_blue_stained_glass_flask.json
│     │     ├─ small_dark_oak_brown_stained_glass_flask.json
│     │     ├─ small_dark_oak_cyan_stained_glass_flask.json
│     │     ├─ small_dark_oak_glass_flask.json
│     │     ├─ small_dark_oak_gray_stained_glass_flask.json
│     │     ├─ small_dark_oak_green_stained_glass_flask.json
│     │     ├─ small_dark_oak_light_blue_stained_glass_flask.json
│     │     ├─ small_dark_oak_light_gray_stained_glass_flask.json
│     │     ├─ small_dark_oak_lime_stained_glass_flask.json
│     │     ├─ small_dark_oak_magenta_stained_glass_flask.json
│     │     ├─ small_dark_oak_orange_stained_glass_flask.json
│     │     ├─ small_dark_oak_pink_stained_glass_flask.json
│     │     ├─ small_dark_oak_purple_stained_glass_flask.json
│     │     ├─ small_dark_oak_red_stained_glass_flask.json
│     │     ├─ small_dark_oak_tinted_glass_flask.json
│     │     ├─ small_dark_oak_white_stained_glass_flask.json
│     │     ├─ small_dark_oak_yellow_stained_glass_flask.json
│     │     ├─ small_jungle_black_stained_glass_flask.json
│     │     ├─ small_jungle_blue_stained_glass_flask.json
│     │     ├─ small_jungle_brown_stained_glass_flask.json
│     │     ├─ small_jungle_cyan_stained_glass_flask.json
│     │     ├─ small_jungle_glass_flask.json
│     │     ├─ small_jungle_gray_stained_glass_flask.json
│     │     ├─ small_jungle_green_stained_glass_flask.json
│     │     ├─ small_jungle_light_blue_stained_glass_flask.json
│     │     ├─ small_jungle_light_gray_stained_glass_flask.json
│     │     ├─ small_jungle_lime_stained_glass_flask.json
│     │     ├─ small_jungle_magenta_stained_glass_flask.json
│     │     ├─ small_jungle_orange_stained_glass_flask.json
│     │     ├─ small_jungle_pink_stained_glass_flask.json
│     │     ├─ small_jungle_purple_stained_glass_flask.json
│     │     ├─ small_jungle_red_stained_glass_flask.json
│     │     ├─ small_jungle_tinted_glass_flask.json
│     │     ├─ small_jungle_white_stained_glass_flask.json
│     │     ├─ small_jungle_yellow_stained_glass_flask.json
│     │     ├─ small_mangrove_black_stained_glass_flask.json
│     │     ├─ small_mangrove_blue_stained_glass_flask.json
│     │     ├─ small_mangrove_brown_stained_glass_flask.json
│     │     ├─ small_mangrove_cyan_stained_glass_flask.json
│     │     ├─ small_mangrove_glass_flask.json
│     │     ├─ small_mangrove_gray_stained_glass_flask.json
│     │     ├─ small_mangrove_green_stained_glass_flask.json
│     │     ├─ small_mangrove_light_blue_stained_glass_flask.json
│     │     ├─ small_mangrove_light_gray_stained_glass_flask.json
│     │     ├─ small_mangrove_lime_stained_glass_flask.json
│     │     ├─ small_mangrove_magenta_stained_glass_flask.json
│     │     ├─ small_mangrove_orange_stained_glass_flask.json
│     │     ├─ small_mangrove_pink_stained_glass_flask.json
│     │     ├─ small_mangrove_purple_stained_glass_flask.json
│     │     ├─ small_mangrove_red_stained_glass_flask.json
│     │     ├─ small_mangrove_tinted_glass_flask.json
│     │     ├─ small_mangrove_white_stained_glass_flask.json
│     │     ├─ small_mangrove_yellow_stained_glass_flask.json
│     │     ├─ small_oak_black_stained_glass_flask.json
│     │     ├─ small_oak_blue_stained_glass_flask.json
│     │     ├─ small_oak_brown_stained_glass_flask.json
│     │     ├─ small_oak_cyan_stained_glass_flask.json
│     │     ├─ small_oak_glass_flask.json
│     │     ├─ small_oak_gray_stained_glass_flask.json
│     │     ├─ small_oak_green_stained_glass_flask.json
│     │     ├─ small_oak_light_blue_stained_glass_flask.json
│     │     ├─ small_oak_light_gray_stained_glass_flask.json
│     │     ├─ small_oak_lime_stained_glass_flask.json
│     │     ├─ small_oak_magenta_stained_glass_flask.json
│     │     ├─ small_oak_orange_stained_glass_flask.json
│     │     ├─ small_oak_pink_stained_glass_flask.json
│     │     ├─ small_oak_purple_stained_glass_flask.json
│     │     ├─ small_oak_red_stained_glass_flask.json
│     │     ├─ small_oak_tinted_glass_flask.json
│     │     ├─ small_oak_white_stained_glass_flask.json
│     │     ├─ small_oak_yellow_stained_glass_flask.json
│     │     ├─ small_pale_oak_black_stained_glass_flask.json
│     │     ├─ small_pale_oak_blue_stained_glass_flask.json
│     │     ├─ small_pale_oak_brown_stained_glass_flask.json
│     │     ├─ small_pale_oak_cyan_stained_glass_flask.json
│     │     ├─ small_pale_oak_glass_flask.json
│     │     ├─ small_pale_oak_gray_stained_glass_flask.json
│     │     ├─ small_pale_oak_green_stained_glass_flask.json
│     │     ├─ small_pale_oak_light_blue_stained_glass_flask.json
│     │     ├─ small_pale_oak_light_gray_stained_glass_flask.json
│     │     ├─ small_pale_oak_lime_stained_glass_flask.json
│     │     ├─ small_pale_oak_magenta_stained_glass_flask.json
│     │     ├─ small_pale_oak_orange_stained_glass_flask.json
│     │     ├─ small_pale_oak_pink_stained_glass_flask.json
│     │     ├─ small_pale_oak_purple_stained_glass_flask.json
│     │     ├─ small_pale_oak_red_stained_glass_flask.json
│     │     ├─ small_pale_oak_tinted_glass_flask.json
│     │     ├─ small_pale_oak_white_stained_glass_flask.json
│     │     ├─ small_pale_oak_yellow_stained_glass_flask.json
│     │     ├─ small_spruce_black_stained_glass_flask.json
│     │     ├─ small_spruce_blue_stained_glass_flask.json
│     │     ├─ small_spruce_brown_stained_glass_flask.json
│     │     ├─ small_spruce_cyan_stained_glass_flask.json
│     │     ├─ small_spruce_glass_flask.json
│     │     ├─ small_spruce_gray_stained_glass_flask.json
│     │     ├─ small_spruce_green_stained_glass_flask.json
│     │     ├─ small_spruce_light_blue_stained_glass_flask.json
│     │     ├─ small_spruce_light_gray_stained_glass_flask.json
│     │     ├─ small_spruce_lime_stained_glass_flask.json
│     │     ├─ small_spruce_magenta_stained_glass_flask.json
│     │     ├─ small_spruce_orange_stained_glass_flask.json
│     │     ├─ small_spruce_pink_stained_glass_flask.json
│     │     ├─ small_spruce_purple_stained_glass_flask.json
│     │     ├─ small_spruce_red_stained_glass_flask.json
│     │     ├─ small_spruce_tinted_glass_flask.json
│     │     ├─ small_spruce_white_stained_glass_flask.json
│     │     ├─ small_spruce_yellow_stained_glass_flask.json
│     │     ├─ small_warped_black_stained_glass_flask.json
│     │     ├─ small_warped_blue_stained_glass_flask.json
│     │     ├─ small_warped_brown_stained_glass_flask.json
│     │     ├─ small_warped_cyan_stained_glass_flask.json
│     │     ├─ small_warped_glass_flask.json
│     │     ├─ small_warped_gray_stained_glass_flask.json
│     │     ├─ small_warped_green_stained_glass_flask.json
│     │     ├─ small_warped_light_blue_stained_glass_flask.json
│     │     ├─ small_warped_light_gray_stained_glass_flask.json
│     │     ├─ small_warped_lime_stained_glass_flask.json
│     │     ├─ small_warped_magenta_stained_glass_flask.json
│     │     ├─ small_warped_orange_stained_glass_flask.json
│     │     ├─ small_warped_pink_stained_glass_flask.json
│     │     ├─ small_warped_purple_stained_glass_flask.json
│     │     ├─ small_warped_red_stained_glass_flask.json
│     │     ├─ small_warped_tinted_glass_flask.json
│     │     ├─ small_warped_white_stained_glass_flask.json
│     │     ├─ small_warped_yellow_stained_glass_flask.json
│     │     ├─ spruce_copper_barrel.json
│     │     ├─ spruce_copper_exposed_barrel.json
│     │     ├─ spruce_copper_oxidized_barrel.json
│     │     ├─ spruce_copper_weathered_barrel.json
│     │     ├─ spruce_gold_barrel.json
│     │     ├─ spruce_iron_barrel.json
│     │     ├─ spruce_netherite_barrel.json
│     │     ├─ warped_copper_barrel.json
│     │     ├─ warped_copper_exposed_barrel.json
│     │     ├─ warped_copper_oxidized_barrel.json
│     │     ├─ warped_copper_weathered_barrel.json
│     │     ├─ warped_gold_barrel.json
│     │     ├─ warped_iron_barrel.json
│     │     └─ warped_netherite_barrel.json
│     └─ textures
│        ├─ block
│        │  ├─ acacia_copper_barrel_block.png
│        │  ├─ acacia_copper_exposed_barrel_block.png
│        │  ├─ acacia_copper_oxidized_barrel_block.png
│        │  ├─ acacia_copper_weathered_barrel_block.png
│        │  ├─ acacia_gold_barrel_block.png
│        │  ├─ acacia_iron_barrel_block.png
│        │  ├─ acacia_netherite_barrel_block.png
│        │  ├─ bamboo_copper_barrel_block.png
│        │  ├─ bamboo_copper_exposed_barrel_block.png
│        │  ├─ bamboo_copper_oxidized_barrel_block.png
│        │  ├─ bamboo_copper_weathered_barrel_block.png
│        │  ├─ bamboo_gold_barrel_block.png
│        │  ├─ bamboo_iron_barrel_block.png
│        │  ├─ bamboo_netherite_barrel_block.png
│        │  ├─ birch_copper_barrel_block.png
│        │  ├─ birch_copper_exposed_barrel_block.png
│        │  ├─ birch_copper_oxidized_barrel_block.png
│        │  ├─ birch_copper_weathered_barrel_block.png
│        │  ├─ birch_gold_barrel_block.png
│        │  ├─ birch_iron_barrel_block.png
│        │  ├─ birch_netherite_barrel_block.png
│        │  ├─ cherry_copper_barrel_block.png
│        │  ├─ cherry_copper_exposed_barrel_block.png
│        │  ├─ cherry_copper_oxidized_barrel_block.png
│        │  ├─ cherry_copper_weathered_barrel_block.png
│        │  ├─ cherry_gold_barrel_block.png
│        │  ├─ cherry_iron_barrel_block.png
│        │  ├─ cherry_netherite_barrel_block.png
│        │  ├─ copper_exposed_keg_block.png
│        │  ├─ copper_keg_block.png
│        │  ├─ copper_oxidized_keg_block.png
│        │  ├─ copper_weathered_keg_block.png
│        │  ├─ crimson_copper_barrel_block.png
│        │  ├─ crimson_copper_exposed_barrel_block.png
│        │  ├─ crimson_copper_oxidized_barrel_block.png
│        │  ├─ crimson_copper_weathered_barrel_block.png
│        │  ├─ crimson_gold_barrel_block.png
│        │  ├─ crimson_iron_barrel_block.png
│        │  ├─ crimson_netherite_barrel_block.png
│        │  ├─ dark_oak_copper_barrel_block.png
│        │  ├─ dark_oak_copper_exposed_barrel_block.png
│        │  ├─ dark_oak_copper_oxidized_barrel_block.png
│        │  ├─ dark_oak_copper_weathered_barrel_block.png
│        │  ├─ dark_oak_gold_barrel_block.png
│        │  ├─ dark_oak_iron_barrel_block.png
│        │  ├─ dark_oak_netherite_barrel_block.png
│        │  ├─ gold_keg_block.png
│        │  ├─ iron_keg_block.png
│        │  ├─ jungle_copper_barrel_block.png
│        │  ├─ jungle_copper_exposed_barrel_block.png
│        │  ├─ jungle_copper_oxidized_barrel_block.png
│        │  ├─ jungle_copper_weathered_barrel_block.png
│        │  ├─ jungle_gold_barrel_block.png
│        │  ├─ jungle_iron_barrel_block.png
│        │  ├─ jungle_netherite_barrel_block.png
│        │  ├─ mangrove_copper_barrel_block.png
│        │  ├─ mangrove_copper_exposed_barrel_block.png
│        │  ├─ mangrove_copper_oxidized_barrel_block.png
│        │  ├─ mangrove_copper_weathered_barrel_block.png
│        │  ├─ mangrove_gold_barrel_block.png
│        │  ├─ mangrove_iron_barrel_block.png
│        │  ├─ mangrove_netherite_barrel_block.png
│        │  ├─ netherite_keg_block.png
│        │  ├─ oak_copper_barrel_block.png
│        │  ├─ oak_copper_exposed_barrel_block.png
│        │  ├─ oak_copper_oxidized_barrel_block.png
│        │  ├─ oak_copper_weathered_barrel_block.png
│        │  ├─ oak_gold_barrel_block.png
│        │  ├─ oak_iron_barrel_block.png
│        │  ├─ oak_netherite_barrel_block.png
│        │  ├─ pale_oak_copper_barrel_block.png
│        │  ├─ pale_oak_copper_exposed_barrel_block.png
│        │  ├─ pale_oak_copper_oxidized_barrel_block.png
│        │  ├─ pale_oak_copper_weathered_barrel_block.png
│        │  ├─ pale_oak_gold_barrel_block.png
│        │  ├─ pale_oak_iron_barrel_block.png
│        │  ├─ pale_oak_netherite_barrel_block.png
│        │  ├─ spruce_copper_barrel_block.png
│        │  ├─ spruce_copper_exposed_barrel_block.png
│        │  ├─ spruce_copper_oxidized_barrel_block.png
│        │  ├─ spruce_copper_weathered_barrel_block.png
│        │  ├─ spruce_gold_barrel_block.png
│        │  ├─ spruce_iron_barrel_block.png
│        │  ├─ spruce_netherite_barrel_block.png
│        │  ├─ warped_copper_barrel_block.png
│        │  ├─ warped_copper_exposed_barrel_block.png
│        │  ├─ warped_copper_oxidized_barrel_block.png
│        │  ├─ warped_copper_weathered_barrel_block.png
│        │  ├─ warped_gold_barrel_block.png
│        │  ├─ warped_iron_barrel_block.png
│        │  └─ warped_netherite_barrel_block.png
│        └─ item
│           ├─ acacia_copper_barrel.png
│           ├─ acacia_copper_exposed_barrel.png
│           ├─ acacia_copper_oxidized_barrel.png
│           ├─ acacia_copper_weathered_barrel.png
│           ├─ acacia_gold_barrel.png
│           ├─ acacia_iron_barrel.png
│           ├─ acacia_netherite_barrel.png
│           ├─ bamboo_copper_barrel.png
│           ├─ bamboo_copper_exposed_barrel.png
│           ├─ bamboo_copper_oxidized_barrel.png
│           ├─ bamboo_copper_weathered_barrel.png
│           ├─ bamboo_gold_barrel.png
│           ├─ bamboo_iron_barrel.png
│           ├─ bamboo_netherite_barrel.png
│           ├─ big_acacia_black_stained_glass_flask.png
│           ├─ big_acacia_blue_stained_glass_flask.png
│           ├─ big_acacia_brown_stained_glass_flask.png
│           ├─ big_acacia_cyan_stained_glass_flask.png
│           ├─ big_acacia_glass_flask.png
│           ├─ big_acacia_gray_stained_glass_flask.png
│           ├─ big_acacia_green_stained_glass_flask.png
│           ├─ big_acacia_light_blue_stained_glass_flask.png
│           ├─ big_acacia_light_gray_stained_glass_flask.png
│           ├─ big_acacia_lime_stained_glass_flask.png
│           ├─ big_acacia_magenta_stained_glass_flask.png
│           ├─ big_acacia_orange_stained_glass_flask.png
│           ├─ big_acacia_pink_stained_glass_flask.png
│           ├─ big_acacia_purple_stained_glass_flask.png
│           ├─ big_acacia_red_stained_glass_flask.png
│           ├─ big_acacia_tinted_glass_flask.png
│           ├─ big_acacia_white_stained_glass_flask.png
│           ├─ big_acacia_yellow_stained_glass_flask.png
│           ├─ big_bamboo_black_stained_glass_flask.png
│           ├─ big_bamboo_blue_stained_glass_flask.png
│           ├─ big_bamboo_brown_stained_glass_flask.png
│           ├─ big_bamboo_cyan_stained_glass_flask.png
│           ├─ big_bamboo_glass_flask.png
│           ├─ big_bamboo_gray_stained_glass_flask.png
│           ├─ big_bamboo_green_stained_glass_flask.png
│           ├─ big_bamboo_light_blue_stained_glass_flask.png
│           ├─ big_bamboo_light_gray_stained_glass_flask.png
│           ├─ big_bamboo_lime_stained_glass_flask.png
│           ├─ big_bamboo_magenta_stained_glass_flask.png
│           ├─ big_bamboo_orange_stained_glass_flask.png
│           ├─ big_bamboo_pink_stained_glass_flask.png
│           ├─ big_bamboo_purple_stained_glass_flask.png
│           ├─ big_bamboo_red_stained_glass_flask.png
│           ├─ big_bamboo_tinted_glass_flask.png
│           ├─ big_bamboo_white_stained_glass_flask.png
│           ├─ big_bamboo_yellow_stained_glass_flask.png
│           ├─ big_birch_black_stained_glass_flask.png
│           ├─ big_birch_blue_stained_glass_flask.png
│           ├─ big_birch_brown_stained_glass_flask.png
│           ├─ big_birch_cyan_stained_glass_flask.png
│           ├─ big_birch_glass_flask.png
│           ├─ big_birch_gray_stained_glass_flask.png
│           ├─ big_birch_green_stained_glass_flask.png
│           ├─ big_birch_light_blue_stained_glass_flask.png
│           ├─ big_birch_light_gray_stained_glass_flask.png
│           ├─ big_birch_lime_stained_glass_flask.png
│           ├─ big_birch_magenta_stained_glass_flask.png
│           ├─ big_birch_orange_stained_glass_flask.png
│           ├─ big_birch_pink_stained_glass_flask.png
│           ├─ big_birch_purple_stained_glass_flask.png
│           ├─ big_birch_red_stained_glass_flask.png
│           ├─ big_birch_tinted_glass_flask.png
│           ├─ big_birch_white_stained_glass_flask.png
│           ├─ big_birch_yellow_stained_glass_flask.png
│           ├─ big_cherry_black_stained_glass_flask.png
│           ├─ big_cherry_blue_stained_glass_flask.png
│           ├─ big_cherry_brown_stained_glass_flask.png
│           ├─ big_cherry_cyan_stained_glass_flask.png
│           ├─ big_cherry_glass_flask.png
│           ├─ big_cherry_gray_stained_glass_flask.png
│           ├─ big_cherry_green_stained_glass_flask.png
│           ├─ big_cherry_light_blue_stained_glass_flask.png
│           ├─ big_cherry_light_gray_stained_glass_flask.png
│           ├─ big_cherry_lime_stained_glass_flask.png
│           ├─ big_cherry_magenta_stained_glass_flask.png
│           ├─ big_cherry_orange_stained_glass_flask.png
│           ├─ big_cherry_pink_stained_glass_flask.png
│           ├─ big_cherry_purple_stained_glass_flask.png
│           ├─ big_cherry_red_stained_glass_flask.png
│           ├─ big_cherry_tinted_glass_flask.png
│           ├─ big_cherry_white_stained_glass_flask.png
│           ├─ big_cherry_yellow_stained_glass_flask.png
│           ├─ big_crimson_black_stained_glass_flask.png
│           ├─ big_crimson_blue_stained_glass_flask.png
│           ├─ big_crimson_brown_stained_glass_flask.png
│           ├─ big_crimson_cyan_stained_glass_flask.png
│           ├─ big_crimson_glass_flask.png
│           ├─ big_crimson_gray_stained_glass_flask.png
│           ├─ big_crimson_green_stained_glass_flask.png
│           ├─ big_crimson_light_blue_stained_glass_flask.png
│           ├─ big_crimson_light_gray_stained_glass_flask.png
│           ├─ big_crimson_lime_stained_glass_flask.png
│           ├─ big_crimson_magenta_stained_glass_flask.png
│           ├─ big_crimson_orange_stained_glass_flask.png
│           ├─ big_crimson_pink_stained_glass_flask.png
│           ├─ big_crimson_purple_stained_glass_flask.png
│           ├─ big_crimson_red_stained_glass_flask.png
│           ├─ big_crimson_tinted_glass_flask.png
│           ├─ big_crimson_white_stained_glass_flask.png
│           ├─ big_crimson_yellow_stained_glass_flask.png
│           ├─ big_dark_oak_black_stained_glass_flask.png
│           ├─ big_dark_oak_blue_stained_glass_flask.png
│           ├─ big_dark_oak_brown_stained_glass_flask.png
│           ├─ big_dark_oak_cyan_stained_glass_flask.png
│           ├─ big_dark_oak_glass_flask.png
│           ├─ big_dark_oak_gray_stained_glass_flask.png
│           ├─ big_dark_oak_green_stained_glass_flask.png
│           ├─ big_dark_oak_light_blue_stained_glass_flask.png
│           ├─ big_dark_oak_light_gray_stained_glass_flask.png
│           ├─ big_dark_oak_lime_stained_glass_flask.png
│           ├─ big_dark_oak_magenta_stained_glass_flask.png
│           ├─ big_dark_oak_orange_stained_glass_flask.png
│           ├─ big_dark_oak_pink_stained_glass_flask.png
│           ├─ big_dark_oak_purple_stained_glass_flask.png
│           ├─ big_dark_oak_red_stained_glass_flask.png
│           ├─ big_dark_oak_tinted_glass_flask.png
│           ├─ big_dark_oak_white_stained_glass_flask.png
│           ├─ big_dark_oak_yellow_stained_glass_flask.png
│           ├─ big_jungle_black_stained_glass_flask.png
│           ├─ big_jungle_blue_stained_glass_flask.png
│           ├─ big_jungle_brown_stained_glass_flask.png
│           ├─ big_jungle_cyan_stained_glass_flask.png
│           ├─ big_jungle_glass_flask.png
│           ├─ big_jungle_gray_stained_glass_flask.png
│           ├─ big_jungle_green_stained_glass_flask.png
│           ├─ big_jungle_light_blue_stained_glass_flask.png
│           ├─ big_jungle_light_gray_stained_glass_flask.png
│           ├─ big_jungle_lime_stained_glass_flask.png
│           ├─ big_jungle_magenta_stained_glass_flask.png
│           ├─ big_jungle_orange_stained_glass_flask.png
│           ├─ big_jungle_pink_stained_glass_flask.png
│           ├─ big_jungle_purple_stained_glass_flask.png
│           ├─ big_jungle_red_stained_glass_flask.png
│           ├─ big_jungle_tinted_glass_flask.png
│           ├─ big_jungle_white_stained_glass_flask.png
│           ├─ big_jungle_yellow_stained_glass_flask.png
│           ├─ big_mangrove_black_stained_glass_flask.png
│           ├─ big_mangrove_blue_stained_glass_flask.png
│           ├─ big_mangrove_brown_stained_glass_flask.png
│           ├─ big_mangrove_cyan_stained_glass_flask.png
│           ├─ big_mangrove_glass_flask.png
│           ├─ big_mangrove_gray_stained_glass_flask.png
│           ├─ big_mangrove_green_stained_glass_flask.png
│           ├─ big_mangrove_light_blue_stained_glass_flask.png
│           ├─ big_mangrove_light_gray_stained_glass_flask.png
│           ├─ big_mangrove_lime_stained_glass_flask.png
│           ├─ big_mangrove_magenta_stained_glass_flask.png
│           ├─ big_mangrove_orange_stained_glass_flask.png
│           ├─ big_mangrove_pink_stained_glass_flask.png
│           ├─ big_mangrove_purple_stained_glass_flask.png
│           ├─ big_mangrove_red_stained_glass_flask.png
│           ├─ big_mangrove_tinted_glass_flask.png
│           ├─ big_mangrove_white_stained_glass_flask.png
│           ├─ big_mangrove_yellow_stained_glass_flask.png
│           ├─ big_oak_black_stained_glass_flask.png
│           ├─ big_oak_blue_stained_glass_flask.png
│           ├─ big_oak_brown_stained_glass_flask.png
│           ├─ big_oak_cyan_stained_glass_flask.png
│           ├─ big_oak_glass_flask.png
│           ├─ big_oak_gray_stained_glass_flask.png
│           ├─ big_oak_green_stained_glass_flask.png
│           ├─ big_oak_light_blue_stained_glass_flask.png
│           ├─ big_oak_light_gray_stained_glass_flask.png
│           ├─ big_oak_lime_stained_glass_flask.png
│           ├─ big_oak_magenta_stained_glass_flask.png
│           ├─ big_oak_orange_stained_glass_flask.png
│           ├─ big_oak_pink_stained_glass_flask.png
│           ├─ big_oak_purple_stained_glass_flask.png
│           ├─ big_oak_red_stained_glass_flask.png
│           ├─ big_oak_tinted_glass_flask.png
│           ├─ big_oak_white_stained_glass_flask.png
│           ├─ big_oak_yellow_stained_glass_flask.png
│           ├─ big_pale_oak_black_stained_glass_flask.png
│           ├─ big_pale_oak_blue_stained_glass_flask.png
│           ├─ big_pale_oak_brown_stained_glass_flask.png
│           ├─ big_pale_oak_cyan_stained_glass_flask.png
│           ├─ big_pale_oak_glass_flask.png
│           ├─ big_pale_oak_gray_stained_glass_flask.png
│           ├─ big_pale_oak_green_stained_glass_flask.png
│           ├─ big_pale_oak_light_blue_stained_glass_flask.png
│           ├─ big_pale_oak_light_gray_stained_glass_flask.png
│           ├─ big_pale_oak_lime_stained_glass_flask.png
│           ├─ big_pale_oak_magenta_stained_glass_flask.png
│           ├─ big_pale_oak_orange_stained_glass_flask.png
│           ├─ big_pale_oak_pink_stained_glass_flask.png
│           ├─ big_pale_oak_purple_stained_glass_flask.png
│           ├─ big_pale_oak_red_stained_glass_flask.png
│           ├─ big_pale_oak_tinted_glass_flask.png
│           ├─ big_pale_oak_white_stained_glass_flask.png
│           ├─ big_pale_oak_yellow_stained_glass_flask.png
│           ├─ big_spruce_black_stained_glass_flask.png
│           ├─ big_spruce_blue_stained_glass_flask.png
│           ├─ big_spruce_brown_stained_glass_flask.png
│           ├─ big_spruce_cyan_stained_glass_flask.png
│           ├─ big_spruce_glass_flask.png
│           ├─ big_spruce_gray_stained_glass_flask.png
│           ├─ big_spruce_green_stained_glass_flask.png
│           ├─ big_spruce_light_blue_stained_glass_flask.png
│           ├─ big_spruce_light_gray_stained_glass_flask.png
│           ├─ big_spruce_lime_stained_glass_flask.png
│           ├─ big_spruce_magenta_stained_glass_flask.png
│           ├─ big_spruce_orange_stained_glass_flask.png
│           ├─ big_spruce_pink_stained_glass_flask.png
│           ├─ big_spruce_purple_stained_glass_flask.png
│           ├─ big_spruce_red_stained_glass_flask.png
│           ├─ big_spruce_tinted_glass_flask.png
│           ├─ big_spruce_white_stained_glass_flask.png
│           ├─ big_spruce_yellow_stained_glass_flask.png
│           ├─ big_warped_black_stained_glass_flask.png
│           ├─ big_warped_blue_stained_glass_flask.png
│           ├─ big_warped_brown_stained_glass_flask.png
│           ├─ big_warped_cyan_stained_glass_flask.png
│           ├─ big_warped_glass_flask.png
│           ├─ big_warped_gray_stained_glass_flask.png
│           ├─ big_warped_green_stained_glass_flask.png
│           ├─ big_warped_light_blue_stained_glass_flask.png
│           ├─ big_warped_light_gray_stained_glass_flask.png
│           ├─ big_warped_lime_stained_glass_flask.png
│           ├─ big_warped_magenta_stained_glass_flask.png
│           ├─ big_warped_orange_stained_glass_flask.png
│           ├─ big_warped_pink_stained_glass_flask.png
│           ├─ big_warped_purple_stained_glass_flask.png
│           ├─ big_warped_red_stained_glass_flask.png
│           ├─ big_warped_tinted_glass_flask.png
│           ├─ big_warped_white_stained_glass_flask.png
│           ├─ big_warped_yellow_stained_glass_flask.png
│           ├─ birch_copper_barrel.png
│           ├─ birch_copper_exposed_barrel.png
│           ├─ birch_copper_oxidized_barrel.png
│           ├─ birch_copper_weathered_barrel.png
│           ├─ birch_gold_barrel.png
│           ├─ birch_iron_barrel.png
│           ├─ birch_netherite_barrel.png
│           ├─ cherry_copper_barrel.png
│           ├─ cherry_copper_exposed_barrel.png
│           ├─ cherry_copper_oxidized_barrel.png
│           ├─ cherry_copper_weathered_barrel.png
│           ├─ cherry_gold_barrel.png
│           ├─ cherry_iron_barrel.png
│           ├─ cherry_netherite_barrel.png
│           ├─ copper_exposed_keg.png
│           ├─ copper_keg.png
│           ├─ copper_oxidized_keg.png
│           ├─ copper_weathered_keg.png
│           ├─ crimson_copper_barrel.png
│           ├─ crimson_copper_exposed_barrel.png
│           ├─ crimson_copper_oxidized_barrel.png
│           ├─ crimson_copper_weathered_barrel.png
│           ├─ crimson_gold_barrel.png
│           ├─ crimson_iron_barrel.png
│           ├─ crimson_netherite_barrel.png
│           ├─ dark_oak_copper_barrel.png
│           ├─ dark_oak_copper_exposed_barrel.png
│           ├─ dark_oak_copper_oxidized_barrel.png
│           ├─ dark_oak_copper_weathered_barrel.png
│           ├─ dark_oak_gold_barrel.png
│           ├─ dark_oak_iron_barrel.png
│           ├─ dark_oak_netherite_barrel.png
│           ├─ gold_keg.png
│           ├─ iron_keg.png
│           ├─ jungle_copper_barrel.png
│           ├─ jungle_copper_exposed_barrel.png
│           ├─ jungle_copper_oxidized_barrel.png
│           ├─ jungle_copper_weathered_barrel.png
│           ├─ jungle_gold_barrel.png
│           ├─ jungle_iron_barrel.png
│           ├─ jungle_netherite_barrel.png
│           ├─ mangrove_copper_barrel.png
│           ├─ mangrove_copper_exposed_barrel.png
│           ├─ mangrove_copper_oxidized_barrel.png
│           ├─ mangrove_copper_weathered_barrel.png
│           ├─ mangrove_gold_barrel.png
│           ├─ mangrove_iron_barrel.png
│           ├─ mangrove_netherite_barrel.png
│           ├─ medium_acacia_black_stained_glass_flask.png
│           ├─ medium_acacia_blue_stained_glass_flask.png
│           ├─ medium_acacia_brown_stained_glass_flask.png
│           ├─ medium_acacia_cyan_stained_glass_flask.png
│           ├─ medium_acacia_glass_flask.png
│           ├─ medium_acacia_gray_stained_glass_flask.png
│           ├─ medium_acacia_green_stained_glass_flask.png
│           ├─ medium_acacia_light_blue_stained_glass_flask.png
│           ├─ medium_acacia_light_gray_stained_glass_flask.png
│           ├─ medium_acacia_lime_stained_glass_flask.png
│           ├─ medium_acacia_magenta_stained_glass_flask.png
│           ├─ medium_acacia_orange_stained_glass_flask.png
│           ├─ medium_acacia_pink_stained_glass_flask.png
│           ├─ medium_acacia_purple_stained_glass_flask.png
│           ├─ medium_acacia_red_stained_glass_flask.png
│           ├─ medium_acacia_tinted_glass_flask.png
│           ├─ medium_acacia_white_stained_glass_flask.png
│           ├─ medium_acacia_yellow_stained_glass_flask.png
│           ├─ medium_bamboo_black_stained_glass_flask.png
│           ├─ medium_bamboo_blue_stained_glass_flask.png
│           ├─ medium_bamboo_brown_stained_glass_flask.png
│           ├─ medium_bamboo_cyan_stained_glass_flask.png
│           ├─ medium_bamboo_glass_flask.png
│           ├─ medium_bamboo_gray_stained_glass_flask.png
│           ├─ medium_bamboo_green_stained_glass_flask.png
│           ├─ medium_bamboo_light_blue_stained_glass_flask.png
│           ├─ medium_bamboo_light_gray_stained_glass_flask.png
│           ├─ medium_bamboo_lime_stained_glass_flask.png
│           ├─ medium_bamboo_magenta_stained_glass_flask.png
│           ├─ medium_bamboo_orange_stained_glass_flask.png
│           ├─ medium_bamboo_pink_stained_glass_flask.png
│           ├─ medium_bamboo_purple_stained_glass_flask.png
│           ├─ medium_bamboo_red_stained_glass_flask.png
│           ├─ medium_bamboo_tinted_glass_flask.png
│           ├─ medium_bamboo_white_stained_glass_flask.png
│           ├─ medium_bamboo_yellow_stained_glass_flask.png
│           ├─ medium_birch_black_stained_glass_flask.png
│           ├─ medium_birch_blue_stained_glass_flask.png
│           ├─ medium_birch_brown_stained_glass_flask.png
│           ├─ medium_birch_cyan_stained_glass_flask.png
│           ├─ medium_birch_glass_flask.png
│           ├─ medium_birch_gray_stained_glass_flask.png
│           ├─ medium_birch_green_stained_glass_flask.png
│           ├─ medium_birch_light_blue_stained_glass_flask.png
│           ├─ medium_birch_light_gray_stained_glass_flask.png
│           ├─ medium_birch_lime_stained_glass_flask.png
│           ├─ medium_birch_magenta_stained_glass_flask.png
│           ├─ medium_birch_orange_stained_glass_flask.png
│           ├─ medium_birch_pink_stained_glass_flask.png
│           ├─ medium_birch_purple_stained_glass_flask.png
│           ├─ medium_birch_red_stained_glass_flask.png
│           ├─ medium_birch_tinted_glass_flask.png
│           ├─ medium_birch_white_stained_glass_flask.png
│           ├─ medium_birch_yellow_stained_glass_flask.png
│           ├─ medium_cherry_black_stained_glass_flask.png
│           ├─ medium_cherry_blue_stained_glass_flask.png
│           ├─ medium_cherry_brown_stained_glass_flask.png
│           ├─ medium_cherry_cyan_stained_glass_flask.png
│           ├─ medium_cherry_glass_flask.png
│           ├─ medium_cherry_gray_stained_glass_flask.png
│           ├─ medium_cherry_green_stained_glass_flask.png
│           ├─ medium_cherry_light_blue_stained_glass_flask.png
│           ├─ medium_cherry_light_gray_stained_glass_flask.png
│           ├─ medium_cherry_lime_stained_glass_flask.png
│           ├─ medium_cherry_magenta_stained_glass_flask.png
│           ├─ medium_cherry_orange_stained_glass_flask.png
│           ├─ medium_cherry_pink_stained_glass_flask.png
│           ├─ medium_cherry_purple_stained_glass_flask.png
│           ├─ medium_cherry_red_stained_glass_flask.png
│           ├─ medium_cherry_tinted_glass_flask.png
│           ├─ medium_cherry_white_stained_glass_flask.png
│           ├─ medium_cherry_yellow_stained_glass_flask.png
│           ├─ medium_crimson_black_stained_glass_flask.png
│           ├─ medium_crimson_blue_stained_glass_flask.png
│           ├─ medium_crimson_brown_stained_glass_flask.png
│           ├─ medium_crimson_cyan_stained_glass_flask.png
│           ├─ medium_crimson_glass_flask.png
│           ├─ medium_crimson_gray_stained_glass_flask.png
│           ├─ medium_crimson_green_stained_glass_flask.png
│           ├─ medium_crimson_light_blue_stained_glass_flask.png
│           ├─ medium_crimson_light_gray_stained_glass_flask.png
│           ├─ medium_crimson_lime_stained_glass_flask.png
│           ├─ medium_crimson_magenta_stained_glass_flask.png
│           ├─ medium_crimson_orange_stained_glass_flask.png
│           ├─ medium_crimson_pink_stained_glass_flask.png
│           ├─ medium_crimson_purple_stained_glass_flask.png
│           ├─ medium_crimson_red_stained_glass_flask.png
│           ├─ medium_crimson_tinted_glass_flask.png
│           ├─ medium_crimson_white_stained_glass_flask.png
│           ├─ medium_crimson_yellow_stained_glass_flask.png
│           ├─ medium_dark_oak_black_stained_glass_flask.png
│           ├─ medium_dark_oak_blue_stained_glass_flask.png
│           ├─ medium_dark_oak_brown_stained_glass_flask.png
│           ├─ medium_dark_oak_cyan_stained_glass_flask.png
│           ├─ medium_dark_oak_glass_flask.png
│           ├─ medium_dark_oak_gray_stained_glass_flask.png
│           ├─ medium_dark_oak_green_stained_glass_flask.png
│           ├─ medium_dark_oak_light_blue_stained_glass_flask.png
│           ├─ medium_dark_oak_light_gray_stained_glass_flask.png
│           ├─ medium_dark_oak_lime_stained_glass_flask.png
│           ├─ medium_dark_oak_magenta_stained_glass_flask.png
│           ├─ medium_dark_oak_orange_stained_glass_flask.png
│           ├─ medium_dark_oak_pink_stained_glass_flask.png
│           ├─ medium_dark_oak_purple_stained_glass_flask.png
│           ├─ medium_dark_oak_red_stained_glass_flask.png
│           ├─ medium_dark_oak_tinted_glass_flask.png
│           ├─ medium_dark_oak_white_stained_glass_flask.png
│           ├─ medium_dark_oak_yellow_stained_glass_flask.png
│           ├─ medium_jungle_black_stained_glass_flask.png
│           ├─ medium_jungle_blue_stained_glass_flask.png
│           ├─ medium_jungle_brown_stained_glass_flask.png
│           ├─ medium_jungle_cyan_stained_glass_flask.png
│           ├─ medium_jungle_glass_flask.png
│           ├─ medium_jungle_gray_stained_glass_flask.png
│           ├─ medium_jungle_green_stained_glass_flask.png
│           ├─ medium_jungle_light_blue_stained_glass_flask.png
│           ├─ medium_jungle_light_gray_stained_glass_flask.png
│           ├─ medium_jungle_lime_stained_glass_flask.png
│           ├─ medium_jungle_magenta_stained_glass_flask.png
│           ├─ medium_jungle_orange_stained_glass_flask.png
│           ├─ medium_jungle_pink_stained_glass_flask.png
│           ├─ medium_jungle_purple_stained_glass_flask.png
│           ├─ medium_jungle_red_stained_glass_flask.png
│           ├─ medium_jungle_tinted_glass_flask.png
│           ├─ medium_jungle_white_stained_glass_flask.png
│           ├─ medium_jungle_yellow_stained_glass_flask.png
│           ├─ medium_mangrove_black_stained_glass_flask.png
│           ├─ medium_mangrove_blue_stained_glass_flask.png
│           ├─ medium_mangrove_brown_stained_glass_flask.png
│           ├─ medium_mangrove_cyan_stained_glass_flask.png
│           ├─ medium_mangrove_glass_flask.png
│           ├─ medium_mangrove_gray_stained_glass_flask.png
│           ├─ medium_mangrove_green_stained_glass_flask.png
│           ├─ medium_mangrove_light_blue_stained_glass_flask.png
│           ├─ medium_mangrove_light_gray_stained_glass_flask.png
│           ├─ medium_mangrove_lime_stained_glass_flask.png
│           ├─ medium_mangrove_magenta_stained_glass_flask.png
│           ├─ medium_mangrove_orange_stained_glass_flask.png
│           ├─ medium_mangrove_pink_stained_glass_flask.png
│           ├─ medium_mangrove_purple_stained_glass_flask.png
│           ├─ medium_mangrove_red_stained_glass_flask.png
│           ├─ medium_mangrove_tinted_glass_flask.png
│           ├─ medium_mangrove_white_stained_glass_flask.png
│           ├─ medium_mangrove_yellow_stained_glass_flask.png
│           ├─ medium_oak_black_stained_glass_flask.png
│           ├─ medium_oak_blue_stained_glass_flask.png
│           ├─ medium_oak_brown_stained_glass_flask.png
│           ├─ medium_oak_cyan_stained_glass_flask.png
│           ├─ medium_oak_glass_flask.png
│           ├─ medium_oak_gray_stained_glass_flask.png
│           ├─ medium_oak_green_stained_glass_flask.png
│           ├─ medium_oak_light_blue_stained_glass_flask.png
│           ├─ medium_oak_light_gray_stained_glass_flask.png
│           ├─ medium_oak_lime_stained_glass_flask.png
│           ├─ medium_oak_magenta_stained_glass_flask.png
│           ├─ medium_oak_orange_stained_glass_flask.png
│           ├─ medium_oak_pink_stained_glass_flask.png
│           ├─ medium_oak_purple_stained_glass_flask.png
│           ├─ medium_oak_red_stained_glass_flask.png
│           ├─ medium_oak_tinted_glass_flask.png
│           ├─ medium_oak_white_stained_glass_flask.png
│           ├─ medium_oak_yellow_stained_glass_flask.png
│           ├─ medium_pale_oak_black_stained_glass_flask.png
│           ├─ medium_pale_oak_blue_stained_glass_flask.png
│           ├─ medium_pale_oak_brown_stained_glass_flask.png
│           ├─ medium_pale_oak_cyan_stained_glass_flask.png
│           ├─ medium_pale_oak_glass_flask.png
│           ├─ medium_pale_oak_gray_stained_glass_flask.png
│           ├─ medium_pale_oak_green_stained_glass_flask.png
│           ├─ medium_pale_oak_light_blue_stained_glass_flask.png
│           ├─ medium_pale_oak_light_gray_stained_glass_flask.png
│           ├─ medium_pale_oak_lime_stained_glass_flask.png
│           ├─ medium_pale_oak_magenta_stained_glass_flask.png
│           ├─ medium_pale_oak_orange_stained_glass_flask.png
│           ├─ medium_pale_oak_pink_stained_glass_flask.png
│           ├─ medium_pale_oak_purple_stained_glass_flask.png
│           ├─ medium_pale_oak_red_stained_glass_flask.png
│           ├─ medium_pale_oak_tinted_glass_flask.png
│           ├─ medium_pale_oak_white_stained_glass_flask.png
│           ├─ medium_pale_oak_yellow_stained_glass_flask.png
│           ├─ medium_spruce_black_stained_glass_flask.png
│           ├─ medium_spruce_blue_stained_glass_flask.png
│           ├─ medium_spruce_brown_stained_glass_flask.png
│           ├─ medium_spruce_cyan_stained_glass_flask.png
│           ├─ medium_spruce_glass_flask.png
│           ├─ medium_spruce_gray_stained_glass_flask.png
│           ├─ medium_spruce_green_stained_glass_flask.png
│           ├─ medium_spruce_light_blue_stained_glass_flask.png
│           ├─ medium_spruce_light_gray_stained_glass_flask.png
│           ├─ medium_spruce_lime_stained_glass_flask.png
│           ├─ medium_spruce_magenta_stained_glass_flask.png
│           ├─ medium_spruce_orange_stained_glass_flask.png
│           ├─ medium_spruce_pink_stained_glass_flask.png
│           ├─ medium_spruce_purple_stained_glass_flask.png
│           ├─ medium_spruce_red_stained_glass_flask.png
│           ├─ medium_spruce_tinted_glass_flask.png
│           ├─ medium_spruce_white_stained_glass_flask.png
│           ├─ medium_spruce_yellow_stained_glass_flask.png
│           ├─ medium_warped_black_stained_glass_flask.png
│           ├─ medium_warped_blue_stained_glass_flask.png
│           ├─ medium_warped_brown_stained_glass_flask.png
│           ├─ medium_warped_cyan_stained_glass_flask.png
│           ├─ medium_warped_glass_flask.png
│           ├─ medium_warped_gray_stained_glass_flask.png
│           ├─ medium_warped_green_stained_glass_flask.png
│           ├─ medium_warped_light_blue_stained_glass_flask.png
│           ├─ medium_warped_light_gray_stained_glass_flask.png
│           ├─ medium_warped_lime_stained_glass_flask.png
│           ├─ medium_warped_magenta_stained_glass_flask.png
│           ├─ medium_warped_orange_stained_glass_flask.png
│           ├─ medium_warped_pink_stained_glass_flask.png
│           ├─ medium_warped_purple_stained_glass_flask.png
│           ├─ medium_warped_red_stained_glass_flask.png
│           ├─ medium_warped_tinted_glass_flask.png
│           ├─ medium_warped_white_stained_glass_flask.png
│           ├─ medium_warped_yellow_stained_glass_flask.png
│           ├─ netherite_keg.png
│           ├─ oak_copper_barrel.png
│           ├─ oak_copper_exposed_barrel.png
│           ├─ oak_copper_oxidized_barrel.png
│           ├─ oak_copper_weathered_barrel.png
│           ├─ oak_gold_barrel.png
│           ├─ oak_iron_barrel.png
│           ├─ oak_netherite_barrel.png
│           ├─ pale_oak_copper_barrel.png
│           ├─ pale_oak_copper_exposed_barrel.png
│           ├─ pale_oak_copper_oxidized_barrel.png
│           ├─ pale_oak_copper_weathered_barrel.png
│           ├─ pale_oak_gold_barrel.png
│           ├─ pale_oak_iron_barrel.png
│           ├─ pale_oak_netherite_barrel.png
│           ├─ small_acacia_black_stained_glass_flask.png
│           ├─ small_acacia_blue_stained_glass_flask.png
│           ├─ small_acacia_brown_stained_glass_flask.png
│           ├─ small_acacia_cyan_stained_glass_flask.png
│           ├─ small_acacia_glass_flask.png
│           ├─ small_acacia_gray_stained_glass_flask.png
│           ├─ small_acacia_green_stained_glass_flask.png
│           ├─ small_acacia_light_blue_stained_glass_flask.png
│           ├─ small_acacia_light_gray_stained_glass_flask.png
│           ├─ small_acacia_lime_stained_glass_flask.png
│           ├─ small_acacia_magenta_stained_glass_flask.png
│           ├─ small_acacia_orange_stained_glass_flask.png
│           ├─ small_acacia_pink_stained_glass_flask.png
│           ├─ small_acacia_purple_stained_glass_flask.png
│           ├─ small_acacia_red_stained_glass_flask.png
│           ├─ small_acacia_tinted_glass_flask.png
│           ├─ small_acacia_white_stained_glass_flask.png
│           ├─ small_acacia_yellow_stained_glass_flask.png
│           ├─ small_bamboo_black_stained_glass_flask.png
│           ├─ small_bamboo_blue_stained_glass_flask.png
│           ├─ small_bamboo_brown_stained_glass_flask.png
│           ├─ small_bamboo_cyan_stained_glass_flask.png
│           ├─ small_bamboo_glass_flask.png
│           ├─ small_bamboo_gray_stained_glass_flask.png
│           ├─ small_bamboo_green_stained_glass_flask.png
│           ├─ small_bamboo_light_blue_stained_glass_flask.png
│           ├─ small_bamboo_light_gray_stained_glass_flask.png
│           ├─ small_bamboo_lime_stained_glass_flask.png
│           ├─ small_bamboo_magenta_stained_glass_flask.png
│           ├─ small_bamboo_orange_stained_glass_flask.png
│           ├─ small_bamboo_pink_stained_glass_flask.png
│           ├─ small_bamboo_purple_stained_glass_flask.png
│           ├─ small_bamboo_red_stained_glass_flask.png
│           ├─ small_bamboo_tinted_glass_flask.png
│           ├─ small_bamboo_white_stained_glass_flask.png
│           ├─ small_bamboo_yellow_stained_glass_flask.png
│           ├─ small_birch_black_stained_glass_flask.png
│           ├─ small_birch_blue_stained_glass_flask.png
│           ├─ small_birch_brown_stained_glass_flask.png
│           ├─ small_birch_cyan_stained_glass_flask.png
│           ├─ small_birch_glass_flask.png
│           ├─ small_birch_gray_stained_glass_flask.png
│           ├─ small_birch_green_stained_glass_flask.png
│           ├─ small_birch_light_blue_stained_glass_flask.png
│           ├─ small_birch_light_gray_stained_glass_flask.png
│           ├─ small_birch_lime_stained_glass_flask.png
│           ├─ small_birch_magenta_stained_glass_flask.png
│           ├─ small_birch_orange_stained_glass_flask.png
│           ├─ small_birch_pink_stained_glass_flask.png
│           ├─ small_birch_purple_stained_glass_flask.png
│           ├─ small_birch_red_stained_glass_flask.png
│           ├─ small_birch_tinted_glass_flask.png
│           ├─ small_birch_white_stained_glass_flask.png
│           ├─ small_birch_yellow_stained_glass_flask.png
│           ├─ small_cherry_black_stained_glass_flask.png
│           ├─ small_cherry_blue_stained_glass_flask.png
│           ├─ small_cherry_brown_stained_glass_flask.png
│           ├─ small_cherry_cyan_stained_glass_flask.png
│           ├─ small_cherry_glass_flask.png
│           ├─ small_cherry_gray_stained_glass_flask.png
│           ├─ small_cherry_green_stained_glass_flask.png
│           ├─ small_cherry_light_blue_stained_glass_flask.png
│           ├─ small_cherry_light_gray_stained_glass_flask.png
│           ├─ small_cherry_lime_stained_glass_flask.png
│           ├─ small_cherry_magenta_stained_glass_flask.png
│           ├─ small_cherry_orange_stained_glass_flask.png
│           ├─ small_cherry_pink_stained_glass_flask.png
│           ├─ small_cherry_purple_stained_glass_flask.png
│           ├─ small_cherry_red_stained_glass_flask.png
│           ├─ small_cherry_tinted_glass_flask.png
│           ├─ small_cherry_white_stained_glass_flask.png
│           ├─ small_cherry_yellow_stained_glass_flask.png
│           ├─ small_crimson_black_stained_glass_flask.png
│           ├─ small_crimson_blue_stained_glass_flask.png
│           ├─ small_crimson_brown_stained_glass_flask.png
│           ├─ small_crimson_cyan_stained_glass_flask.png
│           ├─ small_crimson_glass_flask.png
│           ├─ small_crimson_gray_stained_glass_flask.png
│           ├─ small_crimson_green_stained_glass_flask.png
│           ├─ small_crimson_light_blue_stained_glass_flask.png
│           ├─ small_crimson_light_gray_stained_glass_flask.png
│           ├─ small_crimson_lime_stained_glass_flask.png
│           ├─ small_crimson_magenta_stained_glass_flask.png
│           ├─ small_crimson_orange_stained_glass_flask.png
│           ├─ small_crimson_pink_stained_glass_flask.png
│           ├─ small_crimson_purple_stained_glass_flask.png
│           ├─ small_crimson_red_stained_glass_flask.png
│           ├─ small_crimson_tinted_glass_flask.png
│           ├─ small_crimson_white_stained_glass_flask.png
│           ├─ small_crimson_yellow_stained_glass_flask.png
│           ├─ small_dark_oak_black_stained_glass_flask.png
│           ├─ small_dark_oak_blue_stained_glass_flask.png
│           ├─ small_dark_oak_brown_stained_glass_flask.png
│           ├─ small_dark_oak_cyan_stained_glass_flask.png
│           ├─ small_dark_oak_glass_flask.png
│           ├─ small_dark_oak_gray_stained_glass_flask.png
│           ├─ small_dark_oak_green_stained_glass_flask.png
│           ├─ small_dark_oak_light_blue_stained_glass_flask.png
│           ├─ small_dark_oak_light_gray_stained_glass_flask.png
│           ├─ small_dark_oak_lime_stained_glass_flask.png
│           ├─ small_dark_oak_magenta_stained_glass_flask.png
│           ├─ small_dark_oak_orange_stained_glass_flask.png
│           ├─ small_dark_oak_pink_stained_glass_flask.png
│           ├─ small_dark_oak_purple_stained_glass_flask.png
│           ├─ small_dark_oak_red_stained_glass_flask.png
│           ├─ small_dark_oak_tinted_glass_flask.png
│           ├─ small_dark_oak_white_stained_glass_flask.png
│           ├─ small_dark_oak_yellow_stained_glass_flask.png
│           ├─ small_jungle_black_stained_glass_flask.png
│           ├─ small_jungle_blue_stained_glass_flask.png
│           ├─ small_jungle_brown_stained_glass_flask.png
│           ├─ small_jungle_cyan_stained_glass_flask.png
│           ├─ small_jungle_glass_flask.png
│           ├─ small_jungle_gray_stained_glass_flask.png
│           ├─ small_jungle_green_stained_glass_flask.png
│           ├─ small_jungle_light_blue_stained_glass_flask.png
│           ├─ small_jungle_light_gray_stained_glass_flask.png
│           ├─ small_jungle_lime_stained_glass_flask.png
│           ├─ small_jungle_magenta_stained_glass_flask.png
│           ├─ small_jungle_orange_stained_glass_flask.png
│           ├─ small_jungle_pink_stained_glass_flask.png
│           ├─ small_jungle_purple_stained_glass_flask.png
│           ├─ small_jungle_red_stained_glass_flask.png
│           ├─ small_jungle_tinted_glass_flask.png
│           ├─ small_jungle_white_stained_glass_flask.png
│           ├─ small_jungle_yellow_stained_glass_flask.png
│           ├─ small_mangrove_black_stained_glass_flask.png
│           ├─ small_mangrove_blue_stained_glass_flask.png
│           ├─ small_mangrove_brown_stained_glass_flask.png
│           ├─ small_mangrove_cyan_stained_glass_flask.png
│           ├─ small_mangrove_glass_flask.png
│           ├─ small_mangrove_gray_stained_glass_flask.png
│           ├─ small_mangrove_green_stained_glass_flask.png
│           ├─ small_mangrove_light_blue_stained_glass_flask.png
│           ├─ small_mangrove_light_gray_stained_glass_flask.png
│           ├─ small_mangrove_lime_stained_glass_flask.png
│           ├─ small_mangrove_magenta_stained_glass_flask.png
│           ├─ small_mangrove_orange_stained_glass_flask.png
│           ├─ small_mangrove_pink_stained_glass_flask.png
│           ├─ small_mangrove_purple_stained_glass_flask.png
│           ├─ small_mangrove_red_stained_glass_flask.png
│           ├─ small_mangrove_tinted_glass_flask.png
│           ├─ small_mangrove_white_stained_glass_flask.png
│           ├─ small_mangrove_yellow_stained_glass_flask.png
│           ├─ small_oak_black_stained_glass_flask.png
│           ├─ small_oak_blue_stained_glass_flask.png
│           ├─ small_oak_brown_stained_glass_flask.png
│           ├─ small_oak_cyan_stained_glass_flask.png
│           ├─ small_oak_glass_flask.png
│           ├─ small_oak_gray_stained_glass_flask.png
│           ├─ small_oak_green_stained_glass_flask.png
│           ├─ small_oak_light_blue_stained_glass_flask.png
│           ├─ small_oak_light_gray_stained_glass_flask.png
│           ├─ small_oak_lime_stained_glass_flask.png
│           ├─ small_oak_magenta_stained_glass_flask.png
│           ├─ small_oak_orange_stained_glass_flask.png
│           ├─ small_oak_pink_stained_glass_flask.png
│           ├─ small_oak_purple_stained_glass_flask.png
│           ├─ small_oak_red_stained_glass_flask.png
│           ├─ small_oak_tinted_glass_flask.png
│           ├─ small_oak_white_stained_glass_flask.png
│           ├─ small_oak_yellow_stained_glass_flask.png
│           ├─ small_pale_oak_black_stained_glass_flask.png
│           ├─ small_pale_oak_blue_stained_glass_flask.png
│           ├─ small_pale_oak_brown_stained_glass_flask.png
│           ├─ small_pale_oak_cyan_stained_glass_flask.png
│           ├─ small_pale_oak_glass_flask.png
│           ├─ small_pale_oak_gray_stained_glass_flask.png
│           ├─ small_pale_oak_green_stained_glass_flask.png
│           ├─ small_pale_oak_light_blue_stained_glass_flask.png
│           ├─ small_pale_oak_light_gray_stained_glass_flask.png
│           ├─ small_pale_oak_lime_stained_glass_flask.png
│           ├─ small_pale_oak_magenta_stained_glass_flask.png
│           ├─ small_pale_oak_orange_stained_glass_flask.png
│           ├─ small_pale_oak_pink_stained_glass_flask.png
│           ├─ small_pale_oak_purple_stained_glass_flask.png
│           ├─ small_pale_oak_red_stained_glass_flask.png
│           ├─ small_pale_oak_tinted_glass_flask.png
│           ├─ small_pale_oak_white_stained_glass_flask.png
│           ├─ small_pale_oak_yellow_stained_glass_flask.png
│           ├─ small_spruce_black_stained_glass_flask.png
│           ├─ small_spruce_blue_stained_glass_flask.png
│           ├─ small_spruce_brown_stained_glass_flask.png
│           ├─ small_spruce_cyan_stained_glass_flask.png
│           ├─ small_spruce_glass_flask.png
│           ├─ small_spruce_gray_stained_glass_flask.png
│           ├─ small_spruce_green_stained_glass_flask.png
│           ├─ small_spruce_light_blue_stained_glass_flask.png
│           ├─ small_spruce_light_gray_stained_glass_flask.png
│           ├─ small_spruce_lime_stained_glass_flask.png
│           ├─ small_spruce_magenta_stained_glass_flask.png
│           ├─ small_spruce_orange_stained_glass_flask.png
│           ├─ small_spruce_pink_stained_glass_flask.png
│           ├─ small_spruce_purple_stained_glass_flask.png
│           ├─ small_spruce_red_stained_glass_flask.png
│           ├─ small_spruce_tinted_glass_flask.png
│           ├─ small_spruce_white_stained_glass_flask.png
│           ├─ small_spruce_yellow_stained_glass_flask.png
│           ├─ small_warped_black_stained_glass_flask.png
│           ├─ small_warped_blue_stained_glass_flask.png
│           ├─ small_warped_brown_stained_glass_flask.png
│           ├─ small_warped_cyan_stained_glass_flask.png
│           ├─ small_warped_glass_flask.png
│           ├─ small_warped_gray_stained_glass_flask.png
│           ├─ small_warped_green_stained_glass_flask.png
│           ├─ small_warped_light_blue_stained_glass_flask.png
│           ├─ small_warped_light_gray_stained_glass_flask.png
│           ├─ small_warped_lime_stained_glass_flask.png
│           ├─ small_warped_magenta_stained_glass_flask.png
│           ├─ small_warped_orange_stained_glass_flask.png
│           ├─ small_warped_pink_stained_glass_flask.png
│           ├─ small_warped_purple_stained_glass_flask.png
│           ├─ small_warped_red_stained_glass_flask.png
│           ├─ small_warped_tinted_glass_flask.png
│           ├─ small_warped_white_stained_glass_flask.png
│           ├─ small_warped_yellow_stained_glass_flask.png
│           ├─ spruce_copper_barrel.png
│           ├─ spruce_copper_exposed_barrel.png
│           ├─ spruce_copper_oxidized_barrel.png
│           ├─ spruce_copper_weathered_barrel.png
│           ├─ spruce_gold_barrel.png
│           ├─ spruce_iron_barrel.png
│           ├─ spruce_netherite_barrel.png
│           ├─ warped_copper_barrel.png
│           ├─ warped_copper_exposed_barrel.png
│           ├─ warped_copper_oxidized_barrel.png
│           ├─ warped_copper_weathered_barrel.png
│           ├─ warped_gold_barrel.png
│           ├─ warped_iron_barrel.png
│           └─ warped_netherite_barrel.png
├─ palettes
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
├─ schemas
│  ├─ common.schema.json
│  └─ texture-palettes.schema.json
├─ templates
│  └─ modid
│     ├─ barrel.btg-template.json
│     ├─ barrel.png
│     ├─ barrel_block.btg-template.json
│     ├─ barrel_block.png
│     ├─ big_flask.btg-template.json
│     ├─ big_flask.png
│     ├─ keg.btg-template.json
│     ├─ keg.png
│     ├─ keg_block.btg-template.json
│     ├─ keg_block.png
│     ├─ medium_flask.btg-template.json
│     ├─ medium_flask.png
│     ├─ small_flask.btg-template.json
│     └─ small_flask.png
├─ textures
│  ├─ glass
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
│  ├─ metal
│  │  ├─ copper.png
│  │  ├─ copper_exposed.png
│  │  ├─ copper_oxidized.png
│  │  ├─ copper_weathered.png
│  │  ├─ gold.png
│  │  ├─ iron.png
│  │  └─ netherite.png
│  └─ wood
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
└─ tools
   ├─ btg.py
   ├─ btg_gui.py
   ├─ btg_gui_modular
   │  ├─ commands.py
   │  ├─ config.py
   │  ├─ constants.py
   │  ├─ main.py
   │  ├─ paths.py
   │  ├─ runner.py
   │  ├─ ui.py
   │  └─ __init__.py
   ├─ btg_gui_v1.py
   ├─ btg_gui_v2.py
   ├─ btg_gui_v3.py
   ├─ btg_gui_v4.py
   ├─ btg_v1.py
   ├─ btg_v2.py
   ├─ btg_v3.py
   └─ btg_v4.py

```

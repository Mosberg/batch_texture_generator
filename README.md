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
│     │  ├─ iron_keg_block.json
│     │  └─ oak_iron_barrel_block.json
│     ├─ items                                # Item JSON files
│     │  ├─ big_oak_glass_flask.json
│     │  ├─ iron_keg.json
│     │  ├─ medium_oak_glass_flask.json
│     │  ├─ oak_iron_barrel.json
│     │  └─ small_oak_glass_flask.json
│     ├─ lang                                 # Language files
│     │  └─ en_us.json
│     ├─ models                               # Model JSON files
│     │  ├─ block                             # Block model JSON files
│     │  │  ├─ iron_keg_block.json
│     │  │  └─ oak_iron_barrel_block.json
│     │  └─ item                              # Item model JSON files
│     │     ├─ big_oak_glass_flask.json
│     │     ├─ iron_keg.json
│     │     ├─ medium_oak_glass_flask.json
│     │     ├─ oak_iron_barrel.json
│     │     └─ small_oak_glass_flask.json
│     └─ textures                             # Texture image files
│        ├─ block                             # Block texture image files
│        │  ├─ iron_keg_block.png
│        │  └─ oak_iron_barrel_block.png
│        └─ item                              # Item texture image files
│           ├─ big_oak_glass_flask.png
│           ├─ iron_keg.png
│           ├─ medium_oak_glass_flask.png
│           ├─ oak_iron_barrel.png
│           └─ small_oak_glass_flask.png
├─ input                                      # Input textures for processing
│  ├─ block                                   # Block input textures
│  │  ├─ barrel_block.png
│  │  └─ keg_block.png
│  └─ item                                    # Item input textures
│     ├─ barrel.png
│     ├─ big_flask.png
│     ├─ keg.png
│     ├─ medium_flask.png
│     └─ small_flask.png
├─ output                                     # Output files generated after processing
│  └─ modid
│     ├─ blockstates                          # Blockstate JSON files
│     │  ├─ iron_keg_block.json
│     │  └─ oak_iron_barrel_block.json
│     ├─ items                                # Item JSON files
│     │  ├─ big_oak_glass_flask.json
│     │  ├─ iron_keg.json
│     │  ├─ medium_oak_glass_flask.json
│     │  ├─ oak_iron_barrel.json
│     │  └─ small_oak_glass_flask.json
│     ├─ lang                                 # Language files
│     │  └─ en_us.json
│     ├─ models                               # Model JSON files
│     │  ├─ block                             # Block model JSON files
│     │  │  ├─ iron_keg_block.json
│     │  │  └─ oak_iron_barrel_block.json
│     │  └─ item                              # Item model JSON files
│     │     ├─ big_oak_glass_flask.json
│     │     ├─ iron_keg.json
│     │     ├─ medium_oak_glass_flask.json
│     │     ├─ oak_iron_barrel.json
│     │     └─ small_oak_glass_flask.json
│     └─ textures                             # Texture image files
│        ├─ block                             # Block texture image files
│        │  ├─ iron_keg_block.png
│        │  └─ oak_iron_barrel_block.png
│        └─ item                              # Item texture image files
│           ├─ big_oak_glass_flask.png
│           ├─ iron_keg.png
│           ├─ medium_oak_glass_flask.png
│           ├─ oak_iron_barrel.png
│           └─ small_oak_glass_flask.png
├─ palettes                                   # Color palettes for texture variations
│  ├─ glass                                   # Glass texture palettes
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
│  ├─ metal                                   # Metal texture palettes
│  │  ├─ copper.texture-palettes.json
│  │  ├─ copper_exposed.texture-palettes.json
│  │  ├─ copper_oxidized.texture-palettes.json
│  │  ├─ copper_weathered.texture-palettes.json
│  │  ├─ gold.texture-palettes.json
│  │  ├─ iron.texture-palettes.json
│  │  └─ netherite.texture-palettes.json
│  └─ wood                                    # Wood texture palettes
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
├─ README.md                                 # Project documentation and overview
├─ requirements.txt                          # Python dependencies
├─ schemas                                   # JSON schema definitions
│  ├─ common.schema.json                     # Common schema definitions
│  └─ texture-palettes.schema.json           # Texture palettes schema definition
├─ templates                                 # Model templates for blocks and items
│  ├─ block                                  # Block model templates
│  │  ├─ barrel_block.btg-template.json
│  │  └─ keg_block.btg-template.json
│  └─ item                                   # Item model templates
│     ├─ barrel.btg-template.json
│     ├─ big_flask.btg-template.json
│     ├─ keg.btg-template.json
│     ├─ medium_flask.btg-template.json
│     └─ small_flask.btg-template.json
├─ textures                                  # Texture image files for palette generation
│  ├─ glass                                  # Glass texture image files
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
│  ├─ metal                                   # Metal texture image files
│  │  ├─ copper.png
│  │  ├─ copper_exposed.png
│  │  ├─ copper_oxidized.png
│  │  ├─ copper_weathered.png
│  │  ├─ gold.png
│  │  ├─ iron.png
│  │  └─ netherite.png
│  └─ wood                                    # Wood texture image files
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
   ├─ btg.py                                  # Main script for batch texture generation
   └─ btg_gui.py                              # GUI script for batch texture generation

```

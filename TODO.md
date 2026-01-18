Yes—this can be automated by adding an `autotemplate` command that scans each `textures_input/*.png`, detects which **materials** are present by matching the image’s unique RGBA pixels against your known `palettes/<material>/*.texture-palettes.json`, then writes `textures_input/<name>.btg-template.json` automatically. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/66f78ca6-85c2-4f5b-a108-7525c3b0cbdf/README.md)

## What the auto-template does

- Reads `textures_input/<template>.png` and collects its unique non-transparent RGBA colors. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/66f78ca6-85c2-4f5b-a108-7525c3b0cbdf/README.md)
- Scores every palette entry (e.g. `wood/oak`, `metal/iron`, `glass/glass`) by how many of those colors appear in the template image (exact RGBA match first, optional nearest-match fallback). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/69448c1e-a90e-46ba-8479-37eda34bd1a1/btg.py)
- Picks the best match per material category and emits a `*.btg-template.json` that your `generate` command can use to produce _all combinations_ (e.g. `{wood}` × `{metal}` for barrel, `{wood}` × `{glass}` for flasks, `{metal}` for keg). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/66f78ca6-85c2-4f5b-a108-7525c3b0cbdf/README.md)

## Detection approach (robust + fast)

A practical heuristic that works well for pixel-art templates like yours:

- For each material folder (wood/metal/glass), pick the palette ID with the highest “hit count” = number of template colors found in that palette’s group colors. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/69448c1e-a90e-46ba-8479-37eda34bd1a1/btg.py)
- Require a minimum hit threshold (e.g. `>= 2` or `>= 10% of template unique colors`) so the tool doesn’t “detect” glass in a purely metal texture by accident. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/66f78ca6-85c2-4f5b-a108-7525c3b0cbdf/README.md)
- If you ever have templates where two palettes share some colors, optionally add a “competition” step: assign pixels to whichever palette yields the smallest distance, then score by assigned-pixel-count. (This is the same concept your multi-slot recolor uses.) [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/69448c1e-a90e-46ba-8479-37eda34bd1a1/btg.py)

## btg.py: add `autotemplate`

Below is a drop-in addition (new command + helpers). It assumes:

- `palettes/` has the structure shown in your README (`palettes/wood/*.json`, `palettes/metal/*.json`, `palettes/glass/*.json`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/66f78ca6-85c2-4f5b-a108-7525c3b0cbdf/README.md)
- Palette files follow your `texture-palettes` schema and expose `items[].material` + `groups.base.colors`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/ac1c74d6-9c5a-4ecf-bc6d-cc33eb2befe1/texture-palettes.schema.json)

Add these helpers somewhere near your other “index” functions:

```python
def _rel_posix(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()

def palette_hit_score(template_colors: set[RGBA], palette: list[RGBA]) -> int:
    pal_set = set(palette)
    return sum(1 for c in template_colors if c in pal_set)

def infer_output_pattern(template_id: str, slots: list[str]) -> str:
    # Heuristics tailored to your examples.
    if template_id == "barrel":
        return "{wood}_{metal}_barrel.png"
    if template_id == "keg":
        return "{metal}_keg.png"
    if template_id.endswith("_flask"):
        # big_flask -> big_{wood}_{glass}_flask.png
        if template_id in ("big_flask", "medium_flask", "small_flask"):
            size = template_id.split("_", 1)[0]
            return f"{size}_{{wood}}_{{glass}}_flask.png"
        return "{wood}_{glass}_" + template_id + ".png"

    # Generic fallback: {wood}_{metal}_{glass}_<template>.png (only the slots that exist)
    return "_".join("{" + s + "}" for s in slots) + f"_{template_id}.png"
```

Then add the new command:

```python
def cmd_autotemplate(args: argparse.Namespace) -> int:
    templates_dir = Path(args.templates)
    palettes_dir = Path(args.palettes)
    out_dir = Path(args.out_dir) if args.out_dir else templates_dir

    palette_index = load_all_palettes_index(palettes_dir)

    pngs = sorted(templates_dir.glob("*.png"))
    if not pngs:
        LOG.warning("No PNG templates found in %s", templates_dir.as_posix())
        return 0

    written = 0
    for png in pngs:
        template_id = png.stem

        img = Image.open(png).convert("RGBA")
        pixels: list[RGBA] = list(img.getdata())
        template_colors: set[RGBA] = {p for p in pixels if p [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/ac1c74d6-9c5a-4ecf-bc6d-cc33eb2befe1/texture-palettes.schema.json) >= args.min_alpha}

        slots: list[dict[str, Any]] = []
        slot_names: list[str] = []

        for material in args.materials.split(","):
            material = material.strip()
            if not material:
                continue

            by_id = palette_index.get(material, {})
            if not by_id:
                continue

            best_id = None
            best_score = 0
            best_item = None
            best_path = None

            for pid, (p_path, p_item) in by_id.items():
                # default_group() prefers "base" when present
                _, grp = p_item.default_group()
                score = palette_hit_score(template_colors, grp.colors_rgba())
                if score > best_score:
                    best_score = score
                    best_id = pid
                    best_item = p_item
                    best_path = p_path

            if best_id is None or best_score < args.min_hits:
                continue

            slot_name = material  # "wood"/"metal"/"glass"
            slot_names.append(slot_name)
            slots.append({
                "slot": slot_name,
                "material": material,
                "source": {
                    "palette": _rel_posix(best_path, palettes_dir),
                    "id": best_item.id,
                    "group": "base",
                },
            })

        if not slots:
            LOG.warning("No slots detected for %s (try lowering --min-hits).", png.name)
            continue

        out_pattern = infer_output_pattern(template_id, slot_names)

        data = {
            "schema": "btg-template",
            "version": 1,
            "template": {"id": template_id, "path": str(png.as_posix()).replace("\\", "/")},
            "output": {"pattern": out_pattern},
            "slots": slots,
        }

        out_path = out_dir / f"{template_id}.btg-template.json"
        if args.dry_run:
            LOG.info("[DRY] Would write %s", out_path.as_posix())
        else:
            save_json(out_path, data)
            LOG.info("Wrote %s", out_path.as_posix())
            written += 1

    LOG.info("Autotemplate complete: wrote %d file(s).", written)
    return 0
```

Finally wire it into `build_parser()`:

```python
a = sub.add_parser("autotemplate", help="Auto-generate *.btg-template.json from template PNGs.")
a.add_argument("--templates", default="textures_input")
a.add_argument("--palettes", default="palettes")
a.add_argument("--out-dir", default=None, help="Where to write templates (default: templates dir).")
a.add_argument("--materials", default="wood,metal,glass", help="Comma list; scan only these materials.")
a.add_argument("--min-alpha", type=int, default=1)
a.add_argument("--min-hits", type=int, default=2, help="Minimum exact color hits to accept a material.")
a.add_argument("--dry-run", action="store_true")
a.set_defaults(func=cmd_autotemplate)
```

## How you’ll run it

1. Generate templates:

```bash
python tools/btg.py autotemplate
```

2. Then generate all combinations:

```bash
python tools/btg.py generate
```

That fits your repo layout (`textures_input/` for templates, `palettes/` for materials, `textures_output/` for results). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/9838088/66f78ca6-85c2-4f5b-a108-7525c3b0cbdf/README.md)

If the heuristic for filename patterns should be 100% data-driven (instead of hardcoding barrel/keg/flask naming), what naming rule is preferred for “unknown” templates: `{slot...}_{template}.png`, or `{template}_{slot...}.png`?

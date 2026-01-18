#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: Pillow (PIL). Install requirements.txt into your venv.\n"
        f"Import error: {e}"
    )

HEX_RGBA_RE = re.compile(r"^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
PNG_EXTS = {".png"}


# -------------------------
# JSON helpers
# -------------------------
def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    # Keep files stable in git
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


# -------------------------
# Color helpers
# -------------------------
def normalize_hex_rgba(value: str) -> str:
    """
    Accepts '#RRGGBB' or '#RRGGBBAA' and returns normalized '#rrggbbaa'.
    """
    if not isinstance(value, str):
        raise TypeError("Expected str")
    m = HEX_RGBA_RE.match(value.strip())
    if not m:
        raise ValueError(f"Not a hex color: {value!r}")
    hexpart = m.group(1)
    if len(hexpart) == 6:
        hexpart = hexpart + "ff"
    return "#" + hexpart.lower()


def hex_to_rgba_tuple(hex_rgba: str) -> tuple[int, int, int, int]:
    h = normalize_hex_rgba(hex_rgba)[1:]
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    a = int(h[6:8], 16)
    return (r, g, b, a)


def rgba_tuple_to_hex(rgba: tuple[int, int, int, int]) -> str:
    r, g, b, a = rgba
    return f"#{r:02x}{g:02x}{b:02x}{a:02x}"


# -------------------------
# Palette IO (flexible)
# -------------------------
def _walk_json_mutate(obj: Any, fn) -> Any:
    """
    Deep-map a JSON-like structure, allowing mutation of scalar strings.
    """
    if isinstance(obj, dict):
        return {k: _walk_json_mutate(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_json_mutate(v, fn) for v in obj]
    return fn(obj)


def _extract_palette_ids(palette_json: Any) -> set[str]:
    """
    Support multiple palette file shapes:
    - {"palettes": {"id": ["#..."]}}
    - {"palettes": [{"id":"oak","colors":[...]}]}
    - {"id":"oak","colors":[...]}  (single)
    """
    ids: set[str] = set()

    if isinstance(palette_json, dict) and isinstance(
        palette_json.get("palettes"), dict
    ):
        for k, v in palette_json["palettes"].items():
            if isinstance(k, str) and isinstance(v, list):
                ids.add(k)
        return ids

    if isinstance(palette_json, dict) and isinstance(
        palette_json.get("palettes"), list
    ):
        for entry in palette_json["palettes"]:
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                ids.add(entry["id"])
        return ids

    if (
        isinstance(palette_json, dict)
        and isinstance(palette_json.get("id"), str)
        and isinstance(palette_json.get("colors"), list)
    ):
        ids.add(palette_json["id"])
        return ids

    return ids


def _get_palette_colors(palette_json: Any, palette_id: str) -> list[str]:
    """
    Returns a list of '#rrggbbaa' colors for a given palette_id.
    """
    if isinstance(palette_json, dict) and isinstance(
        palette_json.get("palettes"), dict
    ):
        palettes = palette_json["palettes"]
        if palette_id not in palettes:
            raise KeyError(f"Palette id not found: {palette_id!r}")
        colors = palettes[palette_id]
        if not isinstance(colors, list):
            raise TypeError(f"Palette {palette_id!r} is not a list")
        return [normalize_hex_rgba(c) for c in colors]

    if isinstance(palette_json, dict) and isinstance(
        palette_json.get("palettes"), list
    ):
        for entry in palette_json["palettes"]:
            if isinstance(entry, dict) and entry.get("id") == palette_id:
                colors = entry.get("colors", [])
                if not isinstance(colors, list):
                    raise TypeError(f"Palette {palette_id!r}.colors is not a list")
                return [normalize_hex_rgba(c) for c in colors]
        raise KeyError(f"Palette id not found: {palette_id!r}")

    if (
        isinstance(palette_json, dict)
        and palette_json.get("id") == palette_id
        and isinstance(palette_json.get("colors"), list)
    ):
        return [normalize_hex_rgba(c) for c in palette_json["colors"]]

    raise TypeError("Unsupported palette file shape")


def load_palette_colors(palette_file: Path, palette_id: str) -> list[str]:
    data = read_json(palette_file)
    return _get_palette_colors(data, palette_id)


# -------------------------
# Image operations
# -------------------------
def build_color_map(
    src_colors: list[str], dst_colors: list[str]
) -> dict[tuple[int, int, int, int], tuple[int, int, int, int]]:
    if len(src_colors) != len(dst_colors):
        raise ValueError(
            f"Palette length mismatch: src has {len(src_colors)} colors, dst has {len(dst_colors)} colors"
        )
    mapping: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    for s, d in zip(src_colors, dst_colors, strict=True):
        mapping[hex_to_rgba_tuple(s)] = hex_to_rgba_tuple(d)
    return mapping


def apply_palette_maps(
    img: Image.Image,
    maps: list[dict[tuple[int, int, int, int], tuple[int, int, int, int]]],
) -> Image.Image:
    """
    Applies maps sequentially (later maps override earlier ones if keys overlap).
    """
    img = img.convert("RGBA")
    data = list(img.getdata())

    # Merge maps (preserve sequence semantics: later overwrites earlier)
    merged: dict[tuple[int, int, int, int], tuple[int, int, int, int]] = {}
    for m in maps:
        merged.update(m)

    out = [merged.get(px, px) for px in data]
    img2 = Image.new("RGBA", img.size)
    img2.putdata(out)
    return img2


# -------------------------
# Generation (items/models/lang/blockstates)
# -------------------------
def title_from_id(s: str) -> str:
    s = s.replace(":", "_").replace("/", "_").replace("-", "_")
    parts = [p for p in s.split("_") if p]
    return " ".join(p[:1].upper() + p[1:] for p in parts)


def minecraft_item_model(namespace: str, item_id: str) -> dict[str, Any]:
    return {
        "parent": "item/generated",
        "textures": {"layer0": f"{namespace}:item/{item_id}"},
    }


def minecraft_item_definition(namespace: str, item_id: str) -> dict[str, Any]:
    # 1.21+ items/ format (simple forwarding file)
    return {
        "model": {
            "type": "minecraft:model",
            "model": f"{namespace}:item/{item_id}",
        }
    }


def minecraft_block_model_cube_all(namespace: str, block_id: str) -> dict[str, Any]:
    return {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": f"{namespace}:block/{block_id}"},
    }


def minecraft_blockstate_facing(
    namespace: str, block_id: str, model_path: str | None = None
) -> dict[str, Any]:
    """
    Creates a variants blockstate with facing={north,east,south,west}.
    """
    model_ref = model_path or f"{namespace}:block/{block_id}"
    return {
        "variants": {
            "facing=north": {"model": model_ref, "y": 0},
            "facing=east": {"model": model_ref, "y": 90},
            "facing=south": {"model": model_ref, "y": 180},
            "facing=west": {"model": model_ref, "y": 270},
        }
    }


def merge_lang(
    existing: dict[str, Any] | None, updates: dict[str, str]
) -> dict[str, Any]:
    out: dict[str, Any] = dict(existing or {})
    out.update(updates)
    return out


@dataclass(frozen=True)
class SwapSpec:
    src_palette_file: Path
    src_id: str
    dst_palette_file: Path
    dst_id: str

    def make_map(self) -> dict[tuple[int, int, int, int], tuple[int, int, int, int]]:
        src = load_palette_colors(self.src_palette_file, self.src_id)
        dst = load_palette_colors(self.dst_palette_file, self.dst_id)
        return build_color_map(src, dst)


@dataclass
class TemplateTask:
    kind: str  # "item" or "block"
    base_texture: Path
    output_id: str
    display_name: str
    swaps: list[SwapSpec]
    item_group_id: str | None = None
    item_group_name: str | None = None
    # optional explicit model/blockstate templates
    block_model_template: Path | None = None
    blockstate_template: Path | None = None


def _resolve_rel(base_dir: Path, maybe_rel: str) -> Path:
    p = Path(maybe_rel)
    return p if p.is_absolute() else (base_dir / p)


def parse_btg_template(path: Path) -> list[TemplateTask]:
    """
    Flexible template parsing.

    Supported shapes:
    A) {"tasks":[{...}, {...}]}
    B) { ...single task fields... }
    """
    data = read_json(path)
    base_dir = path.parent

    def parse_task(obj: dict[str, Any]) -> TemplateTask:
        kind = str(obj.get("kind", "item"))
        base_texture = _resolve_rel(
            base_dir, str(obj.get("base_texture", obj.get("texture", "")))
        )
        if not base_texture.exists():
            raise FileNotFoundError(
                f"Template refers to missing texture: {base_texture}"
            )

        output_id = str(obj.get("output_id", obj.get("id", base_texture.stem)))
        display_name = str(
            obj.get("display_name", obj.get("name", title_from_id(output_id)))
        )

        swaps_raw = obj.get("swaps", [])
        if not isinstance(swaps_raw, list):
            raise TypeError(f"{path}: swaps must be a list")

        swaps: list[SwapSpec] = []
        for s in swaps_raw:
            if not isinstance(s, dict):
                raise TypeError(f"{path}: swap entries must be objects")
            swaps.append(
                SwapSpec(
                    src_palette_file=_resolve_rel(base_dir, str(s["src_palette"])),
                    src_id=str(s["src_id"]),
                    dst_palette_file=_resolve_rel(base_dir, str(s["dst_palette"])),
                    dst_id=str(s["dst_id"]),
                )
            )

        block_model_template = obj.get("block_model_template")
        blockstate_template = obj.get("blockstate_template")

        return TemplateTask(
            kind=kind,
            base_texture=base_texture,
            output_id=output_id,
            display_name=display_name,
            swaps=swaps,
            item_group_id=(
                str(obj["item_group_id"]) if "item_group_id" in obj else None
            ),
            item_group_name=(
                str(obj["item_group_name"]) if "item_group_name" in obj else None
            ),
            block_model_template=(
                _resolve_rel(base_dir, str(block_model_template))
                if block_model_template
                else None
            ),
            blockstate_template=(
                _resolve_rel(base_dir, str(blockstate_template))
                if blockstate_template
                else None
            ),
        )

    if isinstance(data, dict) and isinstance(data.get("tasks"), list):
        return [parse_task(t) for t in data["tasks"]]
    if isinstance(data, dict):
        return [parse_task(data)]

    raise TypeError(f"Unsupported template JSON root in {path}")


def write_task_outputs(
    task: TemplateTask,
    namespace: str,
    out_root: Path,
    write_modid_tree: bool,
    write_flat_tree: bool,
    lang_file_name: str = "en_us.json",
) -> None:
    """
    Write recolored texture + generated JSON files into:
    - output/modid/... (resourcepack-ish tree) if write_modid_tree
    - output/... (flat tree: textures/, models/, items/, lang/) if write_flat_tree
    """
    img = Image.open(task.base_texture)
    maps = [s.make_map() for s in task.swaps]
    recolored = apply_palette_maps(img, maps)

    def write_for_base(base: Path) -> None:
        if task.kind == "block":
            tex_path = base / namespace / "textures" / "block" / f"{task.output_id}.png"
            model_path = (
                base / namespace / "models" / "block" / f"{task.output_id}.json"
            )
            blockstates_path = (
                base / namespace / "blockstates" / f"{task.output_id}.json"
            )
        else:
            tex_path = base / namespace / "textures" / "item" / f"{task.output_id}.png"
            model_path = base / namespace / "models" / "item" / f"{task.output_id}.json"
            blockstates_path = None

        items_def_path = base / namespace / "items" / f"{task.output_id}.json"
        lang_path = base / namespace / "lang" / lang_file_name

        tex_path.parent.mkdir(parents=True, exist_ok=True)
        recolored.save(tex_path)

        # Model JSON
        if task.kind == "block":
            if task.block_model_template and task.block_model_template.exists():
                model_json = read_json(task.block_model_template)
                # Best-effort replace modid namespace references
                model_json = _walk_json_mutate(
                    model_json,
                    lambda v: (
                        v.replace("modid:", f"{namespace}:")
                        if isinstance(v, str)
                        else v
                    ),
                )
                model_json = _walk_json_mutate(
                    model_json,
                    lambda v: (
                        v.replace("modid/", f"{namespace}/")
                        if isinstance(v, str)
                        else v
                    ),
                )
                # Also try to replace known block texture id in strings if present
                model_json = _walk_json_mutate(
                    model_json,
                    lambda v: (
                        v.replace("modid:block", f"{namespace}:block")
                        if isinstance(v, str)
                        else v
                    ),
                )
            else:
                model_json = minecraft_block_model_cube_all(namespace, task.output_id)
        else:
            model_json = minecraft_item_model(namespace, task.output_id)

        write_json(model_path, model_json)

        # items/ JSON (1.21+ forwarding)
        write_json(items_def_path, minecraft_item_definition(namespace, task.output_id))

        # blockstates for blocks
        if task.kind == "block":
            if task.blockstate_template and task.blockstate_template.exists():
                bs_json = read_json(task.blockstate_template)
                bs_json = _walk_json_mutate(
                    bs_json,
                    lambda v: (
                        v.replace("modid:", f"{namespace}:")
                        if isinstance(v, str)
                        else v
                    ),
                )
                bs_json = _walk_json_mutate(
                    bs_json,
                    lambda v: (
                        v.replace("modid/", f"{namespace}/")
                        if isinstance(v, str)
                        else v
                    ),
                )
            else:
                bs_json = minecraft_blockstate_facing(namespace, task.output_id)
            if blockstates_path is not None:
                write_json(blockstates_path, bs_json)

        # lang merge
        existing = read_json(lang_path) if lang_path.exists() else {}
        updates: dict[str, str] = {}
        if task.kind == "block":
            updates[f"block.{namespace}.{task.output_id}"] = task.display_name
        else:
            updates[f"item.{namespace}.{task.output_id}"] = task.display_name

        if task.item_group_id and task.item_group_name:
            updates[f"itemGroup.{namespace}.{task.item_group_id}"] = (
                task.item_group_name
            )

        write_json(lang_path, merge_lang(existing, updates))

    if write_modid_tree:
        write_for_base(out_root)

    if write_flat_tree:
        # mirror your README's "flat" output layout (textures/, models/, items/, lang/)
        # by treating out_root_flat = out_root / "" but without namespace folder:
        # we still include the namespace folder inside those dirs? Some users want it without.
        # We'll write WITHOUT the namespace folder to match README wording.
        base = out_root

        # Texture
        if task.kind == "block":
            tex_path = base / "textures" / "block" / f"{task.output_id}.png"
            model_path = base / "models" / "block" / f"{task.output_id}.json"
            blockstates_path = base / "blockstates" / f"{task.output_id}.json"
        else:
            tex_path = base / "textures" / "item" / f"{task.output_id}.png"
            model_path = base / "models" / "item" / f"{task.output_id}.json"
            blockstates_path = None

        items_def_path = base / "items" / f"{task.output_id}.json"
        lang_path = base / "lang" / lang_file_name

        tex_path.parent.mkdir(parents=True, exist_ok=True)
        recolored.save(tex_path)

        if task.kind == "block":
            model_json = minecraft_block_model_cube_all(namespace, task.output_id)
        else:
            model_json = minecraft_item_model(namespace, task.output_id)
        write_json(model_path, model_json)

        write_json(items_def_path, minecraft_item_definition(namespace, task.output_id))

        if task.kind == "block" and blockstates_path is not None:
            write_json(
                blockstates_path, minecraft_blockstate_facing(namespace, task.output_id)
            )

        existing = read_json(lang_path) if lang_path.exists() else {}
        updates: dict[str, str] = {}
        if task.kind == "block":
            updates[f"block.{namespace}.{task.output_id}"] = task.display_name
        else:
            updates[f"item.{namespace}.{task.output_id}"] = task.display_name
        write_json(lang_path, merge_lang(existing, updates))


# -------------------------
# Commands
# -------------------------
def cmd_normalize(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes_dir)
    paths = sorted(palettes_dir.rglob("*.texture-palettes.json"))

    changed = 0
    for p in paths:
        data = read_json(p)

        def normalize_scalar(v: Any) -> Any:
            if isinstance(v, str) and HEX_RGBA_RE.match(v.strip()):
                try:
                    return normalize_hex_rgba(v)
                except Exception:
                    return v
            return v

        normalized = _walk_json_mutate(data, normalize_scalar)
        if normalized != data:
            write_json(p, normalized)
            changed += 1

    print(f"Normalized {changed}/{len(paths)} palette files.")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes_dir)
    paths = sorted(palettes_dir.rglob("*.texture-palettes.json"))

    errors: list[str] = []
    for p in paths:
        try:
            data = read_json(p)
            ids = _extract_palette_ids(data)
            if not ids:
                errors.append(f"{p}: no palettes found (unsupported shape or empty).")
                continue

            for pid in sorted(ids):
                colors = _get_palette_colors(data, pid)
                # validate normalized format
                for c in colors:
                    if not isinstance(c, str) or not HEX_RGBA_RE.match(c):
                        errors.append(f"{p}: palette {pid!r} invalid color {c!r}")
                    if len(c) != 9:
                        errors.append(
                            f"{p}: palette {pid!r} must be #RRGGBBAA; got {c!r}"
                        )
        except Exception as e:
            errors.append(f"{p}: {e}")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(" -", e)
        return 1

    print(f"Validated {len(paths)} palette files OK.")
    return 0


def cmd_extract(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures_dir)
    out_dir = Path(args.output_dir)
    max_colors = int(args.max_colors)

    pngs = [p for p in sorted(textures_dir.rglob("*.png")) if p.is_file()]
    written = 0

    for png in pngs:
        img = Image.open(png).convert("RGBA")
        pixels = list(img.getdata())
        # preserve order but keep unique by seen-set
        seen: set[tuple[int, int, int, int]] = set()
        uniq: list[tuple[int, int, int, int]] = []
        for px in pixels:
            if px not in seen:
                seen.add(px)
                uniq.append(px)

        if len(uniq) > max_colors:
            uniq = uniq[:max_colors]

        colors = [rgba_tuple_to_hex(px) for px in uniq]
        palette_id = png.stem

        rel = png.relative_to(textures_dir)
        out_path = out_dir / rel.parent / f"{palette_id}.texture-palettes.json"
        payload = {
            "$schema": "../schemas/texture-palettes.schema.json",
            "palettes": {
                palette_id: colors,
            },
        }
        write_json(out_path, payload)
        written += 1

    print(f"Extracted palettes for {written} textures into: {out_dir}")
    return 0


def _iter_pngs(input_dir: Path) -> Iterable[Path]:
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in PNG_EXTS:
            yield p


def cmd_recolor(args: argparse.Namespace) -> int:
    namespace = args.namespace
    out_root = Path(args.output_dir)

    write_modid_tree = not args.no_modid_tree
    write_flat_tree = not args.no_flat_tree

    # Mode A: batch templates
    templates_dir = Path(args.templates_dir) if args.templates_dir else None
    if templates_dir:
        template_files = sorted(templates_dir.rglob("*.btg-template.json"))
        if not template_files:
            raise SystemExit(f"No templates found in: {templates_dir}")

        tasks: list[TemplateTask] = []
        for tf in template_files:
            tasks.extend(parse_btg_template(tf))

        for t in tasks:
            write_task_outputs(
                t,
                namespace=namespace,
                out_root=out_root,
                write_modid_tree=write_modid_tree,
                write_flat_tree=write_flat_tree,
                lang_file_name=args.lang_file,
            )

        print(f"Generated {len(tasks)} tasks from templates in {templates_dir}")
        return 0

    # Mode B: manual swaps on a directory
    if not args.swap:
        raise SystemExit(
            "recolor: either provide --templates-dir or one/more --swap entries."
        )

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise SystemExit(f"Input dir not found: {input_dir}")

    swaps: list[SwapSpec] = []
    for src_palette, src_id, dst_palette, dst_id in args.swap:
        swaps.append(
            SwapSpec(
                src_palette_file=Path(src_palette),
                src_id=src_id,
                dst_palette_file=Path(dst_palette),
                dst_id=dst_id,
            )
        )
    maps = [s.make_map() for s in swaps]

    pngs = list(_iter_pngs(input_dir))
    if not pngs:
        print(f"No PNGs found in {input_dir}")
        return 0

    for p in pngs:
        img = Image.open(p)
        recolored = apply_palette_maps(img, maps)

        rel = p.relative_to(input_dir)
        out_path = out_root / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        recolored.save(out_path)

        # optional minimal JSON generation (item only)
        if args.generate_json:
            item_id = out_path.stem
            base = out_root / namespace if write_modid_tree else out_root
            # Put them into the namespaced tree (recommended)
            write_json(
                base / "models" / "item" / f"{item_id}.json",
                minecraft_item_model(namespace, item_id),
            )
            write_json(
                base / "items" / f"{item_id}.json",
                minecraft_item_definition(namespace, item_id),
            )
            lang_path = base / "lang" / args.lang_file
            existing = read_json(lang_path) if lang_path.exists() else {}
            existing = merge_lang(
                existing, {f"item.{namespace}.{item_id}": title_from_id(item_id)}
            )
            write_json(lang_path, existing)

    print(f"Recolored {len(pngs)} images into: {out_root}")
    return 0


# -------------------------
# CLI
# -------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="btg.py", description="Batch Texture Generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_norm = sub.add_parser(
        "normalize", help="Normalize palettes to RGBA (#RRGGBBAA) and casing"
    )
    p_norm.add_argument("--palettes-dir", default="palettes", help="Palettes directory")
    p_norm.set_defaults(func=cmd_normalize)

    p_val = sub.add_parser("validate", help="Validate palette JSON files")
    p_val.add_argument("--palettes-dir", default="palettes", help="Palettes directory")
    p_val.set_defaults(func=cmd_validate)

    p_ext = sub.add_parser("extract", help="Extract RGBA palettes from textures/")
    p_ext.add_argument(
        "--textures-dir",
        default="textures",
        help="Directory containing source textures",
    )
    p_ext.add_argument(
        "--output-dir",
        default="palettes_extracted",
        help="Where to write extracted palettes",
    )
    p_ext.add_argument(
        "--max-colors", type=int, default=32, help="Max colors per palette file"
    )
    p_ext.set_defaults(func=cmd_extract)

    p_rec = sub.add_parser(
        "recolor", help="Recolor textures using palette swaps (manual or templates)"
    )
    p_rec.add_argument(
        "--namespace", default="modid", help="Resource namespace (e.g. mod id)"
    )
    p_rec.add_argument("--output-dir", default="output", help="Output root directory")
    p_rec.add_argument("--lang-file", default="en_us.json", help="Language file name")

    # batch mode
    p_rec.add_argument(
        "--templates-dir", default=None, help="Directory containing *.btg-template.json"
    )

    # manual mode
    p_rec.add_argument(
        "--input-dir", default="textures_input", help="Input directory of PNGs"
    )
    p_rec.add_argument(
        "--swap",
        action="append",
        nargs=4,
        metavar=("SRC_PALETTE", "SRC_ID", "DST_PALETTE", "DST_ID"),
        help="Add a palette swap (repeatable).",
    )
    p_rec.add_argument(
        "--generate-json",
        action="store_true",
        help="Also generate basic item json/model/lang entries",
    )

    # output layout toggles
    p_rec.add_argument(
        "--no-modid-tree",
        action="store_true",
        help="Do not write output/<modid>/... tree",
    )
    p_rec.add_argument(
        "--no-flat-tree",
        action="store_true",
        help="Do not write flat output/textures/... tree",
    )

    p_rec.set_defaults(func=cmd_recolor)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

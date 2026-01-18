from __future__ import annotations

import argparse
import json
import logging
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image
from jsonschema import Draft202012Validator


LOG = logging.getLogger("btg")


# ----------------------------
# Models
# ----------------------------

RGBA = Tuple[int, int, int, int]


@dataclass(frozen=True)
class PaletteGroup:
    colors: List[str]
    comment: str = ""
    metadata: Optional[dict] = None

    def colors_rgba(self) -> List[RGBA]:
        return [parse_hex_color(c) for c in self.colors]


@dataclass(frozen=True)
class PaletteItem:
    id: str
    name: str
    path: str
    material: str
    groups: Dict[str, PaletteGroup]
    metadata: Optional[dict] = None

    def group(self, group_id: str) -> PaletteGroup:
        if group_id in self.groups:
            return self.groups[group_id]
        raise KeyError(f"Group '{group_id}' not found for palette item '{self.id}'")

    def default_group(self) -> Tuple[str, PaletteGroup]:
        if "base" in self.groups:
            return "base", self.groups["base"]
        # Deterministic fallback
        first_key = sorted(self.groups.keys())[0]
        return first_key, self.groups[first_key]


@dataclass(frozen=True)
class PaletteFile:
    schema: str
    version: int
    items: List[PaletteItem]


# ----------------------------
# Color helpers
# ----------------------------


def parse_hex_color(s: str) -> RGBA:
    s = s.strip()
    if not s.startswith("#"):
        raise ValueError(f"Invalid color '{s}' (missing '#')")
    h = s[1:]
    if len(h) == 6:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return (r, g, b, 255)
    if len(h) == 8:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        a = int(h[6:8], 16)
        return (r, g, b, a)
    raise ValueError(f"Invalid color '{s}' (expected #RRGGBB or #RRGGBBAA)")


def rgba_to_hex(c: RGBA, *, with_alpha: bool = False) -> str:
    r, g, b, a = c
    if with_alpha:
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
    return f"#{r:02x}{g:02x}{b:02x}"


def color_dist2(a: RGBA, b: RGBA, *, alpha_weight: float = 0.25) -> float:
    ar, ag, ab, aa = a
    br, bg, bb, ba = b
    dr = ar - br
    dg = ag - bg
    db = ab - bb
    da = aa - ba
    return (dr * dr) + (dg * dg) + (db * db) + (alpha_weight * da * da)


# ----------------------------
# Schema validation (local refs)
# ----------------------------


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_schema_store(schema_dir: Path) -> Dict[str, dict]:
    store: Dict[str, dict] = {}
    for p in schema_dir.rglob("*.schema.json"):
        data = load_json(p)
        schema_id = data.get("$id")
        if schema_id:
            store[schema_id] = data
        store[str(p.as_posix())] = data
    return store


def validate_with_local_store(
    instance: dict, schema: dict, store: Dict[str, dict]
) -> None:
    validator = Draft202012Validator(
        schema, registry=None
    )  # registry handled by jsonschema internally
    # jsonschema resolves refs using $id-based lookups; we support that by preloading store IDs above.
    # If you want strict local-only refs, keep all $id values stable and consistent.
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        lines = []
        for e in errors[:20]:
            loc = "$." + ".".join(map(str, e.path)) if e.path else "$"
            lines.append(f"{loc}: {e.message}")
        more = "" if len(errors) <= 20 else f"\n...and {len(errors)-20} more"
        raise ValueError("Schema validation failed:\n" + "\n".join(lines) + more)


def validate_palette_file(palette_path: Path, schema_dir: Path) -> None:
    store = build_schema_store(schema_dir)
    schema_path = schema_dir / "texture-palettes.schema.json"
    schema = load_json(schema_path)
    data = load_json(palette_path)
    validate_with_local_store(data, schema, store)


# ----------------------------
# Palette parsing
# ----------------------------


def parse_palette_file(palette_path: Path) -> PaletteFile:
    raw = load_json(palette_path)
    if raw.get("schema") != "texture-palettes":
        raise ValueError(f"{palette_path}: schema must be 'texture-palettes'")

    items: List[PaletteItem] = []
    for it in raw.get("items", []):
        groups: Dict[str, PaletteGroup] = {}
        for gid, g in it.get("groups", {}).items():
            groups[gid] = PaletteGroup(
                colors=list(g.get("colors", [])),
                comment=str(g.get("comment", "")),
                metadata=g.get("metadata"),
            )
        items.append(
            PaletteItem(
                id=it["id"],
                name=it["name"],
                path=it["path"],
                material=it["material"],
                groups=groups,
                metadata=it.get("metadata"),
            )
        )
    return PaletteFile(
        schema=raw["schema"], version=int(raw.get("version", 1)), items=items
    )


# ----------------------------
# Palette extraction (from PNG)
# ----------------------------


def extract_palette_from_png(
    png_path: Path,
    *,
    max_colors: int = 32,
    min_alpha: int = 1,
    method: str = "quantize",  # "quantize" | "unique"
) -> List[RGBA]:
    img = Image.open(png_path).convert("RGBA")

    if method == "unique":
        colors = {}
        for px in img.getdata():
            if px[3] < min_alpha:
                continue
            colors[px] = colors.get(px, 0) + 1

        # Sort by frequency desc, then luminance asc for determinism.
        def key(item):
            (r, g, b, a), count = item
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            return (-count, lum, r, g, b, a)

        out = [c for (c, _) in sorted(colors.items(), key=key)[:max_colors]]
        return out

    if method == "quantize":
        # Pillow quantize is fast and good enough for Minecraft-style palettes.
        q = img.convert("RGBA").quantize(colors=max_colors, method=Image.MEDIANCUT)
        pal = q.getpalette() or []
        used = sorted(set(q.getdata()))
        out: List[RGBA] = []
        for idx in used:
            r = pal[idx * 3 + 0]
            g = pal[idx * 3 + 1]
            b = pal[idx * 3 + 2]
            out.append((r, g, b, 255))
        return out[:max_colors]

    raise ValueError(f"Unknown method: {method}")


# ----------------------------
# Recolor (palette swap)
# ----------------------------


def build_index_map(
    src: List[RGBA],
    dst: List[RGBA],
) -> List[RGBA]:
    if not src or not dst:
        raise ValueError("Empty palette")
    # If palette sizes differ, map by normalized index (keeps ramps usable).
    out: List[RGBA] = []
    for i in range(len(src)):
        t = 0.0 if len(src) == 1 else i / (len(src) - 1)
        j = int(round(t * (len(dst) - 1)))
        out.append(dst[j])
    return out


def recolor_png(
    input_png: Path,
    output_png: Path,
    *,
    src_palette: List[RGBA],
    dst_palette: List[RGBA],
    alpha_weight: float = 0.25,
    preserve_alpha: bool = True,
    min_alpha: int = 1,
) -> None:
    img = Image.open(input_png).convert("RGBA")
    pix = list(img.getdata())

    mapped_dst = build_index_map(src_palette, dst_palette)

    # Precompute nearest-color mapping for performance.
    # Keyed by exact pixel RGBA to avoid re-searching duplicates.
    cache: Dict[RGBA, RGBA] = {}

    def map_pixel(p: RGBA) -> RGBA:
        if p[3] < min_alpha:
            return p
        if p in cache:
            return cache[p]

        # Find nearest in src palette.
        best_i = 0
        best_d = float("inf")
        for i, c in enumerate(src_palette):
            d = color_dist2(p, c, alpha_weight=alpha_weight)
            if d < best_d:
                best_d = d
                best_i = i

        dst = mapped_dst[best_i]
        if preserve_alpha:
            dst = (dst[0], dst[1], dst[2], p[3])
        cache[p] = dst
        return dst

    out = [map_pixel(p) for p in pix]
    img.putdata(out)

    output_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_png)


# ----------------------------
# CLI
# ----------------------------


def cmd_validate(args: argparse.Namespace) -> int:
    schema_dir = Path(args.schema_dir)
    ok = True
    for p in Path(args.palettes_dir).rglob("*.texture-palettes.json"):
        try:
            validate_palette_file(p, schema_dir)
            LOG.info("OK   %s", p.as_posix())
        except Exception as e:
            ok = False
            LOG.error("FAIL %s\n%s", p.as_posix(), e)
    return 0 if ok else 2


def cmd_extract(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures_dir)
    palettes_dir = Path(args.palettes_dir)
    palettes_dir.mkdir(parents=True, exist_ok=True)

    for png in textures_dir.rglob("*.png"):
        material = png.parent.name  # assumes textures/<material>/<name>.png layout
        item_id = png.stem
        out_dir = palettes_dir / material
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{item_id}.texture-palettes.json"

        colors = extract_palette_from_png(
            png,
            max_colors=args.max_colors,
            min_alpha=args.min_alpha,
            method=args.method,
        )
        payload = {
            "$schema": str(
                Path("..") / ".." / "schemas" / "texture-palettes.schema.json"
            ).replace("\\", "/"),
            "schema": "texture-palettes",
            "version": 1,
            "items": [
                {
                    "id": item_id,
                    "name": item_id.replace("_", " ").title(),
                    "path": f"textures/{material}/{png.name}".replace("\\", "/"),
                    "material": material,
                    "groups": {
                        "base": {
                            "comment": f"Extracted from {png.as_posix()}",
                            "colors": [
                                rgba_to_hex(c, with_alpha=False) for c in colors
                            ],
                        }
                    },
                }
            ],
        }
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        LOG.info("Wrote %s", out_path.as_posix())

    return 0


def cmd_recolor(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes_dir)
    src_file = palettes_dir / args.src_palette
    dst_file = palettes_dir / args.dst_palette

    src_pf = parse_palette_file(src_file)
    dst_pf = parse_palette_file(dst_file)

    src_item = next((i for i in src_pf.items if i.id == args.src_id), None)
    dst_item = next((i for i in dst_pf.items if i.id == args.dst_id), None)
    if not src_item:
        raise SystemExit(f"Source id '{args.src_id}' not found in {src_file}")
    if not dst_item:
        raise SystemExit(f"Target id '{args.dst_id}' not found in {dst_file}")

    src_gid, src_group = (
        src_item.default_group()
        if args.group is None
        else (args.group, src_item.group(args.group))
    )
    dst_gid, dst_group = (
        dst_item.default_group()
        if args.group is None
        else (args.group, dst_item.group(args.group))
    )

    LOG.info("Using group src=%s dst=%s", src_gid, dst_gid)

    src_colors = src_group.colors_rgba()
    dst_colors = dst_group.colors_rgba()

    inp = Path(args.input_dir)
    out = Path(args.output_dir)

    files = sorted(inp.rglob("*.png"))
    if not files:
        LOG.warning("No PNG files found in %s", inp.as_posix())
        return 0

    for f in files:
        rel = f.relative_to(inp)
        out_path = out / rel
        recolor_png(
            f,
            out_path,
            src_palette=src_colors,
            dst_palette=dst_colors,
            alpha_weight=args.alpha_weight,
            preserve_alpha=not args.no_preserve_alpha,
            min_alpha=args.min_alpha,
        )
        LOG.info("Recolored %s -> %s", f.as_posix(), out_path.as_posix())

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="btg",
        description="Batch Texture Generator (palette extraction + palette-swap recolor).",
    )
    p.add_argument(
        "--log", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)."
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser(
        "validate", help="Validate all palette JSON files against local schemas."
    )
    v.add_argument(
        "--schemas", dest="schema_dir", default="schemas", help="Schema directory."
    )
    v.add_argument(
        "--palettes",
        dest="palettes_dir",
        default="palettes",
        help="Palettes directory.",
    )
    v.set_defaults(func=cmd_validate)

    e = sub.add_parser(
        "extract",
        help="Extract palettes from textures/*.png into palettes/*.texture-palettes.json.",
    )
    e.add_argument(
        "--textures",
        dest="textures_dir",
        default="textures",
        help="Textures directory.",
    )
    e.add_argument(
        "--palettes",
        dest="palettes_dir",
        default="palettes",
        help="Palettes directory.",
    )
    e.add_argument("--max-colors", type=int, default=32, help="Maximum palette size.")
    e.add_argument(
        "--min-alpha",
        type=int,
        default=1,
        help="Ignore pixels with alpha < this value.",
    )
    e.add_argument(
        "--method",
        choices=["quantize", "unique"],
        default="quantize",
        help="Extraction method.",
    )
    e.set_defaults(func=cmd_extract)

    r = sub.add_parser(
        "recolor",
        help="Recolor textures_input/ using a source->target palette swap into textures_output/.",
    )
    r.add_argument(
        "--palettes",
        dest="palettes_dir",
        default="palettes",
        help="Palettes directory.",
    )
    r.add_argument(
        "--src-palette",
        required=True,
        help="Path under palettes/ to source palette file (e.g. wood/oak.texture-palettes.json).",
    )
    r.add_argument(
        "--dst-palette",
        required=True,
        help="Path under palettes/ to target palette file (e.g. metal/iron.texture-palettes.json).",
    )
    r.add_argument("--src-id", required=True, help="Source palette item id (e.g. oak).")
    r.add_argument(
        "--dst-id", required=True, help="Target palette item id (e.g. iron)."
    )
    r.add_argument(
        "--group",
        default=None,
        help="Palette group id (default: 'base' if present, else first group).",
    )

    r.add_argument(
        "--input", dest="input_dir", default="textures_input", help="Input directory."
    )
    r.add_argument(
        "--output",
        dest="output_dir",
        default="textures_output",
        help="Output directory.",
    )

    r.add_argument(
        "--min-alpha",
        type=int,
        default=1,
        help="Leave pixels with alpha < this value unchanged.",
    )
    r.add_argument(
        "--alpha-weight",
        type=float,
        default=0.25,
        help="How much alpha affects nearest-color matching.",
    )
    r.add_argument(
        "--no-preserve-alpha",
        action="store_true",
        help="Do not preserve original alpha; use palette alpha instead.",
    )
    r.set_defaults(func=cmd_recolor)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, str(args.log).upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

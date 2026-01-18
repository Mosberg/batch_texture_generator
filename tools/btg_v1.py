from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image
from jsonschema import Draft202012Validator

try:
    # jsonschema >= 4 uses referencing for robust ref resolution
    from referencing import Registry, Resource
except Exception:  # pragma: no cover
    Registry = None  # type: ignore[assignment]
    Resource = None  # type: ignore[assignment]


LOG = logging.getLogger("btg")

RGBA = Tuple[int, int, int, int]


# ----------------------------
# Paths / config
# ----------------------------


def _norm_slash(p: str) -> str:
    return p.replace("\\", "/")


def _repo_root_from_tools_dir(tools_dir: Path) -> Path:
    # tools/ is expected to live in repo root: <root>/tools/btg.py
    return tools_dir.parent


# ----------------------------
# Hex utilities (RGBA only)
# ----------------------------


def hex6_to_hex8(s: str) -> str:
    s = s.strip()
    if len(s) == 7 and s.startswith("#"):
        return (s + "ff").lower()
    return s.lower()


def parse_hex8(s: str) -> RGBA:
    s = s.strip()
    if not (s.startswith("#") and len(s) == 9):
        raise ValueError(f"Invalid RGBA hex '{s}' (expected #RRGGBBAA)")
    h = s[1:]
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    a = int(h[6:8], 16)
    return (r, g, b, a)


def rgba_to_hex8(c: RGBA) -> str:
    r, g, b, a = c
    return f"#{r:02x}{g:02x}{b:02x}{a:02x}"


def color_dist2(a: RGBA, b: RGBA, *, alpha_weight: float = 0.25) -> float:
    ar, ag, ab, aa = a
    br, bg, bb, ba = b
    dr = ar - br
    dg = ag - bg
    db = ab - bb
    da = aa - ba
    return (dr * dr) + (dg * dg) + (db * db) + (alpha_weight * da * da)


# ----------------------------
# Models
# ----------------------------


@dataclass(frozen=True, slots=True)
class PaletteGroup:
    colors: List[str]
    comment: str = ""

    def colors_rgba(self) -> List[RGBA]:
        return [parse_hex8(c) for c in self.colors]


@dataclass(frozen=True, slots=True)
class PaletteItem:
    id: str
    name: str
    path: str
    material: str
    groups: Dict[str, PaletteGroup]
    metadata: Optional[dict] = None

    def group(self, group_id: str) -> PaletteGroup:
        try:
            return self.groups[group_id]
        except KeyError as e:
            raise KeyError(f"Group '{group_id}' not found for item '{self.id}'") from e

    def default_group(self) -> Tuple[str, PaletteGroup]:
        if "base" in self.groups:
            return "base", self.groups["base"]
        first = sorted(self.groups.keys())[0]
        return first, self.groups[first]


# ----------------------------
# JSON helpers
# ----------------------------


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# ----------------------------
# Schema validation (local refs)
# ----------------------------


def _build_registry(schema_dir: Path) -> Optional["Registry"]:
    if Registry is None or Resource is None:
        return None

    reg = Registry()
    for p in schema_dir.rglob("*.schema.json"):
        doc = load_json(p)

        # Register by local file URI so relative $ref works robustly.
        reg = reg.with_resource(p.as_uri(), Resource.from_contents(doc))

        # Also register by $id if present so $id-based refs work.
        sid = doc.get("$id")
        if isinstance(sid, str) and sid:
            reg = reg.with_resource(sid, Resource.from_contents(doc))

    return reg


def validate_palette_json(palette_path: Path, schema_dir: Path) -> None:
    schema_path = schema_dir / "texture-palettes.schema.json"
    schema = load_json(schema_path)
    instance = load_json(palette_path)

    registry = _build_registry(schema_dir)
    validator = (
        Draft202012Validator(schema, registry=registry)
        if registry is not None
        else Draft202012Validator(schema)
    )

    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if not errors:
        return

    lines: List[str] = []
    for e in errors[:50]:
        loc = "$" + ("." + ".".join(map(str, e.path)) if e.path else "")
        lines.append(f"{loc}: {e.message}")

    more = "" if len(errors) <= 50 else f"\n...and {len(errors) - 50} more"
    raise ValueError(
        f"Schema validation failed for {palette_path.as_posix()}:\n"
        + "\n".join(lines)
        + more
    )


# ----------------------------
# Palette parsing
# ----------------------------


def parse_palette_file(palette_path: Path) -> List[PaletteItem]:
    raw = load_json(palette_path)
    if raw.get("schema") != "texture-palettes":
        raise ValueError(f"{palette_path}: 'schema' must be 'texture-palettes'")

    out: List[PaletteItem] = []
    for it in raw.get("items", []):
        groups: Dict[str, PaletteGroup] = {}
        for gid, g in (it.get("groups") or {}).items():
            groups[str(gid)] = PaletteGroup(
                colors=[hex6_to_hex8(str(c)) for c in (g.get("colors") or [])],
                comment=str(g.get("comment") or ""),
            )

        out.append(
            PaletteItem(
                id=str(it["id"]),
                name=str(it["name"]),
                path=str(it["path"]),
                material=str(it["material"]),
                groups=groups,
                metadata=it.get("metadata"),
            )
        )

    return out


# ----------------------------
# Palette extraction
# ----------------------------


def extract_palette_from_png(
    png_path: Path,
    *,
    max_colors: int = 32,
    min_alpha: int = 1,
) -> List[RGBA]:

    img = Image.open(png_path).convert("RGBA")
    pixels = list(img.getdata())

    uniq = sorted({p for p in pixels if p[3] >= min_alpha})
    if 0 < len(uniq) <= max_colors:
        return uniq

    # Deterministic palette approximation for larger/gradient images.
    q = img.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette() or []
    used = sorted(set(q.getdata()))

    out: List[RGBA] = []
    for idx in used:
        r = pal[idx * 3 + 0]
        g = pal[idx * 3 + 1]
        b = pal[idx * 3 + 2]
        a = 255
        if a >= min_alpha:
            out.append((r, g, b, a))

    return out[:max_colors]


# ----------------------------
# Recolor (palette swap)
# ----------------------------


def build_index_map(src: List[RGBA], dst: List[RGBA]) -> List[RGBA]:
    if not src or not dst:
        raise ValueError("Empty palette(s)")
    mapped: List[RGBA] = []
    for i in range(len(src)):
        t = 0.0 if len(src) == 1 else i / (len(src) - 1)
        j = int(round(t * (len(dst) - 1)))
        mapped.append(dst[j])
    return mapped


def recolor_png(
    input_png: Path,
    output_png: Path,
    *,
    src_palette: List[RGBA],
    dst_palette: List[RGBA],
    alpha_weight: float = 0.25,
    preserve_alpha: bool = True,
    min_alpha: int = 1,
    exact_first: bool = True,
) -> None:
    img = Image.open(input_png).convert("RGBA")
    pixels: List[RGBA] = list(img.getdata())

    dst_by_src_index = build_index_map(src_palette, dst_palette)
    exact_map: Dict[RGBA, RGBA] = {}
    if exact_first:
        for i, c in enumerate(src_palette):
            exact_map[c] = dst_by_src_index[i]

    cache: Dict[RGBA, RGBA] = {}

    def map_pixel(p: RGBA) -> RGBA:
        if p[3] < min_alpha:
            return p
        if p in cache:
            return cache[p]

        if exact_first:
            m = exact_map.get(p)
            if m is not None:
                dst = m
                if preserve_alpha:
                    dst = (dst[0], dst[1], dst[2], p[3])
                cache[p] = dst
                return dst

        best_i = 0
        best_d = float("inf")
        for i, c in enumerate(src_palette):
            d = color_dist2(p, c, alpha_weight=alpha_weight)
            if d < best_d:
                best_d = d
                best_i = i

        dst = dst_by_src_index[best_i]
        if preserve_alpha:
            dst = (dst[0], dst[1], dst[2], p[3])

        cache[p] = dst
        return dst

    img.putdata([map_pixel(p) for p in pixels])
    output_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_png)


# ----------------------------
# Normalize palettes to RGBA
# ----------------------------


def normalize_palette_json(path: Path) -> bool:
    raw = load_json(path)
    changed = False

    for item in raw.get("items", []):
        groups = item.get("groups") or {}
        for group in groups.values():
            cols = group.get("colors") or []
            new_cols: List[str] = []
            for c in cols:
                c2 = hex6_to_hex8(str(c))
                if c2 != str(c):
                    changed = True
                new_cols.append(c2)
            group["colors"] = new_cols

    if changed:
        save_json(path, raw)

    return changed


# ----------------------------
# Commands
# ----------------------------


def cmd_validate(args: argparse.Namespace) -> int:
    schema_dir = Path(args.schemas)
    palettes_dir = Path(args.palettes)

    ok = True
    for p in sorted(palettes_dir.rglob("*.texture-palettes.json")):
        try:
            validate_palette_json(p, schema_dir)
            LOG.info("OK   %s", p.as_posix())
        except Exception as e:
            ok = False
            LOG.error("FAIL %s\n%s", p.as_posix(), e)

    return 0 if ok else 2


def cmd_extract(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures)
    palettes_dir = Path(args.palettes)
    schema_rel = args.schema_ref or "../../schemas/texture-palettes.schema.json"

    count = 0
    for png in sorted(textures_dir.rglob("*.png")):
        material = png.parent.name
        item_id = png.stem

        out_dir = palettes_dir / material
        out_path = out_dir / f"{item_id}.texture-palettes.json"

        colors = extract_palette_from_png(
            png, max_colors=args.max_colors, min_alpha=args.min_alpha
        )

        payload: Dict[str, Any] = {
            "$schema": schema_rel,
            "schema": "texture-palettes",
            "version": 1,
            "generator": {"name": "btg", "version": args.generator_version},
            "items": [
                {
                    "id": item_id,
                    "name": item_id.replace("_", " ").title(),
                    "path": _norm_slash(f"textures/{material}/{png.name}"),
                    "material": material,
                    "groups": {
                        "base": {
                            "comment": f"Extracted from {png.as_posix()}",
                            "colors": [rgba_to_hex8(c) for c in colors],
                        }
                    },
                }
            ],
        }

        save_json(out_path, payload)
        LOG.info("Wrote %s", out_path.as_posix())
        count += 1

    LOG.info("Extract complete (%d files).", count)
    return 0


def cmd_recolor(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes)
    src_file = palettes_dir / args.src_palette
    dst_file = palettes_dir / args.dst_palette

    src_items = parse_palette_file(src_file)
    dst_items = parse_palette_file(dst_file)

    src_item = next((i for i in src_items if i.id == args.src_id), None)
    dst_item = next((i for i in dst_items if i.id == args.dst_id), None)

    if not src_item:
        raise SystemExit(
            f"Source id '{args.src_id}' not found in {src_file.as_posix()}"
        )
    if not dst_item:
        raise SystemExit(
            f"Target id '{args.dst_id}' not found in {dst_file.as_posix()}"
        )

    if args.group is None:
        _, src_group = src_item.default_group()
        _, dst_group = dst_item.default_group()
    else:
        src_group = src_item.group(args.group)
        dst_group = dst_item.group(args.group)

    src_palette = src_group.colors_rgba()
    dst_palette = dst_group.colors_rgba()

    inp = Path(args.input)
    out = Path(args.output)

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
            src_palette=src_palette,
            dst_palette=dst_palette,
            alpha_weight=args.alpha_weight,
            preserve_alpha=not args.no_preserve_alpha,
            min_alpha=args.min_alpha,
            exact_first=not args.no_exact_first,
        )
        LOG.info("Recolored %s -> %s", f.as_posix(), out_path.as_posix())

    return 0


def cmd_normalize(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes)
    changed_any = False

    for p in sorted(palettes_dir.rglob("*.texture-palettes.json")):
        if normalize_palette_json(p):
            changed_any = True
            LOG.info("Normalized %s", p.as_posix())

    if not changed_any:
        LOG.info("No palette files required normalization.")

    return 0


# ----------------------------
# CLI
# ----------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="btg",
        description="Batch Texture Generator (validate/extract/recolor/normalize palettes).",
    )
    p.add_argument(
        "--log", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)."
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser(
        "validate", help="Validate all palette JSON files against local schemas."
    )
    v.add_argument("--schemas", default="schemas", help="Schema directory.")
    v.add_argument("--palettes", default="palettes", help="Palettes directory.")
    v.set_defaults(func=cmd_validate)

    e = sub.add_parser(
        "extract",
        help="Extract RGBA palettes from textures/*.png into palettes/*.json.",
    )
    e.add_argument("--textures", default="textures", help="Textures directory.")
    e.add_argument("--palettes", default="palettes", help="Palettes directory.")
    e.add_argument("--max-colors", type=int, default=32, help="Maximum palette size.")
    e.add_argument(
        "--min-alpha",
        type=int,
        default=1,
        help="Ignore pixels with alpha < this value.",
    )
    e.add_argument(
        "--schema-ref",
        default="../../schemas/texture-palettes.schema.json",
        help="Value to write to $schema in created palette files.",
    )
    e.add_argument(
        "--generator-version",
        default="1.0.0",
        help="Generator version string to include in output.",
    )
    e.set_defaults(func=cmd_extract)

    r = sub.add_parser(
        "recolor", help="Recolor textures_input/ using a source->target palette swap."
    )
    r.add_argument("--palettes", default="palettes", help="Palettes directory.")
    r.add_argument(
        "--src-palette",
        required=True,
        help="Under palettes/: e.g. wood/oak.texture-palettes.json",
    )
    r.add_argument(
        "--dst-palette",
        required=True,
        help="Under palettes/: e.g. metal/iron.texture-palettes.json",
    )
    r.add_argument("--src-id", required=True, help="Source item id (e.g. oak).")
    r.add_argument("--dst-id", required=True, help="Target item id (e.g. iron).")
    r.add_argument(
        "--group",
        default=None,
        help="Group id (default: base if present, else first group).",
    )
    r.add_argument("--input", default="textures_input", help="Input directory.")
    r.add_argument("--output", default="output/textures/item", help="Output directory.")
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
        help="Do not preserve original alpha.",
    )
    r.add_argument(
        "--no-exact-first",
        action="store_true",
        help="Disable exact-match mapping before nearest-color.",
    )
    r.set_defaults(func=cmd_recolor)

    n = sub.add_parser(
        "normalize",
        help="Upgrade palettes to RGBA hex (#RRGGBBAA) and normalize casing.",
    )
    n.add_argument("--palettes", default="palettes", help="Palettes directory.")
    n.set_defaults(func=cmd_normalize)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, str(args.log).upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    # Make relative paths resolve from repo root when run from tools/ in GUI.
    # If launched from elsewhere, keep current working directory.
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

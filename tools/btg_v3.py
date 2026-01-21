from __future__ import annotations

import argparse
import itertools
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from jsonschema import Draft202012Validator
from PIL import Image

try:
    # jsonschema >= 4 can use referencing.Registry for robust $ref resolution
    from referencing import Registry, Resource
except Exception:  # pragma: no cover
    Registry = None  # type: ignore[assignment]
    Resource = None  # type: ignore[assignment]


LOG = logging.getLogger("btg")
RGBA = Tuple[int, int, int, int]


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
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))


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
# Palette models
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
# Template models
# ----------------------------
@dataclass(frozen=True, slots=True)
class SlotSource:
    palette: str  # relative to palettes/
    id: str
    group: str = "base"


@dataclass(frozen=True, slots=True)
class TemplateSlot:
    slot: str  # placeholder name, e.g. {wood}, {metal}, {glass}
    material: str  # material folder name under palettes/
    source: SlotSource
    include_ids: Optional[List[str]] = None
    exclude_ids: Optional[List[str]] = None


@dataclass(frozen=True, slots=True)
class TemplateDef:
    template_id: str
    template_path: str
    output_pattern: str
    slots: List[TemplateSlot]


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


def _rel_posix(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


# ----------------------------
# Schema validation (local refs)
# ----------------------------
def _build_registry(schema_dir: Path) -> Optional["Registry"]:
    if Registry is None or Resource is None:
        return None

    reg = Registry()
    for p in schema_dir.rglob("*.schema.json"):
        doc = load_json(p)
        reg = reg.with_resource(p.as_uri(), Resource.from_contents(doc))
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
# Palette parsing / indexing
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


def load_all_palettes_index(
    palettes_dir: Path,
) -> Dict[str, Dict[str, Tuple[Path, PaletteItem]]]:
    """
    Returns:
      material -> id -> (palette_file_path, item)
    """
    index: Dict[str, Dict[str, Tuple[Path, PaletteItem]]] = {}
    for p in sorted(palettes_dir.rglob("*.texture-palettes.json")):
        try:
            items = parse_palette_file(p)
        except Exception:
            continue
        for it in items:
            index.setdefault(it.material, {})[it.id] = (p, it)
    return index


# ----------------------------
# Palette extraction
# ----------------------------
def extract_palette_from_png(
    png_path: Path, *, max_colors: int = 32, min_alpha: int = 1
) -> List[RGBA]:
    """
    Deterministic palette extraction:
    - If unique colors <= max_colors: return exact set (sorted)
    - Else: quantize to max_colors
    """
    img = Image.open(png_path).convert("RGBA")
    pixels = list(img.getdata())

    uniq = sorted({p for p in pixels if p[3] >= min_alpha})
    if 0 < len(uniq) <= max_colors:
        return uniq

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
# Recolor (single palette swap)
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
# Multi-material helpers
# ----------------------------
def _classify_pixels_for_slots(
    pixels: List[RGBA],
    slot_src_palettes: List[List[RGBA]],
    *,
    alpha_weight: float,
    min_alpha: int,
    exact_first: bool,
) -> Dict[RGBA, Tuple[int, int]]:
    """
    For each unique pixel (alpha >= min_alpha), decide:
      pixel -> (slot_index, src_color_index)
    """
    exact_lookup: Dict[RGBA, Tuple[int, int]] = {}
    if exact_first:
        for si, pal in enumerate(slot_src_palettes):
            for ci, c in enumerate(pal):
                exact_lookup.setdefault(c, (si, ci))

    uniq = {p for p in pixels if p[3] >= min_alpha}
    mapping: Dict[RGBA, Tuple[int, int]] = {}

    for p in uniq:
        m = exact_lookup.get(p)
        if m is not None:
            mapping[p] = m
            continue

        best_slot = 0
        best_idx = 0
        best_d = float("inf")

        for si, pal in enumerate(slot_src_palettes):
            for ci, c in enumerate(pal):
                d = color_dist2(p, c, alpha_weight=alpha_weight)
                if d < best_d:
                    best_d = d
                    best_slot = si
                    best_idx = ci

        mapping[p] = (best_slot, best_idx)

    return mapping


# ----------------------------
# Template parsing
# ----------------------------
def load_template_def(path: Path) -> TemplateDef:
    raw = load_json(path)
    if raw.get("schema") != "btg-template":
        raise ValueError(f"{path}: schema must be 'btg-template'")
    if int(raw.get("version", 0)) < 1:
        raise ValueError(f"{path}: version must be >= 1")

    t = raw.get("template") or {}
    out = raw.get("output") or {}
    slots_raw = raw.get("slots") or []

    slots: List[TemplateSlot] = []
    for s in slots_raw:
        src = s.get("source") or {}
        slots.append(
            TemplateSlot(
                slot=str(s["slot"]),
                material=str(s["material"]),
                source=SlotSource(
                    palette=str(src["palette"]),
                    id=str(src["id"]),
                    group=str(src.get("group") or "base"),
                ),
                include_ids=list(s.get("includeIds") or []) or None,
                exclude_ids=list(s.get("excludeIds") or []) or None,
            )
        )

    if not slots:
        raise ValueError(f"{path}: slots must not be empty")

    template_id = str(t["id"])
    template_path = str(t["path"])
    output_pattern = str(
        out.get("pattern") or f"{{{slots[0].slot}}}_{Path(template_path).stem}.png"
    )

    return TemplateDef(
        template_id=template_id,
        template_path=template_path,
        output_pattern=output_pattern,
        slots=slots,
    )


def _apply_includes_excludes(
    ids: List[str], inc: Optional[List[str]], exc: Optional[List[str]]
) -> List[str]:
    out = ids
    if inc:
        inc_set = set(inc)
        out = [x for x in out if x in inc_set]
    if exc:
        exc_set = set(exc)
        out = [x for x in out if x not in exc_set]
    return out


def _safe_format_pattern(pattern: str, mapping: Dict[str, str]) -> str:
    try:
        return pattern.format(**mapping)
    except KeyError as e:
        raise ValueError(
            f"Pattern '{pattern}' references missing placeholder {e!s}"
        ) from e


# ----------------------------
# Auto-template heuristics
# ----------------------------
def palette_hit_score(template_colors: set[RGBA], palette: List[RGBA]) -> int:
    pal_set = set(palette)
    return sum(1 for c in template_colors if c in pal_set)


def infer_output_pattern(template_id: str, slots: List[str]) -> str:
    # Heuristics tailored to your current template names
    if template_id == "barrel":
        return "{wood}_{metal}_barrel.png"
    if template_id == "keg":
        return "{metal}_keg.png"
    if template_id.endswith("_flask"):
        if template_id in ("large_flask", "medium_flask", "small_flask"):
            size = template_id.split("_", 1)[0]
            return f"{size}_{{wood}}_{{glass}}_flask.png"
        return "{wood}_{glass}_" + template_id + ".png"

    # Generic fallback: {slot...}_{template}.png
    return "_".join("{" + s + "}" for s in slots) + f"_{template_id}.png"


# ----------------------------
# Assets generation (items/models/lang)
# ----------------------------
def _title_from_id(item_id: str) -> str:
    # acacia_copper_barrel -> "Acacia Copper Barrel"
    parts = [p for p in item_id.split("_") if p]
    return " ".join(p[:1].upper() + p[1:] for p in parts)


def _load_lang(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    data = load_json(path)
    if not isinstance(data, dict):
        return {}
    out: Dict[str, str] = {}
    for k, v in data.items():
        if isinstance(k, str):
            out[k] = str(v)
    return out


def _save_lang(path: Path, data: Dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = dict(sorted(data.items(), key=lambda kv: kv[0]))
    path.write_text(
        json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def cmd_assets(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures)
    items_dir = Path(args.items_dir)
    models_dir = Path(args.models_dir)
    lang_path = Path(args.lang)

    namespace = str(args.namespace).strip() or "modid"

    if not textures_dir.exists():
        raise SystemExit(f"Textures dir not found: {textures_dir.as_posix()}")

    # IMPORTANT: only output/textures/item/*.png (non-recursive)
    pngs = sorted(textures_dir.glob("*.png"))
    if not pngs:
        LOG.warning("No PNGs found in %s", textures_dir.as_posix())
        return 0

    lang = _load_lang(lang_path)

    written_items = 0
    written_models = 0
    lang_changes = 0

    for png in pngs:
        item_id = png.stem
        if not item_id:
            continue

        model_loc = f"{namespace}:item/{item_id}"

        item_json = {
            "model": {
                "type": "minecraft:model",
                "model": model_loc,
            }
        }
        model_json = {
            "parent": "item/generated",
            "textures": {"layer0": model_loc},
        }

        item_path = items_dir / f"{item_id}.json"
        model_path = models_dir / f"{item_id}.json"

        if args.dry_run:
            LOG.info("[DRY] Would write %s", item_path.as_posix())
            LOG.info("[DRY] Would write %s", model_path.as_posix())
        else:
            save_json(item_path, item_json)
            save_json(model_path, model_json)
            written_items += 1
            written_models += 1
            LOG.info("Wrote %s", item_path.as_posix())
            LOG.info("Wrote %s", model_path.as_posix())

        lang_key = f"item.{namespace}.{item_id}"
        lang_val = _title_from_id(item_id)

        if args.overwrite_lang or (lang_key not in lang):
            if lang.get(lang_key) != lang_val:
                lang[lang_key] = lang_val
                lang_changes += 1

    if args.dry_run:
        LOG.info("[DRY] Would update %s", lang_path.as_posix())
    else:
        _save_lang(lang_path, lang)
        LOG.info("Updated %s (%d change(s))", lang_path.as_posix(), lang_changes)

    LOG.info(
        "Assets complete: %d item json, %d model json, %d lang change(s).",
        written_items,
        written_models,
        lang_changes,
    )
    return 0


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
            LOG.info("OK %s", p.as_posix())
        except Exception as e:
            ok = False
            LOG.error("FAIL %s\n%s", p.as_posix(), e)

    return 0 if ok else 2


def cmd_extract(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures)
    palettes_dir = Path(args.palettes)
    schema_rel = args.schema_ref

    count = 0
    for png in sorted(textures_dir.rglob("*.png")):
        material = png.parent.name
        item_id = png.stem
        out_path = palettes_dir / material / f"{item_id}.texture-palettes.json"

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
                    "path": f"textures/{material}/{png.name}".replace("\\", "/"),
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
        raw = load_json(p)
        changed = False

        for item in raw.get("items", []):
            groups = item.get("groups") or {}
            for group in groups.values():
                cols = group.get("colors") or []
                new_cols: List[str] = []
                for c in cols:
                    c2 = hex6_to_hex8(str(c))
                    changed |= c2 != str(c)
                    new_cols.append(c2)
                group["colors"] = new_cols

        if changed:
            save_json(p, raw)
            changed_any = True
            LOG.info("Normalized %s", p.as_posix())

    if not changed_any:
        LOG.info("No palette files required normalization.")

    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    templates_dir = Path(args.templates)
    palettes_dir = Path(args.palettes)
    output_dir = Path(args.output)

    palette_index = load_all_palettes_index(palettes_dir)

    template_files = sorted(templates_dir.glob("*.btg-template.json"))
    if not template_files:
        LOG.warning("No templates found in %s", templates_dir.as_posix())
        return 0

    total_written = 0

    for tf in template_files:
        tdef = load_template_def(tf)

        template_png = Path(tdef.template_path)
        if not template_png.exists():
            template_png = (templates_dir / tdef.template_path).resolve()
        if not template_png.exists():
            raise SystemExit(
                f"Template PNG not found: {tdef.template_path} (from {tf.as_posix()})"
            )

        # Build slot sources (palettes present in the template PNG)
        slot_src_palettes: List[List[RGBA]] = []
        slot_choices: List[List[str]] = []

        for slot in tdef.slots:
            material_map = palette_index.get(slot.material, {})
            if not material_map:
                raise SystemExit(
                    f"No palettes found for material '{slot.material}' under {palettes_dir.as_posix()}"
                )

            ids = sorted(material_map.keys())
            ids = _apply_includes_excludes(ids, slot.include_ids, slot.exclude_ids)
            if not ids:
                raise SystemExit(
                    f"After include/exclude, slot '{slot.slot}' has no ids for material '{slot.material}'"
                )

            src_palette_path = palettes_dir / slot.source.palette
            src_items = parse_palette_file(src_palette_path)
            src_item = next((i for i in src_items if i.id == slot.source.id), None)
            if not src_item:
                raise SystemExit(
                    f"Source id '{slot.source.id}' not found in {src_palette_path.as_posix()}"
                )

            src_group = src_item.group(slot.source.group)
            slot_src_palettes.append(src_group.colors_rgba())
            slot_choices.append(ids)

        # Precompute per-pixel classification once per template
        img = Image.open(template_png).convert("RGBA")
        pixels: List[RGBA] = list(img.getdata())
        pixel_class = _classify_pixels_for_slots(
            pixels,
            slot_src_palettes,
            alpha_weight=args.alpha_weight,
            min_alpha=args.min_alpha,
            exact_first=not args.no_exact_first,
        )

        combos: Iterable[Tuple[str, ...]] = itertools.product(*slot_choices)
        if args.limit is not None:
            combos = itertools.islice(combos, int(args.limit))

        for combo in combos:
            mapping = {tdef.slots[i].slot: combo[i] for i in range(len(combo))}
            filename = _safe_format_pattern(tdef.output_pattern, mapping)
            out_path = output_dir / filename

            if args.dry_run:
                LOG.info("[DRY] %s -> %s", template_png.name, out_path.as_posix())
                continue

            # Destination palettes for this combo
            slot_dst_palettes: List[List[RGBA]] = []
            for i, dst_id in enumerate(combo):
                material = tdef.slots[i].material
                _, dst_item = palette_index[material][dst_id]
                _, dst_group = dst_item.default_group()
                slot_dst_palettes.append(dst_group.colors_rgba())

            slot_dst_by_src = [
                build_index_map(src, dst)
                for src, dst in zip(slot_src_palettes, slot_dst_palettes, strict=True)
            ]

            out_pixels: List[RGBA] = []
            for p in pixels:
                if p[3] < args.min_alpha:
                    out_pixels.append(p)
                    continue

                si, ci = pixel_class[p]
                dst = slot_dst_by_src[si][ci]
                if not args.no_preserve_alpha:
                    dst = (dst[0], dst[1], dst[2], p[3])
                out_pixels.append(dst)

            out_img = Image.new("RGBA", img.size)
            out_img.putdata(out_pixels)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_img.save(out_path)

            total_written += 1
            LOG.info("Wrote %s", out_path.as_posix())

    LOG.info("Generate complete: wrote %d file(s).", total_written)
    return 0


def cmd_autotemplate(args: argparse.Namespace) -> int:
    templates_dir = Path(args.templates)
    palettes_dir = Path(args.palettes)
    out_dir = Path(args.out_dir).resolve() if args.out_dir else templates_dir

    palette_index = load_all_palettes_index(palettes_dir)

    pngs = sorted(templates_dir.glob("*.png"))
    if not pngs:
        LOG.warning("No PNG templates found in %s", templates_dir.as_posix())
        return 0

    written = 0
    for png in pngs:
        template_id = png.stem

        img = Image.open(png).convert("RGBA")
        pixels: List[RGBA] = list(img.getdata())
        template_colors: set[RGBA] = {p for p in pixels if p[3] >= args.min_alpha}

        slots: List[Dict[str, Any]] = []
        slot_names: List[str] = []

        for material in (m.strip() for m in args.materials.split(",")):
            if not material:
                continue

            by_id = palette_index.get(material, {})
            if not by_id:
                continue

            best_score = 0
            best_item: Optional[PaletteItem] = None
            best_path: Optional[Path] = None

            for _, (p_path, p_item) in by_id.items():
                _, grp = p_item.default_group()
                score = palette_hit_score(template_colors, grp.colors_rgba())
                if score > best_score:
                    best_score = score
                    best_item = p_item
                    best_path = p_path

            if best_item is None or best_path is None or best_score < args.min_hits:
                continue

            slot_names.append(material)
            slots.append(
                {
                    "slot": material,
                    "material": material,
                    "source": {
                        "palette": _rel_posix(best_path, palettes_dir),
                        "id": best_item.id,
                        "group": "base",
                    },
                }
            )

        if not slots:
            LOG.warning("No slots detected for %s (try lowering --min-hits).", png.name)
            continue

        out_pattern = infer_output_pattern(template_id, slot_names)
        data = {
            "schema": "btg-template",
            "version": 1,
            "template": {"id": template_id, "path": png.as_posix().replace("\\", "/")},
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


# ----------------------------
# CLI
# ----------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="btg", description="Batch Texture Generator.")
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
        help="Value to write to $schema.",
    )
    e.add_argument(
        "--generator-version",
        default="1.0.0",
        help="Generator version string for output.",
    )
    e.set_defaults(func=cmd_extract)

    r = sub.add_parser(
        "recolor",
        help="Single-material recolor for textures_input/ into output/textures/item/.",
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
        "--group", default=None, help="Group id (default: base if present, else first)."
    )
    r.add_argument("--input", default="textures_input", help="Input directory.")
    r.add_argument("--output", default="output/textures/item", help="Output directory.")
    r.add_argument("--min-alpha", type=int, default=1)
    r.add_argument("--alpha-weight", type=float, default=0.25)
    r.add_argument("--no-preserve-alpha", action="store_true")
    r.add_argument("--no-exact-first", action="store_true")
    r.set_defaults(func=cmd_recolor)

    n = sub.add_parser(
        "normalize", help="Normalize palettes (#RRGGBB -> #RRGGBBff) and casing."
    )
    n.add_argument("--palettes", default="palettes", help="Palettes directory.")
    n.set_defaults(func=cmd_normalize)

    g = sub.add_parser(
        "generate", help="Generate all combinations from *.btg-template.json files."
    )
    g.add_argument(
        "--templates",
        default="textures_input",
        help="Directory containing *.btg-template.json + PNGs.",
    )
    g.add_argument("--palettes", default="palettes", help="Palettes directory.")
    g.add_argument("--output", default="output/textures/item", help="Output directory.")
    g.add_argument("--min-alpha", type=int, default=1)
    g.add_argument("--alpha-weight", type=float, default=0.25)
    g.add_argument("--no-preserve-alpha", action="store_true")
    g.add_argument("--no-exact-first", action="store_true")
    g.add_argument(
        "--dry-run", action="store_true", help="List outputs but do not write PNGs."
    )
    g.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of generated outputs per run.",
    )
    g.set_defaults(func=cmd_generate)

    a = sub.add_parser(
        "autotemplate", help="Auto-generate *.btg-template.json from template PNGs."
    )
    a.add_argument("--templates", default="textures_input")
    a.add_argument("--palettes", default="palettes")
    a.add_argument(
        "--out-dir",
        default=None,
        help="Where to write templates (default: templates dir).",
    )
    a.add_argument(
        "--materials",
        default="wood,metal,glass",
        help="Comma list of materials to scan.",
    )
    a.add_argument(
        "--min-alpha", type=int, default=1, help="Minimum alpha to consider a pixel."
    )
    a.add_argument(
        "--min-hits",
        type=int,
        default=2,
        help="Minimum exact palette hits to accept a material.",
    )
    a.add_argument("--dry-run", action="store_true")
    a.set_defaults(func=cmd_autotemplate)

    x = sub.add_parser(
        "assets",
        help="Generate output/items, output/models/item and output/lang/en_us.json from output/textures/item/*.png.",
    )
    x.add_argument(
        "--textures",
        default="output/textures/item",
        help="Textures directory (non-recursive).",
    )
    x.add_argument(
        "--items-dir", default="output/items", help="Output items directory."
    )
    x.add_argument(
        "--models-dir",
        default="output/models/item",
        help="Output models/item directory.",
    )
    x.add_argument(
        "--lang",
        default="output/lang/en_us.json",
        help="Language file to create/update.",
    )
    x.add_argument(
        "--namespace",
        default="modid",
        help="Namespace/modid used in model/texture references.",
    )
    x.add_argument(
        "--overwrite-lang",
        action="store_true",
        help="Overwrite existing lang keys if present.",
    )
    x.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write any files; only log actions.",
    )
    x.set_defaults(func=cmd_assets)

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

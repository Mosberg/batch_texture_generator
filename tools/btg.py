#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# ----------------------------
# Optional deps with friendly errors
# ----------------------------
try:
    from PIL import Image  # type: ignore
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: Pillow (PIL). Install requirements.txt into your venv.\n"
        f"Import error: {e}"
    )

# jsonschema is optional but strongly recommended for validate() on schema-driven formats.
try:
    from jsonschema import Draft202012Validator  # type: ignore
except Exception:  # pragma: no cover
    Draft202012Validator = None  # type: ignore[assignment]

try:
    # jsonschema >= 4 may use referencing.Registry for robust $ref resolution
    from referencing import Registry, Resource  # type: ignore
except Exception:  # pragma: no cover
    Registry = None  # type: ignore[assignment]
    Resource = None  # type: ignore[assignment]

LOG = logging.getLogger("btg")

RGBA = Tuple[int, int, int, int]
HEX6_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
HEX8_RE = re.compile(r"^#[0-9a-fA-F]{8}$")
HEX6_OR_8_RE = re.compile(r"^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


# ----------------------------
# Small utilities
# ----------------------------
def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any, *, sort_keys: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=sort_keys)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def rel_posix(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def is_png(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() == ".png"


def walk_pngs(root: Path, *, recursive: bool = True) -> List[Path]:
    if not root.exists():
        return []
    if root.is_file():
        return [root] if is_png(root) else []
    if recursive:
        return [p for p in sorted(root.rglob("*.png")) if p.is_file()]
    return [p for p in sorted(root.glob("*.png")) if p.is_file()]


# ----------------------------
# Color / hex helpers
# ----------------------------
def hex6_to_hex8(s: str) -> str:
    s = str(s).strip()
    if HEX6_RE.match(s):
        return (s + "ff").lower()
    if HEX8_RE.match(s):
        return s.lower()
    raise ValueError(f"Invalid hex color '{s}' (expected #RRGGBB or #RRGGBBAA)")


def parse_hex8(s: str) -> RGBA:
    s = str(s).strip()
    if not HEX8_RE.match(s):
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
# Palette models (unified)
# ----------------------------
@dataclass(frozen=True, slots=True)
class PaletteGroup:
    colors: List[str]
    comment: str = ""

    def colors_rgba(self) -> List[RGBA]:
        return [parse_hex8(hex6_to_hex8(c)) for c in self.colors]


@dataclass(frozen=True, slots=True)
class PaletteItem:
    """
    Unified palette item.

    - For schema-driven palettes: comes from raw['items'][...]
    - For legacy palettes: 'id' is legacy palette id, groups={'base': ...}
    """

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


@dataclass(frozen=True, slots=True)
class PaletteRef:
    file_path: Path
    item: PaletteItem


def _infer_material_from_path(palette_path: Path) -> str:
    # expected: palettes/<material>/<file>.texture-palettes.json
    parent = palette_path.parent.name
    return parent or "unknown"


# ----------------------------
# Palette parsing (schema-driven + legacy)
# ----------------------------
def parse_palette_file_any(palette_path: Path) -> List[PaletteItem]:
    raw = load_json(palette_path)

    # A) New schema-driven (btg-newest style)
    if isinstance(raw, dict) and raw.get("schema") == "texture-palettes":
        items_raw = raw.get("items") or []
        if not isinstance(items_raw, list):
            raise ValueError(f"{palette_path}: 'items' must be a list")

        out: List[PaletteItem] = []
        for it in items_raw:
            if not isinstance(it, dict):
                continue
            groups: Dict[str, PaletteGroup] = {}
            groups_raw = it.get("groups") or {}
            if isinstance(groups_raw, dict):
                for gid, g in groups_raw.items():
                    if not isinstance(g, dict):
                        continue
                    cols = g.get("colors") or []
                    if not isinstance(cols, list):
                        cols = []
                    groups[str(gid)] = PaletteGroup(
                        colors=[hex6_to_hex8(str(c)) for c in cols],
                        comment=str(g.get("comment") or ""),
                    )
            out.append(
                PaletteItem(
                    id=str(it["id"]),
                    name=str(it.get("name") or str(it["id"])),
                    path=str(it.get("path") or ""),
                    material=str(
                        it.get("material") or _infer_material_from_path(palette_path)
                    ),
                    groups=groups,
                    metadata=it.get("metadata"),
                )
            )
        return out

    # B) Legacy flexible shapes (btg.py older style)
    #    Supported shapes:
    #    1) {"palettes": {"oak": ["#..."], "spruce": [...]}}
    #    2) {"palettes": [{"id":"oak","colors":[...]}]}
    #    3) {"id":"oak","colors":[...]}  (single)
    if isinstance(raw, dict) and isinstance(raw.get("palettes"), dict):
        material = _infer_material_from_path(palette_path)
        items: List[PaletteItem] = []
        for pid, colors in raw["palettes"].items():
            if not isinstance(pid, str) or not isinstance(colors, list):
                continue
            groups = {
                "base": PaletteGroup(colors=[hex6_to_hex8(str(c)) for c in colors])
            }
            items.append(
                PaletteItem(
                    id=pid,
                    name=pid.replace("_", " ").title(),
                    path="",
                    material=material,
                    groups=groups,
                )
            )
        return items

    if isinstance(raw, dict) and isinstance(raw.get("palettes"), list):
        material = _infer_material_from_path(palette_path)
        items = []
        for entry in raw["palettes"]:
            if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
                continue
            cols = entry.get("colors") or []
            if not isinstance(cols, list):
                cols = []
            groups = {"base": PaletteGroup(colors=[hex6_to_hex8(str(c)) for c in cols])}
            pid = str(entry["id"])
            items.append(
                PaletteItem(
                    id=pid,
                    name=str(entry.get("name") or pid.replace("_", " ").title()),
                    path=str(entry.get("path") or ""),
                    material=str(entry.get("material") or material),
                    groups=groups,
                    metadata=entry.get("metadata"),
                )
            )
        return items

    if (
        isinstance(raw, dict)
        and isinstance(raw.get("id"), str)
        and isinstance(raw.get("colors"), list)
    ):
        material = _infer_material_from_path(palette_path)
        pid = str(raw["id"])
        cols = raw.get("colors") or []
        groups = {"base": PaletteGroup(colors=[hex6_to_hex8(str(c)) for c in cols])}
        return [
            PaletteItem(
                id=pid,
                name=str(raw.get("name") or pid.replace("_", " ").title()),
                path=str(raw.get("path") or ""),
                material=str(raw.get("material") or material),
                groups=groups,
                metadata=raw.get("metadata"),
            )
        ]

    raise ValueError(
        f"{palette_path}: Unsupported palette file format. "
        "Expected schema-driven (schema='texture-palettes') or legacy palettes shape."
    )


def load_all_palettes_index(palettes_dir: Path) -> Dict[str, Dict[str, PaletteRef]]:
    """
    Returns material -> id -> PaletteRef(file_path, item)
    """
    index: Dict[str, Dict[str, PaletteRef]] = {}
    for p in sorted(palettes_dir.rglob("*.texture-palettes.json")):
        try:
            items = parse_palette_file_any(p)
        except Exception as e:
            LOG.debug("Skipping palette file %s (%s)", p.as_posix(), e)
            continue
        for it in items:
            index.setdefault(it.material, {})[it.id] = PaletteRef(file_path=p, item=it)
    return index


def find_palette_item(
    palettes_dir: Path,
    rel_palette_path: str,
    item_id: str,
) -> PaletteItem:
    p = (palettes_dir / rel_palette_path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Palette file not found: {p.as_posix()}")
    items = parse_palette_file_any(p)
    it = next((x for x in items if x.id == item_id), None)
    if it is None:
        raise KeyError(f"Item id '{item_id}' not found in {p.as_posix()}")
    return it


# ----------------------------
# Schema validation helpers
# ----------------------------
def build_registry(schema_dir: Path) -> Optional["Registry"]:
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


def schema_validate(
    instance_path: Path, schema_path: Path, schema_dir: Path
) -> List[str]:
    """
    Returns list of error strings. Empty if valid.
    """
    if Draft202012Validator is None:
        return [
            f"jsonschema is not installed; cannot validate {instance_path.as_posix()} against schema."
        ]

    schema = load_json(schema_path)
    instance = load_json(instance_path)
    registry = build_registry(schema_dir)
    validator = (
        Draft202012Validator(schema, registry=registry)
        if registry is not None
        else Draft202012Validator(schema)
    )
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    out: List[str] = []
    for e in errors[:100]:
        loc = "$" + ("." + ".".join(map(str, e.path)) if e.path else "")
        out.append(f"{loc}: {e.message}")
    if len(errors) > 100:
        out.append(f"...and {len(errors) - 100} more")
    return out


# ----------------------------
# Palette extraction
# ----------------------------
def extract_palette_from_png(
    png_path: Path, *, max_colors: int = 32, min_alpha: int = 1
) -> List[RGBA]:
    """
    Deterministic-ish palette extraction:
    - If unique colors <= max_colors: return exact unique colors (sorted).
    - Else: quantize to max_colors, return the used colors (sorted).
    """
    img = Image.open(png_path).convert("RGBA")
    pixels = list(img.getdata())
    uniq = sorted({p for p in pixels if p[3] >= min_alpha})

    if 0 < len(uniq) <= max_colors:
        return uniq

    # Quantize fallback for big palettes
    q = img.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette() or []
    used = sorted(set(q.getdata()))
    out: List[RGBA] = []
    for idx in used:
        base = idx * 3
        if base + 2 >= len(pal):
            continue
        r = pal[base + 0]
        g = pal[base + 1]
        b = pal[base + 2]
        out.append((r, g, b, 255))
    return out[:max_colors]


# ----------------------------
# Recolor helpers
# ----------------------------
def build_index_map(src: List[RGBA], dst: List[RGBA]) -> List[RGBA]:
    """
    Map src indices to dst indices by scaling across lengths.
    Example: src len 4, dst len 8 => src[0]->dst[0], src[3]->dst[7], etc.
    """
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
    ensure_dir(output_png.parent)
    img.save(output_png)


def classify_pixels_for_slots(
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
                # first wins so templates can intentionally share colors
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
# Template formats
# ----------------------------
@dataclass(frozen=True, slots=True)
class SlotSource:
    palette: str  # relative to palettes/ (or absolute)
    id: str
    group: str = "base"


@dataclass(frozen=True, slots=True)
class TemplateSlot:
    slot: str  # placeholder name, e.g. wood, metal, glass (used in pattern)
    material: str  # palette index category (folder/material)
    source: SlotSource
    include_ids: Optional[List[str]] = None
    exclude_ids: Optional[List[str]] = None


@dataclass(frozen=True, slots=True)
class TemplateDef:
    template_id: str
    template_path: str
    output_pattern: str
    slots: List[TemplateSlot]


# Legacy task format (older btg.py)
@dataclass(frozen=True, slots=True)
class LegacySwap:
    src_palette: str
    src_id: str
    dst_palette: str
    dst_id: str


@dataclass(frozen=True, slots=True)
class LegacyTask:
    kind: str  # "item" or "block"
    base_texture: str
    output_id: str
    display_name: str
    swaps: List[LegacySwap]
    item_group_id: Optional[str] = None
    item_group_name: Optional[str] = None
    block_model_template: Optional[str] = None
    blockstate_template: Optional[str] = None


def apply_includes_excludes(
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


def safe_format_pattern(pattern: str, mapping: Dict[str, str]) -> str:
    try:
        return pattern.format(**mapping)
    except KeyError as e:
        raise ValueError(
            f"Pattern '{pattern}' references missing placeholder {e!s}"
        ) from e


def infer_output_pattern(template_id: str, slots: List[str]) -> str:
    # Heuristics aligned to your current template names (keg/barrel/flasks).
    if template_id == "barrel":
        return "{wood}_{metal}_barrel.png"
    if template_id == "keg":
        return "{metal}_keg.png"
    if template_id.endswith("_flask"):
        if template_id in ("big_flask", "medium_flask", "small_flask"):
            size = template_id.split("_", 1)[0]
            return f"{size}_{{wood}}_{{glass}}_flask.png"
        return "{wood}_{glass}_" + template_id + ".png"
    return "_".join("{" + s + "}" for s in slots) + f"_{template_id}.png"


def load_template_def(path: Path) -> TemplateDef:
    raw = load_json(path)
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: template must be a JSON object")

    # New schema-driven template
    if raw.get("schema") == "btg-template":
        if int(raw.get("version", 0)) < 1:
            raise ValueError(f"{path}: version must be >= 1")
        t = raw.get("template") or {}
        out = raw.get("output") or {}
        slots_raw = raw.get("slots") or []
        if not isinstance(slots_raw, list) or not slots_raw:
            raise ValueError(f"{path}: slots must not be empty")

        slots: List[TemplateSlot] = []
        for s in slots_raw:
            if not isinstance(s, dict):
                continue
            src = s.get("source") or {}
            slots.append(
                TemplateSlot(
                    slot=str(s["slot"]).strip("{}"),  # tolerate "{wood}" or "wood"
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

        template_id = str((t.get("id") or path.stem))
        template_path = str(t.get("path") or "")
        if not template_path:
            raise ValueError(f"{path}: template.path is required")
        output_pattern = str(
            out.get("pattern")
            or infer_output_pattern(template_id, [x.slot for x in slots])
        )

        return TemplateDef(
            template_id=template_id,
            template_path=template_path,
            output_pattern=output_pattern,
            slots=slots,
        )

    raise ValueError(
        f"{path}: not a schema-driven btg-template (schema='btg-template'). "
        "Legacy templates are handled via cmd_recolor_templates (older task format)."
    )


def parse_legacy_task_templates(path: Path) -> List[LegacyTask]:
    """
    Legacy parser for *.btg-template.json used by older btg.py:
    Supports:
      A) {"tasks":[{...}, {...}]}
      B) {...single task...}
    """
    raw = load_json(path)
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: legacy template must be JSON object")

    # If it's actually the new schema-driven template, don't parse as legacy.
    if raw.get("schema") == "btg-template":
        raise ValueError(f"{path}: schema-driven template; use generate command")

    def parse_one(obj: Dict[str, Any]) -> LegacyTask:
        kind = str(obj.get("kind", "item"))
        base_texture = str(obj.get("base_texture") or obj.get("texture") or "")
        if not base_texture:
            raise ValueError(f"{path}: missing base_texture")
        output_id = str(
            obj.get("output_id") or obj.get("id") or Path(base_texture).stem
        )
        display_name = str(
            obj.get("display_name") or obj.get("name") or title_from_id(output_id)
        )

        swaps_raw = obj.get("swaps") or []
        if not isinstance(swaps_raw, list):
            raise ValueError(f"{path}: swaps must be a list")
        swaps: List[LegacySwap] = []
        for s in swaps_raw:
            if not isinstance(s, dict):
                raise ValueError(f"{path}: swap entries must be objects")
            swaps.append(
                LegacySwap(
                    src_palette=str(s["src_palette"]),
                    src_id=str(s["src_id"]),
                    dst_palette=str(s["dst_palette"]),
                    dst_id=str(s["dst_id"]),
                )
            )

        return LegacyTask(
            kind=kind,
            base_texture=base_texture,
            output_id=output_id,
            display_name=display_name,
            swaps=swaps,
            item_group_id=str(obj["item_group_id"]) if "item_group_id" in obj else None,
            item_group_name=(
                str(obj["item_group_name"]) if "item_group_name" in obj else None
            ),
            block_model_template=(
                str(obj["block_model_template"])
                if "block_model_template" in obj
                else None
            ),
            blockstate_template=(
                str(obj["blockstate_template"])
                if "blockstate_template" in obj
                else None
            ),
        )

    if isinstance(raw.get("tasks"), list):
        return [parse_one(t) for t in raw["tasks"] if isinstance(t, dict)]
    return [parse_one(raw)]


# ----------------------------
# Vanilla-ish JSON generators (items/models/lang/blockstates)
# ----------------------------
def title_from_id(s: str) -> str:
    s = s.replace(":", "_").replace("/", "_").replace("-", "_")
    parts = [p for p in s.split("_") if p]
    return " ".join(p[:1].upper() + p[1:] for p in parts)


def minecraft_item_model(namespace: str, item_id: str) -> Dict[str, Any]:
    return {
        "parent": "item/generated",
        "textures": {"layer0": f"{namespace}:item/{item_id}"},
    }


def minecraft_item_definition(namespace: str, item_id: str) -> Dict[str, Any]:
    # 1.21+ items/ format (simple forwarding file)
    return {
        "model": {"type": "minecraft:model", "model": f"{namespace}:item/{item_id}"}
    }


def minecraft_block_model_cube_all(namespace: str, block_id: str) -> Dict[str, Any]:
    return {
        "parent": "minecraft:block/cube_all",
        "textures": {"all": f"{namespace}:block/{block_id}"},
    }


def minecraft_blockstate_facing(
    namespace: str, block_id: str, model_ref: Optional[str] = None
) -> Dict[str, Any]:
    # Simple facing variants
    m = model_ref or f"{namespace}:block/{block_id}"
    return {
        "variants": {
            "facing=north": {"model": m, "y": 0},
            "facing=east": {"model": m, "y": 90},
            "facing=south": {"model": m, "y": 180},
            "facing=west": {"model": m, "y": 270},
        }
    }


def merge_lang(
    existing: Optional[Dict[str, Any]], updates: Dict[str, str]
) -> Dict[str, Any]:
    out: Dict[str, Any] = dict(existing or {})
    out.update(updates)
    return out


def walk_json_mutate(obj: Any, fn) -> Any:
    if isinstance(obj, dict):
        return {k: walk_json_mutate(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_json_mutate(v, fn) for v in obj]
    return fn(obj)


def rewrite_namespace_strings(data: Any, *, old_ns: str = "modid", new_ns: str) -> Any:
    """
    Best-effort rewrite of common namespace string patterns in block model/blockstate templates.
    """

    def repl(v: Any) -> Any:
        if not isinstance(v, str):
            return v
        # modid:foo -> new:foo
        v2 = v.replace(f"{old_ns}:", f"{new_ns}:")
        # modid/foo -> new/foo
        v2 = v2.replace(f"{old_ns}/", f"{new_ns}/")
        return v2

    return walk_json_mutate(data, repl)


# ----------------------------
# Output layout helpers
# ----------------------------
@dataclass(frozen=True, slots=True)
class OutputLayout:
    """
    Two write targets (can enable one or both):
      - "modid tree": output/<namespace>/textures/item/..., etc.
      - "flat tree":  output/textures/item/..., etc.
    """

    out_root: Path
    namespace: str
    write_modid_tree: bool
    write_flat_tree: bool

    def bases(self) -> List[Tuple[str, Path]]:
        out: List[Tuple[str, Path]] = []
        if self.write_modid_tree:
            out.append(("modid", self.out_root / self.namespace))
        if self.write_flat_tree:
            out.append(("flat", self.out_root))
        return out


def write_item_outputs(
    layout: OutputLayout,
    *,
    item_id: str,
    display_name: str,
    texture_png: Image.Image,
    lang_file: str = "en_us.json",
    generate_items_json: bool = True,
    generate_models_json: bool = True,
    generate_lang: bool = True,
    dry_run: bool = False,
) -> None:
    for tag, base in layout.bases():
        tex_path = base / "textures" / "item" / f"{item_id}.png"
        model_path = base / "models" / "item" / f"{item_id}.json"
        item_def_path = base / "items" / f"{item_id}.json"
        lang_path = base / "lang" / lang_file

        if dry_run:
            LOG.info("[DRY:%s] Would write %s", tag, tex_path.as_posix())
        else:
            ensure_dir(tex_path.parent)
            texture_png.save(tex_path)

        if generate_models_json:
            if dry_run:
                LOG.info("[DRY:%s] Would write %s", tag, model_path.as_posix())
            else:
                save_json(model_path, minecraft_item_model(layout.namespace, item_id))

        if generate_items_json:
            if dry_run:
                LOG.info("[DRY:%s] Would write %s", tag, item_def_path.as_posix())
            else:
                save_json(
                    item_def_path, minecraft_item_definition(layout.namespace, item_id)
                )

        if generate_lang:
            existing = (
                load_json(lang_path) if (not dry_run and lang_path.exists()) else {}
            )
            updates = {f"item.{layout.namespace}.{item_id}": display_name}
            merged = merge_lang(existing, updates)
            if dry_run:
                LOG.info("[DRY:%s] Would update %s", tag, lang_path.as_posix())
            else:
                save_json(lang_path, merged, sort_keys=True)


def write_block_outputs(
    layout: OutputLayout,
    *,
    block_id: str,
    display_name: str,
    texture_png: Image.Image,
    block_model_json: Optional[Dict[str, Any]] = None,
    blockstate_json: Optional[Dict[str, Any]] = None,
    lang_file: str = "en_us.json",
    dry_run: bool = False,
) -> None:
    for tag, base in layout.bases():
        tex_path = base / "textures" / "block" / f"{block_id}.png"
        model_path = base / "models" / "block" / f"{block_id}.json"
        blockstates_path = base / "blockstates" / f"{block_id}.json"
        lang_path = base / "lang" / lang_file

        if dry_run:
            LOG.info("[DRY:%s] Would write %s", tag, tex_path.as_posix())
        else:
            ensure_dir(tex_path.parent)
            texture_png.save(tex_path)

        # If not provided, fall back to cube_all + simple facing
        model = block_model_json or minecraft_block_model_cube_all(
            layout.namespace, block_id
        )
        bs = blockstate_json or minecraft_blockstate_facing(layout.namespace, block_id)

        if dry_run:
            LOG.info("[DRY:%s] Would write %s", tag, model_path.as_posix())
            LOG.info("[DRY:%s] Would write %s", tag, blockstates_path.as_posix())
        else:
            save_json(model_path, model)
            save_json(blockstates_path, bs)

        existing = load_json(lang_path) if (not dry_run and lang_path.exists()) else {}
        updates = {f"block.{layout.namespace}.{block_id}": display_name}
        merged = merge_lang(existing, updates)
        if dry_run:
            LOG.info("[DRY:%s] Would update %s", tag, lang_path.as_posix())
        else:
            save_json(lang_path, merged, sort_keys=True)


# ----------------------------
# Command: normalize
# ----------------------------
def cmd_normalize(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes or "palettes")
    files = sorted(palettes_dir.rglob("*.texture-palettes.json"))
    if not files:
        LOG.warning("No palette files found under %s", palettes_dir.as_posix())
        return 0

    changed_count = 0
    for p in files:
        try:
            raw = load_json(p)
        except Exception as e:
            LOG.error("Failed to read %s (%s)", p.as_posix(), e)
            continue

        changed = False

        # New schema-driven
        if isinstance(raw, dict) and raw.get("schema") == "texture-palettes":
            for item in (
                raw.get("items", []) if isinstance(raw.get("items"), list) else []
            ):
                if not isinstance(item, dict):
                    continue
                groups = item.get("groups") or {}
                if not isinstance(groups, dict):
                    continue
                for group in groups.values():
                    if not isinstance(group, dict):
                        continue
                    cols = group.get("colors") or []
                    if not isinstance(cols, list):
                        continue
                    new_cols: List[str] = []
                    for c in cols:
                        c_str = str(c)
                        if HEX6_OR_8_RE.match(c_str.strip()):
                            c2 = hex6_to_hex8(c_str)
                            if c2 != c_str:
                                changed = True
                            new_cols.append(c2)
                        else:
                            new_cols.append(c_str)
                    group["colors"] = new_cols

        else:
            # Legacy: walk and normalize any "#RRGGBB" or "#RRGGBBAA"
            def norm_scalar(v: Any) -> Any:
                if isinstance(v, str) and HEX6_OR_8_RE.match(v.strip()):
                    try:
                        return hex6_to_hex8(v)
                    except Exception:
                        return v
                return v

            normalized = walk_json_mutate(raw, norm_scalar)
            if normalized != raw:
                raw = normalized
                changed = True

        if changed:
            if args.dry_run:
                LOG.info("[DRY] Would normalize %s", p.as_posix())
            else:
                save_json(p, raw)
                LOG.info("Normalized %s", p.as_posix())
            changed_count += 1

    LOG.info("Normalize complete: %d/%d file(s) changed.", changed_count, len(files))
    return 0


# ----------------------------
# Command: validate
# ----------------------------
def cmd_validate(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes or "palettes")
    schemas_dir = Path(args.schemas or "schemas")

    files = sorted(palettes_dir.rglob("*.texture-palettes.json"))
    if not files:
        LOG.warning("No palette files found under %s", palettes_dir.as_posix())
        return 0

    schema_path = schemas_dir / "texture-palettes.schema.json"
    ok = True

    for p in files:
        try:
            raw = load_json(p)
        except Exception as e:
            ok = False
            LOG.error("FAIL %s (invalid JSON: %s)", p.as_posix(), e)
            continue

        # If schema-driven and schema exists, validate structure
        if (
            isinstance(raw, dict)
            and raw.get("schema") == "texture-palettes"
            and schema_path.exists()
        ):
            errs = schema_validate(p, schema_path, schemas_dir)
            if errs and not (
                len(errs) == 1 and errs[0].startswith("jsonschema is not installed")
            ):
                ok = False
                LOG.error("FAIL %s\n%s", p.as_posix(), "\n".join(errs))
                continue

        # Semantic checks: all colors must be hex8 after normalization
        try:
            items = parse_palette_file_any(p)
            if not items:
                raise ValueError("No palette items parsed.")
            for it in items:
                for gid, grp in it.groups.items():
                    for c in grp.colors:
                        c8 = hex6_to_hex8(c)
                        if not HEX8_RE.match(c8):
                            raise ValueError(f"{it.id}.{gid}: invalid color {c!r}")
        except Exception as e:
            ok = False
            LOG.error("FAIL %s (%s)", p.as_posix(), e)
            continue

        LOG.info("OK %s", p.as_posix())

    return 0 if ok else 2


# ----------------------------
# Command: extract
# ----------------------------
def cmd_extract(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures or "textures")
    palettes_dir = Path(args.palettes or "palettes")
    schema_ref = str(args.schema_ref or "../../schemas/texture-palettes.schema.json")
    max_colors = int(args.max_colors or 32)
    min_alpha = int(args.min_alpha or 1)
    generator_version = str(args.generator_version or "1.0.0")
    dry_run = bool(args.dry_run)

    pngs = [p for p in sorted(textures_dir.rglob("*.png")) if p.is_file()]
    if not pngs:
        LOG.warning("No textures found under %s", textures_dir.as_posix())
        return 0

    count = 0
    for png in pngs:
        material = png.parent.name or "unknown"
        item_id = png.stem
        out_path = palettes_dir / material / f"{item_id}.texture-palettes.json"
        colors = extract_palette_from_png(
            png, max_colors=max_colors, min_alpha=min_alpha
        )

        payload: Dict[str, Any] = {
            "$schema": schema_ref,
            "schema": "texture-palettes",
            "version": 1,
            "generator": {"name": "btg", "version": generator_version},
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

        if dry_run:
            LOG.info("[DRY] Would write %s", out_path.as_posix())
        else:
            save_json(out_path, payload)
            LOG.info("Wrote %s", out_path.as_posix())
        count += 1

    LOG.info("Extract complete (%d file(s)).", count)
    return 0


# ----------------------------
# Command: recolor (single swap)
# ----------------------------
def cmd_recolor(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes or "palettes")
    src_palette_rel = str(args.src_palette)
    dst_palette_rel = str(args.dst_palette)
    src_id = str(args.src_id)
    dst_id = str(args.dst_id)

    group = args.group  # optional; if None -> default group of each item

    input_dir = Path(args.input or "textures_input")
    output_dir = Path(args.output or "output/textures/item")
    recursive = not bool(args.no_recursive)
    alpha_weight = float(args.alpha_weight or 0.25)
    preserve_alpha = not bool(args.no_preserve_alpha)
    exact_first = not bool(args.no_exact_first)
    min_alpha = int(args.min_alpha or 1)
    dry_run = bool(args.dry_run)

    src_item = find_palette_item(palettes_dir, src_palette_rel, src_id)
    dst_item = find_palette_item(palettes_dir, dst_palette_rel, dst_id)

    if group is None:
        _, src_grp = src_item.default_group()
        _, dst_grp = dst_item.default_group()
    else:
        src_grp = src_item.group(str(group))
        dst_grp = dst_item.group(str(group))

    src_palette = src_grp.colors_rgba()
    dst_palette = dst_grp.colors_rgba()

    files = walk_pngs(input_dir, recursive=recursive)
    if not files:
        LOG.warning("No PNG files found in %s", input_dir.as_posix())
        return 0

    for f in files:
        rel = f.relative_to(input_dir) if input_dir.is_dir() else Path(f.name)
        out_path = output_dir / rel
        if dry_run:
            LOG.info("[DRY] Would recolor %s -> %s", f.as_posix(), out_path.as_posix())
            continue
        recolor_png(
            f,
            out_path,
            src_palette=src_palette,
            dst_palette=dst_palette,
            alpha_weight=alpha_weight,
            preserve_alpha=preserve_alpha,
            min_alpha=min_alpha,
            exact_first=exact_first,
        )
        LOG.info("Recolored %s -> %s", f.as_posix(), out_path.as_posix())

    return 0


# ----------------------------
# Command: recolor-templates (legacy task templates with asset output)
# ----------------------------
def cmd_recolor_templates(args: argparse.Namespace) -> int:
    palettes_dir = Path(args.palettes or "palettes")
    templates_dir = Path(args.templates or "textures_input")
    out_root = Path(args.output_root or "output")
    namespace = str(args.namespace or "modid")
    lang_file = str(args.lang_file or "en_us.json")
    write_modid_tree = not bool(args.no_modid_tree)
    write_flat_tree = not bool(args.no_flat_tree)
    dry_run = bool(args.dry_run)

    template_files = sorted(templates_dir.rglob("*.btg-template.json"))
    if not template_files:
        LOG.warning(
            "No legacy *.btg-template.json found under %s", templates_dir.as_posix()
        )
        return 0

    layout = OutputLayout(
        out_root=out_root,
        namespace=namespace,
        write_modid_tree=write_modid_tree,
        write_flat_tree=write_flat_tree,
    )

    total = 0
    for tf in template_files:
        try:
            tasks = parse_legacy_task_templates(tf)
        except Exception as e:
            # Skip schema-driven templates (handled by generate)
            LOG.debug("Skipping %s (%s)", tf.as_posix(), e)
            continue

        base_dir = tf.parent
        for t in tasks:
            base_texture = (
                (base_dir / t.base_texture).resolve()
                if not Path(t.base_texture).is_absolute()
                else Path(t.base_texture)
            )
            if not base_texture.exists():
                raise SystemExit(
                    f"Legacy template refers to missing texture: {base_texture.as_posix()}"
                )

            img = Image.open(base_texture).convert("RGBA")
            pixels: List[RGBA] = list(img.getdata())

            # Apply swaps sequentially (last wins), by exact palette mapping only.
            # (Legacy format is intended for exact palette colors.)
            for s in t.swaps:
                src_item = find_palette_item(palettes_dir, s.src_palette, s.src_id)
                dst_item = find_palette_item(palettes_dir, s.dst_palette, s.dst_id)
                _, src_grp = src_item.default_group()
                _, dst_grp = dst_item.default_group()
                src_pal = src_grp.colors_rgba()
                dst_pal = dst_grp.colors_rgba()
                dst_by_src = build_index_map(src_pal, dst_pal)
                exact = {src_pal[i]: dst_by_src[i] for i in range(len(src_pal))}

                new_pixels: List[RGBA] = []
                for p in pixels:
                    m = exact.get(p)
                    new_pixels.append(m if m is not None else p)
                pixels = new_pixels

            out_img = Image.new("RGBA", img.size)
            out_img.putdata(pixels)

            if t.kind == "block":
                block_model_json: Optional[Dict[str, Any]] = None
                blockstate_json: Optional[Dict[str, Any]] = None

                if t.block_model_template:
                    tmpl_path = (
                        (base_dir / t.block_model_template).resolve()
                        if not Path(t.block_model_template).is_absolute()
                        else Path(t.block_model_template)
                    )
                    if tmpl_path.exists():
                        block_model_json = rewrite_namespace_strings(
                            load_json(tmpl_path), new_ns=namespace
                        )
                if t.blockstate_template:
                    tmpl_path = (
                        (base_dir / t.blockstate_template).resolve()
                        if not Path(t.blockstate_template).is_absolute()
                        else Path(t.blockstate_template)
                    )
                    if tmpl_path.exists():
                        blockstate_json = rewrite_namespace_strings(
                            load_json(tmpl_path), new_ns=namespace
                        )

                write_block_outputs(
                    layout,
                    block_id=t.output_id,
                    display_name=t.display_name,
                    texture_png=out_img,
                    block_model_json=block_model_json,
                    blockstate_json=blockstate_json,
                    lang_file=lang_file,
                    dry_run=dry_run,
                )
            else:
                # item
                write_item_outputs(
                    layout,
                    item_id=t.output_id,
                    display_name=t.display_name,
                    texture_png=out_img,
                    lang_file=lang_file,
                    generate_items_json=True,
                    generate_models_json=True,
                    generate_lang=True,
                    dry_run=dry_run,
                )

            total += 1

    LOG.info("Legacy recolor-templates complete: %d task(s).", total)
    return 0


# ----------------------------
# Command: generate (schema-driven multi-slot templates)
# ----------------------------
def cmd_generate(args: argparse.Namespace) -> int:
    templates_dir = Path(args.templates or "textures_input")
    palettes_dir = Path(args.palettes or "palettes")
    output_dir = Path(args.output or "output/textures/item")
    alpha_weight = float(args.alpha_weight or 0.25)
    min_alpha = int(args.min_alpha or 1)
    preserve_alpha = not bool(args.no_preserve_alpha)
    exact_first = not bool(args.no_exact_first)
    dry_run = bool(args.dry_run)
    limit = int(args.limit) if args.limit is not None else None

    palette_index = load_all_palettes_index(palettes_dir)

    template_files = sorted(templates_dir.rglob("*.btg-template.json"))
    if not template_files:
        LOG.warning(
            "No schema-driven templates found under %s", templates_dir.as_posix()
        )
        return 0

    total_written = 0

    for tf in template_files:
        try:
            tdef = load_template_def(tf)
        except Exception:
            continue  # ignore legacy templates here

        template_png = Path(tdef.template_path)
        if not template_png.is_absolute():
            # allow paths relative to the template file folder
            cand = (tf.parent / tdef.template_path).resolve()
            template_png = cand
        if not template_png.exists():
            raise SystemExit(
                f"Template PNG not found: {tdef.template_path} (from {tf.as_posix()})"
            )

        # Build slot sources: src palettes (from source palette + id + group)
        slot_src_palettes: List[List[RGBA]] = []
        slot_choices: List[List[str]] = []

        for slot in tdef.slots:
            material_map = palette_index.get(slot.material, {})
            if not material_map:
                raise SystemExit(
                    f"No palettes found for material '{slot.material}' under {palettes_dir.as_posix()}"
                )

            ids = sorted(material_map.keys())
            ids = apply_includes_excludes(ids, slot.include_ids, slot.exclude_ids)
            if not ids:
                raise SystemExit(
                    f"After include/exclude, slot '{slot.slot}' has no ids for material '{slot.material}'"
                )

            src_palette_path = Path(slot.source.palette)
            if not src_palette_path.is_absolute():
                src_palette_path = (palettes_dir / slot.source.palette).resolve()
            if not src_palette_path.exists():
                raise SystemExit(
                    f"Slot source palette not found: {src_palette_path.as_posix()}"
                )

            src_items = parse_palette_file_any(src_palette_path)
            src_item = next((i for i in src_items if i.id == slot.source.id), None)
            if not src_item:
                raise SystemExit(
                    f"Source id '{slot.source.id}' not found in {src_palette_path.as_posix()}"
                )
            src_group = (
                src_item.group(slot.source.group)
                if slot.source.group
                else src_item.default_group()[1]
            )
            slot_src_palettes.append(src_group.colors_rgba())
            slot_choices.append(ids)

        # Precompute per-pixel classification once per template
        img = Image.open(template_png).convert("RGBA")
        pixels: List[RGBA] = list(img.getdata())
        pixel_class = classify_pixels_for_slots(
            pixels,
            slot_src_palettes,
            alpha_weight=alpha_weight,
            min_alpha=min_alpha,
            exact_first=exact_first,
        )

        combos: Iterable[Tuple[str, ...]] = itertools.product(*slot_choices)
        if limit is not None:
            combos = itertools.islice(combos, int(limit))

        for combo in combos:
            mapping = {tdef.slots[i].slot: combo[i] for i in range(len(combo))}
            filename = safe_format_pattern(tdef.output_pattern, mapping)
            out_path = output_dir / filename

            if dry_run:
                LOG.info("[DRY] %s -> %s", template_png.name, out_path.as_posix())
                total_written += 1
                continue

            # Destination palettes for this combo (default group)
            slot_dst_palettes: List[List[RGBA]] = []
            for i, dst_id in enumerate(combo):
                material = tdef.slots[i].material
                ref = palette_index[material][dst_id]
                _, grp = ref.item.default_group()
                slot_dst_palettes.append(grp.colors_rgba())

            slot_dst_by_src = [
                build_index_map(src, dst)
                for src, dst in zip(slot_src_palettes, slot_dst_palettes, strict=True)
            ]

            out_pixels: List[RGBA] = []
            for p in pixels:
                if p[3] < min_alpha:
                    out_pixels.append(p)
                    continue
                si, ci = pixel_class[p]
                dst = slot_dst_by_src[si][ci]
                if preserve_alpha:
                    dst = (dst[0], dst[1], dst[2], p[3])
                out_pixels.append(dst)

            out_img = Image.new("RGBA", img.size)
            out_img.putdata(out_pixels)
            ensure_dir(out_path.parent)
            out_img.save(out_path)

            total_written += 1
            LOG.info("Wrote %s", out_path.as_posix())

    LOG.info("Generate complete: wrote %d file(s).", total_written)
    return 0


# ----------------------------
# Command: autotemplate (schema-driven)
# ----------------------------
def palette_hit_score(template_colors: set[RGBA], palette: List[RGBA]) -> int:
    pal_set = set(palette)
    return sum(1 for c in template_colors if c in pal_set)


def cmd_autotemplate(args: argparse.Namespace) -> int:
    templates_dir = Path(args.templates or "textures_input")
    palettes_dir = Path(args.palettes or "palettes")
    out_dir = Path(args.out_dir).resolve() if args.out_dir else templates_dir
    materials = str(args.materials or "wood,metal,glass")
    min_alpha = int(args.min_alpha or 1)
    min_hits = int(args.min_hits or 2)
    dry_run = bool(args.dry_run)

    palette_index = load_all_palettes_index(palettes_dir)
    pngs = sorted([p for p in templates_dir.glob("*.png") if p.is_file()])
    if not pngs:
        LOG.warning("No PNG templates found in %s", templates_dir.as_posix())
        return 0

    written = 0
    for png in pngs:
        template_id = png.stem
        img = Image.open(png).convert("RGBA")
        pixels: List[RGBA] = list(img.getdata())
        template_colors: set[RGBA] = {p for p in pixels if p[3] >= min_alpha}

        slots: List[Dict[str, Any]] = []
        slot_names: List[str] = []

        for material in (m.strip() for m in materials.split(",")):
            if not material:
                continue
            by_id = palette_index.get(material, {})
            if not by_id:
                continue

            best_score = 0
            best_ref: Optional[PaletteRef] = None
            for _, ref in by_id.items():
                _, grp = ref.item.default_group()
                score = palette_hit_score(template_colors, grp.colors_rgba())
                if score > best_score:
                    best_score = score
                    best_ref = ref

            if best_ref is None or best_score < min_hits:
                continue

            slot_names.append(material)
            slots.append(
                {
                    "slot": material,
                    "material": material,
                    "source": {
                        "palette": rel_posix(best_ref.file_path, palettes_dir),
                        "id": best_ref.item.id,
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
        if dry_run:
            LOG.info("[DRY] Would write %s", out_path.as_posix())
        else:
            save_json(out_path, data)
            LOG.info("Wrote %s", out_path.as_posix())
        written += 1

    LOG.info("Autotemplate complete: %d file(s).", written)
    return 0


# ----------------------------
# Command: assets (items/models/lang from output/textures/item)
# ----------------------------
def load_lang(path: Path) -> Dict[str, str]:
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


def save_lang(path: Path, data: Dict[str, str]) -> None:
    ordered = dict(sorted(data.items(), key=lambda kv: kv[0]))
    save_json(path, ordered, sort_keys=False)


def cmd_assets(args: argparse.Namespace) -> int:
    textures_dir = Path(args.textures or "output/textures/item")
    items_dir = Path(args.items_dir or "output/items")
    models_dir = Path(args.models_dir or "output/models/item")
    lang_path = Path(args.lang or "output/lang/en_us.json")
    namespace = str(args.namespace or "modid").strip() or "modid"
    overwrite_lang = bool(args.overwrite_lang)
    recursive = bool(args.recursive)
    dry_run = bool(args.dry_run)

    pngs = walk_pngs(textures_dir, recursive=recursive)
    if not pngs:
        LOG.warning("No PNGs found in %s", textures_dir.as_posix())
        return 0

    lang = load_lang(lang_path)
    written_items = 0
    written_models = 0
    lang_changes = 0

    for png in pngs:
        item_id = png.stem
        if not item_id:
            continue

        model_loc = f"{namespace}:item/{item_id}"
        item_json = {"model": {"type": "minecraft:model", "model": model_loc}}
        model_json = {"parent": "item/generated", "textures": {"layer0": model_loc}}

        item_path = items_dir / f"{item_id}.json"
        model_path = models_dir / f"{item_id}.json"

        if dry_run:
            LOG.info("[DRY] Would write %s", item_path.as_posix())
            LOG.info("[DRY] Would write %s", model_path.as_posix())
        else:
            save_json(item_path, item_json)
            save_json(model_path, model_json)
        written_items += 1
        written_models += 1

        lang_key = f"item.{namespace}.{item_id}"
        lang_val = title_from_id(item_id)
        if overwrite_lang or (lang_key not in lang):
            if lang.get(lang_key) != lang_val:
                lang[lang_key] = lang_val
                lang_changes += 1

    if dry_run:
        LOG.info(
            "[DRY] Would update %s (%d change(s))", lang_path.as_posix(), lang_changes
        )
    else:
        ensure_dir(lang_path.parent)
        save_lang(lang_path, lang)

    LOG.info(
        "Assets complete: %d item json, %d model json, %d lang change(s).",
        written_items,
        written_models,
        lang_changes,
    )
    return 0


# ----------------------------
# CLI
# ----------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="btg.py", description="Batch Texture Generator")
    p.add_argument(
        "--log", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)."
    )
    p.add_argument(
        "--dry-run", action="store_true", help="Do not write files; only log actions."
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    # normalize
    n = sub.add_parser(
        "normalize", help="Normalize palettes (#RRGGBB -> #RRGGBBff) and casing."
    )
    n.add_argument(
        "--palettes", default=None, help="Palettes directory (default: palettes)."
    )
    n.set_defaults(func=cmd_normalize)

    # validate
    v = sub.add_parser(
        "validate", help="Validate palette JSON files (schema + semantic checks)."
    )
    v.add_argument(
        "--schemas", default=None, help="Schema directory (default: schemas)."
    )
    v.add_argument(
        "--palettes", default=None, help="Palettes directory (default: palettes)."
    )
    v.set_defaults(func=cmd_validate)

    # extract
    e = sub.add_parser(
        "extract", help="Extract RGBA palettes from textures/ into palettes/."
    )
    e.add_argument(
        "--textures", default=None, help="Textures directory (default: textures)."
    )
    e.add_argument(
        "--palettes", default=None, help="Palettes directory (default: palettes)."
    )
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
        help="Value to write to $schema in generated palette files.",
    )
    e.add_argument(
        "--generator-version", default="1.0.0", help="Generator version string."
    )
    e.set_defaults(func=cmd_extract)

    # recolor (single swap)
    r = sub.add_parser(
        "recolor", help="Single-material recolor for textures_input -> output dir."
    )
    r.add_argument(
        "--palettes", default=None, help="Palettes directory (default: palettes)."
    )
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
    r.add_argument(
        "--input",
        default="textures_input",
        help="Input directory (default: textures_input).",
    )
    r.add_argument(
        "--output",
        default="output/textures/item",
        help="Output directory (default: output/textures/item).",
    )
    r.add_argument(
        "--no-recursive", action="store_true", help="Do not recurse input directory."
    )
    r.add_argument("--min-alpha", type=int, default=1)
    r.add_argument("--alpha-weight", type=float, default=0.25)
    r.add_argument("--no-preserve-alpha", action="store_true")
    r.add_argument("--no-exact-first", action="store_true")
    r.set_defaults(func=cmd_recolor)

    # recolor-templates (legacy task templates)
    lt = sub.add_parser(
        "recolor-templates",
        help="Legacy task templates (*.btg-template.json, older format): generate textures + assets into output tree.",
    )
    lt.add_argument(
        "--palettes", default=None, help="Palettes directory (default: palettes)."
    )
    lt.add_argument(
        "--templates",
        default=None,
        help="Templates directory (default: textures_input).",
    )
    lt.add_argument(
        "--output-root", default="output", help="Output root (default: output)."
    )
    lt.add_argument(
        "--namespace", default="modid", help="Namespace/modid (default: modid)."
    )
    lt.add_argument(
        "--lang-file",
        default="en_us.json",
        help="Language file name (default: en_us.json).",
    )
    lt.add_argument(
        "--no-modid-tree",
        action="store_true",
        help="Disable output/<namespace>/... tree.",
    )
    lt.add_argument(
        "--no-flat-tree", action="store_true", help="Disable output/... flat tree."
    )
    lt.set_defaults(func=cmd_recolor_templates)

    # generate (schema-driven multi-slot templates)
    g = sub.add_parser(
        "generate",
        help="Generate all combinations from schema-driven *.btg-template.json files.",
    )
    g.add_argument(
        "--templates",
        default=None,
        help="Templates directory (default: textures_input).",
    )
    g.add_argument(
        "--palettes", default=None, help="Palettes directory (default: palettes)."
    )
    g.add_argument(
        "--output",
        default="output/textures/item",
        help="Output directory (default: output/textures/item).",
    )
    g.add_argument("--min-alpha", type=int, default=1)
    g.add_argument("--alpha-weight", type=float, default=0.25)
    g.add_argument("--no-preserve-alpha", action="store_true")
    g.add_argument("--no-exact-first", action="store_true")
    g.add_argument(
        "--limit", type=int, default=None, help="Limit number of outputs per run."
    )
    g.set_defaults(func=cmd_generate)

    # autotemplate (schema-driven)
    a = sub.add_parser(
        "autotemplate",
        help="Auto-generate schema-driven *.btg-template.json from template PNGs.",
    )
    a.add_argument(
        "--templates",
        default="textures_input",
        help="Templates directory containing *.png.",
    )
    a.add_argument("--palettes", default="palettes", help="Palettes directory.")
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
    a.set_defaults(func=cmd_autotemplate)

    # assets
    x = sub.add_parser(
        "assets",
        help="Generate output/items, output/models/item, output/lang/en_us.json from output/textures/item PNGs.",
    )
    x.add_argument(
        "--textures", default="output/textures/item", help="Textures directory."
    )
    x.add_argument(
        "--recursive",
        action="store_true",
        help="Recurse textures dir (default: false).",
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
    x.set_defaults(func=cmd_assets)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, str(args.log).upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    # Allow global --dry-run to apply everywhere, even if subparser didn't define it
    # (argparse will still set args.dry_run because we added it globally).
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

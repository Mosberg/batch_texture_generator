#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

LOG = logging.getLogger("btg.block_assets")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any, *, sort_keys: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=sort_keys)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def title_from_id(s: str) -> str:
    s = s.replace(":", "_").replace("/", "_").replace("-", "_")
    parts = [p for p in s.split("_") if p]
    return " ".join(p[:1].upper() + p[1:] for p in parts)


def walk_pngs(root: Path, *, recursive: bool = True) -> list[Path]:
    if not root.exists():
        return []
    if root.is_file():
        return [root] if root.suffix.lower() == ".png" else []
    if recursive:
        return [p for p in sorted(root.rglob("*.png")) if p.is_file()]
    return [p for p in sorted(root.glob("*.png")) if p.is_file()]


def walk_json_mutate(obj: Any, fn) -> Any:
    if isinstance(obj, dict):
        return {k: walk_json_mutate(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_json_mutate(v, fn) for v in obj]
    return fn(obj)


def rewrite_namespace_strings(data: Any, *, old_ns: str = "modid", new_ns: str) -> Any:
    def repl(v: Any) -> Any:
        if not isinstance(v, str):
            return v
        v2 = v.replace(f"{old_ns}:", f"{new_ns}:")
        v2 = v2.replace(f"{old_ns}/", f"{new_ns}/")
        return v2

    return walk_json_mutate(data, repl)


def minecraft_item_definition(namespace: str, item_id: str) -> Dict[str, Any]:
    return {
        "model": {
            "type": "minecraft:model",
            "model": f"{namespace}:item/{item_id}",
        }
    }


def minecraft_item_model_for_block(namespace: str, block_id: str) -> Dict[str, Any]:
    # Standard item model that points to the block model.
    return {"parent": f"{namespace}:block/{block_id}"}


def minecraft_block_model_cube_all(namespace: str, block_id: str) -> Dict[str, Any]:
    return {
        "parent": "modid:block/oak_iron_barrel_block",
        "textures": {"all": f"{namespace}:block/{block_id}"},
    }


def minecraft_blockstate_facing(namespace: str, block_id: str) -> Dict[str, Any]:
    m = f"{namespace}:block/{block_id}"
    return {
        "variants": {
            "facing=north": {"model": m, "y": 0},
            "facing=east": {"model": m, "y": 90},
            "facing=south": {"model": m, "y": 180},
            "facing=west": {"model": m, "y": 270},
        }
    }


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


def infer_base_dir_from_textures_dir(textures_dir: Path) -> Optional[Path]:
    # If --textures is something like output/modid/textures/block, infer base as output/modid
    if textures_dir.name == "block" and textures_dir.parent.name == "textures":
        return textures_dir.parent.parent
    return None


def sanitize_group_id(group_id: str) -> str:
    return (
        group_id.strip().replace(" ", "_").replace("-", "_").replace("/", "_").lower()
    )


def cmd_block_assets(args) -> int:
    textures_dir = Path(args.textures or "output/textures/block")
    recursive = not bool(getattr(args, "no_recursive", False))
    namespace = str(getattr(args, "namespace", "modid") or "modid").strip()
    lang_file = str(getattr(args, "lang_file", "en_us.json") or "en_us.json")
    overwrite_lang = bool(getattr(args, "overwrite_lang", False))
    dry_run = bool(getattr(args, "dry_run", False))

    model_templates_dir = Path(
        getattr(args, "model_templates", "templates/block_assets/models")
    )
    blockstate_templates_dir = Path(
        getattr(args, "blockstate_templates", "templates/block_assets/blockstates")
    )

    base_dir = None
    if getattr(args, "base_dir", None):
        base_dir = Path(args.base_dir)
    else:
        base_dir = infer_base_dir_from_textures_dir(textures_dir)

    if base_dir is None:
        raise SystemExit(
            "Could not infer base output directory from --textures. "
            "Either pass --textures ending with 'textures/block' (e.g. output/modid/textures/block) "
            "or provide --base-dir explicitly."
        )

    models_block_dir = base_dir / "models" / "block"
    blockstates_dir = base_dir / "blockstates"
    models_item_dir = base_dir / "models" / "item"
    items_dir = base_dir / "items"
    lang_path = base_dir / "lang" / lang_file

    pngs = walk_pngs(textures_dir, recursive=recursive)
    if not pngs:
        LOG.warning("No PNGs found in %s", textures_dir.as_posix())
        return 0

    lang = load_lang(lang_path)

    written_block_models = 0
    written_blockstates = 0
    written_item_models = 0
    written_item_defs = 0
    lang_changes = 0

    seen_groups: set[str] = set()

    for png in pngs:
        rel = png.relative_to(textures_dir) if textures_dir.is_dir() else Path(png.name)
        block_id = png.stem
        if not block_id:
            continue

        # ItemGroup is inferred from the top-level folder name under textures_dir.
        # If there is no subfolder, default to "blocks".
        group_id = "blocks"
        if len(rel.parts) > 1:
            group_id = sanitize_group_id(rel.parts[0])
        seen_groups.add(group_id)

        # Block model
        model_json: Dict[str, Any]
        model_template = model_templates_dir / f"{block_id}.json"
        if model_template.exists():
            model_json = rewrite_namespace_strings(
                load_json(model_template), new_ns=namespace
            )
        else:
            model_json = minecraft_block_model_cube_all(namespace, block_id)

        # Blockstate
        blockstate_json: Dict[str, Any]
        bs_template = blockstate_templates_dir / f"{block_id}.json"
        if bs_template.exists():
            blockstate_json = rewrite_namespace_strings(
                load_json(bs_template), new_ns=namespace
            )
        else:
            blockstate_json = minecraft_blockstate_facing(namespace, block_id)

        # Item model + item forwarding definition
        item_model_json = minecraft_item_model_for_block(namespace, block_id)
        item_def_json = minecraft_item_definition(namespace, block_id)

        model_path = models_block_dir / f"{block_id}.json"
        bs_path = blockstates_dir / f"{block_id}.json"
        item_model_path = models_item_dir / f"{block_id}.json"
        item_def_path = items_dir / f"{block_id}.json"

        if dry_run:
            LOG.info("[DRY] Would write %s", model_path.as_posix())
            LOG.info("[DRY] Would write %s", bs_path.as_posix())
            LOG.info("[DRY] Would write %s", item_model_path.as_posix())
            LOG.info("[DRY] Would write %s", item_def_path.as_posix())
        else:
            save_json(model_path, model_json)
            save_json(bs_path, blockstate_json)
            save_json(item_model_path, item_model_json)
            save_json(item_def_path, item_def_json)

        written_block_models += 1
        written_blockstates += 1
        written_item_models += 1
        written_item_defs += 1

        # Lang entries
        display_name = title_from_id(block_id)

        block_key = f"block.{namespace}.{block_id}"
        item_key = f"item.{namespace}.{block_id}"

        if overwrite_lang or (block_key not in lang):
            if lang.get(block_key) != display_name:
                lang[block_key] = display_name
                lang_changes += 1

        if overwrite_lang or (item_key not in lang):
            if lang.get(item_key) != display_name:
                lang[item_key] = display_name
                lang_changes += 1

    # ItemGroup lang entries
    for gid in sorted(seen_groups):
        key = f"itemGroup.{namespace}.{gid}"
        val = title_from_id(gid)
        if overwrite_lang or (key not in lang):
            if lang.get(key) != val:
                lang[key] = val
                lang_changes += 1

    if dry_run:
        LOG.info(
            "[DRY] Would update %s (%d change(s))", lang_path.as_posix(), lang_changes
        )
    else:
        lang_path.parent.mkdir(parents=True, exist_ok=True)
        save_lang(lang_path, lang)

    LOG.info(
        "Block assets complete: %d block models, %d blockstates, %d item models, %d item defs, %d lang change(s).",
        written_block_models,
        written_blockstates,
        written_item_models,
        written_item_defs,
        lang_changes,
    )
    return 0

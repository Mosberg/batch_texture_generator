"""block_assets.py

Batch-generates Minecraft *block assets* from the block texture folder:
- Custom blockstates for facing/open=false variants.
- Custom block models that inherit from a "base" model (e.g. iron_keg_block) and only override textures.
- Block-item models that point to the corresponding block model.
- en_us.json updates for itemGroups, block names and item names.

Designed for Mosberg's batch_texture_generator workflow.

Default layout matches BLOCK-ASSETS.md:
output/<namespace>/
  blockstates/
  models/block/
  models/item/
  lang/en_us.json
  textures/block/*.png

Usage:
  python block_assets.py --namespace modid

  # Or explicitly set paths
  python block_assets.py --namespace modid \
    --textures-dir output/modid/textures/block \
    --out-root output/modid

Notes:
- Block texture filenames are treated as block IDs (stem of the .png).
- Item IDs are derived by stripping a trailing "_block".
- "keg" vs "barrel" is inferred from filename suffix:
    *_keg_block.png    -> itemGroup.<ns>.kegs
    *_barrel_block.png -> itemGroup.<ns>.barrels

"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple


@dataclass(frozen=True)
class BlockAssetKind:
    name: str
    item_group_suffix: str  # e.g. "kegs" / "barrels"
    base_parent_model: str  # model id (no namespace) used as parent


KEG_KIND = BlockAssetKind(name="keg", item_group_suffix="kegs", base_parent_model="iron_keg_block")
BARREL_KIND = BlockAssetKind(name="barrel", item_group_suffix="barrels", base_parent_model="oak_iron_barrel_block")


def _discover_block_textures(textures_dir: Path) -> Iterable[Tuple[str, Path]]:
    if not textures_dir.exists():
        return []
    return ((p.stem, p) for p in sorted(textures_dir.glob("*.png")) if p.is_file())


def _kind_for_block_id(block_id: str) -> Optional[BlockAssetKind]:
    if block_id.endswith("_keg_block"):
        return KEG_KIND
    if block_id.endswith("_barrel_block"):
        return BARREL_KIND
    return None


def _item_id_for_block_id(block_id: str) -> str:
    return block_id[:-5] if block_id.endswith("_block") else block_id


def _humanize_id(identifier: str) -> str:
    # For translation values.
    base = identifier[:-5] if identifier.endswith("_block") else identifier
    words = [w for w in base.split("_") if w]
    return " ".join(w[:1].upper() + w[1:] for w in words)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def _write_json(path: Path, data: Any) -> None:
    _ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def generate_facing_open_false_blockstate(namespace: str, block_id: str) -> Dict[str, Any]:
    # Matches BLOCK-ASSETS.md format.
    model = f"{namespace}:block/{block_id}"
    return {
        "variants": {
            "normal": {"model": model},
            "facing=north,open=false": {"model": model, "y": 0},
            "facing=east,open=false": {"model": model, "y": 90},
            "facing=south,open=false": {"model": model, "y": 180},
            "facing=west,open=false": {"model": model, "y": 270},
        }
    }


def generate_inherited_block_model(namespace: str, block_id: str, parent_model_id: str) -> Dict[str, Any]:
    # Inherits from a base Blockbench model and overrides texture key "0".
    # This assumes the parent model uses "#0" (as in BLOCK-ASSETS.md).
    tex = f"{namespace}:block/{block_id}"
    return {
        "parent": f"{namespace}:block/{parent_model_id}",
        "textures": {
            "0": tex,
            "particle": tex,
        },
    }


def generate_block_item_model(namespace: str, block_id: str) -> Dict[str, Any]:
    # Typical block-item model: point to the block model.
    return {"parent": f"{namespace}:block/{block_id}"}


def update_lang(
    lang_path: Path,
    namespace: str,
    kinds_seen: set[str],
    block_ids: Iterable[str],
) -> None:
    lang = _read_json(lang_path)

    # itemGroups
    if "barrel" in kinds_seen:
        lang[f"itemGroup.{namespace}.barrels"] = "Barrels"
    if "keg" in kinds_seen:
        lang[f"itemGroup.{namespace}.kegs"] = "Kegs"

    for block_id in block_ids:
        item_id = _item_id_for_block_id(block_id)
        name = _humanize_id(block_id)
        lang[f"block.{namespace}.{block_id}"] = name
        lang[f"item.{namespace}.{item_id}"] = name

    # Stable-ish output.
    lang_sorted = {k: lang[k] for k in sorted(lang.keys())}
    _write_json(lang_path, lang_sorted)


def generate_block_assets(
    *,
    namespace: str,
    textures_dir: Path,
    out_root: Path,
    keg_parent_model: str = KEG_KIND.base_parent_model,
    barrel_parent_model: str = BARREL_KIND.base_parent_model,
    write_item_models: bool = True,
    write_lang: bool = True,
) -> None:
    blockstates_dir = out_root / "blockstates"
    block_models_dir = out_root / "models" / "block"
    item_models_dir = out_root / "models" / "item"
    lang_path = out_root / "lang" / "en_us.json"

    _ensure_dir(blockstates_dir)
    _ensure_dir(block_models_dir)
    if write_item_models:
        _ensure_dir(item_models_dir)

    generated_block_ids: list[str] = []
    kinds_seen: set[str] = set()

    for block_id, _png in _discover_block_textures(textures_dir):
        kind = _kind_for_block_id(block_id)
        if kind is None:
            # Ignore unknown block texture types.
            continue

        kinds_seen.add(kind.name)
        generated_block_ids.append(block_id)

        # Blockstate
        blockstate = generate_facing_open_false_blockstate(namespace, block_id)
        _write_json(blockstates_dir / f"{block_id}.json", blockstate)

        # Block model
        parent = (
            keg_parent_model
            if kind.name == "keg"
            else barrel_parent_model
        )
        block_model = generate_inherited_block_model(namespace, block_id, parent)
        _write_json(block_models_dir / f"{block_id}.json", block_model)

        # Item model
        if write_item_models:
            item_id = _item_id_for_block_id(block_id)
            item_model = generate_block_item_model(namespace, block_id)
            _write_json(item_models_dir / f"{item_id}.json", item_model)

    if write_lang:
        update_lang(lang_path, namespace, kinds_seen, generated_block_ids)


def _parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate blockstates/models/lang entries from textures/block/*.png")
    p.add_argument("--namespace", required=True, help="Mod ID / namespace (e.g. modid)")

    p.add_argument(
        "--out-root",
        default=None,
        help="Output root (defaults to output/<namespace>)",
    )
    p.add_argument(
        "--textures-dir",
        default=None,
        help="Block texture directory (defaults to <out-root>/textures/block)",
    )

    p.add_argument(
        "--keg-parent-model",
        default=KEG_KIND.base_parent_model,
        help="Base parent model id (no namespace) for keg variants (default: iron_keg_block)",
    )
    p.add_argument(
        "--barrel-parent-model",
        default=BARREL_KIND.base_parent_model,
        help="Base parent model id (no namespace) for barrel variants (default: oak_iron_barrel_block)",
    )

    p.add_argument(
        "--no-item-models",
        action="store_true",
        help="Do not generate models/item/*.json for block items",
    )
    p.add_argument(
        "--no-lang",
        action="store_true",
        help="Do not update lang/en_us.json",
    )

    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = _parse_args(argv)

    out_root = Path(args.out_root) if args.out_root else (Path("output") / args.namespace)
    textures_dir = Path(args.textures_dir) if args.textures_dir else (out_root / "textures" / "block")

    generate_block_assets(
        namespace=args.namespace,
        textures_dir=textures_dir,
        out_root=out_root,
        keg_parent_model=args.keg_parent_model,
        barrel_parent_model=args.barrel_parent_model,
        write_item_models=not args.no_item_models,
        write_lang=not args.no_lang,
    )


if __name__ == "__main__":
    main()

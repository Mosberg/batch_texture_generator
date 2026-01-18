from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class Project:
    repo_root: Path
    btg_script: Path
    python_exe: Path
    log_level: str
    dry_run: bool


def _posix(p: Path) -> str:
    return p.as_posix().replace("\\\\", "/")


def build_base_command(project: Project) -> List[str]:
    cmd = [str(project.python_exe), str(project.btg_script), "--log", project.log_level]
    if project.dry_run:
        cmd.append("--dry-run")
    return cmd


def cmd_validate(project: Project, *, schemas: str, palettes: str) -> List[str]:
    return build_base_command(project) + [
        "validate",
        "--schemas",
        schemas,
        "--palettes",
        palettes,
    ]


def cmd_normalize(project: Project, *, palettes: str) -> List[str]:
    return build_base_command(project) + ["normalize", "--palettes", palettes]


def cmd_extract(
    project: Project,
    *,
    textures: str,
    palettes_out: str,
    max_colors: int,
    min_alpha: int,
    schema_ref: str,
    generator_version: str,
) -> List[str]:
    return build_base_command(project) + [
        "extract",
        "--textures",
        textures,
        "--palettes",
        palettes_out,
        "--max-colors",
        str(max_colors),
        "--min-alpha",
        str(min_alpha),
        "--schema-ref",
        schema_ref,
        "--generator-version",
        generator_version,
    ]


def cmd_recolor(
    project: Project,
    *,
    palettes_dir: str,
    src_palette: str,
    dst_palette: str,
    src_id: str,
    dst_id: str,
    group: Optional[str],
    input_dir: str,
    output_dir: str,
    recursive: bool,
    min_alpha: int,
    alpha_weight: float,
    preserve_alpha: bool,
    exact_first: bool,
) -> List[str]:
    cmd = build_base_command(project) + [
        "recolor",
        "--palettes",
        palettes_dir,
        "--src-palette",
        src_palette,
        "--dst-palette",
        dst_palette,
        "--src-id",
        src_id,
        "--dst-id",
        dst_id,
        "--input",
        input_dir,
        "--output",
        output_dir,
        "--min-alpha",
        str(min_alpha),
        "--alpha-weight",
        str(alpha_weight),
    ]
    if group:
        cmd += ["--group", group]
    if not recursive:
        cmd.append("--no-recursive")
    if not preserve_alpha:
        cmd.append("--no-preserve-alpha")
    if not exact_first:
        cmd.append("--no-exact-first")
    return cmd


def cmd_recolor_templates(
    project: Project,
    *,
    palettes_dir: str,
    templates_dir: str,
    output_root: str,
    namespace: str,
    lang_file: str,
    write_modid_tree: bool,
    write_flat_tree: bool,
) -> List[str]:
    cmd = build_base_command(project) + [
        "recolor-templates",
        "--palettes",
        palettes_dir,
        "--templates",
        templates_dir,
        "--output-root",
        output_root,
        "--namespace",
        namespace,
        "--lang-file",
        lang_file,
    ]
    if not write_modid_tree:
        cmd.append("--no-modid-tree")
    if not write_flat_tree:
        cmd.append("--no-flat-tree")
    return cmd


def cmd_generate(
    project: Project,
    *,
    templates_dir: str,
    palettes_dir: str,
    output_dir: str,
    min_alpha: int,
    alpha_weight: float,
    preserve_alpha: bool,
    exact_first: bool,
    limit: Optional[int],
) -> List[str]:
    cmd = build_base_command(project) + [
        "generate",
        "--templates",
        templates_dir,
        "--palettes",
        palettes_dir,
        "--output",
        output_dir,
        "--min-alpha",
        str(min_alpha),
        "--alpha-weight",
        str(alpha_weight),
    ]
    if not preserve_alpha:
        cmd.append("--no-preserve-alpha")
    if not exact_first:
        cmd.append("--no-exact-first")
    if limit is not None:
        cmd += ["--limit", str(limit)]
    return cmd


def cmd_autotemplate(
    project: Project,
    *,
    templates_dir: str,
    palettes_dir: str,
    out_dir: str,
    materials: str,
    min_alpha: int,
    min_hits: int,
) -> List[str]:
    cmd = build_base_command(project) + [
        "autotemplate",
        "--templates",
        templates_dir,
        "--palettes",
        palettes_dir,
        "--materials",
        materials,
        "--min-alpha",
        str(min_alpha),
        "--min-hits",
        str(min_hits),
    ]
    if out_dir:
        cmd += ["--out-dir", out_dir]
    return cmd


def cmd_assets(
    project: Project,
    *,
    textures_dir: str,
    recursive: bool,
    items_dir: str,
    models_dir: str,
    lang_file: str,
    namespace: str,
    overwrite_lang: bool,
) -> List[str]:
    cmd = build_base_command(project) + [
        "assets",
        "--textures",
        textures_dir,
        "--items-dir",
        items_dir,
        "--models-dir",
        models_dir,
        "--lang",
        lang_file,
        "--namespace",
        namespace,
    ]
    if recursive:
        cmd.append("--recursive")
    if overwrite_lang:
        cmd.append("--overwrite-lang")
    return cmd


def format_command_for_preview(cmd: List[str], repo_root: Path) -> str:
    """Pretty command for display (prefer relative paths where sensible)."""

    out: List[str] = []
    for tok in cmd:
        try:
            p = Path(tok)
            if p.exists() and p.is_absolute():
                out.append(p.resolve().relative_to(repo_root.resolve()).as_posix())
            else:
                out.append(tok)
        except Exception:
            out.append(tok)
    return " ".join(out)

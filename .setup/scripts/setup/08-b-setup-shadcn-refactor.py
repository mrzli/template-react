#!/usr/bin/env python3

# What this script does:
# - Accepts a required controls directory argument (e.g. src/controls)
# - For each shadcn component that defines cva-based variants:
#   - Extracts the variant const(s) into a separate `*-variants.ts` file
#   - Removes cva from the component's imports
#   - Adds an import of the variant from the variants file
#   - Removes the variant from the component's export (it lives in variants file now)
# - Fixes `import { type VariantProps }` → `import type { VariantProps }` everywhere
# - Updates cross-control imports that used to import variants from component files
# - Creates <controls>/index.ts re-exporting all controls and variants files
# - Collapses multiple consecutive blank lines to a single blank line in all written files
# - Uses export const at point of definition in variants files (no trailing export statement)
# - Runs eslint --fix on the controls directory

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

if len(sys.argv) < 2:
    print("Usage: python3 08-b-setup-shadcn-variants.py <controls-dir>")
    sys.exit(1)
CONTROLS = ROOT / sys.argv[1]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def run_lint(cmd: str) -> None:
    """Run linting — exits only on unexpected errors (rc > 1). rc=1 means lint
    warnings/errors that are pre-existing in shadcn components; those are OK."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode > 1:
        sys.exit(result.returncode)


def collapse_blank_lines(src: str) -> str:
    """Replace 3+ consecutive newlines with exactly 2 (one blank line)."""
    return re.sub(r"\n{3,}", "\n\n", src)


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------


def find_cva_end(src: str, var_start: int) -> int:
    """Given position of 'const varName = cva(', return position after closing paren."""
    paren_pos = src.index("(", var_start)
    depth = 0
    i = paren_pos
    while i < len(src):
        if src[i] == "(":
            depth += 1
        elif src[i] == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("Unclosed cva() call")


def extract_cva_const(src: str, var_name: str) -> tuple[str, str]:
    """Extract a single 'const varName = cva(...)' block from src.
    Returns (block_text, remaining_src). Block text has no trailing newline."""
    pattern = f"const {var_name} = cva("
    idx = src.find(pattern)
    if idx == -1:
        raise ValueError(f"Could not find: {pattern}")
    line_start = src.rfind("\n", 0, idx) + 1
    end = find_cva_end(src, idx)
    # Consume exactly one trailing newline
    if end < len(src) and src[end] == "\n":
        end += 1
    block = src[line_start:end].rstrip("\n")
    remaining = src[:line_start] + src[end:]
    return block, remaining


def extract_cva_consts(src: str, var_names: list[str]) -> tuple[list[str], str]:
    """Extract multiple cva const blocks. Returns (blocks, remaining_src)."""
    blocks: list[str] = []
    for name in var_names:
        block, src = extract_cva_const(src, name)
        blocks.append(block)
    return blocks, src


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------


def write_variants_file(path: Path, blocks: list[str]) -> None:
    lines = ['import { cva } from "class-variance-authority"\n']
    for block in blocks:
        exported_block = re.sub(r"^const ", "export const ", block)
        lines.append("\n" + exported_block + "\n")
    content = collapse_blank_lines("".join(lines))
    path.write_text(content)


# ---------------------------------------------------------------------------
# Import / export patchers
# ---------------------------------------------------------------------------


def _remove_cva_from_cva_variantprops_import(src: str) -> str:
    """'import { cva, type VariantProps }' → 'import type { VariantProps }'"""
    return re.sub(
        r'import \{ cva, type VariantProps \} from "class-variance-authority"',
        'import type { VariantProps } from "class-variance-authority"',
        src,
    )


def _remove_bare_cva_import(src: str) -> str:
    """Remove 'import { cva } from "class-variance-authority"' line entirely."""
    return re.sub(
        r'import \{ cva \} from "class-variance-authority"\n',
        "",
        src,
    )


def _fix_inline_type_variantprops(src: str) -> str:
    """'import { type VariantProps }' → 'import type { VariantProps }'"""
    return re.sub(
        r'import \{ type VariantProps \} from "class-variance-authority"',
        'import type { VariantProps } from "class-variance-authority"',
        src,
    )


def fix_component_imports(
    src: str, var_names: list[str], variants_stem: str, had_variant_props: bool
) -> str:
    """Remove cva from imports, fix VariantProps form, add variants import."""
    if had_variant_props:
        src = _remove_cva_from_cva_variantprops_import(src)
    else:
        src = _remove_bare_cva_import(src)

    # Fix any remaining inline-type VariantProps
    src = _fix_inline_type_variantprops(src)

    # Add import of extracted variants — insert after "use client" if present,
    # otherwise prepend (eslint --fix will handle final ordering)
    variants_import = f'import {{ {", ".join(var_names)} }} from "./{variants_stem}"\n'
    if src.startswith('"use client"\n'):
        src = '"use client"\n' + variants_import + src[len('"use client"\n') :]
    else:
        src = variants_import + src
    return src


def remove_from_export_block(src: str, var_names: list[str]) -> str:
    """Remove variant names from the trailing 'export { ... }' block."""
    for name in var_names:
        # ', varName' or 'varName,'
        src = re.sub(r",\s*\b" + re.escape(name) + r"\b", "", src)
        src = re.sub(r"\b" + re.escape(name) + r"\b,\s*", "", src)
    return src


# ---------------------------------------------------------------------------
# Per-component processing
# ---------------------------------------------------------------------------


def process_component(
    stem: str,
    var_names: list[str],
    variants_stem: str,
    *,
    had_variant_props: bool = True,
    exports_variants: bool = False,
) -> None:
    """Extract variants from component file and create variants file."""
    src_path = CONTROLS / f"{stem}.tsx"
    src = src_path.read_text()

    # Extract cva blocks
    blocks, src = extract_cva_consts(src, var_names)

    # Fix imports in component file
    src = fix_component_imports(src, var_names, variants_stem, had_variant_props)

    # If the component was exporting the variant, remove it from the export
    if exports_variants:
        src = remove_from_export_block(src, var_names)

    src_path.write_text(collapse_blank_lines(src))

    # Write variants file
    vars_path = CONTROLS / f"{variants_stem}.ts"
    write_variants_file(vars_path, blocks)

    print(f"  extracted  {stem}.tsx  →  {variants_stem}.ts")


# ---------------------------------------------------------------------------
# Cross-file import fixers
# ---------------------------------------------------------------------------


def fix_pagination() -> None:
    """pagination.tsx: split button import — buttonVariants → button-variants."""
    path = CONTROLS / "pagination.tsx"
    src = path.read_text()

    def _rewrite(m: re.Match[str]) -> str:
        names = m.group(1)
        # Remove buttonVariants with surrounding comma/space
        names = re.sub(r",?\s*\bbuttonVariants\b\s*,?", ",", names)
        names = names.strip().strip(",").strip()
        kept = f'import {{ {names} }} from "@/controls/button"'
        added = 'import { buttonVariants } from "@/controls/button-variants"'
        return kept + "\n" + added

    src = re.sub(r'import \{([^}]+)\} from "@/controls/button"', _rewrite, src)
    path.write_text(src)
    print("  updated    pagination.tsx  (buttonVariants → button-variants)")


def fix_calendar() -> None:
    """calendar.tsx: split button import — buttonVariants → button-variants."""
    path = CONTROLS / "calendar.tsx"
    src = path.read_text()
    src = src.replace(
        'import { Button, buttonVariants } from "@/controls/button"',
        'import { Button } from "@/controls/button"\nimport { buttonVariants } from "@/controls/button-variants"',
    )
    path.write_text(src)
    print("  updated    calendar.tsx  (buttonVariants → button-variants)")


def fix_toggle_group() -> None:
    """toggle-group.tsx: toggleVariants import → toggle-variants, fix VariantProps."""
    path = CONTROLS / "toggle-group.tsx"
    src = path.read_text()
    src = src.replace(
        'import { toggleVariants } from "@/controls/toggle"',
        'import { toggleVariants } from "@/controls/toggle-variants"',
    )
    src = _fix_inline_type_variantprops(src)
    path.write_text(src)
    print("  updated    toggle-group.tsx  (toggleVariants → toggle-variants)")


# ---------------------------------------------------------------------------
# index.ts writer
# ---------------------------------------------------------------------------


def write_index() -> None:
    """Write src/controls/index.ts re-exporting all controls and variants files."""
    files = sorted(
        p.stem
        for p in CONTROLS.iterdir()
        if p.suffix in (".ts", ".tsx") and p.stem != "index"
    )
    lines = [f'export * from "./{stem}"\n' for stem in files]
    (CONTROLS / "index.ts").write_text("".join(lines))
    controls_rel = CONTROLS.relative_to(ROOT)
    print(f"  created    {controls_rel}/index.ts  ({len(files)} exports)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    controls_rel = CONTROLS.relative_to(ROOT)
    print(f"Root: {ROOT}")
    print(f"Controls: {controls_rel}\n")

    # [1] Extract variants from each component
    print("[1] Extract cva variants into separate files")

    process_component(
        "alert",
        ["alertVariants"],
        "alert-variants",
        had_variant_props=True,
        exports_variants=False,
    )
    process_component(
        "badge",
        ["badgeVariants"],
        "badge-variants",
        had_variant_props=True,
        exports_variants=True,
    )
    process_component(
        "button",
        ["buttonVariants"],
        "button-variants",
        had_variant_props=True,
        exports_variants=True,
    )
    process_component(
        "button-group",
        ["buttonGroupVariants"],
        "button-group-variants",
        had_variant_props=True,
        exports_variants=True,
    )
    process_component(
        "empty",
        ["emptyMediaVariants"],
        "empty-variants",
        had_variant_props=True,
        exports_variants=False,
    )
    process_component(
        "field",
        ["fieldVariants"],
        "field-variants",
        had_variant_props=True,
        exports_variants=False,
    )
    process_component(
        "input-group",
        ["inputGroupAddonVariants", "inputGroupButtonVariants"],
        "input-group-variants",
        had_variant_props=True,
        exports_variants=False,
    )
    process_component(
        "item",
        ["itemVariants", "itemMediaVariants"],
        "item-variants",
        had_variant_props=True,
        exports_variants=False,
    )
    process_component(
        "navigation-menu",
        ["navigationMenuTriggerStyle"],
        "navigation-menu-variants",
        had_variant_props=False,  # navigation-menu only imports cva, not VariantProps
        exports_variants=True,
    )
    process_component(
        "sidebar",
        ["sidebarMenuButtonVariants"],
        "sidebar-variants",
        had_variant_props=True,
        exports_variants=False,
    )
    process_component(
        "tabs",
        ["tabsListVariants"],
        "tabs-variants",
        had_variant_props=True,
        exports_variants=True,
    )
    process_component(
        "toggle",
        ["toggleVariants"],
        "toggle-variants",
        had_variant_props=True,
        exports_variants=True,
    )

    # [2] Fix cross-control imports
    print("\n[2] Fix cross-control imports")
    fix_pagination()
    fix_calendar()
    fix_toggle_group()

    # [3] Create index.ts
    print(f"\n[3] Create {controls_rel}/index.ts")
    write_index()

    # [4] Fix all import ordering / lint
    print("\n[4] Fix import ordering and linting")
    run_lint(f"bunx eslint --fix {controls_rel}/")

    print("\nDone.")


main()

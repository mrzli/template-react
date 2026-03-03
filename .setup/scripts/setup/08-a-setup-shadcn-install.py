#!/usr/bin/env python3

# What this script does:
# 1. Adds @/* path alias to tsconfig.app.json (required by shadcn)
# 2. Patches vite.config.ts to add path.resolve alias
# 3. Runs `bunx shadcn@latest init` (zinc base color, CSS variables on)
# 4. Adds ALL shadcn components into src/controls/ directory

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def patch_tsconfig_app() -> None:
    path = ROOT / "tsconfig.app.json"
    src = path.read_text()
    src = src.replace(
        '    "noUncheckedSideEffectImports": true\n  },',
        '    "noUncheckedSideEffectImports": true,\n\n    /* Path aliases */\n    "baseUrl": ".",\n    "paths": {\n      "@/*": ["./src/*"]\n    }\n  },',
    )
    path.write_text(src)


def patch_tsconfig_root() -> None:
    # shadcn init reads tsconfig.json directly and won't traverse project
    # references, so it needs the paths alias here too.
    path = ROOT / "tsconfig.json"
    src = path.read_text()
    src = src.replace(
        '{\n  "files": [],',
        '{\n  "compilerOptions": {\n    "baseUrl": ".",\n    "paths": {\n      "@/*": ["./src/*"]\n    }\n  },\n  "files": [],',
    )
    path.write_text(src)


def patch_vite_config() -> None:
    path = ROOT / "vite.config.ts"
    src = path.read_text()
    # Prepend path import (eslint --fix will sort it into the right position)
    src = src.replace(
        "import tailwindcss from '@tailwindcss/vite'",
        "import path from 'path'\nimport tailwindcss from '@tailwindcss/vite'",
    )
    # Add resolve.alias block
    src = src.replace(
        "  plugins: [react(), tailwindcss()],\n})",
        "  plugins: [react(), tailwindcss()],\n  resolve: {\n    alias: {\n      '@': path.resolve(__dirname, './src'),\n    },\n  },\n})",
    )
    path.write_text(src)


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Add path aliases to tsconfig.app.json
    print("[1] Patch tsconfig.app.json (add @/* path alias)")
    patch_tsconfig_app()
    print("  patched  tsconfig.app.json\n")

    # 2. Add path aliases to tsconfig.json (shadcn init reads this directly)
    print("[2] Patch tsconfig.json (add @/* path alias for shadcn init)")
    patch_tsconfig_root()
    print("  patched  tsconfig.json\n")

    # 3. Add resolve.alias to vite.config.ts
    print("[3] Patch vite.config.ts (add path alias)")
    patch_vite_config()
    print("  patched  vite.config.ts\n")

    # 4. Fix import ordering in vite.config.ts
    print("[4] Fix import ordering in vite.config.ts")
    run("bunx eslint --fix vite.config.ts")
    print()

    # 5. shadcn init — detects Vite + Tailwind v4, installs deps, writes components.json + src/index.css CSS vars
    print("[5] shadcn/ui init")
    run("bunx shadcn@latest init -y --base-color zinc")
    print()

    # 6. Add every available component into src/controls/
    print("[6] Add all shadcn components → src/controls/")
    run("bunx shadcn@latest add -y -a -p src/controls")

    print("\nDone.")


main()

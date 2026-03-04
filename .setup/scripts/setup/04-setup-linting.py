#!/usr/bin/env python3

# What this script does:
# - Installs eslint-plugin-simple-import-sort and prettier as dev dependencies
# - Adds a "format" script (prettier --write .) to package.json
# - Patches eslint.config.js to add simple-import-sort plugin and rules
# - Runs eslint --fix . to apply import sorting to all existing files

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def patch_eslint_config() -> None:
    path = ROOT / "eslint.config.js"
    src = path.read_text()

    # Add simple-import-sort import before the defineConfig import line (guard against re-runs)
    if "eslint-plugin-simple-import-sort" not in src:
        src = src.replace(
            "import { defineConfig, globalIgnores } from 'eslint/config'",
            "import simpleImportSort from 'eslint-plugin-simple-import-sort'\nimport { defineConfig, globalIgnores } from 'eslint/config'",
        )

    # Extend globalIgnores to also exclude tmp/
    src = src.replace(
        "globalIgnores(['dist']),",
        "globalIgnores(['dist', 'tmp']),",
    )

    # Insert plugins + rules after the extends block
    src = src.replace(
        "    ],\n    languageOptions: {",
        "    ],\n    plugins: {\n      'simple-import-sort': simpleImportSort,\n    },\n    rules: {\n      'simple-import-sort/imports': 'error',\n      'simple-import-sort/exports': 'error',\n    },\n    languageOptions: {",
    )

    path.write_text(src)


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Install packages
    print("[1] Install eslint-plugin-simple-import-sort + prettier")
    run("bun add -d eslint-plugin-simple-import-sort prettier")

    # 2. Add format script to package.json
    print("\n[2] Add format script to package.json")
    pkg_path = ROOT / "package.json"
    pkg = json.loads(pkg_path.read_text())
    pkg["scripts"]["format"] = "prettier --write ."
    pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")
    print("  added  scripts.format")

    # 3. Patch eslint.config.js
    print("\n[3] Patch eslint.config.js")
    patch_eslint_config()
    print("  patched  eslint.config.js")

    # 4. Auto-fix import ordering in existing files
    print("\n[4] Fix import ordering")
    run("bunx eslint --fix .")

    print("\nDone.")


main()

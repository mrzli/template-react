#!/usr/bin/env python3

# What this script does:
# - Adds tmp/ to .gitignore if not already present
# - Runs eslint --fix on src/, stories/, .storybook/ to auto-fix issues
# - Runs prettier --write . to enforce consistent formatting across all files
# - Removes the dist/ build output directory (if present)
# - Removes the tmp/ scaffold directory (if present)

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str, allow_lint_errors: bool = False) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode > (1 if allow_lint_errors else 0):
        sys.exit(result.returncode)


def patch_gitignore() -> None:
    path = ROOT / ".gitignore"
    src = path.read_text()
    lines = src.splitlines()
    if "tmp" not in lines:
        src = src.replace("dist\ndist-ssr", "dist\ndist-ssr\ntmp")
        path.write_text(src)
        print("  patched  .gitignore (added tmp)")
    else:
        print("  skipped  .gitignore (tmp already present)")


def remove_dir(name: str) -> None:
    path = ROOT / name
    if path.exists():
        shutil.rmtree(path)
        print(f"  removed  {name}/")
    else:
        print(f"  skipped  {name}/ (not found)")


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Ensure tmp/ is gitignored
    print("[1] Patch .gitignore")
    patch_gitignore()

    # 2. eslint --fix (exit 1 = unfixable shadcn lint errors, tolerated)
    print("\n[2] eslint --fix (src/ stories/ .storybook/)")
    run("bunx eslint --fix src stories .storybook", allow_lint_errors=True)

    # 3. prettier --write (let .prettierignore exclude dist/, tmp/, node_modules)
    print("\n[3] prettier --write .")
    run("bunx prettier --write .")

    # 4. Remove dist/
    print("\n[4] Remove dist/")
    remove_dir("dist")

    # 5. Remove tmp/
    print("\n[5] Remove tmp/")
    remove_dir("tmp")

    print("\nDone.")


main()

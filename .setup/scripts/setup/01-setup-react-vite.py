#!/usr/bin/env python3

# What this script does:
# 1. Takes a project name as a command-line argument
# 2. Scaffolds a new Vite react-ts project into tmp/<name>/ using bun create vite
# 3. Copies the scaffolded project files to the workspace root

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 01-setup-react-vite.py <project-name>")
        sys.exit(1)

    name = sys.argv[1]
    tmp_dir = ROOT / "tmp"
    project_dir = tmp_dir / name

    print(f"Root:    {ROOT}")
    print(f"Project: {name}\n")

    # 1. Create tmp/ if needed
    print("[1] Ensure tmp/ exists")
    tmp_dir.mkdir(exist_ok=True)

    # 2. Scaffold Vite project under tmp/<name>
    print(f"\n[2] Scaffold Vite project into tmp/{name}")
    if project_dir.exists():
        print(f"  tmp/{name} already exists, removing...")
        shutil.rmtree(project_dir)
    subprocess.run(
        f"bun create vite {name} --template react-ts --no-interactive",
        shell=True,
        cwd=tmp_dir,
        check=True,
    )

    # 3. Copy files from tmp/<name>/ into project root
    print(f"\n[3] Copy tmp/{name}/ → project root")
    for item in sorted(project_dir.iterdir(), key=lambda e: e.name):
        dest = ROOT / item.name
        if dest.exists():
            shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
        print(f"  copied  {item.name}")

    print("\nDone.")


main()

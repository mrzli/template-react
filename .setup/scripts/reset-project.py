#!/usr/bin/env python3

import shutil
import sys
from pathlib import Path

KEEP = {".git", ".setup", ".vscode"}

dry_run = "--dry-run" in sys.argv

root = Path(__file__).resolve().parents[2]

print(f"Resetting project at: {root}")
if dry_run:
    print("(dry run — nothing will be deleted)\n")
else:
    print()

for entry in sorted(root.iterdir(), key=lambda e: e.name):
    if entry.name in KEEP:
        print(f"  kept     {entry.name}")
    else:
        if not dry_run:
            shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
        print(f"  removed  {entry.name}")

print("\nDone.")

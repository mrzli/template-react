#!/usr/bin/env python3

# What this script does:
# - Copies all files from .setup/files/ to the project root
#   - .prettierignore
#   - .prettierrc
#   - bunfig.toml

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILES_DIR = ROOT / ".setup" / "files"


def main() -> None:
    print(f"Root: {ROOT}\n")

    print("Copying .setup/files/ → project root")
    for src in sorted(FILES_DIR.rglob("*")):
        if not src.is_file():
            continue
        dest = ROOT / src.relative_to(FILES_DIR)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  copied  {src.relative_to(FILES_DIR)}")

    print("\nDone.")


main()

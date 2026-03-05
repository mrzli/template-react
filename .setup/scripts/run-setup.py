#!/usr/bin/env python3

# What this script does:
# - Runs all setup steps in order
# - Derives the project name from the root directory name
# - Includes the optional Storybook step

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETUP_DIR = ROOT / ".setup" / "scripts" / "setup"


def run_script(script: str, *args: str) -> None:
    path = SETUP_DIR / script
    cmd = [sys.executable, str(path), *args]
    print(f"\n{'=' * 60}")
    print(f"Running: {script}")
    print(f"{'=' * 60}\n")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\nScript failed: {script}")
        sys.exit(result.returncode)


def main() -> None:
    project_name = ROOT.name
    print(f"Root:    {ROOT}")
    print(f"Project: {project_name}")

    run_script("01-setup-react-vite.py", project_name)
    run_script("02-copy-files.py")
    run_script("03-setup-app.py")
    run_script("04-setup-linting.py")
    run_script("05-setup-react-router.py")
    run_script("06-setup-tailwind.py")
    run_script("07-setup-redux.py")
    run_script("08-a-setup-shadcn-install.py", "src/controls")
    run_script("08-b-setup-shadcn-refactor.py", "src/controls")
    run_script("08-c-setup-shadcn-showcase.py")
    run_script("09-setup-storybook.py")
    run_script("10-setup-forms.py")
    run_script("11-finalize.py")

    print(f"\n{'=' * 60}")
    print("All steps complete.")
    print(f"{'=' * 60}")


main()

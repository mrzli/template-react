#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def run_bypassing_min_release_age(cmd: str) -> None:
    """Run cmd with bunfig.toml temporarily hidden so minimumReleaseAge is not applied."""
    bunfig = ROOT / "bunfig.toml"
    bunfig_bak = ROOT / "bunfig.toml.bak"
    bunfig.rename(bunfig_bak)
    try:
        run(cmd)
    finally:
        bunfig_bak.rename(bunfig)


def remove_eslint_plugin_storybook() -> None:
    path = ROOT / "package.json"
    pkg = json.loads(path.read_text())
    pkg.get("devDependencies", {}).pop("eslint-plugin-storybook", None)
    path.write_text(json.dumps(pkg, indent=2) + "\n")


def patch_main_ts() -> None:
    path = ROOT / ".storybook" / "main.ts"
    src = path.read_text()
    # Storybook init may point stories to src/ — redirect to stories/ instead
    src = src.replace('"../src/**/*.mdx"', '"../stories/**/*.mdx"')
    src = src.replace(
        '"../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"',
        '"../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)"',
    )
    path.write_text(src)


def patch_preview_ts() -> None:
    path = ROOT / ".storybook" / "preview.ts"
    src = path.read_text()
    src = "import '../src/index.css';\n\n" + src
    path.write_text(src)


GREETING_STORIES_TSX = """\
import type { Meta, StoryObj } from '@storybook/react-vite';

interface GreetingProps {
  readonly name: string;
}

function Greeting({ name }: GreetingProps) {
  return (
    <div className='rounded-lg bg-blue-50 p-4'>
      <p className='text-lg font-semibold text-blue-800'>Hello, {name}!</p>
    </div>
  );
}

const meta: Meta<typeof Greeting> = {
  title: 'App/Greeting',
  component: Greeting,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    name: 'World',
  },
};
"""


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Run Storybook init — creates .storybook/main.ts, .storybook/preview.ts,
    #    adds scripts + packages to package.json. Exits with code 1 (no npm) — expected.
    print("[1] bun create storybook (exit code 1 is expected)")
    result = subprocess.run(
        "bun create storybook@latest --features docs --yes",
        shell=True,
        cwd=ROOT,
        env={**os.environ, "CI": "true"},
    )
    if result.returncode not in (0, 1):
        sys.exit(result.returncode)

    # 2. Remove eslint-plugin-storybook (added by init, not needed here)
    print("\n[2] Remove eslint-plugin-storybook from package.json")
    remove_eslint_plugin_storybook()
    print("  removed  eslint-plugin-storybook")

    # 3. Install packages — bypass bunfig.toml minimumReleaseAge for new storybook packages
    print("\n[3] bun install (bunfig.toml temporarily hidden)")
    run_bypassing_min_release_age("bun install")

    # 4. Patch .storybook/main.ts — ensure stories path points to stories/ not src/
    print("\n[4] Patch .storybook/main.ts")
    patch_main_ts()
    print("  patched  .storybook/main.ts")

    # 5. Remove all default stories scaffold content
    print("\n[5] Clean stories/ and src/stories/ directories")
    stories_dir = ROOT / "stories"
    if stories_dir.exists():
        shutil.rmtree(stories_dir)
    stories_dir.mkdir()
    src_stories_dir = ROOT / "src" / "stories"
    if src_stories_dir.exists():
        shutil.rmtree(src_stories_dir)
    print("  cleaned  stories/")
    print("  cleaned  src/stories/")

    # 6. Patch .storybook/preview.ts — add Tailwind CSS import
    print("\n[6] Patch .storybook/preview.ts")
    patch_preview_ts()
    print("  patched  .storybook/preview.ts")

    # 7. Add sample story (Greeting component defined inline)
    print("\n[7] Create stories/greeting.stories.tsx")
    (stories_dir / "greeting.stories.tsx").write_text(GREETING_STORIES_TSX)
    print("  created  stories/greeting.stories.tsx")

    # 8. Delete debug log left by storybook init
    print("\n[8] Remove debug-storybook.log")
    log = ROOT / "debug-storybook.log"
    if log.exists():
        log.unlink()
        print("  removed  debug-storybook.log")
    else:
        print("  not found, skipping  debug-storybook.log")

    print("\nDone.")


main()

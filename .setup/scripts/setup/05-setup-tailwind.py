#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


def patch_vite_config() -> None:
    path = ROOT / "vite.config.ts"
    src = path.read_text()

    src = src.replace(
        "import react from '@vitejs/plugin-react'",
        "import tailwindcss from '@tailwindcss/vite'\nimport react from '@vitejs/plugin-react'",
    )
    src = src.replace(
        "  plugins: [react()],",
        "  plugins: [react(), tailwindcss()],",
    )

    path.write_text(src)


APP_TSX = """\
export function App() {
  return (
    <div className='flex min-h-screen items-center justify-center bg-gray-100'>
      <div className='rounded-xl bg-white p-8 shadow-md'>
        <h1 className='text-2xl font-bold text-gray-800'>template-react</h1>
        <p className='mt-2 text-gray-500'>Tailwind CSS is working.</p>
      </div>
    </div>
  );
}
"""


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Install Tailwind + Vite plugin
    print("[1] Install tailwindcss + @tailwindcss/vite")
    run("bun add -d tailwindcss @tailwindcss/vite")

    # 2. Patch vite.config.ts
    print("\n[2] Patch vite.config.ts")
    patch_vite_config()
    print("  patched  vite.config.ts")

    # 3. Add Tailwind import to index.css
    print("\n[3] Patch src/index.css")
    (ROOT / "src" / "index.css").write_text('@import "tailwindcss";\n')
    print("  patched  src/index.css")

    # 4. Update app.tsx to showcase Tailwind
    print("\n[4] Update src/app/app.tsx")
    (ROOT / "src" / "app" / "app.tsx").write_text(APP_TSX)
    print("  updated  src/app/app.tsx")

    print("\nDone.")


main()

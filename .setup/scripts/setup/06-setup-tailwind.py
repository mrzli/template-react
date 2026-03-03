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


def patch_router_tsx() -> None:
    path = ROOT / "src" / "routing" / "router.tsx"
    src = path.read_text()
    src = src.replace(
        "import { homeLoader, HomePage } from '../app/home-page';",
        "import { homeLoader, HomePage } from '../app/home-page';\nimport { TailwindPage } from '../app/tailwind-page';",
    )
    src = src.replace(
        "      { path: 'about', element: <AboutPage />, action: aboutAction },\n    ],",
        "      { path: 'about', element: <AboutPage />, action: aboutAction },\n      { path: 'tailwind', element: <TailwindPage /> },\n    ],",
    )
    path.write_text(src)


def patch_app_tsx() -> None:
    path = ROOT / "src" / "app" / "app.tsx"
    src = path.read_text()
    src = src.replace(
        "        <Link to='/about'>About</Link>\n      </nav>",
        "        <Link to='/about'>About</Link>\n        {' | '}\n        <Link to='/tailwind'>Tailwind</Link>\n      </nav>",
    )
    path.write_text(src)


TAILWIND_PAGE_TSX = """\
export function TailwindPage() {
  return (
    <div className='flex min-h-[60vh] items-center justify-center'>
      <div className='rounded-xl bg-white p-8 shadow-md'>
        <h1 className='text-2xl font-bold text-gray-800'>Tailwind CSS</h1>
        <p className='mt-2 text-gray-500'>
          Tailwind CSS is working. Here are some example components.
        </p>
        <div className='mt-6 flex gap-3'>
          <button className='rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700'>
            Primary
          </button>
          <button className='rounded-lg bg-gray-200 px-4 py-2 font-medium text-gray-700 hover:bg-gray-300'>
            Secondary
          </button>
          <button className='rounded-lg border border-red-400 px-4 py-2 font-medium text-red-600 hover:bg-red-50'>
            Danger
          </button>
        </div>
        <div className='mt-4 grid grid-cols-3 gap-3'>
          <div className='rounded-lg bg-blue-100 p-4 text-center text-blue-800'>
            Blue
          </div>
          <div className='rounded-lg bg-green-100 p-4 text-center text-green-800'>
            Green
          </div>
          <div className='rounded-lg bg-red-100 p-4 text-center text-red-800'>
            Red
          </div>
        </div>
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
    print("\n[3] Write src/index.css")
    (ROOT / "src" / "index.css").write_text('@import "tailwindcss";\n')
    print("  written  src/index.css")

    # 4. Create src/app/tailwind-page.tsx
    print("\n[4] Create src/app/tailwind-page.tsx")
    (ROOT / "src" / "app" / "tailwind-page.tsx").write_text(TAILWIND_PAGE_TSX)
    print("  created  src/app/tailwind-page.tsx")

    # 5. Patch src/routing/router.tsx to add /tailwind route
    print("\n[5] Patch src/routing/router.tsx")
    patch_router_tsx()
    print("  patched  src/routing/router.tsx")

    # 6. Patch src/app/app.tsx nav to add Tailwind link
    print("\n[6] Patch src/app/app.tsx")
    patch_app_tsx()
    print("  patched  src/app/app.tsx")

    # 7. Fix import ordering
    print("\n[7] Fix import ordering")
    run(
        "bunx eslint --fix src/routing/router.tsx src/app/app.tsx src/app/tailwind-page.tsx"
    )

    print("\nDone.")


main()

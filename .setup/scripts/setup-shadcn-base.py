#!/usr/bin/env python3

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_jsonc(text: str) -> dict:
    text = re.sub(r"//[^\n]*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return json.loads(text)


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


print(f"Setting up shadcn base at: {ROOT}\n")

# 1. Scaffold Vite react-ts project
print("[1] Scaffold Vite project")
with tempfile.TemporaryDirectory() as tmp:
    tmp_real = Path(tmp).resolve()
    subprocess.run(
        "bun create vite app --template react-ts --no-interactive",
        shell=True,
        cwd=tmp_real,
        check=True,
    )
    for item in (tmp_real / "app").iterdir():
        dest = ROOT / item.name
        if dest.exists():
            shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
        shutil.copytree(item, dest) if item.is_dir() else shutil.copy2(item, dest)

# 2. Copy .setup/files/ to root
print("\n[2] Copy .setup/files/")
files_dir = ROOT / ".setup" / "files"
for src in files_dir.rglob("*"):
    if src.is_file():
        dest = ROOT / src.relative_to(files_dir)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

# 3. Install dependencies
print("\n[3] bun install")
run("bun install")

# 3b. Install Tailwind CSS v4
print("\n[3b] Install tailwindcss + @tailwindcss/vite")
run("bun add tailwindcss @tailwindcss/vite")

# 3c. Patch vite.config.ts — add tailwind plugin + path alias
print("\n[3c] Patch vite.config.ts")
(ROOT / "vite.config.ts").write_text(
    "import path from 'path'\n"
    "import { defineConfig } from 'vite'\n"
    "import react from '@vitejs/plugin-react'\n"
    "import tailwindcss from '@tailwindcss/vite'\n"
    "\n"
    "export default defineConfig({\n"
    "  plugins: [react(), tailwindcss()],\n"
    "  resolve: {\n"
    "    alias: {\n"
    "      '@': path.resolve(__dirname, './src'),\n"
    "    },\n"
    "  },\n"
    "})\n"
)

# 3d. Patch tsconfig.app.json + tsconfig.json — add baseUrl + paths alias
print("\n[3d] Patch tsconfig.app.json + tsconfig.json")
for tsconfig_path in [ROOT / "tsconfig.app.json", ROOT / "tsconfig.json"]:
    cfg = load_jsonc(tsconfig_path.read_text())
    cfg.setdefault("compilerOptions", {})["baseUrl"] = "."
    cfg["compilerOptions"].setdefault("paths", {})["@/*"] = ["./src/*"]
    tsconfig_path.write_text(json.dumps(cfg, indent=2) + "\n")

# 3e. Patch src/index.css — add Tailwind import
print("\n[3e] Patch src/index.css")
(ROOT / "src" / "index.css").write_text('@import "tailwindcss";\n')

# 4. shadcn init (handles tailwind + path aliases automatically)
print("\n[4] shadcn init")
run("bunx shadcn@latest init --defaults")

# 5. Patch components.json to output to src/controls/
print("\n[5] Patch components.json → src/controls/")
cfg_path = ROOT / "components.json"
cfg = json.loads(cfg_path.read_text())
cfg.setdefault("aliases", {})
cfg["aliases"]["components"] = "@/controls"
cfg["aliases"]["ui"] = "@/controls"
cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")

# 6. Add all shadcn components
print("\n[6] shadcn add --all")
run("bunx shadcn@latest add --all --overwrite")

print("\nDone.")

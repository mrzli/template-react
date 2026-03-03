#!/usr/bin/env python3

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"


APP_TSX = """\
import type { CSSProperties } from 'react';

import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';

const logoRowStyle: CSSProperties = {
  display: 'flex',
  gap: '1rem',
  marginTop: '1rem',
};

const logoStyle: CSSProperties = {
  height: '4rem',
};

export function App() {
  return (
    <div>
      <h1>template-react</h1>
      <p>App is running.</p>
      <div style={logoRowStyle}>
        <img alt='Vite logo' src={viteLogo} style={logoStyle} />
        <img alt='React logo' src={reactLogo} style={logoStyle} />
      </div>
    </div>
  );
}
"""

MAIN_TSX = """\
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { App } from './app/app';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
"""


def main() -> None:
    print(f"Root: {ROOT}\n")

    # Create src/app/app.tsx
    app_dir = SRC / "app"
    app_dir.mkdir(parents=True, exist_ok=True)
    (app_dir / "app.tsx").write_text(APP_TSX)
    print("  created  src/app/app.tsx")

    # Write empty src/index.css
    (SRC / "index.css").write_text("")
    print("  updated  src/index.css")

    # Update src/main.tsx
    (SRC / "main.tsx").write_text(MAIN_TSX)
    print("  updated  src/main.tsx")

    # Remove unused files
    for rel in ["App.tsx", "App.css"]:
        target = SRC / rel
        if target.exists():
            shutil.rmtree(target) if target.is_dir() else target.unlink()
            print(f"  removed  src/{rel}")

    print("\nDone.")


main()

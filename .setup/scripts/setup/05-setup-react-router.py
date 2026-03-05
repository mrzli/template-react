#!/usr/bin/env python3

# What this script does:
# - Installs react-router
# - Creates src/routing/router.tsx — createBrowserRouter with App root layout and nested examples routes
# - Creates src/app/app.tsx — minimal root layout with Home and Examples nav links
# - Creates src/app/examples/examples-layout.tsx — examples section layout with sub-nav
# - Creates src/app/home-page.tsx — simple landing page with Vite/React logos and link to /examples
# - Creates src/app/examples/home-page.tsx — examples index page with Vite/React logos and description
# - Creates src/app/examples/about-page.tsx — async action handling a Form POST, returns a greeting
# - Rewrites src/main.tsx to use RouterProvider
# - Runs eslint --fix on all new and modified files

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run(cmd: str) -> None:
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)


MAIN_TSX = """\
import './index.css';

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router';

import { router } from './routing/router';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
"""


def write_main_tsx() -> None:
    (ROOT / "src" / "main.tsx").write_text(MAIN_TSX)


APP_TSX = """\
import type { CSSProperties } from 'react';
import { Link, Outlet } from 'react-router';

const rootStyle: CSSProperties = {
  minHeight: '100vh',
  fontFamily: 'system-ui, -apple-system, sans-serif',
  background: '#f5f5f5',
  color: '#222',
};

const navStyle: CSSProperties = {
  background: '#fff',
  borderBottom: '1px solid #e5e5e5',
  padding: '0.75rem 1.5rem',
  display: 'flex',
  gap: '1.25rem',
};

const linkStyle: CSSProperties = {
  color: '#2563eb',
  textDecoration: 'none',
};

const mainStyle: CSSProperties = {
  maxWidth: '720px',
  margin: '2rem auto',
  padding: '0 1.5rem',
};

export function App() {
  return (
    <div style={rootStyle}>
      <nav style={navStyle}>
        <Link style={linkStyle} to='/'>
          Home
        </Link>
        <Link style={linkStyle} to='/examples'>
          Examples
        </Link>
      </nav>
      <main style={mainStyle}>
        <Outlet />
      </main>
    </div>
  );
}
"""

ROUTER_TSX = """\
import { createBrowserRouter } from 'react-router';

import { App } from '../app/app';
import { aboutAction, AboutPage } from '../app/examples/about-page';
import { ExamplesHomePage } from '../app/examples/home-page';
import { ExamplesLayout } from '../app/examples/examples-layout';
import { HomePage } from '../app/home-page';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      {
        path: 'examples',
        element: <ExamplesLayout />,
        children: [
          { index: true, element: <ExamplesHomePage /> },
          { path: 'about', element: <AboutPage />, action: aboutAction },
        ],
      },
    ],
  },
]);
"""

EXAMPLES_LAYOUT_TSX = """\
import type { CSSProperties } from 'react';
import { Link, Outlet } from 'react-router';

const navStyle: CSSProperties = {
  background: '#f9fafb',
  borderBottom: '1px solid #e5e5e5',
  padding: '0.5rem 1.5rem',
  display: 'flex',
  gap: '1.25rem',
};

const linkStyle: CSSProperties = {
  color: '#2563eb',
  textDecoration: 'none',
  fontSize: '0.875rem',
};

export function ExamplesLayout() {
  return (
    <div>
      <nav style={navStyle}>
        <Link style={linkStyle} to='/examples'>
          Home
        </Link>
        <Link style={linkStyle} to='/examples/about'>
          About
        </Link>
      </nav>
      <Outlet />
    </div>
  );
}
"""

EXAMPLES_HOME_PAGE_TSX = """\
import type { CSSProperties } from 'react';

import reactLogo from '../../assets/react.svg';
import viteLogo from '/vite.svg';

const cardStyle: CSSProperties = {
  background: '#fff',
  border: '1px solid #e5e5e5',
  borderRadius: '8px',
  padding: '1.5rem 2rem',
};

const headingStyle: CSSProperties = {
  fontSize: '1.5rem',
  fontWeight: 700,
  marginBottom: '0.5rem',
};

const logoRowStyle: CSSProperties = {
  display: 'flex',
  gap: '1rem',
  marginTop: '1rem',
};

const logoStyle: CSSProperties = {
  height: '4rem',
};

export function ExamplesHomePage() {
  return (
    <div style={cardStyle}>
      <h1 style={headingStyle}>Examples</h1>
      <p>Browse the pages in this section to see examples of the features included in this template.</p>
      <div style={logoRowStyle}>
        <img alt='Vite logo' src={viteLogo} style={logoStyle} />
        <img alt='React logo' src={reactLogo} style={logoStyle} />
      </div>
    </div>
  );
}
"""

HOME_PAGE_TSX = """\
import type { CSSProperties } from 'react';
import { Link } from 'react-router';

import reactLogo from '../assets/react.svg';
import viteLogo from '/vite.svg';

const cardStyle: CSSProperties = {
  background: '#fff',
  border: '1px solid #e5e5e5',
  borderRadius: '8px',
  padding: '1.5rem 2rem',
};

const headingStyle: CSSProperties = {
  fontSize: '1.5rem',
  fontWeight: 700,
  marginBottom: '0.5rem',
};

const linkStyle: CSSProperties = {
  color: '#2563eb',
  textDecoration: 'none',
};

const logoRowStyle: CSSProperties = {
  display: 'flex',
  gap: '1rem',
  marginTop: '1rem',
};

const logoStyle: CSSProperties = {
  height: '4rem',
};

export function HomePage() {
  return (
    <div style={cardStyle}>
      <h1 style={headingStyle}>template-react</h1>
      <p>A React + Vite + TypeScript template.</p>
      <p style={{ marginTop: '1rem' }}>
        <Link style={linkStyle} to='/examples'>
          View examples →
        </Link>
      </p>
      <div style={logoRowStyle}>
        <img alt='Vite logo' src={viteLogo} style={logoStyle} />
        <img alt='React logo' src={reactLogo} style={logoStyle} />
      </div>
    </div>
  );
}
"""

ABOUT_PAGE_TSX = """\
import type { CSSProperties } from 'react';
import { Form, useActionData } from 'react-router';

interface AboutActionData {
  readonly greeting: string;
}

const cardStyle: CSSProperties = {
  background: '#fff',
  border: '1px solid #e5e5e5',
  borderRadius: '8px',
  padding: '1.5rem 2rem',
};

const headingStyle: CSSProperties = {
  fontSize: '1.5rem',
  fontWeight: 700,
  marginBottom: '0.5rem',
};

const formStyle: CSSProperties = {
  display: 'flex',
  gap: '0.5rem',
  marginTop: '0.5rem',
};

const inputStyle: CSSProperties = {
  flex: 1,
  padding: '0.5rem 0.75rem',
  border: '1px solid #ccc',
  borderRadius: '6px',
  fontSize: '1rem',
};

const buttonStyle: CSSProperties = {
  padding: '0.5rem 1rem',
  background: '#2563eb',
  color: '#fff',
  border: 'none',
  borderRadius: '6px',
  cursor: 'pointer',
  fontSize: '1rem',
};

const resultStyle: CSSProperties = {
  marginTop: '1rem',
  padding: '0.75rem 1rem',
  background: '#eff6ff',
  border: '1px solid #bfdbfe',
  borderRadius: '6px',
  color: '#1e40af',
};

// eslint-disable-next-line react-refresh/only-export-components
export async function aboutAction({
  request,
}: {
  readonly request: Request;
}): Promise<AboutActionData> {
  const formData = await request.formData();
  const name = (formData.get('name') as string | null) ?? 'stranger';
  return { greeting: `Hello, ${name}! This response came from an action.` };
}

export function AboutPage() {
  const data = useActionData<typeof aboutAction>();

  return (
    <div style={cardStyle}>
      <h1 style={headingStyle}>About</h1>
      <p>Submit the form below to trigger a route action.</p>
      <Form style={formStyle} method='post'>
        <input
          name='name'
          placeholder='Your name'
          style={inputStyle}
          type='text'
        />
        <button style={buttonStyle} type='submit'>
          Submit
        </button>
      </Form>
      {data !== undefined && <p style={resultStyle}>{data.greeting}</p>}
    </div>
  );
}
"""


def main() -> None:
    print(f"Root: {ROOT}\n")

    # 1. Install react-router
    print("[1] Install react-router")
    run("bun add react-router")

    # 2. Create src/routing/ and router.tsx
    print("\n[2] Create src/routing/router.tsx")
    routing_dir = ROOT / "src" / "routing"
    routing_dir.mkdir(exist_ok=True)
    (routing_dir / "router.tsx").write_text(ROUTER_TSX)
    print("  created  src/routing/router.tsx")

    # 3. Rewrite src/app/app.tsx as minimal root layout
    print("\n[3] Rewrite src/app/app.tsx as minimal root layout")
    (ROOT / "src" / "app" / "app.tsx").write_text(APP_TSX)
    print("  updated  src/app/app.tsx")

    # 4. Create src/app/home-page.tsx
    print("\n[4] Create src/app/home-page.tsx")
    (ROOT / "src" / "app" / "home-page.tsx").write_text(HOME_PAGE_TSX)
    print("  created  src/app/home-page.tsx")

    # 5. Create src/app/examples/ and examples-layout.tsx
    print("\n[5] Create src/app/examples/examples-layout.tsx")
    examples_dir = ROOT / "src" / "app" / "examples"
    examples_dir.mkdir(exist_ok=True)
    (examples_dir / "examples-layout.tsx").write_text(EXAMPLES_LAYOUT_TSX)
    print("  created  src/app/examples/examples-layout.tsx")

    # 6. Create src/app/examples/home-page.tsx
    print("\n[6] Create src/app/examples/home-page.tsx")
    (examples_dir / "home-page.tsx").write_text(EXAMPLES_HOME_PAGE_TSX)
    print("  created  src/app/examples/home-page.tsx")

    # 7. Create src/app/examples/about-page.tsx
    print("\n[7] Create src/app/examples/about-page.tsx")
    (examples_dir / "about-page.tsx").write_text(ABOUT_PAGE_TSX)
    print("  created  src/app/examples/about-page.tsx")

    # 8. Write src/main.tsx to use RouterProvider
    print("\n[8] Write src/main.tsx")
    write_main_tsx()
    print("  written  src/main.tsx")

    # 9. Fix import ordering via eslint
    print("\n[9] Fix import ordering")
    run(
        "bunx eslint --fix src/routing/router.tsx src/app/app.tsx src/app/home-page.tsx src/app/examples/examples-layout.tsx src/app/examples/home-page.tsx src/app/examples/about-page.tsx src/main.tsx"
    )

    print("\nDone.")


main()

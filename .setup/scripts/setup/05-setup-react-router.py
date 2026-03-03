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
import { Link, Outlet } from 'react-router';

export function App() {
  return (
    <div>
      <nav>
        <Link to='/'>Home</Link>
        {' | '}
        <Link to='/about'>About</Link>
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
"""

ROUTER_TSX = """\
import { createBrowserRouter } from 'react-router';

import { App } from '../app/app';
import { aboutAction, AboutPage } from '../app/about-page';
import { homeLoader, HomePage } from '../app/home-page';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <HomePage />, loader: homeLoader },
      { path: 'about', element: <AboutPage />, action: aboutAction },
    ],
  },
]);
"""

HOME_PAGE_TSX = """\
import { useLoaderData } from 'react-router';

interface HomeLoaderData {
  readonly message: string;
  readonly items: readonly string[];
}

// eslint-disable-next-line react-refresh/only-export-components
export function homeLoader(): HomeLoaderData {
  return {
    message: 'Welcome to the home page!',
    items: ['React', 'Vite', 'TypeScript', 'React Router'],
  };
}

export function HomePage() {
  const { message, items } = useLoaderData<typeof homeLoader>();

  return (
    <div>
      <h1>{message}</h1>
      <p>This data was provided by a loader.</p>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
"""

ABOUT_PAGE_TSX = """\
import { Form, useActionData } from 'react-router';

interface AboutActionData {
  readonly greeting: string;
}

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
    <div>
      <h1>About</h1>
      <p>Submit the form below to trigger a route action.</p>
      <Form method='post'>
        <input name='name' placeholder='Your name' type='text' />
        <button type='submit'>Submit</button>
      </Form>
      {data !== undefined && <p>{data.greeting}</p>}
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

    # 3. Rewrite src/app/app.tsx as root layout
    print("\n[3] Rewrite src/app/app.tsx as root layout")
    (ROOT / "src" / "app" / "app.tsx").write_text(APP_TSX)
    print("  updated  src/app/app.tsx")

    # 4. Create src/app/home-page.tsx
    print("\n[4] Create src/app/home-page.tsx")
    (ROOT / "src" / "app" / "home-page.tsx").write_text(HOME_PAGE_TSX)
    print("  created  src/app/home-page.tsx")

    # 5. Create src/app/about-page.tsx
    print("\n[5] Create src/app/about-page.tsx")
    (ROOT / "src" / "app" / "about-page.tsx").write_text(ABOUT_PAGE_TSX)
    print("  created  src/app/about-page.tsx")

    # 6. Write src/main.tsx to use RouterProvider
    print("\n[6] Write src/main.tsx")
    write_main_tsx()
    print("  written  src/main.tsx")

    # 7. Fix import ordering via eslint
    print("\n[7] Fix import ordering")
    run(
        "bunx eslint --fix src/routing/router.tsx src/app/app.tsx src/app/home-page.tsx src/app/about-page.tsx src/main.tsx"
    )

    print("\nDone.")


main()

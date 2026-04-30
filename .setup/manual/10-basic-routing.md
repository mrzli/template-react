# Basic Routing

- Add react-router dependency with:
  ```bash
  bun add react-router
  ```

## Create About Page

- Create `about-page.tsx` file under `src/app/examples/` directory.
- It should just be a stub page.
- It is needed to be able to showcase routing.

## Create Router File

- Create `src/routing/` directory if it does not already exist.
- Create `router.tsx` file under that directory.
- Use 'data mode' routing.
- Initially, create an empty router file:
  ```tsx
  import { createBrowserRouter } from 'react-router';

  export const router = createBrowserRouter([]);
  ```
- Add the hierarchy of components to the router configuration.
- Use `index` routes for default subpages.
- This is the structure:
  ```tsx
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'examples',
        element: <ExamplesPage />,
        children: [
          {
            index: true,
            element: <HomePage />,
          },
          {
            path: 'about',
            element: <AboutPage />,
          },
        ],
      },
    ]
  }
  ```

## Use Router in the Application

- Update the `run.tsx` file.
- Add imports:
  ```tsx
  import { RouterProvider } from 'react-router';
  import { router } from '../routing/router';
  ```
- Replace `<App />` with:
  ```tsx
  <RouterProvider router={router} />
  ```
- Remove import for `App` component, since it is now rendered through the router.

## Update `ExamplesPage` Component

- Add imports:
  ```tsx
  import type { CSSProperties, FC } from 'react';
  import { Link, Outlet } from 'react-router';
  ```
- Add styles, as module variables outside of the component:
  ```tsx
  const navStyle: CSSProperties = {
    display: 'flex',
    gap: '1rem',
    padding: '1rem',
  };

  const linkStyle: CSSProperties = {
    textDecoration: 'none',
    color: '#2563eb',
  };
  ```
- Add content inside `div`, links, and `<Outlet />` for rendering child routes:
  ```tsx
  <nav style={navStyle}>
    <Link style={linkStyle} to=''>
      Home
    </Link>
    <Link style={linkStyle} to='about'>
      About
    </Link>
  </nav>
  <Outlet />
  ```

## Update `App` Component

- Update it in same manner as `ExamplesPage`, but use links to root level routes to `HomePage` and `ExamplesPage`.

## Finalize Step

- Format using `bun run format`.
- Commit with "setup basic routing".

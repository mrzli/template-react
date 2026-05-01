# Routing

## Setup Routing

- Add react-router dependency with:
  ```bash
  bun add react-router
  ```

### Create About Page

- Create `about-page.tsx` file under `src/app/examples/` directory.
- It should just be a stub page.
- It is needed to be able to showcase routing.

### Create Router File

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

### Use Router in the Application

- Update the file that renders the app (`main.tsx` or wherever else you placed it).
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

### Update `ExamplesPage` Component

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

### Update `App` Component

- Update it in same manner as `ExamplesPage`, but use links to root level routes to `HomePage` and `ExamplesPage`.

### Finalize Step

- Format using `bun run format`.
- Commit with "setup basic routing".

## Loader Example

- Create `src/app/examples/loader/` directory.
- Create `loader-page.tsx` under that directory.
- Add stub content.
- Update `router.tsx`, add `/examples/loader` route.
- Update `ExamplesPage` to have a link to `loader` page.

### Create Loader

- Add `src/app/examples/loader/loader.ts` file.
- Add lambda function called `loader` (async and exported).
- Returns a promise which resolves in `200ms` with some string.
- Example code:
  ```ts
  export const loader = async () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve('resolved data');
      }, 200);
    });
  };
  ```
- Add the loader to the `/examples/loader` route in `router.tsx`:
  ```tsx
  {
    path: 'loader',
    element: <LoaderPage />,
    loader: loader,
  }
  ```

### Use Loader

- Update `LoaderPage` to use loader data.
- Add line: `const data = useLoaderData<typeof loader>();`
- Display the data in a page, in a `div` for example.
- Example:
  ```tsx
  import type { FC } from 'react';
  import { useLoaderData } from 'react-router';

  import { loader } from './loader';

  export const LoaderPage: FC = () => {
    const data = useLoaderData<typeof loader>();

    return (
      <div>
        <div>loader-page</div>
        <div>{data}</div>
      </div>
    );
  };
  ```

### Finalize Step

- Format using `bun run format`.
- Commit with "setup react-router loader example".

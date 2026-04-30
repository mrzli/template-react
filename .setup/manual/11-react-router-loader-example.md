# React Router Loader Example

- Create `src/app/examples/loader/` directory.
- Create `loader-page.tsx` under that directory.
- Add stub content.
- Update `router.tsx`, add `/examples/loader` route.
- Update `ExamplesPage` to have a link to `loader` page.

## Create Loader

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

## Use Loader

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

## Finalize Step

- Format using `bun run format`.
- Commit with "setup react-router loader example".

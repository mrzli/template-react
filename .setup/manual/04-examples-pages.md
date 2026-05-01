# Examples Pages

## Create Pages Structure for Examples

- This section will provide the structure for files and comoponents showcasing the features described in subsequent steps.
- Create `src/app/examples/` directory if it does not already exist.

### Stub Page Structure

- Nothing to do here, this is just for reference for future steps.
- This is the structure of any new page where no content was defined:
- Component name should be in `PascalCase` of the file name.
- Content should be a single `div`, with the `kebab-case` of the file name as its text content.
- Example for a file named `home-page.tsx`:
  ```tsx
  import type { FC } from 'react';

  export const HomePage: FC = () => {
    return <div>home-page</div>;
  };
  ```

### Create `home-page.tsx` File in `app` Directory

- This will be a starting page for the app.
- It will not be accessible until routing is set up.
- Create `home-page.tsx` file under `src/app/` directory.
- It should be a stub page.

### Create `home-page.tsx` File in `examples` Directory

- This will be starting page for the examples section.
- This page is separate from the `home-page.tsx` in `app` directory.
- Create `home-page.tsx` file under `src/app/examples/` directory.
- Simply copy the content of `App` component into `home-page.tsx` file.
- Rename the component to `HomePage`.

### Create `examples-page.tsx` File in `examples` Directory

- This will be the root page for the examples section.
- Create `examples-page.tsx` file under `src/app/examples/` directory.
- It should be same as a stub page, but instead of the text inside `div`, it should contain the `<HomePage />`.

### Update `App` Component

- The `App` component should simply render `div` and `<ExamplesPage />` inside it, for now.
- Remove all unnecessary code outside of that, including imports.

### Finalize Step

- Format using `bun run format`.
- Commit with "create examples pages structure".


# Clean Up Basic App Code

## CSS Updates

- Keep `index.css` file, but delete all its content.
- Remove all other CSS files and their imports.

## Image Updates

- Make sure there is exactly one image in `src/assets/` and one image in `public/`.
- Add, remove, replace images as necessary.
- For example, have `react.svg` in `src/assets/` and `vite.svg` in `public/`.
- Update imports and uses accordingly.
- Images in `src/assets/` should be imported as modules, usually using a relative path.
- Images in `public/` are imported by starting the path with `/`, where the subsequent path is relative to `public/`.
  - For example, if you have `vite.svg` directly under `public/`, you can import it with `/vite.svg`.

## Update `App.tsx`

- Create `src/app/` directory if it does not already exist.
- Rename to `app.tsx` (uncapitalize) and move to `src/app/` directory.
- Update all imports inside `app.tsx` to reflect the new location.
- Update all imports that referenced previous `App.tsx` file to reference the new location and name.
- Update component to be exported explicitly as a named export, at the definition point.
- Remove any remaining default exports.
- Update imports that reference the component to import the named export.
- Change the component definition to a lambda. Variable type shoule be `FC`, imported from `react`.
- Simplify the component by following the subsequent instructions.
- Remove all code related to state, effects, event handlers, or any other logic. Convert it to a simple presentational component.
- Make root element a `div` with no class or styles.
- Have some text, maybe a `h1` and a `p` element.
- Leave two image elements referencing one image from `src/assets/` and one from `public/`.
- Add some basic inline styles typed as `CSSProperties`. These need to imported a as `import type { CSSProperties } from 'react';`.
- In the end it should look something like this:
  ```tsx
  import type { CSSProperties, FC } from 'react';

  import viteLogo from '/vite.svg';

  import reactLogo from '../assets/react.svg';

  const imageContainerStyle: CSSProperties = {
    height: '4rem',
  };

  const imageStyle: CSSProperties = {
    display: 'flex',
    gap: '1rem',
    marginTop: '1rem',
  };

  export const App: FC = () => {
    return (
      <div>
        <h1>template-react</h1>
        <p>App is running.</p>
        <div style={imageContainerStyle}>
          <img alt='Vite logo' src={viteLogo} style={imageStyle} />
          <img alt='React logo' src={reactLogo} style={imageStyle} />
        </div>
      </div>
    );
  };

## Finalize Step

- Format using `bun run format`.
- Commit with "cleanup basic app code".

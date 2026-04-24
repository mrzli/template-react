# Steps

- Remove any invalid `.git` directory already present in repo root.
- Setup React + Vite project.
  - Create a dir called `tmp/` inside repo root.
  - Navigate into `tmp/`.
  - Run `bun create vite trading-web --template react-ts --no-interactive` to create the project files.
  - Navigate back to repo root.
  - Copy newly created project files into repo root using `cp -a tmp/trading-web/. .`.
  - remove the `tmp/` directory with `rm -rf tmp`.
  - Commit the changes with a message like "initial project setup with React + Vite".
- Copy files from `.setup/files/` into project root using `cp -a .setup/files/. .`.
  - Commit the changes with a message like "copy setup files".
- Install dependencies using `bun install`.
  - Change `minimumReleasaseAge` in `bunfig.toml` if necessary.
  - Commit the changes with a message like "install dependencies".
- Setup linting and formatting.
  - Execute `bun add -d esling-plugin-simple-import-sort prettier`
  - Update `esling.config.js`:
    - Setup `eslint-plugin-simple-import-sort`:
      - Add import:
        ```js
        import simpleImportSort from 'eslint-plugin-simple-import-sort';
        ```
      - Update the main config object:
        - Add a `plugins` field, as an object, if it does not already exist.
        - Add a `rules` field, as an object, if it does not already exist.
      - Add to `plugins` object:
        ```js
        'simple-import-sort': simpleImportSort,
        ```
      - Add to `rules` object:
        ```js
        'simple-import-sort/imports': 'error',
        'simple-import-sort/exports': 'error',
        ```
  - Update `package.json`:
    - Remove any existing `lint` and `format` scripts.
    - Add to the `scripts` section:
      ```json
      "pretty": "prettier --write .",
      "lint": "eslint .",
      "lint:fix": "eslint . --fix",
      "format": "bun run pretty && bun run lint:fix"
      ```
  - Commit the changes with a message like "setup linting and formatting".
- Format project files with `bun run format`.
  - Commit the changes with a message like "format project files".
- Clean up basic app code:
  - CSS updates:
    - Keep `index.css`, but delete all its content.
    - Remove all other CSS files and their imports.
  - Image updates:
    - If either `src/assets/` or `public/` does not have any appropriate images, add some, or copy one from the other directory.
    - Remove all but one image from `src/assets/`.
    - Updates imports and uses accordingly. Imports are relative.
    - Remove all but one image from `public/`.
    - Update imports and uses accordingly. Imports start with `/` and they are then relative to `public/`.
  - Update `App.tsx`:
    - Rename to `app.tsx` (lowercase).
      - Update imports that reference it.
    - Move `app.tsx` into `src/app/` directory.
      - Create `src/app/` if it does not already exist.
      - Update imports that reference it.
      - Update its imports to account for the move.
    - Update `app.tsx` code:
      - Update exports to export directly, and remove any default export. Update imports that reference the component.
      - Change the component to be a functional one, with Type `FC` from `react`.
      - Simplify the component code:
        - Remove all code related to state, effects, event handlers, or any other logic. Keep it a simple presentational component.
        - Make root element a `div` with no class or styles.
        - Have some text, maybe a `h1` and a `p` element.
        - Leave two image elements referencing one image from `src/assets/` and one from `public/`.
        - Add some basic inline styles typed as `CSSProperties`. These need to imported a as `import type { CSSProperties } from 'react';`.
        - Leave something like this:
          ```tsx
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
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "cleanup basic app code".
- Setup basic routing:
  - Add react-router dependency with `bun add react-router`.
  - Create stub pages:
    - Put them under `src/app/` directory.
    - Call them `home-page.tsx` and `about-page.tsx`.
    - Content should just be the kebab-cased name of the component as text content of a `div`
      - For example, `home-page.tsx` should return `<div>home-page</div>`.
  - Create `src/routing/router.tsx` file:
    - Create root directory `src/routing/` if it does not already exist.
    - Initially, just have basic routing without any actions and loaders.
    - Use 'data mode'.
    - This is the skeleton:
      ```tsx
      import { createBrowserRouter } from 'react-router';

      export const router = createBrowserRouter([]);
      ```
    - Root route should render `App` component. It will have child routes, to be added in next steps:
      ```tsx
      {
        path: '/',
        element: <App />,
        children: []
      }
      ```
    - Add the two stub pages as child routes:
      - Code:
        ```tsx
        {
          index: true,
          element: <HomePage />
        },
        {
          path: 'about',
          element: <AboutPage />
        }
        ```
      - `HomePage` should be rendered if there is no subpath (index route).
  - Change `src/main.tsx` to use the router:
    - You need to set this up so that the routing hierarchy is used, instead of just rendering `App` directly.
    - Render code:
      ```tsx
      import { RouterProvider } from 'react-router';
      import { router } from './routing/router';

      // ...
      /* ... */.render(
        <StrictMode>
          <RouterProvider router={router} />
        </StrictMode>
      );
      ```
  - Finally update `App` component:
    - First, copy all the content of `App` component into `HomePage` component. Leave `App` with simple `<div>app</div>` content.
    - Add imports of `Link` and `Outlet` from `react-router`.
    - Have a navigation section with `Link` components linking to the two routes.
    - Add an `Outlet` component to render the child routes.
    - Example code:
      ```tsx
      import type { CSSProperties, FC } from 'react';
      import { Link, Outlet } from 'react-router';

      const navStyle: CSSProperties = {
        display: 'flex',
        gap: '1rem',
        padding: '1rem',
      };

      const linkStyle: CSSProperties = {
        textDecoration: 'none',
        color: '#2563eb',
      };

      export const App: FC = () => {
        return (
          <div>
            <nav style={navStyle}>
              <Link style={linkStyle} to=''>
                Home
              </Link>
              <Link style={linkStyle} to='about'>
                About
              </Link>
            </nav>
            <Outlet />
          </div>
        );
      };
      ```
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup basic routing".
- Setup 'examples' subpages:
  - Create `src/app/examples/` directory.
  - Create stub pages under this dir:
    - `examples-page.tsx`.
    - `home-page.tsx`.
    - `about-page.tsx`.
  - Initially, all should just return the simple `div` as described above.
  - Remove the `src/app/about-page.tsx` file.
  - Update `src/routing/router.tsx` file:
    - Remove the `about` route from the root level.
    - Add `examples` route as child of root route, and have it have children.
    - Add `src/app/examples/home-page.tsx` as index route of `examples`.
    - Add `src/app/examples/about-page.tsx` as `about` route under `examples`.
  - Update `App` to have link to `examples` page instead of the previous root `about` page.
  - Update `ExamplesPage` to have almost identical routing as `App`, with required path differences ('about' instead of 'examples' link).
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup examples subpages and routing".
- Setup a react-router loader example:
  - Create `loader` directory under `src/app/examples/`.
  - Create `loader-page.tsx` under that directory, with the same stub content as described above.
  - Update `router.tsx`, add a route for `loader` page under `examples` route.
  - Update `ExamplesPage` to have a link to `loader` page.
  - Add new file called `loader.ts` under `examples/loading/` directory.
    - Add a lambda function:
      - Variable name: `loader`.
      - It should be an async function, and it should return a promise.
      - Promise resolves after 500ms.
      - Returns a string `'resolved data'`.
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
  - Add the loader to the `loader` route in `router.tsx`:
    ```tsx
    {
      path: 'loader',
      element: <LoaderPage />,
      loader: loader,
    }
    ```
  - Update `LoaderPage` to use loader data:
    - Add line: `const data = useLoaderData<typeof loader>();`
    - Display the data in a page, in a `div` for example.
    - Code example:
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
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup react-router loader example".
- Update application setup:
  - Create `src/setup/` directory.
  - Have an `index.ts` file that exports everything from any future subdectories and files.
  - Create a `run.tsx` file:
    ```tsx
    export const run = async () => {
      const root = document.getElementById('root');

      if (!root) {
        throw new Error('Root element not found');
      }

      const content = (
        <StrictMode>
          <RouterProvider router={router} />
        </StrictMode>
      );

      createRoot(root).render(content);
    };
    ```
  - Update `index.ts` to export everything from `run.tsx`.
  - Update `src/main.tsx` to import and call the `run` function.
    - It should contain nothing but call to run, import for `index.css` and import for the `run` function itself.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "update application setup and entry point".
- Setup app context:
  - Create `context/` directory under `src/setup/`.
  - Create files for context:
    - Create value type for context in `app-context-value.ts`.
      - Make it a very simple interface, with just `appName: string` field.
      - Code:
        ```ts
        export interface AppContextValue {
          readonly appName: string;
        }
        ```
    - Create the `app-context.ts` file:
      - `export const AppContext = createContext<AppContextValue | undefined>(undefined);`
    - Create the provider component in `app-context-provider.tsx`:
      - Create a functional component (as lambda) called `AppContextProvider`.
      - Code:
        ```tsx
        export interface AppContextProviderProps {
          readonly value: AppContextValue;
          readonly children: ReactNode;
        }

        export const AppContextProvider: FC<AppContextProviderProps> = ({
          value,
          children,
        }) => {
          return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
        };
        ```
    - Create a custom app context hook file `use-app-context.ts`:
      ```tsx
      export const useAppContext = (): AppContextValue => {
        const context = useContext(AppContext);
        if (context === undefined) {
          throw new Error('useAppContext must be used within an AppContextProvider');
        }
        return context;
      };
      ```
    - Add an index file which exports everything from the context directory.
  - Update `run.tsx` to wrap the app in the context provider.
  - Add an example file for context, with the necessary route and links.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup app context and example page".
- Setup app dependencies:
  - Create `app-dependencies.ts` file under `src/setup/`.
  - For now, just have a stub interface for dependencies, with no actual dependencies in it.
    - Code:
      ```ts
      export interface AppDependencies {
        // Add your app dependencies here
      }
      ```
  - Export the dependencies interface in the `index.ts` file.
  - Add `dependencies` field to context value, remember to initialize it.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup app dependencies in context".
- Setup env:
  - Add `zod` dependency with `bun add zod` if not already added.
  - Create `env/` directory under `src/setup/`.
  - Have two example env variables in an env file:
    - `VITE_EXAMPLE_VAR=example`
    - `VITE_BACKEND_BASE_URL=http://localhost:3000`
  - Create files for handling env:
    - `app-env-raw-base.ts`:
      ```ts
      export type AppEnvMode = 'development' | 'production' | string;

      export interface AppEnvRawBase {
        readonly MODE: AppEnvMode;
        readonly BASE_URL: string;
        readonly PROD: boolean;
        readonly DEV: boolean;
        readonly SSR: boolean;
      }
      ```
    - `app-env-raw.ts`:
      ```ts
      export interface AppEnvRawExplicit {
        readonly VITE_EXAMPLE_VAR: string;
        readonly VITE_BACKEND_BASE_URL: string;
      }

      export type AppEnvRaw = AppEnvRawExplicit & AppEnvRawBase;

      export const APP_ENV_RAW: AppEnvRaw = {
        MODE: import.meta.env.MODE,
        // rest of the base env variables...
        VITE_EXAMPLE_VAR: import.meta.env.VITE_EXAMPLE_VAR,
        VITE_BACKEND_BASE_URL: import.meta.env.VITE_BACKEND_BASE_URL,
      };
      ```
    - `app-env-parsed.ts`:
      ```ts
      const APP_ENV_BASE_SCHEMA = z.object({
        MODE: z.string(),
        BASE_URL: z.url(),
        PROD: z.boolean(),
        DEV: z.boolean(),
        SSR: z.boolean(),
      });

      const APP_ENV_SCHEMA = z.object({
        ...APP_ENV_BASE_SCHEMA.shape,
        VITE_EXAMPLE_VAR: z.string(),
        VITE_BACKEND_BASE_URL: z.url(),
      });

      export type AppEnvParsed = z.infer<typeof APP_ENV_SCHEMA>;

      export const appEnvParsed = (): AppEnvParsed => {
        return APP_ENV_SCHEMA.parse(APP_ENV_RAW);
      };
      ```
    - `app-env.ts`:
      ```ts
      export interface AppEnv {
        readonly mode: AppEnvMode;
        readonly baseUrl: string;
        readonly prod: boolean;
        readonly dev: boolean;
        readonly ssr: boolean;
        readonly exampleVar: string;
        readonly backendBaseUrl: string;
      }

      export const appEnv = (): AppEnv => {
        const parsed = appEnvParsed();
        return envRawToEnv(parsed);
      };

      const envRawToEnv = (raw: AppEnvParsed): AppEnv => {
        return {
          mode: raw.MODE,
          baseUrl: raw.BASE_URL,
          prod: raw.PROD,
          dev: raw.DEV,
          ssr: raw.SSR,
          exampleVar: raw.VITE_EXAMPLE_VAR,
          backendBaseUrl: raw.VITE_BACKEND_BASE_URL,
        };
      };
      ```
    - Add an index file.
  - Add `env` field to context, remember to initialize it.
  - Add sample env file `.env.sample` with the two example env variables:
    ```
    VITE_EXAMPLE_VAR=example
    VITE_BACKEND_BASE_URL=http://localhost:3000
    ```
  - Add actual local env variables in `.env.local` file:
    ```
    VITE_EXAMPLE_VAR=example
    VITE_BACKEND_BASE_URL=http://localhost:3000
    ```
  - Display one of the env variables in the context example page.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup env handling and example page".
- Setup app dependencies:
  - Just create an empty dopendencies type and creator in `src/setup/app-dependencies.ts`:
    ```ts
    export interface AppDependencies {}

    export const createAppDependencies = (env: AppEnv): AppDependencies => {
      return {};
    };
    ```
  - Add any `index.ts` entries if necessary.
  - Add `dependencies` field to context value, remember to initialize it with the `createAppDependencies` function.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup app dependencies and example page".
- Setup api stub:
  - Create `src/api/` directory and `parts/` subdirectory under it.
  - Create sub files:
    - `api-config.ts`:
      ```ts
      export interface ApiConfig {
        readonly backendBaseUrl: string;
      }
      ```
    - `parts/example-api.ts`:
      ```ts
      export interface ExampleApi {
        readonly offline: () => Promise<string>;
      }

      export const createExampleApi = (config: ApiConfig): ExampleApi => {
        return {
          offline: async () => {
            return new Promise((resolve) => {
              setTimeout(() => {
                resolve(`This is an example response. Backend Base URL: ${config.backendBaseUrl}`);
              }, 1000);
            });
          },
        };
      };
      ```
    - Create index files for `parts`.
    - `app-api.ts`:
      ```ts
      export interface AppApi {
        readonly example: ExampleApi;
      }

      export const createAppApi = (config: ApiConfig): AppApi => {
        return {
          example: createExampleApi(config),
        };
      };
      ```
    - Create index file for `api` that exports everything inside it.
  - Update `app-dependencies.ts` to create the api and add it to the dependencies.
  - Add example usage of `offline` api function in the context example page.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup api stub and example usage".
- Expand api stub:
  - Add a new function in example api which uses `fetch` to get some data from a public api:
    - Call it `jsonPlaceholder`.
    - It should accept an `id` parameter, which is a number.
    - It should fetch data from `https://jsonplaceholder.typicode.com/posts/:id`.
    - It should return the response as json. Put type in same file.
  - Expan api example page to include that:
    - Display it in `pre` tag, pretty printed with `JSON.stringify(post, undefined, 2)`.
    - Style it with border, padding, and light gray background, and 'auto' overflow for x axis.
    - Use non-tailwind styling for this, with inline styles.
    - Use suspense etc, just like with `offline` function.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "expand api stub and example usage".
- Setup tailwind:
  - Install dependencies:
    - `bun add -d tailwindcss @tailwindcss/vite prettier-plugin-tailwindcss`
  - Update prettier config, add:
    ```json
    "plugins": ["prettier-plugin-tailwindcss"]
    ```
  - Update `vite.config.ts`:
    - Add import: `import tailwindcss from '@tailwindcss/vite';`
    - Add to plugins array: `tailwindcss()`
  - Update `index.css`:
    - Add `@import 'tailwindcss';`
  - Add example for tailwind usage:
    - Add stub `app/examples/tailwind-page.tsx`.
    - Add some tailwind classes to the `div`, for example: `text-2xl text-blue-500 bg-orange-200`.
  - Add route to `router.tsx`.
  - Add link to `ExamplesPage`.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup tailwind and example page".
- Setup icons:
  - Install dependencies:
    - `bun add @iconify/react`
  - Add example for icon usage:
    - Add stub `app/examples/icons-page.tsx`.
    - Add some icons to it:
      - Import `import { Icon } from '@iconify/react';`
      - Add these icons to the page:
        ```tsx
        <Icon icon='cif:hr' width='500' height='300' />
        <Icon icon='mdi:linkedin' width='48' height='48' color='#0a66c2' />
        <Icon icon='mdi:github' width='48' height='48' color='#181717' />
        <Icon icon='mdi:stackoverflow' width='48' height='48' color='#f48024' />
        ```
  - Add route to `router.tsx`.
  - Add link to `ExamplesPage`.
  - Run `bun run format` to format the updated files.
  - Commit the changes with a message like "setup icon library and example page".
- Setup storybook:
  - For reference, you can see what needs to be done by executing:
    - `bun create storybook@latest --features docs`
  - Install dependencies:
    - `bun add -d @storybook/react @storybook/addon-essentials @storybook/builder-vite @storybook/addon-interactions`
  - Initialize storybook with `npx storybook init --builder @storybook/builder-vite`.
  - Add a sample story for `Button` component:
    - Create `src/stories/Button.stories.tsx` file.
    - Add a simple button component and a story for it.
  - Run storybook with `bun run storybook`.
  - Commit the changes with a message like "setup Storybook and add sample story".

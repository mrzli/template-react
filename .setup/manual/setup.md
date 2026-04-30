# Steps

## TODO

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

# Project setup plan

All input file paths for this are this directory, `.setup`. Project needs to be created.

Single source of truth for stack, environment, steps, and conventions. This project will later be a React app; this document defines how to bootstrap and maintain it.

Use `bun` for all javascript ecosystem tooling and package management. Do not use `node`, `npm`, `pnpm` or `yarn` for running any scripts if not absolutely necessary! Feel free to use other tools such as `bash`, `ruby`, `python` or whatever is needed and appropriate.

Do just the steps specified in 'Setup steps' and anything else that is implied by conventions and required to make the project runnable. Do not add other dependencies or tools unless specified.

## Placeholders

When a value is not fixed (e.g. differs per clone or machine), we use **angle brackets** in this doc and in script comments:

| Placeholder      | Meaning                                                                                                                                             |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<root>`         | Project root directory (where `.setup/` lives). Not an absolute path; resolve at runtime (e.g. script’s working directory or `$(dirname "$0")/..`). |
| `<project-name>` | Human or package name of the project (e.g. for `package.json` `name`, README title).                                                                |

This follows common CLI/man-style convention: replace `<placeholder>` with your actual value. Do not use curly braces `{...}` here so as to avoid confusion with shell variables or templating syntax.

## Conventions

- Setup definition:
  - Lives in `.setup/` (this file and `setup.sh`). Do not put app documentation here.
- Documentation:
  - API reference, runbooks, generated docs go in `docs/` when added.
- Code:
  - All source code files names will be in kebab-case, including React components (e.g. `my-component.tsx`), to avoid confusion and maintain consistency.
  - All exports should be named unless there is a strong reason otherwise.
    - This includes React components.
  - All React components will go under `src/app/`.
  - Routing will go under `src/routing/`.
  - Other things choose as appropriate, I will explicitly specify here later on if needed.
  - When both options are appropriate, prefer interface over type for types.
    - However, if type inheritance is needed when using interfaces, prefer type with intersection instead.
  - Use `readonly` for fields whenever possible, and use readonly arrays and tuples instead of mutable ones when possible.
  - All branching and looping should be implemented using a block statement (e.g. `{}`) even if it is not strictly required, to avoid confusion and maintain consistency.
  - All lambda functions which return `void` (or `Promise<void>` for async ones) should be implemented with a block body (e.g. `{}`) even if it is not strictly required, to avoid confusion and maintain consistency.
    - Do the same for functions which return other types, if that return value is meant to be ignored (e.g. many event handlers).

## Stack

- **Runtime / build:** Bun. Package manager is assumed available.
- **App:** React, Vite, TypeScript.

## Environment

- No env vars required for initial setup.
- Add `.env` / `.env.local` for secrets or config when needed; keep `.env*` in `.gitignore` where appropriate.

## Setup steps

- Create a simple project. You can use CLI tooling for such purposes.
  - Use `##-setup-react-vite.py` to do this. Pass in the project name, equal to the root directory name of this project.
  - Do not install dependencies yet.
- Copy any files and directories from `files`.
  - Use `##-copy-files.py` for this.
  - Replace any placeholders in those files with the actual values (e.g. `<project-name>` with the project name).
  - In any future steps, do not edit `.vscode/settings.json` or `.prettierrc` files, as they are already set up with the correct configuration.
- Install dependencies.
- Remove most of the components and styles.
  - Use `##-cleanup-components.py` for this.
- Add linting and formatting.
  - Use `##-setup-linting.py` for this.
- Add Tailwind.
  - Remember to run the install command after.
  - Update `App.tsx` to showcase a simple Tailwind usage (e.g. a styled div with some text).
- Add Storybook.
  - This step is optional. Prompt the user whether they want it or not, and only add it if they say yes.
  - Consider using `bun create storybook@latest --features docs --yes` for initial installation.
  - `stories` directory should be outside of `src`, on the same level.
  - Do not use all the default features, use only essentials and `docs`.
  - Remove all the default stories added by the Storybook setup.
  - Add just one simple story to be able to showcase that the Storybook is working. Use best practices for that story (e.g. CSF format, args, controls, docs).
    - The component should use Tailwind, to make sure that Tailwind is working in Storybook as well.
  - Check the setup:
    - Make sure there is no `stories` directory in `src`.
    - Make sure that the `stories` directory is on the same level as `src`, and that it only contains the story file you added.
    - Make sure that the Storybook is configured to use that `stories` directory and not any other one.
    - Make sure that Tailwind styles work with Storybook (no need to run, just check any configuration).
    - Check that the configuration files are only referencing the features you are actually using (e.g. no addons that you are not using).
- Add React Router.
  - Use tht 'Data' mode with loaders and actions.
  - Add just two simple routes rendered under `App` component to be able to showcase that the routing is working.
  - Use best practices for that (e.g. separate route components, use of loaders and actions).
  - For loaders and actions, just use to simples possible solution to render something, hardcode, or use frontend-only in-memory data, do not add any backend or API for that.
- Add React Toolkit support.
  - Use best practices for that (e.g. create a slice, use hooks).
  - Use `src/store/` for the store setup and slices.
  - Create a minimal example which showcases the store and state management.
    - In the example, showcase RTK query usage with a simple in-memory data source (e.g. a hardcoded array or an in-memory object). Do not add any backend or API for that.
    - Make sure to use proper cache invalidation to avoid stale data in the example.
  - Slices should be stored under `slices/` subdirectory.
  - Api should be stored under `api/` subdirectory.
  - Slices, api and the main store directory should all have index files for easier imports.
    - Each index file should export all files in that directory, and all direct subdirectories, which will each have their index files for recursive exporting.
- Add low level controls.
  - Add `shadcn/ui` to the project.
  - This may require you to first add path aliases to the tsconfing and vite config, so do that if needed.
  - Add all components to the project.
    - Components should be added directly under `src/controls/` directory.
  - Extract variant functions of the components into separate files.
    - For example, `buttonVariants` function for the button component should be extracted into `button-variants.ts` file.
    - Make sure that the new files have correct imports.
      - Specifically, original component files will probably not need to import `cva` from `'class-variance-authority'`.
      - Also, variant files will probably not need `type VariantProps` from `'class-variance-authority'`.
      - Additionally, if you are left with an `import { type VariantProps }`, it can be changed to `import type { VariantProps }` for better readability and consistency.
  - There should be an index file exporting all the files in that directory.
  - Add another page to the app where all of the components and variants are showcased.
    - Read the `controls` directory to find out what all of the controls are, the use each of them, alphabetically on this showcase page.
- Finalize the setup.
  - Check for conventions and consistency across the project, and fix any issues if needed.
  - Make sure to format the entire project, specifically the source code files.
    - For example, make sure that all quotes are consistent, and other linting/prettier rules are followed.
  - Make sure that code files don't have unused imports.
  - Delete any log or temporary files created during the setup.

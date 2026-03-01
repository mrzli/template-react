# Project setup plan

All input file paths for this are this directory, `.setup`. Project needs to be created.

Single source of truth for stack, environment, steps, and conventions. This project will later be a React app; this document defines how to bootstrap and maintain it.

Use `bun` for all javascript ecosystem tooling and package management. Do not use `node`, `npm`, `pnpm` or `yarn` for running any scripts if not absolutely necessary! Feel free to use other tools such as `bash`, `ruby`, `python` or whatever is needed and appropriate.

Do just the steps specified in 'Setup steps' and anything else that is implied by conventions and required to make the project runnable. Do not add other dependencies or tools unless specified.

## Placeholders

When a value is not fixed (e.g. differs per clone or machine), we use **angle brackets** in this doc and in script comments:

| Placeholder        | Meaning |
| ------------------ | ------- |
| `<root>`           | Project root directory (where `.setup/` lives). Not an absolute path; resolve at runtime (e.g. script’s working directory or `$(dirname "$0")/..`). |
| `<project-name>`   | Human or package name of the project (e.g. for `package.json` `name`, README title). |

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

## Stack

- **Runtime / build:** Bun. Package manager is assumed available.
- **App:** React, Vite, TypeScript.
- **Tooling:** None for now.

## Environment

- No env vars required for initial setup.
- Add `.env` / `.env.local` for secrets or config when needed; keep `.env*` in `.gitignore` where appropriate.

## Setup steps

- Create a simple project. You can use CLI tooling for such purposes.
  - I recommend you use `bun create vite . --template react-ts --no-interactive`.
  - You will need to create it in a temporary directory and then copy the files over, because it will otherwise complain about the directory not being empty.
  - Rename the project name in `package.json` and `index.html` to the name of the project directory.
  - Do not install dependencies yet.
- Copy any files and directories from `files` keeping the structure underneath it, and replacing any placeholders in those files.
  - In any future steps, do not edit `.vscode/settings.json` or `.prettierrc` files, as they are already set up with the correct configuration.
- Install dependencies.
- Remove most of the components and styles.
  - Keep `App.tsx` and `index.css` with just some minimal placeholder content, so that the project is runnable and shows something on the screen.
  - Rename `App.tsx` to `app.tsx` and move under `src/app/` to follow the conventions.
  - Make sure `app.tsx` exports a React component as a named export `App` (not default export), again to follow the conventions.
  - Remove all other app files.
- Add linting and formatting.
  - I recommend ESLint and Prettier, but you can choose other tools if you prefer.
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

# Project setup plan

All input file paths for this are this directory, `.setup`. Project needs to be created.

Single source of truth for stack, environment, steps, and conventions. This project will later be a React app; this document defines how to bootstrap and maintain it.

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
  - All React components will go under `src/app/`.
  - Routing will go under `src/routing/`.
- See `.github/copilot-instructions.md` for other coding conventions and guidelines.

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
- Add React Router.
  - Use `##-setup-react-router.py` for this.
- Add Tailwind.
  - Use `##-setup-tailwind.py` for this.
- Add Redux Toolkit.
  - Use `##-setup-redux.py` for this.
- Add `shadcn/ui` components.
  - First use `##-a-setup-shadcn-install.py` to add the shadcn/ui components to the project.
    - Components should be added directly under `src/controls/` directory.
  - Next use `##-b-setup-shadcn-refactor.py` to change the component code to follow the conventions defined in this project.
  - Next use `##-c-setup-shadcn-integration.py` to create a showcase page for the controls.
- Add storybook.
  - This step is optional. Prompt the user whether they want it or not, and only add it if they say yes.
  - Use `##-setup-storybook.py` for this.
- Finalize the setup.
  - Check for conventions and consistency across the project, and fix any issues if needed.
  - Make sure to format the entire project, specifically the source code files.
    - For example, make sure that all quotes are consistent, and other linting/prettier rules are followed.
  - Make sure that code files don't have unused imports.
  - Delete any log or temporary files or directories created during the setup.

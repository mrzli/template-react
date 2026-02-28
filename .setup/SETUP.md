# Project setup plan

All input file paths for this are this directory, `.setup`. Project needs to be created.

Single source of truth for stack, environment, steps, and conventions. This project will later be a React app; this document defines how to bootstrap and maintain it.

Use `bun` for all javascript ecosystem tooling and package management. Do not use `node`, `npm`, `pnpm` or `yarn` for running any scripts if not absolutely necessary! Feel free to use other tools such as `bash`, `ruby`, `python` or whatever is needed and appropriate.

## Placeholders

When a value is not fixed (e.g. differs per clone or machine), we use **angle brackets** in this doc and in script comments:

| Placeholder        | Meaning |
| ------------------ | ------- |
| `<root>`           | Project root directory (where `.setup/` lives). Not an absolute path; resolve at runtime (e.g. script’s working directory or `$(dirname "$0")/..`). |
| `<project-name>`   | Human or package name of the project (e.g. for `package.json` `name`, README title). |

This follows common CLI/man-style convention: replace `<placeholder>` with your actual value. Do not use curly braces `{...}` here so as to avoid confusion with shell variables or templating syntax.

## Conventions

- **Setup definition** lives in `.setup/` (this file and `setup.sh`). Do not put app documentation here.
- **App docs** (API reference, runbooks, generated docs) go in `docs/` when added.
- **Cursor:** Project rules and agent guidance in `.cursor/`; they may reference `.setup/SETUP.md`.

## Stack

- **Runtime / build:** Bun. Package manager is assumed available.
- **App:** React, Vite, TypeScript.
- **Tooling:** None for now.

## Environment

- No env vars required for initial setup.
- Add `.env` / `.env.local` for secrets or config when needed; keep `.env*` in `.gitignore` where appropriate.

## Setup steps

1. Create a simple project. You can use CLI tooling for such purposes. Do not install dependencies yet.
    1. I recommend you use `bun create vite . --template react-ts --no-interactive`.
    2. You will need to create it in a temporary directory and then copy the files over, because it will otherwise complain about the directory not being empty.
2. Copy any files from `files` keeping the structure underneath it, and replacing any placeholders in those files.
3. Install dependencies.
4. Remove most of the components and styles.
    1. Keep `App.tsx` and `index.css` with just some minimal placeholder content, so that the project is runnable and shows something on the screen.
    2. Remove all other app files.
4. Add following tools:
    1. Storybook.
    2. Prettier.
    3. Tailwind.

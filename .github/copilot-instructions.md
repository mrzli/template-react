# Project Instructions for GitHub Copilot

## Tech Stack

- React + TypeScript
- Vite for bundling/dev server
- Bun for package management and scripts

## Command Conventions

- Prefer Bun commands:
  - `bun install`
  - `bun run dev`
  - `bun run build`
  - `bun run test`
- Do not suggest `node`, `npm`, `pnpm`, or `yarn` unless explicitly requested.
- Feel free to use other tools such as `bash`, `ruby`, `python` or whatever is needed and appropriate.

## Code Style and Quality

- Use TypeScript-first patterns and keep types explicit at module boundaries.
- Prefer functional React components and hooks.
- Avoid one-letter variable names.
- Avoid inline comments unless requested.
- Match existing code style in touched files.
- Make sure to update relevant comments and documentation when making code/configuration changes that affect them.

## React Guidelines

- Use composition over prop-heavy monolith components.
- Keep state as local as possible; lift only when needed.
- Avoid premature global state; introduce it only for truly shared cross-route concerns.
- Memoize only when there is a clear render/perf reason.
- Prefer controlled, typed props and clear component contracts.
- Use tailwindcss for styling; avoid custom CSS when possible, except for initial setup or when necessary for specific cases.
- Use named exports for components and hooks to improve tree-shaking and readability.
- For all TypeScript files, including React component file, use kebab-case when naming the file (e.g. `my-component.tsx`), to avoid confusion and maintain consistency.
- Use `readonly` for fields whenever possible, and use readonly arrays and tuples instead of mutable ones when possible.
- All branching and looping should be implemented using a block statement (e.g. `{}`) even if it is not strictly required, to avoid confusion and maintain consistency.
- All lambda functions which return `void` (or `Promise<void>` for async ones) should be implemented with a block body (e.g. `{}`) even if it is not strictly required, to avoid confusion and maintain consistency.
  - Do the same for functions which return other types, if that return value is meant to be ignored (e.g. many event handlers).
- When both options are appropriate, prefer interface over type for types.
    - However, if type inheritance is needed when using interfaces, prefer type with intersection instead.

## Vite Guidelines

- Use `import.meta.env` for environment variables.
- Only expose client-safe variables via the `VITE_` prefix.
- Do not hardcode secrets in frontend code.

## Project Structure Preferences

- Prefer a clear `src/` organization by feature or domain.
- Co-locate component-specific styles/tests with components when practical.
- Keep shared utilities in dedicated `lib/` or `utils/` areas.

## Dependency and Library Guidance

- Favor lightweight, actively maintained libraries.
- Minimize dependencies; use platform/browser APIs when sufficient.
- When proposing a new dependency, include a short justification and tradeoff.

## Testing and Validation

- Add or update tests for meaningful logic changes when test setup exists.
- For UI behavior, prefer user-focused tests over implementation-detail tests.
- After changes, run the smallest relevant checks first, then broader checks.

## Copilot Behavior Expectations

- Make minimal, targeted changes that solve root causes.
- Do not refactor unrelated areas.
- If requirements are ambiguous, ask concise clarifying questions.
- If a requested change affects architecture, propose 2–3 options with tradeoffs, then implement the selected one.

## Additional Notes

- Never alter the following files, either directly or by using terminal commands (after initial copy from `.setup/files`):
  - `.vscode/settings.json`
  - `.prettierrc`
  - `bunfig.toml`

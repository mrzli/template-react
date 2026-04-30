# Setup Linting and Formatting

- Install missing dependencies:
  ```bash
  bun add -d eslint-plugin-simple-import-sort prettier
  ```

## Update Lint Config File

- This refers to `eslint.config.js`.
- You need to setup `eslint-plugin-simple-import-sort` to sort imports and exports.
- Add required import and add (or update) `plugins` and `rules` in the config file:
  ```js
  // ...
  import simpleImportSort from 'eslint-plugin-simple-import-sort';
  // ...

  // ...
    {
      // rest of the main config
       plugins: {
         // other plugins...
         'simple-import-sort': simpleImportSort,
       },
       rules: {
         // other rules...
         'simple-import-sort/imports': 'error',
         'simple-import-sort/exports': 'error',
       },
    }
  // ...
  ```

## Update `package.json`

- Remove any existing `lint` and `format` scripts.
- Add the following scripts:
  ```json
  "scripts": {
    // other scripts...
    "pretty": "prettier --write .",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "bun run pretty && bun run lint:fix",
    "backport": "..."
  }
  ```

## Finalize Step

- Commit with "setup linting and formatting".

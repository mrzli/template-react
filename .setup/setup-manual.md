# Steps

- Remove any invalid `.git` directory already present in repo root.
- Setup React + Vite project.
  - Create a dir called `tmp/` inside repo root.
  - Navigate into `tmp/`.
  - Run `bun create vite trading-web --template react-ts --no-interactive` to create the project files.
  - Navigate back to repo root.
  - Copy newly created project files into repo root using `cp -a tmp/trading-web/. .`.
  - remove the `tmp/` directory with `rm -rf tmp`.
- Copy files from `.setup/files/` into project root using `cp -a .setup/files/. .`.
- Install dependencies using `bun install`.
  - Change `minimumReleasaseAge` in `bunfig.toml` if necessary.
- Setup linting and formatting.
  - Execute `bun add -d esling-plugin-simple-import-sort prettier`
  - Update `esling.config.js`:
    - Setup `eslint-plugin-simple-import-sort`:
      - Add import:
        ```js
        import simpleImportSort from 'eslint-plugin-simple-import-sort'
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
    - Add to the `scripts` section:
      ```json
      "pretty": "prettier --write .",
      "lint": "eslint .",
      "lint:fix": "eslint . --fix",
      "format": "bun run pretty && bun run lint:fix"
      ```
  


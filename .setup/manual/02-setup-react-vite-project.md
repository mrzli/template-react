# Setup React + Vite Project

- Create a dir called `tmp/` inside repo root.
- Navigate into `tmp/`.
- Run script to create the project files:
  ```bash
  bun create vite trading-web --template react-ts --no-interactive
  ```
- Navigate back to repo root.
- Copy newly created project files into repo root using:
  ```bash
  cp -a tmp/trading-web/. .
  ```
- Remove the `tmp/` directory with:
  ```bash
  rm -rf tmp
  ```

## Finalize Step

- Commit with "initial project setup with React + Vite".

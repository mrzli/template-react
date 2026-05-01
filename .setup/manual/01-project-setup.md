# Project Setup

## Clean Up Template Files

- Remove any invalid `.git` directory already present in repo root.

## Setup React + Vite Project

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

### Finalize Step

- Commit with "initial project setup with React + Vite".

## Copy Files from Setup

- Copy files from `.setup/files/` into project root using:
  ```bash
  cp -a .setup/files/. .
  ```

### Finalize Step

- Commit with "copy setup files".

## Add Script for Backporting Setup Files

- Add the following script to `package.json`:
  ```json
  "scripts": {
    // other scripts...
    "backport": "./.setup/backport.sh . ../../templates/template-react"
  }
  ```
- Adjust target path if necessary, to point to `template-react` repo location.

### Finalize Step

- Commit with "add backport script".

## Install Dependencies

- Change `minimumReleasaseAge` in `bunfig.toml` if necessary.
- Install dependencies using `bun install`.

### Finalize Step

- Commit with "install dependencies".


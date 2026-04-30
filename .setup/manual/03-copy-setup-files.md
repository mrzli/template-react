# Copy Setup Files

- Copy files from `.setup/files/` into project root using:
  ```bash
  cp -a .setup/files/. .
  ```

## Add Script for Backporting Setup Files

- Add the following script to `package.json`:
  ```json
  "scripts": {
    // other scripts...
    "backport": "./.setup/backport.sh . ../../templates/template-react"
  }
  ```
- Adjust target path if necessary, to point to `template-react` repo location.

## Finalize Step

- Commit with "copy setup files".

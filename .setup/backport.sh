#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <src-root> <dst-root>" >&2
  exit 1
fi

SRC="$1"
DST="$2"

if [[ ! -d "$SRC" ]]; then
  echo "Error: source directory does not exist: $SRC" >&2
  exit 1
fi

if [[ ! -d "$DST" ]]; then
  echo "Error: destination directory does not exist: $DST" >&2
  exit 1
fi

rm -rf "$DST/.setup" "$DST/.github" "$DST/.vscode"
cp -r "$SRC/.setup" "$SRC/.github" "$SRC/.vscode" "$DST/"
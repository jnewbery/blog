#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
URL="http://${HOST}:${PORT}"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Expected .venv/bin/python but it was not found or not executable." >&2
  exit 1
fi

(.venv/bin/python -m webbrowser "${URL}" >/dev/null 2>&1 &) 

pelican -d -r --listen

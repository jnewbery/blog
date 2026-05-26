#!/usr/bin/env bash
set -euo pipefail

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
URL="http://${HOST}:${PORT}"

# Watch source files and rebuild on changes
uv run pelican -d -r content -o output -s pelicanconf.py &
PELICAN_PID=$!
trap "kill $PELICAN_PID 2>/dev/null" EXIT

# Open browser after a short delay for the initial build to complete
(sleep 2 && python3 -m webbrowser "${URL}" >/dev/null 2>&1 &)

# Serve with proper 404 and range request support
npx serve output --listen "tcp://${HOST}:${PORT}"

#!/usr/bin/env bash
set -euo pipefail
KEY="${1:-}"
OPENCLAW_DIST="$(npm root -g)/openclaw/dist"
if [[ ! -d "$OPENCLAW_DIST" ]]; then
  OPENCLAW_DIST="$(find "$HOME" -maxdepth 4 -type d -path '*/.npm*/lib/node_modules/openclaw/dist' 2>/dev/null | head -n 1 || true)"
fi
[[ -n "$KEY" ]] || { echo "Usage: scripts/schema_probe.sh <search-term>"; exit 1; }
[[ -d "$OPENCLAW_DIST" ]] || { echo "Could not locate openclaw dist directory"; exit 2; }
find "$OPENCLAW_DIST" -maxdepth 1 -type f -name 'config-*.js' -print0 | xargs -0 grep -nF "$KEY" | head -n 120 || true

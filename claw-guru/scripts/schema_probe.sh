#!/usr/bin/env bash
set -euo pipefail

KEY="${1:-}"
DIST_GLOB="$HOME/.npm-global/lib/node_modules/openclaw/dist/config-*.js"

if [[ -z "$KEY" ]]; then
  echo "Usage: $0 <search-term>"
  echo "Example: $0 nativeSkills"
  exit 1
fi

echo "== Searching schema in: $DIST_GLOB"
grep -nE "${KEY}|NativeCommandsSettingSchema|DmPolicySchema|GroupPolicySchema|ReplyToModeSchema|visibility: z.enum|kind: z.union" $DIST_GLOB | head -n 120 || true

echo
echo "Tip: verify exact accepted literals near your key before editing openclaw.json"

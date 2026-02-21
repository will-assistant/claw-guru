#!/usr/bin/env bash
set -euo pipefail

KEY="${1:-}"
DIST_DIR="$HOME/.npm-global/lib/node_modules/openclaw/dist"

if [[ -z "$KEY" ]]; then
  cat <<'USAGE'
Usage: scripts/schema_probe.sh <search-term>
Examples:
  scripts/schema_probe.sh nativeSkills
  scripts/schema_probe.sh DmPolicySchema
USAGE
  exit 1
fi

mapfile -t DIST_FILES < <(find "$DIST_DIR" -maxdepth 1 -type f -name 'config-*.js' | sort)
if [[ ${#DIST_FILES[@]} -eq 0 ]]; then
  echo "No config-*.js files found in: $DIST_DIR" >&2
  exit 2
fi

echo "== OpenClaw config schema probe"
echo "== Dist files:"
printf ' - %s\n' "${DIST_FILES[@]}"
echo

echo "== Symbol/value matches for: $KEY"
# Fixed-string search avoids regex surprises from user input.
grep -nF "$KEY" "${DIST_FILES[@]}" | head -n 120 || true

echo
echo "== Common schema anchors (quick verification)"
grep -nE 'NativeCommandsSettingSchema|DmPolicySchema|GroupPolicySchema|ReplyToModeSchema|tools: z.object\(|sessions: z.object\(\{ visibility: z\.enum|BindingsSchema = z\.array|HeartbeatSchema = z\.object' "${DIST_FILES[@]}" | head -n 200 || true

echo
echo "Tip: inspect nearby lines for exact literals before editing openclaw.json/openclaw.json5"

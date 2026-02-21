# claw-guru build plan

## Goal
Build a production-ready ClawHub skill that gives agents a safe, deterministic workflow for OpenClaw config edits, routing setup, gateway troubleshooting, heartbeat/cron operations, and version migration.

## What I am changing
1. **Rewrite `SKILL.md` trigger description** to be broader and more precise for real support requests (config, routing, Discord/Slack, heartbeat/cron, migrations, schema validation, doctor triage).
2. **Keep `SKILL.md` lean** and procedural (<500 lines body), with strict change protocol and escalation flow.
3. **Expand references** into practical runbooks:
   - `references/config.md`: verified schema values and high-signal config patterns (commands, heartbeat, bindings, sessions visibility, DM/group policies, reply modes).
   - `references/routing.md`: deterministic binding precedence, peer kind correctness, Discord/Slack account/channel patterns, slash command conflict avoidance.
   - `references/troubleshooting.md`: exact error/signature → root cause → exact fix for common gateway/channel issues.
   - `references/version-notes.md`: version-drift table and migration checklist.
4. **Add one utility script** (`scripts/schema_probe.sh`) to quickly verify accepted schema values from local installed dist source before edits.
5. **Validate and package** with OpenClaw skill-creator scripts.
6. **Create/push GitHub repo** `will-assistant/claw-guru`.

## Verification sources
- Local installed OpenClaw dist schema (`~/.npm-global/lib/node_modules/openclaw/dist/config-*.js`) for accepted values.
- OpenClaw docs index and key pages: configuration reference, multi-agent routing, Discord, Slack, heartbeat, gateway troubleshooting.

## Success criteria
- ClawHub-compatible layout
- Accurate, version-aware guidance
- Every troubleshooting item has exact message/signature + cause + exact fix
- Packager + quick validator pass
- Repo committed and pushed

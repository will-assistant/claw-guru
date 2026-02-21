# OpenClaw Troubleshooting Runbook

Format: **Signature** → Root cause → Exact fix.

## Common fixes
- `Application command names must be unique` → command collision → disable `nativeSkills` on one bot.
- `Invalid config ... nativeSkills` → invalid enum → use `true | false | "auto"`.
- `Gateway start blocked: set gateway.mode=local` → mode mismatch → set `gateway.mode: "local"`.
- `refusing to bind gateway ... without auth` → non-loopback without auth → configure `gateway.auth.*`.
- `EADDRINUSE` → port conflict.
- `unknown heartbeat target` / `heartbeat: unknown accountId` → bad routing/account mapping.
- `Discord IDs must be strings` → quote IDs.
- `forbidden` → sessions/channel/auth policy restriction.

## Verification
```bash
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

## Resources
- Gateway troubleshooting: https://docs.openclaw.ai/gateway/troubleshooting.md
- Channel troubleshooting: https://docs.openclaw.ai/channels/troubleshooting.md
- Automation troubleshooting: https://docs.openclaw.ai/automation/troubleshooting.md
- Health: https://docs.openclaw.ai/gateway/health.md
- Logging: https://docs.openclaw.ai/gateway/logging.md
- Heartbeat: https://docs.openclaw.ai/gateway/heartbeat.md
- GitHub: https://github.com/openclaw/openclaw
- Community Discord: https://discord.gg/clawd
- ClawHub: https://clawhub.ai
- Changelog/Releases: https://github.com/openclaw/openclaw/releases

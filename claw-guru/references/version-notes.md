# OpenClaw Version Notes & Migration Guardrails

Use this when config worked before but fails after upgrade.

---

## 1) Always verify against installed dist

```bash
bash scripts/schema_probe.sh <key>
```

Dist source is authoritative for your install:
`~/.npm-global/lib/node_modules/openclaw/dist/config-*.js`

---

## 2) High-impact drift points

### commands.native / commands.nativeSkills
Current verified schema:
- `true | false | "auto"`

If old config uses removed literals, replace with supported values and run:

```bash
openclaw doctor
openclaw gateway restart
```

### Session visibility
Current verified options:
- `self | tree | agent | all`

### Binding peer kinds
Current verified options:
- `direct | group | channel | dm`

### Policy strictness and auth guardrails
Recent versions enforce stricter startup checks for non-loopback binds without auth.
If gateway fails after upgrade, verify `gateway.bind` and `gateway.auth.*` together.

---

## 3) Migration checklist

1. Backup current config.
2. Run `openclaw doctor` and inspect warnings/issues.
3. Probe changed keys with `scripts/schema_probe.sh`.
4. Replace only invalid/removed values.
5. Restart gateway.
6. Run `openclaw channels status --probe`.
7. Smoke-test one DM + one group/channel route.

---

## 4) Install / update checklist for community users

1. Check current version:
```bash
openclaw --version
```
2. Update OpenClaw using your install method.
3. Run:
```bash
openclaw doctor
openclaw gateway restart
openclaw gateway status
openclaw channels status --probe
```
4. Re-test channel auth-sensitive paths (Discord/Slack tokens, webhook paths, pairing).
5. If behavior changed, compare config against current docs and local schema.

---

## 5) Downgrade-safe editing principle

When unsure, prefer broadly accepted values (`true/false` over niche literals), then validate with local schema before restart.
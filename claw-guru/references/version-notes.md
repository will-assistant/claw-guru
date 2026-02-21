# OpenClaw Version Notes & Migration Guardrails

Use this file whenever a config worked before but fails after upgrade.

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

If old config uses removed literals (for example legacy values), replace with supported values and run:

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

## 4) Downgrade-safe editing principle

When unsure, prefer values accepted across more versions (`true/false` over niche literals), then validate with local schema before restart.

# OpenClaw Troubleshooting Runbook

Format: **Exact error/signature** → Root cause → Exact fix.

---

## Table of contents

1. Slash commands / registration
2. Config schema mismatch
3. JSON5 parse/edit mistakes
4. Gateway start blocked
5. Non-loopback bind without auth
6. Port conflict
7. Heartbeat target/account mismatch
8. Routing over-broad / wrong channel responses
9. DM blocked by policy
10. Slack mode/token mismatch
11. Discord ID type mismatch
12. Probe warning misread as outage
13. Sessions visibility forbidden
14. Sub-agent spawn denied

---

## 1) Slash commands / registration

### Error
`Application command names must be unique`

**Root cause**
Multiple Discord bot accounts register overlapping native skill command names.

**Exact fix**
Set `nativeSkills` to false globally or on conflicting accounts.

```json5
{ commands: { nativeSkills: false } }
```

or

```json5
{
  channels: {
    discord: {
      accounts: {
        bot2: { commands: { nativeSkills: false } }
      }
    }
  }
}
```

Verify:
```bash
openclaw gateway restart
openclaw channels status --probe
```

---

## 2) Config schema mismatch

### Error
`Invalid config at openclaw.json: - commands.nativeSkills: Invalid input`

**Root cause**
Configured value is not accepted by installed schema.

**Exact fix**
Use only `true | false | "auto"` for `commands.nativeSkills`.

Verify local schema:
```bash
bash scripts/schema_probe.sh nativeSkills
```

---

## 3) JSON5 parse/edit mistakes

### Error
`Invalid config ...` after manual edits

**Root cause**
Syntax break in JSON5 (unclosed braces, bad commas/quotes, malformed comments).

**Exact fix**
Revert to backup, re-apply minimal edit, run:
```bash
openclaw doctor
```

Avoid validating with strict JSON tools (`python -m json.tool`) because OpenClaw config is JSON5.

---

## 4) Gateway start blocked

### Error
`Gateway start blocked: set gateway.mode=local`

**Root cause**
Gateway mode is not configured for local service start.

**Exact fix**
Set `gateway.mode` to `"local"`, then restart.

```bash
openclaw config set gateway.mode '"local"' --json
openclaw gateway restart
```

---

## 5) Non-loopback bind without auth

### Error
`refusing to bind gateway ... without auth`

**Root cause**
Gateway bind is non-loopback but auth token/password not configured.

**Exact fix**
Configure `gateway.auth.*` before LAN/tailnet/custom bind, then restart.

---

## 6) Port conflict

### Error
`another gateway instance is already listening`
or `EADDRINUSE`

**Root cause**
Port already in use by another process.

**Exact fix**
Stop conflicting process or change bind/port, then restart.

```bash
openclaw gateway status
openclaw gateway restart
```

---

## 7) Heartbeat target/account mismatch

### Errors
`unknown heartbeat target: <value>`

`heartbeat: unknown accountId`

**Root cause**
Heartbeat target/account does not map to a valid configured delivery route.

**Exact fix**
Use `last`, `none`, or valid channel target; use existing account id for that channel (or remove `accountId`).
Then restart and verify logs.

---

## 8) Routing over-broad / wrong channel responses

### Signature
Agent responds in unexpected channels after binding change.

**Root cause**
Binding mismatch (wrong `peer.kind`, `peer.id`, `guildId`, `teamId`, `accountId`) or over-broad lower-tier binding winning.

**Exact fix**
Re-copy IDs; tighten binding specificity.
For Discord text channels use:

```json5
{ peer: { kind: "channel", id: "<channelId>" } }
```

---

## 9) DM blocked by policy

### Signature
Logs show pairing/allowlist/blocked; DMs ignored.

**Root cause**
`dmPolicy` and allowlist/pairing state disallow sender.

**Exact fix**
- `dmPolicy: "pairing"`: approve code
- `dmPolicy: "allowlist"`: add sender
- `dmPolicy: "open"`: include `"*"` in provider `allowFrom`

Verify:
```bash
openclaw pairing list <channel>
openclaw channels status --probe
```

---

## 10) Slack mode/token mismatch

### Signatures
Slack not connecting; auth/event errors when switching socket/http mode.

**Root cause**
Wrong token set for mode:
- Socket mode needs `botToken` + `appToken`
- HTTP mode needs `botToken` + `signingSecret`

**Exact fix**
Set matching credentials for configured `channels.slack.mode`, restart, and re-check probe.

---

## 11) Discord ID type mismatch

### Error
`Discord IDs must be strings (wrap numeric IDs in quotes).`

**Root cause**
Numeric literal used where schema requires string ID.

**Exact fix**
Quote all Discord IDs in config.

---

## 12) Probe warning misread as outage

### Signature
`RPC probe failed / SECURITY ERROR` while service appears running.

**Root cause**
Probe transport/auth mismatch, not always runtime crash.

**Exact fix**
Confirm runtime + logs before rollback:

```bash
openclaw gateway status
openclaw logs --follow
```

---

## 13) Sessions visibility forbidden

### Error
`forbidden` when reading other agent session history.

**Root cause**
`tools.sessions.visibility` too restrictive.

**Exact fix**
Set required scope (often `all` for cross-agent diagnostics):

```json5
{ tools: { sessions: { visibility: "all" } } }
```

Verified values: `self | tree | agent | all`.

---

## 14) Sub-agent spawn denied

### Signature
Spawn attempts fail for target agent.

**Root cause**
`subagents.allowAgents` and/or `tools.agentToAgent.allow` excludes target.

**Exact fix**
Add target IDs in both relevant allowlists and restart gateway.
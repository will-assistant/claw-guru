# OpenClaw Troubleshooting Runbook

Format: **Exact error/signature** → Root cause → Exact fix.

---

## 1) Slash commands / registration

### Error
`Application command names must be unique`

**Root cause**
Multiple Discord bot accounts are registering overlapping native skill command names.

**Exact fix**
Set `nativeSkills` to false globally or on one/more conflicting accounts.

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

## 3) Gateway start blocked

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

## 4) Non-loopback bind without auth

### Error
`refusing to bind gateway ... without auth`

**Root cause**
Gateway bind is non-loopback but auth token/password not configured.

**Exact fix**
Configure auth (`gateway.auth.token` or password mode) before LAN/tailnet/custom bind.
Then restart gateway.

---

## 5) Port conflict

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

## 6) Heartbeat target invalid

### Error
`unknown heartbeat target: <value>`

**Root cause**
`agents.*.heartbeat.target` points to unknown channel id/name.

**Exact fix**
Use `last`, `none`, or a valid configured channel id.
Then restart and verify.

---

## 7) Heartbeat account mismatch

### Error
`heartbeat: unknown accountId`

**Root cause**
Heartbeat `accountId` does not exist for selected target channel.

**Exact fix**
Set an existing account id under `channels.<provider>.accounts.<id>` or remove `accountId`.

---

## 8) Routing over-broad / wrong channel responses

### Signature
Agent responds in unexpected channels after binding change.

**Root cause**
Binding mismatch (often wrong `peer.kind`, `peer.id`, `guildId`, or `accountId`).

**Exact fix**
Re-copy IDs; set exact binding.
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
- `dmPolicy: "open"`: include `"*"` in `allowFrom`

Verify:
```bash
openclaw pairing list <channel>
openclaw channels status --probe
```

---

## 10) Probe warning misread as outage

### Signature
`RPC probe failed / SECURITY ERROR` while service appears running.

**Root cause**
Probe transport/auth mismatch, not always runtime crash.

**Exact fix**
Confirm actual runtime status + logs before rollback.

```bash
openclaw gateway status
openclaw logs --follow
```

---

## 11) Sessions visibility forbidden

### Error
`forbidden` when reading other agent session history

**Root cause**
`tools.sessions.visibility` too restrictive.

**Exact fix**
Set required scope (often `all` for full cross-agent diagnostics):

```json5
{ tools: { sessions: { visibility: "all" } } }
```

Verified values: `self | tree | agent | all`.

---

## 12) Sub-agent spawn denied

### Signature
Spawn attempts fail for a target agent.

**Root cause**
`subagents.allowAgents` and/or `tools.agentToAgent.allow` does not include target.

**Exact fix**
Add target IDs in both relevant allowlists and restart gateway.

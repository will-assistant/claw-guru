# OpenClaw Routing & Multi-Agent Reference

---

## 1) Deterministic binding precedence

Most-specific wins:
1. `match.peer`
2. `match.parentPeer` (if used)
3. `match.guildId + roles` (Discord role routing)
4. `match.guildId`
5. `match.teamId`
6. `match.accountId` (exact)
7. channel-level (`accountId: "*"` or broad channel match)
8. default agent

If multiple entries match in the same tier, first in config order wins.

---

## 2) Binding template

```json5
{
  bindings: [
    {
      agentId: "support",
      match: {
        channel: "discord",
        accountId: "support-bot",
        guildId: "1234567890",
        peer: { kind: "channel", id: "2345678901" }
      }
    }
  ]
}
```

Verified peer kinds: `direct | group | channel | dm`.

---

## 3) Discord routing pitfalls

### Symptom
Agent replies in wrong channels or broadly in guild.

### Common causes
- Wrong `peer.kind`
- Wrong `guildId`/`peer.id`
- Binding attached to wrong `accountId`

### Exact fix
- Use Developer Mode, re-copy IDs.
- For text channels, set `peer.kind: "channel"`.
- Ensure binding references intended bot account.

---

## 4) Multi-account + multi-agent pattern

```json5
{
  agents: {
    list: [
      { id: "main" },
      { id: "forge" }
    ]
  },
  channels: {
    discord: {
      accounts: {
        main: { token: "..." },
        forge: { token: "..." }
      }
    }
  },
  bindings: [
    { agentId: "main",  match: { channel: "discord", accountId: "main" } },
    { agentId: "forge", match: { channel: "discord", accountId: "forge" } }
  ]
}
```

Use account-level routing first; add peer-specific overrides only where needed.

---

## 5) Slash command collisions in multi-bot setups

If Discord returns command uniqueness failures, disable native skill command registration on overlapping bots:

```json5
{
  channels: {
    discord: {
      accounts: {
        forge: { commands: { nativeSkills: false } }
      }
    }
  }
}
```

Global alternative:

```json5
{ commands: { nativeSkills: false } }
```

---

## 6) Cross-agent visibility and messaging

### Session visibility
```json5
{ tools: { sessions: { visibility: "all" } } }
```

Verified options: `self | tree | agent | all`.

### Agent-to-agent messaging
```json5
{
  tools: {
    agentToAgent: {
      enabled: true,
      allow: ["main", "forge", "sentinel"]
    }
  }
}
```

Both source and target agent IDs must be permitted.

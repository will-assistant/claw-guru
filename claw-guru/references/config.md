# OpenClaw Config Reference (verified patterns)

Source of truth for accepted values: local installed schema in
`~/.npm-global/lib/node_modules/openclaw/dist/config-*.js`.

---

## 1) Verified enums / key values

### Commands
- `commands.native`: `true | false | "auto"`
- `commands.nativeSkills`: `true | false | "auto"`
- `commands.restart`: boolean (default true)

> Verified from `NativeCommandsSettingSchema = z.union([z.boolean(), z.literal("auto")])`.

### DM / Group policy
- `dmPolicy`: `"pairing" | "allowlist" | "open" | "disabled"`
- `groupPolicy`: `"open" | "disabled" | "allowlist"`

### Reply threading
- `replyToMode`: `"off" | "first" | "all"`

### Bindings peer kind
- `bindings[].match.peer.kind`: `"direct" | "group" | "channel" | "dm"`

### Session visibility
- `tools.sessions.visibility`: `"self" | "tree" | "agent" | "all"`

---

## 2) Commands block

```json5
{
  commands: {
    native: "auto",
    nativeSkills: "auto",
    text: true,
    config: false,
    debug: false,
    restart: true,
    useAccessGroups: true
  }
}
```

### Multi-agent slash command conflict guard
If multiple Discord bots register duplicate skill/native commands and you see uniqueness errors, set:

```json5
{ commands: { nativeSkills: false } }
```

You can also override per account:

```json5
{
  channels: {
    discord: {
      accounts: {
        botA: { commands: { nativeSkills: false } }
      }
    }
  }
}
```

---

## 3) Heartbeat block

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",      // use "0m" to disable
        target: "last",    // "last" | "none" | channel id/name (validated)
        includeReasoning: false,
        ackMaxChars: 300
      }
    }
  }
}
```

Important behavior:
- If **any** `agents.list[].heartbeat` block exists, only those agents run heartbeat.
- Invalid `heartbeat.target` causes validation issues ("unknown heartbeat target: ...").

---

## 4) Agents + subagents

```json5
{
  agents: {
    list: [
      {
        id: "main",
        workspace: "~/.openclaw/workspace",
        subagents: {
          allowAgents: ["forge", "sentinel"]
        }
      }
    ]
  },
  tools: {
    agentToAgent: {
      enabled: true,
      allow: ["main", "forge", "sentinel"]
    }
  }
}
```

If spawn/message fails between agents, validate both allowlists.

---

## 5) Bindings and routing essentials

```json5
{
  bindings: [
    {
      agentId: "main",
      match: {
        channel: "discord",
        accountId: "default",
        guildId: "123...",
        peer: { kind: "channel", id: "456..." }
      }
    }
  ]
}
```

Notes:
- `channel` is required in each binding.
- Most-specific match wins (peer > guild/team > account > channel fallback).
- For Discord text channels, `peer.kind` should usually be `"channel"`.

---

## 6) Discord and Slack high-signal keys

### Discord
- `channels.discord.token` (or account token)
- `channels.discord.groupPolicy`
- `channels.discord.dmPolicy`
- `channels.discord.guilds.<guildId>.channels.<channelKey>.allow`
- `channels.discord.commands.native`
- `channels.discord.commands.nativeSkills`
- `channels.discord.replyToMode`

### Slack
- `channels.slack.mode`: `"socket" | "http"`
- Socket mode: requires `botToken` + `appToken`
- HTTP mode: requires `botToken` + `signingSecret`
- `channels.slack.groupPolicy`
- `channels.slack.dmPolicy`
- `channels.slack.replyToMode`
- `channels.slack.replyToModeByChatType.direct|group|channel`

---

## 7) Safe edit checklist (copy/paste)

1. Probe schema: `bash scripts/schema_probe.sh <key>`
2. Backup config
3. Edit minimal keys only
4. `openclaw doctor`
5. Restart gateway
6. Probe channel health + logs
7. Roll back if broken

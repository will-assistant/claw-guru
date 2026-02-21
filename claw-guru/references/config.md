# OpenClaw Config Reference (verified patterns)

Source of truth: local installed schema in
`$(npm root -g)/openclaw/dist/config-*.js`.

Use:
```bash
bash scripts/schema_probe.sh <key>
```

---

## Table of contents

1. Verified enums / key values
2. Commands block
3. Heartbeat block
4. Agents + subagents
5. Bindings and routing essentials
6. Discord and Slack high-signal keys
7. Common policy guardrails
8. Safe edit checklist

---

## 1) Verified enums / key values

### Commands
- `commands.native`: `true | false | "auto"`
- `commands.nativeSkills`: `true | false | "auto"`
- `commands.restart`: boolean

Verified from dist:
- `const NativeCommandsSettingSchema = z.union([z.boolean(), z.literal("auto")]);`

### DM / Group policy
- `dmPolicy`: `"pairing" | "allowlist" | "open" | "disabled"`
- `groupPolicy`: `"open" | "disabled" | "allowlist"`

### Reply threading
- `replyToMode`: `"off" | "first" | "all"`

### Bindings peer kind
- `bindings[].match.peer.kind`: `"direct" | "group" | "channel" | "dm"`

### Session visibility
- `tools.sessions.visibility`: `"self" | "tree" | "agent" | "all"`

### Slack mode
- `channels.slack.mode`: `"socket" | "http"`

### Heartbeat target/accountId
- `heartbeat.target` is **string** (not strict enum in schema).
- `heartbeat.accountId` is **string**.

Implication: schema may accept values that runtime later rejects (e.g., unknown target/account). Always verify with `openclaw doctor` + runtime logs.

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
If multiple Discord bots register overlapping commands and you see uniqueness errors:

```json5
{ commands: { nativeSkills: false } }
```

Per account override:

```json5
{
  channels: {
    discord: {
      accounts: {
        your-bot: { commands: { nativeSkills: false } }
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
        every: "30m",
        target: "last",
        includeReasoning: false,
        ackMaxChars: 300
      }
    }
  }
}
```

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
          allowAgents: ["your-agent-a", "your-agent-b"]
        }
      }
    ]
  },
  tools: {
    agentToAgent: {
      enabled: true,
      allow: ["main", "your-agent-a", "your-agent-b"]
    }
  }
}
```

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
        guildId: "YOUR_GUILD_ID",
        peer: { kind: "channel", id: "YOUR_CHANNEL_ID" }
      }
    }
  ]
}
```

---

## 6) Discord and Slack high-signal keys

### Discord
- `channels.discord.token` (or account token)
- `channels.discord.groupPolicy`
- `channels.discord.dmPolicy`
- `channels.discord.commands.native`
- `channels.discord.commands.nativeSkills`

### Slack
- `channels.slack.mode`: `"socket" | "http"`
- Socket mode requires `botToken` + `appToken`
- HTTP mode requires `botToken` + `signingSecret`

---

## 7) Common policy guardrails

- `dmPolicy: "open"` requires `allowFrom` to include `"*"`.
- Discord IDs in config must be strings (quote numeric IDs).

---

## 8) Safe edit checklist (copy/paste)

1. Probe schema: `bash scripts/schema_probe.sh <key>`
2. Backup config
3. Edit minimal keys only
4. `openclaw doctor`
5. Restart gateway
6. Probe channel health + logs
7. Roll back if broken

---

## Resources

- Config docs: https://docs.openclaw.ai/gateway/configuration.md
- Config reference: https://docs.openclaw.ai/gateway/configuration-reference.md
- Multi-agent: https://docs.openclaw.ai/concepts/multi-agent.md
- Heartbeat: https://docs.openclaw.ai/gateway/heartbeat.md
- Troubleshooting: https://docs.openclaw.ai/gateway/troubleshooting.md
- GitHub: https://github.com/openclaw/openclaw
- Community Discord: https://discord.gg/clawd
- ClawHub: https://clawhub.ai
- Changelog/Releases: https://github.com/openclaw/openclaw/releases

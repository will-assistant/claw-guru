# OpenClaw Config Reference (verified patterns)

Source of truth: local installed schema in
`~/.npm-global/lib/node_modules/openclaw/dist/config-*.js`.

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

Verified from dist:
- `const DmPolicySchema = z.enum(["pairing","allowlist","open","disabled"]);`
- `const GroupPolicySchema = z.enum(["open","disabled","allowlist"]);`

### Reply threading
- `replyToMode`: `"off" | "first" | "all"`

Verified from dist:
- `const ReplyToModeSchema = z.union([z.literal("off"), z.literal("first"), z.literal("all")]);`

### Bindings peer kind
- `bindings[].match.peer.kind`: `"direct" | "group" | "channel" | "dm"`

Verified from dist binding schema.

### Session visibility
- `tools.sessions.visibility`: `"self" | "tree" | "agent" | "all"`

Verified from dist `z.enum([...])` in Tools schema.

### Slack mode
- `channels.slack.mode`: `"socket" | "http"`

Verified from dist `z.enum(["socket","http"])`.

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
        botA: { commands: { nativeSkills: false } }
      }
    }
  }
}
```

Slack note: `commands.native: "auto"` does **not** auto-enable Slack native commands.
Use explicit `channels.slack.commands.native: true` (or global `commands.native: true`).

---

## 3) Heartbeat block

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",      // "0m" disables
        target: "last",    // last | none | provider id string (runtime-validated)
        includeReasoning: false,
        ackMaxChars: 300
      }
    }
  }
}
```

Important behavior:
- If **any** `agents.list[].heartbeat` block exists, only those agents run heartbeat.
- Invalid `heartbeat.target` or `accountId` can fail runtime delivery even if schema parse passes.

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
- `match.channel` is required.
- Most-specific match wins (peer > guild/team > account > channel fallback).
- For Discord text channels, `peer.kind` should usually be `"channel"`.
- If a binding sets multiple fields, matching is AND semantics.

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

Delivery target format:
- `user:<id>` for DM
- `channel:<id>` for guild channel
- Bare numeric IDs are rejected.

### Slack
- `channels.slack.mode`: `"socket" | "http"`
- Socket mode requires `botToken` + `appToken`
- HTTP mode requires `botToken` + `signingSecret`
- `channels.slack.groupPolicy`
- `channels.slack.dmPolicy`
- `channels.slack.replyToMode`
- `channels.slack.replyToModeByChatType.direct|group|channel`

---

## 7) Common policy guardrails

- `dmPolicy: "open"` requires `allowFrom` to include `"*"` (provider-specific path).
- Discord IDs in config must be strings (quote numeric IDs).
- Fallback groupPolicy behavior can differ if provider section is missing entirely; prefer explicit provider config.

---

## 8) Safe edit checklist (copy/paste)

1. Probe schema: `bash scripts/schema_probe.sh <key>`
2. Backup config
3. Edit minimal keys only
4. `openclaw doctor`
5. Restart gateway
6. Probe channel health + logs
7. Roll back if broken
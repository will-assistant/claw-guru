# OpenClaw Routing & Multi-Agent Reference

## 1) Deterministic binding precedence
Most-specific wins: peer > parentPeer > guild+roles > guild > team > account > channel > default agent.

## 2) Binding template
```json5
{
  bindings: [
    {
      agentId: "your-agent",
      match: {
        channel: "discord",
        accountId: "your-bot",
        guildId: "YOUR_GUILD_ID",
        peer: { kind: "channel", id: "YOUR_CHANNEL_ID" }
      }
    }
  ]
}
```

## 3) Session key behavior
- DMs usually collapse to main session.
- Channel chats stay isolated per channel/peer.
- Threads add `:thread:<threadId>`.

## 4) Multi-account + multi-agent pattern
```json5
{
  agents: { list: [{ id: "main" }, { id: "your-agent" }] },
  channels: {
    discord: {
      accounts: {
        main: { token: "YOUR_BOT_TOKEN" },
        your-bot: { token: "YOUR_BOT_TOKEN" }
      }
    }
  }
}
```

## 5) Command collisions
Disable native skill registration for overlapping bots:
```json5
{ channels: { discord: { accounts: { your-bot: { commands: { nativeSkills: false } } } } } }
```

## 6) Cross-agent visibility
```json5
{ tools: { sessions: { visibility: "all" } } }
```

## Resources
- Channel routing: https://docs.openclaw.ai/channels/channel-routing.md
- Multi-agent: https://docs.openclaw.ai/concepts/multi-agent.md
- Session tools: https://docs.openclaw.ai/concepts/session-tool.md
- Discord docs: https://docs.openclaw.ai/channels/discord.md
- Slack docs: https://docs.openclaw.ai/channels/slack.md
- Channel troubleshooting: https://docs.openclaw.ai/channels/troubleshooting.md
- GitHub: https://github.com/openclaw/openclaw
- Community Discord: https://discord.gg/clawd
- ClawHub: https://clawhub.ai
- Changelog/Releases: https://github.com/openclaw/openclaw/releases

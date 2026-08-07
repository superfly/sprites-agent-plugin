---
name: sprites-status
description: Check whether the Sprites Agent Plugin MCP tools are loaded and authenticated without creating resources. Use when the user asks whether Sprites is installed, connected, authorized, ready, or working, or requests a setup status check.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Check Sprites status

1. Check whether Sprites MCP tools such as `list_sprites` are available.
2. If absent, report that the plugin MCP component is not loaded. Tell the user
   to confirm the plugin is installed/enabled and reload or restart according to
   their client. Do not install a CLI or register a fallback server.
3. If tools exist, call `list_sprites`.
4. Interpret OAuth/authorization errors as authentication incomplete; ask the
   user to finish the client-provided browser OAuth flow and retry once.
5. Treat an empty list as success. Otherwise summarize count, exact names,
   status, and URLs without creating or deleting resources.

Report in this compact form:

```text
Sprites status
- MCP tools: available | missing
- Auth: OK | needs OAuth | unknown
- Sprites: N | empty | unavailable
- Next: one concrete action
```

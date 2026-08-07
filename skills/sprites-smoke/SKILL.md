---
name: sprites-smoke
description: Run an end-to-end Sprites smoke test through MCP by listing, creating, executing, and optionally destroying a temporary Sprite. Use when the user asks to verify the plugin after installation or OAuth or explicitly requests a Sprites smoke test.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Smoke-test Sprites

Use MCP only. Do not install the Sprites CLI, call the REST API, or register a
second MCP server.

1. Confirm that Sprites tools are available; otherwise report the loading issue
   and stop.
2. Call `list_sprites`. An empty result is valid.
3. Create a short-lived name such as `mcp-smoke-<shortid>` when no token prefix
   is known. If creation reports a different required prefix, retry once with
   that prefix.
4. Call `exec` with a harmless command such as `uname -a` or `echo smoke-ok`.
5. Destroy the temporary sprite only when the user already requested teardown;
   otherwise ask before cleanup because destruction is irreversible.
6. Report:

```text
Sprites smoke test
- list: OK (N sprites) | empty (OK)
- create: NAME — STATUS — URL
- exec: exit CODE — brief output
- destroy: destroyed | skipped (kept) | not requested
- prefix learned: PREFIX | full access/none | unknown
```

Do not install packages, start services, or change network policy during this
test.

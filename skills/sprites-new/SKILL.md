---
name: sprites-new
description: Create and verify a fresh Sprite for a task. Use when the user wants a new isolated environment, remote sandbox, preview environment, persistent development microVM, or a clean place to run code with Sprites.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Create a Sprite

1. Use the hosted Sprites MCP server, not the local shell, CLI, or REST API.
2. Choose a short task-scoped name. If the user supplied a name, try it exactly.
3. Call `create_sprite`.
4. If a restricted token rejects the name with a required prefix, retry once
   with that prefix only when the mapping is unambiguous. Do not assume `mcp-`.
5. Wait for usable state if needed. Run a tiny verification command only when it
   adds confidence for the requested task.
6. Report the actual sprite name, status, URL, and useful next action.

Do not destroy the sprite after creation unless the user explicitly requested a
temporary environment and cleanup.

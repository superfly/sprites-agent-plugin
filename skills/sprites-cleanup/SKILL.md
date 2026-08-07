---
name: sprites-cleanup
description: Safely inspect and clean up stale Sprites, services, and exec sessions. Use when the user asks to tidy, prune, stop, delete, destroy, remove old environments, or reduce Sprites clutter.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Clean up Sprites

1. List sprites and identify candidates using exact names. Treat prefixes and
   age only as evidence, not permission to delete.
2. Inspect relevant services, exec sessions, and checkpoints to understand what
   would be lost.
3. Present an exact cleanup plan with destructive effects.
4. Obtain confirmation before destroying sprites, stopping services, or killing
   sessions unless the user's request already names those exact actions and
   targets.
5. Execute only the approved scope and report what changed and what was kept.

Destroying a sprite irreversibly removes its filesystem, services, checkpoints,
and URL. Individual checkpoints cannot currently be deleted through MCP.

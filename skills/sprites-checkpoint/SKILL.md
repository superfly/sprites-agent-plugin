---
name: sprites-checkpoint
description: Create, list, inspect, or restore Sprite checkpoints. Use before risky remote changes or when the user asks for a snapshot, restore point, rollback, recovery, or checkpoint history.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Manage Sprite checkpoints

1. Identify the exact sprite.
2. For creation, call `checkpoint_create` with a short reason-based comment.
3. For listing or inspection, summarize IDs, comments, state, and timestamps
   when returned.
4. Before `checkpoint_restore`, explain that restoring rewinds filesystem state
   and discards later changes, then obtain clear approval for the exact target.
5. Restore only after approval and inspect filesystem or service state afterward.

Individual checkpoints cannot currently be deleted through the hosted MCP
tools. Destroying a sprite removes all its checkpoints and is irreversible.

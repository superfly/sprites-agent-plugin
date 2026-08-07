---
name: sprites-list
description: List and summarize Sprites or choose a target environment. Use when the user asks what Sprites exist, wants to find a matching or stale environment, or needs a concise inventory before remote work.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# List Sprites

1. Call the read-only `list_sprites` tool.
2. An empty list is a successful authenticated result.
3. Summarize exact name, status, URL, identifiers, labels, or age when returned
   and useful. Paginate when the user wants a complete inventory.
4. If the user needs a target, recommend the safest obvious match and quote its
   exact name. Ask only if several choices remain materially different.
5. You may identify likely stale sprites, but do not stop, kill, or destroy
   anything without separate intent or approval.

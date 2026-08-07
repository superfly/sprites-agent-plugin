---
name: sprites-run
description: Execute, test, build, inspect, install, or debug inside a Sprite. Use for one-off remote commands or isolated compute when the user names a Sprite or asks to run work in a remote sandbox.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Run work in a Sprite

1. Identify the exact target with `list_sprites` when it is ambiguous.
2. Create a checkpoint before a risky command changes valuable state.
3. Call `exec` with the executable and arguments in the form required by its
   live input schema. Use a shell explicitly only for real shell syntax.
4. Set the intended working directory and environment deliberately; never put
   secrets into reportable command text.
5. Prefer non-interactive flags. Use a service instead of a blocking exec for a
   long-running process.
6. Summarize the command's purpose, exit status, relevant output, and next step.

The host's local terminal is not the sprite runtime. Do not silently substitute
a local command when the remote tool is unavailable.

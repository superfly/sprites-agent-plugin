---
name: sprites-service
description: Manage long-running services in a Sprite. Use when the user wants to create, start, stop, restart, expose, inspect, or debug a web server, worker, database, daemon, or preview service.
license: MIT
compatibility: Requires the Sprites MCP server from this Agent Plugin.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Manage a Sprite service

1. Identify the exact sprite and call `service_list` before changing anything.
2. Use a stable role-based name such as `web`, `api`, `worker`, or `preview`.
3. Define the command, arguments, dependencies, and `http_port` intentionally
   with `service_create`.
4. Start with `service_start`. Restart by stopping and starting only the
   affected service; there is no separate restart tool.
5. Verify with `service_get` and `service_logs` before reporting success.
6. Report service name, state, port, sprite URL/access mode, and log highlights.

Confirm before creating a new public surface. Never expose secrets, environment
dumps, arbitrary files, unfiltered logs, or debug/admin endpoints.

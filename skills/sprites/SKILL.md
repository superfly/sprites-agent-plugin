---
name: sprites
description: Use this skill to create, list, inspect, operate, checkpoint, and safely clean up Sprites—isolated persistent cloud development environments. Trigger for remote sandboxes, cloud development environments, running builds or tests away from the local machine, long-running preview services, checkpoint/restore workflows, or any request that names Sprites or the Sprites MCP server.
license: MIT
compatibility: Requires an Agent Plugins client with Agent Skills, Streamable HTTP MCP, and OAuth support.
metadata:
  author: Fly.io
  version: "1.0.0"
---

# Sprites

Sprites are isolated, persistent Linux environments with their own filesystem,
URL, services, checkpoints, and outbound network policy. The host agent runs
outside the sprite. Use the hosted Sprites MCP tools as the control plane; do
not treat the host's local shell or workspace as the sprite runtime.

## Golden path

1. Use the Sprites MCP tools directly.
2. If the task needs a sprite and none is named, call `list_sprites`. Reuse an
   obvious task match; ask only if several plausible choices would materially
   change the result.
3. Use `exec` for bounded commands and services for long-running processes.
4. Inspect before mutating. Create a checkpoint before risky changes to valuable
   state.
5. Verify the result with command output, service state/logs, or checkpoint data.
6. Report the exact sprite name plus meaningful status, output, URLs, or
   checkpoint IDs.

Do not install the Sprites CLI, call the REST API, register a second MCP server,
or inspect local client configuration as part of normal plugin use. If tools or
OAuth are unavailable, follow [authentication and setup](references/authentication.md).

## Tool map

Use the smallest direct tool for the request:

- Sprite lifecycle: `list_sprites`, `create_sprite`, `destroy_sprite`.
- One-off commands: `exec`; inspect or stop sessions with `exec_list` and
  `exec_kill`.
- Services: `service_list`, `service_get`, `service_create`, `service_start`,
  `service_stop`, `service_logs`.
- Checkpoints: `checkpoint_create`, `checkpoint_list`, `checkpoint_get`,
  `checkpoint_restore`.
- Outbound network policy: `policy_network_get`, `policy_network_update`.

Most tools are sprite-scoped and require the exact `sprite` name. Use the live
tool schema for argument types. See [the tool reference](references/tools.md)
when parameter details matter.

## Common flows

### List or choose

Call `list_sprites`. Summarize names, state, and URLs or identifiers that help
the user choose. An empty list is a successful result. Never infer permission
to delete stale-looking sprites.

### Create

Choose a short task-scoped name. When the user provided a name, try it exactly.
If a restricted token rejects the name with a required prefix, retry once with
that prefix only when the mapping is unambiguous, then report the actual name.
Do not hard-code `mcp-`; it is a common default, not a guarantee.

### Run work

Use `exec` for short commands, diagnostics, tests, and builds. Supply command
and argument values in the form required by the live tool schema; do not assume
the MCP tool accepts a shell command string. Use a shell explicitly only when
the requested operation needs shell syntax. Prefer non-interactive flags.

For environment bootstrap, repositories, or file-transfer work, read
[remote compute](references/compute.md) and [files](references/files.md).

### Run a service

Inspect existing services, create or update a stable service definition, start
it, then verify with `service_get` and `service_logs`. Read
[services](references/services.md) for long-running processes and previews.

### Checkpoint and restore

Create a checkpoint with a reason-based comment before broad or risky changes.
Before restore, explain that it rewinds filesystem state and discards later
changes, then obtain clear user approval. Inspect state after restoration.

### Clean up

Stop only the services or exec sessions whose cleanup is in scope. Destroy a
sprite only on explicit delete/destroy/remove intent or after the user approves
an exact cleanup plan. Destruction removes the environment, services,
checkpoints, and URL and cannot be undone.

## Safety

Treat HTTP services as potentially internet-accessible. Never expose secrets,
environment dumps, arbitrary files, unfiltered logs, debug/admin endpoints, or
private data. Inspect network policy before changing it and confirm before
widening access. Follow [the safety reference](references/safety.md) for risky
actions.

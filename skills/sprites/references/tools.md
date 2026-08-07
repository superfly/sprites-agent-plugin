# Sprites MCP tools

The live MCP server's `tools/list` response is authoritative. This reference
summarizes the current 18-tool surface.

## Sprite management

| Tool | Access | Purpose |
| --- | --- | --- |
| `list_sprites` | read | List visible sprites; supports pagination and optional prefix filtering. |
| `create_sprite` | write | Create a sprite by name, optionally waiting for capacity. |
| `destroy_sprite` | destructive | Permanently destroy a sprite by name. |

## Commands

| Tool | Access | Purpose |
| --- | --- | --- |
| `exec` | write | Run a non-TTY command inside a sprite. |
| `exec_list` | read | List active exec sessions. |
| `exec_kill` | destructive | Signal an exec session and wait for termination. |

`exec` accepts a required repeatable `cmd` value representing the command and
arguments, plus optional path, stdin, environment, and working-directory
fields. Follow the live input schema rather than flattening arguments into one
shell string.

## Checkpoints

| Tool | Access | Purpose |
| --- | --- | --- |
| `checkpoint_create` | write | Snapshot current state, optionally with a comment. |
| `checkpoint_list` | read | List checkpoints. |
| `checkpoint_get` | read | Get one checkpoint by ID, such as `v7`. |
| `checkpoint_restore` | destructive | Restore a checkpoint and discard later filesystem state. |

Individual checkpoints cannot currently be deleted through MCP. Destroying a
sprite removes all of its checkpoints.

## Services

| Tool | Access | Purpose |
| --- | --- | --- |
| `service_list` | read | List configured services and state. |
| `service_get` | read | Get one service by name. |
| `service_create` | write | Create or replace a definition with command, args, dependencies, and optional HTTP port. |
| `service_start` | write | Start a service. |
| `service_stop` | destructive | Stop a service. |
| `service_logs` | read | Read or stream service logs. |

There is no separate restart tool: stop, then start the affected service.

## Network policy

| Tool | Access | Purpose |
| --- | --- | --- |
| `policy_network_get` | read | Read outbound DNS-based network policy. |
| `policy_network_update` | destructive | Replace outbound network policy rules. |

All sprite-scoped tools require the exact `sprite` name. Resource-specific
tools also require values such as `session_id`, `checkpoint_id`, or
`service_name`.

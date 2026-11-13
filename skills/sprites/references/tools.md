# Sprites MCP tools

The live MCP server's `tools/list` response is authoritative. This reference
summarizes the 27 Sprites tools served by the Fly MCP at `https://mcp.fly.io`
(names aligned with the [Fly MCP guide](https://mcp.fly.io/guide.md)).

Depending on the grant, the same connection may also list tools for other
Fly.io products (apps, Machines, volumes, secrets, Managed Postgres) and
account tools such as `get_fly_context`, which reports the grant's Sprites
restrictions. They are outside this reference; a listed tool is not permission
to use it.

## Reading the risk column

The `Risk` column below is editorial guidance for deciding when to confirm with
the user. It is not the server's own classification.

The server's own MCP annotations can be coarser than this column: ordinary
write operations such as `create_sprite`, `exec`, `checkpoint_create`,
`service_create`, and `service_start` may arrive annotated `destructiveHint:
true`. Do not treat that mismatch as a bug, and do not use `destructiveHint`
alone to decide whether to ask permission.

Sprite-scoped tools require the exact `sprite` name.

## Sprite management

| Tool | Risk | Purpose |
| --- | --- | --- |
| `list_sprites` | read | List visible sprites; supports pagination and optional prefix filtering. |
| `create_sprite` | write | Create a sprite by name, optionally waiting for capacity. |
| `destroy_sprite` | destructive | Permanently destroy a sprite by name. |
| `get_sprite_info` | read | Read a sprite's metadata without waking it. |
| `search_sprite_mentions` | read | Find up to 20 visible sprites by name prefix, for composer mentions. |
| `open_sprite_inspector` | read | Open the read-only Sprite Inspector in clients that support MCP Apps UI. |

- `list_sprites` — `prefix` (string, optional), `max_results` (integer,
  optional), `continuation_token` (string, optional). Pass the returned token
  back as `continuation_token` for a complete inventory.
- `create_sprite` — `name` (string, required), `wait_for_capacity` (boolean,
  optional). Set `wait_for_capacity` rather than polling or retrying in a loop.
- `destroy_sprite` — `name` (string, required).
- `get_sprite_info`, `search_sprite_mentions`, `open_sprite_inspector` — follow
  the live input schema. Reading metadata does not wake a sprite; reading
  runtime state, services, logs, or files may.

## Commands

| Tool | Risk | Purpose |
| --- | --- | --- |
| `exec` | write | Run a non-TTY command inside a sprite. |
| `exec_list` | read | List active exec sessions. |
| `exec_kill` | destructive | Signal an exec session and wait for termination. |

- `exec` — `cmd` (string, required, repeatable for the executable and each
  argument), `path` (string, optional), `stdin` (boolean, optional), `env`
  (string, optional, repeatable, each entry formatted `KEY=VALUE`), `dir`
  (string, optional).
- `exec_kill` — `session_id` (string, required), `signal` (string, optional,
  default `SIGTERM`), `timeout` (string, optional, default `10s`).

Follow the live input schema rather than flattening arguments into one shell
string.

## Files

| Tool | Risk | Purpose |
| --- | --- | --- |
| `file_read` | read | Read a file's contents. Returns an embedded text or binary resource. |
| `file_list` | read | List the entries of a directory. |
| `file_write` | write | Write contents to a file. |
| `file_copy` | write | Copy a file or directory. |
| `file_rename` | write | Rename or move a file or directory. |
| `file_delete` | destructive | Delete a file or directory. |

Paths resolve against `workingDir`, and access is confined to the sprite's
root. Prefer these tools over shell quoting tricks; fall back to `exec` only
when no file tool fits. Confirm path and scope before `file_delete`; inspect
destinations before `file_rename` / `file_copy` overwrites.

## Checkpoints

| Tool | Risk | Purpose |
| --- | --- | --- |
| `checkpoint_create` | write | Snapshot current state, optionally with a comment. |
| `checkpoint_list` | read | List checkpoints. |
| `checkpoint_get` | read | Get one checkpoint by ID, such as `v7`. |
| `checkpoint_restore` | destructive | Restore a checkpoint and discard later filesystem state. |

- `checkpoint_create` — `comment` (string, optional).
- `checkpoint_get` — `checkpoint_id` (string, required, such as `v7`).
- `checkpoint_restore` — `checkpoint_id` (string, required).

Individual checkpoints cannot currently be deleted through MCP. Destroying a
sprite removes all of its checkpoints.

## Services

| Tool | Risk | Purpose |
| --- | --- | --- |
| `service_list` | read | List configured services and state. |
| `service_get` | read | Get one service by name. |
| `service_create` | write | Create or replace a definition with command, args, dependencies, and optional HTTP port. |
| `service_start` | write | Start a service. |
| `service_stop` | destructive | Stop a service. |
| `service_logs` | read | Read or stream service logs. |

- `service_create` — `service_name` (string, required), `cmd` (string,
  required, the executable only), `args` (array, optional), `needs` (array,
  optional dependency service names), `http_port` (integer, optional),
  `duration` (string, optional). Unlike `exec`, `cmd` here is a single string
  and arguments belong in `args`.
- `service_get` — `service_name` (string, required).
- `service_start` / `service_stop` — `service_name` (string, required), plus an
  optional `duration`/`timeout` (string).
- `service_logs` — `service_name` (string, required), `lines` (integer,
  optional), `duration` (string, optional).

There is no separate restart tool: stop, then start the affected service.

## Network policy

| Tool | Risk | Purpose |
| --- | --- | --- |
| `policy_network_get` | read | Read outbound DNS-based network policy. |
| `policy_network_update` | destructive | Replace outbound network policy rules. |

- `policy_network_update` — `rules` (array, required; each rule has `domain`,
  `action`, and an optional `include`).

`policy_network_update` replaces the entire rule set rather than merging into
it. Read the current policy with `policy_network_get` first and send the
complete intended set, or unrelated rules are silently dropped.

Resource-specific tools require values such as `session_id`, `checkpoint_id`,
or `service_name` in addition to `sprite`.

# Sprites safety

## Require explicit intent or confirmation

- Destroying a sprite.
- Restoring a checkpoint.
- Killing sessions or stopping services not clearly owned by the current task.
- Changing outbound network policy in either direction.
- Exposing a new public HTTP surface.
- Broad destructive filesystem commands inside a sprite.

Resolve exact resource names and inspect current state before these operations.

## Network policy replaces, it does not merge

`policy_network_update` overwrites the entire rule set. A change intended to
narrow or add a single domain will silently drop every rule you did not send.
Always read the current policy with `policy_network_get`, build the complete
intended set from it, and confirm that full set with the user before writing.

## Create a checkpoint first

Checkpoint valuable state before package upgrades, migrations, bulk rewrites or
deletes, service-definition changes, network-policy changes, and untrusted or
agent-generated experiments. Use a reason-based comment such as
`before-node-upgrade` or `before-db-migration`.

## Secrets and public surfaces

- Prefer scoped connectors or runtime environment variables over persistent
  credentials in files.
- Never place tokens in command output, logs, repositories, or served content.
- Never add env-dump, arbitrary file-browser, debug, or unfiltered log
  endpoints.
- Assume a service URL may become public; authenticate and minimize exposure.

## Recovery

Before restore, explain that it rewinds filesystem state and discards changes
made after the checkpoint. List newer checkpoints or relevant files when the
user may need them. Verify filesystem and service state after restoration.

Sprite destruction is irreversible and removes the environment, services,
checkpoints, and URL. State the exact target and impact before calling it.

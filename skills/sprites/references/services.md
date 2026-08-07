# Sprites services

Use services for web servers, workers, daemons, databases, and any process that
must survive the initiating MCP call.

## Workflow

1. Call `service_list` before adding a definition.
2. Choose a stable role-based name such as `web`, `api`, `worker`, or `preview`.
3. Call `service_create` with an intentional command, argument list,
   dependencies, and `http_port` when applicable.
4. Call `service_start`.
5. Verify with `service_get` and `service_logs`.
6. Report the exact service name, state, port, sprite URL, expected access mode,
   and useful log summary.

There is no separate restart tool. Restart by stopping and starting only the
affected service. Read logs before changing code or definitions.

## Exposure

Treat any sprite URL as potentially internet-accessible. Confirm before making
a new public surface or broadening access. Never serve environment variables,
credentials, arbitrary files, unfiltered logs, debug/admin interfaces, or user
data. Stop temporary services when cleanup is in scope.

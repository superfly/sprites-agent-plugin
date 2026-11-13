# Authentication and setup

The plugin connects only to the hosted Fly MCP, a Streamable HTTP MCP endpoint
registered under the server name `sprites`:

```text
https://mcp.fly.io
```

The Fly MCP serves the Sprites tools and, depending on the grant, tools for
other Fly.io products. Use only the Sprites tools for Sprites workflows.

The installing client owns OAuth discovery, browser interaction, credential
storage, and refresh. The package contains no API token and Agent Plugins v1 has
no portable OAuth configuration fields.

## Diagnose by layer

### MCP tools are missing

The plugin or its MCP component is not loaded in the current session.

1. Confirm the plugin is installed and enabled using the client's plugin UI or
   documented command.
2. Reload plugins, start a new agent session, or restart the client as its
   documentation requires.
3. Confirm that the client supports the `streamable-http` Agent Plugins MCP
   transport.
4. Report the missing component and stop the Sprites workflow.

Do not install the Sprites CLI, use `mcp-remote`, call the REST API, or register
a second copy of the server to hide a plugin-loading problem.

### Tools exist but calls require authorization

1. Complete the browser OAuth flow presented by the client; sign-in goes
   through Fly.io.
2. Choose the intended Fly.io organization and grant the Sprites permissions.
3. Review the grant's restrictions, such as the name prefix and Sprite limit.
4. Retry the original MCP call once.

A user who previously authorized the previous `https://sprites.dev/mcp` endpoint
must authorize again: the two endpoints hold separate OAuth grants.

Do not ask the user to paste an API token into chat or a shell and do not start
an independent CLI login.

### Calls are authenticated but restricted

The grant may restrict sprite names by prefix, cap sprite creation, require a
label, or expire.

- When `get_fly_context` is available, call it to read the Sprites restrictions
  (`name_prefix`, `max_sprites_total`). Otherwise read the required prefix from
  the API error. Do not assume it is `mcp-`.
- If a user-requested bare name can be mapped unambiguously, retry once as
  `<required-prefix><requested-name>` and report the actual name.
- Do not loop on a creation cap or policy denial.
- Explain that removing a required prefix generally means authorizing broader
  access, potentially all sprites in the organization.

### Expected sprite is absent

Confirm the selected OAuth organization and that Sprites access was granted at
consent. Restricted grants can hide sprites outside their allowed prefix or
label. Use names returned by `list_sprites` and
never guess.

### Empty list

An empty `list_sprites` response proves that the MCP connection and
authentication succeeded; it is not an error.

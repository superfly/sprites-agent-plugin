# Sprites Agent Plugin

The official portable Agent Plugin for [Sprites](https://sprites.dev): isolated,
persistent cloud development environments that agents can create, operate,
checkpoint, and clean up.

The package targets [Agent Plugins v1.0.0](https://agent-plugins.org/specification).
It connects compatible clients to the hosted Sprites MCP server and bundles
Agent Skills for common workflows. There is no local server process to install.

## What it provides

- A Streamable HTTP MCP connection to `https://sprites.dev/mcp`.
- OAuth handled by the installing client.
- Skills for day-to-day Sprites work, focused create/run/service/checkpoint/list/
  cleanup workflows, setup diagnostics, and an end-to-end smoke test.
- Safety guidance for destructive operations, public services, secrets, and
  outbound network policy.

The MCP server currently exposes 18 tools for sprite management, command
execution, checkpoints, services, and network policy. Its live `tools/list`
response is authoritative.

## Install

Install this repository or directory with a client that supports the Agent
Plugins v1 format. The client discovers `plugin.json`, the immediate children of
`skills/`, and `mcp.json` at fixed locations.

On first MCP use, complete the browser OAuth flow and select the intended Fly.io
organization. Restricted connector tokens may enforce a sprite-name prefix,
creation cap, label, or expiry.

Agent Plugins standardizes the package contents, not marketplace distribution,
installation UI, or permissions. Follow the installing client's documentation
for its current local, Git, workspace, or marketplace install flow.

## Current client compatibility

The Agent Plugins project currently lists VS Code, Cursor, GitHub Copilot,
ChatGPT and Codex, and Kiro as compatible clients. This package is designed to
replace the reusable skills-and-MCP core of the existing Codex and Cursor
packages; marketplace publication remains a separate client-owned step.

Google's August 2026 announcement says Agents CLI and Data Agent Kit currently
support the format and that support is expected in more Google products. It
mentions Antigravity as an agent that can consume Agents CLI's skills, but does
not identify Antigravity itself as a conforming Agent Plugins client. Keep the
existing Antigravity package for its hooks, rules, and native installation until
that support is documented and tested. Grok is likewise not on the current
compatible-client list.

## Example prompts

- "List my sprites and recommend the best one for this task."
- "Create an isolated sprite for this repository and run its tests."
- "Checkpoint my `mcp-api-debug` sprite, then upgrade its dependencies."
- "Start the web app as a service and inspect its logs."
- "Check whether the Sprites plugin is authenticated."
- "Run an end-to-end Sprites smoke test and clean up afterward."

## Package layout

```text
.
├── plugin.json
├── mcp.json
├── skills/
│   ├── sprites/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── sprites-new/
│   ├── sprites-run/
│   ├── sprites-service/
│   ├── sprites-checkpoint/
│   ├── sprites-list/
│   ├── sprites-cleanup/
│   ├── sprites-status/
│   └── sprites-smoke/
├── assets/
├── scripts/
└── tests/
```

Portable Agent Plugins v1 has no commands, hooks, rules, or arbitrary manifest
fields. The focused skills preserve the intent of command-like workflows from
older client-specific packages without adding non-standard package structure.

## Authentication and attribution

Agent Plugins v1 deliberately leaves OAuth discovery, user interaction, and
credential storage to the client. The Sprites server supports the OAuth flow
expected by modern MCP clients; no token is stored in this repository.

The package does not send `Fly-Client-Agent` attribution headers. A single
portable package cannot truthfully hard-code one host-agent identity, and v1
does not define header interpolation from client identity. Clients may add their
own truthful attribution outside the portable configuration.

## Development

Run the dependency-free validation suite:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

The tests validate the closed v1 manifests, fixed component locations, skill
frontmatter, local links, text hygiene, HTTPS transport, and package-boundary
rules. They do not make network calls.

## Source material

This package consolidates the reusable behavior from the existing Sprites
plugins for Codex, Cursor, Antigravity, and Grok. The MCP tool model is checked
against the Sprites platform source and the public
[Sprites MCP server reference](https://github.com/superfly/sprites-mcp).
See [migration coverage](docs/migration-coverage.md) for the artifact-by-artifact
mapping and the client-specific behavior that Agent Plugins v1 cannot carry.

- [Agent Plugins specification](https://agent-plugins.org/specification)
- [Agent Skills specification](https://agentskills.io/specification)
- [Sprites API](https://sprites.dev/api)
- [Sprites remote MCP documentation](https://docs.sprites.dev/integrations/remote-mcp/)

## License

[MIT](LICENSE) © 2026 Fly.io

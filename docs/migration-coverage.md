# Migration coverage

This package is an additive portable replacement candidate. It does not modify
or remove the existing client-specific repositories.

## Artifact mapping

| Existing artifact | Portable destination | Coverage |
| --- | --- | --- |
| Codex and Cursor root workflow skill | `skills/sprites/` | Consolidated and expanded with progressive references. |
| Codex `.mcp.json`, Cursor `mcp.json`, Grok MCP configs, Antigravity `mcp_config.json` | Root `mcp.json` | Converted to Agent Plugins v1 `streamable-http`. |
| Antigravity `/sprites:list` command and skill | `skills/sprites-list/` | Workflow preserved as an invokable/discoverable skill. |
| Antigravity `/sprites:new` command and skill | `skills/sprites-new/` | Workflow preserved as an invokable/discoverable skill. |
| Antigravity `/sprites:run` command and skill | `skills/sprites-run/` | Workflow preserved as an invokable/discoverable skill. |
| Antigravity `/sprites:service` command and skill | `skills/sprites-service/` | Workflow preserved as an invokable/discoverable skill. |
| Antigravity `/sprites:checkpoint` command and skill | `skills/sprites-checkpoint/` | Workflow preserved as an invokable/discoverable skill. |
| Antigravity `/sprites:cleanup` command and skill | `skills/sprites-cleanup/` | Workflow preserved as an invokable/discoverable skill. |
| Grok `sprites-status` skill | `skills/sprites-status/` | Generalized to client-neutral setup and OAuth diagnostics. |
| Grok `sprites-smoke` skill | `skills/sprites-smoke/` | Preserved with safe optional teardown. |
| Grok auth, compute, file, service, safety, and smoke references | `skills/sprites/references/` | Consolidated, corrected against the current MCP surface, and made client-neutral. |
| Logos and MIT license | `assets/` and `LICENSE` | Preserved. |

## Intentionally not portable in v1

| Artifact | Reason |
| --- | --- |
| Codex, Cursor, and Grok marketplace catalogs and rich UI metadata | Distribution and install UI are outside Agent Plugins v1. |
| Client-specific manifests | Root `plugin.json` is the only portable manifest. |
| Antigravity hooks and hook script | Hooks are not a v1 portable component and no documented client extension namespace is available here. Safety behavior is retained as model guidance, not mechanical enforcement. |
| Antigravity rules file | Rules are not a v1 portable component; relevant behavior is included in the core skill. |
| Antigravity command TOML | Commands are not a v1 portable component; focused skills preserve their workflows. |
| Client-specific request-attribution headers | A portable package cannot truthfully hard-code a single host identity. |
| Client-specific MCP timeout fields | The closed portable MCP schema does not define a timeout field. |

## Compatibility implications

The portable package can replace the skills-and-MCP core for conforming clients.
It cannot claim feature parity with enforced Antigravity pre-tool hooks or any
marketplace presentation until those behaviors are represented by documented
client extensions or retained compatibility packages.

As of August 2026, the Agent Plugins compatible-client list includes Cursor and
ChatGPT/Codex but not Antigravity or Grok. Google's launch announcement says its
current format integrations are Agents CLI and Data Agent Kit; Antigravity is
named as an agent that can consume Agents CLI skills, not as a native plugin
client. Treat Antigravity replacement as unverified until its loader explicitly
documents the v1 root manifest and MCP configuration.

Before deleting a legacy repository, test installation, OAuth, skill discovery,
all 18 live tools, and destructive-action behavior in each target client.

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
EXPECTED_SKILLS = {
    "sprites",
    "sprites-checkpoint",
    "sprites-cleanup",
    "sprites-list",
    "sprites-new",
    "sprites-run",
    "sprites-service",
    "sprites-smoke",
    "sprites-status",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class AgentPluginRepositoryTests(unittest.TestCase):
    def test_offline_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_repository.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_manifest_targets_agent_plugins_v1(self) -> None:
        manifest = load_json(ROOT / "plugin.json")
        self.assertEqual(manifest["$schema"], PLUGIN_SCHEMA)
        self.assertEqual(manifest["name"], "sprites")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(manifest["license"], "MIT")

    def test_mcp_uses_portable_streamable_http(self) -> None:
        config = load_json(ROOT / "mcp.json")
        self.assertEqual(config["$schema"], MCP_SCHEMA)
        self.assertEqual(set(config), {"$schema", "mcpServers"})
        server = config["mcpServers"]["sprites"]
        self.assertEqual(server["type"], "streamable-http")
        parsed = urlsplit(server["url"])
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "sprites.dev")
        self.assertEqual(parsed.path, "/mcp")

    def test_portable_config_does_not_misattribute_the_client(self) -> None:
        server = load_json(ROOT / "mcp.json")["mcpServers"]["sprites"]
        self.assertNotIn("headers", server)

    def test_expected_skills_are_immediate_children(self) -> None:
        actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_skill_names_match_directories(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^name: ([a-z0-9-]+)$", text, flags=re.MULTILINE)
            self.assertIsNotNone(match, path)
            self.assertEqual(match.group(1), path.parent.name)

    def test_no_legacy_client_manifest_is_required(self) -> None:
        self.assertFalse((ROOT / ".codex-plugin").exists())
        self.assertFalse((ROOT / ".cursor-plugin").exists())
        self.assertFalse((ROOT / ".grok-plugin").exists())
        self.assertFalse((ROOT / "mcp_config.json").exists())
        self.assertFalse((ROOT / "hooks.json").exists())


if __name__ == "__main__":
    unittest.main()

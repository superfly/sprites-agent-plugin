#!/usr/bin/env python3
"""Offline structural checks for the Sprites Agent Plugin."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
SKIPPED_DIRECTORIES = {".git", "__pycache__", ".pytest_cache", ".ruff_cache"}
TEXT_SUFFIXES = {".json", ".md", ".py", ".svg", ".yaml", ".yml"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
SKILL_NAME = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains a duplicate key."""


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate key {key!r}")
        result[key] = value
    return result


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (OSError, json.JSONDecodeError, DuplicateKeyError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        return None


def repository_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not SKIPPED_DIRECTORIES.intersection(path.relative_to(ROOT).parts)
    )


def validate_text(path: Path, errors: list[str]) -> str | None:
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "LICENSE":
        return None
    relative = path.relative_to(ROOT)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{relative}: not valid UTF-8 ({exc})")
        return None
    if text and not text.endswith("\n"):
        errors.append(f"{relative}: missing final newline")
    for number, line in enumerate(text.splitlines(), start=1):
        if line != line.rstrip():
            errors.append(f"{relative}:{number}: trailing whitespace")
    return text


def validate_manifest(errors: list[str]) -> None:
    path = ROOT / "plugin.json"
    if not path.is_file():
        errors.append("plugin.json: required manifest is missing")
        return
    data = load_json(path, errors)
    if not isinstance(data, dict):
        errors.append("plugin.json: manifest must be an object")
        return
    unknown = sorted(set(data) - PLUGIN_FIELDS)
    if unknown:
        errors.append(f"plugin.json: unknown top-level fields {unknown}")
    if data.get("$schema") != PLUGIN_SCHEMA:
        errors.append("plugin.json: wrong Agent Plugins schema")
    name = data.get("name")
    if not isinstance(name, str) or not PLUGIN_NAME.fullmatch(name):
        errors.append("plugin.json: invalid plugin name")
    for field in ("version", "description", "homepage", "repository", "license"):
        if field in data and not isinstance(data[field], str):
            errors.append(f"plugin.json: {field} must be a string")
    author = data.get("author")
    if author is not None:
        if not isinstance(author, dict) or set(author) - {"name", "email", "url"}:
            errors.append("plugin.json: invalid author object")
        elif not all(isinstance(value, str) for value in author.values()):
            errors.append("plugin.json: author values must be strings")
    keywords = data.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list)
        or not all(isinstance(value, str) for value in keywords)
    ):
        errors.append("plugin.json: keywords must be an array of strings")
    extensions = data.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict)
        or not all(isinstance(value, dict) for value in extensions.values())
    ):
        errors.append("plugin.json: extensions must map namespaces to objects")


def validate_remote_url(value: Any, context: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{context}: url must be a string")
        return
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname:
        errors.append(f"{context}: non-loopback remote URL must use HTTPS")
    if parsed.username or parsed.password or parsed.fragment:
        errors.append(f"{context}: URL cannot contain userinfo or a fragment")


def validate_mcp(errors: list[str]) -> None:
    path = ROOT / "mcp.json"
    if not path.is_file():
        return
    data = load_json(path, errors)
    if not isinstance(data, dict):
        errors.append("mcp.json: configuration must be an object")
        return
    if set(data) != {"$schema", "mcpServers"}:
        errors.append("mcp.json: top-level fields must be $schema and mcpServers")
    if data.get("$schema") != MCP_SCHEMA:
        errors.append("mcp.json: wrong or mismatched Agent Plugins schema")
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        errors.append("mcp.json: mcpServers must be an object")
        return
    for name, server in servers.items():
        context = f"mcp.json: server {name!r}"
        if not isinstance(server, dict):
            errors.append(f"{context} must be an object")
            continue
        transport = server.get("type")
        if transport == "stdio":
            allowed = {"type", "command", "args", "env", "cwd"}
            command = server.get("command")
            if not isinstance(command, str) or not command:
                errors.append(f"{context}: stdio command must be a string")
            elif "/" in command and not command.startswith("./"):
                errors.append(f"{context}: packaged command must begin with ./")
        elif transport in {"streamable-http", "sse"}:
            allowed = {"type", "url", "headers"}
            validate_remote_url(server.get("url"), context, errors)
            headers = server.get("headers")
            if headers is not None and (
                not isinstance(headers, dict)
                or not all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in headers.items()
                )
            ):
                errors.append(f"{context}: headers must map strings to strings")
        else:
            errors.append(f"{context}: unsupported transport {transport!r}")
            continue
        unknown = sorted(set(server) - allowed)
        if unknown:
            errors.append(f"{context}: unknown fields {unknown}")


def parse_frontmatter(path: Path, text: str, errors: list[str]) -> dict[str, str] | None:
    relative = path.relative_to(ROOT)
    if not text.startswith("---\n"):
        errors.append(f"{relative}: missing YAML frontmatter")
        return None
    try:
        frontmatter, body = text[4:].split("\n---\n", maxsplit=1)
    except ValueError:
        errors.append(f"{relative}: unclosed YAML frontmatter")
        return None
    if not body.strip():
        errors.append(f"{relative}: skill instructions are empty")
    fields: dict[str, str] = {}
    for number, line in enumerate(frontmatter.splitlines(), start=2):
        if not line or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            errors.append(f"{relative}:{number}: malformed frontmatter field")
            continue
        key, value = line.split(":", maxsplit=1)
        key = key.strip()
        if key not in SKILL_FIELDS:
            errors.append(f"{relative}:{number}: unknown skill field {key!r}")
        fields[key] = value.strip().strip("\"'")
    return fields


def validate_skills(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    if not skills_root.is_dir():
        return
    for directory in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_path = directory / "SKILL.md"
        if not skill_path.is_file():
            continue
        text = skill_path.read_text(encoding="utf-8")
        fields = parse_frontmatter(skill_path, text, errors)
        if fields is None:
            continue
        name = fields.get("name")
        if name != directory.name:
            errors.append(f"{skill_path.relative_to(ROOT)}: name must match directory")
        if not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
            errors.append(f"{skill_path.relative_to(ROOT)}: invalid skill name")
        description = fields.get("description", "")
        if not description or len(description) > 1024:
            errors.append(
                f"{skill_path.relative_to(ROOT)}: description must be 1-1024 characters"
            )
        compatibility = fields.get("compatibility")
        if compatibility is not None and not 1 <= len(compatibility) <= 500:
            errors.append(
                f"{skill_path.relative_to(ROOT)}: compatibility must be 1-500 characters"
            )


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    elif " " in target:
        target = target.split(" ", maxsplit=1)[0]
    return urllib.parse.unquote(target.split("#", maxsplit=1)[0])


def validate_markdown_links(path: Path, text: str, errors: list[str]) -> None:
    for match in MARKDOWN_LINK.finditer(text):
        target = markdown_target(match.group(1))
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: local link escapes plugin root")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link {target!r}")


def validate_package_paths(errors: list[str]) -> None:
    root = ROOT.resolve()
    for path in ROOT.rglob("*"):
        if SKIPPED_DIRECTORIES.intersection(path.relative_to(ROOT).parts):
            continue
        if path.is_symlink():
            try:
                path.resolve().relative_to(root)
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: symlink escapes plugin root")


def main() -> int:
    errors: list[str] = []
    files = repository_files()
    for path in files:
        text = validate_text(path, errors)
        if path.suffix.lower() == ".json":
            load_json(path, errors)
        elif path.suffix.lower() == ".svg":
            try:
                ET.parse(path)
            except ET.ParseError as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid SVG ({exc})")
        if text is not None and path.suffix.lower() == ".md":
            validate_markdown_links(path, text, errors)
    validate_manifest(errors)
    validate_mcp(errors)
    validate_skills(errors)
    validate_package_paths(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(files)} repository files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

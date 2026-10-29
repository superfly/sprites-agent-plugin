# Files on a sprite

Use `file_list` / `file_read` / `file_write` / `file_copy` / `file_rename` /
`file_delete` for filesystem work (`workingDir` + path flags per live schema).
Prefer `git clone` for repos; use `file_write` (utf8/base64) for small
generated files; fall back to `exec` only when no file tool fits.

## Preferred transfer methods

1. `git clone` or fetch for real repositories and multi-file projects.
2. `file_write` with `encoding: "utf8"` for literal text or `"base64"` for
   encoded bytes (no data URL prefix); create parents when the schema allows.
3. `file_list` / `file_read` for directory and content inspection. Limit large
   reads before dumping files into model context.
4. Ask the user for an authorized transfer path for private code or secrets.

## When to use `exec` instead

Fall back to `exec` only when no file tool fits (for example unpacking an
archive after a `file_write`, or non-CRUD commands). Follow the live `exec`
input schema: keep the executable and arguments as separate repeated `cmd`
values. When shell syntax is necessary, invoke a shell explicitly and pass its
program as one argument rather than assuming MCP will parse redirection,
quotes, substitutions, or heredocs.

## Reliable write and verify

Use `file_write` with `sprite`, `path`, `workingDir`, and `content`. Verify with
`file_read`, `file_list`, or a short `exec` (`wc -c`, checksum). Do not put
secrets in command arguments, logs, repository files, or HTTP-served
directories.

For a multi-file archive, write the encoded archive with `file_write`, verify
it, then unpack with a simple `tar` or `unzip` via `exec`. Avoid dozens of
fragile generated shell writes when a repository or archive is available.

`file_delete` takes explicit `recursive` / `asRoot` flags — confirm path and
scope before deletion. `file_rename` and `file_copy` take `source` and `dest`;
inspect the destination before overwriting.

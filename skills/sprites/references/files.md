# Files on a sprite

The current hosted Sprites MCP tool set has no direct file read/write tool.
Operate on the remote filesystem with `exec`.

## Preferred transfer methods

1. `git clone` or fetch for real repositories and multi-file projects.
2. A base64 payload decoded inside the sprite for small generated files.
3. A short, simple command for tiny content without shell-sensitive data.
4. Ask the user for an authorized transfer path for private code or secrets.

Follow the live `exec` input schema: keep the executable and arguments as
separate repeated `cmd` values. When shell syntax is necessary, invoke a shell
explicitly and pass its program as one argument rather than assuming MCP will
parse redirection, quotes, substitutions, or heredocs.

## Reliable base64 pattern

Encode content on the host, then run Python inside the sprite with separate
arguments equivalent to:

```text
python3
-c
import base64,pathlib;pathlib.Path('/home/sprite/app/file').write_bytes(base64.b64decode('BASE64'))
```

Create the parent directory first. Verify with `wc -c`, a checksum, or a small
targeted read. Do not put secrets in command arguments, logs, repository files,
or HTTP-served directories.

For a multi-file archive, write the encoded archive, verify it, then unpack it
with a simple `tar` or `unzip` command. Avoid dozens of fragile generated shell
writes when a repository or archive is available.

Limit reads with `head`, `tail`, or `wc` before dumping large files into model
context.

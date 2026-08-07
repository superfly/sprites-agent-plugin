# Deploying and syncing into a sprite

Use this reference when copying local project state into a sprite, building
inside one, or running a preview service from synced code.

## Recommended flow

1. Confirm the target sprite and the remote working directory.
2. Create or verify a checkpoint before overwriting remote files.
3. Sync selected paths, not the whole workspace by default.
4. Install dependencies or build inside the sprite only when the task needs it.
5. Run tests or a smoke check inside the sprite.
6. Start or update a service for a long-running preview.
7. Report the sprite URL, expected access mode, log highlights, and any manual
   step left for the user.

Prefer `git clone` inside the sprite over copying a working tree. It is faster,
avoids most of the boundaries below, and gives the sprite a real repository.
See [files](files.md) for transfer patterns when no repository is available.

## Do not sync

- `.git/`. Clone or fetch inside the sprite instead of copying history.
- Dependency and build caches such as `node_modules/`, `_build/`, `deps/`,
  `.venv/`, `target/`, `dist/`, and `.next/`. Reinstall inside the sprite; host
  artifacts are frequently built for a different platform.
- Local secrets: `.env` and its variants, key files, certificates, token
  caches, cloud credential stores, and shell history.
- Large generated artifacts, media, datasets, and databases unless they are the
  intended payload and the user asked for them.
- Editor, OS, and agent state such as `.DS_Store`, `.idea/`, and local client
  configuration directories.

When a sync would pull in a secret, stop and ask how the sprite should obtain
it. Provide credentials as service or exec environment values at run time
rather than writing them into the remote filesystem.

## After syncing

Verify what actually landed with a file count, `du`, or a checksum before
building. Report the paths you synced and the paths you deliberately skipped so
the user can correct the boundary.

# Remote compute with Sprites

Use a sprite when the user wants isolated or persistent remote Linux compute,
untrusted/generated code execution, heavyweight dependency installation,
integration tests, a long-running preview, or checkpoint/restore semantics.
Use the host workspace for ordinary local edits unless the user wants the work
performed remotely.

## Bootstrap a task environment

1. List sprites and reuse an obvious task match, or create a task-scoped sprite.
2. Probe only the runtimes and package managers relevant to the job.
3. Create a clean baseline checkpoint before large installs or risky work.
4. Bring code in:
   - Prefer `git clone` for a repository the user identified and that the sprite
     can access.
   - For small generated files, use the reliable patterns in
     [files.md](files.md).
   - When copying local project state, follow the sync boundaries in
     [deployment.md](deployment.md).
   - Ask how private code should be transferred when no authorized path exists;
     never invent credentials.
5. Run bounded work with `exec`; use services for processes that must persist.
6. Verify with tests, health checks, service state, or logs.
7. Report sprite name, significant commands, exit status, URLs, and checkpoint
   IDs.

Prefer non-interactive command flags. If a job will outlive an MCP call, model
it as a service or a restartable unit rather than leaving a blocking exec.

## Isolation and recovery

- Use separate sprites for experiments that need strong isolation.
- Reuse a sprite when the user expects environment state to persist.
- Checkpoint before speculative branches of work.
- Restore only after explaining that later filesystem changes will be lost and
  receiving approval.

Leaving an idle sprite is acceptable unless the user asked for cleanup.

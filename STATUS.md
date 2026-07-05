# STATUS

> Updated: 2026-07-05
> Current task: SignalForge Checkpoint v0.1 alpha is published.
> Next step: Add repository topics and plan the first adapter implementation.

## Current State

SignalForge Checkpoint is a lightweight file protocol for keeping long-running AI agents aligned with project state and operating rules.

## Core Files

| File | Purpose | Status |
|---|---|---|
| `AGENTS.md` | Agent operating rules | Draft |
| `STATUS.md` | Current worksite state | Draft |
| `LOG.md` | Append-only work history | Draft |
| `.signalforge.toml` | Optional adapter config | Draft |
| `templates/` | Copyable starter templates | Draft |

## Decisions

- Keep the public MVP small: `AGENTS.md`, `STATUS.md`, `LOG.md`.
- Keep `.signalforge.toml` optional.
- Treat Codex + relay as the first adapter, not the whole project.
- Include protocol compliance as part of anti-drift, not as a separate project.
- Use MIT License for the first public release.
- Use repository name `signalforge-checkpoint`.

## Open Questions

- Decide whether the first release should include a working relay wrapper or only protocol templates.

# STATUS

> Updated: 2026-07-05
> Current task: v0.2.0 checkpoint scripts are ready to publish.
> Next step: Commit, push, and create the v0.2.0 release.

## Current State

fight-on-memory is a lightweight file protocol for keeping long-running AI agents aligned with project state and operating rules.

## Core Files

| File | Purpose | Status |
|---|---|---|
| `AGENTS.md` | Agent operating rules | Draft |
| `STATUS.md` | Current worksite state | Draft |
| `LOG.md` | Append-only work history | Draft |
| `.fightonmemory.toml` | Optional adapter config | Draft |
| `templates/` | Copyable starter templates | Draft |
| `scripts/` | Optional CLI helpers | Ready for v0.2.0 |

## Decisions

- Keep the public MVP small: `AGENTS.md`, `STATUS.md`, `LOG.md`.
- Keep `.fightonmemory.toml` optional.
- Treat Codex + relay as the first adapter, not the whole project.
- Include protocol compliance as part of anti-drift, not as a separate project.
- Use MIT License for the first public release.
- Use repository name `fight-on-memory`.
- Ship v0.1 as protocol, templates, and docs before adding a working adapter.
- Add minimal scripts before building a relay wrapper.

## Open Questions

- After v0.2.0, should the next milestone be a relay wrapper, packaging, or more examples?

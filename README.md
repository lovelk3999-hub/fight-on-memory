# fight-on-memory

Three files to keep long-running AI agents from drifting.

fight-on-memory is a lightweight file protocol for keeping AI coding agents aligned with project state and operating rules during long-running work.

It helps agents recover from context compaction, session breaks, model switching, and protocol drift without introducing a memory database.

## Quick Start

Copy these three files into your project:

```text
AGENTS.md
STATUS.md
LOG.md
```

Then tell your agent:

```text
Read AGENTS.md and STATUS.md before continuing.
After each meaningful step, update STATUS.md and append LOG.md.
```

That is the simple mode.

## Why

Long-running AI agents drift.

They may forget:

- where the work stopped
- which decision was already made
- which local skill or workflow should be used
- whether a PreFlight, setup, validation, or checkpoint step is required

fight-on-memory keeps the active worksite in files, so agents can re-anchor from the project instead of relying on chat memory.

## Core Files

```text
AGENTS.md
STATUS.md
LOG.md
```

| File | Purpose |
|---|---|
| `AGENTS.md` | Operating rules for AI agents |
| `STATUS.md` | Current task, next step, blockers, and recent decisions |
| `LOG.md` | Append-only history for recovery and audit |

## Optional Adapter Config

```text
.fightonmemory.toml
```

This file is optional. It is for scripts, relay wrappers, editor adapters, or automation layers. Agents do not need to read it directly.

## Simple Mode

Use only the three core files.

```text
project/
  AGENTS.md
  STATUS.md
  LOG.md
```

Agent workflow:

1. Read `AGENTS.md`.
2. Read `STATUS.md`.
3. Do the next task.
4. Update `STATUS.md`.
5. Append `LOG.md`.

## Scripts

The scripts are optional. They make the file protocol easier to use from a terminal.

Initialize a project:

```bash
python scripts/init_checkpoint.py /path/to/project --with-config
```

Append a checkpoint:

```bash
python scripts/checkpoint.py /path/to/project \
  --change "Finished the parser fix" \
  --result "Done" \
  --notes "Tests pass" \
  --current-task "Parser fix is complete" \
  --next-step "Review the diff"
```

Generate a resume prompt:

```bash
python scripts/resume_summary.py /path/to/project --output RESUME.md
```

## Adapter Mode

Use the optional config when an integration can inject or validate project anchors.

```text
project/
  AGENTS.md
  STATUS.md
  LOG.md
  .fightonmemory.toml
```

Example adapter behavior:

1. Read `.fightonmemory.toml`.
2. Inject `AGENTS.md` and `STATUS.md` before each model request.
3. Do not inject `LOG.md` by default.
4. Stop if `STATUS.md` is stale or unclear.

## What It Solves

- Context compaction recovery
- Session resume
- Model handoff
- Task drift
- Skill and tool protocol drift
- PreFlight / validation step drift

## What It Looks Like

Minimal `STATUS.md`:

```markdown
# STATUS

> Updated: 2026-07-05
> Current task: Implement the next parser fix.
> Next step: Run the parser test and inspect the failing case.

## Current State

We are fixing CSV import edge cases.

## Blockers

- None.

## Recent Decisions

- Keep the parser dependency-free for now.
```

Minimal `LOG.md`:

```markdown
# LOG

## 2026-07-05

| # | Change | Result |
|---|---|---|
| 1 | Reproduced CSV import bug | Done |
```

## What It Is Not

- Not a vector memory database
- Not a task management app
- Not a replacement for tool-specific rules
- Not tied to one model or one editor

## First Reference Adapter

The first reference adapter is for Codex using an OpenAI-compatible model through a relay, such as DeepSeek via `codex-relay`.

The protocol itself is generic. The relay adapter is only one implementation path.

See [docs/codex-relay-adapter.md](docs/codex-relay-adapter.md).

## Status

v0.2 alpha.

## License

MIT.

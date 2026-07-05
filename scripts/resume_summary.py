#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path


def read_required(path: Path) -> str:
    if not path.exists():
        print(f"error: missing required file: {path}", file=sys.stderr)
        raise SystemExit(1)
    return path.read_text(encoding="utf-8-sig").strip()


def recent_log_entries(log_text: str, limit: int) -> str:
    rows = []
    for line in log_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if stripped.startswith("| # ") or stripped.startswith("|---"):
            continue
        rows.append(stripped)
    return "\n".join(rows[-limit:]) if rows else "- No log entries found."


def clamp_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    marker = "\n\n[Truncated to fit --max-chars. Read the source files for full context.]\n"
    return text[: max_chars - len(marker)].rstrip() + marker


def build_summary(target_dir: Path, log_entries: int, max_chars: int) -> str:
    agents = read_required(target_dir / "AGENTS.md")
    status = read_required(target_dir / "STATUS.md")
    log = read_required(target_dir / "LOG.md")

    summary = f"""# Resume Summary

Generated: {dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
Project: {target_dir}

## Continue Protocol

- File state wins over chat memory.
- Read `AGENTS.md` and `STATUS.md` before acting.
- Continue from the `Next step` in `STATUS.md`.
- Do not invent missing project state.
- After a meaningful step, update `STATUS.md` and append `LOG.md`.

## STATUS.md

{status}

## Recent LOG.md Entries

{recent_log_entries(log, log_entries)}

## AGENTS.md

{agents}

## Resume Instruction

Continue from the current `STATUS.md` next step. If the state is stale, unclear, or inconsistent with the user request, stop and refresh the status before doing work.
"""
    return clamp_text(summary.strip() + "\n", max_chars)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a concise prompt for resuming a fight-on-memory project."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Project directory containing AGENTS.md, STATUS.md, and LOG.md.",
    )
    parser.add_argument(
        "--log-entries",
        type=int,
        default=8,
        help="Number of recent LOG.md table entries to include.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Maximum output size.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the summary. Defaults to stdout.",
    )
    args = parser.parse_args()

    if args.log_entries < 1:
        print("error: --log-entries must be at least 1", file=sys.stderr)
        return 1
    if args.max_chars < 1000:
        print("error: --max-chars must be at least 1000", file=sys.stderr)
        return 1

    target_dir = Path(args.target).resolve()
    summary = build_summary(target_dir, args.log_entries, args.max_chars)
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(summary, encoding="utf-8", newline="\n")
        print(f"Resume summary written to: {output_path}")
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

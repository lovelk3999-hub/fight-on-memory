#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


def markdown_cell(value: str) -> str:
    return " ".join(value.splitlines()).replace("|", r"\|").strip()


def next_entry_number(section: str) -> int:
    numbers = [
        int(match.group(1))
        for match in re.finditer(r"^\|\s*(\d+)\s*\|", section, re.MULTILINE)
    ]
    return max(numbers, default=0) + 1


def append_log_entry(log_path: Path, change: str, result: str, notes: str) -> int:
    if not log_path.exists():
        print(f"error: {log_path} not found. Run init_checkpoint.py first.", file=sys.stderr)
        raise SystemExit(1)

    today = dt.date.today().isoformat()
    date_header = f"## {today}"
    table_header = "| # | Change | Result | Notes |\n|---|---|---|---|"
    text = log_path.read_text(encoding="utf-8-sig")

    if date_header not in text:
        text = text.rstrip() + f"\n\n{date_header}\n\n{table_header}\n"
        section = ""
        insert_at = len(text)
    else:
        start = text.index(date_header)
        after_header_start = start + len(date_header)
        after_header = text[after_header_start:]
        next_date = re.search(r"\n## \d{4}-\d{2}-\d{2}\b", after_header)
        if next_date:
            insert_at = after_header_start + next_date.start()
            section = text[after_header_start:insert_at]
        else:
            insert_at = len(text)
            section = text[after_header_start:]

        if "| # | Change | Result | Notes |" not in section:
            text = text[:insert_at].rstrip() + f"\n\n{table_header}\n" + text[insert_at:]
            insert_at += len(f"\n\n{table_header}\n")
            section = table_header + "\n" + section

    number = next_entry_number(section)
    row = (
        f"| {number} | {markdown_cell(change)} | {markdown_cell(result)} | "
        f"{markdown_cell(notes)} |"
    )
    text = text[:insert_at].rstrip() + "\n" + row + "\n" + text[insert_at:].lstrip("\n")
    log_path.write_text(text, encoding="utf-8", newline="\n")
    return number


def replace_or_add_header(text: str, label: str, value: str) -> str:
    pattern = re.compile(rf"^> {re.escape(label)}:.*$", re.MULTILINE)
    replacement = f"> {label}: {value}"
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    lines = text.splitlines()
    insert_at = 1 if lines and lines[0].startswith("# ") else 0
    lines.insert(insert_at, replacement)
    return "\n".join(lines) + "\n"


def update_status(
    status_path: Path,
    current_task: str | None,
    next_step: str | None,
) -> None:
    if not status_path.exists():
        print(f"warning: {status_path} not found; skipped status update", file=sys.stderr)
        return

    text = status_path.read_text(encoding="utf-8-sig")
    text = replace_or_add_header(text, "Updated", dt.date.today().isoformat())
    if current_task:
        text = replace_or_add_header(text, "Current task", current_task)
    if next_step:
        text = replace_or_add_header(text, "Next step", next_step)
    status_path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a fight-on-memory checkpoint and refresh STATUS.md."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Project directory containing STATUS.md and LOG.md.",
    )
    parser.add_argument("--change", required=True, help="What changed.")
    parser.add_argument("--result", default="Done", help="Result label. Defaults to Done.")
    parser.add_argument("--notes", default="-", help="Short notes for the log row.")
    parser.add_argument("--current-task", help="New STATUS.md current task.")
    parser.add_argument("--next-step", help="New STATUS.md next step.")
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    entry_number = append_log_entry(
        target_dir / "LOG.md",
        args.change,
        args.result,
        args.notes,
    )
    update_status(target_dir / "STATUS.md", args.current_task, args.next_step)

    print(f"Checkpoint #{entry_number} written in: {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path


CORE_FILES = ("AGENTS.md", "STATUS.md", "LOG.md")
CONFIG_FILE = ".fightonmemory.toml"


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def render_template(text: str) -> str:
    return text.replace("YYYY-MM-DD", dt.date.today().isoformat())


def write_from_template(template_path: Path, target_path: Path, force: bool) -> str:
    existed = target_path.exists()
    if existed and not force:
        return "skipped"

    target_path.parent.mkdir(parents=True, exist_ok=True)
    text = render_template(template_path.read_text(encoding="utf-8-sig"))
    target_path.write_text(text, encoding="utf-8", newline="\n")
    return "overwritten" if existed else "created"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize fight-on-memory files in a project."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Project directory to initialize. Defaults to the current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    parser.add_argument(
        "--with-config",
        action="store_true",
        help=f"Also create optional {CONFIG_FILE}.",
    )
    args = parser.parse_args()

    target_dir = Path(args.target).resolve()
    templates_dir = project_root() / "templates"
    if not templates_dir.exists():
        print(f"error: templates directory not found: {templates_dir}", file=sys.stderr)
        return 1

    results: list[tuple[str, str]] = []
    for name in CORE_FILES:
        template_path = templates_dir / name
        if not template_path.exists():
            print(f"error: template not found: {template_path}", file=sys.stderr)
            return 1
        status = write_from_template(template_path, target_dir / name, args.force)
        results.append((name, status))

    if args.with_config:
        template_path = templates_dir / CONFIG_FILE
        if not template_path.exists():
            template_path = project_root() / CONFIG_FILE
        if not template_path.exists():
            print(f"error: config template not found: {CONFIG_FILE}", file=sys.stderr)
            return 1
        status = write_from_template(template_path, target_dir / CONFIG_FILE, args.force)
        results.append((CONFIG_FILE, status))

    print(f"Initialized fight-on-memory in: {target_dir}")
    for name, status in results:
        print(f"- {status}: {name}")
    print("Next: edit STATUS.md, then run checkpoint.py after meaningful work.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

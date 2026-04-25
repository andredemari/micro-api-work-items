"""Opt-in installer for local safety-check Git hooks."""

from __future__ import annotations

import argparse
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def default_python_command() -> str:
    return shlex.quote(sys.executable)


def hook_commands(python_command: str) -> dict[str, str]:
    return {
        "pre-commit": (
            'cd "$(git rev-parse --show-toplevel)" || exit 1\n'
            f"{python_command} scripts/safety_check.py --mode staged\n"
        ),
        "pre-push": (
            'cd "$(git rev-parse --show-toplevel)" || exit 1\n'
            f"{python_command} scripts/safety_check.py --mode release\n"
        ),
    }


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("not a Git repository")
    return Path(result.stdout.strip())


def install_hooks(root: Path, python_command: str, force: bool = False) -> int:
    hooks_dir = root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    for name, command in hook_commands(python_command).items():
        hook_path = hooks_dir / name
        if hook_path.exists() and not force:
            print(f"Refusing to overwrite existing hook: {hook_path}")
            return 1

        hook_path.write_text(f"#!/bin/sh\n{command}", encoding="utf-8")
        current_mode = hook_path.stat().st_mode
        hook_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"Installed {name} hook: {hook_path}")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install local safety-check Git hooks.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing hooks; use only after reviewing current hook contents",
    )
    parser.add_argument(
        "--python-command",
        default=default_python_command(),
        help="shell command used by hooks to run Python; defaults to the current interpreter path",
    )
    args = parser.parse_args(argv)

    try:
        return install_hooks(repo_root(), python_command=args.python_command, force=args.force)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

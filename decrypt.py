#!/usr/bin/env python3
"""Restore files encrypted by the Ransomware-Lab simulator."""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

from ransomlab.common import (
    ENCRYPTED_SUFFIX,
    LabError,
    atomic_write,
    decrypt_bytes,
    iter_encrypted_files,
    resolve_lab_target,
)


def decrypt_directory(target: Path, code: str) -> int:
    files = list(iter_encrypted_files(target))
    destinations = {
        path: path.with_name(path.name[: -len(ENCRYPTED_SUFFIX)]) for path in files
    }
    collisions = [destination for destination in destinations.values() if destination.exists()]
    if collisions:
        raise LabError(f"Restore destination already exists: {collisions[0]}")

    # Verify every file before changing any of them. A wrong code leaves the set intact.
    plaintext = {source: decrypt_bytes(source.read_bytes(), code) for source in files}
    completed = 0
    for source, destination in destinations.items():
        atomic_write(destination, plaintext[source])
        source.unlink()
        completed += 1
    return completed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Restore Ransomware-Lab test files.")
    parser.add_argument("--target", required=True, help="Prepared lab directory")
    parser.add_argument(
        "--code",
        help="Recovery code (omit this option to enter it at a hidden prompt)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    code = args.code or getpass.getpass("Recovery code: ")
    try:
        target = resolve_lab_target(args.target)
        count = decrypt_directory(target, code)
    except (LabError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Restored {count} file(s) inside: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


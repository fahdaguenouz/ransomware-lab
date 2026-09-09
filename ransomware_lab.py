#!/usr/bin/env python3
"""Single command-line entry point for the safe Ransomware-Lab simulation."""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path

from decrypt import decrypt_directory
from encrypt import CONFIRMATION_FLAG, default_desktop, encrypt_directory, write_note
from ransomlab.common import LabError, MARKER_NAME, atomic_write, generate_code, resolve_lab_target


def prepare_lab(raw_target: str | Path) -> Path:
    target = Path(raw_target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    atomic_write(
        target / MARKER_NAME,
        b"This directory is explicitly opted in to the Ransomware-Lab simulation.\n",
    )
    return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ransomware-lab",
        description="Safe, directory-scoped educational ransomware simulation.",
    )
    parser.add_argument("--version", action="version", version="Ransomware-Lab 1.0.0")
    commands = parser.add_subparsers(dest="command", required=True)

    setup = commands.add_parser("setup", help="Prepare a disposable lab directory")
    setup.add_argument("target", help="Directory to create and mark as lab data")

    encrypt = commands.add_parser("encrypt", help="Encrypt files in a marked directory")
    encrypt.add_argument("--target", required=True, help="Prepared lab directory")
    encrypt.add_argument(
        CONFIRMATION_FLAG,
        action="store_true",
        help="Confirm that the target is disposable test data in an isolated VM",
    )
    encrypt.add_argument(
        "--note-dir",
        type=Path,
        default=default_desktop(),
        help="Note directory (default: current user's Desktop)",
    )

    decrypt = commands.add_parser("decrypt", help="Restore encrypted lab files")
    decrypt.add_argument("--target", required=True, help="Prepared lab directory")
    decrypt.add_argument("--code", help="Recovery code; omitted means prompt securely")
    return parser


def run_setup(args: argparse.Namespace) -> int:
    try:
        target = prepare_lab(args.target)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Prepared lab directory: {target}")
    print("Only place disposable test files in this directory.")
    return 0


def run_encrypt(args: argparse.Namespace) -> int:
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


def run_decrypt(args: argparse.Namespace) -> int:
    code = args.code or getpass.getpass("Recovery code: ")
    try:
        target = resolve_lab_target(args.target)
        count = decrypt_directory(target, code)
    except (LabError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Restored {count} file(s) inside: {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "setup":
        return run_setup(args)
    if args.command == "encrypt":
        return run_encrypt(args)
    return run_decrypt(args)


if __name__ == "__main__":
    raise SystemExit(main())


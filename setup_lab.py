#!/usr/bin/env python3
"""Prepare an empty or disposable directory for the safe simulation."""

from __future__ import annotations

import argparse
from pathlib import Path

from ransomlab.common import MARKER_NAME, atomic_write


def main() -> int:
    parser = argparse.ArgumentParser(description="Mark a directory as disposable lab data.")
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    atomic_write(
        target / MARKER_NAME,
        b"This directory is explicitly opted in to the Ransomware-Lab simulation.\n",
    )
    print(f"Prepared lab directory: {target}")
    print("Only place disposable test files in this directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


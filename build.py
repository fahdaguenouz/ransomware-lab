#!/usr/bin/env python3
"""Build the unified Ransomware-Lab command as one executable file."""

from __future__ import annotations

import os
from pathlib import Path

import PyInstaller.__main__


ROOT = Path(__file__).resolve().parent
OUTPUT_NAME = "ransomware-lab"


def main() -> int:
    os.chdir(ROOT)
    PyInstaller.__main__.run(
        [
            "--onefile",
            "--clean",
            "--noconfirm",
            "--name",
            OUTPUT_NAME,
            "--distpath",
            str(ROOT / "release"),
            "--workpath",
            str(ROOT / "build" / OUTPUT_NAME),
            "--specpath",
            str(ROOT),
            str(ROOT / "ransomware_lab.py"),
        ]
    )
    suffix = ".exe" if os.name == "nt" else ""
    output = ROOT / "release" / f"{OUTPUT_NAME}{suffix}"
    print(f"\nSingle-file executable created: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""Shared cryptographic and safety helpers for the lab programs."""

from __future__ import annotations

import os
import secrets
import string
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


MARKER_NAME = ".ransomware_lab_safe"
ENCRYPTED_SUFFIX = ".ransomlab"
NOTE_NAME = "RANSOM_NOTE.txt"
MAGIC = b"RANSIM01"
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
HEADER_SIZE = len(MAGIC) + SALT_SIZE + NONCE_SIZE
CODE_ALPHABET = string.ascii_uppercase + string.digits
CODE_LENGTH = 24


class LabError(Exception):
    """An expected, user-facing lab error."""


def resolve_lab_target(raw_target: str | Path) -> Path:
    """Resolve a target and require the opt-in marker created by setup_lab.py."""
    target = Path(raw_target).expanduser().resolve(strict=True)
    if not target.is_dir():
        raise LabError(f"Target is not a directory: {target}")

    home = Path.home().resolve()
    filesystem_root = Path(target.anchor).resolve()
    if target in {home, filesystem_root}:
        raise LabError("Refusing to operate on a home directory or filesystem root.")
    if not (target / MARKER_NAME).is_file():
        raise LabError(
            f"Safety marker missing. Run setup_lab.py for this directory first: {target}"
        )
    return target


def generate_code() -> str:
    """Generate a cryptographically random, human-readable recovery code."""
    raw = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
    return "-".join(raw[index : index + 6] for index in range(0, CODE_LENGTH, 6))


def normalize_code(code: str) -> bytes:
    compact = code.strip().replace("-", "").upper()
    if len(compact) != CODE_LENGTH or any(ch not in CODE_ALPHABET for ch in compact):
        raise LabError("The recovery code must contain 24 letters/numbers.")
    return compact.encode("ascii")


def derive_key(code: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from the recovery code and a random per-file salt."""
    return Scrypt(salt=salt, length=KEY_SIZE, n=2**14, r=8, p=1).derive(
        normalize_code(code)
    )


def iter_plain_files(target: Path):
    """Yield regular files within target without following symlinks."""
    for root, directory_names, file_names in os.walk(target, followlinks=False):
        directory_names[:] = [
            name for name in directory_names if not (Path(root) / name).is_symlink()
        ]
        for name in file_names:
            path = Path(root) / name
            if path.is_symlink() or name == MARKER_NAME or name.endswith(ENCRYPTED_SUFFIX):
                continue
            yield path


def iter_encrypted_files(target: Path):
    for root, directory_names, file_names in os.walk(target, followlinks=False):
        directory_names[:] = [
            name for name in directory_names if not (Path(root) / name).is_symlink()
        ]
        for name in file_names:
            path = Path(root) / name
            if not path.is_symlink() and name.endswith(ENCRYPTED_SUFFIX):
                yield path


def encrypt_bytes(data: bytes, code: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(derive_key(code, salt)).encrypt(nonce, data, MAGIC)
    return MAGIC + salt + nonce + ciphertext


def decrypt_bytes(payload: bytes, code: str) -> bytes:
    if len(payload) < HEADER_SIZE + 16 or not payload.startswith(MAGIC):
        raise LabError("File is not a valid Ransomware-Lab encrypted file.")
    salt_start = len(MAGIC)
    nonce_start = salt_start + SALT_SIZE
    body_start = nonce_start + NONCE_SIZE
    salt = payload[salt_start:nonce_start]
    nonce = payload[nonce_start:body_start]
    try:
        return AESGCM(derive_key(code, salt)).decrypt(nonce, payload[body_start:], MAGIC)
    except InvalidTag as exc:
        raise LabError("Wrong recovery code or damaged encrypted file.") from exc


def atomic_write(path: Path, data: bytes) -> None:
    """Write beside the destination and atomically replace it when complete."""
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(6)}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


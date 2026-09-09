from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from decrypt import decrypt_directory
from encrypt import encrypt_directory, write_note
from ransomlab.common import (
    ENCRYPTED_SUFFIX,
    MARKER_NAME,
    NOTE_NAME,
    LabError,
    generate_code,
    resolve_lab_target,
)
from ransomware_lab import main as unified_main


class RansomwareLabTests(unittest.TestCase):
    def make_lab(self, root: Path) -> Path:
        target = root / "safe-test-data"
        target.mkdir()
        (target / MARKER_NAME).write_text("test marker\n", encoding="utf-8")
        return target

    def test_round_trip_nested_text_and_binary_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = self.make_lab(root)
            (target / "nested").mkdir()
            original = {
                target / "hello.txt": b"hello ransomware lab\n",
                target / "empty.bin": b"",
                target / "nested" / "random.bin": bytes(range(256)),
            }
            for path, content in original.items():
                path.write_bytes(content)

            code = generate_code()
            self.assertEqual(encrypt_directory(resolve_lab_target(target), code), 3)
            for path in original:
                self.assertFalse(path.exists())
                self.assertTrue(Path(str(path) + ENCRYPTED_SUFFIX).exists())

            self.assertEqual(decrypt_directory(resolve_lab_target(target), code), 3)
            for path, content in original.items():
                self.assertEqual(path.read_bytes(), content)

    def test_wrong_code_does_not_modify_encrypted_set(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_lab(Path(temporary))
            source = target / "important.txt"
            source.write_text("disposable", encoding="utf-8")
            encrypt_directory(target, generate_code())
            encrypted = Path(str(source) + ENCRYPTED_SUFFIX)

            with self.assertRaises(LabError):
                decrypt_directory(target, generate_code())
            self.assertTrue(encrypted.exists())
            self.assertFalse(source.exists())

    def test_directory_without_marker_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(LabError):
                resolve_lab_target(temporary)

    def test_note_contains_dynamic_code(self):
        with tempfile.TemporaryDirectory() as temporary:
            note_dir = Path(temporary)
            code = generate_code()
            path = write_note(note_dir, code)
            self.assertEqual(path.name, NOTE_NAME)
            self.assertIn(code, path.read_text(encoding="utf-8"))

    def test_codes_are_well_formed_and_different(self):
        first = generate_code()
        second = generate_code()
        self.assertNotEqual(first, second)
        self.assertEqual([len(part) for part in first.split("-")], [6, 6, 6, 6])

    def test_unified_setup_command_creates_marker(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "unified-lab"
            self.assertEqual(unified_main(["setup", str(target)]), 0)
            self.assertTrue((target / MARKER_NAME).is_file())


if __name__ == "__main__":
    unittest.main()

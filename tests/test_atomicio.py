"""Atomic filesystem writes (embodied_learning/atomicio.py).

Nothing network- or CIFS-specific is exercised: tmpfs honors O_EXCL and
same-directory os.replace with the same semantics as a CIFS share, which is
all the helpers rely on. The scripts-layer re-export (lib.jsonio) is checked
for identity so the two import paths can never drift.
"""

import importlib.util
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "embodied_learning" / "atomicio.py"
_spec = importlib.util.spec_from_file_location("atomicio_test_module", _SCRIPT)
atomicio = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(atomicio)


class AtomicWriteJsonTest(unittest.TestCase):
    def test_round_trip_and_no_tmp_leftovers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "doc.json"
            atomicio.atomic_write_json(path, {"topic": "具身智能", "n": 2})
            self.assertEqual(
                json.loads(path.read_text(encoding="utf-8")), {"topic": "具身智能", "n": 2}
            )
            self.assertEqual(list(Path(tmp).glob("**/.*tmp-*")), [])
            self.assertTrue(path.read_text(encoding="utf-8").endswith("\n"))

    def test_replaces_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.json"
            path.write_text("stale", encoding="utf-8")
            atomicio.atomic_write_json(path, [1, 2])
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), [1, 2])

    def test_cleanup_on_failure_keeps_old_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.json"
            atomicio.atomic_write_json(path, {"v": 1})
            original = path.read_text(encoding="utf-8")
            with mock.patch.object(atomicio.json, "dumps", side_effect=RuntimeError("boom")):
                with self.assertRaises(RuntimeError):
                    atomicio.atomic_write_json(path, {"v": 2})
            self.assertEqual(path.read_text(encoding="utf-8"), original)
            self.assertEqual(list(Path(tmp).glob(".*tmp-*")), [])


class AtomicWriteTextAndBytesTest(unittest.TestCase):
    def test_text_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "note.md"
            atomicio.atomic_write_text(path, "# 速读\n中文内容\n")
            self.assertEqual(path.read_text(encoding="utf-8"), "# 速读\n中文内容\n")

    def test_bytes_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "paper.html"
            payload = b"<html>\xff\xfe</html>"
            atomicio.atomic_write_bytes(path, payload)
            self.assertEqual(path.read_bytes(), payload)

    def test_repeated_replaces_leave_single_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "doc.txt"
            atomicio.atomic_write_text(path, "v1")
            atomicio.atomic_write_text(path, "v2")
            self.assertEqual(path.read_text(encoding="utf-8"), "v2")
            self.assertEqual(list(Path(tmp).iterdir()), [path])


class AtomicCopyTest(unittest.TestCase):
    def test_copies_content_and_replaces_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src" / "wiki.js"
            dst = Path(tmp) / "out" / "assets" / "wiki.js"
            src.parent.mkdir(parents=True)
            src.write_bytes(b"console.log('v1')")
            atomicio.atomic_copy(src, dst)
            self.assertEqual(dst.read_bytes(), b"console.log('v1')")
            atomicio.atomic_copy(src, dst)  # overwrite path is fine too
            self.assertEqual(dst.read_bytes(), b"console.log('v1')")
            self.assertEqual(list(dst.parent.iterdir()), [dst])


class JsonioReexportTest(unittest.TestCase):
    def test_lib_jsonio_reexports_atomicio(self) -> None:
        spec = importlib.util.spec_from_file_location(
            f"jsonio_test_{uuid.uuid4().hex}", _REPO_ROOT / "scripts" / "lib" / "jsonio.py"
        )
        assert spec and spec.loader
        lib_jsonio = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lib_jsonio)
        # The shim must resolve to the same package module (single source of
        # truth), not to a redefinition — hence the module-name + identity check
        # against the regular import path.
        import embodied_learning.atomicio as package_atomicio

        self.assertEqual(lib_jsonio.atomic_write_json.__module__, "embodied_learning.atomicio")
        self.assertIs(lib_jsonio.atomic_write_json, package_atomicio.atomic_write_json)
        self.assertIs(lib_jsonio.atomic_write_text, package_atomicio.atomic_write_text)
        self.assertIs(lib_jsonio.atomic_write_bytes, package_atomicio.atomic_write_bytes)
        self.assertIs(lib_jsonio.atomic_copy, package_atomicio.atomic_copy)


if __name__ == "__main__":
    unittest.main()

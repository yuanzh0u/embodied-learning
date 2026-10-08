#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "print_registry_titles.py"
SPEC = importlib.util.spec_from_file_location("print_registry_titles", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


class PrintRegistryTitlesTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.registry_path = self.tmp / "candidate-registry.json"
        payload = {
            "candidate_count": 3,
            "status_counts": {"discovered": 2, "accepted": 1},
            "candidates": [
                {"arxiv_id": "2401.00001", "status": "discovered", "title": "Alpha Paper", "published": "2024-01-01", "summary": "LONG " * 200},
                {"arxiv_id": "2401.00002", "status": "accepted", "title": "Beta Paper", "published": "2024-02-01", "summary": "LONG " * 200},
                {"arxiv_id": "2401.00003", "status": "discovered", "title": "Gamma Paper", "published": "2024-03-01", "summary": "LONG " * 200},
            ],
        }
        self.registry_path.write_text(json.dumps(payload), encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_title_slice_omits_summaries(self) -> None:
        import io
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = mod.main(
                [
                    "--candidate-registry",
                    str(self.registry_path),
                    "--limit",
                    "2",
                ]
            )
        self.assertEqual(0, code)
        out = buf.getvalue()
        self.assertIn("NEVER dump full candidate-registry.json", out)
        self.assertIn("2401.00002\taccepted\tBeta Paper", out)
        self.assertNotIn("LONG LONG", out)
        self.assertEqual(2, sum(1 for line in out.splitlines() if "\t" in line))

    def test_status_counts_only(self) -> None:
        import io
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = mod.main(
                [
                    "--candidate-registry",
                    str(self.registry_path),
                    "--status-counts-only",
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(0, code)
        data = json.loads(buf.getvalue())
        self.assertEqual(3, data["candidate_count"])
        self.assertEqual({"discovered": 2, "accepted": 1}, data["status_counts"])
        self.assertNotIn("titles", data)


if __name__ == "__main__":
    unittest.main()

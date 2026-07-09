#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_run.py"
SPEC = importlib.util.spec_from_file_location("init_run", SCRIPT)
init_run = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(init_run)


class InitRunTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--topic",
                "感知误差 vs 认知误差",
                "--knowledge-id",
                "EA-DATA",
                "--knowledge-id",
                "EA-MODEL",
                "--time-range",
                "2026-01-09..2026-07-09",
                "--date",
                "20260709",
                "--work-dir",
                str(self.tmp),
                *extra,
            ],
            text=True,
            capture_output=True,
        )

    def test_creates_in_progress_birth_certificate(self) -> None:
        completed = self.run_cli()
        self.assertEqual(0, completed.returncode, completed.stderr)
        run_dirs = list(self.tmp.glob("literature-review-*-20260709"))
        self.assertEqual(1, len(run_dirs))
        manifest = json.loads((run_dirs[0] / "run.json").read_text(encoding="utf-8"))
        self.assertEqual("in-progress", manifest["status"])
        self.assertEqual(["EA-DATA", "EA-MODEL"], manifest["knowledge_ids"])
        self.assertEqual("2026-01-09..2026-07-09", manifest["time_range"])
        self.assertEqual(0, manifest["event_count"])
        self.assertEqual({}, manifest["files"])
        self.assertEqual(run_dirs[0].name, manifest["run"])

    def test_refuses_to_overwrite_without_force(self) -> None:
        first = self.run_cli()
        self.assertEqual(0, first.returncode)
        second = self.run_cli()
        self.assertEqual(1, second.returncode)
        self.assertIn("--force", second.stderr)
        third = self.run_cli("--force")
        self.assertEqual(0, third.returncode)


if __name__ == "__main__":
    unittest.main()

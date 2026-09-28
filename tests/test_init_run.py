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
import sys  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))  # lib.* imports inside the script
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

    def _command(self, *extra: str) -> list[str]:
        return [
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
        ]

    def run_cli(self, *extra: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            self._command(*extra),
            text=True,
            capture_output=True,
        )

    def run_cli_async(self, *extra: str) -> subprocess.Popen:
        return subprocess.Popen(
            self._command(*extra),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_creates_in_progress_birth_certificate(self) -> None:
        completed = self.run_cli()
        self.assertEqual(0, completed.returncode, completed.stderr)
        run_dirs = list(self.tmp.glob("literature-review-*-20260709"))
        self.assertEqual(1, len(run_dirs))
        manifest = json.loads((run_dirs[0] / "run.json").read_text(encoding="utf-8"))
        self.assertEqual("in-progress", manifest["status"])
        self.assertEqual(2, manifest["workflow_version"])
        self.assertEqual("scoping", manifest["review_mode"])
        self.assertEqual(["EA-DATA", "EA-MODEL"], manifest["knowledge_ids"])
        self.assertEqual("2026-01-09..2026-07-09", manifest["time_range"])
        self.assertEqual(0, manifest["event_count"])
        self.assertEqual({}, manifest["files"])
        self.assertEqual(run_dirs[0].name, manifest["run"])

    def test_accepts_systematic_review_mode(self) -> None:
        completed = self.run_cli("--review-mode", "systematic")
        self.assertEqual(0, completed.returncode, completed.stderr)
        run_dir = next(self.tmp.glob("literature-review-*-20260709"))
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual("systematic", manifest["review_mode"])

    def test_refuses_to_overwrite_without_force(self) -> None:
        first = self.run_cli()
        self.assertEqual(0, first.returncode)
        second = self.run_cli()
        self.assertEqual(1, second.returncode)
        self.assertIn("--force", second.stderr)
        third = self.run_cli("--force")
        self.assertEqual(0, third.returncode)

    def test_concurrent_creation_yields_exactly_one_winner(self) -> None:
        """Two terminals/machines starting the same topic+date run: O_EXCL
        creation lets one win; the other must exit 1, not clobber."""
        processes = [self.run_cli_async() for _ in range(3)]
        outputs = [process.communicate(timeout=60) for process in processes]
        codes = [process.returncode for process in processes]
        self.assertEqual(codes.count(0), 1, str(outputs))
        run_dir = next(self.tmp.glob("literature-review-*-20260709"))
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "in-progress")


if __name__ == "__main__":
    unittest.main()

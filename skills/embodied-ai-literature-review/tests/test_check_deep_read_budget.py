#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = (
    ROOT
    / "skills"
    / "embodied-ai-literature-review"
    / "scripts"
    / "check_deep_read_budget.py"
)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=check,
        text=True,
        capture_output=True,
        cwd=ROOT,
    )


class DeepReadBudgetTests(unittest.TestCase):
    def _summary(self, deep: int, accepted: int = 15) -> Path:
        path = Path(self._tmp.name) / f"summary-{deep}.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "deep_read_count": deep,
                    "map_read_count": deep,
                    "accepted_evidence_paper_count": accepted,
                }
            ),
            encoding="utf-8",
        )
        return path

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_within_budget_ok(self) -> None:
        # scoping floor 15 + 10 = 25
        summary = self._summary(20)
        completed = run(
            "--reading-summary",
            str(summary),
            "--review-mode",
            "scoping",
            "--json",
        )
        report = json.loads(completed.stdout)
        self.assertTrue(report["within_budget"])
        self.assertEqual(report["llm_deep_read_budget"], 25)
        self.assertEqual(report["accepted_paper_floor"], 15)

    def test_over_budget_warns_but_exits_zero(self) -> None:
        summary = self._summary(40)
        completed = run(
            "--reading-summary",
            str(summary),
            "--review-mode",
            "scoping",
            "--json",
            check=False,
        )
        self.assertEqual(completed.returncode, 0)
        report = json.loads(completed.stdout)
        self.assertFalse(report["within_budget"])
        self.assertIn("exceeds", report["warning"])

    def test_strict_over_budget_exits_one(self) -> None:
        summary = self._summary(40)
        completed = run(
            "--reading-summary",
            str(summary),
            "--review-mode",
            "scoping",
            "--strict",
            check=False,
        )
        self.assertEqual(completed.returncode, 1)


if __name__ == "__main__":
    unittest.main()

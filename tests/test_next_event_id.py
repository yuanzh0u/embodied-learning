#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "next_event_id.py"
SPEC = importlib.util.spec_from_file_location("next_event_id", SCRIPT)
next_event_id = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(next_event_id)


def write_run(evidence_dir: Path, run: str, event_ids: list[str]) -> None:
    run_dir = evidence_dir / run
    run_dir.mkdir(parents=True)
    lines = [json.dumps({"event_id": event_id}) for event_id in event_ids]
    (run_dir / "evidence.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


class NextEventIdTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.evidence = Path(self._tmp.name) / "evidence"
        self.evidence.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_scan_reports_max_per_prefix(self) -> None:
        write_run(self.evidence, "run-a", ["EA-TWM-2026-0001", "EA-TWM-2026-0018"])
        write_run(self.evidence, "run-b", ["EA-TWM-2026-0007", "EA-ALIGN-2026-0010"])
        highest = next_event_id.scan(self.evidence)
        self.assertEqual(highest["EA-TWM-2026"], 18)
        self.assertEqual(highest["EA-ALIGN-2026"], 10)

    def test_cross_run_collision_avoided(self) -> None:
        write_run(self.evidence, "run-a", ["EA-DATA-2026-0005"])
        write_run(self.evidence, "run-b", ["EA-DATA-2026-0009"])
        highest = next_event_id.scan(self.evidence)
        self.assertEqual(f"EA-DATA-2026-{highest['EA-DATA-2026'] + 1:04d}", "EA-DATA-2026-0010")

    def test_malformed_lines_and_ids_skipped(self) -> None:
        run_dir = self.evidence / "run-a"
        run_dir.mkdir()
        (run_dir / "evidence.jsonl").write_text(
            'not json\n{"event_id": "no-sequence-suffix"}\n{"event_id": "EA-X-2026-0002"}\n',
            encoding="utf-8",
        )
        highest = next_event_id.scan(self.evidence)
        self.assertEqual(highest, {"EA-X-2026": 2})

    def test_empty_layer(self) -> None:
        self.assertEqual(next_event_id.scan(self.evidence), {})


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "next_event_id.py"
import sys  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))  # lib.* imports inside the script
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


class ClaimPrefixTest(unittest.TestCase):
    """O_EXCL prefix reservations under <kb-root>/.claims/event-prefix/."""

    def setUp(self) -> None:
        import os

        self._tmp = tempfile.TemporaryDirectory()
        self.kb_root = Path(self._tmp.name)
        self.evidence = self.kb_root / "evidence"
        self.evidence.mkdir()
        self._env = os.environ.copy()
        os.environ["EMBODIED_KB_LOCK_DIR"] = str(self.kb_root / ".locks")

    def tearDown(self) -> None:
        import os

        os.environ.clear()
        os.environ.update(self._env)
        self._tmp.cleanup()

    def _run_cli(self, *flags: str) -> tuple[int, str]:
        """CLI-level coverage via subprocess (main() parses sys.argv)."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, str(SCRIPT), *flags,
             "--evidence-dir", str(self.evidence), "--kb-root", str(self.kb_root)],
            capture_output=True, text=True, timeout=60,
        )
        return result.returncode, result.stdout + result.stderr

    def test_claim_then_conflict_then_list(self) -> None:
        code, out = self._run_cli("--claim-prefix", "EA-DEMO-2026", "--run", "run-a")
        self.assertEqual(code, 0, out)
        claim_file = self.kb_root / ".claims" / "event-prefix" / "EA-DEMO-2026.json"
        self.assertTrue(claim_file.is_file())
        # Same prefix for a different run loses (exit 4).
        code, out = self._run_cli("--claim-prefix", "EA-DEMO-2026", "--run", "run-b")
        self.assertEqual(code, 4)
        self.assertIn("run-a", out)
        # The report annotates claims.
        code, out = self._run_cli("--prefix", "EA-DEMO-2026", "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["EA-DEMO-2026"]["claimed_by_run"], "run-a")
        # Listing shows the claim.
        code, out = self._run_cli("--claims", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)[0]["prefix"], "EA-DEMO-2026")

    def test_release_allows_reclaim(self) -> None:
        code, out = self._run_cli("--claim-prefix", "EA-DEMO-2026", "--run", "run-a")
        self.assertEqual(code, 0, out)
        code, out = self._run_cli("--release", "--claim-prefix", "EA-DEMO-2026")
        self.assertEqual(code, 0, out)
        code, out = self._run_cli("--claim-prefix", "EA-DEMO-2026", "--run", "run-b")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import json
import subprocess
import tempfile
import unittest
from unittest import mock
import os
# Keep the machine-wide rate-limit gate off the real shared state: tests
# here mock urlopen but still pass through the gate, so redirect its state
# dir before any gated module is exercised.
os.environ.setdefault("EMBODIED_RATELIMIT_DIR", tempfile.mkdtemp(prefix="ratelimit-test-"))
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))  # modules under src/ import embodied_learning.* at load time

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("extract_content_queue", ROOT / "embodied_learning" / "fetch" / "queue.py")
extract_content_queue = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(extract_content_queue)


class ExtractContentQueueTest(unittest.TestCase):
    def test_load_ids_normalizes_comments_urls_versions_and_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ids.txt"
            path.write_text("2606.03784v2\nhttps://arxiv.org/abs/2607.00673\n2606.03784 # duplicate\n", encoding="utf-8")
            self.assertEqual(["2606.03784", "2607.00673"], extract_content_queue.load_ids(path))


    def _opts(self, output_dir: Path) -> "extract_content_queue.QueueOptions":
        return extract_content_queue.QueueOptions(
            paper_id_file="ids.txt", terms="t", output_dir=str(output_dir),
        )

    def test_held_extraction_is_retried_not_cached(self) -> None:
        """A HELD paper must be supplementable: a rerun re-extracts it instead
        of returning the cached failure forever (transient fetch failures,
        e.g. rate limiting, would otherwise permanently drop the paper)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()
            held = output_dir / "2110.10805.json"
            held.write_text(json.dumps({
                "paper_id": "2110.10805", "available": False,
                "evidence_eligible": False, "error": "extractor exit 2: ",
            }), encoding="utf-8")
            calls: list[list[str]] = []

            def fake_run(command, capture_output, text, timeout, check):
                calls.append(command)
                target = Path(command[command.index("--output") + 1])
                target.write_text(json.dumps({
                    "paper_id": "2110.10805", "available": True,
                    "evidence_eligible": True,
                }), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run):
                result = extract_content_queue.extract_one("2110.10805", self._opts(output_dir), output_dir)
            self.assertEqual(len(calls), 1, "HELD paper must be re-extracted")
            self.assertTrue(result["evidence_eligible"])

            # An evidence-eligible extraction stays cached — no re-fetch.
            calls.clear()
            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run):
                result = extract_content_queue.extract_one("2110.10805", self._opts(output_dir), output_dir)
            self.assertEqual(calls, [])
            self.assertEqual(result["state"], "cached")

    def test_still_held_paper_recheckpoints_failure(self) -> None:
        """A genuinely unrecoverable paper re-extracts and re-checkpoints the
        HELD marker instead of crashing the queue."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()
            held = output_dir / "2110.10805.json"
            held.write_text(json.dumps({
                "paper_id": "2110.10805", "available": False,
                "evidence_eligible": False, "error": "old",
            }), encoding="utf-8")

            def fake_fail(command, capture_output, text, timeout, check):
                return subprocess.CompletedProcess(command, 2, "", "")

            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_fail):
                result = extract_content_queue.extract_one("2110.10805", self._opts(output_dir), output_dir)
            self.assertFalse(result["evidence_eligible"])
            data = json.loads((output_dir / "2110.10805.json").read_text(encoding="utf-8"))
            self.assertIn("extractor exit 2", data["error"])


class ChannelCircuitTest(unittest.TestCase):
    """When arxiv.org is unreachable every paper waits out its full
    paper_timeout — 79 x 300s on 2026-10-12 burned the whole extraction
    window. The circuit stops spending per-paper budgets on a dead channel."""

    def _opts(self, output_dir):
        return extract_content_queue.QueueOptions(
            paper_id_file="ids.txt", terms="t", output_dir=str(output_dir),
        )

    def test_connection_failures_trip_the_circuit(self) -> None:
        circuit = extract_content_queue._ChannelCircuit(limit=3)
        for _ in range(2):
            circuit.record(True)
            self.assertFalse(circuit.tripped)
        circuit.record(True)
        self.assertTrue(circuit.tripped)

    def test_success_resets_the_streak(self) -> None:
        circuit = extract_content_queue._ChannelCircuit(limit=3)
        circuit.record(True)
        circuit.record(True)
        circuit.record(False)  # a real extraction clears the streak
        circuit.record(True)
        self.assertFalse(circuit.tripped)

    def test_tripped_circuit_short_circuits_without_spawning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            circuit = extract_content_queue._ChannelCircuit(limit=1)
            circuit.record(True)  # trip it
            with mock.patch.object(extract_content_queue.subprocess, "run") as run:
                result = extract_content_queue.extract_one(
                    "2110.10805", self._opts(output_dir), output_dir, circuit
                )
            run.assert_not_called()
            self.assertEqual(result["state"], "channel-down")
            data = json.loads((output_dir / "2110.10805.json").read_text(encoding="utf-8"))
            self.assertIn("channel down", data["error"])

    def test_hard_timeout_counts_as_connection_failure(self) -> None:
        self.assertTrue(
            extract_content_queue._is_connection_failure("hard timeout after 300s")
        )
        self.assertTrue(
            extract_content_queue._is_connection_failure("Connection timed out")
        )
        # A per-paper failure must NOT advance the streak.
        self.assertFalse(
            extract_content_queue._is_connection_failure("extractor exit 2: no such paper")
        )

if __name__ == "__main__":
    unittest.main()

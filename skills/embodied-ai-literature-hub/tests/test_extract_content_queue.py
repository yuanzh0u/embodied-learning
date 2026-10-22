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

    def test_exit2_with_result_json_preserves_reason(self) -> None:
        """extract-content exits 2 for "ran but not evidence-eligible" and
        still writes its full result (quality grade, fallback_reason, error)
        to --output. Discarding it for a bare "extractor exit 2: " record
        erased every downstream reason (2026-10-16: packet and deep-read
        failures all read "extractor exit 2: " with an empty tail)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()

            def fake_exit2_with_payload(command, capture_output, text, timeout, check):
                target = Path(command[command.index("--output") + 1])
                target.write_text(json.dumps({
                    "paper_id": "2110.10805", "available": True,
                    "evidence_eligible": False,
                    "quality": {"grade": "low"},
                    "fallback_reason": "HTML unavailable or below the minimum full-text quality gate.",
                    "error": "HTML unavailable",
                }), encoding="utf-8")
                return subprocess.CompletedProcess(command, 2, "", "")

            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_exit2_with_payload):
                result = extract_content_queue.extract_one("2110.10805", self._opts(output_dir), output_dir)
            self.assertFalse(result["evidence_eligible"])
            data = json.loads((output_dir / "2110.10805.json").read_text(encoding="utf-8"))
            self.assertEqual(data["error"], "HTML unavailable")
            self.assertEqual(data["quality"]["grade"], "low")

    def test_run_queue_retries_held_papers_once_in_the_same_run(self) -> None:
        """2026-10-16 强化学习: all 16 HELD papers re-extracted cleanly minutes
        later — their failures were transient (rate limit / hard timeout under
        load), and waiting for a driver rerun wasted the whole deep-read floor.
        The queue now gives each HELD paper one more attempt before giving up."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()
            ids = tmp / "ids.txt"
            ids.write_text("2110.10805\n2110.10806\n", encoding="utf-8")
            attempts: dict[str, int] = {}

            def fake_run(command, capture_output, text, timeout, check):
                paper_id = command[command.index("--paper-id") + 1]
                attempts[paper_id] = attempts.get(paper_id, 0) + 1
                target = Path(command[command.index("--output") + 1])
                # First paper fails on attempt 1 and recovers on the retry;
                # second paper fails every time.
                ok = paper_id == "2110.10805" and attempts[paper_id] >= 2
                target.write_text(json.dumps({
                    "paper_id": paper_id,
                    "available": ok,
                    "evidence_eligible": ok,
                    "error": "" if ok else "HTML unavailable",
                }), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0 if ok else 2, "", "")

            options = extract_content_queue.QueueOptions(
                paper_id_file=str(ids), terms="t", output_dir=str(output_dir),
            )
            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run):
                summary = extract_content_queue.run_queue(options)
            self.assertEqual(attempts["2110.10805"], 2, "transient HELD must be retried")
            self.assertEqual(attempts["2110.10806"], 2, "still-HELD paper gets exactly one retry")
            self.assertEqual(summary["evidence_eligible_count"], 1)
            self.assertEqual(summary["held_count"], 1)


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

    def test_explicit_cache_dirs_reach_the_per_paper_options(self) -> None:
        """A queue-level cache dir (the driver passes the shared KB cache)
        must not be silently replaced by html.py/pdf.py's /tmp defaults —
        that made cross-run reuse impossible."""
        options = extract_content_queue.QueueOptions(
            paper_id_file="ids.txt", terms="t", output_dir="/tmp/x",
            html_cache_dir="/kb/.cache/html", pdf_cache_dir="/kb/.cache/pdfs",
        )
        derived = extract_content_queue.extraction_args("2402.10329", options)
        self.assertEqual(derived.html_cache_dir, "/kb/.cache/html")
        self.assertEqual(derived.pdf_cache_dir, "/kb/.cache/pdfs")

    def test_hard_timeout_keeps_the_extractor_stderr_tail(self) -> None:
        """A 600s timeout used to checkpoint a bare "hard timeout" string;
        the reason (gate cooldown, dead endpoint) died with the subprocess."""
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            options = self._opts(output_dir)

            def fake_run(command, capture_output, text, timeout, check):
                raise subprocess.TimeoutExpired(command, timeout, output=b"", stderr=b"gate 'arxiv' cooldown 90.0s exceeded 60.0s\n")

            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run), \
                 mock.patch("builtins.print"):
                result = extract_content_queue.extract_one("2110.10805", options, output_dir)
            self.assertFalse(result["evidence_eligible"])
            self.assertIn("hard timeout after", result["error"])
            self.assertIn("cooldown 90.0s", result["error"])


class HeldReasonTest(unittest.TestCase):
    """held_reason() compresses a HELD payload to one  · -joined line."""

    def test_channel_down_and_timeout_win(self) -> None:
        self.assertEqual(
            extract_content_queue.held_reason({"error": "channel down: skipped after consecutive connection failures"}),
            "channel-down",
        )
        self.assertEqual(
            extract_content_queue.held_reason({"error": "hard timeout after 600s: gate cooldown"}),
            "timeout 600s",
        )
        self.assertEqual(
            extract_content_queue.held_reason({"error": "hard timeout after"}, paper_timeout=300),
            "timeout 300s",
        )

    def test_queue_synthesized_error_is_copied(self) -> None:
        self.assertEqual(
            extract_content_queue.held_reason({"error": "extractor exit 2: boom"}),
            "error extractor exit 2: boom",
        )

    def test_unavailable_combines_manifest_and_fallback_attempts(self) -> None:
        data = {
            "available": False,
            "attempts": [
                {"method": "html-latexml", "available": False, "quality": "low"},
                {"method": "arxiv2md", "available": False, "quality": "low"},
                {"method": "pdf-text", "available": False, "quality": "low"},
            ],
        }
        self.assertEqual(
            extract_content_queue.held_reason(data, manifest_state="unavailable", manifest_status=404),
            "HTML 404 · tex unavailable · pdf unavailable",
        )
        self.assertEqual(
            extract_content_queue.held_reason(data, manifest_state="failed"),
            "HTML fetch failed · tex unavailable · pdf unavailable",
        )

    def test_low_quality_names_grade_chars_and_structure(self) -> None:
        data = {
            "available": True,
            "quality": {"grade": "low", "text_chars": 320, "structure": "flat"},
        }
        self.assertEqual(
            extract_content_queue.held_reason(data),
            "quality low text=320 structure=flat",
        )

    def test_reason_is_capped_at_120_chars(self) -> None:
        data = {"error": "x" * 300}
        self.assertLessEqual(len(extract_content_queue.held_reason(data)), 120)


class ManifestCacheOnlyTest(unittest.TestCase):
    """The download manifest (step 1) decides html_cache_only and channel-down
    short-circuits in extract_one."""

    def _opts(self, output_dir: Path, manifest: Path | None = None) -> "extract_content_queue.QueueOptions":
        return extract_content_queue.QueueOptions(
            paper_id_file="ids.txt", terms="t", output_dir=str(output_dir),
            download_manifest=str(manifest) if manifest else None,
        )

    def test_manifest_states_drive_html_cache_only_and_channel_down(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()
            manifest = tmp / "html-download.json"
            manifest.write_text(json.dumps({"results": [
                {"paper_id": "a", "state": "downloaded", "status": 200},
                {"paper_id": "b", "state": "unavailable", "status": 404},
                {"paper_id": "c", "state": "failed", "status": None, "error": "timeout"},
                {"paper_id": "d", "state": "channel-down", "status": None},
            ]}), encoding="utf-8")
            ids = tmp / "ids.txt"
            ids.write_text("a\nb\nc\nd\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_run(command, capture_output, text, timeout, check):
                commands.append(command)
                target = Path(command[command.index("--output") + 1])
                paper_id = command[command.index("--paper-id") + 1]
                target.write_text(json.dumps({
                    "paper_id": paper_id, "available": True, "evidence_eligible": True,
                }), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            options = extract_content_queue.QueueOptions(
                paper_id_file=str(ids), terms="t", output_dir=str(output_dir),
                download_manifest=str(manifest),
            )
            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run):
                summary = extract_content_queue.run_queue(options)
            by_id = {c[c.index("--paper-id") + 1]: c for c in commands}
            self.assertIn("--html-cache-only", by_id["a"])
            self.assertIn("--html-cache-only", by_id["b"])
            self.assertNotIn("--html-cache-only", by_id["c"], "failed gets one last network chance")
            self.assertNotIn("d", by_id, "channel-down must not spawn a subprocess")
            states = {item["paper_id"]: item["state"] for item in summary["results"]}
            self.assertEqual(states["d"], "channel-down")
            self.assertEqual(states["a"], "extracted")

    def test_missing_manifest_keeps_legacy_single_step(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()
            ids = tmp / "ids.txt"
            ids.write_text("a\n", encoding="utf-8")
            commands: list[list[str]] = []

            def fake_run(command, capture_output, text, timeout, check):
                commands.append(command)
                target = Path(command[command.index("--output") + 1])
                target.write_text(json.dumps({
                    "paper_id": "a", "available": True, "evidence_eligible": True,
                }), encoding="utf-8")
                return subprocess.CompletedProcess(command, 0, "", "")

            options = extract_content_queue.QueueOptions(
                paper_id_file=str(ids), terms="t", output_dir=str(output_dir),
                download_manifest=str(tmp / "nope.json"),
            )
            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run):
                extract_content_queue.run_queue(options)
            self.assertNotIn("--html-cache-only", commands[0])


class TierForwardingTest(unittest.TestCase):
    """TIER fallback lines from the extract-content subprocess reach the queue's
    stdout so the driver can show which path recovered the paper."""

    def test_tier_lines_on_stderr_are_forwarded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()

            def fake_run(command, capture_output, text, timeout, check):
                target = Path(command[command.index("--output") + 1])
                target.write_text(json.dumps({
                    "paper_id": "2110.10805", "available": True, "evidence_eligible": True,
                }), encoding="utf-8")
                return subprocess.CompletedProcess(
                    command, 0, "",
                    "TIER 2110.10805 html failed：HTML 404 → tex\n"
                    "TIER 2110.10805 tex ok（quality=medium，tex）\n",
                )

            import contextlib, io
            buf = io.StringIO()
            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run), \
                 contextlib.redirect_stdout(buf):
                extract_content_queue.extract_one("2110.10805", self._opts(output_dir), output_dir)
            text = buf.getvalue()
            self.assertIn("TIER 2110.10805 html failed：HTML 404 → tex", text)
            self.assertIn("TIER 2110.10805 tex ok（quality=medium，tex）", text)

    def _opts(self, output_dir: Path) -> "extract_content_queue.QueueOptions":
        return extract_content_queue.QueueOptions(
            paper_id_file="ids.txt", terms="t", output_dir=str(output_dir),
        )

    def test_held_stdout_line_carries_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            output_dir = tmp / "extractions"
            output_dir.mkdir()
            ids = tmp / "ids.txt"
            ids.write_text("2110.10805\n", encoding="utf-8")

            def fake_run(command, capture_output, text, timeout, check):
                target = Path(command[command.index("--output") + 1])
                target.write_text(json.dumps({
                    "paper_id": "2110.10805", "available": False, "evidence_eligible": False,
                    "error": "HTML unavailable",
                }), encoding="utf-8")
                return subprocess.CompletedProcess(command, 2, "", "")

            options = extract_content_queue.QueueOptions(
                paper_id_file=str(ids), terms="t", output_dir=str(output_dir),
            )
            import contextlib, io
            buf = io.StringIO()
            with mock.patch.object(extract_content_queue.subprocess, "run", side_effect=fake_run), \
                 contextlib.redirect_stdout(buf):
                summary = extract_content_queue.run_queue(options)
            text = buf.getvalue()
            held_lines = [line for line in text.splitlines() if line.startswith("HELD ")]
            self.assertEqual(len(held_lines), 1)
            self.assertRegex(held_lines[0], r"^HELD 2110\.10805 \(1/1\) \S")
            self.assertEqual(summary["results"][0]["held_reason"], "error HTML unavailable")


if __name__ == "__main__":
    unittest.main()

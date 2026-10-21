"""Usage/trace ledger (embodied_learning/harness/session_log.py + the
harness wiring): the embodied-learning side of
``monica/spec/usage-records-format.md``.

Contract under test:

- usage lines carry the four canonical counters and a timezone-aware
  timestamp (billing reads them);
- event lines carry ``level``/``kind``/``text``/``attrs`` (loglens reads them);
- ``message.id`` is the dedup key — the consumer keeps the largest
  ``output_tokens`` per id, so distinct invocations must not share one;
- the file sits directly under the conversation store (monica attributes by
  ``path.parent.name``; a dated subfolder would degrade the project name);
- recording never breaks a model call and the kill switch works;
- a caller-owned ledger stays open until the caller closes it.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

import embodied_learning.harness.claude as claude
from embodied_learning.harness.session_log import (
    CANONICAL_USAGE_KEYS,
    SessionLog,
    canonical_usage,
    iso_ts,
    usage_totals,
    write_event,
    write_metric,
    write_step,
    write_usage,
)


def _read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


class UsageFormatTest(unittest.TestCase):
    def test_usage_line_has_four_canonical_counters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "s.jsonl"
            with path.open("w", encoding="utf-8") as fh:
                write_usage(
                    fh, model="m", input_tokens=10, output_tokens=3,
                    cache_read=4, cache_write=5, msg_id="msg-1",
                )
            entry = _read_jsonl(path)[0]
            self.assertEqual(entry["type"], "assistant")
            self.assertEqual(entry["message"]["id"], "msg-1")
            self.assertEqual(entry["message"]["model"], "m")
            self.assertEqual(
                set(entry["message"]["usage"]), set(CANONICAL_USAGE_KEYS)
            )
            self.assertEqual(
                entry["message"]["usage"],
                {
                    "input_tokens": 10,
                    "output_tokens": 3,
                    "cache_read_input_tokens": 4,
                    "cache_creation_input_tokens": 5,
                },
            )

    def test_timestamp_is_timezone_aware(self) -> None:
        self.assertIsNotNone(datetime.fromisoformat(iso_ts()).tzinfo)
        naive = datetime(2026, 10, 19, 12, 0, 0)
        self.assertIsNotNone(datetime.fromisoformat(iso_ts(naive)).tzinfo)

    def test_canonical_usage_variants(self) -> None:
        self.assertEqual(
            canonical_usage({
                "input_tokens": 7, "output_tokens": 2,
                "cache_read_input_tokens": 1,
                "claude_cache_creation_5m_tokens": 3,
                "claude_cache_creation_1h_tokens": 4,
            }),
            {
                "input_tokens": 7, "output_tokens": 2,
                "cache_read_input_tokens": 1,
                "cache_creation_input_tokens": 7,
            },
        )
        # The canonical key wins; variants are not summed on top of it.
        self.assertEqual(
            canonical_usage({
                "cache_creation_input_tokens": 9,
                "claude_cache_creation_5m_tokens": 3,
            })["cache_creation_input_tokens"],
            9,
        )
        # Non-integer counters never count.
        self.assertEqual(canonical_usage({"input_tokens": True})["input_tokens"], 0)

    def test_usage_totals(self) -> None:
        self.assertEqual(
            usage_totals([
                {"usage": {"input_tokens": 2, "output_tokens": 1}},
                {"usage": {"input_tokens": 3, "output_tokens": 4,
                           "cache_read_input_tokens": 5}},
            ]),
            {"input_tokens": 5, "output_tokens": 5,
             "cache_read_input_tokens": 5, "cache_creation_input_tokens": 0},
        )


class EventFormatTest(unittest.TestCase):
    def test_event_text_is_clipped(self) -> None:
        """D9: diagnostics are capped so an agent's prose cannot leak into the
        ledger through an error message."""

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "s.jsonl"
            with path.open("w", encoding="utf-8") as fh:
                write_event(fh, level="error", kind="error", text="x" * 5000)
            entry = _read_jsonl(path)[0]
            self.assertEqual(len(entry["text"]), 300)

    def test_usage_rejects_non_integer_counters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "s.jsonl"
            with path.open("w", encoding="utf-8") as fh:
                write_usage(fh, model="m", input_tokens=True, output_tokens="9")
            usage = _read_jsonl(path)[0]["message"]["usage"]
            self.assertEqual(usage["input_tokens"], 0)
            self.assertEqual(usage["output_tokens"], 0)

    def test_event_lines_carry_loglens_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "s.jsonl"
            with path.open("w", encoding="utf-8") as fh:
                write_step(fh, stage="collect", command="search.py")
                write_metric(fh, stage="collect", duration_s=1.2345, returncode=0)
                write_event(fh, level="warn", kind="warn", text="slow",
                            stage="collect", duration_s=9)
            step, metric, warn = _read_jsonl(path)
            self.assertEqual(
                (step["type"], step["level"], step["kind"], step["text"]),
                ("system", "info", "step", "collect"),
            )
            self.assertEqual(step["attrs"]["stage"], "collect")
            self.assertEqual(metric["kind"], "metric")
            self.assertEqual(metric["attrs"]["duration_s"], 1.234)
            self.assertEqual(warn["level"], "warn")
            self.assertEqual(warn["text"], "slow")


class SessionLogTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def test_session_log_path_sits_directly_in_store(self) -> None:
        """monica attributes a session by ``path.parent.name``; a dated
        subfolder would make the project a date (misc bucket)."""

        with mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": str(self.root)}):
            path = claude.session_log_path("pipeline", "literature-review-demo")
        self.assertEqual(path.parent, self.root)
        self.assertTrue(path.name.startswith("usage-pipeline-"))
        self.assertIn("literature-review-demo", path.name)

    def test_inherited_ledger_path_is_shared(self) -> None:
        """A parent driver exports EMBODIED_AGENT_LEDGER so spawned stage
        scripts append to the run's one file instead of opening siblings."""

        shared = self.root / "run-ledger.jsonl"
        with mock.patch.dict(
            os.environ,
            {"EMBODIED_AGENT_LEDGER": str(shared),
             "EMBODIED_CONVERSATION_STORE": str(self.root / "store")},
        ):
            path = claude.session_log_path("one-shot", "selection-smart")
        self.assertEqual(path, shared)

    def test_kill_switch(self) -> None:
        with mock.patch.dict(os.environ, {"EMBODIED_AGENT_SESSION_LOG": "0"}):
            self.assertFalse(claude.session_ledger_enabled())
        with mock.patch.dict(os.environ, {"EMBODIED_AGENT_SESSION_LOG": "off"}):
            self.assertFalse(claude.session_ledger_enabled())
        with mock.patch.dict(os.environ, {"EMBODIED_AGENT_SESSION_LOG": "1"}):
            self.assertTrue(claude.session_ledger_enabled())

    def test_closed_property_and_context_manager(self) -> None:
        log = SessionLog(self.root / "s.jsonl")
        self.assertFalse(log.closed)
        log.close()
        self.assertTrue(log.closed)
        with SessionLog(self.root / "t.jsonl") as other:
            other.step("x")
        self.assertTrue(other.closed)

    def test_write_failure_never_raises(self) -> None:
        """Recording is a side channel: a dead mount must not break the call."""

        log = SessionLog(self.root / "s.jsonl")
        log.close()
        self.assertEqual(log.step("after-close"), {})
        log2 = SessionLog(self.root / "t.jsonl")
        self.addCleanup(log2.close)
        log2._fh.close()  # simulate a vanished handle under an open SessionLog
        self.assertEqual(log2.metric("x", 1.0), {})


class CompleteLedgerTest(unittest.TestCase):
    """``complete()`` owns a ledger when the caller passes none, and never
    closes a caller-owned one."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        env = mock.patch.dict(
            os.environ,
            {
                "EMBODIED_CONVERSATION_STORE": str(self.root),
                "EMBODIED_AGENT_SESSION_LOG": "1",
            },
        )
        env.start()
        self.addCleanup(env.stop)

    def _envelope(self) -> str:
        return json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "result": "PAYLOAD", "session_id": "sess-1", "num_turns": 2,
            "total_cost_usd": 0.02,
            "modelUsage": {
                "model-a": {
                    "inputTokens": 10, "outputTokens": 3,
                    "cacheReadInputTokens": 4, "cacheCreationInputTokens": 0,
                    "costUSD": 0.02,
                },
            },
        })

    def test_one_shot_writes_usage_and_metric(self) -> None:
        with mock.patch.object(
            claude.subprocess, "run",
            return_value=subprocess.CompletedProcess(["claude"], 0, self._envelope(), ""),
        ):
            result = claude.complete("p", timeout_s=5, cli="claude", label="agent-x")
        self.assertEqual(result.stdout, "PAYLOAD")
        ledgers = list(self.root.glob("usage-one-shot-*.jsonl"))
        self.assertEqual(len(ledgers), 1)
        entries = _read_jsonl(ledgers[0])
        usage = [e for e in entries if e.get("type") == "assistant"]
        self.assertEqual(len(usage), 1)
        self.assertEqual(usage[0]["message"]["model"], "model-a")
        self.assertEqual(usage[0]["message"]["usage"]["input_tokens"], 10)
        metric = [e for e in entries if e.get("kind") == "metric"]
        self.assertEqual(len(metric), 1)
        self.assertEqual(metric[0]["attrs"]["cost_usd"], 0.02)
        self.assertEqual(metric[0]["attrs"]["num_turns"], 2)

    def test_retries_use_distinct_message_ids(self) -> None:
        """A retried agent reuses its label; the usage dedup key must not, or
        two billed invocations collapse into one row."""

        def fake_run(command, **kwargs):
            envelope = json.loads(self._envelope())
            envelope["session_id"] = f"sess-{len(calls)}"
            calls.append(command)
            return subprocess.CompletedProcess(command, 0, json.dumps(envelope), "")

        calls: list = []
        with mock.patch.object(claude.subprocess, "run", side_effect=fake_run):
            claude.complete("p", timeout_s=5, cli="claude", label="same-label")
            claude.complete("p", timeout_s=5, cli="claude", label="same-label")
        ids = {
            e["message"]["id"]
            for path in self.root.glob("usage-one-shot-*.jsonl")
            for e in _read_jsonl(path)
            if e.get("type") == "assistant"
        }
        self.assertEqual(ids, {"sess-0:0", "sess-1:0"})

    def test_caller_owned_ledger_is_not_closed(self) -> None:
        log = SessionLog(self.root / "run.jsonl")
        self.addCleanup(log.close)
        with mock.patch.object(
            claude.subprocess, "run",
            return_value=subprocess.CompletedProcess(["claude"], 0, self._envelope(), ""),
        ):
            claude.complete("p", timeout_s=5, cli="claude", label="agent", ledger=log)
        self.assertFalse(log.closed)
        kinds = [e.get("kind") for e in _read_jsonl(self.root / "run.jsonl")]
        self.assertIn("step", kinds)
        self.assertIn("metric", kinds)

    def test_kill_switch_writes_no_ledger(self) -> None:
        with mock.patch.dict(os.environ, {"EMBODIED_AGENT_SESSION_LOG": "0"}), \
             mock.patch.object(
                 claude.subprocess, "run",
                 return_value=subprocess.CompletedProcess(
                     ["claude"], 0, self._envelope(), ""),
             ):
            claude.complete("p", timeout_s=5, cli="claude", label="agent")
        self.assertEqual(list(self.root.glob("usage-*.jsonl")), [])


class ChatTurnLedgerTest(unittest.TestCase):
    def test_turn_ledger_records_deduped_usage(self) -> None:
        """Streamed partial frames share one message.id; the ledger keeps the
        largest output count and emits a chat metric with the cost envelope."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stream = "\n".join(json.dumps(item) for item in [
                {"type": "system", "subtype": "init", "session_id": "s-1", "model": "m"},
                {"type": "assistant", "message": {
                    "id": "msg-1", "model": "m",
                    "usage": {"input_tokens": 5, "output_tokens": 0},
                    "content": [{"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}],
                }},
                {"type": "assistant", "message": {
                    "id": "msg-1", "model": "m",
                    "usage": {"input_tokens": 5, "output_tokens": 9},
                    "content": [{"type": "text", "text": "done"}],
                }},
                {"type": "result", "session_id": "s-1", "is_error": False,
                 "result": "done", "total_cost_usd": 0.03, "num_turns": 3},
            ]) + "\n"
            turn = claude.ChatTurn(
                cli="claude", prompt=stream, cwd=root, model="m", system_prompt="SYS",
            )

            def fake_popen(command, **kwargs):
                return real_popen(
                    ["/bin/cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, text=True,
                )

            real_popen = claude.subprocess.Popen  # capture before patching

            with mock.patch.dict(
                os.environ,
                {
                    "EMBODIED_CONVERSATION_STORE": str(root / "store"),
                    "EMBODIED_AGENT_SESSION_LOG": "1",
                },
            ), mock.patch.object(claude.subprocess, "Popen", side_effect=fake_popen):
                turn.start()
                list(turn.events())
            ledgers = list((root / "store").glob("usage-chat-*.jsonl"))
            self.assertEqual(len(ledgers), 1)
            entries = _read_jsonl(ledgers[0])
            usage = [e for e in entries if e.get("type") == "assistant"]
            self.assertEqual(len(usage), 1)
            self.assertEqual(usage[0]["message"]["usage"]["output_tokens"], 9)
            metric = [e for e in entries if e.get("kind") == "metric"]
            self.assertEqual(len(metric), 1)
            self.assertEqual(metric[0]["attrs"]["cost_usd"], 0.03)
            self.assertEqual(metric[0]["attrs"]["tool_calls"], {"Bash": 1})


if __name__ == "__main__":
    unittest.main()

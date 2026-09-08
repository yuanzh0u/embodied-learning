"""Tests for scripts/wiki_chat.py — the claude CLI chat bridge."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "wiki_chat.py"
SPEC = importlib.util.spec_from_file_location("wiki_chat", SCRIPT)
wiki_chat = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["wiki_chat"] = wiki_chat
SPEC.loader.exec_module(wiki_chat)


class BuildClaudeCommandTest(unittest.TestCase):
    def test_minimal_command(self):
        argv = wiki_chat.build_claude_command(cli="claude")
        self.assertEqual(
            argv,
            [
                "claude",
                "-p",
                "--output-format",
                "stream-json",
                "--verbose",
                "--permission-mode",
                "bypassPermissions",
                "--append-system-prompt",
                wiki_chat.CHAT_SYSTEM_PROMPT,
            ],
        )
        # The user prompt must never travel through argv.
        self.assertNotIn("prompt", argv[1:])

    def test_resume_model_and_allowed_tools(self):
        argv = wiki_chat.build_claude_command(
            cli="/usr/local/bin/claude",
            session_id="abc-123",
            model="haiku",
            permission_mode="plan",
            allowed_tools="Read,Write",
        )
        self.assertIn("--resume", argv)
        self.assertEqual(argv[argv.index("--resume") + 1], "abc-123")
        self.assertIn("--model", argv)
        self.assertEqual(argv[argv.index("--model") + 1], "haiku")
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "plan")
        self.assertIn("--allowedTools", argv)
        self.assertEqual(argv[argv.index("--allowedTools") + 1], "Read,Write")


class ParseStreamLineTest(unittest.TestCase):
    def test_init_event_becomes_session(self):
        line = json.dumps(
            {"type": "system", "subtype": "init", "session_id": "s-1", "model": "m"}
        )
        self.assertEqual(
            wiki_chat.parse_stream_line(line),
            [{"type": "session", "session_id": "s-1", "model": "m"}],
        )

    def test_assistant_blocks(self):
        line = json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "thinking", "thinking": "hmm"},
                        {"type": "text", "text": "你好"},
                        {"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "/x/y.md"}},
                    ]
                },
            }
        )
        events = wiki_chat.parse_stream_line(line)
        self.assertEqual(
            events,
            [
                {"type": "status", "stage": "thinking"},
                {"type": "delta", "text": "你好"},
                {"type": "status", "stage": "tool", "tool": "Read", "detail": "/x/y.md"},
            ],
        )

    def test_result_event(self):
        line = json.dumps(
            {
                "type": "result",
                "subtype": "success",
                "is_error": False,
                "result": "答案",
                "session_id": "s-2",
                "total_cost_usd": 0.05,
                "num_turns": 2,
            }
        )
        self.assertEqual(
            wiki_chat.parse_stream_line(line),
            [
                {
                    "type": "done",
                    "session_id": "s-2",
                    "is_error": False,
                    "result_text": "答案",
                    "cost_usd": 0.05,
                    "num_turns": 2,
                }
            ],
        )

    def test_garbage_is_ignored(self):
        self.assertEqual(wiki_chat.parse_stream_line(""), [])
        self.assertEqual(wiki_chat.parse_stream_line("not json"), [])
        self.assertEqual(wiki_chat.parse_stream_line("[1,2]"), [])
        self.assertEqual(wiki_chat.parse_stream_line(json.dumps({"type": "unknown"})), [])


class ResumeFailureTest(unittest.TestCase):
    def test_matches_known_wording(self):
        self.assertTrue(wiki_chat.is_resume_failure("No conversation found with session ID abc"))
        self.assertTrue(wiki_chat.is_resume_failure("error: Session not found"))

    def test_rejects_other_errors(self):
        self.assertFalse(wiki_chat.is_resume_failure("rate limit exceeded"))


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = wiki_chat.ChatSessionRegistry(Path(self.tmp.name) / "chat-sessions.json")

    def test_missing_file_starts_empty(self):
        self.assertIsNone(self.registry.get("topic-abc123"))
        self.assertEqual(self.registry.load(), {"version": 1, "topics": {}})

    def test_corrupt_file_recovers(self):
        self.registry.path.write_text("{not json", encoding="utf-8")
        self.assertIsNone(self.registry.get("topic-abc123"))
        # And it can still write afterwards.
        self.registry.record_session("topic-abc123", "s-9")
        self.assertEqual(self.registry.get("topic-abc123")["session_id"], "s-9")

    def test_roundtrip_and_reset(self):
        self.registry.record_session("topic-abc123", "s-1", model="m")
        self.registry.append_message("topic-abc123", "user", "问题")
        self.registry.append_message("topic-abc123", "assistant", "回答")
        entry = self.registry.get("topic-abc123")
        self.assertEqual(entry["session_id"], "s-1")
        self.assertEqual(entry["model"], "m")
        self.assertEqual([m["role"] for m in entry["messages"]], ["user", "assistant"])
        self.registry.reset("topic-abc123")
        self.assertIsNone(self.registry.get("topic-abc123"))

    def test_message_cap(self):
        for index in range(wiki_chat.MAX_HISTORY_MESSAGES + 10):
            self.registry.append_message("topic-cap", "user", f"m{index}")
        messages = self.registry.get("topic-cap")["messages"]
        self.assertEqual(len(messages), wiki_chat.MAX_HISTORY_MESSAGES)
        self.assertEqual(messages[-1]["text"], f"m{wiki_chat.MAX_HISTORY_MESSAGES + 9}")

    def test_empty_values_are_skipped(self):
        self.registry.record_session("topic-x", None)
        self.registry.append_message("topic-x", "user", "")
        entry = self.registry.get("topic-x")
        self.assertTrue(entry is None or entry["messages"] == [])


class BuildTurnPromptTest(unittest.TestCase):
    def test_paths_are_relative_and_message_is_last(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "evidence" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text("{}", encoding="utf-8")
            (run_dir / "evidence-appendix.md").write_text("x", encoding="utf-8")
            topic = {"id": "topic-abc123def456", "title": "演示话题"}
            prompt = wiki_chat.build_turn_prompt(
                topic=topic, run_dir=run_dir, kb_root=kb_root, message="帮我写综述"
            )
        self.assertIn("<topic_context>", prompt)
        self.assertIn("evidence/literature-review-demo-20260101", prompt)
        self.assertNotIn(str(kb_root), prompt)
        self.assertIn("topic-abc123def456", prompt)
        self.assertTrue(prompt.rstrip().endswith("帮我写综述"))


class FakeCliTurnTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)
        self.fake_cli = self.tmp_path / "fake-claude"
        self.fake_cli.write_text(
            "#!/bin/sh\n"
            'cat >/dev/null\n'
            'printf \'%s\\n\' \'{"type":"system","subtype":"init","session_id":"fx-1","model":"fake"}\'\n'
            'printf \'%s\\n\' \'{"type":"assistant","message":{"content":[{"type":"text","text":"你好"}]}}\'\n'
            'printf \'%s\\n\' \'{"type":"result","subtype":"success","is_error":false,"result":"你好","session_id":"fx-1","total_cost_usd":0.01,"num_turns":1}\'\n',
            encoding="utf-8",
        )
        self.fake_cli.chmod(0o755)

    def test_turn_streams_expected_events(self):
        turn = wiki_chat.ChatTurn(
            cli=str(self.fake_cli), prompt="hi", cwd=self.tmp_path, timeout_s=30
        )
        turn.start()
        events = list(turn.events())
        kinds = [event["type"] for event in events]
        self.assertEqual(kinds, ["session", "delta", "done"])
        self.assertEqual(events[0]["session_id"], "fx-1")
        self.assertEqual(events[1]["text"], "你好")

    def test_peek_event_then_events_streams_all(self):
        turn = wiki_chat.ChatTurn(
            cli=str(self.fake_cli), prompt="hi", cwd=self.tmp_path, timeout_s=30
        )
        turn.start()
        first = turn.peek_event()
        assert first is not None
        self.assertEqual(first["type"], "session")
        events = list(turn.events())
        self.assertEqual([event["type"] for event in events], ["session", "delta", "done"])

    def test_nonzero_exit_yields_error(self):
        failing = self.tmp_path / "failing-claude"
        failing.write_text(
            "#!/bin/sh\ncat >/dev/null\necho 'No conversation found with session ID x' >&2\nexit 1\n",
            encoding="utf-8",
        )
        failing.chmod(0o755)
        turn = wiki_chat.ChatTurn(
            cli=str(failing),
            prompt="hi",
            cwd=self.tmp_path,
            session_id="stale",
            timeout_s=30,
        )
        turn.start()
        events = list(turn.events())
        self.assertEqual(events[-1]["type"], "error")
        self.assertTrue(events[-1]["resume_failed"])

    def test_stop_terminates_process(self):
        script = self.tmp_path / "slow-claude"
        script.write_text(
            "#!/bin/sh\ncat >/dev/null\nsleep 30\n",
            encoding="utf-8",
        )
        script.chmod(0o755)
        turn = wiki_chat.ChatTurn(
            cli=str(script), prompt="hi", cwd=self.tmp_path, timeout_s=60
        )
        turn.start()
        turn.stop()
        events = list(turn.events())
        self.assertEqual(events[-1]["type"], "done")
        self.assertTrue(events[-1].get("stopped"))
        assert turn._process is not None
        self.assertIsNotNone(turn._process.poll())


class ResolveCliTest(unittest.TestCase):
    def test_explicit_path_wins_when_it_exists(self):
        cli = wiki_chat.resolve_cli("/usr/local/bin/claude") if Path("/usr/local/bin/claude").is_file() else None
        if cli is None:
            self.skipTest("no /usr/local/bin/claude on this machine")
        self.assertEqual(cli, "/usr/local/bin/claude")

    def test_falls_back_when_explicit_path_missing(self):
        # A missing explicit path falls through to PATH / the standard
        # install location — the desktop-launcher scenario.
        cli = wiki_chat.resolve_cli("/nonexistent/claude-binary")
        self.assertTrue(Path(cli).exists())

    def test_some_cli_is_resolvable(self):
        try:
            cli = wiki_chat.resolve_cli(None)
        except wiki_chat.ChatUnavailableError:
            self.skipTest("no claude binary on this machine")
        self.assertTrue(Path(cli).exists())


if __name__ == "__main__":
    unittest.main()

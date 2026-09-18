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
        self.assertIn("--permission-mode", argv)
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "plan")
        self.assertIn("--allowedTools", argv)
        self.assertEqual(argv[argv.index("--allowedTools") + 1], "Read,Write")

    def test_effort_flag_forwarded_when_set(self):
        argv = wiki_chat.build_claude_command(cli="claude", effort="low")
        self.assertIn("--effort", argv)
        self.assertEqual(argv[argv.index("--effort") + 1], "low")
        # Omitted effort must not leak a bare flag.
        self.assertNotIn("--effort",
                         wiki_chat.build_claude_command(cli="claude"))


class ParseStreamLineTest(unittest.TestCase):

    def test_init_event_becomes_session(self):
        line = json.dumps({
            "type": "system",
            "subtype": "init",
            "session_id": "s-1",
            "model": "m"
        })
        self.assertEqual(
            wiki_chat.parse_stream_line(line),
            [{
                "type": "session",
                "session_id": "s-1",
                "model": "m"
            }],
        )

    def test_assistant_blocks(self):
        line = json.dumps({
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "thinking",
                        "thinking": "hmm"
                    },
                    {
                        "type": "text",
                        "text": "你好"
                    },
                    {
                        "type": "tool_use",
                        "id": "t1",
                        "name": "Read",
                        "input": {
                            "file_path": "/x/y.md"
                        }
                    },
                ]
            },
        })
        events = wiki_chat.parse_stream_line(line)
        self.assertEqual(
            events,
            [
                {
                    "type": "status",
                    "stage": "thinking"
                },
                {
                    "type": "delta",
                    "text": "你好"
                },
                {
                    "type": "status",
                    "stage": "tool",
                    "tool": "Read",
                    "detail": "/x/y.md"
                },
            ],
        )

    def test_result_event(self):
        line = json.dumps({
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "result": "答案",
            "session_id": "s-2",
            "total_cost_usd": 0.05,
            "num_turns": 2,
        })
        self.assertEqual(
            wiki_chat.parse_stream_line(line),
            [{
                "type": "done",
                "session_id": "s-2",
                "is_error": False,
                "result_text": "答案",
                "cost_usd": 0.05,
                "num_turns": 2,
            }],
        )

    def test_garbage_is_ignored(self):
        self.assertEqual(wiki_chat.parse_stream_line(""), [])
        self.assertEqual(wiki_chat.parse_stream_line("not json"), [])
        self.assertEqual(wiki_chat.parse_stream_line("[1,2]"), [])
        self.assertEqual(
            wiki_chat.parse_stream_line(json.dumps({"type": "unknown"})), [])


class ResumeFailureTest(unittest.TestCase):

    def test_matches_known_wording(self):
        self.assertTrue(
            wiki_chat.is_resume_failure(
                "No conversation found with session ID abc"))
        self.assertTrue(
            wiki_chat.is_resume_failure("error: Session not found"))

    def test_rejects_other_errors(self):
        self.assertFalse(wiki_chat.is_resume_failure("rate limit exceeded"))


class RegistryTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = wiki_chat.ChatSessionRegistry(
            Path(self.tmp.name) / "chat-sessions.json")

    def test_missing_file_starts_empty(self):
        self.assertIsNone(self.registry.get("topic-abc123"))
        self.assertIsNone(self.registry.get_workspace("ws-abc123"))
        self.assertEqual(self.registry.load(), {
            "version": 1,
            "topics": {},
            "workspaces": {}
        })

    def test_corrupt_file_recovers(self):
        self.registry.path.write_text("{not json", encoding="utf-8")
        self.assertIsNone(self.registry.get("topic-abc123"))
        # And it can still write afterwards.
        self.registry.record_session("topic-abc123", "s-9")
        self.assertEqual(
            self.registry.get("topic-abc123")["session_id"], "s-9")

    def test_roundtrip_and_reset(self):
        self.registry.record_session("topic-abc123", "s-1", model="m")
        self.registry.append_message("topic-abc123", "user", "问题")
        self.registry.append_message("topic-abc123", "assistant", "回答")
        entry = self.registry.get("topic-abc123")
        self.assertEqual(entry["session_id"], "s-1")
        self.assertEqual(entry["model"], "m")
        self.assertEqual([m["role"] for m in entry["messages"]],
                         ["user", "assistant"])
        self.registry.reset("topic-abc123")
        self.assertIsNone(self.registry.get("topic-abc123"))

    def test_message_cap(self):
        for index in range(wiki_chat.MAX_HISTORY_MESSAGES + 10):
            self.registry.append_message("topic-cap", "user", f"m{index}")
        messages = self.registry.get("topic-cap")["messages"]
        self.assertEqual(len(messages), wiki_chat.MAX_HISTORY_MESSAGES)
        self.assertEqual(messages[-1]["text"],
                         f"m{wiki_chat.MAX_HISTORY_MESSAGES + 9}")

    def test_empty_values_are_skipped(self):
        self.registry.record_session("topic-x", None)
        self.registry.append_message("topic-x", "user", "")
        entry = self.registry.get("topic-x")
        self.assertTrue(entry is None or entry["messages"] == [])


class WorkspaceRegistryTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = wiki_chat.ChatSessionRegistry(
            Path(self.tmp.name) / "chat-sessions.json")

    def test_workspace_roundtrip(self):
        self.registry.record_session("ws-abc123", "s-7", model="m")
        self.registry.append_message("ws-abc123", "user", "综述高斯溅射SLAM")
        self.registry.set_workflow_state("ws-abc123",
                                         stage="packet",
                                         awaiting_input=True)
        self.registry.set_workflow_state("ws-abc123", awaiting_input=False)
        self.registry.link_topic("ws-abc123", "topic-def456")
        entry = self.registry.get_workspace("ws-abc123")
        self.assertEqual(entry["session_id"], "s-7")
        self.assertEqual(entry["model"], "m")
        self.assertEqual(entry["messages"][0]["text"], "综述高斯溅射SLAM")
        self.assertEqual(entry["workflow"]["stage"], "packet")
        self.assertFalse(entry["workflow"]["awaiting_input"])
        self.assertEqual(entry["topic_id"], "topic-def456")

    def test_workspace_and_topic_namespaces_are_separate(self):
        # ws- keys route to "workspaces", topic- keys to "topics" — sharing a
        # store must not leak one into the other's view.
        self.registry.record_session("ws-abc123", "s-ws")
        self.registry.record_session("topic-abc123", "s-topic")
        self.assertIsNone(self.registry.get("ws-abc123"))
        self.assertIsNone(self.registry.get_workspace("topic-abc123"))
        self.assertEqual(
            self.registry.get("topic-abc123")["session_id"], "s-topic")
        self.assertEqual(
            self.registry.get_workspace("ws-abc123")["session_id"], "s-ws")

    def test_workspace_reset(self):
        self.registry.record_session("ws-abc123", "s-1")
        self.registry.reset("ws-abc123")
        self.assertIsNone(self.registry.get_workspace("ws-abc123"))
        self.registry.reset("ws-nonexistent")  # no-op, must not raise

    def test_workspace_message_cap(self):
        for index in range(wiki_chat.MAX_HISTORY_MESSAGES + 5):
            self.registry.append_message("ws-cap", "user", f"m{index}")
        messages = self.registry.get_workspace("ws-cap")["messages"]
        self.assertEqual(len(messages), wiki_chat.MAX_HISTORY_MESSAGES)


class StageMarkerTest(unittest.TestCase):

    def test_extracts_markers_in_order(self):
        text = ("先看一下。\n[STAGE:plan] 生成查询计划\n"
                "[STAGE:retrieval] 第 1 轮检索完成\n结束。")
        self.assertEqual(
            wiki_chat.extract_stage_markers(text),
            [("plan", "生成查询计划"), ("retrieval", "第 1 轮检索完成")],
        )

    def test_ignores_non_markers_and_unknown_stages(self):
        self.assertEqual(
            wiki_chat.extract_stage_markers("普通文本 [STAGE:plan] 行中"), [])
        self.assertEqual(
            wiki_chat.extract_stage_markers("[STAGE:custom_stage] 自定义"),
            [("custom_stage", "自定义")],
        )

    def test_topic_marker(self):
        self.assertEqual(
            wiki_chat.extract_topic_marker(
                "落盘完成\n[TOPIC:evidence/literature-review-x-20260908]"),
            "evidence/literature-review-x-20260908",
        )
        self.assertIsNone(wiki_chat.extract_topic_marker("没有标记"))
        self.assertIsNone(wiki_chat.extract_topic_marker("[TOPIC:partial"))


class BuildWorkflowPromptTest(unittest.TestCase):

    def test_params_and_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-demo-20260908"
            run_dir.mkdir(parents=True)
            prompt = wiki_chat.build_workflow_prompt(
                params={
                    "topic": "高斯溅射 SLAM",
                    "review_mode": "scoping",
                    "time_range": "2026-03-08..2026-09-08",
                    "target_style": "all",
                    "focus": "鲁棒性",
                },
                run_dir=run_dir,
                kb_root=kb_root,
                pipeline_root=Path("/repo"),
            )
        self.assertIn("<workflow_request>", prompt)
        self.assertIn("综述主题：高斯溅射 SLAM", prompt)
        self.assertIn("综述模式：scoping", prompt)
        self.assertIn("2026-03-08..2026-09-08", prompt)
        self.assertIn("关注重点：鲁棒性", prompt)
        self.assertIn("work/literature-review-demo-20260908", prompt)
        self.assertNotIn(str(kb_root), prompt)

    def test_no_outline_checkpoint_in_workflow_prompt(self):
        """The workflow runs packet → settle in one turn; the outline
        stop-and-wait checkpoint is gone. Only insufficient-evidence stops."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-x"
            run_dir.mkdir(parents=True)
            prompt = wiki_chat.build_workflow_prompt(
                params={"topic": "x"},
                run_dir=run_dir,
                kb_root=kb_root,
                pipeline_root=Path("/repo"),
            )
        self.assertNotIn("立即停止本轮回复", prompt)
        self.assertNotIn("等待用户确认", prompt)
        self.assertIn("一气呵成", prompt)
        self.assertIn("检索失败或文献不足", prompt)

    def test_workflow_prompt_requires_publish_steps(self):
        """Settle includes catalog registration + wiki rebuild, not just
        copying into evidence/."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-x"
            run_dir.mkdir(parents=True)
            prompt = wiki_chat.build_workflow_prompt(
                params={"topic": "x"},
                run_dir=run_dir,
                kb_root=kb_root,
                pipeline_root=Path("/repo"),
            )
        self.assertIn("literature-review-catalog.md", prompt)
        self.assertIn("build_research_wiki.py", prompt)

    def test_continuation_prompt_carries_feedback(self):
        prompt = wiki_chat.build_continuation_prompt(feedback="补充一下评测部分", stage="packet")
        self.assertIn("补充一下评测部分", prompt)
        self.assertIn("[STAGE:writing]", prompt)
        no_feedback = wiki_chat.build_continuation_prompt(feedback="  ", stage="packet")
        self.assertIn("无，按现有证据继续", no_feedback)

    def test_continuation_prompt_mid_pipeline_runs_through_settle(self):
        """A run parked mid-pipeline (e.g. mining was interrupted) resumes its
        current stage and continues through settle in the same turn — no
        outline checkpoint to stop at."""
        prompt = wiki_chat.build_continuation_prompt(stage="mining")
        self.assertIn("从磁盘已有进度继续当前阶段", prompt)
        self.assertIn("[STAGE:writing]", prompt)
        self.assertNotIn("等待用户确认", prompt)
        self.assertIn("literature-review-catalog.md", prompt)

    def test_continuation_prompt_honors_target_style(self):
        single = wiki_chat.build_continuation_prompt(target_style="scientific-memo", stage="packet")
        self.assertIn("仅撰写采访中选定的风格", single)
        self.assertIn("scientific-memo_keyan.md", single)
        self.assertIn("style 与 scope_note", single)
        self.assertNotIn("3 个并行 subagent", single)
        zhihu = wiki_chat.build_continuation_prompt(target_style="expert-explainer", stage="packet")
        self.assertIn("zhihu-explainer_zhihu.md", zhihu)
        full = wiki_chat.build_continuation_prompt(target_style="all", stage="packet")
        self.assertIn("三种成稿", full)


class WorkflowDriverContractTest(unittest.TestCase):
    """The workflow prompt assumes the driver ran the mechanical stages and
    pushes per-paper subagent deep reading."""

    def test_workflow_prompt_defers_mechanical_stages_to_driver(self):
        prompt = wiki_chat.WORKFLOW_SYSTEM_PROMPT
        self.assertIn("run_review_pipeline.py", prompt)
        self.assertIn("pipeline-summary.json", prompt)
        self.assertIn("不要手动执行任何检索/抽取/筛选/深读/投影命令", prompt)
        self.assertIn("search.py search-arxiv", prompt)  # named among banned commands
        self.assertIn("search.py search-semantic-scholar", prompt)

    def test_workflow_prompt_parallel_deep_reading_contract(self):
        prompt = wiki_chat.WORKFLOW_SYSTEM_PROMPT
        # Deep reading now runs inside the driver; the agent must not redo it.
        self.assertIn("论文深读（速记骨架+审计）与证据投影已由驱动脚本", prompt)
        self.assertIn("不要派发深读 subagent", prompt)
        self.assertIn("不要跑 note_tools.py project-evidence-events", prompt)
        # Outline/writing remain the agent's judgment work.
        self.assertIn("build_review_packet.py", prompt)
        self.assertIn("check_run_bundle.py", prompt)

    def test_substitute_prompt_roots_fills_pool(self):
        text = wiki_chat.substitute_prompt_roots(
            "s=<skills-root> sc=<scripts-root> p=<pool-root>",
            skills_root=Path("/r/skills"), scripts_root=Path("/r/scripts"),
            pool_root=Path("/kb/pool"),
        )
        self.assertEqual(text, "s=/r/skills sc=/r/scripts p=/kb/pool")
        # Absent pool keeps the placeholder literal.
        kept = wiki_chat.substitute_prompt_roots(
            "p=<pool-root>", skills_root=Path("/r/skills"), scripts_root=Path("/r/scripts")
        )
        self.assertEqual(kept, "p=<pool-root>")

    def test_kickoff_prompt_references_driver_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            prompt = wiki_chat.build_workflow_prompt(
                params={"topic": "demo", "review_mode": "rapid",
                        "time_range": "2023-01-01..2026-09-09",
                        "target_style": "scientific-memo", "focus": ""},
                run_dir=run_dir, kb_root=kb_root,
                pipeline_root=kb_root / "skills",
            )
            self.assertIn("pipeline-summary.json", prompt)
            self.assertIn("不要重跑任何检索/抽取/筛选/深读/投影命令", prompt)
            self.assertIn("build_review_packet.py", prompt)

    def test_extract_driver_stage_maps_to_workflow_stages(self):
        self.assertEqual(
            wiki_chat.extract_driver_stage("[DRIVER-STAGE:retrieval-arxiv] ok ran"),
            ("retrieval", "ok ran"),
        )
        self.assertEqual(
            wiki_chat.extract_driver_stage("[DRIVER-STAGE:packets] ok 50/50"),
            ("mining", "ok 50/50"),
        )
        self.assertIsNone(wiki_chat.extract_driver_stage("[STAGE:plan] claude line"))
        self.assertIsNone(wiki_chat.extract_driver_stage("plain text"))


class SystemPromptOverrideTest(unittest.TestCase):

    def test_default_is_chat_prompt(self):
        argv = wiki_chat.build_claude_command(cli="claude")
        self.assertEqual(argv[argv.index("--append-system-prompt") + 1],
                         wiki_chat.CHAT_SYSTEM_PROMPT)

    def test_workflow_overrides_system_prompt(self):
        argv = wiki_chat.build_claude_command(
            cli="claude", system_prompt=wiki_chat.WORKFLOW_SYSTEM_PROMPT)
        self.assertEqual(argv[argv.index("--append-system-prompt") + 1],
                         wiki_chat.WORKFLOW_SYSTEM_PROMPT)

    def test_chat_config_new_turn_forwards_override_and_timeout(self):
        config = wiki_chat.ChatConfig(cli="claude", timeout_s=900)
        turn = config.new_turn(
            prompt="p",
            cwd=Path("."),
            system_prompt=wiki_chat.WORKFLOW_SYSTEM_PROMPT,
            timeout_s=5400,
        )
        self.assertEqual(turn.system_prompt, wiki_chat.WORKFLOW_SYSTEM_PROMPT)
        self.assertEqual(turn.timeout_s, 5400)
        default_turn = config.new_turn(prompt="p", cwd=Path("."))
        self.assertEqual(default_turn.system_prompt,
                         wiki_chat.CHAT_SYSTEM_PROMPT)
        self.assertEqual(default_turn.timeout_s, 900)


class BuildTurnPromptTest(unittest.TestCase):

    def test_paths_are_relative_and_message_is_last(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "evidence" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text("{}", encoding="utf-8")
            (run_dir / "evidence-appendix.md").write_text("x",
                                                          encoding="utf-8")
            topic = {"id": "topic-abc123def456", "title": "演示话题"}
            prompt = wiki_chat.build_turn_prompt(topic=topic,
                                                 run_dir=run_dir,
                                                 kb_root=kb_root,
                                                 message="帮我写综述")
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
        turn = wiki_chat.ChatTurn(cli=str(self.fake_cli),
                                  prompt="hi",
                                  cwd=self.tmp_path,
                                  timeout_s=30)
        turn.start()
        events = list(turn.events())
        kinds = [event["type"] for event in events]
        self.assertEqual(kinds, ["session", "delta", "done"])
        self.assertEqual(events[0]["session_id"], "fx-1")
        self.assertEqual(events[1]["text"], "你好")

    def test_peek_event_then_events_streams_all(self):
        turn = wiki_chat.ChatTurn(cli=str(self.fake_cli),
                                  prompt="hi",
                                  cwd=self.tmp_path,
                                  timeout_s=30)
        turn.start()
        first = turn.peek_event()
        assert first is not None
        self.assertEqual(first["type"], "session")
        events = list(turn.events())
        self.assertEqual([event["type"] for event in events],
                         ["session", "delta", "done"])

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
        turn = wiki_chat.ChatTurn(cli=str(script),
                                  prompt="hi",
                                  cwd=self.tmp_path,
                                  timeout_s=60)
        turn.start()
        turn.stop()
        events = list(turn.events())
        self.assertEqual(events[-1]["type"], "done")
        self.assertTrue(events[-1].get("stopped"))
        assert turn._process is not None
        self.assertIsNotNone(turn._process.poll())


class ResolveCliTest(unittest.TestCase):

    def test_explicit_path_wins_when_it_exists(self):
        cli = wiki_chat.resolve_cli("/usr/local/bin/claude") if Path(
            "/usr/local/bin/claude").is_file() else None
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

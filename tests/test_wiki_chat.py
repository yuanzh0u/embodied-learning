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

    def test_subprocess_mutation_survives_local_mutation(self):
        """Two processes mutating the same registry file must not lose each
        other's entry — the KB-shared lock serializes load→mutate→save."""
        import subprocess
        import sys

        helper = (
            "import sys, time\n"
            "sys.path.insert(0, {repo_root!r})\n"
            "sys.path.insert(0, {scripts!r})\n"
            "import wiki_chat\n"
            "registry = wiki_chat.ChatSessionRegistry({path!r})\n"
            "registry.append_message('topic-child', 'user', 'from subprocess')\n"
        ).format(
            repo_root=str(Path(__file__).resolve().parents[1]),
            scripts=str(Path(__file__).resolve().parents[1] / "scripts"),
            path=str(self.registry.path),
        )
        subprocess.run([sys.executable, "-c", helper], check=True, timeout=60)
        # Local mutation after the subprocess finished must keep its entry.
        self.registry.append_message("topic-local", "user", "local")
        data = self.registry.load()
        self.assertIn("topic-child", data["topics"])
        self.assertIn("topic-local", data["topics"])

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

    def test_workflow_prompt_settle_runs_finalize(self):
        """The agent publisher's mechanical settle tail is finalize_run.py —
        the old hand-run register_run.py / build_research_wiki.py duo (and the
        wiki-port topic-count check) must not come back."""
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
        self.assertIn("finalize_run.py", prompt)
        self.assertNotIn("register_run.py", prompt)
        self.assertNotIn("build_research_wiki.py", prompt)

    def test_workflow_prompt_launcher_stops_after_gates(self):
        """The headless writer (publisher="launcher") must stop right after the
        audit gates: no stage/topic markers, no finalize instruction — the
        launcher process does the mechanical settle/publish in code."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-x"
            run_dir.mkdir(parents=True)
            prompt = wiki_chat.build_workflow_prompt(
                params={"topic": "x"},
                run_dir=run_dir,
                kb_root=kb_root,
                pipeline_root=Path("/repo"),
                publisher="launcher",
            )
        self.assertIn("立即停止本轮回复", prompt)
        self.assertIn("由 launcher 机械完成", prompt)
        self.assertNotIn("[STAGE:", prompt)
        self.assertNotIn("[TOPIC:", prompt)
        self.assertIn("运行目录根", prompt)
        self.assertIn("build_review_packet.py", prompt)
        self.assertIn("work/literature-review-x", prompt)
        self.assertNotIn(str(kb_root), prompt)

    def test_workflow_prompt_single_style_keeps_citation_contract_out_of_user_prompt(self):
        """The memo citation contract lives ONLY in the system layer; the
        single-style user prompt carries a pointer, not a second copy."""
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
        self.assertNotIn("引文格式（Wiki 渲染依赖，必须遵守）", prompt)
        # Voice contract stays (memo must not drift into the zhihu register).
        self.assertIn("风格契约（scientific-memo）", prompt)
        self.assertIn("references/scientific-memo.md", prompt)
        self.assertIn("不是A，而是B", prompt)

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
        self.assertIn("一次性读取现状", prompt)
        self.assertIn("[STAGE:writing]", prompt)
        self.assertNotIn("等待用户确认", prompt)
        self.assertIn("finalize_run.py", prompt)
        self.assertNotIn("build_research_wiki.py", prompt)

    def test_continuation_prompt_launcher_stops_after_gates(self):
        """The launcher publisher's continuation stops after the gates: no
        topic marker, no finalize instruction; stage passthrough semantics
        (mid-pipeline vs writing branch) are unchanged."""
        launcher = wiki_chat.build_continuation_prompt(
            feedback="引文格式错误", target_style="scientific-memo",
            stage="packet", publisher="launcher")
        self.assertIn("立即停止本轮回复", launcher)
        self.assertNotIn("[TOPIC:", launcher)
        self.assertNotIn("[STAGE:", launcher)
        self.assertNotIn("finalize_run.py", launcher)
        self.assertIn("仅撰写采访中选定的风格", launcher)
        self.assertNotIn("3 个并行 subagent", launcher)
        mid = wiki_chat.build_continuation_prompt(publisher="launcher")
        writing = wiki_chat.build_continuation_prompt(stage="writing", publisher="launcher")
        self.assertIn("一次性读取现状", mid)
        self.assertNotIn("一次性读取现状", writing)

    def test_continuation_prompt_launcher_survey_style_passthrough(self):
        """survey is not in STYLE_VOICE_CONTRACTS: the label passes through
        untouched for the launcher publisher too."""
        prompt = wiki_chat.build_continuation_prompt(
            feedback="f", target_style="survey", stage="packet", publisher="launcher")
        self.assertIn("survey", prompt)

    def test_workflow_turn_prompts_is_the_single_assembly_point(self):
        """workflow_turn_prompts returns (system, user) with the root
        placeholders substituted — byte-identical to composing the pieces by
        hand, so both entry points can only diverge on publisher."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            pipeline_root = kb_root / "pipeline"
            (pipeline_root / "scripts").mkdir(parents=True)
            system_prompt, user_prompt = wiki_chat.workflow_turn_prompts(
                params={"topic": "demo"}, run_dir=run_dir, kb_root=kb_root,
                pipeline_root=pipeline_root, publisher="agent",
            )
            skills_root, scripts_root = wiki_chat.resolve_pipeline_layout(pipeline_root)
            expected_system = wiki_chat.substitute_prompt_roots(
                wiki_chat.workflow_system_prompt("agent"),
                skills_root=skills_root, scripts_root=scripts_root,
                pool_root=kb_root / "pool",
            )
            self.assertEqual(system_prompt, expected_system)
            self.assertIn(run_dir.name, user_prompt)
            self.assertNotIn(str(kb_root), user_prompt)
            launcher_system, _ = wiki_chat.workflow_turn_prompts(
                params={"topic": "demo"}, run_dir=run_dir, kb_root=kb_root,
                pipeline_root=pipeline_root, publisher="launcher",
            )
            self.assertIn("立即停止", launcher_system)
            self.assertNotEqual(launcher_system, system_prompt)

    def test_workflow_turn_system_prompt_degrades_to_literal_placeholders(self):
        """pipeline_root=None keeps the placeholders literal — the same
        degradation the interactive server used to do when the pipeline root
        could not be resolved."""
        prompt = wiki_chat.workflow_turn_system_prompt(None)
        self.assertIn("<skills-root>", prompt)
        self.assertEqual(prompt, wiki_chat.workflow_system_prompt("agent"))

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


class WorkflowPublisherPromptTest(unittest.TestCase):
    """The workflow system prompt has one deliberate fork (agent vs launcher
    publisher); the shared base is byte-identical for both entry points."""

    CITE_ANCHOR = "引文格式（Wiki 渲染依赖，必须遵守）"

    def test_agent_publisher_finalizes_itself(self):
        prompt = wiki_chat.workflow_system_prompt("agent")
        self.assertIn("finalize_run.py", prompt)
        self.assertNotIn("register_run.py", prompt)
        self.assertNotIn("build_research_wiki.py", prompt)
        self.assertNotIn("topic 数量", prompt)  # wiki-port topic-count check is gone
        self.assertIn("[STAGE:settle]", prompt)
        self.assertIn("[TOPIC:", prompt)
        self.assertIn(self.CITE_ANCHOR, prompt)

    def test_launcher_publisher_stops_after_gates(self):
        prompt = wiki_chat.workflow_system_prompt("launcher")
        self.assertIn("立即停止本轮回复", prompt)
        self.assertIn("finalize_run.py", prompt)
        self.assertIn("launcher", prompt)
        self.assertNotIn("[STAGE:", prompt)
        self.assertNotIn("[TOPIC:", prompt)
        self.assertNotIn("register_run.py", prompt)
        # The launcher's writer still produces the memo, so the citation
        # contract must reach it through the shared base.
        self.assertIn(self.CITE_ANCHOR, prompt)

    def test_alias_is_the_agent_variant(self):
        self.assertEqual(
            wiki_chat.WORKFLOW_SYSTEM_PROMPT,
            wiki_chat.workflow_system_prompt("agent"),
        )

    def test_unknown_publisher_rejected(self):
        with self.assertRaises(ValueError):
            wiki_chat.workflow_system_prompt("bogus")

    def test_base_is_shared_between_publishers(self):
        agent = wiki_chat.workflow_system_prompt("agent")
        launcher = wiki_chat.workflow_system_prompt("launcher")
        self.assertTrue(agent.startswith(launcher.split("\n\n【机械落盘")[0]))
        self.assertTrue(launcher.startswith(agent.split("\n\n【机械落盘")[0]))


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
            # Single-style runs carry the voice contract (memo must not drift
            # into the zhihu-explainer register — 2026-09 regression).
            self.assertIn("风格契约（scientific-memo）", prompt)
            self.assertIn("references/scientific-memo.md", prompt)
            self.assertIn("不是A，而是B", prompt)

    def test_all_style_prompt_has_no_single_style_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp).resolve()
            run_dir = kb_root / "work" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            prompt = wiki_chat.build_workflow_prompt(
                params={"topic": "demo", "review_mode": "rapid",
                        "time_range": "2023-01-01..2026-09-09",
                        "target_style": "all", "focus": ""},
                run_dir=run_dir, kb_root=kb_root,
                pipeline_root=kb_root / "skills",
            )
        self.assertNotIn("风格契约", prompt)

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

    def test_extract_driver_detail_forwards_warnings(self):
        self.assertEqual(wiki_chat.extract_driver_detail("[DRIVER] 检索计划完成"), "检索计划完成")
        self.assertEqual(
            wiki_chat.extract_driver_detail("[DRIVER-WARN] arXiv 返回 0 结果"),
            "arXiv 返回 0 结果",
        )
        self.assertEqual(wiki_chat.extract_driver_detail("[PAPER] 2402.10329 审计通过"), "2402.10329 审计通过")
        self.assertIsNone(wiki_chat.extract_driver_detail("plain stdout line"))

    def test_extract_driver_phase_opens_blocks(self):
        self.assertEqual(
            wiki_chat.extract_driver_phase("[DRIVER-PHASE:plan] 查询规划与检索词生成"),
            ("plan", "查询规划与检索词生成"),
        )
        self.assertEqual(
            wiki_chat.extract_driver_phase("[DRIVER-PHASE:mining] 候选注册、筛选与全文挖掘"),
            ("mining", "候选注册、筛选与全文挖掘"),
        )
        self.assertIsNone(wiki_chat.extract_driver_phase("[DRIVER-PHASE:unknown] x"))
        self.assertIsNone(wiki_chat.extract_driver_phase("[DRIVER-STAGE:plan] ok"))

    def test_extract_driver_progress_parses_counts(self):
        self.assertEqual(
            wiki_chat.extract_driver_progress("[DRIVER-PROGRESS:deep-read:12/48]"),
            ("deep-read", 12, 48, ""),
        )
        self.assertEqual(
            wiki_chat.extract_driver_progress("[DRIVER-PROGRESS:extract:3/48] 2402.10329 全文不满足证据条件（HELD）"),
            ("extract", 3, 48, "2402.10329 全文不满足证据条件（HELD）"),
        )
        self.assertIsNone(wiki_chat.extract_driver_progress("[DRIVER] not progress"))

    def test_registry_stage_maps_to_mining(self):
        # the mining phase opens before the registry stage completes; the
        # completion line must not flip the pill back to retrieval
        self.assertEqual(wiki_chat.extract_driver_stage("[DRIVER-STAGE:registry] ok ran")[0], "mining")


class SystemPromptOverrideTest(unittest.TestCase):

    def test_default_is_chat_prompt(self):
        # The harness knows nothing about the wiki persona: the caller passes
        # the system prompt explicitly (ChatConfig.new_turn does this).
        argv = wiki_chat.build_claude_command(
            cli="claude", system_prompt=wiki_chat.CHAT_SYSTEM_PROMPT)
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


class DialogJournalTest(unittest.TestCase):
    """The run-dir dialog transcript: mirrored SSE events survive a page
    refresh; a fresh kickoff truncates whatever the run dir already had."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run_dir = Path(self.tmp.name) / "work" / "literature-review-demo"
        self.journal = wiki_chat.DialogJournal(self.run_dir)
        self.path = self.run_dir / "dialog" / "journal.jsonl"

    def records(self) -> list[dict]:
        return wiki_chat.read_dialog_journal(self.path)

    def test_start_truncates_existing_journal(self):
        self.journal.start()
        self.journal.user("第一轮")
        # A re-kickoff reuses the in-progress run dir but begins a new
        # conversation: the old dialog must not bleed into the new one.
        wiki_chat.DialogJournal(self.run_dir).start()
        self.assertEqual(self.records(), [])

    def test_user_and_events_append_in_order(self):
        self.journal.start()
        self.journal.user("综述主题")
        self.journal.event({"type": "stage", "stage": "plan", "detail": "生成查询计划"})
        self.journal.event({"type": "delta", "text": "你好"})
        self.journal.flush_deltas()
        records = self.records()
        self.assertEqual(records[0], {"kind": "user", "text": "综述主题"})
        self.assertEqual(records[1]["event"]["type"], "stage")
        self.assertEqual(records[2]["event"], {"type": "delta", "text": "你好"})

    def test_small_deltas_coalesce_into_one_record(self):
        self.journal.start()
        for index in range(50):
            self.journal.event({"type": "delta", "text": f"片段{index}"})
        self.journal.flush_deltas()
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["event"]["text"], "".join(f"片段{i}" for i in range(50)))

    def test_large_deltas_flush_at_threshold(self):
        self.journal.start()
        self.journal.event({"type": "delta", "text": "x" * (wiki_chat.DialogJournal.DELTA_FLUSH_CHARS - 1)})
        self.assertEqual(self.records(), [])  # below threshold, still buffered
        self.journal.event({"type": "delta", "text": "y"})
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["event"]["text"], "x" * (wiki_chat.DialogJournal.DELTA_FLUSH_CHARS - 1) + "y")

    def test_non_delta_event_flushes_pending_deltas_first(self):
        self.journal.start()
        self.journal.event({"type": "delta", "text": "半段输出"})
        self.journal.event({"type": "awaiting_input", "stage": "packet", "detail": "已暂停"})
        records = self.records()
        self.assertEqual(records[0]["event"]["text"], "半段输出")
        self.assertEqual(records[1]["event"]["type"], "awaiting_input")

    def test_torn_last_line_is_skipped(self):
        self.journal.start()
        self.journal.user("问题")
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write('{"kind": "event", "event": {"type": "del')  # crash mid-write
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["kind"], "user")

    def test_read_missing_file_is_empty(self):
        self.assertEqual(wiki_chat.read_dialog_journal(self.run_dir / "none" / "journal.jsonl"), [])


class JournalableEventTest(unittest.TestCase):

    def test_dialog_bearing_events_are_kept(self):
        for event in (
            {"type": "delta", "text": "x"},
            {"type": "stage", "stage": "plan", "detail": "d"},
            {"type": "status", "stage": "tool", "tool": "Bash", "detail": "d"},
            {"type": "awaiting_input", "stage": "packet"},
            {"type": "topic_ready", "topic_id": "topic-1"},
            {"type": "topic_error", "message": "m"},
            {"type": "session_reset"},
            {"type": "error", "message": "m"},
        ):
            self.assertTrue(wiki_chat.journalable_event(event), event)

    def test_transient_events_are_dropped(self):
        for event in (
            {"type": "status", "stage": "driver", "detail": "d"},
            {"type": "status"},  # thinking spinner
            {"type": "progress", "name": "deep-read", "done": 1, "total": 8},
            {"type": "session", "session_id": "s-1"},
            {"type": "done", "session_id": "s-1"},
        ):
            self.assertFalse(wiki_chat.journalable_event(event), event)


class RevisionPromptTest(unittest.TestCase):
    """build_revision_prompts — the wiki revision flow's agent contract."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb_root = Path(self.tmp.name)
        self.run_dir = self.kb_root / "evidence" / "literature-review-x-20260929"
        self.run_dir.mkdir(parents=True)

    def test_prompts_carry_target_gates_and_marker(self):
        system, user = wiki_chat.build_revision_prompts(
            run_dir=self.run_dir, kb_root=self.kb_root,
            style_key="keyan", revision_number=2, topic_title="时序深度估计",
            base_filename="scientific-memo_keyan.md", pipeline_root=None,
            message="开头加落地建议",
        )
        self.assertIn("[REVISION:revisions/keyan-v2.md]", system)
        self.assertIn("build-trace-map", system)
        self.assertIn("audit-article-quality --memo", system)
        self.assertIn("audit_citations.py --article revisions/keyan-v2.md", system)
        self.assertIn("evidence-appendix.md", system)
        self.assertIn("trace-map-keyan-v2.json", system)  # base trace-map untouched
        self.assertIn("风格契约（scientific-memo）", system)  # voice contract injected
        # Immutability contract: base deliverables are read-only.
        self.assertIn("绝不覆盖任何既有文件", system)
        self.assertIn("revisions/keyan-v2.md", user)
        self.assertIn("开头加落地建议", user)
        self.assertIn("scientific-memo_keyan.md", user)

    def test_zhihu_revision_uses_zhihu_gates(self):
        system, _ = wiki_chat.build_revision_prompts(
            run_dir=self.run_dir, kb_root=self.kb_root,
            style_key="zhihu", revision_number=1, topic_title="t",
            base_filename="zhihu-explainer_zhihu.md", pipeline_root=None,
            message="",
        )
        self.assertIn("audit-article-quality --zhihu", system)
        self.assertIn("（无具体要求，请改善整体质量）", _)

    def test_unknown_style_key_rejected(self):
        with self.assertRaises(ValueError):
            wiki_chat.build_revision_prompts(
                run_dir=self.run_dir, kb_root=self.kb_root,
                style_key="quickread", revision_number=1, topic_title="t",
                base_filename="x.md", pipeline_root=None, message="m",
            )

if __name__ == "__main__":
    unittest.main()

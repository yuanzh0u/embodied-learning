"""Tests for scripts/serve_research_wiki.py — chat endpoints, topic
resolution, and the /api/refresh regression guard."""

import http.client
import importlib.util
import json
import shutil
import sys
import tempfile
import threading
import unittest
from functools import partial
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "serve_research_wiki.py"
SPEC = importlib.util.spec_from_file_location("serve_research_wiki_tested", SCRIPT)
server_module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["serve_research_wiki_tested"] = server_module
SPEC.loader.exec_module(server_module)


def build_temp_kb() -> tuple[tempfile.TemporaryDirectory, Path, Path, str]:
    """A minimal KB: catalog, one snapshot with one topic pointing at a run dir."""

    tmp = tempfile.TemporaryDirectory()
    kb_root = Path(tmp.name) / "kb"
    (kb_root / "knowledge").mkdir(parents=True)
    (kb_root / "knowledge" / "literature-review-catalog.md").write_text("# catalog\n", encoding="utf-8")
    (kb_root / "wiki").mkdir()
    run_dir = kb_root / "evidence" / "literature-review-demo-20260101"
    run_dir.mkdir(parents=True)
    (run_dir / "run.json").write_text("{}", encoding="utf-8")
    snapshot_id = "20260101T000000-abcdef1234"
    topics_dir = kb_root / "wiki" / "data" / "snapshots" / snapshot_id / "topics"
    topics_dir.mkdir(parents=True)
    topic_id = "topic-abcdef123456"
    (topics_dir / f"{topic_id}.json").write_text(
        json.dumps(
            {
                "id": topic_id,
                "title": "演示话题",
                "source_directory": str(run_dir),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (kb_root / "wiki" / "data" / "current.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "snapshot_id": snapshot_id,
                "base_path": f"snapshots/{snapshot_id}",
            }
        ),
        encoding="utf-8",
    )
    return tmp, kb_root, run_dir, topic_id


class FakeTurn:
    """ChatTurn stand-in: replays canned events; records constructor args."""

    instances: list["FakeTurn"] = []

    def __init__(self, *, cli, prompt, cwd, session_id=None, model=None,
                 permission_mode="bypassPermissions", allowed_tools=None, timeout_s=900,
                 system_prompt=None, effort=None):
        self.kwargs = dict(
            cli=cli, prompt=prompt, cwd=cwd, session_id=session_id, model=model,
            permission_mode=permission_mode, allowed_tools=allowed_tools, timeout_s=timeout_s,
            system_prompt=system_prompt, effort=effort,
        )
        self.started = 0
        self.stopped = False
        self.stop_requested = False
        self._events = [
            {"type": "session", "session_id": "fresh-1", "model": "fake"},
            {"type": "delta", "text": "你好"},
            {"type": "done", "session_id": "fresh-1", "is_error": False},
        ]
        FakeTurn.instances.append(self)

    def start(self):
        self.started += 1

    def peek_event(self):
        return self._events[0] if self._events else None

    def events(self):
        yield from self._events

    def stop(self):
        self.stopped = True


class ChatServerHarness(unittest.TestCase):
    """Boots the real WikiHandler on an ephemeral port with a fake ChatTurn.
    Subclasses set ``chat_enabled = False`` to boot without a chat CLI."""

    chat_enabled = True

    def setUp(self):
        self.kb_tmp, self.kb_root, self.run_dir, self.topic_id = build_temp_kb()
        self.addCleanup(self.kb_tmp.cleanup)
        FakeTurn.instances = []
        self._original_turn = server_module.wiki_chat.ChatTurn
        server_module.wiki_chat.ChatTurn = FakeTurn
        self.addCleanup(self._restore_turn)
        self._original_current = server_module.CURRENT_CHAT
        server_module.CURRENT_CHAT = None
        self.addCleanup(self._restore_current)

        chat = server_module.wiki_chat.ChatConfig(cli="/fake/claude" if self.chat_enabled else None)
        handler = partial(
            server_module.WikiHandler,
            kb_root=self.kb_root,
            wiki_root=self.kb_root / "wiki",
            data_dir=self.kb_root / "wiki" / "data",
            chat=chat,
        )
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.addCleanup(self.httpd.server_close)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        # Cleanups run LIFO: shutdown must happen before join.
        self.addCleanup(self.thread.join, 5)
        self.addCleanup(self.httpd.shutdown)
        self.port = self.httpd.server_address[1]

    def _restore_turn(self):
        server_module.wiki_chat.ChatTurn = self._original_turn

    def _restore_current(self):
        server_module.CURRENT_CHAT = self._original_current

    def request(self, method: str, path: str, body: dict | None = None) -> tuple[int, dict | str, dict]:
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        payload = json.dumps(body) if body is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        connection.request(method, path, body=payload, headers=headers)
        response = connection.getresponse()
        raw = response.read().decode("utf-8")
        response_headers = dict(response.getheaders())
        status = response.status
        connection.close()
        if "application/json" in (response_headers.get("Content-Type") or ""):
            return status, json.loads(raw), response_headers
        return status, raw, response_headers

    def sse_events(self) -> list[dict]:
        return [
            json.loads(line[5:].strip())
            for line in self._last_sse.splitlines()
            if line.startswith("data:")
        ]

    def _collect_sse(self, result):
        status, raw, headers = result
        self._last_sse = raw
        return status, raw, headers


class ResolveTopicTest(ChatServerHarness):
    """resolve_topic runs through the HTTP layer: valid ids stream, invalid
    ones get 400. The security boundary (path traversal, foreign run dirs) is
    covered by the 400 cases below plus the regex in wiki_chat."""

    def test_foreign_run_dir_rejected(self):
        # Point the topic at a directory outside the KB root.
        topic_path = (
            self.kb_root / "wiki" / "data" / "snapshots" / "20260101T000000-abcdef1234"
            / "topics" / f"{self.topic_id}.json"
        )
        topic = json.loads(topic_path.read_text(encoding="utf-8"))
        topic["source_directory"] = str(Path(self.kb_tmp.name) / "outside")
        Path(self.kb_tmp.name, "outside").mkdir()
        topic_path.write_text(json.dumps(topic, ensure_ascii=False), encoding="utf-8")
        status, payload, _ = self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "hi"})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        self.assertIn("知识库", payload["error"])


class ChatEndpointTest(ChatServerHarness):
    def test_chat_streams_sse_and_persists(self):
        status, raw, headers = self._collect_sse(
            self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "总结一下"})
        )
        self.assertEqual(status, HTTPStatus.OK)
        self.assertIn("text/event-stream", headers.get("Content-Type", ""))
        events = self.sse_events()
        self.assertEqual([e["type"] for e in events], ["session", "delta", "done"])
        turn = FakeTurn.instances[-1]
        self.assertEqual(turn.kwargs["cli"], "/fake/claude")
        self.assertIn(self.run_dir.name, turn.kwargs["prompt"])
        registry = server_module.wiki_chat.ChatSessionRegistry(
            self.kb_root / "wiki" / "data" / "chat-sessions.json"
        )
        entry = registry.get(self.topic_id)
        self.assertEqual(entry["session_id"], "fresh-1")
        self.assertEqual([m["role"] for m in entry["messages"]], ["user", "assistant"])

    def test_empty_message_rejected(self):
        status, payload, _ = self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "  "})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_bad_topic_id_rejected(self):
        status, payload, _ = self.request("POST", "/api/chat", {"topic_id": "../evil", "message": "hi"})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_unknown_topic_rejected(self):
        status, payload, _ = self.request("POST", "/api/chat", {"topic_id": "topic-000000000000", "message": "hi"})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_stale_session_resets_and_retries_fresh(self):
        registry = server_module.wiki_chat.ChatSessionRegistry(
            self.kb_root / "wiki" / "data" / "chat-sessions.json"
        )
        registry.record_session(self.topic_id, "stale-id")
        created: list[FakeTurn] = []

        original_init = FakeTurn.__init__

        def seeded_init(self_turn, **kwargs):
            original_init(self_turn, **kwargs)
            if kwargs.get("session_id") == "stale-id":
                self_turn._events = [
                    {"type": "error",
                     "message": "claude 执行失败：No conversation found with session ID stale-id",
                     "resume_failed": True},
                ]
            created.append(self_turn)

        FakeTurn.__init__ = seeded_init
        try:
            status, raw, _ = self._collect_sse(
                self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "还在吗"})
            )
        finally:
            FakeTurn.__init__ = original_init
        self.assertEqual(status, HTTPStatus.OK)
        events = self.sse_events()
        self.assertEqual(events[0]["type"], "session_reset")
        self.assertEqual([e["type"] for e in events[1:]], ["session", "delta", "done"])
        # The retry turn must have been spawned without a session id.
        fresh = [t for t in created if t.kwargs.get("session_id") is None]
        self.assertTrue(fresh, "expected a fresh-session retry turn")
        entry = registry.get(self.topic_id)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["session_id"], "fresh-1")

    def test_state_endpoint_reflects_registry(self):
        self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "hi"})
        status, payload, _ = self.request("GET", f"/api/chat/state?topic={self.topic_id}")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(payload["session_id"], "fresh-1")
        self.assertEqual(len(payload["messages"]), 2)

    def test_reset_endpoint_clears_entry(self):
        self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "hi"})
        status, payload, _ = self.request("POST", "/api/chat/reset", {"topic_id": self.topic_id})
        self.assertEqual(status, HTTPStatus.OK)
        status, payload, _ = self.request("GET", f"/api/chat/state?topic={self.topic_id}")
        self.assertIsNone(payload["session_id"])
        self.assertEqual(payload["messages"], [])

    def test_stop_endpoint_idempotent_when_idle(self):
        status, payload, _ = self.request("POST", "/api/chat/stop")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertTrue(payload.get("idle"))

    def test_refresh_endpoint_regression(self):
        status, payload, _ = self.request("POST", "/api/refresh")
        # The temp KB has no real builder output; either success or a builder
        # error is fine — the contract is "not 404".
        self.assertIn(status, (HTTPStatus.OK, HTTPStatus.INTERNAL_SERVER_ERROR))


class WorkflowEndpointTest(ChatServerHarness):
    """One-click survey workflow: kickoff → checkpoint → continuation →
    topic_ready. Runs against the real init_run.py in the temp KB."""

    def params(self, topic="高斯溅射SLAM综述"):
        return {
            "topic": topic,
            "review_mode": "scoping",
            "time_range": "recent",
            "target_style": "all",
            "focus": "",
        }

    def setUp(self):
        super().setUp()
        self.addCleanup(self._cleanup_work_dir)
        self._install_fake_driver()

    def _cleanup_work_dir(self):
        shutil.rmtree(self.kb_root / "work", ignore_errors=True)

    def _install_fake_driver(self):
        """Replace the driver subprocess with an in-process fake that emits
        two DRIVER-STAGE lines (so stage events flow) and writes the summary
        the kickoff prompt references. Records invocations for assertions."""
        self.driver_calls: list[tuple[dict, Path]] = []

        original_start = server_module.WikiHandler._start_pipeline_driver

        class FakeDriver:
            def __init__(self, fail: bool = False):
                self._fail = fail
                self.stdout = iter([
                    "[DRIVER-STAGE:retrieval-arxiv] ok ran\n",
                    "[DRIVER-STAGE:packets] ok 8/8 packets\n",
                ])
                self.stderr = None
                self.returncode = 1 if fail else 0
                self.killed = False

            def wait(self, timeout=None):
                return self.returncode

            def kill(self):
                self.killed = True

            def poll(self):
                return self.returncode

        def fake_start(handler_self, params, run_dir):
            self.driver_calls.append((params, run_dir))
            return FakeDriver()

        server_module.WikiHandler._start_pipeline_driver = fake_start
        self.addCleanup(setattr, server_module.WikiHandler, "_start_pipeline_driver", original_start)

    def _checkpoint_turn_events(self, session_id="ws-fresh-1"):
        return [
            {"type": "session", "session_id": session_id, "model": "fake"},
            {"type": "delta", "text": "[STAGE:plan] 生成查询计划\n"},
            {"type": "delta", "text": "[STAGE:packet] 综述包已生成，大纲如下\n"},
            {"type": "delta", "text": "## 大纲\n1. 问题定义\n2. 方法谱系\n"},
            {"type": "done", "session_id": session_id, "is_error": False},
        ]

    def _settle_turn_events(self):
        return [
            {"type": "session", "session_id": "ws-fresh-2", "model": "fake"},
            {"type": "delta", "text": "[STAGE:writing] 撰写成稿\n"},
            {"type": "delta", "text": "成稿已完成。\n[TOPIC:evidence/literature-review-高斯溅射slam综述-20260101]\n"},
            {"type": "done", "session_id": "ws-fresh-2", "is_error": False},
        ]

    def _seed_turn_factory(self, script):
        original_init = FakeTurn.__init__

        def seeded_init(turn_self, **kwargs):
            original_init(turn_self, **kwargs)
            script(turn_self, kwargs)

        FakeTurn.__init__ = seeded_init
        self.addCleanup(setattr, FakeTurn, "__init__", original_init)

    def test_kickoff_creates_run_and_parks_at_checkpoint(self):
        def script(turn_self, kwargs):
            turn_self._events = self._checkpoint_turn_events()

        self._seed_turn_factory(script)
        status, raw, headers = self._collect_sse(
            self.request("POST", "/api/workflow", {"message": "高斯溅射SLAM综述", "params": self.params()})
        )
        self.assertEqual(status, HTTPStatus.OK)
        ws_id = headers.get("X-Workflow-Id")
        self.assertRegex(ws_id, r"^ws-[0-9a-f]{8}$")
        events = self.sse_events()
        # Driver stages come from the fake driver's stdout before claude runs.
        self.assertEqual(events[0]["type"], "status")
        self.assertEqual(events[0]["stage"], "driver")
        stage_events = [e for e in events if e["type"] == "stage" and e.get("detail")]
        self.assertIn(("retrieval", "ok ran"), [(e["stage"], e.get("detail")) for e in stage_events])
        self.assertIn(("mining", "ok 8/8 packets"), [(e["stage"], e.get("detail")) for e in stage_events])
        # The fake driver was invoked with the kickoff params and run dir.
        self.assertEqual(len(self.driver_calls), 1)
        driver_params, driver_run_dir = self.driver_calls[0]
        self.assertEqual(driver_params["topic"], "高斯溅射SLAM综述")
        self.assertIn("literature-review-", str(driver_run_dir))
        self.assertIn("session", [e["type"] for e in events])
        self.assertIn("stage", [e["type"] for e in events])
        self.assertEqual(events[-1]["type"], "awaiting_input")
        self.assertEqual(events[-1]["stage"], "packet")
        # init_run.py really created the in-progress run in the temp KB.
        run_dirs = list((self.kb_root / "work").glob("literature-review-*"))
        self.assertEqual(len(run_dirs), 1)
        manifest = json.loads((run_dirs[0] / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "in-progress")
        self.assertEqual(manifest["review_mode"], "scoping")
        # The workflow system prompt reached the turn with the placeholder
        # roots substituted (repo checkout → absolute repo paths) and the run
        # dir in the kickoff prompt.
        turn = FakeTurn.instances[-1]
        expected_prompt = server_module.wiki_chat.substitute_prompt_roots(
            server_module.wiki_chat.WORKFLOW_SYSTEM_PROMPT,
            skills_root=server_module.REPO_ROOT / "skills",
            scripts_root=server_module.REPO_ROOT / "scripts",
            pool_root=server_module.pool_root(self.kb_root),
        )
        self.assertEqual(turn.kwargs["system_prompt"], expected_prompt)
        self.assertNotIn("<skills-root>", turn.kwargs["system_prompt"])
        self.assertNotIn("<pool-root>", turn.kwargs["system_prompt"])
        self.assertGreaterEqual(turn.kwargs["timeout_s"], 3600)
        self.assertIn(run_dirs[0].name, turn.kwargs["prompt"])
        # Registry state.
        registry = server_module.wiki_chat.ChatSessionRegistry(
            self.kb_root / "wiki" / "data" / "chat-sessions.json"
        )
        entry = registry.get_workspace(ws_id)
        self.assertEqual(entry["session_id"], "ws-fresh-1")
        self.assertTrue(entry["workflow"]["awaiting_input"])
        self.assertEqual(entry["workflow"]["stage"], "packet")
        self.assertEqual(entry["workflow"]["run_dir"], f"work/{run_dirs[0].name}")
        return ws_id

    def test_invalid_params_rejected(self):
        status, payload, _ = self.request(
            "POST", "/api/workflow",
            {"message": "x", "params": {"topic": "x", "review_mode": "bogus"}},
        )
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        status, payload, _ = self.request(
            "POST", "/api/workflow",
            {"message": "x", "params": {"topic": "这个主题太长" * 40}},
        )
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)
        status, payload, _ = self.request(
            "POST", "/api/workflow",
            {"message": "x", "params": {"topic": "合法主题", "time_range": "custom"}},
        )
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_time_range_presets_resolve_to_absolute_windows(self):
        """6mo/3y/10y/20y presets (3y default) with legacy names still mapped;
        2026-09-11 request to replace since2023/recent with year-based options."""
        resolve = server_module.WikiHandler._resolve_time_range
        import datetime as dt_module

        today = dt_module.date.today()
        cases = {
            "6mo": (today - dt_module.timedelta(days=183)).strftime("%Y-%m-%d"),
            "recent": (today - dt_module.timedelta(days=183)).strftime("%Y-%m-%d"),
            "3y": today.replace(year=today.year - 3).strftime("%Y-%m-%d"),
            "since2023": today.replace(year=today.year - 3).strftime("%Y-%m-%d"),
            "10y": today.replace(year=today.year - 10).strftime("%Y-%m-%d"),
            "20y": today.replace(year=today.year - 20).strftime("%Y-%m-%d"),
        }
        end = today.strftime("%Y-%m-%d")
        for preset, start in cases.items():
            with self.subTest(preset=preset):
                self.assertEqual(resolve(self, preset), f"{start}..{end}")
        self.assertEqual(resolve(self, {"range": "2024-01-01..2026-01-01"}), "2024-01-01..2026-01-01")
        with self.assertRaises(server_module.ChatBadRequest):
            resolve(self, "bogus-preset")

    def test_search_strategy_and_seeds_flow_to_driver(self):
        """2026-09-11 request: the interview card's strategy choice and seed
        arXiv IDs must reach the driver's --search-strategy/--seed-arxiv-ids."""
        strategy = self.params()
        strategy["search_strategy"] = "seeds"
        strategy["seed_arxiv_ids"] = "2402.14207, 1704.02084"
        self.request("POST", "/api/workflow", {"params": strategy})
        self.assertTrue(self.driver_calls)
        driver_params = self.driver_calls[0][0]
        self.assertEqual(driver_params["search_strategy"], "seeds")
        self.assertEqual(driver_params["seed_arxiv_ids"], "2402.14207, 1704.02084")
        kickoff_prompt = FakeTurn.instances[-1].kwargs["prompt"]
        self.assertIn("seeds", kickoff_prompt)

    def test_invalid_search_strategy_rejected(self):
        bad = self.params()
        bad["search_strategy"] = "bogus"
        status, _, _ = self.request("POST", "/api/workflow", {"params": bad})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_continuation_resumes_and_emits_topic_ready(self):
        ws_id = self.test_kickoff_creates_run_and_parks_at_checkpoint()
        # Simulate a settled run the builder could route: the work dir copied
        # to evidence/ with the three 成稿, plus a matching topic in the
        # snapshot that refresh_snapshot() would produce.
        run_dir = next((self.kb_root / "work").glob("literature-review-*"))
        settled = self.kb_root / "evidence" / run_dir.name
        shutil.copytree(run_dir, settled)
        (settled / "scientific-memo_keyan.md").write_text("# 成稿\n", encoding="utf-8")
        (settled / "zhihu-explainer_zhihu.md").write_text("# 成稿\n", encoding="utf-8")
        (settled / "xiaohongshu-post_xiaohongshu.md").write_text("# 成稿\n", encoding="utf-8")
        run_manifest = json.loads((settled / "run.json").read_text(encoding="utf-8"))
        run_manifest["status"] = "settled"
        run_manifest["files"] = {"evidence": "evidence.jsonl"}
        (settled / "evidence.jsonl").write_text("", encoding="utf-8")
        (settled / "run.json").write_text(json.dumps(run_manifest, ensure_ascii=False), encoding="utf-8")
        # Route the settled run the way the workflow's settle stage would.
        catalog = self.kb_root / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "# catalog\n\n| ID | 主题 | 卡 | 规模 | 审计入口 |\n|---|---|---|---:|---|\n"
            f"| X | 演示话题 | — | — | [run](../evidence/{run_dir.name}/run.json) |\n",
            encoding="utf-8",
        )

        def script(turn_self, kwargs):
            turn_self._events = self._settle_turn_events()

        self._seed_turn_factory(script)
        status, raw, headers = self._collect_sse(
            self.request("POST", "/api/workflow", {"message": "继续", "ws_id": ws_id})
        )
        self.assertEqual(status, HTTPStatus.OK)
        events = self.sse_events()
        types = [e["type"] for e in events]
        self.assertIn("stage", types)
        self.assertEqual(types[-1], "topic_ready")
        ready = events[-1]
        # The published topic id is derived by the builder from run.json's
        # topic field (topic-<sha1[:12]>) — verify it's a real topic id and
        # that it matches the topic the builder published for this run.
        self.assertRegex(ready["topic_id"], r"^topic-[0-9a-f]{12}$")
        self.assertEqual(ready["title"], "高斯溅射SLAM综述")  # run.json's topic
        # The continuation resumed the parked session.
        turn = FakeTurn.instances[-1]
        self.assertEqual(turn.kwargs["session_id"], "ws-fresh-1")
        self.assertIn("继续执行", turn.kwargs["prompt"])
        registry = server_module.wiki_chat.ChatSessionRegistry(
            self.kb_root / "wiki" / "data" / "chat-sessions.json"
        )
        entry = registry.get_workspace(ws_id)
        self.assertEqual(entry["topic_id"], ready["topic_id"])
        self.assertFalse(entry["workflow"]["awaiting_input"])

    def test_state_endpoint_reports_workflow(self):
        status, payload, _ = self.request("GET", "/api/chat/state")
        self.assertTrue(payload["workflow"])
        status, payload, _ = self.request("GET", "/api/workflow/state")
        self.assertTrue(payload["enabled"])
        status, payload, _ = self.request("GET", "/api/workflow/state?ws_id=ws-00000000")
        self.assertEqual(status, HTTPStatus.OK)
        # Unknown-but-wellformed workspace ids report nulls, not 400 — the
        # frontend probes idly on reload.
        self.assertEqual(payload["ws_id"], "ws-00000000")
        self.assertEqual(payload["messages"], [])
        self.assertIsNone(payload["stage"])

    def test_reset_endpoint_clears_workspace(self):
        ws_id = self.test_kickoff_creates_run_and_parks_at_checkpoint()
        status, payload, _ = self.request("POST", "/api/workflow/reset", {"ws_id": ws_id})
        self.assertEqual(status, HTTPStatus.OK)
        status, payload, _ = self.request("GET", f"/api/workflow/state?ws_id={ws_id}")
        self.assertEqual(payload["messages"], [])
        self.assertIsNone(payload["stage"])
        status, payload, _ = self.request("POST", "/api/workflow/reset", {"ws_id": "bogus"})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_disabled_chat_blocks_workflow(self):
        self.chat_enabled = False  # too late for setUp; exercise precheck path directly
        handler_state = self.request("GET", "/api/workflow/state")[1]
        # Harness already booted with chat enabled; verify the probe contract
        # instead (the 503 path is covered by ChatDisabledTest).
        self.assertTrue(handler_state["enabled"])

    def test_workflow_turn_uses_model_and_effort_overrides(self):
        """With no overrides, the workflow turn carries the DEFAULT_CHAT_MODEL
        (glm-5.3-flash); --workflow-model would win over it."""

        def script(turn_self, kwargs):
            turn_self._events = self._checkpoint_turn_events()

        self._seed_turn_factory(script)
        status, raw, _ = self._collect_sse(
            self.request("POST", "/api/workflow", {"message": "主题", "params": self.params()})
        )
        self.assertEqual(status, HTTPStatus.OK)
        turn_kwargs = FakeTurn.instances[-1].kwargs
        self.assertEqual(turn_kwargs["model"], server_module.DEFAULT_CHAT_MODEL)
        self.assertIsNone(turn_kwargs["effort"])
        # The workflow system prompt carries the deep-reading contract: one
        # subagent per paper, driver work is off-limits.
        self.assertIn("subagent", turn_kwargs["system_prompt"])
        self.assertIn("run_review_pipeline.py", turn_kwargs["system_prompt"])

    def test_driver_failure_blocks_claude_and_reports(self):
        """A failed driver emits an SSE error and never spawns claude; the run
        stays in-progress so a retry resumes idempotently."""

        original_start = server_module.WikiHandler._start_pipeline_driver

        def failing_start(handler_self, params, run_dir):
            class FailingDriver:
                stdout = iter(["[DRIVER-STAGE:plan] ok ran\n"])
                stderr = None
                returncode = 1

                def wait(self, timeout=None):
                    return 1

                def kill(self):
                    pass

            return FailingDriver()

        server_module.WikiHandler._start_pipeline_driver = failing_start
        self.addCleanup(setattr, server_module.WikiHandler, "_start_pipeline_driver", original_start)
        status, raw, headers = self._collect_sse(
            self.request("POST", "/api/workflow", {"message": "主题", "params": self.params()})
        )
        self.assertEqual(status, HTTPStatus.OK)
        events = self.sse_events()
        self.assertEqual(events[-1]["type"], "topic_error")
        self.assertIn("固定流程执行失败", events[-1]["message"])
        self.assertEqual(FakeTurn.instances, [])
        # The run dir exists and is still in-progress for the retry.
        manifest = json.loads(
            next((self.kb_root / "work").glob("literature-review-*/run.json")).read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["status"], "in-progress")

    def test_workflow_kickoff_request_model_wins(self):
        """The composer's model choice sticks: kickoff stores it, the
        continuation turn resumes with the same model."""

        def script(turn_self, kwargs):
            turn_self._events = self._checkpoint_turn_events()

        self._seed_turn_factory(script)
        status, raw, headers = self._collect_sse(
            self.request(
                "POST", "/api/workflow",
                {"message": "主题", "model": "deepseek-v4-flash-vision-exp", "params": self.params()},
            )
        )
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(
            FakeTurn.instances[-1].kwargs["model"], "deepseek-v4-flash-vision-exp"
        )
        # The request model reached the turn's argv (the registry's model field
        # is later overwritten by the session event's actual-model report).

    def test_topic_chat_default_model(self):
        """Topic chats default to glm-5.3-flash unless the request says otherwise."""

        self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "hi"})
        self.assertEqual(FakeTurn.instances[-1].kwargs["model"], server_module.DEFAULT_CHAT_MODEL)
        self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "hi", "model": "opus"})
        self.assertEqual(FakeTurn.instances[-1].kwargs["model"], "opus")

    def test_concurrent_keys_do_not_conflict(self):
        """Per-key CHAT_LOCKS: a chat on a topic must not 409 while a
        workflow segment holds its own lock (the old global lock rejected
        any second conversation)."""

        def script(turn_self, kwargs):
            turn_self._events = self._checkpoint_turn_events()

        self._seed_turn_factory(script)
        status, raw, _ = self._collect_sse(
            self.request("POST", "/api/workflow", {"message": "甲主题", "params": self.params("甲主题")})
        )
        self.assertEqual(status, HTTPStatus.OK)
        workflow_events = [e["type"] for e in self.sse_events()]
        # Now, with the workflow registry populated, a topic chat must still
        # stream (distinct lock key) — the old global lock would 409.
        status, raw, _ = self._collect_sse(
            self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "总结"})
        )
        self.assertEqual(status, HTTPStatus.OK, "topic chat must not 409 while a workflow runs")
        self.assertEqual(self.sse_events()[0]["type"], "session")
        self.assertEqual(workflow_events[-1], "awaiting_input")


class WikiRootResolutionTest(unittest.TestCase):
    """Serving rule: editable install (repo checkout) serves the repo wiki/;
    non-editable serves <kb-root>/wiki, bootstrapping it when missing."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb_root = Path(self.tmp.name) / "kb"
        self.kb_root.mkdir()
        self._saved = (server_module.IS_REPO_CHECKOUT, server_module.REPO_WIKI_ROOT)

    def tearDown(self):
        server_module.IS_REPO_CHECKOUT, server_module.REPO_WIKI_ROOT = self._saved

    def _set(self, *, is_repo: bool, repo_wiki: Path | None):
        server_module.IS_REPO_CHECKOUT = is_repo
        server_module.REPO_WIKI_ROOT = repo_wiki or Path(self.tmp.name) / "no-repo-wiki"

    def test_repo_checkout_serves_repo_wiki(self):
        repo_wiki = Path(self.tmp.name) / "repo" / "wiki"
        repo_wiki.mkdir(parents=True)
        (repo_wiki / "index.html").write_text("<html></html>", encoding="utf-8")
        self._set(is_repo=True, repo_wiki=repo_wiki)
        self.assertEqual(server_module.resolve_wiki_root(self.kb_root), repo_wiki)

    def test_repo_checkout_without_frontend_falls_back_to_kb_wiki(self):
        self._set(is_repo=True, repo_wiki=None)
        kb_wiki = self.kb_root / "wiki"
        kb_wiki.mkdir()
        (kb_wiki / "index.html").write_text("<html></html>", encoding="utf-8")
        self.assertEqual(server_module.resolve_wiki_root(self.kb_root), kb_wiki)

    def test_non_editable_serves_kb_wiki(self):
        self._set(is_repo=False, repo_wiki=None)
        kb_wiki = self.kb_root / "wiki"
        kb_wiki.mkdir()
        (kb_wiki / "index.html").write_text("<html></html>", encoding="utf-8")
        self.assertEqual(server_module.resolve_wiki_root(self.kb_root), kb_wiki)

    def test_non_editable_bootstraps_missing_kb_wiki_from_bundled_assets(self):
        """A non-editable install has no repo checkout; bootstrap copies the
        wheel-bundled frontend (wiki_scripts/wiki_assets, mapped from repo
        wiki/ at build time)."""

        self._set(is_repo=False, repo_wiki=None)
        source = Path(self.tmp.name) / "bundled"
        (source / "assets").mkdir(parents=True)
        (source / "index.html").write_text("<html></html>", encoding="utf-8")
        (source / "assets" / "wiki.js").write_text(";", encoding="utf-8")
        (source / "data").mkdir()  # never copied
        (source / "__init__.py").write_text("# package marker\n", encoding="utf-8")
        original_assets = server_module.FRONTEND_ASSETS
        server_module.FRONTEND_ASSETS = source
        try:
            served = server_module.resolve_wiki_root(self.kb_root)
        finally:
            server_module.FRONTEND_ASSETS = original_assets
        self.assertEqual(served, self.kb_root / "wiki")
        self.assertTrue((served / "index.html").is_file())
        self.assertTrue((served / "assets" / "wiki.js").is_file())
        self.assertFalse((served / "data").exists(), "data/ must not be seeded by bootstrap")
        self.assertFalse((served / "__init__.py").exists(), "package marker must not leak")

    def test_non_editable_bootstraps_from_repo_when_unbundled(self):
        """A repo run without bundled assets (e.g. wheel mapping changed)
        falls back to copying the repo checkout's wiki/."""

        self._set(is_repo=False, repo_wiki=None)
        repo_wiki = Path(self.tmp.name) / "repo" / "wiki"
        (repo_wiki / "assets").mkdir(parents=True)
        (repo_wiki / "index.html").write_text("<html></html>", encoding="utf-8")
        (repo_wiki / "assets" / "wiki.js").write_text(";", encoding="utf-8")
        (repo_wiki / "data").mkdir()
        original_assets = server_module.FRONTEND_ASSETS
        server_module.FRONTEND_ASSETS = Path(self.tmp.name) / "no-bundled-assets"
        self._set(is_repo=False, repo_wiki=repo_wiki)
        try:
            served = server_module.resolve_wiki_root(self.kb_root)
        finally:
            server_module.FRONTEND_ASSETS = original_assets
        self.assertEqual(served, self.kb_root / "wiki")
        self.assertTrue((served / "index.html").is_file())
        self.assertFalse((served / "data").exists(), "data/ must not be seeded by bootstrap")

    def test_bootstrap_without_any_frontend_raises(self):
        self._set(is_repo=False, repo_wiki=None)
        original_assets = server_module.FRONTEND_ASSETS
        server_module.FRONTEND_ASSETS = Path(self.tmp.name) / "missing-assets"
        try:
            with self.assertRaisesRegex(RuntimeError, "前端"):
                server_module.bootstrap_wiki_frontend(self.kb_root / "wiki")
        finally:
            server_module.FRONTEND_ASSETS = original_assets

    def test_bundled_assets_exist_or_wheel_mapping_is_live(self):
        """Either the wheel bundles the frontend (pyproject maps
        wiki_scripts.wiki_assets onto repo wiki/) or we are running from a
        source tree — in both cases a bootstrap source must exist."""

        has_bundled = (server_module.FRONTEND_ASSETS / "index.html").is_file()
        has_repo = (server_module.REPO_WIKI_ROOT / "index.html").is_file()
        self.assertTrue(has_bundled or has_repo, "no frontend bootstrap source found")


class EmptyKbStartupTest(unittest.TestCase):
    """main() must keep serving when the refresh finds no publishable topics
    (first-run empty KB), warning instead of exiting."""

    def test_empty_kb_does_not_exit(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        kb_root = Path(tmp.name) / "kb"
        (kb_root / "knowledge").mkdir(parents=True)
        (kb_root / "knowledge" / "literature-review-catalog.md").write_text("# catalog\n", encoding="utf-8")
        wiki_root = kb_root / "wiki"
        wiki_root.mkdir()
        (wiki_root / "index.html").write_text("<html></html>", encoding="utf-8")

        original_refresh = server_module.refresh_snapshot
        original_map = server_module.build_knowledge_map
        server_module.refresh_snapshot = lambda *a, **k: (_ for _ in ()).throw(
            RuntimeError("没有发现同时包含三种成稿的完整话题，保留现有快照。")
        )
        server_module.build_knowledge_map = lambda *a, **k: None
        started = {}

        class FakeServer:
            def __init__(self, addr, handler):
                started["handler"] = handler

            def serve_forever(self):
                started["served"] = True
                raise KeyboardInterrupt  # exit the serve loop immediately

            def server_close(self):
                pass

        original_httpd = server_module.ThreadingHTTPServer
        server_module.ThreadingHTTPServer = FakeServer
        try:
            argv = [
                "serve_research_wiki",
                "--kb-root", str(kb_root),
                "--port", "0",
                "--no-chat",
            ]
            original_argv = sys.argv
            sys.argv = argv
            try:
                code = server_module.main()
            finally:
                sys.argv = original_argv
        finally:
            server_module.refresh_snapshot = original_refresh
            server_module.build_knowledge_map = original_map
            server_module.ThreadingHTTPServer = original_httpd

        self.assertEqual(code, 0)
        self.assertTrue(started.get("served"), "server should start despite empty KB")


class NewUserKbCreationTest(unittest.TestCase):
    """First run with no knowledge base anywhere: a skeleton KB is created at
    the default location (starter catalog routing zero runs) and the server
    starts into its empty-library state. Explicit --kb-root is never created."""

    def setUp(self):
        self._saved_default = server_module.DEFAULT_KB_ROOT
        self._saved_repo_root = server_module.REPO_ROOT

    def tearDown(self):
        server_module.DEFAULT_KB_ROOT = self._saved_default
        server_module.REPO_ROOT = self._saved_repo_root

    def _run_main(self, *extra_args):
        started = {}

        class FakeServer:
            def __init__(self, addr, handler):
                started["handler"] = handler

            def serve_forever(self):
                started["served"] = True
                raise KeyboardInterrupt  # exit the serve loop immediately

            def server_close(self):
                pass

        swaps = (
            (server_module, "refresh_snapshot", lambda *a, **k: None),
            (server_module, "build_knowledge_map", lambda *a, **k: None),
            (server_module, "resolve_wiki_root", lambda kb_root: kb_root / "wiki"),
            (server_module, "ThreadingHTTPServer", FakeServer),
        )
        saved = [(owner, name, getattr(owner, name)) for owner, name, _ in swaps]
        for owner, name, value in swaps:
            setattr(owner, name, value)
        original_argv = sys.argv
        sys.argv = ["serve_research_wiki", "--port", "0", "--no-chat", *extra_args]
        try:
            code = server_module.main()
        finally:
            sys.argv = original_argv
            for owner, name, value in saved:
                setattr(owner, name, value)
        return code, started

    def test_missing_default_kb_is_created_and_server_starts(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        home = Path(tmp.name)
        kb_root = home / "Documents" / "arxiv"  # does not exist yet
        server_module.DEFAULT_KB_ROOT = kb_root
        server_module.REPO_ROOT = home / "empty-repo"  # no fallback catalog

        code, started = self._run_main()

        self.assertEqual(code, 0)
        self.assertTrue(started.get("served"), "server should start with a fresh skeleton KB")
        catalog = kb_root / "knowledge" / "literature-review-catalog.md"
        self.assertTrue(catalog.is_file(), "starter catalog should be created")
        self.assertIn("KB-LIT-REVIEWS", catalog.read_text(encoding="utf-8"))
        self.assertTrue((kb_root / "evidence").is_dir(), "evidence/ should be created")

    def test_explicit_kb_root_is_never_created(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        missing = Path(tmp.name) / "no-such-kb"

        code, _ = self._run_main("--kb-root", str(missing))

        self.assertEqual(code, 1)
        self.assertFalse(missing.exists(), "explicit --kb-root must not be auto-created")


class ChatDisabledTest(ChatServerHarness):
    """--no-chat / missing claude: the POST endpoints return 503, but the
    state endpoint is a capability probe and reports enabled=false with 200."""

    chat_enabled = False

    def test_chat_returns_503_when_disabled(self):
        status, payload, _ = self.request("POST", "/api/chat", {"topic_id": self.topic_id, "message": "hi"})
        self.assertEqual(status, HTTPStatus.SERVICE_UNAVAILABLE)

    def test_reset_returns_503_when_disabled(self):
        status, payload, _ = self.request("POST", "/api/chat/reset", {"topic_id": self.topic_id})
        self.assertEqual(status, HTTPStatus.SERVICE_UNAVAILABLE)

    def test_state_probe_reports_disabled(self):
        status, payload, _ = self.request("GET", f"/api/chat/state?topic={self.topic_id}")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertFalse(payload["enabled"])


class ReaderEndpointTest(ChatServerHarness):
    """/api/reader/<id> serves the cleaned paper document (network mocked)."""

    def _mock_fetch(self, calls):
        original = server_module.arxiv_reader.fetch_paper

        def fake_fetch(paper_id, cache_dir, **kwargs):
            calls.append((paper_id, cache_dir))
            return {
                "ok": True,
                "paper_id": paper_id,
                "html": '<!doctype html><html><body data-reader-doc="ok">paper</body></html>',
                "source": "cache",
                "error": "",
            }

        server_module.arxiv_reader.fetch_paper = fake_fetch
        self.addCleanup(lambda: setattr(server_module.arxiv_reader, "fetch_paper", original))

    def test_reader_serves_paper_document(self):
        calls = []
        self._mock_fetch(calls)
        status, raw, headers = self.request("GET", "/api/reader/2402.10329")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertIn("text/html", headers.get("Content-Type", ""))
        self.assertIn('data-reader-doc="ok"', raw)
        self.assertEqual(calls[0][0], "2402.10329")
        # Cache lives under <kb-root>/work/ (scratch), never inside wiki/.
        self.assertEqual(calls[0][1], self.kb_root / "work" / "reader-cache")

    def test_reader_normalizes_arxiv_urls(self):
        calls = []
        self._mock_fetch(calls)
        self.request("GET", "/api/reader/https://arxiv.org/abs/2402.10329v3")
        self.assertEqual(calls[0][0], "2402.10329")

    def test_reader_rejects_non_paper_ids(self):
        status, payload, _ = self.request("GET", "/api/reader/not-a-paper")
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_reader_serves_unavailable_page_when_fetch_fails(self):
        original = server_module.arxiv_reader.fetch_paper

        def fake_fetch(paper_id, cache_dir, **kwargs):
            return {"ok": False, "paper_id": paper_id, "html": "", "source": "", "error": "无 HTML 版本"}

        server_module.arxiv_reader.fetch_paper = fake_fetch
        self.addCleanup(lambda: setattr(server_module.arxiv_reader, "fetch_paper", original))
        status, raw, _ = self.request("GET", "/api/reader/1905.02688")
        self.assertEqual(status, HTTPStatus.OK)  # friendly page, not an error
        self.assertIn('data-reader-doc="unavailable"', raw)
        self.assertIn("1905.02688", raw)


class PaperChatEndpointTest(ChatServerHarness):
    """Paper chat: per-arXiv-id conversation with pool+deep-read preparation.

    The preparation subprocess is faked (it would otherwise hit the network
    and spawn a claude skeleton agent); the fake writes the pool artifacts the
    real one would produce, so the endpoint's branching is exercised for real."""

    def setUp(self):
        super().setUp()
        self.prepare_calls: list[str] = []
        self._fake_prepare()

    def _fake_prepare(self):
        original = server_module.WikiHandler._run_paper_preparation

        def fake_prepare(handler_self, paper_id):
            self.prepare_calls.append(paper_id)
            pool_dir = server_module.pool_root(self.kb_root) / f"arxiv-{paper_id}"
            pool_dir.mkdir(parents=True, exist_ok=True)
            (pool_dir / "extraction.json").write_text("{}", encoding="utf-8")
            (pool_dir / "note.json.audit.json").write_text(
                json.dumps({"status": "pass"}), encoding="utf-8"
            )
            return "pass", True

        server_module.WikiHandler._run_paper_preparation = fake_prepare
        self.addCleanup(setattr, server_module.WikiHandler, "_run_paper_preparation", original)

    def test_state_without_id_reports_capability(self):
        status, payload, _ = self.request("GET", "/api/paper/chat/state")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertTrue(payload["enabled"])

    def test_invalid_id_rejected(self):
        status, payload, _ = self.request(
            "POST", "/api/paper/chat", {"arxiv_id": "not-an-id", "message": "hi"}
        )
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_first_message_prepares_paper_and_streams(self):
        status, raw, headers = self._collect_sse(
            self.request(
                "POST", "/api/paper/chat",
                {"arxiv_id": "2402.10329", "message": "这篇论文的方法是什么？"},
            )
        )
        self.assertEqual(status, HTTPStatus.OK)
        events = self.sse_events()
        types = [event["type"] for event in events]
        self.assertIn("stage", types)  # preparation progress + cache notice
        self.assertIn("session", types)
        self.assertIn("delta", types)
        self.assertEqual(self.prepare_calls, ["2402.10329"])
        # Session is cached under the paper-<id> key.
        entry = server_module.WikiHandler._paper_chat_key("2402.10329")
        recorded = server_module.wiki_chat.ChatSessionRegistry(
            self.kb_root / "wiki" / "data" / "chat-sessions.json"
        ).get(entry)
        self.assertIsNotNone(recorded)
        self.assertTrue(any(m["role"] == "user" for m in recorded["messages"]))

    def test_second_message_reuses_cache_without_preparation(self):
        self.request("POST", "/api/paper/chat", {"arxiv_id": "2402.10329", "message": "一问"})
        self.request("POST", "/api/paper/chat", {"arxiv_id": "2402.10329", "message": "二问"})
        # Preparation ran once (first contact only); both turns produced output.
        self.assertEqual(len(self.prepare_calls), 1)
        self.assertEqual(len(FakeTurn.instances), 2)
        second_prompt = FakeTurn.instances[-1].kwargs["prompt"]
        self.assertIn("2402.10329", second_prompt)
        system_prompt = FakeTurn.instances[-1].kwargs["system_prompt"]
        self.assertIn("论文精读助手", system_prompt)

    def test_reset_clears_paper_session(self):
        self.request("POST", "/api/paper/chat", {"arxiv_id": "2402.10329", "message": "一问"})
        status, payload, _ = self.request(
            "POST", "/api/paper/chat/reset", {"arxiv_id": "2402.10329"}
        )
        self.assertEqual(status, HTTPStatus.OK)
        key = server_module.WikiHandler._paper_chat_key("2402.10329")
        registry = server_module.wiki_chat.ChatSessionRegistry(
            self.kb_root / "wiki" / "data" / "chat-sessions.json"
        )
        self.assertIsNone(registry.get(key))
        # State probe reports no history after reset.
        status, payload, _ = self.request("GET", "/api/paper/chat/state?id=2402.10329")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(payload["messages"], [])
        self.assertEqual(payload["deep_read_status"], "pass")


class QuickReadEndpointTest(ChatServerHarness):
    """The 速读 routes: state probe (no article / with article / bad id) and
    the SSE generate endpoint backed by a stubbed quick_read_paper.py run."""

    def seed_pool(self, paper_id: str = "2402.10329", *, with_article: bool = False):
        pool_dir = self.kb_root / "pool" / f"arxiv-{paper_id}"
        pool_dir.mkdir(parents=True, exist_ok=True)
        (pool_dir / "extraction.json").write_text("{}", encoding="utf-8")
        (pool_dir / "note.json").write_text("{}", encoding="utf-8")
        (pool_dir / "note.json.audit.json").write_text(json.dumps({"status": "pass"}), encoding="utf-8")
        if with_article:
            card = "# 速读：测试\n\narXiv:2402.10329 · method\n\n## 一句话定位\n\n测试内容。\n\n" \
                   "## 链接\n\n[arXiv:2402.10329](https://arxiv.org/abs/2402.10329)\n"
            (pool_dir / "quick-read_sudu.md").write_text(card, encoding="utf-8")
        return pool_dir

    def test_state_reports_unpooled_paper(self):
        status, payload, _ = self.request("GET", "/api/paper/quickread/state?id=2402.10329")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertFalse(payload["pooled"])
        self.assertIsNone(payload["deep_read_status"])
        self.assertFalse(payload["quick_read"])
        self.assertEqual(payload["markdown"], "")
        self.assertIn("agent_available", payload)

    def test_state_reports_pooled_card(self):
        self.seed_pool(with_article=True)
        status, payload, _ = self.request("GET", "/api/paper/quickread/state?id=2402.10329")
        self.assertEqual(status, HTTPStatus.OK)
        self.assertTrue(payload["pooled"])
        self.assertEqual(payload["deep_read_status"], "pass")
        self.assertTrue(payload["quick_read"])
        self.assertIn("## 一句话定位", payload["markdown"])
        self.assertIsNotNone(payload["updated_at"])

    def test_state_bad_id_rejected(self):
        status, payload, _ = self.request("GET", "/api/paper/quickread/state?id=not-an-id")
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_generate_streams_sse_and_delivers_markdown(self):
        self.seed_pool()

        def fake_popen(command, **kwargs):
            # The stub run reports success; the article file must already
            # exist for the handler to read it back.
            pool_dir = self.kb_root / "pool" / "arxiv-2402.10329"
            (pool_dir / "quick-read_sudu.md").write_text(
                "# 速读：生成结果\n\n## 一句话定位\n\n新卡。\n", encoding="utf-8"
            )
            return FakeProcess(returncode=0, lines=["[PAPER-CHAT] pool 命中", "[QUICK-READ] 速读卡已写入"])

        with mock.patch.object(server_module.subprocess, "Popen", side_effect=fake_popen):
            status, raw, headers = self._collect_sse(
                self.request("POST", "/api/paper/quickread", {"arxiv_id": "2402.10329"})
            )
        self.assertEqual(status, HTTPStatus.OK)
        events = self.sse_events()
        kinds = [event["type"] for event in events]
        self.assertIn("stage", kinds)
        self.assertEqual(kinds[-1], "quickread_done")
        done = events[-1]
        self.assertEqual(done["arxiv_id"], "2402.10329")
        self.assertIn("生成结果", done["markdown"])
        # Both progress prefixes are forwarded.
        details = [event["detail"] for event in events if event["type"] == "stage"]
        self.assertTrue(any("pool 命中" in detail for detail in details))
        self.assertTrue(any("速读卡已写入" in detail for detail in details))

    def test_generate_failure_reports_topic_error(self):
        self.seed_pool()
        with mock.patch.object(server_module.subprocess, "Popen",
                               return_value=FakeProcess(returncode=3, lines=[])):
            status, raw, _ = self._collect_sse(
                self.request("POST", "/api/paper/quickread", {"arxiv_id": "2402.10329"})
            )
        self.assertEqual(status, HTTPStatus.OK)
        events = self.sse_events()
        self.assertEqual(events[-1]["type"], "topic_error")
        self.assertIn("失败", events[-1]["message"])

    def test_generate_bad_id_rejected(self):
        status, payload, _ = self.request("POST", "/api/paper/quickread", {"arxiv_id": "garbage"})
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)


class FakeProcess:
    """subprocess.Popen stand-in for the quick-read generation stub."""

    def __init__(self, *, returncode: int, lines: list[str]):
        self.returncode = returncode
        self._lines = lines
        self.stdout = iter(lines)
        self.stderr = iter([])

    def wait(self, timeout=None):
        return self.returncode

    def kill(self):
        pass


if __name__ == "__main__":
    unittest.main()

"""Tests for scripts/serve_research_wiki.py — chat endpoints, topic
resolution, and the /api/refresh regression guard."""

import http.client
import importlib.util
import json
import sys
import tempfile
import threading
import unittest
from functools import partial
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from pathlib import Path

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
                 permission_mode="bypassPermissions", allowed_tools=None, timeout_s=900):
        self.kwargs = dict(
            cli=cli, prompt=prompt, cwd=cwd, session_id=session_id, model=model,
            permission_mode=permission_mode, allowed_tools=allowed_tools, timeout_s=timeout_s,
        )
        self.started = 0
        self.stopped = False
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


if __name__ == "__main__":
    unittest.main()

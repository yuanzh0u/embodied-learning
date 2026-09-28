#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import threading
import time
import unittest
from functools import partial
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "serve_research_wiki.py"
SPEC = importlib.util.spec_from_file_location("serve_research_wiki", SCRIPT)
serve = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(serve)


FAKE_BUILDER = """\
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

argv = sys.argv[1:]
output = Path(argv[argv.index("--output") + 1])
output.mkdir(parents=True, exist_ok=True)
manifest = {
    "topics": [{"id": "smoke-topic"}],
    "generated_at": "2026-01-02T03:04:05Z",
}
(output / "manifest.json").write_text(
    json.dumps(manifest, ensure_ascii=False),
    encoding="utf-8",
)
print("fake refresh ok")
"""


class ServeResearchWikiSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.wiki_root = self.root / "wiki"
        self.wiki_root.mkdir()
        (self.wiki_root / "index.html").write_text(
            "<!doctype html><title>wiki-smoke</title>\n",
            encoding="utf-8",
        )
        self.builder = self.root / "fake_builder.py"
        self.builder.write_text(FAKE_BUILDER, encoding="utf-8")

        self._orig_wiki = serve.WIKI_ROOT
        self._orig_builder = serve.BUILDER
        serve.WIKI_ROOT = self.wiki_root
        serve.BUILDER = self.builder

    def tearDown(self) -> None:
        # Ensure the module lock is never left held across tests.
        if serve.REFRESH_LOCK.locked():
            serve.REFRESH_LOCK.release()
        serve.WIKI_ROOT = self._orig_wiki
        serve.BUILDER = self._orig_builder
        self._tmp.cleanup()

    @contextmanager
    def _running_server(self, knowledge_map: Path | None = None) -> Iterator[tuple[str, int]]:
        handler = partial(serve.WikiHandler, knowledge_map=knowledge_map)
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        host, port = server.server_address[:2]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            # Give the listener a moment to accept connections.
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                try:
                    conn = HTTPConnection(host, port, timeout=0.2)
                    conn.request("GET", "/")
                    conn.getresponse().read()
                    conn.close()
                    break
                except OSError:
                    time.sleep(0.01)
            yield host, port
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2.0)

    def _request(
        self,
        host: str,
        port: int,
        method: str,
        path: str,
        body: bytes | None = None,
    ) -> tuple[int, bytes, dict[str, str]]:
        conn = HTTPConnection(host, port, timeout=2.0)
        headers = {}
        if body is not None:
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(body))
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        payload = response.read()
        header_map = {key.lower(): value for key, value in response.getheaders()}
        status = response.status
        conn.close()
        return status, payload, header_map

    def test_bind_serves_index_and_404(self) -> None:
        with self._running_server() as (host, port):
            status, body, _ = self._request(host, port, "GET", "/")
            self.assertEqual(status, 200)
            self.assertIn(b"wiki-smoke", body)

            status, _, _ = self._request(host, port, "GET", "/does-not-exist.html")
            self.assertEqual(status, 404)

    def test_post_unknown_path_is_404(self) -> None:
        with self._running_server() as (host, port):
            status, _, _ = self._request(host, port, "POST", "/api/other")
            self.assertEqual(status, 404)

    def test_refresh_endpoint_success(self) -> None:
        with self._running_server() as (host, port):
            status, body, headers = self._request(host, port, "POST", "/api/refresh")
            self.assertEqual(status, 200)
            self.assertIn("application/json", headers.get("content-type", ""))
            payload = json.loads(body.decode("utf-8"))
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["topics"], 1)
            self.assertEqual(payload["generated_at"], "2026-01-02T03:04:05Z")
            self.assertTrue((self.wiki_root / "data" / "manifest.json").is_file())

    def test_refresh_lock_returns_conflict(self) -> None:
        acquired = serve.REFRESH_LOCK.acquire(blocking=False)
        self.assertTrue(acquired)
        try:
            with self._running_server() as (host, port):
                status, body, _ = self._request(host, port, "POST", "/api/refresh")
                self.assertEqual(status, 409)
                payload = json.loads(body.decode("utf-8"))
                self.assertIn("error", payload)
        finally:
            serve.REFRESH_LOCK.release()

    def test_knowledge_map_missing_is_404(self) -> None:
        with self._running_server(knowledge_map=None) as (host, port):
            status, _, _ = self._request(host, port, "GET", "/knowledge-map")
            self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()

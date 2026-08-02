#!/usr/bin/env python3
"""Serve the research Wiki locally and expose its safe refresh endpoint."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import threading
import webbrowser
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_research_wiki import resolve_snapshot_directory  # noqa: E402


WIKI_ROOT = REPO_ROOT / "wiki"
BUILDER = REPO_ROOT / "scripts" / "build_research_wiki.py"
GRAPH_BUILDER = REPO_ROOT / "scripts" / "visualize_kb_index.py"
REFRESH_LOCK = threading.Lock()


class WikiHandler(SimpleHTTPRequestHandler):
    server_version = "ResearchWiki/1.0"

    def __init__(self, *args, knowledge_map: Path | None = None, **kwargs):
        self.knowledge_map = knowledge_map
        super().__init__(*args, directory=str(WIKI_ROOT), **kwargs)

    def end_headers(self) -> None:
        if self.path.startswith("/data/"):
            self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        print(f"[Wiki] {format % args}")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/knowledge-map", "/knowledge-map/", "/knowledge-map/index.html"}:
            self._serve_knowledge_map()
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/refresh":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not REFRESH_LOCK.acquire(blocking=False):
            self._send_json(HTTPStatus.CONFLICT, {"error": "已有刷新正在进行，请稍候。"})
            return
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILDER),
                    "--output",
                    str(WIKI_ROOT / "data"),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            if result.returncode:
                message = (result.stderr or result.stdout or "刷新脚本执行失败").strip()
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": message})
                return
            snapshot_dir = resolve_snapshot_directory(WIKI_ROOT / "data")
            manifest = json.loads((snapshot_dir / "manifest.json").read_text(encoding="utf-8"))
            self._send_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "topics": len(manifest["topics"]),
                    "generated_at": manifest["generated_at"],
                    "message": result.stdout.strip(),
                },
            )
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
        finally:
            REFRESH_LOCK.release()

    def _serve_knowledge_map(self) -> None:
        if not self.knowledge_map or not self.knowledge_map.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "知识图谱尚未生成")
            return
        payload = self.knowledge_map.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_json(self, status: HTTPStatus, value: object) -> None:
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def refresh_snapshot() -> None:
    result = subprocess.run(
        [sys.executable, str(BUILDER)],
        cwd=REPO_ROOT,
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError("初始成果快照构建失败。")


def build_knowledge_map(output: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(GRAPH_BUILDER), "--no-open", "--output", str(output)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        print("知识图谱本地预览生成失败，Wiki 阅读功能仍可正常使用。", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="在本地打开空间智能研究 Wiki")
    parser.add_argument("--port", type=int, default=8018, help="本地端口，默认 8018")
    parser.add_argument("--open", action="store_true", help="启动后自动打开浏览器")
    parser.add_argument("--no-refresh", action="store_true", help="启动时不重新扫描成果")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.no_refresh:
        try:
            refresh_snapshot()
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 1

    with tempfile.TemporaryDirectory(prefix="research-wiki-map-") as temp_dir:
        knowledge_map = Path(temp_dir) / "index.html"
        build_knowledge_map(knowledge_map)
        handler = partial(WikiHandler, knowledge_map=knowledge_map)
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        url = f"http://127.0.0.1:{args.port}/"
        print(f"空间智能研究 Wiki 已准备好：{url}")
        print("保持此窗口打开即可阅读；按 Control-C 关闭。")
        if args.open:
            threading.Timer(0.45, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nWiki 已关闭。")
        finally:
            server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

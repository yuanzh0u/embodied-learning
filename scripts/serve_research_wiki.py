#!/usr/bin/env python3
"""Serve the research Wiki locally and expose its safe refresh endpoint."""

from __future__ import annotations

import argparse
import errno
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


# Sibling scripts resolve next to this file, so the installed console command
# (site-packages/wiki_scripts/) and a repo checkout behave identically.
BUILDER = SCRIPT_DIR / "build_research_wiki.py"
GRAPH_BUILDER = SCRIPT_DIR / "visualize_kb_index.py"
# Frontend is never bundled or copied: serve the existing wiki/ folder next to
# the knowledge base, falling back to the repo checkout's wiki/ in-place.
DEFAULT_KB_ROOT = Path.home() / "Documents" / "arxiv"
REPO_WIKI_ROOT = REPO_ROOT / "wiki"
CATALOG_RELPATH = Path("knowledge") / "literature-review-catalog.md"
REFRESH_LOCK = threading.Lock()


def resolve_kb_root(requested: Path | None) -> Path | None:
    """KB root: an explicit --kb-root (must carry a catalog, validated by the
    caller), else ~/Documents/arxiv, else the repo checkout. None = not found."""

    candidates: list[Path] = []
    if requested is not None:
        candidates.append(requested)
    else:
        candidates.append(DEFAULT_KB_ROOT)
        candidates.append(REPO_ROOT)
    for candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if (resolved / CATALOG_RELPATH).is_file():
            return resolved
    return None


def resolve_wiki_root(kb_root: Path) -> Path:
    """Serve <kb-root>/wiki when it exists (data refreshes in place there);
    otherwise fall back to the repo checkout's wiki/ (a plain repo run)."""

    kb_wiki = kb_root / "wiki"
    if (kb_wiki / "index.html").is_file():
        return kb_wiki
    if not REPO_WIKI_ROOT.is_dir():
        # First serve against a KB without wiki/: build the static shell in
        # place from the repo frontend assets if available, else fail loudly.
        raise RuntimeError(
            f"未找到 Wiki 前端目录：{kb_wiki}（缺少 index.html）。"
            "请从仓库复制 wiki/ 目录到该路径。"
        )
    return REPO_WIKI_ROOT


def build_refresh_command(kb_root: Path, data_dir: Path) -> list[str]:
    command = [sys.executable, str(BUILDER), "--output", str(data_dir)]
    if (kb_root / CATALOG_RELPATH).is_file():
        command += ["--kb-root", str(kb_root)]
    return command


class WikiHandler(SimpleHTTPRequestHandler):
    server_version = "ResearchWiki/1.0"

    def __init__(
        self,
        *args,
        knowledge_map: Path | None = None,
        kb_root: Path,
        wiki_root: Path,
        data_dir: Path,
        **kwargs,
    ):
        self.knowledge_map = knowledge_map
        self.kb_root = kb_root
        self.data_dir = data_dir
        self.refresh_command = build_refresh_command(kb_root, data_dir)
        super().__init__(*args, directory=str(wiki_root), **kwargs)

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
                self.refresh_command,
                cwd=str(self.kb_root),
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            if result.returncode:
                message = (result.stderr or result.stdout or "刷新脚本执行失败").strip()
                self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": message})
                return
            snapshot_dir = resolve_snapshot_directory(self.data_dir)
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


def refresh_snapshot(kb_root: Path, data_dir: Path) -> None:
    result = subprocess.run(
        build_refresh_command(kb_root, data_dir),
        cwd=str(kb_root),
        text=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError("初始成果快照构建失败。")


def build_knowledge_map(output: Path, kb_root: Path) -> None:
    command = [sys.executable, str(GRAPH_BUILDER), "--no-open", "--output", str(output)]
    if (kb_root / "knowledge" / "index.md").is_file():
        command += ["--root", str(kb_root)]
    result = subprocess.run(
        command,
        cwd=str(kb_root),
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
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=None,
        help=f"本地知识库根目录（含 knowledge/ 与 evidence/），默认优先 {DEFAULT_KB_ROOT}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.kb_root is not None:
        # An explicit --kb-root is authoritative: never fall back to defaults.
        kb_root = args.kb_root.expanduser().resolve()
        if not (kb_root / CATALOG_RELPATH).is_file():
            print(
                f"--kb-root 指定的目录缺少 {CATALOG_RELPATH}：{kb_root}",
                file=sys.stderr,
            )
            return 1
    else:
        kb_root = resolve_kb_root(None)
    if kb_root is None:
        print(
            f"未找到本地知识库（默认查找 {DEFAULT_KB_ROOT}）。"
            "请用 --kb-root 指定包含 knowledge/literature-review-catalog.md 的目录。",
            file=sys.stderr,
        )
        return 1
    wiki_root = resolve_wiki_root(kb_root)
    data_dir = wiki_root / "data"
    if not args.no_refresh:
        try:
            refresh_snapshot(kb_root, data_dir)
        except RuntimeError as exc:
            print(exc, file=sys.stderr)
            return 1

    with tempfile.TemporaryDirectory(prefix="research-wiki-map-") as temp_dir:
        knowledge_map = Path(temp_dir) / "index.html"
        build_knowledge_map(knowledge_map, kb_root)
        handler = partial(
            WikiHandler,
            knowledge_map=knowledge_map,
            kb_root=kb_root,
            wiki_root=wiki_root,
            data_dir=data_dir,
        )
        url = f"http://127.0.0.1:{args.port}/"
        try:
            server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise
            print(f"已有实例正在运行：{url}")
            if args.open:
                threading.Timer(0.45, lambda: webbrowser.open(url)).start()
            return 0
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

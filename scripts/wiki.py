#!/usr/bin/env python3
"""Publish-domain CLI: wiki snapshot, static site, knowledge map, serving.

This entry owns the argparse flag tables and argv handling; the business logic
lives in ``embodied_learning.wiki.publish.*`` as ``run(args) -> int`` (no
argparse, no ``main`` in the library — see docs/adr/0005).
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
for _root in (_HERE.parents[3], _HERE.parents[1]):
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

from embodied_learning.utils.layout import DEFAULT_KB_ROOT, find_roots  # noqa: E402
from embodied_learning.wiki.publish import chat as wiki_chat  # noqa: E402

REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()

_MODULES: dict[str, str] = {
    "build-wiki": "embodied_learning.wiki.publish.snapshot",
    "build-site": "embodied_learning.wiki.publish.site",
    "build-knowledge-map": "embodied_learning.wiki.publish.knowledge_map",
    "build-mind-omni-reader": "embodied_learning.wiki.publish.mind_omni",
    "check-kb-links": "embodied_learning.wiki.publish.links",
    "serve": "embodied_learning.wiki.publish.server",
}

_HELP: dict[str, str] = {
    "build-wiki": "rebuild the wiki content snapshot from the catalog",
    "build-site": "build the static research site from a snapshot",
    "build-knowledge-map": "render the knowledge-base graph",
    "build-mind-omni-reader": "build the mind-omni reader page for one run",
    "check-kb-links": "audit knowledge/ links, source IDs and locators",
    "serve": "serve the local research wiki",
}

_PARSER_NAMES = {
    "build-wiki": "_snapshot_parser",
    "build-site": "_site_parser",
    "build-knowledge-map": "_knowledge_map_parser",
    "build-mind-omni-reader": "_mind_omni_parser",
    "check-kb-links": "_links_parser",
    "serve": "_server_parser",
}

_PARSERS: dict[str, object] = {}

def _snapshot_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="构建空间智能研究 Wiki 的静态内容快照")
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="成果目录 Markdown；也兼容直接扫描目录（默认随 --kb-root 或仓库目录解析）",
    )
    parser.add_argument("--output", type=Path, default=None, help="静态数据输出目录（默认 wiki/data）")
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=None,
        help="本地知识库根目录（含 knowledge/ 与 evidence/）；--source 未指定时使用其中的文献综述目录",
    )
    parser.add_argument(
        "--site-config",
        type=Path,
        default=None,
        help="品牌、英文标题与永久 URL 配置（默认随 --kb-root 或仓库目录解析）",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="只校验当前原子快照")
    action.add_argument("--activate", metavar="SNAPSHOT_ID", help="回滚或切换到已验证快照")
    parser.add_argument("--retain", type=int, default=2, help="至少保留的快照数，默认 2")
    return parser



def _site_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="从 schema v2 快照构建可抓取的具身智能研究站")
    parser.add_argument("--snapshot-root", type=Path, default=site.DEFAULT_SNAPSHOT_ROOT)
    parser.add_argument("--wiki-root", type=Path, default=site.DEFAULT_WIKI_ROOT)
    parser.add_argument("--output", type=Path, default=site.DEFAULT_OUTPUT)
    parser.add_argument("--base-url", default=site.DEFAULT_BASE_URL)
    parser.add_argument("--preview", action="store_true", help="输出 noindex,nofollow 的 PR Preview")
    parser.add_argument("--check-only", action="store_true", help="仅复查已有站点输出")
    return parser



def _knowledge_map_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=knowledge_map.__doc__)
    parser.add_argument("--root", default=str(knowledge_map.REPO_ROOT), help="Repository root.")
    parser.add_argument(
        "--start", default="knowledge/index.md", help="Entry markdown file, relative to --root."
    )
    parser.add_argument(
        "--output",
        default="work/kb-graph/index.html",
        help="Output HTML path, relative to --root unless absolute.",
    )
    parser.add_argument("--max-nodes", type=int, default=400, help="BFS node cap.")
    parser.add_argument("--no-open", action="store_true", help="Write the file but skip opening a browser.")
    return parser



def _mind_omni_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=mind_omni.__doc__)
    parser.add_argument(
        "--run",
        type=Path,
        required=True,
        help="Settled evidence bundle directory (holds run.json).",
    )
    parser.add_argument("--source", type=Path, default=mind_omni.DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=mind_omni.DEFAULT_OUTPUT)
    parser.add_argument("--canonical-url", default=mind_omni.DEFAULT_CANONICAL_URL)
    parser.add_argument("--preview", action="store_true")
    return parser



def _links_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=links.__doc__)
    parser.add_argument("--root", default=str(links.REPO_ROOT), help="Repository root to check.")
    return parser



def _server_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="在本地打开空间智能研究 Wiki")
    parser.add_argument("--port", type=int, default=8018, help="本地端口，默认 8018")
    parser.add_argument("--open", action="store_true", help="启动后自动打开浏览器")
    parser.add_argument("--no-refresh", action="store_true", help="启动时不重新扫描成果")
    parser.add_argument(
        "--close",
        action="store_true",
        help="关闭已在运行的 Wiki 实例（按端口找到监听进程并优雅停止）后退出",
    )
    parser.add_argument(
        "--kb-root",
        type=Path,
        default=None,
        help=f"本地知识库根目录（含 knowledge/ 与 evidence/），默认优先 {server.DEFAULT_KB_ROOT}",
    )
    chat = parser.add_argument_group("研究助手对话（本地 claude CLI）")
    chat.add_argument(
        "--chat-cli",
        default=None,
        help="claude 可执行文件路径，默认从 PATH 查找（回退 /usr/local/bin/claude）",
    )
    chat.add_argument("--chat-model", default=None, help="对话使用的模型，默认跟随 claude 配置")
    chat.add_argument(
        "--chat-permission-mode",
        default=server.wiki_chat.DEFAULT_PERMISSION_MODE,
        choices=["bypassPermissions", "acceptEdits", "plan", "default"],
        help=f"对话的权限模式，默认 {server.wiki_chat.DEFAULT_PERMISSION_MODE}",
    )
    chat.add_argument(
        "--chat-allowed-tools",
        default=None,
        help="限制对话可用的工具（传给 claude --allowedTools），默认不限制",
    )
    chat.add_argument(
        "--chat-timeout-s",
        type=float,
        default=server.wiki_chat.DEFAULT_CHAT_TIMEOUT_S,
        help="单轮对话超时秒数，默认 900",
    )
    chat.add_argument("--no-chat", action="store_true", help="禁用研究助手对话功能")
    wf = parser.add_argument_group("综述工作流（STORM 式加速）")
    wf.add_argument(
        "--pipeline-root",
        type=Path,
        default=None,
        help="包含 skills/ 的仓库根目录（工作流读取 SKILL.md 用）；默认自动探测脚本旁的仓库检出",
    )
    wf.add_argument(
        "--workflow-model",
        default=None,
        help="工作流主线程使用的模型（显式指定时优先于页面选择）；默认跟随页面采访选择或 --chat-model",
    )
    wf.add_argument(
        "--workflow-effort",
        default=None,
        choices=["low", "medium", "high"],
        help="工作流推理力度（低档更快）；默认跟随 claude 配置",
    )
    return parser



def _parser_for(name: str):
    """Build the argparse parser for one subcommand (flag table lives here)."""
    if name not in _PARSERS:
        globals().update({m.split(".")[-1]: importlib.import_module(m) for m in set(_MODULES.values())})
        _PARSERS[name] = globals()[_PARSER_NAMES[name]]()
    return _PARSERS[name]


def usage() -> str:
    lines = ["usage: wiki.py <subcommand> [args]", "", "subcommands:"]
    width = max(len(name) for name in _HELP)
    for name, help_text in _HELP.items():
        lines.append(f"  {name.ljust(width)}  {help_text}")
    return "\n".join(lines)


def dispatch(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(usage())
        return 0
    name, rest = argv[0], argv[1:]
    if name not in _MODULES:
        print(f"wiki.py: unknown subcommand {name!r}\n\n{usage()}", file=sys.stderr)
        return 2
    parser = _parser_for(name)
    parser.prog = name
    args = parser.parse_args(rest)
    mod = importlib.import_module(_MODULES[name])
    return int(mod.run(args) or 0)


def main(argv: list[str] | None = None) -> int:
    return dispatch(list(sys.argv[1:] if argv is None else argv))


# Console-script alias (pyproject [project.scripts]).
def serve_main() -> int:
    return dispatch(["serve", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Write one single-paper slide deck (汇报展示, reveal.js) into the public pool.

Single-paper pipeline, sibling of quick_read_paper.py:

    1. pool check   — reuse ensure_extraction (idempotent)
    2. deep read    — MANDATORY: reuse ensure_deep_read; no audited note,
                      no deck
    3. brief        — build_slide_brief renders note.json + meta.json into
                      slide-brief.md (deterministic, cheap)
    4. slide-source — one-shot agent writes the slide-source DSL between
                      sentinels; the script (never the agent) writes
                      slide-deck_report.md and compiles slide-deck_report.html
                      via the skill's build_slide_deck.py. Invalid output gets
                      one retry; rejected output is dumped verbatim to
                      slide-deck-agent-raw.txt for post-hoc diagnosis.
    5. audit        — audit-slide-deck findings are logged; errors do not
                      delete the deck but are reported in the summary JSON.

Exit codes: 0 deck written (or cache hit), 3 deep-read unavailable, 1 hard
failure. Progress prints one ``[SLIDE-DECK] <stage> <detail>`` line per step;
reused stages print ``[PAPER-CHAT]`` lines. The final stdout line is
machine-readable JSON.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from lib.agent_invoke import pool_root_for  # noqa: E402
    from lib.layout import find_roots  # noqa: E402
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.lib.agent_invoke import pool_root_for  # noqa: E402
    from wiki_scripts.lib.layout import find_roots  # noqa: E402
# AI-model capability goes through the harness binding (pybind-style); prompts and KB layout stay with the feature module.
from embodied_learning.harness.claude import complete, resolve_cli  # noqa: E402
try:
    from prepare_paper_chat import ensure_deep_read, ensure_extraction, normalize_arxiv_id  # noqa: E402
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.prepare_paper_chat import ensure_deep_read, ensure_extraction, normalize_arxiv_id  # noqa: E402
from embodied_learning.atomicio import atomic_write_text  # noqa: E402
from embodied_learning import locks  # noqa: E402

_REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()
WRITER_SCRIPTS = SKILLS_ROOT / "embodied-ai-review-writer" / "scripts"
if str(WRITER_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(WRITER_SCRIPTS))
import build_slide_deck as bsd  # noqa: E402

SOURCE_NAME = "slide-deck_report.md"
DECK_NAME = "slide-deck_report.html"
REFS_NAME = "refs.json"
BRIEF_NAME = "slide-brief.md"
RAW_DUMP_NAME = "slide-deck-agent-raw.txt"
AUDIT_SCRIPT = WRITER_SCRIPTS / "writing_audit.py"
STYLE_REFERENCE = SKILLS_ROOT / "embodied-ai-review-writer" / "references" / "slide-deck.md"
SOURCE_TIMEOUT_S = 600.0
SOURCE_OPEN = "<<<SLIDE-DECK-SOURCE>>>"
SOURCE_CLOSE = "<<<END-SLIDE-DECK-SOURCE>>>"
MIN_SLIDES = 5

UNPROVIDED = "（笔记未提供，需从 paper.md 核对）"


def log(message: str) -> None:
    print(f"[SLIDE-DECK] {message}", flush=True)


def _lines(items) -> list[str]:
    return [str(item).strip() for item in items or [] if str(item).strip()]


def _field(value) -> str:
    text = str(value or "").strip()
    return text if text else UNPROVIDED


def build_slide_brief(paper_id: str, note: dict, meta: dict) -> str:
    """Render note.json + meta.json into the slide-writing brief. Pure stdlib;
    every line is traceable to the note — the agent adds nothing."""
    def pick(*keys: str):
        node: dict = note
        for key in keys:
            node = node.get(key) if isinstance(node, dict) else None
            if node is None:
                return None
        return node

    lines = [f"# 汇报展示写作简报：arXiv:{paper_id}", ""]
    title = _field(pick("paper", "title") or pick("title") or meta.get("title"))
    lines.append(f"- 论文标题：{title}")

    positioning = _field(pick("one_sentence") or pick("summary")
                         or pick("paper", "one_sentence"))
    lines.append(f"- 一句话定位：{positioning}")
    lines.append("")

    lines.append("## 可上页的素材（数字与主张只能来自这里或 paper.md）")
    results = pick("results") or {}
    quantitative = _lines((results.get("quantitative") or pick("evidence_cards") or []))
    for item in quantitative:
        if isinstance(item, dict):
            lines.append(f"- {item.get('claim') or item.get('metric') or item}（{item.get('value', '')}）"
                         .replace("（）", ""))
        else:
            lines.append(f"- {item}")
    if not quantitative:
        lines.append(f"- {UNPROVIDED}")
    lines.append("")

    limits = pick("limitations") or {}
    stated = _lines(limits.get("stated"))
    reader_inferred = _lines(limits.get("reader_inferred"))
    boundary = _field(limits.get("boundary") or pick("boundary"))
    if stated:
        lines.append("## 论文承认的局限")
        lines.extend(f"- {item}" for item in stated)
    if reader_inferred:
        lines.append("## 读者推断的边界（依据见下）")
        lines.extend(f"- {item.get('boundary')}（依据：{item.get('basis')}）"
                     for item in reader_inferred if isinstance(item, dict))
    lines.append(f"- 迁移边界：{boundary}")
    lines.append("")

    lines.append("## 写作契约")
    lines.append("- 允许的输入：本简报、池内 paper.md（唯一补充来源）、风格参考（路径见任务说明）。")
    lines.append(f"- 输出 slide-source DSL（不是 HTML、不是 Markdown 文章）；全册 ≥{MIN_SLIDES} 页，"
                 "首页 class: cover，每张内容页必填 verdict。")
    lines.append("- 引文只用 {{main}}（本篇论文，refs 由脚本提供）；数字只能来自简报素材或 paper.md。")
    lines.append("- 没有本地图片文件就完全不用 @fig；不要引用任何 URL 图片。")
    return "\n".join(lines) + "\n"


def build_refs(paper_id: str, meta: dict) -> dict:
    title = str(meta.get("title") or f"arXiv:{paper_id}")
    return {"main": {"title": title, "url": f"https://arxiv.org/abs/{paper_id}"}}


def build_agent_prompt(paper_id: str, pool_dir: Path) -> str:
    """Point the agent at local files; never inline their content."""
    return f"""为论文 {paper_id} 制作一份组会汇报（reveal.js 幻灯片）的 slide-source。

输入（本地文件，直接 Read，不要联网）：
1. 写作简报：{pool_dir / BRIEF_NAME}
2. 风格参考（DSL 语法、页面结构、密度红线，必须遵守）：{STYLE_REFERENCE}
3. 论文全文（仅当简报某节标注「（笔记未提供，需从 paper.md 核对）」时才去核对，不得引入简报之外的数字或论文）：{pool_dir / 'paper.md'}

任务：按风格参考的 DSL 写出完整 slide-source，按主题组织（问题 → 方法 → 结果 → 局限 → 启示），
不要按论文章节顺序照抄。
- 只输出两个标记之间的内容，不要写文件，不要跑命令，不要输出标记之外的任何文字。
- 文档头必须含 # title / # subtitle；不要写 # refs（脚本提供）；首页 class: cover；每张内容页带 verdict。
- 引文只用 {{{{main}}}}；不用 @fig；简报未支撑的判断写「论文未给出」。

{SOURCE_OPEN}
（在此输出 slide-source DSL）
{SOURCE_CLOSE}"""


def extract_source(raw: str, allowed_keys: frozenset[str] = frozenset({"main"})) -> str | None:
    """Slice the slide-source between sentinels and sanity-check the shape."""
    if not raw:
        return None
    start = raw.find(SOURCE_OPEN)
    end = raw.find(SOURCE_CLOSE)
    if start < 0 or end <= start:
        return None
    source = raw[start + len(SOURCE_OPEN):end].strip()
    if len(source) < 800:
        return None
    if "class: cover" not in source:
        return None
    page_breaks = len(re.findall(r"(?m)^---\s*$", source))
    if page_breaks < MIN_SLIDES:  # N breaks -> N content/aux pages (meta head excluded)
        return None
    keys = set(re.findall(r"\{\{([A-Za-z0-9][A-Za-z0-9_.-]*)\}\}", source))
    if keys - allowed_keys:
        return None
    if "data:image" in source or re.search(r"@fig\s+https?://", source):
        return None
    return source + "\n"


def describe_rejection(raw: str, allowed_keys: frozenset[str] = frozenset({"main"})) -> str:
    start = raw.find(SOURCE_OPEN)
    end = raw.find(SOURCE_CLOSE)
    if start < 0 or end <= start:
        return "哨兵缺失或顺序错误"
    source = raw[start + len(SOURCE_OPEN):end].strip()
    if len(source) < 800:
        return "slide-source 不足 800 字符"
    if "class: cover" not in source:
        return "缺少 class: cover 首页"
    if len(re.findall(r"(?m)^---\s*$", source)) < MIN_SLIDES:
        return f"页数不足（分隔符少于 {MIN_SLIDES} 个）"
    keys = set(re.findall(r"\{\{([A-Za-z0-9][A-Za-z0-9_.-]*)\}\}", source))
    if keys - allowed_keys:
        return f"引文键超出白名单：{sorted(keys - allowed_keys)}"
    return "包含外链图片"


def compile_and_audit(pool_dir: Path, with_audit: bool = True) -> tuple[bool, list[dict]]:
    """Compile slide-source -> HTML, then optionally audit. Returns (ok, findings)."""
    refs_path = pool_dir / REFS_NAME
    html_path = pool_dir / DECK_NAME
    errors: list[str] = []
    try:
        html, _summary = bsd.compile_deck(pool_dir / SOURCE_NAME, refs_path, errors)
    except bsd.CompileError as exc:
        log(f"编译失败：{exc}")
        return False, [{"severity": "error", "check": "compile", "message": str(exc)}]
    if errors:
        for err in errors:
            log(f"校验失败：{err}")
        return False, [{"severity": "error", "check": "validate", "message": e} for e in errors]
    atomic_write_text(html_path, html)
    log(f"幻灯片已编译：{html_path}")
    if not with_audit:
        return True, []

    result = subprocess.run(
        [sys.executable, str(AUDIT_SCRIPT), "audit-slide-deck",
         "--source", str(pool_dir / SOURCE_NAME), "--refs", str(refs_path),
         "--html", str(html_path), "--json"],
        cwd=str(SCRIPTS_DIR), text=True, capture_output=True, timeout=60.0, check=False,
    )
    try:
        findings = json.loads(result.stdout or "{}").get("findings", [])
    except json.JSONDecodeError:
        log(f"审计输出无法解析：exit {result.returncode}")
        findings = []
    for finding in findings:
        log(f"审计 {finding.get('severity')}: [{finding.get('check')}] {finding.get('message')}")
    return True, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--kb-root", default=str(Path.home() / "Documents" / "arxiv"))
    parser.add_argument("--force", action="store_true",
                        help="Re-extract / re-deep-read / rewrite the deck even when cached.")
    parser.add_argument("--skip-agent", action="store_true",
                        help="Write only the brief (debugging); no deck.")
    parser.add_argument("--no-audit", action="store_true", help="Skip the audit after compiling.")
    args = parser.parse_args(argv)

    try:
        paper_id = normalize_arxiv_id(args.arxiv_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    pool_root = pool_root_for(args.kb_root)
    pool_dir = pool_root / f"arxiv-{paper_id}"
    brief_path = pool_dir / BRIEF_NAME
    source_path = pool_dir / SOURCE_NAME
    log(f"准备论文 {paper_id}")

    if not ensure_extraction(paper_id, pool_root, args.force):
        log("入池失败，无法继续")
        return 1

    status = ensure_deep_read(paper_id, pool_root, resolve_cli(), args.force)
    if status not in {"pass", "needs-review"}:
        log(f"深读不可用（{status}），汇报必须基于审计过的深读笔记，拒绝生成")
        return 3

    try:
        note = json.loads((pool_dir / "note.json").read_text(encoding="utf-8"))
        meta_path = pool_dir / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    except (json.JSONDecodeError, OSError) as exc:
        log(f"读取深读笔记失败：{exc}")
        return 1
    # Same lock discipline as quick_read_paper: only the short read-merge-write
    # critical sections hold the lock, never the minutes-long agent call.
    with locks.kb_lock(pool_root, f"pool-paper__{pool_dir.name}"):
        atomic_write_text(brief_path, build_slide_brief(paper_id, note, meta))
        atomic_write_text(pool_dir / REFS_NAME,
                          json.dumps(build_refs(paper_id, meta), ensure_ascii=False, indent=2) + "\n")
    log(f"写作简报已更新：{brief_path}")

    if args.skip_agent:
        log("已按要求跳过制作（--skip-agent）")
        print(json.dumps({"arxiv_id": paper_id, "pool_dir": str(pool_dir), "deep_read": status,
                          "slide_deck": False, "cached": False, "deck_path": None,
                          "brief_path": str(brief_path),
                          "ts": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False))
        return 0

    note_mtime = (pool_dir / "note.json").stat().st_mtime
    if (source_path.is_file() and (pool_dir / DECK_NAME).is_file()
            and not args.force and source_path.stat().st_mtime >= note_mtime):
        log(f"幻灯片缓存命中：{pool_dir / DECK_NAME}")
        ok, findings = compile_and_audit(pool_dir, with_audit=not args.no_audit)
        print(json.dumps({"arxiv_id": paper_id, "pool_dir": str(pool_dir), "deep_read": status,
                          "slide_deck": ok, "cached": True, "deck_path": str(pool_dir / DECK_NAME),
                          "source_path": str(source_path), "audit": findings,
                          "ts": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False))
        return 0 if ok else 1

    cli = resolve_cli()
    if not cli:
        log("claude CLI 不存在，无法制作汇报")
        return 1
    log("slide-source 写作 agent 启动…")
    raw_dump_path = pool_dir / RAW_DUMP_NAME
    source = None
    for attempt in (1, 2):
        if attempt == 2:
            log("第 1 次输出无效，重试…")
        try:
            completed = complete(
                build_agent_prompt(paper_id, pool_dir),
                timeout_s=SOURCE_TIMEOUT_S,
                cli=cli,
            )
        except subprocess.TimeoutExpired:
            log(f"slide-source 写作 agent 超时（{SOURCE_TIMEOUT_S:.0f}s）")
            return 1
        source = extract_source(completed.stdout or "")
        if source is not None:
            break
        raw = completed.stdout or ""
        # Dump verbatim before rejecting — without this the failure is undiagnosable.
        with locks.kb_lock(pool_root, f"pool-paper__{pool_dir.name}"):
            atomic_write_text(raw_dump_path, raw)
        log(f"agent 输出无效（{describe_rejection(raw)}），已转储：{raw_dump_path}")
    if source is None:
        log("重试后仍无有效 slide-source，已丢弃")
        return 1
    with locks.kb_lock(pool_root, f"pool-paper__{pool_dir.name}"):
        atomic_write_text(source_path, source)
    log(f"slide-source 已写入：{source_path}")

    ok, findings = compile_and_audit(pool_dir, with_audit=not args.no_audit)

    print(json.dumps({"arxiv_id": paper_id, "pool_dir": str(pool_dir), "deep_read": status,
                      "slide_deck": ok, "cached": False, "deck_path": str(pool_dir / DECK_NAME),
                      "source_path": str(source_path), "audit": findings,
                      "ts": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

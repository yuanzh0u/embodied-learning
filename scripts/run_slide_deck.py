#!/usr/bin/env python3
"""Generate a run-level slide deck (汇报展示) from a review run folder.

Run-level sibling of paper_slide_deck.py (single-paper 组会汇报). Pipeline:

    1. validate   — run dir with run.json + writing-brief.md + evidence-appendix.md
    2. refs       — parse refs.json from the evidence appendix's References
                    section (keys are the appendix's own reference labels,
                    i.e. arXiv IDs — the deck cites {{2505.11709}}-style)
    3. source     — one-shot agent writes the slide-source DSL between
                    sentinels from the writing brief + evidence appendix +
                    style reference; invalid output gets one retry, rejected
                    output is dumped verbatim to slide-deck-agent-raw.txt
    4. compile    — build_slide_deck.py compiles slide-deck_report.html
                    (shared with paper_slide_deck.py, including the audit)

Outputs land in the run dir (per-run outputs are lock-free per convention):
slide-deck_report.md (slide-source, source of truth) + slide-deck_report.html
(refresh the wiki snapshot to flip the topic page's 汇报放映 entry).

Exit codes: 0 deck written, 2 invalid run dir / no references, 1 hard failure.
Progress prints one ``[SLIDE-DECK] <stage> <detail>`` line per step. The final
stdout line is machine-readable JSON.
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
    from lib.layout import find_roots  # noqa: E402
except ImportError:  # installed console-script entry: package import path
    from wiki_scripts.lib.layout import find_roots  # noqa: E402
# AI-model capability goes through the harness binding (pybind-style); prompts and KB layout stay with the feature module.
from embodied_learning.harness.claude import complete, resolve_cli  # noqa: E402
import paper_slide_deck as psd  # noqa: E402  (sibling: sentinels, guards, compile+audit)

SKILLS_ROOT = find_roots()[1]
STYLE_REFERENCE = SKILLS_ROOT / "embodied-ai-review-writer" / "references" / "slide-deck.md"

SOURCE_NAME = psd.SOURCE_NAME
DECK_NAME = psd.DECK_NAME
REFS_NAME = psd.REFS_NAME
BRIEF_NAME = "writing-brief.md"
APPENDIX_NAME = "evidence-appendix.md"
RAW_DUMP_NAME = psd.RAW_DUMP_NAME

# Evidence appendix reference line: `- `2505.11709` [Title](https://arxiv.org/abs/2505.11709) (2025)`
_APPENDIX_REF_RE = re.compile(
    r"^- `([^`]+)`\s+\[([^\]]+)\]\((https?://[^)\s]+)\)", re.M)


def log(message: str) -> None:
    print(f"[SLIDE-DECK] {message}", flush=True)


def sanitize_key(label: str) -> str:
    key = re.sub(r"[^A-Za-z0-9_.-]", "_", str(label).strip())
    if not re.match(r"^[A-Za-z0-9]", key):
        key = f"r{key}"
    return key or "ref"


def parse_appendix_refs(appendix_text: str) -> dict[str, dict[str, str]]:
    """refs.json from the evidence appendix's References section. Keys are the
    appendix's own reference labels; collisions after sanitization get _2/_3."""
    refs: dict[str, dict[str, str]] = {}
    for match in _APPENDIX_REF_RE.finditer(appendix_text):
        label, title, url = match.group(1).strip(), match.group(2).strip(), match.group(3).strip()
        key = sanitize_key(label)
        suffix = 2
        while key in refs and refs[key]["url"] != url:
            key = f"{sanitize_key(label)}_{suffix}"
            suffix += 1
        refs.setdefault(key, {"title": title, "url": url})
    return refs


def build_agent_prompt(run_dir: Path, refs: dict) -> str:
    """Point the agent at local files; never inline their content."""
    ref_lines = "\n".join(
        f"- {{{{{key}}}}} → {info['title']}" for key, info in sorted(refs.items()))
    return f"""为综述 run 制作一份汇报（reveal.js 幻灯片）的 slide-source。

输入（本地文件，直接 Read，不要联网）：
1. 写作简报（内容与组织的唯一依据）：{run_dir / BRIEF_NAME}
2. 证据附录（引文来源，含 References）：{run_dir / APPENDIX_NAME}
3. 风格参考（DSL 语法、页面结构、密度红线，必须遵守）：{STYLE_REFERENCE}

可用引文键（refs 已由脚本生成，正文只用这些键，禁止自造）：
{ref_lines}

任务：按主题组织汇报（背景 → 谱系 → 对比 → 机制 → 局限 → 启示），
不要按任何一篇文章的章节顺序照抄；每页一个论点、页底 verdict。
- 只输出两个标记之间的内容，不要写文件，不要跑命令，不要输出标记之外的任何文字。
- 文档头必须含 # title / # subtitle；不要写 # refs（脚本提供）；首页 class: cover；每张内容页带 verdict。
- 没有 @fig 指令可用的本地图片，完全不用 @fig；不要引用任何 URL 图片。
- 简报未支撑的判断不要写；保留 可能/仅/尚未/在……条件下 等限定词。

{psd.SOURCE_OPEN}
（在此输出 slide-source DSL）
{psd.SOURCE_CLOSE}"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True,
                        help="review run folder (literature-review-<topic>-<date>/)")
    parser.add_argument("--skip-agent", action="store_true",
                        help="Write only refs.json (debugging); no deck.")
    parser.add_argument("--no-audit", action="store_true",
                        help="Compile without running the editorial audit.")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate the slide-source even when cached.")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).expanduser().resolve()
    brief_path = run_dir / BRIEF_NAME
    appendix_path = run_dir / APPENDIX_NAME
    source_path = run_dir / SOURCE_NAME
    if not (run_dir / "run.json").is_file():
        print(f"不是 run 目录（缺 run.json）：{run_dir}", file=sys.stderr)
        return 2
    if not brief_path.is_file() or not appendix_path.is_file():
        print(f"run 目录缺少 {BRIEF_NAME} 或 {APPENDIX_NAME}：{run_dir}", file=sys.stderr)
        return 2

    try:
        refs = parse_appendix_refs(appendix_path.read_text(encoding="utf-8"))
    except OSError as exc:
        log(f"读取证据附录失败：{exc}")
        return 1
    if not refs:
        log("证据附录没有可解析的 References，无法生成带引文的汇报")
        return 2
    (run_dir / REFS_NAME).write_text(
        json.dumps(refs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    log(f"引文键表已写入：{run_dir / REFS_NAME}（{len(refs)} 键）")

    if args.skip_agent:
        log("已按要求跳过制作（--skip-agent）")
        print(json.dumps({"run_dir": str(run_dir), "slide_deck": False,
                          "refs": len(refs),
                          "ts": dt.datetime.now(dt.timezone.utc).isoformat()},
                         ensure_ascii=False))
        return 0

    note_mtime = 0.0
    for probe in (brief_path, appendix_path):
        note_mtime = max(note_mtime, probe.stat().st_mtime)
    if (source_path.is_file() and (run_dir / DECK_NAME).is_file()
            and not args.force and source_path.stat().st_mtime >= note_mtime):
        log(f"幻灯片缓存命中：{run_dir / DECK_NAME}")
        ok, findings = psd.compile_and_audit(run_dir, with_audit=not args.no_audit)
        print(json.dumps({"run_dir": str(run_dir), "slide_deck": ok, "cached": True,
                          "deck_path": str(run_dir / DECK_NAME), "audit": findings,
                          "ts": dt.datetime.now(dt.timezone.utc).isoformat()},
                         ensure_ascii=False))
        return 0 if ok else 1

    cli = resolve_cli()
    if not cli:
        log("claude CLI 不存在，无法制作汇报")
        return 1
    allowed_keys = frozenset(refs)
    log("slide-source 写作 agent 启动…")
    raw_dump_path = run_dir / RAW_DUMP_NAME
    source = None
    for attempt in (1, 2):
        if attempt == 2:
            log("第 1 次输出无效，重试…")
        try:
            completed = complete(
                build_agent_prompt(run_dir, refs),
                timeout_s=psd.SOURCE_TIMEOUT_S,
                cli=cli,
            )
        except subprocess.TimeoutExpired:
            log(f"slide-source 写作 agent 超时（{psd.SOURCE_TIMEOUT_S:.0f}s）")
            return 1
        source = psd.extract_source(completed.stdout or "", allowed_keys=allowed_keys)
        if source is not None:
            break
        raw = completed.stdout or ""
        # Dump verbatim before rejecting — without this the failure is undiagnosable.
        raw_dump_path.write_text(raw, encoding="utf-8")
        log(f"agent 输出无效（{psd.describe_rejection(raw, allowed_keys=allowed_keys)}），已转储：{raw_dump_path}")
    if source is None:
        log("重试后仍无有效 slide-source，已丢弃")
        return 1
    source_path.write_text(source, encoding="utf-8")
    log(f"slide-source 已写入：{source_path}")

    ok, findings = psd.compile_and_audit(run_dir, with_audit=not args.no_audit)
    print(json.dumps({"run_dir": str(run_dir), "slide_deck": ok, "cached": False,
                      "deck_path": str(run_dir / DECK_NAME), "audit": findings,
                      "ts": dt.datetime.now(dt.timezone.utc).isoformat()},
                     ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

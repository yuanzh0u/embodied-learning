#!/usr/bin/env python3
"""Write one single-paper quick-read card (速读) into the public pool.

Single-paper pipeline, sibling of prepare_paper_chat.py:

    1. pool check   — reuse ensure_extraction (idempotent)
    2. deep read    — MANDATORY: reuse ensure_deep_read; no audited note,
                      no card
    3. brief        — build_quick_read_brief renders note.json + meta.json
                      into quick-read-brief.md (deterministic, cheap)
    4. article      — one-shot agent drafts the card from the brief + style
                      reference between sentinels; the script (never the
                      agent) writes pool/arxiv-<id>/quick-read_sudu.md
    5. audit        — optional editorial audit (warnings only, non-fatal)

Exit codes: 0 card written (or cache hit), 3 deep-read unavailable
(opposite of paper-chat semantics — callers must not treat 3 as success),
1 hard failure. Progress prints one ``[QUICK-READ] <stage> <detail>`` line
per step; reused stages print ``[PAPER-CHAT]`` lines. The final stdout line
is machine-readable JSON.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from lib.agent_invoke import pool_root_for, resolve_cli, run_one_shot_agent  # noqa: E402
from prepare_paper_chat import ensure_deep_read, ensure_extraction, normalize_arxiv_id  # noqa: E402

ARTICLE_NAME = "quick-read_sudu.md"
BRIEF_NAME = "quick-read-brief.md"
ARTICLE_TIMEOUT_S = 300.0
AUDIT_SCRIPT = REPO_ROOT / "skills" / "embodied-ai-review-writer" / "scripts" / "writing_audit.py"
STYLE_REFERENCE = REPO_ROOT / "skills" / "embodied-ai-review-writer" / "references" / "quick-read.md"
CITATION_REFERENCE = REPO_ROOT / "skills" / "embodied-ai-review-writer" / "references" / "citation-projection.md"
ARTICLE_OPEN = "<<<QUICK-READ-ARTICLE>>>"
ARTICLE_CLOSE = "<<<END-QUICK-READ-ARTICLE>>>"

UNPROVIDED = "（笔记未提供，需从 paper.md 核对）"


def log(message: str) -> None:
    print(f"[QUICK-READ] {message}", flush=True)


def _lines(items) -> list[str]:
    return [str(item).strip() for item in items or [] if str(item).strip()]


def _field(value) -> str:
    text = str(value or "").strip()
    return text if text else UNPROVIDED


def build_quick_read_brief(paper_id: str, note: dict, meta: dict) -> str:
    """Render note.json + meta.json into the writing brief. Pure stdlib; every
    fact the agent may cite appears here verbatim or is marked unprovided."""
    paper = note.get("paper") or {}
    review = note.get("review") or {}
    reading = note.get("reading") or {}
    relevance = reading.get("relevance") or {}
    method = note.get("method") or {}
    study = note.get("study_context") or {}
    evaluation = note.get("evaluation") or {}
    findings = note.get("findings") or []
    limitations = note.get("limitations") or {}
    boundary = note.get("transfer_boundary")
    appraisal = note.get("critical_appraisal") or {}

    lines: list[str] = []
    title = _field(paper.get("title") or meta.get("title"))
    lines.append(f"# 速读写作简报：{paper_id}")
    lines.append("")
    lines.append(f"- 标题：{title}")
    lines.append(f"- URL：{_field(paper.get('url') or meta.get('url'))}")
    lines.append(f"- 发表时间：{_field(paper.get('published') or meta.get('published'))}")
    lines.append(f"- 论文类型：{_field(reading.get('paper_type'))}")
    lines.append(f"- 抽取质量：{_field((note.get('extraction') or {}).get('quality') or meta.get('quality'))}")
    lines.append(f"- 深读模式：{_field(review.get('mode'))}")
    if _field(relevance.get("reason")) != UNPROVIDED:
        lines.append(f"- 相关性理由：{relevance.get('reason')}")
    lines.append("")

    lines.append("## 一句话定位素材")
    lines.append(f"- 研究问题：{_field(note.get('research_question'))}")
    lines.append("- 贡献：")
    contributions = _lines(note.get("contributions"))
    lines.extend(f"  - {item}" for item in contributions) if contributions else lines.append(f"  - {UNPROVIDED}")
    lines.append("")

    lines.append("## 问题与动机素材")
    lines.append(f"- （取研究问题与贡献中的动机表述，2-4 句）")
    lines.append("")

    lines.append("## 方法步骤素材")
    lines.append(f"- 方法摘要：{_field(method.get('summary'))}")
    lines.append("")

    lines.append("## 关键结果与数字素材（唯一允许的数字来源）")
    cards = note.get("evidence_cards") or []
    if cards:
        for card in cards:
            quantitative = card.get("quantitative")
            card_line = f"- 主张：{card.get('claim')}"
            if isinstance(quantitative, dict) and quantitative:
                card_line += f"（{quantitative.get('metric')} {quantitative.get('value_or_direction')} {quantitative.get('comparator')}）"
            lines.append(card_line)
            context = str(card.get("source_context") or "").strip()
            if context:
                lines.append(f"  - 逐字原文：{context}")
    else:
        lines.append(f"- {UNPROVIDED}")
    lines.append("")

    lines.append("## 三分法评价素材")
    lines.append("- 创新点/性能/工作量需从上述贡献与结果推导；笔记未支撑的维度写「论文未给出」。")
    lines.append("")

    lines.append("## 局限与边界素材")
    author_stated = limitations.get("author_stated") or []
    lines.append("- 论文承认：")
    stated_items = [f"{item.get('limitation')}（locator: {item.get('locator')}）" for item in author_stated if item.get("limitation")]
    lines.extend(f"  - {item}" for item in stated_items) if stated_items else lines.append(f"  - {UNPROVIDED}")
    reader_inferred = limitations.get("reader_inferred") or []
    lines.append("- 读者推断：")
    inferred_items = [f"{item.get('boundary')}（依据：{item.get('basis')}）" for item in reader_inferred if item.get("boundary")]
    lines.extend(f"  - {item}" for item in inferred_items) if inferred_items else lines.append(f"  - {UNPROVIDED}")
    lines.append(f"- 迁移边界：{_field(boundary)}")
    lines.append("")

    design = _field(evaluation.get("design"))
    baselines = _lines(evaluation.get("baselines"))
    metrics = _lines(evaluation.get("metrics"))
    if design != UNPROVIDED or baselines or metrics:
        lines.append("## 评估设置（仅作背景，不额外引用）")
        lines.append(f"- 设计：{design}")
        if baselines:
            lines.append(f"- 基线：{'；'.join(baselines)}")
        if metrics:
            lines.append(f"- 指标：{'；'.join(metrics)}")
        lines.append("")

    datasets = _lines(study.get("datasets"))
    tasks = _lines(study.get("tasks"))
    embodiments = _lines(study.get("embodiments"))
    if datasets or tasks or embodiments:
        lines.append("## 研究语境（仅作背景）")
        if datasets:
            lines.append(f"- 数据集：{'；'.join(datasets)}")
        if tasks:
            lines.append(f"- 任务：{'；'.join(tasks)}")
        if embodiments:
            lines.append(f"- 具身体：{'；'.join(embodiments)}")
        lines.append("")

    design_strengths = _lines(appraisal.get("design_strengths"))
    design_risks = _lines(appraisal.get("design_risks"))
    if design_strengths or design_risks:
        lines.append("## 批判性评估（仅作三分法评价的参考）")
        if design_strengths:
            lines.extend(f"- 优点：{item}" for item in design_strengths)
        if design_risks:
            lines.extend(f"- 风险：{item}" for item in design_risks)
        lines.append("")

    lines.append("## 写作契约")
    lines.append(f"- 允许的输入：本简报、池内 paper.md（唯一补充来源）、风格参考与引用规范（路径见任务说明）。")
    lines.append("- 中文正文 600-1200 字（不含链接行）；禁止表格；固定 8 节结构。")
    lines.append(f"- 数字只能来自「关键结果与数字素材」；论文承认局限为空时按读者推断补足并标注。")
    lines.append(f"- 链接节固定为：[arXiv:{paper_id}](https://arxiv.org/abs/{paper_id})")
    lines.append("- 局限与边界一节不得为空。")
    return "\n".join(lines) + "\n"


def build_agent_prompt(paper_id: str, pool_dir: Path) -> str:
    """Point the agent at local files; never inline their content."""
    return f"""为论文 {paper_id} 撰写一张速读卡（quick-read card）。

输入（本地文件，直接 Read，不要联网）：
1. 写作简报：{pool_dir / BRIEF_NAME}
2. 风格参考（结构、语气、拒绝条件，必须遵守）：{STYLE_REFERENCE}
3. 引用投影规范：{CITATION_REFERENCE}
4. 论文全文（仅当简报某节标注「（笔记未提供，需从 paper.md 核对）」时才去核对，不得引入简报之外的数字或论文）：{pool_dir / 'paper.md'}

任务：按风格参考的固定结构输出一张中文速读卡。
- 只输出两个标记之间的内容，不要写文件，不要跑命令，不要输出标记之外的任何文字。
- 正文 600-1200 中文字符；禁表格；固定 8 节；链接节只有论文自己的 arXiv 链接。
- 简报未支撑的判断写「论文未给出」；保留 可能/仅/尚未/在……条件下 等限定词。

{ARTICLE_OPEN}
（在此输出速读卡 Markdown）
{ARTICLE_CLOSE}"""


def extract_article(raw: str, paper_id: str) -> str | None:
    """Slice the card between sentinels and sanity-check the shape."""
    if not raw:
        return None
    start = raw.find(ARTICLE_OPEN)
    end = raw.find(ARTICLE_CLOSE)
    if start < 0 or end <= start:
        return None
    article = raw[start + len(ARTICLE_OPEN) : end].strip()
    if len(article) < 300:
        return None
    if f"arxiv.org/abs/{paper_id}" not in article:
        return None
    if any(line.strip().startswith("|") for line in article.splitlines()):
        return None
    return article + "\n"


def audit_article(path: Path) -> None:
    """Editorial audit; findings are warnings only and never change the exit code."""
    result = subprocess.run(
        [sys.executable, str(AUDIT_SCRIPT), "audit-article-quality", "--quickread", str(path), "--json"],
        cwd=str(REPO_ROOT), text=True, capture_output=True, timeout=60.0, check=False,
    )
    try:
        findings = json.loads(result.stdout or "{}").get("findings", [])
    except json.JSONDecodeError:
        log(f"审计输出无法解析：exit {result.returncode}")
        return
    for finding in findings:
        log(f"审计 {finding.get('severity')}: [{finding.get('rule')}] {finding.get('message')}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--kb-root", default=str(Path.home() / "Documents" / "arxiv"))
    parser.add_argument("--force", action="store_true", help="Re-extract / re-deep-read / rewrite the card even when cached.")
    parser.add_argument("--skip-agent", action="store_true", help="Write only the brief (debugging); no article.")
    parser.add_argument("--no-audit", action="store_true", help="Skip the editorial audit after writing.")
    args = parser.parse_args(argv)

    try:
        paper_id = normalize_arxiv_id(args.arxiv_id)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    pool_root = pool_root_for(args.kb_root)
    pool_dir = pool_root / f"arxiv-{paper_id}"
    brief_path = pool_dir / BRIEF_NAME
    article_path = pool_dir / ARTICLE_NAME
    log(f"准备论文 {paper_id}")

    if not ensure_extraction(paper_id, pool_root, args.force):
        log("入池失败，无法继续")
        return 1

    status = ensure_deep_read(paper_id, pool_root, resolve_cli(), args.force)
    if status not in {"pass", "needs-review"}:
        log(f"深读不可用（{status}），速读卡必须基于审计过的深读笔记，拒绝生成")
        return 3

    try:
        note = json.loads((pool_dir / "note.json").read_text(encoding="utf-8"))
        meta_path = pool_dir / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    except (json.JSONDecodeError, OSError) as exc:
        log(f"读取深读笔记失败：{exc}")
        return 1
    brief_path.write_text(build_quick_read_brief(paper_id, note, meta), encoding="utf-8")
    log(f"写作简报已更新：{brief_path}")

    if args.skip_agent:
        log("已按要求跳过写作（--skip-agent）")
        print(json.dumps({"arxiv_id": paper_id, "pool_dir": str(pool_dir), "deep_read": status,
                          "quick_read": False, "cached": False, "article_path": None,
                          "brief_path": str(brief_path),
                          "ts": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False))
        return 0

    note_mtime = (pool_dir / "note.json").stat().st_mtime
    if article_path.is_file() and not args.force and article_path.stat().st_mtime >= note_mtime:
        log(f"速读卡缓存命中：{article_path}")
        if not args.no_audit:
            audit_article(article_path)
        print(json.dumps({"arxiv_id": paper_id, "pool_dir": str(pool_dir), "deep_read": status,
                          "quick_read": True, "cached": True, "article_path": str(article_path),
                          "brief_path": str(brief_path),
                          "ts": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False))
        return 0

    cli = resolve_cli()
    if not cli:
        log("claude CLI 不存在，无法写作速读卡")
        return 1
    log("速读写作 agent 启动…")
    try:
        completed = run_one_shot_agent(
            build_agent_prompt(paper_id, pool_dir),
            timeout_s=ARTICLE_TIMEOUT_S,
            cli=cli,
        )
    except subprocess.TimeoutExpired:
        log(f"速读写作 agent 超时（{ARTICLE_TIMEOUT_S:.0f}s）")
        return 1
    article = extract_article(completed.stdout or "", paper_id)
    if article is None:
        log("agent 输出缺少有效速读卡（哨兵缺失或结构不合规），已丢弃")
        return 1
    article_path.write_text(article, encoding="utf-8")
    log(f"速读卡已写入：{article_path}")

    if not args.no_audit:
        audit_article(article_path)

    print(json.dumps({"arxiv_id": paper_id, "pool_dir": str(pool_dir), "deep_read": status,
                      "quick_read": True, "cached": False, "article_path": str(article_path),
                      "brief_path": str(brief_path),
                      "ts": dt.datetime.now(dt.timezone.utc).isoformat()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

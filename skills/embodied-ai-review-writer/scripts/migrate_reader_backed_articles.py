#!/usr/bin/env python3
"""Revise legacy articles against a paper-reader-backed evidence set.

The script preserves mature prose blocks whose paper links remain in the new
accepted set, drops blocks that cite papers without complete readable full
text, inserts manually authored replacement arguments, and rebuilds compact
reader-facing references. It is intended for a controlled migration, not for
mechanically authoring new reviews from scratch.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ARXIV_RE = re.compile(r"https?://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?")
ARTICLE_FILES = {
    "memo": "scientific-memo_keyan.md",
    "zhihu": "zhihu-explainer_zhihu.md",
    "xiaohongshu": "xiaohongshu-post_xiaohongshu.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft-root", required=True)
    parser.add_argument("--source-root", default="evidence")
    parser.add_argument("--updates", required=True)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def strip_reference_tail(text: str, style: str) -> str:
    markers = ["\n## References"]
    if style == "zhihu":
        markers.append("\n## 延伸阅读")
    if style == "xiaohongshu":
        markers.append("\n📚")
    positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    return text[: min(positions)].rstrip() if positions else text.rstrip()


def drop_unsupported_blocks(text: str, unsupported: set[str]) -> str:
    blocks = re.split(r"\n\s*\n", text)
    kept: list[str] = []
    for block in blocks:
        cited = set(ARXIV_RE.findall(block))
        if cited & unsupported:
            continue
        kept.append(block.rstrip())
    return "\n\n".join(item for item in kept if item.strip()).strip()


def insert_after_heading(text: str, headings: list[str], value: str) -> str:
    for heading in headings:
        marker = heading + "\n"
        if marker in text:
            return text.replace(marker, marker + "\n" + value.strip() + "\n", 1)
    lines = text.splitlines()
    if lines:
        return lines[0] + "\n\n" + value.strip() + "\n\n" + "\n".join(lines[1:])
    return value.strip()


def insert_update(text: str, style: str, update: str) -> str:
    if not update.strip():
        return text
    markers = ["\n## 结论"] if style in {"memo", "zhihu"} else ["\n⚠️"]
    positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    if positions:
        index = min(positions)
        return text[:index].rstrip() + "\n\n" + update.strip() + "\n" + text[index:]
    return text.rstrip() + "\n\n" + update.strip()


def cited_order(text: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for paper_id in ARXIV_RE.findall(text):
        if paper_id not in seen:
            result.append(paper_id)
            seen.add(paper_id)
    return result


def reference_tail(style: str, paper_ids: list[str], metadata: dict[str, dict[str, Any]]) -> str:
    if style == "memo":
        lines = ["## References"]
        for paper_id in paper_ids:
            title = str(metadata[paper_id].get("title") or paper_id)
            lines.append(f"- [{title}](https://arxiv.org/abs/{paper_id})")
        return "\n".join(lines)
    if style == "zhihu":
        lines = ["## 延伸阅读"]
        for paper_id in paper_ids[:12]:
            title = str(metadata[paper_id].get("title") or paper_id)
            lines.append(f"- [{title}](https://arxiv.org/abs/{paper_id})")
        return "\n".join(lines)
    links = [f"[论文{index}](https://arxiv.org/abs/{paper_id})" for index, paper_id in enumerate(paper_ids[:5], start=1)]
    return "📚 依据：" + " · ".join(links) + "。"


def migrate_article(
    style: str,
    source: Path,
    target: Path,
    accepted_ids: set[str],
    metadata: dict[str, dict[str, Any]],
    update: str,
) -> dict[str, Any]:
    original = source.read_text(encoding="utf-8")
    legacy_citations = set(ARXIV_RE.findall(original))
    unsupported = legacy_citations - accepted_ids
    body = drop_unsupported_blocks(strip_reference_tail(original, style), unsupported)
    if style == "memo":
        scope = (
            "版本说明：本轮以 15 篇可获取完整正文的论文为论证主干，"
            "逐篇核对问题、方法、结果与限制；未能取得可读全文的论文不再承担正文结论。"
        )
        body = insert_after_heading(body, ["## 研究边界", "## 研究范围", "## 摘要"], scope)
    elif style == "zhihu":
        scope = (
            "这一版不只核对摘要，而是对 15 篇入选论文逐篇阅读方法、结果与局限。"
            "下文只保留能在完整正文中重新定位的判断。"
        )
        body = insert_after_heading(body, ["## TL;DR"], scope)
    else:
        scope = "这一版只保留已在完整正文中重新核对过的论文结论。"
        body = insert_after_heading(body, [], scope)

    body = insert_update(body, style, update)
    body_citations = cited_order(body)
    unknown = set(body_citations) - accepted_ids
    if unknown:
        raise ValueError(f"{target}: replacement prose cites papers outside accepted evidence: {sorted(unknown)}")
    minimum = {"memo": 5, "zhihu": 3, "xiaohongshu": 3}[style]
    maximum = {"memo": 999, "zhihu": 12, "xiaohongshu": 5}[style]
    selected = list(body_citations)
    for paper_id in metadata:
        if len(selected) >= minimum:
            break
        if paper_id not in selected:
            selected.append(paper_id)
    selected = selected[:maximum]
    target.write_text(body.rstrip() + "\n\n" + reference_tail(style, selected, metadata) + "\n", encoding="utf-8")
    return {
        "file": target.name,
        "removed_unreadable_paper_ids": sorted(unsupported),
        "final_cited_paper_ids": selected,
    }


def main() -> int:
    args = parse_args()
    draft_root = Path(args.draft_root)
    source_root = Path(args.source_root)
    updates = load_json(Path(args.updates))
    report: list[dict[str, Any]] = []
    for run in sorted(draft_root.glob("literature-review-*")):
        manifest = load_json(run / "run.json")
        source_name = str(manifest["source_runs"][0])
        source = source_root / source_name
        events = load_events(run / "evidence.jsonl")
        metadata: dict[str, dict[str, Any]] = {}
        for event in events:
            paper = event.get("paper") if isinstance(event.get("paper"), dict) else {}
            paper_id = str(paper.get("arxiv_id") or "")
            if paper_id:
                metadata.setdefault(paper_id, paper)
        accepted_ids = set(metadata)
        run_updates = updates.get(source_name, {}) if isinstance(updates, dict) else {}
        article_results: list[dict[str, Any]] = []
        for style, filename in ARTICLE_FILES.items():
            article_results.append(
                migrate_article(
                    style,
                    source / filename,
                    run / filename,
                    accepted_ids,
                    metadata,
                    str(run_updates.get(style) or ""),
                )
            )
        report.append({"run": run.name, "articles": article_results})
    output = draft_root / "article-migration-report.json"
    output.write_text(json.dumps({"schema_version": 1, "runs": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Migrated reader-backed articles for {len(report)} runs: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

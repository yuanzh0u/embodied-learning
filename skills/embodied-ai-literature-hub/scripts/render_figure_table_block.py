#!/usr/bin/env python3
"""Render a markdown figure/table block for a paper's extracted figures and tables.

The literature-review pipeline captures only each figure's *caption* and the
author's *usage* of it — never the image content. This helper turns those
records into a self-contained markdown snippet that an agent can paste into a
review deliverable (scientific memo, zhihu explainer, xiaohongshu post) or the
evidence appendix.

Figures render as an external arXiv `<img>` link (`![caption](image_url)`),
which the research wiki already turns into a real `<img>`. Tables render as a
markdown grid from their captured rows (LaTeXML tables have no image link).

The per-style *caps* on how many figures to include are a caller (agent)
decision; this script only emits the ids the caller asks for.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_NOTE_PATTERN = "evidence/*/paper-notes/*.json"


def _escape_cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ").strip()


def _caption_text(caption: str) -> str:
    """Flatten an extracted caption into a clean alt/display string.

    Drops a leading figure/table number tag (``Figure 3 :`` / ``Table 1 :``)
    so the alt text reads naturally, and replaces the extraction's ellipsis
    (``...``) with nothing so the text reads as a continuous caption.
    """
    text = re.sub(r"^\s*(?:Figure|Table)\s+\S+\s*:?\s*", "", caption, flags=re.IGNORECASE).strip()
    text = text.replace(" ... ", " ")
    text = text.replace("...", "")
    return " ".join(text.split())


def _rows_to_markdown(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    lines: list[str] = []
    for row_index, row in enumerate(rows):
        cells = [row[i] if i < len(row) else "" for i in range(width)]
        lines.append("| " + " | ".join(_escape_cell(cell) for cell in cells) + " |")
        if row_index == 0:
            lines.append("| " + " | ".join("---" for _ in range(width)) + " |")
    return "\n".join(lines)


def render_figure(figure: dict[str, object], paper_label: str) -> str:
    figure_id = str(figure.get("figure_id") or figure.get("id") or "")
    caption = _caption_text(str(figure.get("caption") or ""))
    image_url = str(figure.get("image_url") or "").strip()
    usage = str(figure.get("usage") or "").strip()
    lines: list[str] = []
    if image_url:
        lines.append(f"![{caption}]({image_url})")
    else:
        lines.append(f"*{caption or figure_id}*")
    if usage:
        lines.append(f"> 用法：{usage}（{paper_label}，{figure_id}）")
    return "\n\n".join(lines)


def render_table_block(table: dict[str, object], paper_label: str) -> str:
    table_id = str(table.get("table_id") or table.get("id") or "")
    caption = str(table.get("caption") or "").strip()
    usage = str(table.get("usage") or "").strip()
    rows = table.get("rows") or table.get("content") or []
    parts: list[str] = []
    if caption:
        parts.append(f"**{caption}**")
    if isinstance(rows, list) and rows:
        parts.append(_rows_to_markdown(rows))
    if usage:
        parts.append(f"> 用法：{usage}（{paper_label}，{table_id}）")
    return "\n\n".join(parts)


def find_event_figures(evidence_events: list[dict[str, object]], paper_id: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Collect figures/tables referenced by any event for the given paper, deduped."""
    figures: list[dict[str, object]] = []
    tables: list[dict[str, object]] = []
    seen_figures: set[str] = set()
    seen_tables: set[str] = set()
    for event in events_with_paper(evidence_events, paper_id):
        evidence = event.get("evidence")
        if not isinstance(evidence, dict):
            continue
        for figure in evidence.get("figures") or []:
            if not isinstance(figure, dict):
                continue
            key = str(figure.get("figure_id") or figure.get("id") or json.dumps(figure, sort_keys=True))
            if key not in seen_figures:
                seen_figures.add(key)
                figures.append(figure)
        for table in evidence.get("tables") or []:
            if not isinstance(table, dict):
                continue
            key = str(table.get("table_id") or table.get("id") or json.dumps(table, sort_keys=True))
            if key not in seen_tables:
                seen_tables.add(key)
                tables.append(table)
    return figures, tables


def events_with_paper(evidence_events: list[dict[str, object]], paper_id: str) -> list[dict[str, object]]:
    return [
        event
        for event in evidence_events
        if str(event.get("paper", {}).get("arxiv_id", "")) == paper_id
    ]


def paper_label(event: dict[str, object]) -> str:
    paper = event.get("paper") or {}
    title = str(paper.get("title") or "")
    arxiv_id = str(paper.get("arxiv_id") or "")
    return f"{title}（arXiv {arxiv_id}）" if title else arxiv_id


def load_events(path: str) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                events.append(json.loads(line))
    return events


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", help="Path to the run's evidence.jsonl.")
    parser.add_argument("--paper-id", help="arXiv ID of the paper whose figures/tables to render.")
    parser.add_argument("--figure-ids", help="Comma-separated figure ids to include (default: all).")
    parser.add_argument("--table-ids", help="Comma-separated table ids to include (default: all).")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.evidence_jsonl:
        print("Provide --evidence-jsonl (path to evidence.jsonl).", file=sys.stderr)
        return 1
    events = load_events(args.evidence_jsonl)
    paper_events = events_with_paper(events, args.paper_id)
    if not paper_events:
        print(f"No evidence events found for paper {args.paper_id}.", file=sys.stderr)
        return 1

    figures, tables = find_event_figures(events, args.paper_id)
    if args.figure_ids:
        wanted = {item.strip() for item in args.figure_ids.split(",") if item.strip()}
        figures = [f for f in figures if str(f.get("figure_id") or f.get("id")) in wanted]
    if args.table_ids:
        wanted = {item.strip() for item in args.table_ids.split(",") if item.strip()}
        tables = [t for t in tables if str(t.get("table_id") or t.get("id")) in wanted]

    label = paper_label(paper_events[0])
    blocks: list[str] = []
    for figure in figures:
        block = render_figure(figure, label)
        if block:
            blocks.append(block)
    for table in tables:
        block = render_table_block(table, label)
        if block:
            blocks.append(block)
    print("\n\n---\n\n".join(blocks) if blocks else "(no figures or tables recorded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
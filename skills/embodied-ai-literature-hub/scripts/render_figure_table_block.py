#!/usr/bin/env python3
"""CLI: render markdown figure/table blocks from captured captions.

Library API lives in embodied_learning/parse/figure_table.py (render_figure,
render_table_block, find_event_figures, load_events). This entry owns only
argument parsing and dispatch.
"""
import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.parse.figure_table import (  # noqa: E402
    events_with_paper,
    find_event_figures,
    load_events,
    paper_label,
    render_figure,
    render_table_block,
)


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

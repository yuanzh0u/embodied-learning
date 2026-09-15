#!/usr/bin/env python3
"""parse-layer CLI: one entry, one subcommand per tool.

Each subcommand owns its original flags (per-subcommand parsers, so legacy
flag names never collide); implementation lives in the embodied_learning
parse layer. Subcommand names are the old single-purpose scripts
kebab-cased: `write-lit-outputs` was `scripts/write_lit_outputs.py`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# ---- write-lit-outputs (was scripts/write_lit_outputs.py) -----------------------

import argparse
import json

from embodied_learning.parse.brief import load_events, render_brief  # noqa: E402


def _write_lit_outputs_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", required=True)
    parser.add_argument("--brief-out")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args(argv)


def _write_lit_outputs_main(argv: list[str] | None = None) -> int:
    args = _write_lit_outputs_parse_args(argv)
    events = load_events(Path(args.evidence_jsonl))
    result = {"valid": True, "event_count": len(events)}
    if args.brief_out and not args.validate_only:
        Path(args.brief_out).write_text(render_brief(events), encoding="utf-8")
        result["brief_out"] = args.brief_out
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

# ---- render-figure-table-block (was scripts/render_figure_table_block.py) ---------------

import argparse

from embodied_learning.parse.figure_table import (  # noqa: E402
    events_with_paper,
    find_event_figures,
    load_events,
    paper_label,
    render_figure,
    render_table_block,
)


def _render_figure_table_block_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", help="Path to the run's evidence.jsonl.")
    parser.add_argument("--paper-id", help="arXiv ID of the paper whose figures/tables to render.")
    parser.add_argument("--figure-ids", help="Comma-separated figure ids to include (default: all).")
    parser.add_argument("--table-ids", help="Comma-separated table ids to include (default: all).")
    return parser.parse_args(argv)


def _render_figure_table_block_main(argv: list[str] | None = None) -> int:
    args = _render_figure_table_block_parse_args(argv)
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



_SUBCOMMANDS = {
    "write-lit-outputs": _write_lit_outputs_main,
    "render-figure-table-block": _render_figure_table_block_main,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch to the tool's own parser: `{layer}.py <subcommand> [flags...]`.

    Each subcommand reuses its original single-purpose parser verbatim, so
    flags, help text, and exit codes are unchanged from the old scripts.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 0
    handler = _SUBCOMMANDS.get(argv[0])
    if handler is None:
        print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 2
    return handler(argv[1:])


if __name__ == "__main__":
    sys.exit(main())

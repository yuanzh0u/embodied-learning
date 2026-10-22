#!/usr/bin/env python3
"""Writer-domain CLI: review packets, editorial audits, slide decks.

This entry owns the argparse flag tables and argv handling; the business logic
lives in ``embodied_learning.writer.*`` as ``run(args) -> int`` (no argparse,
no ``main`` in the library — see docs/adr/0005).
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

from embodied_learning.utils.layout import find_roots  # noqa: E402

REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()

_MODULES: dict[str, str] = {
    "review-packet": "embodied_learning.writer.packet",
    "build-trace-map": "embodied_learning.writer.trace_map",
    "audit-article-quality": "embodied_learning.writer.quality",
    "audit-zhihu-corpus": "embodied_learning.writer.zhihu_corpus",
    "audit-slide-deck": "embodied_learning.writer.slide_audit",
    "check-deep-read-budget": "embodied_learning.writer.budget",
    "project-outline-evidence": "embodied_learning.writer.outline",
    "compile-slide-deck": "embodied_learning.writer.slide_compile",
    "paper-deck": "embodied_learning.writer.deck",
    "run-deck": "embodied_learning.writer.run_deck",
}

_HELP: dict[str, str] = {
    "review-packet": "render review-packet + writing-brief + evidence-appendix",
    "build-trace-map": "build trace-map.json from deliverables + evidence",
    "audit-article-quality": "editorial-quality audit of deliverables",
    "audit-zhihu-corpus": "corpus-level Zhihu style audit",
    "audit-slide-deck": "slide-deck content audit (source + compiled HTML)",
    "check-deep-read-budget": "deep-read budget vs evidence floor",
    "project-outline-evidence": "project outline claims against evidence events",
    "compile-slide-deck": "compile slide-source DSL into reveal.js HTML",
    "paper-deck": "single-paper slide deck (agent writes slide-source)",
    "run-deck": "run-level slide deck (agent writes slide-source)",
}

_PARSER_LOOKUP = {
    "review-packet": "_packet_parser",
    "build-trace-map": "_trace_map_parser",
    "audit-article-quality": "_quality_parser",
    "audit-zhihu-corpus": "_zhihu_corpus_parser",
    "audit-slide-deck": "_slide_audit_parser",
    "check-deep-read-budget": "_budget_parser",
    "project-outline-evidence": "_outline_parser",
    "compile-slide-deck": "_slide_compile_parser",
    "paper-deck": "_deck_parser",
    "run-deck": "_run_deck_parser",
}

_PARSERS: dict[str, object] = {}


def _packet_parser() -> argparse.ArgumentParser:
    parser = packet.build_parser()
    return parser



def _trace_map_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=trace_map.__doc__)
    parser.add_argument("--evidence-jsonl", action="append", required=True, help="Accepted evidence JSONL; repeatable.")
    parser.add_argument("--article", action="append", required=True, help="Reader-facing article Markdown; repeatable.")
    parser.add_argument("--output", required=True, help="Output trace-map.json path.")
    return parser



def _quality_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=quality.__doc__)
    parser.add_argument("--bundle-dir", help="Directory containing a standard or reduced-scope review bundle.")
    parser.add_argument("--memo", help="Scientific memo Markdown path.")
    parser.add_argument("--zhihu", help="Zhihu explainer Markdown path.")
    parser.add_argument("--xiaohongshu", help="Xiaohongshu post Markdown path.")
    parser.add_argument("--quickread", help="Single-paper quick-read card Markdown path.")
    parser.add_argument("--evidence-jsonl", help="Evidence JSONL; enables the figures-available warning.")
    parser.add_argument("--min-chinese-share", type=float, default=0.65)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser



def _zhihu_corpus_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=zhihu_corpus.__doc__)
    parser.add_argument("--topics-dir", required=True, help="Directory containing topic JSON files with source_directory fields.")
    parser.add_argument("--project-root", default=".", help="Root used to resolve relative source_directory values.")
    parser.add_argument("--min-chinese-share", type=float, default=0.65)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser



def _slide_audit_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="audit-slide-deck", description=slide_audit.__doc__)
    parser.add_argument("--source", required=True, help="slide-deck_report.md")
    parser.add_argument("--refs", help="引文键表 JSON（默认读 source 头的 # refs:）")
    parser.add_argument("--html", help="已编译的 slide-deck_report.html")
    parser.add_argument("--json", action="store_true", help="stdout 输出 JSON")
    return parser



def _budget_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=budget.__doc__)
    parser.add_argument("--reading-summary", required=True, help="reading-summary.json")
    parser.add_argument(
        "--review-mode",
        choices=sorted(budget.MODE_FLOORS),
        help="Mode used to derive the accepted-paper floor",
    )
    parser.add_argument(
        "--accepted-floor",
        type=int,
        help="Override accepted-paper floor (else from --review-mode or summary)",
    )
    parser.add_argument(
        "--budget-offset",
        type=int,
        default=budget.DEFAULT_OFFSET,
        help=f"deep_read_budget = floor + offset (default {budget.DEFAULT_OFFSET})",
    )
    parser.add_argument(
        "--budget",
        type=int,
        help="Absolute deep-read budget; overrides floor+offset",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when over budget (default: warn only, exit 0)",
    )
    parser.add_argument("--json", action="store_true", help="Machine-readable report")
    return parser



def _outline_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=outline.__doc__)
    parser.add_argument(
        "--outline",
        required=True,
        help="Outline JSON with thesis + event_ids (see schema in docs)",
    )
    parser.add_argument(
        "--evidence-jsonl",
        action="append",
        required=True,
        help="Accepted evidence JSONL; repeatable",
    )
    parser.add_argument("--output", required=True, help="Projected cards JSON")
    parser.add_argument("--markdown-output", help="Optional short markdown for LLM prompts")
    parser.add_argument("--max-claim-chars", type=int, default=outline.DEFAULT_MAX_CLAIM)
    parser.add_argument("--max-summary-chars", type=int, default=outline.DEFAULT_MAX_SUMMARY)
    parser.add_argument("--max-quote-chars", type=int, default=outline.DEFAULT_MAX_QUOTE)
    return parser



def _slide_compile_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=slide_compile.__doc__.split("\n")[0])
    parser.add_argument("--source", required=True, help="slide-source DSL markdown")
    parser.add_argument("--output", required=True, help="single-file reveal.js HTML")
    parser.add_argument("--refs", help="citation key -> {title,url} JSON (overrides # refs:)")
    parser.add_argument("--qa", help="screenshot every slide into this directory")
    return parser



def _deck_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=deck.__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--kb-root", default=str(Path.home() / "Documents" / "arxiv"))
    parser.add_argument("--force", action="store_true",
                        help="Re-extract / re-deep-read / rewrite the deck even when cached.")
    parser.add_argument("--skip-agent", action="store_true",
                        help="Write only the brief (debugging); no deck.")
    parser.add_argument("--no-audit", action="store_true", help="Skip the audit after compiling.")
    return parser



def _run_deck_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=run_deck.__doc__)
    parser.add_argument("--run-dir", required=True,
                        help="review run_deck.run folder (literature-review-<topic>-<date>/)")
    parser.add_argument("--skip-agent", action="store_true",
                        help="Write only refs.json (debugging); no deck.")
    parser.add_argument("--no-audit", action="store_true",
                        help="Compile without running the editorial audit.")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate the slide-source even when cached.")
    return parser
def _parser_for(name: str):
    if name not in _PARSERS:
        globals().update({m.split(".")[-1]: importlib.import_module(m) for m in set(_MODULES.values())})
        _PARSERS[name] = globals()[_PARSER_LOOKUP[name]]()
    return _PARSERS[name]


def usage() -> str:
    lines = ["usage: write.py <subcommand> [args]", "", "subcommands:"]
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
        print(f"write.py: unknown subcommand {name!r}\n\n{usage()}", file=sys.stderr)
        return 2
    parser = _parser_for(name)
    parser.prog = name
    args = parser.parse_args(rest)
    mod = importlib.import_module(_MODULES[name])
    return int(mod.run(args) or 0)


def main(argv: list[str] | None = None) -> int:
    return dispatch(list(sys.argv[1:] if argv is None else argv))


def paper_deck_main() -> int:
    return dispatch(["paper-deck", *sys.argv[1:]])


def run_deck_main() -> int:
    return dispatch(["run-deck", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())

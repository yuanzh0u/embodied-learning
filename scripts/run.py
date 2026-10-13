#!/usr/bin/env python3
"""Run-domain CLI: review-run lifecycle, gates, orchestration, publish checks.

This entry owns the argparse flag tables and argv handling; the business logic
lives in ``embodied_learning.wiki.run.*`` as ``run(args) -> int`` (no argparse,
no ``main`` in the library — see docs/adr/0005). See scripts/README.md for the
stage map.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
for _root in (_HERE.parents[3], _HERE.parents[1]):
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

from embodied_learning.config import (
    DYNAMIC_AGENT_TIMEOUT_S,
    REVIEW_MODES,
    SEARCH_STRATEGIES,
    SELECTION_STRATEGIES,
    S2_BUDGET_S,
    STYLE_TO_FILE,
    TERMS_AGENT_TIMEOUT_S,
)
from embodied_learning.utils.layout import default_kb_root, find_roots

REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()

# Implementation modules, imported lazily by dispatch() so that --help does not
# drag in the whole library; each parser builder names the module whose __doc__
# becomes that subcommand's argparse description.
_MODULES: dict[str, str] = {
    "init": "embodied_learning.wiki.run.manifest",
    "register": "embodied_learning.wiki.run.register",
    "status": "embodied_learning.wiki.run.status",
    "next-event-id": "embodied_learning.wiki.run.events",
    "check-bundle": "embodied_learning.wiki.run.bundle",
    "audit-citations": "embodied_learning.wiki.run.citations",
    "finalize": "embodied_learning.wiki.run.finalize",
    "check-sink-integrity": "embodied_learning.wiki.run.drift",
    "validate-reviews": "embodied_learning.wiki.run.validate",
    "token-meter": "embodied_learning.wiki.run.meter",
    "pipeline": "embodied_learning.wiki.run.driver",
    "launch": "embodied_learning.wiki.run.launcher",
}

# subcommand -> one-line help (the dispatcher's own usage() listing)
_HELP: dict[str, str] = {
    "init": "create a run folder + in-progress run.json",
    "register": "register a settled run in the catalog",
    "status": "one-shot run digest (funnel/evidence/next commands)",
    "next-event-id": "next free evidence event ID (+ prefix claims)",
    "check-bundle": "bundle-completeness gate",
    "audit-citations": "citation audit gate",
    "finalize": "mechanical settle: stamp -> gates -> publish -> catalog -> wiki",
    "check-sink-integrity": "reconcile work/ vs evidence/ vs catalog",
    "validate-reviews": "batch-validate every catalog-routed run (CI)",
    "token-meter": "append one token-meter record",
    "pipeline": "mechanical stages driver (plan->retrieval->...->projection)",
    "launch": "headless end-to-end launcher (init->driver->writer->finalize)",
}

# subcommand -> parser builder (the flag table; argparse lives only here)
_PARSERS: dict[str, "object"] = {}

def _init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=manifest.__doc__)
    parser.add_argument("--topic", required=True, help="Review topic or question.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="EA/ERR knowledge ID. Repeatable.")
    parser.add_argument("--time-range", help="Resolved review window, e.g. 2026-01-09..2026-07-09.")
    parser.add_argument(
        "--review-mode",
        choices=["rapid", "scoping", "systematic"],
        default="scoping",
        help="Review-depth contract. Targets are floors; stopping remains coverage/saturation based.",
    )
    parser.add_argument("--date", help="Run date YYYYMMDD for the folder name (default: today).")
    parser.add_argument(
        "--run-version",
        type=int,
        default=1,
        help="Version mark for repeat productions of the same topic on the same "
             "date. 1 (default) keeps the bare literature-review-<topic>-<date> "
             "name; N>1 appends -v<N>. Deliberately explicit, not auto-increment: "
             "a duplicate launch_review on the same topic must still fail loudly "
             "instead of silently forking a v2 (see duplicate-launcher hazard).",
    )
    parser.add_argument("--work-dir", default=str(default_kb_root() / "work"), help="Parent directory for the run folder.")
    parser.add_argument(
        "--inputs-json",
        default="",
        help="JSON object of the caller's real inputs (interview answers: requested "
        "review_mode, target_style, focus, strategies, seeds, source). Stamped "
        "verbatim under run.json `inputs` so a later session can see what the "
        "user actually chose without spelunking logs.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing run.json in the target folder.")


    return parser



def _register_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=register.__doc__)
    parser.add_argument("--run-dir", required=True, help="Settled run directory (holds run.json).")
    parser.add_argument("--kb-root", default=str(default_kb_root()), help="KB root owning the catalog.")
    parser.add_argument("--row", help="Custom 成果索引 Markdown row (default: generated from run.json).")
    return parser



def _status_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=status.__doc__)
    parser.add_argument("--run-dir", required=True, help="Run directory to digest.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of text.")
    return parser



def _next_event_id_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=events.__doc__)
    parser.add_argument("--evidence-dir", default=str(default_kb_root() / "evidence"), help="Evidence layer root.")
    parser.add_argument("--kb-root", default=str(default_kb_root()), help="KB root for .claims/ (default: evidence-dir's parent's parent).")
    parser.add_argument("--prefix", help="Only report this event-ID prefix, e.g. EA-TWM-2026.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument(
        "--claim-prefix",
        help="Reserve this event-ID prefix for a run (O_EXCL claim file under <kb-root>/.claims/).",
    )
    parser.add_argument("--run", help="Run folder name the claimed prefix belongs to (required with --claim-prefix).")
    parser.add_argument("--topic", help="Topic recorded in the claim file (informational).")
    parser.add_argument("--claims", action="store_true", help="List all event-prefix claims and exit.")
    parser.add_argument("--release", action="store_true", help="Release the claimed prefix (retry scenarios only).")
    return parser



def _check_bundle_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=bundle.__doc__)
    parser.add_argument("run_dir", help="Path to a literature-review-<topic>-<date> run folder.")
    return parser



def _audit_citations_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=citations.__doc__)
    parser.add_argument("--article", action="append", default=[], help="Article Markdown file. Repeatable.")
    parser.add_argument("--appendix", help="evidence-appendix.md the articles link into.")
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Evidence JSONL the articles may cite. Repeatable.")
    parser.add_argument("--run-json", help="Optional run.json manifest to cross-check.")
    return parser



def _finalize_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=finalize.__doc__)
    parser.add_argument("--run-dir", required=True, help="In-progress run directory (holds run.json).")
    parser.add_argument(
        "--kb-root",
        default=None,
        help="KB root to publish into. Default: inferred from --run-dir "
        "(<kb-root>/work/<run> layout); only needed for non-standard layouts.",
    )
    parser.add_argument("--style", choices=sorted(STYLE_TO_FILE), help="Declare a reduced single-style scope.")
    parser.add_argument("--scope-note", help="Why the user asked for a single style (with --style).")
    parser.add_argument(
        "--declare-gate-exception",
        action="append",
        default=[],
        metavar="NAME",
        help="Mechanical gate_exceptions declaration: waive the named gate (e.g. "
        "saturation / cited_paper_floor) with a --reason justification recorded in "
        "run.json notes. Never hand-edit run.json for this.",
    )
    parser.add_argument("--reason", default="", help="Justification for --declare-gate-exception.")
    parser.add_argument("--skip-wiki", action="store_true", help="Skip the wiki snapshot rebuild.")
    return parser



def _check_sink_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=drift.__doc__)
    parser.add_argument(
        "--repo-root",
        default=str(find_roots()[0] or Path.cwd()),  # find_roots()[0]=repo checkout, None in a wheel
        help="Repository root containing work/, evidence/, and knowledge/ (default: this repo).",
    )
    return parser



def _validate_reviews_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=validate.__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root to validate.")
    return parser



def _pipeline_parser() -> argparse.ArgumentParser:
    today = dt.date.today().isoformat()
    parser = argparse.ArgumentParser(description=driver.__doc__)
    parser.add_argument("--run-dir", required=True, help="In-progress run folder under work/.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--review-mode", choices=sorted(REVIEW_MODES), default="rapid")
    parser.add_argument("--time-range", default=f"2023-01-01..{today}")
    parser.add_argument("--focus", default="", help="Interview focus text; feeds the terms selection.")
    parser.add_argument("--kb-root", default=str(default_kb_root()), help="Knowledge base root (run dir parent conventions).")
    parser.add_argument(
        "--search-strategy",
        choices=sorted(SEARCH_STRATEGIES),
        default="smart",
        help="smart: taxonomy plan + agent dynamic queries (+ citation expansion when seeds given); "
        "fast: taxonomy plan only; seeds: citation-graph expansion only (requires seeds).",
    )
    parser.add_argument(
        "--selection-strategy",
        choices=sorted(SELECTION_STRATEGIES),
        default="smart",
        help="How the deep-read queue is chosen from the registry: smart (one-shot "
        "agent relevance pass, default), bm25, influence (degrades to bm25 without "
        "citation data), or keywords (legacy term-matching screen-candidates).",
    )
    parser.add_argument(
        "--seed-arxiv-ids",
        default="",
        help="Comma/space-separated arXiv IDs used as citation-expansion seeds (optional).",
    )
    parser.add_argument(
        "--external-candidates",
        action="append",
        default=[],
        help=(
            "harvest-curated-list JSON used AS the candidate source (repeatable). Keyword "
            "retrieval (S2 + arXiv) is skipped; the plan stage still runs for knowledge IDs "
            "and the coverage report. For curated-list runs declare workflow_version 1 + "
            "selection_method in run.json — no coverage/saturation gate applies."
        ),
    )
    parser.add_argument(
        "--with-s2",
        action="store_true",
        help="Enable the Semantic Scholar keyword channel (off by default: under the "
        "public rate limit it routinely exceeds its budget and is killed, and the arXiv "
        "channel already carries recall). Citation expansion is unaffected by this flag.",
    )
    parser.add_argument(
        "--arxiv-snapshot",
        help="Offline arXiv retrieval: path to a local metadata OAI snapshot (JSONL). "
        "Passed to search-arxiv --metadata-snapshot; no live arXiv API calls.",
    )
    parser.add_argument("--no-terms-agent", action="store_true", help="Use mechanical terms only (skip the one-shot claude call).")
    parser.add_argument("--no-dynamic-agent", action="store_true", help="Skip the one-shot dynamic-query agent (smart strategy).")
    parser.add_argument("--terms-timeout", type=float, default=TERMS_AGENT_TIMEOUT_S)
    parser.add_argument("--dynamic-timeout", type=float, default=DYNAMIC_AGENT_TIMEOUT_S)
    parser.add_argument("--s2-budget", type=float, default=S2_BUDGET_S)
    parser.add_argument("--workers", type=int, default=4, help="Full-text extraction workers (capped 4 downstream).")
    parser.add_argument("--force", action="store_true", help="Re-run every stage even when outputs exist.")
    parser.add_argument("--skip-deep-read", action="store_true", help="Stop after reading packets (no skeleton agents).")
    parser.add_argument(
        "--deep-read-limit", type=int, default=None,
        help="Max papers to deep-read this run. Default: mode-aware "
             "(rapid 10 / scoping 16 / systematic 40) so the finalize "
             "cited-paper floor is reachable.",
    )
    parser.add_argument("--agent-timeout", type=float, default=420.0, help="Per-paper skeleton agent timeout (s).")
    parser.add_argument(
        "--selection-timeout", type=float, default=900.0,
        help="Per-chunk smart-selection agent timeout (s); a timeout is a failed chunk, not a crash.",
    )
    parser.add_argument(
        "--extraction-timeout", type=float, default=300.0,
        help="Hard per-paper full-text extraction timeout (s).",
    )
    parser.add_argument("--agents-parallel", type=int, default=5, help="Concurrent skeleton agents.")

    return parser


def _launch_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=launcher.__doc__.splitlines()[0])
    parser.add_argument("--topic")
    parser.add_argument("--review-mode", choices=["rapid", "scoping", "systematic"], default="systematic")
    parser.add_argument("--time-range", help="YYYY-MM-DD..YYYY-MM-DD")
    parser.add_argument("--focus")
    parser.add_argument("--search-strategy", choices=["smart", "fast", "seeds"], default="smart")
    parser.add_argument(
        "--selection-strategy",
        choices=["keywords", "influence", "bm25", "smart"],
        default="smart",
        help="Deep-read queue selection (forwarded to the driver; keywords keeps the "
        "legacy term-matching screen-candidates).",
    )
    parser.add_argument("--seed-arxiv-ids")
    parser.add_argument("--external-candidates", action="append", default=[],
                        help="harvest-curated-list JSON as the candidate source; forwarded to the driver (repeatable)")
    parser.add_argument("--agents-parallel", type=int, default=10,
                        help="deep-read one-shot agents running concurrently (forwarded to the driver)")
    parser.add_argument("--arxiv-snapshot", help="OAI JSONL or SQLite/FTS5 db for offline arXiv retrieval")
    parser.add_argument("--kb-root", help=f"KB root (default: {default_kb_root()})")
    parser.add_argument("--knowledge-id", action="append", help="EA/ERR knowledge id; repeatable (default EA-DATA)")
    parser.add_argument("--target-style", default="scientific-memo",
                        help="writer 交付风格（all=三风格；scientific-memo/expert-explainer/kol-thread/survey）")
    parser.add_argument("--scope-note", help="收窄范围时必须说明原因")
    parser.add_argument("--run-dir", help="已有 run 目录（--status/--stop/--resume 必填）")
    parser.add_argument(
        "--run-version", type=int, default=1,
        help="同题同日重复生产的版本标记（2+ 追加 -v<N> 到 run 文件夹名）。"
             "刻意不做自动递增：重复 launch 同题必须响亮失败而不是悄悄分叉出 v2。",
    )
    parser.add_argument("--deep-read-limit", type=int, default=48)
    parser.add_argument("--mechanical-retries", type=int, default=3)
    parser.add_argument("--max-agent-retries", type=int, default=2)
    parser.add_argument("--writer-timeout", type=float, default=5400.0)
    parser.add_argument(
        "--writer-model", default=None,
        help="Model for the spawned writer agent (default: ANTHROPIC_MODEL env > "
        "CLAUDE_CODE_SUBAGENT_MODEL env > the driver's pinned fast model). "
        "Pin it — an unpinned claude -p can fall back to an expensive frontier model.",
    )
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    parser.add_argument("--resume", action="store_true",
                        help="续跑已有 run。续跑本就靠阶段标记幂等（直接重跑 --run-dir 即可）；"
                             "此旗子只为让失败提示里的命令字面可用，无额外行为。")
    return parser



def _token_meter_parser() -> argparse.ArgumentParser:
    return meter.build_parser()


def _parser_for(name: str):
    """Build the argparse parser for one subcommand (flag table lives here)."""
    global _PARSERS
    if name not in _PARSERS:
        builder = globals().get(
            {
                "init": "_init_parser",
                "register": "_register_parser",
                "status": "_status_parser",
                "next-event-id": "_next_event_id_parser",
                "check-bundle": "_check_bundle_parser",
                "audit-citations": "_audit_citations_parser",
                "finalize": "_finalize_parser",
                "check-sink-integrity": "_check_sink_parser",
                "validate-reviews": "_validate_reviews_parser",
                "token-meter": "_token_meter_parser",
                "pipeline": "_pipeline_parser",
                "launch": "_launch_parser",
            }[name]
        )
        # the parser builders name their implementation module for __doc__
        globals().update({m.split(".")[-1]: importlib.import_module(m) for m in set(_MODULES.values())})
        _PARSERS[name] = builder()
    return _PARSERS[name]


def usage() -> str:
    lines = ["usage: run.py <subcommand> [args]", "", "subcommands:"]
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
        print(f"run.py: unknown subcommand {name!r}\n\n{usage()}", file=sys.stderr)
        return 2
    parser = _parser_for(name)
    parser.prog = name
    args = parser.parse_args(rest)
    mod = importlib.import_module(_MODULES[name])
    return int(mod.run(args) or 0)


def main(argv: list[str] | None = None) -> int:
    return dispatch(list(sys.argv[1:] if argv is None else argv))


# Console-script aliases (pyproject [project.scripts]): each prepends its
# subcommand so the historical bare-flag UX keeps working.
def pipeline_main() -> int:
    return dispatch(["pipeline", *sys.argv[1:]])


def launch_main() -> int:
    return dispatch(["launch", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reading-domain CLI: one entry per reading stage (paper-reader skill).

Subcommands dispatch into ``embodied_learning.knowledge.*`` and
``embodied_learning.parse.reading_packet``. The thin schema/audit/projection
handlers (formerly note_tools.py) and the pool handlers (formerly the hub's
knowledge.py) moved here verbatim — flags and exit codes unchanged.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
for _root in (_HERE.parents[3], _HERE.parents[1]):
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

from embodied_learning.knowledge.claim_support import audit, load_object  # noqa: E402
from embodied_learning.knowledge.evidence_projection import project  # noqa: E402
from embodied_learning.knowledge.paper_note import load_note, validate_note  # noqa: E402
from embodied_learning.knowledge.pool import DEFAULT_POOL_ROOT, PaperPool, load_json  # noqa: E402


# ---- validate-paper-note (was note_tools.py) --------------------------------

def validate_paper_note(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a paper-note JSON against the note schema.")
    parser.add_argument("paper_note")
    parser.add_argument("--json-output")
    args = parser.parse_args(argv)
    try:
        note = load_note(Path(args.paper_note))
        errors, warnings = validate_note(note)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors, warnings = [str(exc)], []
    result = {"status": "pass" if not errors else "reject", "errors": errors, "warnings": warnings}
    if args.json_output:
        target = Path(args.json_output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        print(f"paper note rejected ({len(errors)} error(s)):")
        for error in errors:
            print(f"- {error}")
        return 1
    print("paper note OK")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


# ---- audit-claim-support (was note_tools.py) --------------------------------

def audit_claim_support(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit claim/quote verbatim support in a paper note.")
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--extraction", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        note = load_object(Path(args.paper_note))
        extraction = load_object(Path(args.extraction))
        result = audit(note, extraction)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"schema_version": 1, "paper_id": "", "status": "reject", "reason": str(exc), "cards": []}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    print(f"claim-support audit: {result['status']}", file=sys.stderr)
    return {"pass": 0, "needs-review": 1, "reject": 2}[str(result["status"])]


# ---- project-evidence-events (was note_tools.py) ----------------------------

def project_evidence_events(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project a validated note + audit into evidence event JSONL.")
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--audit", required=True, help="Passing audit JSON from audit-claim-support.")
    parser.add_argument("--id-prefix", required=True)
    parser.add_argument("--start-seq", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        note = load_object(Path(args.paper_note))
        audit_result = load_object(Path(args.audit))
        events = project(note, audit_result, args.id_prefix, args.start_seq)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"evidence projection blocked: {exc}", file=sys.stderr)
        return 2
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n", encoding="utf-8")
    print(f"Projected {len(events)} verified evidence event(s): {target}")
    return 0


# ---- pool-add-paper (was the hub's knowledge.py) -----------------------------

def _pool_add_paper_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Paper-pool management (add/import-existing/list/get).")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Add or refresh a paper from an extraction JSON.")
    add.add_argument("--extraction", required=True, help="Unified extraction JSON (extract-content/tex output).")
    add.add_argument("--metadata", help="Optional per-paper metadata JSON (flat or wrapped in `paper`).")
    add.add_argument("--note", help="Optional reading note Markdown to archive as note.md.")
    add.add_argument(
        "--note-json",
        help="Optional paper-note JSON (paper-reader output) to archive as note.json.",
    )
    add.add_argument(
        "--html",
        help="Optional cleaned/raw paper HTML to archive as paper.html (reader fast path).",
    )
    add.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)
    add.add_argument("--force", action="store_true", help="Overwrite an existing pool entry and refresh its index line.")

    import_existing = sub.add_parser("import-existing", help="Migrate legacy flat <id>.md files into the per-paper layout.")
    import_existing.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)
    import_existing.add_argument("--force", action="store_true")

    list_parser = sub.add_parser("list", help="List pool papers.")
    list_parser.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)
    list_parser.add_argument("--format", choices=["table", "json"], default="table")

    get_parser = sub.add_parser("get", help="Print one paper's meta.json.")
    get_parser.add_argument("paper_id", help="arXiv ID or pool directory name.")
    get_parser.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)

    return parser.parse_args(argv)


def pool_add_paper(argv: list[str] | None = None) -> int:
    args = _pool_add_paper_parse_args(argv)
    args = parser.parse_args(argv)
    pool = PaperPool(args.pool_root)
    if args.command == "add":
        metadata = load_json(Path(args.metadata).expanduser()) if args.metadata else None
        note = Path(args.note).expanduser().read_text(encoding="utf-8") if args.note else None
        note_json = load_json(Path(args.note_json).expanduser()) if args.note_json else None
        return pool.add(
            extraction=load_json(Path(args.extraction).expanduser()),
            metadata=metadata,
            note=note,
            note_json=note_json,
            html=args.html,
            force=args.force,
        )
    if args.command == "import-existing":
        return pool.import_existing(force=args.force)
    if args.command == "list":
        return pool.list_papers(as_json=args.format == "json")
    if args.command == "get":
        return pool.get(args.paper_id)
    raise SystemExit("choose a command: add | import-existing | list | get")


# ---- library-main subcommands (module owns its original parser) -------------

_MODULES: dict[str, str] = {
    "build-reading-packet": "embodied_learning.parse.reading_packet",
    "build-paper-note": "embodied_learning.knowledge.note_assembly",
    "quick-read": "embodied_learning.knowledge.quick_read",
    "prepare-chat": "embodied_learning.knowledge.deepread",
    "extract-failed-card-window": "embodied_learning.knowledge.card_window",
    "update-reading-ledger": "embodied_learning.knowledge.reading_ledger",
}

_PARSER_LOOKUP = {
    "build-reading-packet": "_reading_packet_parser",
    "build-paper-note": "_note_assembly_parser",
    "quick-read": "_quick_read_parser",
    "prepare-chat": "_deepread_parser",
    "extract-failed-card-window": "_card_window_parser",
    "update-reading-ledger": "_reading_ledger_parser",
}

_PARSERS: dict[str, object] = {}


def _reading_packet_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=reading_packet.__doc__)
    parser.add_argument("--extraction", required=True, help="Complete Hub extraction JSON.")
    parser.add_argument("--metadata", help="Optional per-paper metadata JSON.")
    parser.add_argument("--review-question", required=True)
    parser.add_argument("--topic-id", action="append", default=[], required=True)
    parser.add_argument("--review-mode", choices=sorted(reading_packet.MODES), default="scoping")
    parser.add_argument("--output", required=True)
    parser.add_argument("--note-template")
    parser.add_argument(
        "--summary-first",
        action="store_true",
        help=(
            "Emit structure map + truncated section windows instead of pasting "
            "Complete extracted text. Full text remains on disk in the extraction JSON "
            "for locator windows and claim-support audits. Recommended for paper-reader "
            "scoping passes."
        ),
    )
    parser.add_argument(
        "--max-section-chars",
        type=int,
        default=reading_packet.DEFAULT_MAX_SECTION_CHARS,
        help=(
            f"When --summary-first is set, truncate each section/page window to this many "
            f"characters (default {reading_packet.DEFAULT_MAX_SECTION_CHARS}). Ignored in full-text mode."
        ),
    )
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help="Force embedding Complete extracted text even when --summary-first is set.",
    )
    return parser



def _note_assembly_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=note_assembly.__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--pool-root", default=note_assembly.DEFAULT_KB_ROOT)
    parser.add_argument("--skeleton", help="Skeleton JSON file; stdin when omitted.")
    parser.add_argument("--max-cards", type=int, default=4)
    return parser



def _quick_read_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=quick_read.__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--kb-root", default=str(Path.home() / "Documents" / "arxiv"))
    parser.add_argument("--force", action="store_true", help="Re-extract / re-deep-read / rewrite the card even when cached.")
    parser.add_argument("--skip-agent", action="store_true", help="Write only the brief (debugging); no article.")
    parser.add_argument("--no-audit", action="store_true", help="Skip the editorial audit after writing.")
    return parser



def _deepread_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=deepread.__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--kb-root", default=str(Path.home() / "Documents" / "arxiv"))
    parser.add_argument("--force", action="store_true", help="Re-extract / re-deep-read even when pooled.")
    return parser



def _card_window_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=card_window.__doc__)
    parser.add_argument("--audit", required=True, help="audit_claim_support JSON")
    parser.add_argument("--extraction", required=True, help="complete extraction JSON")
    parser.add_argument(
        "--paper-note",
        help="optional paper-note JSON (used to attach claim text to failing cards)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=4000,
        help="chars kept around source_context inside a matched surface (default 4000)",
    )
    parser.add_argument(
        "--max-window",
        type=int,
        default=8000,
        help="hard cap per card window in characters (default 8000)",
    )
    parser.add_argument("--output", help="write JSON; default stdout")
    parser.add_argument(
        "--markdown-output",
        help="optional human-readable markdown for the LLM retry prompt",
    )
    return parser



def _reading_ledger_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=reading_ledger.__doc__)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--audit")
    parser.add_argument("--summary-output")
    parser.add_argument("--allow-regression", action="store_true")
    return parser
def _parser_for(name: str):
    if name not in _PARSERS:
        globals().update({m.split(".")[-1]: importlib.import_module(m) for m in set(_MODULES.values())})
        _PARSERS[name] = globals()[_PARSER_LOOKUP[name]]()
    return _PARSERS[name]

HANDLERS = {
    "validate-paper-note": validate_paper_note,
    "audit-claim-support": audit_claim_support,
    "project-evidence-events": project_evidence_events,
    "pool-add-paper": pool_add_paper,
}

HELP = {
    "build-reading-packet": "reading packet + note template from a complete extraction",
    "build-paper-note": "deep-read note assembly (skeleton -> locator resolve -> audit)",
    "quick-read": "single-paper quick-read card (速读)",
    "prepare-chat": "ensure a paper is pooled + deep-read (wiki paper-chat prep)",
    "extract-failed-card-window": "locator windows for failed claim-support cards",
    "update-reading-ledger": "insert/update one paper in the reading ledger",
    "validate-paper-note": "validate a paper-note JSON against the schema",
    "audit-claim-support": "audit claim/quote verbatim support",
    "project-evidence-events": "project note+audit into evidence event JSONL",
    "pool-add-paper": "paper pool add/import-existing/list/get",
}


def usage() -> str:
    lines = ["usage: read.py <subcommand> [args]", "", "subcommands:"]
    width = max(len(name) for name in HELP)
    for name, help_text in HELP.items():
        lines.append(f"  {name.ljust(width)}  {help_text}")
    return "\n".join(lines)


def dispatch(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(usage())
        return 0
    name, rest = argv[0], argv[1:]
    if name in HANDLERS:
        return int(HANDLERS[name](rest) or 0)
    parser = _parser_for(name)
    parser.prog = name
    args = parser.parse_args(rest)
    mod = importlib.import_module(_MODULES[name])
    return int(mod.run(args) or 0)
    print(f"read.py: unknown subcommand {name!r}\n\n{usage()}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    return dispatch(list(sys.argv[1:] if argv is None else argv))


# Console-script aliases (pyproject [project.scripts]).
def quick_read_main() -> int:
    return dispatch(["quick-read", *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())

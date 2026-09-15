#!/usr/bin/env python3
"""CLI: paper-note validation, claim-support audit, and evidence projection.

One entry, three subcommands (the old single-purpose scripts, kebab-cased):
validate-paper-note | audit-claim-support | project-evidence-events.
Library APIs live in embodied_learning/knowledge/{paper_note,claim_support,
evidence_projection}.py; this entry owns only argument parsing and dispatch.
"""
import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.claim_support import audit, load_object  # noqa: E402
from embodied_learning.knowledge.evidence_projection import project  # noqa: E402
from embodied_learning.knowledge.paper_note import load_note, validate_note  # noqa: E402


# ---- validate-paper-note (was scripts/validate_paper_note.py) ---------------

def validate_paper_note_main(argv: list[str] | None = None) -> int:
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


# ---- audit-claim-support (was scripts/audit_claim_support.py) ---------------

def audit_claim_support_main(argv: list[str] | None = None) -> int:
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


# ---- project-evidence-events (was scripts/project_evidence_events.py) -------

def project_evidence_events_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project a validated note + audit into evidence event JSONL.")
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--audit", required=True, help="Passing audit JSON from audit-claim-support.")
    parser.add_argument("--id-prefix", required=True)
    parser.add_argument("--start-seq", type=int, default=1)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        note = load_object(Path(args.paper_note))
        audit = load_object(Path(args.audit))
        events = project(note, audit, args.id_prefix, args.start_seq)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"evidence projection blocked: {exc}", file=sys.stderr)
        return 2
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n", encoding="utf-8")
    print(f"Projected {len(events)} verified evidence event(s): {target}")
    return 0


_SUBCOMMANDS = {
    "validate-paper-note": validate_paper_note_main,
    "audit-claim-support": audit_claim_support_main,
    "project-evidence-events": project_evidence_events_main,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch to the tool's own parser; flags and exit codes unchanged."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 0
    handler = _SUBCOMMANDS.get(argv[0])
    if handler is None:
        print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
        print("subcommands: " + ", ".join(_SUBCOMMANDS), file=sys.stderr)
        return 2
    return handler(argv[1:])


if __name__ == "__main__":
    sys.exit(main())

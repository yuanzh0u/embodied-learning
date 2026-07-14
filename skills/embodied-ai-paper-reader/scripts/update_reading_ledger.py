#!/usr/bin/env python3
"""Insert or update one paper in a JSONL reading ledger and write summary counts."""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("validate_paper_note", SCRIPTS_DIR / "validate_paper_note.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)

ORDER = {
    "discovered": 0, "abstract-screened": 1, "full-text-recovered": 2, "map-read": 3,
    "deep-read": 4, "claim-verified": 5, "evidence-ready": 6, "accepted": 7,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--audit")
    parser.add_argument("--summary-output")
    parser.add_argument("--allow-regression", action="store_true")
    return parser.parse_args()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{lineno}: expected a JSON object")
        records.append(value)
    return records


def reached(status: str, threshold: str) -> bool:
    return status in ORDER and ORDER[status] >= ORDER[threshold]


def summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = [str(record.get("status") or "") for record in records]
    return {
        "schema_version": 1,
        "paper_count": len(records),
        "full_text_recovered_count": sum(reached(status, "full-text-recovered") for status in statuses),
        "map_read_count": sum(reached(status, "map-read") for status in statuses),
        "deep_read_count": sum(reached(status, "deep-read") for status in statuses),
        "claim_verified_paper_count": sum(reached(status, "claim-verified") for status in statuses),
        "evidence_ready_paper_count": sum(reached(status, "evidence-ready") for status in statuses),
        "accepted_evidence_paper_count": sum(status == "accepted" for status in statuses),
        "rejected_count": sum(status == "rejected" for status in statuses),
        "unavailable_count": sum(status == "unavailable" for status in statuses),
    }


def main() -> int:
    args = parse_args()
    try:
        note_path = Path(args.paper_note)
        note = load_object(note_path)
        errors, warnings = validator.validate_note(note)
        if errors:
            raise ValueError("paper note failed validation: " + "; ".join(errors))
        audit = load_object(Path(args.audit)) if args.audit else None
        paper = note["paper"]
        status = str(note["reading"]["status"])
        if status in {"evidence-ready", "accepted"} and (not audit or audit.get("status") != "pass"):
            raise ValueError(f"{status} ledger entry requires a passing claim-support audit")
        if audit and str(audit.get("paper_id") or "") != str(paper["arxiv_id"]):
            raise ValueError("audit paper_id does not match the paper note")
        ledger_path = Path(args.ledger)
        records = load_ledger(ledger_path)
        by_id = {str(record.get("paper_id") or ""): record for record in records}
        old = by_id.get(str(paper["arxiv_id"]))
        if old and not args.allow_regression:
            old_status = str(old.get("status") or "")
            if old_status in ORDER and status in ORDER and ORDER[status] < ORDER[old_status]:
                raise ValueError(f"state regression blocked: {old_status} -> {status}")
            if old_status in {"rejected", "unavailable"} and status != old_status:
                raise ValueError(f"terminal state change blocked: {old_status} -> {status}")
        by_id[str(paper["arxiv_id"])] = {
            "paper_id": paper["arxiv_id"],
            "title": paper["title"],
            "url": paper["url"],
            "status": status,
            "review_mode": note["review"]["mode"],
            "topic_ids": note["review"]["topic_ids"],
            "extraction_method": note["extraction"].get("method"),
            "extraction_quality": note["extraction"].get("quality"),
            "paper_note": str(note_path),
            "claim_support_audit": str(audit.get("status")) if audit else "not-run",
            "evidence_card_count": len(note.get("evidence_cards", [])),
            "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        records = [by_id[key] for key in sorted(by_id)]
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")
        report = summary(records)
        if args.summary_output:
            target = Path(args.summary_output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"reading ledger update blocked: {exc}", file=sys.stderr)
        return 2
    print(f"Updated reading ledger: {args.ledger}")
    print(json.dumps(report, ensure_ascii=False))
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

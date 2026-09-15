#!/usr/bin/env python3
"""Project verified paper-note evidence cards into Hub-compatible JSONL events.

Library API: stateless explicit-parameter functions (:func:`project`,
:func:`normalize_authors`, :func:`author_key`, :func:`load_object`). Consumers
surface owns argument parsing and lives in the skill entry
``skills/embodied-ai-paper-reader/scripts/project_evidence_events.py``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


from embodied_learning.knowledge import paper_note as validator


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def author_key(name: str) -> str:
    ascii_name = name.encode("ascii", errors="ignore").decode("ascii")
    base = ascii_name if ascii_name.strip() else name
    return re.sub(r"[^0-9A-Za-z]+", "-", base.strip().lower()).strip("-") or "unknown-author"


def normalize_authors(authors: list[Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for author in authors:
        if isinstance(author, str):
            result.append({"name": author, "author_key": author_key(author), "role": "paper-author", "institutions": []})
        elif isinstance(author, dict) and str(author.get("name") or "").strip():
            record = dict(author)
            record.setdefault("author_key", author_key(str(record["name"])))
            record.setdefault("role", "paper-author")
            record.setdefault("institutions", [])
            result.append(record)
    return result


def project(note: dict[str, Any], audit: dict[str, Any], prefix: str, start_seq: int) -> list[dict[str, Any]]:
    errors, _ = validator.validate_note(note)
    if errors:
        raise ValueError("paper note failed validation: " + "; ".join(errors))
    reading = note["reading"]
    if reading.get("status") not in {"evidence-ready", "accepted"}:
        raise ValueError("projection requires reading.status evidence-ready or accepted")
    paper = note["paper"]
    if audit.get("status") != "pass":
        raise ValueError("projection requires a passing claim-support audit")
    if str(audit.get("paper_id") or "") != str(paper.get("arxiv_id") or ""):
        raise ValueError("audit paper_id does not match the paper note")
    audit_cards = {str(item.get("card_id")): item for item in audit.get("cards", []) if isinstance(item, dict)}
    extraction = note["extraction"]
    quality = str(extraction["quality"])
    visual_validation = "passed" if quality == "medium" else "not-required"
    topic_ids = note["review"]["topic_ids"]
    topic = str(note["review"]["question"])
    prefix = prefix.rstrip("-")
    events: list[dict[str, Any]] = []
    for offset, card in enumerate(note["evidence_cards"]):
        card_id = str(card["card_id"])
        if (audit_cards.get(card_id) or {}).get("status") != "pass":
            raise ValueError(f"card {card_id} is not pass in the audit")
        event = {
            "event_id": f"{prefix}-{start_seq + offset:04d}",
            "topic_id": str(topic_ids[0]),
            "topic": topic,
            "paper": {
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "published": paper.get("published", ""),
                "url": paper["url"],
            },
            "authors": normalize_authors(paper.get("authors", [])),
            "claim": card["claim"],
            "stance": card["stance"],
            "evidence": {
                "summary": card["summary"],
                "locator": card["locator"],
                "short_quote": str(card["source_context"])[:500],
                "evidence_type": card["evidence_type"],
                "extraction": {
                    "source_format": extraction["source_format"],
                    "method": extraction["method"],
                    "quality": quality,
                    "visual_validation": visual_validation,
                    "visual_validation_pages": [],
                },
            },
            "confidence": card["confidence"],
            "core_citations": note.get("core_citations", []),
            "notes": str(card.get("notes") or note.get("notes") or ""),
            "paper_reading": {
                "paper_note_schema": note["schema_version"],
                "card_id": card_id,
                "review_mode": note["review"]["mode"],
                "reading_status": reading["status"],
                "claim_support_audit": "pass",
                "topic_ids": topic_ids,
                "claim_basis": card["claim_basis"],
                "relation": card["relation"],
                "verification_rationale": card["verification"]["rationale"],
                "quantitative": card.get("quantitative", False),
            },
        }
        events.append(event)
    return events

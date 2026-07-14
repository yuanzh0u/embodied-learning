#!/usr/bin/env python3
"""Validate a paper note against reading-depth and evidence-admission gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MODES = {"rapid", "scoping", "systematic"}
STATUSES = {
    "discovered", "abstract-screened", "full-text-recovered", "map-read", "deep-read",
    "claim-verified", "evidence-ready", "accepted", "rejected", "unavailable",
}
PAPER_TYPES = {"method", "empirical", "dataset", "benchmark", "survey", "position", "theory", "system", "other"}
RELEVANCE = {"include", "background-only", "exclude"}
ROLES = {
    "problem", "relevant-core", "method-or-design", "data-or-setting", "results-or-analysis",
    "conclusion-or-limitations", "appendix-or-supplement",
}
REQUIRED_ROLES = {
    "rapid": {"problem", "relevant-core", "conclusion-or-limitations"},
    "scoping": {"problem", "method-or-design", "results-or-analysis", "conclusion-or-limitations"},
    "systematic": {"problem", "method-or-design", "results-or-analysis", "conclusion-or-limitations"},
}
STANCES = {"support", "limit", "conditional", "gap"}
CONFIDENCE = {"direct", "citation-supported", "inference"}
CLAIM_BASES = {"author-claim", "reported-result", "cited-work", "reader-inference"}
READING_RANK = {
    "discovered": 0, "abstract-screened": 1, "full-text-recovered": 2, "map-read": 3,
    "deep-read": 4, "claim-verified": 5, "evidence-ready": 6, "accepted": 7,
}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "TODO" not in value.upper()


def object_at(value: Any, path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    return value


def list_at(value: Any, path: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return []
    return value


def contains_todo(value: Any) -> bool:
    if isinstance(value, str):
        return "TODO" in value.upper()
    if isinstance(value, list):
        return any(contains_todo(item) for item in value)
    if isinstance(value, dict):
        return any(contains_todo(item) for item in value.values())
    return False


def validate_note(note: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if note.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    paper = object_at(note.get("paper"), "paper", errors)
    if not nonempty(paper.get("arxiv_id")):
        errors.append("paper.arxiv_id is required")
    if not nonempty(paper.get("title")):
        errors.append("paper.title is required")
    if not nonempty(paper.get("url")):
        errors.append("paper.url is required")
    authors = paper.get("authors", [])
    if not isinstance(authors, list):
        errors.append("paper.authors must be a list")

    review = object_at(note.get("review"), "review", errors)
    mode = str(review.get("mode") or "")
    if mode not in MODES:
        errors.append("review.mode must be rapid|scoping|systematic")
    if not nonempty(review.get("question")):
        errors.append("review.question is required")
    topic_ids = list_at(review.get("topic_ids"), "review.topic_ids", errors)
    if not topic_ids or not all(nonempty(item) for item in topic_ids):
        errors.append("review.topic_ids must contain at least one non-empty ID")

    reading = object_at(note.get("reading"), "reading", errors)
    status = str(reading.get("status") or "")
    if status not in STATUSES:
        errors.append("reading.status is invalid")
    relevance = object_at(reading.get("relevance"), "reading.relevance", errors)
    decision = str(relevance.get("decision") or "")
    if decision not in RELEVANCE:
        errors.append("reading.relevance.decision must be include|background-only|exclude")
    if not nonempty(relevance.get("reason")):
        errors.append("reading.relevance.reason is required")

    cards = list_at(note.get("evidence_cards"), "evidence_cards", errors)
    if status == "unavailable":
        extraction = object_at(note.get("extraction"), "extraction", errors)
        if extraction.get("full_text_available") is True:
            errors.append("unavailable paper cannot set extraction.full_text_available=true")
        if cards:
            errors.append("unavailable paper cannot have evidence cards")
        return errors, warnings

    extraction = object_at(note.get("extraction"), "extraction", errors)
    method = str(extraction.get("method") or "")
    if method == "pdf-ocr" or extraction.get("ocr_pages"):
        errors.append("OCR-derived papers are outside this workflow")
    if method not in {"html-latexml", "html-flat", "pdf-text"}:
        errors.append("extraction.method must be html-latexml|html-flat|pdf-text")
    quality = str(extraction.get("quality") or "")
    if quality not in {"high", "medium"}:
        errors.append("extraction.quality must be high|medium")
    if quality == "medium" and extraction.get("visual_validation") != "passed":
        errors.append("medium extraction requires extraction.visual_validation=passed")

    rank = READING_RANK.get(status, -1)
    if rank >= READING_RANK["map-read"] and extraction.get("full_text_available") is not True:
        errors.append("map-read and later states require complete full text")
    if status == "rejected" and cards:
        errors.append("rejected paper cannot have evidence cards")

    if rank >= READING_RANK["map-read"]:
        paper_type = str(reading.get("paper_type") or "")
        if paper_type not in PAPER_TYPES:
            errors.append("reading.paper_type is invalid")
        sections = list_at(reading.get("sections_read"), "reading.sections_read", errors)
        roles: set[str] = set()
        for index, section in enumerate(sections):
            item = object_at(section, f"reading.sections_read[{index}]", errors)
            if not nonempty(item.get("locator")):
                errors.append(f"reading.sections_read[{index}].locator is required")
            role = str(item.get("role") or "")
            if role not in ROLES:
                errors.append(f"reading.sections_read[{index}].role is invalid")
            else:
                roles.add(role)
            if not nonempty(item.get("purpose")):
                errors.append(f"reading.sections_read[{index}].purpose is required")
        if rank >= READING_RANK["deep-read"] and mode in REQUIRED_ROLES:
            missing = sorted(REQUIRED_ROLES[mode] - roles)
            if missing:
                errors.append(f"{mode} deep reading is missing section roles: {', '.join(missing)}")
        if rank >= READING_RANK["deep-read"] and mode == "systematic" and "appendix-or-supplement" not in roles:
            skipped = reading.get("sections_skipped", [])
            appendix_skip = any(
                isinstance(item, dict)
                and item.get("role") == "appendix-or-supplement"
                and nonempty(item.get("reason"))
                for item in skipped if isinstance(skipped, list)
            )
            if not appendix_skip:
                errors.append("systematic reading must read the appendix or record a reason it is not applicable")

    if rank >= READING_RANK["deep-read"]:
        for field in ("research_question", "transfer_boundary"):
            if not nonempty(note.get(field)):
                errors.append(f"{field} is required after deep reading")
        contributions = list_at(note.get("contributions"), "contributions", errors)
        if not contributions or not all(nonempty(item) for item in contributions):
            errors.append("contributions must contain at least one non-empty item")
        method_obj = object_at(note.get("method"), "method", errors)
        if not nonempty(method_obj.get("summary")):
            errors.append("method.summary is required")
        object_at(note.get("study_context"), "study_context", errors)
        object_at(note.get("evaluation"), "evaluation", errors)
        findings = list_at(note.get("findings"), "findings", errors)
        for index, finding in enumerate(findings):
            item = object_at(finding, f"findings[{index}]", errors)
            for field in ("finding", "scope", "locator"):
                if not nonempty(item.get(field)):
                    errors.append(f"findings[{index}].{field} is required")

        limitations = object_at(note.get("limitations"), "limitations", errors)
        author_status = str(limitations.get("author_status") or "")
        author_stated = list_at(limitations.get("author_stated"), "limitations.author_stated", errors)
        if author_status not in {"found", "not-found"}:
            errors.append("limitations.author_status must be found|not-found")
        if author_status == "found" and not author_stated:
            errors.append("author_status=found requires at least one author-stated limitation")
        if author_status == "not-found" and author_stated:
            errors.append("author_status=not-found conflicts with author_stated entries")
        for index, item in enumerate(author_stated):
            obj = object_at(item, f"limitations.author_stated[{index}]", errors)
            if not nonempty(obj.get("limitation")) or not nonempty(obj.get("locator")):
                errors.append(f"limitations.author_stated[{index}] requires limitation and locator")
        inferred = list_at(limitations.get("reader_inferred"), "limitations.reader_inferred", errors)
        if decision == "include" and not inferred:
            errors.append("included deep-read paper requires at least one reader-inferred boundary")
        for index, item in enumerate(inferred):
            obj = object_at(item, f"limitations.reader_inferred[{index}]", errors)
            if not nonempty(obj.get("boundary")) or not nonempty(obj.get("basis")):
                errors.append(f"limitations.reader_inferred[{index}] requires boundary and basis")

        appraisal = object_at(note.get("critical_appraisal"), "critical_appraisal", errors)
        for field in ("design_strengths", "design_risks"):
            list_at(appraisal.get(field), f"critical_appraisal.{field}", errors)
        for field in ("baseline_fairness", "metric_validity", "reproducibility", "external_validity"):
            if not nonempty(appraisal.get(field)):
                errors.append(f"critical_appraisal.{field} is required")

    requires_cards = status in {"claim-verified", "evidence-ready", "accepted"}
    if requires_cards and not cards:
        errors.append(f"{status} requires at least one evidence card")
    if status in {"evidence-ready", "accepted"} and decision != "include":
        errors.append(f"{status} requires reading.relevance.decision=include")
    if status in {"evidence-ready", "accepted"} and not authors:
        errors.append(f"{status} requires at least one paper author for compatible evidence projection")

    card_ids: set[str] = set()
    for index, card in enumerate(cards):
        item = object_at(card, f"evidence_cards[{index}]", errors)
        card_id = str(item.get("card_id") or "")
        if not nonempty(card_id):
            errors.append(f"evidence_cards[{index}].card_id is required")
        elif card_id in card_ids:
            errors.append(f"duplicate evidence card ID: {card_id}")
        card_ids.add(card_id)
        for field in ("claim", "relation", "summary", "locator", "source_context", "evidence_type"):
            if not nonempty(item.get(field)):
                errors.append(f"evidence_cards[{index}].{field} is required")
        if str(item.get("locator") or "").strip().lower() in {"abstract", "metadata", "title", "selected passage"}:
            errors.append(f"evidence_cards[{index}].locator is too vague")
        if len(str(item.get("source_context") or "").strip()) < 20:
            errors.append(f"evidence_cards[{index}].source_context is too short for audit")
        stance = str(item.get("stance") or "")
        confidence = str(item.get("confidence") or "")
        basis = str(item.get("claim_basis") or "")
        if stance not in STANCES:
            errors.append(f"evidence_cards[{index}].stance is invalid")
        if confidence not in CONFIDENCE:
            errors.append(f"evidence_cards[{index}].confidence is invalid")
        if basis not in CLAIM_BASES:
            errors.append(f"evidence_cards[{index}].claim_basis is invalid")
        if confidence == "direct" and basis not in {"author-claim", "reported-result"}:
            errors.append(f"evidence_cards[{index}] direct confidence conflicts with claim_basis={basis}")
        if confidence == "citation-supported" and basis != "cited-work":
            errors.append(f"evidence_cards[{index}] citation-supported confidence requires claim_basis=cited-work")
        if confidence == "inference" and basis != "reader-inference":
            errors.append(f"evidence_cards[{index}] inference confidence requires claim_basis=reader-inference")

        quantitative = item.get("quantitative", False)
        if quantitative is not False:
            quant = object_at(quantitative, f"evidence_cards[{index}].quantitative", errors)
            for field in ("metric", "value_or_direction", "comparator", "task_or_sample", "locator"):
                if not nonempty(quant.get(field)):
                    errors.append(f"evidence_cards[{index}].quantitative.{field} is required")
            if mode == "systematic" and not re.search(r"\b(page|table|figure|appendix)\b|页|表|图", str(quant.get("locator") or ""), re.I):
                errors.append(f"evidence_cards[{index}] systematic quantitative locator must name page/table/figure/appendix")

        verification = object_at(item.get("verification"), f"evidence_cards[{index}].verification", errors)
        if verification.get("status") != "passed":
            errors.append(f"evidence_cards[{index}].verification.status must be passed")
        if verification.get("checked_against") != "full-text":
            errors.append(f"evidence_cards[{index}].verification.checked_against must be full-text")
        if not nonempty(verification.get("rationale")) or len(str(verification.get("rationale") or "")) < 30:
            errors.append(f"evidence_cards[{index}].verification.rationale must explain the entailment and scope")

    if rank >= READING_RANK["deep-read"] and contains_todo(note):
        errors.append("deep-read and later notes cannot contain TODO placeholders")
    if status in {"map-read", "deep-read"} and cards:
        warnings.append(f"{status} has evidence cards, but they cannot be projected until claim-verified/evidence-ready")
    return errors, warnings


def load_note(path: Path) -> dict[str, Any]:
    note = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(note, dict):
        raise ValueError("paper note must be a JSON object")
    return note


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_note")
    parser.add_argument("--json-output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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


if __name__ == "__main__":
    raise SystemExit(main())

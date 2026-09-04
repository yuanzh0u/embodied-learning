#!/usr/bin/env python3
"""Audit evidence-card locators and source contexts against complete extracted text.

This deterministic audit verifies provenance integrity, not semantic entailment.
The paper note must also contain a human/agent `verification` rationale for the
claim's wording and scope.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("validate_paper_note", SCRIPTS_DIR / "validate_paper_note.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-note", required=True)
    parser.add_argument("--extraction", required=True)
    parser.add_argument("--output")
    return parser.parse_args()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def normalize(text: Any) -> str:
    return " ".join(str(text or "").split()).lower()


def meaningful_tokens(text: Any) -> set[str]:
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z0-9]+(?:\.[0-9]+)?|[\u4e00-\u9fff]{2,}", str(text or ""))
        if len(token) > 1
    }


def extraction_text(extraction: dict[str, Any]) -> tuple[str, dict[int, str]]:
    method = str(extraction.get("extraction_method") or extraction.get("method") or "")
    ocr = extraction.get("ocr") if isinstance(extraction.get("ocr"), dict) else {}
    if method == "pdf-ocr" or ocr.get("pages_used") or extraction.get("ocr_pages"):
        raise ValueError("OCR-derived extraction is outside this workflow")
    if isinstance(extraction.get("text"), str) and extraction["text"].strip():
        return str(extraction["text"]), {}
    pages = extraction.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("complete extracted text/pages are missing")
    by_page: dict[int, str] = {}
    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            continue
        number = int(page.get("page") or index)
        if str(page.get("extraction_method") or "pdf-text") == "pdf-ocr":
            raise ValueError(f"page {number} uses OCR")
        by_page[number] = str(page.get("text") or "")
    return "\n".join(by_page[number] for number in sorted(by_page)), by_page


# IEEE-style hierarchical references: "VIII-B2) Title", "V-B.1 Title", "IV-C
# Title" point at the lettered subsection whose own label omits the parent
# roman numeral. Strip the prefix so the locator can still resolve; compound
# locators ("A / B", "A; B") resolve through each fragment separately.
HIERARCHICAL_PREFIX_RE = re.compile(r"^[ivx]+(?:[-.\u2013\u2014][a-z0-9]+)*[).\u2013\u2014]?\s+")
HIER_REF_RE = re.compile(r"^([IVX]{1,5})\s*[-\u2013\u2014.]?\s*([A-Z])\d{0,2}\s*[).\u2013\u2014]?\s+")
FRAGMENT_SPLIT_RE = re.compile(r"\s*[;/]\s+|\s+/\s+")


def locator_variants(fragment: str) -> list[str]:
    normalized = normalize(fragment)
    stripped = HIERARCHICAL_PREFIX_RE.sub("", normalized, count=1)
    variants = [normalized]
    if stripped and stripped != normalized and len(stripped) > 8:
        variants.append(stripped)
    return [variant for variant in variants if variant]


def _surface_for_section(section: dict[str, Any], full_text: str) -> str | None:
    title = str(section.get("title") or str(section.get("path") or "").split(">")[-1]).strip()
    heading = re.search(rf"(?im)^##\s+{re.escape(title)}\s*$", full_text)
    if not heading:
        return None
    next_heading = re.search(r"(?m)^##\s+", full_text[heading.end():])
    end = heading.end() + next_heading.start() if next_heading else len(full_text)
    return full_text[heading.start():end]


def _hierarchical_match(fragment: str, sections: list[Any]) -> int | None:
    """Resolve "VIII-B2)" / "V-B.1" to the lettered subsection under the roman section."""
    match = HIER_REF_RE.match(fragment)
    if not match:
        return None
    roman, letter = match.group(1).upper(), match.group(2).upper()
    under_roman = False
    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            continue
        number = str(section.get("number") or "").upper()
        if not under_roman:
            if number == roman:
                under_roman = True
        elif number == letter:
            return index
    return None


def section_surfaces(locator: str, full_text: str, extraction: dict[str, Any]) -> list[str]:
    sections = extraction.get("sections")
    if not isinstance(sections, list):
        return [full_text]
    fragments = [fragment.strip() for fragment in FRAGMENT_SPLIT_RE.split(locator) if fragment.strip()] or [locator]
    matched: set[int] = set()
    for fragment in fragments:
        variants = locator_variants(fragment)
        for index, section in enumerate(sections):
            if index in matched or not isinstance(section, dict):
                continue
            section_label = normalize(section.get("path") or section.get("title"))
            if section_label and any(variant in section_label or section_label in variant for variant in variants):
                matched.add(index)
        hierarchical_index = _hierarchical_match(fragment, sections)
        if hierarchical_index is not None:
            matched.add(hierarchical_index)
    surfaces: list[str] = []
    for index in sorted(matched):
        surface = _surface_for_section(sections[index], full_text)
        if surface and surface not in surfaces:
            surfaces.append(surface)
    return surfaces


def audit(note: dict[str, Any], extraction: dict[str, Any]) -> dict[str, Any]:
    validation_errors, validation_warnings = validator.validate_note(note)
    paper_id = str((note.get("paper") or {}).get("arxiv_id") or "")
    if validation_errors:
        return {
            "schema_version": 1,
            "paper_id": paper_id,
            "status": "reject",
            "reason": "paper-note validation failed",
            "validation_errors": validation_errors,
            "validation_warnings": validation_warnings,
            "cards": [],
        }
    try:
        full_text, by_page = extraction_text(extraction)
    except ValueError as exc:
        return {
            "schema_version": 1,
            "paper_id": paper_id,
            "status": "reject",
            "reason": str(exc),
            "validation_errors": [],
            "validation_warnings": validation_warnings,
            "cards": [],
        }

    results: list[dict[str, Any]] = []
    overall = "pass"
    for card in note.get("evidence_cards", []):
        locator = str(card.get("locator") or "")
        context = str(card.get("source_context") or "")
        page_match = re.search(r"\bpage\s+(\d+)\b|第\s*(\d+)\s*页", locator, re.I)
        if page_match and by_page:
            number = int(page_match.group(1) or page_match.group(2))
            candidates = [by_page.get(number, "")]
            locator_ok = number in by_page
        else:
            candidates = section_surfaces(locator, full_text, extraction)
            locator_ok = bool(candidates)
        if not candidates:
            candidates = [full_text]
        context_norm = normalize(context)
        context_tokens = meaningful_tokens(context)
        quantitative = card.get("quantitative", False)
        measurement_tokens: set[str] = set()
        if isinstance(quantitative, dict):
            measurement_tokens = meaningful_tokens(
                " ".join(str(quantitative.get(field) or "") for field in ("metric", "value_or_direction", "comparator"))
            )
        best: tuple[tuple[bool, bool, float], str, bool, float, bool] | None = None
        for surface in candidates:
            exact = context_norm in normalize(surface)
            surface_tokens = meaningful_tokens(surface)
            overlap = len(context_tokens & surface_tokens) / max(1, len(context_tokens))
            visible = measurement_tokens & surface_tokens
            quant_ok = not measurement_tokens or len(visible) / len(measurement_tokens) >= 0.34
            score = (exact, quant_ok, overlap)
            if best is None or score > best[0]:
                best = (score, surface, exact, overlap, quant_ok)
        assert best is not None
        _, surface, exact, overlap, quant_ok = best
        status = "pass"
        reasons: list[str] = []
        if not locator_ok:
            status = "reject"
            reasons.append("locator does not resolve in the extraction")
        if not exact:
            if overlap >= 0.6:
                if status != "reject":
                    status = "needs-review"
                reasons.append(f"source context is not an exact normalized match (token overlap {overlap:.2f})")
            else:
                status = "reject"
                reasons.append(f"source context cannot be located (token overlap {overlap:.2f})")
        if not quant_ok:
            if status != "reject":
                status = "needs-review"
            reasons.append("fewer than one third of quantitative metric/value/comparator tokens occur at the locator")

        verification = card.get("verification") if isinstance(card.get("verification"), dict) else {}
        if verification.get("status") != "passed" or verification.get("checked_against") != "full-text":
            status = "reject"
            reasons.append("manual semantic verification is not recorded as passed against full text")

        results.append(
            {
                "card_id": card.get("card_id"),
                "status": status,
                "locator": locator,
                "exact_context_match": exact,
                "token_overlap": round(overlap, 4),
                "reasons": reasons,
            }
        )
        if status == "reject":
            overall = "reject"
        elif status == "needs-review" and overall == "pass":
            overall = "needs-review"

    return {
        "schema_version": 1,
        "paper_id": paper_id,
        "status": overall,
        "reason": "all locator/context and manual-verification gates passed" if overall == "pass" else "one or more cards require attention",
        "validation_errors": [],
        "validation_warnings": validation_warnings,
        "cards": results,
    }


def main() -> int:
    args = parse_args()
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


if __name__ == "__main__":
    raise SystemExit(main())

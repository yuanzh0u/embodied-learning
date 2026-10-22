#!/usr/bin/env python3
"""Audit evidence-card locators and source contexts against complete extracted text.

This deterministic audit verifies provenance integrity, not semantic entailment.
The paper note must also contain a human/agent `verification` rationale for the
claim's wording and scope.

Library API: stateless explicit-parameter functions (:func:`audit`,
:func:`extraction_text`, :func:`locator_surface`, :func:`meaningful_tokens`,
:func:`normalize`, :func:`table_surface`). Consumers import this module
directly — build_paper_note.py /``meaningful_tokens``/``normalize``. The CLI
surface owns argument parsing and lives in the skill entry
``skills/embodied-ai-paper-reader/scripts/audit_claim_support.py``.
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


# PDF text extractors routinely emit Latin ligatures (ﬁ in
# "Simpliﬁcation"), so a verbatim quote typed with plain letters never matches
# the extracted full text. Folding them at normalize() time is what makes the
# quote gate mean "verbatim modulo typography" (2026-10-09: card 3 of
# 2507.15186 failed raw match and passed once ﬁ was folded — 130 occurrences).
_LIGATURE_FOLD = {
    "ﬀ": "ff",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬅ": "st",
    "ﬆ": "st",
}


def normalize(text: Any) -> str:
    out = str(text or "")
    for src, dst in _LIGATURE_FOLD.items():
        if src in out:
            out = out.replace(src, dst)
    return " ".join(out.split()).lower()


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
    # Sections synthesized from pdf-text pages carry their own body and the
    # flat full text has no `## page N` heading to slice against — take the
    # section's own text when it has one.
    own = str(section.get("text") or "")
    if own.strip():
        return own
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
    # Normalized sections (pages synthesize into one section each) so locator
    # resolution works for pdf-text extractions, not just html-latexml ones.
    sections = extraction_sections(extraction)
    if not isinstance(sections, list) or not sections:
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


def table_surface(extraction: dict[str, Any]) -> str:
    """Captions + cell text of every extracted table.

    Quantitative results canonically live in tables, and the HTML extractor
    keeps tables out of section prose entirely (often with ``section_index``
    unset, or set to wherever LaTeX parked the float rather than the section
    that discusses it — 2026-10-15 纹理映射: 5/12 papers lost every card to the
    quant gate because the numbers only existed here). The quote gate still
    binds a card to its locator; this surface only has to prove the
    measurement tokens are real extracted content of this paper, not
    hallucinated, so captions and cells count as visible."""

    chunks: list[str] = []
    for table in extraction.get("tables") or []:
        if not isinstance(table, dict):
            continue
        chunks.append(str(table.get("caption") or ""))
        rows = table.get("rows")
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, list):
                    chunks.append(" ".join(str(cell) for cell in row))
                else:
                    chunks.append(str(row))
    return "\n".join(chunks)


def extraction_sections(extraction: dict[str, Any]) -> list[Any]:
    """Section list in the shape the note pipeline expects.

    html-latexml extractions carry ``sections``; pdf-text extractions carry
    only ``pages``. Both are full-text extractions, so normalizing pages into
    one section each keeps locator resolution, rapid-role labeling, and
    body-quote recovery working for PDF-sourced papers. Without this a
    PDF paper's evidence cards all died in the "quote only in Abstract"
    branch because the body rescan over an empty ``sections`` found nothing
    (2026-10-08, 2507.15186: 4/4 cards dropped, note rejected)."""
    sections = extraction.get("sections")
    if isinstance(sections, list) and sections:
        return sections
    pages = extraction.get("pages")
    if not isinstance(pages, list):
        return []
    out: list[Any] = []
    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            continue
        number = page.get("page") or index
        text = str(page.get("text") or "")
        if not text.strip():
            continue
        label = f"page {number}"
        out.append({"title": label, "path": label, "text": text, "page": number})
    return out


def locator_surface(
    locator: str,
    full_text: str,
    by_page: dict[int, str],
    extraction: dict[str, Any],
) -> tuple[str, bool]:
    """One surface for ``locator`` plus whether the locator actually resolved.

    Page-number locators resolve against ``by_page``; every other locator goes
    through :func:`section_surfaces` (hierarchical refs, compound fragments).
    ``(full_text, False)`` is the unresolved fallback — callers treat it as a
    hint-only match rather than an auditable one."""
    match = re.search(r"\bpage\s+(\d+)\b|第\s*(\d+)\s*页", locator, re.I)
    if match and by_page:
        number = int(match.group(1) or match.group(2))
        return by_page.get(number, ""), number in by_page
    surfaces = section_surfaces(locator, full_text, extraction)
    if surfaces and surfaces[0] != full_text:
        return surfaces[0], True
    if surfaces:
        return surfaces[0], True
    return full_text, False


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
    table_tokens = meaningful_tokens(table_surface(extraction))
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
            # Measurement tokens may verify in the locator's prose OR in the
            # paper's tables (see table_surface) — table numbers never appear
            # in section prose.
            visible = measurement_tokens & (surface_tokens | table_tokens)
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
            reasons.append(
                "fewer than one third of quantitative metric/value/comparator tokens "
                "occur at the locator or in the paper's tables"
            )

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

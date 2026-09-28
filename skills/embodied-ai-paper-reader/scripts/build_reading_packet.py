#!/usr/bin/env python3
"""Build a complete reading packet and an optional paper-note template.

The input extraction must contain the complete HTML text (`text`) or every
text-layer PDF page (`pages`). Ranked/selected passages alone are rejected.
OCR-derived and scan-only papers are outside this workflow.

By default the packet still embeds the complete extracted text (backward
compatible). Prefer ``--summary-first`` for LLM scoping passes: the packet then
carries a structure map plus truncated section windows; keep the full
extraction JSON on disk for locator windows and claim-support audits.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MODES = {"rapid", "scoping", "systematic"}
DEFAULT_MAX_SECTION_CHARS = 4000


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extraction", required=True, help="Complete Hub extraction JSON.")
    parser.add_argument("--metadata", help="Optional per-paper metadata JSON.")
    parser.add_argument("--review-question", required=True)
    parser.add_argument("--topic-id", action="append", default=[], required=True)
    parser.add_argument("--review-mode", choices=sorted(MODES), default="scoping")
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
        default=DEFAULT_MAX_SECTION_CHARS,
        help=(
            f"When --summary-first is set, truncate each section/page window to this many "
            f"characters (default {DEFAULT_MAX_SECTION_CHARS}). Ignored in full-text mode."
        ),
    )
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help="Force embedding Complete extracted text even when --summary-first is set.",
    )
    return parser.parse_args(argv)


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def extraction_method(extraction: dict[str, Any]) -> str:
    return str(extraction.get("extraction_method") or extraction.get("method") or "")


def extraction_quality(extraction: dict[str, Any]) -> str:
    quality = extraction.get("quality")
    if isinstance(quality, dict):
        return str(quality.get("grade") or "")
    return str(quality or "")


def ocr_pages(extraction: dict[str, Any]) -> list[Any]:
    ocr = extraction.get("ocr")
    if isinstance(ocr, dict) and isinstance(ocr.get("pages_used"), list):
        return list(ocr["pages_used"])
    pages = extraction.get("ocr_pages")
    return list(pages) if isinstance(pages, list) else []


def complete_text(extraction: dict[str, Any]) -> tuple[str, str]:
    method = extraction_method(extraction)
    if method == "pdf-ocr" or ocr_pages(extraction):
        raise ValueError("OCR-derived text is outside this workflow; mark the paper unavailable")
    if not extraction.get("available", True) or not extraction.get("evidence_eligible", True):
        raise ValueError("extraction is not available/evidence-eligible")
    quality = extraction_quality(extraction)
    if quality not in {"high", "medium"}:
        raise ValueError(f"extraction quality must be high or medium, got {quality or 'missing'}")

    source_format = str(extraction.get("source_format") or ("pdf" if method == "pdf-text" else "html"))
    if source_format == "html":
        text = extraction.get("text")
        if not isinstance(text, str) or len(re.sub(r"\s+", "", text)) < 500:
            raise ValueError("HTML extraction lacks complete `text`; selected passages are insufficient")
        return source_format, text
    if source_format == "pdf":
        pages = extraction.get("pages")
        if not isinstance(pages, list) or not pages:
            raise ValueError("PDF extraction lacks complete `pages`; ranked pages are insufficient")
        rendered: list[str] = []
        for index, page in enumerate(pages, start=1):
            if not isinstance(page, dict):
                raise ValueError(f"pages[{index - 1}] must be an object")
            number = page.get("page", index)
            text = str(page.get("text") or "")
            if not text.strip():
                raise ValueError(f"page {number} has no text; scan-only/partial PDFs are unavailable")
            if str(page.get("extraction_method") or "pdf-text") == "pdf-ocr":
                raise ValueError(f"page {number} uses OCR, which is outside this workflow")
            rendered.append(f"## page {number}\n\n{text}")
        return source_format, "\n\n".join(rendered)
    raise ValueError(f"unsupported source_format: {source_format or 'missing'}")


def normalize_metadata(metadata: dict[str, Any], extraction: dict[str, Any]) -> dict[str, Any]:
    paper = metadata.get("paper") if isinstance(metadata.get("paper"), dict) else metadata
    paper_id = str(paper.get("arxiv_id") or paper.get("paper_id") or extraction.get("paper_id") or "")
    paper_id = re.sub(r"v\d+$", "", paper_id.rsplit("/", 1)[-1].removesuffix(".pdf"))
    authors = paper.get("authors") if isinstance(paper.get("authors"), list) else []
    return {
        "arxiv_id": paper_id,
        "title": str(paper.get("title") or paper_id or "Untitled paper"),
        "published": str(paper.get("published") or ""),
        "url": str(paper.get("url") or (f"https://arxiv.org/abs/{paper_id}" if paper_id else "")),
        "authors": authors,
    }


def render_structure(extraction: dict[str, Any], source_format: str) -> list[str]:
    if source_format == "html" and isinstance(extraction.get("sections"), list):
        lines = []
        for section in extraction["sections"]:
            if isinstance(section, dict):
                lines.append(
                    f"- {section.get('path') or section.get('title') or section.get('id')} "
                    f"({section.get('char_count', '?')} chars)"
                )
        return lines
    pages = extraction.get("pages")
    if source_format == "pdf" and isinstance(pages, list):
        return [f"- page {page.get('page', index)}" for index, page in enumerate(pages, start=1) if isinstance(page, dict)]
    return ["- No machine-readable outline; map headings manually from the complete text."]


def truncate_window(text: str, limit: int) -> str:
    cleaned = text.strip()
    if limit <= 0 or len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(0, limit - 1)].rstrip() + "…"


def section_windows(
    extraction: dict[str, Any],
    source_format: str,
    full_text: str,
    max_section_chars: int,
) -> list[str]:
    """Build truncated section/page windows for summary-first packets."""
    lines: list[str] = []
    if source_format == "html" and isinstance(extraction.get("sections"), list) and extraction["sections"]:
        # Prefer explicit section text when present; otherwise slice by title from full text.
        for section in extraction["sections"]:
            if not isinstance(section, dict):
                continue
            label = str(section.get("path") or section.get("title") or section.get("id") or "section")
            body = section.get("text") or section.get("content")
            if isinstance(body, str) and body.strip():
                window = truncate_window(body, max_section_chars)
            else:
                # Best-effort: find the heading in full text and take the next window.
                title = str(section.get("title") or section.get("path") or "")
                window = ""
                if title:
                    idx = full_text.find(title)
                    if idx >= 0:
                        window = truncate_window(full_text[idx:], max_section_chars)
                if not window:
                    window = truncate_window(full_text, max_section_chars)
            lines.extend([f"### {label}", "", window, ""])
        return lines

    if source_format == "pdf" and isinstance(extraction.get("pages"), list):
        for index, page in enumerate(extraction["pages"], start=1):
            if not isinstance(page, dict):
                continue
            number = page.get("page", index)
            window = truncate_window(str(page.get("text") or ""), max_section_chars)
            lines.extend([f"### page {number}", "", window, ""])
        return lines

    # Fallback: leading window of the complete text plus a reminder to open extraction on disk.
    lines.extend(
        [
            "### leading-window",
            "",
            truncate_window(full_text, max_section_chars),
            "",
            "_No structured sections/pages available; open the extraction JSON for locator windows._",
            "",
        ]
    )
    return lines


def note_template(
    paper: dict[str, Any],
    extraction: dict[str, Any],
    question: str,
    topic_ids: list[str],
    mode: str,
    source_format: str,
) -> dict[str, Any]:
    quality = extraction_quality(extraction)
    return {
        "schema_version": 1,
        "paper": paper,
        "review": {"question": question, "topic_ids": topic_ids, "mode": mode},
        "extraction": {
            "source_format": source_format,
            "method": extraction_method(extraction),
            "quality": quality,
            "full_text_available": True,
            "ocr_pages": [],
            "visual_validation": "passed" if quality == "medium" else "not-required",
        },
        "reading": {
            "status": "full-text-recovered",
            "paper_type": "TODO",
            "relevance": {"decision": "TODO", "reason": "TODO"},
            "sections_read": [],
            "sections_skipped": [],
        },
        "research_question": "TODO",
        "contributions": [],
        "method": {"summary": "TODO", "assumptions": []},
        "study_context": {"datasets": [], "tasks": [], "embodiments": [], "sample_or_scale": "TODO"},
        "evaluation": {"design": "TODO", "baselines": [], "metrics": [], "ablations": []},
        "findings": [],
        "limitations": {"author_status": "TODO", "author_stated": [], "reader_inferred": []},
        "transfer_boundary": "TODO",
        "critical_appraisal": {
            "design_strengths": [],
            "design_risks": [],
            "baseline_fairness": "TODO",
            "metric_validity": "TODO",
            "reproducibility": "TODO",
            "external_validity": "TODO",
        },
        "evidence_cards": [],
        "core_citations": [],
        "notes": "",
    }


def build_packet_lines(
    paper: dict[str, Any],
    extraction: dict[str, Any],
    source_format: str,
    text: str,
    review_question: str,
    topic_ids: list[str],
    review_mode: str,
    summary_first: bool,
    max_section_chars: int,
    include_full_text: bool,
    extraction_path: str | None = None,
) -> list[str]:
    embed_full = include_full_text or not summary_first
    lines = [
        f"# Reading Packet: {paper['title']}",
        "",
        f"- Paper: {paper['url'] or paper['arxiv_id']}",
        f"- Review question: {review_question}",
        f"- Topic IDs: {', '.join(topic_ids)}",
        f"- Review mode: {review_mode}",
        f"- Extraction: {extraction_method(extraction)} / {extraction_quality(extraction)}",
        "- Status at packet creation: full-text-recovered (not yet map-read or deep-read)",
        f"- Packet mode: {'summary-first' if summary_first and not include_full_text else 'full-text'}",
        f"- Complete text chars (on disk): {len(text)}",
    ]
    if extraction_path:
        lines.append(f"- Extraction path (source of truth for locator windows): `{extraction_path}`")
    lines.extend(
        [
            "",
            "## Required reading roles",
            "",
            "Map problem, method/design, results/analysis, conclusion/limitations, and any relevant appendix before writing evidence cards.",
            "",
            "## Document structure",
            "",
            *render_structure(extraction, source_format),
            "",
        ]
    )
    if summary_first and not include_full_text:
        lines.extend(
            [
                "## Summary-first section windows",
                "",
                f"Each window is truncated to ≤{max_section_chars} characters. "
                "Do **not** paste Complete extracted text into LLM context for scoping. "
                "For claim cards, open the extraction JSON (or a targeted locator window) instead.",
                "",
                *section_windows(extraction, source_format, text, max_section_chars),
            ]
        )
    if embed_full:
        lines.extend(
            [
                "## Complete extracted text",
                "",
                text,
                "",
            ]
        )
    elif summary_first:
        lines.extend(
            [
                "## Complete extracted text",
                "",
                "_Omitted from this summary-first packet. Full text remains in the extraction JSON "
                "on disk for locator windows and `audit_claim_support.py`._",
                "",
            ]
        )
    return lines


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        extraction_path = Path(args.extraction)
        extraction = load_object(extraction_path)
        metadata = load_object(Path(args.metadata)) if args.metadata else {}
        source_format, text = complete_text(extraction)
        paper = normalize_metadata(metadata, extraction)
        if args.max_section_chars < 0:
            raise ValueError("--max-section-chars must be >= 0")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"reading packet blocked: {exc}", file=sys.stderr)
        return 2

    lines = build_packet_lines(
        paper,
        extraction,
        source_format,
        text,
        args.review_question,
        args.topic_id,
        args.review_mode,
        summary_first=args.summary_first,
        max_section_chars=args.max_section_chars,
        include_full_text=args.include_full_text,
        extraction_path=str(extraction_path),
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    if args.note_template:
        target = Path(args.note_template)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(
                note_template(paper, extraction, args.review_question, args.topic_id, args.review_mode, source_format),
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    mode = "summary-first" if args.summary_first and not args.include_full_text else "full-text"
    print(f"Wrote {mode} reading packet: {output}")
    if args.note_template:
        print(f"Wrote paper-note template: {args.note_template}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

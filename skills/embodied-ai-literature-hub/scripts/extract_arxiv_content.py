#!/usr/bin/env python3
"""Extract arXiv full text through HTML -> PDF text with quality gates.

OCR options remain for compatibility with older callers, but the current
paper-reading workflow uses ``--ocr-mode never`` and treats scan-only PDFs as
unavailable.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent


def load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


extract_arxiv_html = load_sibling("extract_arxiv_html")
extract_arxiv_pdf = load_sibling("extract_arxiv_pdf")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--terms", required=True, help="Comma-separated topic terms.")
    parser.add_argument("--html-url")
    parser.add_argument("--pdf-url")
    parser.add_argument("--pdf-file", help="Local PDF for testing/offline extraction.")
    parser.add_argument("--html-cache-dir", default=extract_arxiv_html.DEFAULT_CACHE_DIR)
    parser.add_argument("--pdf-cache-dir", default=extract_arxiv_pdf.DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--top-sections", type=int, default=6)
    parser.add_argument("--max-pages", type=int, default=0)
    parser.add_argument("--ocr-mode", choices=["auto", "never", "always"], default="auto")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument("--ocr-dpi", type=int, default=220)
    parser.add_argument("--min-chars-per-page", type=int, default=180)
    parser.add_argument("--minimum-html-chars", type=int, default=1000)
    parser.add_argument("--force-pdf", action="store_true", help="Skip HTML and exercise PDF/OCR path.")
    parser.add_argument("--include-selected-text", action="store_true")
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help="Include complete HTML text or every text-layer PDF page for $embodied-ai-paper-reader.",
    )
    parser.add_argument("--output", help="Write JSON here instead of stdout.")
    return parser.parse_args()


def normalize_id(value: str) -> str:
    return re.sub(r"v\d+$", "", value.rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html"))


def html_quality(output: dict[str, Any], minimum_chars: int) -> dict[str, object]:
    chars = int(output.get("text_chars") or 0)
    structure = str(output.get("structure") or "unavailable")
    if structure == "latexml" and chars >= max(2000, minimum_chars):
        grade = "high"
    elif structure in {"latexml", "flat"} and chars >= minimum_chars:
        grade = "medium"
    else:
        grade = "low"
    return {"grade": grade, "text_chars": chars, "structure": structure}


def try_html(args: argparse.Namespace, terms: list[str]) -> dict[str, Any]:
    url = args.html_url or f"https://arxiv.org/html/{normalize_id(args.paper_id)}"
    target = Path(args.html_cache_dir).expanduser() / f"{normalize_id(args.paper_id)}.html"
    available, html = extract_arxiv_html.fetch_html(url, target, args.timeout)
    html_args = argparse.Namespace(
        paper_id=args.paper_id,
        terms=",".join(terms),
        max_chars=0,
        include_text=bool(getattr(args, "include_full_text", False)),
        top_sections=args.top_sections,
        include_section_text=bool(args.include_selected_text or getattr(args, "include_full_text", False)),
    )
    output = extract_arxiv_html.build_output(html_args, url, target, available, html)
    output["quality"] = html_quality(output, args.minimum_html_chars)
    output["extraction_method"] = f"html-{output.get('structure')}"
    output["source_format"] = "html"
    output["evidence_eligible"] = bool(available) and output["quality"]["grade"] in {"high", "medium"}
    output["needs_visual_validation"] = False
    output["selected_passages"] = output.get("ranked_sections", [])
    return output


def try_pdf(args: argparse.Namespace, terms: list[str]) -> dict[str, Any]:
    pdf_args = argparse.Namespace(
        paper_id=args.paper_id,
        pdf_url=args.pdf_url,
        pdf_file=args.pdf_file,
        cache_dir=args.pdf_cache_dir,
        max_pages=args.max_pages,
        top_pages=args.top_sections,
        ocr_mode=args.ocr_mode,
        ocr_language=args.ocr_language,
        ocr_dpi=args.ocr_dpi,
        min_chars_per_page=args.min_chars_per_page,
        include_pages=bool(args.include_selected_text or getattr(args, "include_full_text", False)),
        terms=",".join(terms),
    )
    output = extract_arxiv_pdf.extract_pdf_document(pdf_args)
    output["source_format"] = "pdf"
    output["selected_passages"] = output.get("ranked_pages", [])
    # Selected page text is already in ranked_pages. Keep every page only when
    # the downstream paper reader explicitly requests a complete reading input.
    if not getattr(args, "include_full_text", False):
        output.pop("pages", None)
    return output


def extract_content(args: argparse.Namespace) -> dict[str, Any]:
    terms = [term.strip() for term in args.terms.split(",") if term.strip()]
    attempts: list[dict[str, Any]] = []
    if not args.force_pdf:
        try:
            html = try_html(args, terms)
            attempts.append(
                {
                    "method": html["extraction_method"],
                    "available": html.get("available", False),
                    "quality": html["quality"]["grade"],
                }
            )
            if html.get("evidence_eligible"):
                html["attempts"] = attempts
                html["fallback_reason"] = ""
                return html
            fallback_reason = "HTML unavailable or below the minimum full-text quality gate."
        except Exception as exc:  # pragma: no cover - network/parser dependent
            attempts.append({"method": "html", "available": False, "quality": "low", "error": str(exc)})
            fallback_reason = f"HTML extraction failed: {exc}"
    else:
        fallback_reason = "PDF path forced by caller."

    try:
        pdf = try_pdf(args, terms)
        attempts.append(
            {
                "method": pdf.get("extraction_method", "pdf"),
                "available": pdf.get("available", False),
                "quality": (pdf.get("quality") or {}).get("grade", "low"),
                "ocr_pages": (pdf.get("ocr") or {}).get("pages_used", []),
            }
        )
        pdf["attempts"] = attempts
        pdf["fallback_reason"] = fallback_reason
        return pdf
    except Exception as exc:  # pragma: no cover - network/PDF dependent
        attempts.append({"method": "pdf", "available": False, "quality": "low", "error": str(exc)})
        return {
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "paper_id": normalize_id(args.paper_id),
            "available": False,
            "source_format": "metadata-only",
            "extraction_method": "unavailable",
            "quality": {"grade": "low", "text_chars": 0},
            "evidence_eligible": False,
            "needs_visual_validation": False,
            "selected_passages": [],
            "term_matches": [],
            "reference_hints": [],
            "attempts": attempts,
            "fallback_reason": fallback_reason,
        }


def main() -> int:
    args = parse_args()
    output = extract_content(args)
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if output.get("evidence_eligible") else 2


if __name__ == "__main__":
    raise SystemExit(main())

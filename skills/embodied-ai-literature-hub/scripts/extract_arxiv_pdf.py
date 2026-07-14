#!/usr/bin/env python3
"""Download/cache an arXiv PDF, extract text, and OCR low-quality pages when needed."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import site
import statistics
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


DEFAULT_CACHE_DIR = os.path.join(
    os.environ.get("TMPDIR") or "/private/tmp",
    "embodied-ai-literature-hub",
    "pdfs",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID, with or without version.")
    parser.add_argument("--pdf-url", help="PDF URL. Defaults to https://arxiv.org/pdf/<paper-id>.pdf")
    parser.add_argument("--pdf-file", help="Use an existing local PDF instead of downloading.")
    parser.add_argument("--terms", help="Comma-separated terms to locate in extracted text.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--max-pages", type=int, default=0, help="0 means all pages.")
    parser.add_argument("--top-pages", type=int, default=8, help="Ranked topic-relevant pages to report.")
    parser.add_argument("--ocr-mode", choices=["auto", "never", "always"], default="auto")
    parser.add_argument("--ocr-language", default="eng", help="Tesseract language expression, e.g. eng or eng+chi_sim.")
    parser.add_argument("--ocr-dpi", type=int, default=220)
    parser.add_argument("--min-chars-per-page", type=int, default=180)
    parser.add_argument("--include-pages", action="store_true", help="Include full extracted page text in JSON output.")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args()


def import_pypdf():
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as first_error:  # pragma: no cover - depends on runtime
        roots = sorted(
            (Path.home() / ".cache" / "codex-runtimes").glob(
                "*/dependencies/python/lib/python*/site-packages"
            )
        )
        for root in roots:
            site.addsitedir(str(root))
            try:
                from pypdf import PdfReader  # type: ignore
                break
            except Exception:
                continue
        else:
            raise SystemExit(
                "pypdf is required for PDF extraction. Load the Codex workspace dependencies or use their bundled Python runtime."
            ) from first_error
    return PdfReader


def normalize_id(value: str) -> str:
    value = value.rsplit("/", 1)[-1]
    value = value.removesuffix(".pdf")
    return re.sub(r"v\d+$", "", value)


def pdf_url(args: argparse.Namespace) -> str:
    if args.pdf_url:
        return args.pdf_url
    if not args.paper_id:
        raise SystemExit("Provide --paper-id or --pdf-url.")
    return f"https://arxiv.org/pdf/{normalize_id(args.paper_id)}.pdf"


def cache_path(args: argparse.Namespace, url: str) -> Path:
    base = normalize_id(args.paper_id or url)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return Path(args.cache_dir).expanduser() / f"{safe}.pdf"


def download(url: str, target: Path, timeout: float = 90.0) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "embodied-ai-literature-hub/1.0 (research workflow)"},
    )
    with urllib.request.urlopen(request, timeout=max(1.0, timeout)) as response:
        target.write_bytes(response.read())


def extract_pages(pdf_file: Path, max_pages: int) -> list[dict[str, object]]:
    PdfReader = import_pypdf()
    reader = PdfReader(str(pdf_file))
    limit = len(reader.pages) if max_pages <= 0 else min(len(reader.pages), max_pages)
    pages = []
    for index in range(limit):
        text = reader.pages[index].extract_text() or ""
        pages.append(
            {
                "page": index + 1,
                "text": "\n".join(line.rstrip() for line in text.splitlines()),
                "extraction_method": "pdf-text",
            }
        )
    return pages


def nonspace_chars(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def text_quality(pages: list[dict[str, object]], min_chars_per_page: int = 180) -> dict[str, object]:
    counts = [nonspace_chars(str(page.get("text") or "")) for page in pages]
    joined = "".join(str(page.get("text") or "") for page in pages)
    nonspace = re.sub(r"\s+", "", joined)
    covered = sum(count >= min_chars_per_page for count in counts)
    coverage = covered / max(1, len(counts))
    median_chars = statistics.median(counts) if counts else 0.0
    replacement_rate = nonspace.count("\ufffd") / max(1, len(nonspace))
    wordish_rate = len(re.findall(r"[A-Za-z0-9\u4e00-\u9fff]", nonspace)) / max(1, len(nonspace))
    if coverage >= 0.85 and median_chars >= 500 and replacement_rate <= 0.01 and wordish_rate >= 0.45:
        grade = "high"
    elif coverage >= 0.55 and median_chars >= min_chars_per_page and replacement_rate <= 0.03 and wordish_rate >= 0.30:
        grade = "medium"
    else:
        grade = "low"
    return {
        "grade": grade,
        "page_count": len(pages),
        "pages_above_minimum": covered,
        "page_coverage": round(coverage, 4),
        "median_nonspace_chars": round(float(median_chars), 1),
        "total_nonspace_chars": len(nonspace),
        "replacement_char_rate": round(replacement_rate, 6),
        "wordish_char_rate": round(wordish_rate, 4),
        "low_text_pages": [
            int(page["page"]) for page, count in zip(pages, counts) if count < min_chars_per_page
        ],
    }


def ocr_tools() -> tuple[str | None, str | None]:
    return shutil.which("pdftoppm"), shutil.which("tesseract")


def ocr_page(
    pdf_file: Path,
    page_number: int,
    language: str,
    dpi: int,
    pdftoppm: str,
    tesseract: str,
) -> str:
    with tempfile.TemporaryDirectory(prefix="arxiv-pdf-ocr-") as tmpdir:
        prefix = Path(tmpdir) / f"page-{page_number}"
        subprocess.run(
            [
                pdftoppm,
                "-f", str(page_number),
                "-l", str(page_number),
                "-r", str(dpi),
                "-png",
                "-singlefile",
                str(pdf_file),
                str(prefix),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        image = prefix.with_suffix(".png")
        completed = subprocess.run(
            [tesseract, str(image), "stdout", "-l", language, "--psm", "6"],
            check=True,
            capture_output=True,
            text=True,
        )
        return "\n".join(line.rstrip() for line in completed.stdout.splitlines()).strip()


def apply_ocr(
    pdf_file: Path,
    pages: list[dict[str, object]],
    mode: str,
    language: str,
    dpi: int,
    min_chars_per_page: int,
) -> tuple[list[int], list[str], str]:
    if mode == "never":
        return [], [], "none"
    targets = [
        int(page["page"])
        for page in pages
        if mode == "always" or nonspace_chars(str(page.get("text") or "")) < min_chars_per_page
    ]
    if not targets:
        return [], [], "none"
    pdftoppm, tesseract = ocr_tools()
    if not pdftoppm or not tesseract:
        missing = ", ".join(name for name, path in (("pdftoppm", pdftoppm), ("tesseract", tesseract)) if not path)
        return [], [f"OCR requested for pages {targets}, but tools are unavailable: {missing}"], "unavailable"
    backend = "tesseract"
    used: list[int] = []
    warnings: list[str] = []
    by_page = {int(page["page"]): page for page in pages}
    for page_number in targets:
        try:
            text = ocr_page(pdf_file, page_number, language, dpi, pdftoppm, tesseract)
        except Exception as exc:  # pragma: no cover - depends on local binaries/PDF
            warnings.append(f"page {page_number}: OCR failed: {exc}")
            continue
        page = by_page[page_number]
        if nonspace_chars(text) > nonspace_chars(str(page.get("text") or "")):
            page["text"] = text
            page["extraction_method"] = "pdf-ocr"
            used.append(page_number)
    return used, warnings, backend


def find_matches(pages: list[dict[str, object]], terms: list[str], window: int = 220) -> list[dict[str, object]]:
    matches = []
    lowered_terms = [term.lower() for term in terms if term.strip()]
    if not lowered_terms:
        return matches
    for page in pages:
        text = str(page["text"])
        lowered = text.lower()
        for term in lowered_terms:
            start = 0
            while True:
                index = lowered.find(term, start)
                if index < 0:
                    break
                left = max(0, index - window)
                right = min(len(text), index + len(term) + window)
                snippet = " ".join(text[left:right].split())
                matches.append(
                    {
                        "page": page["page"],
                        "locator": f"page {page['page']}",
                        "term": term,
                        "snippet": snippet,
                        "extraction_method": page.get("extraction_method", "pdf-text"),
                    }
                )
                start = index + len(term)
                if len(matches) >= 80:
                    return matches
    return matches


def rank_pages(
    pages: list[dict[str, object]],
    terms: list[str],
    top: int = 8,
    include_text: bool = False,
) -> list[dict[str, object]]:
    ranked: list[dict[str, object]] = []
    lowered_terms = [term.lower() for term in terms if term.strip()]
    for page in pages:
        text = str(page.get("text") or "")
        lowered = text.lower()
        hits = {term: lowered.count(term) for term in lowered_terms}
        total = sum(hits.values())
        if lowered_terms and total == 0:
            continue
        record: dict[str, object] = {
            "page": page["page"],
            "locator": f"page {page['page']}",
            "score": total,
            "hits": total,
            "matched_terms": sorted(term for term, count in hits.items() if count),
            "extraction_method": page.get("extraction_method", "pdf-text"),
        }
        if include_text:
            record["text"] = text
        ranked.append(record)
    ranked.sort(key=lambda item: (-int(item["score"]), int(item["page"])))
    return ranked[:top]


def reference_hints(pages: list[dict[str, object]]) -> list[dict[str, str]]:
    joined = "\n".join(f"\n--- page {page['page']} ---\n{page['text']}" for page in pages[-8:])
    refs_index = joined.lower().find("references")
    if refs_index >= 0:
        joined = joined[refs_index:]
    hints = []
    seen = set()
    for line in joined.splitlines():
        compact = " ".join(line.split())
        if not compact:
            continue
        ids = re.findall(r"arXiv[:\s]+(\d{4}\.\d{4,5})(?:v\d+)?", compact, flags=re.IGNORECASE)
        if not ids:
            ids = re.findall(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b", compact)
        for arxiv_id in ids:
            if arxiv_id not in seen:
                seen.add(arxiv_id)
                hints.append({"arxiv_id": arxiv_id, "line": compact[:500]})
    return hints[:60]


def extract_pdf_document(args: argparse.Namespace) -> dict[str, object]:
    if args.pdf_file:
        target = Path(args.pdf_file).expanduser().resolve()
        if not target.is_file():
            raise FileNotFoundError(f"PDF file not found: {target}")
        url = args.pdf_url or (f"https://arxiv.org/pdf/{normalize_id(args.paper_id)}.pdf" if args.paper_id else "")
    else:
        url = pdf_url(args)
        target = cache_path(args, url)
        download(url, target, getattr(args, "timeout", 90.0))
    pages = extract_pages(target, args.max_pages)
    before_ocr = text_quality(pages, args.min_chars_per_page)
    ocr_pages, warnings, ocr_backend = apply_ocr(
        target,
        pages,
        args.ocr_mode,
        args.ocr_language,
        args.ocr_dpi,
        args.min_chars_per_page,
    )
    quality = text_quality(pages, args.min_chars_per_page)
    terms = [term.strip() for term in (args.terms or "").split(",") if term.strip()]
    output: dict[str, object] = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(args.paper_id or url or target.name),
        "pdf_url": url,
        "cache_file": str(target),
        "available": bool(pages),
        "extraction_method": "pdf-ocr" if ocr_pages else "pdf-text",
        "evidence_eligible": quality["grade"] in {"high", "medium"},
        "quality": quality,
        "quality_before_ocr": before_ocr,
        "ocr": {
            "mode": args.ocr_mode,
            "backend": ocr_backend,
            "language": args.ocr_language,
            "pages_used": ocr_pages,
            "warnings": warnings,
        },
        "needs_visual_validation": bool(ocr_pages) or quality["grade"] != "high",
        "visual_validation_pages": sorted(set(ocr_pages) | set(quality["low_text_pages"]))[:12],
        "page_count_extracted": len(pages),
        "term_matches": find_matches(pages, terms),
        "ranked_pages": rank_pages(pages, terms, args.top_pages, include_text=args.include_pages),
        "reference_hints": reference_hints(pages),
    }
    if args.include_pages:
        output["pages"] = pages
    return output


def main() -> int:
    args = parse_args()
    output = extract_pdf_document(args)
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())

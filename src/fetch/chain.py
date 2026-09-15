#!/usr/bin/env python3
"""Extract arXiv full text through HTML -> PDF text with quality gates.

OCR options remain for compatibility with older callers, but the current
paper-reading workflow uses ``--ocr-mode never`` and treats scan-only PDFs as
unavailable.

Human-friendly shortcuts over the plain flags:

- ``--format`` defaults to ``auto``: markdown when writing to a ``.md`` file or
  printing to a terminal, JSON otherwise (pipe/file redirects get JSON).
- ``markdown`` output always includes full text, so ``--include-full-text``
  does not need to be remembered.
- ``--terms`` is optional for casual reading; ranking/term matching is simply
  skipped when omitted.
- Bare arXiv ID positional: ``extract_arxiv 2403.12550``.
- ``--output/-o`` is optional: interactively it defaults to
  ``/tmp/<paper-id>.md``; a directory argument gets ``<paper-id>.md`` appended.
  Piped stdout stays stdout unless ``-o`` is explicit.
"""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "/tmp"

from src.fetch import html as extract_arxiv_html, pdf as extract_arxiv_pdf
# The TeX tier is loaded lazily inside try_tex(): it only needs boto3/pypandoc
# when actually exercised, and the default html-first chain must not pay for it.
extract_arxiv_tex: Any = None


def _load_tex_tier():
    global extract_arxiv_tex
    if extract_arxiv_tex is None:
        from src.fetch import tex as tex_module
        extract_arxiv_tex = tex_module
    return extract_arxiv_tex


def extract_arxiv_tex_default_cache_dir() -> str:
    """TeX tarball cache default without importing the (optionally-depended) tier."""
    return "/tmp/embodied-ai-literature-hub/src"


VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}


class DocumentTitleParser(HTMLParser):
    """Pull the document title from LaTeXML HTML, ignoring nested markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.capture_kind: str | None = None  # "h1" | "title"
        self.capture_depth = 0
        self.h1_parts: list[str] = []
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str,
                        attrs) -> None:  # type: ignore[no-untyped-def]
        tag = tag.lower()
        if tag in {"script", "style", "svg", "math"}:
            self.skip_depth += 1
            return
        if tag in VOID_ELEMENTS:
            return  # never closed; must not inflate capture_depth
        if self.capture_kind:
            self.capture_depth += 1
            return
        classes = " ".join(value or "" for key, value in attrs
                           if key == "class")
        if tag == "h1" and "ltx_title_document" in classes.split():
            self.capture_kind = "h1"
        elif tag == "title":
            self.capture_kind = "title"

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg", "math"}:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if tag in VOID_ELEMENTS:
            return
        if self.capture_kind:
            if self.capture_depth == 0:
                self.capture_kind = None
            else:
                self.capture_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.capture_kind == "h1":
            self.h1_parts.append(data)
        elif self.capture_kind == "title":
            self.title_parts.append(data)

    def title(self) -> str:
        # A sane document h1 is short; an over-long capture means the depth
        # tracking was defeated by malformed markup, so fall back to <title>.
        h1 = " ".join(" ".join(self.h1_parts).split())
        if not h1 or len(h1) > 400:
            h1 = " ".join(self.title_parts)
        return h1


def document_title(html: str) -> str:
    """Best-effort document title: LaTeXML h1, then <title> minus arXiv suffix."""
    if not html:
        return ""
    parser = DocumentTitleParser()
    try:
        parser.feed(html)
    except Exception:  # pragma: no cover - defensive for odd encodings
        return ""
    title = parser.title()
    if not title:
        return ""
    # arXiv conventions: `<title>[ID] Paper name - arXiv:ID</title>`
    title = re.sub(r"arXiv[:\s]*\d{4}\.\d{4,5}(?:v\d+)?\s*$",
                   "",
                   title,
                   flags=re.IGNORECASE)
    title = re.sub(r"^\[?\d{4}\.\d{4,5}(?:v\d+)?\]?\s*", "", title)
    return title.strip(" -—")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "paper_id_pos", nargs="?",
        help=argparse.SUPPRESS)  # shortcut: leading bare arXiv ID
    parser.add_argument("--paper-id",
                        help="arXiv ID (with or without version).")
    parser.add_argument(
        "--terms",
        help="Comma-separated topic terms (optional for casual reading).")
    parser.add_argument(
        "--format",
        choices=["auto", "json", "markdown"],
        default="auto",
        help=
        "Output format. auto = markdown for .md files/terminals, JSON when piped.",
    )
    parser.add_argument("--html-url")
    parser.add_argument("--pdf-url")
    parser.add_argument("--pdf-file",
                        help="Local PDF for testing/offline extraction.")
    parser.add_argument("--html-cache-dir",
                        default=extract_arxiv_html.DEFAULT_CACHE_DIR)
    parser.add_argument("--pdf-cache-dir",
                        default=extract_arxiv_pdf.DEFAULT_CACHE_DIR)
    parser.add_argument(
        "--preferred-source",
        choices=["html", "tex", "auto"],
        default="html",
        help=("Full-text tier order. html (default) = html -> pdf, the legacy "
              "chain. tex = markdown tier first (arxiv2md API by default, see "
              "--tex-transport) -> html -> pdf. auto = html -> markdown tier "
              "-> pdf. The markdown tier needs only curl (arxiv2md) and is "
              "skipped gracefully when the API has no HTML for the paper."),
    )
    parser.add_argument(
        "--tex-transport",
        choices=["arxiv2md", "s3-tex"],
        default="arxiv2md",
        help=("Transport for the markdown tier. arxiv2md (default) = public "
              "REST API via curl, no credentials. s3-tex = S3 TeX source "
              "tarball + pandoc (TODO: needs AWS credentials — the "
              "s3://arxiv/ bucket is requester-pays)."),
    )
    parser.add_argument("--curl-timeout", type=float, default=120.0,
                        help="[arxiv2md] curl max time in seconds.")
    parser.add_argument("--tex-cache-dir",
                        default=extract_arxiv_tex_default_cache_dir(),
                        help="[s3-tex] Cache directory for S3 TeX source tarballs.")
    parser.add_argument("--source-tarball",
                        help="[s3-tex] Local TeX source .tar.gz; skips the S3 download.")
    parser.add_argument("--main-tex",
                        help="[s3-tex] Main .tex member inside the source tarball.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--top-sections", type=int, default=6)
    parser.add_argument("--max-pages", type=int, default=0)
    parser.add_argument(
        "--ocr-mode",
        choices=["auto", "never", "always"],
        default="never",
        help="Default 'never' per the full-text fallback contract.")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument("--ocr-dpi", type=int, default=220)
    parser.add_argument("--min-chars-per-page", type=int, default=180)
    parser.add_argument("--minimum-html-chars", type=int, default=1000)
    parser.add_argument("--force-pdf",
                        action="store_true",
                        help="Skip HTML and exercise PDF/OCR path.")
    parser.add_argument("--include-selected-text", action="store_true")
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help=
        "Include complete HTML text or every text-layer PDF page for $embodied-ai-paper-reader.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help=("Write result here instead of stdout. Defaults to "
              f"{DEFAULT_OUTPUT_DIR}/<paper-id>.md; a directory gets "
              "<paper-id>.md appended (.md implies markdown under --format auto)."
              ),
    )
    args = parser.parse_args(argv)
    if args.paper_id_pos and not args.paper_id:
        args.paper_id = args.paper_id_pos
    if not args.paper_id:
        parser.error("Provide an arXiv ID, e.g. extract_arxiv 2403.12550")
    paper_id = normalize_id(args.paper_id)
    if args.output is None and sys.stdout.isatty():
        args.output = f"{DEFAULT_OUTPUT_DIR}/{paper_id}.md"  # interactive default
    args.output = resolve_output_path(args.output, paper_id)
    return args


def resolve_output_path(output: str | None, paper_id: str) -> str | None:
    """Complete directories with <paper-id>.md; None means stdout (piped)."""
    if not output:
        return None
    path = Path(output).expanduser()
    if str(output).endswith(os.sep) or path.is_dir():
        path.mkdir(parents=True, exist_ok=True)
        return str(path / f"{paper_id}.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def resolve_format(args: argparse.Namespace) -> str:
    """auto: markdown for terminals or .md outputs, JSON when piped or .json."""
    if args.format != "auto":
        return args.format
    if args.output:
        return "markdown" if args.output.lower().endswith(".md") else "json"
    return "markdown" if sys.stdout.isatty() else "json"


def normalize_id(value: str) -> str:
    return re.sub(
        r"v\d+$", "",
        value.rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html"))


def html_quality(output: dict[str, Any],
                 minimum_chars: int) -> dict[str, object]:
    chars = int(output.get("text_chars") or 0)
    structure = str(output.get("structure") or "unavailable")
    if structure == "latexml" and chars >= max(2000, minimum_chars):
        grade = "high"
    elif structure in {"latexml", "flat"} and chars >= minimum_chars:
        grade = "medium"
    else:
        grade = "low"
    return {"grade": grade, "text_chars": chars, "structure": structure}


def try_html(args: argparse.Namespace,
             terms: list[str],
             want_full_text: bool | None = None) -> dict[str, Any]:
    url = args.html_url or f"https://arxiv.org/html/{normalize_id(args.paper_id)}"
    target = Path(args.html_cache_dir).expanduser(
    ) / f"{normalize_id(args.paper_id)}.html"
    available, html = extract_arxiv_html.fetch_html(url, target, args.timeout)
    if want_full_text is None:
        want_full_text = bool(getattr(args, "include_full_text", False))
    html_args = argparse.Namespace(
        paper_id=args.paper_id,
        terms=",".join(terms),
        max_chars=0,
        include_text=want_full_text,
        top_sections=args.top_sections,
        include_section_text=bool(
            getattr(args, "include_selected_text", False) or want_full_text),
    )
    output = extract_arxiv_html.build_output(html_args, url, target, available,
                                             html)
    output["title"] = document_title(html) if available else ""
    output["quality"] = html_quality(output, args.minimum_html_chars)
    output["extraction_method"] = f"html-{output.get('structure')}"
    output["source_format"] = "html"
    output["evidence_eligible"] = bool(
        available) and output["quality"]["grade"] in {"high", "medium"}
    output["needs_visual_validation"] = False
    output["selected_passages"] = output.get("ranked_sections", [])
    return output


def try_pdf(args: argparse.Namespace,
            terms: list[str],
            want_full_text: bool | None = None) -> dict[str, Any]:
    if want_full_text is None:
        want_full_text = bool(getattr(args, "include_full_text", False))
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
        include_pages=bool(
            getattr(args, "include_selected_text", False) or want_full_text),
        terms=",".join(terms),
    )
    output = extract_arxiv_pdf.extract_pdf_document(pdf_args)
    output["title"] = ""
    output["source_format"] = "pdf"
    output["selected_passages"] = output.get("ranked_pages", [])
    # Selected page text is already in ranked_pages. Keep every page only when
    # the downstream paper reader explicitly requests a complete reading input.
    if not want_full_text:
        output.pop("pages", None)
    return output


def try_tex(args: argparse.Namespace, terms: list[str]) -> dict[str, Any]:
    """Markdown tier via extract_arxiv_tex: arxiv2md API (default) or s3-tex."""
    tex = _load_tex_tier()
    tex_args = argparse.Namespace(
        paper_id=args.paper_id,
        transport=getattr(args, "tex_transport", "arxiv2md"),
        curl_timeout=getattr(args, "curl_timeout", 120.0),
        source=getattr(args, "source_tarball", None),
        source_cache_dir=getattr(args, "tex_cache_dir", None)
        or tex.DEFAULT_SOURCE_CACHE_DIR,
        main_tex=getattr(args, "main_tex", None),
        terms=",".join(terms),
        minimum_chars=args.minimum_html_chars,
        to=tex.DEFAULT_TO,
        pandoc_timeout=60.0,
        output=None,
        markdown_output=None,
    )
    output = tex.run(tex_args)
    return output


def extract_content(args: argparse.Namespace) -> dict[str, Any]:
    terms = [
        term.strip() for term in (args.terms or "").split(",") if term.strip()
    ]
    # Markdown rendering needs readable content even when no include flag was passed.
    want_full_text = bool(
        getattr(args, "include_full_text", False)
        or getattr(args, "_render_markdown", False))
    attempts: list[dict[str, Any]] = []
    preferred = getattr(args, "preferred_source", "html") or "html"

    def run_html() -> dict[str, Any]:
        html = try_html(args, terms, want_full_text=want_full_text)
        attempts.append({
            "method": html["extraction_method"],
            "available": html.get("available", False),
            "quality": html["quality"]["grade"],
        })
        return html

    def run_tex() -> dict[str, Any]:
        tex = try_tex(args, terms)
        attempts.append({
            "method": tex.get("extraction_method", "tex-pandoc"),
            "available": tex.get("available", False),
            "quality": (tex.get("quality") or {}).get("grade", "low"),
        })
        return tex

    def run_pdf() -> dict[str, Any]:
        pdf = try_pdf(args, terms, want_full_text=want_full_text)
        attempts.append({
            "method":
            pdf.get("extraction_method", "pdf"),
            "available":
            pdf.get("available", False),
            "quality": (pdf.get("quality") or {}).get("grade", "low"),
            "ocr_pages": (pdf.get("ocr") or {}).get("pages_used", []),
        })
        return pdf

    # Tier order per --preferred-source. Default "html" reproduces the legacy
    # chain (html -> pdf) exactly; "auto" prefers authoritative TeX over lossy
    # PDF; "tex" forces the TeX tier first.
    tiers: list[tuple[str, Any]] = []
    if preferred == "tex":
        tiers = [("tex", run_tex), ("html", run_html), ("pdf", run_pdf)]
    elif preferred == "auto":
        tiers = [("html", run_html), ("tex", run_tex), ("pdf", run_pdf)]
    else:
        tiers = [("html", run_html), ("pdf", run_pdf)]

    fallback_reason = ""
    for tier_name, runner in tiers:
        if tier_name == "pdf" and args.force_pdf:
            fallback_reason = "PDF path forced by caller."
        try:
            output = runner()
            if output.get("evidence_eligible"):
                output["attempts"] = attempts
                output["fallback_reason"] = ""
                return output
            fallback_reason = f"{tier_name.upper()} unavailable or below the minimum full-text quality gate."
        except SystemExit:
            # Missing optional dependency (boto3/pypandoc) for this tier —
            # fall through to the next tier instead of killing the chain.
            attempts.append({
                "method": tier_name,
                "available": False,
                "quality": "low",
                "error": "optional dependency missing for this tier",
            })
            fallback_reason = f"{tier_name.upper()} tier unavailable: optional dependency missing."
        except Exception as exc:  # pragma: no cover - network/parser dependent
            attempts.append({
                "method": tier_name,
                "available": False,
                "quality": "low",
                "error": str(exc),
            })
            fallback_reason = f"{tier_name.upper()} extraction failed: {exc}"

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(args.paper_id),
        "available": False,
        "source_format": "metadata-only",
        "extraction_method": "unavailable",
        "quality": {
            "grade": "low",
            "text_chars": 0
        },
        "evidence_eligible": False,
        "needs_visual_validation": False,
        "selected_passages": [],
        "term_matches": [],
        "reference_hints": [],
        "attempts": attempts,
        "fallback_reason": fallback_reason,
    }


def _md_escape_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def _render_table(table: dict[str, Any]) -> list[str]:
    rows = [row for row in table.get("rows") or [] if row]
    if not rows:
        return []
    width = max(len(row) for row in rows)
    lines = [
        "| " + " | ".join(
            _md_escape_cell(cell)
            for cell in row + [""] * (width - len(row))) + " |" for row in rows
    ]
    lines.insert(1, "| " + " | ".join(["---"] * width) + " |")
    return lines


def build_markdown(output: dict[str, Any]) -> str:
    """Render an extract_content result dict as a readable markdown document."""
    paper_id = str(output.get("paper_id") or "unknown")
    title = str(output.get("title") or "").strip()
    lines: list[str] = [f"# {title or f'arXiv {paper_id}'}", ""]

    bullets: list[str] = []
    source = str(output.get("source_format") or "html")
    if source == "html":
        bullets.append(
            f"- Source: {output.get('html_url') or f'https://arxiv.org/html/{paper_id}'} (HTML)"
        )
    elif output.get("pdf_url"):
        bullets.append(f"- Source: {output['pdf_url']} (PDF)")
    if output.get("cache_file"):
        bullets.append(f"- Cached at: `{output['cache_file']}`")
    quality = output.get("quality") or {}
    if isinstance(quality, dict) and quality.get("grade"):
        bullets.append(
            f"- Quality: {quality['grade']} ({output.get('extraction_method', 'unknown')})"
        )
    bullets.append(
        f"- Evidence eligible: {'yes' if output.get('evidence_eligible') else 'no'}"
    )
    if output.get("generated_at"):
        bullets.append(f"- Extracted: {str(output['generated_at'])[:10]}")
    lines.extend(bullets)

    if not output.get("available", False):
        lines.extend([
            "",
            "> **Full text unavailable.** HTML render missing/low-quality and PDF fallback failed.",
        ])
        if output.get("fallback_reason"):
            lines.append(f"> Reason: {output['fallback_reason']}")
        for attempt in output.get("attempts") or []:
            error = attempt.get("error")
            if error:
                lines.append(
                    f"> `{attempt.get('method', 'unknown')}` error: {error}")
        return "\n".join(lines) + "\n"

    if output.get("needs_visual_validation"):
        pages = output.get("visual_validation_pages") or []
        lines.append("")
        lines.append(
            f"> **Visually validate pages {', '.join(map(str, pages))} against the PDF before citing.**"
        )

    text = str(output.get("text") or "")
    if text:
        lines.extend(["", text])

    pages = output.get("pages") or []
    if pages:
        for page in pages:
            heading = f"## Page {page.get('page', '?')}"
            method = page.get("extraction_method")
            if method == "pdf-ocr":
                heading += " _(OCR)_"
            lines.extend(
                ["", heading, "",
                 str(page.get("text") or "").strip()])

    figures = output.get("figures") or []
    tables = output.get("tables") or []
    formulas = output.get("formulas") or []
    references = output.get("references") or []
    if figures or tables:
        lines.extend(["", "---", "", "## Figures and Tables"])
        for figure in figures:
            caption = str(figure.get("caption") or "").strip()
            url = str(figure.get("image_url") or "").strip()
            if url:
                lines.extend(["", f"![{caption}]({url})"])
            if caption:
                lines.extend(["", f"*{caption}*"])
        for table in tables:
            caption = str(table.get("caption") or "").strip()
            rows = _render_table(table)
            if caption:
                lines.extend(["", f"**{caption}**"])
            if rows:
                lines.extend(["", *rows])

    if formulas:
        numbered = [
            f for f in formulas
            if str(f.get("number") or "").strip()
        ]
        if numbered:
            lines.extend(["", "---", "", "## Formulas", ""])
            for formula in numbered:
                latex = str(formula.get("latex") or "").strip()
                number = str(formula.get("number") or "").strip()
                lines.append(f"- {number} $${latex}$$")

    if references:
        lines.extend(["", "---", "", "## References", ""])
        for reference in references:
            lines.append(f"- {reference.get('text', '')}")
            arxiv_id = str(reference.get("arxiv_id") or "").strip()
            if arxiv_id:
                lines.append(f"  [arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})")

    if not text and not pages and not figures and not tables and not formulas and not references:
        lines.extend([
            "", "_(No full text included; rerun with `--include-full-text`.)_"
        ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_format = resolve_format(args)
    setattr(args, "_render_markdown", output_format == "markdown")
    output = extract_content(args)
    if output_format == "markdown":
        rendered = build_markdown(output)
    else:
        rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
        if output_format == "markdown" and sys.stdout.isatty():
            print(
                f"wrote {path} ({output.get('extraction_method', 'unknown')}, "
                f"evidence_eligible={bool(output.get('evidence_eligible'))})",
                file=sys.stderr)
    else:
        print(rendered)
    return 0 if output.get("evidence_eligible") else 2


if __name__ == "__main__":
    raise SystemExit(main())

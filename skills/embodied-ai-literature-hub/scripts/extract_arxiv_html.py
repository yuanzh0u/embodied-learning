#!/usr/bin/env python3
"""Fetch/cache arXiv HTML and extract section-aware text, ranked sections, term matches, and citation contexts.

LaTeXML pages (arxiv.org/html) are parsed into a section tree with paragraph
locators; term matches anchor to `section path ¶ paragraph id`, sections are
ranked by term density for selective full-text reading, and in-text citations
are resolved through the bibliography back to arXiv IDs. Non-LaTeXML pages
degrade to the legacy flat extraction (`structure: "flat"`).
"""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_CACHE_DIR = os.path.join(
    os.environ.get("TMPDIR") or "/private/tmp",
    "embodied-ai-literature-hub",
    "html",
)
SKIP_TAGS = {"script", "style", "noscript", "svg", "math"}
SECTION_CLASSES = (
    "ltx_section",
    "ltx_subsection",
    "ltx_subsubsection",
    "ltx_abstract",
    "ltx_bibliography",
    "ltx_appendix",
)
ARXIV_ID_RE = re.compile(r"(?:arXiv[:\s]*)?(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)
MAX_TERM_MATCHES = 120
MAX_CITATION_CONTEXTS = 200
MAX_REFERENCE_HINTS = 80


class FlatHTMLParser(HTMLParser):
    """Legacy fallback: linear text with `## heading` markers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n\n## ")
        elif tag in {"p", "div", "section", "article", "li", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.parts.append(text + " ")

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [" ".join(line.split()) for line in raw.splitlines()]
        return "\n".join(line for line in lines if line).strip()


class LatexmlParser(HTMLParser):
    """Section-aware parser for LaTeXML arXiv HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.div_depth = 0
        self.sections: list[dict[str, object]] = []
        # (section index, opening tag, div depth at open) for correct nested closing.
        self.stack: list[tuple[int, str, int]] = []
        self.in_title_for: int | None = None
        self.current_para: str = ""
        self.citations: list[dict[str, object]] = []
        self.open_cite: dict[str, object] | None = None
        self.bibitems: dict[str, str] = {}
        self.open_bibitem: str | None = None

    @staticmethod
    def _attr(attrs, name: str) -> str:  # type: ignore[no-untyped-def]
        for key, value in attrs:
            if key == name:
                return value or ""
        return ""

    @staticmethod
    def _section_kind(classes: str) -> str:
        parts = classes.split()
        for cls in SECTION_CLASSES:
            if cls in parts:
                return cls
        return ""

    def _current(self) -> dict[str, object] | None:
        return self.sections[self.stack[-1][0]] if self.stack else None

    def _offset(self, section: dict[str, object]) -> int:
        return sum(len(chunk) for chunk in section["chunks"])  # type: ignore[union-attr]

    def _open_section(self, kind: str, elem_id: str, tag: str) -> None:
        index = len(self.sections)
        self.sections.append(
            {
                "index": index,
                "id": elem_id,
                "kind": kind,
                "title": "Abstract" if kind == "ltx_abstract" else "",
                "level": len(self.stack) + 1,
                "para_offsets": [],
                "chunks": [],
            }
        )
        self.stack.append((index, tag, self.div_depth))

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        classes = self._attr(attrs, "class")
        elem_id = self._attr(attrs, "id")
        if tag == "div":
            self.div_depth += 1
        kind = self._section_kind(classes) if tag in {"section", "div"} else ""
        if kind:
            self._open_section(kind, elem_id, tag)
            return
        current = self._current()
        if current is not None:
            if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and "ltx_title" in classes and not current["title"]:
                self.in_title_for = self.stack[-1][0]
            if "ltx_para" in classes.split() and elem_id:
                self.current_para = elem_id
                current["para_offsets"].append((elem_id, self._offset(current)))  # type: ignore[union-attr]
        if tag == "cite" and "ltx_cite" in classes:
            self.open_cite = {
                "section_index": self.stack[-1][0] if self.stack else None,
                "para": self.current_para,
                "offset": self._offset(current) if current is not None else 0,
                "bib_keys": [],
            }
        if self.open_cite is not None and tag == "a":
            match = re.search(r"#(bib\.bib\d+)", self._attr(attrs, "href"))
            if match:
                self.open_cite["bib_keys"].append(match.group(1))
        if tag == "li" and "ltx_bibitem" in classes and elem_id:
            self.open_bibitem = elem_id
            self.bibitems[elem_id] = ""

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self.in_title_for is not None:
            section = self.sections[self.in_title_for]
            section["title"] = " ".join(str(section["title"]).split())
            self.in_title_for = None
        if tag == "cite" and self.open_cite is not None:
            if self.open_cite["bib_keys"]:
                self.citations.append(self.open_cite)
            self.open_cite = None
        if tag == "li" and self.open_bibitem is not None:
            self.open_bibitem = None
        if tag == "div":
            if self.stack and self.stack[-1][1] == "div" and self.div_depth == self.stack[-1][2]:
                self.stack.pop()
            if self.div_depth:
                self.div_depth -= 1
        elif tag == "section":
            if self.stack and self.stack[-1][1] == "section":
                self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if not text:
            return
        if self.in_title_for is not None:
            section = self.sections[self.in_title_for]
            section["title"] = f"{section['title']} {text}".strip()
            return
        if self.open_bibitem is not None:
            self.bibitems[self.open_bibitem] += text + " "
            return
        current = self._current()
        if current is not None:
            current["chunks"].append(text + " ")  # type: ignore[union-attr]

    def finish(self) -> None:
        for section in self.sections:
            text = "".join(section.pop("chunks")).strip()  # type: ignore[arg-type]
            section["text"] = text
            section["char_count"] = len(text)
            section["para_count"] = len(section["para_offsets"])  # type: ignore[arg-type]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", help="arXiv ID, with or without version.")
    parser.add_argument("--html-url", help="HTML URL. Defaults to https://arxiv.org/html/<paper-id>")
    parser.add_argument("--terms", help="Comma-separated terms to locate and rank sections by.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-chars", type=int, default=0, help="0 means all extracted text.")
    parser.add_argument("--include-text", action="store_true", help="Include full extracted text in JSON output.")
    parser.add_argument("--top-sections", type=int, default=8, help="How many ranked sections to report.")
    parser.add_argument(
        "--include-section-text",
        action="store_true",
        help="Include full text for each ranked section (for selective deep reading).",
    )
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args()


def normalize_id(value: str) -> str:
    value = value.rsplit("/", 1)[-1]
    value = value.removesuffix(".html")
    return re.sub(r"v\d+$", "", value)


def html_url(args: argparse.Namespace) -> str:
    if args.html_url:
        return args.html_url
    if not args.paper_id:
        raise SystemExit("Provide --paper-id or --html-url.")
    return f"https://arxiv.org/html/{normalize_id(args.paper_id)}"


def cache_path(args: argparse.Namespace, url: str) -> Path:
    base = normalize_id(args.paper_id or url)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", base)
    return Path(args.cache_dir).expanduser() / f"{safe}.html"


def fetch_html(url: str, target: Path, timeout: float) -> tuple[bool, str]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return True, target.read_text(encoding="utf-8", errors="replace")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "embodied-ai-literature-hub/1.0 (local research workflow)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if status >= 400:
                return False, ""
            payload = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code in {404, 410}:
            return False, ""
        raise
    target.write_text(payload, encoding="utf-8")
    return True, payload


def parse_terms(raw: str | None) -> list[str]:
    return [term.strip() for term in (raw or "").split(",") if term.strip()]


def section_path(sections: list[dict[str, object]], index: int) -> str:
    """Build `parent > child` path by walking back through shallower levels."""
    parts: list[str] = []
    level: int | None = None
    for section in reversed(sections[: index + 1]):
        section_level = int(section["level"])  # type: ignore[arg-type]
        if level is None or section_level < level:
            parts.append(str(section["title"]) or str(section["id"]) or "untitled")
            level = section_level
        if level == 1:
            break
    return " > ".join(reversed(parts))


def para_at_offset(section: dict[str, object], offset: int) -> str:
    para_offsets = section.get("para_offsets") or []
    best = ""
    for para_id, start in para_offsets:  # recorded in document order
        if start <= offset:
            best = str(para_id)
        else:
            break
    return best


def find_term_matches(sections: list[dict[str, object]], terms: list[str], window: int = 260) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for section in sections:
        text = str(section["text"])
        lowered = text.lower()
        path = section_path(sections, int(section["index"]))
        for raw_term in terms:
            term = raw_term.lower()
            start = 0
            while True:
                index = lowered.find(term, start)
                if index < 0:
                    break
                left = max(0, index - window)
                right = min(len(text), index + len(term) + window)
                para = para_at_offset(section, index)
                matches.append(
                    {
                        "term": raw_term,
                        "locator": f"{path} ¶ {para}" if para else path,
                        "section_index": section["index"],
                        "char_start": index,
                        "snippet": " ".join(text[left:right].split()),
                    }
                )
                start = index + len(term)
                if len(matches) >= MAX_TERM_MATCHES:
                    return matches
    return matches


def rank_sections(sections: list[dict[str, object]], terms: list[str], top: int) -> list[dict[str, object]]:
    ranked: list[dict[str, object]] = []
    for section in sections:
        if section["kind"] == "ltx_bibliography":
            continue
        text = str(section["text"]).lower()
        if not text:
            continue
        hits = {term: text.count(term.lower()) for term in terms}
        total = sum(hits.values())
        if total == 0:
            continue
        distinct = sum(1 for count in hits.values() if count)
        # Density-leaning score: reward hits and term diversity, damp very long sections.
        score = (total + 2.0 * distinct) / math.sqrt(1.0 + int(section["char_count"]) / 1000.0)
        ranked.append(
            {
                "section_index": section["index"],
                "path": section_path(sections, int(section["index"])),
                "score": round(score, 3),
                "hits": total,
                "matched_terms": sorted(term for term, count in hits.items() if count),
            }
        )
    ranked.sort(key=lambda item: (-float(item["score"]), item["section_index"]))
    return ranked[:top]


def sentence_around(text: str, offset: int, max_len: int = 420) -> str:
    offset = max(0, min(offset, len(text)))
    left = max(text.rfind(". ", 0, offset), text.rfind("。", 0, offset))
    start = left + 2 if left >= 0 else 0
    candidates = [pos for pos in (text.find(". ", offset), text.find("。", offset)) if pos >= 0]
    end = min(candidates) + 1 if candidates else len(text)
    return " ".join(text[start:end].split())[:max_len]


def resolve_bib_arxiv_ids(bibitems: dict[str, str]) -> dict[str, str]:
    resolved = {}
    for key, text in bibitems.items():
        match = ARXIV_ID_RE.search(text)
        if match:
            resolved[key] = match.group(1)
    return resolved


def citation_contexts(parser: LatexmlParser) -> list[dict[str, object]]:
    bib_arxiv = resolve_bib_arxiv_ids(parser.bibitems)
    contexts: list[dict[str, object]] = []
    for cite in parser.citations[:MAX_CITATION_CONTEXTS]:
        if cite["section_index"] is None:
            continue
        section = parser.sections[int(cite["section_index"])]  # type: ignore[arg-type]
        bib_keys = list(cite["bib_keys"])  # type: ignore[arg-type]
        contexts.append(
            {
                "section": section_path(parser.sections, int(section["index"])),
                "para": str(cite["para"]),
                "bib_keys": bib_keys,
                "arxiv_ids": sorted({bib_arxiv[key] for key in bib_keys if key in bib_arxiv}),
                "sentence": sentence_around(str(section["text"]), int(cite["offset"])),  # type: ignore[arg-type]
            }
        )
    return contexts


def reference_hints_from_bib(bibitems: dict[str, str]) -> list[dict[str, str]]:
    hints = []
    seen: set[str] = set()
    for key in sorted(bibitems):
        match = ARXIV_ID_RE.search(bibitems[key])
        if not match or match.group(1) in seen:
            continue
        seen.add(match.group(1))
        hints.append({"arxiv_id": match.group(1), "snippet": " ".join(bibitems[key].split())[:440]})
        if len(hints) >= MAX_REFERENCE_HINTS:
            break
    return hints


def flat_current_heading(text: str, position: int) -> str:
    headings = re.findall(r"^##\s+(.+)$", text[:position], flags=re.MULTILINE)
    return headings[-1] if headings else "HTML body"


def flat_term_matches(text: str, terms: list[str], window: int = 260) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    lowered = text.lower()
    for raw_term in terms:
        term = raw_term.lower()
        start = 0
        while True:
            index = lowered.find(term, start)
            if index < 0:
                break
            left = max(0, index - window)
            right = min(len(text), index + len(term) + window)
            matches.append(
                {
                    "term": raw_term,
                    "locator": flat_current_heading(text, index),
                    "char_start": index,
                    "snippet": " ".join(text[left:right].split()),
                }
            )
            start = index + len(term)
            if len(matches) >= MAX_TERM_MATCHES:
                return matches
    return matches


def flat_reference_hints(text: str) -> list[dict[str, str]]:
    lower = text.lower()
    start = lower.rfind("references")
    ref_text = text[start:] if start >= 0 else text[-25000:]
    hints = []
    seen: set[str] = set()
    for match in ARXIV_ID_RE.finditer(ref_text):
        arxiv_id = match.group(1)
        if arxiv_id in seen:
            continue
        seen.add(arxiv_id)
        left = max(0, match.start() - 180)
        right = min(len(ref_text), match.end() + 260)
        hints.append({"arxiv_id": arxiv_id, "snippet": " ".join(ref_text[left:right].split())})
        if len(hints) >= MAX_REFERENCE_HINTS:
            break
    return hints


def extract_structured(html: str) -> LatexmlParser | None:
    if "ltx_section" not in html and "ltx_abstract" not in html:
        return None
    parser = LatexmlParser()
    parser.feed(html)
    parser.finish()
    return parser if parser.sections else None


def build_output(args: argparse.Namespace, url: str, target: Path, available: bool, html: str) -> dict[str, object]:
    terms = parse_terms(args.terms)
    output: dict[str, object] = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(args.paper_id or url),
        "html_url": url,
        "available": available,
        "cache_file": str(target) if available else "",
    }
    if not available:
        output.update({"structure": "unavailable", "text_chars": 0, "term_matches": [], "reference_hints": []})
        return output

    structured = extract_structured(html)
    if structured is None:
        flat = FlatHTMLParser()
        flat.feed(html)
        text = flat.text()
        if args.max_chars:
            text = text[: args.max_chars]
        output.update(
            {
                "structure": "flat",
                "text_chars": len(text),
                "term_matches": flat_term_matches(text, terms) if text else [],
                "reference_hints": flat_reference_hints(text) if text else [],
            }
        )
        if args.include_text:
            output["text"] = text
        return output

    sections = structured.sections
    ranked = rank_sections(sections, terms, args.top_sections) if terms else []
    if args.include_section_text:
        by_index = {int(section["index"]): section for section in sections}
        for entry in ranked:
            entry["text"] = str(by_index[int(entry["section_index"])]["text"])
    section_meta = [
        {
            "index": section["index"],
            "id": section["id"],
            "kind": section["kind"],
            "title": section["title"],
            "path": section_path(sections, int(section["index"])),
            "level": section["level"],
            "para_count": section["para_count"],
            "char_count": section["char_count"],
        }
        for section in sections
    ]
    output.update(
        {
            "structure": "latexml",
            "text_chars": sum(int(section["char_count"]) for section in sections),
            "sections": section_meta,
            "ranked_sections": ranked,
            "term_matches": find_term_matches(sections, terms) if terms else [],
            "citation_contexts": citation_contexts(structured),
            "reference_hints": reference_hints_from_bib(structured.bibitems),
        }
    )
    if args.include_text:
        full_text = "\n\n".join(f"## {section['title']}\n{section['text']}" for section in sections if section["text"])
        if args.max_chars:
            full_text = full_text[: args.max_chars]
        output["text"] = full_text
    return output


def main() -> int:
    args = parse_args()
    url = html_url(args)
    target = cache_path(args, url)
    available, html = fetch_html(url, target, args.timeout)
    output = build_output(args, url, target, available, html)
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Promote candidate papers toward evidence: fetch metadata + full text, emit a reading digest and an evidence skeleton.

This mechanizes the expensive half of candidate->evidence promotion. For each
paper it pulls arXiv API metadata and section-aware HTML extraction, then
writes:

- a digest (per-paper ranked sections with text, plus citation contexts) —
  the raw material for writing claims;
- a skeleton JSONL with event_id / topic / paper / authors / locator
  prefilled, and `claim` / `stance` / `evidence.summary` left as TODO
  placeholders. `write_lit_outputs.py --validate-only` rejects TODO stances,
  so an unfilled skeleton can never settle as accepted evidence.

The agent's remaining job is the intellectual one: read the digest, write the
claim, pick the stance, and set the exact locator.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"


def load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


extract_arxiv_html = load_sibling("extract_arxiv_html")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", action="append", default=[], required=True, help="arXiv ID to promote. Repeatable.")
    parser.add_argument("--topic", required=True, help="Run topic (copied into each skeleton event).")
    parser.add_argument("--topic-id", required=True, help="Knowledge ID for these events, e.g. EA-MODEL.")
    parser.add_argument("--id-prefix", required=True, help="Event ID prefix, e.g. EA-PVC-2026.")
    parser.add_argument("--start-seq", type=int, default=1, help="First sequence number (use scripts/next_event_id.py).")
    parser.add_argument("--terms", required=True, help="Comma-separated terms for section ranking.")
    parser.add_argument("--top-sections", type=int, default=4, help="Ranked sections per paper in the digest.")
    parser.add_argument("--cache-dir", default=extract_arxiv_html.DEFAULT_CACHE_DIR)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--output-skeleton", required=True, help="Path for the evidence skeleton JSONL.")
    parser.add_argument("--output-digest", required=True, help="Path for the reading digest Markdown.")
    return parser.parse_args()


def author_key(name: str) -> str:
    ascii_name = name.encode("ascii", errors="ignore").decode("ascii")
    base = ascii_name if ascii_name.strip() else name
    return re.sub(r"[^0-9A-Za-z]+", "-", base.strip().lower()).strip("-") or "unknown-author"


def fetch_metadata(paper_ids: list[str], timeout: float) -> dict[str, dict[str, object]]:
    """One id_list request for all papers (API etiquette: single call, no fan-out)."""
    query = urllib.parse.urlencode({"id_list": ",".join(paper_ids), "max_results": len(paper_ids)})
    request = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={"User-Agent": "embodied-ai-literature-hub/1.0 (local research workflow)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    metadata: dict[str, dict[str, object]] = {}
    for entry in root.findall(ATOM + "entry"):
        entry_id = (entry.findtext(ATOM + "id") or "").strip()
        versioned = entry_id.rsplit("/", 1)[-1]
        arxiv_id = re.sub(r"v\d+$", "", versioned)
        if not arxiv_id:
            continue
        metadata[arxiv_id] = {
            "arxiv_id": arxiv_id,
            "title": " ".join((entry.findtext(ATOM + "title") or "").split()),
            "published": (entry.findtext(ATOM + "published") or "")[:10],
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "authors": [
                " ".join((author.findtext(ATOM + "name") or "").split())
                for author in entry.findall(ATOM + "author")
            ],
        }
    return metadata


def extract_paper(paper_id: str, terms: list[str], top: int, cache_dir: str, timeout: float) -> dict[str, object]:
    """Section-aware extraction via extract_arxiv_html's functions (cached HTML)."""
    url = f"https://arxiv.org/html/{paper_id}"
    target = Path(cache_dir).expanduser() / f"{re.sub(r'[^A-Za-z0-9._-]+', '_', paper_id)}.html"
    available, html = extract_arxiv_html.fetch_html(url, target, timeout)
    if not available:
        return {"available": False, "structure": "unavailable", "ranked": [], "citations": []}
    structured = extract_arxiv_html.extract_structured(html)
    if structured is None:
        return {"available": True, "structure": "flat", "ranked": [], "citations": []}
    sections = structured.sections
    ranked = extract_arxiv_html.rank_sections(sections, terms, top)
    by_index = {int(section["index"]): section for section in sections}
    for entry in ranked:
        entry["text"] = str(by_index[int(entry["section_index"])]["text"])
    return {
        "available": True,
        "structure": "latexml",
        "ranked": ranked,
        "citations": extract_arxiv_html.citation_contexts(structured)[:12],
    }


def skeleton_event(
    topic: str,
    topic_id: str,
    event_id: str,
    meta: dict[str, object],
    extraction: dict[str, object],
) -> dict[str, object]:
    ranked = extraction.get("ranked") or []
    locator = str(ranked[0]["path"]) if ranked else "TODO(locator: section path from digest)"
    return {
        "event_id": event_id,
        "topic_id": topic_id,
        "topic": topic,
        "paper": {
            "arxiv_id": meta["arxiv_id"],
            "title": meta["title"],
            "published": meta["published"],
            "url": meta["url"],
        },
        "authors": [
            {"name": name, "author_key": author_key(str(name)), "role": "paper-author", "institutions": []}
            for name in meta.get("authors", [])
        ],
        "claim": "TODO(claim: one precise topic-relevant claim in your words)",
        "stance": "TODO(stance: support|limit|conditional|gap)",
        "evidence": {
            "summary": "TODO(evidence summary: paraphrase what in the paper backs the claim)",
            "locator": locator,
            "evidence_type": "TODO(e.g. method-and-experiment, dataset, analysis)",
        },
        "confidence": "direct",
        "core_citations": [],
        "notes": f"Skeleton generated by promote_candidates.py; extraction structure: {extraction.get('structure')}.",
    }


def render_digest(
    topic: str,
    papers: list[tuple[str, dict[str, object], dict[str, object], str]],
    terms: list[str],
) -> str:
    lines = [
        f"# Promotion Digest: {topic}",
        "",
        f"- Terms: {', '.join(terms)}",
        "- 每篇论文列出按词密度排序的章节全文与引用上下文;据此为 skeleton 填写 claim/stance/summary,并把 locator 精确到章节。",
        "",
    ]
    for paper_id, meta, extraction, event_id in papers:
        lines.append(f"## {meta.get('title') or paper_id} ({event_id})")
        lines.append("")
        lines.append(f"- arXiv: https://arxiv.org/abs/{paper_id} | published: {meta.get('published')}")
        lines.append(f"- extraction: {extraction.get('structure')}")
        lines.append("")
        ranked = extraction.get("ranked") or []
        if not ranked:
            lines.append("- No ranked sections (HTML unavailable or flat): read the abs page and fill the skeleton manually.")
            lines.append("")
        for entry in ranked:
            lines.append(f"### §{entry['path']} (score {entry['score']}, terms: {', '.join(entry['matched_terms'])})")
            lines.append("")
            lines.append(str(entry.get("text") or "")[:2600])
            lines.append("")
        citations = extraction.get("citations") or []
        if citations:
            lines.append("### Citation contexts")
            lines.append("")
            for ctx in citations[:8]:
                ids = ", ".join(ctx.get("arxiv_ids") or []) or "unresolved"
                lines.append(f"- [{ids}] §{ctx['section']}: {str(ctx['sentence'])[:260]}")
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    terms = [term.strip() for term in args.terms.split(",") if term.strip()]
    paper_ids = [re.sub(r"v\d+$", "", pid.strip()) for pid in args.paper_id]
    metadata = fetch_metadata(paper_ids, args.timeout)
    missing = [pid for pid in paper_ids if pid not in metadata]
    if missing:
        print(f"arXiv API returned no metadata for: {', '.join(missing)}", file=sys.stderr)
        return 1
    rows: list[tuple[str, dict[str, object], dict[str, object], str]] = []
    skeleton_lines: list[str] = []
    for offset, paper_id in enumerate(paper_ids):
        event_id = f"{args.id_prefix}-{args.start_seq + offset:04d}"
        extraction = extract_paper(paper_id, terms, args.top_sections, args.cache_dir, args.timeout)
        event = skeleton_event(args.topic, args.topic_id, event_id, metadata[paper_id], extraction)
        skeleton_lines.append(json.dumps(event, ensure_ascii=False))
        rows.append((paper_id, metadata[paper_id], extraction, event_id))
        if offset + 1 < len(paper_ids):
            time.sleep(0.5)  # be gentle on arxiv.org/html
    Path(args.output_skeleton).write_text("\n".join(skeleton_lines) + "\n", encoding="utf-8")
    Path(args.output_digest).write_text(render_digest(args.topic, rows, terms), encoding="utf-8")
    print(f"Wrote skeleton: {args.output_skeleton} ({len(skeleton_lines)} events, claims/stances are TODO)")
    print(f"Wrote digest:   {args.output_digest}")
    print("Next: fill claim/stance/evidence.summary per event from the digest, then run write_lit_outputs.py --validate-only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

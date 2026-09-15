#!/usr/bin/env python3
"""Promote candidate papers toward evidence: fetch metadata + full text, emit a reading digest and an evidence skeleton.

This mechanizes the expensive half of candidate->evidence promotion. For each
paper it pulls arXiv API metadata and runs HTML -> PDF text -> OCR extraction, then
writes:

- a digest (per-paper ranked sections with text, plus citation contexts) —
  the raw material for writing claims;
- a skeleton JSONL with event_id / topic / paper / authors / locator
  prefilled, and `claim` / `stance` / `evidence.summary` left as TODO
  placeholders. `write_lit_outputs.py --validate-only` rejects TODO stances,
  so an unfilled skeleton can never settle as accepted evidence.

The agent's remaining job is the intellectual one: read the digest, write the
claim, pick the stance, and set the exact locator.

Library API: explicit-parameter functions (:func:`load_paper_ids`,
:func:`fetch_metadata`, :func:`extract_paper`, :func:`skeleton_event`,
:func:`render_digest`) plus :func:`run_promotion`, which drives the whole
pipeline. The CLI surface owns argument parsing and lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/promote_candidates.py``.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"


from embodied_learning.fetch import chain as extract_arxiv_content


def load_paper_ids(cli_ids: list[str], id_files: list[str]) -> list[str]:
    """Load, normalize, and stably deduplicate CLI/file paper IDs."""
    raw_ids = list(cli_ids)
    for filename in id_files:
        for line in Path(filename).read_text(encoding="utf-8").splitlines():
            value = line.split("#", 1)[0].strip()
            if value:
                raw_ids.append(value)
    result: list[str] = []
    seen: set[str] = set()
    for value in raw_ids:
        paper_id = re.sub(r"v\d+$", "", value.strip().rsplit("/", 1)[-1].removesuffix(".pdf"))
        if paper_id and paper_id not in seen:
            seen.add(paper_id)
            result.append(paper_id)
    return result


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


def extract_paper(
    paper_id: str,
    terms: list[str],
    top: int,
    cache_dir: str,
    pdf_cache_dir: str,
    timeout: float,
    ocr_mode: str,
    ocr_language: str,
) -> dict[str, object]:
    """Run the unified HTML/PDF/OCR extraction path and normalize digest fields."""
    from embodied_learning.fetch.chain import ContentOptions

    args = ContentOptions(
        paper_id=paper_id,
        terms=",".join(terms),
        html_url=None,
        pdf_url=None,
        pdf_file=None,
        html_cache_dir=cache_dir,
        pdf_cache_dir=pdf_cache_dir,
        timeout=timeout,
        top_sections=top,
        max_pages=0,
        ocr_mode=ocr_mode,
        ocr_language=ocr_language,
        ocr_dpi=220,
        min_chars_per_page=180,
        minimum_html_chars=1000,
        force_pdf=False,
        include_selected_text=True,
    )
    output = extract_arxiv_content.extract_content(args)
    ranked = []
    for entry in output.get("selected_passages", []):
        if not isinstance(entry, dict):
            continue
        normalized = dict(entry)
        normalized["path"] = entry.get("path") or entry.get("locator") or f"page {entry.get('page')}"
        ranked.append(normalized)
    return {
        "available": output.get("available", False),
        "evidence_eligible": output.get("evidence_eligible", False),
        "structure": output.get("extraction_method", "unavailable"),
        "source_format": output.get("source_format", "metadata-only"),
        "quality": output.get("quality", {"grade": "low"}),
        "needs_visual_validation": output.get("needs_visual_validation", False),
        "visual_validation_pages": output.get("visual_validation_pages", []),
        "attempts": output.get("attempts", []),
        "ranked": ranked,
        "citations": output.get("citation_contexts", [])[:12],
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
            "extraction": {
                "source_format": extraction.get("source_format", "metadata-only"),
                "method": extraction.get("structure", "unavailable"),
                "quality": (extraction.get("quality") or {}).get("grade", "low"),
                "visual_validation": "required" if extraction.get("needs_visual_validation") else "not-required",
                "visual_validation_pages": extraction.get("visual_validation_pages", []),
            },
        },
        "confidence": "direct",
        "core_citations": [],
        "notes": f"Skeleton generated by promote_candidates.py; extraction method: {extraction.get('structure')}.",
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
        quality = (extraction.get("quality") or {}).get("grade", "low")
        lines.append(f"- extraction: {extraction.get('structure')} | quality: {quality}")
        if extraction.get("needs_visual_validation"):
            pages = ", ".join(str(item) for item in extraction.get("visual_validation_pages", [])) or "selected pages"
            lines.append(f"- visual validation required before evidence settlement: {pages}")
        lines.append("")
        ranked = extraction.get("ranked") or []
        if not ranked:
            lines.append("- No ranked full-text passages: keep this paper as a candidate; do not promote metadata-only claims.")
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


def run_promotion(
    *,
    paper_ids: list[str],
    terms: list[str],
    topic: str,
    topic_id: str,
    id_prefix: str,
    start_seq: int,
    top_sections: int,
    cache_dir: str,
    pdf_cache_dir: str,
    timeout: float,
    ocr_mode: str,
    ocr_language: str,
    output_skeleton: str,
    output_digest: str,
) -> int:
    """Fetch metadata, extract each paper, and write the skeleton JSONL + digest.

    ``paper_ids`` and ``terms`` are pre-normalized (the CLI entry derives them
    from raw flags via :func:`load_paper_ids` and comma splitting).
    """
    metadata = fetch_metadata(paper_ids, timeout)
    missing = [pid for pid in paper_ids if pid not in metadata]
    if missing:
        print(f"arXiv API returned no metadata for: {', '.join(missing)}", file=sys.stderr)
        return 1
    rows: list[tuple[str, dict[str, object], dict[str, object], str]] = []
    skeleton_lines: list[str] = []
    for offset, paper_id in enumerate(paper_ids):
        event_id = f"{id_prefix}-{start_seq + offset:04d}"
        extraction = extract_paper(
            paper_id,
            terms,
            top_sections,
            cache_dir,
            pdf_cache_dir,
            timeout,
            ocr_mode,
            ocr_language,
        )
        if not extraction.get("evidence_eligible"):
            rows.append((paper_id, metadata[paper_id], extraction, event_id))
            print(f"HELD {paper_id}: no evidence-eligible full text after HTML/PDF/OCR", file=sys.stderr)
            continue
        event = skeleton_event(topic, topic_id, event_id, metadata[paper_id], extraction)
        skeleton_lines.append(json.dumps(event, ensure_ascii=False))
        rows.append((paper_id, metadata[paper_id], extraction, event_id))
        if offset + 1 < len(paper_ids):
            time.sleep(0.5)  # be gentle on arxiv.org/html
    Path(output_skeleton).write_text("\n".join(skeleton_lines) + ("\n" if skeleton_lines else ""), encoding="utf-8")
    Path(output_digest).write_text(render_digest(topic, rows, terms), encoding="utf-8")
    print(f"Wrote skeleton: {output_skeleton} ({len(skeleton_lines)} events, claims/stances are TODO)")
    print(f"Wrote digest:   {output_digest}")
    print("Next: fill claim/stance/evidence.summary per event from the digest, then run write_lit_outputs.py --validate-only.")
    return 0 if skeleton_lines else 2

#!/usr/bin/env python3
"""Project registry metadata into abstract-tier evidence events.

Abstracts are themselves evidence for related-work positioning: a human
survey writer never reads every paper in full either. One event per
registry candidate with a title + abstract, ``tier: "abstract"``, claim =
a condensed excerpt of the abstract. No stance and no full-text
verification — downstream consumers (packet, appendix, citation gate)
treat abstract-tier events as positioning-only material, never as
mechanism-level claims.

Output events share the run's event-ID prefix and numbering with the
deep-read projection (same citable namespace); allocate the deep-read
``start_seq`` after this file exists (the driver computes it from the
highest allocated event ID in ``evidence/*.jsonl``).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ABSTRACT_TIER = "abstract"
ABSTRACT_FILENAME = "abstract-tier.jsonl"
# Sentence splitter good enough for excerpting: split on ., ！, ?, ； kept
# simple on purpose — an off-by-one sentence in an excerpt is harmless.
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
MAX_EXCERPT_CHARS = 300


def excerpt(text: str, *, max_chars: int = MAX_EXCERPT_CHARS) -> str:
    """First one-to-two sentences of an abstract, hard-capped. Whitespace
    normalized; the excerpt is positioning material, not a quote-verified
    claim, so mild truncation is acceptable by construction."""
    text = " ".join(str(text or "").split())
    if not text:
        return ""
    sentences = _SENTENCE_RE.split(text)
    out = sentences[0] if sentences else text
    if len(out) < max_chars * 0.6 and len(sentences) > 1:
        candidate = out + " " + sentences[1]
        if len(candidate) <= max_chars:
            out = candidate
    if len(out) > max_chars:
        out = out[: max_chars - 1].rstrip() + "…"
    return out


def _normalize_authors(authors: Any) -> list[dict[str, Any]]:
    from embodied_learning.knowledge.evidence_projection import normalize_authors

    if not isinstance(authors, list):
        return []
    return normalize_authors(authors)


def build_abstract_events(
    registry: dict[str, Any],
    *,
    topic: str,
    topic_id: str,
    prefix: str,
    start_seq: int,
    exclude_arxiv_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    """One abstract-tier event per registry candidate with title + abstract.

    ``exclude_arxiv_ids`` drops papers that already carry full-text evidence
    (their abstract event would be redundant positioning)."""
    prefix = prefix.rstrip("-")
    exclude = exclude_arxiv_ids or set()
    events: list[dict[str, Any]] = []
    seq = start_seq
    for candidate in registry.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        arxiv_id = str(candidate.get("arxiv_id") or "").strip()
        title = str(candidate.get("title") or "").strip()
        summary = str(candidate.get("summary") or "").strip()
        if not arxiv_id or not title or not summary or arxiv_id in exclude:
            continue
        cond = excerpt(summary)
        if not cond:
            continue
        events.append({
            "event_id": f"{prefix}-{seq:04d}",
            "tier": ABSTRACT_TIER,
            "topic_id": topic_id,
            "topic": topic,
            "paper": {
                "arxiv_id": arxiv_id,
                "title": title,
                "published": str(candidate.get("published") or ""),
                "url": str(candidate.get("abs_url") or f"https://arxiv.org/abs/{arxiv_id}"),
            },
            "authors": _normalize_authors(candidate.get("authors")),
            "claim": cond,
            "stance": "",
            "evidence": {
                "summary": cond,
                "locator": "abstract",
                "short_quote": cond,
                "evidence_type": "positioning",
                "extraction": {
                    "source_format": "registry-metadata",
                    "method": "abstract-excerpt",
                    "quality": "abstract-only",
                    "visual_validation": "not-required",
                    "visual_validation_pages": [],
                },
            },
        })
        seq += 1
    return events


def write_abstract_tier(events: list[dict[str, Any]], evidence_dir: Path) -> Path:
    """Atomically write the abstract-tier JSONL next to the deep-read events."""
    from embodied_learning.atomicio import atomic_write_text

    evidence_dir.mkdir(parents=True, exist_ok=True)
    target = evidence_dir / ABSTRACT_FILENAME
    payload = "\n".join(json.dumps(event, ensure_ascii=False) for event in events)
    atomic_write_text(target, payload + "\n" if payload else "")
    return target


def load_tier(events: list[dict[str, Any]], tier: str | None) -> list[dict[str, Any]]:
    """Split helper: ``tier=None`` returns full-text-tier events only
    (everything without the abstract marker); ``tier="abstract"`` returns
    abstract-tier events only."""
    if tier == ABSTRACT_TIER:
        return [e for e in events if str(e.get("tier") or "") == ABSTRACT_TIER]
    return [e for e in events if str(e.get("tier") or "") != ABSTRACT_TIER]


def max_event_seq(events: list[dict[str, Any]]) -> int:
    """Highest numeric suffix across ``{prefix}-{seq:04d}`` event IDs."""
    highest = 0
    for event in events:
        match = re.search(r"-(\d{4,})$", str(event.get("event_id") or ""))
        if match:
            highest = max(highest, int(match.group(1)))
    return highest


def read_events(path: Path) -> list[dict[str, Any]]:
    """Load one evidence JSONL (a per-paper file or ``abstract-tier.jsonl``).

    Malformed lines are skipped, not fatal: the projection counters and the
    next-sequence computation tolerate a torn line on a shared mount."""
    events: list[dict[str, Any]] = []
    if not path.is_file():
        return events
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events

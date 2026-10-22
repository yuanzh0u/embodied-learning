"""KB search: case-insensitive substring query over runs, papers, events, topics.

Named ``query`` to stay clear of ``embodied_learning.search`` (external arXiv /
Semantic Scholar retrieval). Library entry is :func:`kb_search`; the CLI is
``wiki.py kb-search``.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from embodied_learning.knowledge.model import KnowledgeBase

SCOPES = ("all", "runs", "papers", "events", "topics")
DEFAULT_LIMIT = 20


def _terms(query: str) -> list[str]:
    return [term for term in query.casefold().split() if term]


def _matched_fields(fields: dict[str, str], terms: list[str]) -> list[str]:
    """A field matches when every term is a substring of its casefolded text."""
    hits: list[str] = []
    for name, value in fields.items():
        text = (value or "").casefold()
        if text and all(term in text for term in terms):
            hits.append(name)
    return hits


def _run_row(run, matched: list[str]) -> dict[str, Any]:
    return {
        "scope": "runs",
        "id": run.name,
        "matched_fields": matched,
        "topic": run.topic,
        "status": run.status,
        "review_mode": run.review_mode,
        "event_count": len(run.events()),
        "kb_path": str(run.path),
    }


def _paper_row(paper, matched: list[str]) -> dict[str, Any]:
    return {
        "scope": "papers",
        "id": paper.dir_name,
        "matched_fields": matched,
        "title": paper.title,
        "arxiv_id": paper.arxiv_id,
        "quality": paper.quality,
        "has_full_text": paper.has_full_text,
        "has_deep_read": paper.has_deep_read,
        "kb_path": str(paper.path),
    }


def _event_row(event, matched: list[str]) -> dict[str, Any]:
    return {
        "scope": "events",
        "id": event.event_id,
        "matched_fields": matched,
        "run": event.run_name,
        "paper_id": event.paper_id,
        "paper_title": event.paper_title,
        "claim": event.claim,
        "stance": event.stance,
        "topic_id": event.topic_id,
        "kb_path": f"evidence/{event.run_name}/evidence.jsonl",
    }


def _topic_row(topic, matched: list[str]) -> dict[str, Any]:
    return {
        "scope": "topics",
        "id": topic.id,
        "matched_fields": matched,
        "title": topic.title,
        "topic_key": topic.topic_key,
        "field": topic.field,
        "date": topic.date,
    }


def kb_search(
    kb: KnowledgeBase,
    query: str,
    *,
    scope: str = "all",
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    """Substring search across the KB. ``scope=all`` applies ``limit`` per scope."""
    if scope not in SCOPES:
        raise ValueError(f"unknown scope {scope!r}; expected one of {SCOPES}")
    terms = _terms(query)
    if not terms:
        return []
    if limit <= 0:
        return []

    hits: list[dict[str, Any]] = []

    def take(rows: list[dict[str, Any]]) -> None:
        hits.extend(rows[:limit])

    if scope in ("all", "runs"):
        rows: list[dict[str, Any]] = []
        for run in kb.runs():
            manifest = run.manifest
            matched = _matched_fields(
                {
                    "topic": manifest.topic,
                    "run": run.name,
                    "review_mode": manifest.review_mode,
                    "status": manifest.status,
                    "notes": manifest.notes,
                    "time_range": manifest.time_range,
                    "knowledge_ids": " ".join(manifest.knowledge_ids),
                },
                terms,
            )
            if matched:
                rows.append(_run_row(run, matched))
            if scope == "runs" and len(rows) >= limit:
                break
        take(rows)

    if scope in ("all", "papers"):
        rows = []
        for paper in kb.papers():
            matched = _matched_fields(
                {
                    "title": paper.title,
                    "dir_name": paper.dir_name,
                    "arxiv_id": paper.arxiv_id,
                    "published": str(paper.meta.get("published") or ""),
                },
                terms,
            )
            if matched:
                rows.append(_paper_row(paper, matched))
            if scope == "papers" and len(rows) >= limit:
                break
        take(rows)

    if scope in ("all", "events"):
        rows = []
        for event in kb.iter_events():
            evidence = event.raw.get("evidence") if isinstance(event.raw.get("evidence"), dict) else {}
            matched = _matched_fields(
                {
                    "claim": event.claim,
                    "evidence.summary": str(evidence.get("summary") or ""),
                    "paper.title": event.paper_title,
                    "paper.arxiv_id": event.paper_id,
                    "topic_id": event.topic_id,
                    "event_id": event.event_id,
                },
                terms,
            )
            if matched:
                rows.append(_event_row(event, matched))
            if scope == "events" and len(rows) >= limit:
                break
        take(rows)

    if scope in ("all", "topics"):
        rows = []
        for topic in kb.wiki_topics():
            matched = _matched_fields(
                {
                    "title": topic.title,
                    "topic_key": topic.topic_key,
                    "excerpt": topic.excerpt,
                    "field": topic.field,
                },
                terms,
            )
            if matched:
                rows.append(_topic_row(topic, matched))
            if scope == "topics" and len(rows) >= limit:
                break
        take(rows)

    return hits


def render(hits: list[dict[str, Any]], query: str, scope: str) -> str:
    if not hits:
        return "（无命中）"
    lines = [f"检索：{query!r}（scope={scope}）命中 {len(hits)} 条", ""]
    for hit in hits:
        kind = hit.get("scope", "")
        if kind == "runs":
            lines.append(
                f"[run] {hit.get('id')}  {hit.get('topic')}"
                f"  ({hit.get('review_mode')}, {hit.get('status')}, events={hit.get('event_count')})"
            )
        elif kind == "papers":
            flags = []
            if hit.get("has_full_text"):
                flags.append("全文")
            if hit.get("has_deep_read"):
                flags.append("精读")
            suffix = f"  [{'+'.join(flags)}]" if flags else ""
            lines.append(f"[paper] {hit.get('arxiv_id') or hit.get('id')}  {hit.get('title')}{suffix}")
        elif kind == "events":
            claim = str(hit.get("claim") or "")
            if len(claim) > 160:
                claim = claim[:157] + "…"
            lines.append(
                f"[event] {hit.get('id')}  ({hit.get('stance')}, {hit.get('run')})  {claim}"
            )
        elif kind == "topics":
            lines.append(f"[topic] {hit.get('title')}  ({hit.get('field')}, {hit.get('date')})")
        else:
            lines.append(f"[{kind}] {hit.get('id')}")
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/wiki.py."""
    kb = KnowledgeBase.open(args.kb_root)
    if not kb.root.is_dir():
        print(f"KB root 不存在：{kb.root}", file=sys.stderr)
        return 1
    scope = str(getattr(args, "scope", "all") or "all")
    limit = int(getattr(args, "limit", DEFAULT_LIMIT) or DEFAULT_LIMIT)
    try:
        hits = kb_search(kb, args.query, scope=scope, limit=limit)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if getattr(args, "json", False):
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        print(render(hits, args.query, scope))
    return 0

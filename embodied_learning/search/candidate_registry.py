#!/usr/bin/env python3
"""Merge multi-round arXiv/API/browser discovery into one deduplicated candidate registry.

Library API: the module-level :func:`build_registry` function (pure merge of
discovery JSON files into the registry dict) plus the per-channel loaders
(``load_api_results``, ``load_browser_results``, ...). The CLI surface owns
argument parsing and file writing and lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/build_candidate_registry.py``.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {
    "discovered",
    "title-screened",
    "full-text-queued",
    "extracted",
    "accepted",
    "rejected",
    "unavailable",
}


def normalize_id(value: object) -> str:
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_base(arxiv_id: str) -> dict[str, Any]:
    return {
        "arxiv_id": arxiv_id,
        "doi": "",
        "title": "",
        "authors": [],
        "published": "",
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "summary": "",
        "categories": [],
        "citation_count": None,
        "status": "discovered",
        "exclusion_reason": "",
        "extraction": {},
        "discoveries": [],
    }


def merge_metadata(record: dict[str, Any], raw: dict[str, Any]) -> None:
    for field in ("title", "published", "summary", "abs_url", "pdf_url", "doi"):
        value = raw.get(field)
        if value and not record.get(field):
            record[field] = value
    for field in ("authors", "categories"):
        values = raw.get(field)
        if isinstance(values, list):
            current = record.setdefault(field, [])
            for value in values:
                if value not in current:
                    current.append(value)
    citation_count = raw.get("citation_count")
    if isinstance(citation_count, (int, float)):
        record["citation_count"] = max(int(citation_count), int(record.get("citation_count") or 0))


def add_discovery(record: dict[str, Any], *, batch: str, channel: str, labels: list[str], source: str) -> None:
    item = {"batch": batch, "channel": channel, "query_labels": labels, "source": source}
    if item not in record["discoveries"]:
        record["discoveries"].append(item)


def load_api_results(paths: list[Path], registry: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    batches: list[dict[str, Any]] = []
    for index, path in enumerate(paths, start=1):
        data = load_json(path)
        batch = str(data.get("batch") or path.stem or f"api-{index}")
        ids: list[str] = []
        for raw in data.get("papers", []):
            if not isinstance(raw, dict):
                continue
            arxiv_id = normalize_id(raw.get("arxiv_id"))
            if not arxiv_id:
                continue
            ids.append(arxiv_id)
            record = registry.setdefault(arxiv_id, candidate_base(arxiv_id))
            merge_metadata(record, raw)
            labels = [label for label in str(raw.get("query_label") or "").split(",") if label]
            add_discovery(record, batch=batch, channel="arxiv-api", labels=labels, source=str(path))
        batches.append({"batch": batch, "channel": "arxiv-api", "candidate_ids": sorted(set(ids)), "source": str(path)})
    return batches


def load_semantic_scholar_results(paths: list[Path], registry: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge search_semantic_scholar.py output: S2 metadata-search candidates.

    Shares load_api_results()'s "papers" shape (plus doi/citation_count which
    merge_metadata carries through) but tags the discovery channel truthfully
    as "semantic-scholar".
    """
    batches: list[dict[str, Any]] = []
    for index, path in enumerate(paths, start=1):
        data = load_json(path)
        batch = str(data.get("batch") or path.stem or f"s2-{index}")
        ids: list[str] = []
        for raw in data.get("papers", []):
            if not isinstance(raw, dict):
                continue
            arxiv_id = normalize_id(raw.get("arxiv_id"))
            if not arxiv_id:
                continue
            ids.append(arxiv_id)
            record = registry.setdefault(arxiv_id, candidate_base(arxiv_id))
            merge_metadata(record, raw)
            labels = [label for label in str(raw.get("query_label") or "").split(",") if label]
            add_discovery(record, batch=batch, channel="semantic-scholar", labels=labels, source=str(path))
        batches.append({"batch": batch, "channel": "semantic-scholar", "candidate_ids": sorted(set(ids)), "source": str(path)})
    return batches


def load_browser_results(paths: list[Path], registry: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    batches: list[dict[str, Any]] = []
    for index, path in enumerate(paths, start=1):
        data = load_json(path)
        batch = str(data.get("batch") or data.get("source_label") or path.stem or f"browser-{index}")
        ids: list[str] = []
        for raw in data.get("candidates", []):
            if not isinstance(raw, dict) or raw.get("in_window") is False:
                continue
            arxiv_id = normalize_id(raw.get("arxiv_id"))
            if not arxiv_id:
                continue
            ids.append(arxiv_id)
            record = registry.setdefault(arxiv_id, candidate_base(arxiv_id))
            merge_metadata(record, raw)
            context = str(raw.get("context") or "")
            if context and not record.get("discovery_context"):
                record["discovery_context"] = context
            labels = [str(data.get("source_label") or "browser-fallback")]
            add_discovery(record, batch=batch, channel="browser", labels=labels, source=str(path))
        batches.append({"batch": batch, "channel": "browser", "candidate_ids": sorted(set(ids)), "source": str(path)})
    return batches


def load_citation_results(paths: list[Path], registry: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge expand_via_citations.py output: citation/co-citation-derived candidates.

    Shares load_api_results()'s "papers" shape (same arxiv_id/title/authors/
    published/summary/categories/query_label fields) but tags the discovery
    channel truthfully as "citation-graph" and carries through the
    shared_seed_count/connected_seeds coupling signal for future screening use.
    """
    batches: list[dict[str, Any]] = []
    for index, path in enumerate(paths, start=1):
        data = load_json(path)
        batch = str(data.get("batch") or path.stem or f"citation-{index}")
        ids: list[str] = []
        for raw in data.get("papers", []):
            if not isinstance(raw, dict):
                continue
            arxiv_id = normalize_id(raw.get("arxiv_id"))
            if not arxiv_id:
                continue
            ids.append(arxiv_id)
            record = registry.setdefault(arxiv_id, candidate_base(arxiv_id))
            merge_metadata(record, raw)
            if raw.get("shared_seed_count") is not None:
                record["shared_seed_count"] = max(int(raw["shared_seed_count"]), int(record.get("shared_seed_count", 0)))
            connected = raw.get("connected_seeds")
            if isinstance(connected, list):
                current = record.setdefault("connected_seeds", [])
                for seed in connected:
                    if seed not in current:
                        current.append(seed)
            labels = [label for label in str(raw.get("query_label") or "").split(",") if label]
            add_discovery(record, batch=batch, channel="citation-graph", labels=labels, source=str(path))
        batches.append({"batch": batch, "channel": "citation-graph", "candidate_ids": sorted(set(ids)), "source": str(path)})
    return batches


def load_screening(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    data = load_json(path)
    rows = data.get("candidates", []) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError(f"{path}: expected a list or {{'candidates': [...]}}")
    updates: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        arxiv_id = normalize_id(row.get("arxiv_id"))
        if not arxiv_id:
            continue
        status = str(row.get("status") or "discovered")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"{path}: invalid status {status!r} for {arxiv_id}")
        updates[arxiv_id] = row
    return updates


def apply_screening(registry: dict[str, dict[str, Any]], updates: dict[str, dict[str, Any]]) -> None:
    for arxiv_id, update in updates.items():
        record = registry.setdefault(arxiv_id, candidate_base(arxiv_id))
        record["status"] = update.get("status", record["status"])
        record["exclusion_reason"] = update.get("exclusion_reason", record["exclusion_reason"])
        if isinstance(update.get("extraction"), dict):
            record["extraction"] = update["extraction"]
        merge_metadata(record, update)


def build_registry(
    search_results: list[Path],
    browser_results: list[Path],
    screening_file: Path | None = None,
    citation_results: list[Path] | None = None,
    semantic_scholar_results: list[Path] | None = None,
) -> dict[str, Any]:
    registry: dict[str, dict[str, Any]] = {}
    batches = load_api_results(search_results, registry)
    batches.extend(load_semantic_scholar_results(semantic_scholar_results or [], registry))
    batches.extend(load_browser_results(browser_results, registry))
    batches.extend(load_citation_results(citation_results or [], registry))
    apply_screening(registry, load_screening(screening_file))
    candidates = [registry[key] for key in sorted(registry)]
    status_counts: dict[str, int] = {}
    for item in candidates:
        status = str(item["status"])
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "candidate_count": len(candidates),
        "status_counts": dict(sorted(status_counts.items())),
        "batches": batches,
        "candidates": candidates,
    }


def run(
    search_results: list[Path],
    browser_results: list[Path],
    citation_results: list[Path],
    semantic_scholar_results: list[Path],
    screening_file: Path | None,
    output: Path,
) -> int:
    """CLI-side orchestration: validate inputs, build, and write the registry file."""
    if not search_results and not browser_results and not citation_results and not semantic_scholar_results:
        raise SystemExit(
            "provide at least one --search-result, --semantic-scholar-result, --browser-result, or --citation-result"
        )
    result = build_registry(
        search_results,
        browser_results,
        screening_file,
        citation_results,
        semantic_scholar_results,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote candidate registry: {output} ({result['candidate_count']} unique papers)")
    return 0



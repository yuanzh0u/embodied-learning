#!/usr/bin/env python3
"""Merge multi-round arXiv/API/browser discovery into one deduplicated candidate registry."""

from __future__ import annotations

import argparse
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search-result", action="append", default=[], help="search_arxiv.py JSON; repeat by round.")
    parser.add_argument("--browser-result", action="append", default=[], help="parse_browser_candidates.py JSON; repeatable.")
    parser.add_argument("--screening-file", help="Optional JSON candidate/status updates.")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def normalize_id(value: object) -> str:
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_base(arxiv_id: str) -> dict[str, Any]:
    return {
        "arxiv_id": arxiv_id,
        "title": "",
        "authors": [],
        "published": "",
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "summary": "",
        "categories": [],
        "status": "discovered",
        "exclusion_reason": "",
        "extraction": {},
        "discoveries": [],
    }


def merge_metadata(record: dict[str, Any], raw: dict[str, Any]) -> None:
    for field in ("title", "published", "summary", "abs_url", "pdf_url"):
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
) -> dict[str, Any]:
    registry: dict[str, dict[str, Any]] = {}
    batches = load_api_results(search_results, registry)
    batches.extend(load_browser_results(browser_results, registry))
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


def main() -> int:
    args = parse_args()
    if not args.search_result and not args.browser_result:
        raise SystemExit("provide at least one --search-result or --browser-result")
    result = build_registry(
        [Path(path) for path in args.search_result],
        [Path(path) for path in args.browser_result],
        Path(args.screening_file) if args.screening_file else None,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote candidate registry: {output} ({result['candidate_count']} unique papers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

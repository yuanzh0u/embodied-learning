#!/usr/bin/env python3
"""Print a title-only slice of a candidate registry without dumping summaries.

Agents MUST NOT Read full candidate-registry.json into LLM context (often
2–5 MB). Use coverage-report.json, screening-*.md, status_counts, or this
script's title-only stdout instead.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


STATUS_PRIORITY = {
    "accepted": 0,
    "extracted": 1,
    "full-text-queued": 2,
    "title-screened": 3,
    "discovered": 4,
    "rejected": 5,
    "unavailable": 6,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-registry", required=True, help="Path to candidate-registry.json")
    parser.add_argument(
        "--status",
        action="append",
        default=[],
        help="Only include this status (repeatable). Default: all statuses.",
    )
    parser.add_argument("--limit", type=int, default=80, help="Max titles to print (default 80).")
    parser.add_argument(
        "--status-counts-only",
        action="store_true",
        help="Print only registry metadata and status_counts; no candidate titles.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default text).",
    )
    return parser


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def select_candidates(
    registry: dict[str, Any],
    statuses: list[str],
    limit: int,
) -> list[dict[str, str]]:
    wanted = {item.strip() for item in statuses if item.strip()}
    rows: list[dict[str, str]] = []
    for candidate in registry.get("candidates") or []:
        if not isinstance(candidate, dict):
            continue
        status = str(candidate.get("status") or "discovered")
        if wanted and status not in wanted:
            continue
        rows.append(
            {
                "arxiv_id": str(candidate.get("arxiv_id") or ""),
                "status": status,
                "title": str(candidate.get("title") or "").strip(),
                "published": str(candidate.get("published") or ""),
            }
        )
    rows.sort(
        key=lambda row: (
            STATUS_PRIORITY.get(row["status"], 99),
            row["published"],
            row["arxiv_id"],
        )
    )
    if limit < 0:
        return rows
    return rows[: max(0, limit)]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        registry = load_registry(Path(args.candidate_registry))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"print_registry_titles blocked: {exc}", file=sys.stderr)
        return 2

    meta = {
        "candidate_count": registry.get("candidate_count", len(registry.get("candidates") or [])),
        "status_counts": registry.get("status_counts") or {},
        "version": registry.get("version"),
        "generated_at": registry.get("generated_at"),
    }

    if args.status_counts_only:
        if args.format == "json":
            json.dump(meta, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        else:
            sys.stdout.write(f"candidate_count: {meta['candidate_count']}\n")
            sys.stdout.write("status_counts:\n")
            for status, count in sorted((meta["status_counts"] or {}).items()):
                sys.stdout.write(f"  {status}: {count}\n")
        return 0

    rows = select_candidates(registry, args.status, args.limit)
    if args.format == "json":
        payload = {**meta, "limit": args.limit, "returned": len(rows), "titles": rows}
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    sys.stdout.write(
        f"# registry title slice (n={meta['candidate_count']}; showing {len(rows)}; "
        f"NEVER dump full candidate-registry.json into LLM context)\n"
    )
    sys.stdout.write(f"# status_counts: {meta['status_counts']}\n")
    for row in rows:
        title = row["title"].replace("\n", " ").strip()
        sys.stdout.write(f"{row['arxiv_id']}\t{row['status']}\t{title}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

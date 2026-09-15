#!/usr/bin/env python3
"""Prioritize a large candidate registry for full-text recovery without accepting evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-registry", required=True)
    parser.add_argument("--terms", required=True, help="Comma-separated title/abstract relevance terms.")
    parser.add_argument("--query-label-prefix", action="append", default=[], help="Prefer discoveries whose query label starts with this prefix.")
    parser.add_argument("--seed-evidence-jsonl", action="append", default=[], help="Previously accepted evidence used only as a priority seed.")
    parser.add_argument("--limit", type=int, default=40, help="Number of candidates to queue for full-text recovery.")
    parser.add_argument("--output-screening", required=True)
    parser.add_argument("--output-ids", required=True)
    parser.add_argument("--output-markdown")
    return parser.parse_args()


def load_seed_ids(paths: list[str]) -> set[str]:
    result: set[str] = set()
    for filename in paths:
        for line in Path(filename).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            paper = event.get("paper") or {}
            if isinstance(paper, dict) and paper.get("arxiv_id"):
                result.add(str(paper["arxiv_id"]).split("v", 1)[0])
    return result


def discovery_labels(candidate: dict[str, Any]) -> set[str]:
    labels: set[str] = set()
    for discovery in candidate.get("discoveries", []):
        if isinstance(discovery, dict):
            labels.update(str(value) for value in discovery.get("query_labels", []) if value)
    return labels


def score_candidate(candidate: dict[str, Any], terms: list[str], prefixes: list[str], seed_ids: set[str]) -> dict[str, Any]:
    arxiv_id = str(candidate.get("arxiv_id") or "")
    title = str(candidate.get("title") or "").lower()
    summary = str(candidate.get("summary") or "").lower()
    labels = discovery_labels(candidate)
    matched_title = [term for term in terms if term in title]
    matched_summary = [term for term in terms if term in summary and term not in matched_title]
    matched_labels = sorted(label for label in labels if any(label.startswith(prefix) for prefix in prefixes))
    seeded = arxiv_id in seed_ids
    # Prior evidence is a small continuity signal, not an automatic win. The
    # former +100 bonus could crowd new, limiting, or contradictory papers out
    # of the recovery queue before their full text was inspected.
    score = (4 if seeded else 0) + 10 * len(matched_title) + 2 * len(matched_summary) + 6 * len(matched_labels)
    return {
        "candidate": candidate,
        "score": score,
        "seeded": seeded,
        "matched_title_terms": matched_title,
        "matched_summary_terms": matched_summary,
        "matched_query_labels": matched_labels,
    }


def select_candidates(registry: dict[str, Any], terms: list[str], prefixes: list[str], seed_ids: set[str], limit: int) -> list[dict[str, Any]]:
    ranked = [score_candidate(item, terms, prefixes, seed_ids) for item in registry.get("candidates", []) if isinstance(item, dict)]
    ranked = [item for item in ranked if item["score"] > 0]
    ranked.sort(
        key=lambda item: (
            -int(item["score"]),
            -int(bool(item["seeded"])),
            str((item["candidate"].get("published") or "")),
            str(item["candidate"].get("arxiv_id") or ""),
        )
    )
    limit = max(0, limit)
    if not limit:
        return []
    seeded = [item for item in ranked if item["seeded"]]
    new = [item for item in ranked if not item["seeded"]]
    # Reserve at most 25% of a normal queue for prior accepted papers while
    # allowing unused capacity to be filled from either stratum.
    seed_quota = min(len(seeded), max(1, limit // 4))
    selected = seeded[:seed_quota] + new[: max(0, limit - seed_quota)]
    selected_ids = {str(item["candidate"].get("arxiv_id") or "") for item in selected}
    if len(selected) < limit:
        selected.extend(
            item
            for item in ranked
            if str(item["candidate"].get("arxiv_id") or "") not in selected_ids
        )
    selected = selected[:limit]
    selected.sort(
        key=lambda item: (
            -int(item["score"]),
            str((item["candidate"].get("published") or "")),
            str(item["candidate"].get("arxiv_id") or ""),
        )
    )
    return selected


def render_markdown(selected: list[dict[str, Any]], registry_count: int) -> str:
    lines = [
        "# Full-text screening queue",
        "",
        f"- Candidate registry: {registry_count} papers",
        f"- Queued for full text: {len(selected)} papers",
        "- This is priority screening only; queued papers are not accepted evidence.",
        "",
        "| Rank | arXiv | Score | Seed | Title | Matches |",
        "|---:|---|---:|---|---|---|",
    ]
    for rank, item in enumerate(selected, start=1):
        candidate = item["candidate"]
        matches = item["matched_title_terms"] + item["matched_summary_terms"] + item["matched_query_labels"]
        title = str(candidate.get("title") or "").replace("|", "\\|")
        lines.append(
            f"| {rank} | [{candidate.get('arxiv_id')}]({candidate.get('abs_url')}) | {item['score']} | "
            f"{'yes' if item['seeded'] else 'no'} | {title} | {', '.join(matches[:8])} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    registry = json.loads(Path(args.candidate_registry).read_text(encoding="utf-8"))
    terms = [value.strip().lower() for value in args.terms.split(",") if value.strip()]
    selected = select_candidates(registry, terms, args.query_label_prefix, load_seed_ids(args.seed_evidence_jsonl), args.limit)
    if len(selected) < args.limit:
        print(f"Only {len(selected)} candidates matched; requested {args.limit}.")
    screening = {
        "version": 1,
        "candidate_registry": args.candidate_registry,
        "selection_rule": {
            "terms": terms,
            "query_label_prefixes": args.query_label_prefix,
            "seed_evidence_jsonl": args.seed_evidence_jsonl,
            "limit": args.limit,
            "prior_seed_bonus": 4,
            "prior_seed_queue_cap": "25% when enough non-seed candidates match; unused capacity is backfilled",
            "note": "Priority queue only. Complete full-text recovery and paper-reader verification remain mandatory.",
        },
        "candidates": [
            {
                "arxiv_id": item["candidate"].get("arxiv_id"),
                "status": "full-text-queued",
                "exclusion_reason": "",
                "screening_score": item["score"],
                "seeded_from_prior_evidence": item["seeded"],
                "matched_title_terms": item["matched_title_terms"],
                "matched_summary_terms": item["matched_summary_terms"],
                "matched_query_labels": item["matched_query_labels"],
            }
            for item in selected
        ],
    }
    Path(args.output_screening).write_text(json.dumps(screening, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.output_ids).write_text("\n".join(str(item["candidate"].get("arxiv_id")) for item in selected) + "\n", encoding="utf-8")
    if args.output_markdown:
        Path(args.output_markdown).write_text(render_markdown(selected, int(registry.get("candidate_count") or 0)), encoding="utf-8")
    print(f"Queued {len(selected)} of {registry.get('candidate_count', 0)} candidates for full-text recovery.")
    return 0 if selected else 2


if __name__ == "__main__":
    raise SystemExit(main())

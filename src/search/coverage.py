#!/usr/bin/env python3
"""Assess query-dimension coverage and multi-round saturation for a candidate registry."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


FULL_TEXT_STATUSES = {"extracted", "accepted"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-plan", required=True)
    parser.add_argument("--candidate-registry", required=True)
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Accepted evidence; repeatable.")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def accepted_ids(paths: list[Path]) -> set[str]:
    result: set[str] = set()
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            paper = event.get("paper") or {}
            if isinstance(paper, dict) and paper.get("arxiv_id"):
                result.add(str(paper["arxiv_id"]).split("v", 1)[0])
    return result


def discovery_labels(candidate: dict[str, Any]) -> set[str]:
    labels: set[str] = set()
    for item in candidate.get("discoveries", []):
        if not isinstance(item, dict):
            continue
        labels.update(str(label) for label in item.get("query_labels", []) if label)
    return labels


def batch_saturation(batches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    results: list[dict[str, Any]] = []
    for item in batches:
        ids = {str(value) for value in item.get("candidate_ids", []) if value}
        new_ids = ids - seen
        results.append(
            {
                "batch": item.get("batch"),
                "channel": item.get("channel"),
                "batch_unique": len(ids),
                "new_unique": len(new_ids),
                "new_unique_rate": round(len(new_ids) / max(1, len(ids)), 4),
                "cumulative_unique": len(seen | ids),
            }
        )
        seen.update(ids)
    return results


def assess(plan: dict[str, Any], registry: dict[str, Any], evidence_paths: list[Path]) -> dict[str, Any]:
    candidates = [item for item in registry.get("candidates", []) if isinstance(item, dict)]
    accepted_evidence = accepted_ids(evidence_paths)
    accepted = set(accepted_evidence)
    accepted.update(
        str(item.get("arxiv_id")) for item in candidates if item.get("status") == "accepted"
    )
    full_text = {
        str(item.get("arxiv_id"))
        for item in candidates
        if item.get("status") in FULL_TEXT_STATUSES
        or bool((item.get("extraction") or {}).get("evidence_eligible"))
    }
    targets = plan.get("search_targets") or {
        "candidate_floor": plan.get("minimum_candidate_count", 0),
        "full_text_floor": 0,
        "accepted_paper_floor": 0,
    }
    dimensions: list[dict[str, Any]] = []
    for raw in plan.get("coverage_dimensions", []):
        labels = {str(value) for value in raw.get("query_labels", [])}
        matched = sorted(
            str(item.get("arxiv_id"))
            for item in candidates
            if labels & discovery_labels(item)
        )
        minimum = int(raw.get("minimum_unique_candidates") or 0)
        dimensions.append(
            {
                "dimension": raw.get("dimension"),
                "minimum_unique_candidates": minimum,
                "unique_candidates": len(set(matched)),
                "passed": len(set(matched)) >= minimum,
                "candidate_ids": sorted(set(matched)),
            }
        )
    rounds = batch_saturation(registry.get("batches", []))
    rule = plan.get("stopping_rule") or {}
    minimum_batches = int(rule.get("minimum_batches") or 1)
    saturation_rounds = int(rule.get("saturation_rounds") or 1)
    max_rate = float(rule.get("max_new_unique_rate") or 0.10)
    tail = rounds[-saturation_rounds:] if saturation_rounds else []
    saturated = (
        len(rounds) >= minimum_batches
        and len(tail) == saturation_rounds
        and all(float(item["new_unique_rate"]) <= max_rate for item in tail)
    )
    checks = {
        "candidate_floor": len(candidates) >= int(targets.get("candidate_floor") or 0),
        "full_text_floor": len(full_text) >= int(targets.get("full_text_floor") or 0),
        # When evidence JSONL is provided, only papers in that accepted evidence
        # set satisfy the gate. Registry `accepted` is retained for legacy runs.
        "accepted_paper_floor": len(accepted_evidence if evidence_paths else accepted)
        >= int(targets.get("accepted_paper_floor") or 0),
        "coverage_dimensions": all(item["passed"] for item in dimensions) if dimensions else False,
        "saturation": saturated,
    }
    unresolved = [name for name, passed in checks.items() if not passed]
    return {
        "version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "review_mode": plan.get("review_mode", "unknown"),
        "targets": targets,
        "observed": {
            "candidate_count": len(candidates),
            "full_text_recovered_count": len(full_text),
            "full_text_count": len(full_text),
            "accepted_paper_count": len(accepted),
            "accepted_evidence_paper_count": len(accepted_evidence),
            "batch_count": len(rounds),
        },
        "metric_notes": {
            "full_text_count": "Deprecated compatibility alias for full_text_recovered_count; it does not mean read.",
            "coverage_dimensions": "Candidate discovery-label coverage, not deep-read accepted-evidence coverage.",
        },
        "coverage_dimensions": dimensions,
        "saturation_rounds": rounds,
        "stop_assessment": {
            "ready_to_stop": all(checks.values()),
            "checks": checks,
            "unresolved": unresolved,
            "note": "A paper-count floor is necessary but never sufficient; all checks must pass.",
        },
    }


def main() -> int:
    args = parse_args()
    result = assess(
        load_json(Path(args.query_plan)),
        load_json(Path(args.candidate_registry)),
        [Path(path) for path in args.evidence_jsonl],
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state = "ready" if result["stop_assessment"]["ready_to_stop"] else "continue"
    print(f"wrote coverage report: {output} ({state})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Plan a paper-reader migration across existing literature-review runs.

Select each run's reader-facing citations first, then limiting/conditional/gap
evidence and multi-event core papers until the requested accepted-paper floor
is met. The union is deduplicated across runs for full-text recovery/reading.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ARXIV_URL_RE = re.compile(r"https://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?")
ARTICLE_NAMES = (
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", default="evidence")
    parser.add_argument("--run-pattern", default="literature-review-*-20260714")
    parser.add_argument("--extraction-dir")
    parser.add_argument(
        "--require-readable",
        action="store_true",
        help="Select only papers with complete, evidence-eligible full text.",
    )
    parser.add_argument(
        "--supplement-file",
        help=(
            "Optional JSON object mapping a source run directory name or run id "
            "to candidate-registry arXiv ids used to backfill unreadable papers."
        ),
    )
    parser.add_argument("--paper-floor", type=int, default=15)
    parser.add_argument("--output", required=True)
    parser.add_argument("--paper-id-output", required=True)
    return parser.parse_args()


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            events.append(value)
    return events


def cited_ids(run_dir: Path) -> set[str]:
    ids: set[str] = set()
    for name in ARTICLE_NAMES:
        path = run_dir / name
        if path.is_file():
            ids.update(ARXIV_URL_RE.findall(path.read_text(encoding="utf-8")))
    return ids


def extraction_state(extraction_dir: Path | None, paper_id: str) -> dict[str, Any]:
    if extraction_dir is None:
        return {"path": "", "exists": False, "complete_full_text": False, "eligible": False}
    path = extraction_dir / f"{paper_id}.json"
    if not path.is_file():
        return {"path": str(path), "exists": False, "complete_full_text": False, "eligible": False}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"path": str(path), "exists": True, "complete_full_text": False, "eligible": False}
    complete = bool(
        (isinstance(payload.get("text"), str) and payload["text"].strip())
        or (isinstance(payload.get("pages"), list) and payload["pages"])
    )
    return {
        "path": str(path),
        "exists": True,
        "complete_full_text": complete,
        "eligible": bool(payload.get("evidence_eligible")),
        "method": payload.get("extraction_method", ""),
        "quality": (payload.get("quality") or {}).get("grade", "") if isinstance(payload.get("quality"), dict) else payload.get("quality", ""),
    }


def load_supplements(path: Path | None) -> dict[str, list[str]]:
    if path is None:
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("supplement file must contain a JSON object")
    result: dict[str, list[str]] = {}
    for key, items in value.items():
        if not isinstance(items, list):
            raise ValueError(f"supplement list for {key!r} must be an array")
        result[str(key)] = [str(item).split("v", 1)[0] for item in items]
    return result


def plan_run(
    run_dir: Path,
    floor: int,
    extraction_dir: Path | None,
    require_readable: bool,
    supplements: dict[str, list[str]],
) -> dict[str, Any]:
    manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    events = load_events(run_dir / "evidence.jsonl")
    cited = cited_ids(run_dir)
    by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        paper = event.get("paper")
        if isinstance(paper, dict) and paper.get("arxiv_id"):
            by_paper[str(paper["arxiv_id"]).split("v", 1)[0]].append(event)

    ranked: list[dict[str, Any]] = []
    for paper_id, paper_events in by_paper.items():
        stance_set = {str(event.get("stance") or "") for event in paper_events}
        has_quote = any(
            isinstance(event.get("evidence"), dict)
            and len(str((event.get("evidence") or {}).get("short_quote") or "").strip()) >= 20
            for event in paper_events
        )
        has_extraction = any(
            isinstance(event.get("evidence"), dict)
            and isinstance((event.get("evidence") or {}).get("extraction"), dict)
            for event in paper_events
        )
        score = (
            (1000 if paper_id in cited else 0)
            + 20 * len(paper_events)
            + 12 * len(stance_set & {"limit", "conditional", "gap"})
            + (5 if has_extraction else 0)
            + (3 if has_quote else 0)
        )
        first = paper_events[0].get("paper") or {}
        ranked.append(
            {
                "paper_id": paper_id,
                "title": first.get("title", ""),
                "published": first.get("published", ""),
                "cited_by_articles": paper_id in cited,
                "event_count": len(paper_events),
                "stances": sorted(stance_set),
                "event_ids": [event.get("event_id") for event in paper_events],
                "score": score,
                "extraction": extraction_state(extraction_dir, paper_id),
            }
        )
    supplement_ids = set(supplements.get(run_dir.name, [])) | set(
        supplements.get(str(manifest.get("run") or ""), [])
    )
    if supplement_ids:
        registry = json.loads((run_dir / "candidate-registry.json").read_text(encoding="utf-8"))
        candidates = registry.get("candidates", []) if isinstance(registry, dict) else []
        candidate_map = {
            str(item.get("arxiv_id", "")).split("v", 1)[0]: item
            for item in candidates
            if isinstance(item, dict) and item.get("arxiv_id")
        }
        existing_ids = {str(item["paper_id"]) for item in ranked}
        for paper_id in sorted(supplement_ids - existing_ids):
            candidate = candidate_map.get(paper_id)
            if candidate is None:
                raise ValueError(f"supplement {paper_id} is absent from {run_dir}/candidate-registry.json")
            ranked.append(
                {
                    "paper_id": paper_id,
                    "title": candidate.get("title", ""),
                    "published": candidate.get("published", ""),
                    "cited_by_articles": False,
                    "event_count": 0,
                    "stances": [],
                    "event_ids": [],
                    "score": 1,
                    "selection_reason": "readable candidate backfill",
                    "extraction": extraction_state(extraction_dir, paper_id),
                }
            )
    if require_readable:
        ranked = [
            item
            for item in ranked
            if item["extraction"].get("complete_full_text") and item["extraction"].get("eligible")
        ]
    ranked.sort(key=lambda item: (-int(item["score"]), str(item["published"]), str(item["paper_id"])))
    target = min(len(ranked), max(floor, len(cited)))
    selected = ranked[:target]
    return {
        "run": manifest.get("run", run_dir.name),
        "source_dir": str(run_dir),
        "topic": manifest.get("topic", ""),
        "review_mode": manifest.get("review_mode", "scoping"),
        "knowledge_ids": manifest.get("knowledge_ids", []),
        "time_range": manifest.get("time_range", ""),
        "available_paper_count": len(ranked),
        "article_cited_paper_count": len(cited),
        "selected_paper_count": len(selected),
        "paper_floor_met": len(selected) >= floor,
        "selected_papers": selected,
    }


def build_plan(
    root: Path,
    pattern: str,
    floor: int,
    extraction_dir: Path | None,
    require_readable: bool,
    supplements: dict[str, list[str]],
) -> dict[str, Any]:
    runs = [
        plan_run(path, floor, extraction_dir, require_readable, supplements)
        for path in sorted(root.glob(pattern))
        if (path / "run.json").is_file() and (path / "evidence.jsonl").is_file()
    ]
    union: dict[str, dict[str, Any]] = {}
    for run in runs:
        for paper in run["selected_papers"]:
            paper_id = str(paper["paper_id"])
            record = union.setdefault(
                paper_id,
                {
                    "paper_id": paper_id,
                    "title": paper["title"],
                    "runs": [],
                    "extraction": paper["extraction"],
                },
            )
            record["runs"].append(run["run"])
    union_papers = [union[key] for key in sorted(union)]
    return {
        "schema_version": 1,
        "paper_floor_per_run": floor,
        "run_count": len(runs),
        "selected_instances": sum(int(run["selected_paper_count"]) for run in runs),
        "unique_selected_paper_count": len(union_papers),
        "unique_with_existing_extraction": sum(bool(item["extraction"].get("exists")) for item in union_papers),
        "unique_with_complete_full_text": sum(bool(item["extraction"].get("complete_full_text")) for item in union_papers),
        "require_readable": require_readable,
        "runs_below_floor": [run["run"] for run in runs if not run["paper_floor_met"]],
        "runs": runs,
        "union_papers": union_papers,
    }


def main() -> int:
    args = parse_args()
    extraction_dir = Path(args.extraction_dir) if args.extraction_dir else None
    supplements = load_supplements(Path(args.supplement_file) if args.supplement_file else None)
    result = build_plan(
        Path(args.runs_root),
        args.run_pattern,
        max(1, args.paper_floor),
        extraction_dir,
        args.require_readable,
        supplements,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ids = Path(args.paper_id_output)
    ids.parent.mkdir(parents=True, exist_ok=True)
    ids.write_text("\n".join(item["paper_id"] for item in result["union_papers"]) + "\n", encoding="utf-8")
    print(
        f"Planned {result['run_count']} runs, {result['selected_instances']} paper instances, "
        f"{result['unique_selected_paper_count']} unique papers."
    )
    return 0 if result["run_count"] and not result["runs_below_floor"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

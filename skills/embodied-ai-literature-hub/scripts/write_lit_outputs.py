#!/usr/bin/env python3
"""Validate evidence JSONL and optionally render a compact Markdown brief."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path

REQUIRED = {
    "event_id",
    "topic_id",
    "topic",
    "paper",
    "authors",
    "claim",
    "stance",
    "evidence",
    "confidence",
}
STANCES = {"support", "limit", "conditional", "gap"}
CONFIDENCE = {"direct", "citation-supported", "inference"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", required=True)
    parser.add_argument("--brief-out")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def load_events(path: Path) -> list[dict[str, object]]:
    events = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            missing = sorted(REQUIRED - set(event))
            if missing:
                raise SystemExit(f"{path}:{line_no}: missing required fields: {', '.join(missing)}")
            if event.get("stance") not in STANCES:
                raise SystemExit(f"{path}:{line_no}: invalid stance {event.get('stance')!r}")
            if event.get("confidence") not in CONFIDENCE:
                raise SystemExit(f"{path}:{line_no}: invalid confidence {event.get('confidence')!r}")
            evidence = event.get("evidence")
            if not isinstance(evidence, dict) or not evidence.get("locator"):
                raise SystemExit(f"{path}:{line_no}: evidence.locator is required")
            paper = event.get("paper")
            if not isinstance(paper, dict) or not paper.get("arxiv_id") or not paper.get("title"):
                raise SystemExit(f"{path}:{line_no}: paper.arxiv_id and paper.title are required")
            events.append(event)
    return events


def render_brief(events: list[dict[str, object]]) -> str:
    by_stance = collections.Counter(str(event["stance"]) for event in events)
    by_topic = collections.defaultdict(list)
    for event in events:
        by_topic[str(event["topic_id"])].append(event)
    lines = [
        "# Literature Evidence Brief",
        "",
        f"- Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        f"- Evidence events: {len(events)}",
        f"- Stance counts: {dict(sorted(by_stance.items()))}",
        "",
        "## Claim Map",
        "",
        "| Topic | Stance | Claim | Evidence | Paper | Authors |",
        "|---|---|---|---|---|---|",
    ]
    for event in events:
        paper = event["paper"]
        evidence = event["evidence"]
        authors = ", ".join(author.get("author_key", author.get("name", "")) for author in event.get("authors", []))
        lines.append(
            "| {topic} | {stance} | {claim} | {evidence} ({locator}) | {paper} | {authors} |".format(
                topic=event["topic_id"],
                stance=event["stance"],
                claim=str(event["claim"]).replace("|", "/"),
                evidence=str(evidence.get("summary", "")).replace("|", "/"),
                locator=str(evidence.get("locator", "")).replace("|", "/"),
                paper=str(paper.get("title", "")).replace("|", "/"),
                authors=authors.replace("|", "/"),
            )
        )
    lines.extend(["", "## Topic Card Update Suggestions", "", "- Add only high-signal synthesis with source IDs; keep raw evidence in JSONL."])
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    events = load_events(Path(args.evidence_jsonl))
    result = {"valid": True, "event_count": len(events)}
    if args.brief_out and not args.validate_only:
        Path(args.brief_out).write_text(render_brief(events), encoding="utf-8")
        result["brief_out"] = args.brief_out
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

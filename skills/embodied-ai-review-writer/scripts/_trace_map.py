#!/usr/bin/env python3
"""Map reader-facing arXiv citations in review articles to accepted evidence events."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ARXIV_LINK_RE = re.compile(r"https?://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?")


def event_anchor(event_id: str) -> str:
    return re.sub(r"[^0-9a-z一-鿿-]", "", event_id.lower().replace(" ", "-"))


def load_evidence(paths: list[Path]) -> dict[str, dict[str, Any]]:
    papers: dict[str, dict[str, Any]] = {}
    seen_events: set[str] = set()
    for path in paths:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSONL: {exc}") from exc
            event_id = str(event.get("event_id") or "")
            if not event_id or event_id in seen_events:
                continue
            seen_events.add(event_id)
            paper = event.get("paper") or {}
            if not isinstance(paper, dict):
                continue
            arxiv_id = re.sub(r"v\d+$", "", str(paper.get("arxiv_id") or "").strip())
            if not arxiv_id:
                continue
            record = papers.setdefault(
                arxiv_id,
                {
                    "arxiv_id": arxiv_id,
                    "title": str(paper.get("title") or ""),
                    "url": f"https://arxiv.org/abs/{arxiv_id}",
                    "event_ids": [],
                    "event_anchors": [],
                },
            )
            record["event_ids"].append(event_id)
            record["event_anchors"].append(f"evidence-appendix.md#{event_anchor(event_id)}")
    return papers


def article_record(path: Path, papers: dict[str, dict[str, Any]]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    cited_ids = sorted(set(ARXIV_LINK_RE.findall(text)))
    return {
        "path": str(path),
        "cited_papers": [papers[item] for item in cited_ids if item in papers],
        "uncovered_papers": [item for item in cited_ids if item not in papers],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", action="append", required=True, help="Accepted evidence JSONL; repeatable.")
    parser.add_argument("--article", action="append", required=True, help="Reader-facing article Markdown; repeatable.")
    parser.add_argument("--output", required=True, help="Output trace-map.json path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evidence_paths = [Path(item) for item in args.evidence_jsonl]
    article_paths = [Path(item) for item in args.article]
    for path in evidence_paths + article_paths:
        if not path.is_file():
            raise SystemExit(f"missing input: {path}")
    papers = load_evidence(evidence_paths)
    articles = [article_record(path, papers) for path in article_paths]
    result = {
        "version": 1,
        "evidence_files": [str(path) for path in evidence_paths],
        "articles": articles,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    uncovered = [(item["path"], paper) for item in articles for paper in item["uncovered_papers"]]
    if uncovered:
        for path, paper in uncovered:
            print(f"UNCOVERED {path}: {paper}")
        return 1
    print(f"wrote trace map: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit review articles against their evidence appendix and loaded evidence set.

Checks four failure classes seen in real runs:
1. Dead anchors — event links whose target file or `### <event_id>` heading
   does not exist (e.g. links into an invented `review-bundle/` path).
2. Out-of-set citations — event IDs cited in an article that are not present
   in the loaded evidence JSONL set (e.g. citing 54 events while only 6 were
   settled into the run folder).
3. Uncovered paper links — arxiv.org/abs links in an article whose paper has
   no event in the loaded evidence set (body citations are paper links under
   the citation contract, so paper-level coverage is what readers rely on).
4. Manifest drift — run.json listing missing files, or an `event_count` that
   does not match the deduplicated loaded evidence.

Exit code is non-zero when any problem is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EVENT_ID_RE = re.compile(r"\b(?:EA|ERR)-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{4}\b")
EVENT_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)#\s]*)#([^)\s]+)\)")
ARXIV_LINK_RE = re.compile(r"\(https?://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--article", action="append", default=[], help="Article Markdown file. Repeatable.")
    parser.add_argument("--appendix", help="evidence-appendix.md the articles link into.")
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Evidence JSONL the articles may cite. Repeatable.")
    parser.add_argument("--run-json", help="Optional run.json manifest to cross-check.")
    return parser.parse_args()


def anchor_for(event_id: str) -> str:
    """GitHub-style anchor of an `### <event_id>` heading (mirrors build_review_packet.event_anchor)."""
    return re.sub(r"[^0-9a-z一-鿿-]", "", event_id.lower().replace(" ", "-"))


def load_event_ids(paths: list[Path]) -> tuple[set[str], set[str], list[str]]:
    """Return (event IDs, paper arXiv IDs, problems) from the loaded evidence set."""
    ids: set[str] = set()
    paper_ids: set[str] = set()
    problems: list[str] = []
    for path in paths:
        if not path.is_file():
            problems.append(f"evidence file missing: {path}")
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"{path}:{lineno}: invalid JSONL line")
                continue
            event_id = str(event.get("event_id") or "")
            if event_id:
                ids.add(event_id)
            paper = event.get("paper") or {}
            if isinstance(paper, dict):
                arxiv_id = re.sub(r"v\d+$", "", str(paper.get("arxiv_id") or "").strip())
                if arxiv_id:
                    paper_ids.add(arxiv_id)
    return ids, paper_ids, problems


def appendix_anchors(appendix: Path) -> tuple[set[str], list[str]]:
    if not appendix.is_file():
        return set(), [f"appendix missing: {appendix}"]
    anchors = {
        anchor_for(match.group(1))
        for match in re.finditer(r"^###\s+(.+)$", appendix.read_text(encoding="utf-8"), flags=re.MULTILINE)
    }
    return anchors, []


def audit_article(
    article: Path,
    appendix: Path | None,
    anchors: set[str],
    evidence_ids: set[str],
    paper_ids: set[str] | None = None,
) -> list[str]:
    problems: list[str] = []
    if not article.is_file():
        return [f"article missing: {article}"]
    text = article.read_text(encoding="utf-8")
    rel = article.name

    cited_ids = set(EVENT_ID_RE.findall(text))
    linked_ids: set[str] = set()
    for match in EVENT_LINK_RE.finditer(text):
        label, target_file, anchor = match.groups()
        label_ids = EVENT_ID_RE.findall(label)
        if not label_ids:
            continue
        linked_ids.update(label_ids)
        # The link must point at the real appendix next to the article, and the anchor must exist.
        if appendix is not None:
            expected = {appendix.name}
            if target_file and target_file not in expected:
                problems.append(f"{rel}: event link points at `{target_file}` instead of {appendix.name}: [{label}]")
                continue
            resolved = article.parent / (target_file or appendix.name)
            if not resolved.is_file():
                problems.append(f"{rel}: linked appendix file missing: {target_file or appendix.name}")
                continue
        if anchors and anchor not in anchors:
            problems.append(f"{rel}: dead anchor #{anchor} for [{label}]")

    if evidence_ids:
        for event_id in sorted(cited_ids - evidence_ids):
            problems.append(f"{rel}: cites event outside loaded evidence set: {event_id}")

    if paper_ids:
        linked_papers = {match.group(1) for match in ARXIV_LINK_RE.finditer(text)}
        for arxiv_id in sorted(linked_papers - paper_ids):
            problems.append(f"{rel}: links paper with no event in loaded evidence set: {arxiv_id}")

    for event_id in sorted(cited_ids - linked_ids):
        # Bare (unlinked) event IDs violate the citation/link contract in formal outputs.
        problems.append(f"{rel}: bare event ID (not linked to appendix): {event_id}")
    return problems


def audit_run_json(run_json: Path, evidence_ids: set[str]) -> list[str]:
    problems: list[str] = []
    if not run_json.is_file():
        return [f"run.json missing: {run_json}"]
    try:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{run_json}: invalid JSON ({exc})"]
    run_dir = run_json.parent
    files = manifest.get("files", {})
    listed: list[str] = []
    for value in files.values():
        if isinstance(value, str):
            listed.append(value)
        elif isinstance(value, list):
            listed.extend(item for item in value if isinstance(item, str))
    for name in listed:
        if not (run_dir / name).is_file():
            problems.append(f"run.json lists missing file: {name}")
    recorded = manifest.get("event_count")
    if isinstance(recorded, int) and evidence_ids and recorded != len(evidence_ids):
        problems.append(
            f"run.json event_count={recorded} but loaded evidence has {len(evidence_ids)} deduplicated events"
        )
    return problems


def main() -> int:
    args = parse_args()
    evidence_ids, paper_ids, problems = load_event_ids([Path(path) for path in args.evidence_jsonl])
    appendix = Path(args.appendix) if args.appendix else None
    anchors: set[str] = set()
    if appendix is not None:
        anchors, appendix_problems = appendix_anchors(appendix)
        problems.extend(appendix_problems)
    for article in [Path(path) for path in args.article]:
        problems.extend(audit_article(article, appendix, anchors, evidence_ids, paper_ids))
    if args.run_json:
        problems.extend(audit_run_json(Path(args.run_json), evidence_ids))
    if problems:
        print(f"{len(problems)} problem(s):")
        for item in problems:
            print(f"- {item}")
        return 1
    print("citation audit OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

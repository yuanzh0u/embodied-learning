#!/usr/bin/env python3
"""Validate evidence JSONL and optionally render a compact Markdown brief."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
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
EXTRACTION_METHODS = {"html-latexml", "html-flat", "pdf-text", "pdf-ocr"}
EXTRACTION_QUALITY = {"high", "medium"}

PRIMARY_INSTITUTION_RULES = (
    (("北京大学",), "北京大学", "peking-university"),
    (("peking university",), "Peking University", "peking-university"),
    (("google deepmind", "google research", "google"), "Google", "google"),
    (("stanford ai lab", "stanford university", "stanford"), "Stanford University", "stanford-university"),
    (("mit csail", "massachusetts institute of technology", "mit"), "MIT", "mit"),
)
SUBUNIT_PREFIXES = ("department", "school", "college", "laboratory", "lab", "center", "centre", "institute")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-jsonl", required=True)
    parser.add_argument("--brief-out")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def institution_key(name: str) -> str:
    ascii_name = name.encode("ascii", errors="ignore").decode("ascii")
    if ascii_name.strip():
        key = re.sub(r"[^0-9A-Za-z]+", "-", ascii_name.strip().lower()).strip("-")
    else:
        key = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", name.strip().lower()).strip("-")
    return key or "unknown-institution"


def institution_rule_matches(name: str, folded_name: str, needle: str) -> bool:
    if re.search(r"[\u4e00-\u9fff]", needle):
        return needle in name
    if " " in needle:
        return needle in folded_name
    return re.search(rf"\b{re.escape(needle)}\b", folded_name) is not None


def normalize_primary_institution(raw_name: object) -> tuple[str, str]:
    name = " ".join(str(raw_name).replace("\xa0", " ").split())
    if not name:
        return "", ""
    folded = name.casefold()
    for needles, canonical_name, canonical_key in PRIMARY_INSTITUTION_RULES:
        if any(institution_rule_matches(name, folded, needle) for needle in needles):
            return canonical_name, canonical_key

    chinese_university = re.search(r"([\u4e00-\u9fff]+?大学)", name)
    if chinese_university:
        primary = chinese_university.group(1)
        return primary, institution_key(primary)

    parts = [part.strip() for part in re.split(r"\s*(?:,|;|\|| - )\s*", name) if part.strip()]
    primary = parts[0] if parts else name
    if primary.casefold().startswith(SUBUNIT_PREFIXES) and len(parts) > 1:
        primary = parts[1]
    primary = re.sub(r"^(Department|School|College|Laboratory|Lab) of .+?\bat\s+", "", primary, flags=re.IGNORECASE)
    return primary or name, institution_key(primary or name)


def normalize_institution_entry(institution: object, *, line_ref: str) -> dict[str, object]:
    if not isinstance(institution, dict):
        raise SystemExit(f"{line_ref}: author.institutions entries must be objects")
    name = institution.get("name")
    if not name:
        raise SystemExit(f"{line_ref}: author.institutions[].name is required")
    canonical_name, canonical_key = normalize_primary_institution(name)
    normalized = dict(institution)
    normalized["name"] = canonical_name
    normalized["institution_key"] = canonical_key
    return normalized


def normalize_author(author: object, *, line_ref: str) -> dict[str, object]:
    if not isinstance(author, dict):
        raise SystemExit(f"{line_ref}: authors entries must be objects")
    if not author.get("name") and not author.get("author_key"):
        raise SystemExit(f"{line_ref}: authors[].name or authors[].author_key is required")
    institutions = author.get("institutions", [])
    if institutions is None:
        institutions = []
    if not isinstance(institutions, list):
        raise SystemExit(f"{line_ref}: authors[].institutions must be a list")
    normalized = dict(author)
    normalized["institutions"] = [
        normalize_institution_entry(institution, line_ref=line_ref) for institution in institutions
    ]
    return normalized


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
            extraction = evidence.get("extraction")
            if extraction is not None:
                if not isinstance(extraction, dict):
                    raise SystemExit(f"{path}:{line_no}: evidence.extraction must be an object")
                method = extraction.get("method")
                quality = extraction.get("quality")
                visual_validation = extraction.get("visual_validation")
                if method not in EXTRACTION_METHODS:
                    raise SystemExit(f"{path}:{line_no}: invalid evidence.extraction.method {method!r}")
                if quality not in EXTRACTION_QUALITY:
                    raise SystemExit(
                        f"{path}:{line_no}: extraction quality {quality!r} cannot support accepted full-text evidence"
                    )
                if visual_validation not in {"not-required", "passed"}:
                    raise SystemExit(
                        f"{path}:{line_no}: OCR/medium-quality extraction requires visual validation before settlement"
                    )
            paper = event.get("paper")
            if not isinstance(paper, dict) or not paper.get("arxiv_id") or not paper.get("title"):
                raise SystemExit(f"{path}:{line_no}: paper.arxiv_id and paper.title are required")
            authors = event.get("authors")
            if not isinstance(authors, list) or not authors:
                raise SystemExit(f"{path}:{line_no}: authors must be a non-empty list")
            event["authors"] = [normalize_author(author, line_ref=f"{path}:{line_no}") for author in authors]
            events.append(event)
    return events


def format_institutions(author: dict[str, object]) -> str:
    institutions = author.get("institutions", [])
    if not isinstance(institutions, list) or not institutions:
        return "unlisted"
    names = []
    for institution in institutions:
        if isinstance(institution, dict) and institution.get("name"):
            names.append(str(institution["name"]))
    return "; ".join(dict.fromkeys(names)) if names else "unlisted"


def format_authors(authors: object) -> str:
    if not isinstance(authors, list):
        return ""
    formatted = []
    for author in authors:
        if not isinstance(author, dict):
            continue
        author_label = author.get("author_key", author.get("name", ""))
        institutions = format_institutions(author)
        formatted.append(f"{author_label} [{institutions}]")
    return ", ".join(str(item) for item in formatted)


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
        authors = format_authors(event.get("authors", []))
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
    lines.extend(
        [
            "",
            "## Author Stance Events",
            "",
            "| Author key | Institutions | Paper | Date | Claim | Stance |",
            "|---|---|---|---|---|---|",
        ]
    )
    for event in events:
        paper = event["paper"]
        for author in event.get("authors", []):
            if not isinstance(author, dict):
                continue
            lines.append(
                "| {author} | {institutions} | {paper} | {date} | {claim} | {stance} |".format(
                    author=str(author.get("author_key", author.get("name", ""))).replace("|", "/"),
                    institutions=format_institutions(author).replace("|", "/"),
                    paper=str(paper.get("title", "")).replace("|", "/"),
                    date=str(paper.get("published", "")).replace("|", "/"),
                    claim=str(event["claim"]).replace("|", "/"),
                    stance=str(event["stance"]).replace("|", "/"),
                )
            )
    lines.extend(
        [
            "",
            "## Topic Card Update Suggestions",
            "",
            "- Add only high-signal synthesis with source IDs; keep raw evidence in JSONL.",
            "- Treat this as a candidate update list, not an automatic topic-card patch.",
        ]
    )
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

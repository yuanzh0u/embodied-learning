#!/usr/bin/env python3
"""Extract local reference context for persona generation.

Collects topic-card key judgments and related literature-review runs from the
knowledge base, producing the deterministic reference context that an
LLM/agent uses to generate a persona file (see references/persona-expansion.md).
Pure Python: no LLM calls, no network, no timestamps, so the same inputs always
produce byte-identical output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CARDS_DIR = ROOT / "knowledge" / "embodied-ai"
CATALOG = ROOT / "knowledge" / "literature-review-catalog.md"

JUDGMENT_HEADING = "## 关键判断"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Chinese or English embodied-AI topic.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="EA knowledge ID (e.g. EA-SENSOR). May be repeated.")
    parser.add_argument("--max-judgments", type=int, default=8, help="Max key judgments per topic card.")
    parser.add_argument("--max-runs", type=int, default=6, help="Max related runs to report.")
    parser.add_argument("--output", help="Write JSON context to this path instead of stdout.")
    return parser.parse_args()


def parse_inline_list(raw: str) -> list[str]:
    inner = raw.strip().strip("[]")
    if not inner:
        return []
    return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    frontmatter: dict[str, Any] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("["):
            frontmatter[key] = parse_inline_list(value)
        elif value:
            frontmatter[key] = value
    return frontmatter


def extract_key_judgments(text: str, limit: int) -> list[str]:
    lines = text.splitlines()
    judgments: list[str] = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            in_section = stripped == JUDGMENT_HEADING
            continue
        if in_section and stripped.startswith("- "):
            judgments.append(stripped[2:].strip())
    return judgments[:limit]


def load_topic_cards() -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    if not CARDS_DIR.is_dir():
        return cards
    for path in sorted(CARDS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if not frontmatter.get("id"):
            continue
        cards.append(
            {
                "id": str(frontmatter["id"]),
                "title": str(frontmatter.get("title", "")),
                "aliases": [str(item) for item in frontmatter.get("aliases", [])],
                "tags": [str(item) for item in frontmatter.get("tags", [])],
                "file": path.relative_to(ROOT).as_posix(),
                "text": text,
            }
        )
    return cards


def match_cards(
    topic: str,
    requested_ids: list[str],
    cards: list[dict[str, Any]],
    max_judgments: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    notes: list[str] = []
    matched: list[dict[str, Any]] = []
    requested = [item.strip().upper() for item in requested_ids if item.strip()]

    for card in cards:
        matched_by = ""
        if card["id"].upper() in requested:
            matched_by = "knowledge-id"
        else:
            for term in [card["title"], *card["aliases"]]:
                if term and term in topic:
                    matched_by = f"alias:{term}"
                    break
            if not matched_by:
                topic_lower = topic.lower()
                for tag in card["tags"]:
                    if tag and tag.lower() in topic_lower:
                        matched_by = f"tag:{tag}"
                        break
        if not matched_by:
            continue
        judgments = extract_key_judgments(card["text"], max_judgments)
        if not judgments:
            notes.append(f"Topic card {card['id']} matched but exposes no key judgments; skipped.")
            continue
        matched.append(
            {
                "id": card["id"],
                "title": card["title"],
                "file": card["file"],
                "matched_by": matched_by,
                "aliases": card["aliases"],
                "key_judgments": judgments,
            }
        )

    missing = [item for item in requested if item not in {card["id"].upper() for card in matched}]
    for item in missing:
        notes.append(f"Requested knowledge id {item} has no topic card with key judgments; ignored.")

    if requested and not matched:
        notes.append("No requested knowledge id matched; fell back to nothing. Pass a topic containing known aliases or valid EA ids.")
    if not requested and not matched:
        notes.append("No topic card matched by alias/tag; add --knowledge-id or rephrase the topic.")
    return matched, notes


def parse_catalog_runs() -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    if not CATALOG.is_file():
        return runs
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("| LR-"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        run_id, run_topic, run_cards, scale = cells[0], cells[1], cells[2], cells[3]
        knowledge_ids = [item.strip() for item in run_cards.split(",") if item.strip()]
        runs.append(
            {
                "id": run_id,
                "topic": run_topic,
                "knowledge_ids": knowledge_ids,
                "scale": scale,
            }
        )
    return runs


def match_runs(
    matched_cards: list[dict[str, Any]],
    requested_ids: list[str],
    topic: str,
    runs: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    requested = {item.strip().upper() for item in requested_ids if item.strip()}
    card_ids = {card["id"] for card in matched_cards}
    referenced = requested | card_ids
    card_aliases = [alias for card in matched_cards for alias in card.get("aliases", [])]

    scored: list[tuple[int, str, dict[str, Any]]] = []
    for run in runs:
        overlap = len(referenced & set(run["knowledge_ids"]))
        alias_bonus = 1 if any(alias and alias in run["topic"] for alias in card_aliases) else 0
        score = overlap * 2 + alias_bonus
        if score:
            scored.append((score, run["id"], run))

    scored.sort(key=lambda triple: (-triple[0], triple[1]))
    return [
        {
            "id": run["id"],
            "topic": run["topic"],
            "knowledge_ids": run["knowledge_ids"],
            "scale": run["scale"],
        }
        for _, _, run in scored[:limit]
    ]


def build_context(args: argparse.Namespace) -> dict[str, Any]:
    cards = load_topic_cards()
    matched, notes = match_cards(args.topic, args.knowledge_id, cards, args.max_judgments)
    runs = parse_catalog_runs()
    related = match_runs(matched, args.knowledge_id, args.topic, runs, args.max_runs)
    return {
        "topic": args.topic,
        "topic_cards": matched,
        "related_runs": related,
        "notes": notes,
    }


def main() -> int:
    args = parse_args()
    context = build_context(args)
    rendered = json.dumps(context, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())

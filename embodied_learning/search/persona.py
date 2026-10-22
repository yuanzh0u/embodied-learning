"""Extract local reference context for persona generation.

Collects topic-card key judgments and related literature-review runs from the
knowledge base, producing the deterministic reference context that an
LLM/agent uses to generate a persona file (see references/persona-expansion.md).
Pure Python: no LLM calls, no network, no timestamps, so the same inputs always
produce byte-identical output.
"""

from __future__ import annotations

import argparse
import re
import json
from pathlib import Path
import sys
from typing import Any

from embodied_learning.utils.layout import find_roots

ROOT = find_roots()[0] or Path.cwd()
CARDS_DIR = ROOT / "knowledge" / "embodied-ai"
CATALOG = ROOT / "knowledge" / "literature-review-catalog.md"

from embodied_learning.utils.frontmatter import (  # noqa: E402
    parse_frontmatter,
    parse_inline_list,
)

JUDGMENT_HEADING = "## 关键判断"


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


def topic_tokens(text: str) -> set[str]:
    """Extract overlap tokens from a free-form topic string.

    Latin words of length >= 2 are kept lowercased. Continuous CJK runs
    contribute character bigrams so Chinese queries without spaces still
    produce useful keyword overlap against catalog run topics.
    """
    tokens: set[str] = set()
    for part in re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]+", text.lower()):
        if re.fullmatch(r"[a-z0-9]+", part):
            if len(part) >= 2:
                tokens.add(part)
            continue
        for index in range(len(part) - 1):
            tokens.add(part[index : index + 2])
    return tokens


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

    query_tokens = topic_tokens(topic)
    scored: list[tuple[int, str, dict[str, Any]]] = []
    for run in runs:
        overlap = len(referenced & set(run["knowledge_ids"]))
        alias_bonus = 1 if any(alias and alias in run["topic"] for alias in card_aliases) else 0
        topic_overlap = len(query_tokens & topic_tokens(run["topic"]))
        score = overlap * 2 + alias_bonus + topic_overlap
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


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in the dispatcher."""
    context = build_context(args)
    rendered = json.dumps(context, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0

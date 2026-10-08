#!/usr/bin/env python3
"""Project short evidence cards for outline-first writing (token-opt medium).

After the first LLM call produces a writing outline (central thesis + selected
8–12 ``event_id``s), this script pulls only those events from ``evidence.jsonl``
into compact cards. Downstream genre drafts should load these projected cards —
not the full brief thrice.

Compatible with stance-capped ``writing-brief.md`` surfaces when present: the
outline still picks from the reservoir; this projector only materializes the
chosen IDs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_MAX_CLAIM = 400
DEFAULT_MAX_SUMMARY = 320
DEFAULT_MAX_QUOTE = 220


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--outline",
        required=True,
        help="Outline JSON with thesis + event_ids (see schema in docs)",
    )
    parser.add_argument(
        "--evidence-jsonl",
        action="append",
        required=True,
        help="Accepted evidence JSONL; repeatable",
    )
    parser.add_argument("--output", required=True, help="Projected cards JSON")
    parser.add_argument("--markdown-output", help="Optional short markdown for LLM prompts")
    parser.add_argument("--max-claim-chars", type=int, default=DEFAULT_MAX_CLAIM)
    parser.add_argument("--max-summary-chars", type=int, default=DEFAULT_MAX_SUMMARY)
    parser.add_argument("--max-quote-chars", type=int, default=DEFAULT_MAX_QUOTE)
    return parser.parse_args()


def load_outline(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("outline must be a JSON object")
    event_ids = value.get("event_ids") or value.get("selected_event_ids")
    if not isinstance(event_ids, list) or not event_ids:
        raise ValueError("outline.event_ids must be a non-empty list")
    cleaned = [str(item).strip() for item in event_ids if str(item).strip()]
    if not cleaned:
        raise ValueError("outline.event_ids produced no usable IDs")
    if len(cleaned) < 8 or len(cleaned) > 12:
        # Soft guidance only — still project, but record a warning.
        pass
    value = dict(value)
    value["event_ids"] = cleaned
    return value


def load_events(paths: list[str]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for raw in paths:
        path = Path(raw)
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL") from exc
            if not isinstance(event, dict) or not event.get("event_id"):
                raise ValueError(f"{path}:{line_no}: expected object with event_id")
            by_id[str(event["event_id"])] = event
    return by_id


def clip(text: Any, limit: int) -> str:
    value = " ".join(str(text or "").split())
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 1)].rstrip() + "…"


def project_card(
    event: dict[str, Any],
    *,
    max_claim: int,
    max_summary: int,
    max_quote: int,
) -> dict[str, Any]:
    evidence = event.get("evidence") if isinstance(event.get("evidence"), dict) else {}
    paper = event.get("paper") if isinstance(event.get("paper"), dict) else {}
    quote = evidence.get("short_quote") or evidence.get("quote") or ""
    return {
        "event_id": event.get("event_id"),
        "stance": event.get("stance"),
        "confidence": event.get("confidence"),
        "claim": clip(event.get("claim"), max_claim),
        "summary": clip(evidence.get("summary"), max_summary),
        "locator": evidence.get("locator"),
        "short_quote": clip(quote, max_quote),
        "paper": {
            "arxiv_id": paper.get("arxiv_id"),
            "title": clip(paper.get("title"), 160),
            "url": paper.get("url"),
        },
        "topic_id": event.get("topic_id"),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Outline-projected evidence cards",
        "",
        f"**Thesis:** {payload.get('thesis') or '(missing)'}",
        "",
    ]
    if payload.get("claim_clusters"):
        lines.append("## Claim clusters")
        lines.append("")
        for cluster in payload["claim_clusters"]:
            lines.append(f"- {cluster}")
        lines.append("")
    lines.append(f"Selected events: {len(payload.get('cards') or [])}")
    lines.append("")
    for card in payload.get("cards") or []:
        lines.append(
            f"### `{card.get('event_id')}` · {card.get('stance')} · "
            f"{(card.get('paper') or {}).get('arxiv_id')}"
        )
        lines.append("")
        lines.append(f"- Claim: {card.get('claim')}")
        if card.get("summary"):
            lines.append(f"- Summary: {card.get('summary')}")
        if card.get("locator"):
            lines.append(f"- Locator: {card.get('locator')}")
        if card.get("short_quote"):
            lines.append(f"- Quote: {card.get('short_quote')}")
        url = (card.get("paper") or {}).get("url")
        title = (card.get("paper") or {}).get("title")
        if url:
            lines.append(f"- Paper: [{title}]({url})")
        lines.append("")
    if payload.get("missing_event_ids"):
        lines.append("## Missing event IDs")
        lines.append("")
        for event_id in payload["missing_event_ids"]:
            lines.append(f"- `{event_id}`")
        lines.append("")
    lines.append(
        "_Load only these projected cards for genre drafts. Do not re-ingest the full brief thrice._"
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    try:
        outline = load_outline(Path(args.outline))
        events = load_events(args.evidence_jsonl)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    cards: list[dict[str, Any]] = []
    missing: list[str] = []
    for event_id in outline["event_ids"]:
        event = events.get(event_id)
        if not event:
            missing.append(event_id)
            continue
        cards.append(
            project_card(
                event,
                max_claim=args.max_claim_chars,
                max_summary=args.max_summary_chars,
                max_quote=args.max_quote_chars,
            )
        )

    warnings: list[str] = []
    n = len(outline["event_ids"])
    if n < 8 or n > 12:
        warnings.append(
            f"outline selected {n} event_ids; preferred band is 8–12 for token control"
        )
    if missing:
        warnings.append(f"{len(missing)} event_ids not found in evidence JSONL")

    payload = {
        "schema_version": 1,
        "thesis": outline.get("thesis") or outline.get("central_thesis") or "",
        "claim_clusters": outline.get("claim_clusters") or outline.get("clusters") or [],
        "counterevidence_notes": outline.get("counterevidence_notes") or [],
        "mandatory_caveats": outline.get("mandatory_caveats") or [],
        "event_ids": outline["event_ids"],
        "cards": cards,
        "missing_event_ids": missing,
        "warnings": warnings,
        "usage": (
            "Pass this projection (or its markdown twin) into each genre draft. "
            "Keep editorial plans independent per style; share evidence cards, not prose."
        ),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_output:
        Path(args.markdown_output).write_text(render_markdown(payload), encoding="utf-8")

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if missing:
        return 1
    print(json.dumps({"ok": True, "card_count": len(cards), "output": str(out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

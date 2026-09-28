#!/usr/bin/env python3
"""Extract locator windows for claim-support audit failures (one-shot retry aid).

Given a failing ``audit_claim_support.py`` JSON and the matching extraction,
emit only the section/page windows needed to retry the failing cards — never
re-paste the complete extracted text into the LLM.

Default window is the matched section surface, truncated around the source
context (± ``--radius`` characters) when an exact/near match exists.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "audit_claim_support", SCRIPTS_DIR / "audit_claim_support.py"
)
audit_mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(audit_mod)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", required=True, help="audit_claim_support JSON")
    parser.add_argument("--extraction", required=True, help="complete extraction JSON")
    parser.add_argument(
        "--paper-note",
        help="optional paper-note JSON (used to attach claim text to failing cards)",
    )
    parser.add_argument(
        "--radius",
        type=int,
        default=4000,
        help="chars kept around source_context inside a matched surface (default 4000)",
    )
    parser.add_argument(
        "--max-window",
        type=int,
        default=8000,
        help="hard cap per card window in characters (default 8000)",
    )
    parser.add_argument("--output", help="write JSON; default stdout")
    parser.add_argument(
        "--markdown-output",
        help="optional human-readable markdown for the LLM retry prompt",
    )
    return parser.parse_args()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def window_around(surface: str, needle: str, radius: int, max_window: int) -> str:
    if not surface:
        return ""
    norm_surface = audit_mod.normalize(surface)
    norm_needle = audit_mod.normalize(needle)
    if needle and needle in surface:
        idx = surface.index(needle)
        start = max(0, idx - radius)
        end = min(len(surface), idx + len(needle) + radius)
        chunk = surface[start:end]
    elif norm_needle and norm_needle in norm_surface:
        # Approximate via raw length ratio when only normalized match exists.
        ratio = len(surface) / max(1, len(norm_surface))
        approx = int(norm_surface.index(norm_needle) * ratio)
        start = max(0, approx - radius)
        end = min(len(surface), approx + len(needle or "") + radius)
        chunk = surface[start:end]
    else:
        chunk = surface[:max_window]
    if len(chunk) > max_window:
        half = max_window // 2
        chunk = chunk[:half] + "\n…\n" + chunk[-half:]
    return chunk


def build_windows(
    audit: dict[str, Any],
    extraction: dict[str, Any],
    note: dict[str, Any] | None,
    radius: int,
    max_window: int,
) -> dict[str, Any]:
    full_text, by_page = audit_mod.extraction_text(extraction)
    cards_by_id: dict[str, dict[str, Any]] = {}
    if note:
        for card in note.get("evidence_cards") or []:
            if isinstance(card, dict) and card.get("card_id"):
                cards_by_id[str(card["card_id"])] = card

    failing: list[dict[str, Any]] = []
    for item in audit.get("cards") or []:
        if not isinstance(item, dict):
            continue
        if str(item.get("status") or "") == "pass":
            continue
        card_id = str(item.get("card_id") or "")
        locator = str(item.get("locator") or "")
        note_card = cards_by_id.get(card_id) or {}
        context = str(note_card.get("source_context") or item.get("source_context") or "")

        surfaces = audit_mod.section_surfaces(locator, full_text, extraction)
        if not surfaces and by_page:
            # Fall back: page locator or whole text.
            import re

            page_match = re.search(r"\bpage\s+(\d+)\b|第\s*(\d+)\s*页", locator, re.I)
            if page_match:
                number = int(page_match.group(1) or page_match.group(2))
                surfaces = [by_page.get(number, "")]
        if not surfaces:
            surfaces = [full_text]

        windows = [
            window_around(surface, context, radius=radius, max_window=max_window)
            for surface in surfaces
        ]
        failing.append(
            {
                "card_id": card_id,
                "locator": locator,
                "claim": note_card.get("claim") or item.get("claim"),
                "reasons": item.get("reasons") or ([item.get("reason")] if item.get("reason") else []),
                "audit_status": item.get("status"),
                "window_chars": sum(len(w) for w in windows),
                "windows": windows,
            }
        )

    return {
        "schema_version": 1,
        "paper_id": str(audit.get("paper_id") or extraction.get("paper_id") or ""),
        "audit_status": audit.get("status"),
        "failed_card_count": len(failing),
        "cards": failing,
        "note": (
            "Retry only these failing cards with the attached windows. "
            "Do not re-read the complete extracted text."
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Failed-card retry windows — {payload.get('paper_id') or 'unknown'}",
        "",
        f"Audit status: `{payload.get('audit_status')}` · "
        f"failing cards: **{payload.get('failed_card_count', 0)}**",
        "",
        str(payload.get("note") or ""),
        "",
    ]
    for card in payload.get("cards") or []:
        lines.append(f"## Card `{card.get('card_id')}`")
        lines.append("")
        lines.append(f"- Locator: `{card.get('locator')}`")
        if card.get("claim"):
            lines.append(f"- Claim: {card['claim']}")
        reasons = card.get("reasons") or []
        if reasons:
            lines.append("- Reasons:")
            for reason in reasons:
                if reason:
                    lines.append(f"  - {reason}")
        lines.append("")
        for index, window in enumerate(card.get("windows") or [], start=1):
            lines.append(f"### Window {index} ({len(window)} chars)")
            lines.append("")
            lines.append("```text")
            lines.append(window.rstrip())
            lines.append("```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    try:
        audit = load_object(Path(args.audit))
        extraction = load_object(Path(args.extraction))
        note = load_object(Path(args.paper_note)) if args.paper_note else None
        payload = build_windows(
            audit, extraction, note, radius=args.radius, max_window=args.max_window
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    if args.markdown_output:
        Path(args.markdown_output).write_text(render_markdown(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Minimal YAML-subset frontmatter parser.

One implementation of the ``--- key: value ---`` frontmatter handling that
used to be copy-pasted in visualize_kb_index / check_kb_links /
gen_persona_context / build_review_packet. Covers the union of what those
callers need:

- scalar keys (``id: EA-DATA``)
- inline lists (``tags: [a, b]`` -> ``["a", "b"]``)
- ``source:`` block lists of ``- key: value`` items (topic-card source entries)
"""

from __future__ import annotations

import re

FRONTMATTER_BOUNDS = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)


def parse_inline_list(raw: str) -> list[str]:
    inner = raw.strip().strip("[]")
    if not inner:
        return []
    return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]


def parse_frontmatter(text: str) -> dict[str, object]:
    """Parse the leading frontmatter block; ``{}`` when absent or malformed."""
    match = FRONTMATTER_BOUNDS.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    sources: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_source = False
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if not line.startswith(" "):
            in_source = line.strip() == "source:"
            current = None
            if ":" in line and not in_source:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()
                if value.startswith("["):
                    data[key] = parse_inline_list(value)
                elif value:
                    data[key] = value
            continue
        if in_source:
            stripped = line.strip()
            if stripped.startswith("- "):
                current = {}
                sources.append(current)
                stripped = stripped[2:]
            if current is not None and ":" in stripped:
                key, _, value = stripped.partition(":")
                current[key.strip()] = value.strip().strip('"')
    if sources:
        data["source"] = sources
    return data


def strip_frontmatter(text: str) -> str:
    """Return the body after a leading frontmatter block (whole text when none)."""
    match = FRONTMATTER_BOUNDS.match(text)
    if not match:
        return text
    return text[match.end():]

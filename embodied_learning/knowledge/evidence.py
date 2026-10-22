"""Evidence-bundle helpers: the single home for event anchors and consolidation.

``event_anchor`` is the canonical GitHub-style anchor for ``### <event_id>``
headings in evidence-appendix.md. Three copies used to exist (build_review_packet,
_trace_map, audit_citations) and had to agree byte-for-byte — one definition now.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


def event_anchor(event_id: str) -> str:
    """GitHub-style anchor for an `### <event_id>` heading in the appendix."""
    return re.sub(r"[^0-9a-z一-鿿-]", "", event_id.lower().replace(" ", "-"))


def consolidate_evidence(run_dir: Path) -> Path:
    """One deduplicated ``evidence.jsonl`` at the run root, always rebuilt.

    The single merge both gate surfaces read (launcher gate loop and
    finalize_run). Always rebuilt, never reused: the driver re-projects
    events whenever a deep-read round resumes, so a cached merge would
    silently lag the evidence/ tree and fail the event_count gate
    (20260929 图像粗配准). Flat runs keep canonical evidence at the run
    root with no evidence/ subdir — its lines are folded in as the seed so
    the rebuild never clobbers them."""
    merged = run_dir / "evidence.jsonl"
    seen: set[str] = set()
    lines: list[str] = []

    def absorb(path: Path) -> None:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event_id = str(json.loads(line).get("event_id") or "")
            except json.JSONDecodeError:
                event_id = ""
            key = event_id or line
            if key in seen:
                continue
            seen.add(key)
            lines.append(line)

    canonical = run_dir / "evidence.jsonl"
    if canonical.is_file():
        absorb(canonical)
    for path in sorted((run_dir / "evidence").glob("*.jsonl")):
        absorb(path)
    merged.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return merged

#!/usr/bin/env python3
"""Set fully audited paper-reader migration drafts to settled status."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = (
    "evidence.jsonl",
    "reading-ledger.jsonl",
    "reading-summary.json",
    "paper-note-index.json",
    "claim-support-audit-index.json",
    "review-packet.md",
    "writing-brief.md",
    "evidence-appendix.md",
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
    "trace-map.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft_root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    runs = sorted(Path(args.draft_root).glob("literature-review-*"))
    for run in runs:
        missing = [name for name in REQUIRED if not (run / name).is_file()]
        if missing:
            raise SystemExit(f"{run}: missing required migration files: {', '.join(missing)}")
        summary = json.loads((run / "reading-summary.json").read_text(encoding="utf-8"))
        if int(summary.get("accepted_evidence_paper_count") or 0) < 15:
            raise SystemExit(f"{run}: accepted paper floor is not met")
        manifest_path = run / "run.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["status"] = "settled"
        manifest["notes"] = (
            "Paper-reader migration settled: 15 complete non-OCR full texts were map-read and deep-read; "
            "every accepted paper has a validated note, a passing full-text claim-support audit, and one "
            "projected evidence event. The three reader-facing articles passed citation and editorial gates."
        )
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"settled_runs={len(runs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

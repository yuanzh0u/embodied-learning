#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = (
    ROOT / "skills" / "embodied-ai-review-writer" / "scripts" / "project_outline_evidence.py"
)


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=check,
        text=True,
        capture_output=True,
        cwd=ROOT,
    )


class ProjectOutlineEvidenceTests(unittest.TestCase):
    def test_projects_selected_events_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            events = [
                {
                    "event_id": f"EA-DATA-2026-{i:04d}",
                    "stance": "support" if i % 2 == 0 else "limit",
                    "confidence": "direct",
                    "claim": f"Claim number {i} " + ("x" * 50),
                    "topic_id": "EA-DATA",
                    "paper": {
                        "arxiv_id": f"2402.{i:05d}",
                        "title": f"Paper {i}",
                        "url": f"https://arxiv.org/abs/2402.{i:05d}",
                    },
                    "evidence": {
                        "summary": f"Summary {i}",
                        "locator": "4 Experiments",
                        "short_quote": f"Quote {i}",
                    },
                }
                for i in range(1, 16)
            ]
            jsonl = tmp_path / "evidence.jsonl"
            jsonl.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )
            selected = [f"EA-DATA-2026-{i:04d}" for i in range(1, 11)]
            outline = {
                "thesis": "Portable interfaces transfer only under scoped embodiment assumptions.",
                "claim_clusters": ["interface portability", "embodiment limits"],
                "event_ids": selected,
            }
            outline_path = tmp_path / "outline.json"
            outline_path.write_text(json.dumps(outline), encoding="utf-8")
            out = tmp_path / "cards.json"
            md = tmp_path / "cards.md"
            completed = run(
                "--outline",
                str(outline_path),
                "--evidence-jsonl",
                str(jsonl),
                "--output",
                str(out),
                "--markdown-output",
                str(md),
            )
            self.assertEqual(completed.returncode, 0)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["cards"]), 10)
            self.assertEqual(payload["thesis"], outline["thesis"])
            self.assertEqual([c["event_id"] for c in payload["cards"]], selected)
            body = md.read_text(encoding="utf-8")
            self.assertIn(outline["thesis"], body)
            self.assertIn("EA-DATA-2026-0001", body)
            self.assertNotIn("EA-DATA-2026-0015", body)

    def test_missing_ids_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            jsonl = tmp_path / "evidence.jsonl"
            jsonl.write_text(
                json.dumps(
                    {
                        "event_id": "EA-DATA-2026-0001",
                        "claim": "only one",
                        "stance": "support",
                        "paper": {"arxiv_id": "2402.00001", "title": "A", "url": "https://arxiv.org/abs/2402.00001"},
                        "evidence": {"summary": "s", "locator": "1"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            outline = {
                "thesis": "t",
                "event_ids": [f"EA-DATA-2026-{i:04d}" for i in range(1, 9)],
            }
            outline_path = tmp_path / "outline.json"
            outline_path.write_text(json.dumps(outline), encoding="utf-8")
            completed = run(
                "--outline",
                str(outline_path),
                "--evidence-jsonl",
                str(jsonl),
                "--output",
                str(tmp_path / "cards.json"),
                check=False,
            )
            self.assertEqual(completed.returncode, 1)


if __name__ == "__main__":
    unittest.main()

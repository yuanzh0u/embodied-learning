#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-review-writer" / "scripts" / "build_trace_map.py"


class BuildTraceMapTests(unittest.TestCase):
    def test_maps_article_papers_to_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            evidence = root / "evidence.jsonl"
            events = [
                {
                    "event_id": "EA-DATA-2026-0001",
                    "paper": {"arxiv_id": "2603.09056", "title": "Quality over Quantity"},
                },
                {
                    "event_id": "EA-DATA-2026-0002",
                    "paper": {"arxiv_id": "2603.09056", "title": "Quality over Quantity"},
                },
            ]
            evidence.write_text("\n".join(json.dumps(item) for item in events) + "\n", encoding="utf-8")
            article = root / "memo.md"
            article.write_text("正文引用 [QoQ](https://arxiv.org/abs/2603.09056)。\n", encoding="utf-8")
            output = root / "trace-map.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--evidence-jsonl",
                    str(evidence),
                    "--article",
                    str(article),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            data = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        paper = data["articles"][0]["cited_papers"][0]
        self.assertEqual("2603.09056", paper["arxiv_id"])
        self.assertEqual(["EA-DATA-2026-0001", "EA-DATA-2026-0002"], paper["event_ids"])
        self.assertEqual([], data["articles"][0]["uncovered_papers"])

    def test_uncovered_paper_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            evidence = root / "evidence.jsonl"
            evidence.write_text(
                json.dumps({"event_id": "EA-DATA-2026-0001", "paper": {"arxiv_id": "2603.09056"}}) + "\n",
                encoding="utf-8",
            )
            article = root / "memo.md"
            article.write_text("[unknown](https://arxiv.org/abs/2607.99999)\n", encoding="utf-8")
            output = root / "trace-map.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--evidence-jsonl",
                    str(evidence),
                    "--article",
                    str(article),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("UNCOVERED", completed.stdout)


if __name__ == "__main__":
    unittest.main()

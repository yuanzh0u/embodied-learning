#!/usr/bin/env python3
"""Behavior tests for the persona reference-context extractor."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-query-planner" / "scripts" / "gen_persona_context.py"


def run_context(*args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


class GenPersonaContextTests(unittest.TestCase):
    def test_extracts_key_judgments_from_topic_card(self) -> None:
        context = run_context(
            "--topic", "近半年触觉数据联合训练的坑",
            "--knowledge-id", "EA-SENSOR",
            "--knowledge-id", "EA-DATA",
        )

        card_ids = {card["id"] for card in context["topic_cards"]}
        self.assertIn("EA-SENSOR", card_ids)
        self.assertIn("EA-DATA", card_ids)

        sensor = next(card for card in context["topic_cards"] if card["id"] == "EA-SENSOR")
        self.assertEqual("knowledge-id", sensor["matched_by"])
        self.assertTrue(sensor["key_judgments"])
        self.assertLessEqual(len(sensor["key_judgments"]), 8)
        self.assertTrue(all(isinstance(item, str) and item for item in sensor["key_judgments"]))
        self.assertTrue(sensor["file"].startswith("knowledge/embodied-ai/"))

        self.assertTrue(context["related_runs"])
        for run in context["related_runs"]:
            self.assertTrue(run["id"].startswith("LR-"))
            self.assertTrue(run["topic"])
            self.assertTrue(run["scale"])
        # A tactile-related run should surface for a tactile topic.
        self.assertIn("LR-TACTILE-YEAR", {run["id"] for run in context["related_runs"]})

    def test_unknown_id_fuzzy_fallback(self) -> None:
        context = run_context("--topic", "近半年触觉数据联合训练的坑")

        self.assertTrue(context["topic_cards"])
        sensor = next(card for card in context["topic_cards"] if card["id"] == "EA-SENSOR")
        self.assertEqual("alias:触觉", sensor["matched_by"])

        context_unknown = run_context("--topic", "完全无关的量子计算话题", "--knowledge-id", "EA-GHOST")
        self.assertEqual([], context_unknown["topic_cards"])
        self.assertTrue(any("EA-GHOST" in note for note in context_unknown["notes"]))
        self.assertTrue(any("No requested knowledge id matched" in note for note in context_unknown["notes"]))

    def test_deterministic_output(self) -> None:
        first = run_context("--topic", "近半年触觉数据联合训练的坑", "--knowledge-id", "EA-SENSOR")
        second = run_context("--topic", "近半年触觉数据联合训练的坑", "--knowledge-id", "EA-SENSOR")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

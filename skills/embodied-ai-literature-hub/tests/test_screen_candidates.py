#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("screen_candidates", ROOT / "scripts" / "screen_candidates.py")
screen_candidates = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(screen_candidates)


class ScreenCandidatesTest(unittest.TestCase):
    def test_seed_and_query_labels_prioritize_without_accepting(self) -> None:
        registry = {
            "candidates": [
                {"arxiv_id": "1", "title": "Generic Robot Paper", "summary": "", "published": "2026-01-01", "discoveries": []},
                {"arxiv_id": "2", "title": "Tactile World Model", "summary": "contact prediction", "published": "2026-02-01", "discoveries": []},
                {"arxiv_id": "3", "title": "Other", "summary": "", "published": "2026-03-01", "discoveries": [{"query_labels": ["dynamic-tactile-action-model"]}]},
            ]
        }
        selected = screen_candidates.select_candidates(
            registry, ["tactile", "contact"], ["dynamic-tactile"], {"1"}, 3
        )
        self.assertEqual(["2", "3", "1"], [item["candidate"]["arxiv_id"] for item in selected])
        self.assertTrue(selected[-1]["seeded"])
        self.assertGreater(selected[0]["score"], selected[-1]["score"])

    def test_prior_evidence_cannot_fill_a_normal_queue_when_new_candidates_match(self) -> None:
        registry = {
            "candidates": [
                {"arxiv_id": str(index), "title": "Tactile evidence", "summary": "", "discoveries": []}
                for index in range(1, 9)
            ]
        }
        selected = screen_candidates.select_candidates(
            registry, ["tactile"], [], {"1", "2", "3", "4"}, 4
        )
        self.assertEqual(1, sum(bool(item["seeded"]) for item in selected))


if __name__ == "__main__":
    unittest.main()

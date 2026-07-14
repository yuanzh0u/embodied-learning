#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


registry_module = load_script("build_candidate_registry")
coverage_module = load_script("assess_review_coverage")


class CandidateRegistryAndCoverageTest(unittest.TestCase):
    def test_registry_deduplicates_rounds_and_preserves_discovery_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            round1 = root / "round-1.json"
            round2 = root / "round-2.json"
            browser = root / "round-3.json"
            round1.write_text(
                json.dumps({"papers": [{"arxiv_id": "2601.00001", "title": "A", "query_label": "core"}]}),
                encoding="utf-8",
            )
            round2.write_text(
                json.dumps({"papers": [
                    {"arxiv_id": "2601.00001", "title": "A", "query_label": "limit"},
                    {"arxiv_id": "2601.00002", "title": "B", "query_label": "limit"},
                ]}),
                encoding="utf-8",
            )
            browser.write_text(
                json.dumps({"source_label": "browser-gap", "candidates": [
                    {"arxiv_id": "2601.00003", "context": "gap paper", "in_window": True},
                ]}),
                encoding="utf-8",
            )

            result = registry_module.build_registry([round1, round2], [browser])

        self.assertEqual(3, result["candidate_count"])
        first = next(item for item in result["candidates"] if item["arxiv_id"] == "2601.00001")
        labels = {label for discovery in first["discoveries"] for label in discovery["query_labels"]}
        self.assertEqual({"core", "limit"}, labels)
        self.assertEqual(3, len(result["batches"]))

    def test_coverage_requires_targets_dimensions_and_saturation(self) -> None:
        plan = {
            "review_mode": "rapid",
            "search_targets": {"candidate_floor": 3, "full_text_floor": 2, "accepted_paper_floor": 2},
            "coverage_dimensions": [
                {"dimension": "direct-topic", "query_labels": ["core"], "minimum_unique_candidates": 1},
                {"dimension": "limits", "query_labels": ["limit"], "minimum_unique_candidates": 1},
            ],
            "stopping_rule": {"minimum_batches": 3, "saturation_rounds": 1, "max_new_unique_rate": 0.10},
        }
        candidates = [
            {
                "arxiv_id": "2601.00001", "status": "accepted", "extraction": {"evidence_eligible": True},
                "discoveries": [{"query_labels": ["core"]}],
            },
            {
                "arxiv_id": "2601.00002", "status": "accepted", "extraction": {"evidence_eligible": True},
                "discoveries": [{"query_labels": ["limit"]}],
            },
            {
                "arxiv_id": "2601.00003", "status": "title-screened", "extraction": {},
                "discoveries": [{"query_labels": ["core"]}],
            },
        ]
        registry = {
            "candidates": candidates,
            "batches": [
                {"batch": "r1", "channel": "api", "candidate_ids": ["2601.00001", "2601.00002", "2601.00003"]},
                {"batch": "r2", "channel": "api", "candidate_ids": ["2601.00001", "2601.00002"]},
                {"batch": "r3", "channel": "browser", "candidate_ids": ["2601.00001"]},
            ],
        }

        report = coverage_module.assess(plan, registry, [])

        self.assertTrue(report["stop_assessment"]["ready_to_stop"])
        self.assertTrue(all(report["stop_assessment"]["checks"].values()))
        self.assertEqual(2, report["observed"]["full_text_recovered_count"])
        self.assertIn("does not mean read", report["metric_notes"]["full_text_count"])
        self.assertEqual(0.0, report["saturation_rounds"][-1]["new_unique_rate"])

    def test_coverage_does_not_stop_on_candidate_count_alone(self) -> None:
        plan = {
            "review_mode": "scoping",
            "search_targets": {"candidate_floor": 2, "full_text_floor": 2, "accepted_paper_floor": 1},
            "coverage_dimensions": [
                {"dimension": "limits", "query_labels": ["limit"], "minimum_unique_candidates": 1},
            ],
            "stopping_rule": {"minimum_batches": 2, "saturation_rounds": 1, "max_new_unique_rate": 0.10},
        }
        registry = {
            "candidates": [
                {"arxiv_id": "2601.00001", "status": "discovered", "discoveries": [{"query_labels": ["core"]}]},
                {"arxiv_id": "2601.00002", "status": "discovered", "discoveries": [{"query_labels": ["core"]}]},
            ],
            "batches": [
                {"batch": "r1", "candidate_ids": ["2601.00001", "2601.00002"]},
                {"batch": "r2", "candidate_ids": ["2601.00001"]},
            ],
        }

        report = coverage_module.assess(plan, registry, [])

        self.assertFalse(report["stop_assessment"]["ready_to_stop"])
        self.assertIn("coverage_dimensions", report["stop_assessment"]["unresolved"])
        self.assertIn("full_text_floor", report["stop_assessment"]["unresolved"])


if __name__ == "__main__":
    unittest.main()

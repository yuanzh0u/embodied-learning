#!/usr/bin/env python3
"""Behavior tests for the embodied-AI query planner CLI."""

from __future__ import annotations

import json
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
HUB_SCRIPTS = ROOT / "skills" / "embodied-ai-literature-hub" / "scripts"
PLANNER_ENTRY = HUB_SCRIPTS / "build_query_plan.py"  # thin entry, used via subprocess
SRC_SEARCH = ROOT / "src" / "search" 
PLANNER = SRC_SEARCH / "query_plan.py"  # implementation module for spec-loading
SEARCH = SRC_SEARCH / "arxiv.py"


def run_json(*args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(PLANNER_ENTRY), *args],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def load_search_module():
    spec = importlib.util.spec_from_file_location("search_arxiv", SEARCH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load search_arxiv module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_planner_module():
    # build_query_plan.py does `from src.search.query_taxonomy import ...`,
    # which needs the repo root on sys.path (subprocess invocation gets this for
    # free since the thin entry inserts it; direct exec_module here does not).
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("build_query_plan", PLANNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load build_query_plan module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class QueryPlannerTests(unittest.TestCase):
    def test_maps_chinese_topic_to_ea_data_and_umi_family(self) -> None:
        plan = run_json("--topic", "UMI 数据可用性", "--max-queries", "50")

        self.assertIn("EA-DATA", plan["knowledge_ids"])
        self.assertIn("umi", plan["families"])
        self.assertGreaterEqual(len(plan["queries"]), 10)
        self.assertTrue(all({"label", "tier", "query", "why"} <= set(item) for item in plan["queries"]))
        self.assertEqual(plan["queries"], plan["arxiv_api_queries"])
        self.assertEqual("scoping", plan["review_mode"])
        self.assertGreaterEqual(plan["search_targets"]["candidate_floor"], 100)
        self.assertEqual(plan["minimum_candidate_count"], plan["search_targets"]["candidate_floor"])
        self.assertTrue(plan["coverage_dimensions"])
        self.assertEqual(2, plan["stopping_rule"]["saturation_rounds"])

    def test_systematic_mode_scales_candidate_floor_with_query_surface(self) -> None:
        plan = run_json(
            "--topic", "VLA的数据金字塔",
            "--review-mode", "systematic",
            "--max-queries", "50",
        )

        self.assertEqual("systematic", plan["review_mode"])
        self.assertGreaterEqual(plan["search_targets"]["candidate_floor"], 200)
        self.assertGreaterEqual(
            plan["search_targets"]["candidate_floor"],
            len(plan["queries"]) * 6,
        )
        self.assertEqual(30, plan["search_targets"]["accepted_paper_floor"])
        self.assertAlmostEqual(0.05, plan["stopping_rule"]["max_new_unique_rate"])

    def test_mode_targets_can_be_overridden_without_becoming_caps(self) -> None:
        plan = run_json(
            "--topic", "UMI 数据可用性",
            "--review-mode", "rapid",
            "--target-candidates", "75",
            "--target-full-text", "24",
            "--target-evidence", "12",
        )

        self.assertEqual(
            {"candidate_floor": 75, "full_text_floor": 24, "accepted_paper_floor": 12},
            plan["search_targets"],
        )
        self.assertIn("never establish coverage", plan["stopping_rule"]["note"])

    def test_maps_simulation_data_limits_to_sim2real(self) -> None:
        plan = run_json("--topic", "仿真数据的局限", "--max-queries", "12")

        self.assertIn("EA-DATA", plan["knowledge_ids"])
        self.assertIn("EA-EVAL", plan["knowledge_ids"])
        self.assertIn("EA-MODEL", plan["knowledge_ids"])
        self.assertIn("sim2real", plan["families"])
        self.assertIn("world-model", plan["families"])
        self.assertEqual(plan["queries"][0]["source_key"], "sim2real")
        self.assertTrue(any(item["source_key"] == "world-model" for item in plan["queries"]))

    def test_maps_vla_data_pyramid_to_adjacent_data_layers(self) -> None:
        plan = run_json("--topic", "VLA的数据金字塔", "--max-queries", "16")

        self.assertIn("EA-DATA", plan["knowledge_ids"])
        self.assertIn("EA-MODEL", plan["knowledge_ids"])
        self.assertIn("EA-EVAL", plan["knowledge_ids"])
        self.assertIn("vla", plan["families"])
        self.assertIn("droid-ego4d", plan["families"])
        self.assertIn("sim2real", plan["families"])
        labels = {item["label"] for item in plan["queries"]}
        self.assertIn("vla-open-x-embodiment", labels)
        self.assertIn("droid-robot-manipulation", labels)
        self.assertIn("sim2real-synthetic-data", labels)

    def test_all_specialized_families_generate_queries(self) -> None:
        families = [
            "umi",
            "droid-ego4d",
            "teleoperation-demo-quality",
            "vla",
            "sim2real",
            "world-model",
            "retargeting",
            "tactile-force",
            "last-centimeter",
            "industrial-deployment",
        ]
        for family in families:
            with self.subTest(family=family):
                plan = run_json("--topic", family, "--family", family, "--max-queries", "50")
                self.assertIn(family, plan["families"])
                self.assertGreater(len(plan["queries"]), 0)

    def test_key_families_emit_family_aware_browser_fallback_queries(self) -> None:
        cases = {
            "umi": ("UMI 数据可用性", ["UMI-FT", "RealDexUMI", "demonstration quality"]),
            "vla": ("VLA 微调数据", ["OpenVLA", "Open X-Embodiment", "negative transfer"]),
            "sim2real": ("仿真数据的局限", ["sim-to-real", "synthetic data", "reality gap"]),
        }
        for family, (topic, expected_terms) in cases.items():
            with self.subTest(family=family):
                plan = run_json("--topic", topic, "--family", family, "--max-queries", "20")
                fallback_blob = "\n".join(item["query"] for item in plan["browser_fallback_queries"])
                self.assertIn(family, plan["families"])
                self.assertNotEqual(plan["browser_fallback_queries"][0]["label"], "browser-topic-arxiv")
                for term in expected_terms:
                    self.assertIn(term, fallback_blob)

    def test_calibration_terms_are_labeled_and_do_not_replace_offline_plan(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
            json.dump(
                {
                    "sources": [{"source": "x-twitter", "confidence": "low", "notes": "Alias seen in public discussion."}],
                    "terms": [{"term": "RealDexUMI", "source": "x-twitter", "why": "Fresh UMI-family alias."}],
                },
                handle,
            )
            calibration_path = handle.name

        try:
            plan = run_json("--topic", "UMI 数据可用性", "--calibration-file", calibration_path)
        finally:
            Path(calibration_path).unlink(missing_ok=True)

        calibrated = [item for item in plan["queries"] if item["tier"] == "calibrated-term"]
        self.assertTrue(calibrated)
        self.assertEqual(calibrated[0]["calibration_confidence"], "low")
        self.assertEqual(calibrated[0]["evidence_role"], "query-calibration-only")
        self.assertTrue(any("x-twitter" in note for note in plan["calibration_notes"]))

    def test_dynamic_file_adds_adjacent_families_and_labeled_queries(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
            json.dump(
                {
                    "sources": [{"source": "llm", "confidence": "medium", "notes": "World-model adjacency for a new metaphor."}],
                    "knowledge_ids": ["EA-EVAL"],
                    "families": ["world-model"],
                    "queries": [
                        {
                            "label": "dynamic-real-data-world-model",
                            "tier": "dynamic-association",
                            "query": 'all:"world model" AND all:"real-world data" AND all:robot',
                            "why": "World-model papers may discuss real-world data needs without the user's wording.",
                            "source": "llm",
                            "confidence": "medium",
                        }
                    ],
                },
                handle,
            )
            dynamic_path = handle.name

        try:
            plan = run_json("--topic", "新隐喻话题", "--dynamic-file", dynamic_path, "--max-queries", "50")
        finally:
            Path(dynamic_path).unlink(missing_ok=True)

        self.assertIn("EA-EVAL", plan["knowledge_ids"])
        self.assertIn("world-model", plan["families"])
        dynamic = [item for item in plan["queries"] if item["label"] == "dynamic-real-data-world-model"]
        self.assertTrue(dynamic)
        self.assertEqual(dynamic[0]["source_type"], "dynamic-suggestion")
        self.assertEqual(dynamic[0]["dynamic_source"], "llm")
        self.assertEqual(dynamic[0]["dynamic_confidence"], "medium")
        self.assertEqual(dynamic[0]["evidence_role"], "query-planning-only")
        self.assertTrue(plan["dynamic_suggestions"])

    def test_dynamic_queries_enter_budget_before_family_baseline(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
            json.dump(
                {
                    "families": ["world-model"],
                    "queries": [
                        {
                            "label": "dynamic-wam-world-action-model",
                            "query": '(all:WAM OR all:"world action model") AND all:robot',
                            "why": "Direct WAM wording should not be truncated behind broad family baselines.",
                            "source": "llm",
                        }
                    ],
                },
                handle,
            )
            dynamic_path = handle.name

        try:
            plan = run_json("--topic", "WAM的数据需求量", "--dynamic-file", dynamic_path, "--max-queries", "1")
        finally:
            Path(dynamic_path).unlink(missing_ok=True)

        self.assertEqual(plan["queries"][0]["label"], "dynamic-wam-world-action-model")
        self.assertEqual(plan["queries"][0]["source_type"], "dynamic-suggestion")

    def test_query_file_remains_search_arxiv_compatible_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            query_file = Path(tmpdir) / "query-plan.json"
            subprocess.run(
                [
                    sys.executable,
                    str(PLANNER_ENTRY),
                    "--topic",
                    "VLA 微调数据",
                    "--output",
                    str(query_file),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            data = json.loads(query_file.read_text(encoding="utf-8"))
            self.assertIn("queries", data)
            self.assertTrue(all("query" in item for item in data["queries"]))

            search_arxiv = load_search_module()
            loaded = search_arxiv.load_queries(
                argparse.Namespace(query_file=str(query_file), query=None)
            )
            self.assertEqual(len(loaded), len(data["queries"]))
            self.assertTrue(all({"label", "query"} <= set(item) for item in loaded))


class CoverageGroupTests(unittest.TestCase):
    """Regression tests for coverage_group() classifying by the tier string's own
    keywords, not by taxonomy-alias-normalizing it first (see the docstring in
    build_query_plan.coverage_group for the bug this guards against: tier words
    like "evaluation"/"closed-loop"/"deployment"/"tracking" are ALSO taxonomy
    aliases, and normalize_key() used to swap in an uppercase EA-* id that broke
    every lowercase substring check, silently misrouting queries into
    "adjacent-and-transfer")."""

    def setUp(self) -> None:
        self.planner = load_planner_module()

    def test_tier_words_that_double_as_taxonomy_aliases_still_classify_correctly(self) -> None:
        cases = {
            "evaluation": "evaluation-and-validation",
            "closed-loop": "evaluation-and-validation",
            "benchmark": "evaluation-and-validation",
            "deployment": "deployment-and-operations",
            "tracking": "mechanisms-and-interfaces",
        }
        for tier, expected in cases.items():
            with self.subTest(tier=tier):
                self.assertEqual(self.planner.coverage_group(tier), expected)

    def test_plain_keyword_tiers_still_classify_correctly(self) -> None:
        cases = {
            "limitation": "limits-and-counterevidence",
            "failure": "limits-and-counterevidence",
            "gap": "limits-and-counterevidence",
            "core": "direct-topic",
            "exact-lineage": "direct-topic",
            "method": "mechanisms-and-interfaces",
            "representation": "mechanisms-and-interfaces",
            "production": "deployment-and-operations",
            "generative-adjacent": "adjacent-and-transfer",
        }
        for tier, expected in cases.items():
            with self.subTest(tier=tier):
                self.assertEqual(self.planner.coverage_group(tier), expected)

    def test_dynamic_and_calibrated_tiers_fall_back_to_label_keywords(self) -> None:
        """A 2026-09-11 review run generated 50 dynamic/calibrated queries that
        all collapsed into one adjacent-and-transfer dimension because their
        tier names carry no dimension signal. The label keywords name the
        dimension instead."""
        cases = {
            ("dynamic-association", "dynamic-direct-topic-online-temporal-calibration"): "direct-topic",
            ("dynamic-association", "dynamic-limit-degenerate-motion"): "limits-and-counterevidence",
            ("dynamic-association", "dynamic-benchmark-euroco"): "evaluation-and-validation",
            ("dynamic-association", "dynamic-mechanism-bspline"): "mechanisms-and-interfaces",
            ("dynamic-association", "dynamic-association-unlabeled"): "adjacent-and-transfer",
            ("dynamic-core", "latin-1"): "direct-topic",
            ("calibrated-term", "calibrated-limit-degeneracy"): "limits-and-counterevidence",
            ("calibrated-term", "calibrated-time-offset"): "adjacent-and-transfer",
        }
        for (tier, label), expected in cases.items():
            with self.subTest(tier=tier, label=label):
                self.assertEqual(self.planner.coverage_group(tier, label), expected)


class WeakAliasConfidenceTests(unittest.TestCase):
    """A topic matched ONLY through generic vocabulary aliases (点云/传感器/data/
    model/...) must not inherit the matched card's static queries: the 2026-09-11
    点云特征法粗配准 run inherited EA-SENSOR's robot-manipulation queries, the real
    topic vocabulary never entered the plan, and retrieval failed end to end.
    infer_confident_keys is the planner's confidence gate; the plan still keeps
    the weak ids in knowledge_ids for run-manifest routing context."""

    def setUp(self) -> None:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from src.search import query_taxonomy

        self.taxonomy = query_taxonomy

    def test_vocabulary_only_topic_degrades_to_no_confident_keys(self) -> None:
        for topic in ("点云特征法粗配准", "多传感器时间同步误差估计", "点云粗配准", "点云去动态"):
            with self.subTest(topic=topic):
                raw = self.taxonomy.infer_keys(topic)
                self.assertEqual(raw, ["EA-SENSOR"], "expected the old mis-route to reproduce")
                self.assertEqual(self.taxonomy.infer_confident_keys(topic), [])

    def test_distinctive_topic_still_maps_confidently(self) -> None:
        cases = {
            "传感器融合": ["EA-SENSOR"],
            "vla数据金字塔": ["EA-DATA", "EA-MODEL", "EA-EVAL", "droid-ego4d", "vla", "sim2real"],
            "触觉力控": ["EA-SENSOR", "tactile-force"],
            "世界模型驱动4d仿真与规划": ["EA-MODEL", "EA-EVAL", "world-model"],
        }
        for topic, expected in cases.items():
            with self.subTest(topic=topic):
                self.assertEqual(self.taxonomy.infer_confident_keys(topic), expected)

    def test_weak_only_plan_skips_card_queries_and_keeps_routing_ids(self) -> None:
        plan = run_json("--topic", "点云特征法粗配准", "--max-queries", "10")
        self.assertEqual(plan["knowledge_ids"], ["EA-SENSOR"])
        self.assertEqual(plan["plan_knowledge_ids"], [])
        labels = {item["label"] for item in plan["arxiv_api_queries"]}
        self.assertNotIn("ea-sensor-multimodal-policy", labels)
        self.assertTrue(any(label.startswith("generic") for label in labels))
        self.assertTrue(
            any("generic vocabulary aliases" in note for note in plan["notes"]),
            plan["notes"],
        )

    def test_confident_plan_keeps_card_queries(self) -> None:
        plan = run_json("--topic", "传感器融合", "--max-queries", "10")
        self.assertEqual(plan["plan_knowledge_ids"], ["EA-SENSOR"])
        labels = {item["label"] for item in plan["arxiv_api_queries"]}
        self.assertIn("ea-sensor-multimodal-policy", labels)


if __name__ == "__main__":
    unittest.main()

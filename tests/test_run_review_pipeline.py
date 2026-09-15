"""Tests for scripts/run_review_pipeline.py — the mechanical-stage driver.

Network is fully mocked: every pipeline script invocation goes through a fake
``run_command``/``Popen`` seam, so the assertions here are about command
shapes, stage ordering, idempotent skipping, and the summary payload.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
DRIVER_PATH = REPO_ROOT / "scripts" / "run_review_pipeline.py"


def load_driver():
    spec = importlib.util.spec_from_file_location("run_review_pipeline", DRIVER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TermsTest(unittest.TestCase):
    def setUp(self):
        self.driver = load_driver()

    def test_mechanical_terms_prefer_latin_words(self):
        # Screening is substring matching against English titles/abstracts:
        # Latin tokens win; pure-Chinese text falls through to CJK tokens.
        self.assertEqual(
            self.driver.mechanical_terms("高斯压缩蒸馏 Gaussian compression distillation", ""),
            ["gaussian", "compression", "distillation"],
        )
        self.assertEqual(
            self.driver.mechanical_terms("点云去动态", ""),
            ["点云去动态"],
        )

    def test_mechanical_terms_dedupe_and_drop_stopwords(self):
        self.assertEqual(
            self.driver.mechanical_terms("ERASOR erasor the removal", "dynamic"),
            ["erasor", "removal", "dynamic"],
        )

    def test_extract_terms_json(self):
        self.assertEqual(
            self.driver.extract_terms_json('前置说明 {"terms": ["gaussian", "splatting"]}') ,
            ["gaussian", "splatting"],
        )
        self.assertIsNone(self.driver.extract_terms_json("不是 JSON"))
        self.assertIsNone(self.driver.extract_terms_json('{"terms": []}'))

    def test_agent_terms_falls_back_on_failure(self):
        def ok_run(command, **kwargs):
            return mock.Mock(returncode=0, stdout='{"terms": ["ok"]}\n', stderr="")

        with mock.patch.object(self.driver.subprocess, "run", side_effect=ok_run):
            self.assertEqual(self.driver.agent_terms("主题", "", 1.0, "/fake/claude"), ["ok"])
        with mock.patch.object(self.driver.subprocess, "run", side_effect=OSError("no cli")):
            self.assertIsNone(self.driver.agent_terms("主题", "", 1.0, "/fake/claude"))
        with mock.patch.object(self.driver.subprocess, "run", side_effect=self.driver.subprocess.TimeoutExpired(cmd="x", timeout=1)):
            self.assertIsNone(self.driver.agent_terms("主题", "", 1.0, "/fake/claude"))

    def test_terms_selector_agent_success(self):
        result = mock.Mock(returncode=0, stdout='{"terms": ["lidar", "calibration"]}\n', stderr="")
        with mock.patch.object(self.driver.subprocess, "run", return_value=result):
            selector = self.driver.TermsSelector("主题", "", use_agent=True, timeout_s=1.0, cli="/fake/claude")
            selector.start()
            terms, source = selector.join()
        self.assertEqual(terms, ["lidar", "calibration"])
        self.assertEqual(source, "agent")

    def test_terms_selector_mechanical_mode_never_spawns(self):
        selector = self.driver.TermsSelector("ERASOR 点云", "", use_agent=False, timeout_s=1.0, cli="/fake/claude")
        selector.start()
        terms, source = selector.join()
        self.assertEqual(source, "mechanical")
        self.assertEqual(terms, ["erasor"])


class DriverPipelineTest(unittest.TestCase):
    """End-to-end driver run with every subprocess faked onto disk."""

    def setUp(self):
        self.driver = load_driver()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run_dir = Path(self.tmp.name) / "work" / "literature-review-demo-20260101"
        self.run_dir.mkdir(parents=True)
        (self.run_dir / "run.json").write_text(
            json.dumps({"status": "in-progress", "topic": "demo", "knowledge_ids": []}),
            encoding="utf-8",
        )
        self.commands: list[list[str]] = []

    # -- fake subprocess plumbing -----------------------------------------

    STAGE_SCRIPTS = {
        "build-query-plan": ("query-plan.json", "query-plan.md"),
        "search-arxiv": ("search-arxiv.json",),
        "build-candidate-registry": ("candidate-registry.json",),
        "screen-candidates": ("screening.json", "screening-ids.txt", "screening.md"),
        "assess-review-coverage": ("coverage-report.json",),
        "extract-content-queue": ("extraction-summary.json",),
    }

    def _stage_payload(self, script: str) -> str:
        plan = {"knowledge_ids": ["EA-SENSOR"], "queries": [{"label": "a", "query": "all:demo"}]}
        registry = {"candidate_count": 42, "candidates": []}
        coverage = {
            "observed": {"full_text_recovered_count": 3},
            "coverage_dimensions": True,
            "stop_assessment": {"checks": {"candidate_floor": True, "saturation": False}},
        }
        payloads = {
            "build-query-plan": plan,
            "search-arxiv": {},
            "build-candidate-registry": registry,
            "screen-candidates": {},
            "assess-review-coverage": coverage,
            "extract-content-queue": {"paper_count": 2},
        }
        return json.dumps(payloads[script])

    def fake_run(self, command, timeout=None):
        """Record the argv and write the stage's declared outputs."""
        self.commands.append(command)
        joined = " ".join(command)
        # Longest marker first: the registry command carries "search-arxiv.json" as a
        # path argument, which would otherwise shadow "build-candidate-registry".
        for script in sorted(self.STAGE_SCRIPTS, key=len, reverse=True):
            outputs = self.STAGE_SCRIPTS[script]
            if script in joined:
                for name in outputs:
                    out = self.run_dir / name
                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_text(self._stage_payload(script), encoding="utf-8")
                return mock.Mock(returncode=0, stdout="", stderr="")
        return mock.Mock(returncode=0, stdout="", stderr="")

    def run_driver(self, argv: list[str], *, agent_dynamic=None) -> tuple[int, dict]:
        """agent_dynamic=None keeps the default patch (agent returns None);
        pass a Mock to observe/override the dynamic-query agent."""
        agent_patch = (
            mock.patch.object(self.driver, "agent_dynamic_queries", return_value=None)
            if agent_dynamic is None
            else mock.patch.object(self.driver, "agent_dynamic_queries", new=agent_dynamic)
        )
        with mock.patch.object(self.driver, "run_command", side_effect=self.fake_run), \
             mock.patch.object(self.driver.subprocess, "Popen", side_effect=AssertionError("S2 must be skipped in this harness")), \
             mock.patch.object(self.driver.TermsSelector, "join", return_value=(["demo"], "mechanical")), \
             agent_patch, \
             mock.patch.object(self.driver.time, "sleep"), \
             mock.patch.object(Path, "glob", return_value=iter([])):
            code = self.driver.main(argv)
        summary = json.loads((self.run_dir / "pipeline-summary.json").read_text(encoding="utf-8"))
        return code, summary

    def argv(self, *extra: str) -> list[str]:
        return [
            "--run-dir", str(self.run_dir),
            "--topic", "demo topic ERASOR",
            "--review-mode", "rapid",
            "--time-range", "2023-01-01..2026-09-09",
            "--kb-root", str(self.tmp.name),
            *extra,
        ]

    def stage_names(self) -> list[str]:
        names = []
        for command in self.commands:
            joined = " ".join(command)
            for marker in ("build-query-plan", "search-arxiv", "build-candidate-registry", "screen-candidates", "assess-review-coverage", "extract-content-queue"):
                if marker in joined:
                    names.append(marker)
        return names

    def test_full_run_stage_order_and_summary(self):
        code, summary = self.run_driver(self.argv("--skip-s2", "--no-terms-agent"))
        self.assertEqual(code, 0)
        names = self.stage_names()
        # search-arxiv appears twice: first pass + empty-result cooldown retry.
        self.assertEqual(
            [n for n in names if n != "search-arxiv"],
            [
                "build-query-plan",
                "build-candidate-registry",
                "screen-candidates",
                "assess-review-coverage",
                "extract-content-queue",
            ],
        )
        self.assertGreaterEqual(names.count("search-arxiv"), 2)
        self.assertEqual(summary["knowledge_ids"], ["EA-SENSOR"])
        self.assertEqual(summary["candidate_count"], 42)
        self.assertEqual(summary["screening_limit"], 24)  # rapid
        self.assertTrue(summary["coverage_dimensions_passed"])
        self.assertTrue(summary["candidate_floor_passed"])
        self.assertFalse(summary["saturation_passed"])
        self.assertEqual(summary["terms"], ["demo"])
        self.assertEqual(summary["terms_source"], "mechanical")
        # knowledge_ids flowed back into run.json (init memoization).
        manifest = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["knowledge_ids"], ["EA-SENSOR"])

    def test_arxiv_command_shape_single_process(self):
        self.run_driver(self.argv("--skip-s2", "--no-terms-agent"))
        arxiv = next(c for c in self.commands if "search-arxiv" in " ".join(c))
        self.assertIn("--query-file", arxiv)
        self.assertIn("--start-date", arxiv)
        self.assertIn("--end-date", arxiv)
        # One process for the whole plan: no --query repetition here.
        self.assertNotIn("--query", arxiv)

    def test_screening_uses_terms_and_mode_limit(self):
        self.run_driver(self.argv("--skip-s2", "--no-terms-agent"))
        screen = next(c for c in self.commands if "screen-candidates" in " ".join(c))
        self.assertIn("demo", screen[screen.index("--terms") + 1].split(","))
        self.assertEqual(screen[screen.index("--limit") + 1], "24")
        scoping = self.run_driver(self.argv("--skip-s2", "--no-terms-agent", "--review-mode", "scoping"))
        self.assertEqual(scoping[1]["screening_limit"], 40)

    def test_extraction_workers_capped_and_checkpointed(self):
        self.run_driver(self.argv("--skip-s2", "--no-terms-agent", "--workers", "9"))
        extraction = next(c for c in self.commands if "extract-content-queue" in " ".join(c))
        self.assertEqual(extraction[extraction.index("--workers") + 1], "4")
        self.assertIn("--include-full-text", extraction)
        self.assertEqual(extraction[extraction.index("--ocr-mode") + 1], "never")

    def test_idempotent_rerun_skips_completed_stages(self):
        self.run_driver(self.argv("--skip-s2", "--no-terms-agent"))
        first_count = len(self.commands)
        code, _ = self.run_driver(self.argv("--skip-s2", "--no-terms-agent"))
        self.assertEqual(code, 0)
        # All script stages skipped on the rerun (the fresh run's extra arXiv
        # retry command is not repeated because outputs are present).
        self.assertEqual(len(self.commands), first_count)

    def test_missing_run_json_rejected(self):
        code = self.driver.main([
            "--run-dir", str(self.run_dir.parent / "nope"),
            "--topic", "x", "--no-terms-agent",
        ])
        self.assertEqual(code, 2)

    def test_bad_time_range_rejected(self):
        code = self.driver.main([
            "--run-dir", str(self.run_dir),
            "--topic", "x", "--time-range", "2023-01-01", "--no-terms-agent",
        ])
        self.assertEqual(code, 2)

    def test_plan_stage_merges_prior_dynamic_queries_instead_of_dropping_them(self):
        """2026-09-11 regression: a claude session wrote 20 good dynamic queries
        into dynamic-queries.json; a driver replan for a pure-Chinese topic had
        no latin terms, omitted --dynamic-file, and the plan lost every one of
        them. The driver must always pass the file and re-merge its content."""
        prior = {
            "queries": [
                {"label": "dynamic-direct-topic-x", "query": 'all:"temporal calibration"', "tier": "dynamic-association"},
            ],
        }
        (self.run_dir / "dynamic-queries.json").write_text(json.dumps(prior), encoding="utf-8")
        self.run_driver(self.argv("--skip-s2", "--no-terms-agent"))
        plan_cmd = next(c for c in self.commands if "build-query-plan" in " ".join(c))
        self.assertIn("--dynamic-file", plan_cmd)
        merged = json.loads((self.run_dir / "dynamic-queries.json").read_text(encoding="utf-8"))
        labels = {q["label"] for q in merged["queries"]}
        self.assertIn("dynamic-direct-topic-x", labels)
        # mechanical latin terms from "demo topic ERASOR" are appended, not clobbered
        self.assertTrue(any(q["label"].startswith("latin-") for q in merged["queries"]))


class SearchStrategyTest(DriverPipelineTest):
    """Strategy selection + seed parsing + dynamic-query agent plumbing."""

    def test_seed_id_parsing_normalizes(self):
        parse = self.driver.parse_seed_ids
        self.assertEqual(
            parse("2402.14207, arxiv:1704.02084v2  https://arxiv.org/abs/2005.04243"),
            ["2402.14207", "1704.02084", "2005.04243"],
        )
        self.assertEqual(parse("2402.14207 2402.14207"), ["2402.14207"])
        self.assertEqual(parse(""), [])
        self.assertEqual(parse("not-an-id"), [])

    def test_dynamic_agent_output_shape(self):
        raw = '前置说明 {"queries": [{"label": "direct-anchor", "tier": "direct-anchor", "query": "all:\\"coarse registration\\"", "why": "w"}]} 后置'
        payload = self.driver.extract_dynamic_queries_json(raw)
        self.assertEqual(payload["queries"][0]["label"], "direct-anchor")
        self.assertIsNone(self.driver.extract_dynamic_queries_json("no json"))

    def test_smart_strategy_runs_agent_and_records_source(self):
        agent = mock.Mock(return_value={"queries": [{"label": "direct-x", "tier": "direct-x", "query": "all:demo"}]})
        _, summary = self.run_driver(self.argv("--skip-s2", "--no-terms-agent"), agent_dynamic=agent)
        agent.assert_called_once()
        self.assertEqual(summary["dynamic_source"], "agent")

    def test_fast_strategy_skips_dynamic_agent(self):
        agent = mock.Mock()
        _, summary = self.run_driver(
            self.argv("--skip-s2", "--no-terms-agent", "--search-strategy", "fast"),
            agent_dynamic=agent,
        )
        agent.assert_not_called()
        self.assertEqual(summary["dynamic_source"], "disabled (fast strategy)")

    def test_seeds_strategy_with_ids_skips_arxiv_keyword_search(self):
        argv = self.argv(
            "--skip-s2", "--no-terms-agent", "--search-strategy", "seeds",
            "--seed-arxiv-ids", "2402.14207",
        )
        code, summary = self.run_driver(argv)
        self.assertEqual(code, 0)
        self.assertEqual(summary["seed_ids"], ["2402.14207"])
        self.assertNotIn("search-arxiv", " ".join(" ".join(c) for c in self.commands))

    def test_smart_strategy_with_seeds_runs_citation_expansion(self):
        argv = self.argv(
            "--skip-s2", "--no-terms-agent", "--search-strategy", "smart",
            "--seed-arxiv-ids", "2402.14207, 1704.02084",
        )
        code, summary = self.run_driver(argv)
        self.assertEqual(code, 0)
        self.assertEqual(summary["seed_ids"], ["2402.14207", "1704.02084"])
        expand = next(c for c in self.commands if "expand-via-citations" in " ".join(c))
        self.assertEqual(expand[expand.index("--seed-id") + 1], "2402.14207")
        self.assertNotEqual(summary["citation_expansion"], "skipped (no seeds)")

    def test_registry_receives_citation_result_when_present(self):
        # Simulate a completed expansion: the fake stage writer must emit the file.
        def fake_run_with_citation(command, timeout=None):
            joined = " ".join(command)
            result = self.fake_run(command, timeout=timeout)
            if "expand-via-citations" in joined:
                (self.run_dir / "citation-expansion.json").write_text(
                    json.dumps({"papers": []}), encoding="utf-8"
                )
            return result
        with mock.patch.object(self.driver, "run_command", side_effect=fake_run_with_citation):
            with mock.patch.object(self.driver, "agent_dynamic_queries", return_value=None), \
                 mock.patch.object(self.driver.TermsSelector, "join", return_value=(["demo"], "mechanical")), \
                 mock.patch.object(self.driver.time, "sleep"), \
                 mock.patch.object(Path, "glob", return_value=iter([])):
                code = self.driver.main(self.argv(
                    "--skip-s2", "--no-terms-agent", "--seed-arxiv-ids", "2402.14207",
                ))
        self.assertEqual(code, 0)
        registry = next(c for c in self.commands if "build-candidate-registry" in " ".join(c))
        self.assertIn("--citation-result", registry)


if __name__ == "__main__":
    unittest.main()

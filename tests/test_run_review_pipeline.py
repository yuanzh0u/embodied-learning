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


class ExtractionQueueLineTest(unittest.TestCase):
    """The extraction queue's stdout becomes progress ticks; only HELD papers
    and summaries remain as dialog lines."""

    def setUp(self):
        self.driver = load_driver()

    def test_ok_is_progress_held_is_noted(self):
        lines: list[str] = []
        with mock.patch.object(self.driver, "log", side_effect=lines.append):
            self.driver.extraction_queue_line("OK 2402.10329 (3/48)")
            self.driver.extraction_queue_line("HELD 2302.01109 (4/48)")
            self.driver.extraction_queue_line("Recovered 47 of 48 papers; held 1.")
        self.assertEqual(lines[0], "[DRIVER-PROGRESS:extract:3/48]")
        self.assertEqual(lines[1], "[DRIVER-PROGRESS:extract:4/48]")
        self.assertIn("[PAPER] 2302.01109", lines[2])
        self.assertIn("HELD", lines[2])
        self.assertTrue(lines[3].startswith("[DRIVER] 全文抽取 Recovered"))

    def test_command_label_uses_script_and_subcommand(self):
        self.assertEqual(
            self.driver.command_label(["/usr/bin/python3", "/x/search.py", "search-arxiv", "--flag"]),
            "search.py search-arxiv",
        )
        self.assertEqual(self.driver.command_label(["/usr/bin/python3", "/x/build_paper_note.py"]), "build_paper_note.py")


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
        self.with_s2 = False
        self.held_in_summary = False

    # -- fake subprocess plumbing -----------------------------------------

    STAGE_SCRIPTS = {
        "build-query-plan": ("query-plan.json", "query-plan.md"),
        "search-arxiv": ("search-arxiv.json",),
        "build-candidate-registry": ("candidate-registry.json",),
        "screen-candidates": ("screening.json", "screening-ids.txt", "screening.md"),
        "select-candidates": ("screening.json", "screening-ids.txt", "screening.md"),
        "assess-review-coverage": ("coverage-report.json",),
        "extract-content-queue": ("extraction-summary.json",),
        "build_review_packet": ("review-packet.md", "writing-brief.md", "evidence-appendix.md"),
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
            "select-candidates": {
                "selection_rule": {
                    "strategy": "smart",
                    "detail": "smart selected 2/42 considered; shortfall: only 2 relevant (limit 24), not padded",
                },
                "candidates": [],
            },
            "assess-review-coverage": coverage,
            "extract-content-queue": {"paper_count": 2},
            "build_review_packet": {"packet": "mechanical"},
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
                    if name == "screening-ids.txt":
                        out.write_text("2402.10329\n2402.10330\n", encoding="utf-8")
                    else:
                        out.write_text(self._stage_payload(script), encoding="utf-8")
                return mock.Mock(returncode=0, stdout="", stderr="")
        return mock.Mock(returncode=0, stdout="", stderr="")

    def fake_popen(self, command, **kwargs):
        """Fake for the streaming stage path (extract-content-queue): records
        the argv, writes the stage's outputs, returns a process whose stdout
        emits per-paper progress lines. The S2 keyword channel is opt-in and
        only reaches Popen under --with-s2."""
        self.commands.append(command)
        joined = " ".join(command)
        if "search-semantic-scholar" in joined:
            if not self.with_s2:
                raise AssertionError("S2 keyword channel must be opt-in (--with-s2)")
            out = self.run_dir / "search-semantic-scholar.json"
            out.write_text(json.dumps({"paper_count": 7, "papers": []}), encoding="utf-8")
            return mock.Mock(communicate=lambda timeout=None: (None, None), returncode=0)
        if "extract-content-queue" not in joined:
            raise AssertionError(f"unexpected streaming subprocess: {joined}")
        payload = json.loads(self._stage_payload("extract-content-queue"))
        if self.held_in_summary:
            payload["held_count"] = 2
        for name in self.STAGE_SCRIPTS["extract-content-queue"]:
            out = self.run_dir / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(payload), encoding="utf-8")
        return mock.Mock(stdout=iter(["OK 2402.10329 (1/2)", "HELD 2302.01109 (2/2)"]), wait=lambda timeout=None: 0)

    def run_driver(self, argv: list[str], *, agent_dynamic=None) -> tuple[int, dict]:
        """agent_dynamic=None keeps the default patch (agent returns None);
        pass a Mock to observe/override the dynamic-query agent."""
        agent_patch = (
            mock.patch.object(self.driver, "agent_dynamic_queries", return_value=None)
            if agent_dynamic is None
            else mock.patch.object(self.driver, "agent_dynamic_queries", new=agent_dynamic)
        )
        with mock.patch.object(self.driver, "run_command", side_effect=self.fake_run), \
             mock.patch.object(self.driver.subprocess, "Popen", side_effect=self.fake_popen), \
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
            for marker in ("build-query-plan", "search-arxiv", "build-candidate-registry", "screen-candidates", "select-candidates", "assess-review-coverage", "extract-content-queue"):
                if marker in joined:
                    names.append(marker)
        return names

    def test_snapshot_autodetected_and_forwarded(self):
        """Offline-first: a snapshot under the KB root is picked up without any
        flag and forwarded to search-arxiv as --metadata-snapshot."""
        snapshot = Path(self.tmp.name) / "arxiv-metadata-oai-snapshot.sqlite"
        snapshot.write_text("", encoding="utf-8")
        code, _ = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        arxiv_cmd = next(c for c in self.commands if "search-arxiv" in " ".join(c))
        self.assertIn("--metadata-snapshot", arxiv_cmd)
        self.assertEqual(arxiv_cmd[arxiv_cmd.index("--metadata-snapshot") + 1], str(snapshot))

    def test_snapshot_autodetect_prefers_sqlite_and_allows_jsonl(self):
        base = Path(self.tmp.name)
        self.assertIsNone(self.driver.autodetect_snapshot(base))
        (base / "arxiv-metadata-oai-snapshot.jsonl").write_text("", encoding="utf-8")
        self.assertEqual(self.driver.autodetect_snapshot(base), base / "arxiv-metadata-oai-snapshot.jsonl")
        (base / "arxiv-metadata-oai-snapshot.sqlite").write_text("", encoding="utf-8")
        self.assertEqual(self.driver.autodetect_snapshot(base), base / "arxiv-metadata-oai-snapshot.sqlite")

    def test_full_run_stage_order_and_summary(self):
        code, summary = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        names = self.stage_names()
        # search-arxiv appears twice: first pass + empty-result cooldown retry.
        self.assertEqual(
            [n for n in names if n != "search-arxiv"],
            [
                "build-query-plan",
                "build-candidate-registry",
                "select-candidates",
                "assess-review-coverage",
                "extract-content-queue",
            ],
        )
        self.assertGreaterEqual(names.count("search-arxiv"), 2)
        self.assertEqual(summary["knowledge_ids"], ["EA-SENSOR"])
        self.assertEqual(summary["candidate_count"], 42)
        self.assertEqual(summary["screening_limit"], 24)  # rapid
        self.assertEqual(summary["selection_strategy"], "smart")
        self.assertIn("smart selected", summary["selection_detail"])
        self.assertEqual(summary["abstract_events"], 0)
        self.assertTrue(summary["coverage_dimensions_passed"])
        self.assertTrue(summary["candidate_floor_passed"])
        self.assertFalse(summary["saturation_passed"])
        self.assertEqual(summary["terms"], ["demo"])
        self.assertEqual(summary["terms_source"], "mechanical")
        # knowledge_ids flowed back into run.json (init memoization), and so
        # did the selection strategy the run was born with.
        manifest = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["knowledge_ids"], ["EA-SENSOR"])
        self.assertEqual(manifest["selection_strategy"], "smart")

    def test_arxiv_command_shape_single_process(self):
        self.run_driver(self.argv("--no-terms-agent"))
        arxiv = next(c for c in self.commands if "search-arxiv" in " ".join(c))
        self.assertIn("--query-file", arxiv)
        self.assertIn("--start-date", arxiv)
        self.assertIn("--end-date", arxiv)
        # One process for the whole plan: no --query repetition here.
        self.assertNotIn("--query", arxiv)

    def test_selection_strategy_defaults_to_smart(self):
        args = self.driver.parse_args(self.argv())
        self.assertEqual(args.selection_strategy, "smart")
        self.assertEqual(
            sorted(self.driver.SELECTION_STRATEGIES),
            ["bm25", "influence", "keywords", "smart"],
        )

    def test_smart_selection_dispatches_select_candidates(self):
        """Default (smart): screening goes through search.py select-candidates
        with the registry + topic + focus; the terms thread still runs but the
        screening command does not consume it."""
        self.run_driver(self.argv("--no-terms-agent"))
        screen = next(c for c in self.commands if "select-candidates" in " ".join(c))
        self.assertIn("--registry", screen)
        self.assertEqual(screen[screen.index("--strategy") + 1], "smart")
        self.assertEqual(screen[screen.index("--topic") + 1], "demo topic ERASOR")
        self.assertEqual(screen[screen.index("--limit") + 1], "24")
        self.assertIn("--terms", screen)  # English terms augment the bm25/smart query
        self.assertFalse(any("screen-candidates" in " ".join(c) for c in self.commands))

    def test_screening_uses_terms_and_mode_limit(self):
        """The keywords strategy keeps the legacy term-matching screen."""
        self.run_driver(self.argv("--no-terms-agent", "--selection-strategy", "keywords"))
        screen = next(c for c in self.commands if "screen-candidates" in " ".join(c))
        self.assertIn("demo", screen[screen.index("--terms") + 1].split(","))
        self.assertEqual(screen[screen.index("--limit") + 1], "24")
        self.assertFalse(any("select-candidates" in " ".join(c) for c in self.commands))
        scoping = self.run_driver(self.argv("--no-terms-agent", "--review-mode", "scoping"))
        self.assertEqual(scoping[1]["screening_limit"], 40)

    def test_deep_read_limit_defaults_to_mode(self):
        """Deep-read throughput is mode-aware by default (the fixed default 10
        starved scoping reviews down to 7 citable papers in real runs)."""
        self.assertIsNone(self.driver.parse_args(self.argv()).deep_read_limit)
        self.assertEqual(self.driver.DEEP_READ_LIMITS, {"rapid": 10, "scoping": 16, "systematic": 40})

    def test_deep_read_order_puts_seeds_first(self):
        """Influence-scored screening buries fresh seed papers below the cut;
        the deep-read queue must force them to the front (the 20260924 run
        never deep-read its user-supplied seed)."""
        order = self.driver.deep_read_order(["a", "b", "c", "d"], ["c"], 3)
        self.assertEqual(order, ["c", "a", "b"])
        # A seed below the screening cut is still queued.
        self.assertEqual(self.driver.deep_read_order(["a", "b"], ["z"], 2), ["z", "a"])
        # Seed already present is not duplicated.
        self.assertEqual(self.driver.deep_read_order(["a", "b"], ["a"], 2), ["a", "b"])

    def test_projection_stamps_event_scale_into_run_json(self):
        """check_run_bundle requires run.json event_count to match the evidence
        set; only the driver knows it at projection time, so it must stamp the
        manifest instead of leaving the writer to reverse-engineer the gate."""
        evidence_dir = self.run_dir / "evidence"
        evidence_dir.mkdir()
        for stem in ("p1", "p2"):
            (evidence_dir / f"{stem}.jsonl").write_text(
                json.dumps({"id": f"EA-DEMO-2026-{stem}"}) + "\n", encoding="utf-8"
            )
        (evidence_dir / "p3.jsonl").write_text("", encoding="utf-8")
        self.driver._stamp_evidence_scale(
            Path(self.tmp.name), self.run_dir / "run.json", evidence_dir, 2
        )
        manifest = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["event_count"], 2)
        self.assertEqual(manifest["evidence_papers"], 2)  # empty p3.jsonl ignored

    def test_extraction_workers_capped_and_checkpointed(self):
        self.run_driver(self.argv("--no-terms-agent", "--workers", "9"))
        extraction = next(c for c in self.commands if "extract-content-queue" in " ".join(c))
        self.assertEqual(extraction[extraction.index("--workers") + 1], "4")
        self.assertIn("--include-full-text", extraction)
        self.assertEqual(extraction[extraction.index("--ocr-mode") + 1], "never")

    def test_idempotent_rerun_skips_completed_stages(self):
        self.run_driver(self.argv("--no-terms-agent"))
        first_count = len(self.commands)
        code, _ = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        # All script stages skipped on the rerun (the fresh run's extra arXiv
        # retry command is not repeated because outputs are present).
        self.assertEqual(len(self.commands), first_count)

    def test_arxiv_hit_count_reads_top_level_paper_count(self):
        """Both arXiv backends put paper_count at the top level and per-query
        entries only carry result_count — a successful retrieval must not be
        misread as 0 hits and force the cooldown retry."""
        base = self.fake_run

        def fake_run(command, timeout=None):
            result = base(command, timeout=timeout)
            if len(command) > 2 and command[2] == "search-arxiv":
                (self.run_dir / "search-arxiv.json").write_text(
                    json.dumps({
                        "paper_count": 399,
                        "queries": [{"label": "a", "query": "all:demo", "result_count": 25}],
                    }),
                    encoding="utf-8",
                )
            return result

        self.fake_run = fake_run
        code, _ = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        arxiv_runs = [c for c in self.commands if len(c) > 2 and c[2] == "search-arxiv"]
        self.assertEqual(len(arxiv_runs), 1)

    def test_s2_keyword_channel_is_opt_in(self):
        """Default retrieval is fast: no search-semantic-scholar pass runs and
        the summary records the channel as skipped."""
        code, summary = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        self.assertFalse(any("search-semantic-scholar" in " ".join(c) for c in self.commands))
        self.assertIn("skipped", summary["s2_detail"])

    def test_with_s2_runs_keyword_channel_and_merges(self):
        self.with_s2 = True
        code, summary = self.run_driver(self.argv("--no-terms-agent", "--with-s2"))
        self.assertEqual(code, 0)
        self.assertTrue(any("search-semantic-scholar" in " ".join(c) for c in self.commands))
        self.assertEqual(summary["s2_detail"], "ok")
        registry_cmd = next(c for c in self.commands if len(c) > 2 and c[2] == "build-candidate-registry")
        self.assertIn("--semantic-scholar-result", registry_cmd)

    def test_extraction_reruns_while_held_papers_outstanding(self):
        """HELD extractions are retryable: while extraction-summary.json
        reports held_count > 0, a rerun re-runs the queue (the queue caches
        evidence-eligible papers, so only HELD ones re-fetch). A fully
        recovered summary goes back to plain stage skipping."""
        self.held_in_summary = True
        self.run_driver(self.argv("--no-terms-agent"))
        self.run_driver(self.argv("--no-terms-agent"))
        held_reruns = len([c for c in self.commands if "extract-content-queue" in " ".join(c)])
        self.assertEqual(held_reruns, 2)

        self.held_in_summary = False
        self.commands.clear()
        self.run_driver(self.argv("--no-terms-agent"))
        self.run_driver(self.argv("--no-terms-agent"))
        recovered_reruns = len([c for c in self.commands if "extract-content-queue" in " ".join(c)])
        self.assertEqual(recovered_reruns, 1)

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
        self.run_driver(self.argv("--no-terms-agent"))
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
        _, summary = self.run_driver(self.argv("--no-terms-agent"), agent_dynamic=agent)
        agent.assert_called_once()
        self.assertEqual(summary["dynamic_source"], "agent")

    def test_fast_strategy_skips_dynamic_agent(self):
        agent = mock.Mock()
        _, summary = self.run_driver(
            self.argv("--no-terms-agent", "--search-strategy", "fast"),
            agent_dynamic=agent,
        )
        agent.assert_not_called()
        self.assertEqual(summary["dynamic_source"], "disabled (fast strategy)")

    def test_seeds_strategy_with_ids_skips_arxiv_keyword_search(self):
        argv = self.argv(
            "--no-terms-agent", "--search-strategy", "seeds",
            "--seed-arxiv-ids", "2402.14207",
        )
        code, summary = self.run_driver(argv)
        self.assertEqual(code, 0)
        self.assertEqual(summary["seed_ids"], ["2402.14207"])
        self.assertNotIn("search-arxiv", " ".join(" ".join(c) for c in self.commands))

    def test_external_candidates_skip_retrieval_and_feed_registry(self):
        harvest = Path(self.tmp.name) / "harvest.json"
        harvest.write_text(
            json.dumps({
                "batch": "curated-list:demo/repo",
                "source_label": "curated-list:demo/repo",
                "candidates": [{"arxiv_id": "2311.18259", "title": "Ego-Exo4D", "context": "c"}],
            }),
            encoding="utf-8",
        )
        code, summary = self.run_driver(
            self.argv("--no-terms-agent", "--external-candidates", str(harvest))
        )
        self.assertEqual(code, 0)
        names = self.stage_names()
        self.assertNotIn("search-arxiv", names)  # keyword retrieval replaced by the list
        self.assertEqual(names[0], "build-query-plan")  # plan still runs (knowledge IDs + coverage)
        registry = next(c for c in self.commands if "build-candidate-registry" in " ".join(c))
        self.assertEqual(registry[registry.index("--curated-list-result") + 1], str(harvest))
        self.assertEqual(summary["external_candidates"], [str(harvest)])

    def test_external_candidates_missing_file_rejected(self):
        code = self.driver.main(self.argv("--no-terms-agent", "--external-candidates", "/nonexistent.json"))
        self.assertEqual(code, 2)
        self.assertEqual(self.commands, [])  # rejected before any stage ran

    def test_smart_strategy_with_seeds_runs_citation_expansion(self):
        argv = self.argv(
            "--no-terms-agent", "--search-strategy", "smart",
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
                 mock.patch.object(self.driver.subprocess, "Popen", side_effect=self.fake_popen), \
                 mock.patch.object(self.driver.TermsSelector, "join", return_value=(["demo"], "mechanical")), \
                 mock.patch.object(self.driver.time, "sleep"), \
                 mock.patch.object(Path, "glob", return_value=iter([])):
                code = self.driver.main(self.argv(
                    "--no-terms-agent", "--seed-arxiv-ids", "2402.14207",
                ))
        self.assertEqual(code, 0)
        registry = next(c for c in self.commands if "build-candidate-registry" in " ".join(c))
        self.assertIn("--citation-result", registry)


class AbstractEvidenceStageTest(unittest.TestCase):
    """The abstract-evidence stage: registry metadata becomes positioning-only
    events (tier: abstract) under the run's event-ID prefix."""

    def setUp(self):
        self.driver = load_driver()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb_root = Path(self.tmp.name)
        self.run_dir = self.kb_root / "work" / "literature-review-demo-20260101"
        self.run_dir.mkdir(parents=True)
        (self.run_dir / "run.json").write_text(
            json.dumps({"status": "in-progress", "topic": "demo"}), encoding="utf-8"
        )
        (self.run_dir / "candidate-registry.json").write_text(json.dumps({
            "candidate_count": 3,
            "candidates": [
                {"arxiv_id": "2402.10329", "title": "UMI", "summary": "Universal manipulation interface. It collects data with a gripper.",
                 "authors": ["Alice"], "published": "2024-02-01"},
                {"arxiv_id": "2302.01109", "title": "No abstract candidate"},
                {"arxiv_id": "2311.18259", "title": "Ego-Exo4D", "summary": "Ego-exo dataset.", "authors": []},
            ],
        }), encoding="utf-8")
        self.args = self.driver.parse_args([
            "--run-dir", str(self.run_dir), "--topic", "demo topic",
        ])
        self.summary: dict = {}

    def run_stage(self):
        self.driver.abstract_evidence_stage(
            self.kb_root, self.run_dir, self.run_dir / "run.json",
            ["EA-SENSOR"], self.args, self.summary,
        )

    def events(self) -> list[dict]:
        return [
            json.loads(line)
            for line in (self.run_dir / "evidence" / "abstract-tier.jsonl")
            .read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_projects_registry_metadata_with_claimed_prefix(self):
        self.run_stage()
        events = self.events()
        self.assertEqual(len(events), 2)  # the no-abstract candidate is skipped
        prefix = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))["event_prefix"]
        self.assertEqual([event["event_id"] for event in events], [f"{prefix}-0001", f"{prefix}-0002"])
        self.assertEqual({event["tier"] for event in events}, {"abstract"})
        self.assertEqual({event["stance"] for event in events}, {""})
        self.assertEqual(events[0]["topic_id"], "EA-SENSOR")
        self.assertEqual(self.summary["abstract_events"], 2)

    def test_idempotent_on_existing_output(self):
        self.run_stage()
        first = (self.run_dir / "evidence" / "abstract-tier.jsonl").read_text(encoding="utf-8")
        self.summary.clear()
        self.run_stage()
        self.assertEqual(
            (self.run_dir / "evidence" / "abstract-tier.jsonl").read_text(encoding="utf-8"), first
        )
        self.assertEqual(self.summary["abstract_events"], 2)

    def test_stamp_counts_abstract_papers_separately(self):
        """event_count is the whole set; evidence_papers (the cited-paper floor
        input) stays full-text-only and abstract_papers records the rest."""
        evidence_dir = self.run_dir / "evidence"
        evidence_dir.mkdir()
        (evidence_dir / "p1.jsonl").write_text(
            json.dumps({"event_id": "EA-DEMO-2026-0042"}) + "\n", encoding="utf-8"
        )
        (evidence_dir / "p2.jsonl").write_text("", encoding="utf-8")
        (evidence_dir / "abstract-tier.jsonl").write_text(
            "\n".join(
                json.dumps({"event_id": f"EA-DEMO-2026-{seq:04d}", "tier": "abstract",
                            "paper": {"arxiv_id": arxiv_id}})
                for seq, arxiv_id in ((1, "2402.10329"), (2, "2402.10329"), (3, "2311.18259"))
            ) + "\n",
            encoding="utf-8",
        )
        self.driver._stamp_evidence_scale(
            self.kb_root, self.run_dir / "run.json", evidence_dir, 4
        )
        manifest = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["event_count"], 4)  # deep read + abstract
        self.assertEqual(manifest["evidence_papers"], 1)  # empty p2 ignored
        self.assertEqual(manifest["abstract_papers"], 2)  # 2402.10329 deduplicated

    def test_stamp_without_abstract_tier(self):
        evidence_dir = self.run_dir / "evidence"
        evidence_dir.mkdir()
        self.driver._stamp_evidence_scale(
            self.kb_root, self.run_dir / "run.json", evidence_dir, 0
        )
        manifest = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["abstract_papers"], 0)


if __name__ == "__main__":
    unittest.main()

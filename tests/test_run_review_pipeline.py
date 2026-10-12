"""Tests for scripts/run_review_pipeline.py — the mechanical-stage driver.

Network is fully mocked: every pipeline script invocation goes through a fake
``run_command``/``Popen`` seam, so the assertions here are about command
shapes, stage ordering, idempotent skipping, and the summary payload.
"""

from __future__ import annotations

import importlib.util
import json
import os
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
        self.assertEqual(summary["screening_limit"], 80)  # rapid
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

    def test_driver_emits_per_stage_result_briefs(self):
        """Each mechanical stage closes with a [DRIVER-BRIEF:<stage>] JSON
        block — the human-checkable work product (query list, selected papers,
        deep-read outcomes…) the wiki dialog renders as 成果简报."""
        import contextlib
        import io

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.run_driver(self.argv("--no-terms-agent"))
        brief_lines = [
            line for line in buffer.getvalue().splitlines()
            if line.startswith("[DRIVER-BRIEF:")
        ]
        stages = [line.split("]", 1)[0].split(":", 1)[1] for line in brief_lines]
        for expected in ("plan", "retrieval", "selection", "summary"):
            self.assertIn(expected, stages)
        plan_line = next(line for line in brief_lines if line.startswith("[DRIVER-BRIEF:plan]"))
        payload = json.loads(plan_line.split("] ", 1)[1])
        self.assertIn("查询计划", payload["title"])
        self.assertTrue(payload["lines"])

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
        self.assertEqual(screen[screen.index("--limit") + 1], "80")
        self.assertIn("--terms", screen)  # English terms augment the bm25/smart query
        self.assertFalse(any("screen-candidates" in " ".join(c) for c in self.commands))

    def test_screening_uses_terms_and_mode_limit(self):
        """The keywords strategy keeps the legacy term-matching screen."""
        self.run_driver(self.argv("--no-terms-agent", "--selection-strategy", "keywords"))
        screen = next(c for c in self.commands if "screen-candidates" in " ".join(c))
        self.assertIn("demo", screen[screen.index("--terms") + 1].split(","))
        self.assertEqual(screen[screen.index("--limit") + 1], "80")
        self.assertFalse(any("select-candidates" in " ".join(c) for c in self.commands))
        scoping = self.run_driver(self.argv("--no-terms-agent", "--review-mode", "scoping"))
        self.assertEqual(scoping[1]["screening_limit"], 120)
        self.assertEqual(self.driver.DEEP_READ_LIMITS, {"rapid": 12, "scoping": 22, "systematic": 43})
        self.assertEqual(self.driver.EVIDENCE_FLOORS, {"rapid": 8, "scoping": 15, "systematic": 30})

    def test_deep_read_limit_defaults_to_mode(self):
        """Deep-read throughput is mode-aware by default (the fixed default 10
        starved scoping reviews down to 7 citable papers in real runs)."""
        self.assertIsNone(self.driver.parse_args(self.argv()).deep_read_limit)
        self.assertEqual(self.driver.DEEP_READ_LIMITS, {"rapid": 12, "scoping": 22, "systematic": 43})

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

    def test_deep_read_order_without_limit_is_the_waitlist_pool(self):
        """limit=None returns the full scored order so the 候补 fill can walk
        past the first cut in the same ranking (2026-10-10)."""
        full = self.driver.deep_read_order(["a", "b", "c", "d"], ["c"], limit=None)
        self.assertEqual(full, ["c", "a", "b", "d"])
        self.assertEqual(full[2:], ["b", "d"])  # the 候补 tail

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

    def test_latin_terms_become_one_conjunctive_query_not_bare_words(self):
        """机械拉丁词合成一条 AND 查询：单词裸查询（absolute/pose/estimation）
        会灌垃圾进候选池（20260930 绝对位姿 run 池里大半是高能物理/量子/NLP）。"""
        self.run_driver(self.argv("--no-terms-agent"))
        dyn = json.loads((self.run_dir / "dynamic-queries.json").read_text(encoding="utf-8"))
        queries = [str(item.get("query") or "") for item in dyn.get("queries") or []]
        # 没有任何裸单词查询（无空格且非 all: 语法的条目）
        bare = [q for q in queries if q and " " not in q and not q.startswith("all:")]
        self.assertEqual(bare, [], f"bare word queries leaked: {bare}")
        combined = [q for q in queries if q.count(" AND ") >= 1]
        self.assertTrue(combined, "expected a conjunctive latin-combined query")
        self.assertIn("latin-combined", [str(item.get("label") or "") for item in dyn.get("queries") or []])

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


class StructuralSaturationTest(unittest.TestCase):
    """Saturation is MEASURED as diminishing returns across rounds — never
    asserted. Discovery rounds are 100% new by construction; the driver earns
    a passing verdict by appending low-novelty recall rounds as the tail
    (2026-10-10: an earlier structural auto-pass just silenced the alarm)."""

    def _plan(self):
        return {
            "review_mode": "scoping",
            "search_targets": {"candidate_floor": 2, "full_text_floor": 1, "accepted_paper_floor": 1},
            "coverage_dimensions": [],
            "stopping_rule": {
                "minimum_batches": 3,
                "saturation_rounds": 2,
                "max_new_unique_rate": 0.10,
            },
        }

    def _registry(self, batches):
        return {"candidates": [{"arxiv_id": f"p{i}"} for i in range(20)], "batches": batches}

    def test_discovery_tail_alone_is_not_saturated(self):
        """Two disjoint discovery rounds cannot show diminishing returns —
        the judge must NOT call that saturated (the old auto-pass bug)."""
        from embodied_learning.search import coverage

        plan = self._plan()
        registry = self._registry([
            {"batch": "r1", "channel": "arxiv-api", "candidate_ids": [f"a{i}" for i in range(10)]},
            {"batch": "r2", "channel": "citation-graph", "candidate_ids": [f"c{i}" for i in range(10)]},
        ])
        result = coverage.assess(plan, registry, [])
        self.assertFalse(result["stop_assessment"]["checks"]["saturation"])

    def test_recall_tail_measures_saturation(self):
        """Discovery → recall tail: the tail re-finds known papers, so its
        new_unique_rate is low and the judge can honestly pass."""
        from embodied_learning.search import coverage

        plan = self._plan()
        registry = self._registry([
            {"batch": "plan-r1", "channel": "arxiv-api", "candidate_ids": [f"a{i}" for i in range(10)]},
            {"batch": "citation-seeds", "channel": "citation-graph", "candidate_ids": [f"c{i}" for i in range(10)]},
            {"batch": "recall-author-r3", "channel": "arxiv-api", "candidate_ids": [f"a{i}" for i in range(6)]},
            {"batch": "recall-title-r4", "channel": "arxiv-api", "candidate_ids": [f"a{i}" for i in range(4)]},
        ])
        result = coverage.assess(plan, registry, [])
        self.assertTrue(result["stop_assessment"]["checks"]["saturation"])
        self.assertEqual(result["saturation_kind"], "measured")

    def test_repeat_channel_still_100pct_new_is_not_saturated(self):
        from embodied_learning.search import coverage

        plan = self._plan()
        registry = self._registry([
            {"batch": "r1", "channel": "arxiv-api", "candidate_ids": [f"a{i}" for i in range(10)]},
            {"batch": "r2", "channel": "arxiv-api", "candidate_ids": [f"b{i}" for i in range(10)]},
            {"batch": "r3", "channel": "arxiv-api", "candidate_ids": [f"c{i}" for i in range(10)]},
        ])
        result = coverage.assess(plan, registry, [])
        self.assertFalse(result["stop_assessment"]["checks"]["saturation"])


class RecallQueryTest(unittest.TestCase):
    """Recall rounds derive queries mechanically from already-found papers —
    no agent, cheap, and low-novelty by construction (the saturation tail)."""

    def setUp(self):
        self.driver = load_driver()
        self.papers = [
            {"title": "Reflexion: language agents with verbal reinforcement learning",
             "authors": ["Noah Shinn", "Federico Cassano", "Shunyu Yao"]},
            {"title": "Self-Refine: Iterative Refinement with Self-Feedback",
             "authors": ["Aman Madaan", "Noah Shinn"]},
            {"title": "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering",
             "authors": ["John Yang", "Noah Shinn"]},
            {"title": "The AI Scientist",
             "authors": ["Chris Lu"]},  # short title → title round skips it
        ]

    def test_author_recall_targets_recurrent_authors(self):
        queries = self.driver.recall_author_queries(self.papers, limit=5)
        labels = [q["label"] for q in queries]
        self.assertEqual(len(queries), 5)  # 6 unique names, cap 5
        self.assertTrue(all(q["query"].startswith('au:"') for q in queries))
        self.assertIn("recall-author-1", labels)
        # Most-represented author first.
        self.assertIn("Noah Shinn", queries[0]["query"])

    def test_author_recall_scopes_to_topic(self):
        """An unscoped au: harvests every paper the author ever wrote (0.92
        new-rate, not a tail). The English-term clause keeps it a recall —
        and a pure-Chinese topic must still get a scope from the terms list."""
        queries = self.driver.recall_author_queries(
            self.papers, terms=["automated", "research", "agents"], limit=3)
        self.assertIn(" AND (", queries[0]["query"])
        self.assertIn("all:automated", queries[0]["query"])

    def test_author_recall_chinese_topic_without_terms_is_unscoped(self):
        """No Latin tokens and no terms list → empty scope (honest), and the
        caller is expected to pass the English retrieval terms instead."""
        queries = self.driver.recall_author_queries(self.papers, terms="自动化研究", limit=2)
        self.assertNotIn(" AND (", queries[0]["query"])

    def test_title_recall_uses_distinctive_phrases(self):
        queries = self.driver.recall_title_queries(self.papers, limit=5)
        self.assertGreaterEqual(len(queries), 2)  # "The AI Scientist" is too short
        self.assertTrue(all(q["query"].startswith('ti:"') for q in queries))
        # Phrases come from title content words, not stopwords.
        self.assertNotIn("the ", queries[0]["query"].lower())

    def test_known_works_probes_exact_titles_with_seeds_first(self):
        """Exact-title probes re-find the paper itself — the reliable
        low-novelty tail. Seeds are forced to the front."""
        papers = [
            {"arxiv_id": "2303.11366", "title": "Reflexion: language agents with verbal reinforcement learning"},
            {"arxiv_id": "2408.06292", "title": "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"},
            {"arxiv_id": "2501.04227", "title": "Agent Laboratory: Using LLM Agents as Research Assistants"},
        ]
        queries = self.driver.known_works_queries(papers, seeds=["2408.06292"], limit=3)
        self.assertEqual(len(queries), 3)
        self.assertIn("The AI Scientist", queries[0]["query"])
        self.assertTrue(all(q["query"].startswith('ti:"') and q["query"].endswith('"') for q in queries))

    def test_recall_skips_tiny_pools(self):
        self.assertEqual(self.driver.recall_author_queries([]), [])
        self.assertEqual(self.driver.recall_title_queries([]), [])
        self.assertEqual(self.driver.known_works_queries([]), [])

    def test_write_round_queries_labels_the_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "q.json"
            self.driver.write_round_queries(
                path, [{"label": "x", "query": 'au:"A B"'}], batch_label="recall-author")
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["batch"], "recall-author")
            self.assertEqual(payload["queries"][0]["query"], 'au:"A B"')


class GateReportTest(unittest.TestCase):
    """log_gates is the stage-end mirror of the finalize gate table: cheap
    enough to run at every stage boundary and again at settle."""

    def test_log_gates_names_remedy_for_failures(self):
        driver = load_driver()
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "coverage-report.json"
            report.write_text(json.dumps({
                "targets": {"candidate_floor": 100, "full_text_floor": 35, "accepted_paper_floor": 15},
                "observed": {"candidate_count": 465, "full_text_recovered_count": 34, "accepted_evidence_paper_count": 12},
                "saturation_kind": "measured",
                "stop_assessment": {"checks": {
                    "candidate_floor": True,
                    "full_text_floor": False,
                    "accepted_paper_floor": False,
                    "coverage_dimensions": True,
                    "saturation": True,
                }},
            }), encoding="utf-8")
            with mock.patch.object(driver, "log") as logger:
                driver.log_gates(report, "抽取后")
            lines = [str(call.args[0]) for call in logger.call_args_list]
            joined = "\n".join(lines)
            self.assertIn("DRIVER-GATES:抽取后", joined)
            self.assertIn("full_text_floor", joined)
            self.assertIn("34/35", joined)
            self.assertIn("抽取重试可补", joined)
            self.assertIn("saturation_kind=measured", joined)
            # passing gates are summarized, not listed one-by-one
            self.assertNotIn("未过 candidate_floor", joined)

    def test_log_gates_silent_on_missing_report(self):
        driver = load_driver()
        with mock.patch.object(driver, "log") as logger:
            driver.log_gates(Path("/nonexistent/coverage-report.json"), "检索后")
        logger.assert_not_called()


class InputsNewerThanTest(unittest.TestCase):
    """Stages must rebuild when their INPUTS change, not only when outputs
    are missing — a registry built from r1 must be rebuilt after a recall
    round lands, or the new batch never reaches the saturation judge."""

    def test_newer_input_triggers_rebuild(self):
        driver = load_driver()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "registry.json"
            src = Path(tmp) / "search-recall.json"
            out.write_text("{}", encoding="utf-8")
            self.assertFalse(driver.inputs_newer_than(out, [src]))  # src missing
            src.write_text("{}", encoding="utf-8")
            os.utime(out, (1, 1))  # output older than input
            os.utime(src, (9_000_000_000, 9_000_000_000))
            self.assertTrue(driver.inputs_newer_than(out, [src]))

    def test_older_input_does_not_rebuild(self):
        driver = load_driver()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "registry.json"
            src = Path(tmp) / "search-r1.json"
            src.write_text("{}", encoding="utf-8")
            out.write_text("{}", encoding="utf-8")
            os.utime(src, (1, 1))
            os.utime(out, (9_000_000_000, 9_000_000_000))
            self.assertFalse(driver.inputs_newer_than(out, [src]))

    def test_missing_output_rebuilds(self):
        driver = load_driver()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "registry.json"
            src = Path(tmp) / "search-r1.json"
            src.write_text("{}", encoding="utf-8")
            self.assertTrue(driver.inputs_newer_than(out, [src]))


if __name__ == "__main__":
    unittest.main()

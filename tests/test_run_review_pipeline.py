"""Tests for scripts/run_review_pipeline.py — the mechanical-stage driver.

Network is fully mocked: every pipeline script invocation goes through a fake
``run_command``/``Popen`` seam, so the assertions here are about command
shapes, stage ordering, idempotent skipping, and the summary payload.
"""

from __future__ import annotations

from _entry import invoke, parse

import importlib.util
import inspect
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def load_driver():
    # Load the implementation module (not the scripts/ forwarder) so
    # mock.patch on module attributes reaches the live globals.
    import importlib

    return importlib.import_module("embodied_learning.wiki.run.driver")


class TermsTest(unittest.TestCase):
    def setUp(self):
        self.driver = load_driver()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = mock.patch.dict(
            os.environ, {"EMBODIED_CONVERSATION_STORE": str(Path(self.tmp.name) / "store")}
        )
        env.start()
        self.addCleanup(env.stop)

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

    def test_terms_selector_prefers_precomputed_fallback_terms(self):
        # The caller already merged a translation into the mechanical terms; a
        # second mechanical pass over the raw Chinese topic would drop back to
        # CJK tokens that English titles never match.
        selector = self.driver.TermsSelector(
            "强化学习", "", use_agent=False, timeout_s=1.0, cli="/fake/claude",
            fallback_terms=["reinforcement", "learning", "强化学习"],
        )
        selector.start()
        terms, source = selector.join()
        self.assertEqual(source, "mechanical")
        self.assertEqual(terms, ["reinforcement", "learning", "强化学习"])

    def test_translation_terms_merges_english_with_topic_tokens(self):
        # Merge, never replace: the topic's own tokens stay in the list (call
        # sites filter to Latin where it matters), English first so the 12-cap
        # and the recall scope clause prefer them.
        with mock.patch.object(self.driver, "translate_text", return_value="reinforcement learning"):
            terms, translated = self.driver.translation_terms("强化学习", "")
        self.assertEqual(translated, "reinforcement learning")
        self.assertEqual(terms, ["reinforcement", "learning", "强化学习"])

    def test_translation_terms_passthrough_when_latin_present_or_unavailable(self):
        with mock.patch.object(self.driver, "translate_text", return_value="image segmentation") as called:
            terms, translated = self.driver.translation_terms("图像分割 Gaussian", "")
        self.assertEqual(translated, "")
        self.assertEqual(terms, ["gaussian"])
        called.assert_not_called()  # already has Latin tokens — no network call

        with mock.patch.object(self.driver, "translate_text", return_value=None):
            terms, translated = self.driver.translation_terms("点云去动态", "")
        self.assertEqual(translated, "")
        self.assertEqual(terms, ["点云去动态"])


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
        self.assertEqual(self.driver.command_label(["/usr/bin/python3", "/x/read.py", "build-paper-note"]), "read.py build-paper-note")


class DriverPipelineTest(unittest.TestCase):
    """End-to-end driver run with every subprocess faked onto disk."""

    def setUp(self):
        self.driver = load_driver()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # The usage/trace ledger is machine-local; keep test runs out of the
        # real ~/.claude/projects archive.
        env = mock.patch.dict(
            os.environ, {"EMBODIED_CONVERSATION_STORE": str(Path(self.tmp.name) / "store")}
        )
        env.start()
        self.addCleanup(env.stop)
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
        "review-packet": ("review-packet.md", "writing-brief.md", "evidence-appendix.md"),
    }

    def _stage_payload(self, script: str) -> str:
        # coverage_dimensions + search_targets must be present: the driver's
        # refresh_coverage_inplace() recomputes coverage-report.json through the
        # REAL assess() at every stage end, so a plan without them would report
        # every dimension failed and disagree with this fixture's payload.
        plan = {
            "knowledge_ids": ["EA-SENSOR"],
            "queries": [{"label": "a", "query": "all:demo"}],
            "coverage_dimensions": [
                {"dimension": "direct-topic", "query_labels": ["a"],
                 "minimum_unique_candidates": 0},
            ],
            "search_targets": {
                "candidate_floor": 0, "full_text_floor": 0, "accepted_paper_floor": 0,
            },
        }
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
                    "strategy": "smart-jev",
                    "detail": "smart-jev selected 2/42 considered; kept those above 0.60 (jev)",
                },
                "candidates": [],
            },
            "assess-review-coverage": coverage,
            "extract-content-queue": {"paper_count": 2},
            "review-packet": {"packet": "mechanical"},
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
        if "screen-candidates" in joined or "select-candidates" in joined:
            # streaming stage: per-chunk progress + the screening outputs.
            # select-candidates carries selection_rule.detail; screen-candidates
            # is the legacy term-match path with a bare payload.
            script = "select-candidates" if "select-candidates" in joined else "screen-candidates"
            for name in self.STAGE_SCRIPTS["screen-candidates"]:
                out = self.run_dir / name
                out.parent.mkdir(parents=True, exist_ok=True)
                if name == "screening-ids.txt":
                    out.write_text("2402.10329\n2402.10330\n", encoding="utf-8")
                else:
                    out.write_text(self._stage_payload(script), encoding="utf-8")
            return mock.Mock(
                stdout=iter(["chunk 1/2: judging 3 of 3 candidates…", "chunk 2/2: judging 0 of 3 candidates…"]),
                wait=lambda timeout=None: 0,
            )
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

    def run_driver(self, argv: list[str], *, agent_dynamic=None, fake_run=None,
                   translate_en=None, system_one: bool = True) -> tuple[int, dict]:
        """agent_dynamic=None keeps the default patch (agent returns None);
        pass a Mock to observe/override the dynamic-query agent. fake_run
        overrides the stage-subprocess fake (e.g. to write an empty plan).
        translate_en is the MyMemory stand-in (default None = translation
        unavailable, so tests never touch the network). system_one=True is the
        default patch for the decision-model preflight (smart-jev is the CLI
        default); pass False to exercise the fail-fast path. The driver's
        stderr is captured on ``self.last_stderr``; a failed pipeline writes no
        pipeline-summary.json, so the summary is ``{}``."""
        agent_patch = (
            mock.patch.object(self.driver, "agent_dynamic_queries", return_value=None)
            if agent_dynamic is None
            else mock.patch.object(self.driver, "agent_dynamic_queries", new=agent_dynamic)
        )
        stderr = io.StringIO()
        with mock.patch.object(self.driver, "run_command", side_effect=fake_run or self.fake_run), \
             mock.patch.object(self.driver.subprocess, "Popen", side_effect=self.fake_popen), \
             mock.patch.object(self.driver.TermsSelector, "join", return_value=(["demo"], "mechanical")), \
             mock.patch.object(self.driver, "translate_text", return_value=translate_en), \
             mock.patch("embodied_learning.harness.claude.system_one_ready", return_value=system_one), \
             agent_patch, \
             mock.patch.object(self.driver.time, "sleep"), \
             mock.patch.object(Path, "glob", return_value=iter([])), \
             mock.patch.object(sys, "stderr", stderr):
            code = invoke("run.py", "pipeline", argv)
        self.last_stderr = stderr.getvalue()
        summary_path = self.run_dir / "pipeline-summary.json"
        summary = (
            json.loads(summary_path.read_text(encoding="utf-8"))
            if summary_path.is_file()
            else {}
        )
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
        self.assertNotIn("screening_limit", summary)
        self.assertEqual(summary["selection_strategy"], "smart-jev")
        self.assertIn("smart-jev selected", summary["selection_detail"])
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
        self.assertEqual(manifest["selection_strategy"], "smart-jev")

    def test_driver_writes_funnel_artifact(self):
        """The funnel is a run artifact: derived from disk, listed in the
        summary, and self-contained enough to publish."""
        code, summary = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        funnel_path = self.run_dir / "funnel.json"
        self.assertTrue(funnel_path.is_file())
        funnel = json.loads(funnel_path.read_text(encoding="utf-8"))
        self.assertEqual(funnel["schema_version"], 1)
        # The fixture registry carries only a count — the stage still knows it.
        self.assertEqual(funnel["stages"]["candidates"], 42)
        self.assertEqual(funnel["stages"]["screened"], 2)
        self.assertEqual(funnel["stages"]["deep_read"], 2)
        self.assertEqual(funnel["detail"]["abstract_basis"], "screened")
        self.assertEqual(funnel["detail"]["deep_read_failed"], 2)
        self.assertEqual(summary["artifacts"]["funnel"], "funnel.json")
        self.assertIn("funnel", summary["stage_seconds"])

    def test_driver_writes_one_run_ledger_with_stage_trace(self):
        """Every mechanical stage appends step + metric lines to ONE pipeline
        ledger (usage-records-format trace layer), so a run's trajectory is
        one file and its stages are machine-readable."""
        code, _ = self.run_driver(self.argv("--no-terms-agent"))
        self.assertEqual(code, 0)
        ledgers = list((Path(self.tmp.name) / "store").glob("usage-pipeline-*.jsonl"))
        self.assertEqual(len(ledgers), 1)
        entries = [
            json.loads(line)
            for line in ledgers[0].read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        stages = {
            entry.get("attrs", {}).get("stage")
            for entry in entries
            if entry.get("kind") == "step"
        }
        for expected in ("pipeline", "plan", "registry", "screening", "coverage", "extraction"):
            self.assertIn(expected, stages)
        metrics = [
            entry for entry in entries
            if entry.get("kind") == "metric"
            and entry.get("attrs", {}).get("stage") == "pipeline"
        ]
        self.assertEqual(len(metrics), 1)
        self.assertIn("stage_seconds", metrics[0]["attrs"])

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

    def test_selection_strategy_defaults_to_smart_jev(self):
        args = parse("run.py", "pipeline", self.argv())
        self.assertEqual(args.selection_strategy, "smart-jev")
        self.assertEqual(
            sorted(self.driver.SELECTION_STRATEGIES),
            ["bm25", "influence", "keywords", "smart", "smart-jev"],
        )

    def test_default_selection_strategy_dispatches_select_candidates(self):
        """Default (smart-jev): screening goes through search.py select-candidates
        with the registry + topic + focus; the terms thread still runs but the
        screening command does not consume it."""
        self.run_driver(self.argv("--no-terms-agent"))
        screen = next(c for c in self.commands if "select-candidates" in " ".join(c))
        self.assertIn("--registry", screen)
        self.assertEqual(screen[screen.index("--strategy") + 1], "smart-jev")
        self.assertIn("--selection-threshold", screen)
        self.assertEqual(screen[screen.index("--topic") + 1], "demo topic ERASOR")
        self.assertNotIn("--limit", screen)  # selection never truncates
        self.assertIn("--terms", screen)  # English terms augment the bm25/smart query
        self.assertFalse(any("screen-candidates" in " ".join(c) for c in self.commands))

    def test_smart_selection_forwards_the_execution_model(self):
        """The card's 执行模型 reaches select-candidates --complete-model; the
        decision-model strategy must not inherit it."""
        self.run_driver(
            self.argv("--no-terms-agent", "--selection-strategy", "smart",
                      "--selection-model", "deepseek-v4-flash-vision-exp")
        )
        screen = next(c for c in self.commands if "select-candidates" in " ".join(c))
        self.assertEqual(screen[screen.index("--strategy") + 1], "smart")
        self.assertEqual(
            screen[screen.index("--complete-model") + 1], "deepseek-v4-flash-vision-exp"
        )

    def test_smart_jev_forwards_threshold_not_complete_model(self):
        with mock.patch(
            "embodied_learning.harness.claude.system_one_ready", return_value=True
        ):
            self.run_driver(
                self.argv("--no-terms-agent", "--selection-strategy", "smart-jev",
                          "--selection-model", "ignored", "--selection-threshold", "0.55")
            )
        screen = next(c for c in self.commands if "select-candidates" in " ".join(c))
        self.assertEqual(screen[screen.index("--strategy") + 1], "smart-jev")
        self.assertEqual(screen[screen.index("--selection-threshold") + 1], "0.55")
        self.assertNotIn("--complete-model", screen)

    def test_smart_jev_fails_fast_before_retrieval_when_unconfigured(self):
        """An unconfigured decision model must stop the driver up front — not
        after a paid retrieval/registry round, and never as silent downtime.
        This is also the default strategy's preflight: no flag needed."""
        code, summary = self.run_driver(self.argv("--no-terms-agent"), system_one=False)
        self.assertEqual(code, 2)
        self.assertEqual(self.commands, [])
        self.assertEqual(summary, {})
        self.assertIn("决策模型", self.last_stderr)

    def test_screening_uses_terms_and_has_no_mode_limit(self):
        """The keywords strategy keeps the legacy term-matching screen, but it
        queues every match — deep reading owns the funnel's only truncation."""
        self.run_driver(self.argv("--no-terms-agent", "--selection-strategy", "keywords"))
        screen = next(c for c in self.commands if "screen-candidates" in " ".join(c))
        self.assertIn("demo", screen[screen.index("--terms") + 1].split(","))
        self.assertNotIn("--limit", screen)
        self.assertFalse(any("select-candidates" in " ".join(c) for c in self.commands))
        scoping = self.run_driver(self.argv("--no-terms-agent", "--review-mode", "scoping"))
        self.assertNotIn("screening_limit", scoping[1])
        self.assertEqual(self.driver.DEEP_READ_LIMITS, {"rapid": 12, "scoping": 22, "systematic": 43})
        self.assertEqual(self.driver.EVIDENCE_FLOORS, {"rapid": 8, "scoping": 15, "systematic": 30})

    def test_deep_read_limit_defaults_to_mode(self):
        """Deep-read throughput is mode-aware by default (the fixed default 10
        starved scoping reviews down to 7 citable papers in real runs)."""
        self.assertIsNone(parse("run.py", "pipeline", self.argv()).deep_read_limit)
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

    def test_evidence_floor_counts_projection_units_not_reads(self):
        """needs-review papers must not count toward the floor that triggers
        the 候补 fill. The projector now emits each passing card (2026-10-15),
        but a needs-review paper is only projectable if at least one card
        passed — at deep-read time that is unknown, so the floor counter stays
        conservative. Regression (2026-10-14 时空智能体): 13 pass + 6
        needs-review read as "19 ≥ 15", the fill never ran, and the run
        stopped at 13/15."""
        self.assertEqual(self.driver.projection_units(13, 6), 13)
        self.assertEqual(self.driver.projection_units(15, 0), 15)
        self.assertEqual(self.driver.projection_units(0, 30), 0)
        # The 2026-10-14 shape must now be under the scoping floor of 15.
        self.assertLess(self.driver.projection_units(13, 6), self.driver.EVIDENCE_FLOORS["scoping"])
        # And a real pass must satisfy it without padding from needs-review.
        self.assertGreaterEqual(self.driver.projection_units(15, 6), self.driver.EVIDENCE_FLOORS["scoping"])

    def test_projection_skips_unaudited_cards_so_floor_must_not_count_them(self):
        """Pin the two halves of the contract together: the projector keeps a
        paper's passing cards when one card is needs-review (card-level gate,
        2026-10-15 纹理映射: 5 papers lost 3-4 passing cards each), and the
        driver's floor counter still counts only full-pass papers so the 候补
        fill is not skipped on a maybe (2026-10-14 时空智能体)."""
        from embodied_learning.knowledge import evidence_projection

        source = inspect.getsource(evidence_projection.project)
        self.assertIn('(audit_cards.get(card_id) or {}).get("status") != "pass"', source)
        self.assertIn("continue", source)
        self.assertNotIn('raise ValueError("projection requires a passing claim-support audit")', source)
        self.assertNotIn('raise ValueError(f"card {card_id} is not pass in the audit")', source)
        # The counter is the projection unit — never `passed + needs_review`.
        source = inspect.getsource(self.driver.projection_units)
        self.assertIn("return int(passed)", source)
        self.assertNotIn("passed + needs_review", source)

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

    def test_extraction_uses_the_shared_kb_cache(self):
        """Full text is cached under <kb-root>/.cache, not /tmp: a paper fetched
        by an earlier run or a quick-read is reused, and sibling machines on
        the same KB mount see the cache."""
        self.run_driver(self.argv("--no-terms-agent"))
        extraction = next(c for c in self.commands if "extract-content-queue" in " ".join(c))
        html_dir = extraction[extraction.index("--html-cache-dir") + 1]
        pdf_dir = extraction[extraction.index("--pdf-cache-dir") + 1]
        self.assertEqual(html_dir, str(Path(self.tmp.name) / ".cache" / "html"))
        self.assertEqual(pdf_dir, str(Path(self.tmp.name) / ".cache" / "pdfs"))

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
        code = invoke("run.py", "pipeline", [
            "--run-dir", str(self.run_dir.parent / "nope"),
            "--topic", "x", "--no-terms-agent",
        ])
        self.assertEqual(code, 2)

    def test_bad_time_range_rejected(self):
        code = invoke("run.py", "pipeline", [
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

    def test_dynamic_agent_output_repairs_truncated_head(self):
        """The completion channel occasionally drops the first bytes of the
        response (2026-10-13/14/15 runs arrived as ``queries":[{…`` / ``":[{…``
        instead of ``{"queries":[{…``). The extractor must repair the wrapper
        instead of discarding 20 good queries."""
        body = '{"label": "direct-anchor", "tier": "direct", "query": "all:\\"rl\\"", "why": "w"}]}'
        for truncated in (
            "queries\":[" + body,   # missing {"
            "\":[" + body,          # missing {"queries
            "[" + body,             # missing {"queries":
            body,                   # missing {"queries": [ — first element only
        ):
            payload = self.driver.extract_dynamic_queries_json(truncated)
            self.assertIsNotNone(payload, msg=repr(truncated))
            self.assertEqual(payload["queries"][0]["query"], 'all:"rl"', msg=repr(truncated))

    def test_dynamic_agent_output_accepts_fences_and_bare_list(self):
        fenced = '```json\n{"queries": [{"label": "x", "tier": "direct", "query": "q", "why": "w"}]}\n```'
        self.assertEqual(self.driver.extract_dynamic_queries_json(fenced)["queries"][0]["label"], "x")
        bare = '[{"label": "y", "tier": "direct", "query": "all:y", "why": "w"}]'
        self.assertEqual(self.driver.extract_dynamic_queries_json(bare)["queries"][0]["label"], "y")
        self.assertIsNone(self.driver.extract_dynamic_queries_json('{"queries": [{"label": "x"}]}'))

    def test_dynamic_agent_retries_unparseable_output(self):
        # Mode seen 2026-10-15 (VGGT run): a bare unquoted "query" value makes
        # the payload invalid JSON; a second call lands.
        bad = mock.Mock(
            returncode=0, stderr="",
            stdout='{"queries": [{"label": "x", "query": (all:a OR all:b), "why": "w"}]}',
        )
        good = mock.Mock(
            returncode=0, stderr="",
            stdout='{"queries": [{"label": "direct-x", "tier": "direct", "query": "all:rl"}]}',
        )
        with mock.patch.object(self.driver, "complete", side_effect=[bad, good]) as complete, \
             mock.patch.object(self.driver, "log") as logs:
            payload = self.driver.agent_dynamic_queries("强化学习", "", [], 5.0, "/fake/claude")
        self.assertEqual(payload["queries"][0]["label"], "direct-x")
        self.assertEqual(complete.call_count, 2)
        joined = " ".join(str(call) for call in logs.call_args_list)
        self.assertIn("无法解析", joined)

    def test_dynamic_agent_retries_nonzero_exit_and_gives_up_loudly(self):
        def failing(command, **kwargs):
            return mock.Mock(returncode=1, stdout="", stderr="api error")

        with mock.patch.object(self.driver.subprocess, "run", side_effect=failing) as run, \
             mock.patch.object(self.driver, "log") as logs, \
             mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": self.tmp.name}):
            payload = self.driver.agent_dynamic_queries("主题", "", [], 5.0, "/fake/claude")
        self.assertIsNone(payload)
        self.assertEqual(run.call_count, 2)  # DYNAMIC_AGENT_ATTEMPTS total tries
        joined = " ".join(str(call) for call in logs.call_args_list)
        self.assertIn("退出 1", joined)

    def test_dynamic_agent_timeout_does_not_retry(self):
        def timing_out(command, **kwargs):
            raise self.driver.subprocess.TimeoutExpired(cmd="x", timeout=1)

        with mock.patch.object(self.driver.subprocess, "run", side_effect=timing_out) as run, \
             mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": self.tmp.name}):
            self.assertIsNone(self.driver.agent_dynamic_queries("主题", "", [], 5.0, "/fake/claude"))
        self.assertEqual(run.call_count, 1)

    def test_skeleton_agent_retries_unparseable_output(self):
        """2026-10-16 强化学习: 20/43 deep reads produced no skel-*.json at all
        — one-shot skeleton calls died on truncated streams. The skeleton
        agent retries parse/exit failures, timeouts and spawn failures
        differently: see the three dedicated tests below."""
        bad = mock.Mock(returncode=0, stderr="", stdout="stream cut mid-object {")
        good = mock.Mock(
            returncode=0, stderr="",
            stdout='{"arxiv_id": "2401.00001", "cards": []}',
        )
        with mock.patch.object(self.driver, "complete", side_effect=[bad, good]) as complete, \
             mock.patch.object(self.driver, "log") as logs:
            skeleton = self.driver.run_skeleton_agent("/fake/claude", "2401.00001", Path("/pool"), 5.0)
        self.assertEqual(skeleton["arxiv_id"], "2401.00001")
        self.assertEqual(complete.call_count, 2)
        joined = " ".join(str(call) for call in logs.call_args_list)
        self.assertIn("不可解析", joined)

    def test_skeleton_agent_retries_nonzero_exit_and_gives_up_loudly(self):
        # Not a stream-truncation error: that one is now healed INSIDE complete()
        # with a fallback-model switch (2026-10-20), so it would double the
        # driver-level SKELETON_AGENT_ATTEMPTS budget. This keeps the two retry
        # layers testable in isolation.
        def failing(command, **kwargs):
            return mock.Mock(returncode=1, stdout="", stderr="API Error: model blew up")

        with mock.patch.object(self.driver.subprocess, "run", side_effect=failing) as run, \
             mock.patch.object(self.driver, "log") as logs, \
             mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": self.tmp.name}):
            skeleton = self.driver.run_skeleton_agent("/fake/claude", "2401.00001", Path("/pool"), 5.0)
        self.assertIsNone(skeleton)
        self.assertEqual(run.call_count, 2)  # SKELETON_AGENT_ATTEMPTS total tries
        joined = " ".join(str(call) for call in logs.call_args_list)
        self.assertIn("exit 1", joined)

    def test_skeleton_agent_retries_timeout(self):
        """Deep reads run several agents at once; an overloaded upstream
        surfaces as a timeout, so a timeout gets the same retry budget as a
        broken stream. A spawn failure still fails fast (OSError below)."""
        def timing_out(command, **kwargs):
            raise self.driver.subprocess.TimeoutExpired(cmd="x", timeout=1)

        with mock.patch.object(self.driver.subprocess, "run", side_effect=timing_out) as run, \
             mock.patch.object(self.driver, "log") as logs, \
             mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": self.tmp.name}):
            self.assertIsNone(self.driver.run_skeleton_agent("/fake/claude", "2401.00001", Path("/pool"), 5.0))
        self.assertEqual(run.call_count, 2)  # SKELETON_AGENT_ATTEMPTS total tries
        joined = " ".join(str(call) for call in logs.call_args_list)
        self.assertIn("超时", joined)

    def test_skeleton_agent_timeout_then_success(self):
        bad = mock.Mock(returncode=0, stderr="", stdout="")
        good = mock.Mock(
            returncode=0, stderr="",
            stdout='{"arxiv_id": "2401.00001", "cards": []}',
        )
        def flaky(command, **kwargs):
            if flaky.calls == 0:
                flaky.calls += 1
                raise self.driver.subprocess.TimeoutExpired(cmd="x", timeout=1)
            return good

        flaky.calls = 0
        with mock.patch.object(self.driver.subprocess, "run", side_effect=flaky), \
             mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": self.tmp.name}):
            skeleton = self.driver.run_skeleton_agent("/fake/claude", "2401.00001", Path("/pool"), 5.0)
        self.assertEqual(skeleton["arxiv_id"], "2401.00001")

    def test_skeleton_agent_spawn_failure_fails_fast(self):
        with mock.patch.object(self.driver.subprocess, "run", side_effect=OSError("no cli")) as run, \
             mock.patch.dict(os.environ, {"EMBODIED_CONVERSATION_STORE": self.tmp.name}):
            self.assertIsNone(self.driver.run_skeleton_agent("/fake/claude", "2401.00001", Path("/pool"), 5.0))
        self.assertEqual(run.call_count, 1)  # retrying a missing CLI only burns the clock

    def test_empty_plan_without_seeds_stops_with_actionable_error(self):
        """2026-10-15 强化学习: agent output was unparseable, the pure-Chinese
        topic had no Latin tokens or seeds, and search-arxiv died on the empty
        plan with a misleading "outputs missing". Stop at the plan stage with
        what-is-missing guidance and drop the empty plan outputs so a retry
        re-plans instead of skipping on stale artifacts."""

        def empty_plan_run(command, timeout=None):
            self.commands.append(command)
            if "build-query-plan" in " ".join(command):
                plan = json.loads(self._stage_payload("build-query-plan"))
                plan["queries"] = []
                (self.run_dir / "query-plan.json").write_text(
                    json.dumps(plan), encoding="utf-8")
                (self.run_dir / "query-plan.md").write_text("# 0 queries\n", encoding="utf-8")
                return mock.Mock(returncode=0, stdout="", stderr="")
            return self.fake_run(command, timeout=timeout)

        code, summary = self.run_driver(
            ["--run-dir", str(self.run_dir), "--topic", "强化学习",
             "--review-mode", "rapid", "--time-range", "2023-01-01..2026-06-06",
             "--kb-root", str(self.tmp.name), "--no-terms-agent"],
            fake_run=empty_plan_run,
        )
        self.assertEqual(code, 1)
        self.assertIn("检索计划 0 条查询", self.last_stderr)
        self.assertIn("dynamic-queries.json", self.last_stderr)
        self.assertFalse(any("search-arxiv" in c for c in self.commands))
        self.assertFalse((self.run_dir / "query-plan.json").exists())
        self.assertFalse((self.run_dir / "query-plan.md").exists())

    def test_empty_plan_with_seeds_skips_keyword_retrieval(self):
        """With seed papers the citation channel can still feed the registry:
        an empty plan must skip search-arxiv (its empty-query guard would exit
        1) and let the seed/citation channel carry retrieval, not stop."""

        def empty_plan_run(command, timeout=None):
            self.commands.append(command)
            if "build-query-plan" in " ".join(command):
                plan = json.loads(self._stage_payload("build-query-plan"))
                plan["queries"] = []
                (self.run_dir / "query-plan.json").write_text(
                    json.dumps(plan), encoding="utf-8")
                (self.run_dir / "query-plan.md").write_text("# 0 queries\n", encoding="utf-8")
                return mock.Mock(returncode=0, stdout="", stderr="")
            return self.fake_run(command, timeout=timeout)

        code, summary = self.run_driver(
            ["--run-dir", str(self.run_dir), "--topic", "强化学习",
             "--review-mode", "rapid", "--time-range", "2023-01-01..2026-06-06",
             "--kb-root", str(self.tmp.name), "--no-terms-agent",
             "--seed-arxiv-ids", "2402.14207"],
            fake_run=empty_plan_run,
        )
        self.assertEqual(code, 0)
        self.assertFalse(any("search-arxiv" in c for c in self.commands))
        self.assertEqual(summary["seed_ids"], ["2402.14207"])

    def test_stale_empty_plan_replans_when_dynamic_queries_arrive(self):
        """Resume path (2026-10-15 强化学习): a failed run left an empty
        query-plan.json behind; a retry whose dynamic-query agent succeeds must
        re-run planning instead of skipping on the stale outputs and stranding
        the fresh dynamic-queries.json content outside the plan."""
        plan = json.loads(self._stage_payload("build-query-plan"))
        plan["queries"] = []
        (self.run_dir / "query-plan.json").write_text(json.dumps(plan), encoding="utf-8")
        (self.run_dir / "query-plan.md").write_text("# 0 queries\n", encoding="utf-8")

        agent = mock.Mock(return_value={"queries": [
            {"label": "direct-rl", "tier": "direct", "query": 'all:"reinforcement learning"'},
        ]})
        code, _ = self.run_driver(
            ["--run-dir", str(self.run_dir), "--topic", "强化学习",
             "--review-mode", "rapid", "--time-range", "2023-01-01..2026-06-06",
             "--kb-root", str(self.tmp.name), "--no-terms-agent"],
            agent_dynamic=agent,
        )
        self.assertEqual(code, 0)
        # planning re-ran (the fake writes a non-empty plan) and the merged
        # dynamic queries persisted for the next resume
        planned = json.loads((self.run_dir / "query-plan.json").read_text(encoding="utf-8"))
        self.assertTrue(planned["queries"])
        merged = json.loads((self.run_dir / "dynamic-queries.json").read_text(encoding="utf-8"))
        self.assertIn("direct-rl", {q["label"] for q in merged["queries"]})

    def test_resume_with_complete_plan_skips_dynamic_agent(self):
        """Resume path (2026-10-16 强化学习): query-plan.json already carried 21
        queries, so run_stage("plan") skipped — but the dynamic-query agent ran
        first and burned two API retries before that skip. A complete non-empty
        plan with no --force must not call the agent at all: its fresh queries
        would be stranded in dynamic-queries.json outside the plan."""
        plan = json.loads(self._stage_payload("build-query-plan"))
        (self.run_dir / "query-plan.json").write_text(json.dumps(plan), encoding="utf-8")
        (self.run_dir / "query-plan.md").write_text("# plan\n", encoding="utf-8")
        agent = mock.Mock(return_value={"queries": [
            {"label": "direct-x", "tier": "direct-x", "query": "all:demo"},
        ]})
        code, summary = self.run_driver(self.argv("--no-terms-agent"), agent_dynamic=agent)
        self.assertEqual(code, 0)
        agent.assert_not_called()
        self.assertEqual(summary["dynamic_source"], "skipped (plan present)")
        self.assertFalse(any("build-query-plan" in " ".join(c) for c in self.commands))
        # the existing plan is reused verbatim — nothing rewrote it
        planned = json.loads((self.run_dir / "query-plan.json").read_text(encoding="utf-8"))
        self.assertEqual(planned["queries"], [{"label": "a", "query": "all:demo"}])

    def test_force_reruns_agent_despite_complete_plan(self):
        """--force re-plans everything, so a complete plan must not suppress the
        dynamic-query agent (the escape hatch for the skip above)."""
        plan = json.loads(self._stage_payload("build-query-plan"))
        (self.run_dir / "query-plan.json").write_text(json.dumps(plan), encoding="utf-8")
        (self.run_dir / "query-plan.md").write_text("# plan\n", encoding="utf-8")
        agent = mock.Mock(return_value={"queries": [
            {"label": "direct-x", "tier": "direct-x", "query": "all:demo"},
        ]})
        code, summary = self.run_driver(self.argv("--no-terms-agent", "--force"), agent_dynamic=agent)
        self.assertEqual(code, 0)
        agent.assert_called_once()
        self.assertEqual(summary["dynamic_source"], "agent")
        self.assertTrue(any("build-query-plan" in " ".join(c) for c in self.commands))

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

    def test_pure_chinese_topic_forces_dynamic_agent_under_fast(self):
        # A pure-Chinese topic has no Latin token to conjunct, so without the
        # agent the plan is left with CJK fallbacks arXiv can never match —
        # retrieval died at 0 candidates on 2026-10-12. The agent is the only
        # English-query source there, so fast strategy must not disable it.
        agent = mock.Mock(return_value={"queries": [
            {"label": "direct-x", "tier": "direct-x", "query": 'all:"image segmentation"'},
        ]})
        _, summary = self.run_driver(
            ["--run-dir", str(self.run_dir), "--topic", "图像分割",
             "--review-mode", "rapid", "--time-range", "2023-01-01..2026-06-06",
             "--kb-root", str(self.tmp.name), "--no-terms-agent",
             "--search-strategy", "fast"],
            agent_dynamic=agent,
        )
        agent.assert_called_once()
        self.assertEqual(summary["dynamic_source"], "agent-forced")

    def test_pure_chinese_topic_merges_translation_into_latin_queries(self):
        """Problem #2 (2026-10-15 强化学习): the agent failed and the
        pure-Chinese topic had no Latin token, so the plan fell to 0 queries.
        The MyMemory translation must supply the mechanical English channel —
        merged with the topic's own tokens — even without the agent."""
        code, _ = self.run_driver(
            ["--run-dir", str(self.run_dir), "--topic", "强化学习",
             "--review-mode", "rapid", "--time-range", "2023-01-01..2026-06-06",
             "--kb-root", str(self.tmp.name), "--no-terms-agent"],
            translate_en="reinforcement learning",
        )
        self.assertEqual(code, 0)
        merged = json.loads((self.run_dir / "dynamic-queries.json").read_text(encoding="utf-8"))
        labels = {q["label"]: q for q in merged["queries"]}
        self.assertIn('all:"reinforcement"', labels["latin-combined"]["query"])
        self.assertIn('all:"learning"', labels["latin-combined"]["query"])

    def test_translation_satisfies_fast_strategy_without_forcing_agent(self):
        # With the translated English channel in place, a pure-Chinese topic no
        # longer needs to force the dynamic agent under fast strategy.
        agent = mock.Mock()
        _, summary = self.run_driver(
            ["--run-dir", str(self.run_dir), "--topic", "强化学习",
             "--review-mode", "rapid", "--time-range", "2023-01-01..2026-06-06",
             "--kb-root", str(self.tmp.name), "--no-terms-agent",
             "--search-strategy", "fast"],
            agent_dynamic=agent,
            translate_en="reinforcement learning",
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
        code = invoke("run.py", "pipeline", self.argv("--no-terms-agent", "--external-candidates", "/nonexistent.json"))
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
                code = invoke("run.py", "pipeline", self.argv(
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
            "candidate_count": 4,
            "candidates": [
                {"arxiv_id": "2402.10329", "title": "UMI", "summary": "Universal manipulation interface. It collects data with a gripper.",
                 "authors": ["Alice"], "published": "2024-02-01"},
                {"arxiv_id": "2302.01109", "title": "No abstract candidate"},
                {"arxiv_id": "2311.18259", "title": "Ego-Exo4D", "summary": "Ego-exo dataset.", "authors": []},
                {"arxiv_id": "2305.01111", "title": "Off-topic BEV", "summary": "Bird's-eye-view segmentation for driving.",
                 "authors": [], "published": "2023-05-01"},
            ],
        }), encoding="utf-8")
        # The selection rejected 2305.01111: its abstract must never become
        # positioning evidence.
        (self.run_dir / "screening-ids.txt").write_text(
            "2402.10329\n2302.01109\n2311.18259\n", encoding="utf-8"
        )
        self.args = parse("run.py", "pipeline", [
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
        self.assertEqual(self.summary["abstract_basis"], "screened")

    def test_selection_rejected_candidates_never_become_abstract_evidence(self):
        """The registry's 2305.01111 was screened out: abstract-tier scope is
        the selection, not the registry (the 2026-10-13 leak)."""
        self.run_stage()
        self.assertEqual(
            {event["paper"]["arxiv_id"] for event in self.events()},
            {"2402.10329", "2311.18259"},
        )

    def test_missing_screening_ids_skips_instead_of_falling_back_to_registry(self):
        (self.run_dir / "screening-ids.txt").unlink()
        self.run_stage()
        self.assertFalse((self.run_dir / "evidence" / "abstract-tier.jsonl").exists())
        self.assertEqual(self.summary["abstract_events"], 0)
        self.assertEqual(self.summary["abstract_basis"], "skipped")

    def test_idempotent_on_existing_output(self):
        self.run_stage()
        first = (self.run_dir / "evidence" / "abstract-tier.jsonl").read_text(encoding="utf-8")
        self.summary.clear()
        self.run_stage()
        self.assertEqual(
            (self.run_dir / "evidence" / "abstract-tier.jsonl").read_text(encoding="utf-8"), first
        )
        self.assertEqual(self.summary["abstract_events"], 2)
        self.assertEqual(self.summary["abstract_basis"], "screened")

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



class EventPrefixClaimTest(unittest.TestCase):
    """Event-ID prefixes are reserved O_EXCL under <kb-root>/.claims/. Two
    races bit this on 2026-10-13 (5 concurrent runs): every Chinese topic
    collapsed to base "REVIEW" (CJK is stripped from TOPIC8, which must stay
    ASCII per EVENT_ID_RE), and the post-5-attempts fallback returned an
    UNRESERVED prefix — 图像内参估计 and 图像拼接 both settled on
    EA-REVIEW-2026-8."""

    def setUp(self) -> None:
        import os

        self._tmp = tempfile.TemporaryDirectory()
        self.kb_root = Path(self._tmp.name)
        (self.kb_root / "evidence").mkdir()
        self._env = os.environ.copy()
        os.environ["EMBODIED_KB_LOCK_DIR"] = str(self.kb_root / ".locks")

    def tearDown(self) -> None:
        import os

        os.environ.clear()
        os.environ.update(self._env)
        self._tmp.cleanup()

    def _claim(self, topic: str, run_name: str) -> str:
        driver = load_driver()
        run_dir = self.kb_root / "work" / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        run_json = run_dir / "run.json"
        run_json.write_text(json.dumps({"topic": topic}), encoding="utf-8")
        return driver.claim_event_prefix(self.kb_root, run_json, {"topic": topic})

    def test_distinct_chinese_topics_get_distinct_prefixes(self) -> None:
        first = self._claim("图像内参估计", "literature-review-a-20261013")
        second = self._claim("图像拼接", "literature-review-b-20261013")
        self.assertNotEqual(first, second, "two Chinese topics must not share an event-ID namespace")

    def test_claim_is_reserved_on_disk(self) -> None:
        prefix = self._claim("图像重定位", "literature-review-c-20261013")
        claims = self.kb_root / ".claims" / "event-prefix"
        self.assertTrue((claims / f"{prefix}.json").is_file(), "the fallback must never return an unreserved prefix")

    def test_same_topic_is_idempotent_via_manifest(self) -> None:
        driver = load_driver()
        run_dir = self.kb_root / "work" / "literature-review-d-20261013"
        run_dir.mkdir(parents=True, exist_ok=True)
        run_json = run_dir / "run.json"
        run_json.write_text(json.dumps({"topic": "图像分割", "event_prefix": "EA-KEEP-2026"}), encoding="utf-8")
        self.assertEqual(
            driver.claim_event_prefix(self.kb_root, run_json, {"topic": "图像分割", "event_prefix": "EA-KEEP-2026"}),
            "EA-KEEP-2026",
        )



class StageAnnounceTest(unittest.TestCase):
    """A stage that blocks for minutes with no output reads as a hang
    (2026-10-13: 13 silent minutes between "注册 558 篇去重候选" and
    "精读候选 29 篇"). Every stage now announces itself before it blocks."""

    def test_run_stage_announces_before_blocking(self):
        driver = load_driver()
        out: list[str] = []

        def fake_run(command, **kwargs):
            # the mocked command still has to land the stage output, or
            # run_stage reports "outputs missing after run"
            target.write_text("{}", encoding="utf-8")
            return mock.Mock(returncode=0, stdout="", stderr="")

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out.json"
            with mock.patch.object(driver, "log", side_effect=out.append), \
                 mock.patch.object(driver, "run_command", side_effect=fake_run):
                driver.run_stage("screening", [target], True, lambda: ["true"])
        self.assertTrue(any("screening 开始" in line for line in out), out)
        # and it is announced BEFORE the completion line
        start = next(i for i, l in enumerate(out) if "开始" in l)
        done = next(i for i, l in enumerate(out) if "DRIVER-STAGE:screening" in l)
        self.assertLess(start, done)


class DeepReadRetryTest(unittest.TestCase):
    """Upstream instability under parallel deep reads: a failed paper whose
    full text is on disk gets one whole-queue retry pass; a paper without an
    extraction does not (its bottleneck is the fetch)."""

    def setUp(self):
        self.driver = load_driver()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.kb = root / "kb"
        self.pool = self.kb / "pool"
        self.run_dir = root / "work" / "literature-review-demo"
        self.run_dir.mkdir(parents=True)
        self.ids = ["2401.00001", "2401.00002", "2401.00003"]
        for paper_id in self.ids[:2]:  # 00003 never gets full text
            pool_dir = self.pool / f"arxiv-{paper_id}"
            pool_dir.mkdir(parents=True)
            (pool_dir / "extraction.json").write_text(
                json.dumps({"available": True}), encoding="utf-8"
            )
        (self.run_dir / "screening-ids.txt").write_text(
            "\n".join(self.ids) + "\n", encoding="utf-8"
        )
        self.run_json = self.run_dir / "run.json"
        self.run_json.write_text("{}", encoding="utf-8")
        self.args = mock.Mock(
            kb_root=str(self.kb), review_mode="rapid", deep_read_limit=10,
            agents_parallel=2, agent_timeout=5.0, force=False,
        )

    def _run(self, fake_deep_read):
        summary: dict = {"seed_ids": []}
        with mock.patch.object(self.driver, "resolve_cli", return_value="/fake/claude"), \
             mock.patch.object(self.driver, "deep_read_paper", side_effect=fake_deep_read), \
             mock.patch.object(self.driver, "log"):
            self.driver.deep_read(
                self.run_dir, self.run_json, self.run_dir / "screening-ids.txt",
                self.args, summary,
            )
        return summary

    def test_failed_paper_is_retried_and_counted_once(self):
        calls: dict[str, int] = {}

        def fake(paper_id, *args, **kwargs):
            calls[paper_id] = calls.get(paper_id, 0) + 1
            if paper_id == "2401.00001" and calls[paper_id] == 1:
                return "failed", "骨架 agent 失败"
            return "pass", ""

        summary = self._run(fake)
        self.assertEqual(calls["2401.00001"], 2)  # first pass + retry pass
        self.assertEqual(calls["2401.00002"], 1)
        self.assertEqual(
            summary["deep_read"],
            {"total": 3, "pass": 2, "needs_review": 0, "failed": 1},
        )
        # 00003 has no full text: failed once, never retried.
        self.assertNotIn("2401.00003", calls)
        self.assertTrue((self.run_dir / "paper-notes" / "2401.00003.failed.json").is_file())
        # The recovered paper's transient failure marker is cleared.
        self.assertFalse((self.run_dir / "paper-notes" / "2401.00001.failed.json").is_file())

    def test_still_failing_paper_is_not_double_counted(self):
        def always_fail(paper_id, *args, **kwargs):
            if paper_id == "2401.00001":
                return "failed", "骨架 agent 失败"
            return "pass", ""

        summary = self._run(always_fail)
        self.assertEqual(
            summary["deep_read"],
            {"total": 3, "pass": 1, "needs_review": 0, "failed": 2},
        )  # 00001 counted once + 00003 without full text


class SelectionProgressTest(unittest.TestCase):
    """smart selection makes one agent call per chunk — minutes each. The
    chunk lines must become wiki progress ticks, not be swallowed."""

    def test_chunk_lines_translate_to_progress(self):
        driver = load_driver()
        out: list[str] = []
        with mock.patch.object(driver, "log", side_effect=out.append):
            driver.selection_line("chunk 1/2: judging 300 of 558 candidates…")
            driver.selection_line("chunk 2/2: judging 258 of 558 candidates…")
            driver.selection_line("smart selected 29/558 considered (2 chunk(s))")
        self.assertIn("[DRIVER-PROGRESS:select:1/2]", out)
        self.assertIn("[DRIVER-PROGRESS:select:2/2]", out)
        self.assertIn("[DRIVER] 选文 judging 300 of 558 candidates…", out)
        self.assertIn("[DRIVER] 选文 smart selected 29/558 considered (2 chunk(s))", out)
        self.assertFalse(any("选文 :" in line for line in out), out)

    def test_smart_select_prints_chunk_progress(self):
        import contextlib, io
        selection = __import__("embodied_learning.search.selection", fromlist=["smart_select"])
        saved = selection.SMART_CANDIDATES_PER_CALL
        selection.SMART_CANDIDATES_PER_CALL = 2
        try:
            def fake_complete(prompt, **kwargs):
                return mock.Mock(returncode=0, stdout='{"relevant": []}')
            registry = {"candidates": [
                {"arxiv_id": f"2401.{i:05d}", "title": f"P{i}", "abstract": "x"} for i in range(3)
            ]}
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                selection.smart_select(
                    registry, topic="t", focus="",
                    complete_fn=fake_complete, cli="x", model="x",
                )
        finally:
            selection.SMART_CANDIDATES_PER_CALL = saved
        text = buf.getvalue()
        self.assertIn("chunk 1/2:", text)
        self.assertIn("chunk 2/2:", text)

if __name__ == "__main__":
    unittest.main()

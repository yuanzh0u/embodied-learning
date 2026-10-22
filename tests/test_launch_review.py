#!/usr/bin/env python3

from __future__ import annotations

from _entry import invoke, parse

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def load(name: str, relative: str):
    # Load implementation modules (not the scripts/ forwarders) so mock.patch
    # on module attributes reaches the live globals the functions read.
    import importlib

    mapping = {
        "rrp_for_launch_test": "embodied_learning.wiki.run.driver",
        "launch_review_for_test": "embodied_learning.wiki.run.launcher",
    }
    return importlib.import_module(mapping[name])


rrp = load("rrp_for_launch_test", "scripts/run.py pipeline")
launcher = load("launch_review_for_test", "scripts/launch_review.py")


class BuildScreeningUpdatesTest(unittest.TestCase):
    def test_merges_extraction_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            screening = tmp / "screening.json"
            extraction = tmp / "extraction-summary.json"
            screening.write_text(json.dumps({"candidates": [
                {"arxiv_id": "1", "status": "full-text-queued", "screening_score": 10},
                {"arxiv_id": "2", "status": "full-text-queued", "screening_score": 9},
            ]}), encoding="utf-8")
            extraction.write_text(json.dumps({"results": [
                {"paper_id": "1", "evidence_eligible": True, "path": "/x/1.json"},
                {"paper_id": "2", "evidence_eligible": False},
            ]}), encoding="utf-8")
            updates = rrp.build_screening_updates(screening, extraction)
            self.assertEqual(updates[0]["status"], "extracted")
            self.assertTrue(updates[0]["extraction"]["evidence_eligible"])
            self.assertEqual(updates[1]["status"], "full-text-queued")

    def test_returns_none_on_missing_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(
                rrp.build_screening_updates(Path(tmp) / "a.json", Path(tmp) / "b.json"))


class FinalizeCoverageTest(unittest.TestCase):
    def test_skips_without_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            detail = rrp.finalize_coverage(Path(tmp), ["true"], Path(tmp) / "coverage.json")
            self.assertIn("skipped", detail)


class StageMarkersTest(unittest.TestCase):
    def test_mark_and_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            self.assertFalse(launcher.stage_done(run_dir, "mechanical"))
            launcher.mark_stage(run_dir, "mechanical", "ok")
            self.assertTrue(launcher.stage_done(run_dir, "mechanical"))
            self.assertIn("ok", (run_dir / ".launch" / "mechanical.done").read_text())


class BackfillReentryParamsTest(unittest.TestCase):
    def test_manifest_backfills_identity_and_kb_root(self) -> None:
        # Re-entry with a bare --run-dir: topic/mode/range come from run.json
        # and the KB root is inferred from <kb-root>/work/<run> — a bare
        # resume used to crash with a None arg in the driver command.
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            run_dir = kb_root / "work" / "literature-review-demo-20260924"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({
                    "topic": "点云表面重建",
                    "review_mode": "systematic",
                    "time_range": "2016-09-22..2026-09-22",
                }),
                encoding="utf-8",
            )
            args = mock.Mock(
                topic=None, review_mode=None, time_range=None, kb_root=None,
            )
            launcher.backfill_reentry_params(args, run_dir)
            self.assertEqual(args.topic, "点云表面重建")
            self.assertEqual(args.review_mode, "systematic")
            self.assertEqual(args.time_range, "2016-09-22..2026-09-22")
            self.assertEqual(args.kb_root, str(kb_root))

    def test_manifest_backfills_target_style(self) -> None:
        """A bare --resume leaves --target-style at the parser default
        (scientific-memo), which run_finalize forwards as --style and would
        shrink a three-style run at settle. The birth interview answer is the
        authority (2026-10-21 点云匹配)."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "work" / "run"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({"topic": "t", "inputs": {"target_style": "all"}}),
                encoding="utf-8",
            )
            args = mock.Mock(topic=None, review_mode=None, time_range=None,
                             kb_root=str(tmp), target_style="scientific-memo")
            launcher.backfill_reentry_params(args, run_dir)
            self.assertEqual(args.target_style, "all")

    def test_launch_init_carries_the_interview_inputs(self) -> None:
        """The CLI launch must stamp the same `inputs` payload the wiki kickoff
        does — otherwise run.json has no target_style for the pre-settle gates
        to read."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            run_dir = kb_root / "work" / "literature-review-demo-20261021"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps({"topic": "demo", "review_mode": "rapid", "status": "in-progress",
                            "inputs": {"target_style": "scientific-memo"}}),
                encoding="utf-8",
            )
            captured: list[list[str]] = []

            def fake_run(command, **kwargs):
                captured.append([str(part) for part in command])
                if "init" in command:
                    return mock.Mock(returncode=0, stdout=f"Initialized run: {run_dir}\n", stderr="")
                return mock.Mock(returncode=0, stdout="", stderr="")

            with mock.patch.object(launcher, "system_one_ready", return_value=True), \
                    mock.patch.object(launcher.subprocess, "run", side_effect=fake_run), \
                    mock.patch.object(launcher, "stage_done", return_value=None), \
                    mock.patch.object(launcher, "run_mechanical"), \
                    mock.patch.object(launcher, "writer_prompts", return_value=("s", "u")), \
                    mock.patch.object(launcher, "run_writer", return_value=False), \
                    mock.patch.object(launcher, "collect_gate_problems", return_value=[]), \
                    mock.patch.object(launcher, "run_finalize"), \
                    mock.patch.object(launcher, "verify_publish", return_value=[]), \
                    mock.patch.object(launcher, "mark_stage"):
                code = invoke("run.py", "launch", [
                    "--topic", "demo", "--kb-root", str(kb_root),
                    "--target-style", "scientific-memo",
                ])
            self.assertEqual(code, 0)
            init = next(cmd for cmd in captured if "init" in cmd)
            payload = json.loads(init[init.index("--inputs-json") + 1])
            self.assertEqual(payload["target_style"], "scientific-memo")
            self.assertEqual(payload["source"], "cli")

    def test_explicit_kb_root_not_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "work" / "run"
            run_dir.mkdir(parents=True)
            args = mock.Mock(topic=None, review_mode=None, time_range=None, kb_root="/explicit")
            launcher.backfill_reentry_params(args, run_dir)
            self.assertEqual(args.kb_root, "/explicit")

    def test_missing_manifest_leaves_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "work" / "run"
            run_dir.mkdir(parents=True)
            args = mock.Mock(topic="t", review_mode="rapid", time_range="r", kb_root=None)
            launcher.backfill_reentry_params(args, run_dir)
            self.assertEqual(args.topic, "t")
            self.assertEqual(args.kb_root, str(Path(tmp)))


class PrepareGateInputsTest(unittest.TestCase):
    def test_rebuilds_shared_evidence_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "evidence").mkdir()
            (run_dir / "evidence" / "a.jsonl").write_text('{"event_id": "E1"}\n{"event_id": "E2"}\n', encoding="utf-8")
            (run_dir / "evidence" / "b.jsonl").write_text('{"event_id": "E3"}\n', encoding="utf-8")
            launcher.prepare_gate_inputs(run_dir)
            merged = (run_dir / "evidence.jsonl").read_text().splitlines()
            self.assertEqual(len(merged), 3)
            self.assertFalse((run_dir / "evidence-all.jsonl").exists())

    def test_flat_run_keeps_canonical_root_file(self) -> None:
        """Runs with no evidence/ subdir keep canonical evidence.jsonl at the
        run root; the rebuild must fold its lines in, not clobber them —
        regression for the flat-run evidence loss."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "evidence.jsonl").write_text('{"e": 1}\n{"e": 2}\n', encoding="utf-8")
            launcher.prepare_gate_inputs(run_dir)
            self.assertEqual((run_dir / "evidence.jsonl").read_text(), '{"e": 1}\n{"e": 2}\n')

    def test_rebuild_refreshes_stale_merge(self) -> None:
        """A stale merged file from before a resumed deep-read round must be
        refreshed (20260929 split-brain: launcher gate and finalize gate saw
        different evidence sets)."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "evidence").mkdir()
            (run_dir / "evidence.jsonl").write_text('{"event_id": "OLD"}\n', encoding="utf-8")
            (run_dir / "evidence" / "new.jsonl").write_text('{"event_id": "NEW"}\n', encoding="utf-8")
            launcher.prepare_gate_inputs(run_dir)
            text = (run_dir / "evidence.jsonl").read_text()
            self.assertIn("OLD", text)
            self.assertIn("NEW", text)


class CollectGateProblemsTest(unittest.TestCase):
    def test_reports_missing_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            problems = launcher.collect_gate_problems(Path(tmp))
            self.assertTrue(any("成稿" in problem for problem in problems))

    def test_filters_run_not_settled_timing_noise(self) -> None:
        """check_run_bundle runs BEFORE run.py finalize, so its
        "run not settled: status is `in-progress`" line is timing noise that
        would burn a continuation round; real missing-field lines still report."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "scientific-memo_keyan.md").write_text("# 成稿\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                if "check-bundle" in [str(part) for part in command]:
                    return mock.Mock(
                        returncode=1,
                        stdout="run not settled: status is `in-progress`\n"
                               "run.json: missing required field `x`\n",
                        stderr="",
                    )
                return mock.Mock(returncode=0, stdout="{}", stderr="")

            with mock.patch.object(launcher.subprocess, "run", side_effect=fake_run):
                problems = launcher.collect_gate_problems(run_dir)
        self.assertTrue(any("missing required field" in problem for problem in problems))
        self.assertFalse(any("run not settled" in problem for problem in problems))

    def test_single_style_run_audits_only_its_own_article(self) -> None:
        """A run born with inputs.target_style=expert-explainer ships no memo;
        the launcher used to hard-code the memo path into audit-citations and
        report "article missing" for a file the run never promised."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "run.json").write_text(json.dumps({
                "status": "in-progress",
                "inputs": {"source": "wiki-interview", "target_style": "expert-explainer"},
            }), encoding="utf-8")
            (run_dir / "zhihu-explainer_zhihu.md").write_text("# 知乎\n", encoding="utf-8")
            captured: list[list[str]] = []

            def fake_run(command, **kwargs):
                captured.append([str(part) for part in command])
                return mock.Mock(returncode=0, stdout="{}", stderr="")

            with mock.patch.object(launcher.subprocess, "run", side_effect=fake_run):
                problems = launcher.collect_gate_problems(run_dir)
        self.assertEqual(problems, [])
        citation = next(cmd for cmd in captured if "audit-citations" in cmd)
        articles = [b for a, b in zip(citation, citation[1:]) if a == "--article"]
        self.assertEqual(len(articles), 1)
        self.assertTrue(articles[0].endswith("zhihu-explainer_zhihu.md"))


class WriterPromptsTest(unittest.TestCase):
    def test_launcher_prompts_come_from_the_shared_factory(self) -> None:
        """The headless writer's (system, user) prompts are composed by the
        same wiki_chat assembly point the interactive wiki uses — the only
        divergence is publisher="launcher"."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            run_dir = kb_root / "work" / "literature-review-demo-20260928"
            run_dir.mkdir(parents=True)
            args = mock.Mock(
                topic="点云表面重建", review_mode="systematic",
                time_range="2016-09-28..2026-09-28", search_strategy="smart",
                selection_strategy="bm25",
                seed_arxiv_ids=None, target_style="scientific-memo",
                focus=None, kb_root=str(kb_root),
            )
            wiki = launcher.load_wiki_prompts()
            system_prompt, user_prompt = launcher.writer_prompts(run_dir, args, wiki)
            self.assertEqual(
                system_prompt,
                wiki.workflow_turn_system_prompt(
                    launcher.pipeline_root(), Path(args.kb_root).resolve(),
                    publisher="launcher",
                ),
            )
            self.assertIn("立即停止本轮回复", system_prompt)
            self.assertNotIn("[TOPIC:", system_prompt)
            self.assertIn(run_dir.name, user_prompt)
            # The launcher branch must not instruct the agent to run finalize.
            self.assertNotIn("run.py finalize", user_prompt)
            self.assertIn("write.py review-packet", user_prompt)
            # The selection strategy reaches the writer prompt (and run_mechanical
            # forwards the same flag to the driver).
            self.assertIn("选文策略：bm25", user_prompt)

    def test_selection_strategy_flag_defaults_and_forwards(self) -> None:
        # Default is smart-jev (the decision model); unknown values are rejected.
        with mock.patch.object(launcher, "system_one_ready", return_value=True), \
                mock.patch.object(launcher, "launch", return_value=0) as launch:
            invoke("run.py", "launch", ["--topic", "demo"])
        self.assertEqual(launch.call_args.args[0].selection_strategy, "smart-jev")
        with self.assertRaises(SystemExit):
            invoke("run.py", "launch", ["--topic", "demo", "--selection-strategy", "bogus"])

    def test_launch_refuses_default_smart_jev_without_the_decision_model(self) -> None:
        """The default strategy is the decision model: an unconfigured channel
        stops the launch before a run dir is created (no init subprocess)."""
        with mock.patch.object(launcher, "system_one_ready", return_value=False), \
                mock.patch.object(launcher.subprocess, "run") as run:
            code = invoke("run.py", "launch", ["--topic", "demo", "--kb-root", "/tmp/kb"])
        self.assertEqual(code, 2)
        run.assert_not_called()

    def test_run_mechanical_forwards_selection_strategy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            args = mock.Mock(
                topic="点云表面重建", review_mode="systematic", focus=None,
                time_range="2016-09-28..2026-09-28", search_strategy="smart",
                selection_strategy="influence", deep_read_limit=48,
                agents_parallel=10, arxiv_snapshot=None, kb_root=str(kb_root),
                seed_arxiv_ids=None, external_candidates=[], mechanical_retries=1,
            )
            with mock.patch.object(launcher.subprocess, "run", return_value=mock.Mock(returncode=0)) as run:
                launcher.run_mechanical(args, Path(tmp) / "run")
            command = run.call_args.args[0]
            self.assertEqual(
                command[command.index("--selection-strategy") + 1], "influence"
            )
            self.assertEqual(command[command.index("--search-strategy") + 1], "smart")


class RunFinalizeTest(unittest.TestCase):
    def _args(self, kb_root: Path, target_style="scientific-memo", scope_note=None):
        return argparse_namespace(
            kb_root=str(kb_root), target_style=target_style, scope_note=scope_note,
        )

    def test_single_style_declares_style(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            run_dir = kb_root / "work" / "run"
            with mock.patch.object(
                launcher.subprocess, "run", return_value=mock.Mock(returncode=0)
            ) as run:
                launcher.run_finalize(self._args(kb_root), run_dir)
            command = run.call_args.args[0]
            self.assertTrue(any(str(part).endswith("run.py") for part in command) and "finalize" in command)
            self.assertIn("--style", command)
            self.assertIn("scientific-memo", command)
            self.assertNotIn("--scope-note", command)
            self.assertEqual(str(command[command.index("--kb-root") + 1]), str(kb_root))

    def test_all_style_does_not_pollute_three_style_inference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            with mock.patch.object(
                launcher.subprocess, "run", return_value=mock.Mock(returncode=0)
            ) as run:
                launcher.run_finalize(
                    self._args(kb_root, target_style="all"), kb_root / "work" / "run")
            self.assertNotIn("--style", run.call_args.args[0])

    def test_scope_note_forwarded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            with mock.patch.object(
                launcher.subprocess, "run", return_value=mock.Mock(returncode=0)
            ) as run:
                launcher.run_finalize(
                    self._args(kb_root, scope_note="仅速读"), kb_root / "work" / "run")
            command = run.call_args.args[0]
            self.assertIn("--scope-note", command)
            self.assertIn("仅速读", command)

    def test_nonzero_exit_raises_with_resume_hint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            with mock.patch.object(
                launcher.subprocess, "run", return_value=mock.Mock(returncode=2)
            ):
                with self.assertRaises(RuntimeError) as ctx:
                    launcher.run_finalize(self._args(kb_root), kb_root / "work" / "run")
            self.assertIn("--resume", str(ctx.exception))

    def test_zero_exit_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            with mock.patch.object(
                launcher.subprocess, "run", return_value=mock.Mock(returncode=0)
            ):
                launcher.run_finalize(self._args(kb_root), kb_root / "work" / "run")


class VerifyPublishTest(unittest.TestCase):
    def test_reports_missing_catalog_and_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp)
            run_dir = kb_root / "work" / "literature-review-x-20260101"
            run_dir.mkdir(parents=True)
            args = argparse_namespace(kb_root=str(kb_root))
            problems = launcher.verify_publish(args, run_dir, launcher.load_wiki_prompts())
            self.assertTrue(any("catalog" in problem for problem in problems))
            self.assertTrue(any("wiki" in problem for problem in problems))

    def test_topic_matched_by_key_without_date_suffix(self) -> None:
        """The wiki indexes topics by topic_key/title (no date suffix); a folder
        name with `-20260101` must still match — regression for the false
        'wiki 最新快照不含本 run 话题' report on settled runs."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            kb_root = tmp / "kb"
            run_dir = kb_root / "work" / "literature-review-ego-视频数据集全景-20260918"
            run_dir.mkdir(parents=True)
            (kb_root / "knowledge").mkdir(parents=True)
            catalog = kb_root / "knowledge" / "literature-review-catalog.md"
            catalog.write_text("literature-review-ego-视频数据集全景-20260918", encoding="utf-8")
            snapshots = kb_root / "wiki" / "data" / "snapshots" / "snap1"
            snapshots.mkdir(parents=True)
            (snapshots / "manifest.json").write_text(json.dumps({"topics": [
                {"topic_key": "ego-视频数据集全景", "title": "ego 视频数据集全景"},
            ]}), encoding="utf-8")
            (kb_root / "wiki" / "data" / "current.json").write_text("{}", encoding="utf-8")
            args = argparse_namespace(kb_root=str(kb_root))
            problems = launcher.verify_publish(args, run_dir, launcher.load_wiki_prompts())
            self.assertEqual([p for p in problems if "wiki" in p], [])


def argparse_namespace(**kwargs):
    import argparse
    return argparse.Namespace(**kwargs)



class UserDecisionStopTest(unittest.TestCase):
    """Deep-read shortfall is a designed decision point: the writer reports the
    shortlisted papers and emits [STOP:awaiting-user]. That is the correct
    terminal state, not a failure — but the launcher used to ignore the marker
    and burn every continuation round re-asking (2026-10-13, run 05: 4 writer
    rounds, $31 of tokens, all ending in the same stop)."""

    def test_stop_marker_is_recognised(self) -> None:
        import os
        import tempfile

        self.assertEqual(launcher.USER_DECISION_STOP, "[STOP:awaiting-user]")
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "writer.log"
            log.write_text("...输出如下\n[STOP:awaiting-user]\n", encoding="utf-8")
            self.assertIn(launcher.USER_DECISION_STOP, log.read_text(encoding="utf-8")[-20000:])

if __name__ == "__main__":
    unittest.main()


class ResolveWriterModelTest(unittest.TestCase):
    def test_subagent_env_var_is_ignored(self) -> None:
        """CLAUDE_CODE_SUBAGENT_MODEL is shell-profile pollution (e.g. the
        "-cc" SKU), never an intent signal for the writer; honoring it made
        the pinned fast model unreachable. Subagent consistency is enforced
        at spawn time instead (isolated_claude_env strips the var)."""
        args = argparse_namespace(writer_model=None)
        with mock.patch.dict(
            "os.environ", {"CLAUDE_CODE_SUBAGENT_MODEL": "glm-5.3-flash-cc"}, clear=False
        ):
            self.assertEqual(launcher.resolve_writer_model(args), launcher.DRIVER_AGENT_MODEL)

    def test_anthropic_model_beats_driver_default(self) -> None:
        args = argparse_namespace(writer_model=None)
        with mock.patch.dict("os.environ", {"ANTHROPIC_MODEL": "glm-5.3-flash"}, clear=False):
            self.assertEqual(launcher.resolve_writer_model(args), "glm-5.3-flash")

    def test_flag_beats_env(self) -> None:
        args = argparse_namespace(writer_model="glm-5.3-flash")
        env = {"ANTHROPIC_MODEL": "should-lose", "CLAUDE_CODE_SUBAGENT_MODEL": "also-lose"}
        with mock.patch.dict("os.environ", env, clear=False):
            self.assertEqual(launcher.resolve_writer_model(args), "glm-5.3-flash")

    def test_falls_back_to_driver_model(self) -> None:
        args = argparse_namespace(writer_model=None)
        env = {"ANTHROPIC_MODEL": "", "CLAUDE_CODE_SUBAGENT_MODEL": ""}
        with mock.patch.dict("os.environ", env, clear=False):
            self.assertEqual(launcher.resolve_writer_model(args), launcher.DRIVER_AGENT_MODEL)


class EvidenceProblemClassificationTest(unittest.TestCase):
    """Floor/coverage failures are a mechanical-driver job. Feeding them to a
    writer continuation can never resolve them (the writer is forbidden from
    re-running retrieval) and burned every retry round on an unsolvable
    problem (2026-10-13, run 02: a network outage killed all extractions and
    the launcher spent 3 writer rounds unable to help)."""

    def test_floor_problems_are_evidence_side(self) -> None:
        for problem in (
            "coverage/saturation gate not passed: full_text_floor, accepted_paper_floor",
            "full_text_floor（0/12） — 抽取重试可补",
            "accepted_paper_floor（0/8） — 深读/候补可补",
            "cited_paper_floor 未过",
            "补检索/深读后重算",
        ):
            with self.subTest(problem=problem):
                self.assertTrue(launcher.is_evidence_problem(problem), problem)

    def test_editorial_problems_go_to_the_writer(self) -> None:
        for problem in (
            "citation audit: anchor 3 outside the loaded evidence",
            "中文字符占比 0.31 低于阈值 0.60",
            "trace-map 未生成：删改成稿中无证据支撑的 arXiv 引用",
        ):
            with self.subTest(problem=problem):
                self.assertFalse(launcher.is_evidence_problem(problem), problem)

#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


rrp = load("rrp_for_launch_test", "scripts/run_review_pipeline.py")
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
    def test_merges_and_canonicalizes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "evidence").mkdir()
            (run_dir / "evidence" / "a.jsonl").write_text('{"e": 1}\n{"e": 2}\n', encoding="utf-8")
            (run_dir / "evidence" / "b.jsonl").write_text('{"e": 3}\n', encoding="utf-8")
            launcher.prepare_gate_inputs(run_dir)
            merged = (run_dir / "evidence-all.jsonl").read_text().splitlines()
            self.assertEqual(len(merged), 3)
            self.assertTrue((run_dir / "evidence.jsonl").is_file())

    def test_flat_run_merges_canonical_root_file(self) -> None:
        """Runs with no evidence/ subdir keep canonical evidence.jsonl at the
        run root; the gates' merged path must still be produced — regression
        for the 'evidence file missing: .../evidence-all.jsonl' report."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "evidence.jsonl").write_text('{"e": 1}\n{"e": 2}\n', encoding="utf-8")
            launcher.prepare_gate_inputs(run_dir)
            self.assertEqual((run_dir / "evidence-all.jsonl").read_text(), '{"e": 1}\n{"e": 2}\n')


class CollectGateProblemsTest(unittest.TestCase):
    def test_reports_missing_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            problems = launcher.collect_gate_problems(Path(tmp))
            self.assertTrue(any("成稿" in problem for problem in problems))

    def test_filters_run_not_settled_timing_noise(self) -> None:
        """check_run_bundle runs BEFORE finalize_run.py, so its
        "run not settled: status is `in-progress`" line is timing noise that
        would burn a continuation round; real missing-field lines still report."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "scientific-memo_keyan.md").write_text("# 成稿\n", encoding="utf-8")

            def fake_run(command, **kwargs):
                if str(command[1]).endswith("check_run_bundle.py"):
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
            self.assertNotIn("finalize_run.py", user_prompt)
            self.assertIn("build_review_packet.py", user_prompt)


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
            self.assertTrue(any(str(part).endswith("finalize_run.py") for part in command))
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

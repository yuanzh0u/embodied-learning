#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


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


class CollectGateProblemsTest(unittest.TestCase):
    def test_reports_missing_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            problems = launcher.collect_gate_problems(Path(tmp))
            self.assertTrue(any("成稿" in problem for problem in problems))


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

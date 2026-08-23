#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sink_run.py"
SPEC = importlib.util.spec_from_file_location("sink_run", SCRIPT)
sink_run = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(sink_run)

DELIVERABLES = [
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
]


def make_bundle(
    parent: Path,
    name: str = "literature-review-fixture-topic-20260101",
    *,
    gate_ok: bool = True,
    status: str = "settled",
) -> Path:
    run_dir = parent / name
    run_dir.mkdir(parents=True)
    for item in DELIVERABLES + ["evidence-appendix.md", "review-packet.md"]:
        (run_dir / item).write_text(f"# {item}\n", encoding="utf-8")
    (run_dir / "evidence.jsonl").write_text(
        "\n".join(json.dumps({"event_id": f"FIX-000{index}"}) for index in (1, 2)) + "\n",
        encoding="utf-8",
    )
    (run_dir / "query-plan.json").write_text("{}", encoding="utf-8")
    (run_dir / "candidate-registry.json").write_text("{}", encoding="utf-8")
    coverage = {
        "stop_assessment": {"ready_to_stop": gate_ok, "unresolved": [] if gate_ok else ["candidate_floor"]},
        "candidate_count": 20,
        "full_text_count": 16,
        "accepted_count": 15,
    }
    (run_dir / "coverage-report.json").write_text(json.dumps(coverage), encoding="utf-8")
    manifest = {
        "run": name,
        "topic": "fixture topic",
        "time_range": "2026-01-01..2026-06-30",
        "event_count": 2,
        "review_mode": "scoping",
        "workflow_version": 2,
        "status": status,
        "knowledge_ids": ["EA-DATA"],
        "files": {
            "evidence": "evidence.jsonl",
            "outputs": DELIVERABLES,
            "appendix": "evidence-appendix.md",
            "query_plan": "query-plan.json",
            "candidate_registry": "candidate-registry.json",
            "coverage_report": "coverage-report.json",
        },
    }
    (run_dir / "run.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    return run_dir


def run_sink(run_dir: Path, repo: Path, *extra: str) -> tuple[int, str]:
    argv = ["sink_run.py", str(run_dir), "--repo-root", str(repo), *extra]
    stdout = io.StringIO()
    with mock.patch.object(sys, "argv", argv):
        with contextlib.redirect_stdout(stdout):
            code = sink_run.main()
    return code, stdout.getvalue()


class SinkRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "evidence").mkdir()
        (self.repo / "knowledge").mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def target(self, run_dir: Path) -> Path:
        return self.repo / "evidence" / run_dir.name

    def test_sinks_valid_bundle_and_stamps_checklist(self) -> None:
        run_dir = make_bundle(self.repo / "work")

        code, out = run_sink(run_dir, self.repo)

        self.assertEqual(0, code)
        target = self.target(run_dir)
        self.assertTrue((target / "run.json").is_file())
        for manifest_path in (run_dir / "run.json", target / "run.json"):
            checklist = json.loads(manifest_path.read_text(encoding="utf-8"))["sink_checklist"]
            self.assertTrue(checklist["copied"])
            self.assertTrue(checklist["bundle_audited"])
            self.assertTrue(checklist["gate_passed"])
            self.assertFalse(checklist["catalog_registered"])
        self.assertIn("catalog: NOT registered", out)
        self.assertIn("LR-<NEW-ID>", out)
        self.assertIn("fixture topic", out)

    def test_idempotent_rerun(self) -> None:
        run_dir = make_bundle(self.repo / "work")
        self.assertEqual(0, run_sink(run_dir, self.repo)[0])

        code, out = run_sink(run_dir, self.repo)

        self.assertEqual(0, code)
        self.assertIn("target exists", out)
        self.assertIn("sink complete", out)
        self.assertTrue((self.target(run_dir) / "evidence.jsonl").is_file())

    def test_refuses_gate_failed_without_flag(self) -> None:
        run_dir = make_bundle(self.repo / "work", gate_ok=False)

        code, out = run_sink(run_dir, self.repo)

        self.assertEqual(1, code)
        self.assertIn("refusing", out)
        self.assertIn("--allow-gate-fail", out)
        self.assertFalse(self.target(run_dir).exists())

    def test_allow_gate_fail_sinks_and_marks(self) -> None:
        run_dir = make_bundle(self.repo / "work", gate_ok=False)

        code, out = run_sink(run_dir, self.repo, "--allow-gate-fail")

        self.assertEqual(0, code)
        checklist = json.loads((self.target(run_dir) / "run.json").read_text(encoding="utf-8"))["sink_checklist"]
        self.assertFalse(checklist["gate_passed"])
        self.assertIn("覆盖门未过", out)
        self.assertIn("candidate_floor", out)

    def test_refuses_in_progress_run(self) -> None:
        run_dir = make_bundle(self.repo / "work", status="in-progress")

        code, out = run_sink(run_dir, self.repo)

        self.assertEqual(1, code)
        self.assertIn("refusing", out)
        self.assertFalse(self.target(run_dir).exists())

    def test_detects_catalog_registration(self) -> None:
        run_dir = make_bundle(self.repo / "work")
        catalog = self.repo / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "## 23 项成果\n\n| ID | 主题 | 规模 | 审计入口 |\n|---|---|---|---|\n"
            f"| LR-TEST | test | 1 / 1 / 1 | [run](../evidence/{run_dir.name}/run.json) |\n",
            encoding="utf-8",
        )

        code, out = run_sink(run_dir, self.repo)

        self.assertEqual(0, code)
        self.assertIn("catalog: already registered", out)
        self.assertNotIn("LR-<NEW-ID>", out)
        checklist = json.loads((self.target(run_dir) / "run.json").read_text(encoding="utf-8"))["sink_checklist"]
        self.assertTrue(checklist["catalog_registered"])

    def test_dry_run_writes_nothing(self) -> None:
        run_dir = make_bundle(self.repo / "work")

        code, out = run_sink(run_dir, self.repo, "--dry-run")

        self.assertEqual(0, code)
        self.assertIn("dry-run", out)
        self.assertFalse(self.target(run_dir).exists())
        self.assertNotIn("sink_checklist", (run_dir / "run.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_sink_integrity.py"
SPEC = importlib.util.spec_from_file_location("check_sink_integrity", SCRIPT)
check_sink_integrity = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(check_sink_integrity)

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


def run_check(repo: Path) -> tuple[int, str]:
    argv = ["check_sink_integrity.py", "--repo-root", str(repo)]
    stdout = io.StringIO()
    with mock.patch.object(sys, "argv", argv):
        with contextlib.redirect_stdout(stdout):
            code = check_sink_integrity.main()
    return code, stdout.getvalue()


class CheckSinkIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "work").mkdir()
        (self.repo / "evidence").mkdir()
        (self.repo / "knowledge").mkdir()
        self.catalog = self.repo / "knowledge" / "literature-review-catalog.md"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write_catalog(self, header: str, run_name: str) -> None:
        self.catalog.write_text(
            f"# 文献综述成果目录\n\n## {header}\n\n| ID | 主题 | 规模 | 审计入口 |\n|---|---|---|---|\n"
            f"| LR-TEST | test | 1 / 1 / 1 | [run](../evidence/{run_name}/run.json) |\n",
            encoding="utf-8",
        )

    def test_clean_state_no_drift(self) -> None:
        run_dir = make_bundle(self.repo / "work")
        shutil.copytree(run_dir, self.repo / "evidence" / run_dir.name)
        self.write_catalog("23 项成果", run_dir.name)

        code, out = run_check(self.repo)

        self.assertEqual(0, code)
        self.assertIn("no drift", out)
        self.assertIn("deletable remnant", out)

    def test_detects_settled_run_not_sunk(self) -> None:
        make_bundle(self.repo / "work")

        code, out = run_check(self.repo)

        self.assertEqual(1, code)
        self.assertIn("never sunk to evidence/", out)

    def test_in_progress_work_run_is_note_not_drift(self) -> None:
        make_bundle(self.repo / "work", status="in-progress")

        code, out = run_check(self.repo)

        self.assertEqual(0, code)
        self.assertIn("in-flight run", out)

    def test_detects_broken_catalog_link(self) -> None:
        self.write_catalog("23 项成果", "literature-review-missing-20260101")

        code, out = run_check(self.repo)

        self.assertEqual(1, code)
        self.assertIn("missing evidence dir", out)

    def test_gate_failed_in_main_section_is_drift(self) -> None:
        run_dir = make_bundle(self.repo / "evidence", gate_ok=False)
        self.write_catalog("23 项成果", run_dir.name)

        code, out = run_check(self.repo)

        self.assertEqual(1, code)
        self.assertIn("gate-failed run registered", out)
        self.assertIn("gate-failed section", out)

    def test_gate_failed_section_is_exempt(self) -> None:
        run_dir = make_bundle(self.repo / "evidence", gate_ok=False)
        self.write_catalog("覆盖门未过的补沉淀 run（2026-08-23 登记）", run_dir.name)

        code, out = run_check(self.repo)

        self.assertEqual(0, code)
        self.assertIn("no drift", out)

    def test_unregistered_evidence_bundle_is_note_not_drift(self) -> None:
        make_bundle(self.repo / "evidence")

        code, out = run_check(self.repo)

        self.assertEqual(0, code)
        self.assertIn("not referenced in catalog", out)

    def test_reader_variants_not_flagged_as_unregistered(self) -> None:
        make_bundle(self.repo / "evidence", name="literature-review-fixture-20260101-reader-v1")

        code, out = run_check(self.repo)

        self.assertEqual(0, code)
        self.assertNotIn("not referenced in catalog", out)


if __name__ == "__main__":
    unittest.main()

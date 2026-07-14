#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_run_bundle.py"
SPEC = importlib.util.spec_from_file_location("check_run_bundle", SCRIPT)
check_run_bundle = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(check_run_bundle)

DELIVERABLES = [
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
]


def make_run(
    tmp: Path,
    deliverables: list[str] | None = None,
    manifest_extra: dict | None = None,
    event_ids: list[str] | None = None,
    manifest_override: dict | None = None,
) -> Path:
    run_dir = tmp / "literature-review-test-20260708"
    run_dir.mkdir(parents=True, exist_ok=True)
    event_ids = event_ids if event_ids is not None else ["EA-TEST-2026-0001", "EA-TEST-2026-0002"]
    (run_dir / "evidence.jsonl").write_text(
        "\n".join(json.dumps({"event_id": event_id}) for event_id in event_ids) + "\n",
        encoding="utf-8",
    )
    names = DELIVERABLES if deliverables is None else deliverables
    for name in names:
        (run_dir / name).write_text(f"# {name}\n", encoding="utf-8")
    (run_dir / "evidence-appendix.md").write_text("# Evidence Appendix\n", encoding="utf-8")
    manifest = {
        "run": run_dir.name,
        "topic": "test",
        "time_range": "2026-01-01..2026-07-08",
        "event_count": len(event_ids),
        "files": {
            "evidence": "evidence.jsonl",
            "outputs": names,
            "appendix": "evidence-appendix.md",
        },
    }
    manifest.update(manifest_extra or {})
    if manifest_override is not None:
        manifest = manifest_override
    (run_dir / "run.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    return run_dir


class CheckRunBundleTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_compliant_bundle_passes(self) -> None:
        run_dir = make_run(self.tmp)
        self.assertEqual(check_run_bundle.check_run_bundle(run_dir), [])

    def test_missing_style_file_fails(self) -> None:
        # The perception-error failure: memo only, no zhihu/xiaohongshu, no declaration.
        run_dir = make_run(self.tmp, deliverables=["scientific-memo_keyan.md"])
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("zhihu-explainer_zhihu.md" in p for p in problems))
        self.assertTrue(any("xiaohongshu-post_xiaohongshu.md" in p for p in problems))
        self.assertTrue(any("three styles are the default" in p for p in problems))

    def test_declared_reduced_scope_passes(self) -> None:
        run_dir = make_run(
            self.tmp,
            deliverables=["scientific-memo_keyan.md"],
            manifest_extra={"style": "scientific-memo", "scope_note": "用户只要求科研备忘录"},
        )
        self.assertEqual(check_run_bundle.check_run_bundle(run_dir), [])

    def test_declared_scope_without_note_fails(self) -> None:
        run_dir = make_run(
            self.tmp,
            deliverables=["scientific-memo_keyan.md"],
            manifest_extra={"style": "scientific-memo"},
        )
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("scope_note" in p for p in problems))

    def test_field_drift_reported_with_standard_name(self) -> None:
        # The real drift: selected_event_count + files.memo instead of standard fields.
        run_dir = make_run(self.tmp)
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        del manifest["event_count"]
        manifest["selected_event_count"] = 2
        manifest["files"] = {"evidence": "evidence.jsonl", "memo": "scientific-memo_keyan.md"}
        (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("`selected_event_count` — use `event_count`" in p for p in problems))
        self.assertTrue(any("`memo` — use `outputs (list)`" in p for p in problems))
        self.assertTrue(any("missing required field `event_count`" in p for p in problems))

    def test_missing_local_evidence_fails(self) -> None:
        run_dir = make_run(self.tmp)
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        manifest["files"].pop("evidence")
        (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("self-contained" in p for p in problems))

    def test_event_count_mismatch_fails(self) -> None:
        run_dir = make_run(self.tmp, manifest_extra={"event_count": 54})
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("event_count=54" in p and "2 deduplicated" in p for p in problems))

    def test_deliverable_not_listed_in_outputs_fails(self) -> None:
        run_dir = make_run(self.tmp)
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        manifest["files"]["outputs"] = ["scientific-memo_keyan.md"]  # others exist on disk but unlisted
        (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("not listed in files.outputs" in p for p in problems))

    def test_in_progress_status_fails(self) -> None:
        # A birth-certificate run that was never settled must be reported as unfinished.
        run_dir = make_run(self.tmp, manifest_extra={"status": "in-progress"})
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("run not settled" in p for p in problems))

    def test_settled_status_passes(self) -> None:
        run_dir = make_run(self.tmp, manifest_extra={"status": "settled"})
        self.assertEqual(check_run_bundle.check_run_bundle(run_dir), [])

    def test_v2_requires_ready_coverage_artifacts(self) -> None:
        run_dir = make_run(
            self.tmp,
            manifest_extra={"workflow_version": 2, "review_mode": "scoping", "status": "settled"},
        )
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        manifest["files"].update(
            {
                "query_plan": "query-plan.json",
                "candidate_registry": "candidate-registry.json",
                "coverage_report": "coverage-report.json",
            }
        )
        (run_dir / "query-plan.json").write_text("{}\n", encoding="utf-8")
        (run_dir / "candidate-registry.json").write_text("{}\n", encoding="utf-8")
        (run_dir / "coverage-report.json").write_text(
            json.dumps({"stop_assessment": {"ready_to_stop": False, "unresolved": ["saturation"]}}),
            encoding="utf-8",
        )
        (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("coverage/saturation gate not passed" in item for item in problems))

        (run_dir / "coverage-report.json").write_text(
            json.dumps({"stop_assessment": {"ready_to_stop": True, "unresolved": []}}),
            encoding="utf-8",
        )
        self.assertEqual([], check_run_bundle.check_run_bundle(run_dir))

    def test_unknown_status_reported(self) -> None:
        run_dir = make_run(self.tmp, manifest_extra={"status": "done"})
        problems = check_run_bundle.check_run_bundle(run_dir)
        self.assertTrue(any("unknown status" in p for p in problems))

    def test_reused_evidence_counts_toward_self_containment(self) -> None:
        run_dir = make_run(self.tmp, event_ids=[])
        (run_dir / "evidence.jsonl").unlink()
        reused = run_dir / "reused"
        reused.mkdir()
        (reused / "prior-evidence.jsonl").write_text(
            json.dumps({"event_id": "EA-PRIOR-2026-0001"}) + "\n", encoding="utf-8"
        )
        manifest = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        manifest["files"] = {
            "reused_evidence": ["reused/prior-evidence.jsonl"],
            "outputs": DELIVERABLES,
            "appendix": "evidence-appendix.md",
        }
        manifest["event_count"] = 1
        (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.assertEqual(check_run_bundle.check_run_bundle(run_dir), [])


if __name__ == "__main__":
    unittest.main()

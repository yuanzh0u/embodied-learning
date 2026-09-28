"""run_status.py — one-shot run digest replacing agent file-loop improvisation."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "run_status.py"
_spec = importlib.util.spec_from_file_location("run_status_test_module", _SCRIPT)
run_status = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(run_status)


class RunStatusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run_dir = Path(self.tmp.name) / "literature-review-demo-20260101"
        self.run_dir.mkdir()
        (self.run_dir / "run.json").write_text(json.dumps({
            "run": "literature-review-demo-20260101", "topic": "demo",
            "review_mode": "scoping", "status": "in-progress", "files": {},
        }), encoding="utf-8")
        (self.run_dir / "pipeline-summary.json").write_text(json.dumps({
            "review_mode": "scoping", "candidate_count": 527, "screened_count": 40,
            "deep_read": {"total": 16, "pass": 10, "needs_review": 6, "failed": 0},
        }), encoding="utf-8")
        (self.run_dir / "candidate-registry.json").write_text(json.dumps({"candidates": [
            {"arxiv_id": "2412.01090", "title": "STATIC", "authors": ["S. Yang", "M. Lee"],
             "published": "2024-12-02T03:53:33Z"},
        ]}), encoding="utf-8")
        evidence = self.run_dir / "evidence"
        evidence.mkdir()
        events = []
        for index in range(4):
            events.append(json.dumps({
                "id": f"EA-DEMO-2026-{index:04d}",
                "paper": {"arxiv_id": "2412.01090", "title": "STATIC", "published": ""},
                "claim": f"claim {index}", "stance": "support" if index < 3 else "limit",
            }, ensure_ascii=False))
        (evidence / "2412.01090.jsonl").write_text("\n".join(events) + "\n", encoding="utf-8")
        (evidence / "empty.jsonl").write_text("", encoding="utf-8")
        (self.run_dir / "writing-brief.md").write_text("# brief\n", encoding="utf-8")

    def test_digest_aggregates_papers_metadata_and_floor(self):
        report = run_status.build_report(self.run_dir)
        self.assertEqual(report["status"], "in-progress")
        funnel = report["funnel"]
        self.assertEqual(funnel["candidates"], 527)
        self.assertEqual((funnel["paper_count"], funnel["event_count"]), (1, 4))
        self.assertEqual(funnel["cited_floor"], 10)  # scoping
        self.assertFalse(funnel["floor_met"])
        paper = report["papers"][0]
        # Registry join fills authors/published for the References section.
        self.assertEqual(paper["authors"], ["S. Yang", "M. Lee"])
        self.assertEqual(paper["published"], "2024-12-02T03:53:33Z")
        self.assertEqual(paper["stances"], {"support": 3, "limit": 1})
        self.assertEqual(len(paper["claims"]), 3)
        # Empty jsonl neither counts as a paper nor as an event.
        self.assertEqual(report["artifacts"]["writing-brief.md"], True)
        self.assertEqual(report["artifacts"]["review-packet.md"], False)

    def test_render_is_single_call_text(self):
        text = run_status.render(
            run_status.build_report(self.run_dir), self.run_dir, Path("/scripts")
        )
        self.assertIn("[funnel] 候选 527 → 筛选 40 → 深读 16", text)
        self.assertIn("S. Yang et al.", text)
        self.assertIn("引用篇数下限 10：不足", text)
        self.assertIn("[next]", text)
        self.assertIn("finalize_run.py", text)

    def test_missing_run_json_rejected(self):
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(run_status.main(["--run-dir", other]), 1)


if __name__ == "__main__":
    unittest.main()

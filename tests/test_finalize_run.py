"""finalize_run.py — the mechanical settle/publish tail of a review run.

Covers the contract that forced the 20260924 writer agent into hand-patching
run.json and reverse-engineering gate sources: the manifest is stamped here,
the cited-paper floor is enforced here, and publish/register/wiki are one
idempotent command.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "finalize_run.py"
_spec = importlib.util.spec_from_file_location("finalize_run_test_module", _SCRIPT)
finalize = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(finalize)


def _event(event_id: str) -> str:
    return json.dumps({"id": event_id, "claim": f"claim {event_id}"}, ensure_ascii=False) + "\n"


class FinalizeRunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb_root = Path(self.tmp.name) / "kb"
        self.kb_root.mkdir()
        self.run_dir = self.kb_root / "work" / "literature-review-demo-20260101"
        self.run_dir.mkdir(parents=True)
        (self.run_dir / "run.json").write_text(json.dumps({
            "run": "literature-review-demo-20260101",
            "topic": "demo",
            "time_range": "2023-01-01..2026-09-09",
            "review_mode": "rapid",
            "status": "in-progress",
            "files": {},
        }), encoding="utf-8")
        evidence = self.run_dir / "evidence"
        evidence.mkdir()
        for index in range(6):  # rapid floor is 6 papers
            (evidence / f"p{index}.jsonl").write_text(
                _event(f"EA-DEMO-2026-{index}"), encoding="utf-8"
            )
        (self.run_dir / "scientific-memo_keyan.md").write_text("# memo\n", encoding="utf-8")
        (self.run_dir / "evidence-appendix.md").write_text("# appendix\n", encoding="utf-8")
        (self.run_dir / "pipeline-summary.json").write_text(json.dumps({
            "review_mode": "rapid", "candidate_count": 421,
            "full_text_recovered_count": 40,
        }), encoding="utf-8")

    def finalize(self, *extra):
        """Run finalize with the two gates' subprocesses and the wiki rebuild
        mocked (their own suites cover them); the catalog registration runs
        for real against the temp KB."""
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)) as run, \
             mock.patch.object(finalize, "build_trace_map", return_value=(True, [])) as trace, \
             mock.patch.object(finalize, "register_run_in_catalog", return_value=True) as register:
            code = finalize.main([
                "--run-dir", str(self.run_dir), "--kb-root", str(self.kb_root), *extra,
            ])
        return code, run, register, trace

    def manifest(self):
        return json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))

    def test_stamps_manifest_and_publishes(self):
        code, run, register, trace = self.finalize()
        self.assertEqual(code, 0)
        manifest = self.manifest()
        self.assertEqual(manifest["event_count"], 6)
        self.assertEqual(manifest["evidence_papers"], 6)
        self.assertEqual(manifest["candidate_count"], 421)
        self.assertEqual(manifest["full_text_count"], 40)
        self.assertEqual(manifest["status"], "settled")
        self.assertEqual(manifest["files"]["evidence"], "evidence.jsonl")
        self.assertIn("scientific-memo_keyan.md", manifest["files"]["outputs"])
        # Single deliverable → reduced scope declared mechanically.
        self.assertEqual(manifest["style"], "scientific-memo")
        self.assertTrue(manifest["scope_note"])
        # Evidence consolidated next to run.json.
        merged = (self.run_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(merged), 6)
        # Published into the KB evidence layer.
        published = self.kb_root / "evidence" / "literature-review-demo-20260101"
        self.assertTrue((published / "run.json").is_file())
        self.assertEqual(
            json.loads((published / "run.json").read_text(encoding="utf-8"))["status"],
            "settled",
        )
        self.assertTrue((published / "evidence" / "p0.jsonl").is_file())
        self.assertTrue((published / "scientific-memo_keyan.md").is_file())
        # Gates ran with the run dir; catalog registration pointed at the copy.
        commands = [call.args[0] for call in run.call_args_list]
        bundle_cmd = next(cmd for cmd in commands if "check_run_bundle.py" in cmd[1])
        self.assertEqual(bundle_cmd[2], str(self.run_dir))
        trace.assert_called_once()
        register.assert_called_once()

    def test_trace_map_failure_blocks_with_fix_message(self):
        """UNCOVERED citations in a deliverable are a fix-and-rerun condition:
        finalize refuses and names the remedy, run stays in-progress."""
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)), \
             mock.patch.object(finalize, "build_trace_map",
                               return_value=(False, ["UNCOVERED scientific-memo_keyan.md: 9999.99999"])), \
             mock.patch.object(finalize, "register_run_in_catalog", return_value=True):
            code = finalize.main([
                "--run-dir", str(self.run_dir), "--kb-root", str(self.kb_root),
            ])
        self.assertEqual(code, 2)
        self.assertEqual(self.manifest()["status"], "in-progress")
        self.assertFalse((self.kb_root / "evidence" / "literature-review-demo-20260101").exists())

    def test_floor_gate_blocks_and_keeps_run_in_progress(self):
        (self.run_dir / "evidence" / "p3.jsonl").write_text("", encoding="utf-8")
        (self.run_dir / "evidence" / "p4.jsonl").write_text("", encoding="utf-8")
        (self.run_dir / "evidence" / "p5.jsonl").write_text("", encoding="utf-8")
        code, run, _, _ = self.finalize()
        self.assertEqual(code, 2)
        self.assertEqual(self.manifest()["status"], "in-progress")
        self.assertFalse((self.kb_root / "evidence" / "literature-review-demo-20260101").exists())
        run.assert_not_called()

    def test_three_deliverables_need_no_style_field(self):
        for name in ("zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"):
            (self.run_dir / name).write_text(f"# {name}\n", encoding="utf-8")
        code, _, _, _ = self.finalize()
        self.assertEqual(code, 0)
        manifest = self.manifest()
        self.assertNotIn("style", manifest)
        self.assertNotIn("scope_note", manifest)

    def test_rerun_is_idempotent(self):
        code, _, _, _ = self.finalize()
        self.assertEqual(code, 0)
        code, _, _, _ = self.finalize()
        self.assertEqual(code, 0)
        merged = (self.run_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(merged), 6)

    def test_declared_style_never_sweeps_the_packet_in(self):
        # A declared style must not have the disk scan's survey mapping
        # (survey → review-packet.md) sweep the mechanically generated packet
        # into outputs and the citation gate: the packet's inventory tables
        # carry bare event IDs and can never pass an article audit.
        manifest = self.manifest()
        manifest["style"] = "scientific-memo"
        (self.run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.run_dir / "review-packet.md").write_text(
            "| paper | EA-DEMO-2026-0 |\n", encoding="utf-8"
        )
        code, run, _, _ = self.finalize()
        self.assertEqual(code, 0)
        outputs = self.manifest()["files"]["outputs"]
        self.assertIn("scientific-memo_keyan.md", outputs)
        self.assertNotIn("review-packet.md", outputs)
        commands = [call.args[0] for call in run.call_args_list]
        audit_cmd = next(cmd for cmd in commands if "audit_citations.py" in cmd[1])
        self.assertIn("audit_citations.py", audit_cmd[1])
        articles = [b for a, b in zip(audit_cmd, audit_cmd[1:]) if a == "--article"]
        self.assertEqual(len(articles), 1)
        self.assertIn("scientific-memo_keyan.md", articles[0])
        self.assertTrue(all("review-packet.md" not in a for a in audit_cmd))

    def test_declared_style_with_missing_article_fails_before_gates(self):
        (self.run_dir / "scientific-memo_keyan.md").unlink()
        manifest = self.manifest()
        manifest["style"] = "scientific-memo"
        (self.run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        code, run, register, trace = self.finalize()
        self.assertEqual(code, 2)
        self.assertEqual(self.manifest()["status"], "in-progress")
        run.assert_not_called()
        register.assert_not_called()

    def test_abstract_tier_never_counts_toward_evidence_papers(self):
        """Abstract-tier events are positioning-only: they add event_count and
        abstract_papers, but the cited-paper floor keeps measuring deep-read
        papers only."""
        evidence = self.run_dir / "evidence"
        abstract_events = [
            {"event_id": f"EA-DEMO-2026-{900 + index:04d}", "tier": "abstract",
             "paper": {"arxiv_id": f"2601.0000{index}"}}
            for index in range(6)
        ]
        (evidence / "abstract-tier.jsonl").write_text(
            "\n".join(json.dumps(event) for event in abstract_events) + "\n",
            encoding="utf-8",
        )
        code, _, _, _ = self.finalize()
        self.assertEqual(code, 0)
        manifest = self.manifest()
        self.assertEqual(manifest["event_count"], 12)  # 6 deep read + 6 abstract
        self.assertEqual(manifest["evidence_papers"], 6)
        self.assertEqual(manifest["abstract_papers"], 6)

    def test_abstract_papers_alone_cannot_satisfy_the_floor(self):
        evidence = self.run_dir / "evidence"
        for index in range(6):
            (evidence / f"p{index}.jsonl").write_text("", encoding="utf-8")
        (evidence / "abstract-tier.jsonl").write_text(
            "\n".join(
                json.dumps({"event_id": f"EA-DEMO-2026-{900 + index:04d}", "tier": "abstract",
                            "paper": {"arxiv_id": f"2601.0000{index}"}})
                for index in range(6)
            ) + "\n",
            encoding="utf-8",
        )
        code, run, _, _ = self.finalize()
        self.assertEqual(code, 2)  # floor counts full-text papers only
        self.assertEqual(self.manifest()["status"], "in-progress")
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()

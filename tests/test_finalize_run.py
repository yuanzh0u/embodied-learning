"""finalize_run.py — the mechanical settle/publish tail of a review run.

Covers the contract that forced the 20260924 writer agent into hand-patching
run.json and reverse-engineering gate sources: the manifest is stamped here,
the cited-paper floor is enforced here, and publish/register/wiki are one
idempotent command.
"""

from _entry import invoke, parse

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
# Load the implementation module (not the scripts/ forwarder) so mock.patch on
# module attributes reaches the live globals the functions read.
from embodied_learning.wiki.run import finalize  # noqa: E402


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
        (self.run_dir / "writing-brief.md").write_text("# brief\n", encoding="utf-8")
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
            code = invoke("run.py", "finalize", [
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
        self.assertTrue((published / "writing-brief.md").is_file())
        # Gates ran with the run dir; catalog registration pointed at the copy.
        commands = [call.args[0] for call in run.call_args_list]
        bundle_cmd = next(cmd for cmd in commands if "check-bundle" in cmd)
        self.assertEqual(bundle_cmd[3], str(self.run_dir))
        # The script path must be the REAL scripts root's run.py. A
        # Path(__file__).parent guess resolved to
        # embodied_learning/wiki/run/run.py and the gate died ENOENT
        # (2026-10-12, smoke run #1).
        self.assertTrue(
            bundle_cmd[1].endswith("run.py") and Path(bundle_cmd[1]).is_file(),
            bundle_cmd,
        )
        self.assertNotIn("embodied_learning", bundle_cmd[1])
        trace.assert_called_once()
        register.assert_called_once()

    def test_stamps_all_workflow_v2_files_keys(self):
        """workflow_version 2 requires files.query_plan / candidate_registry /
        coverage_report / evidence so the run is self-contained. finalize used
        to stamp only evidence+outputs, so a run with every artifact on disk
        still failed check_run_bundle on three "missing" declarations
        (2026-10-09)."""
        (self.run_dir / "query-plan.json").write_text("{}", encoding="utf-8")
        (self.run_dir / "candidate-registry.json").write_text("{}", encoding="utf-8")
        (self.run_dir / "coverage-report.json").write_text("{}", encoding="utf-8")
        code, _run, _register, _trace = self.finalize()
        self.assertEqual(0, code)
        files = self.manifest()["files"]
        self.assertEqual("query-plan.json", files.get("query_plan"))
        self.assertEqual("candidate-registry.json", files.get("candidate_registry"))
        self.assertEqual("coverage-report.json", files.get("coverage_report"))
        self.assertEqual("evidence.jsonl", files.get("evidence"))

    def test_publishes_funnel_artifact_and_stamps_files_funnel(self):
        """funnel.json is a run artifact like the appendix: published with the
        bundle and declared in files.* — but its absence is not an error
        (historical runs predate it)."""
        (self.run_dir / "funnel.json").write_text(
            json.dumps({"schema_version": 1, "stages": {}}), encoding="utf-8"
        )
        code, _run, _register, _trace = self.finalize()
        self.assertEqual(0, code)
        self.assertEqual("funnel.json", self.manifest()["files"].get("funnel"))
        published = self.kb_root / "evidence" / "literature-review-demo-20260101"
        self.assertTrue((published / "funnel.json").is_file())

    def test_run_without_funnel_publishes_fine_and_declares_nothing(self):
        code, _run, _register, _trace = self.finalize()
        self.assertEqual(0, code)
        self.assertNotIn("funnel", self.manifest()["files"])

    def test_declare_gate_exception_writes_manifest_and_notes(self):
        code, run, register, trace = self.finalize(
            "--declare-gate-exception", "cited_paper_floor",
            "--reason", "选文策略如实缩水：该 niche 仅 3 篇核心论文",
        )
        self.assertEqual(code, 0)
        manifest = self.manifest()
        self.assertIn("cited_paper_floor", manifest["gate_exceptions"])
        self.assertTrue(any("选文策略如实缩水" in str(note) for note in manifest["notes"]))

    def test_declare_gate_exception_requires_reason(self):
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)), \
             mock.patch.object(finalize, "build_trace_map", return_value=(True, [])), \
             mock.patch.object(finalize, "register_run_in_catalog", return_value=True):
            code = invoke("run.py", "finalize", [
                "--run-dir", str(self.run_dir), "--kb-root", str(self.kb_root),
                "--declare-gate-exception", "saturation",
            ])
        self.assertEqual(code, 2)

    def test_floor_gate_waived_by_cited_paper_floor_exception(self):
        for stem in ("p3", "p4", "p5"):
            (self.run_dir / "evidence" / f"{stem}.jsonl").write_text("", encoding="utf-8")
        code, run, register, trace = self.finalize(
            "--declare-gate-exception", "cited_paper_floor", "--reason", "诚实薄审",
        )
        self.assertEqual(code, 0)
        self.assertEqual(self.manifest()["status"], "settled")

    def test_floor_gate_shortfall_reports_paper_list_and_stops(self):
        """2026-09-30 定案：精读数量不够 = 用户决策点——汇报选定的精读论文列表
        后立即停轮等决策，不薄审落盘、不换选文策略、不继续硬修。"""
        for stem in ("p3", "p4", "p5"):
            (self.run_dir / "evidence" / f"{stem}.jsonl").write_text("", encoding="utf-8")
        (self.run_dir / "screening.json").write_text(json.dumps({
            "selection_rule": {"strategy": "smart", "detail": "smart selected 3/481 considered; shortfall: only 3 relevant (limit 40), not padded"},
        }), encoding="utf-8")
        import contextlib, io
        buf = io.StringIO()
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)), \
             mock.patch.object(finalize, "build_trace_map", return_value=(True, [])), \
             contextlib.redirect_stdout(buf):
            code = invoke("run.py", "finalize", [
                "--run-dir", str(self.run_dir), "--kb-root", str(self.kb_root),
            ])
        out = buf.getvalue()
        self.assertEqual(code, 2)
        self.assertEqual(self.manifest()["status"], "in-progress")
        self.assertIn("精读数量不够", out)
        self.assertIn("已选定并深读的论文列表", out)
        for stem in ("p0", "p1", "p2"):
            self.assertIn(stem, out)  # 报告含选定论文清单
        self.assertIn("立即停轮", out)
        self.assertIn("等待用户决策", out)
        self.assertIn("严禁薄审落盘", out)
        self.assertIn("严禁更换选文策略", out)

    def test_trace_map_failure_blocks_with_fix_message(self):
        """UNCOVERED citations in a deliverable are a fix-and-rerun condition:
        finalize refuses and names the remedy, run stays in-progress."""
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)), \
             mock.patch.object(finalize, "build_trace_map",
                               return_value=(False, ["UNCOVERED scientific-memo_keyan.md: 9999.99999"])), \
             mock.patch.object(finalize, "register_run_in_catalog", return_value=True):
            code = invoke("run.py", "finalize", [
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

    def test_birth_style_declares_the_single_article_scope(self):
        """A memo-only run born from a single-style interview answer must
        settle: the writer wrote exactly what was asked, and finalize used to
        refuse it with 成稿不足三种 because `style` is stamped by finalize
        itself (2026-10-21 点云匹配)."""
        manifest = self.manifest()
        manifest["inputs"] = {"source": "wiki-interview", "target_style": "scientific-memo"}
        (self.run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        code, _, _, _ = self.finalize()
        self.assertEqual(code, 0)
        manifest = self.manifest()
        self.assertEqual(manifest["style"], "scientific-memo")
        self.assertTrue(manifest["scope_note"])

    def test_birth_style_does_not_shrink_a_three_article_bundle(self):
        # The declaration is a required minimum, not a cap: a run asked for one
        # face but shipping all three keeps the standard three-style contract.
        manifest = self.manifest()
        manifest["inputs"] = {"source": "wiki-interview", "target_style": "scientific-memo"}
        (self.run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        for name in ("zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"):
            (self.run_dir / name).write_text(f"# {name}\n", encoding="utf-8")
        code, _, _, _ = self.finalize()
        self.assertEqual(code, 0)
        self.assertNotIn("style", self.manifest())

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
        audit_cmd = next(cmd for cmd in commands if "audit-citations" in cmd)
        self.assertIn("audit-citations", audit_cmd)
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

    def test_kb_root_inferred_from_run_dir_when_omitted(self):
        """--kb-root is optional: <kb-root>/work/<run> layout publishes into the
        KB that owns the run (2026-09-30 absolute-pose published into
        ~/Documents/arxiv because the writer omitted --kb-root)."""
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)), \
             mock.patch.object(finalize, "build_trace_map", return_value=(True, [])), \
             mock.patch.object(finalize, "register_run_in_catalog", return_value=True):
            code = invoke("run.py", "finalize", ["--run-dir", str(self.run_dir)])
        self.assertEqual(code, 0)
        published = self.kb_root / "evidence" / "literature-review-demo-20260101"
        self.assertTrue((published / "run.json").is_file())

    def test_kb_root_mismatch_refuses_cross_kb_publish(self):
        """An explicit --kb-root that disagrees with the run's owning KB is a
        hard error — never copy a run into a foreign knowledge base."""
        other_kb = Path(self.tmp.name) / "other-kb"
        other_kb.mkdir()
        with mock.patch.object(finalize.subprocess, "run", return_value=mock.Mock(returncode=0)), \
             mock.patch.object(finalize, "build_trace_map", return_value=(True, [])), \
             mock.patch.object(finalize, "register_run_in_catalog", return_value=True):
            code = invoke("run.py", "finalize", [
                "--run-dir", str(self.run_dir), "--kb-root", str(other_kb),
            ])
        self.assertEqual(code, 2)
        self.assertFalse((other_kb / "evidence").exists())
        self.assertFalse((self.kb_root / "evidence").exists())
        self.assertEqual(self.manifest()["status"], "in-progress")


if __name__ == "__main__":
    unittest.main()

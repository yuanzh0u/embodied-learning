"""run_status.py — one-shot run digest replacing agent file-loop improvisation."""

from _entry import invoke, parse

import contextlib
import importlib.util
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = "embodied_learning.wiki.run.status"  # implementation module (old scripts/run_status.py deleted)
run_status = importlib.import_module(_SCRIPT)


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
        # Deep-read funnel inputs: screening queue + extraction outcomes + audits.
        (self.run_dir / "screening-ids.txt").write_text(
            "2412.01090\n2110.10805\n2203.02677\n", encoding="utf-8"
        )
        (self.run_dir / "extraction-summary.json").write_text(json.dumps({"results": [
            {"paper_id": "2412.01090", "evidence_eligible": True},
            {"paper_id": "2110.10805", "evidence_eligible": False},
            {"paper_id": "2203.02677", "evidence_eligible": False},
        ]}), encoding="utf-8")
        (self.run_dir / "screening.json").write_text(json.dumps({"candidates": [
            {"arxiv_id": "2110.10805", "matched_title_terms": ["depth", "temporal"]},
        ]}), encoding="utf-8")
        paper_notes = self.run_dir / "paper-notes"
        paper_notes.mkdir()
        (paper_notes / "2203.02677.json").write_text("{}", encoding="utf-8")  # note without audit

    def test_deep_read_funnel_resolves_per_paper_stage(self):
        """The per-paper stage table replaces the writer's inline-python loops
        over extraction/audit/screening files."""
        rows = {row["arxiv_id"]: row for row in run_status.build_report(self.run_dir)["paper_funnel"]}
        self.assertEqual(rows["2412.01090"]["stage"], "evidence")
        self.assertEqual(rows["2110.10805"]["stage"], "held")
        self.assertEqual(rows["2110.10805"]["matched_title_terms"], ["depth", "temporal"])
        # Note present but audit missing → retryable deep-read failure.
        self.assertEqual(rows["2203.02677"]["stage"], "deep-read-failed")

    def test_packet_command_is_fully_specified(self):
        """The [next] packet command must be executable verbatim — the writer
        used to read the packet script's argparse source to discover flags."""
        text = run_status.render(
            run_status.build_report(self.run_dir), self.run_dir, Path("/scripts"), Path("/skills")
        )
        command_line = next(line for line in text.splitlines() if "review-packet --run-dir" in line or "review-packet" in line and "write.py" in line)
        self.assertIn("--run-dir", command_line)
        self.assertIn("--topic demo", command_line)
        self.assertIn("--review-mode scoping", command_line)
        self.assertIn("--consolidate-evidence", command_line)
        # Per-paper JSONL fallback (empty files skipped) when no consolidated file exists.
        self.assertIn("--evidence-jsonl", command_line)

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
        self.assertEqual(report["artifacts"]["funnel.json"], False)

    def test_funnel_artifact_shows_up_once_written(self):
        (self.run_dir / "funnel.json").write_text(
            json.dumps({"schema_version": 1, "stages": {}}), encoding="utf-8"
        )
        report = run_status.build_report(self.run_dir)
        self.assertEqual(report["artifacts"]["funnel.json"], True)

    def test_funnel_falls_back_to_registry_and_screening_mid_run(self):
        # pipeline-summary.json is written at the driver's tail — an agent
        # reading status mid-run used to see "候选 None → 筛选 None" while the
        # registry and screening list were already on disk.
        (self.run_dir / "pipeline-summary.json").unlink()
        report = run_status.build_report(self.run_dir)
        funnel = report["funnel"]
        self.assertEqual(funnel["candidates"], 1)  # candidate-registry.json
        self.assertEqual(funnel["screened"], 3)  # screening-ids.txt

    def test_render_is_single_call_text(self):
        text = run_status.render(
            run_status.build_report(self.run_dir), self.run_dir, Path("/scripts"), Path("/skills")
        )
        self.assertIn("[funnel] 候选 527 → 筛选 40 → 深读 16", text)
        self.assertIn("S. Yang et al.", text)
        self.assertIn("引用篇数下限 10：不足", text)
        self.assertIn("[next]", text)
        self.assertIn("run.py", text)

    def test_gates_block_surfaces_stop_assessment_and_exceptions(self):
        (self.run_dir / "coverage-report.json").write_text(json.dumps({
            "saturation_rounds": [
                {"batch": "r1", "channel": "arxiv-api", "new_unique_rate": 1.0},
                {"batch": "r2", "channel": "citation-seeds", "new_unique_rate": 0.91},
            ],
            "stop_assessment": {
                "ready_to_stop": False,
                "checks": {"candidate_floor": True, "saturation": False},
                "unresolved": ["saturation"],
            },
        }), encoding="utf-8")
        (self.run_dir / "run.json").write_text(json.dumps({
            "run": "literature-review-demo-20260101", "topic": "demo",
            "review_mode": "scoping", "status": "in-progress", "files": {},
            "gate_exceptions": ["saturation"],
        }), encoding="utf-8")
        report = run_status.build_report(self.run_dir)
        text = run_status.render(report, self.run_dir, Path("/scripts"), Path("/skills"))
        self.assertIn("[gates]", text)
        self.assertIn("saturation=未过", text)
        self.assertIn("已声明豁免：saturation", text)
        self.assertIn("gate_exceptions", text)  # 修法提示里的逃生门键名
        self.assertIn("新篇目率 0.91", text)

    def test_deep_read_row_carries_failure_reason(self):
        (self.run_dir / "paper-notes" / "2203.02677.failed.json").write_text(
            json.dumps({"outcome": "failed", "reason": "agent 异常：timeout"}, ensure_ascii=False),
            encoding="utf-8",
        )
        report = run_status.build_report(self.run_dir)
        text = run_status.render(report, self.run_dir, Path("/scripts"), Path("/skills"))
        self.assertIn("因:agent 异常：timeout", text)

    def test_next_block_carries_verbatim_gate_commands(self):
        (self.run_dir / "scientific-memo_keyan.md").write_text("# memo\n", encoding="utf-8")
        report = run_status.build_report(self.run_dir)
        text = run_status.render(report, self.run_dir, Path("/scripts"), Path("/skills"))
        self.assertIn("check-bundle", text)
        # Pre-settle flag: without it the gate always fails on the lifecycle
        # line the writer must not touch (finalize flips the status).
        self.assertIn("--pre-settle", text)
        self.assertIn("--article", text)
        self.assertIn("audit-citations", text)
        self.assertIn("audit-article-quality", text)
        self.assertIn("--declare-gate-exception", text)

    def test_single_style_scope_comes_from_the_birth_input(self):
        """The writer reads status before finalize stamps `style`; the
        interview answer must already narrow the gate commands to one article
        (2026-10-21 点云匹配: status listed all three, check-bundle demanded
        all three)."""
        manifest = json.loads((self.run_dir / "run.json").read_text(encoding="utf-8"))
        manifest["inputs"] = {"source": "wiki-interview", "target_style": "scientific-memo"}
        (self.run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.run_dir / "scientific-memo_keyan.md").write_text("# memo\n", encoding="utf-8")
        report = run_status.build_report(self.run_dir)
        self.assertEqual(report["style"], "scientific-memo")
        self.assertFalse(report["style_declared_in_manifest"])
        text = run_status.render(report, self.run_dir, Path("/scripts"), Path("/skills"))
        citation_lines = [line for line in text.splitlines() if "audit-citations" in line]
        self.assertEqual(len(citation_lines), 1)
        self.assertIn("scientific-memo_keyan.md", citation_lines[0])
        self.assertNotIn("zhihu-explainer_zhihu.md", citation_lines[0])

    def test_next_block_prints_resolved_kb_root_not_placeholder(self):
        """The [next] finalize command carries the real --kb-root (inferred from
        the <kb-root>/work/<run> layout), never the literal <kb-root> placeholder
        the writer used to guess wrong (2026-09-30 absolute-pose)."""
        with tempfile.TemporaryDirectory() as tmp:
            kb_root = Path(tmp) / "kb"
            run_dir = kb_root / "work" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            for name in ("run.json", "pipeline-summary.json"):
                source = self.run_dir / name
                (run_dir / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            text = run_status.render(
                run_status.build_report(run_dir), run_dir, Path("/scripts"), Path("/skills")
            )
        self.assertIn(f"--kb-root {kb_root}", text)
        self.assertNotIn("--kb-root <kb-root>", text)

    def test_missing_run_json_rejected(self):
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(invoke("run.py", "status", ["--run-dir", other]), 1)

    def test_next_commands_point_at_real_scripts(self):
        """main() must resolve both roots via find_roots(), not
        Path(__file__).parent / scripts_root/"skills" — those guesses printed
        [next] commands pointing at embodied_learning/wiki/run/run.py and
        scripts/skills/.../write.py, neither of which exists (2026-10-12)."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(invoke("run.py", "status", ["--run-dir", str(self.run_dir)]), 0)
        text = buf.getvalue()
        self.assertNotIn("embodied_learning", text)
        self.assertNotIn("scripts/skills", text)
        # every `python3 <path> *.py` suggestion must exist on disk
        paths = re.findall(r"python3 (\S+\.py)", text)
        self.assertTrue(paths, text)
        for path in paths:
            self.assertTrue(Path(path).is_file(), path)
        self.assertTrue(any(p.endswith("write.py") for p in paths), paths)


if __name__ == "__main__":
    unittest.main()

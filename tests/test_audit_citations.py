#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_citations.py"
SPEC = importlib.util.spec_from_file_location("audit_citations", SCRIPT)
audit_citations = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(audit_citations)


def write_evidence(path: Path, event_ids: list[str], arxiv_by_event: dict[str, str] | None = None) -> None:
    lines = []
    for event_id in event_ids:
        record: dict[str, object] = {"event_id": event_id, "claim": "x"}
        if arxiv_by_event and event_id in arxiv_by_event:
            record["paper"] = {"arxiv_id": arxiv_by_event[event_id]}
        lines.append(json.dumps(record))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_appendix(path: Path, event_ids: list[str]) -> None:
    chunks = ["# Evidence Appendix: test", ""]
    for event_id in event_ids:
        chunks.extend([f"### {event_id}", "", "- Claim: x", ""])
    path.write_text("\n".join(chunks), encoding="utf-8")


def linked(event_id: str, target: str = "evidence-appendix.md") -> str:
    return f"[{event_id}]({target}#{audit_citations.anchor_for(event_id)})"


class AuditCitationsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.evidence = self.tmp / "evidence.jsonl"
        self.appendix = self.tmp / "evidence-appendix.md"
        self.article = self.tmp / "memo.md"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_audit(self) -> list[str]:
        ids, paper_ids, problems = audit_citations.load_event_ids([self.evidence])
        anchors, appendix_problems = audit_citations.appendix_anchors(self.appendix)
        problems.extend(appendix_problems)
        problems.extend(audit_citations.audit_article(self.article, self.appendix, anchors, ids, paper_ids))
        return problems

    def test_clean_article_passes(self) -> None:
        write_evidence(self.evidence, ["EA-DATA-2026-0001", "EA-DATA-2026-0002"])
        write_appendix(self.appendix, ["EA-DATA-2026-0001", "EA-DATA-2026-0002"])
        self.article.write_text(
            f"论点一({linked('EA-DATA-2026-0001')})与论点二({linked('EA-DATA-2026-0002')})。\n",
            encoding="utf-8",
        )
        self.assertEqual(self.run_audit(), [])

    def test_invented_path_reported_as_wrong_target(self) -> None:
        # Real failure: article linked into a nonexistent review-bundle/ directory.
        write_evidence(self.evidence, ["EA-DATA-2026-0001"])
        write_appendix(self.appendix, ["EA-DATA-2026-0001"])
        self.article.write_text(
            f"论点({linked('EA-DATA-2026-0001', 'review-bundle/evidence-appendix.md')})。\n",
            encoding="utf-8",
        )
        problems = self.run_audit()
        self.assertTrue(any("review-bundle/evidence-appendix.md" in p for p in problems))

    def test_dead_anchor_reported(self) -> None:
        write_evidence(self.evidence, ["EA-DATA-2026-0001"])
        write_appendix(self.appendix, ["EA-DATA-2026-0001"])
        self.article.write_text(
            "论点([EA-DATA-2026-0001](evidence-appendix.md#ea-data-2026-9999))。\n",
            encoding="utf-8",
        )
        problems = self.run_audit()
        self.assertTrue(any("dead anchor" in p for p in problems))

    def test_citation_outside_evidence_set_reported(self) -> None:
        # Real failure: memo cited 54 events while the run settled only 6.
        write_evidence(self.evidence, ["EA-DATA-2026-DQ-0001"])
        write_appendix(self.appendix, ["EA-DATA-2026-DQ-0001", "EA-TWM-2026-0005"])
        self.article.write_text(
            f"新证据({linked('EA-DATA-2026-DQ-0001')})与历史证据({linked('EA-TWM-2026-0005')})。\n",
            encoding="utf-8",
        )
        problems = self.run_audit()
        self.assertTrue(any("outside loaded evidence set: EA-TWM-2026-0005" in p for p in problems))

    def test_bare_event_id_reported(self) -> None:
        write_evidence(self.evidence, ["EA-DATA-2026-0001"])
        write_appendix(self.appendix, ["EA-DATA-2026-0001"])
        self.article.write_text("论点(EA-DATA-2026-0001)。\n", encoding="utf-8")
        problems = self.run_audit()
        self.assertTrue(any("bare event ID" in p for p in problems))

    def test_paper_link_style_body_passes(self) -> None:
        # New citation contract: body cites arXiv paper links; References carries event anchors.
        write_evidence(self.evidence, ["EA-DATA-2026-0001"], {"EA-DATA-2026-0001": "2607.06442"})
        write_appendix(self.appendix, ["EA-DATA-2026-0001"])
        self.article.write_text(
            "论点来自([SIEVE](https://arxiv.org/abs/2607.06442))。\n\n"
            f"## References\n\n- [SIEVE](https://arxiv.org/abs/2607.06442) — 证据: {linked('EA-DATA-2026-0001')}\n",
            encoding="utf-8",
        )
        self.assertEqual(self.run_audit(), [])

    def test_paper_link_without_evidence_coverage_reported(self) -> None:
        write_evidence(self.evidence, ["EA-DATA-2026-0001"], {"EA-DATA-2026-0001": "2607.06442"})
        write_appendix(self.appendix, ["EA-DATA-2026-0001"])
        self.article.write_text(
            "论点([SIEVE](https://arxiv.org/abs/2607.06442)),但还有([幽灵论文](https://arxiv.org/abs/2699.99999))。\n",
            encoding="utf-8",
        )
        problems = self.run_audit()
        self.assertTrue(any("no event in loaded evidence set: 2699.99999" in p for p in problems))

    def test_versioned_arxiv_link_normalized(self) -> None:
        write_evidence(self.evidence, ["EA-DATA-2026-0001"], {"EA-DATA-2026-0001": "2607.06442"})
        write_appendix(self.appendix, ["EA-DATA-2026-0001"])
        self.article.write_text("论点([SIEVE](https://arxiv.org/abs/2607.06442v2))。\n", encoding="utf-8")
        self.assertEqual(self.run_audit(), [])

    def test_run_json_event_count_mismatch_reported(self) -> None:
        write_evidence(self.evidence, ["EA-DATA-2026-0001", "EA-DATA-2026-0002"])
        run_json = self.tmp / "run.json"
        run_json.write_text(
            json.dumps({"event_count": 54, "files": {"evidence": "evidence.jsonl"}}),
            encoding="utf-8",
        )
        ids, _, _ = audit_citations.load_event_ids([self.evidence])
        problems = audit_citations.audit_run_json(run_json, ids)
        self.assertTrue(any("event_count=54" in p and "2 deduplicated" in p for p in problems))

    def test_run_json_missing_file_reported(self) -> None:
        run_json = self.tmp / "run.json"
        run_json.write_text(
            json.dumps({"files": {"outputs": ["missing-memo.md"]}}),
            encoding="utf-8",
        )
        problems = audit_citations.audit_run_json(run_json, set())
        self.assertTrue(any("missing-memo.md" in p for p in problems))


if __name__ == "__main__":
    unittest.main()

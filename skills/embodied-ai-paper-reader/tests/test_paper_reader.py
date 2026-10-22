#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))  # src/ modules import embodied_learning.* at load time

# Scripts that stayed in the skill: validate_paper_note / audit_claim_support /
# validate/audit/project moved to note_tools.py (impl loaded via package import
# below); build_reading_packet and update_reading_ledger remain skill entries.
_SCRIPTS_DIR = ROOT / "scripts"


def load_script(name: str):  # type: ignore[no-untyped-def]
    mapping = {"build_reading_packet": "embodied_learning.parse.reading_packet",
               "update_reading_ledger": "embodied_learning.knowledge.reading_ledger"}
    return importlib.import_module(mapping[name])


def _unused_load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS_DIR / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


build_packet = load_script("build_reading_packet")
ledger = load_script("update_reading_ledger")

from embodied_learning.knowledge import claim_support as audit_support
from embodied_learning.knowledge import evidence_projection as projector
from embodied_learning.knowledge import paper_note as validator


FULL_CONTEXT = (
    "Across three real-robot tasks, the proposed interface improved success rate by 12 percentage "
    "points over Baseline X, but the study did not evaluate deformable objects or long-horizon tasks."
)
FULL_TEXT = (
    "## 1 Introduction\nThis paper studies portable robot demonstrations and states the research problem. "
    "The authors claim a universal interface under the evaluated setup.\n\n"
    "## 3 Method\nThe system records synchronized camera poses, gripper states, and actions. "
    "Its central assumption is reliable pose tracking.\n\n"
    "## 4 Experiments\n" + FULL_CONTEXT + " Additional ablations isolate the tracking component.\n\n"
    "## 6 Limitations\nThe authors state that the experiments cover only rigid tabletop manipulation. "
    "These limitations constrain transfer to other embodiments and environments.\n"
) * 3


def extraction() -> dict:
    return {
        "paper_id": "2402.10329",
        "available": True,
        "evidence_eligible": True,
        "source_format": "html",
        "extraction_method": "html-latexml",
        "quality": {"grade": "high", "text_chars": len(FULL_TEXT)},
        "text": FULL_TEXT,
        "sections": [
            {"path": "1 Introduction", "title": "1 Introduction", "char_count": 120},
            {"path": "3 Method", "title": "3 Method", "char_count": 140},
            {"path": "4 Experiments", "title": "4 Experiments", "char_count": 220},
            {"path": "6 Limitations", "title": "6 Limitations", "char_count": 160},
        ],
        "ocr": {"pages_used": []},
    }


def valid_note(card_count: int = 1, status: str = "accepted") -> dict:
    cards = []
    for index in range(card_count):
        cards.append(
            {
                "card_id": f"2402.10329-C{index + 1:02d}",
                "claim": "The interface improved task success in the three evaluated real-robot tasks.",
                "stance": "conditional",
                "relation": "Supports data-interface portability only within the evaluated task scope.",
                "confidence": "direct",
                "claim_basis": "reported-result",
                "summary": "The experiment reports a scoped improvement and explicitly leaves other settings unevaluated.",
                "locator": "4 Experiments",
                "source_context": FULL_CONTEXT,
                "evidence_type": "experiment",
                "quantitative": {
                    "metric": "success rate",
                    "value_or_direction": "12 percentage points",
                    "comparator": "Baseline X",
                    "task_or_sample": "three real-robot tasks",
                    "locator": "4 Experiments",
                },
                "verification": {
                    "status": "passed",
                    "checked_against": "full-text",
                    "rationale": "The experiment reports the same task set, metric, comparator, and direction, and the claim remains limited to those tasks.",
                },
            }
        )
    return {
        "schema_version": 1,
        "paper": {
            "arxiv_id": "2402.10329",
            "title": "Universal Manipulation Interface",
            "published": "2024-02-15",
            "url": "https://arxiv.org/abs/2402.10329",
            "authors": [{"name": "Jane Doe", "author_key": "jane-doe", "role": "paper-author", "institutions": []}],
        },
        "review": {"question": "When does UMI data transfer?", "topic_ids": ["EA-DATA"], "mode": "scoping"},
        "extraction": {
            "source_format": "html",
            "method": "html-latexml",
            "quality": "high",
            "full_text_available": True,
            "ocr_pages": [],
            "visual_validation": "not-required",
        },
        "reading": {
            "status": status,
            "paper_type": "method",
            "relevance": {"decision": "include", "reason": "Directly tests the review's data-transfer mechanism."},
            "sections_read": [
                {"locator": "1 Introduction", "role": "problem", "purpose": "Identify the research question."},
                {"locator": "3 Method", "role": "method-or-design", "purpose": "Assess the proposed interface and assumptions."},
                {"locator": "4 Experiments", "role": "results-or-analysis", "purpose": "Verify task-level results and ablations."},
                {"locator": "6 Limitations", "role": "conclusion-or-limitations", "purpose": "Bound the transfer claim."},
            ],
            "sections_skipped": [],
        },
        "research_question": "Can a portable interface collect demonstrations that transfer across evaluated robot tasks?",
        "contributions": ["A portable demonstration interface and an evaluation on three real-robot tasks."],
        "method": {"summary": "Synchronizes camera pose, gripper state, and actions for policy training.", "assumptions": ["Reliable pose tracking"]},
        "study_context": {"datasets": ["collected demonstrations"], "tasks": ["three tasks"], "embodiments": ["one robot"], "sample_or_scale": "three real-robot tasks"},
        "evaluation": {"design": "Controlled comparison on three tasks.", "baselines": ["Baseline X"], "metrics": ["success rate"], "ablations": ["tracking ablation"]},
        "findings": [{"finding": "Success improved in the tested tasks.", "scope": "Three real-robot tasks only.", "locator": "4 Experiments"}],
        "limitations": {
            "author_status": "found",
            "author_stated": [{"limitation": "Only rigid tabletop manipulation was evaluated.", "locator": "6 Limitations"}],
            "reader_inferred": [{"boundary": "The result does not establish transfer to deformable or long-horizon tasks.", "basis": "Those task families are absent from the evaluation."}],
        },
        "transfer_boundary": "Applies to the tested rigid tabletop tasks with reliable pose tracking.",
        "critical_appraisal": {
            "design_strengths": ["Task-level comparison and ablation"],
            "design_risks": ["Narrow task and embodiment coverage"],
            "baseline_fairness": "Baseline X uses the same task protocol, but compute parity is not reported.",
            "metric_validity": "Success rate measures completion but not safety or recovery quality.",
            "reproducibility": "The interface is described, while some calibration details are not reported.",
            "external_validity": "External validity is limited to rigid tabletop manipulation under reliable tracking.",
        },
        "evidence_cards": cards,
        "core_citations": [],
        "notes": "",
    }


class CardVisualsTest(unittest.TestCase):
    """Evidence cards may carry figures/tables joined at note assembly; the
    projection must copy them onto the event's evidence (the writer's packet
    renders them into the brief/appendix)."""

    def test_projection_passes_card_visuals_through(self) -> None:
        figure = {
            "figure_id": "S3.F3",
            "caption": "The Aria device used for egocentric recordings.",
            "image_url": "https://arxiv.org/html/2311.18259v4/figs/aria/aria.png",
            "section": "3 Ego-Exo4D dataset",
            "usage": "作者用该图展示采集 rig。",
        }
        table = {
            "table_id": "S1.T1",
            "caption": "Dataset comparison.",
            "section": "3 Ego-Exo4D dataset",
            "rows": [["Dataset", "Year"], ["Ego-Exo4D", "2023"]],
            "usage": "作者用该表对比数据集。",
        }
        note = valid_note()
        note["evidence_cards"][0]["figures"] = [figure]
        note["evidence_cards"][0]["tables"] = [table]
        audit = audit_support.audit(note, extraction())
        events = projector.project(note, audit, "EA-DATA-2026", 1)
        self.assertEqual(1, len(events))
        self.assertEqual([figure], events[0]["evidence"]["figures"])
        self.assertEqual([table], events[0]["evidence"]["tables"])

    def test_projection_without_visuals_keeps_evidence_shape(self) -> None:
        note = valid_note()
        audit = audit_support.audit(note, extraction())
        events = projector.project(note, audit, "EA-DATA-2026", 1)
        self.assertNotIn("figures", events[0]["evidence"])
        self.assertNotIn("tables", events[0]["evidence"])

    def test_card_visuals_ignores_empty_lists(self) -> None:
        self.assertEqual({}, projector.card_visuals({"figures": [], "tables": []}))
        self.assertEqual(
            {"figures": [{"figure_id": "S1.F1"}]},
            projector.card_visuals({"figures": [{"figure_id": "S1.F1"}], "tables": []}),
        )


class PaperReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_build_packet_requires_complete_non_ocr_text(self) -> None:
        source_format, text = build_packet.complete_text(extraction())
        self.assertEqual("html", source_format)
        self.assertIn("4 Experiments", text)
        selected_only = extraction()
        selected_only.pop("text")
        selected_only["selected_passages"] = [{"text": FULL_CONTEXT}]
        with self.assertRaisesRegex(ValueError, "selected passages"):
            build_packet.complete_text(selected_only)
        ocr = extraction()
        ocr["extraction_method"] = "pdf-ocr"
        with self.assertRaisesRegex(ValueError, "OCR-derived"):
            build_packet.complete_text(ocr)

    def test_validator_enforces_deep_read_and_quantitative_context(self) -> None:
        note = valid_note()
        errors, warnings = validator.validate_note(note)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        note["reading"]["sections_read"] = note["reading"]["sections_read"][:1]
        note["evidence_cards"][0]["quantitative"].pop("comparator")
        errors, _ = validator.validate_note(note)
        self.assertTrue(any("missing section roles" in item for item in errors))
        self.assertTrue(any("quantitative.comparator" in item for item in errors))

    def test_audit_requires_context_at_locator(self) -> None:
        result = audit_support.audit(valid_note(), extraction())
        self.assertEqual("pass", result["status"])
        note = valid_note()
        note["evidence_cards"][0]["source_context"] = "A completely unrelated statement about underwater navigation and sonar sensors."
        result = audit_support.audit(note, extraction())
        self.assertEqual("reject", result["status"])
        note = valid_note()
        note["evidence_cards"][0]["locator"] = "3 Method"
        result = audit_support.audit(note, extraction())
        self.assertEqual("reject", result["status"])

    def test_audit_counts_table_numbers_as_locator_evidence(self) -> None:
        """Quantitative results canonically live in tables; the extractor keeps
        them out of section prose. A card whose measurement tokens appear only
        in extraction.tables must pass the quant gate (2026-10-15 纹理映射:
        5/12 papers lost every card because the numbers only existed in
        tables)."""
        note = valid_note()
        note["evidence_cards"][0]["quantitative"] = {
            "metric": "PSNR",
            "value_or_direction": "29.03 vs 21.27",
            "comparator": "Baseline X",
            "task_or_sample": "the benchmark split",
            "locator": "4 Experiments",
        }
        # Without tables the same card must still trip the quant gate.
        result = audit_support.audit(note, extraction())
        self.assertEqual("needs-review", result["status"])
        self.assertEqual(["needs-review"], [card["status"] for card in result["cards"]])
        self.assertIn("tables", result["cards"][0]["reasons"][0])
        # With the numbers present in a table (caption or cells), it passes.
        ext = extraction()
        ext["tables"] = [
            {
                "id": "S4.T1",
                "caption": "Table 1: Comparison on the benchmark.",
                "section_index": None,
                "section": "",
                "rows": [["Method", "PSNR"], ["Ours", "29.03"], ["Baseline X", "21.27"]],
            }
        ]
        result = audit_support.audit(note, ext)
        self.assertEqual("pass", result["status"])
        self.assertEqual(["pass"], [card["status"] for card in result["cards"]])

    def test_projection_skips_unaudited_cards_without_zeroing_the_paper(self) -> None:
        """One needs-review card must not discard the paper's passing cards
        (2026-10-15 纹理映射: each of 5 papers lost 3-4 passing cards to one
        table-number card). Reject a card, not the paper."""
        note = valid_note(card_count=2)
        audit = audit_support.audit(note, extraction())
        audit["status"] = "needs-review"
        audit["cards"][1]["status"] = "needs-review"
        audit["cards"][1]["reasons"] = ["fewer than one third of quantitative metric/value/comparator tokens occur at the locator or in the paper's tables"]
        events = projector.project(note, audit, "EA-DATA-2026", 1)
        self.assertEqual(1, len(events))
        self.assertEqual("2402.10329-C01", events[0]["paper_reading"]["card_id"])
        # IDs stay contiguous from start_seq even when a card is skipped.
        self.assertEqual("EA-DATA-2026-0001", events[0]["event_id"])

    def test_projection_without_any_passing_card_returns_empty(self) -> None:
        """Every card needs-review: the paper contributes nothing, but it is a
        zero-event outcome rather than a projection error."""
        note = valid_note(card_count=2)
        audit = audit_support.audit(note, extraction())
        audit["status"] = "needs-review"
        for card in audit["cards"]:
            card["status"] = "needs-review"
        events = projector.project(note, audit, "EA-DATA-2026", 1)
        self.assertEqual([], events)

    def test_projection_emits_one_event_per_verified_card(self) -> None:
        note = valid_note(card_count=2)
        audit = audit_support.audit(note, extraction())
        events = projector.project(note, audit, "EA-DATA-2026", 7)
        self.assertEqual(2, len(events))
        self.assertEqual("EA-DATA-2026-0007", events[0]["event_id"])
        self.assertEqual("2402.10329-C02", events[1]["paper_reading"]["card_id"])
        self.assertEqual("html-latexml", events[0]["evidence"]["extraction"]["method"])

    def test_ledger_reports_reading_states_separately(self) -> None:
        records = [
            {"status": "full-text-recovered"},
            {"status": "deep-read"},
            {"status": "accepted"},
            {"status": "unavailable"},
        ]
        report = ledger.summary(records)
        self.assertEqual(3, report["full_text_recovered_count"])
        self.assertEqual(2, report["deep_read_count"])
        self.assertEqual(1, report["claim_verified_paper_count"])
        self.assertEqual(1, report["accepted_evidence_paper_count"])
        self.assertEqual(1, report["unavailable_count"])

    def test_tex_source_extraction_builds_packet_and_passes_pipeline(self) -> None:
        """TeX-source (tex-pandoc) extraction rides the html contract end to end."""
        tex_extraction = extraction()
        tex_extraction["source_format"] = "tex"
        tex_extraction["extraction_method"] = "tex-pandoc"
        source_format, text = build_packet.complete_text(tex_extraction)
        self.assertEqual("tex", source_format)
        self.assertIn("4 Experiments", text)

        note = valid_note()
        note["extraction"].update({"source_format": "tex", "method": "tex-pandoc", "visual_validation": "not-required"})
        errors, warnings = validator.validate_note(note)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        audit = audit_support.audit(note, tex_extraction)
        self.assertEqual("pass", audit["status"])
        events = projector.project(note, audit, "EA-DATA-2026", 1)
        self.assertEqual("tex-pandoc", events[0]["evidence"]["extraction"]["method"])

    def test_arxiv2md_method_rides_the_same_contract(self) -> None:
        """arxiv2md markdown is authoritative text like tex-pandoc."""
        md_extraction = extraction()
        md_extraction["source_format"] = "tex"
        md_extraction["extraction_method"] = "arxiv2md"
        source_format, text = build_packet.complete_text(md_extraction)
        self.assertEqual("tex", source_format)

        note = valid_note()
        note["extraction"].update({"source_format": "tex", "method": "arxiv2md", "visual_validation": "not-required"})
        errors, _ = validator.validate_note(note)
        self.assertEqual([], errors)
        audit = audit_support.audit(note, md_extraction)
        self.assertEqual("pass", audit["status"])
        events = projector.project(note, audit, "EA-DATA-2026", 1)
        self.assertEqual("arxiv2md", events[0]["evidence"]["extraction"]["method"])

    def test_cli_end_to_end_projection_passes_hub_validator(self) -> None:
        note_path = self.tmp / "paper-note.json"
        extraction_path = self.tmp / "extraction.json"
        audit_path = self.tmp / "audit.json"
        events_path = self.tmp / "events.jsonl"
        note_path.write_text(json.dumps(valid_note(), ensure_ascii=False), encoding="utf-8")
        extraction_path.write_text(json.dumps(extraction(), ensure_ascii=False), encoding="utf-8")
        audit_result = audit_support.audit(valid_note(), extraction())
        audit_path.write_text(json.dumps(audit_result, ensure_ascii=False), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable, str(ROOT / "scripts" / "read.py") if False else str(ROOT.parents[1] / "skills" / "embodied-ai-paper-reader" / "scripts" / "read.py"), "project-evidence-events",
                "--paper-note", str(note_path), "--audit", str(audit_path),
                "--id-prefix", "EA-DATA-2026", "--output", str(events_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        hub_validator = ROOT.parent / "embodied-ai-literature-hub" / "scripts" / "fetch.py"
        hub_validator_argv = ["write-lit-outputs"]
        completed = subprocess.run(
            [sys.executable, str(hub_validator), *hub_validator_argv, "--evidence-jsonl", str(events_path), "--validate-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr + completed.stdout)



    def test_summary_first_omits_complete_text_body(self) -> None:
        extraction_path = self.tmp / "extraction.json"
        output = self.tmp / "packet.md"
        extraction_path.write_text(json.dumps(extraction(), ensure_ascii=False), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "read.py") if False else str(ROOT.parents[1] / "skills" / "embodied-ai-paper-reader" / "scripts" / "read.py"), "build-reading-packet",
                "--extraction",
                str(extraction_path),
                "--review-question",
                "When does UMI data transfer?",
                "--topic-id",
                "EA-DATA",
                "--summary-first",
                "--max-section-chars",
                "120",
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        body = output.read_text(encoding="utf-8")
        self.assertIn("Packet mode: summary-first", body)
        self.assertIn("Summary-first section windows", body)
        self.assertIn("Omitted from this summary-first packet", body)
        # Full repeated corpus must not be embedded.
        self.assertLess(len(body), len(FULL_TEXT))
        self.assertNotIn(FULL_TEXT, body)

    def test_default_packet_still_embeds_complete_text(self) -> None:
        extraction_path = self.tmp / "extraction.json"
        output = self.tmp / "packet-full.md"
        extraction_path.write_text(json.dumps(extraction(), ensure_ascii=False), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "read.py") if False else str(ROOT.parents[1] / "skills" / "embodied-ai-paper-reader" / "scripts" / "read.py"), "build-reading-packet",
                "--extraction",
                str(extraction_path),
                "--review-question",
                "When does UMI data transfer?",
                "--topic-id",
                "EA-DATA",
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        body = output.read_text(encoding="utf-8")
        self.assertIn("## Complete extracted text", body)
        self.assertIn("4 Experiments", body)
        self.assertIn(FULL_TEXT[:80], body)

if __name__ == "__main__":
    unittest.main()

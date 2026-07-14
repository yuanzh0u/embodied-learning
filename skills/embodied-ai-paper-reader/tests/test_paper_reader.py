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


def load_script(name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


build_packet = load_script("build_reading_packet")
validator = load_script("validate_paper_note")
audit_support = load_script("audit_claim_support")
projector = load_script("project_evidence_events")
ledger = load_script("update_reading_ledger")


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
                sys.executable, str(ROOT / "scripts" / "project_evidence_events.py"),
                "--paper-note", str(note_path), "--audit", str(audit_path),
                "--id-prefix", "EA-DATA-2026", "--output", str(events_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        hub_validator = ROOT.parent / "embodied-ai-literature-hub" / "scripts" / "write_lit_outputs.py"
        completed = subprocess.run(
            [sys.executable, str(hub_validator), "--evidence-jsonl", str(events_path), "--validate-only"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr + completed.stdout)


if __name__ == "__main__":
    unittest.main()

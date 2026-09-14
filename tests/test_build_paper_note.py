"""Tests for scripts/build_paper_note.py — skeleton → note assembler."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = REPO_ROOT / "scripts" / "build_paper_note.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_paper_note", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def sample_extraction() -> dict:
    sections = [
        {"index": 0, "title": "Abstract", "path": "Abstract", "char_count": 100},
        {"index": 1, "title": "1 Introduction", "path": "1 Introduction", "char_count": 400},
        {"index": 2, "title": "3 Method", "path": "3 Method", "char_count": 500},
        {"index": 3, "title": "4.1 Quantitative Results", "path": "4.1 Quantitative Results", "char_count": 300},
    ]
    text = (
        "## Abstract\nThis paper presents a fast calibration method. Extensive experiments show accuracy gains.\n"
        "## 1 Introduction\nCalibration matters for fusion. Our first objective is to select a subset of Gaussians that preserves the global structure.\n"
        "## 3 Method\nWe propose an efficient geometry-driven pruning score that leverages intrinsic attributes.\n"
        "## 4.1 Quantitative Results\nAs shown in Table 1, our method increases PSNR from 21.27 to 29.03 on the benchmark at 50% sparsity.\n"
    )
    return {
        "paper_id": "2401.00001",
        "title": "Fast Calibration",
        "available": True,
        "extraction_method": "html-latexml",
        "source_format": "html",
        "quality": {"grade": "high", "text_chars": len(text)},
        "sections": sections,
        "text": text,
    }


class BuildPaperNoteTest(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.extraction = sample_extraction()

    def skeleton(self, **overrides):
        base = {
            "arxiv_id": "2401.00001",
            "paper_type": "method",
            "relevance_reason": "r",
            "research_question": "q",
            "contributions": ["c"],
            "method_summary": "m",
            "findings": ["f"],
            "limitations": ["只在合成数据验证"],
            "cards": [
                {
                    "claim": "选择保持全局结构的高斯子集。",
                    "stance": "support",
                    "evidence_type": "method",
                    "quote": "Our first objective is to select a subset of Gaussians that preserves the global structure.",
                    "locator_hint": "Introduction",
                    "quantitative": False,
                },
                {
                    "claim": "PSNR 从 21.27 提升到 29.03。",
                    "stance": "support",
                    "evidence_type": "experiment",
                    "quote": "As shown in Table 1, our method increases PSNR from 21.27 to 29.03 on the benchmark at 50% sparsity.",
                    "locator_hint": "Quantitative",
                    "quantitative": {"metric": "PSNR", "value_or_direction": "21.27 -> 29.03", "comparator": "baseline"},
                },
            ],
        }
        base.update(overrides)
        return base

    def test_assemble_passes_validation_and_audit(self):
        note, problems = self.mod.assemble_note(self.skeleton(), self.extraction, Path("/tmp"))
        self.assertEqual(problems, [])
        self.assertEqual(len(note["evidence_cards"]), 2)
        self.assertEqual(note["reading"]["status"], "evidence-ready")
        errors, warnings = self.mod.validator.validate_note(note)
        self.assertEqual(errors, [])
        audit = self.mod.auditor.audit(note, self.extraction)
        self.assertEqual(audit.get("status"), "pass")

    def test_locators_resolve_to_exact_titles(self):
        note, _ = self.mod.assemble_note(self.skeleton(), self.extraction, Path("/tmp"))
        locators = [card["locator"] for card in note["evidence_cards"]]
        self.assertEqual(locators, ["1 Introduction", "4.1 Quantitative Results"])

    def test_abstract_only_quote_is_dropped_with_reason(self):
        skeleton = self.skeleton(
            cards=[
                {
                    "claim": "c",
                    "stance": "support",
                    "evidence_type": "method",
                    "quote": "This paper presents a fast calibration method.",
                    "locator_hint": "Abstract",
                    "quantitative": False,
                }
            ]
        )
        note, problems = self.mod.assemble_note(skeleton, self.extraction, Path("/tmp"))
        self.assertEqual(note["evidence_cards"], [])
        self.assertTrue(any("Abstract/References" in p for p in problems))

    def test_paraphrased_quote_is_auto_repaired(self):
        # Agent garbles the quote slightly; the assembler must repair it from
        # the section surface so the audit's exact-match gate passes.
        skeleton = self.skeleton(
            cards=[
                {
                    "claim": "c",
                    "stance": "support",
                    "evidence_type": "method",
                    "quote": "Our first objective is to select a subset of Gaussians that preserves global structure.",
                    "locator_hint": "Introduction",
                    "quantitative": False,
                }
            ]
        )
        note, problems = self.mod.assemble_note(skeleton, self.extraction, Path("/tmp"))
        self.assertEqual(len(note["evidence_cards"]), 1)
        audit = self.mod.auditor.audit(note, self.extraction)
        self.assertEqual(audit.get("status"), "pass")

    def test_findings_and_limitations_shapes(self):
        note, _ = self.mod.assemble_note(self.skeleton(), self.extraction, Path("/tmp"))
        self.assertEqual(set(note["findings"][0]), {"finding", "scope", "locator"})
        inferred = note["limitations"]["reader_inferred"][0]
        self.assertIn("boundary", inferred)
        self.assertTrue(inferred["basis"])
        self.assertEqual(note["limitations"]["author_status"], "not-found")

    def test_max_cards_enforced(self):
        cards = self.skeleton()["cards"] * 3
        note, _ = self.mod.assemble_note(self.skeleton(cards=cards), self.extraction, Path("/tmp"))
        self.assertLessEqual(len(note["evidence_cards"]), 4)


if __name__ == "__main__":
    unittest.main()

"""Tests for scripts/build_paper_note.py — skeleton → note assembler."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # build_paper_note imports embodied_learning.*

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = "embodied_learning.knowledge.note_assembly"  # implementation module (old scripts/build_paper_note.py deleted)
def load_module():
    module = importlib.import_module(BUILDER_PATH)
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

    def test_ligature_laden_pdf_text_still_matches_plain_quotes(self):
        """PDF text extractors emit Latin ligatures (U+FB01 for "fi"), so a
        quote typed with plain letters never matched the extracted full text.
        Regression: card 3 of 2507.15186 failed raw match and passed once the
        ligature was folded (130 occurrences in that paper)."""
        skeleton = self.skeleton(cards=[
            {
                "claim": "R-Simp is linear for a fixed output size.",
                "quote": "R-Simp is linear for a fixed output size.",
                "locator_hint": "Results",
                "stance": "support",
                "evidence_type": "quantitative",
            }
        ])
        extraction = dict(self.extraction)
        extraction["text"] = (
            "## Results\n\nThus R-Simp is linear for a fi xed output size.\n"
        ).replace("fi xed", "\ufb01xed")  # force the ligature form
        note, problems = self.mod.assemble_note(skeleton, extraction, Path("/tmp"))
        self.assertEqual(len(note["evidence_cards"]), 1)
        self.assertEqual(note["paper"]["title"].strip() != "", True)

    def test_page_shaped_extraction_resolves_body_quotes(self):
        """pdf-text extractions carry `pages` and no `sections`. Without a
        sections normalizer every card died in the "quote only in Abstract"
        branch because the body rescan over an empty `sections` found nothing
        (2026-10-09, 2507.15186: 4/4 cards dropped)."""
        body = "The algorithm simplifies in reverse from coarse to fine, guaranteeing display quality."
        skeleton = self.skeleton(cards=[
            {
                "claim": "Progressive simplification guarantees display quality.",
                "quote": body,
                "locator_hint": "Method",
                "stance": "support",
                "evidence_type": "method",
            }
        ])
        extraction = {
            "paper_id": "2507.15186",
            "available": True,
            "source_format": "pdf",
            "extraction_method": "pdf-text",
            "title": "Model Simplification Through Refinement",
            "pages": [
                {"page": 1, "text": "Model Simplification Through Refinement\nAbstract\nWe simplify meshes."},
                {"page": 2, "text": "Method\n" + body},
            ],
            "quality": {"grade": "high"},
        }
        note, _problems = self.mod.assemble_note(skeleton, extraction, Path("/tmp"))
        self.assertEqual(len(note["evidence_cards"]), 1)
        self.assertNotEqual(note["evidence_cards"][0]["locator"].lower(), "abstract")

    def test_map_read_status_used_when_no_cards(self):
        """`mapped` is not in the STATUSES vocabulary (map-read is); emitting it
        made an otherwise valid note schema-invalid."""
        note, _problems = self.mod.assemble_note(self.skeleton(cards=[]), self.extraction, Path("/tmp"))
        self.assertEqual(note["reading"]["status"], "map-read")

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

    def test_card_figure_ids_join_extraction_records(self):
        self.extraction["figures"] = [
            {
                "id": "S3.F3",
                "caption": "The Aria device used for egocentric recordings.",
                "image_url": "https://arxiv.org/html/2401.00001v2/figs/aria.png",
                "section": "3 Method",
            }
        ]
        self.extraction["tables"] = [
            {"id": "S4.T1", "caption": "PSNR comparison.", "section": "4.1 Quantitative Results",
             "rows": [["Method", "PSNR"], ["Ours", "29.03"]]}
        ]
        skeleton = self.skeleton()
        skeleton["cards"][0]["figure_id"] = "S3.F3"
        skeleton["cards"][0]["figure_usage"] = "作者用该图展示标定 rig。"
        skeleton["cards"][1]["table_id"] = "S4.T1"
        skeleton["cards"][1]["figure_usage"] = "作者用该表对比 PSNR。"
        note, problems = self.mod.assemble_note(skeleton, self.extraction, Path("/tmp"))
        self.assertEqual(problems, [])
        first = note["evidence_cards"][0]["figures"][0]
        self.assertEqual(first["figure_id"], "S3.F3")
        self.assertEqual(first["image_url"], "https://arxiv.org/html/2401.00001v2/figs/aria.png")
        self.assertEqual(first["caption"], "The Aria device used for egocentric recordings.")
        self.assertEqual(first["usage"], "作者用该图展示标定 rig。")
        second = note["evidence_cards"][1]["tables"][0]
        self.assertEqual(second["table_id"], "S4.T1")
        self.assertEqual(second["rows"], [["Method", "PSNR"], ["Ours", "29.03"]])
        # The URL/caption/rows come from the extraction; the agent never invents them.
        self.assertNotIn("figures", note["evidence_cards"][1])

    def test_unknown_figure_ids_are_dropped(self):
        skeleton = self.skeleton()
        skeleton["cards"][0]["figure_id"] = "S9.F99"  # hallucinated
        skeleton["cards"][0]["figure_usage"] = "不存在"
        note, problems = self.mod.assemble_note(skeleton, self.extraction, Path("/tmp"))
        self.assertNotIn("figures", note["evidence_cards"][0])
        self.assertTrue(any("S9.F99" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()

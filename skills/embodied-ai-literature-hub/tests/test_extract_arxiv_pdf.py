#!/usr/bin/env python3

from __future__ import annotations

import importlib
import sys
import unittest
import os
import tempfile
# Keep the machine-wide rate-limit gate off the real shared state: tests
# here mock urlopen but still pass through the gate, so redirect its state
# dir before any gated module is exercised.
os.environ.setdefault("EMBODIED_RATELIMIT_DIR", tempfile.mkdtemp(prefix="ratelimit-test-"))
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_script(name: str):
    # Package imports: fetch/*.py do `from .. import ratelimit`, which needs
    # package context (a bare spec_from_file_location load breaks).
    MODNAMES = {
        "extract_arxiv_content": "embodied_learning.fetch.chain",
        "extract_arxiv_html": "embodied_learning.fetch.html",
        "extract_arxiv_pdf": "embodied_learning.fetch.pdf",
    }
    return importlib.import_module(MODNAMES[name])


pdf = load_script("extract_arxiv_pdf")
content = load_script("extract_arxiv_content")


class PdfQualityTest(unittest.TestCase):
    def test_quality_marks_sparse_extraction_low(self) -> None:
        pages = [
            {"page": 1, "text": "title only", "extraction_method": "pdf-text"},
            {"page": 2, "text": "", "extraction_method": "pdf-text"},
        ]
        quality = pdf.text_quality(pages, min_chars_per_page=100)
        self.assertEqual("low", quality["grade"])
        self.assertEqual([1, 2], quality["low_text_pages"])

    def test_quality_marks_dense_text_high_and_ranks_pages(self) -> None:
        dense = ("robot manipulation data quality and closed loop evaluation " * 30).strip()
        pages = [
            {"page": 1, "text": dense, "extraction_method": "pdf-text"},
            {"page": 2, "text": dense.replace("quality", "planning"), "extraction_method": "pdf-text"},
        ]
        quality = pdf.text_quality(pages, min_chars_per_page=100)
        ranked = pdf.rank_pages(pages, ["quality", "closed loop"], top=2, include_text=True)
        self.assertEqual("high", quality["grade"])
        self.assertEqual(1, ranked[0]["page"])
        self.assertIn("text", ranked[0])

    def test_auto_ocr_reports_missing_tools_instead_of_silent_success(self) -> None:
        pages = [{"page": 1, "text": "", "extraction_method": "pdf-text"}]
        with mock.patch.object(pdf, "ocr_tools", return_value=(None, None)):
            used, warnings, backend = pdf.apply_ocr(Path("paper.pdf"), pages, "auto", "eng", 220, 100)
        self.assertEqual([], used)
        self.assertEqual("unavailable", backend)
        self.assertIn("tools are unavailable", warnings[0])


class ContentFallbackTest(unittest.TestCase):
    def args(self):
        return type("Args", (), {
            "paper_id": "2601.00001",
            "terms": "robot,quality",
            "force_pdf": False,
        })()

    def test_uses_pdf_when_html_is_unavailable(self) -> None:
        html = {
            "available": False,
            "extraction_method": "html-unavailable",
            "quality": {"grade": "low"},
            "evidence_eligible": False,
        }
        pdf_output = {
            "available": True,
            "extraction_method": "pdf-text",
            "quality": {"grade": "high"},
            "evidence_eligible": True,
            "ocr": {"pages_used": []},
        }
        with mock.patch.object(content, "try_html", return_value=html), mock.patch.object(
            content, "try_pdf", return_value=pdf_output
        ):
            result = content.extract_content(self.args())
        self.assertEqual("pdf-text", result["extraction_method"])
        self.assertTrue(result["evidence_eligible"])
        self.assertEqual(["html-unavailable", "pdf-text"], [item["method"] for item in result["attempts"]])

    def test_does_not_download_pdf_when_html_passes(self) -> None:
        html = {
            "available": True,
            "extraction_method": "html-latexml",
            "quality": {"grade": "high"},
            "evidence_eligible": True,
        }
        with mock.patch.object(content, "try_html", return_value=html), mock.patch.object(content, "try_pdf") as try_pdf:
            result = content.extract_content(self.args())
        self.assertEqual("html-latexml", result["extraction_method"])
        try_pdf.assert_not_called()

    def test_pdf_keeps_every_page_only_for_paper_reader_handoff(self) -> None:
        args = type("Args", (), {
            "paper_id": "2601.00001", "pdf_url": None, "pdf_file": None,
            "pdf_cache_dir": "/tmp", "max_pages": 0, "top_sections": 3,
            "ocr_mode": "never", "ocr_language": "eng", "ocr_dpi": 220,
            "min_chars_per_page": 180, "include_selected_text": True,
            "include_full_text": True,
        })()
        extracted = {
            "available": True, "extraction_method": "pdf-text",
            "quality": {"grade": "high"}, "evidence_eligible": True,
            "pages": [{"page": 1, "text": "complete page", "extraction_method": "pdf-text"}],
            "ranked_pages": [{"page": 1, "text": "complete page"}],
        }
        with mock.patch.object(content.extract_arxiv_pdf, "extract_pdf_document", return_value=dict(extracted)):
            result = content.try_pdf(args, ["robot"])
        self.assertIn("pages", result)
        args.include_full_text = False
        with mock.patch.object(content.extract_arxiv_pdf, "extract_pdf_document", return_value=dict(extracted)):
            result = content.try_pdf(args, ["robot"], want_full_text=False)
        self.assertNotIn("pages", result)


if __name__ == "__main__":
    unittest.main()

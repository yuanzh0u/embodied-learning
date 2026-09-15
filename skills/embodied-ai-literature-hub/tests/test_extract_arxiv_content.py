#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))  # modules under src/ import src.* at load time
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]


def load_script(name: str):
    MODNAMES = {"extract_arxiv_content": "chain", "extract_arxiv_html": "html",
               "extract_arxiv_pdf": "pdf"}
    path = ROOT / "src" / "fetch" / f"{MODNAMES[name]}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def load_entry(name: str):
    path = ROOT / "skills" / "embodied-ai-literature-hub" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


content = load_script("extract_arxiv_content")
content_entry = load_entry("extract_arxiv_content")

HTML_FIXTURE = """
<html><head><title>[2403.12550] GS-ICP-SLAM</title></head><body>
<h1 class="ltx_title ltx_title_document">Efficient RGBD SLAM with 3D Gaussian Splatting</h1>
<section class="ltx_section" id="S1">
<h2 class="ltx_title ltx_title_section">1 Introduction</h2>
<div id="S1.p1" class="ltx_para"><p class="ltx_p">SLAM matters.</p></div>
</section>
</body></html>
"""


def make_args(**overrides) -> content.ContentOptions:
    base = dict(
        paper_id="2403.12550",
        terms="SLAM,Gaussian",
        html_url=None,
        pdf_url=None,
        pdf_file=None,
        html_cache_dir="/tmp/kb-test-html",
        pdf_cache_dir="/tmp/kb-test-pdfs",
        timeout=1.0,
        top_sections=3,
        max_pages=0,
        ocr_mode="never",
        ocr_language="eng",
        ocr_dpi=220,
        min_chars_per_page=180,
        minimum_html_chars=100,
        force_pdf=False,
        include_selected_text=False,
        include_full_text=False,
        render_markdown=False,
    )
    base.update(overrides)
    return content.ContentOptions(**base)


class DocumentTitleTest(unittest.TestCase):
    def test_prefers_latexml_h1_over_title_tag(self) -> None:
        self.assertEqual("Efficient RGBD SLAM with 3D Gaussian Splatting", content.document_title(HTML_FIXTURE))

    def test_title_tag_fallback_strips_arxiv_id(self) -> None:
        html = "<html><head><title>[2401.12345] A Study of Robots - arXiv:2401.12345</title></head><body></body></html>"
        self.assertEqual("A Study of Robots", content.document_title(html))

    def test_empty_html_gives_empty_title(self) -> None:
        self.assertEqual("", content.document_title(""))

    def test_void_element_in_h1_does_not_swallow_document(self) -> None:
        # LaTeXML line-broken titles use <br class="ltx_break">, a void element;
        # counting it as a nested tag used to capture the whole document as "title".
        html = (
            "<html><head><title>Real-Time LiDAR SLAM</title></head><body>"
            '<h1 class="ltx_title ltx_title_document">Real-Time LiDAR Gaussian Splatting SLAM'
            '<br class="ltx_break">via Geometry-Aware Covariance Coupling</h1>'
            "<p>Long body that must not leak into the title.</p></body></html>"
        )
        title = content.document_title(html)
        self.assertEqual("Real-Time LiDAR Gaussian Splatting SLAM via Geometry-Aware Covariance Coupling", title)
        self.assertNotIn("body", title.lower())

    def test_overlong_h1_capture_falls_back_to_title_tag(self) -> None:
        # Defensive: if malformed markup still defeats depth tracking, prefer <title>.
        html = (
            "<html><head><title>Short Correct Title</title></head><body>"
            '<h1 class="ltx_title_document">' + "word " * 120 + "</h1>"
            "</body></html>"
        )
        self.assertEqual("Short Correct Title", content.document_title(html))

    def test_title_surfaces_in_try_html_output(self) -> None:
        with mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(True, HTML_FIXTURE)), \
             mock.patch.object(content.extract_arxiv_html, "extract_structured", return_value=None):
            args = make_args()
            output = content.try_html(args, ["SLAM"])
        self.assertEqual("Efficient RGBD SLAM with 3D Gaussian Splatting", output["title"])


class ResolveOutputPathTest(unittest.TestCase):
    def test_none_stays_none(self) -> None:
        self.assertIsNone(content.resolve_output_path(None, "2403.12550"))
        self.assertIsNone(content.resolve_output_path("", "2403.12550"))

    def test_directory_gets_paper_id_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = content.resolve_output_path(tmpdir, "2403.12550")
        self.assertEqual(f"{tmpdir}/2403.12550.md", result)

    def test_trailing_slash_treated_as_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            parent = Path(tmpdir) / "fresh"
            result = content.resolve_output_path(str(parent) + "/", "2403.12550")
        self.assertEqual(f"{parent}/2403.12550.md", result)

    def test_existing_file_untouched(self) -> None:
        handle = tempfile.NamedTemporaryFile(suffix=".md", delete=False)
        handle.close()
        try:
            result = content.resolve_output_path(handle.name, "2403.12550")
            self.assertEqual(handle.name, result)
        finally:
            os.unlink(handle.name)

    def test_interactive_default_targets_tmp_md(self) -> None:
        args = content_entry.parse_args(["2403.12550"])
        # Non-TTY under the test runner: output stays None (piped contract).
        self.assertIsNone(args.output)


class ResolveFormatTest(unittest.TestCase):
    def test_explicit_format_wins(self) -> None:
        args = make_args()
        args.format = "json"
        args.output = "paper.md"
        self.assertEqual("json", content.resolve_format(args))

    def test_md_output_implies_markdown(self) -> None:
        args = make_args()
        args.format = "auto"
        args.output = "paper.md"
        self.assertEqual("markdown", content.resolve_format(args))

    def test_json_output_implies_json(self) -> None:
        args = make_args()
        args.format = "auto"
        args.output = "paper.json"
        self.assertEqual("json", content.resolve_format(args))

    def test_stdout_tty_markdown_pipe_json(self) -> None:
        args = make_args()
        args.format = "auto"
        args.output = None
        with mock.patch.object(sys.stdout, "isatty", return_value=True):
            self.assertEqual("markdown", content.resolve_format(args))
        with mock.patch.object(sys.stdout, "isatty", return_value=False):
            self.assertEqual("json", content.resolve_format(args))


class ParseArgsShortcutTest(unittest.TestCase):
    def test_positional_paper_id(self) -> None:
        args = content_entry.parse_args(["2403.12550"])
        self.assertEqual("2403.12550", args.paper_id)

    def test_terms_optional_and_defaults(self) -> None:
        args = content_entry.parse_args(["2403.12550"])
        self.assertIsNone(args.terms)
        self.assertEqual("never", args.ocr_mode)
        self.assertEqual("auto", args.format)

    def test_flag_paper_id_still_works(self) -> None:
        args = content_entry.parse_args(["--paper-id", "2403.12550", "--terms", "SLAM"])
        self.assertEqual("2403.12550", args.paper_id)
        self.assertEqual("SLAM", args.terms)

    def test_missing_paper_id_errors(self) -> None:
        with self.assertRaises(SystemExit):
            content_entry.parse_args([])


class BuildMarkdownTest(unittest.TestCase):
    def test_latexml_render_with_figures_and_tables(self) -> None:
        output = {
            "paper_id": "2403.12550",
            "title": "Sample Paper",
            "html_url": "https://arxiv.org/html/2403.12550",
            "source_format": "html",
            "extraction_method": "html-latexml",
            "quality": {"grade": "high"},
            "evidence_eligible": True,
            "available": True,
            "generated_at": "2026-09-07T00:00:00+00:00",
            "text": "## 1 Introduction\n\nBody text about SLAM.",
            "figures": [{"caption": "Fig 1: robot.", "image_url": "https://arxiv.org/html/x/fig1.png"}],
            "tables": [{"caption": "Table 1: stats", "rows": [["Method", "ATE|RMSE"], ["Ours", "0.01"]]}],
            "formulas": [
                {"id": "S3.E1", "latex": "E = mc^2", "display": True, "number": "(1)"},
                {"id": "S3.EQ1.m1", "latex": r"\alpha_i \geq \alpha_{\min}", "display": False, "number": ""},
            ],
            "references": [
                {"id": "bib.bib1", "text": "Doe J. Teleop at scale. 2023.", "arxiv_id": "2301.00001"},
                {"id": "bib.bib2", "text": "Poe E. A clean dataset. 2024.", "arxiv_id": ""},
            ],
        }
        rendered = content.build_markdown(output)
        self.assertIn("# Sample Paper", rendered)
        self.assertIn("## 1 Introduction", rendered)
        self.assertIn("Body text about SLAM.", rendered)
        self.assertIn("![Fig 1: robot.](https://arxiv.org/html/x/fig1.png)", rendered)
        self.assertIn(r"| Method | ATE\|RMSE |", rendered)
        self.assertIn("| Ours | 0.01 |", rendered)
        self.assertIn("| --- | --- |", rendered)
        self.assertIn("## Formulas", rendered)
        self.assertIn("- (1) $$E = mc^2$$", rendered)
        self.assertNotIn(r"\alpha_i", rendered)  # inline/unnumbered formulas dropped
        self.assertIn("## References", rendered)
        self.assertIn("- Doe J. Teleop at scale. 2023.", rendered)
        self.assertIn("[arXiv:2301.00001](https://arxiv.org/abs/2301.00001)", rendered)
        self.assertIn("- Poe E. A clean dataset. 2024.", rendered)
        self.assertNotIn("arXiv:](https://", rendered)  # empty arxiv_id adds no link

    def test_pdf_render_uses_page_text(self) -> None:
        output = {
            "paper_id": "2403.12550",
            "title": "",
            "pdf_url": "https://arxiv.org/pdf/2403.12550.pdf",
            "source_format": "pdf",
            "extraction_method": "pdf-text",
            "quality": {"grade": "medium"},
            "evidence_eligible": True,
            "needs_visual_validation": True,
            "visual_validation_pages": [3, 7],
            "available": True,
            "generated_at": "2026-09-07T00:00:00+00:00",
            "text": "",
            "figures": [],
            "tables": [],
            "pages": [
                {"page": 1, "text": "First page words.", "extraction_method": "pdf-text"},
                {"page": 2, "text": "Second page words.", "extraction_method": "pdf-ocr"},
            ],
        }
        rendered = content.build_markdown(output)
        self.assertIn("## Page 1", rendered)
        self.assertIn("First page words.", rendered)
        self.assertIn("## Page 2", rendered)
        self.assertIn("Second page words.", rendered)
        self.assertIn("pages 3, 7", rendered)

    def test_unavailable_render_shows_reason(self) -> None:
        output = {
            "paper_id": "1234.56789",
            "title": "",
            "available": False,
            "source_format": "metadata-only",
            "evidence_eligible": False,
            "fallback_reason": "HTML unavailable or below the minimum full-text quality gate.",
            "attempts": [{"method": "html", "available": False, "quality": "low", "error": "boom"}],
        }
        rendered = content.build_markdown(output)
        self.assertIn("# arXiv 1234.56789", rendered)
        self.assertIn("**Full text unavailable.**", rendered)
        self.assertIn("boom", rendered)

    def test_unnumbered_formulas_dropped(self) -> None:
        output = {
            "paper_id": "x",
            "title": "T",
            "available": True,
            "evidence_eligible": True,
            "formulas": [
                {"id": "1", "latex": ">", "display": False, "number": ""},
                {"id": "2", "latex": r"\alpha", "display": False, "number": ""},
                {"id": "3", "latex": r"\mu_i \in \mathbb{R}^3", "display": True, "number": ""},
                {"id": "4", "latex": r"\int f\,dx", "display": True, "number": "(7)"},
            ],
        }
        rendered = content.build_markdown(output)
        self.assertIn("## Formulas", rendered)
        self.assertIn("- (7) $$" + r"\int f\,dx" + "$$", rendered)
        self.assertNotIn(r"\mu_i", rendered)
        self.assertNotIn("$>$", rendered)
        self.assertNotIn(r"\alpha", rendered)

    def test_missing_text_hints_rerun(self) -> None:
        output = {"paper_id": "1234.56789", "title": "T", "available": True, "evidence_eligible": True}
        rendered = content.build_markdown(output)
        self.assertIn("--include-full-text", rendered)


class PreferredSourceChainTest(unittest.TestCase):
    """--preferred-source controls the fallback tier order; default is legacy."""

    def make_chain_args(self, preferred: str) -> content.ContentOptions:
        # minimum_html_chars=1 makes the small fixture pass the medium gate so
        # no test in this class ever reaches the real network tier.
        return make_args(preferred_source=preferred, tex_cache_dir="/tmp/kb-test-src", minimum_html_chars=1)

    def test_default_chain_is_html_then_pdf_without_tex(self) -> None:
        pdf_result = {"available": False, "evidence_eligible": False, "quality": {"grade": "low"}, "extraction_method": "pdf-text"}
        with mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(False, "")), \
             mock.patch.object(content, "try_pdf", return_value=pdf_result):
            output = content.extract_content(self.make_chain_args("html"))
        methods = [attempt["method"] for attempt in output["attempts"]]
        self.assertEqual(["html-unavailable", "pdf-text"], methods)

    def test_html_eligible_short_circuits_tex_tier_on_default(self) -> None:
        with mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(True, HTML_FIXTURE)), \
             mock.patch.object(content, "try_tex") as try_tex:
            output = content.extract_content(self.make_chain_args("html"))
        self.assertTrue(output["evidence_eligible"])
        try_tex.assert_not_called()

    def test_tex_chain_tries_tex_first_and_falls_back(self) -> None:
        tex_result = {"available": False, "evidence_eligible": False, "quality": {"grade": "low"},
                      "extraction_method": "tex-pandoc"}
        pdf_result = {"available": False, "evidence_eligible": False, "quality": {"grade": "low"}, "extraction_method": "pdf-text"}
        with mock.patch.object(content, "try_tex", return_value=tex_result), \
             mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(False, "")), \
             mock.patch.object(content, "try_pdf", return_value=pdf_result):
            output = content.extract_content(self.make_chain_args("tex"))
        methods = [attempt["method"] for attempt in output["attempts"]]
        self.assertEqual(["tex-pandoc", "html-unavailable", "pdf-text"], methods)

    def test_auto_chain_is_html_tex_pdf(self) -> None:
        tex_result = {"available": True, "evidence_eligible": True, "quality": {"grade": "high"},
                      "extraction_method": "tex-pandoc", "text": "full text"}
        with mock.patch.object(content, "try_tex", return_value=tex_result), \
             mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(False, "")):
            output = content.extract_content(self.make_chain_args("auto"))
        self.assertTrue(output["evidence_eligible"])
        self.assertEqual("tex-pandoc", output["extraction_method"])
        methods = [attempt["method"] for attempt in output["attempts"]]
        self.assertEqual(["html-unavailable", "tex-pandoc"], methods)

    def test_tex_tier_missing_dependency_falls_through(self) -> None:
        with mock.patch.object(content, "try_tex", side_effect=SystemExit("pandoc missing")), \
             mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(True, HTML_FIXTURE)):
            output = content.extract_content(self.make_chain_args("tex"))
        # HTML succeeds after the TeX tier's SystemExit; chain survives.
        self.assertTrue(output["evidence_eligible"])
        tex_attempt = next(attempt for attempt in output["attempts"] if attempt["method"] == "tex")
        self.assertFalse(tex_attempt["available"])


class MainPlumbingTest(unittest.TestCase):
    def run_main(self, argv: list[str], *, markdown_source: dict, isatty: bool) -> tuple[int, str]:
        buf = io.StringIO()
        with mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(True, HTML_FIXTURE)), \
             mock.patch.object(content_entry, "extract_content", return_value=markdown_source), \
             mock.patch.object(sys.stdout, "isatty", return_value=isatty):
            with redirect_stdout(buf):
                code = content_entry.main(argv)
        return code, buf.getvalue()

    def test_markdown_stdout_and_exit_code(self) -> None:
        source = {
            "paper_id": "2403.12550",
            "title": "Sample Paper",
            "available": True,
            "evidence_eligible": True,
            "source_format": "html",
            "text": "hello",
        }
        code, out = self.run_main(["2403.12550", "--format", "markdown"], markdown_source=source, isatty=True)
        self.assertEqual(0, code)
        self.assertIn("# Sample Paper", out)

    def test_json_stdout_when_piped(self) -> None:
        source = {"paper_id": "2403.12550", "title": "T", "available": True, "evidence_eligible": True}
        code, out = self.run_main(["2403.12550"], markdown_source=source, isatty=False)
        self.assertEqual(0, code)
        self.assertEqual("T", json.loads(out)["title"])

    def test_noneligible_exit_code_is_two(self) -> None:
        source = {"paper_id": "x", "title": "", "available": False, "evidence_eligible": False}
        code, _ = self.run_main(["x", "--format", "markdown"], markdown_source=source, isatty=False)
        self.assertEqual(2, code)

    def test_markdown_forces_full_text_inclusion(self) -> None:
        captured: dict[str, content.ContentOptions] = {}

        def fake_extract(options: content.ContentOptions) -> dict:
            captured["args"] = options
            return {"paper_id": "x", "available": True, "evidence_eligible": True, "title": "T", "text": "hi"}

        with mock.patch.object(content.extract_arxiv_html, "fetch_html", return_value=(True, HTML_FIXTURE)), \
             mock.patch.object(content_entry, "extract_content", side_effect=fake_extract), \
             mock.patch.object(sys.stdout, "isatty", return_value=True), \
             redirect_stdout(io.StringIO()) as buf:
            content_entry.main(["2403.12550", "--format", "markdown"])
        self.assertTrue(captured["args"].render_markdown)


if __name__ == "__main__":
    unittest.main()

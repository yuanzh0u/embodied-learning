"""Tests for src/knowledge/legacy/arxiv_reader.py — id parsing, document cleaning,
anchor/image neutralization, and the unavailable-page fallback."""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "knowledge" / "legacy" / "arxiv_reader.py"
SPEC = importlib.util.spec_from_file_location("arxiv_reader_tested", SCRIPT)
reader = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["arxiv_reader_tested"] = reader
SPEC.loader.exec_module(reader)


class ParseArxivIdTest(unittest.TestCase):
    def test_accepts_bare_ids_and_versions(self):
        self.assertEqual(reader.parse_arxiv_id("2402.10329"), "2402.10329")
        self.assertEqual(reader.parse_arxiv_id("2402.10329v3"), "2402.10329")
        self.assertEqual(reader.parse_arxiv_id("cs/0301012"), "cs/0301012")

    def test_accepts_arxiv_urls(self):
        self.assertEqual(reader.parse_arxiv_id("https://arxiv.org/abs/2402.10329"), "2402.10329")
        self.assertEqual(reader.parse_arxiv_id("http://arxiv.org/html/2402.10329v2"), "2402.10329")
        self.assertEqual(reader.parse_arxiv_id("https://arxiv.org/pdf/2501.12948"), "2501.12948")
        self.assertEqual(reader.parse_arxiv_id("https://arxiv.org/abs/cs/0301012"), "cs/0301012")

    def test_rejects_non_paper_targets(self):
        # Deep asset paths, foreign hosts, junk, non-strings.
        self.assertIsNone(reader.parse_arxiv_id("https://arxiv.org/html/2402.10329v3/figures/setup.jpg"))
        self.assertIsNone(reader.parse_arxiv_id("https://example.com/abs/2402.10329"))
        self.assertIsNone(reader.parse_arxiv_id("not-an-id"))
        self.assertIsNone(reader.parse_arxiv_id(""))
        self.assertIsNone(reader.parse_arxiv_id(None))


class BuildDocumentTest(unittest.TestCase):
    def setUp(self):
        self.base = "https://arxiv.org/html/2402.10329"
        self.raw = (
            "<html><head><title>Original</title></head><body>"
            '<nav class="ltx_page_header"><a href="/abs/2402.10329v3">arXiv</a></nav>'
            '<div class="ltx_page_content"><article class="ltx_document">'
            '<h1 class="ltx_title">Sample Paper: '
            '<math alttext="\\\\alpha + \\\\beta"><mi>a</mi></math></h1>'
            '<p>Cite <a href="#bib.bib1">[1]</a> and jump <a href="#S2">§2</a>.</p>'
            '<p>See <a href="https://github.com/example/repo">code</a> '
            'and <a href="../2402.10329v1/paper.pdf">pdf</a>.</p>'
            '<figure><img src="2402.10329v3/fig1.png"><figcaption>Fig 1</figcaption></figure>'
            '<script>alert(1)</script><svg><circle/></svg>'
            "</article></div>"
            '<footer class="ltx_page_footer">Colophon</footer>'
            "</body></html>"
        )

    def test_builds_standalone_document_with_title(self):
        doc = reader.build_document("2402.10329", self.raw, base_url=self.base)
        self.assertIsNotNone(doc)
        self.assertIn('data-reader-doc="ok"', doc)
        self.assertIn("<title>Sample Paper:", doc)
        self.assertIn('data-paper-id="2402.10329"', doc)

    def test_drops_non_content_markup(self):
        doc = reader.build_document("2402.10329", self.raw, base_url=self.base)
        self.assertNotIn("<script", doc)
        self.assertNotIn("<svg", doc)
        self.assertNotIn("ltx_page_header", doc)
        self.assertNotIn("ltx_page_footer", doc)

    def test_math_becomes_latex_source(self):
        doc = reader.build_document("2402.10329", self.raw, base_url=self.base)
        self.assertIn('class="math-inline"', doc)
        self.assertIn("\\alpha", doc)
        self.assertNotIn("<math", doc)

    def test_fragment_anchors_survive(self):
        doc = reader.build_document("2402.10329", self.raw, base_url=self.base)
        self.assertIn('href="#bib.bib1"', doc)
        self.assertIn('href="#S2"', doc)

    def test_arxiv_and_external_links_neutralized(self):
        doc = reader.build_document("2402.10329", self.raw, base_url=self.base)
        # The ../2402.10329v1/paper.pdf link resolves against base → /html/2402.10329v1/paper.pdf,
        # which is an asset path, not a paper — inert. A real abs link becomes a reader ref.
        self.assertIn("https://github.com/example/repo", doc)
        self.assertNotIn('href="https://github.com', doc)
        doc2 = reader.build_document(
            "2402.10329",
            '<article><p><a href="https://arxiv.org/abs/2004.06720">prior work</a></p></article>',
            base_url=self.base,
        )
        self.assertIn('data-arxiv="2004.06720"', doc2)

    def test_images_absolutized(self):
        doc = reader.build_document("2402.10329", self.raw, base_url=self.base)
        # Relative src resolves against the final fetch URL (which carries v3).
        self.assertIn('src="https://arxiv.org/html/2402.10329v3/fig1.png"', doc)

    def test_empty_article_returns_none(self):
        self.assertIsNone(reader.build_document("2402.10329", "<html><body></body></html>", base_url=self.base))


class FetchPaperTest(unittest.TestCase):
    def setUp(self):
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.cache = Path(self._tmp.name)
        self.base = "https://arxiv.org/html/2402.10329"

    def tearDown(self):
        self._tmp.cleanup()

    def test_rejects_invalid_id_without_network(self):
        result = reader.fetch_paper("../../etc/passwd", self.cache)
        self.assertFalse(result["ok"])
        self.assertIn("无效", result["error"])

    def test_unavailable_page_renders(self):
        page = reader.unavailable_page("hep-th/9801001", "no html")
        self.assertIn('data-reader-doc="unavailable"', page)
        self.assertIn("hep-th/9801001", page)
        self.assertIn("https://arxiv.org/abs/hep-th/9801001", page)

    def test_served_document_is_self_contained(self):
        doc = reader.build_document(
            "2402.10329", "<article><h1>T</h1><p>body</p></article>", base_url=self.base
        )
        self.assertTrue(doc.startswith("<!doctype html>"))
        self.assertIn(reader.READER_CSS, doc)


if __name__ == "__main__":
    unittest.main()

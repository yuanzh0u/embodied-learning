#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract_arxiv_html.py"
SPEC = importlib.util.spec_from_file_location("extract_arxiv_html", SCRIPT)
extract_arxiv_html = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(extract_arxiv_html)


LATEXML_FIXTURE = """
<html><body>
<div class="ltx_abstract">
<h6 class="ltx_title ltx_title_abstract">Abstract</h6>
<div id="p1" class="ltx_para"><p class="ltx_p">We study robot data quality in the wild.</p></div>
</div>
<section class="ltx_section" id="S1">
<h2 class="ltx_title ltx_title_section">1 Introduction</h2>
<div id="S1.p1" class="ltx_para"><p class="ltx_p">Robot learning needs demonstrations.
Prior systems <cite class="ltx_cite ltx_citemacro_cite">[<a class="ltx_ref" href="#bib.bib1">1</a>]</cite> collect teleoperation data.</p></div>
</section>
<section class="ltx_section" id="S4">
<h2 class="ltx_title ltx_title_section">4 Experiments</h2>
<section class="ltx_subsection" id="S4.SS2">
<h3 class="ltx_title ltx_title_subsection">4.2 Data Quality</h3>
<div id="S4.SS2.p1" class="ltx_para"><p class="ltx_p">The demonstrations exhibit inconsistent gripper closure.
Data quality varies across operators. Data quality drops under occlusion.</p></div>
<div id="S4.SS2.p2" class="ltx_para"><p class="ltx_p">The dataset from <cite class="ltx_cite ltx_citemacro_cite">[<a class="ltx_ref" href="#bib.bib2">2</a>]</cite> shows lower noise than ours.</p></div>
</section>
</section>
<section class="ltx_bibliography" id="bib">
<h2 class="ltx_title ltx_title_bibliography">References</h2>
<ul class="ltx_biblist">
<li class="ltx_bibitem" id="bib.bib1">
<span class="ltx_tag ltx_role_refnum ltx_tag_bibitem">Doe et al. [2023]</span>
<span class="ltx_bibblock">Jane Doe and John Roe.</span>
<span class="ltx_bibblock">Teleop at scale. arXiv:2301.00001, 2023.</span>
</li>
<li class="ltx_bibitem" id="bib.bib2">
<span class="ltx_tag ltx_role_refnum ltx_tag_bibitem">Poe et al. [2024]</span>
<span class="ltx_bibblock">Edgar Poe.</span>
<span class="ltx_bibblock">A clean dataset. In RSS, 2024.</span>
</li>
</ul>
</section>
</body></html>
"""

FLAT_FIXTURE = """
<html><body>
<h2>Old Style Page</h2>
<p>Data quality matters. See arXiv:1901.01234 for details.</p>
<h2>References</h2>
<p>[1] Someone. arXiv:1901.01234.</p>
</body></html>
"""


def parse_fixture(html: str):
    parser = extract_arxiv_html.extract_structured(html)
    assert parser is not None
    return parser


class SectionTreeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = parse_fixture(LATEXML_FIXTURE)
        self.sections = self.parser.sections

    def test_section_tree_with_titles_and_nesting(self) -> None:
        titles = [s["title"] for s in self.sections]
        self.assertEqual(titles, ["Abstract", "1 Introduction", "4 Experiments", "4.2 Data Quality", "References"])
        by_title = {s["title"]: s for s in self.sections}
        self.assertEqual(by_title["4.2 Data Quality"]["level"], 2)
        self.assertEqual(by_title["4 Experiments"]["level"], 1)

    def test_section_path_includes_parent(self) -> None:
        subsection = next(s for s in self.sections if s["title"] == "4.2 Data Quality")
        path = extract_arxiv_html.section_path(self.sections, int(subsection["index"]))
        self.assertEqual(path, "4 Experiments > 4.2 Data Quality")

    def test_para_counts(self) -> None:
        by_title = {s["title"]: s for s in self.sections}
        self.assertEqual(by_title["4.2 Data Quality"]["para_count"], 2)
        self.assertEqual(by_title["1 Introduction"]["para_count"], 1)


class TermMatchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = parse_fixture(LATEXML_FIXTURE)

    def test_match_locator_has_section_path_and_para(self) -> None:
        matches = extract_arxiv_html.find_term_matches(self.parser.sections, ["gripper closure"])
        self.assertEqual(len(matches), 1)
        self.assertIn("4 Experiments > 4.2 Data Quality", matches[0]["locator"])
        self.assertIn("S4.SS2.p1", matches[0]["locator"])

    def test_ranked_sections_prefer_dense_section(self) -> None:
        ranked = extract_arxiv_html.rank_sections(self.parser.sections, ["data quality", "occlusion"], top=3)
        self.assertTrue(ranked)
        self.assertEqual(
            extract_arxiv_html.section_path(self.parser.sections, int(ranked[0]["section_index"])),
            "4 Experiments > 4.2 Data Quality",
        )
        self.assertIn("occlusion", ranked[0]["matched_terms"])

    def test_bibliography_excluded_from_ranking(self) -> None:
        ranked = extract_arxiv_html.rank_sections(self.parser.sections, ["dataset"], top=5)
        paths = [entry["path"] for entry in ranked]
        self.assertTrue(all("References" not in path for path in paths))


class CitationContextTest(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = parse_fixture(LATEXML_FIXTURE)
        self.contexts = extract_arxiv_html.citation_contexts(self.parser)

    def test_citation_resolved_to_arxiv_id(self) -> None:
        first = self.contexts[0]
        self.assertEqual(first["bib_keys"], ["bib.bib1"])
        self.assertEqual(first["arxiv_ids"], ["2301.00001"])
        self.assertIn("teleoperation", first["sentence"].lower())

    def test_citation_without_arxiv_id_keeps_bib_key(self) -> None:
        second = self.contexts[1]
        self.assertEqual(second["bib_keys"], ["bib.bib2"])
        self.assertEqual(second["arxiv_ids"], [])
        self.assertIn("4 Experiments > 4.2 Data Quality", second["section"])

    def test_reference_hints_from_bibliography(self) -> None:
        hints = extract_arxiv_html.reference_hints_from_bib(self.parser.bibitems)
        self.assertEqual([hint["arxiv_id"] for hint in hints], ["2301.00001"])


class FlatFallbackTest(unittest.TestCase):
    def test_non_latexml_returns_none(self) -> None:
        self.assertIsNone(extract_arxiv_html.extract_structured(FLAT_FIXTURE))

    def test_flat_parser_extracts_text_and_hints(self) -> None:
        flat = extract_arxiv_html.FlatHTMLParser()
        flat.feed(FLAT_FIXTURE)
        text = flat.text()
        matches = extract_arxiv_html.flat_term_matches(text, ["data quality"])
        self.assertEqual(len(matches), 1)
        hints = extract_arxiv_html.flat_reference_hints(text)
        self.assertEqual(hints[0]["arxiv_id"], "1901.01234")


if __name__ == "__main__":
    unittest.main()

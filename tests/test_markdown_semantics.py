from __future__ import annotations

import unittest

from scripts import build_research_wiki as wiki
from scripts import visualize_kb_index as viz
from scripts.lib.markdown_semantics import render_markdown


class MarkdownSemanticsTest(unittest.TestCase):
    def test_shared_renderer_escapes_html_and_builds_stable_toc(self) -> None:
        result = render_markdown(
            "# 标题\n\n<script>x</script>\n\n## 重复\n\n## 重复\n",
            heading_ids=True,
            collect_toc=True,
        )

        self.assertNotIn("<script>", result.html)
        self.assertIn("&lt;script&gt;", result.html)
        self.assertEqual([item["id"] for item in result.toc], ["标题", "重复", "重复-2"])

    def test_both_consumers_share_core_block_semantics(self) -> None:
        markdown = (
            "# Title\n\n"
            "> line one\n> line two\n\n"
            "+ item\n\n"
            "| a | b |\n|---|---|\n| 1 | 2 |\n\n"
            "```python\nprint(1)\n```\n"
        )
        wiki_html, _toc = wiki.markdown_to_html(markdown)
        viz_html = viz.markdown_to_html(markdown)

        for fragment in ["<blockquote>line one line two</blockquote>", "<li>item</li>", "<table>"]:
            self.assertIn(fragment, wiki_html)
            self.assertIn(fragment, viz_html)
        self.assertIn('class="language-python"', wiki_html)
        self.assertIn('class="language-python"', viz_html)

    def test_unsafe_link_protocol_is_never_emitted(self) -> None:
        wiki_html, _toc = wiki.markdown_to_html("[bad](javascript:alert(1))\n")
        viz_html = viz.markdown_to_html("[bad](javascript:alert(1))\n")

        self.assertNotIn('href="javascript:', wiki_html)
        self.assertNotIn('href="javascript:', viz_html)

    def test_superscript_citations_render_as_sup(self) -> None:
        # Scientific-memo citation markers: one bracketed marker per number.
        wiki_html, _toc = wiki.markdown_to_html("受排序影响^[1]^，随时间漂移^[2]^。\n")
        self.assertIn("受排序影响<sup>[1]</sup>", wiki_html)
        self.assertIn("随时间漂移<sup>[2]</sup>", wiki_html)
        self.assertNotIn("^[1]^", wiki_html)

    def test_blank_lines_inside_reference_list_keep_one_ol(self) -> None:
        """2026-09-11 固化 workflow 回归：成稿作者用空行分隔参考文献条目，
        渲染器把每条拆成独立 <ol>，页面显示编号全是 1。空行+同类列表项
        必须延续同一个列表。"""
        markdown = (
            "## 参考文献\n\n"
            "1. First paper 2026. [arXiv:2609.06165](https://arxiv.org/abs/2609.06165)\n\n"
            "2. Second paper 2026. [arXiv:2609.10789](https://arxiv.org/abs/2609.10789)\n\n"
            "3. Third paper 2026. [arXiv:2609.11472](https://arxiv.org/abs/2609.11472)\n"
        )
        html_out, _toc = wiki.markdown_to_html(markdown)
        self.assertEqual(html_out.count("<ol>"), 1, html_out)
        self.assertEqual(html_out.count("<li>"), 3)
        # and an interrupting paragraph still closes the list
        markdown_break = "1. one\n\nmiddle text\n\n2. two\n"
        html_break, _ = wiki.markdown_to_html(markdown_break)
        self.assertEqual(html_break.count("<ol>"), 2, html_break)
        self.assertIn("<p>middle text</p>", html_break)


if __name__ == "__main__":
    unittest.main()

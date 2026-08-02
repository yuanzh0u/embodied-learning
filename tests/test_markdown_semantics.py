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


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import build_research_wiki as wiki


def write_triplet(directory: Path, topic: str = "测试话题") -> None:
    directory.mkdir(parents=True)
    (directory / "run.json").write_text(json.dumps({"topic": topic}, ensure_ascii=False), encoding="utf-8")
    for _key, (label, filename) in wiki.VERSION_FILES.items():
        (directory / filename).write_text(
            f"# {label}标题\n\n## 结论\n\n这是{label}的完整正文，包含一个[外部证据](https://example.com/paper)。\n",
            encoding="utf-8",
        )
    (directory / "evidence-appendix.md").write_text("# 证据附录\n\n- 证据一\n", encoding="utf-8")


class BuildResearchWikiTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.source = self.root / "work"
        self.output = self.root / "wiki" / "data"
        self.source.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_discovery_requires_all_three_versions(self) -> None:
        write_triplet(self.source / "literature-review-complete-topic-20260102")
        incomplete = self.source / "literature-review-incomplete-topic-20260103"
        incomplete.mkdir()
        (incomplete / "scientific-memo_keyan.md").write_text("# only one\n", encoding="utf-8")

        selected, stats = wiki.discover_topics(self.source)

        self.assertEqual(len(selected), 1)
        self.assertEqual(stats["skipped_incomplete"], 1)

    def test_discovery_keeps_only_newest_normalized_topic(self) -> None:
        write_triplet(self.source / "literature-review-same-topic-20260101", "同一话题")
        write_triplet(self.source / "literature-review-same-topic-20260203", "同一话题")

        selected, stats = wiki.discover_topics(self.source)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].date, "2026-02-03")
        self.assertEqual(stats["superseded_versions"], 1)

    def test_historical_english_alias_is_deduplicated(self) -> None:
        old = self.source / "literature-review-tactile-world-model-20260101"
        write_triplet(old, "旧标题")
        (old / "run.json").unlink()
        write_triplet(self.source / "literature-review-触觉世界模型-20260201", "触觉世界模型")

        selected, stats = wiki.discover_topics(self.source)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].date, "2026-02-01")
        self.assertEqual(stats["superseded_versions"], 1)

    def test_snapshot_defaults_to_zhihu_and_validates_triplets(self) -> None:
        write_triplet(self.source / "literature-review-test-topic-20260304")

        manifest = wiki.build_snapshot(self.source, self.output)
        validated = wiki.validate_snapshot(self.output)
        topic_id = manifest["topics"][0]["id"]
        topic = json.loads((self.output / "topics" / f"{topic_id}.json").read_text(encoding="utf-8"))

        self.assertEqual(validated["site"]["default_version"], "zhihu")
        self.assertEqual(set(topic["versions"]), {"keyan", "zhihu", "xiaohongshu"})
        self.assertTrue(topic["evidence"]["available"])

    def test_markdown_renderer_escapes_html_and_keeps_external_links(self) -> None:
        rendered, toc = wiki.markdown_to_html(
            "# 标题\n\n<script>alert(1)</script>\n\n## 小节\n\n[论文](https://example.com/paper)\n"
        )

        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn('href="https://example.com/paper"', rendered)
        self.assertEqual([item["label"] for item in toc], ["标题", "小节"])

    def test_markdown_renderer_marks_arxiv_links_only(self) -> None:
        rendered, _toc = wiki.markdown_to_html(
            "[论文](https://arxiv.org/abs/2607.07287) 与 [项目](https://example.com/project)\n"
        )

        self.assertEqual(rendered.count('class="arxiv-icon"'), 1)
        self.assertIn(
            '<span class="arxiv-icon" aria-hidden="true">arXiv</span>'
            '<a href="https://arxiv.org/abs/2607.07287"',
            rendered,
        )
        self.assertIn('<a href="https://example.com/project"', rendered)

    def test_wiki_home_links_to_github_repository(self) -> None:
        index = (Path(__file__).resolve().parents[1] / "wiki" / "index.html").read_text(encoding="utf-8")

        self.assertIn('href="https://github.com/yuanzh0u/embodied-learning"', index)
        self.assertIn("GitHub 代码仓", index)
        self.assertIn('target="_blank" rel="noopener noreferrer"', index)

    def test_wiki_uses_topbar_actions_and_tree_drawer(self) -> None:
        wiki_root = Path(__file__).resolve().parents[1] / "wiki"
        index = (wiki_root / "index.html").read_text(encoding="utf-8")
        script = (wiki_root / "assets" / "wiki.js").read_text(encoding="utf-8")
        styles = (wiki_root / "assets" / "wiki.css").read_text(encoding="utf-8")
        topbar = index.split('<header class="topbar">', 1)[1].split("</header>", 1)[0]
        sidebar = index.split('<aside class="sidebar"', 1)[1].split("</aside>", 1)[0]

        self.assertIn('href="https://github.com/yuanzh0u/embodied-learning"', topbar)
        self.assertIn('href="knowledge-map/"', topbar)
        self.assertIn('id="refresh-button"', topbar)
        self.assertNotIn("github.com", sidebar)
        self.assertNotIn("knowledge-map/", sidebar)
        self.assertIn('id="all-research"', sidebar)
        self.assertIn('id="recent-research"', sidebar)
        self.assertIn('aria-hidden="true" inert', index)
        self.assertIn("function renderFieldTree()", script)
        self.assertIn('class="tree-folder ${expanded ? "is-expanded" : ""}"', script)
        self.assertIn("transform: translateX(-105%);", styles)


if __name__ == "__main__":
    unittest.main()

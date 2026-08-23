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
        self.assertEqual(validated["site"]["title"], "空间智能研究 Wiki")
        self.assertEqual(set(topic["versions"]), {"keyan", "zhihu", "xiaohongshu"})
        self.assertTrue(topic["evidence"]["available"])

    def test_catalog_source_publishes_only_routed_settled_runs(self) -> None:
        evidence = self.root / "evidence"
        routed = evidence / "literature-review-routed-20260304"
        unrouted = evidence / "literature-review-unrouted-20260305"
        write_triplet(routed, "目录话题")
        write_triplet(unrouted, "未路由话题")
        for directory in [routed, unrouted]:
            (directory / "evidence.jsonl").write_text(
                json.dumps({"event_id": "EA-TEST-0001"}) + "\n", encoding="utf-8"
            )
            manifest = json.loads((directory / "run.json").read_text(encoding="utf-8"))
            manifest.update(
                {
                    "status": "settled",
                    "files": {
                        "evidence": "evidence.jsonl",
                        "outputs": [filename for _label, filename in wiki.VERSION_FILES.values()],
                    },
                }
            )
            (directory / "run.json").write_text(
                json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
            )
        knowledge = self.root / "knowledge"
        knowledge.mkdir()
        catalog = knowledge / "literature-review-catalog.md"
        catalog.write_text(
            "[run](../evidence/literature-review-routed-20260304/run.json)\n",
            encoding="utf-8",
        )

        selected, stats = wiki.discover_topics(catalog)

        self.assertEqual([item.directory.name for item in selected], [routed.name])
        self.assertEqual(stats["source_mode"], "catalog")

    def test_atomic_publish_switches_only_after_validation(self) -> None:
        write_triplet(self.source / "literature-review-test-topic-20260304")

        manifest = wiki.publish_snapshot(self.source, self.output)
        pointer = json.loads((self.output / "current.json").read_text(encoding="utf-8"))
        active = self.output / pointer["base_path"]

        self.assertFalse((self.output / "manifest.json").exists())
        self.assertTrue((active / "manifest.json").is_file())
        self.assertEqual(pointer["topic_count"], len(manifest["topics"]))
        self.assertEqual(wiki.validate_published_snapshot(self.output)["topics"], manifest["topics"])

    def test_failed_publish_preserves_previous_pointer(self) -> None:
        directory = self.source / "literature-review-test-topic-20260304"
        write_triplet(directory)
        wiki.publish_snapshot(self.source, self.output)
        previous = (self.output / "current.json").read_text(encoding="utf-8")
        (directory / "zhihu-explainer_zhihu.md").write_text(
            "# 更新稿\n\n这是足够长的更新内容，用于生成第二个候选快照。\n",
            encoding="utf-8",
        )

        def fail_before_activate(_snapshot: Path) -> None:
            raise RuntimeError("injected failure")

        with self.assertRaisesRegex(RuntimeError, "injected failure"):
            wiki.publish_snapshot(
                self.source,
                self.output,
                before_activate=fail_before_activate,
            )

        self.assertEqual((self.output / "current.json").read_text(encoding="utf-8"), previous)
        self.assertEqual(len(wiki.validate_published_snapshot(self.output)["topics"]), 1)

    def test_previous_snapshot_can_be_atomically_reactivated(self) -> None:
        directory = self.source / "literature-review-test-topic-20260304"
        write_triplet(directory)
        wiki.publish_snapshot(self.source, self.output)
        first = json.loads((self.output / "current.json").read_text(encoding="utf-8"))[
            "snapshot_id"
        ]
        (directory / "zhihu-explainer_zhihu.md").write_text(
            "# 第二版\n\n这是第二版的完整内容，用于验证快照回滚。\n",
            encoding="utf-8",
        )
        wiki.publish_snapshot(self.source, self.output)
        second = json.loads((self.output / "current.json").read_text(encoding="utf-8"))[
            "snapshot_id"
        ]
        self.assertNotEqual(first, second)

        with wiki.publication_lock(self.output):
            wiki.activate_snapshot(self.output, first)

        current = json.loads((self.output / "current.json").read_text(encoding="utf-8"))
        self.assertEqual(current["snapshot_id"], first)
        self.assertEqual(len(wiki.validate_published_snapshot(self.output)["topics"]), 1)

    def test_publication_lock_rejects_concurrent_writer(self) -> None:
        with wiki.publication_lock(self.output):
            with self.assertRaisesRegex(RuntimeError, "正在进行"):
                with wiki.publication_lock(self.output):
                    pass

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
        self.assertIn("<title>Embodied AI Evidence Hub｜具身智能证据知识库</title>", index)
        self.assertIn("<strong>Embodied AI Evidence Hub</strong>", index)

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
        self.assertIn('id="topic-count"', topbar)
        self.assertIn('id="snapshot-time"', topbar)
        self.assertIn('src="assets/github-mark.svg"', topbar)
        self.assertNotIn("github.com", sidebar)
        self.assertNotIn("knowledge-map/", sidebar)
        self.assertNotIn('id="all-research"', sidebar)
        self.assertIn('id="recent-research"', sidebar)
        self.assertIn('aria-hidden="false"', index)
        self.assertIn("function renderFieldTree()", script)
        self.assertIn('class="tree-folder ${expanded ? "is-expanded" : ""}"', script)
        self.assertIn('class="tree-count"', script)
        self.assertIn('class="tree-topic-meta"', script)
        self.assertIn('return `更新于 ${value}`', script)
        self.assertIn("function syncSidebarForViewport()", script)
        self.assertIn("transform: translateX(-105%);", styles)
        self.assertIn('.tree-folder-row[aria-expanded="true"] .folder-icon::after', styles)
        self.assertIn("--paper: #f5f4f0", styles)
        self.assertNotIn("--coral:", styles)
        self.assertIn('--topbar-height: 68px', styles)
        self.assertIn('@media (max-width: 900px)', styles)
        self.assertIn('font-size: clamp(32px, 2.6vw, 38px)', styles)
        self.assertIn('.markdown-body h2 { margin: 40px 0 14px; padding-top: 4px; font-size: 22px; }', styles)
        self.assertIn('nodes.articleTitle.textContent = version.article_title', script)
        self.assertIn('if (repeatedTitle?.tagName === "H1") repeatedTitle.remove()', script)
        self.assertIn('nodes.versionArticleTitle.textContent = `所属话题：${topic.title}`', script)
        self.assertIn('Embodied AI Evidence Hub', script)
        self.assertIn('data/current.json', script)
        self.assertIn('state.dataBase', script)


if __name__ == "__main__":
    unittest.main()

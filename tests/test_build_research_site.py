#!/usr/bin/env python3

from __future__ import annotations

import json
import html
import re
import struct
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

from scripts import build_research_site as site
from scripts import build_research_wiki as wiki


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://yuanzh0u.github.io/embodied-learning"


class BuildResearchSiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = TemporaryDirectory()
        cls.temp_root = Path(cls._tmp.name)
        cls.snapshot_root = cls.temp_root / "wiki-data"
        cls.site_root = cls.temp_root / "site"
        wiki.publish_snapshot(
            wiki.DEFAULT_SOURCE,
            cls.snapshot_root,
            site_config=wiki.DEFAULT_SITE_CONFIG,
        )
        site.build_site(
            cls.snapshot_root,
            ROOT / "wiki",
            cls.site_root,
            base_url=BASE_URL,
            preview=False,
        )
        cls.snapshot_dir = wiki.resolve_snapshot_directory(cls.snapshot_root)
        cls.manifest = json.loads(
            (cls.snapshot_dir / "manifest.json").read_text(encoding="utf-8")
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_publication_config_covers_exactly_38_current_topics(self) -> None:
        selected, _stats = wiki.discover_topics(wiki.DEFAULT_SOURCE)
        config = wiki.load_site_config(
            wiki.DEFAULT_SITE_CONFIG,
            {candidate.topic_key for candidate in selected},
        )
        topics = config["topics"]
        slugs = [value["slug"] for value in topics.values()]

        self.assertEqual(len(topics), 38)
        self.assertEqual(len(slugs), len(set(slugs)))
        self.assertTrue(all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) for slug in slugs))

    def test_schema_v2_has_complete_publication_and_evidence_metadata(self) -> None:
        self.assertEqual(self.manifest["schema_version"], 2)
        self.assertEqual(
            self.manifest["site"]["title"],
            "Embodied AI Evidence Hub｜具身智能证据知识库",
        )
        self.assertEqual(len(self.manifest["topics"]), 38)
        for item in self.manifest["topics"]:
            self.assertEqual(item["canonical_path"], f"/research/{item['slug']}/")
            self.assertTrue(item["title_en"])
            self.assertIsInstance(item["knowledge_ids"], list)
            self.assertGreaterEqual(item["paper_count"], 0)
            self.assertGreater(item["evidence_event_count"], 0)
            topic = json.loads(
                (self.snapshot_dir / "topics" / f"{item['id']}.json").read_text(encoding="utf-8")
            )
            citation_urls = [citation["url"] for citation in topic["citations"]]
            self.assertEqual(len(citation_urls), len(set(citation_urls)))

    def test_build_contains_exactly_38_crawlable_topic_pages(self) -> None:
        pages = sorted((self.site_root / "research").glob("*/index.html"))
        self.assertEqual(len(pages), 38)
        for page in pages:
            source = page.read_text(encoding="utf-8")
            self.assertIn("<h1>", source)
            self.assertIn("知乎解释版 · 完整正文", source)
            self.assertIn('id="evidence"', source)
            self.assertIn("去重论文引用", source)
            self.assertRegex(source, r'<a href="https?://[^\"]+"')
            self.assertIn('type="application/ld+json"', source)
            self.assertIn("?version=zhihu&amp;ai=1", source)

    def test_page_metadata_and_json_ld_are_unique_and_parseable(self) -> None:
        pages = sorted((self.site_root / "research").glob("*/index.html"))
        titles: set[str] = set()
        descriptions: set[str] = set()
        canonicals: set[str] = set()
        for page in pages:
            source = page.read_text(encoding="utf-8")
            title = re.search(r"<title>(.*?)</title>", source).group(1)
            description = html.unescape(
                re.search(r'<meta name="description" content="([^"]+)">', source).group(1)
            )
            canonical = re.search(r'<link rel="canonical" href="([^"]+)">', source).group(1)
            payload = re.search(
                r'<script type="application/ld\+json">(.*?)</script>', source, re.DOTALL
            ).group(1)
            structured = json.loads(payload)

            self.assertTrue(120 <= len(description) <= 160)
            self.assertEqual(structured["@type"], "Article")
            self.assertEqual(len(structured["citation"]), len(set(structured["citation"])))
            titles.add(title)
            descriptions.add(description)
            canonicals.add(canonical)
        self.assertEqual(len(titles), 38)
        self.assertEqual(len(descriptions), 38)
        self.assertEqual(len(canonicals), 38)

    def test_sitemap_has_only_home_directory_and_38_topics(self) -> None:
        tree = ElementTree.parse(self.site_root / "sitemap.xml")
        locations = [
            node.text
            for node in tree.findall(
                "{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        ]
        self.assertEqual(len(locations), 40)
        self.assertEqual(len(locations), len(set(locations)))
        self.assertNotIn(f"{BASE_URL}/knowledge-map/", locations)
        self.assertTrue(all("#" not in value and "/data/" not in value for value in locations))

    def test_robots_llms_and_raw_home_directory_are_crawlable(self) -> None:
        robots = (self.site_root / "robots.txt").read_text(encoding="utf-8")
        llms = (self.site_root / "llms.txt").read_text(encoding="utf-8")
        homepage = (self.site_root / "index.html").read_text(encoding="utf-8")

        self.assertIn("User-agent: OAI-SearchBot\nAllow: /", robots)
        self.assertIn(f"Sitemap: {BASE_URL}/sitemap.xml", robots)
        self.assertEqual(llms.count(f"{BASE_URL}/research/"), 39)
        self.assertEqual(homepage.count('class="research-card"'), 38)
        self.assertIn(f'<link rel="canonical" href="{BASE_URL}/">', homepage)
        payload = re.search(
            r'<script type="application/ld\+json">(.*?)</script>', homepage, re.DOTALL
        ).group(1)
        types = {item["@type"] for item in json.loads(payload)["@graph"]}
        self.assertEqual(types, {"WebSite", "Organization"})

    def test_social_preview_has_required_dimensions_and_file_size(self) -> None:
        image = ROOT / "wiki" / "assets" / "social-preview.png"
        payload = image.read_bytes()
        width, height = struct.unpack(">II", payload[16:24])

        self.assertEqual((width, height), (1280, 640))
        self.assertLess(len(payload), 1_000_000)

    def test_preview_disallows_crawling_and_marks_pages_noindex(self) -> None:
        preview_root = self.temp_root / "preview"
        site.build_site(
            self.snapshot_root,
            ROOT / "wiki",
            preview_root,
            base_url=BASE_URL,
            preview=True,
        )
        robots = (preview_root / "robots.txt").read_text(encoding="utf-8")
        topic_page = next((preview_root / "research").glob("*/index.html")).read_text(encoding="utf-8")
        homepage = (preview_root / "index.html").read_text(encoding="utf-8")

        self.assertEqual(robots, "User-agent: *\nDisallow: /\n")
        self.assertIn('name="robots" content="noindex,nofollow"', topic_page)
        self.assertIn('name="robots" content="noindex,nofollow"', homepage)
        self.assertIn(f'<link rel="canonical" href="{BASE_URL}/', topic_page)

    def test_static_markdown_escapes_html_and_rejects_broken_relative_links(self) -> None:
        with TemporaryDirectory() as temporary:
            repo = Path(temporary)
            source = repo / "evidence" / "run"
            source.mkdir(parents=True)
            renderer = site.StaticMarkdownRenderer(repo, source, "https://github.com/example/repo")
            rendered = renderer.render("<script>alert(1)</script>\n\n[论文](https://example.com/paper)\n")

            self.assertNotIn("<script>", rendered)
            self.assertIn("&lt;script&gt;", rendered)
            self.assertIn('href="https://example.com/paper"', rendered)
            with self.assertRaisesRegex(RuntimeError, "失效的仓库相对链接"):
                renderer.render("[坏链接](missing.md)\n")

    def test_spa_topic_navigation_has_real_static_hrefs(self) -> None:
        script = (ROOT / "wiki" / "assets" / "wiki.js").read_text(encoding="utf-8")
        template = (ROOT / "wiki" / "index.html").read_text(encoding="utf-8")
        self.assertIn("function canonicalHref(topic)", script)
        self.assertIn('href="${escapeHtml(canonicalHref(topic))}"', script)
        self.assertIn("openTopicFromLink(event", script)
        self.assertIn('id="ai-research-button"', template)
        self.assertIn('id="ai-dialog"', template)
        self.assertIn("function buildAiPrompt(task", script)
        self.assertIn("topic.evidence_event_count", script)
        self.assertIn('data-ai-provider="Gemini"', template)


if __name__ == "__main__":
    unittest.main()

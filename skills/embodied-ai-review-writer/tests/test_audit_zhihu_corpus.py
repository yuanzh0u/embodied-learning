#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-review-writer" / "scripts" / "audit_zhihu_corpus.py"


class AuditZhihuCorpusTests(unittest.TestCase):
    def write_good_bundle(self, root: Path) -> None:
        fixture_path = Path(__file__).with_name("test_audit_article_quality.py")
        spec = importlib.util.spec_from_file_location("article_quality_fixture", fixture_path)
        if not spec or not spec.loader:
            raise RuntimeError(f"cannot load fixture module: {fixture_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.AuditArticleQualityTests().write_good_bundle(root)

    def write_topic(self, topics_dir: Path, index: int, source_directory: str) -> None:
        payload = {
            "id": f"topic-{index}",
            "title": f"主题{index}",
            "source_directory": source_directory,
        }
        (topics_dir / f"topic-{index}.json").write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )

    def test_empty_topics_directory_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(0, completed.returncode)
        report = json.loads(completed.stdout)
        self.assertIn("empty-corpus", {item["rule"] for item in report["findings"]})

    def test_topics_directory_is_a_public_corpus_interface(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            for index in (1, 2):
                bundle = project / f"bundle-{index}"
                bundle.mkdir()
                self.write_good_bundle(bundle)
                self.write_topic(topics_dir, index, bundle.name)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(2, report["stats"]["article_count"])
        self.assertEqual(0, report["stats"]["files_with_errors"])

    def test_article_errors_make_the_corpus_audit_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            bundle = project / "bundle-1"
            bundle.mkdir()
            self.write_good_bundle(bundle)
            zhihu = bundle / "zhihu-explainer_zhihu.md"
            zhihu.write_text(
                zhihu.read_text(encoding="utf-8").replace("## 延伸阅读", "正文残留相关研究。\n\n## 延伸阅读"),
                encoding="utf-8",
            )
            self.write_topic(topics_dir, 1, bundle.name)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(0, completed.returncode)
        report = json.loads(completed.stdout)
        self.assertEqual(1, report["stats"]["files_with_errors"])
        self.assertIn("generic-citation-anchor", {item["rule"] for item in report["findings"]})

    def test_report_includes_accessibility_distribution_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            bundle = project / "bundle-1"
            bundle.mkdir()
            self.write_good_bundle(bundle)
            self.write_topic(topics_dir, 1, bundle.name)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(0, report["stats"]["articles_below_1800"])
        self.assertEqual(1, report["stats"]["articles_with_complete_reading_lists"])
        self.assertEqual(0, report["stats"]["articles_with_images"])
        self.assertGreaterEqual(report["stats"]["median_chinese_chars"], 1800)

    def test_cross_article_repetition_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            for index in (1, 2):
                bundle = project / f"bundle-{index}"
                bundle.mkdir()
                self.write_good_bundle(bundle)
                self.write_topic(topics_dir, index, bundle.name)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        report = json.loads(completed.stdout)
        rules = {item["rule"] for item in report["findings"]}
        self.assertIn("cross-article-repetition", rules)
        self.assertGreater(report["stats"]["repeated_substantive_lines"], 0)

    def test_heading_template_concentration_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            for index in (1, 2, 3):
                bundle = project / f"bundle-{index}"
                bundle.mkdir()
                self.write_good_bundle(bundle)
                self.write_topic(topics_dir, index, bundle.name)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        report = json.loads(completed.stdout)
        rules = {item["rule"] for item in report["findings"]}
        self.assertIn("heading-template-concentration", rules)
        self.assertEqual(3, report["stats"]["largest_heading_template_cluster"])

    def test_common_generic_heading_is_reported_across_varied_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            topics_dir = project / "topics"
            topics_dir.mkdir()
            replacements = [
                {},
                {"## 误区从哪来": "## 为什么这个直觉会失灵", "## 真实机制": "## 问题到底出在哪"},
                {"## 误区从哪来": "## 为什么我们会误判", "## 真实机制": "## 为什么系统会失败"},
            ]
            for index, changes in enumerate(replacements, start=1):
                bundle = project / f"bundle-{index}"
                bundle.mkdir()
                self.write_good_bundle(bundle)
                zhihu = bundle / "zhihu-explainer_zhihu.md"
                text = zhihu.read_text(encoding="utf-8")
                for old, new in changes.items():
                    text = text.replace(old, new)
                zhihu.write_text(text, encoding="utf-8")
                self.write_topic(topics_dir, index, bundle.name)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topics-dir",
                    str(topics_dir),
                    "--project-root",
                    str(project),
                    "--json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        report = json.loads(completed.stdout)
        rules = {item["rule"] for item in report["findings"]}
        self.assertIn("generic-heading-concentration", rules)
        self.assertEqual(3, report["stats"]["largest_heading_name_cluster"])


if __name__ == "__main__":
    unittest.main()

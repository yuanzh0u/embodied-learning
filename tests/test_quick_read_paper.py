"""Tests for scripts/quick_read_paper.py — single-paper quick-read cards.

Network, the claude CLI, and the editorial audit are mocked; assertions cover
brief rendering, the mandatory deep-read gate, cache semantics, sentinel
extraction, and the exit-code contract (0 = card written/cached, 3 = deep-read
unavailable, 1 = hard failure).
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest

from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # script imports embodied_learning.*

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "quick_read_paper.py"


def load_module():
    spec = importlib.util.spec_from_file_location("quick_read_paper", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PAPER_ID = "2402.10329"


def sample_note() -> dict:
    return {
        "schema_version": 1,
        "paper": {"arxiv_id": PAPER_ID, "title": "A Study of Embodied Data", "published": "2024-02-15",
                  "url": f"https://arxiv.org/abs/{PAPER_ID}"},
        "review": {"question": "数据质量如何界定", "topic_ids": ["EA-DATA"], "mode": "rapid"},
        "extraction": {"quality": "high"},
        "reading": {"status": "evidence-ready", "paper_type": "method", "relevance": {"decision": "include", "reason": "直接相关"}},
        "research_question": "什么时候数据算高质量",
        "contributions": ["提出效用中心的数据质量框架"],
        "method": {"summary": "先定义质量信号再验证"},
        "evidence_cards": [{
            "card_id": f"{PAPER_ID}-C01", "claim": "闭环收益决定数据价值",
            "quantitative": {"metric": "success rate", "value_or_direction": "+12%", "comparator": "vs baseline"},
            "source_context": "Closed-loop utility improves success rate by 12 points.",
        }],
        "limitations": {
            "author_stated": [{"limitation": "仅在单臂平台验证", "locator": "Discussion"}],
            "reader_inferred": [{"boundary": "可能不外推到腿式", "basis": "未含腿式实验"}],
        },
        "transfer_boundary": "仅在桌面抓放场景成立",
        "study_context": {"datasets": ["RLBench"], "tasks": ["pick-and-place"], "embodiments": ["单臂"]},
        "evaluation": {"design": "对照实验", "baselines": ["random"], "metrics": ["success rate"]},
        "critical_appraisal": {"design_strengths": ["有对照"], "design_risks": ["样本少"]},
    }


SAMPLE_META = {"title": "A Study of Embodied Data", "quality": "high", "url": f"https://arxiv.org/abs/{PAPER_ID}"}


class BriefBuilderTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_brief_carries_verbatim_fields(self):
        brief = self.module.build_quick_read_brief(PAPER_ID, sample_note(), SAMPLE_META)
        for expected in (
            "A Study of Embodied Data", "闭环收益决定数据价值", "+12%", "success rate",
            "仅在单臂平台验证", "可能不外推到腿式", "仅在桌面抓放场景成立", "RLBench",
            f"[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})", "600-1200", "禁止表格",
        ):
            self.assertIn(expected, brief)

    def test_empty_fields_get_placeholders(self):
        note = sample_note()
        note["study_context"] = {}
        note["critical_appraisal"] = {}
        note["limitations"]["author_stated"] = []
        brief = self.module.build_quick_read_brief(PAPER_ID, note, SAMPLE_META)
        self.assertIn(self.module.UNPROVIDED, brief)
        self.assertNotIn("RLBench", brief)

    def test_non_dict_quantitative_card_rendered_without_numbers(self):
        note = sample_note()
        note["evidence_cards"][0]["quantitative"] = False
        brief = self.module.build_quick_read_brief(PAPER_ID, note, SAMPLE_META)
        self.assertNotIn("+12%", brief)


class QuickReadPipelineTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb_root = Path(self.tmp.name) / "kb"
        self.kb_root.mkdir()
        self.pool_dir = self.kb_root / "pool" / f"arxiv-{PAPER_ID}"

    def seed_pool(self, *, note: dict | None = None):
        self.pool_dir.mkdir(parents=True, exist_ok=True)
        (self.pool_dir / "extraction.json").write_text("{}", encoding="utf-8")
        (self.pool_dir / "note.json").write_text(json.dumps(note or sample_note()), encoding="utf-8")
        (self.pool_dir / "note.json.audit.json").write_text(json.dumps({"status": "pass"}), encoding="utf-8")
        (self.pool_dir / "paper.md").write_text("## 1 Introduction\n\nSome text.\n", encoding="utf-8")

    def run_main(self, argv, *, deep_status="pass", agent_stdout=None):
        """Stub the reused ensure_* helpers plus the agent call; returns (code, captured)."""
        captured = {}

        def fake_agent(prompt, **kwargs):
            captured["prompt"] = prompt
            return mock.Mock(returncode=0, stdout=agent_stdout or "", stderr="")

        with mock.patch.object(self.module, "ensure_extraction", return_value=True) as extract, \
             mock.patch.object(self.module, "ensure_deep_read", return_value=deep_status) as deep, \
             mock.patch.object(self.module, "audit_article") as audit, \
             mock.patch.object(self.module, "resolve_cli", return_value="/fake/claude"), \
             mock.patch.object(self.module, "run_one_shot_agent", side_effect=fake_agent):
            code = self.module.main(argv)
        captured.update(extract=extract, deep=deep, audit=audit)
        return code, captured

    def test_full_pipeline_writes_card_and_json(self):
        self.seed_pool()
        article = "# 速读\n\n## 一句话定位\n\n" + "测试正文。" * 100 + f"\n\n## 链接\n\n[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})\n"
        sentinel_output = f"前置说明\n{self.module.ARTICLE_OPEN}\n{article}\n{self.module.ARTICLE_CLOSE}\n后记"
        code, captured = self.run_main(
            ["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)],
            agent_stdout=sentinel_output,
        )
        self.assertEqual(code, 0)
        article_path = self.pool_dir / self.module.ARTICLE_NAME
        self.assertTrue(article_path.is_file())
        self.assertIn("测试正文。", article_path.read_text(encoding="utf-8"))
        self.assertFalse("前置说明" in article_path.read_text(encoding="utf-8"))
        self.assertTrue((self.pool_dir / self.module.BRIEF_NAME).is_file())
        self.assertIn(f"{self.pool_dir / 'paper.md'}", captured["prompt"])
        self.assertIn(self.module.ARTICLE_OPEN, captured["prompt"])
        captured["audit"].assert_called_once()

    def test_deep_read_unavailable_is_exit_3_without_article(self):
        self.seed_pool()
        code, _ = self.run_main(
            ["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)],
            deep_status="failed",
        )
        self.assertEqual(code, 3)
        self.assertFalse((self.pool_dir / self.module.ARTICLE_NAME).exists())

    def test_needs_review_is_acceptable(self):
        self.seed_pool()
        article = "# 速读\n\n## 一句话定位\n\n" + "测试正文。" * 100 + f"\n\n## 链接\n\n[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})\n"
        output = f"{self.module.ARTICLE_OPEN}\n{article}\n{self.module.ARTICLE_CLOSE}"
        code, _ = self.run_main(
            ["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)],
            deep_status="needs-review", agent_stdout=output,
        )
        self.assertEqual(code, 0)

    def test_cache_hit_skips_agent_until_note_changes(self):
        self.seed_pool()
        article_path = self.pool_dir / self.module.ARTICLE_NAME
        article_path.write_text("缓存卡", encoding="utf-8")
        code, captured = self.run_main(["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)])
        self.assertEqual(code, 0)
        self.assertEqual("缓存卡", article_path.read_text(encoding="utf-8"))
        # run_one_shot_agent never called: its mock side_effect would have raised KeyError.
        # Now touch note.json so the cache goes stale.
        (self.pool_dir / "note.json").write_text(json.dumps(sample_note()), encoding="utf-8")
        article = "# 速读\n\n## 一句话定位\n\n" + "重写正文。" * 100 + f"\n\n## 链接\n\n[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})\n"
        output = f"{self.module.ARTICLE_OPEN}\n{article}\n{self.module.ARTICLE_CLOSE}"
        code, _ = self.run_main(["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)], agent_stdout=output)
        self.assertEqual(code, 0)
        self.assertIn("重写正文。", article_path.read_text(encoding="utf-8"))

    def test_force_rewrites_even_when_fresh(self):
        self.seed_pool()
        article_path = self.pool_dir / self.module.ARTICLE_NAME
        article_path.write_text("旧卡", encoding="utf-8")
        article = "# 速读\n\n## 一句话定位\n\n" + "强制重写。" * 100 + f"\n\n## 链接\n\n[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})\n"
        output = f"{self.module.ARTICLE_OPEN}\n{article}\n{self.module.ARTICLE_CLOSE}"
        code, _ = self.run_main(
            ["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root), "--force"],
            agent_stdout=output,
        )
        self.assertEqual(code, 0)
        self.assertIn("强制重写。", article_path.read_text(encoding="utf-8"))

    def test_missing_sentinel_is_exit_1(self):
        self.seed_pool()
        code, _ = self.run_main(
            ["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)],
            agent_stdout="没有标记的输出",
        )
        self.assertEqual(code, 1)
        self.assertFalse((self.pool_dir / self.module.ARTICLE_NAME).exists())

    def test_skip_agent_writes_brief_only(self):
        self.seed_pool()
        code, _ = self.run_main(["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root), "--skip-agent"])
        self.assertEqual(code, 0)
        self.assertTrue((self.pool_dir / self.module.BRIEF_NAME).is_file())
        self.assertFalse((self.pool_dir / self.module.ARTICLE_NAME).exists())

    def test_extraction_failure_is_exit_1(self):
        with mock.patch.object(self.module, "ensure_extraction", return_value=False), \
             mock.patch.object(self.module, "ensure_deep_read") as deep:
            code = self.module.main(["--arxiv-id", PAPER_ID, "--kb-root", str(self.kb_root)])
        self.assertEqual(code, 1)
        deep.assert_not_called()


class SentinelExtractionTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_accepts_valid_card(self):
        article = "# 速读\n\n" + "正文。" * 100 + f"\n[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})"
        raw = f"noise\n{self.module.ARTICLE_OPEN}\n{article}\n{self.module.ARTICLE_CLOSE}\nnoise"
        # extract_article strips sentinel-bounded content and appends one newline.
        self.assertEqual(self.module.extract_article(raw, PAPER_ID), article + "\n")

    def test_rejects_missing_sentinels_or_short_or_table_or_wrong_link(self):
        good_body = "# 速读\n\n" + "正文。" * 100 + f"\n[arXiv:{PAPER_ID}](https://arxiv.org/abs/{PAPER_ID})\n"
        with self.subTest("no sentinels"):
            self.assertIsNone(self.module.extract_article("plain text", PAPER_ID))
        with self.subTest("too short"):
            self.assertIsNone(self.module.extract_article(
                f"{self.module.ARTICLE_OPEN}\n太短\n{self.module.ARTICLE_CLOSE}", PAPER_ID))
        with self.subTest("table"):
            self.assertIsNone(self.module.extract_article(
                f"{self.module.ARTICLE_OPEN}\n{good_body}\n| a | b |\n{self.module.ARTICLE_CLOSE}", PAPER_ID))
        with self.subTest("wrong link"):
            self.assertIsNone(self.module.extract_article(
                f"{self.module.ARTICLE_OPEN}\n# 速读\n\n{'正文。' * 100}\n{self.module.ARTICLE_CLOSE}", PAPER_ID))


if __name__ == "__main__":
    unittest.main()

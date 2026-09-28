#!/usr/bin/env python3
"""Tests for scripts/paper_slide_deck.py — single-paper slide decks.

The agent call, CLI resolution, and the editorial audit are mocked; assertions
cover brief rendering, the mandatory deep-read gate, cache semantics, sentinel
extraction with the citation whitelist, and the exit-code contract
(0 = deck written/cached, 3 = deep-read unavailable, 1 = hard failure).
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # script imports embodied_learning.*

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "paper_slide_deck.py"


def load_module():
    spec = importlib.util.spec_from_file_location("paper_slide_deck", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


psd = load_module()
PAPER_ID = "2402.10329"


def sample_note() -> dict:
    return {
        "paper": {"title": "A Study of Embodied Data", "arxiv_id": PAPER_ID},
        "one_sentence": "A benchmark for embodied data quality.",
        "results": {"quantitative": [
            {"claim": "过滤后通过率提升", "value": "0.30→0.71"},
        ]},
        "limitations": {"stated": ["单机器人场景"], "reader_inferred": [],
                        "boundary": "不覆盖双臂"},
    }


def sample_source() -> str:
    filler = "该页给出论文中可核验的细节与限定条件，数字只来自简报素材。" * 2
    slides = []
    for i in range(6):
        slides.append(
            f"---\nkicker: 章节\ntitle: 论点{i}\nverdict: 结论{i}\n\n"
            f"- 要点 {{{{main}}}}：{filler}\n- 边界与条件：{filler}\n")
    return ("# title: A Study of Embodied Data\n# subtitle: 组会汇报\n\n"
            "---\nclass: cover\n\n" + "\n".join(slides))


class SlideBriefTest(unittest.TestCase):
    def test_brief_renders_note_fields(self) -> None:
        brief = psd.build_slide_brief(PAPER_ID, sample_note(), {"title": "T"})
        self.assertIn(PAPER_ID, brief)
        self.assertIn("A Study of Embodied Data", brief)
        self.assertIn("0.30→0.71", brief)
        self.assertIn("单机器人场景", brief)
        self.assertIn("{{main}}", brief)

    def test_brief_handles_sparse_note(self) -> None:
        brief = psd.build_slide_brief(PAPER_ID, {}, {})
        self.assertIn(psd.UNPROVIDED, brief)

    def test_refs_whitelist_single_main_key(self) -> None:
        refs = psd.build_refs(PAPER_ID, {"title": "T"})
        self.assertEqual(list(refs), ["main"])
        self.assertEqual(refs["main"]["url"], f"https://arxiv.org/abs/{PAPER_ID}")


class ExtractSourceTest(unittest.TestCase):
    def test_valid_source_passes(self) -> None:
        raw = f"{psd.SOURCE_OPEN}\n{sample_source()}\n{psd.SOURCE_CLOSE}"
        source = psd.extract_source(raw)
        self.assertIsNotNone(source)
        self.assertIn("class: cover", source)

    def test_missing_sentinels_rejected(self) -> None:
        self.assertIsNone(psd.extract_source("no sentinels here"))

    def test_missing_cover_rejected(self) -> None:
        body = sample_source().replace("class: cover\n", "")
        raw = f"{psd.SOURCE_OPEN}\n{body}\n{psd.SOURCE_CLOSE}"
        self.assertIsNone(psd.extract_source(raw))
        self.assertIn("cover", psd.describe_rejection(raw))

    def test_too_few_pages_rejected(self) -> None:
        filler = "填充内容用于越过长度下限检查，重复到足够长。" * 40
        body = ("# title: T\n\n---\nclass: cover\n\n---\nkicker: k\ntitle: t\n"
                f"verdict: v\n\n- a {filler}\n")
        raw = f"{psd.SOURCE_OPEN}\n{body}\n{psd.SOURCE_CLOSE}"
        self.assertIsNone(psd.extract_source(raw))
        self.assertIn("页数不足", psd.describe_rejection(raw))

    def test_foreign_citation_key_rejected(self) -> None:
        body = sample_source().replace("{{main}}", "{{other}}", 1)
        raw = f"{psd.SOURCE_OPEN}\n{body}\n{psd.SOURCE_CLOSE}"
        self.assertIsNone(psd.extract_source(raw))
        self.assertIn("白名单", psd.describe_rejection(raw))

    def test_remote_image_rejected(self) -> None:
        body = sample_source() + "\n@fig https://arxiv.org/x.png | 图\n"
        raw = f"{psd.SOURCE_OPEN}\n{body}\n{psd.SOURCE_CLOSE}"
        self.assertIsNone(psd.extract_source(raw))
        self.assertIn("外链图片", psd.describe_rejection(raw))


class MainFlowTest(unittest.TestCase):
    def _pool(self, actions: list[list[str]]):
        """Run psd.main for each argv inside one pool tmpdir.

        Yields (exit codes, pool_dir, agent mock); the pool_dir is only valid
        inside the with-block.
        """

        @contextlib.contextmanager
        def pool():
            with tempfile.TemporaryDirectory() as tmp:
                pool_root = Path(tmp)
                pool_dir = pool_root / f"arxiv-{PAPER_ID}"
                pool_dir.mkdir()
                (pool_dir / "note.json").write_text(json.dumps(sample_note()),
                                                    encoding="utf-8")
                (pool_dir / "paper.md").write_text("paper text", encoding="utf-8")
                codes = []
                with mock.patch.object(psd, "pool_root_for", return_value=pool_root), \
                     mock.patch.object(psd, "ensure_extraction", return_value=True), \
                     mock.patch.object(psd, "ensure_deep_read", return_value="pass"), \
                     mock.patch.object(psd, "resolve_cli", return_value="claude"), \
                     mock.patch.object(psd, "complete",
                                       return_value=mock.Mock(
                                           stdout=f"{psd.SOURCE_OPEN}\n{sample_source()}\n"
                                                  f"{psd.SOURCE_CLOSE}")) as agent, \
                     mock.patch.object(psd, "compile_and_audit",
                                       side_effect=lambda pool_dir, with_audit=True: (
                                           (pool_dir / psd.DECK_NAME).write_text(
                                               "<html></html>", encoding="utf-8"),
                                           True, [])[1:]):
                    for argv in actions:
                        codes.append(psd.main(argv))
                yield codes, pool_dir, agent

        return pool()

    def test_exit_zero_and_deck_written(self) -> None:
        with self._pool([["--arxiv-id", PAPER_ID, "--kb-root", "/nowhere"]]) as (
                codes, pool_dir, _agent):
            self.assertEqual(codes, [0])
            self.assertTrue((pool_dir / "slide-deck_report.md").is_file())
            self.assertTrue((pool_dir / "refs.json").is_file())
            self.assertTrue((pool_dir / "slide-brief.md").is_file())

    def test_second_run_hits_cache_without_new_agent_call(self) -> None:
        argv = ["--arxiv-id", PAPER_ID, "--kb-root", "/nowhere"]
        with self._pool([argv, argv]) as (codes, _pool_dir, agent):
            self.assertEqual(codes, [0, 0])
            self.assertEqual(agent.call_count, 1)  # second run: cache hit

    def test_deep_read_unavailable_is_exit_3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(psd, "pool_root_for", return_value=Path(tmp)), \
             mock.patch.object(psd, "ensure_extraction", return_value=True), \
             mock.patch.object(psd, "ensure_deep_read", return_value="failed"):
            code = psd.main(["--arxiv-id", PAPER_ID, "--kb-root", str(tmp)])
            self.assertEqual(code, 3)

    def test_skip_agent_writes_only_brief(self) -> None:
        with self._pool([["--arxiv-id", PAPER_ID, "--kb-root", "/nowhere",
                          "--skip-agent"]]) as (codes, pool_dir, agent):
            self.assertEqual(codes, [0])
            self.assertFalse((pool_dir / "slide-deck_report.md").is_file())
            self.assertTrue((pool_dir / "slide-brief.md").is_file())
            agent.assert_not_called()


if __name__ == "__main__":
    unittest.main()

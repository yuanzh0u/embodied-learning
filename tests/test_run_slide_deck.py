#!/usr/bin/env python3
"""Tests for scripts/run_slide_deck.py — run-level slide decks.

The agent call, CLI resolution, and compile/audit are mocked; assertions cover
appendix reference parsing, the run-dir validation gate, sentinel extraction
with the run's own reference keys as the whitelist, and the exit-code contract
(0 = deck written/cached, 2 = invalid run dir, 1 = hard failure).
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
SCRIPT_PATH = REPO_ROOT / "scripts" / "run_slide_deck.py"


def load_module():
    spec = importlib.util.spec_from_file_location("run_slide_deck", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


rsd = load_module()
psd = rsd.psd  # sibling single-paper module: sentinels, guards, compile+audit
APPENDIX = (
    "# 证据附录\n\n## References\n\n"
    "- `2505.11709` [EgoDex](https://arxiv.org/abs/2505.11709) (2025)\n"
    "- `2602.16710` [EgoScale](https://arxiv.org/abs/2602.16710) (2026)\n"
    "- `2505.11709` [EgoDex](https://arxiv.org/abs/2505.11709) (2025)\n"  # duplicate line
)
BRIEF = "# 写作简报\n\n## 核心主张\n\n- 底图模式把配准难题收敛为四类退化源。\n"


def sample_source(cited_key: str = "2505.11709") -> str:
    filler = "该页给出可核验的细节与限定条件，数字只来自简报素材。" * 2
    slides = []
    for i in range(6):
        slides.append(
            f"---\nkicker: 章节\ntitle: 论点{i}\nverdict: 结论{i}\n\n"
            f"- 要点 {{{{{cited_key}}}}}：{filler}\n- 边界与条件：{filler}\n")
    return ("# title: 汇报\n# subtitle: run 级\n\n---\nclass: cover\n\n" + "\n".join(slides))


class ParseAppendixRefsTest(unittest.TestCase):
    def test_parses_labels_and_dedupes(self) -> None:
        refs = rsd.parse_appendix_refs(APPENDIX)
        self.assertEqual(sorted(refs), ["2505.11709", "2602.16710"])
        self.assertEqual(refs["2505.11709"]["title"], "EgoDex")
        self.assertEqual(refs["2602.16710"]["url"], "https://arxiv.org/abs/2602.16710")

    def test_digit_leading_label_is_a_legal_key(self) -> None:
        self.assertEqual(rsd.sanitize_key("2505.11709"), "2505.11709")

    def test_odd_labels_get_sanitized(self) -> None:
        self.assertEqual(rsd.sanitize_key("weird key!"), "weird_key_")
        self.assertTrue(rsd.sanitize_key("_x").startswith("r"))
        self.assertEqual(rsd.parse_appendix_refs("- `weird key!` [T](https://a/b)")[ "weird_key_"]["title"], "T")

    def test_collision_same_label_different_url_gets_suffix(self) -> None:
        text = (APPENDIX
                + "- `2505.11709` [Other](https://example.org/other)\n")
        refs = rsd.parse_appendix_refs(text)
        self.assertEqual(len(refs), 3)
        self.assertIn("2505.11709_2", refs)


class ExtractSourceTest(unittest.TestCase):
    def test_arxiv_id_citation_keys_allowed(self) -> None:
        raw = f"{psd.SOURCE_OPEN}\n{sample_source()}\n{psd.SOURCE_CLOSE}"
        source = psd.extract_source(raw, allowed_keys=frozenset({"2505.11709"}))
        self.assertIsNotNone(source)

    def test_unknown_key_rejected(self) -> None:
        raw = f"{psd.SOURCE_OPEN}\n{sample_source('9999.99999')}\n{psd.SOURCE_CLOSE}"
        self.assertIsNone(psd.extract_source(raw, allowed_keys=frozenset({"2505.11709"})))
        self.assertIn("白名单", psd.describe_rejection(raw, allowed_keys=frozenset({"2505.11709"})))


class MainFlowTest(unittest.TestCase):
    def _pool(self, actions, *, with_brief: bool = True, with_appendix: bool = True):
        """actions: list of callables run_dir -> argv (paths only exist inside)."""
        import contextlib

        @contextlib.contextmanager
        def run_ctx():
            with tempfile.TemporaryDirectory() as tmp:
                run_dir = Path(tmp) / "literature-review-demo-20260101"
                run_dir.mkdir()
                (run_dir / "run.json").write_text("{}", encoding="utf-8")
                if with_brief:
                    (run_dir / "writing-brief.md").write_text(BRIEF, encoding="utf-8")
                if with_appendix:
                    (run_dir / "evidence-appendix.md").write_text(APPENDIX, encoding="utf-8")
                codes = []
                with mock.patch.object(rsd, "resolve_cli", return_value="claude"), \
                     mock.patch.object(rsd, "complete",
                                       return_value=mock.Mock(
                                           stdout=f"{psd.SOURCE_OPEN}\n{sample_source()}\n"
                                                  f"{psd.SOURCE_CLOSE}")) as agent, \
                     mock.patch.object(rsd.psd, "compile_and_audit",
                                       side_effect=lambda d, with_audit=True: (
                                           (d / psd.DECK_NAME).write_text("<html></html>",
                                                                          encoding="utf-8"),
                                           True, [])[1:]):
                    for build_argv in actions:
                        codes.append(rsd.main(build_argv(run_dir)))
                yield codes, run_dir, agent

        return run_ctx()

    def test_exit_zero_and_outputs_written(self) -> None:
        with self._pool([lambda d: ["--run-dir", str(d)]]) as (codes, run_dir, agent):
            self.assertEqual(codes, [0])
            self.assertTrue((run_dir / "refs.json").is_file())
            self.assertTrue((run_dir / "slide-deck_report.md").is_file())
            agent.assert_called_once()

    def test_second_run_hits_cache_without_new_agent_call(self) -> None:
        with self._pool([lambda d: ["--run-dir", str(d)]] * 2) as (codes, _run_dir, agent):
            self.assertEqual(codes, [0, 0])
            self.assertEqual(agent.call_count, 1)

    def test_missing_appendix_is_exit_2(self) -> None:
        with self._pool([lambda d: ["--run-dir", str(d)]], with_appendix=False) as (codes, run_dir, agent):
            self.assertEqual(codes, [2])
            agent.assert_not_called()

    def test_appendix_without_references_is_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"
            run_dir.mkdir()
            (run_dir / "run.json").write_text("{}", encoding="utf-8")
            (run_dir / "writing-brief.md").write_text(BRIEF, encoding="utf-8")
            (run_dir / "evidence-appendix.md").write_text("# 无引用\n", encoding="utf-8")
            code = rsd.main(["--run-dir", str(run_dir)])
            self.assertEqual(code, 2)
            self.assertFalse((run_dir / "slide-deck_report.md").is_file())

    def test_not_a_run_dir_is_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = rsd.main(["--run-dir", tmp])
            self.assertEqual(code, 2)

    def test_skip_agent_writes_only_refs(self) -> None:
        with self._pool([lambda d: ["--run-dir", str(d), "--skip-agent"]]) as (codes, run_dir, agent):
            self.assertEqual(codes, [0])
            self.assertFalse((run_dir / "slide-deck_report.md").is_file())
            self.assertTrue((run_dir / "refs.json").is_file())
            agent.assert_not_called()


if __name__ == "__main__":
    unittest.main()

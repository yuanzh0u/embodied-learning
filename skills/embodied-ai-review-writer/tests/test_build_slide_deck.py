#!/usr/bin/env python3
"""Tests for the slide-deck compiler (build_slide_deck.py)."""

from __future__ import annotations

import base64
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


bsd = load("bsd_test", "skills/embodied-ai-review-writer/scripts/build_slide_deck.py")

DOC = """# title: 试编
# refs: refs.json
# end: 谢谢

---
kicker: 章节
title: 页一
verdict: 结论 {{alpha}}

- 要点一 {{alpha}}
- 要点二 {{beta}}

---
kicker: 章节
title: 页二

1. 第一步
2. 第二步

@stat 0.71 | 通过率
@stat 0.85 | 目标

@bars A 0.30 ; *B 0.85 ; !C 1.2
"""

REFS = {
    "alpha": {"title": "Alpha Paper", "url": "https://arxiv.org/abs/1"},
    "beta": {"title": "Beta Paper", "url": ""},
}


def write_source(tmp: Path, doc: str = DOC, refs: dict | None = None) -> Path:
    (tmp / "refs.json").write_text(json.dumps(refs or REFS), encoding="utf-8")
    src = tmp / "slide-deck_report.md"
    src.write_text(doc, encoding="utf-8")
    return src


class CompileHappyPathTest(unittest.TestCase):
    def test_sections_citations_and_balance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = write_source(Path(tmp))
            errors: list[str] = []
            html, summary = bsd.compile_deck(src, None, errors)
            self.assertEqual(errors, [])
            self.assertEqual(summary["citations"], 2)
            body = re.sub(r"<script>.*?</script>", "", html[html.index("<body>"):], flags=re.S)
            secs = re.findall(r"<section.*?</section>", body, flags=re.S)
            # 2 content + 1 refs page + 1 end
            self.assertEqual(len(secs), 4)
            for i, sec in enumerate(secs, 1):
                self.assertEqual(sec.count("<div"), sec.count("</div>"), f"slide {i}")
            # first-appearance numbering: alpha=1, beta=2; verdict re-cites alpha
            self.assertEqual(re.findall(r'class="cite">\[(\d+)\]', body), ["1", "2", "1"])
            # refs page lists both entries
            self.assertIn("Alpha Paper", body)
            self.assertIn("Beta Paper", body)

    def test_html_is_single_file_and_offline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = write_source(Path(tmp))
            html, _ = bsd.compile_deck(src, None, [])
            self.assertNotIn('src="http', html)
            self.assertNotIn('href="http', html.replace(
                '<a href="https://arxiv.org/abs/1">https://arxiv.org/abs/1</a>', ""))
            self.assertIn("Reveal.initialize", html)


class ValidationTest(unittest.TestCase):
    def test_unknown_directive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors: list[str] = []
            bsd.render_body("@bogus 参数", {"a": 1}, 3, Path(tmp), errors)
            self.assertTrue(any("@bogus" in e for e in errors))

    def test_unknown_citation_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = DOC.replace("{{beta}}", "{{missing}}")
            src = write_source(Path(tmp), doc)
            with self.assertRaises(bsd.CompileError):
                bsd.compile_deck(src, None, [])

    def test_missing_title_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = "---\nkicker: x\n\n- 要点\n"
            src = write_source(Path(tmp), doc)
            errors: list[str] = []
            bsd.compile_deck(src, None, errors)
            self.assertTrue(any("缺少 title" in e for e in errors))

    def test_bullet_density_cap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bullets = "\n".join(f"- 要点{i}" for i in range(8))
            doc = "---\nkicker: x\ntitle: 页\n\n" + bullets
            src = write_source(Path(tmp), doc)
            errors: list[str] = []
            bsd.compile_deck(src, None, errors)
            self.assertTrue(any("超过每页" in e for e in errors))

    def test_missing_figure_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = "---\nkicker: x\ntitle: 页\n\n@fig nope.png | 图注\n"
            src = write_source(Path(tmp), doc)
            with self.assertRaises(bsd.CompileError):
                bsd.compile_deck(src, None, [])


class RendererTest(unittest.TestCase):
    def test_bars_marker_classes_and_width(self) -> None:
        html = bsd._bars_html("A 0.30 ; *B 85% ; !C 120", 1)
        self.assertIn('class="row "', html)
        self.assertIn('class="row ours"', html)
        self.assertIn('class="row risk"', html)
        self.assertIn("width:30.0%", html)
        self.assertIn("width:85.0%", html)
        self.assertIn("width:100.0%", html)  # >1 clamps

    def test_tier_hot_and_arrows(self) -> None:
        html = bsd.render_body("@tier A > *B", {}, 1, Path("."), [])
        self.assertIn('<div class="t hot">B</div>', html)
        self.assertEqual(html.count('<div class="arrow">→</div>'), 1)

    def test_statrow_merges_adjacent_stats(self) -> None:
        html = bsd.render_body("@stat 1 | a\n@stat 2 | b", {}, 1, Path("."), [])
        self.assertEqual(html.count('<div class="statrow">'), 1)
        self.assertEqual(html.count('<div class="stat">'), 2)

    def test_fig_inlines_base64(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            png = Path(tmp) / "f.png"
            png.write_bytes(b"\x89PNG\r\n\x1a\n")
            html = bsd.render_body(f"@fig {png} | 图注", {}, 1, Path(tmp), [])
            self.assertIn("data:image/png;base64,", html)
            self.assertIn(base64.b64encode(png.read_bytes()).decode(), html)

    def test_inline_escapes_html_then_formats(self) -> None:
        out = bsd._inline("<b>x</b> **y** `z`", {"k": 1}, 1)
        self.assertIn("&lt;b&gt;", out)
        self.assertIn("<strong>y</strong>", out)
        self.assertIn("<code>z</code>", out)

    def test_verdict_and_kicker_render(self) -> None:
        slide = {"idx": 1, "head": {"kicker": "K", "title": "T", "verdict": "V"},
                 "body": "- a"}
        html = bsd.render_slide(slide, {}, Path("."), [])
        self.assertIn('<p class="kicker">K</p>', html)
        self.assertIn("<h2>T</h2>", html)
        self.assertIn('<div class="verdict">V</div>', html)


class RefsPagesTest(unittest.TestCase):
    def test_chunking(self) -> None:
        keymap = {f"k{i}": i + 1 for i in range(60)}
        refs = {k: {"title": t, "url": ""} for k, t in keymap.items()}
        pages = bsd.render_refs_pages(keymap, refs)
        self.assertEqual(len(pages), 3)
        self.assertIn("参考文献 1–27", pages[0])
        self.assertIn("参考文献 28–54", pages[1])


if __name__ == "__main__":
    unittest.main()

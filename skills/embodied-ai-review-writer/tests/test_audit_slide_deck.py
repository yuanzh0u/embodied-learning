#!/usr/bin/env python3
"""Tests for the audit-slide-deck subcommand (_slide_deck.py)."""

from __future__ import annotations

import importlib.util
import json
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


sd = load("sd_audit_test", "skills/embodied-ai-review-writer/scripts/_slide_deck.py")

REFS = {"alpha": {"title": "Alpha", "url": ""}, "beta": {"title": "Beta", "url": ""}}

GOOD_DOC = (
    "# title: 试编\n# refs: refs.json\n\n"
    + "".join(
        f"---\nkicker: 章节\ntitle: 页{i}\nverdict: 结论 {i}\n\n" + "- 要点 {{alpha}}\n\n"
        for i in range(10)
    )
    + "---\nkicker: 尾\ntitle: 附加页\nverdict: 收束\n\n- {{beta}}\n"
)


class AuditSourceTest(unittest.TestCase):
    def _write(self, tmp: Path, doc: str = GOOD_DOC, refs: dict | None = None) -> Path:
        (tmp / "refs.json").write_text(json.dumps(refs or REFS), encoding="utf-8")
        src = tmp / "slide-deck_report.md"
        src.write_text(doc, encoding="utf-8")
        return src

    def test_clean_deck_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            findings, stats = sd.audit_source(self._write(Path(tmp)), None)
            errors = [f for f in findings if f["severity"] == "error"]
            self.assertEqual(errors, [])
            self.assertEqual(stats["pages"], 11)
            self.assertEqual(stats["citations"], 2)

    def test_unknown_citation_key_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = GOOD_DOC.replace("{{beta}}", "{{ghost}}")
            findings, _ = sd.audit_source(self._write(Path(tmp), doc), None)
            self.assertTrue(any(
                f["severity"] == "error" and "ghost" in f["message"] for f in findings))

    def test_too_few_pages_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = "---\nkicker: x\ntitle: 页\nverdict: v\n\n- {{alpha}}\n"
            findings, _ = sd.audit_source(self._write(Path(tmp), doc), None)
            self.assertTrue(any(
                f["severity"] == "error" and "page-count" in f["check"] for f in findings))

    def test_unused_refs_key_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            refs = dict(REFS, unused={"title": "Unused", "url": ""})
            findings, _ = sd.audit_source(self._write(Path(tmp), refs=refs), None)
            self.assertTrue(any(
                f["severity"] == "warning" and "unused" in f["message"] for f in findings))

    def test_missing_fig_file_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = GOOD_DOC + "\n---\nkicker: x\ntitle: 图页\nverdict: v\n\n@fig nope.png | 图\n"
            findings, _ = sd.audit_source(self._write(Path(tmp), doc), None)
            self.assertTrue(any(
                f["severity"] == "error" and f["check"] == "figure-exists" for f in findings))

    def test_unknown_directive_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            doc = GOOD_DOC + "\n---\nkicker: x\ntitle: 页\nverdict: v\n\n@bogus x\n"
            findings, _ = sd.audit_source(self._write(Path(tmp), doc), None)
            self.assertTrue(any(
                f["severity"] == "error" and f["check"] == "density" for f in findings))


class AuditHtmlTest(unittest.TestCase):
    def test_offline_and_balance(self) -> None:
        html = ('<html><body><div class="reveal"><div class="slides">'
                '<section><div><img src="data:image/png;base64,AAA"></div></section>'
                '<section><div></div></section>'
                "</div></div></body></html>")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slide-deck_report.html"
            path.write_text(html, encoding="utf-8")
            findings, stats = sd.audit_html(path, 2)
            self.assertEqual([f for f in findings if f["severity"] == "error"], [])
            self.assertEqual(stats["html_sections"], 2)

    def test_external_image_flagged(self) -> None:
        html = ('<html><body><div class="reveal"><div class="slides">'
                '<section><img src="https://example.com/x.png"></section>'
                "</div></div></body></html>")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "deck.html"
            path.write_text(html, encoding="utf-8")
            findings, _ = sd.audit_html(path, 1)
            self.assertTrue(any(f["check"] == "html-offline" for f in findings))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tarfile
import tempfile
import types
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))  # the tex module imports embodied_learning.* at load time
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "embodied_learning" / "fetch" / "tex.py"
SPEC = importlib.util.spec_from_file_location("extract_arxiv_tex", SCRIPT_PATH)
tex = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(tex)

DOWNLOADER_PATH = Path(__file__).resolve().parents[3] / "embodied_learning" / "fetch" / "s3_source.py"
DOWN_SPEC = importlib.util.spec_from_file_location("download_arxiv_source", DOWNLOADER_PATH)
das = importlib.util.module_from_spec(DOWN_SPEC)
assert DOWN_SPEC and DOWN_SPEC.loader
DOWN_SPEC.loader.exec_module(das)


MAIN_TEX = """\\documentclass{article}
\\title{Conversion Fixture}
\\begin{document}
\\maketitle
\\section{Introduction}
This paper studies UMI data quality at length.
\\input{sections/method}
\\section{Results}
The outcome improves by a large margin. UMI again.
\\end{document}
"""

METHOD_TEX = """\\section{Method}
We use the method with $E=mc^2$ and a table below.

\\begin{tabular}{|l|c|}
\\hline
a & b \\\\
\\hline
\\end{tabular}
"""

DECOY_TEX = "this fragment has no document environment"


def fake_pypandoc(markdown: str, calls: list[dict]) -> types.ModuleType:
    """A pypandoc stand-in recording convert_file arguments."""

    def convert_file(path: str, to: str, format: str = "", extra_args: list[str] | None = None) -> str:
        calls.append({"path": path, "to": to, "format": format, "extra_args": extra_args or []})
        return markdown

    module = types.ModuleType("pypandoc")
    module.convert_file = convert_file
    return module


MARKDOWN = """# Conversion Fixture

## Introduction

This paper studies UMI data quality at length.

## Method

We use the method with $E=mc^2$ and a table below.

| a | b |
|---|---|
| 1 | 2 |

## Results

The outcome improves by a large margin. UMI again.
"""


def tex_args(**overrides: object) -> tex.TexExtraction:
    values: dict[str, object] = {
        "paper_id": "2403.12550",
        "transport": "s3-tex",
        "curl_timeout": 120.0,
        "source": None,
        "source_cache_dir": "/tmp/nonexistent-src",
        "main_tex": None,
        "terms": "UMI",
        "minimum_chars": 90,
        "to": tex.DEFAULT_TO,
        "pandoc_timeout": 60.0,
        "output": None,
        "markdown_output": None,
    }
    values.update(overrides)
    return tex.TexExtraction(**values)


class Arxiv2mdTransportTest(unittest.TestCase):
    def test_fetch_parses_markdown_and_title(self) -> None:
        markdown_payload = "## Contents\n- 1 Introduction\n\n## Abstract\nBody with $E=mc^2$."
        def fake_curl(url: str, timeout: float) -> tuple[str, str]:
            if "/api/markdown" in url:
                return markdown_payload, "200"
            return json.dumps({"arxiv_id": "2403.12550", "title": "Sample Paper"}), "200"
        with mock.patch.object(tex, "_curl_get", side_effect=fake_curl):
            markdown, title = tex.fetch_arxiv2md("2403.12550", 30.0)
        self.assertIn("$E=mc^2$", markdown)
        self.assertEqual("Sample Paper", title)

    def test_http_400_raises_runtime_error(self) -> None:
        with mock.patch.object(tex, "_curl_get", return_value=("Error: no HTML available", "400")):
            with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
                tex.fetch_arxiv2md("0501001", 30.0)

    def test_run_arxiv2md_returns_unified_output(self) -> None:
        markdown_payload = "## Contents\n- 1 Introduction\n\n## Abstract\n" + "UMI body text. " * 30
        def fake_curl(url: str, timeout: float) -> tuple[str, str]:
            if "/api/markdown" in url:
                return markdown_payload, "200"
            return json.dumps({"title": "Sample Paper"}), "200"
        with mock.patch.object(tex, "_curl_get", side_effect=fake_curl):
            output = tex_args(transport="arxiv2md").run()
        self.assertEqual("arxiv2md", output["extraction_method"])
        self.assertEqual("Sample Paper", output["title"])
        self.assertTrue(output["evidence_eligible"])
        self.assertFalse(output["needs_visual_validation"])

    def test_run_arxiv2md_failure_is_reported_not_raised(self) -> None:
        with mock.patch.object(tex, "_curl_get", return_value=("Error: This paper does not have an HTML version", "400")):
            output = tex_args(transport="arxiv2md", paper_id="0501001").run()
        self.assertFalse(output["available"])
        self.assertFalse(output["evidence_eligible"])
        self.assertIn("arxiv2md", output["attempts"][0]["method"])
        self.assertIn("HTTP 400", output["fallback_reason"])


class SafeExtractTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dest = Path(self._tmp.name) / "extracted"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write_tar(self, members: list[tuple[str, bytes | str]]) -> Path:
        path = Path(self._tmp.name) / "src.tar.gz"
        with tarfile.open(path, "w:gz") as archive:
            for name, content in members:
                data = content.encode("utf-8") if isinstance(content, str) else content
                info = tarfile.TarInfo(name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
        return path

    def test_extracts_allowed_members_only(self) -> None:
        tar_path = self._write_tar([("main.tex", MAIN_TEX), ("sections/method.tex", METHOD_TEX), ("evil.sh", "rm -rf")])
        extracted = tex.safe_extract(tar_path, self.dest)
        self.assertIn("main.tex", extracted)
        self.assertIn("sections/method.tex", extracted)
        self.assertNotIn("evil.sh", extracted)
        self.assertTrue((self.dest / "sections" / "method.tex").is_file())

    def test_rejects_path_traversal_members(self) -> None:
        tar_path = self._write_tar([("../escape.tex", "nope"), ("main.tex", MAIN_TEX)])
        extracted = tex.safe_extract(tar_path, self.dest)
        self.assertNotIn("../escape.tex", extracted)
        self.assertFalse((self.dest.parent / "escape.tex").exists())


class FindMainTexTest(unittest.TestCase):
    def test_prefers_member_with_begin_document(self) -> None:
        names = ["decoy.tex", "main.tex", "tiny.tex"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "decoy.tex").write_text(DECOY_TEX)
            (root / "main.tex").write_text(MAIN_TEX)
            (root / "tiny.tex").write_text("\\begin{document}x\\end{document}")
            picked = tex.find_main_tex(names, root=root)
        self.assertEqual(picked, "main.tex")

    def test_forced_member_must_exist(self) -> None:
        self.assertIsNone(tex.find_main_tex(["main.tex"], forced="missing.tex"))
        self.assertEqual(tex.find_main_tex(["main.tex"], forced="main.tex"), "main.tex")

    def test_no_candidate_returns_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "decoy.tex").write_text(DECOY_TEX)
            self.assertIsNone(tex.find_main_tex(["decoy.tex"], root=root))


class RunTest(unittest.TestCase):
    def test_full_pipeline_produces_unified_extraction_json(self) -> None:
        calls: list[dict] = []
        fake = fake_pypandoc(MARKDOWN, calls)
        with mock.patch.dict(sys.modules, {"pypandoc": fake}):
            with tempfile.TemporaryDirectory() as tmp:
                tar_path = Path(tmp) / "src.tar.gz"
                with tarfile.open(tar_path, "w:gz") as archive:
                    for name, content in [("main.tex", MAIN_TEX), ("sections/method.tex", METHOD_TEX), ("decoy.tex", DECOY_TEX)]:
                        data = content.encode("utf-8")
                        info = tarfile.TarInfo(name)
                        info.size = len(data)
                        archive.addfile(info, io.BytesIO(data))
                output = tex_args(source=str(tar_path)).run()

        self.assertTrue(output["available"])
        self.assertTrue(output["evidence_eligible"])
        self.assertEqual(output["source_format"], "tex")
        self.assertEqual(output["extraction_method"], "tex-pandoc")
        self.assertEqual(output["quality"]["grade"], "high")
        self.assertTrue(output["quality"]["math_preserved"])
        self.assertGreaterEqual(output["quality"]["table_count"], 1)
        self.assertEqual(output["main_tex"], "main.tex")
        titles = [section["title"] for section in output["sections"]]
        self.assertIn("Introduction", titles)
        self.assertIn("Method", titles)
        self.assertIn("$E=mc^2$", output["text"])
        self.assertEqual(calls[0]["format"], "latex")
        self.assertIn(tex.DEFAULT_TO, calls[0]["to"])
        self.assertIn("--resource-path", calls[0]["extra_args"])
        locators = [match["locator"] for match in output["term_matches"]]
        self.assertEqual(len(locators), 2)  # UMI appears in Introduction and Results
        self.assertIn("Introduction", locators[0])
        self.assertIn("Results", locators[1])
        self.assertFalse(output["needs_visual_validation"])
        self.assertEqual(output["visual_validation"], "not-required")

    def test_main_tex_override_targets_forced_member(self) -> None:
        calls: list[dict] = []
        fake = fake_pypandoc(MARKDOWN, calls)
        with mock.patch.dict(sys.modules, {"pypandoc": fake}):
            with tempfile.TemporaryDirectory() as tmp:
                tar_path = Path(tmp) / "src.tar.gz"
                with tarfile.open(tar_path, "w:gz") as archive:
                    for name, content in [("main.tex", MAIN_TEX), ("other.tex", MAIN_TEX.replace("Fixture", "Other"))]:
                        data = content.encode("utf-8")
                        info = tarfile.TarInfo(name)
                        info.size = len(data)
                        archive.addfile(info, io.BytesIO(data))
                output = tex_args(source=str(tar_path), main_tex="other.tex").run()
        self.assertEqual(output["main_tex"], "other.tex")

    def test_low_quality_output_is_not_evidence_eligible(self) -> None:
        calls: list[dict] = []
        fake = fake_pypandoc("too short", calls)
        with mock.patch.dict(sys.modules, {"pypandoc": fake}):
            with tempfile.TemporaryDirectory() as tmp:
                tar_path = Path(tmp) / "src.tar.gz"
                with tarfile.open(tar_path, "w:gz") as archive:
                    data = MAIN_TEX.encode("utf-8")
                    info = tarfile.TarInfo("main.tex")
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))
                output = tex_args(source=str(tar_path)).run()
        self.assertFalse(output["evidence_eligible"])
        self.assertEqual(output["quality"]["grade"], "low")

    def test_download_failure_reports_unavailable(self) -> None:
        class FakeClient:
            class exceptions:
                class NoSuchKey(Exception):
                    pass

            def get_object(self, Bucket: str, Key: str):
                raise self.exceptions.NoSuchKey(Key)

        with mock.patch.dict(sys.modules, {"pypandoc": fake_pypandoc("", [])}):
            with mock.patch.object(das, "make_client", return_value=FakeClient()):
                with mock.patch.object(tex, "download_arxiv_source", das):
                    output = tex_args(paper_id="2403.12550").run()
        self.assertFalse(output["available"])
        self.assertFalse(output["evidence_eligible"])
        self.assertIn("not recoverable", output["fallback_reason"])


if __name__ == "__main__":
    unittest.main()

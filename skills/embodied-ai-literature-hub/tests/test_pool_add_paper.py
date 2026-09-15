#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.knowledge.pool import PaperPool, load_json, paper_identity  # noqa: E402


def extraction_json(tmp: Path, **overrides: object) -> Path:
    payload: dict = {
        "paper_id": "2403.12550",
        "available": True,
        "source_format": "tex",
        "extraction_method": "tex-pandoc",
        "title": "RGBD GS-ICP SLAM",
        "text": "# RGBD GS-ICP SLAM\n\nConverted body text.",
        "quality": {"grade": "high", "text_chars": 4000},
    }
    payload.update(overrides)
    path = tmp / "extraction.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


EXTRACTION_KEYS = {"paper_id", "available", "source_format", "extraction_method", "title", "text", "quality", "doi"}


def make_pool(tmp: Path, **overrides: object) -> PaperPool:
    return PaperPool(str(tmp / "pool"))


def add_kwargs(tmp: Path, **overrides: object) -> dict:
    """Keyword arguments for PaperPool.add, mirroring the old CLI arg namespace."""
    content_overrides = {key: value for key, value in overrides.items() if key in EXTRACTION_KEYS}
    extraction_path = extraction_json(tmp, **content_overrides)
    note = overrides.get("note")
    return {
        "extraction": load_json(extraction_path),
        "metadata": None,
        "note": Path(note).read_text(encoding="utf-8") if note else None,
        "note_json": None,
        "html": overrides.get("html"),
        "force": bool(overrides.get("force", False)),
    }


class AddTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_add_creates_per_paper_layout_and_index(self) -> None:
        self.assertEqual(make_pool(self.tmp).add(**add_kwargs(self.tmp)), 0)
        entry = self.tmp / "pool" / "arxiv-2403.12550"
        self.assertTrue((entry / "paper.md").is_file())
        self.assertTrue((entry / "extraction.json").is_file())
        self.assertTrue((entry / "meta.json").is_file())
        index = [json.loads(line) for line in (self.tmp / "pool" / "index.jsonl").read_text().splitlines()]
        self.assertEqual(len(index), 1)
        self.assertEqual(index[0]["arxiv_id"], "2403.12550")
        self.assertEqual(index[0]["quality"], "high")

    def test_re_add_is_idempotent_without_force(self) -> None:
        make_pool(self.tmp).add(**add_kwargs(self.tmp))
        make_pool(self.tmp).add(**add_kwargs(self.tmp))
        index = (self.tmp / "pool" / "index.jsonl").read_text().splitlines()
        self.assertEqual(len(index), 1)

    def test_force_refreshes_entry(self) -> None:
        make_pool(self.tmp).add(**add_kwargs(self.tmp))
        make_pool(self.tmp).add(**add_kwargs(self.tmp, force=True))
        index = (self.tmp / "pool" / "index.jsonl").read_text().splitlines()
        self.assertEqual(len(index), 1)

    def test_note_is_archived(self) -> None:
        note = self.tmp / "note.md"
        note.write_text("# Reading note", encoding="utf-8")
        make_pool(self.tmp).add(**add_kwargs(self.tmp, note=str(note)))
        self.assertIn("Reading note", (self.tmp / "pool" / "arxiv-2403.12550" / "note.md").read_text())

    def test_unavailable_extraction_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            make_pool(self.tmp).add(**add_kwargs(self.tmp, available=False))

    def test_textless_extraction_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            make_pool(self.tmp).add(**add_kwargs(self.tmp, text=""))

    def test_doi_fallback_naming(self) -> None:
        metadata = self.tmp / "meta.json"
        metadata.write_text(json.dumps({"doi": "10.1000/xyz", "title": "No-arXiv paper"}), encoding="utf-8")
        extraction = self.tmp / "ex.json"
        extraction.write_text(json.dumps({
            "paper_id": "", "available": True, "source_format": "html",
            "extraction_method": "html-latexml", "title": "No-arXiv paper",
            "text": "body", "quality": {"grade": "high", "text_chars": 900},
        }), encoding="utf-8")
        kwargs = add_kwargs(self.tmp)
        kwargs["extraction"] = load_json(extraction)   # empty paper_id -> DOI fallback
        kwargs["metadata"] = load_json(metadata)
        make_pool(self.tmp).add(**kwargs)
        self.assertTrue((self.tmp / "pool" / "doi-10.1000%2Fxyz" / "meta.json").is_file())


class ImportExistingTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_migrates_flat_md_files(self) -> None:
        root = self.tmp / "pool"
        root.mkdir()
        (root / "2403.12550.md").write_text("# RGBD GS-ICP SLAM\n\nbody", encoding="utf-8")
        (root / "not-a-paper.md").write_text("# keep me", encoding="utf-8")
        PaperPool(str(root)).import_existing()
        self.assertTrue((root / "arxiv-2403.12550" / "paper.md").is_file())
        self.assertFalse((root / "2403.12550.md").exists())
        self.assertTrue((root / "not-a-paper.md").exists())  # untouched
        meta = json.loads((root / "arxiv-2403.12550" / "meta.json").read_text())
        self.assertEqual(meta["title"], "RGBD GS-ICP SLAM")


class ListGetTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        make_pool(self.tmp).add(**add_kwargs(self.tmp))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_list_json_and_table(self) -> None:
        import contextlib
        import io as _io

        buffer = _io.StringIO()
        with contextlib.redirect_stdout(buffer):
            make_pool(self.tmp).list_papers(as_json=True)
        records = json.loads(buffer.getvalue())
        self.assertEqual(records[0]["arxiv_id"], "2403.12550")

    def test_get_by_arxiv_id(self) -> None:
        import contextlib
        import io as _io

        buffer = _io.StringIO()
        with contextlib.redirect_stdout(buffer):
            make_pool(self.tmp).get("2403.12550")
        meta = json.loads(buffer.getvalue())
        self.assertEqual(meta["dir_name"], "arxiv-2403.12550")

    def test_get_missing_paper_fails(self) -> None:
        with self.assertRaises(SystemExit):
            make_pool(self.tmp).get("9999.99999")


if __name__ == "__main__":
    unittest.main()

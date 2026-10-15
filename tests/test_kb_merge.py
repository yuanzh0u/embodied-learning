"""Tests for knowledge.merge (kb-merge)."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.merge import kb_merge
from embodied_learning.knowledge.model import KnowledgeBase

from test_kb_model import write_card, write_pool_paper, write_run


def _set_mtime(path: Path, ts: float) -> None:
    os.utime(path, (ts, ts))


class KbMergeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.target = self.root / "target"
        self.source = self.root / "source"
        self._build_target()
        self._build_source()

    def tearDown(self):
        self._tmp.cleanup()

    def _build_target(self):
        write_run(self.target, "run-shared", events=1, topic="Shared")
        _set_mtime(self.target / "evidence" / "run-shared" / "run.json", 1000.0)
        write_pool_paper(self.target, "arxiv-2401.1", full_text=True, deep_read=False,
                         added_at="2026-01-01T00:00:00")
        write_pool_paper(self.target, "arxiv-2402.2", full_text=True, deep_read=True,
                         added_at="2026-01-01T00:00:00")
        write_card(self.target, "card-target", card_id="EA-TARGET")
        catalog = self.target / "knowledge" / "literature-review-catalog.md"
        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(
            "| ID | topic | ids | scale | link |\n|---|---|---|---|---|\n"
            "| LR-SHARED | Shared | EA-S | — | [run](../evidence/run-shared/run.json) |\n",
            encoding="utf-8",
        )

    def _build_source(self):
        # newer run-shared (overwrites) + a brand-new run
        write_run(self.source, "run-shared", events=2, topic="Shared Updated")
        _set_mtime(self.source / "evidence" / "run-shared" / "run.json", 2000.0)
        write_run(self.source, "run-new", events=1, topic="New Topic")
        # pool: 1 older (skipped) + 1 newer (overwritten) + 1 brand-new
        write_pool_paper(self.source, "arxiv-2401.1", full_text=True, deep_read=True,
                         added_at="2025-01-01T00:00:00")  # older than target
        write_pool_paper(self.source, "arxiv-2402.2", full_text=True, deep_read=False,
                         added_at="2026-06-01T00:00:00")  # newer than target
        write_pool_paper(self.source, "arxiv-2403.3", full_text=True, deep_read=False,
                         added_at="2026-07-01T00:00:00")  # brand-new
        # cards: 1 new + 1 older duplicate
        write_card(self.source, "card-source-new", card_id="EA-SRC-NEW")
        write_card(self.source, "card-target", card_id="EA-TARGET")  # same file name
        _set_mtime(self.source / "knowledge" / "embodied-ai" / "card-target.md", 500.0)  # older
        # site-config with slugs
        (self.source / "wiki").mkdir(parents=True, exist_ok=True)
        (self.source / "wiki" / "site-config.json").write_text(
            json.dumps({
                "schema_version": 1,
                "site": {"title": "Test Wiki"},
                "fields": {"field_label": "领域"},
                "topics": {"shared": {"slug": "shared-slug", "aliases": []}},
            }),
            encoding="utf-8",
        )

    def test_new_run_copied_and_cataloged(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          rebuild_wiki=False)
        self.assertEqual(report["runs"]["copied"], 1)  # run-new
        self.assertEqual(report["runs"]["overwritten"], 1)  # run-shared
        self.assertEqual(report["catalog"]["rows_added"], 1)
        catalog = (self.target / "knowledge" / "literature-review-catalog.md").read_text(encoding="utf-8")
        self.assertIn("run-new", catalog)

    def test_source_newer_overwrites(self):
        kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)], rebuild_wiki=False)
        manifest = json.loads(
            (self.target / "evidence" / "run-shared" / "run.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["topic"], "Shared Updated")

    def test_target_newer_skipped(self):
        # make target's run-shared newer than source's
        _set_mtime(self.target / "evidence" / "run-shared" / "run.json", 3000.0)
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          rebuild_wiki=False)
        self.assertEqual(report["runs"]["overwritten"], 0)
        self.assertEqual(report["runs"]["skipped_target_newer"], 1)
        manifest = json.loads(
            (self.target / "evidence" / "run-shared" / "run.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["topic"], "Shared")  # unchanged

    def test_prefer_target_never_overwrites(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          prefer="target", rebuild_wiki=False)
        self.assertEqual(report["runs"]["overwritten"], 0)
        self.assertEqual(report["pool"]["overwritten"], 0)

    def test_prefer_source_always_overwrites(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          prefer="source", rebuild_wiki=False)
        self.assertEqual(report["pool"]["copied"], 1)  # 2403.3
        self.assertEqual(report["pool"]["overwritten"], 2)  # 2401.1 + 2402.2

    def test_pool_index_merged(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          rebuild_wiki=False)
        self.assertGreaterEqual(report["pool"]["index_merged"], 1)
        index = (self.target / "pool" / "index.jsonl").read_text(encoding="utf-8")
        self.assertIn("arxiv-2403.3", index)

    def test_cards_unrouted_reported(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          rebuild_wiki=False)
        self.assertEqual(report["cards"]["copied"], 1)  # card-source-new
        self.assertEqual(report["cards"]["overwritten"], 0)  # card-target is older
        self.assertIn("EA-SRC-NEW", report["cards"]["unrouted_ids"])

    def test_slugs_not_in_default_what(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          rebuild_wiki=False)
        self.assertEqual(report["slugs"]["added"], 0)

    def test_slugs_merged(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          what=frozenset({"runs", "pool", "cards", "slugs"}),
                          rebuild_wiki=False)
        self.assertGreaterEqual(report["slugs"]["added"], 1)
        cfg_path = self.target / "wiki" / "site-config.json"
        self.assertTrue(cfg_path.is_file())
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        self.assertIn("shared", cfg.get("topics", {}))

    def test_dry_run_no_side_effects(self):
        before_runs = sorted(p.name for p in (self.target / "evidence").iterdir())
        before_pool = sorted(p.name for p in (self.target / "pool").iterdir() if not p.name.startswith("."))
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          dry_run=True, rebuild_wiki=False)
        self.assertTrue(report["dry_run"])
        after_runs = sorted(p.name for p in (self.target / "evidence").iterdir())
        after_pool = sorted(p.name for p in (self.target / "pool").iterdir() if not p.name.startswith("."))
        self.assertEqual(before_runs, after_runs)
        self.assertEqual(before_pool, after_pool)

    def test_what_runs_only(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          what=frozenset({"runs"}), rebuild_wiki=False)
        self.assertEqual(report["pool"]["copied"], 0)
        self.assertEqual(report["cards"]["copied"], 0)
        self.assertEqual(report["slugs"]["added"], 0)
        self.assertEqual(report["runs"]["copied"] + report["runs"]["overwritten"], 2)

    def test_no_wiki_skips_rebuild(self):
        report = kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                          rebuild_wiki=False)
        self.assertFalse(report["wiki"]["rebuilt"])

    def test_invalid_prefer_raises(self):
        with self.assertRaises(ValueError):
            kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                     prefer="bogus", rebuild_wiki=False)

    def test_invalid_what_raises(self):
        with self.assertRaises(ValueError):
            kb_merge(KnowledgeBase.open(self.target), [KnowledgeBase.open(self.source)],
                     what=frozenset({"bogus"}), rebuild_wiki=False)


class KbMergeCliTest(unittest.TestCase):
    def test_cli_json_report(self):
        from tests._entry import invoke
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "src"
            dst = root / "dst"
            write_run(src, "run-x", events=1, topic="X")
            (dst / "knowledge").mkdir(parents=True, exist_ok=True)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = invoke("wiki.py", "kb-merge", [
                    "--kb-root", str(dst), "--source", str(src),
                    "--dry-run", "--no-wiki", "--json",
                ])
            self.assertEqual(code, 0)
            report = json.loads(buf.getvalue())
            self.assertEqual(report["runs"]["copied"], 1)

    def test_cli_requires_source(self):
        from tests._entry import parse
        with self.assertRaises(SystemExit):
            parse("wiki.py", "kb-merge", ["--kb-root", "/tmp"])


if __name__ == "__main__":
    unittest.main()

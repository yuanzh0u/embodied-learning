"""Tests for knowledge.inventory (kb-stats) and knowledge.query (kb-search)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.inventory import kb_stats
from embodied_learning.knowledge.model import KnowledgeBase
from embodied_learning.knowledge.query import kb_search

from test_kb_model import write_card, write_pool_paper, write_run


class KbStatsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        # 2 runs: one settled + one in-progress; one without evidence.jsonl
        write_run(self.root, "run-a", events=3, status="settled", review_mode="rapid", topic="Alpha")
        write_run(self.root, "run-b", events=0, status="in-progress", review_mode="scoping", topic="Beta")
        (self.root / "evidence" / "run-b" / "evidence.jsonl").unlink(missing_ok=True)
        # 3 pool papers: full+deep / full only / meta only (not in index)
        write_pool_paper(self.root, "arxiv-2401.1", full_text=True, deep_read=True)
        write_pool_paper(self.root, "arxiv-2402.2", full_text=True, deep_read=False)
        write_pool_paper(self.root, "arxiv-2403.3", full_text=False, deep_read=False, in_index=False)
        # hidden dir noise
        (self.root / "pool" / ".locks").mkdir(exist_ok=True)
        # catalog registers only run-a
        catalog = self.root / "knowledge" / "literature-review-catalog.md"
        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(
            "| ID | topic | ids | scale | link |\n|---|---|---|---|---|\n"
            "| LR-A | Alpha | EA-A | — | [run](../evidence/run-a/run.json) |\n",
            encoding="utf-8",
        )
        # minimal wiki snapshot with 1 topic
        snap = self.root / "wiki" / "data" / "snapshots" / "snap-1"
        (snap / "topics").mkdir(parents=True)
        (snap / "manifest.json").write_text(
            json.dumps({"snapshot_id": "snap-1", "stats": {"published_topics": 1, "superseded_versions": 0}}),
            encoding="utf-8",
        )
        (snap / "topics" / "topic-abc.json").write_text(
            json.dumps({"id": "topic-abc", "topic_key": "tk", "title": "Alpha", "field": "AI",
                        "date": "2026-01-01", "excerpt": "ex", "default_version": "keyan", "versions": {}}),
            encoding="utf-8",
        )
        (self.root / "wiki" / "data" / "current.json").write_text(
            json.dumps({"snapshot_id": "snap-1", "base_path": "snapshots/snap-1"}), encoding="utf-8",
        )
        self.kb = KnowledgeBase.open(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_run_counts_by_status_and_mode(self):
        payload = kb_stats(self.kb)
        self.assertEqual(payload["runs"]["total"], 2)
        self.assertEqual(payload["runs"]["by_status"], {"settled": 1, "in-progress": 1})
        self.assertEqual(payload["runs"]["by_review_mode"], {"rapid": 1, "scoping": 1})

    def test_event_count_tolerates_missing_evidence(self):
        payload = kb_stats(self.kb)
        self.assertEqual(payload["runs"]["total_events"], 3)  # run-b has 0

    def test_registered_vs_unregistered(self):
        payload = kb_stats(self.kb)
        self.assertEqual(payload["runs"]["registered_in_catalog"], 1)
        self.assertEqual(payload["runs"]["unregistered"], 1)

    def test_pool_counts(self):
        payload = kb_stats(self.kb)
        self.assertEqual(payload["pool"]["papers"], 3)
        self.assertEqual(payload["pool"]["full_text"], 2)
        self.assertEqual(payload["pool"]["deep_read"], 1)
        self.assertEqual(payload["pool"]["full_text_and_deep_read"], 1)
        self.assertEqual(payload["pool"]["deep_read_without_full_text"], 0)
        self.assertIn("arxiv-2403.3", payload["pool"]["not_in_index"])
        self.assertEqual(payload["pool"]["in_index"], 2)

    def test_wiki_topic_count(self):
        payload = kb_stats(self.kb)
        self.assertEqual(payload["wiki"]["published_topics"], 1)

    def test_runs_detail_only_when_requested(self):
        self.assertNotIn("runs_detail", kb_stats(self.kb))
        detail = kb_stats(self.kb, include_runs=True)
        self.assertIn("runs_detail", detail)
        self.assertEqual(len(detail["runs_detail"]), 2)

    def test_empty_kb_returns_zeroes(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = KnowledgeBase.open(tmp)
            payload = kb_stats(empty)
            self.assertEqual(payload["runs"]["total"], 0)
            self.assertEqual(payload["pool"]["papers"], 0)

    def test_skip_hidden_pool_dirs(self):
        payload = kb_stats(self.kb)
        # .locks is not counted as a paper
        self.assertEqual(payload["pool"]["papers"], 3)


class KbSearchTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        write_run(self.root, "run-calib", events=2, topic="外参标定 Methods")
        # second event with legacy "id" key
        run_dir = self.root / "evidence" / "run-calib"
        lines = (run_dir / "evidence.jsonl").read_text(encoding="utf-8").splitlines()
        lines.append(json.dumps({"id": "EA-LEGACY-0001", "claim": "legacy id event",
                                 "paper": {"arxiv_id": "2499.1", "title": "Legacy Paper"}}))
        (run_dir / "evidence.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        write_pool_paper(self.root, "arxiv-2401.1", full_text=True, deep_read=True)
        write_card(self.root, "card-calib", card_id="EA-CALIB")
        self.kb = KnowledgeBase.open(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_run_hit(self):
        hits = kb_search(self.kb, "外参标定", scope="runs")
        self.assertTrue(any(h["id"] == "run-calib" for h in hits))

    def test_run_miss(self):
        self.assertEqual(kb_search(self.kb, "nonexistent-term", scope="runs"), [])

    def test_multi_term_and(self):
        self.assertTrue(kb_search(self.kb, "外参 标定", scope="runs"))
        self.assertFalse(kb_search(self.kb, "外参 nonexistent", scope="runs"))

    def test_case_insensitive(self):
        self.assertTrue(kb_search(self.kb, "CALIB", scope="runs"))
        self.assertTrue(kb_search(self.kb, "calib", scope="runs"))

    def test_event_hit_with_legacy_id(self):
        hits = kb_search(self.kb, "legacy", scope="events")
        self.assertTrue(any(h["id"] == "EA-LEGACY-0001" for h in hits))

    def test_paper_hit(self):
        hits = kb_search(self.kb, "2401", scope="papers")
        self.assertTrue(len(hits) >= 1)

    def test_scope_filter(self):
        self.assertEqual(kb_search(self.kb, "calib", scope="papers"), [])
        self.assertTrue(kb_search(self.kb, "calib", scope="runs"))

    def test_all_scope_hits_multiple(self):
        hits = kb_search(self.kb, "calib", scope="all")
        scopes = {h["scope"] for h in hits}
        self.assertIn("runs", scopes)

    def test_limit_per_scope(self):
        # 2 events in run-calib; limit=1 should return at most 1 per scope
        hits = kb_search(self.kb, "claim", scope="events", limit=1)
        self.assertLessEqual(len(hits), 1)

    def test_empty_query_returns_empty(self):
        self.assertEqual(kb_search(self.kb, "", scope="all"), [])
        self.assertEqual(kb_search(self.kb, "   ", scope="all"), [])


class KbInventoryCliTest(unittest.TestCase):
    """CLI-level smoke tests through the wiki.py dispatcher."""

    def test_kb_stats_json(self):
        from tests._entry import invoke
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_run(root, "run-a", events=1)
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = invoke("wiki.py", "kb-stats", ["--kb-root", str(root), "--json"])
            self.assertEqual(code, 0)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["runs"]["total"], 1)

    def test_kb_search_json(self):
        from tests._entry import invoke
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_run(root, "run-a", events=1, topic="HelloWorld")
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = invoke("wiki.py", "kb-search", ["HelloWorld", "--kb-root", str(root), "--json"])
            self.assertEqual(code, 0)
            hits = json.loads(buf.getvalue())
            self.assertTrue(any(h["id"] == "run-a" for h in hits))

    def test_kb_stats_parse_defaults(self):
        from tests._entry import parse
        args = parse("wiki.py", "kb-stats", [])
        self.assertFalse(args.json)
        self.assertFalse(args.runs_detail)

    def test_kb_search_parse_defaults(self):
        from tests._entry import parse
        args = parse("wiki.py", "kb-search", ["q"])
        self.assertEqual(args.scope, "all")
        self.assertEqual(args.limit, 20)


if __name__ == "__main__":
    unittest.main()

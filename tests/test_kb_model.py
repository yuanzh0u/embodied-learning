"""Tests for embodied_learning.knowledge.model — domain types + aggregates."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.model import (
    Catalog,
    CatalogEntry,
    Deliverable,
    EvidenceEvent,
    KnowledgeBase,
    PoolPaper,
    ReviewRun,
    RunManifest,
    TopicCard,
    WikiTopic,
)


def write_run(root: Path, name: str, *, events: int = 1, status: str = "settled",
              review_mode: str = "rapid", topic: str = "") -> Path:
    run_dir = root / "evidence" / name
    run_dir.mkdir(parents=True, exist_ok=True)
    if events:
        lines = [
            json.dumps({"event_id": f"EA-TEST-{i:04d}", "claim": f"claim-{i}",
                        "stance": "support", "confidence": "direct",
                        "paper": {"arxiv_id": f"2401.{i:05d}", "title": f"Paper {i}"}})
            for i in range(events)
        ]
        (run_dir / "evidence.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest = {
        "run": name, "topic": topic or name, "status": status,
        "review_mode": review_mode, "event_count": events,
        "evidence_papers": events, "candidate_count": events * 2,
        "full_text_count": events,
    }
    (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")
    for fname in ("scientific-memo_keyan.md", "zhihu-explainer_zhihu.md",
                  "xiaohongshu-post_xiaohongshu.md"):
        (run_dir / fname).write_text(f"# {name} {fname}\n", encoding="utf-8")
    return run_dir


def write_pool_paper(root: Path, dir_name: str, *, full_text: bool = True,
                     deep_read: bool = False, added_at: str = "2026-01-01T00:00:00",
                     in_index: bool = True) -> Path:
    paper_dir = root / "pool" / dir_name
    paper_dir.mkdir(parents=True, exist_ok=True)
    meta = {"arxiv_id": dir_name.removeprefix("arxiv-"), "title": f"Paper {dir_name}",
            "added_at": added_at, "quality": "high"}
    (paper_dir / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    if full_text:
        (paper_dir / "paper.md").write_text("full text\n", encoding="utf-8")
    if deep_read:
        (paper_dir / "note.json").write_text("{}", encoding="utf-8")
    if in_index:
        index = root / "pool" / "index.jsonl"
        lines = index.read_text(encoding="utf-8").splitlines() if index.is_file() else []
        lines.append(json.dumps({"dir_name": dir_name, **meta}))
        index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return paper_dir


def write_card(root: Path, name: str, *, card_id: str = "") -> Path:
    folder = root / "knowledge" / "embodied-ai"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.md"
    path.write_text(
        f"---\nid: {card_id or name}\ntitle: {name} title\ntags: [ai, robotics]\n"
        f"load_when: always\nsource: test\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    return path


class RunManifestTest(unittest.TestCase):
    def test_parses_all_fields(self):
        m = RunManifest.from_json({
            "run": "r1", "topic": "T", "status": "settled", "review_mode": "systematic",
            "time_range": "2023-2026", "knowledge_ids": ["EA-A", "EA-B"],
            "event_count": 5, "candidate_count": 10, "full_text_count": 7,
            "evidence_papers": 6, "style": "survey", "notes": "n",
        }, run_name="fallback")
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m.run_name, "r1")
        self.assertEqual(m.knowledge_ids, ("EA-A", "EA-B"))
        self.assertEqual(m.event_count, 5)
        self.assertEqual(m.style, "survey")

    def test_missing_fields_tolerated(self):
        m = RunManifest.from_json({"run": "r2"}, run_name="fallback")
        self.assertIsNotNone(m)
        assert m is not None
        self.assertEqual(m.topic, "fallback")  # falls back to run_name
        self.assertEqual(m.status, "")
        self.assertEqual(m.event_count, 0)
        self.assertIsNone(m.candidate_count)
        self.assertIsNone(m.evidence_papers)
        self.assertIsNone(m.style)

    def test_non_dict_returns_none(self):
        self.assertIsNone(RunManifest.from_json(None, run_name="x"))
        self.assertIsNone(RunManifest.from_json([1, 2], run_name="x"))


class EvidenceEventTest(unittest.TestCase):
    def test_event_id_key(self):
        e = EvidenceEvent.from_record({
            "event_id": "EA-001", "claim": "c", "stance": "support",
            "confidence": "direct", "paper": {"arxiv_id": "2401.1", "title": "P"},
        }, run_name="r")
        self.assertEqual(e.event_id, "EA-001")
        self.assertEqual(e.paper_id, "2401.1")

    def test_legacy_id_key(self):
        e = EvidenceEvent.from_record({
            "id": "EA-002", "claim": "c2", "paper_id": "2402.2",
        }, run_name="r")
        self.assertEqual(e.event_id, "EA-002")
        self.assertEqual(e.paper_id, "2402.2")

    def test_event_id_wins_over_legacy(self):
        e = EvidenceEvent.from_record({"event_id": "EA-A", "id": "EA-B"}, run_name="r")
        self.assertEqual(e.event_id, "EA-A")


class PoolPaperTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "pool").mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_flags(self):
        write_pool_paper(self.root, "arxiv-2401.1", full_text=True, deep_read=True)
        write_pool_paper(self.root, "arxiv-2402.2", full_text=True, deep_read=False)
        write_pool_paper(self.root, "arxiv-2403.3", full_text=False, deep_read=False, in_index=False)
        kb = KnowledgeBase.open(self.root)
        papers = {p.dir_name: p for p in kb.papers()}
        self.assertTrue(papers["arxiv-2401.1"].has_full_text)
        self.assertTrue(papers["arxiv-2401.1"].has_deep_read)
        self.assertTrue(papers["arxiv-2401.1"].in_index)
        self.assertTrue(papers["arxiv-2402.2"].has_full_text)
        self.assertFalse(papers["arxiv-2402.2"].has_deep_read)
        self.assertFalse(papers["arxiv-2403.3"].has_full_text)
        self.assertFalse(papers["arxiv-2403.3"].in_index)

    def test_hidden_dirs_skipped(self):
        (self.root / "pool" / ".locks").mkdir(exist_ok=True)
        write_pool_paper(self.root, "arxiv-2401.1")
        kb = KnowledgeBase.open(self.root)
        names = {p.dir_name for p in kb.papers()}
        self.assertNotIn(".locks", names)
        self.assertIn("arxiv-2401.1", names)


class ReviewRunTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_events_and_deliverables(self):
        run_dir = write_run(self.root, "run-a", events=3)
        run = ReviewRun.open(run_dir / "run.json")
        self.assertIsNotNone(run)
        assert run is not None
        self.assertEqual(len(run.events()), 3)
        styles = {d.style for d in run.deliverables()}
        self.assertIn("scientific-memo", styles)
        self.assertIn("expert-explainer", styles)
        self.assertIn("kol-thread", styles)

    def test_revisions_included(self):
        run_dir = write_run(self.root, "run-a", events=1)
        rev = run_dir / "revisions"
        rev.mkdir()
        (rev / "keyan-v2.md").write_text("# rev2\n", encoding="utf-8")
        run = ReviewRun.open(run_dir / "run.json")
        assert run is not None
        styles = {d.style: d for d in run.deliverables()}
        self.assertIn("keyan-v2", styles)
        self.assertEqual(styles["keyan-v2"].revision, 2)
        self.assertEqual(styles["keyan-v2"].based_on, "keyan")

    def test_events_tolerates_missing_evidence(self):
        run_dir = write_run(self.root, "run-a", events=0)
        (run_dir / "evidence.jsonl").unlink(missing_ok=True)
        run = ReviewRun.open(run_dir / "run.json")
        assert run is not None
        self.assertEqual(run.events(), [])


class CatalogTest(unittest.TestCase):
    def test_parses_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog_path = root / "knowledge" / "literature-review-catalog.md"
            catalog_path.parent.mkdir(parents=True)
            catalog_path.write_text(
                "# 成果索引\n\n"
                "| ID | topic | ids | scale | link |\n"
                "|---|---|---|---|---|\n"
                "| LR-A | Topic A | EA-A | — | [run](../evidence/run-a/run.json) |\n"
                "| LR-B | Topic B | EA-B | — | [run](../evidence/run-b/run.json) |\n"
                "| LR-C | No link | — | — | — |\n",
                encoding="utf-8",
            )
            cat = Catalog(catalog_path)
            names = cat.run_names()
            self.assertEqual(names, {"run-a", "run-b"})


class KnowledgeBaseTest(unittest.TestCase):
    def test_open_empty_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            kb = KnowledgeBase.open(tmp)
            self.assertEqual(kb.runs(), [])
            self.assertEqual(kb.papers(), [])
            self.assertEqual(kb.wiki_topics(), [])
            self.assertEqual(list(kb.iter_events()), [])

    def test_runs_collected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_run(root, "run-a", events=2)
            write_run(root, "run-b", events=1, status="in-progress")
            kb = KnowledgeBase.open(root)
            names = {r.name for r in kb.runs()}
            self.assertEqual(names, {"run-a", "run-b"})

    def test_iter_events_across_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_run(root, "run-a", events=2)
            write_run(root, "run-b", events=3)
            kb = KnowledgeBase.open(root)
            events = list(kb.iter_events())
            self.assertEqual(len(events), 5)

    def test_wiki_topics_reads_current_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snap = root / "wiki" / "data" / "snapshots" / "snap-1"
            (snap / "topics").mkdir(parents=True)
            (snap / "manifest.json").write_text(
                json.dumps({"snapshot_id": "snap-1", "stats": {"published_topics": 1}}),
                encoding="utf-8",
            )
            (snap / "topics" / "topic-abc.json").write_text(
                json.dumps({
                    "id": "topic-abc", "topic_key": "tk", "title": "T", "field": "f",
                    "date": "2026-01-01", "excerpt": "ex", "default_version": "keyan",
                    "versions": {"keyan": {"label": "科研", "article_title": "T",
                                           "source_file": "x.md", "characters": 100}},
                }),
                encoding="utf-8",
            )
            (root / "wiki" / "data" / "current.json").write_text(
                json.dumps({"snapshot_id": "snap-1", "base_path": "snapshots/snap-1"}),
                encoding="utf-8",
            )
            kb = KnowledgeBase.open(root)
            topics = kb.wiki_topics()
            self.assertEqual(len(topics), 1)
            self.assertEqual(topics[0].title, "T")
            self.assertIn("keyan", topics[0].versions)

    def test_cards_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_card(root, "card-1", card_id="EA-CARD-1")
            kb = KnowledgeBase.open(root)
            cards = kb.cards()
            self.assertEqual(len(cards), 1)
            self.assertEqual(cards[0].card_id, "EA-CARD-1")
            self.assertIn("ai", cards[0].tags)


if __name__ == "__main__":
    unittest.main()

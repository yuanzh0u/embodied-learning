"""Tests for scripts/migrate_pool.py — work/ artifacts → shared pool."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MIGRATE_PATH = REPO_ROOT / "scripts" / "migrate_pool.py"


def load_module():
    spec = importlib.util.spec_from_file_location("migrate_pool", MIGRATE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class MigratePoolTest(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb = Path(self.tmp.name)
        self.work = self.kb / "work"
        run = self.work / "literature-review-demo-20260101"
        (run / "reading-packets").mkdir(parents=True)
        (run / "extractions").mkdir()
        (run / "paper-notes").mkdir()
        (self.work / "reader-cache").mkdir()
        self.run_dir = run

    def write(self, rel: str, payload: str) -> Path:
        path = self.kb / "work" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        return path

    def extraction(self, pid: str, title: str = "T") -> str:
        return json.dumps({
            "paper_id": pid, "title": title, "available": True,
            "text": f"# {title}\nfull text", "extraction_method": "html-latexml",
            "source_format": "html", "quality": {"grade": "high", "text_chars": 100},
        }, ensure_ascii=False)

    def test_collect_maps_artifacts_by_id(self):
        self.write("literature-review-demo-20260101/reading-packets/2401.00001.md", "# packet")
        self.write("literature-review-demo-20260101/extractions/2401.00001.json", self.extraction("2401.00001"))
        note = {"evidence_cards": [{"card_id": "c1"}]}
        self.write("literature-review-demo-20260101/paper-notes/2401.00001.json", json.dumps(note))
        self.write("literature-review-demo-20260101/paper-notes/2401.00001.audit.json", '{"status": "pass"}')
        self.write("reader-cache/2401.00001.html", "<article>cleaned</article>")

        papers = self.mod.collect(self.work)
        entry = papers.get("2401.00001")
        self.assertIsNotNone(entry)
        for kind in ("paper_md", "extraction", "note", "audit", "html"):
            self.assertIn(kind, entry)

    def test_migrate_writes_pool_layout_and_index(self):
        self.write("literature-review-demo-20260101/extractions/2401.00002.json", self.extraction("2401.00002"))
        self.write("literature-review-demo-20260101/reading-packets/2401.00002.md", "# packet 2")
        note = {"evidence_cards": [{"card_id": "c1"}]}
        self.write("literature-review-demo-20260101/paper-notes/2401.00002.json", json.dumps(note))
        self.write("literature-review-demo-20260101/paper-notes/2401.00002.audit.json", '{"status": "pass"}')

        pool = self.kb / "pool"
        pool.mkdir()
        added, refreshed = self.mod.migrate(self.mod.collect(self.work), pool, force=False)
        self.assertEqual((added, refreshed), (1, 0))
        entry = pool / "arxiv-2401.00002"
        self.assertTrue((entry / "paper.md").is_file())
        self.assertTrue((entry / "extraction.json").is_file())
        self.assertTrue((entry / "note.json").is_file())
        self.assertTrue((entry / "note.json.audit.json").is_file())
        meta = json.loads((entry / "meta.json").read_text(encoding="utf-8"))
        self.assertTrue(meta["deep_read"])
        self.assertEqual(meta["audit_status"], "pass")
        index = [json.loads(line) for line in (pool / "index.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([record["dir_name"] for record in index], ["arxiv-2401.00002"])

    def test_template_shell_note_not_archived(self):
        # A note without evidence_cards is a template shell — skip it.
        self.write("literature-review-demo-20260101/extractions/2401.00003.json", self.extraction("2401.00003"))
        self.write("literature-review-demo-20260101/paper-notes/2401.00003.json", '{"evidence_cards": []}')
        pool = self.kb / "pool"
        pool.mkdir()
        self.mod.migrate(self.mod.collect(self.work), pool, force=False)
        entry = pool / "arxiv-2401.00003"
        self.assertTrue((entry / "paper.md").is_file())
        self.assertFalse((entry / "note.json").is_file())

    def test_second_run_newest_wins(self):
        import time
        self.write("literature-review-a-20260101/reading-packets/2401.00004.md", "# old")
        time.sleep(0.01)
        newer = self.write("literature-review-b-20260101/reading-packets/2401.00004.md", "# newer")
        os.utime(newer, (time.time() + 10, time.time() + 10))
        papers = self.mod.collect(self.work)
        self.assertIn("newer", papers["2401.00004"]["paper_md"].read_text(encoding="utf-8"))

    def test_dry_run_touches_nothing(self):
        self.write("literature-review-demo-20260101/extractions/2401.00005.json", self.extraction("2401.00005"))
        code = self.mod.main(["--kb-root", str(self.kb), "--dry-run"])
        self.assertEqual(code, 0)
        self.assertFalse((self.kb / "pool").exists())


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SNAPSHOT_PATH = Path(__file__).resolve().parents[3] / "embodied_learning" / "search" / "arxiv_snapshot.py"
DB_PATH = Path(__file__).resolve().parents[3] / "embodied_learning" / "search" / "arxiv_snapshot_db.py"
SNAP_SPEC = importlib.util.spec_from_file_location("snapshot_for_db_test", SNAPSHOT_PATH)
snap = importlib.util.module_from_spec(SNAP_SPEC)
assert SNAP_SPEC and SNAP_SPEC.loader
SNAP_SPEC.loader.exec_module(snap)
SPEC = importlib.util.spec_from_file_location("search_arxiv_snapshot_db", DB_PATH)
db_mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(db_mod)


RECORDS = [
    {
        "id": "2311.18259",
        "title": "Ego-Exo4D: Understanding Skilled Human Activity",
        "abstract": "A large egocentric and exocentric dataset with expert commentary.",
        "authors": "Kristen Grauman, Andrew Westbury",
        "categories": "cs.CV",
        "versions": [{"version": "v1", "created": "Mon, 27 Nov 2023 18:00:00 GMT"}],
        "update_date": "2024-01-02",
        "comments": "CVPR 2024",
        "journal-ref": "",
    },
    {
        "id": "1804.02748",
        "title": "Scaling Egocentric Vision: The EPIC-KITCHENS Dataset",
        "abstract": "Egocentric cooking videos with annotations.",
        "authors": "Dima Damen",
        "categories": "cs.CV",
        "versions": [{"version": "v1", "created": "Sun, 8 Apr 2018 12:00:00 GMT"}],
        "update_date": "2019-01-01",
        "comments": "",
        "journal-ref": "IJCV",
    },
    {
        "id": "2000.99999",
        "title": "Old Egocentric Work",
        "abstract": "egocentric driving before the window",
        "authors": "A. Old",
        "categories": "cs.CV",
        "versions": [{"version": "v1", "created": "Mon, 1 May 2000 12:00:00 GMT"}],
        "update_date": "2001-01-01",
        "comments": "",
        "journal-ref": "",
    },
]


def build_test_db() -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        for record in RECORDS:
            handle.write(json.dumps(record) + "\n")
        jsonl = handle.name
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as handle:
        db = handle.name
    Path(db).unlink()  # build_db refuses to overwrite; start clean
    code = db_mod.build_db(jsonl, db, progress_every=10**9)
    assert code == 0
    return db


def run_query(db: str, query: str, **overrides) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        output = handle.name
    search = db_mod.SnapshotDbSearch(
        db_path=db, start_date="2016-09-17", end_date="2026-09-17", output=output, **overrides
    )
    code = search.run([{"label": "q1", "query": query}])
    assert code == 0
    with open(output) as handle:
        return json.load(handle)


class BuildDbTest(unittest.TestCase):
    def test_rejects_existing_db(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as handle:
            db = handle.name
        with self.assertRaises(SystemExit):
            db_mod.build_db(RECORDS and db and db, db)  # type: ignore[arg-type]

    def test_schema_and_rowcount(self) -> None:
        db = build_test_db()
        import sqlite3
        connection = sqlite3.connect(db)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM papers").fetchone()[0], 3)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM fts").fetchone()[0], 3)
        v1 = connection.execute(
            "SELECT v1_date FROM papers WHERE id='2311.18259'"
        ).fetchone()[0]
        import datetime as dt
        stamp = dt.datetime.fromtimestamp(v1, tz=dt.timezone.utc)
        self.assertEqual(stamp.strftime("%Y-%m-%d"), "2023-11-27")


class MatchExprTest(unittest.TestCase):
    def test_term_prefix(self) -> None:
        node = db_mod.parse_query("all:ego")
        self.assertEqual(db_mod.match_expr(node), "all_ : ego*")

    def test_phrase(self) -> None:
        node = db_mod.parse_query('ti:"Ego-Exo4D"')
        self.assertEqual(db_mod.match_expr(node), 'ti : "ego exo4d"')

    def test_andnot(self) -> None:
        node = db_mod.parse_query("all:ego ANDNOT ti:driving")
        self.assertEqual(db_mod.match_expr(node), "all_ : ego* ANDNOT ti : driving*")

    def test_date_range_extracted(self) -> None:
        node = db_mod.parse_query("submittedDate:[202001010000 TO 202312312359]")
        sql, lo, hi = db_mod._split_date_range(node)
        self.assertEqual(sql, "")
        self.assertTrue(lo.startswith("2020-01-01"))
        self.assertTrue(hi.startswith("2023-12-31"))


class SnapshotDbSearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.db = build_test_db()

    def test_finds_seed_excludes_out_of_window(self) -> None:
        result = run_query(self.db, "all:egocentric")
        ids = {p["arxiv_id"] for p in result["papers"]}
        self.assertEqual(ids, {"2311.18259", "1804.02748"})

    def test_phrase_with_hyphen(self) -> None:
        result = run_query(self.db, 'ti:"Ego-Exo4D"')
        self.assertEqual(result["paper_count"], 1)
        self.assertEqual(result["papers"][0]["arxiv_id"], "2311.18259")

    def test_published_from_v1(self) -> None:
        result = run_query(self.db, "all:epic")
        self.assertTrue(result["papers"][0]["published"].startswith("2018-04-08"))

    def test_order_newest_first(self) -> None:
        result = run_query(self.db, "all:egocentric")
        published = [p["published"] for p in result["papers"]]
        self.assertEqual(published, sorted(published, reverse=True))

    def test_batch_shape(self) -> None:
        result = run_query(self.db, "all:ego")
        self.assertTrue(result["api"].startswith("sqlite:"))
        self.assertEqual(result["snapshot_backend"], "sqlite-fts5")
        for key in ("generated_at", "batch", "queries", "paper_count", "papers"):
            self.assertIn(key, result)


if __name__ == "__main__":
    unittest.main()

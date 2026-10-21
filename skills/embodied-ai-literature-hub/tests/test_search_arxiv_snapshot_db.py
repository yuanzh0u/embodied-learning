#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
# arxiv_snapshot_db imports embodied_learning.search.arxiv_snapshot as a real
# package import — put the repo root first so it does not resolve to a stale
# installed wheel (2026-10-16: the wheel lacked select_balanced_by_year).
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SNAPSHOT_PATH = REPO_ROOT / "embodied_learning" / "search" / "arxiv_snapshot.py"
DB_PATH = REPO_ROOT / "embodied_learning" / "search" / "arxiv_snapshot_db.py"
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


def build_test_db(records: list[dict] | None = None) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        for record in RECORDS if records is None else records:
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


ALL_COLUMNS = "{title abstract authors comments journal_ref categories}"


class MatchExprTest(unittest.TestCase):
    def test_term_prefix(self) -> None:
        node = db_mod.parse_query("all:ego")
        self.assertEqual(db_mod.match_expr(node), f"{ALL_COLUMNS} : ego*")

    def test_phrase(self) -> None:
        node = db_mod.parse_query('ti:"Ego-Exo4D"')
        self.assertEqual(db_mod.match_expr(node), 'title : "ego exo4d"')

    def test_andnot(self) -> None:
        node = db_mod.parse_query("all:ego ANDNOT ti:driving")
        self.assertEqual(
            db_mod.match_expr(node), f"{ALL_COLUMNS} : ego* ANDNOT title : driving*"
        )

    def test_date_range_extracted(self) -> None:
        node = db_mod.parse_query("submittedDate:[202001010000 TO 202312312359]")
        sql, lo, hi = db_mod._split_date_range(node)
        self.assertEqual(sql, "")
        self.assertTrue(lo.startswith("2020-01-01"))
        self.assertTrue(hi.startswith("2023-12-31"))

    def test_and_keeps_both_fts_conjuncts(self) -> None:
        # Regression: `left_sql or right_sql` silently dropped the second
        # conjunct, so `A AND B AND submittedDate:[...]` searched only A.
        node = db_mod.parse_query(
            'all:"object pose" AND all:"CAD model" AND submittedDate:[202001010000 TO 202312312359]'
        )
        sql, lo, hi = db_mod._split_date_range(node)
        self.assertEqual(
            sql,
            f'{ALL_COLUMNS} : "object pose" AND {ALL_COLUMNS} : "cad model"',
        )
        self.assertTrue(lo.startswith("2020-01-01"))


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

    def test_order_relevance_first(self) -> None:
        """Default sort is relevance (bm25), not newest-first. The EPIC-KITCHENS
        title/abstract hits 'egocentric' more densely than the Ego-Exo4D record."""
        result = run_query(self.db, "all:egocentric")
        ids = [p["arxiv_id"] for p in result["papers"]]
        self.assertEqual(result["sort_by"], "relevance")
        self.assertEqual(len(ids), 2)
        # Both match; the denser one (EPIC-KITCHENS: 'Egocentric' in title AND
        # abstract) must not be displaced by the newer paper's date.
        self.assertIn("1804.02748", ids)
        self.assertIn("2311.18259", ids)

    def test_date_sort_when_requested(self) -> None:
        result = run_query(self.db, "all:egocentric", sort_by="submittedDate")
        published = [p["published"] for p in result["papers"]]
        self.assertEqual(published, sorted(published, reverse=True))

    def test_relevance_cut_drops_marginal_matches(self) -> None:
        """Top-``max_results`` is by bm25, so a dense match survives while a
        marginal (but newer) one is cut — not the other way round."""
        records = [
            {
                "id": "2601.0001", "title": "A general robotics paper",
                "abstract": "machines and control theory " * 8,
                "authors": "A. Author", "categories": "cs.RO",
                "versions": [{"version": "v1", "created": "Fri, 1 Jan 2026 10:00:00 GMT"}],
                "update_date": "2026-02-01", "comments": "", "journal-ref": "",
            },
            {
                "id": "1804.0001", "title": "Egocentric video benchmark",
                "abstract": "egocentric video benchmark egocentric video " * 3,
                "authors": "A. Author", "categories": "cs.CV",
                "versions": [{"version": "v1", "created": "Sun, 8 Apr 2018 12:00:00 GMT"}],
                "update_date": "2018-05-01", "comments": "", "journal-ref": "",
            },
            {
                "id": "2301.0001", "title": "Egocentric vision",
                "abstract": "egocentric",
                "authors": "A. Author", "categories": "cs.CV",
                "versions": [{"version": "v1", "created": "Sun, 1 Jan 2023 12:00:00 GMT"}],
                "update_date": "2023-02-01", "comments": "", "journal-ref": "",
            },
        ]
        db = build_test_db(records)
        # Both 1804.0001 (dense title+abstract) and 2301.0001 (title-only) match
        # `egocentric`; the 2026 general paper does not. max_results=1 must keep
        # the densest and cut the marginal one — and report the cut.
        result = run_query(db, "all:egocentric", max_results=1)
        self.assertEqual([p["arxiv_id"] for p in result["papers"]], ["1804.0001"])
        meta = result["queries"][0]
        self.assertTrue(meta["capped"])
        self.assertGreaterEqual(meta["matched"], 2)

    def test_batch_shape(self) -> None:
        result = run_query(self.db, "all:ego")
        self.assertTrue(result["api"].startswith("sqlite:"))
        self.assertEqual(result["snapshot_backend"], "sqlite-fts5")
        for key in ("generated_at", "batch", "queries", "paper_count", "papers"):
            self.assertIn(key, result)

    def test_external_content_stores_text_once(self) -> None:
        import sqlite3
        connection = sqlite3.connect(self.db)
        ddl = connection.execute(
            "SELECT sql FROM sqlite_master WHERE name='fts'"
        ).fetchone()[0]
        self.assertIn("content='papers'", ddl)
        self.assertNotIn("CREATE TABLE fts_content", ddl)
        connection.close()

    def test_parallel_queries_merge_labels(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            output = handle.name
        search = db_mod.SnapshotDbSearch(
            db_path=self.db, start_date="2016-09-17", end_date="2026-09-17", output=output
        )
        code = search.run([
            {"label": "a", "query": "all:egocentric"},
            {"label": "b", "query": "abs:dataset"},
        ])
        self.assertEqual(code, 0)
        with open(output) as handle:
            result = json.load(handle)
        by_id = {p["arxiv_id"]: p for p in result["papers"]}
        self.assertIn("2311.18259", by_id)
        self.assertIn("a,b", by_id["2311.18259"]["query_label"])
        self.assertEqual([q["label"] for q in result["queries"]], ["a", "b"])

    def test_two_phase_matches_single_sql_plan(self) -> None:
        """The two-phase plan (FTS docids + date table + top-row fetch) must
        return the same ids in the same order as the single-SQL plan."""
        import sqlite3

        queries = [
            "all:egocentric",
            'all:"egocentric driving" AND all:dataset',
            "all:ego ANDNOT ti:old",
            "all:expert",
        ]
        for query in queries:
            from embodied_learning.search.arxiv import with_date_filter  # type: ignore[attr-defined]
            effective = with_date_filter(query, "2016-09-17", "2026-09-17")
            sql_expr, lo_iso, hi_iso = db_mod._split_date_range(db_mod.parse_query(effective))
            low = db_mod.dt.datetime.fromisoformat(lo_iso).timestamp()
            high = db_mod.dt.datetime.fromisoformat(hi_iso).timestamp()
            connection = sqlite3.connect(self.db)
            reference = [
                row[0]
                for row in connection.execute(
                    "SELECT p.id FROM papers p JOIN fts f ON f.rowid = p.rowid_alias"
                    " WHERE fts MATCH ? AND p.v1_date >= ? AND p.v1_date <= ?"
                    " ORDER BY bm25(fts) ASC, p.v1_date DESC, p.id",
                    (sql_expr, int(low), int(high)),
                ).fetchall()
            ]
            connection.close()
            result = run_query(self.db, query)
            self.assertEqual(
                [p["arxiv_id"] for p in result["papers"]],
                reference,
                msg=f"plan mismatch for {query!r}",
            )

    def test_rejects_pre_external_content_schema(self) -> None:
        import sqlite3
        with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as handle:
            db = handle.name
        connection = sqlite3.connect(db)
        connection.executescript(
            "CREATE VIRTUAL TABLE fts USING fts5(all_, ti, id UNINDEXED);"
        )
        connection.close()
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            output = handle.name
        search = db_mod.SnapshotDbSearch(
            db_path=db, start_date="2016-09-17", end_date="2026-09-17", output=output
        )
        with self.assertRaises(SystemExit):
            search.run([{"label": "q1", "query": "all:ego"}])


if __name__ == "__main__":
    unittest.main()

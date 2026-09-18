#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "embodied_learning" / "search" / "arxiv_snapshot.py"
SPEC = importlib.util.spec_from_file_location("search_arxiv_snapshot", SCRIPT_PATH)
snap = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(snap)


def make_record(
    arxiv_id: str = "2311.18259",
    title: str = "Ego-Exo4D",
    abstract: str = "A dataset of egocentric and exocentric videos.",
    authors: str = "A. Author, B. Author",
    categories: str = "cs.CV",
    v1_created: str = "Mon, 27 Nov 2023 18:00:00 GMT",
    update_date: str = "2024-01-02",
    comments: str = "",
    journal_ref: str = "",
    **extra: object,
) -> dict:
    record = {
        "id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "categories": categories,
        "versions": [{"version": "v1", "created": v1_created}],
        "update_date": update_date,
        "comments": comments,
        "journal-ref": journal_ref,
    }
    record.update(extra)
    return record


def write_snapshot(records: list[dict]) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")
        return handle.name


def run_search(records: list[dict], query: str, **overrides) -> dict:
    path = write_snapshot(records)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        output = handle.name
    search = snap.SnapshotArxivSearch(
        snapshot_path=path,
        start_date="2016-09-17",
        end_date="2026-09-17",
        output=output,
        **overrides,
    )
    code = search.run([{"label": "q1", "query": query}])
    assert code == 0
    with open(output) as handle:
        return json.load(handle)


class QueryParserTest(unittest.TestCase):
    def test_term_and_phrase(self) -> None:
        node = snap.parse_query('all:"ego-exo" AND abs:egocentric')
        self.assertIsInstance(node, snap.BinaryNode)
        self.assertEqual(node.op, "AND")

    def test_date_range(self) -> None:
        node = snap.parse_query("submittedDate:[202001010000 TO 202312312359]")
        self.assertIsInstance(node, snap.DateRangeNode)

    def test_malformed_range_rejected(self) -> None:
        with self.assertRaises(ValueError):
            snap.parse_query("submittedDate:[bogus TO 202312312359]")

    def test_andnot(self) -> None:
        node = snap.parse_query("all:ego ANDNOT all:cat")
        self.assertEqual(node.op, "ANDNOT")

    def test_unknown_field_is_term(self) -> None:
        # "foo:" is not a known field, tokenizes as a bare term.
        node = snap.parse_query("foo:bar")
        self.assertIsInstance(node, snap.TermNode)
        self.assertEqual(node.term, "foo:bar")


class RecordTest(unittest.TestCase):
    def test_submitted_date_from_v1(self) -> None:
        record = make_record()
        self.assertEqual(
            snap.submitted_date(record).strftime("%Y-%m-%d"), "2023-11-27"
        )

    def test_submitted_date_fallback_update_date(self) -> None:
        record = make_record(versions=[])
        self.assertEqual(
            snap.submitted_date(record).strftime("%Y-%m-%d"), "2024-01-02"
        )

    def test_record_to_paper_shape(self) -> None:
        paper = snap.record_to_paper(make_record(), "q1", "effective")
        self.assertEqual(paper["arxiv_id"], "2311.18259")
        self.assertEqual(paper["query_label"], "q1")
        self.assertEqual(paper["abs_url"], "https://arxiv.org/abs/2311.18259")
        self.assertTrue(paper["title"])
        self.assertTrue(paper["published"].startswith("2023-11-27"))

    def test_authors_parsed_preferred(self) -> None:
        # Kaggle authors_parsed layout: [Last, First, Middle, Suffix]
        record = make_record(
            authors_parsed=[["Author", "A.", "", ""], ["Writer", "B.", "", "Jr."]]
        )
        paper = snap.record_to_paper(record, "q1", "effective")
        self.assertEqual(paper["authors"], ["A. Author", "B. Writer Jr."])

class SnapshotSearchTest(unittest.TestCase):
    def test_matches_title_and_respects_date_range(self) -> None:
        records = [
            make_record(arxiv_id="2311.18259", title="Ego-Exo4D dataset"),
            make_record(
                arxiv_id="9999.99999",
                title="Ego-Exo4D too old",
                v1_created="Mon, 27 Nov 2000 18:00:00 GMT",
            ),
        ]
        result = run_search(records, 'ti:"Ego-Exo4D"')
        self.assertEqual(result["paper_count"], 1)
        self.assertEqual(result["papers"][0]["arxiv_id"], "2311.18259")

    def test_prefix_match_on_all(self) -> None:
        records = [make_record(title="Unrelated", abstract="We study egocentric video.")]
        result = run_search(records, "all:ego")
        self.assertEqual(result["paper_count"], 1)

    def test_andnot_excludes(self) -> None:
        records = [
            make_record(arxiv_id="1", title="Egocentric cooking"),
            make_record(arxiv_id="2", title="Egocentric driving"),
        ]
        result = run_search(records, "all:egocentric ANDNOT ti:driving")
        self.assertEqual(result["paper_count"], 1)
        self.assertEqual(result["papers"][0]["arxiv_id"], "1")

    def test_max_results_truncates(self) -> None:
        records = [
            make_record(arxiv_id=str(index), title="Egocentric video", v1_created=f"Mon, 0{(index % 9) + 1} Nov 2023 10:00:00 GMT")
            for index in range(1, 12)
        ]
        result = run_search(records, "all:egocentric", max_results=3)
        self.assertEqual(result["paper_count"], 3)

    def test_heap_replace_with_identical_sort_keys(self) -> None:
        # >slack matches sharing one sort key: heap tuples must stay comparable
        # via the sequence tiebreaker, never fall through to dict comparison.
        records = [
            make_record(arxiv_id=str(index), title="Egocentric video", v1_created="Mon, 6 Nov 2023 10:00:00 GMT")
            for index in range(150)
        ]
        result = run_search(records, "all:egocentric", max_results=1)
        self.assertEqual(result["paper_count"], 1)
        self.assertIn(result["papers"][0]["arxiv_id"], {str(i) for i in range(150)})

    def test_query_label_merge_on_dedupe(self) -> None:
        records = [make_record(title="Ego-Exo4D")]
        path = write_snapshot(records)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            output = handle.name
        search = snap.SnapshotArxivSearch(
            snapshot_path=path, start_date="2016-09-17", end_date="2026-09-17", output=output
        )
        code = search.run(
            [{"label": "a", "query": 'ti:"Ego-Exo4D"'}, {"label": "b", "query": "all:dataset"}]
        )
        self.assertEqual(code, 0)
        with open(output) as handle:
            data = json.load(handle)
        self.assertEqual(data["paper_count"], 1)
        self.assertEqual(set(data["papers"][0]["query_label"].split(",")), {"a", "b"})

    def test_no_prefilter_when_query_has_no_literal(self) -> None:
        # A pure submittedDate range query has no text literals; prefilter
        # must disable itself instead of skipping every line.
        records = [make_record(title="Whatever")]
        result = run_search(records, "submittedDate:[202001010000 TO 202612312359]")
        self.assertEqual(result["paper_count"], 1)
        self.assertFalse(result["snapshot_prefilter"])

    def test_batch_shape_mirrors_api_backend(self) -> None:
        result = run_search([make_record()], 'all:"ego"')
        for key in ("generated_at", "batch", "api", "start_date", "end_date", "queries", "paper_count", "papers"):
            self.assertIn(key, result)
        self.assertTrue(str(result["api"]).startswith("snapshot:"))


if __name__ == "__main__":
    unittest.main()

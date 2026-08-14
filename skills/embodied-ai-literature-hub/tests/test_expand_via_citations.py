#!/usr/bin/env python3

from __future__ import annotations

import argparse
import email.message
import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "expand_via_citations.py"
SPEC = importlib.util.spec_from_file_location("expand_via_citations", SCRIPT_PATH)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


# ---------------------------------------------------------------------------
# Network retry (mirrors tests/test_search_arxiv.py's mocking pattern)
# ---------------------------------------------------------------------------


class DummyResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def __enter__(self) -> "DummyResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


def args_with_retries(retries: int) -> argparse.Namespace:
    return argparse.Namespace(
        max_per_seed_per_direction=50,
        timeout=1.0,
        user_agent="test-agent",
        api_key=None,
        retries=retries,
        retry_base_seconds=5.0,
        retry_max_seconds=60.0,
    )


def http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = email.message.Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://api.semanticscholar.org/graph/v1/paper/x", code, "error", headers, None)


class FetchRetryTest(unittest.TestCase):
    def test_fetch_retries_429_with_retry_after_and_caps_at_three_retries(self) -> None:
        error = http_error(429, retry_after="7")
        with mock.patch.object(mod.urllib.request, "urlopen", side_effect=[error, error, error, error]) as urlopen:
            with mock.patch.object(mod.time, "sleep") as sleep:
                with self.assertRaises(RuntimeError):
                    mod.fetch("2401.01339", "references", args_with_retries(99))

        self.assertEqual(urlopen.call_count, 4)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [7.0, 7.0, 7.0])

    def test_fetch_succeeds_after_429_retry(self) -> None:
        with mock.patch.object(
            mod.urllib.request,
            "urlopen",
            side_effect=[http_error(429, retry_after="2"), DummyResponse(b'{"data": []}')],
        ) as urlopen:
            with mock.patch.object(mod.time, "sleep") as sleep:
                payload = mod.fetch("2401.01339", "citations", args_with_retries(3))

        self.assertEqual(payload, b'{"data": []}')
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(2.0)

    def test_fetch_does_not_retry_non_transient_http_errors(self) -> None:
        with mock.patch.object(mod.urllib.request, "urlopen", side_effect=http_error(400)) as urlopen:
            with mock.patch.object(mod.time, "sleep") as sleep:
                with self.assertRaisesRegex(RuntimeError, "after 1 attempt"):
                    mod.fetch("2401.01339", "references", args_with_retries(3))

        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()

    def test_fetch_sends_api_key_header_when_present(self) -> None:
        args = args_with_retries(3)
        args.api_key = "secret-key"
        captured = {}

        def fake_urlopen(request, timeout):
            captured["headers"] = dict(request.header_items())
            return DummyResponse(b'{"data": []}')

        with mock.patch.object(mod.urllib.request, "urlopen", side_effect=fake_urlopen):
            mod.fetch("2401.01339", "references", args)

        self.assertEqual(captured["headers"].get("X-api-key"), "secret-key")

    def test_build_neighbor_url_clamps_limit_and_picks_endpoint(self) -> None:
        url = mod.build_neighbor_url("2401.01339", "citations", 5000)
        self.assertIn("/paper/ARXIV:2401.01339/citations", url)
        self.assertIn("limit=1000", url)


# ---------------------------------------------------------------------------
# Pure logic
# ---------------------------------------------------------------------------


class ExtractNeighborPapersTest(unittest.TestCase):
    def test_extracts_arxiv_papers_and_counts_exclusions(self) -> None:
        raw = {
            "data": [
                {"citedPaper": {"title": "A", "externalIds": {"ArXiv": "2401.00001"}, "authors": [{"name": "X"}], "year": 2024}},
                {"citedPaper": {"title": "No arXiv", "externalIds": {"DOI": "10.1/x"}}},
                {"citedPaper": None},
                {},
            ]
        }
        papers, excluded = mod.extract_neighbor_papers("references", raw)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["arxiv_id"], "2401.00001")
        self.assertEqual(papers[0]["authors"], ["X"])
        self.assertEqual(excluded, 3)

    def test_citations_direction_reads_citing_paper_wrapper(self) -> None:
        raw = {"data": [{"citingPaper": {"title": "B", "externalIds": {"ArXiv": "2402.99999v2"}}}]}
        papers, excluded = mod.extract_neighbor_papers("citations", raw)
        self.assertEqual(papers[0]["arxiv_id"], "2402.99999")
        self.assertEqual(excluded, 0)

    def test_prefers_publication_date_over_year(self) -> None:
        raw = {"data": [{"citedPaper": {"externalIds": {"ArXiv": "2401.00001"}, "year": 2024, "publicationDate": "2024-03-15"}}]}
        papers, _ = mod.extract_neighbor_papers("references", raw)
        self.assertEqual(papers[0]["published"], "2024-03-15")


class DateFilterTest(unittest.TestCase):
    def test_filters_by_year_when_range_given(self) -> None:
        papers = [{"published": "2020-01-01"}, {"published": "2024-06-01"}, {"published": ""}]
        kept = mod.filter_by_date(papers, "2023-01-01", "2025-01-01")
        self.assertEqual(len(kept), 2)  # unknown-date paper is kept, not dropped

    def test_no_range_returns_all(self) -> None:
        papers = [{"published": "2020-01-01"}]
        self.assertEqual(mod.filter_by_date(papers, None, None), papers)


class SeedSimilarityTest(unittest.TestCase):
    def test_shared_references_and_citers_raise_jaccard_score(self) -> None:
        seed_references = {"A": {"x1", "x2", "x3"}, "B": {"x1", "x2", "x4"}, "C": {"y1"}}
        seed_citations = {"A": {"c1"}, "B": {"c1"}, "C": set()}
        pairs = mod.compute_seed_similarity(seed_references, seed_citations)
        by_pair = {(p["seed_a"], p["seed_b"]): p for p in pairs}
        ab = by_pair[("A", "B")]
        ac = by_pair[("A", "C")]
        self.assertGreater(ab["reference_coupling_jaccard"], ac["reference_coupling_jaccard"])
        self.assertGreater(ab["combined_score"], ac["combined_score"])
        # A/B share 2 of 4 distinct references -> 0.5; C shares none with A -> 0.0
        self.assertAlmostEqual(ab["reference_coupling_jaccard"], 0.5)
        self.assertAlmostEqual(ac["reference_coupling_jaccard"], 0.0)

    def test_pairs_sorted_by_combined_score_descending(self) -> None:
        seed_references = {"A": {"x1"}, "B": {"x1"}, "C": set()}
        pairs = mod.compute_seed_similarity(seed_references, {})
        self.assertEqual(pairs[0]["seed_a"], "A")
        self.assertEqual(pairs[0]["seed_b"], "B")


class ScoreAndSelectCandidatesTest(unittest.TestCase):
    def test_candidate_shared_by_two_seeds_outranks_single_seed_hit(self) -> None:
        seed_references = {"A": {"shared", "onlyA"}, "B": {"shared", "onlyB"}}
        seed_citations: dict[str, set[str]] = {}
        paper_by_id = {
            "shared": {"title": "Shared paper", "authors": [], "published": "2023", "summary": ""},
            "onlyA": {"title": "Only A", "authors": [], "published": "2023", "summary": ""},
            "onlyB": {"title": "Only B", "authors": [], "published": "2023", "summary": ""},
        }
        scored = mod.score_candidates(seed_references, seed_citations, paper_by_id, {"A", "B"})
        by_id = {item["arxiv_id"]: item for item in scored}
        self.assertEqual(by_id["shared"]["shared_seed_count"], 2)
        self.assertEqual(by_id["onlyA"]["shared_seed_count"], 1)
        self.assertEqual(set(by_id["shared"]["query_label"].split(",")), {"citation:A:references", "citation:B:references"})

    def test_seeds_never_appear_as_their_own_candidates(self) -> None:
        seed_references = {"A": {"B"}}  # A references seed B
        scored = mod.score_candidates(seed_references, {}, {}, {"A", "B"})
        self.assertEqual(scored, [])

    def test_select_candidates_splits_at_threshold_without_silent_drops(self) -> None:
        scored = [
            {"arxiv_id": "high", "shared_seed_count": 3},
            {"arxiv_id": "mid", "shared_seed_count": 2},
            {"arxiv_id": "low", "shared_seed_count": 1},
        ]
        kept, below, truncated = mod.select_candidates(scored, min_shared_seeds=2, max_total=None)
        self.assertEqual([c["arxiv_id"] for c in kept], ["high", "mid"])
        self.assertEqual([c["arxiv_id"] for c in below], ["low"])
        self.assertEqual(truncated, 0)

    def test_select_candidates_reports_truncation_count(self) -> None:
        scored = [{"arxiv_id": f"p{i}", "shared_seed_count": 2} for i in range(5)]
        kept, below, truncated = mod.select_candidates(scored, min_shared_seeds=2, max_total=3)
        self.assertEqual(len(kept), 3)
        self.assertEqual(below, [])
        self.assertEqual(truncated, 2)

    def test_default_min_shared_seeds(self) -> None:
        self.assertEqual(mod.default_min_shared_seeds(1), 1)
        self.assertEqual(mod.default_min_shared_seeds(2), 2)
        self.assertEqual(mod.default_min_shared_seeds(5), 2)


class ExtractTermsTest(unittest.TestCase):
    def test_bigram_survives_even_when_second_word_is_a_generic_domain_word(self) -> None:
        papers = [
            {"arxiv_id": "p1", "title": "A World Model for Robot Planning", "summary": ""},
            {"arxiv_id": "p2", "title": "Learning a World Model from Video", "summary": ""},
        ]
        terms = mod.extract_terms(papers, top_n=20, min_doc_freq=2)
        term_set = {item["term"] for item in terms}
        self.assertIn("world model", term_set)
        self.assertNotIn("model", term_set)  # generic unigram suppressed

    def test_min_doc_frequency_filters_singletons(self) -> None:
        papers = [{"arxiv_id": "p1", "title": "Unique Idiosyncratic Phrase", "summary": ""}]
        terms = mod.extract_terms(papers, top_n=20, min_doc_freq=2)
        self.assertEqual(terms, [])

    def test_extra_stopwords_are_respected(self) -> None:
        papers = [
            {"arxiv_id": "p1", "title": "Foobar tactile sensing", "summary": ""},
            {"arxiv_id": "p2", "title": "Foobar tactile control", "summary": ""},
        ]
        terms = mod.extract_terms(papers, top_n=20, min_doc_freq=2, extra_stopwords=frozenset({"foobar"}))
        term_set = {item["term"] for item in terms}
        self.assertNotIn("foobar", term_set)
        self.assertIn("tactile", term_set)


class BuildOutputsTest(unittest.TestCase):
    def test_build_dynamic_suggestions_shape_matches_planner_contract(self) -> None:
        terms = [{"term": "world model", "doc_frequency": 4, "example_arxiv_id": "2401.00001"}]
        result = mod.build_dynamic_suggestions(terms, ["2401.01339"], "references")
        self.assertEqual(result["queries"][0]["query"], 'all:"world model"')
        self.assertEqual(result["queries"][0]["tier"], "dynamic-association")
        self.assertEqual(result["queries"][0]["source"], "citation-expansion")
        self.assertEqual(result["queries"][0]["confidence"], "medium")
        for key in ("browser_fallback_queries", "web_calibration_queries", "knowledge_ids", "families", "sources"):
            self.assertIn(key, result)

    def test_calibrated_query_from_term_quotes_multiword_terms(self) -> None:
        self.assertEqual(mod.calibrated_query_from_term("umi"), "all:umi")
        self.assertEqual(mod.calibrated_query_from_term("data mixture"), 'all:"data mixture"')

    def test_build_candidate_output_matches_search_arxiv_papers_shape(self) -> None:
        kept = [
            {
                "arxiv_id": "2401.00001",
                "title": "T",
                "authors": ["X"],
                "published": "2024",
                "summary": "S",
                "shared_seed_count": 2,
                "connected_seeds": ["A", "B"],
                "query_label": "citation:A:references,citation:B:references",
            }
        ]
        output = mod.build_candidate_output("batch-1", "both", ["A", "B"], kept, 3, 1, 2, [])
        self.assertEqual(output["batch"], "batch-1")
        self.assertEqual(output["below_threshold_count"], 3)
        self.assertEqual(output["truncated_count"], 1)
        self.assertEqual(output["excluded_no_arxiv_id"], 2)
        self.assertEqual(output["papers"][0]["arxiv_id"], "2401.00001")
        self.assertEqual(output["papers"][0]["query_label"], "citation:A:references,citation:B:references")

    def test_build_graph_output_edge_direction(self) -> None:
        output = mod.build_graph_output(["A", "B"], {"A": {"ref1"}}, {"A": {"citer1"}}, [], 0)
        edges = {(e["from"], e["to"], e["direction"]) for e in output["edges"]}
        self.assertIn(("A", "ref1", "references"), edges)
        self.assertIn(("citer1", "A", "citations"), edges)


class SeedCollectionTest(unittest.TestCase):
    def test_collect_seed_ids_merges_explicit_file_and_registry_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            seed_file = root / "seeds.txt"
            seed_file.write_text("2401.00002\n2401.00002\n", encoding="utf-8")
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "candidates": [
                            {"arxiv_id": "2401.00003", "status": "accepted"},
                            {"arxiv_id": "2401.00004", "status": "discovered"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(
                seed_id=["2401.00001"],
                seed_id_file=str(seed_file),
                seed_registry=str(registry),
                seed_status=[],
            )
            ids = mod.collect_seed_ids(args)

        self.assertEqual(ids, ["2401.00001", "2401.00002", "2401.00003"])

    def test_load_seed_ids_from_registry_filters_by_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            registry = Path(tmpdir) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "candidates": [
                            {"arxiv_id": "2401.00001", "status": "accepted"},
                            {"arxiv_id": "2401.00002", "status": "rejected"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            ids = mod.load_seed_ids_from_registry(str(registry), {"accepted"})
        self.assertEqual(ids, ["2401.00001"])


class EndToEndTest(unittest.TestCase):
    def test_main_writes_candidate_and_dynamic_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            output = root / "candidates.json"
            dynamic_output = root / "dynamic.json"
            graph_output = root / "graph.json"

            def fake_urlopen(request, timeout):
                url = request.full_url
                if "/references" in url:
                    payload = json.dumps(
                        {
                            "data": [
                                {
                                    "citedPaper": {
                                        "title": "Shared World Model Paper",
                                        "abstract": "world model for robot planning",
                                        "externalIds": {"ArXiv": "2401.09999"},
                                        "year": 2023,
                                    }
                                }
                            ]
                        }
                    ).encode("utf-8")
                else:
                    payload = json.dumps({"data": []}).encode("utf-8")
                return DummyResponse(payload)

            argv = [
                "expand_via_citations.py",
                "--seed-id",
                "2401.00001",
                "--seed-id",
                "2401.00002",
                "--min-shared-seeds",
                "1",
                "--output",
                str(output),
                "--dynamic-output",
                str(dynamic_output),
                "--graph-output",
                str(graph_output),
                "--sleep-seconds",
                "0",
                "--min-doc-frequency",
                "1",
            ]
            with mock.patch.object(mod.sys, "argv", argv):
                with mock.patch.object(mod.urllib.request, "urlopen", side_effect=fake_urlopen):
                    exit_code = mod.main()

            self.assertEqual(exit_code, 0)
            candidate_data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(candidate_data["paper_count"], 1)
            self.assertEqual(candidate_data["papers"][0]["arxiv_id"], "2401.09999")
            self.assertEqual(candidate_data["papers"][0]["shared_seed_count"], 2)

            dynamic_data = json.loads(dynamic_output.read_text(encoding="utf-8"))
            self.assertTrue(any(q["query"] == 'all:"world model"' for q in dynamic_data["queries"]))

            graph_data = json.loads(graph_output.read_text(encoding="utf-8"))
            self.assertTrue(len(graph_data["edges"]) >= 2)


if __name__ == "__main__":
    unittest.main()

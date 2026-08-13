#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "rank_influential_papers.py"
SPEC = importlib.util.spec_from_file_location("rank_influential_papers", SCRIPT_PATH)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def args(**overrides: object) -> argparse.Namespace:
    base = argparse.Namespace(
        author_strategy="max-hindex",
        code_source="abstract",
        direction="both",
        sleep_seconds=0.0,
        max_per_seed_per_direction=500,
        api_key=None,
        weights="citation=0.40,venue=0.25,author=0.20,code=0.15",
    )
    for key, value in overrides.items():
        setattr(base, key, value)
    return base


class NormalizeTest(unittest.TestCase):
    def test_strips_version_and_suffixes(self) -> None:
        self.assertEqual(mod.normalize_arxiv_id("2104.07905v2"), "2104.07905")
        self.assertEqual(mod.normalize_arxiv_id("https://arxiv.org/abs/2104.07905"), "2104.07905")
        self.assertEqual(mod.normalize_arxiv_id("2104.07905.pdf"), "2104.07905")


class VenueTest(unittest.TestCase):
    def test_tier1_venues(self) -> None:
        for venue in (
            "Computer Vision and Pattern Recognition",
            "European Conference on Computer Vision",
            "International Conference on Computer Vision",
            "Neural Information Processing Systems",
            "International Conference on Learning Representations",
            "International Conference on Machine Learning",
            "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        ):
            result = mod.classify_venue(venue)
            self.assertEqual(result["score"], 1.0, venue)

    def test_tier2_venues(self) -> None:
        for venue in ("Robotics and Automation", "Intelligent Robots and Systems", "Conference on Robot Learning"):
            result = mod.classify_venue(venue)
            self.assertEqual(result["score"], 0.66, venue)

    def test_ral_before_icra_substring_ordering(self) -> None:
        self.assertEqual(mod.classify_venue("IEEE Robotics and Automation Letters")["canonical"], "RA-L")
        self.assertEqual(mod.classify_venue("Robotics and Automation")["canonical"], "ICRA")

    def test_preprint_and_unknown(self) -> None:
        self.assertEqual(mod.classify_venue("")["score"], 0.0)
        self.assertEqual(mod.classify_venue("")["canonical"], "preprint")
        self.assertEqual(mod.classify_venue("Some Unmappable Venue Quarterly")["score"], 0.5)
        self.assertEqual(mod.classify_venue("Some Unmappable Venue Quarterly")["canonical"], "unknown")


class LogNormalizeTest(unittest.TestCase):
    def test_zero_max_is_zero(self) -> None:
        self.assertEqual(mod.log_normalize(5, 0), 0.0)

    def test_max_value_is_one(self) -> None:
        self.assertEqual(mod.log_normalize(1000, 1000), 1.0)

    def test_log_compressess_orders_of_magnitude(self) -> None:
        # 1000 citations vs 100 citations should compress far below the linear 0.1
        score = mod.log_normalize(100, 1000)
        self.assertGreater(score, 0.1)
        self.assertLess(score, 1.0)


class WeightsTest(unittest.TestCase):
    def test_default_parses(self) -> None:
        w = mod.parse_weights("citation=0.40,venue=0.25,author=0.20,code=0.15")
        self.assertAlmostEqual(sum(w.values()), 1.0)

    def test_renormalizes_when_not_summing_to_one(self) -> None:
        w = mod.parse_weights("citation=1,venue=1")
        self.assertAlmostEqual(sum(w.values()), 1.0)
        self.assertAlmostEqual(w["citation"], 0.5)

    def test_garbage_falls_back_to_defaults(self) -> None:
        w = mod.parse_weights("nonsense")
        self.assertIn("citation", w)


class AuthorTest(unittest.TestCase):
    def test_max_hindex_strategy(self) -> None:
        h, known = mod.author_h_index([{"name": "a", "hIndex": 10}, {"name": "b", "hIndex": 99}], "max-hindex")
        self.assertTrue(known)
        self.assertEqual(h, 99.0)

    def test_first_author_strategy(self) -> None:
        h, _ = mod.author_h_index([{"name": "a", "hIndex": 10}, {"name": "b", "hIndex": 99}], "first-author")
        self.assertEqual(h, 10.0)

    def test_unknown_when_no_hindex(self) -> None:
        h, known = mod.author_h_index([{"name": "a"}], "max-hindex")
        self.assertFalse(known)
        self.assertEqual(h, 0.0)


class CodeTest(unittest.TestCase):
    def test_abstract_mention_confirms(self) -> None:
        self.assertTrue(mod.code_mention("We release code at github.com/foo/bar."))

    def test_abstract_no_mention_is_confirm_only_neutral(self) -> None:
        result = mod.code_score("abstract", "1", "A model for X.", args())
        self.assertEqual(result["score"], 0.5)
        self.assertFalse(result["known"])

    def test_none_source_is_neutral(self) -> None:
        self.assertEqual(mod.code_score("none", "1", "anything", args())["score"], 0.5)

    def test_pwc_positive(self) -> None:
        with mock.patch.object(mod, "pwc_repo_count", return_value=(3, True)):
            result = mod.code_score("pwc", "1", "x", args())
        self.assertEqual(result["score"], 1.0)
        self.assertTrue(result["known"])

    def test_pwc_zero(self) -> None:
        with mock.patch.object(mod, "pwc_repo_count", return_value=(0, True)):
            result = mod.code_score("pwc", "1", "x", args())
        self.assertEqual(result["score"], 0.0)


class TypeFlagsTest(unittest.TestCase):
    def test_detects_survey_and_dataset(self) -> None:
        self.assertTrue(mod.type_flags("A Survey of Egocentric Video")["is_survey"])
        self.assertTrue(mod.type_flags("The EPIC-Kitchens Dataset")["is_dataset"])
        self.assertFalse(mod.type_flags("Learning Representations")["is_survey"])


class RankTest(unittest.TestCase):
    def _papers(self) -> list[dict]:
        return [
            {"arxiv_id": "a", "title": "High", "abstract": "", "authors": ["x"], "published": "2015-01-01",
             "citation_count": 10000, "venue": "Computer Vision and Pattern Recognition", "direction": "citations", "connected_seeds": ["s"]},
            {"arxiv_id": "b", "title": "Low", "abstract": "", "authors": ["y"], "published": "2015-01-01",
             "citation_count": 5, "venue": "", "direction": "references", "connected_seeds": ["s"]},
        ]

    def test_higher_citation_and_venue_outranks(self) -> None:
        ranked = mod.rank_papers(self._papers(), {"citation": 0.4, "venue": 0.25, "author": 0.2, "code": 0.15}, {}, args(), 10)
        self.assertEqual(ranked[0]["arxiv_id"], "a")
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[1]["arxiv_id"], "b")

    def test_composite_is_weighted_sum_of_subscores(self) -> None:
        ranked = mod.rank_papers(self._papers(), {"citation": 0.4, "venue": 0.25, "author": 0.2, "code": 0.15}, {}, args(), 10)
        for item in ranked:
            sub = item["sub_scores"]
            expected = 0.4 * sub["citation"] + 0.25 * sub["venue"] + 0.2 * sub["author"] + 0.15 * sub["code"]
            self.assertAlmostEqual(item["composite_score"], round(min(1.0, expected), 4), places=4)

    def test_truncates_to_top(self) -> None:
        ranked = mod.rank_papers(self._papers(), {"citation": 0.4, "venue": 0.25, "author": 0.2, "code": 0.15}, {}, args(), top=1)
        self.assertEqual(len(ranked), 1)


class MarkdownOutputTest(unittest.TestCase):
    def test_emits_table_rows(self) -> None:
        ranked = mod.rank_papers(
            [{"arxiv_id": "a", "title": "T", "abstract": "", "authors": ["x"], "published": "2015",
              "citation_count": 10, "venue": "Computer Vision and Pattern Recognition", "direction": "citations", "connected_seeds": ["s"]}],
            {"citation": 0.4, "venue": 0.25, "author": 0.2, "code": 0.15}, {}, args(), 1,
        )
        md = mod.markdown_output(["s"], args(), ranked)
        self.assertIn("| 1 |", md)
        self.assertIn("arxiv.org/abs/a", md)


class FilterTest(unittest.TestCase):
    def test_min_year_drops_older_but_keeps_unknown_year(self) -> None:
        papers = [
            {"arxiv_id": "a", "published": "2015-01-01", "title": "", "abstract": ""},
            {"arxiv_id": "b", "published": "2022-01-01", "title": "", "abstract": ""},
            {"arxiv_id": "c", "published": "", "title": "", "abstract": ""},
        ]
        kept, dropped = mod.filter_papers(papers, min_year=2021, require_terms=None)
        self.assertEqual([p["arxiv_id"] for p in kept], ["b", "c"])
        self.assertEqual(dropped, 1)

    def test_require_terms_keeps_any_match(self) -> None:
        papers = [
            {"arxiv_id": "a", "published": "2022", "title": "Egocentric Video-Language Pretraining", "abstract": ""},
            {"arxiv_id": "b", "published": "2022", "title": "First-person hand-object interaction", "abstract": ""},
            {"arxiv_id": "c", "published": "2022", "title": "Object Detection", "abstract": "a generic detector"},
        ]
        kept, dropped = mod.filter_papers(papers, min_year=None, require_terms="egocentric,first-person,ego4d")
        self.assertEqual([p["arxiv_id"] for p in kept], ["a", "b"])
        self.assertEqual(dropped, 1)

    def test_no_filters_keeps_all(self) -> None:
        papers = [{"arxiv_id": "a", "published": "2015", "title": "", "abstract": ""}]
        kept, dropped = mod.filter_papers(papers, None, None)
        self.assertEqual(len(kept), 1)
        self.assertEqual(dropped, 0)

    def test_title_terms_is_tighter_than_abstract_terms(self) -> None:
        papers = [
            {"arxiv_id": "core", "published": "2022", "title": "Egocentric Video-Language Pretraining", "abstract": ""},
            {"arxiv_id": "tangential", "published": "2022", "title": "Composing Multimodal Reasoning", "abstract": "evaluated on egocentric video"},
        ]
        kept, dropped = mod.filter_papers(papers, None, None, require_title_terms="egocentric,ego,exo,first-person")
        self.assertEqual([p["arxiv_id"] for p in kept], ["core"])
        self.assertEqual(dropped, 1)

    def test_must_terms_drops_papers_without_the_required_side(self) -> None:
        papers = [
            {"arxiv_id": "ego_only", "published": "2022", "title": "Egocentric Video-Language Pretraining", "abstract": "first-person video understanding"},
            {"arxiv_id": "ego_exo", "published": "2022", "title": "Ego-Exo Transfer", "abstract": "third-person to first-person"},
            {"arxiv_id": "exo_only", "published": "2022", "title": "Affordance Grounding from Exocentric Images", "abstract": ""},
        ]
        kept, dropped = mod.filter_papers(papers, None, None, None, must_terms="third-person,third person,exocentric,exo-centric,exo")
        self.assertEqual([p["arxiv_id"] for p in kept], ["ego_exo", "exo_only"])
        self.assertEqual(dropped, 1)

    def test_must_terms_composes_with_min_year(self) -> None:
        papers = [
            {"arxiv_id": "old_exo", "published": "2018", "title": "Exocentric affordance", "abstract": ""},
            {"arxiv_id": "new_exo", "published": "2022", "title": "Exocentric affordance", "abstract": ""},
        ]
        kept, dropped = mod.filter_papers(papers, 2021, None, None, must_terms="exo")
        self.assertEqual([p["arxiv_id"] for p in kept], ["new_exo"])
        self.assertEqual(dropped, 1)

    def test_year_of_parses_prefix(self) -> None:
        self.assertEqual(mod.year_of("2022-03-15"), 2022)
        self.assertIsNone(mod.year_of(""))
        self.assertIsNone(mod.year_of("nope"))


class CitationsPerYearTest(unittest.TestCase):
    def test_divides_by_age(self) -> None:
        # 100 citations over ~4 years vs 200 over ~10 years -> velocity favors the younger paper
        self.assertAlmostEqual(mod.citations_per_year(400, "2022-01-01"), 100.0, places=0)
        self.assertGreater(mod.citations_per_year(400, "2022-01-01"), mod.citations_per_year(800, "2016-01-01"))

    def test_unknown_year_is_zero(self) -> None:
        self.assertEqual(mod.citations_per_year(100, ""), 0.0)


class YearNormalizedRankingTest(unittest.TestCase):
    def test_young_paper_with_high_velocity_outranks_old_paper_with_more_raw_citations(self) -> None:
        papers = [
            {"arxiv_id": "old", "title": "Old", "abstract": "", "authors": ["x"], "published": "2015-01-01",
             "citation_count": 3000, "venue": "Computer Vision and Pattern Recognition", "direction": "citations", "connected_seeds": []},
            {"arxiv_id": "young", "title": "Young", "abstract": "", "authors": ["y"], "published": "2025-01-01",
             "citation_count": 300, "venue": "Computer Vision and Pattern Recognition", "direction": "citations", "connected_seeds": []},
        ]
        # same venue, same (unknown) author -> citation dimension decides; velocity favors "young"
        ranked = mod.rank_papers(papers, {"citation": 0.4, "venue": 0.25, "author": 0.2, "code": 0.15}, {}, args(), 10)
        self.assertEqual(ranked[0]["arxiv_id"], "young")
        # raw count still reported untouched
        self.assertEqual(ranked[0]["citation_count"], 300)


class DiscoverNeighborsTest(unittest.TestCase):
    def test_pagination_walks_next_offset(self) -> None:
        pages = [
            {"data": [{"citedPaper": {"title": "P1", "externalIds": {"ArXiv": "1.1"}, "authors": [], "year": 2020}}], "next": 1},
            {"data": [{"citedPaper": {"title": "P2", "externalIds": {"ArXiv": "2.2"}, "authors": [], "year": 2021}}], "next": None},
        ]

        def fake_fetch(url, a, data=None):
            return pages.pop(0)

        with mock.patch.object(mod, "fetch_json", side_effect=fake_fetch):
            papers, excluded = mod.discover_neighbors("s", "references", args(max_per_seed_per_direction=500))

        self.assertEqual([p["arxiv_id"] for p in papers], ["1.1", "2.2"])
        self.assertEqual(excluded, 0)


class BatchEnrichmentTest(unittest.TestCase):
    def test_maps_arxiv_ids_to_authors(self) -> None:
        payload = [{"externalIds": {"ArXiv": "1.1"}, "authors": [{"name": "a", "hIndex": 42}], "title": "T"}]

        def fake_fetch(url, a, data=None):
            self.assertIn("/paper/batch", url)
            return payload

        with mock.patch.object(mod, "fetch_json", side_effect=fake_fetch):
            out = mod.batch_enrichment(["1.1"], args())

        self.assertIn("1.1", out)
        self.assertEqual(out["1.1"]["authors"][0]["hIndex"], 42)


if __name__ == "__main__":
    unittest.main()

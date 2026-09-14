#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "rank_problem_relevance.py"
SPEC = importlib.util.spec_from_file_location("rank_problem_relevance", SCRIPT_PATH)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def make_surface(abstract="", introduction="", related_work=""):
    return {
        "abstract": abstract,
        "introduction": introduction,
        "related_work": related_work,
        "complete": bool(abstract or introduction or related_work),
    }


def make_doc(arxiv_id, title="", abstract="", introduction="", related_work="", **extra):
    doc = {
        "arxiv_id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "published": "2022-01-01",
        "connected_seeds": [],
        "round": 1,
        "judgment_surface": make_surface(abstract, introduction, related_work),
    }
    doc.update(extra)
    return doc


class NormalizeTest(unittest.TestCase):
    def test_strips_version_and_suffixes(self) -> None:
        self.assertEqual(mod.normalize_arxiv_id("2104.07905v2"), "2104.07905")
        self.assertEqual(mod.normalize_arxiv_id("https://arxiv.org/abs/2104.07905"), "2104.07905")
        self.assertEqual(mod.normalize_arxiv_id("2104.07905.pdf"), "2104.07905")


class TokenizeTest(unittest.TestCase):
    def test_strips_stopwords_and_question_words(self) -> None:
        tokens = mod.tokenize("How to align first-person and third-person views?")
        for word in ("how", "to", "and"):
            self.assertNotIn(word, tokens)
        for word in ("align", "first-person", "third-person", "views"):
            self.assertIn(word, tokens)

    def test_keeps_hyphenated_and_dehyphenated_forms(self) -> None:
        tokens = mod.tokenize("multi-view camera configuration")
        self.assertIn("multi-view", tokens)
        self.assertIn("multiview", tokens)
        self.assertIn("camera", tokens)
        self.assertIn("configuration", tokens)

    def test_drops_short_tokens(self) -> None:
        self.assertNotIn("to", mod.tokenize("to"))
        self.assertNotIn("in", mod.tokenize("in"))


class SectionTest(unittest.TestCase):
    def test_classifies_abstract(self) -> None:
        self.assertEqual(mod.classify_judgment_section("", "ltx_abstract"), "abstract")
        self.assertEqual(mod.classify_judgment_section("Abstract", "ltx_section"), "abstract")

    def test_classifies_introduction(self) -> None:
        self.assertEqual(mod.classify_judgment_section("Introduction", "ltx_section"), "introduction")

    def test_classifies_related_work_variants(self) -> None:
        for title in ("Related Work", "Related Works", "Prior Work", "Background", "Relation to Prior Work"):
            self.assertEqual(mod.classify_judgment_section(title, "ltx_section"), "related_work", title)

    def test_classifies_other(self) -> None:
        self.assertEqual(mod.classify_judgment_section("Method", "ltx_section"), "other")
        self.assertEqual(mod.classify_judgment_section("", "ltx_section"), "other")

    def test_extract_judgment_surface_joins_sections(self) -> None:
        sections = [
            {"title": "Abstract", "kind": "ltx_abstract", "text": "A."},
            {"title": "Introduction", "kind": "ltx_section", "text": "I1."},
            {"title": "Related Work", "kind": "ltx_section", "text": "RW1."},
            {"title": "Method", "kind": "ltx_section", "text": "M."},
        ]
        surface = mod.extract_judgment_surface(sections)
        self.assertEqual(surface["abstract"], "A.")
        self.assertEqual(surface["introduction"], "I1.")
        self.assertEqual(surface["related_work"], "RW1.")
        self.assertTrue(surface["complete"])

    def test_extract_tolerates_missing_related_work(self) -> None:
        sections = [{"title": "Introduction", "kind": "ltx_section", "text": "I1."}]
        surface = mod.extract_judgment_surface(sections)
        self.assertEqual(surface["related_work"], "")
        self.assertTrue(surface["complete"])


class FieldGatesTest(unittest.TestCase):
    def test_year_of_parses_prefix(self) -> None:
        self.assertEqual(mod.year_of("2022-03-15"), 2022)
        self.assertIsNone(mod.year_of(""))
        self.assertIsNone(mod.year_of("nope"))

    def test_no_gates_passes(self) -> None:
        args = type("A", (), {"require_terms": None, "must_terms": None})()
        self.assertTrue(mod.passes_field_gates("title", "abstract", args))

    def test_require_terms_is_or(self) -> None:
        args = type("A", (), {"require_terms": "egocentric,exo", "must_terms": None})()
        self.assertTrue(mod.passes_field_gates("Ego-Exo transfer", "", args))
        self.assertFalse(mod.passes_field_gates("Object detection", "", args))

    def test_must_terms_is_and_gate(self) -> None:
        args = type("A", (), {"require_terms": None, "must_terms": "third-person,exocentric"})()
        self.assertTrue(mod.passes_field_gates("third-person views", "", args))
        self.assertFalse(mod.passes_field_gates("egocentric only", "", args))


class CouplingTest(unittest.TestCase):
    def test_shared_seed_count(self) -> None:
        seed_references = {"s1": {"a", "b"}, "s2": {"b", "c"}}
        seed_citations: dict[str, set[str]] = {}
        scored = mod.coupling_scores(seed_references, seed_citations, {"s1", "s2"})
        by_id = {s["arxiv_id"]: s for s in scored}
        self.assertEqual(by_id["a"]["shared_seed_count"], 1)
        self.assertEqual(by_id["b"]["shared_seed_count"], 2)
        self.assertEqual(sorted(by_id["b"]["connected_seeds"]), ["s1", "s2"])
        self.assertEqual(by_id["c"]["shared_seed_count"], 1)
        # seeds themselves are excluded
        self.assertNotIn("s1", by_id)


class Bm25Test(unittest.TestCase):
    def test_monotonic_in_tf(self) -> None:
        low = mod.bm25_field(tf=1, df=1, n=10, doc_len=10, avg_len=10)
        high = mod.bm25_field(tf=3, df=1, n=10, doc_len=10, avg_len=10)
        self.assertGreater(high, low)

    def test_inverse_in_df(self) -> None:
        rare = mod.bm25_field(tf=1, df=1, n=10, doc_len=10, avg_len=10)
        common = mod.bm25_field(tf=1, df=9, n=10, doc_len=10, avg_len=10)
        self.assertGreater(rare, common)

    def test_length_normalized(self) -> None:
        short = mod.bm25_field(tf=1, df=1, n=10, doc_len=5, avg_len=10)
        long = mod.bm25_field(tf=1, df=1, n=10, doc_len=50, avg_len=10)
        self.assertGreater(short, long)

    def test_zero_tf_is_zero(self) -> None:
        self.assertEqual(mod.bm25_field(tf=0, df=1, n=10, doc_len=10, avg_len=10), 0.0)

    def test_hand_computed_value(self) -> None:
        # tf=2, df=1, n=4, len=avg_len=10 -> idf=log((4-1+.5)/(1+.5)+1), norm=2*2.5/(2+1.5*(0.25+0.75))
        import math as _m
        expected = _m.log((4 - 1 + 0.5) / (1 + 0.5) + 1.0) * (2 * 2.5 / (2 + 1.5 * (0.25 + 0.75)))
        self.assertAlmostEqual(mod.bm25_field(tf=2, df=1, n=4, doc_len=10, avg_len=10), expected, places=6)


class IndexTest(unittest.TestCase):
    def test_build_index_computes_df_and_avg_len(self) -> None:
        docs = [make_doc("a"), make_doc("b")]
        field_tokens = {
            "a": {"title": ["x"], "abstract": ["y", "y"], "introduction": [], "related_work": []},
            "b": {"title": ["x", "z"], "abstract": [], "introduction": [], "related_work": []},
        }
        index = mod.build_index(docs, field_tokens)
        self.assertEqual(index["n"], 2)
        self.assertEqual(index["field_df"]["title"]["x"], 2)
        self.assertEqual(index["field_df"]["title"]["z"], 1)
        self.assertEqual(index["field_df"]["abstract"]["y"], 1)
        self.assertEqual(index["avg_len"]["title"], 1.5)
        self.assertEqual(index["avg_len"]["abstract"], 1.0)


class ScoreDocumentTest(unittest.TestCase):
    def _index(self, docs, field_tokens):
        return mod.build_index(docs, field_tokens)

    def test_title_term_scores_higher_than_abstract_term(self) -> None:
        field_weights = mod.parse_field_weights("title=2.0,abstract=1.0,introduction=1.5,related_work=1.5")
        docs = [make_doc("a"), make_doc("b")]
        field_tokens = {
            "a": {"title": ["camera"], "abstract": [], "introduction": [], "related_work": []},
            "b": {"title": [], "abstract": ["camera"], "introduction": [], "related_work": []},
        }
        index = self._index(docs, field_tokens)
        score_a = mod.score_document(field_tokens["a"], ["camera"], index, field_weights)["score"]
        score_b = mod.score_document(field_tokens["b"], ["camera"], index, field_weights)["score"]
        self.assertGreater(score_a, score_b)

    def test_empty_doc_is_zero(self) -> None:
        field_weights = mod.parse_field_weights("title=2.0,abstract=1.0,introduction=1.5,related_work=1.5")
        index = mod.build_index([make_doc("a")], {"a": {"title": [], "abstract": [], "introduction": [], "related_work": []}})
        score = mod.score_document({"title": [], "abstract": [], "introduction": [], "related_work": []}, ["camera"], index, field_weights)
        self.assertEqual(score["score"], 0.0)
        self.assertEqual(score["matched_terms"], [])


class RetrieveTest(unittest.TestCase):
    def _corpus(self):
        # "direct" is highly relevant to the question; "adjacent" is not.
        direct = make_doc(
            "direct",
            title="Aligning first-person and third-person views",
            abstract="We align first-person and third-person camera views.",
            introduction="How to align first-person and third-person views is the core problem.",
            related_work="Prior work aligns first-person and third-person views via calibration.",
        )
        adjacent = make_doc(
            "adjacent",
            title="A survey of video classification",
            abstract="We study video classification.",
            introduction="Video classification is important.",
            related_work="Many approaches classify video.",
        )
        return [direct, adjacent]

    def test_relevant_surface_outranks_adjacent(self) -> None:
        questions = [{"text": "How to align first-person and third-person views?", "terms": mod.tokenize("How to align first-person and third-person views?")}]
        field_weights = mod.parse_field_weights("title=2.0,abstract=1.0,introduction=1.5,related_work=1.5")
        retrieved, truncated, _ = mod.retrieve(self._corpus(), questions, field_weights, target=50)
        self.assertEqual(truncated, 0)
        self.assertEqual(retrieved[0]["arxiv_id"], "direct")
        self.assertEqual(retrieved[0]["rank"], 1)

    def test_explanation_is_non_empty_for_matches(self) -> None:
        questions = [{"text": "How to align first-person and third-person views?", "terms": mod.tokenize("How to align first-person and third-person views?")}]
        field_weights = mod.parse_field_weights("title=2.0,abstract=1.0,introduction=1.5,related_work=1.5")
        retrieved, _, _ = mod.retrieve(self._corpus(), questions, field_weights, target=50)
        direct = next(r for r in retrieved if r["arxiv_id"] == "direct")
        self.assertTrue(direct["explanation"])
        self.assertTrue(any("align" == t["term"] for q in direct["explanation"] for t in q["terms"]))

    def test_truncation_reported(self) -> None:
        questions = [{"text": "q", "terms": mod.tokenize("camera view")}]
        corpus = [make_doc(f"p{i}", title=f"camera view paper {i}", abstract="camera view") for i in range(10)]
        field_weights = mod.parse_field_weights("title=2.0,abstract=1.0,introduction=1.5,related_work=1.5")
        retrieved, truncated, _ = mod.retrieve(corpus, questions, field_weights, target=3)
        self.assertEqual(len(retrieved), 3)
        self.assertEqual(truncated, 7)


class FieldWeightsTest(unittest.TestCase):
    def test_parses_and_defaults_missing(self) -> None:
        weights = mod.parse_field_weights("title=2.0,abstract=1.0")
        self.assertEqual(weights["title"], 2.0)
        self.assertEqual(weights["abstract"], 1.0)
        self.assertEqual(weights["introduction"], 0.0)
        self.assertEqual(weights["related_work"], 0.0)


class MinSharedSeedsTest(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(mod.default_min_shared_seeds(1), 1)
        self.assertEqual(mod.default_min_shared_seeds(2), 2)
        self.assertEqual(mod.default_min_shared_seeds(5), 2)


if __name__ == "__main__":
    unittest.main()

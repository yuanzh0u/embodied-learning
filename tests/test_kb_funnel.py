"""Tests for knowledge.funnel — the publishable retrieval→evidence funnel.

The funnel is derived from run-directory artifacts only. These tests pin the
layer-derivation rules (including the ``null`` = artifact-absent convention),
the abstract-tier scope check, the KB aggregation, and the layer query used by
``wiki.py kb-funnel``.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.funnel import (
    FUNNEL_FILENAME,
    LAYERS,
    build_funnel,
    kb_funnel,
    read_funnel,
    summarize,
    write_funnel,
)
from embodied_learning.knowledge.model import KnowledgeBase

from test_kb_model import write_run


def write_registry(run_dir: Path, ids: list[str], *, count: int | None = None) -> None:
    payload = {
        "candidate_count": len(ids) if count is None else count,
        "candidates": [
            {"arxiv_id": paper_id, "title": f"Title {paper_id}", "published": "2025-01-01"}
            for paper_id in ids
        ],
    }
    (run_dir / "candidate-registry.json").write_text(json.dumps(payload), encoding="utf-8")


def write_screening(run_dir: Path, ids: list[str], *, reasons: dict[str, str] | None = None,
                    strategy: str = "smart", limit: int = 20) -> None:
    reasons = reasons or {}
    payload = {
        "selection_rule": {"strategy": strategy, "detail": "selected for relevance", "limit": limit},
        "candidates": [
            {"arxiv_id": paper_id, "selection_reason": reasons.get(paper_id, "")}
            for paper_id in ids
        ],
    }
    (run_dir / "screening.json").write_text(json.dumps(payload), encoding="utf-8")
    (run_dir / "screening-ids.txt").write_text("\n".join(ids) + "\n", encoding="utf-8")


def write_extraction(run_dir: Path, eligible: list[str], held: list[str],
                     channel_down: list[str] | None = None) -> None:
    results = [
        {"paper_id": paper_id, "state": "ok", "evidence_eligible": True}
        for paper_id in eligible
    ]
    results += [
        {"paper_id": paper_id, "state": "held", "evidence_eligible": False}
        for paper_id in held
    ]
    results += [
        {"paper_id": paper_id, "state": "channel-down", "evidence_eligible": False}
        for paper_id in channel_down or []
    ]
    payload = {
        "paper_count": len(results),
        "results": results,
        "held_count": len(held),
        "channel_down_count": len(channel_down or []),
    }
    (run_dir / "extraction-summary.json").write_text(json.dumps(payload), encoding="utf-8")


def write_note(run_dir: Path, paper_id: str, *, status: str = "pass", failed: bool = False) -> None:
    notes = run_dir / "paper-notes"
    notes.mkdir(exist_ok=True)
    if failed:
        (notes / f"{paper_id}.failed.json").write_text(
            json.dumps({"paper_id": paper_id, "reason": "skeleton"}), encoding="utf-8"
        )
        return
    (notes / f"{paper_id}.json").write_text(json.dumps({"paper_id": paper_id}), encoding="utf-8")
    (notes / f"{paper_id}.audit.json").write_text(
        json.dumps({"status": status}), encoding="utf-8"
    )


def write_evidence(run_dir: Path, paper_id: str, events: int = 1) -> None:
    evidence = run_dir / "evidence"
    evidence.mkdir(exist_ok=True)
    lines = [json.dumps({"event_id": f"EA-X-{i:04d}", "paper": {"arxiv_id": paper_id}})
             for i in range(events)]
    (evidence / f"{paper_id}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_abstract_tier(run_dir: Path, ids: list[str]) -> None:
    evidence = run_dir / "evidence"
    evidence.mkdir(exist_ok=True)
    lines = [json.dumps({"event_id": f"EA-A-{i:04d}", "tier": "abstract",
                         "paper": {"arxiv_id": paper_id}}) for i, paper_id in enumerate(ids)]
    (evidence / "abstract-tier.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


class FunnelTestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.run_dir = Path(self._tmp.name) / "literature-review-demo-20260101"
        self.run_dir.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def build(self, **kwargs) -> dict:
        options = {"run": self.run_dir.name, "topic": "demo", "review_mode": "rapid"}
        options.update(kwargs)
        return build_funnel(self.run_dir, **options)


class BuildFunnelTest(FunnelTestBase):
    def test_six_layers_from_disk(self):
        write_registry(self.run_dir, ["a", "b", "c", "d"])
        write_screening(self.run_dir, ["a", "b", "c"])
        write_extraction(self.run_dir, eligible=["a", "b"], held=["c"])
        write_note(self.run_dir, "a", status="pass")
        write_note(self.run_dir, "b", status="needs-review")
        write_note(self.run_dir, "c", failed=True)
        write_evidence(self.run_dir, "a", events=2)
        write_evidence(self.run_dir, "b", events=1)
        write_abstract_tier(self.run_dir, ["a", "b", "c"])

        payload = self.build(summary={"seed_ids": [], "abstract_basis": "screened"})

        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(tuple(payload["layers"]), LAYERS)
        self.assertEqual(payload["stages"], {
            "candidates": 4,
            "screened": 3,
            "full_text": 2,
            "deep_read": 3,
            "evidence_papers": 2,
            "evidence_events": 3,
            "abstract_papers": 3,
            "abstract_events": 3,
        })
        self.assertEqual(payload["layers"]["screened"], ["a", "b", "c"])
        self.assertEqual(sorted(payload["layers"]["deep_read"]), ["a", "b", "c"])
        self.assertEqual(sorted(payload["layers"]["evidence"]), ["a", "b"])
        self.assertEqual(payload["detail"]["deep_read_pass"], 1)
        self.assertEqual(payload["detail"]["deep_read_needs_review"], 1)
        self.assertEqual(payload["detail"]["deep_read_failed"], 1)
        self.assertEqual(payload["detail"]["held"], 1)
        self.assertEqual(payload["detail"]["channel_down"], 0)
        self.assertEqual(payload["detail"]["abstract_basis"], "screened")
        self.assertEqual(payload["detail"]["abstract_leaked"], 0)
        self.assertEqual(payload["detail"]["cited_floor"], 6)
        self.assertEqual(payload["detail"]["floor_met"], False)

    def test_missing_artifacts_yield_null_layers_not_guesses(self):
        payload = self.build()

        self.assertEqual(payload["stages"]["candidates"], None)
        for name in ("screened", "full_text", "deep_read", "evidence", "abstract"):
            self.assertEqual(payload["stages"][
                {"screened": "screened", "full_text": "full_text", "deep_read": "deep_read",
                 "evidence": "evidence_papers", "abstract": "abstract_papers"}[name]
            ], None)
            self.assertIsNone(payload["layers"][name])
        self.assertEqual(payload["layers"]["registry"], [])

    def test_registry_count_falls_back_when_candidate_list_is_trimmed(self):
        (self.run_dir / "candidate-registry.json").write_text(
            json.dumps({"candidate_count": 42, "candidates": []}), encoding="utf-8"
        )
        payload = self.build()
        self.assertEqual(payload["stages"]["candidates"], 42)
        self.assertEqual(payload["layers"]["registry"], [])

    def test_full_text_is_intersected_with_the_selection(self):
        write_registry(self.run_dir, ["a", "b", "stale"])
        write_screening(self.run_dir, ["a", "b"])
        # An older extraction summary still lists a paper a re-run screening dropped.
        write_extraction(self.run_dir, eligible=["a", "stale"], held=[])
        payload = self.build()
        self.assertEqual(payload["layers"]["full_text"], ["a"])
        self.assertEqual(payload["stages"]["full_text"], 1)

    def test_deep_read_counts_notes_and_failures_but_not_audits(self):
        write_screening(self.run_dir, ["a", "b"])
        write_note(self.run_dir, "a", status="pass")
        write_note(self.run_dir, "b", failed=True)
        payload = self.build()
        self.assertEqual(sorted(payload["layers"]["deep_read"]), ["a", "b"])
        self.assertEqual(payload["stages"]["deep_read"], 2)

    def test_skip_deep_read_still_reports_artifacts_on_disk(self):
        """``--skip-deep-read`` is a flag, not a fact about the disk (D8)."""
        write_note(self.run_dir, "a", status="pass")
        payload = self.build(skipped=["deep-read"])
        self.assertEqual(payload["stages"]["deep_read"], 1)
        self.assertEqual(payload["detail"]["skipped"], ["deep-read"])

    def test_abstract_leak_outside_selection_is_counted(self):
        write_registry(self.run_dir, ["a", "leak"])
        write_screening(self.run_dir, ["a"])
        write_abstract_tier(self.run_dir, ["a", "leak"])
        payload = self.build()
        self.assertEqual(payload["detail"]["abstract_leaked"], 1)

    def test_seeds_outside_the_selection_are_counted(self):
        write_screening(self.run_dir, ["a"])
        write_note(self.run_dir, "seed", status="pass")
        write_note(self.run_dir, "a", status="pass")
        payload = self.build(summary={"seed_ids": ["seed", "a"]})
        self.assertEqual(payload["detail"]["seeds_outside_screened"], 1)

    def test_papers_carry_title_published_and_selection_reason(self):
        write_registry(self.run_dir, ["a"])
        write_screening(self.run_dir, ["a"], reasons={"a": "benchmarks UMI data"}, limit=7)
        payload = self.build()
        self.assertEqual(payload["papers"]["a"], {
            "title": "Title a",
            "published": "2025-01-01",
            "reason": "benchmarks UMI data",
        })
        self.assertEqual(payload["detail"]["screen_limit"], 7)
        self.assertEqual(payload["detail"]["selection_strategy"], "smart")

    def test_layer_derivation_never_calls_path_glob(self):
        """The driver test harness patches ``Path.glob``; the funnel must use
        ``iterdir`` so it keeps working under that patch."""
        write_screening(self.run_dir, ["a"])
        write_note(self.run_dir, "a", status="pass")
        write_evidence(self.run_dir, "a")
        write_abstract_tier(self.run_dir, ["a"])
        with mock.patch.object(Path, "glob", side_effect=AssertionError("glob used")):
            payload = self.build()
        self.assertEqual(payload["stages"]["deep_read"], 1)
        self.assertEqual(payload["stages"]["evidence_papers"], 1)


class TruncationTest(FunnelTestBase):
    def test_layer_over_cap_is_truncated_and_flagged(self):
        write_registry(self.run_dir, ["a", "b", "c"])
        with mock.patch("embodied_learning.knowledge.funnel.FUNNEL_LAYER_PAPER_CAP", 2):
            payload = self.build()
        self.assertTrue(payload["truncated"])
        self.assertEqual(payload["layers"]["registry"], ["a", "b"])
        self.assertLessEqual(len(payload["papers"]), 2)


class WriteReadTest(FunnelTestBase):
    def test_round_trip_and_missing_or_foreign_schema_degrade_to_none(self):
        self.assertIsNone(read_funnel(self.run_dir))
        payload = self.build()
        target = write_funnel(payload, self.run_dir)
        self.assertEqual(target, self.run_dir / FUNNEL_FILENAME)
        self.assertEqual(read_funnel(self.run_dir)["stages"], payload["stages"])

        (self.run_dir / FUNNEL_FILENAME).write_text("{not json", encoding="utf-8")
        self.assertIsNone(read_funnel(self.run_dir))
        (self.run_dir / FUNNEL_FILENAME).write_text(
            json.dumps({"schema_version": 99, "stages": {}}), encoding="utf-8"
        )
        self.assertIsNone(read_funnel(self.run_dir))


class KbFunnelTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        with_data = write_run(self.root, "run-with", events=2, topic="Alpha")
        without = write_run(self.root, "run-without", events=0, topic="Beta")
        write_registry(with_data, ["a", "b", "c"])
        write_screening(with_data, ["a", "b"], reasons={"a": "first"})
        write_evidence(with_data, "a")
        write_funnel(
            build_funnel(with_data, run="run-with", topic="Alpha", review_mode="rapid"),
            with_data,
        )
        self.assertFalse((without / FUNNEL_FILENAME).exists())
        self.kb = KnowledgeBase.open(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_run_rows_include_runs_without_data(self):
        rows = kb_funnel(self.kb)
        self.assertEqual([row["run"] for row in rows], ["run-with", "run-without"])
        self.assertTrue(rows[0]["funnel_available"])
        self.assertEqual(rows[0]["stages"]["screened"], 2)
        self.assertIsNone(rows[1]["stages"])
        self.assertFalse(rows[1]["funnel_available"])

    def test_layer_query_returns_papers_with_metadata(self):
        rows = kb_funnel(self.kb, layer="screened", run="run-with")
        self.assertEqual([row["arxiv_id"] for row in rows], ["a", "b"])
        self.assertEqual(rows[0]["title"], "Title a")
        self.assertEqual(rows[0]["reason"], "first")
        self.assertEqual(rows[1]["reason"], "")

    def test_layer_query_skips_runs_without_funnel(self):
        self.assertEqual(kb_funnel(self.kb, layer="screened"), [
            {"run": "run-with", "layer": "screened", "arxiv_id": "a",
             "title": "Title a", "published": "2025-01-01", "reason": "first"},
            {"run": "run-with", "layer": "screened", "arxiv_id": "b",
             "title": "Title b", "published": "2025-01-01", "reason": ""},
        ])

    def test_filters_narrow_by_topic_and_mode(self):
        self.assertEqual([row["run"] for row in kb_funnel(self.kb, topic="alph")], ["run-with"])
        self.assertEqual(kb_funnel(self.kb, review_mode="scoping"), [])

    def test_numeric_sort_is_descending_with_null_last(self):
        rows = kb_funnel(self.kb, sort="screened")
        self.assertEqual([row["run"] for row in rows], ["run-with", "run-without"])

    def test_unknown_layer_or_sort_is_a_value_error(self):
        with self.assertRaises(ValueError):
            kb_funnel(self.kb, layer="nope")
        with self.assertRaises(ValueError):
            kb_funnel(self.kb, sort="nope")

    def test_knowledge_base_proxy_matches_the_function(self):
        self.assertEqual(self.kb.funnel(layer="screened", run="run-with"),
                         kb_funnel(self.kb, layer="screened", run="run-with"))

    def test_summarize_counts_runs_with_and_without_data(self):
        block = summarize(self.kb)
        self.assertEqual(block["runs_with_funnel"], 1)
        self.assertEqual(block["runs_without_funnel"], 1)
        self.assertEqual(block["sums"]["candidates"], 3)
        self.assertEqual(block["sums"]["screened"], 2)
        self.assertEqual(block["rates"]["screen"], 0.6667)
        self.assertEqual(block["rates"]["full_text"], None)  # null layer → null rate


if __name__ == "__main__":
    unittest.main()

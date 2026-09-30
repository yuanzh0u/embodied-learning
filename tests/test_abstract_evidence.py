"""embodied_learning.search.abstract_evidence — the abstract evidence tier.

Abstract-tier events are positioning-only evidence projected from registry
metadata; these tests pin the excerpting, the per-candidate projection rules,
and the tier-splitting helpers the packet and the driver share.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


from embodied_learning.search.abstract_evidence import (
    ABSTRACT_FILENAME,
    build_abstract_events,
    excerpt,
    load_tier,
    max_event_seq,
    read_events,
    write_abstract_tier,
)


def registry_with(*candidates: dict) -> dict:
    return {"candidate_count": len(candidates), "candidates": list(candidates)}


def candidate(arxiv_id: str, summary: str, title: str = "A paper") -> dict:
    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "summary": summary,
        "published": "2026-05-01",
        "authors": [{"name": "Alice", "author_key": "alice"}],
    }


class ExcerptTest(unittest.TestCase):
    def test_takes_first_two_sentences_up_to_the_cap(self):
        text = "First sentence about the method. Second sentence adds scope. Third one is dropped."
        self.assertEqual(excerpt(text), "First sentence about the method. Second sentence adds scope.")

    def test_hard_cap_adds_ellipsis(self):
        text = "x" * 500
        out = excerpt(text, max_chars=300)
        self.assertEqual(len(out), 300)
        self.assertTrue(out.endswith("…"))

    def test_whitespace_normalized_and_empty_safe(self):
        self.assertEqual(excerpt("  a\n b  "), "a b")
        self.assertEqual(excerpt(""), "")
        self.assertEqual(excerpt(None), "")  # type: ignore[arg-type]


class BuildAbstractEventsTest(unittest.TestCase):
    def test_one_event_per_candidate_with_title_and_abstract(self):
        registry = registry_with(
            candidate("2402.10329", "First sentence here."),
            {"arxiv_id": "2302.01109", "title": "No abstract"},  # no summary -> skipped
            {"title": "No id", "summary": "orphan"},  # no arxiv_id -> skipped
            candidate("2311.18259", "Another abstract."),
        )
        events = build_abstract_events(
            registry, topic="demo", topic_id="EA-DATA", prefix="EA-DEMO-2026", start_seq=1
        )
        self.assertEqual(
            [event["event_id"] for event in events],
            ["EA-DEMO-2026-0001", "EA-DEMO-2026-0002"],
        )
        first = events[0]
        self.assertEqual(first["tier"], "abstract")
        self.assertEqual(first["stance"], "")  # no stance: positioning only
        self.assertEqual(first["topic_id"], "EA-DATA")
        self.assertEqual(first["paper"]["arxiv_id"], "2402.10329")
        self.assertEqual(first["evidence"]["locator"], "abstract")
        self.assertEqual(first["evidence"]["evidence_type"], "positioning")
        self.assertEqual(first["claim"], "First sentence here.")

    def test_exclude_drops_papers_that_already_have_full_text_evidence(self):
        registry = registry_with(
            candidate("2402.10329", "One."),
            candidate("2311.18259", "Two."),
        )
        events = build_abstract_events(
            registry, topic="demo", topic_id="EA-DATA", prefix="EA-DEMO-2026",
            start_seq=3, exclude_arxiv_ids={"2311.18259"},
        )
        self.assertEqual(
            [event["event_id"] for event in events], ["EA-DEMO-2026-0003"]
        )
        self.assertEqual(events[0]["paper"]["arxiv_id"], "2402.10329")

    def test_prefix_trailing_dash_is_normalized(self):
        events = build_abstract_events(
            registry_with(candidate("2402.10329", "s.")),
            topic="demo", topic_id="EA-DATA", prefix="EA-DEMO-2026-", start_seq=1,
        )
        self.assertEqual(events[0]["event_id"], "EA-DEMO-2026-0001")


class WriteAbstractTierTest(unittest.TestCase):
    def test_writes_jsonl_atomically_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence_dir = Path(tmp)
            events = build_abstract_events(
                registry_with(candidate("2402.10329", "One.")),
                topic="demo", topic_id="EA-DATA", prefix="EA-DEMO-2026", start_seq=1,
            )
            first = write_abstract_tier(events, evidence_dir)
            self.assertEqual(first, evidence_dir / ABSTRACT_FILENAME)
            payload = first.read_text(encoding="utf-8")
            self.assertEqual(len(read_events(first)), 1)
            self.assertTrue(payload.endswith("\n"))
            # A rerun with the same events rewrites the identical file (atomic
            # replace, no tmp leftovers).
            second = write_abstract_tier(events, evidence_dir)
            self.assertEqual(first.read_text(encoding="utf-8"), payload)
            self.assertEqual(list(evidence_dir.glob("*.tmp-*")), [])
            self.assertEqual(second, first)

    def test_empty_event_list_writes_an_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = write_abstract_tier([], Path(tmp))
            self.assertEqual(target.read_text(encoding="utf-8"), "")


class TierHelpersTest(unittest.TestCase):
    def test_load_tier_splits_full_text_from_abstract(self):
        fulltext = {"event_id": "EA-DEMO-2026-0009", "claim": "deep read"}
        abstract = {"event_id": "EA-DEMO-2026-0001", "tier": "abstract", "claim": "positioning"}
        events = [fulltext, abstract]
        self.assertEqual(load_tier(events, None), [fulltext])
        self.assertEqual(load_tier(events, "abstract"), [abstract])

    def test_max_event_seq_reads_highest_suffix(self):
        events = [
            {"event_id": "EA-DEMO-2026-0007"},
            {"event_id": "EA-DEMO-2026-0042"},
            {"event_id": "no-suffix"},
            {"event_id": ""},
        ]
        self.assertEqual(max_event_seq(events), 42)
        self.assertEqual(max_event_seq([]), 0)

    def test_read_events_tolerates_missing_and_malformed_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.jsonl"
            self.assertEqual(read_events(path), [])
            path.write_text(
                '{"event_id": "a"}\nnot json\n\n{"event_id": "b"}\n', encoding="utf-8"
            )
            self.assertEqual(
                [event["event_id"] for event in read_events(path)], ["a", "b"]
            )


if __name__ == "__main__":
    unittest.main()

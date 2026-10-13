#!/usr/bin/env python3
"""Contract tests: event_anchor has exactly one home and the three historical
call sites agree with it (build_review_packet / _trace_map / audit_citations
used to carry copies that had to match byte-for-byte)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.knowledge.evidence import event_anchor  # noqa: E402
from embodied_learning.writer.trace_map import event_anchor as trace_anchor  # noqa: E402
from embodied_learning.wiki.run import citations  # noqa: E402


class EventAnchorContractTest(unittest.TestCase):
    def test_known_anchor_shapes(self) -> None:
        self.assertEqual(event_anchor("EA-DATA-2026-0001"), "ea-data-2026-0001")
        self.assertEqual(event_anchor("摘要级相关工作"), "摘要级相关工作")

    def test_all_call_sites_agree_with_the_single_home(self) -> None:
        for sample in ("EA-DATA-2026-0001", "摘要级相关工作", "EV-12  A/B"):
            self.assertEqual(trace_anchor(sample), event_anchor(sample), sample)

    def test_citations_anchor_matches(self) -> None:
        if hasattr(citations, "event_anchor"):
            self.assertEqual(citations.event_anchor("EA-X-0001"), event_anchor("EA-X-0001"))
        elif hasattr(citations, "anchor_for"):
            self.assertEqual(citations.anchor_for("EA-X-0001"), event_anchor("EA-X-0001"))


if __name__ == "__main__":
    unittest.main()

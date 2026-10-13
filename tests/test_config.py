#!/usr/bin/env python3
"""Contract tests for embodied_learning.config (single home for mode tables)."""

from __future__ import annotations

import unittest

from embodied_learning import config


class ConfigContractTest(unittest.TestCase):
    def test_mode_tables_cover_all_review_modes(self) -> None:
        for table_name in (
            "EVIDENCE_FLOORS",
            "CITED_PAPER_FLOORS",
            "SCREEN_LIMITS",
            "DEEP_READ_LIMITS",
        ):
            table = getattr(config, table_name)
            self.assertEqual(set(table), set(config.REVIEW_MODES), table_name)

    def test_floor_values_are_the_review_contract(self) -> None:
        self.assertEqual(config.EVIDENCE_FLOORS, {"rapid": 8, "scoping": 15, "systematic": 30})
        self.assertEqual(config.CITED_PAPER_FLOORS, {"rapid": 6, "scoping": 10, "systematic": 15})

    def test_cited_floor_never_exceeds_evidence_floor(self) -> None:
        for mode in config.REVIEW_MODES:
            self.assertLessEqual(
                config.CITED_PAPER_FLOORS[mode],
                config.EVIDENCE_FLOORS[mode],
                mode,
            )

    def test_style_contract(self) -> None:
        self.assertEqual(config.STYLE_TO_ARTICLE, config.STYLE_TO_FILE)
        for name in config.STANDARD_ARTICLES:
            self.assertIn(name, config.STYLE_TO_FILE.values())

    def test_stance_caps_cover_fixed_vocabulary(self) -> None:
        self.assertEqual(
            set(config.DEFAULT_WRITER_STANCE_CAPS),
            {"support", "limit", "conditional", "gap"},
        )


if __name__ == "__main__":
    unittest.main()

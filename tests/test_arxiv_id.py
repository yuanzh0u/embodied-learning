#!/usr/bin/env python3
"""Tests for embodied_learning.utils.arxiv_id (unified normalization)."""

from __future__ import annotations

import unittest

from embodied_learning.utils.arxiv_id import normalize_arxiv_id


class NormalizeArxivIdTest(unittest.TestCase):
    def test_strips_version_and_suffixes(self) -> None:
        self.assertEqual(normalize_arxiv_id("2608.15659v2"), "2608.15659")
        self.assertEqual(normalize_arxiv_id("2608.15659v2.pdf"), "2608.15659")
        self.assertEqual(normalize_arxiv_id("2608.15659.html"), "2608.15659")

    def test_takes_last_url_path_segment(self) -> None:
        self.assertEqual(normalize_arxiv_id("https://arxiv.org/abs/2608.15659v3"), "2608.15659")
        self.assertEqual(normalize_arxiv_id("http://arxiv.org/pdf/2608.15659v1.pdf"), "2608.15659")

    def test_empty_input_is_empty_string(self) -> None:
        self.assertEqual(normalize_arxiv_id(None), "")
        self.assertEqual(normalize_arxiv_id(""), "")

    def test_strict_mode_accepts_bare_id_and_url(self) -> None:
        self.assertEqual(normalize_arxiv_id("2608.15659v2", strict=True), "2608.15659")
        self.assertEqual(
            normalize_arxiv_id("https://arxiv.org/abs/2608.15659", strict=True),
            "2608.15659",
        )

    def test_strict_mode_strips_arxiv_prefix(self) -> None:
        self.assertEqual(normalize_arxiv_id("arXiv:2608.15659", strict=True), "2608.15659")

    def test_strict_mode_raises_with_offending_value(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            normalize_arxiv_id("not-a-paper", strict=True)
        self.assertIn("not-a-paper", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

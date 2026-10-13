#!/usr/bin/env python3
"""Tests for embodied_learning.utils.frontmatter (unified YAML-subset parser)."""

from __future__ import annotations

import unittest

from embodied_learning.utils.frontmatter import parse_frontmatter, strip_frontmatter


class FrontmatterTest(unittest.TestCase):
    def test_scalars(self) -> None:
        parsed = parse_frontmatter("---\nid: EA-DATA\ntitle: 数据可用性\n---\nbody\n")
        self.assertEqual(parsed["id"], "EA-DATA")
        self.assertEqual(parsed["title"], "数据可用性")

    def test_inline_lists(self) -> None:
        parsed = parse_frontmatter("---\nid: EA-DATA\ntags: [data, umi]\naliases: ['数据', \"可用性\"]\n---\n")
        self.assertEqual(parsed["tags"], ["data", "umi"])
        self.assertEqual(parsed["aliases"], ["数据", "可用性"])

    def test_source_block_list(self) -> None:
        text = (
            "---\n"
            "id: EA-DATA\n"
            "source:\n"
            "  - id: RUN-x\n"
            "    file: ../evidence/run.json\n"
            "    status: active\n"
            "  - id: POOL-y\n"
            "    file: /pool/arxiv-1/paper.md\n"
            "---\n"
            "body\n"
        )
        parsed = parse_frontmatter(text)
        source = parsed["source"]
        self.assertEqual(len(source), 2)
        self.assertEqual(source[0], {"id": "RUN-x", "file": "../evidence/run.json", "status": "active"})
        self.assertEqual(source[1]["id"], "POOL-y")

    def test_no_frontmatter(self) -> None:
        self.assertEqual(parse_frontmatter("# just a doc\n"), {})
        self.assertEqual(strip_frontmatter("# just a doc\n"), "# just a doc\n")

    def test_strip_frontmatter_returns_body(self) -> None:
        text = "---\nid: X\n---\nbody\n"
        self.assertEqual(strip_frontmatter(text), "body\n")

    def test_missing_close_is_empty(self) -> None:
        self.assertEqual(parse_frontmatter("---\nid: X\nbody\n"), {})


if __name__ == "__main__":
    unittest.main()

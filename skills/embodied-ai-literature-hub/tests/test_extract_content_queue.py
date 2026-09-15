#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))  # modules under src/ import src.* at load time

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("extract_content_queue", ROOT / "src" / "fetch" / "legacy" / "extract_content_queue.py")
extract_content_queue = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(extract_content_queue)


class ExtractContentQueueTest(unittest.TestCase):
    def test_load_ids_normalizes_comments_urls_versions_and_duplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ids.txt"
            path.write_text("2606.03784v2\nhttps://arxiv.org/abs/2607.00673\n2606.03784 # duplicate\n", encoding="utf-8")
            self.assertEqual(["2606.03784", "2607.00673"], extract_content_queue.load_ids(path))


if __name__ == "__main__":
    unittest.main()

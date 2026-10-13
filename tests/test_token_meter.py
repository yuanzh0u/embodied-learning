#!/usr/bin/env python3

from __future__ import annotations

from _entry import invoke, parse

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "embodied_learning.wiki.run.meter"  # implementation module (old scripts/token_meter.py deleted)
mod = importlib.import_module(SCRIPT)


class TokenMeterTests(unittest.TestCase):
    def test_force_appends_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "token-meter.jsonl"
            sample = Path(tmp) / "brief.md"
            sample.write_text("hello", encoding="utf-8")
            code = invoke("run.py", "token-meter", 
                [
                    "--output",
                    str(out),
                    "--stage",
                    "writer.zhihu",
                    "--run-id",
                    "demo",
                    "--file",
                    str(sample),
                    "--prompt-chars",
                    "12",
                    "--force",
                ]
            )
            self.assertEqual(0, code)
            rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(1, len(rows))
            self.assertEqual("writer.zhihu", rows[0]["stage"])
            self.assertEqual(12, rows[0]["prompt_chars"])
            self.assertEqual(str(sample), rows[0]["files_loaded"][0]["path"])
            self.assertEqual(5, rows[0]["files_loaded"][0]["bytes"])

    def test_disabled_without_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "token-meter.jsonl"
            old = os.environ.pop(mod.ENV_FLAG, None)
            try:
                code = invoke("run.py", "token-meter", ["--output", str(out), "--stage", "hub.coverage_decide"])
            finally:
                if old is not None:
                    os.environ[mod.ENV_FLAG] = old
            self.assertEqual(0, code)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()

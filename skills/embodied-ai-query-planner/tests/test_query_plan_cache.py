#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-query-planner" / "scripts" / "query_plan_cache.py"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=check,
        text=True,
        capture_output=True,
        cwd=ROOT,
    )


class QueryPlanCacheTests(unittest.TestCase):
    def test_put_get_roundtrip_and_key_stability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_root = str(Path(tmp) / "cache")
            plan = Path(tmp) / "plan.json"
            plan.write_text(
                json.dumps({"schema_version": 1, "topic": "UMI", "queries": []}),
                encoding="utf-8",
            )
            common = [
                "--topic",
                "UMI  数据可用性",
                "--review-mode",
                "scoping",
                "--time-range",
                "近六个月",
                "--family",
                "umi",
                "--cache-root",
                cache_root,
            ]
            key_a = json.loads(run("key", *common).stdout)["cache_key"]
            # Family order / whitespace should not change the key.
            key_b = json.loads(
                run(
                    "key",
                    "--topic",
                    "umi 数据可用性",
                    "--review-mode",
                    "scoping",
                    "--time-range",
                    "近六个月",
                    "--family",
                    "umi",
                    "--cache-root",
                    cache_root,
                ).stdout
            )["cache_key"]
            self.assertEqual(key_a, key_b)

            miss = run("get", *common, "--json", check=False)
            self.assertEqual(miss.returncode, 2)
            self.assertFalse(json.loads(miss.stdout)["hit"])

            put = json.loads(
                run("put", *common, "--plan", str(plan), "--had-persona").stdout
            )
            self.assertTrue(put["stored"])

            out = Path(tmp) / "copied.json"
            hit = json.loads(
                run("get", *common, "--output", str(out), "--json").stdout
            )
            self.assertTrue(hit["hit"])
            self.assertTrue(hit["skip_dynamic_llm"])
            self.assertTrue(hit["skip_persona_llm"])
            self.assertTrue(hit["persona_regen_on_coverage_gaps_still_allowed"])
            copied = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(copied["topic"], "UMI")

            run("invalidate", *common)
            miss2 = run("get", *common, "--json", check=False)
            self.assertEqual(miss2.returncode, 2)


if __name__ == "__main__":
    unittest.main()

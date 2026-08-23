#!/usr/bin/env python3
"""Behavior tests for the saturation-triggered persona regeneration suggester."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-query-planner" / "scripts" / "suggest_persona_regeneration.py"
PLANNER = ROOT / "skills" / "embodied-ai-query-planner" / "scripts" / "build_query_plan.py"

PASSING_DIMENSIONS = [
    {"dimension": "direct-topic", "unique_candidates": 40, "minimum_unique_candidates": 10, "passed": True},
    {"dimension": "mechanisms-and-interfaces", "unique_candidates": 25, "minimum_unique_candidates": 10, "passed": True},
    {"dimension": "evaluation-and-validation", "unique_candidates": 18, "minimum_unique_candidates": 10, "passed": True},
    {"dimension": "deployment-and-operations", "unique_candidates": 22, "minimum_unique_candidates": 10, "passed": True},
    {"dimension": "adjacent-and-transfer", "unique_candidates": 15, "minimum_unique_candidates": 10, "passed": True},
]


def write_json(directory: Path, name: str, payload: object) -> str:
    path = directory / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def run_script(*args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def base_plan(regeneration_round: int | None = None) -> dict:
    query = {
        "label": "core-tactile",
        "tier": "core",
        "query": 'all:"tactile sensing" AND all:robot',
        "why": "core query",
        "coverage_dimension": "direct-topic",
    }
    if regeneration_round is not None:
        query["regeneration_round"] = regeneration_round
    return {"topic": "触觉数据联合训练", "queries": [query]}


class SuggestPersonaRegenerationTests(unittest.TestCase):
    def test_dimension_gap_generates_draft_persona(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan_path = write_json(directory, "query-plan.json", base_plan())
            coverage_path = write_json(
                directory,
                "coverage-report.json",
                {
                    "coverage_dimensions": PASSING_DIMENSIONS
                    + [
                        {
                            "dimension": "limits-and-counterevidence",
                            "unique_candidates": 3,
                            "minimum_unique_candidates": 10,
                            "passed": False,
                        }
                    ]
                },
            )

            draft = run_script("--plan", plan_path, "--coverage-report", coverage_path)

            self.assertEqual("draft-needs-review", draft["status"])
            self.assertEqual(1, draft["regeneration_round"])
            self.assertEqual(2, draft["max_regeneration_rounds"])
            self.assertTrue(
                any("limits-and-counterevidence" in trigger for trigger in draft["triggered_by"])
            )

            personas = {persona["id"]: persona for persona in draft["personas"]}
            self.assertIn("P-LIMIT-REG-R1", personas)
            limit_persona = personas["P-LIMIT-REG-R1"]
            self.assertEqual(["limits-and-counterevidence"], limit_persona["primary_dimensions"])
            self.assertEqual(1, limit_persona["regeneration_round"])
            self.assertTrue(limit_persona["triggered_by"])

            queries = [query for query in draft["queries"] if query["persona"] == "P-LIMIT-REG-R1"]
            self.assertTrue(queries)
            for query in queries:
                self.assertEqual(1, query["regeneration_round"])
                self.assertEqual("limits-and-counterevidence", query["coverage_dimension"])
                self.assertNotIn("tier", query)
            # Anchor terms from the plan's direct-topic queries should seed the
            # gap dimension's starter queries.
            self.assertTrue(any("tactile sensing" in query["query"] for query in queries))

    def test_stance_skew_triggers_counter_evidence_persona(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan_path = write_json(directory, "query-plan.json", base_plan())

            skewed = directory / "evidence-skewed.jsonl"
            skewed.write_text(
                "\n".join(
                    json.dumps({"event_id": f"EA-T-{index}", "stance": stance})
                    for index, stance in enumerate(["support"] * 10 + ["limit", "conditional"])
                )
                + "\n",
                encoding="utf-8",
            )
            draft = run_script("--plan", plan_path, "--evidence", str(skewed))
            persona_ids = {persona["id"] for persona in draft["personas"]}
            self.assertIn("P-COUNTER-EVIDENCE-REG-R1", persona_ids)
            self.assertTrue(
                any("stance share" in trigger for trigger in draft["triggered_by"])
            )

            balanced = directory / "evidence-balanced.jsonl"
            balanced.write_text(
                "\n".join(
                    json.dumps({"event_id": f"EA-T-{index}", "stance": stance})
                    for index, stance in enumerate(["support"] * 6 + ["limit"] * 4 + ["gap"] * 2)
                )
                + "\n",
                encoding="utf-8",
            )
            draft = run_script("--plan", plan_path, "--evidence", str(balanced))
            persona_ids = {persona["id"] for persona in draft["personas"]}
            self.assertNotIn("P-COUNTER-EVIDENCE-REG-R1", persona_ids)
            self.assertTrue(any("Stance check not triggered" in note for note in draft["notes"]))

            small = directory / "evidence-small.jsonl"
            small.write_text(
                "\n".join(
                    json.dumps({"event_id": f"EA-T-{index}", "stance": "support"})
                    for index in range(5)
                )
                + "\n",
                encoding="utf-8",
            )
            draft = run_script("--plan", plan_path, "--evidence", str(small))
            self.assertTrue(any("too few" in note for note in draft["notes"]))

    def test_round_cap_refuses_beyond_max_rounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            coverage_path = write_json(
                directory,
                "coverage-report.json",
                {
                    "coverage_dimensions": PASSING_DIMENSIONS
                    + [
                        {
                            "dimension": "direct-topic",
                            "unique_candidates": 4,
                            "minimum_unique_candidates": 10,
                            "passed": False,
                        }
                    ]
                },
            )

            at_cap = write_json(directory, "plan-at-cap.json", base_plan(regeneration_round=2))
            refused = run_script("--plan", at_cap, "--coverage-report", coverage_path)
            self.assertEqual("refused", refused["status"])
            self.assertNotIn("personas", refused)
            self.assertIn("exceeds the cap", refused["reason"])

            below_cap = write_json(directory, "plan-below-cap.json", base_plan(regeneration_round=1))
            draft = run_script("--plan", below_cap, "--coverage-report", coverage_path)
            self.assertEqual("draft-needs-review", draft["status"])
            self.assertEqual(2, draft["regeneration_round"])
            self.assertTrue(
                any("P-DIRECT-REG-R2" == persona["id"] for persona in draft["personas"])
            )

    def test_draft_persona_file_merges_into_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            plan_path = write_json(directory, "query-plan.json", base_plan())
            coverage_path = write_json(
                directory,
                "coverage-report.json",
                {
                    "coverage_dimensions": PASSING_DIMENSIONS
                    + [
                        {
                            "dimension": "limits-and-counterevidence",
                            "unique_candidates": 3,
                            "minimum_unique_candidates": 10,
                            "passed": False,
                        }
                    ]
                },
            )
            draft_path = directory / "persona-regeneration.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--plan",
                    plan_path,
                    "--coverage-report",
                    coverage_path,
                    "--output",
                    str(draft_path),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual("", completed.stdout.strip())

            plan = json.loads(
                subprocess.run(
                    [
                        sys.executable,
                        str(PLANNER),
                        "--topic",
                        "近半年触觉数据联合训练的坑",
                        "--max-queries",
                        "50",
                        "--persona-file",
                        str(draft_path),
                    ],
                    check=True,
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                ).stdout
            )

            reg_queries = [
                query
                for query in plan["queries"]
                if query.get("persona_id") == "P-LIMIT-REG-R1"
            ]
            self.assertTrue(reg_queries)
            for query in reg_queries:
                self.assertEqual("persona", query["persona_source"])
                self.assertEqual("limits-and-counterevidence", query["coverage_dimension"])
                self.assertEqual("persona-limit", query["tier"])
                self.assertEqual(1, query["regeneration_round"])
            self.assertTrue(
                any(persona["id"] == "P-LIMIT-REG-R1" for persona in plan["personas"])
            )


if __name__ == "__main__":
    unittest.main()

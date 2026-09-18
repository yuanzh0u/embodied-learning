#!/usr/bin/env python3
"""Dispatch tests for the consolidated search.py entry.

search.py folds several former single-purpose scripts into one file, and three
sections each own a ``run()`` (candidate_registry / screening / coverage). A
bare ``from ... import run`` rebinds one shared module global, so every handler
silently routed to whichever import came last — build-candidate-registry called
coverage.run(6 args) and died with ``TypeError: run() takes 4 positional
arguments but 6 were given``. These tests pin each handler to its own module's
run so the shadowing cannot come back.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
SEARCH_ENTRY = ROOT / "skills" / "embodied-ai-literature-hub" / "scripts" / "search.py"


def load_search_module():
    spec = importlib.util.spec_from_file_location("hub_search_entry", SEARCH_ENTRY)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class SearchCliDispatchTest(unittest.TestCase):
    def setUp(self):
        self.module = load_search_module()

    def test_build_candidate_registry_dispatches_to_candidate_registry_run(self):
        with mock.patch.object(self.module.candidate_registry, "run", return_value=0) as run:
            code = self.module._build_candidate_registry_main(
                ["--search-result", "/tmp/s.json", "--semantic-scholar-result", "/tmp/s2.json", "--output", "/tmp/o.json"]
            )
        self.assertEqual(code, 0)
        run.assert_called_once_with(
            [Path("/tmp/s.json")], [], [], [Path("/tmp/s2.json")], None, Path("/tmp/o.json")
        )

    def test_screen_candidates_dispatches_to_screening_run(self):
        with mock.patch.object(self.module.screening, "run", return_value=0) as run:
            code = self.module._screen_candidates_main(
                ["--candidate-registry", "/tmp/r.json", "--terms", "UMI,data",
                 "--output-screening", "/tmp/scr.json", "--output-ids", "/tmp/ids.txt"]
            )
        self.assertEqual(code, 0)
        args, kwargs = run.call_args
        self.assertEqual(kwargs.get("candidate_registry"), "/tmp/r.json")
        self.assertEqual(kwargs.get("terms_raw"), "UMI,data")
        self.assertEqual(kwargs.get("output_screening"), "/tmp/scr.json")
        self.assertEqual(kwargs.get("output_ids"), "/tmp/ids.txt")

    def test_assess_review_coverage_dispatches_to_coverage_run(self):
        with mock.patch.object(self.module.coverage, "run", return_value=0) as run:
            code = self.module._assess_review_coverage_main(
                ["--query-plan", "/tmp/plan.json", "--candidate-registry", "/tmp/r.json",
                 "--evidence-jsonl", "/tmp/e.jsonl", "--output", "/tmp/cov.json"]
            )
        self.assertEqual(code, 0)
        run.assert_called_once_with(
            Path("/tmp/plan.json"), Path("/tmp/r.json"), [Path("/tmp/e.jsonl")], Path("/tmp/cov.json")
        )


if __name__ == "__main__":
    unittest.main()

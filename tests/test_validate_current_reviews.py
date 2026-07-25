from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_current_reviews.py"
SPEC = importlib.util.spec_from_file_location("validate_current_reviews", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ValidateCurrentReviewsTests(unittest.TestCase):
    def test_catalog_routes_are_deduplicated_and_sorted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "knowledge").mkdir()
            for name in ["run-b", "run-a"]:
                run_dir = root / "evidence" / name
                run_dir.mkdir(parents=True)
                (run_dir / "run.json").write_text("{}", encoding="utf-8")
            (root / "knowledge" / "literature-review-catalog.md").write_text(
                "\n".join(
                    [
                        "[b](../evidence/run-b/run.json)",
                        "[a](../evidence/run-a/run.json)",
                        "[a again](../evidence/run-a/run.json)",
                    ]
                ),
                encoding="utf-8",
            )

            paths = validator.catalog_run_paths(root.resolve())

            self.assertEqual([path.parent.name for path in paths], ["run-a", "run-b"])

    def test_event_consistency_allows_exact_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifests = []
            event = {"event_id": "EA-TEST-2026-0001", "claim": "same"}
            for name in ["run-a", "run-b"]:
                run_dir = root / name
                run_dir.mkdir()
                (run_dir / "evidence.jsonl").write_text(
                    json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8"
                )
                manifest = run_dir / "run.json"
                manifest.write_text(json.dumps({"files": {"evidence": "evidence.jsonl"}}), encoding="utf-8")
                manifests.append(manifest)

            self.assertEqual(validator.event_consistency_problems(manifests), [])

    def test_event_consistency_rejects_conflicting_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifests = []
            for name, claim in [("run-a", "first"), ("run-b", "second")]:
                run_dir = root / name
                run_dir.mkdir()
                (run_dir / "evidence.jsonl").write_text(
                    json.dumps({"event_id": "EA-TEST-2026-0001", "claim": claim}) + "\n",
                    encoding="utf-8",
                )
                manifest = run_dir / "run.json"
                manifest.write_text(json.dumps({"files": {"evidence": "evidence.jsonl"}}), encoding="utf-8")
                manifests.append(manifest)

            problems = validator.event_consistency_problems(manifests)

            self.assertEqual(len(problems), 1)
            self.assertIn("differs between", problems[0])


if __name__ == "__main__":
    unittest.main()

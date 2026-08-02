from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.lib import review_runs


def write_catalog_run(root: Path, name: str, *, status: str = "settled") -> Path:
    run_dir = root / "evidence" / name
    run_dir.mkdir(parents=True)
    for article in review_runs.STANDARD_ARTICLES:
        (run_dir / article).write_text(f"# {name}\n", encoding="utf-8")
    (run_dir / "evidence.jsonl").write_text(
        json.dumps({"event_id": f"EA-{name.upper()}-0001", "claim": name}) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "topic": name,
        "status": status,
        "files": {
            "evidence": "evidence.jsonl",
            "outputs": list(review_runs.STANDARD_ARTICLES),
        },
    }
    run_json = run_dir / "run.json"
    run_json.write_text(json.dumps(manifest), encoding="utf-8")
    return run_json


class ReviewRunsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "knowledge").mkdir()
        (self.root / "evidence").mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write_catalog(self, *targets: str) -> Path:
        catalog = self.root / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "\n".join(f"[run](../evidence/{target}/run.json)" for target in targets),
            encoding="utf-8",
        )
        return catalog

    def test_loader_selects_only_catalog_routed_settled_runs(self) -> None:
        write_catalog_run(self.root, "run-b")
        write_catalog_run(self.root, "run-a")
        write_catalog_run(self.root, "unrouted")
        catalog = self.write_catalog("run-b", "run-a", "run-a")

        loaded = review_runs.load_catalog_runs(self.root, catalog)

        self.assertEqual([item.directory.name for item in loaded], ["run-a", "run-b"])

    def test_loader_rejects_non_settled_current_run(self) -> None:
        write_catalog_run(self.root, "draft", status="in-progress")
        catalog = self.write_catalog("draft")

        with self.assertRaisesRegex(ValueError, "non-settled"):
            review_runs.load_catalog_runs(self.root, catalog)

    def test_loader_rejects_missing_reader_triplet(self) -> None:
        run_json = write_catalog_run(self.root, "incomplete")
        (run_json.parent / review_runs.STANDARD_ARTICLES[-1]).unlink()
        catalog = self.write_catalog("incomplete")

        with self.assertRaisesRegex(ValueError, "missing reader-facing articles"):
            review_runs.load_catalog_runs(self.root, catalog)

    def test_evidence_path_cannot_escape_its_run(self) -> None:
        run_json = write_catalog_run(self.root, "unsafe")
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        manifest["files"]["evidence"] = "../other/evidence.jsonl"

        with self.assertRaisesRegex(ValueError, "escapes run directory"):
            review_runs.evidence_paths(run_json, manifest)

    def test_catalog_route_cannot_escape_evidence_root(self) -> None:
        catalog = self.root / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "[bad](../evidence/../outside/run.json)\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "escapes evidence root"):
            review_runs.catalog_run_paths(self.root, catalog)


if __name__ == "__main__":
    unittest.main()

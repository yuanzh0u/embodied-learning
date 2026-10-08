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

        with self.assertRaisesRegex(ValueError, "missing reader-facing article"):
            review_runs.load_catalog_runs(self.root, catalog)

    def test_loader_accepts_declared_single_scientific_memo(self) -> None:
        run_json = write_catalog_run(self.root, "memo-only")
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        manifest.update(
            {
                "style": "scientific-memo",
                "scope_note": "用户明确只要求科研备忘录",
            }
        )
        manifest["files"]["outputs"] = ["scientific-memo_keyan.md"]
        run_json.write_text(json.dumps(manifest), encoding="utf-8")
        for name in review_runs.STANDARD_ARTICLES[1:]:
            (run_json.parent / name).unlink()
        catalog = self.write_catalog("memo-only")

        loaded = review_runs.load_catalog_runs(self.root, catalog)

        self.assertEqual([item.directory.name for item in loaded], ["memo-only"])
        self.assertEqual(
            review_runs.reader_articles(run_json, manifest),
            ("scientific-memo_keyan.md",),
        )

    def test_loader_rejects_reduced_scope_without_scope_note(self) -> None:
        run_json = write_catalog_run(self.root, "missing-scope-note")
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        manifest["style"] = "scientific-memo"
        manifest["files"]["outputs"] = ["scientific-memo_keyan.md"]
        run_json.write_text(json.dumps(manifest), encoding="utf-8")
        catalog = self.write_catalog("missing-scope-note")

        with self.assertRaisesRegex(ValueError, "requires scope_note"):
            review_runs.load_catalog_runs(self.root, catalog)

    def test_only_explicit_run_links_route_current_versions(self) -> None:
        write_catalog_run(self.root, "current")
        write_catalog_run(self.root, "historical")
        catalog = self.root / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "[run](../evidence/current/run.json)\n"
            "[历史版本](../evidence/historical/run.json)\n",
            encoding="utf-8",
        )

        loaded = review_runs.load_catalog_runs(self.root, catalog)

        self.assertEqual([item.directory.name for item in loaded], ["current"])

    def test_evidence_path_cannot_escape_its_run(self) -> None:
        run_json = write_catalog_run(self.root, "unsafe")
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        manifest["files"]["evidence"] = "../other/evidence.jsonl"

        with self.assertRaisesRegex(ValueError, "escapes run directory"):
            review_runs.evidence_paths(run_json, manifest)

    def test_catalog_route_cannot_escape_evidence_root(self) -> None:
        catalog = self.root / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "[run](../evidence/../outside/run.json)\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "escapes evidence root"):
            review_runs.catalog_run_paths(self.root, catalog)


class RegisterRunInCatalogTest(unittest.TestCase):
    def setUp(self) -> None:
        import os

        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "knowledge").mkdir()
        (self.root / "evidence").mkdir()
        self._env = os.environ.copy()
        os.environ["EMBODIED_KB_LOCK_DIR"] = str(self.root / ".locks")
        catalog = self.root / "knowledge" / "literature-review-catalog.md"
        catalog.write_text(
            "# 文献综述成果目录\n\n## 成果索引\n\n"
            "| ID | 综述主题 | 主要知识卡 | 规模 | 审计入口 |\n|---|---|---|---:|---|\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        import os

        os.environ.clear()
        os.environ.update(self._env)
        self._tmp.cleanup()

    def test_registers_then_is_idempotent(self) -> None:
        run_json = write_catalog_run(self.root, "literature-review-demo-20260922")
        self.assertTrue(review_runs.register_run_in_catalog(self.root, run_json))
        catalog = (self.root / "knowledge" / "literature-review-catalog.md").read_text(encoding="utf-8")
        self.assertIn("../evidence/literature-review-demo-20260922/run.json", catalog)
        # The row joined the existing table (not appended past it).
        lines = catalog.splitlines()
        self.assertTrue(lines[-1].lstrip().startswith("|"))
        # Second call is a no-op.
        self.assertFalse(review_runs.register_run_in_catalog(self.root, run_json))
        self.assertEqual(
            catalog,
            (self.root / "knowledge" / "literature-review-catalog.md").read_text(encoding="utf-8"),
        )

    def test_generated_row_carries_topic_and_cards(self) -> None:
        run_json = write_catalog_run(self.root, "literature-review-demo2-20260922")
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        manifest["knowledge_ids"] = ["EA-DEMO", "EA-DATA"]
        manifest["candidate_count"] = 421
        manifest["full_text_count"] = 40
        manifest["evidence_papers"] = 12
        run_json.write_text(json.dumps(manifest), encoding="utf-8")
        review_runs.register_run_in_catalog(self.root, run_json)
        row = [
            line
            for line in (self.root / "knowledge" / "literature-review-catalog.md")
            .read_text(encoding="utf-8")
            .splitlines()
            if "demo2" in line
        ][0]
        self.assertIn("EA-DEMO、EA-DATA", row)
        # 规模 = 候选池 / 可读全文 / 精读并接纳论文数 (catalog header semantics)
        self.assertIn("421 / 40 / 12", row)

    def test_generated_row_scale_falls_back_to_dashes(self) -> None:
        run_json = write_catalog_run(self.root, "literature-review-demo3-20260922")
        review_runs.register_run_in_catalog(self.root, run_json)
        row = [
            line
            for line in (self.root / "knowledge" / "literature-review-catalog.md")
            .read_text(encoding="utf-8")
            .splitlines()
            if "demo3" in line
        ][0]
        self.assertIn("| — / — / — |", row)


if __name__ == "__main__":
    unittest.main()

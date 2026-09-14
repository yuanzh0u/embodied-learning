"""Tests for scripts/prepare_paper_chat.py — single-paper chat preparation.

Network and the claude CLI are mocked; assertions cover ID normalization,
pool cache hits, the extraction→pool→deep-read chain, and exit-code contract
(0 = pass, 3 = pooled but deep-read incomplete, 1 = failure).
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "prepare_paper_chat.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prepare_paper_chat", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class NormalizeIdTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_accepts_plain_ids_and_strips_versions(self):
        self.assertEqual(self.module.normalize_arxiv_id("2402.10329"), "2402.10329")
        self.assertEqual(self.module.normalize_arxiv_id("2402.10329v3"), "2402.10329")
        self.assertEqual(self.module.normalize_arxiv_id("arXiv:2402.10329"), "2402.10329")
        self.assertEqual(
            self.module.normalize_arxiv_id("https://arxiv.org/abs/2402.10329v1"), "2402.10329"
        )

    def test_rejects_garbage(self):
        for raw in ("", "hello", "2402.103", "2402.103299999"):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    self.module.normalize_arxiv_id(raw)


class PreparePipelineTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kb_root = Path(self.tmp.name) / "kb"
        self.kb_root.mkdir()

    def run_main(self, argv, *, extraction_fails=False, deep_status="pass"):
        """One unified subprocess fake covering every command the script may
        issue: extraction, pool add, the claude skeleton agent, and note
        assembly."""

        def fake_run(command, timeout=0.0, **kwargs):
            joined = " ".join(str(part) for part in command)
            paper_id = argv[argv.index("--arxiv-id") + 1] if "--arxiv-id" in argv else ""
            if "extract_arxiv_content.py" in joined:
                if extraction_fails:
                    return mock.Mock(returncode=1, stdout="", stderr="boom")
                output = Path(command[command.index("-o") + 1])
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps({"paper": {"arxiv_id": paper_id}}), encoding="utf-8")
                return mock.Mock(returncode=0, stdout="", stderr="")
            if "pool_add_paper.py" in joined:
                return mock.Mock(returncode=0, stdout="", stderr="")
            if "build_paper_note.py" in joined:
                pool_dir = self.kb_root / "pool" / f"arxiv-{paper_id}"
                (pool_dir / "note.json").write_text("{}", encoding="utf-8")
                (pool_dir / "note.json.audit.json").write_text(
                    json.dumps({"status": deep_status}), encoding="utf-8"
                )
                return mock.Mock(returncode=0 if deep_status == "pass" else 3,
                                 stdout=json.dumps({"status": deep_status}), stderr="")
            # The skeleton agent is a `claude -p …` call: return a valid skeleton.
            return mock.Mock(returncode=0, stdout=json.dumps({"cards": []}), stderr="")

        with mock.patch.object(self.module.subprocess, "run", side_effect=fake_run), \
             mock.patch.object(self.module, "run", side_effect=fake_run):
            code = self.module.main(argv)
        return code

    def test_cached_paper_short_circuits(self):
        pool_dir = self.kb_root / "pool" / "arxiv-2402.10329"
        pool_dir.mkdir(parents=True)
        (pool_dir / "extraction.json").write_text("{}", encoding="utf-8")
        (pool_dir / "note.json.audit.json").write_text(json.dumps({"status": "pass"}), encoding="utf-8")
        with mock.patch.object(self.module, "ensure_extraction") as extract, \
             mock.patch.object(self.module, "ensure_deep_read", return_value="pass") as deep:
            code = self.run_main(["--arxiv-id", "2402.10329", "--kb-root", str(self.kb_root)])
        self.assertEqual(code, 0)
        extract.assert_called_once()
        deep.assert_called_once()

    def test_extraction_failure_is_exit_1(self):
        code = self.run_main(
            ["--arxiv-id", "2402.10329", "--kb-root", str(self.kb_root)],
            extraction_fails=True,
        )
        self.assertEqual(code, 1)

    def test_deep_read_failed_is_exit_3(self):
        """needs-review still counts as usable (exit 0, mirrors the driver);
        only a hard audit failure degrades to exit 3. Different paper ids per
        call — the pool cache must not leak a prior status into the next."""
        code = self.run_main(
            ["--arxiv-id", "2402.10329", "--kb-root", str(self.kb_root)],
            deep_status="needs-review",
        )
        self.assertEqual(code, 0)
        code = self.run_main(
            ["--arxiv-id", "2501.00001", "--kb-root", str(self.kb_root)],
            deep_status="failed",
        )
        self.assertEqual(code, 3)

    def test_deep_read_pass_is_exit_0(self):
        code = self.run_main(
            ["--arxiv-id", "2402.10329", "--kb-root", str(self.kb_root)],
            deep_status="pass",
        )
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()

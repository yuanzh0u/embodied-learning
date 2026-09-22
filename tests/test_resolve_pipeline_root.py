#!/usr/bin/env python3
"""resolve_pipeline_root candidate ordering: packaged/install layouts only —
no machine-specific path probes."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_serve_research_wiki import server_module


class ResolvePipelineRootTest(unittest.TestCase):
    def setUp(self) -> None:
        # reset the process-lifetime cache and any CLI override around each case
        patches = [
            mock.patch.object(server_module, "_PIPELINE_ROOT_CACHE", server_module._PIPELINE_ROOT_UNSET),
            mock.patch.object(server_module, "PIPELINE_ROOT_OVERRIDE", None),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def test_repo_checkout_wins(self) -> None:
        self.assertEqual(server_module.resolve_pipeline_root(),
                         server_module.REPO_ROOT)

    def test_installed_scripts_dir_candidate(self) -> None:
        # wheel install: SCRIPT_DIR itself holds init_run.py + skills/, and the
        # "repo" next to it resolves to site-packages (no skills tree).
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / "site-packages" / "wiki_scripts"
            skill = pkg / "skills" / "embodied-ai-review-writer"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\n---\n", encoding="utf-8")
            (pkg / "init_run.py").write_text("# stub\n", encoding="utf-8")
            with mock.patch.object(server_module, "REPO_ROOT", Path(tmp) / "site-packages"), \
                 mock.patch.object(server_module, "SCRIPT_DIR", pkg):
                self.assertEqual(server_module.resolve_pipeline_root(), pkg)

    def test_no_machine_specific_probe(self) -> None:
        # the conventional-clone fallback (~/code/embodied-learning) is gone:
        # a bare HOME must not resurrect a workflow root.
        source = Path(server_module.__file__).read_text(encoding="utf-8")
        self.assertNotIn("code/embodied-learning", source.replace("\\", "/"))


if __name__ == "__main__":
    unittest.main()

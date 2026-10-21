"""CLI flag tables live in the dispatchers and are a contract (ADR 0005).

Moving argparse out of the library is not a license to edit flags. Each
subcommand's option strings are pinned here; a diff means either an
unintended flag change or a deliberate one that must update this inventory in
the same review.
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _load(entry: str):
    path = next(
        p for p in [_REPO_ROOT / "scripts" / entry, *_REPO_ROOT.glob(f"skills/*/scripts/{entry}")]
        if p.is_file()
    )
    spec = importlib.util.spec_from_file_location(f"flagtbl_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _options(module, subcommand: str) -> set[str]:
    parser = module._parser_for(subcommand)
    out: set[str] = set()
    for action in parser._actions:
        out.update(action.option_strings)
    return out


class RunFlagTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load("run.py")

    def test_init(self):
        self.assertEqual(_options(self.mod, "init"), {
            "-h", "--help", "--topic", "--knowledge-id", "--time-range",
            "--review-mode", "--date", "--run-version", "--work-dir",
            "--inputs-json", "--force",
        })

    def test_finalize(self):
        self.assertEqual(_options(self.mod, "finalize"), {
            "-h", "--help", "--run-dir", "--kb-root", "--style", "--scope-note",
            "--declare-gate-exception", "--reason", "--skip-wiki",
        })

    def test_pipeline(self):
        self.assertEqual(_options(self.mod, "pipeline"), {
            "-h", "--help", "--run-dir", "--topic", "--review-mode", "--time-range",
            "--focus", "--kb-root", "--search-strategy", "--selection-strategy",
            "--selection-model", "--selection-threshold",
            "--seed-arxiv-ids", "--external-candidates", "--with-s2",
            "--arxiv-snapshot", "--no-terms-agent", "--no-dynamic-agent",
            "--terms-timeout", "--dynamic-timeout", "--s2-budget", "--workers",
            "--force", "--skip-deep-read", "--deep-read-limit", "--agent-timeout",
            "--selection-timeout", "--extraction-timeout", "--agents-parallel",
        })

    def test_launch(self):
        self.assertEqual(_options(self.mod, "launch"), {
            "-h", "--help", "--topic", "--review-mode", "--time-range", "--focus",
            "--search-strategy", "--selection-strategy", "--seed-arxiv-ids",
            "--selection-model", "--selection-threshold",
            "--external-candidates", "--agents-parallel", "--arxiv-snapshot",
            "--kb-root", "--knowledge-id", "--target-style", "--scope-note",
            "--run-dir", "--run-version", "--deep-read-limit", "--mechanical-retries",
            "--max-agent-retries", "--writer-timeout", "--writer-model",
            "--status", "--stop", "--resume",
        })

    def test_status(self):
        self.assertEqual(_options(self.mod, "status"), {"-h", "--help", "--run-dir", "--json"})

    def test_check_bundle(self):
        self.assertEqual(_options(self.mod, "check-bundle"), {"-h", "--help", "--pre-settle"})


class WikiFlagTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load("wiki.py")

    def test_build_wiki(self):
        self.assertEqual(_options(self.mod, "build-wiki"), {
            "-h", "--help", "--source", "--output", "--kb-root", "--site-config",
            "--check", "--activate", "--retain",
        })

    def test_serve(self):
        opts = _options(self.mod, "serve")
        for flag in ("--port", "--open", "--no-refresh", "--close", "--kb-root",
                     "--no-chat", "--chat-cli", "--chat-model", "--pipeline-root",
                     "--workflow-model", "--workflow-effort"):
            self.assertIn(flag, opts)

    def test_kb_stats(self):
        self.assertEqual(_options(self.mod, "kb-stats"), {
            "-h", "--help", "--kb-root", "--json", "--runs-detail",
        })

    def test_kb_search(self):
        self.assertEqual(_options(self.mod, "kb-search"), {
            "-h", "--help", "--scope", "--limit", "--kb-root", "--json",
        })

    def test_kb_funnel(self):
        self.assertEqual(_options(self.mod, "kb-funnel"), {
            "-h", "--help", "--layer", "--kb-root", "--run", "--topic",
            "--review-mode", "--sort", "--limit", "--json",
        })

    def test_kb_merge(self):
        self.assertEqual(_options(self.mod, "kb-merge"), {
            "-h", "--help", "--kb-root", "--source", "--what", "--prefer",
            "--dry-run", "--no-wiki", "--json",
        })


class WriterFlagTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load("write.py")

    def test_audit_article_quality(self):
        opts = _options(self.mod, "audit-article-quality")
        for flag in ("--bundle-dir", "--memo", "--zhihu", "--xiaohongshu",
                     "--quickread", "--evidence-jsonl", "--min-chinese-share", "--json"):
            self.assertIn(flag, opts)

    def test_paper_deck(self):
        self.assertEqual(_options(self.mod, "paper-deck"), {
            "-h", "--help", "--arxiv-id", "--kb-root", "--force",
            "--skip-agent", "--no-audit",
        })

    def test_run_deck(self):
        self.assertEqual(_options(self.mod, "run-deck"), {
            "-h", "--help", "--run-dir", "--skip-agent", "--no-audit", "--force",
        })


class ReaderFlagTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load("read.py")

    def test_prepare_chat(self):
        self.assertEqual(_options(self.mod, "prepare-chat"), {
            "-h", "--help", "--arxiv-id", "--kb-root", "--force",
        })

    def test_quick_read(self):
        opts = _options(self.mod, "quick-read")
        self.assertIn("--arxiv-id", opts)
        self.assertIn("--kb-root", opts)


if __name__ == "__main__":
    unittest.main()

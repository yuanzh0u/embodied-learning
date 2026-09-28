#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "extract_failed_card_window.py"


def load_module():
    spec = importlib.util.spec_from_file_location("extract_failed_card_window", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    # Ensure sibling audit_claim_support / validate_paper_note import paths work
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec.loader.exec_module(module)
    return module


FULL_CONTEXT = (
    "Across three real-robot tasks, the proposed interface improved success rate by 12 percentage "
    "points over Baseline X, but the study did not evaluate deformable objects or long-horizon tasks."
)
FULL_TEXT = (
    "## 1 Introduction\nThis paper studies portable robot demonstrations and states the research problem.\n\n"
    "## 3 Method\nThe system records synchronized camera poses and actions.\n\n"
    "## 4 Experiments\n" + FULL_CONTEXT + " Additional ablations isolate tracking.\n\n"
    "## 6 Limitations\nOnly rigid tabletop manipulation was evaluated.\n"
)


def extraction() -> dict:
    return {
        "paper_id": "2402.10329",
        "extraction_method": "html-latexml",
        "text": FULL_TEXT,
        "sections": [
            {"path": "1 Introduction", "title": "1 Introduction"},
            {"path": "3 Method", "title": "3 Method"},
            {"path": "4 Experiments", "title": "4 Experiments"},
            {"path": "6 Limitations", "title": "6 Limitations"},
        ],
        "ocr": {"pages_used": []},
    }


def failing_audit() -> dict:
    return {
        "schema_version": 1,
        "paper_id": "2402.10329",
        "status": "reject",
        "cards": [
            {
                "card_id": "2402.10329-C01",
                "status": "fail",
                "locator": "4 Experiments",
                "reasons": ["source context is not an exact normalized match"],
            },
            {
                "card_id": "2402.10329-C02",
                "status": "pass",
                "locator": "6 Limitations",
            },
        ],
    }


def note() -> dict:
    return {
        "evidence_cards": [
            {
                "card_id": "2402.10329-C01",
                "claim": "Scoped success-rate improvement under evaluated tasks.",
                "locator": "4 Experiments",
                "source_context": FULL_CONTEXT,
            }
        ]
    }


class ExtractFailedCardWindowTests(unittest.TestCase):
    def test_only_failing_cards_get_windows(self) -> None:
        mod = load_module()
        payload = mod.build_windows(
            failing_audit(), extraction(), note(), radius=500, max_window=2000
        )
        self.assertEqual(payload["failed_card_count"], 1)
        self.assertEqual(len(payload["cards"]), 1)
        card = payload["cards"][0]
        self.assertEqual(card["card_id"], "2402.10329-C01")
        self.assertTrue(card["windows"])
        self.assertIn("Baseline X", card["windows"][0])
        self.assertLessEqual(card["window_chars"], 2000)

    def test_cli_writes_json_and_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "audit.json").write_text(
                json.dumps(failing_audit()), encoding="utf-8"
            )
            (tmp_path / "extraction.json").write_text(
                json.dumps(extraction()), encoding="utf-8"
            )
            (tmp_path / "note.json").write_text(json.dumps(note()), encoding="utf-8")
            out = tmp_path / "windows.json"
            md = tmp_path / "windows.md"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--audit",
                    str(tmp_path / "audit.json"),
                    "--extraction",
                    str(tmp_path / "extraction.json"),
                    "--paper-note",
                    str(tmp_path / "note.json"),
                    "--output",
                    str(out),
                    "--markdown-output",
                    str(md),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["failed_card_count"], 1)
            body = md.read_text(encoding="utf-8")
            self.assertIn("Failed-card retry windows", body)
            self.assertIn("2402.10329-C01", body)


if __name__ == "__main__":
    unittest.main()

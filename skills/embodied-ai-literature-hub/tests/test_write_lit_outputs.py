#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "write_lit_outputs.py"
SPEC = importlib.util.spec_from_file_location("write_lit_outputs", SCRIPT_PATH)
write_lit_outputs = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(write_lit_outputs)


def event_with_authors(authors: list[dict[str, object]]) -> dict[str, object]:
    return {
        "event_id": "EA-DATA-2026-0001",
        "topic_id": "EA-DATA",
        "topic": "UMI data usability",
        "paper": {
            "arxiv_id": "2604.14089",
            "title": "UMI-3D",
            "published": "2026-04-15",
            "url": "https://arxiv.org/abs/2604.14089",
        },
        "authors": authors,
        "claim": "UMI-style data is useful only when collection and deployment conditions align.",
        "stance": "conditional",
        "evidence": {
            "summary": "The paper discusses embodied data collection constraints.",
            "locator": "section 3",
            "evidence_type": "discussion",
        },
        "confidence": "direct",
    }


class WriteLitOutputsTest(unittest.TestCase):
    def test_normalizes_primary_institution_examples(self) -> None:
        cases = {
            "北京大学计算机学院": ("北京大学", "peking-university"),
            "Google DeepMind": ("Google", "google"),
            "Stanford AI Lab": ("Stanford University", "stanford-university"),
            "MIT CSAIL": ("MIT", "mit"),
            "School of Computer Science, Peking University": ("Peking University", "peking-university"),
        }
        for raw_name, expected in cases.items():
            with self.subTest(raw_name=raw_name):
                self.assertEqual(write_lit_outputs.normalize_primary_institution(raw_name), expected)

    def test_loads_old_jsonl_without_institutions(self) -> None:
        event = event_with_authors(
            [
                {
                    "name": "Legacy Author",
                    "author_key": "legacy-author",
                    "role": "paper-author",
                }
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence.jsonl"
            path.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
            events = write_lit_outputs.load_events(path)
        self.assertEqual(events[0]["authors"][0]["institutions"], [])
        brief = write_lit_outputs.render_brief(events)
        self.assertIn("legacy-author [unlisted]", brief)
        self.assertIn("| legacy-author | unlisted |", brief)

    def test_renders_first_level_institutions_in_author_stance_events(self) -> None:
        event = event_with_authors(
            [
                {
                    "name": "UMI Author",
                    "author_key": "umi-author",
                    "role": "paper-author",
                    "institutions": [
                        {
                            "name": "北京大学计算机学院",
                            "institution_key": "peking-university-computer-science",
                            "source": "arxiv-html-author-block",
                            "confidence": "direct",
                        },
                        {
                            "name": "Google DeepMind",
                            "institution_key": "google-deepmind",
                            "source": "arxiv-html-author-block",
                            "confidence": "direct",
                        },
                    ],
                }
            ]
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence.jsonl"
            path.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
            events = write_lit_outputs.load_events(path)
        institutions = events[0]["authors"][0]["institutions"]
        self.assertEqual(
            [(item["name"], item["institution_key"]) for item in institutions],
            [("北京大学", "peking-university"), ("Google", "google")],
        )
        brief = write_lit_outputs.render_brief(events)
        self.assertIn("umi-author [北京大学; Google]", brief)
        self.assertIn("| umi-author | 北京大学; Google |", brief)
        self.assertNotIn("Google DeepMind", brief)
        self.assertNotIn("计算机学院", brief)

    def test_rejects_ocr_evidence_until_visual_validation_passes(self) -> None:
        event = event_with_authors(
            [{"name": "OCR Author", "author_key": "ocr-author", "role": "paper-author"}]
        )
        event["evidence"]["extraction"] = {  # type: ignore[index]
            "source_format": "pdf",
            "method": "pdf-ocr",
            "quality": "medium",
            "visual_validation": "required",
            "visual_validation_pages": [2, 3],
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "evidence.jsonl"
            path.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "requires visual validation"):
                write_lit_outputs.load_events(path)

            event["evidence"]["extraction"]["visual_validation"] = "passed"  # type: ignore[index]
            path.write_text(json.dumps(event, ensure_ascii=False) + "\n", encoding="utf-8")
            events = write_lit_outputs.load_events(path)
        self.assertEqual("pdf-ocr", events[0]["evidence"]["extraction"]["method"])


if __name__ == "__main__":
    unittest.main()

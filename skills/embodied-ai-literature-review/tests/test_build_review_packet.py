#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-literature-review" / "scripts" / "build_review_packet.py"
SPEC = importlib.util.spec_from_file_location("build_review_packet", SCRIPT)
build_review_packet = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(build_review_packet)


def sample_event(event_id: str, stance: str) -> dict[str, object]:
    return {
        "event_id": event_id,
        "topic_id": "EA-DATA",
        "topic": "UMI data usability",
        "paper": {
            "arxiv_id": "2604.14089",
            "title": "UMI-3D",
            "published": "2026-04-15",
            "url": "https://arxiv.org/abs/2604.14089",
        },
        "authors": [
            {
                "name": "UMI Author",
                "author_key": "umi-author",
                "role": "paper-author",
                "institutions": [{"name": "Peking University", "institution_key": "peking-university"}],
            }
        ],
        "claim": f"UMI evidence has a {stance} stance for data usability.",
        "stance": stance,
        "evidence": {
            "summary": "The paper discusses embodied data collection constraints.",
            "locator": "section 3",
            "evidence_type": "discussion",
        },
        "confidence": "direct",
    }


def event_for_paper(event_id: str, arxiv_id: str) -> dict[str, object]:
    event = sample_event(event_id, "support")
    paper = dict(event["paper"])  # type: ignore[index]
    paper["arxiv_id"] = arxiv_id
    paper["title"] = f"Paper {arxiv_id}"
    event["paper"] = paper
    return event


class BuildReviewPacketTests(unittest.TestCase):
    def test_skill_docs_describe_review_orchestration_and_styles(self) -> None:
        skill_doc = (ROOT / "skills" / "embodied-ai-literature-review" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("planner -> hub -> review packet -> style menu", skill_doc)
        self.assertIn("5 paper-level sources", skill_doc)
        self.assertIn("scientific-memo", skill_doc)
        self.assertIn("expert-explainer", skill_doc)
        self.assertIn("kol-thread", skill_doc)

    def test_render_packet_preserves_event_traceability_and_stances(self) -> None:
        events = [sample_event("EA-DATA-2026-0001", "support"), sample_event("EA-DATA-2026-0002", "gap")]
        cards = [
            {
                "path": "knowledge/embodied-ai/data-collection-quality.md",
                "id": "EA-DATA",
                "title": "数据采集与数据质量",
                "summary": "数据质量最终要通过目标策略闭环收益验证。",
                "judgments": ["自然场景数据决定跨场景和长尾泛化。"],
            }
        ]

        packet = build_review_packet.render_packet(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            cards,
            ["S-EA-QUESTIONS"],
            "survey",
        )

        self.assertIn("EA-DATA-2026-0001", packet)
        self.assertIn("EA-DATA-2026-0002", packet)
        self.assertIn("`support`", packet)
        self.assertIn("`gap`", packet)
        self.assertIn("S-EA-QUESTIONS", packet)
        self.assertIn("数据采集与数据质量", packet)
        self.assertIn("Traceability Checklist", packet)

    def test_cli_writes_packet_from_jsonl_and_topic_card(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evidence = tmp / "evidence.jsonl"
            evidence.write_text(json.dumps(sample_event("EA-DATA-2026-0001", "conditional"), ensure_ascii=False) + "\n", encoding="utf-8")
            topic_card = tmp / "card.md"
            topic_card.write_text(
                """---
id: EA-DATA
title: 数据采集与数据质量
---

# 数据采集与数据质量

## 30 秒摘要

数据采集不是单纯堆轨迹。

## 关键判断

- 数据质量最终要通过闭环收益验证。
""",
                encoding="utf-8",
            )
            output = tmp / "packet.md"

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--knowledge-id",
                    "EA-DATA",
                    "--evidence-jsonl",
                    str(evidence),
                    "--topic-card",
                    str(topic_card),
                    "--output",
                    str(output),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            packet = output.read_text(encoding="utf-8")
            self.assertIn("Review Packet: UMI 数据可用性", packet)
            self.assertIn("EA-DATA-2026-0001", packet)
            self.assertIn("条件成立", packet)
            self.assertIn("数据质量最终要通过闭环收益验证", packet)

    def test_packet_declares_upstream_orchestration_contract(self) -> None:
        packet = build_review_packet.render_packet(
            "VLA 的数据金字塔",
            ["EA-MODEL"],
            [],
            [],
            [],
            "survey",
        )

        self.assertIn("planner -> hub -> review packet -> style menu", packet)
        self.assertIn("$embodied-ai-query-planner", packet)
        self.assertIn("$embodied-ai-literature-hub", packet)
        self.assertIn("not a replacement", packet)

    def test_packet_exposes_evidence_core_and_source_gaps(self) -> None:
        events = [
            sample_event("EA-DATA-2026-0001", "support"),
            {
                **sample_event("EA-DATA-2026-0002", "limit"),
                "confidence": "inference",
            },
        ]

        packet = build_review_packet.render_packet(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "survey",
        )

        self.assertIn("## Evidence Core", packet)
        self.assertIn("Stance labels: `limit`, `support`", packet)
        self.assertIn("Confidence labels: `direct`, `inference`", packet)
        self.assertIn("Trace IDs: `EA-DATA-2026-0001`, `EA-DATA-2026-0002`", packet)
        self.assertIn("## Source Gaps", packet)
        self.assertIn("No registered source file was loaded", packet)

    def test_packet_marks_preliminary_when_paper_level_sources_are_below_threshold(self) -> None:
        events = [
            event_for_paper("EA-DATA-2026-0001", "2601.00001"),
            event_for_paper("EA-DATA-2026-0002", "2601.00002"),
            event_for_paper("EA-DATA-2026-0003", "2601.00003"),
        ]

        packet = build_review_packet.render_packet(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            ["S-ARXIV-2601-00001"],
            "survey",
        )

        self.assertIn("Evidence sufficiency: preliminary", packet)
        self.assertIn("Paper-level sources: 3 / 5", packet)
        self.assertIn("Formal outputs are blocked until at least 5 paper-level sources are available.", packet)

    def test_packet_includes_style_menu_when_sources_are_sufficient(self) -> None:
        events = [
            event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}")
            for index in range(1, 6)
        ]

        packet = build_review_packet.render_packet(
            "VLA 的数据金字塔",
            ["EA-MODEL"],
            events,
            [],
            ["S-ARXIV-2601-00001"],
            "survey",
        )

        self.assertIn("## Style Menu", packet)
        self.assertIn("Recommended default: scientific-memo", packet)
        self.assertIn("Scientific memo preview:", packet)
        self.assertIn("Expert explainer preview:", packet)
        self.assertIn("KOL thread preview:", packet)

    def test_cli_can_render_scientific_memo_from_sufficient_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evidence = tmp / "evidence.jsonl"
            events = [
                event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}")
                for index in range(1, 6)
            ]
            evidence.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--knowledge-id",
                    "EA-DATA",
                    "--evidence-jsonl",
                    str(evidence),
                    "--style",
                    "scientific-memo",
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertIn("# UMI 数据可用性研究备忘录", completed.stdout)
        self.assertIn("## Claim Map", completed.stdout)
        self.assertIn("## 研究启发与开放问题", completed.stdout)
        self.assertIn("EA-DATA-2026-0001", completed.stdout)

    def test_cli_can_render_expert_explainer_from_sufficient_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evidence = tmp / "evidence.jsonl"
            events = [
                event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}")
                for index in range(1, 6)
            ]
            events[1]["stance"] = "limit"
            evidence.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--knowledge-id",
                    "EA-DATA",
                    "--evidence-jsonl",
                    str(evidence),
                    "--style",
                    "expert-explainer",
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertIn("# UMI 数据可用性：专家解释帖", completed.stdout)
        self.assertIn("## TL;DR", completed.stdout)
        self.assertIn("## 常见误区或争议", completed.stdout)
        self.assertIn("## 证据与限制", completed.stdout)
        self.assertIn("## 延伸阅读与可信度", completed.stdout)
        self.assertIn("EA-DATA-2026-0002", completed.stdout)

    def test_cli_can_render_kol_thread_without_upgrading_conditional_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evidence = tmp / "evidence.jsonl"
            events = [
                event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}")
                for index in range(1, 6)
            ]
            events[0]["stance"] = "conditional"
            events[0]["claim"] = "UMI-style data helps only when collection and deployment conditions align."
            evidence.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--knowledge-id",
                    "EA-DATA",
                    "--evidence-jsonl",
                    str(evidence),
                    "--style",
                    "kol-thread",
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertIn("# UMI 数据可用性：洞察短串", completed.stdout)
        self.assertIn("## Hook", completed.stdout)
        self.assertIn("## 证据约束洞察", completed.stdout)
        self.assertIn("## 边界提醒", completed.stdout)
        self.assertIn("## 依据来源", completed.stdout)
        self.assertIn("conditional", completed.stdout)
        self.assertIn("only when collection and deployment conditions align", completed.stdout)

    def test_cli_renders_fallback_source_tiers_as_preliminary_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fallback_sources = tmp / "fallback-sources.json"
            fallback_sources.write_text(
                json.dumps(
                    [
                        {"title": "Paper source", "url": "https://arxiv.org/abs/2601.00001", "tier": "paper-level"},
                        {"title": "Project page", "url": "https://example.com/project", "tier": "official-context"},
                        {"title": "Discussion thread", "url": "https://reddit.com/r/robotics/example", "tier": "social-calibration"},
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--knowledge-id",
                    "EA-DATA",
                    "--time-range",
                    "2024-01-01..2026-06-11",
                    "--fallback-source-json",
                    str(fallback_sources),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertIn("Evidence sufficiency: preliminary", completed.stdout)
        self.assertIn("## Source Tiers", completed.stdout)
        self.assertIn("### paper-level", completed.stdout)
        self.assertIn("Paper source", completed.stdout)
        self.assertIn("### social-calibration", completed.stdout)
        self.assertIn("Discussion thread", completed.stdout)
        self.assertIn("Fallback sources are review-packet context, not Hub evidence JSONL.", completed.stdout)
        self.assertIn("Paper-level sources: 1 / 5", completed.stdout)
        self.assertNotIn("Paper-level sources: 0 / 5", completed.stdout)

    def test_style_request_with_only_fallback_sources_still_degrades_to_packet_with_tiers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fallback_sources = tmp / "fallback-sources.json"
            fallback_sources.write_text(
                json.dumps(
                    [{"title": "Paper source", "url": "https://arxiv.org/abs/2601.00001", "tier": "paper-level"}],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--knowledge-id",
                    "EA-DATA",
                    "--time-range",
                    "2024-01-01..2026-06-11",
                    "--fallback-source-json",
                    str(fallback_sources),
                    "--style",
                    "kol-thread",
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertIn("# Review Packet: UMI 数据可用性", completed.stdout)
        self.assertIn("### paper-level", completed.stdout)
        self.assertIn("Paper source", completed.stdout)

    def test_fallback_sources_require_time_range(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fallback_sources = tmp / "fallback-sources.json"
            fallback_sources.write_text("[]", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--fallback-source-json",
                    str(fallback_sources),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("--time-range is required", completed.stderr)


if __name__ == "__main__":
    unittest.main()

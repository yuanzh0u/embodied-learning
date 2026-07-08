#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date
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
    def test_skill_docs_describe_default_readable_markdown_and_styles(self) -> None:
        skill_doc = (ROOT / "skills" / "embodied-ai-literature-review" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("planner -> hub -> review packet -> style menu", skill_doc)
        self.assertIn("Default final deliverable", skill_doc)
        self.assertIn("readable Markdown", skill_doc)
        self.assertIn("three Markdown files", skill_doc)
        self.assertIn("scientific-memo_keyan.md", skill_doc)
        self.assertIn("zhihu-explainer_zhihu.md", skill_doc)
        self.assertIn("xiaohongshu-post_xiaohongshu.md", skill_doc)
        self.assertIn("If no time range is provided, default to the most recent six months.", skill_doc)
        self.assertIn("work/", skill_doc)
        self.assertIn("5 paper-level sources", skill_doc)
        self.assertIn("scientific-memo", skill_doc)
        self.assertIn("expert-explainer", skill_doc)
        self.assertIn("kol-thread", skill_doc)

    def test_default_time_range_is_recent_half_year(self) -> None:
        self.assertEqual(
            "2025-12-12..2026-06-12",
            build_review_packet.default_time_range(date(2026, 6, 12)),
        )

    def test_default_time_range_clamps_month_end(self) -> None:
        self.assertEqual(
            "2025-09-30..2026-03-31",
            build_review_packet.default_time_range(date(2026, 3, 31)),
        )

    def test_style_filenames_use_three_default_deliverable_names(self) -> None:
        self.assertEqual("scientific-memo_keyan.md", build_review_packet.artifact_filename("scientific-memo"))
        self.assertEqual("zhihu-explainer_zhihu.md", build_review_packet.artifact_filename("expert-explainer"))
        self.assertEqual("xiaohongshu-post_xiaohongshu.md", build_review_packet.artifact_filename("kol-thread"))

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

    def test_cli_writes_packet_from_jsonl_and_topic_card_when_survey_is_explicit(self) -> None:
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
                    "--style",
                    "survey",
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

    def test_cli_can_render_readable_expert_explainer_markdown_to_stdout(self) -> None:
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
                    "expert-explainer",
                    "--output",
                    "-",
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
        self.assertNotIn("# Review Packet:", completed.stdout)

    def test_cli_default_output_writes_three_markdown_files_into_work_project_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            work_dir = tmp / "work"
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
                    "--work-dir",
                    str(work_dir),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            prefix = "Wrote Markdown artifacts:"
            self.assertTrue(completed.stdout.startswith(prefix))
            artifact_paths = [
                Path(line[2:])
                for line in completed.stdout.splitlines()[1:]
                if line.startswith("- ")
            ]
            self.assertEqual(4, len(artifact_paths))
            for artifact_path in artifact_paths:
                self.assertTrue(artifact_path.exists())
                self.assertEqual(work_dir, artifact_path.parent.parent)
                self.assertTrue(artifact_path.parent.name.startswith("literature-review-umi-数据可用性-"))
            names = {artifact_path.name for artifact_path in artifact_paths}
            self.assertEqual(
                {
                    "scientific-memo_keyan.md",
                    "zhihu-explainer_zhihu.md",
                    "xiaohongshu-post_xiaohongshu.md",
                    "evidence-appendix.md",
                },
                names,
            )
            by_name = {artifact_path.name: artifact_path.read_text(encoding="utf-8") for artifact_path in artifact_paths}
            self.assertIn("# UMI 数据可用性研究备忘录", by_name["scientific-memo_keyan.md"])
            self.assertIn("# UMI 数据可用性：专家解释帖", by_name["zhihu-explainer_zhihu.md"])
            self.assertIn("# UMI 数据可用性：洞察短串", by_name["xiaohongshu-post_xiaohongshu.md"])
            self.assertIn("# Evidence Appendix: UMI 数据可用性", by_name["evidence-appendix.md"])

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
        self.assertIn("Recommended default: all", packet)
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
                    "--output",
                    "-",
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
                    "--output",
                    "-",
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
                    "--output",
                    "-",
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
                    "--output",
                    "-",
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
                    "--output",
                    "-",
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertIn("# Review Packet: UMI 数据可用性", completed.stdout)
        self.assertIn("### paper-level", completed.stdout)
        self.assertIn("Paper source", completed.stdout)

    def test_fallback_sources_use_default_recent_half_year_when_time_range_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fallback_sources = tmp / "fallback-sources.json"
            fallback_sources.write_text("[]", encoding="utf-8")
            expected_time_range = build_review_packet.default_time_range()

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--topic",
                    "UMI 数据可用性",
                    "--fallback-source-json",
                    str(fallback_sources),
                    "--style",
                    "survey",
                    "--output",
                    "-",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

        self.assertEqual(0, completed.returncode)
        self.assertIn(f"Time range: {expected_time_range}", completed.stdout)

    def test_formal_outputs_link_event_ids_and_papers(self) -> None:
        events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 6)]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
        )

        self.assertIn("evidence-appendix.md", artifacts)
        for name in ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"]:
            content = artifacts[name]
            # Every in-text event ID must be a link into the appendix.
            for match in re.finditer(r"EA-DATA-2026-\d{4}", content):
                start = match.start()
                self.assertEqual("[", content[start - 1], f"{name}: bare event ID at offset {start}")
            self.assertIn("(evidence-appendix.md#", content)
            # References section with https links is mandatory in formal outputs.
            self.assertIn("## References", content)
            self.assertIn("https://arxiv.org/abs/2601.00001", content)

    def test_claim_map_paper_column_links_to_arxiv(self) -> None:
        events = [event_for_paper("EA-DATA-2026-0001", "2601.00001")]
        claim_map = build_review_packet.render_claim_map(events, linked=True)
        self.assertIn("[2601.00001](https://arxiv.org/abs/2601.00001)", claim_map)
        self.assertIn("[EA-DATA-2026-0001](evidence-appendix.md#ea-data-2026-0001)", claim_map)

    def test_appendix_anchors_align_with_event_links(self) -> None:
        events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 6)]
        appendix = build_review_packet.render_evidence_appendix("UMI 数据可用性", events)
        for event in events:
            event_id = str(event["event_id"])
            anchor = build_review_packet.event_anchor(event_id)
            self.assertIn(f"### {event_id}", appendix)
            self.assertEqual(anchor, build_review_packet.event_anchor(event_id))
            # GitHub-style anchor derived from the heading must equal the link target.
            heading_anchor = re.sub(r"[^0-9a-z一-鿿-]", "", event_id.lower().replace(" ", "-"))
            self.assertEqual(heading_anchor, anchor)
        self.assertIn("## References", appendix)

    def test_references_deduplicate_papers_across_events(self) -> None:
        events = [
            event_for_paper("EA-DATA-2026-0001", "2601.00001"),
            event_for_paper("EA-DATA-2026-0002", "2601.00001"),
            event_for_paper("EA-DATA-2026-0003", "2601.00002"),
        ]
        references = build_review_packet.render_references(events)
        self.assertEqual(1, references.count("https://arxiv.org/abs/2601.00001"))
        self.assertEqual(1, references.count("https://arxiv.org/abs/2601.00002"))

    def test_preliminary_outputs_do_not_emit_appendix(self) -> None:
        events = [event_for_paper("EA-DATA-2026-0001", "2601.00001")]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
        )
        self.assertNotIn("evidence-appendix.md", artifacts)


if __name__ == "__main__":
    unittest.main()

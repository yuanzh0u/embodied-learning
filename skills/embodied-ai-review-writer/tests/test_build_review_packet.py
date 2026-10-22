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
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# Implementation module (not the scripts/ forwarder) so mock.patch and
# underscore helpers resolve against the live namespace.
import importlib
build_review_packet = importlib.import_module("embodied_learning.writer.packet")
# The CLI is still exercised through the path-stable entry (forwarder).
SCRIPT = Path(__file__).resolve().parents[3] / "skills/embodied-ai-review-writer/scripts/write.py"  # subcommand: review-packet
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


FIGURE = {
    "figure_id": "S3.F3",
    "caption": "The Aria device used for egocentric recordings.",
    "image_url": "https://arxiv.org/html/2604.14089v1/figs/aria.png",
    "section": "3 Setup",
    "usage": "作者用该图展示采集 rig。",
}
TABLE = {
    "table_id": "S1.T1",
    "caption": "Dataset comparison.",
    "section": "3 Setup",
    "rows": [["Dataset", "Year"], ["Ego-Exo4D", "2023"]],
    "usage": "作者用该表对比数据集。",
}


def event_with_figures(event_id: str) -> dict[str, object]:
    event = sample_event(event_id, "support")
    event["evidence"] = {  # type: ignore[index]
        **event["evidence"],  # type: ignore[index]
        "figures": [FIGURE],
        "tables": [TABLE],
    }
    return event


class FigureSurfaceTests(unittest.TestCase):
    """evidence.figures/tables render into the appendix and the writing
    brief's 可用图表 section, so the deliverables actually embed images."""

    def test_appendix_renders_figure_and_table_blocks(self) -> None:
        markdown = build_review_packet.render_evidence_appendix(
            "demo", [event_with_figures("EA-DATA-2026-0001")], "2026-01-01..2026-06-01"
        )
        self.assertIn(f"![{FIGURE['caption']}]({FIGURE['image_url']})", markdown)
        self.assertIn(f"> 用法：{FIGURE['usage']}（UMI-3D（arXiv 2604.14089），S3.F3）", markdown)
        self.assertIn("| Dataset | Year |", markdown)
        self.assertIn(f"> 用法：{TABLE['usage']}（UMI-3D（arXiv 2604.14089），S1.T1）", markdown)

    def test_appendix_without_visuals_stays_clean(self) -> None:
        markdown = build_review_packet.render_evidence_appendix(
            "demo", [sample_event("EA-DATA-2026-0002", "support")], None
        )
        self.assertNotIn("![", markdown)

    def test_brief_lists_available_visuals_with_caps(self) -> None:
        events = [event_with_figures("EA-DATA-2026-0001"), sample_event("EA-DATA-2026-0002", "limit")]
        brief = build_review_packet.render_writing_brief(
            "demo topic", ["EA-DATA"], events, ["src-arxiv"]
        )
        self.assertIn("## 可用图表", brief)
        self.assertIn("科研备忘录 ≤4 图 + 1 表", brief)
        self.assertIn(f"![{FIGURE['caption']}]({FIGURE['image_url']})", brief)
        self.assertIn("EA-DATA-2026-0001", brief)
        # The empty case tells the writer to stay text-only, not to invent images.
        empty = build_review_packet.render_writing_brief(
            "demo topic", ["EA-DATA"], [sample_event("EA-DATA-2026-0003", "support")], ["src-arxiv"]
        )
        self.assertIn("没有携带可用图表", empty)
        self.assertIn("不要自造图片", empty)


class BuildReviewPacketTests(unittest.TestCase):
    def test_style_contract_teaches_zhihu_style_gates_up_front(self):
        """The brief's contract section carries the editorial standards the
        first draft must meet — including the zhihu sentence-length /
        acronym-load / body-citation rules whose violations used to be
        discovered only at audit time (2026-09-30 absolute-pose)."""
        lines = "\n".join(build_review_packet.render_style_contract())
        self.assertIn("## 各风格写作契约", lines)
        self.assertIn("单句不超过 70 个中文字符", lines)
        self.assertIn("缩写不超过 5 个", lines)
        self.assertIn("3–12 篇", lines)

    def test_skill_docs_describe_default_readable_markdown_and_styles(self) -> None:
        skill_doc = (ROOT / "skills" / "embodied-ai-review-writer" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("review mode -> planner -> candidate registry -> coverage/saturation", skill_doc)
        self.assertIn("HTML/PDF recovery -> $embodied-ai-paper-reader -> review packet -> writing brief -> $embodied-ai-review-writer", skill_doc)
        self.assertIn("Default final deliverable", skill_doc)
        self.assertIn("validated writing inputs", skill_doc)
        self.assertIn("three Markdown files", skill_doc)
        self.assertIn("scientific-memo_keyan.md", skill_doc)
        self.assertIn("zhihu-explainer_zhihu.md", skill_doc)
        self.assertIn("xiaohongshu-post_xiaohongshu.md", skill_doc)
        self.assertIn("If no time range is provided, default to the most recent six months.", skill_doc)
        self.assertIn("work/", skill_doc)
        self.assertIn("`rapid` 8, `scoping` 15, `systematic` 30", skill_doc)
        self.assertIn("scientific-memo", skill_doc)
        self.assertIn("expert-explainer", skill_doc)
        self.assertIn("kol-thread", skill_doc)
        self.assertIn("$embodied-ai-review-writer", skill_doc)
        self.assertIn("write.py audit-article-quality", skill_doc)

    def test_default_time_range_is_recent_half_year(self) -> None:
        self.assertEqual(
            "2025-12-12..2026-06-12",
            build_review_packet.default_time_range(date(2026, 6, 12)),
        )

    def test_reading_summary_gate_requires_verified_projected_events(self) -> None:
        events = [event_for_paper("EA-DATA-2026-0001", "2601.00001")]
        coverage = {"stop_assessment": {"ready_to_stop": True, "unresolved": []}}
        summary = {
            "full_text_recovered_count": 8,
            "map_read_count": 8,
            "deep_read_count": 8,
            "claim_verified_paper_count": 8,
            "accepted_evidence_paper_count": 8,
        }
        blocked = build_review_packet.apply_reading_gate(events, "rapid", coverage, summary)
        self.assertFalse(blocked["stop_assessment"]["ready_to_stop"])
        self.assertIn("unverified-paper-reading-events:1", blocked["stop_assessment"]["unresolved"])
        events[0]["paper_reading"] = {"claim_support_audit": "pass"}
        passed = build_review_packet.apply_reading_gate(events, "rapid", coverage, summary)
        self.assertTrue(passed["stop_assessment"]["ready_to_stop"])
        self.assertTrue(passed["paper_reading"]["ready"])

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
                    "review-packet",
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
                    "review-packet",
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
                    "review-packet",
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
            self.assertEqual(3, len(artifact_paths))
            for artifact_path in artifact_paths:
                self.assertTrue(artifact_path.exists())
                self.assertEqual(work_dir, artifact_path.parent.parent)
                self.assertTrue(artifact_path.parent.name.startswith("literature-review-umi-数据可用性-"))
            names = {artifact_path.name for artifact_path in artifact_paths}
            # Briefing bundle only: the prose articles are written by the agent, not the script.
            self.assertEqual({"review-packet.md", "writing-brief.md", "evidence-appendix.md"}, names)
            by_name = {artifact_path.name: artifact_path.read_text(encoding="utf-8") for artifact_path in artifact_paths}
            self.assertIn("# Review Packet: UMI 数据可用性", by_name["review-packet.md"])
            self.assertIn("# Writing Brief: UMI 数据可用性", by_name["writing-brief.md"])
            self.assertIn("写作输入,不是交付物", by_name["writing-brief.md"])
            self.assertIn("# Evidence Appendix: UMI 数据可用性", by_name["evidence-appendix.md"])
            # The script must remind the agent that prose writing is still pending.
            self.assertIn("NEXT", completed.stdout)
            for legacy_name in ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"]:
                self.assertNotIn(legacy_name, names)

    def test_packet_declares_upstream_orchestration_contract(self) -> None:
        packet = build_review_packet.render_packet(
            "VLA 的数据金字塔",
            ["EA-MODEL"],
            [],
            [],
            [],
            "survey",
        )

        self.assertIn("review mode -> planner -> candidate registry -> coverage/saturation", packet)
        self.assertIn("complete HTML/text-layer-PDF recovery", packet)
        self.assertIn("$embodied-ai-paper-reader", packet)
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
        self.assertIn("Formal outputs are blocked until the paper floor and every coverage/saturation check pass.", packet)

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

    def test_run_dir_without_evidence_flag_autoloads_run_manifest_evidence(self) -> None:
        """--run-dir alone must auto-load run.json files.evidence: the bare
        --run-dir invocation used to render an EMPTY packet and exit 0
        (20260929 图像粗配准 stale-appendix chase)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            run_dir = tmp / "work" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            (run_dir / "evidence.jsonl").write_text(
                "".join(
                    json.dumps(event_for_paper(f"EA-DATA-2026-{index:04d}", f"2601.{index:05d}")) + "\n"
                    for index in range(1, 4)
                ),
                encoding="utf-8",
            )
            (run_dir / "run.json").write_text(
                json.dumps({"files": {"evidence": "evidence.jsonl"}}), encoding="utf-8"
            )

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "review-packet", "--topic", "UMI", "--run-dir", str(run_dir),
                 "--output", "-"],
                cwd=ROOT, text=True, capture_output=True,
            )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("EA-DATA-2026-0003", completed.stdout)

    def test_zero_events_without_fallback_refuses_to_render(self) -> None:
        """An empty packet renders placeholders and exits 0; the writer then
        writes from nothing. Refuse next to the cause instead."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evidence = tmp / "empty.jsonl"
            evidence.write_text("", encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "review-packet", "--topic", "UMI", "--evidence-jsonl", str(evidence),
                 "--style", "survey", "--output", "-"],
                cwd=ROOT, text=True, capture_output=True,
            )

        self.assertEqual(2, completed.returncode)
        self.assertIn("拒绝渲染空综述包", completed.stderr)

    def test_new_cli_flow_requires_coverage_report_not_only_paper_count(self) -> None:
        events = [
            event_for_paper(f"EA-DATA-2026-{index:04d}", f"2601.{index:05d}")
            for index in range(1, 16)
        ]
        blocked = build_review_packet.render_writing_brief(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            "2025-01-01..2026-01-01",
            [],
            "scoping",
            None,
        )
        ready = build_review_packet.render_writing_brief(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            "2025-01-01..2026-01-01",
            [],
            "scoping",
            {"stop_assessment": {"ready_to_stop": True, "unresolved": []}},
        )

        self.assertIn("Writing readiness: preliminary", blocked)
        self.assertIn("coverage-report-missing", blocked)
        self.assertIn("Writing readiness: formal-ready", ready)
        self.assertIn("15 / 10 floor (not a cap)", ready)

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
                    "review-packet",
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
                    "review-packet",
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
                    "review-packet",
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
                    "review-packet",
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
        self.assertIn("Paper-level sources: 1 / 10 floor (not a cap)", completed.stdout)
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
                    "review-packet",
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
                    "review-packet",
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

    def test_default_bundle_is_briefing_not_articles(self) -> None:
        events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 6)]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
        )

        self.assertEqual({"review-packet.md", "writing-brief.md", "evidence-appendix.md"}, set(artifacts))
        brief = artifacts["writing-brief.md"]
        self.assertIn("写作输入,不是交付物", brief)
        self.assertIn("中心论点候选", brief)
        self.assertIn("(evidence-appendix.md#", brief)
        self.assertIn("## References", artifacts["evidence-appendix.md"])

    def test_emit_scaffold_adds_bannered_scaffold_files(self) -> None:
        events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 6)]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
            emit_scaffold=True,
        )

        for name in [
            "scientific-memo_keyan.scaffold.md",
            "zhihu-explainer_zhihu.scaffold.md",
            "xiaohongshu-post_xiaohongshu.scaffold.md",
        ]:
            self.assertIn(name, artifacts)
            content = artifacts[name]
            self.assertIn("本文件不是综述成稿", content)
            # Scaffold keeps the link contract: linked event IDs and References.
            self.assertIn("(evidence-appendix.md#", content)
            self.assertIn("## References", content)
        # Finished-article filenames must never be produced by the script.
        for legacy_name in ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"]:
            self.assertNotIn(legacy_name, artifacts)

    def test_explicit_formal_style_emits_scaffold_not_article(self) -> None:
        events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 6)]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "scientific-memo",
        )
        self.assertIn("scientific-memo_keyan.scaffold.md", artifacts)
        self.assertNotIn("scientific-memo_keyan.md", artifacts)
        self.assertIn("writing-brief.md", artifacts)
        self.assertIn("evidence-appendix.md", artifacts)

    def test_load_events_deduplicates_across_files_by_event_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            run_a = tmp / "run-a.jsonl"
            run_b = tmp / "run-b.jsonl"
            shared = event_for_paper("EA-DATA-2026-0001", "2601.00001")
            only_b = event_for_paper("EA-DATA-2026-0002", "2601.00002")
            run_a.write_text(json.dumps(shared, ensure_ascii=False) + "\n", encoding="utf-8")
            run_b.write_text(
                json.dumps(shared, ensure_ascii=False) + "\n" + json.dumps(only_b, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            events = build_review_packet.load_events([run_a, run_b])
        self.assertEqual(["EA-DATA-2026-0001", "EA-DATA-2026-0002"], [event["event_id"] for event in events])
        # First occurrence wins: the shared event keeps run-a provenance.
        self.assertEqual(str(run_a), events[0]["_input_file"])

    def test_select_events_filters_and_rejects_unknown_ids(self) -> None:
        events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 4)]
        picked = build_review_packet.select_events(events, ["EA-DATA-2026-0003", "EA-DATA-2026-0001"])
        self.assertEqual(["EA-DATA-2026-0003", "EA-DATA-2026-0001"], [event["event_id"] for event in picked])
        with self.assertRaises(ValueError) as ctx:
            build_review_packet.select_events(events, ["EA-DATA-2026-9999"])
        self.assertIn("EA-DATA-2026-9999", str(ctx.exception))

    def test_selection_file_accepts_lines_and_json_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            lines_file = tmp / "ids.txt"
            lines_file.write_text("EA-DATA-2026-0001\n\nEA-DATA-2026-0002\n", encoding="utf-8")
            json_file = tmp / "ids.json"
            json_file.write_text('["EA-DATA-2026-0002", "EA-DATA-2026-0003"]', encoding="utf-8")
            ids = build_review_packet.load_selection_ids(["EA-DATA-2026-0000"], [lines_file, json_file])
        self.assertEqual(
            ["EA-DATA-2026-0000", "EA-DATA-2026-0001", "EA-DATA-2026-0002", "EA-DATA-2026-0003"],
            ids,
        )

    def test_cli_select_and_consolidate_writes_local_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            evidence = tmp / "prior-run.jsonl"
            events = [event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}") for index in range(1, 7)]
            evidence.write_text(
                "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
                encoding="utf-8",
            )
            out_dir = tmp / "out"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "review-packet",
                        "--topic",
                    "感知误差溯源",
                    "--knowledge-id",
                    "EA-DATA",
                    "--evidence-jsonl",
                    str(evidence),
                    "--select-event",
                    "EA-DATA-2026-0002",
                    "--select-event",
                    "EA-DATA-2026-0005",
                    "--consolidate-evidence",
                    "--output",
                    str(out_dir),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, completed.returncode)
            local = out_dir / "evidence.jsonl"
            self.assertTrue(local.exists())
            records = [json.loads(line) for line in local.read_text(encoding="utf-8").splitlines() if line]
            self.assertEqual(["EA-DATA-2026-0002", "EA-DATA-2026-0005"], [r["event_id"] for r in records])
            # Internal provenance fields must not leak into the consolidated file.
            self.assertTrue(all("_input_file" not in r and "_input_line" not in r for r in records))
            # Brief and appendix only contain the selected events.
            brief = (out_dir / "writing-brief.md").read_text(encoding="utf-8")
            self.assertIn("EA-DATA-2026-0002", brief)
            self.assertNotIn("EA-DATA-2026-0001", brief)
            appendix = (out_dir / "evidence-appendix.md").read_text(encoding="utf-8")
            self.assertIn("### EA-DATA-2026-0005", appendix)
            self.assertNotIn("### EA-DATA-2026-0003", appendix)

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

    def test_appendix_emitted_whenever_events_exist(self) -> None:
        # Appendix is a citation-anchor scaffold, tied to evidence presence, not the formal-source gate.
        events = [event_for_paper("EA-DATA-2026-0001", "2601.00001")]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
        )
        self.assertIn("evidence-appendix.md", artifacts)

    def test_no_events_no_appendix(self) -> None:
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            [],
            [],
            [],
            "all",
        )
        self.assertNotIn("evidence-appendix.md", artifacts)
        self.assertIn("writing-brief.md", artifacts)
        self.assertIn("review-packet.md", artifacts)



    def test_writer_stance_caps_limit_brief_and_appendix(self) -> None:
        events = []
        for idx in range(20):
            events.append(sample_event(f"EA-DATA-2026-{idx+1:04d}", "support"))
        for idx in range(20, 30):
            events.append(sample_event(f"EA-DATA-2026-{idx+1:04d}", "limit"))
        for idx in range(30, 40):
            events.append(sample_event(f"EA-DATA-2026-{idx+1:04d}", "conditional"))
        for idx in range(40, 50):
            events.append(sample_event(f"EA-DATA-2026-{idx+1:04d}", "gap"))
        selected, stats = build_review_packet.cap_events_for_writer(events)
        self.assertEqual(8 + 6 + 6 + 4, len(selected))
        self.assertEqual(50, stats["total_events"])
        self.assertEqual(24, stats["writer_events"])
        self.assertEqual({"support": 12, "limit": 4, "conditional": 4, "gap": 6}, stats["omitted_by_stance"])

        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
        )
        brief = artifacts["writing-brief.md"]
        appendix = artifacts["evidence-appendix.md"]
        self.assertIn("Writer evidence caps", brief)
        self.assertIn("support≤8", brief)
        self.assertIn("Events in this brief/appendix: 24 / 50 loaded", brief)
        # Cap applies to appendix headings.
        heading_count = sum(1 for line in appendix.splitlines() if line.startswith("### EA-DATA-"))
        self.assertEqual(24, heading_count)
        # Full event set still drives sufficiency counts in the brief.
        self.assertIn("Accepted events (full evidence set): 50", brief)

    def test_writer_paper_floor_keeps_one_event_per_paper(self) -> None:
        # Stance-only truncation dropped whole papers (2026-10-15 纹理映射:
        # 3/12 papers had 0 appendix hits → claim-level citations dead-anchored).
        # Four papers, 10 support events each; the late papers' cards all sort
        # past the support cap, but every paper must still keep one event.
        events = []
        for idx, arxiv_id in enumerate(["2601.00001", "2601.00002", "2601.00003", "2601.00004"]):
            for n in range(10):
                event = event_for_paper(f"EA-DATA-2026-{idx*10+n+1:04d}", arxiv_id)
                events.append(event)
        selected, stats = build_review_packet.cap_events_for_writer(events)
        covered = {build_review_packet.paper_key(event) for event in selected}
        self.assertEqual({"2601.00001", "2601.00002", "2601.00003", "2601.00004"}, covered)
        self.assertEqual(4, stats["paper_floor_count"])
        # Floors first, then the leftover support quota (8 total).
        self.assertEqual(8, len(selected))
        self.assertEqual(40, stats["total_events"])

    def test_writer_paper_floor_overflows_stance_cap(self) -> None:
        # When papers outnumber a stance cap, the floor wins: caps bound
        # stance volume, never paper coverage.
        events = [event_for_paper(f"EA-DATA-2026-{idx+1:04d}", f"2601.{idx+1:05d}") for idx in range(10)]
        selected, stats = build_review_packet.cap_events_for_writer(events)
        covered = {build_review_packet.paper_key(event) for event in selected}
        self.assertEqual(10, len(covered))
        self.assertEqual(10, len(selected))
        self.assertEqual(10, stats["paper_floor_count"])
        # Every support slot is a floor; none omitted.
        self.assertEqual({}, stats["omitted_by_stance"])

    def test_uncapped_writer_keeps_all_events_in_brief(self) -> None:
        events = [sample_event(f"EA-DATA-2026-{idx+1:04d}", "support") for idx in range(12)]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性",
            ["EA-DATA"],
            events,
            [],
            [],
            "all",
            uncapped_writer=True,
        )
        brief = artifacts["writing-brief.md"]
        self.assertIn("Writer-facing events (capped): 12", brief)
        self.assertIn("Writer subset includes every loaded event", brief)

    def test_parse_stance_caps_overrides(self) -> None:
        caps = build_review_packet.parse_stance_caps("support=2,gap=1")
        self.assertEqual(2, caps["support"])
        self.assertEqual(1, caps["gap"])
        self.assertEqual(6, caps["limit"])

if __name__ == "__main__":
    unittest.main()

    def test_cli_run_dir_writes_briefing_into_existing_run_folder(self) -> None:
        """The wiki workflow passes --run-dir: artifacts land next to run.json
        instead of a fresh work/<topic>-<date>/ folder the agent must mv out."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            run_dir = tmp / "kb" / "work" / "literature-review-demo-20260101"
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text("{}", encoding="utf-8")
            evidence = tmp / "evidence.jsonl"
            evidence.write_text(
                "\n".join(
                    json.dumps(event_for_paper(f"EA-DATA-2026-000{index}", f"2601.0000{index}"), ensure_ascii=False)
                    for index in range(1, 6)
                )
                + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "review-packet",
                        "--topic",
                    "demo topic",
                    "--knowledge-id",
                    "EA-DATA",
                    "--evidence-jsonl",
                    str(evidence),
                    "--run-dir",
                    str(run_dir),
                ],
                check=True,
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            written = {path.name for path in run_dir.glob("*.md")}
            self.assertEqual({"review-packet.md", "writing-brief.md", "evidence-appendix.md"}, written)
            # No fresh dated project folder appears next to the run dir.
            self.assertEqual(
                ["literature-review-demo-20260101"],
                [path.name for path in (tmp / "kb" / "work").iterdir()],
            )


def abstract_event(event_id: str, arxiv_id: str, claim: str) -> dict[str, object]:
    return {
        "event_id": event_id,
        "tier": "abstract",
        "topic_id": "EA-DATA",
        "topic": "UMI data usability",
        "paper": {
            "arxiv_id": arxiv_id,
            "title": f"Abstract-only paper {arxiv_id}",
            "published": "2026-05-01",
        },
        "authors": [],
        "claim": claim,
        "stance": "",
        "evidence": {"summary": claim, "locator": "abstract"},
    }


class AbstractTierRenderingTests(unittest.TestCase):
    """tier: abstract events are candidate-landscape positioning: one shared
    appendix section, excluded from every full-text stat."""

    def test_split_tiers_separates_and_deduplicates_papers(self) -> None:
        fulltext = event_for_paper("EA-DATA-2026-0001", "2601.00001")
        events = [
            fulltext,
            abstract_event("EA-DATA-2026-0002", "2601.00001", "redundant positioning"),
            abstract_event("EA-DATA-2026-0003", "2601.00002", "landscape only"),
        ]
        fulltext_events, abstract_events = build_review_packet.split_tiers(events)
        self.assertEqual([str(event["event_id"]) for event in fulltext_events], ["EA-DATA-2026-0001"])
        # The abstract event for a paper that already deep-read is redundant.
        self.assertEqual(
            [str(event["event_id"]) for event in abstract_events], ["EA-DATA-2026-0003"]
        )

    def test_appendix_has_one_shared_abstract_section(self) -> None:
        abstract = [
            abstract_event("EA-DATA-2026-0003", "2601.00002", "landscape claim one"),
            abstract_event("EA-DATA-2026-0004", "2601.00003", "landscape claim two"),
        ]
        appendix = build_review_packet.render_evidence_appendix(
            "demo", [], None, abstract_events=abstract
        )
        self.assertEqual(1, appendix.count("### 摘要级相关工作"))
        self.assertNotIn("### EA-DATA-2026-0003", appendix)
        self.assertIn("| 事件 ID | 年份 | 标题 | 摘要节选 |", appendix)
        self.assertIn("仅定位用", appendix)
        # The section heading is the anchor these events link through.
        anchor = build_review_packet.event_anchor("摘要级相关工作")
        self.assertEqual(anchor, "摘要级相关工作")
        self.assertIn(f"(evidence-appendix.md#{anchor})", appendix)

    def test_packet_carries_abstract_landscape_and_keeps_stats_fulltext_only(self) -> None:
        fulltext = [event_for_paper("EA-DATA-2026-0001", "2601.00001")]
        abstract = [abstract_event("EA-DATA-2026-0003", "2601.00002", "landscape claim")]
        packet = build_review_packet.render_packet(
            "demo", ["EA-DATA"], fulltext, [], [], "survey", abstract_events=abstract
        )
        self.assertIn("## 摘要级相关工作（候选景观）", packet)
        self.assertIn("EA-DATA-2026-0003", packet)
        self.assertIn("- Evidence events: 1", packet)
        self.assertIn("- Abstract-tier events: 1", packet)
        self.assertEqual(build_review_packet.count_paper_level_sources(fulltext), 1)

    def test_no_abstract_events_no_section(self) -> None:
        packet = build_review_packet.render_packet(
            "demo", ["EA-DATA"], [event_for_paper("EA-DATA-2026-0001", "2601.00001")], [], [], "survey"
        )
        self.assertNotIn("摘要级相关工作", packet)
        appendix = build_review_packet.render_evidence_appendix(
            "demo", [event_for_paper("EA-DATA-2026-0001", "2601.00001")]
        )
        self.assertNotIn("摘要级相关工作", appendix)

    def test_bundle_routes_tiers_and_brief_explains_usage(self) -> None:
        events = [
            event_for_paper("EA-DATA-2026-0001", "2601.00001"),
            abstract_event("EA-DATA-2026-0003", "2601.00002", "landscape claim"),
        ]
        artifacts = build_review_packet.render_output_artifacts(
            "UMI 数据可用性", ["EA-DATA"], events, [], [], "all"
        )
        self.assertIn("## 摘要级相关工作（候选景观）", artifacts["review-packet.md"])
        self.assertIn("### 摘要级相关工作", artifacts["evidence-appendix.md"])
        brief = artifacts["writing-brief.md"]
        self.assertIn("摘要级相关工作（选文通过、尚未深读的候选，仅定位用）", brief)
        self.assertIn("References 中对应条目末尾标注（摘要级）", brief)
        # Full-text stats stay on the full-text tier.
        self.assertIn("- Evidence events: 1", artifacts["review-packet.md"])
        self.assertNotIn("EA-DATA-2026-0003 |", artifacts["writing-brief.md"])

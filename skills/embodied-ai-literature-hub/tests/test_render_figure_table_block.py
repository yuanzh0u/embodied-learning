#!/usr/bin/env python3

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "render_figure_table_block.py"
SPEC = importlib.util.spec_from_file_location("render_figure_table_block", SCRIPT_PATH)
render_figure_table_block = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(render_figure_table_block)


EVENT = {
    "event_id": "EA-CAMALIGN-2026-0001",
    "topic_id": "EA-DATA",
    "paper": {
        "arxiv_id": "2311.18259",
        "title": "Ego-Exo4D: Understanding Skilled Human Activity",
    },
    "evidence": {
        "figures": [
            {
                "figure_id": "S3.F3",
                "caption": "The Aria device used for egocentric recordings.",
                "image_url": "https://arxiv.org/html/2311.18259v4/figs/aria/aria.png",
                "usage": "作者用该图展示采集 rig 中 Aria 眼镜本体。",
            }
        ],
        "tables": [
            {
                "table_id": "S1.T1",
                "caption": "Comparison between Ego-Exo4D and relevant datasets.",
                "rows": [["Dataset", "Year"], ["Ego-Exo4D", "2023"]],
                "usage": "作者用该表对比数据集。",
            }
        ],
    },
}


class RenderFigureTableBlockTest(unittest.TestCase):
    def test_paper_label_joins_title_and_arxiv_id(self) -> None:
        self.assertEqual(
            render_figure_table_block.paper_label(EVENT),
            "Ego-Exo4D: Understanding Skilled Human Activity（arXiv 2311.18259）",
        )

    def test_render_figure_emits_markdown_image_link_and_usage(self) -> None:
        block = render_figure_table_block.render_figure(EVENT["evidence"]["figures"][0], "Ego-Exo4D")
        self.assertIn(
            "![The Aria device used for egocentric recordings.]"
            "(https://arxiv.org/html/2311.18259v4/figs/aria/aria.png)",
            block,
        )
        self.assertIn("> 用法：", block)
        self.assertIn("S3.F3", block)

    def test_render_table_emits_markdown_grid_with_header_separator(self) -> None:
        block = render_figure_table_block.render_table_block(EVENT["evidence"]["tables"][0], "Ego-Exo4D")
        self.assertIn("| Dataset | Year |", block)
        self.assertIn("| --- | --- |", block)
        self.assertIn("| Ego-Exo4D | 2023 |", block)
        self.assertIn("> 用法：", block)

    def test_events_with_paper_filters_by_arxiv_id(self) -> None:
        matched = render_figure_table_block.events_with_paper([EVENT], "2311.18259")
        self.assertEqual(len(matched), 1)
        self.assertEqual(
            render_figure_table_block.events_with_paper([EVENT], "9999.99999"), []
        )

    def test_find_event_figures_collects_evidence_figures_and_tables(self) -> None:
        figures, tables = render_figure_table_block.find_event_figures([EVENT], "2311.18259")
        self.assertEqual([f["figure_id"] for f in figures], ["S3.F3"])
        self.assertEqual([t["table_id"] for t in tables], ["S1.T1"])

    def test_cli_renders_requested_ids_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            evidence_path = Path(tmp) / "evidence.jsonl"
            evidence_path.write_text(json.dumps(EVENT, ensure_ascii=False) + "\n", encoding="utf-8")
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = render_figure_table_block.main(
                    [
                        "--evidence-jsonl",
                        str(evidence_path),
                        "--paper-id",
                        "2311.18259",
                    ]
                )
            self.assertEqual(code, 0)
            self.assertIn("S3.F3", stream.getvalue())
            self.assertIn("S1.T1", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
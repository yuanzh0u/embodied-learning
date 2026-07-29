#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "visualize_kb_index.py"
SPEC = importlib.util.spec_from_file_location("visualize_kb_index", SCRIPT)
viz = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(viz)


def make_repo(tmp: Path) -> None:
    kb = tmp / "knowledge"
    (kb / "embodied-ai").mkdir(parents=True)
    (kb / "index.md").write_text(
        "---\n"
        "id: KB-INDEX\n"
        "title: Index\n"
        "type: index\n"
        "---\n\n"
        "# Index\n\n"
        "[domain](embodied-ai/index.md)\n"
        "[evidence readme](../evidence/README.md)\n",
        encoding="utf-8",
    )
    (kb / "embodied-ai" / "index.md").write_text(
        "---\n"
        "id: EA-INDEX\n"
        "title: Domain\n"
        "type: domain-index\n"
        "---\n\n"
        "# Domain\n\n"
        "[card](card.md)\n",
        encoding="utf-8",
    )
    (kb / "embodied-ai" / "card.md").write_text(
        "---\n"
        "id: EA-TEST\n"
        "title: Card\n"
        "type: topic-card\n"
        "source:\n"
        "  - id: S-TEST\n"
        "    file: card.sources.md\n"
        "---\n\n"
        "# Card\n\n"
        "## 30 秒摘要\n\n"
        "Some **bold** text with a [link](https://example.com) and:\n\n"
        "- bullet one\n"
        "- bullet two\n\n"
        "| a | b |\n"
        "|---|---|\n"
        "| 1 | 2 |\n",
        encoding="utf-8",
    )
    (kb / "embodied-ai" / "card.sources.md").write_text("# Sources\n", encoding="utf-8")
    # A second card also links back to the domain index, creating a cross-reference
    # that must not create a second tree slot for embodied-ai/index.md.
    (kb / "embodied-ai" / "card2.md").write_text(
        "---\nid: EA-TEST-2\ntitle: Card2\ntype: topic-card\n---\n\n"
        "[back to domain](index.md)\n",
        encoding="utf-8",
    )
    with (kb / "embodied-ai" / "index.md").open("a", encoding="utf-8") as f:
        f.write("[card2](card2.md)\n")
    (tmp / "evidence").mkdir()
    (tmp / "evidence" / "README.md").write_text("# Evidence\n", encoding="utf-8")


class VisualizeKbIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        make_repo(self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_build_graph_expands_only_under_knowledge(self) -> None:
        start = self.root / "knowledge" / "index.md"
        nodes, edges, children_map, root_rel, truncated = viz.build_graph(self.root, start, max_nodes=50)
        self.assertFalse(truncated)
        self.assertEqual(root_rel, "knowledge/index.md")
        self.assertIn("knowledge/index.md", nodes)
        self.assertIn("knowledge/embodied-ai/index.md", nodes)
        self.assertIn("knowledge/embodied-ai/card.md", nodes)
        self.assertIn("knowledge/embodied-ai/card.sources.md", nodes)
        self.assertIn("evidence/README.md", nodes)
        self.assertEqual(nodes["knowledge/embodied-ai/card.md"]["id"], "EA-TEST")
        self.assertIn(
            ("knowledge/embodied-ai/card.md", "knowledge/embodied-ai/card.sources.md", "source"),
            edges,
        )
        self.assertIn(("knowledge/index.md", "evidence/README.md", "link"), edges)

    def test_evidence_readme_is_a_leaf(self) -> None:
        (self.root / "evidence" / "README.md").write_text(
            "# Evidence\n\n[should not expand](../knowledge/embodied-ai/card.md)\n",
            encoding="utf-8",
        )
        start = self.root / "knowledge" / "index.md"
        _nodes, edges, _children_map, _root_rel, _truncated = viz.build_graph(self.root, start, max_nodes=50)
        self.assertEqual([e for e in edges if e[0] == "evidence/README.md"], [])

    def test_cross_reference_does_not_duplicate_tree_slot(self) -> None:
        start = self.root / "knowledge" / "index.md"
        _nodes, edges, children_map, _root_rel, _truncated = viz.build_graph(self.root, start, max_nodes=50)
        placements = [
            p for p, kids in children_map.items() for c, _k in kids if c == "knowledge/embodied-ai/index.md"
        ]
        self.assertEqual(len(placements), 1)
        self.assertIn(
            ("knowledge/embodied-ai/card2.md", "knowledge/embodied-ai/index.md", "link"), edges
        )

    def test_max_nodes_cap_reports_truncation(self) -> None:
        start = self.root / "knowledge" / "index.md"
        _nodes, _edges, _children_map, _root_rel, truncated = viz.build_graph(self.root, start, max_nodes=2)
        self.assertTrue(truncated)

    def test_markdown_to_html_renders_common_constructs(self) -> None:
        body = (
            "# Title\n\n"
            "Some **bold** and `code` and a [link](https://example.com).\n\n"
            "- one\n- two\n\n"
            "| a | b |\n|---|---|\n| 1 | 2 |\n"
        )
        out = viz.markdown_to_html(body)
        self.assertIn("<h1>Title</h1>", out)
        self.assertIn("<strong>bold</strong>", out)
        self.assertIn("<code>code</code>", out)
        self.assertIn('<a href="https://example.com"', out)
        self.assertIn("<ul>", out)
        self.assertIn("<li>one</li>", out)
        self.assertIn("<table>", out)
        self.assertIn("<th>a</th>", out)
        self.assertIn("<td>1</td>", out)

    def test_markdown_to_html_escapes_raw_html(self) -> None:
        out = viz.markdown_to_html("<script>alert(1)</script>\n\ntext\n")
        self.assertNotIn("<script>alert(1)</script>", out)
        self.assertIn("&lt;script&gt;", out)

    def test_link_resolver_flags_internal_and_broken_links(self) -> None:
        ids = {"knowledge/embodied-ai/card.md": "n5"}
        resolve = viz.make_link_resolver(self.root, self.root / "knowledge" / "embodied-ai", ids)

        internal = resolve("card.md")
        self.assertEqual(internal["internal_id"], "n5")
        self.assertFalse(internal["broken"])

        broken = resolve("does-not-exist.md")
        self.assertTrue(broken["broken"])

        external = resolve("https://example.com")
        self.assertFalse(external["broken"])
        self.assertIsNone(external["internal_id"])

    def test_markdown_to_html_rewrites_relative_links_via_resolver(self) -> None:
        ids = {"knowledge/embodied-ai/card.md": "n5"}
        resolve = viz.make_link_resolver(self.root, self.root / "knowledge" / "embodied-ai", ids)
        out = viz.markdown_to_html("[good](card.md) and [bad](missing.md)\n", resolve)
        self.assertIn('data-goto="n5"', out)
        self.assertIn('class="internal-link"', out)
        self.assertIn('class="broken-link"', out)

    def test_render_markdown_preview_truncates_long_body(self) -> None:
        resolve = viz.make_link_resolver(self.root, self.root, {})
        long_body = "para one\n\n" + ("x" * (viz.BODY_PREVIEW_LIMIT + 500))
        out = viz.render_markdown_preview(long_body, resolve)
        self.assertIn("truncated-note", out)

    def test_render_json_preview_renders_table(self) -> None:
        out = viz.render_json_preview(json.dumps({"status": "settled", "event_count": 2}))
        self.assertIn("json-table", out)
        self.assertIn("settled", out)

    def test_render_jsonl_preview_renders_records(self) -> None:
        body = "\n".join(
            json.dumps({"event_id": f"EA-TEST-{i:04d}", "stance": "support"}) for i in range(3)
        )
        out = viz.render_jsonl_preview(body)
        self.assertIn("共 3 条记录", out)
        self.assertIn("EA-TEST-0000", out)
        self.assertIn("json-record", out)

    def test_render_jsonl_preview_reports_parse_errors(self) -> None:
        out = viz.render_jsonl_preview('not json\n{"ok": true}')
        self.assertIn("1 条解析失败", out)

    def test_evidence_json_files_become_typed_nodes_and_render(self) -> None:
        run_dir = self.root / "evidence" / "literature-review-test-20260101"
        run_dir.mkdir(parents=True)
        (run_dir / "evidence.jsonl").write_text(
            json.dumps({"event_id": "EA-TEST-READ-0001", "stance": "support"}) + "\n", encoding="utf-8"
        )
        (run_dir / "run.json").write_text(json.dumps({"status": "settled"}), encoding="utf-8")
        card = self.root / "knowledge" / "embodied-ai" / "card3.md"
        card.write_text(
            "---\nid: EA-TEST-3\ntitle: Card3\ntype: topic-card\n"
            "source:\n"
            "  - id: RUN-TEST-20260101\n"
            "    file: ../../evidence/literature-review-test-20260101/evidence.jsonl\n"
            "---\n\n# Card3\n",
            encoding="utf-8",
        )
        with (self.root / "knowledge" / "embodied-ai" / "index.md").open("a", encoding="utf-8") as f:
            f.write("[card3](card3.md)\n")

        start = self.root / "knowledge" / "index.md"
        nodes, edges, children_map, root_rel, truncated = viz.build_graph(self.root, start, max_nodes=50)
        evidence_rel = "evidence/literature-review-test-20260101/evidence.jsonl"
        self.assertIn(evidence_rel, nodes)
        self.assertEqual(nodes[evidence_rel]["type"], "evidence-jsonl")

        doc = viz.render_html(self.root, nodes, edges, children_map, root_rel, truncated)
        self.assertIn("json-record", doc)
        self.assertIn("EA-TEST-READ-0001", doc)

    def test_render_html_does_not_leave_raw_relative_md_hrefs(self) -> None:
        start = self.root / "knowledge" / "index.md"
        nodes, edges, children_map, root_rel, truncated = viz.build_graph(self.root, start, max_nodes=50)
        doc = viz.render_html(self.root, nodes, edges, children_map, root_rel, truncated)
        self.assertNotIn('href="card.md"', doc)
        self.assertNotIn('href="index.md"', doc)
        self.assertIn("internal-link", doc)

    def test_render_html_is_self_contained_tree_with_backlinks(self) -> None:
        start = self.root / "knowledge" / "index.md"
        nodes, edges, children_map, root_rel, truncated = viz.build_graph(self.root, start, max_nodes=50)
        doc = viz.render_html(self.root, nodes, edges, children_map, root_rel, truncated)
        self.assertNotIn("cdn.", doc)
        self.assertNotIn("unpkg", doc)
        self.assertIn("EA-TEST", doc)
        self.assertIn('id="tree-wrap"', doc)
        self.assertIn('id="pane-body"', doc)
        self.assertIn("BACKLINKS", doc)

    def test_end_to_end_writes_html_without_opening_browser(self) -> None:
        import subprocess
        import sys

        output = self.root / "work" / "graph.html"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "--output", str(output), "--no-open"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(output.is_file())
        content = output.read_text(encoding="utf-8")
        self.assertIn("EA-TEST", content)
        self.assertIn("selectNode(ROOT_ID)", content)


if __name__ == "__main__":
    unittest.main()

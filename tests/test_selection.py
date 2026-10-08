"""embodied_learning.search.selection — deep-read queue selection strategies.

The keywords strategy stays with screen-candidates; these tests pin bm25
relevance ordering, the honest influence degradation, the smart agent contract
(JSON / garbage / failure), and the screening artifacts the driver consumes.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


from embodied_learning.search import selection as selection_mod
from embodied_learning.search.selection import (
    bm25_scores,
    bm25_select,
    influence_select,
    render_selection_markdown,
    run_select,
    smart_select,
    to_screening_artifacts,
)



def registry_with(*candidates: dict) -> dict:
    return {"candidate_count": len(candidates), "candidates": list(candidates)}


def candidate(arxiv_id: str, title: str, summary: str, **extra) -> dict:
    record = {
        "arxiv_id": arxiv_id,
        "title": title,
        "summary": summary,
        "published": "2026-01-01",
    }
    record.update(extra)
    return record


class Bm25Test(unittest.TestCase):
    REGISTRY = registry_with(
        candidate("2402.10329", "UMI", "Universal manipulation interface for data collection."),
        candidate("1704.02084", "PointNet", "Deep learning on point clouds for classification."),
        candidate("2311.18259", "Ego-Exo4D", "Egocentric and exocentric video dataset."),
    )

    def test_relevant_paper_outranks_offtopic_ones(self):
        scored = bm25_scores(self.REGISTRY, "umi manipulation data collection")
        self.assertEqual(scored[0][0], "2402.10329")
        self.assertGreater(scored[0][1], 0.0)
        # PointNet shares no query term and scores nothing at all.
        self.assertNotIn("1704.02084", [arxiv_id for arxiv_id, _, _ in scored])

    def test_select_truncates_to_limit(self):
        selected = bm25_select(self.REGISTRY, "umi manipulation", 1)
        self.assertEqual([c["arxiv_id"] for c in selected], ["2402.10329"])
        self.assertEqual(bm25_select(self.REGISTRY, "umi", 0), [])


class InfluenceTest(unittest.TestCase):
    def test_citation_count_descending(self):
        registry = registry_with(
            candidate("a", "A", "abstract a", citation_count=3),
            candidate("b", "B", "abstract b", citation_count=900),
            candidate("c", "C", "abstract c"),  # no citation data
        )
        selected, with_data = influence_select(registry, 2)
        self.assertEqual(with_data, 2)
        self.assertEqual([c["arxiv_id"] for c in selected], ["b", "a"])

    def test_shortfall_is_reported_not_padded(self):
        registry = registry_with(candidate("a", "A", "abstract a", citation_count=1))
        selected, with_data = influence_select(registry, 5)
        self.assertEqual(len(selected), 1)
        self.assertEqual(with_data, 1)


class SmartSelectTest(unittest.TestCase):
    REGISTRY = registry_with(
        candidate("2402.10329", "UMI", "Universal manipulation interface."),
        candidate("1704.02084", "PointNet", "Point cloud classification."),
    )

    def test_parses_agent_json_and_caps_at_limit(self):
        result = mock.Mock(returncode=0, stdout='说明 {"relevant": ["2402.10329", "1704.02084", "9999.99999"]} 结束')
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="", limit=1,
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        # Unknown IDs are dropped, the cap is respected, and one relevant paper
        # against a limit of 1 is a full queue (no shortfall note).
        self.assertEqual([c["arxiv_id"] for c in selected], ["2402.10329"])
        self.assertIn("smart selected 2/2 considered (1 full-coverage chunk(s))", detail)

    def test_reasons_are_parsed_and_carried_into_artifacts(self):
        """smart 输出逐篇选中理由（供调试）：解析 {arxiv_id, reason}，进
        screening.json 行与 screening.md 表格。"""
        result = mock.Mock(returncode=0, stdout=json.dumps({
            "relevant": [
                {"arxiv_id": "2402.10329", "reason": "提供数据采集接口，支撑可用性机制讨论"},
                {"arxiv_id": "1704.02084", "reason": "点云分类先验，作对比基线"},
                {"arxiv_id": "2402.10329", "reason": "重复条目应去重"},
            ],
            "shortfall_note": "",
        }))
        selected, _ = smart_select(
            self.REGISTRY, topic="umi", focus="", limit=2,
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertEqual(
            [(c["arxiv_id"], c["selection_reason"]) for c in selected],
            [("2402.10329", "提供数据采集接口，支撑可用性机制讨论"),
             ("1704.02084", "点云分类先验，作对比基线")],
        )
        rows, ids = to_screening_artifacts(selected, "smart detail")
        self.assertEqual(rows[0]["selection_reason"], "提供数据采集接口，支撑可用性机制讨论")
        markdown = render_selection_markdown("smart", "smart detail", selected, 3)
        self.assertIn("提供数据采集接口，支撑可用性机制讨论", markdown)

    def test_malformed_chunk_output_is_salvaged_not_silently_dropped(self):
        """20260930 绝对位姿 run：chunk-1 模型输出的 JSON 数组里混进 .replace()
        代码残留 → 解析归零、300 篇（含 PnP 核心论文）被静默跳过。修复：坏输出
        打捞已知 ID，并在 detail 里如实标注。"""
        registry = registry_with(
            candidate("2410.14164", "Optimal DLT PnP", "PnP solver."),
            candidate("2407.15540", "Reloc", "Camera relocalization."),
        )
        garbled = '前言 {"relevant": ["2410.14164", "2407.15540".replace("x","x"), "2407.15540"]} 后记'
        result = mock.Mock(returncode=0, stdout=garbled)
        selected, detail = smart_select(
            registry, topic="absolute pose", focus="", limit=40,
            complete_fn=mock.Mock(return_value=result), cli="c", model="m",
        )
        self.assertEqual(sorted(c["arxiv_id"] for c in selected), ["2407.15540", "2410.14164"])
        self.assertIn("malformed", detail)
        self.assertIn("salvaged", detail)

    def test_unparseable_chunk_counts_as_coverage_hole(self):
        result = mock.Mock(returncode=0, stdout="好的，我认为这些论文都不错。")
        _, detail = smart_select(
            self.REGISTRY, topic="umi", focus="", limit=2,
            complete_fn=mock.Mock(return_value=result), cli="c", model="m",
        )
        # 非空但不可解析 = 覆盖缺口（failed chunk），不是"0 篇相关"的诚实结论
        self.assertIn("1/1 chunk(s) failed", detail)

    def test_legacy_string_form_still_parses(self):
        self.assertEqual(
            selection_mod._parse_selections('{"relevant": ["2402.10329"]}', {"2402.10329"}),
            [("2402.10329", "")],
        )

    def test_shortfall_is_reported_when_relevant_below_limit(self):
        result = mock.Mock(returncode=0, stdout='{"relevant": ["2402.10329"]}')
        _, detail = smart_select(
            self.REGISTRY, topic="umi", focus="", limit=2,
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertIn("shortfall: only 1 relevant (limit 2), not padded", detail)

    def test_garbage_output_selects_nothing(self):
        result = mock.Mock(returncode=0, stdout="好的，我认为这些论文都不错。")
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="", limit=2,
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertEqual(selected, [])
        self.assertIn("shortfall", detail)

    def test_agent_failure_is_honest_not_padded(self):
        result = mock.Mock(returncode=1, stdout="", stderr="boom")
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="", limit=2,
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertEqual(selected, [])
        self.assertIn("1/1 chunk(s) failed", detail)

    def test_empty_registry_short_circuits(self):
        selected, detail = smart_select(
            registry_with(), topic="umi", focus="", limit=2,
            complete_fn=mock.Mock(), cli="/fake/claude", model="m",
        )
        self.assertEqual((selected, detail), ([], "empty registry"))


class ToScreeningArtifactsTest(unittest.TestCase):
    def test_row_shape_and_id_list(self):
        rows, ids = to_screening_artifacts(
            [{"arxiv_id": "2402.10329", "title": "UMI"}], "smart detail"
        )
        self.assertEqual(rows, [{
            "arxiv_id": "2402.10329", "title": "UMI",
            "status": "full-text-queued", "selection_detail": "smart detail",
            "selection_reason": "",
        }])
        self.assertEqual(ids, ["2402.10329"])
        self.assertEqual(to_screening_artifacts([{"title": "no id"}], "d"), ([], []))


class RunSelectTest(unittest.TestCase):
    REGISTRY = registry_with(
        candidate("2402.10329", "UMI", "Universal manipulation interface."),
        candidate("1704.02084", "PointNet", "Point cloud classification.", citation_count=50),
    )

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry_path = Path(self.tmp.name) / "registry.json"
        self.registry_path.write_text(json.dumps(self.REGISTRY), encoding="utf-8")
        self.screening = Path(self.tmp.name) / "screening.json"
        self.ids = Path(self.tmp.name) / "screening-ids.txt"
        self.markdown = Path(self.tmp.name) / "screening.md"

    def run_select(self, strategy: str, limit: int = 1, **kwargs) -> int:
        return run_select(
            str(self.registry_path), strategy, "umi manipulation", "focus text", limit,
            str(self.screening), str(self.ids), str(self.markdown), **kwargs,
        )

    def screening_payload(self) -> dict:
        return json.loads(self.screening.read_text(encoding="utf-8"))

    def test_keywords_is_rejected_here(self):
        with mock.patch("sys.stderr"):
            self.assertEqual(self.run_select("keywords"), 2)
        self.assertFalse(self.screening.exists())

    def test_bm25_writes_screening_artifacts(self):
        self.assertEqual(self.run_select("bm25"), 0)
        payload = self.screening_payload()
        self.assertEqual(payload["selection_rule"]["strategy"], "bm25")
        rows = payload["candidates"]
        self.assertEqual([row["arxiv_id"] for row in rows], ["2402.10329"])
        self.assertEqual(rows[0]["status"], "full-text-queued")
        self.assertEqual(self.ids.read_text(encoding="utf-8"), "2402.10329\n")
        markdown = self.markdown.read_text(encoding="utf-8")
        self.assertIn("| Rank | arXiv | Score | Title | Selection note |", markdown)
        self.assertIn("2402.10329", markdown)

    def test_influence_degrades_to_bm25_with_detail(self):
        self.assertEqual(self.run_select("influence", limit=2), 0)
        rule = self.screening_payload()["selection_rule"]
        self.assertEqual(rule["strategy"], "influence")
        self.assertIn("influence degraded to bm25 (citation data: 1 papers)", rule["detail"])
        # bm25 backfills the remaining slot: the queue reaches the limit even
        # though only one candidate carries citation data.
        self.assertEqual(len(self.screening_payload()["candidates"]), 2)

    def test_smart_uses_the_harness_one_shot(self):
        result = mock.Mock(returncode=0, stdout='{"relevant": ["2402.10329"]}')
        complete_fn = mock.Mock(return_value=result)
        code = self.run_select(
            "smart", cli="/fake/claude", model="m", timeout_s=5.0, complete_fn=complete_fn,
        )
        self.assertEqual(code, 0)
        payload = self.screening_payload()
        self.assertEqual(payload["selection_rule"]["strategy"], "smart")
        self.assertIn("smart selected 1/", payload["selection_rule"]["detail"])
        complete_fn.assert_called_once()
        kwargs = complete_fn.call_args.kwargs
        self.assertEqual(kwargs["cli"], "/fake/claude")
        self.assertEqual(kwargs["model"], "m")
        self.assertEqual(kwargs["label"], "selection-smart")

    def test_smart_without_cli_fails_loudly(self):
        with mock.patch("sys.stderr"), \
             mock.patch("embodied_learning.harness.claude.resolve_cli", return_value=None):
            self.assertEqual(self.run_select("smart"), 2)
        self.assertFalse(self.screening.exists())

    def test_zero_matches_exit_two(self):
        self.registry_path.write_text(
            json.dumps(registry_with(candidate("9999.00001", "Unrelated", "nothing matches"))),
            encoding="utf-8",
        )
        self.assertEqual(self.run_select("bm25"), 2)


    def test_smart_covers_every_candidate_via_chunks(self) -> None:
        # The smart contract: no lexical prefilter decides what the agent
        # sees. 300 candidates = one call; 301 = two calls, all seen once.
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i} on tactile sensing",
             "summary": "We study tactile sensing for robotic manipulation."}
            for i in range(300)
        ]}
        seen = []

        def fake_complete(prompt, **kwargs):
            seen.append(prompt)
            return mock.Mock(returncode=0, stdout='{"relevant": ["2601.00001"]}')

        selected, detail = selection_mod.smart_select(
            registry, topic="图像粗配准", focus="", limit=40,
            complete_fn=fake_complete, cli="claude", model="test-model",
        )
        self.assertEqual(len(seen), 1)  # single call, no prefilter
        import re as _re
        self.assertEqual(len(_re.findall(r"\n\d+\. \[", seen[0])), 300)
        self.assertEqual([c["arxiv_id"] for c in selected], ["2601.00001"])

    def test_smart_chunks_large_registry_without_dropping_anyone(self) -> None:
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i}",
             "summary": f"Abstract {i} about robotic manipulation."}
            for i in range(301)
        ]}
        seen = []

        def fake_complete(prompt, **kwargs):
            seen.append(prompt)
            last = len(seen) == 2
            ids = ["2601.00000"] if not last else ["2601.00300"]
            import json as _json
            return mock.Mock(returncode=0, stdout=_json.dumps({"relevant": ids}))

        selected, detail = selection_mod.smart_select(
            registry, topic="图像粗配准", focus="", limit=40,
            complete_fn=fake_complete, cli="claude", model="test-model",
        )
        self.assertEqual(len(seen), 2)
        import re as _re
        self.assertEqual(len(_re.findall(r"\n\d+\. \[", seen[0])), 300)
        self.assertEqual(len(_re.findall(r"\n\d+\. \[", seen[1])), 1)
        self.assertEqual([c["arxiv_id"] for c in selected], ["2601.00000", "2601.00300"])
        self.assertIn("full-coverage chunk(s)", detail)

    def test_smart_partial_chunk_failure_reports_incomplete_coverage(self) -> None:
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i}", "summary": f"A{i}."}
            for i in range(301)
        ]}
        calls = {"n": 0}

        def fake_complete(prompt, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                return mock.Mock(returncode=0, stdout='{"relevant": ["2601.00001"]}')
            return mock.Mock(returncode=1, stdout="", stderr="boom")

        selected, detail = selection_mod.smart_select(
            registry, topic="t", focus="", limit=40,
            complete_fn=fake_complete, cli="c", model="m",
        )
        self.assertEqual(len(selected), 1)
        self.assertIn("1/2 chunk(s) failed", detail)

    def test_terms_augment_bm25_query(self) -> None:
        registry = {"candidates": [
            {"arxiv_id": "1", "title": "Coarse registration of point clouds",
             "summary": "Geometric matching without correspondences."},
            {"arxiv_id": "2", "title": "A diet study", "summary": "Nutrition and health."},
        ]}
        selected = selection_mod.bm25_select(registry, "图像粗配准 coarse registration", 2)
        self.assertEqual([c["arxiv_id"] for c in selected][0], "1")

    def test_run_select_forwards_terms_to_query(self) -> None:
        import json as _json
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            reg = Path(tmp) / "registry.json"
            reg.write_text(_json.dumps({"candidates": [
                {"arxiv_id": "1", "title": "Coarse registration of clouds",
                 "summary": "Geometric matching."},
                {"arxiv_id": "2", "title": "Unrelated", "summary": "Other stuff."},
            ]}), encoding="utf-8")
            code = selection_mod.run_select(
                str(reg), "bm25", "图像粗配准", "", 1,
                str(Path(tmp) / "s.json"), str(Path(tmp) / "ids.txt"),
                terms="coarse registration,point clouds",
            )
            self.assertEqual(code, 0)
            ids = Path(tmp, "ids.txt").read_text().split()
            self.assertEqual(ids, ["1"])


if __name__ == "__main__":
    unittest.main()

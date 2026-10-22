"""embodied_learning.search.selection — deep-read queue selection strategies.

The keywords strategy stays with screen-candidates; these tests pin bm25
relevance ordering, the honest influence degradation, the smart agent contract
(JSON / garbage / failure), and the screening artifacts the driver consumes.
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


from embodied_learning.search import selection as selection_mod
from embodied_learning.search.selection import (
    bm25_scores,
    bm25_select,
    influence_select,
    pack_chunks,
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

    def test_parses_agent_json_and_keeps_retrieval_order(self):
        """No cap: every relevant paper is queued, in registry (retrieval)
        order rather than the agent's reply order."""
        result = mock.Mock(returncode=0, stdout='说明 {"relevant": ["2402.10329", "1704.02084", "9999.99999"]} 结束')
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="",
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        # Unknown IDs are dropped; both known papers are kept.
        self.assertEqual([c["arxiv_id"] for c in selected], ["2402.10329", "1704.02084"])
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
        }))
        selected, _ = smart_select(
            self.REGISTRY, topic="umi", focus="",
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
            registry, topic="absolute pose", focus="",
            complete_fn=mock.Mock(return_value=result), cli="c", model="m",
        )
        self.assertEqual(sorted(c["arxiv_id"] for c in selected), ["2407.15540", "2410.14164"])
        self.assertIn("malformed", detail)
        self.assertIn("salvaged", detail)

    def test_unparseable_chunk_counts_as_coverage_hole(self):
        result = mock.Mock(returncode=0, stdout="好的，我认为这些论文都不错。")
        _, detail = smart_select(
            self.REGISTRY, topic="umi", focus="",
            complete_fn=mock.Mock(return_value=result), cli="c", model="m",
        )
        # 非空但不可解析 = 覆盖缺口（failed chunk），不是"0 篇相关"的诚实结论
        self.assertIn("1/1 chunk(s) failed", detail)

    def test_legacy_string_form_still_parses(self):
        self.assertEqual(
            selection_mod._parse_selections('{"relevant": ["2402.10329"]}', {"2402.10329"}),
            [("2402.10329", "")],
        )

    def test_queue_is_never_padded_to_a_quota(self):
        """No count cap: the queue is exactly what the agent judged relevant.

        Selection does not pad toward a number — deep reading owns the only
        truncation (and the driver's 候补 fill reads the extracted pool)."""
        result = mock.Mock(returncode=0, stdout='{"relevant": ["2402.10329"]}')
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="",
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertEqual([c["arxiv_id"] for c in selected], ["2402.10329"])
        self.assertNotIn("shortfall", detail)

    def test_selection_follows_registry_order_not_agent_reply_order(self):
        """2026-10-20 自监督预训练: chunk-arrival order put every deep read in
        2021-2022. The agent's reply order carries no global ranking, so the
        queue is re-projected onto the registry's retrieval order."""
        registry = registry_with(
            candidate("2601.00001", "First found", "a"),
            candidate("2601.00002", "Second found", "b"),
            candidate("2601.00003", "Third found", "c"),
        )
        result = mock.Mock(returncode=0, stdout='{"relevant": ["2601.00003", "2601.00001", "2601.00002"]}')
        selected, _ = smart_select(
            registry, topic="t", focus="",
            complete_fn=mock.Mock(return_value=result), cli="c", model="m",
        )
        self.assertEqual(
            [c["arxiv_id"] for c in selected],
            ["2601.00001", "2601.00002", "2601.00003"],
        )

    def test_garbage_output_selects_nothing(self):
        result = mock.Mock(returncode=0, stdout="好的，我认为这些论文都不错。")
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="",
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertEqual(selected, [])
        self.assertIn("failed", detail)

    def test_agent_failure_is_honest_not_padded(self):
        result = mock.Mock(returncode=1, stdout="", stderr="boom")
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="",
            complete_fn=mock.Mock(return_value=result), cli="/fake/claude", model="m",
        )
        self.assertEqual(selected, [])
        self.assertIn("1/1 chunk(s) failed", detail)

    def test_timeout_is_a_failed_chunk_not_a_crash(self):
        """A slow agent call must not abort the run. Regression: TimeoutExpired
        escaped smart_select (the only complete() caller without a guard) and
        killed the whole fixed workflow with exit 1 on 2026-10-08."""
        complete_fn = mock.Mock(
            side_effect=subprocess.TimeoutExpired(cmd=["claude"], timeout=900.0)
        )
        selected, detail = smart_select(
            self.REGISTRY, topic="umi", focus="",
            complete_fn=complete_fn, cli="/fake/claude", model="m", timeout_s=900.0,
        )
        self.assertEqual(selected, [])
        self.assertIn("1/1 chunk(s) timed out after 900s", detail)
        self.assertIn("coverage incomplete", detail)

    def test_timed_out_chunk_does_not_take_down_the_others(self):
        """One hung chunk costs only that chunk's coverage; the rest still land."""
        ok = mock.Mock(
            returncode=0, stdout='{"relevant": [{"arxiv_id": "2402.10329", "reason": "jizhi"}]}'
        )
        # An exception INSTANCE in a side_effect iterable is raised, not returned.
        hang = subprocess.TimeoutExpired(cmd=["claude"], timeout=1.0)
        with mock.patch.object(selection_mod, "SMART_CANDIDATES_PER_CALL", 1):
            selected, detail = smart_select(
                self.REGISTRY, topic="umi", focus="",
                complete_fn=mock.Mock(side_effect=[hang, ok]),
                cli="/fake/claude", model="m", timeout_s=1.0,
            )
        self.assertEqual([c["arxiv_id"] for c in selected], ["2402.10329"])
        self.assertIn("1/2 chunk(s) timed out after 1s", detail)
        self.assertIn("coverage incomplete", detail)

    def test_empty_registry_short_circuits(self):
        selected, detail = smart_select(
            registry_with(), topic="umi", focus="",
            complete_fn=mock.Mock(), cli="/fake/claude", model="m",
        )
        self.assertEqual((selected, detail), ([], "empty registry"))

    def test_prompt_asks_for_relevance_not_a_quota_or_a_score(self):
        """2026-10-20: the agent is asked only "relevant or not" — no count
        quota (selection never truncates) and no relevance score (an
        unanchored number is not a ranking anyone can check)."""
        from embodied_learning.harness.prompt import SMART_SELECTION_PROMPT

        self.assertNotIn("{limit}", SMART_SELECTION_PROMPT)
        self.assertNotIn("最多输出", SMART_SELECTION_PROMPT)
        for token in ("score", "分数", "相关度评分"):
            self.assertNotIn(token, SMART_SELECTION_PROMPT)


class PackChunksTest(unittest.TestCase):
    """pack_chunks 的打包契约：按渲染长度切、计数上限兜底、一篇不丢。"""

    def line_chars(self, candidate: dict) -> int:
        return len(selection_mod._candidate_line(candidate)) + 1

    def test_packs_by_rendered_length_and_keeps_order(self):
        candidates = [candidate(f"2601.{i:05d}", f"Paper {i}", "A" * 400) for i in range(6)]
        per_line = self.line_chars(candidates[0])
        chunks = pack_chunks(candidates, char_budget=per_line * 2 + 10, count_ceiling=60)
        self.assertEqual([len(c) for c in chunks], [2, 2, 2])
        flat = [c["arxiv_id"] for c in sum(chunks, [])]
        self.assertEqual(flat, [f"2601.{i:05d}" for i in range(6)])

    def test_count_ceiling_bounds_tiny_lines(self):
        candidates = [candidate(f"2601.{i:05d}", f"P{i}", "") for i in range(5)]
        chunks = pack_chunks(candidates, char_budget=10_000, count_ceiling=2)
        self.assertEqual([len(c) for c in chunks], [2, 2, 1])

    def test_oversized_single_line_forms_its_own_chunk(self):
        # 单行超过预算也要成片（不丢、不切半个候选）。
        big = candidate("2601.00000", "Huge", "B" * 400)
        small = candidate("2601.00001", "P", "")
        chunks = pack_chunks([big, small], char_budget=self.line_chars(big) // 2, count_ceiling=60)
        self.assertEqual([[c["arxiv_id"] for c in chunk] for chunk in chunks],
                         [["2601.00000"], ["2601.00001"]])

    def test_exact_budget_fit_stays_in_one_chunk(self):
        candidates = [candidate(f"2601.{i:05d}", f"P{i}", "") for i in range(2)]
        budget = sum(self.line_chars(c) for c in candidates)
        chunks = pack_chunks(candidates, char_budget=budget, count_ceiling=60)
        self.assertEqual(len(chunks), 1)
        chunks = pack_chunks(candidates, char_budget=budget - 1, count_ceiling=60)
        self.assertEqual([len(c) for c in chunks], [1, 1])

    def test_empty_registry_packs_nothing(self):
        self.assertEqual(pack_chunks([], char_budget=100, count_ceiling=2), [])


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

    def run_select(self, strategy: str, **kwargs) -> int:
        return run_select(
            str(self.registry_path), strategy, "umi manipulation", "focus text",
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
        self.assertEqual(self.run_select("influence"), 0)
        rule = self.screening_payload()["selection_rule"]
        self.assertEqual(rule["strategy"], "influence")
        self.assertIn("influence degraded to bm25 (citation data: 1 papers)", rule["detail"])
        # bm25 covers every candidate the citation channel could not rank:
        # nothing is dropped for lack of a citation count.
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

    def test_smart_jev_uses_the_decision_model_binding(self):
        """smart-jev is a second binding, not a prompt variant: it asks the
        System One channel one typed question per candidate and keeps the
        papers above the threshold, in registry order."""
        judge_fn = mock.Mock(return_value={"answers": {
            "2402.10329": {"type": "noul", "noul": 0.91},
            "1704.02084": {"type": "noul", "noul": 0.12},
        }})
        with mock.patch(
            "embodied_learning.harness.claude.system_one_ready", return_value=True
        ):
            code = self.run_select("smart-jev", judge_fn=judge_fn, threshold=0.6)
        self.assertEqual(code, 0)
        payload = self.screening_payload()
        self.assertEqual(payload["selection_rule"]["strategy"], "smart-jev")
        self.assertIn("threshold 0.60", payload["selection_rule"]["detail"])
        self.assertEqual([r["arxiv_id"] for r in payload["candidates"]], ["2402.10329"])
        state, questions = judge_fn.call_args.args
        self.assertIn("umi manipulation", state)
        # The strict wording is a measured contract, not decoration: the loose
        # "adjacent field counts" phrasing cost ~20 points of precision.
        self.assertIn("核心贡献直接针对综述话题", state)
        self.assertEqual(questions["2402.10329"]["type"], "noul")
        self.assertIn("[2402.10329]", questions["2402.10329"]["instructions"])
        self.assertTrue(
            questions["2402.10329"]["instructions"].startswith(
                "This paper's main contribution directly addresses the review topic."
            )
        )

    def test_smart_jev_without_configuration_fails_loudly(self):
        with mock.patch("sys.stderr"), \
             mock.patch("embodied_learning.harness.claude.system_one_ready", return_value=False):
            self.assertEqual(self.run_select("smart-jev"), 2)
        self.assertFalse(self.screening.exists())

    def test_jev_select_reports_failed_batch_as_coverage_gap(self):
        registry = registry_with(*[
            candidate(f"2601.{i:05d}", f"Paper {i}", "streaming reconstruction")
            for i in range(4)
        ])

        def judge(state, questions, **kwargs):
            if "2601.00002" in questions:
                raise RuntimeError("upstream 503")
            return {"answers": {k: {"type": "noul", "noul": 0.9} for k in questions}}

        selected, detail = selection_mod.jev_select(
            registry, topic="t", judge_fn=judge, questions_per_call=2, workers=1,
        )
        self.assertEqual([c["arxiv_id"] for c in selected], ["2601.00000", "2601.00001"])
        self.assertIn("2 candidate(s) unjudged", detail)

    def test_zero_matches_exit_two(self):
        self.registry_path.write_text(
            json.dumps(registry_with(candidate("9999.00001", "Unrelated", "nothing matches"))),
            encoding="utf-8",
        )
        self.assertEqual(self.run_select("bm25"), 2)


    def test_smart_covers_every_candidate_via_chunks(self) -> None:
        # The smart contract: no lexical prefilter decides what the agent
        # sees — every candidate is rendered into exactly one chunk prompt.
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i} on tactile sensing",
             "summary": "We study tactile sensing for robotic manipulation."}
            for i in range(120)
        ]}
        seen = []

        def fake_complete(prompt, **kwargs):
            seen.append(prompt)
            return mock.Mock(returncode=0, stdout='{"relevant": ["2601.00001"]}')

        selected, detail = selection_mod.smart_select(
            registry, topic="图像粗配准", focus="",
            complete_fn=fake_complete, cli="claude", model="test-model",
        )
        self.assertGreater(len(seen), 1)  # 120 lines cannot fit one call
        import re as _re
        ids = [i for p in seen for i in _re.findall(r"\[(\d{4}\.\d{4,5})\]", p)]
        self.assertEqual(len(ids), 120)          # full coverage…
        self.assertEqual(len(set(ids)), 120)     # …and each seen exactly once
        self.assertEqual([c["arxiv_id"] for c in selected], ["2601.00001"])

    def test_smart_chunks_by_rendered_size_not_fixed_count(self) -> None:
        """打包按候选行的渲染长度切，不按固定篇数（2026-10-16 强化学习 run：
        固定 300 篇/片渲染出 157KB prompt，完成流在中途断掉）。长摘要即使只有
        6 篇也要切成多次调用。"""
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i}", "summary": "A" * 400}
            for i in range(6)
        ]}
        seen = []

        def fake_complete(prompt, **kwargs):
            seen.append(prompt)
            return mock.Mock(returncode=0, stdout='{"relevant": []}')

        with mock.patch.object(selection_mod, "SMART_CANDIDATE_CHARS_PER_CALL", 800), \
             mock.patch.object(selection_mod, "SMART_CANDIDATES_PER_CALL", 60):
            selection_mod.smart_select(
                registry, topic="t", focus="",
                complete_fn=fake_complete, cli="c", model="m",
            )
        # 每行 ~450 字符，800 预算 → 一篇/片；计数上限没到就先被长度切断
        self.assertEqual(len(seen), 6)
        import re as _re
        self.assertTrue(all(len(_re.findall(r"\n\d+\. \[", p)) == 1 for p in seen))

    def test_smart_chunks_large_registry_without_dropping_anyone(self) -> None:
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i}",
             "summary": f"Abstract {i} about robotic manipulation."}
            for i in range(301)
        ]}
        seen = []

        def fake_complete(prompt, **kwargs):
            seen.append(prompt)
            return mock.Mock(returncode=0, stdout='{"relevant": []}')

        with mock.patch.object(selection_mod, "SMART_CANDIDATES_PER_CALL", 60):
            selected, detail = selection_mod.smart_select(
                registry, topic="图像粗配准", focus="",
                complete_fn=fake_complete, cli="claude", model="test-model",
            )
        import re as _re
        ids = [i for p in seen for i in _re.findall(r"\[(\d{4}\.\d{4,5})\]", p)]
        self.assertEqual(len(ids), 301)
        self.assertEqual(len(set(ids)), 301)
        self.assertTrue(all(len(_re.findall(r"\n\d+\. \[", p)) <= 60 for p in seen))
        self.assertIn("full-coverage chunk(s)", detail)

    def test_smart_partial_chunk_failure_reports_incomplete_coverage(self) -> None:
        registry = {"candidates": [
            {"arxiv_id": f"2601.{i:05d}", "title": f"Paper {i}", "summary": f"A{i}."}
            for i in range(4)
        ]}
        calls = {"n": 0}

        def fake_complete(prompt, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                return mock.Mock(returncode=0, stdout='{"relevant": ["2601.00001"]}')
            return mock.Mock(returncode=1, stdout="", stderr="boom")

        with mock.patch.object(selection_mod, "SMART_CANDIDATES_PER_CALL", 2):
            selected, detail = selection_mod.smart_select(
                registry, topic="t", focus="",
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
                str(reg), "bm25", "图像粗配准", "",
                str(Path(tmp) / "s.json"), str(Path(tmp) / "ids.txt"),
                terms="coarse registration,point clouds",
            )
            self.assertEqual(code, 0)
            ids = Path(tmp, "ids.txt").read_text().split()
            self.assertEqual(ids, ["1"])


if __name__ == "__main__":
    unittest.main()

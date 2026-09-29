#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from scripts import build_research_wiki as wiki


def write_triplet(directory: Path, topic: str = "测试话题") -> None:
    directory.mkdir(parents=True)
    (directory / "run.json").write_text(json.dumps({"topic": topic}, ensure_ascii=False), encoding="utf-8")
    for _key, (label, filename) in wiki.VERSION_FILES.items():
        (directory / filename).write_text(
            f"# {label}标题\n\n## 结论\n\n这是{label}的完整正文，包含一个[外部证据](https://example.com/paper)。\n",
            encoding="utf-8",
        )
    (directory / "evidence-appendix.md").write_text("# 证据附录\n\n- 证据一\n", encoding="utf-8")


class BuildResearchWikiTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.source = self.root / "work"
        self.output = self.root / "wiki" / "data"
        self.source.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_discovery_requires_all_three_versions(self) -> None:
        write_triplet(self.source / "literature-review-complete-topic-20260102")
        incomplete = self.source / "literature-review-incomplete-topic-20260103"
        incomplete.mkdir()
        (incomplete / "scientific-memo_keyan.md").write_text("# only one\n", encoding="utf-8")

        selected, stats = wiki.discover_topics(self.source)

        self.assertEqual(len(selected), 1)
        self.assertEqual(stats["skipped_incomplete"], 1)

    def test_discovery_keeps_only_newest_normalized_topic(self) -> None:
        write_triplet(self.source / "literature-review-same-topic-20260101", "同一话题")
        write_triplet(self.source / "literature-review-same-topic-20260203", "同一话题")

        selected, stats = wiki.discover_topics(self.source)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].date, "2026-02-03")
        self.assertEqual(stats["superseded_versions"], 1)

    def test_historical_english_alias_is_deduplicated(self) -> None:
        old = self.source / "literature-review-tactile-world-model-20260101"
        write_triplet(old, "旧标题")
        (old / "run.json").unlink()
        write_triplet(self.source / "literature-review-触觉世界模型-20260201", "触觉世界模型")

        selected, stats = wiki.discover_topics(self.source)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0].date, "2026-02-01")
        self.assertEqual(stats["superseded_versions"], 1)

    def test_snapshot_defaults_to_zhihu_and_validates_triplets(self) -> None:
        write_triplet(self.source / "literature-review-test-topic-20260304")

        manifest = wiki.build_snapshot(self.source, self.output)
        validated = wiki.validate_snapshot(self.output)
        topic_id = manifest["topics"][0]["id"]
        topic = json.loads((self.output / "topics" / f"{topic_id}.json").read_text(encoding="utf-8"))

        self.assertEqual(validated["site"]["default_version"], "zhihu")
        self.assertEqual(validated["site"]["title"], "空间智能研究 Wiki")
        self.assertEqual(set(topic["versions"]), {"keyan", "zhihu", "xiaohongshu"})
        self.assertTrue(topic["evidence"]["available"])
        for key, version in topic["versions"].items():
            expected = (self.source / "literature-review-test-topic-20260304" / wiki.VERSION_FILES[key][1]).read_text(encoding="utf-8")
            self.assertEqual(version["markdown"], expected)

    def test_export_contract_keeps_markdown_source_and_frontend_defaults_to_html(self) -> None:
        script = (Path(__file__).resolve().parents[1] / "wiki" / "assets" / "wiki.js").read_text(encoding="utf-8")
        index = (Path(__file__).resolve().parents[1] / "wiki" / "index.html").read_text(encoding="utf-8")
        styles = (Path(__file__).resolve().parents[1] / "wiki" / "assets" / "wiki.css").read_text(encoding="utf-8")

        self.assertIn('id="export-button"', index)
        self.assertIn('data-export-format="html"', index)
        self.assertIn('data-export-format="md"', index)
        self.assertIn("function exportTopicVersion(", script)
        self.assertIn('format === "md"', script)
        self.assertIn('exportTopicVersion(item.dataset.exportFormat || "html")', script)
        self.assertIn(".export-dropdown", styles)

    def test_catalog_source_publishes_only_routed_settled_runs(self) -> None:
        evidence = self.root / "evidence"
        routed = evidence / "literature-review-routed-20260304"
        unrouted = evidence / "literature-review-unrouted-20260305"
        write_triplet(routed, "目录话题")
        write_triplet(unrouted, "未路由话题")
        for directory in [routed, unrouted]:
            (directory / "evidence.jsonl").write_text(
                json.dumps({"event_id": "EA-TEST-0001"}) + "\n", encoding="utf-8"
            )
            manifest = json.loads((directory / "run.json").read_text(encoding="utf-8"))
            manifest.update(
                {
                    "status": "settled",
                    "files": {
                        "evidence": "evidence.jsonl",
                        "outputs": [filename for _label, filename in wiki.VERSION_FILES.values()],
                    },
                }
            )
            (directory / "run.json").write_text(
                json.dumps(manifest, ensure_ascii=False), encoding="utf-8"
            )
        knowledge = self.root / "knowledge"
        knowledge.mkdir()
        catalog = knowledge / "literature-review-catalog.md"
        catalog.write_text(
            "[run](../evidence/literature-review-routed-20260304/run.json)\n",
            encoding="utf-8",
        )

        selected, stats = wiki.discover_topics(catalog)

        self.assertEqual([item.directory.name for item in selected], [routed.name])
        self.assertEqual(stats["source_mode"], "catalog")

    def test_atomic_publish_switches_only_after_validation(self) -> None:
        write_triplet(self.source / "literature-review-test-topic-20260304")

        manifest = wiki.publish_snapshot(self.source, self.output)
        pointer = json.loads((self.output / "current.json").read_text(encoding="utf-8"))
        active = self.output / pointer["base_path"]

        self.assertFalse((self.output / "manifest.json").exists())
        self.assertTrue((active / "manifest.json").is_file())
        self.assertEqual(pointer["topic_count"], len(manifest["topics"]))
        self.assertEqual(wiki.validate_published_snapshot(self.output)["topics"], manifest["topics"])

    def test_failed_publish_preserves_previous_pointer(self) -> None:
        directory = self.source / "literature-review-test-topic-20260304"
        write_triplet(directory)
        wiki.publish_snapshot(self.source, self.output)
        previous = (self.output / "current.json").read_text(encoding="utf-8")
        (directory / "zhihu-explainer_zhihu.md").write_text(
            "# 更新稿\n\n这是足够长的更新内容，用于生成第二个候选快照。\n",
            encoding="utf-8",
        )

        def fail_before_activate(_snapshot: Path) -> None:
            raise RuntimeError("injected failure")

        with self.assertRaisesRegex(RuntimeError, "injected failure"):
            wiki.publish_snapshot(
                self.source,
                self.output,
                before_activate=fail_before_activate,
            )

        self.assertEqual((self.output / "current.json").read_text(encoding="utf-8"), previous)
        self.assertEqual(len(wiki.validate_published_snapshot(self.output)["topics"]), 1)

    def test_snapshot_id_carries_uuid_suffix(self) -> None:
        """Two publishers building identical content must never fight over one
        os.replace target, so the id is timestamp-digest-uuid."""
        write_triplet(self.source / "literature-review-test-topic-20260304")
        wiki.publish_snapshot(self.source, self.output)
        snapshot_id = json.loads((self.output / "current.json").read_text(encoding="utf-8"))[
            "snapshot_id"
        ]
        self.assertRegex(snapshot_id, r"^\d{8}T\d{6}\d+-[0-9a-f]{10}-[0-9a-f]{8}$")

    def test_prune_spares_recently_published_snapshots(self) -> None:
        """The prune age floor keeps a snapshot a slow reader may still be
        serving; it becomes deletable on a later prune past the floor."""
        import os as _os

        directory = self.source / "literature-review-test-topic-20260304"
        write_triplet(directory)
        wiki.publish_snapshot(self.source, self.output)  # s1
        first_id = json.loads((self.output / "current.json").read_text(encoding="utf-8"))[
            "snapshot_id"
        ]
        (directory / "zhihu-explainer_zhihu.md").write_text(
            "# 第二版\n\n这是第二版的完整内容，用于验证快照回滚。\n",
            encoding="utf-8",
        )
        wiki.publish_snapshot(self.source, self.output)  # s2 (rollback for s1)
        wiki.publish_snapshot(self.source, self.output)  # s3; prune would drop s1
        self.assertEqual(len(list((self.output / "snapshots").iterdir())), 3)
        wiki.prune_snapshots(self.output)  # s1 is seconds old: floor spares it
        self.assertEqual(len(list((self.output / "snapshots").iterdir())), 3)
        old_time = time.time() - 7200
        for path in (self.output / "snapshots").iterdir():
            if path.name != first_id:
                _os.utime(path, (old_time, old_time))
        wiki.prune_snapshots(self.output)  # fresh s1 still inside the floor
        self.assertIn(first_id, {p.name for p in (self.output / "snapshots").iterdir()})
        _os.utime(self.output / "snapshots" / first_id, (old_time, old_time))
        wiki.prune_snapshots(self.output)  # past the floor: deletable again
        self.assertEqual(len(list((self.output / "snapshots").iterdir())), 2)

    def test_previous_snapshot_can_be_atomically_reactivated(self) -> None:
        directory = self.source / "literature-review-test-topic-20260304"
        write_triplet(directory)
        wiki.publish_snapshot(self.source, self.output)
        first = json.loads((self.output / "current.json").read_text(encoding="utf-8"))[
            "snapshot_id"
        ]
        (directory / "zhihu-explainer_zhihu.md").write_text(
            "# 第二版\n\n这是第二版的完整内容，用于验证快照回滚。\n",
            encoding="utf-8",
        )
        wiki.publish_snapshot(self.source, self.output)
        second = json.loads((self.output / "current.json").read_text(encoding="utf-8"))[
            "snapshot_id"
        ]
        self.assertNotEqual(first, second)

        with wiki.publication_lock(self.output):
            wiki.activate_snapshot(self.output, first)

        current = json.loads((self.output / "current.json").read_text(encoding="utf-8"))
        self.assertEqual(current["snapshot_id"], first)
        self.assertEqual(len(wiki.validate_published_snapshot(self.output)["topics"]), 1)

    def test_publication_lock_rejects_concurrent_writer(self) -> None:
        """Publishers serialize across processes/machines via the KB-shared
        lock file (<output>/.locks/wiki-publish.lock); a second publisher
        waits briefly, then fails with the owner info. Same-process nesting
        is deliberately reentrant (the publisher holds it across stages)."""
        import threading

        lock_file = self.output / ".locks" / "wiki-publish.lock"
        started = threading.Event()
        release = threading.Event()

        def holder() -> None:
            with wiki.publication_lock(self.output):
                started.set()
                release.wait(10)

        thread = threading.Thread(target=holder)
        thread.start()
        self.assertTrue(started.wait(10))
        try:
            self.assertTrue(lock_file.exists())
            with mock.patch.dict(os.environ, {"EMBODIED_KB_LOCK_WAIT": "1"}):
                with self.assertRaisesRegex(RuntimeError, "超过"):
                    with wiki.publication_lock(self.output):
                        pass
        finally:
            release.set()
            thread.join(10)
        self.assertFalse(lock_file.exists())

    def test_single_style_run_publishes_declared_version_only(self) -> None:
        """A run.json declaring style+scope_note publishes with just its own
        deliverable (memo-only interviews must not require the triplet)."""
        evidence = self.root / "evidence"
        run = evidence / "literature-review-memo-only-20260909"
        run.mkdir(parents=True)
        (run / "run.json").write_text(
            json.dumps(
                {
                    "topic": "单风格话题",
                    "status": "settled",
                    "style": "scientific-memo",
                    "scope_note": "用户只要科研备忘录",
                    "files": {"outputs": ["scientific-memo_keyan.md"]},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (run / "scientific-memo_keyan.md").write_text(
            "# 单风格\n\n## 结论\n\n这是仅备忘录的完整正文，长度足够作为发布内容。\n",
            encoding="utf-8",
        )
        (run / "evidence-appendix.md").write_text("# 证据附录\n", encoding="utf-8")

        selected, _stats = wiki.discover_topics(evidence)
        self.assertEqual(len(selected), 1)

        manifest = wiki.build_snapshot(evidence, self.output)
        topic = json.loads(
            (self.output / "topics" / f"{manifest['topics'][0]['id']}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(list(topic["versions"]), ["keyan"])
        self.assertEqual(topic["available_versions"], ["keyan"])
        validated = wiki.validate_snapshot(self.output)
        self.assertEqual(validated["topics"], manifest["topics"])

    def test_declared_style_does_not_cap_extra_deliverables(self) -> None:
        """style declares the required minimum, not a cap: a memo-declared run
        that also ships the zhihu draft publishes both versions (regression for
        zhihu disappearing after a memo regeneration round)."""
        evidence = self.root / "evidence"
        run = evidence / "literature-review-memo-plus-zhihu-20260910"
        run.mkdir(parents=True)
        (run / "run.json").write_text(
            json.dumps(
                {
                    "topic": "双版本话题",
                    "status": "settled",
                    "style": "scientific-memo",
                    "scope_note": "单风格备忘录交付；知乎版为先行产出一并保留",
                    "files": {"outputs": ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md"]},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (run / "scientific-memo_keyan.md").write_text(
            "# 双版本\n\n## 结论\n\n备忘录正文，长度足够作为发布内容。\n",
            encoding="utf-8",
        )
        (run / "zhihu-explainer_zhihu.md").write_text(
            "# 双版本\n\nTL;DR：知乎版正文，长度足够作为发布内容。\n",
            encoding="utf-8",
        )
        (run / "evidence-appendix.md").write_text("# 证据附录\n", encoding="utf-8")

        selected, _stats = wiki.discover_topics(evidence)
        self.assertEqual(len(selected), 1)

        manifest = wiki.build_snapshot(evidence, self.output)
        topic = json.loads(
            (self.output / "topics" / f"{manifest['topics'][0]['id']}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(topic["available_versions"], ["keyan", "zhihu"])
        manifest_item = manifest["topics"][0]
        self.assertEqual(manifest_item["default_version"], "keyan")

    def test_revisions_publish_as_ordered_version_keys(self) -> None:
        """Chat-driven revisions/<style>-vN.md become version keys of their own
        (keyan-v2), ordered after the base style, with revision/based_on/
        request provenance — and the base deliverable stays default."""
        evidence = self.root / "evidence"
        run = evidence / "literature-review-revision-topic-20260911"
        run.mkdir(parents=True)
        (run / "run.json").write_text(
            json.dumps(
                {"topic": "修订话题", "status": "settled", "style": "scientific-memo",
                 "scope_note": "单风格", "files": {"outputs": ["scientific-memo_keyan.md"]}},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (run / "scientific-memo_keyan.md").write_text(
            "# 修订话题\n\n## 结论\n\n原始备忘录正文，长度足够作为发布内容。\n",
            encoding="utf-8",
        )
        (run / "evidence-appendix.md").write_text("# 证据附录\n", encoding="utf-8")
        revisions = run / "revisions"
        revisions.mkdir()
        (revisions / "keyan-v2.md").write_text(
            "# 修订话题\n\n## 结论\n\n按要求生成的修订正文。^[1]^\n\n## References\n\n"
            "1. Demo Paper ([arXiv:2601.00001](https://arxiv.org/abs/2601.00001))\n",
            encoding="utf-8",
        )
        (revisions / "keyan-v3.md").write_text(
            "# 修订话题\n\n## 结论\n\n第三版正文，长度足够作为发布内容。\n", encoding="utf-8"
        )
        (revisions / "index.json").write_text(
            json.dumps([
                {"version_key": "keyan-v2", "style": "keyan", "request": "开头加落地建议",
                 "created_at": "2026-09-29T10:00:00Z"},
            ], ensure_ascii=False),
            encoding="utf-8",
        )
        # A stray non-matching file must be ignored.
        (revisions / "notes.md").write_text("scratch", encoding="utf-8")

        manifest = wiki.build_snapshot(evidence, self.output)
        topic = json.loads(
            (self.output / "topics" / f"{manifest['topics'][0]['id']}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            topic["available_versions"], ["keyan", "keyan-v2", "keyan-v3"]
        )
        self.assertEqual(manifest["topics"][0]["default_version"], "keyan")
        v2 = topic["versions"]["keyan-v2"]
        self.assertEqual(v2["label"], "科研备忘录 · 修订v2")
        self.assertEqual(v2["based_on"], "keyan")
        self.assertEqual(v2["revision"], 2)
        self.assertEqual(v2["request"], "开头加落地建议")
        self.assertEqual(v2["source_file"], "revisions/keyan-v2.md")
        # keyan revisions keep the citation superscript reader links.
        self.assertIn("/api/reader/2601.00001", v2["html"])
        v3 = topic["versions"]["keyan-v3"]
        self.assertEqual(v3["revision"], 3)
        self.assertEqual(v3["request"], "")
        validated = wiki.validate_snapshot(self.output)
        self.assertEqual(validated["topics"], manifest["topics"])

    def test_run_without_revisions_is_unchanged(self) -> None:
        write_triplet(self.source / "literature-review-complete-topic-20260102")
        selected, _stats = wiki.discover_topics(self.source)
        manifest = wiki.build_snapshot(self.source, self.output)
        topic = json.loads(
            (self.output / "topics" / f"{manifest['topics'][0]['id']}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            topic["available_versions"], ["keyan", "zhihu", "xiaohongshu"]
        )

    def test_superseded_runs_publish_as_round_versions(self) -> None:
        """Re-running a whole review (same topic, e.g. re-submitted under an
        English name) must not split into two unlinked topic cards: the older
        run's deliverables publish as 第N轮综述 versions of the winner, oldest
        round first. Exercises the TOPIC_ALIASES merge too."""
        evidence = self.root / "evidence"
        old_run = evidence / "literature-review-地面箭头提取-20260928"
        new_run = evidence / "literature-review-road-marking-extraction-20260929"
        for run, topic in ((old_run, "地面箭头提取"), (new_run, "road marking extraction")):
            run.mkdir(parents=True)
            (run / "run.json").write_text(
                json.dumps({"topic": topic, "status": "settled", "style": "scientific-memo",
                            "scope_note": "单风格", "files": {"outputs": ["scientific-memo_keyan.md"]}},
                           ensure_ascii=False),
                encoding="utf-8",
            )
            (run / "scientific-memo_keyan.md").write_text(
                f"# 地面箭头提取\n\n## 结论\n\n{topic} 轮次的备忘录正文，长度足够作为发布内容。\n",
                encoding="utf-8",
            )
            (run / "evidence-appendix.md").write_text("# 证据附录\n", encoding="utf-8")

        selected, _stats = wiki.discover_topics(evidence)
        self.assertEqual(len(selected), 1, "alias must merge both runs into one topic")
        self.assertEqual(selected[0].directory, new_run)
        self.assertEqual(len(selected[0].superseded_runs), 1)

        manifest = wiki.build_snapshot(evidence, self.output)
        topic = json.loads(
            (self.output / "topics" / f"{manifest['topics'][0]['id']}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(topic["available_versions"], ["keyan", "keyan-r1"])
        r1 = topic["versions"]["keyan-r1"]
        self.assertEqual(r1["label"], "科研备忘录 · 第1轮综述")
        self.assertEqual(r1["based_on"], "keyan")
        self.assertTrue(r1["cross_run"])
        self.assertIn("地面箭头提取-20260928", r1["run_directory"])
        # The winner's own memo is still the default view.
        self.assertEqual(manifest["topics"][0]["default_version"], "keyan")
        # Old-run evidence appendix stays in the old run dir, untouched.
        self.assertTrue((old_run / "evidence-appendix.md").is_file())

    def test_survey_drafts_publish_as_standalone_versions(self) -> None:
        """The topic chat's survey-*.md draft convention used to be write-only;
        each draft now publishes as its own version key (label from the
        filename) so a hand-written or agent-drafted 补注 is versioned."""
        evidence = self.root / "evidence"
        run = evidence / "literature-review-中美具身智能路线差异-20260923"
        run.mkdir(parents=True)
        (run / "run.json").write_text(
            json.dumps({"topic": "中美具身智能路线差异以及原因", "status": "settled",
                        "style": "scientific-memo", "scope_note": "单风格",
                        "files": {"outputs": ["scientific-memo_keyan.md"]}},
                       ensure_ascii=False),
            encoding="utf-8",
        )
        (run / "scientific-memo_keyan.md").write_text(
            "# 中美路线\n\n## 结论\n\n备忘录正文，长度足够作为发布内容。\n", encoding="utf-8"
        )
        (run / "evidence-appendix.md").write_text("# 证据附录\n", encoding="utf-8")
        (run / "survey-机构层补注-中美具身智能路线差异.md").write_text(
            "# 机构层补注\n\n补注正文，长度足够作为发布内容。\n", encoding="utf-8"
        )

        manifest = wiki.build_snapshot(evidence, self.output)
        topic = json.loads(
            (self.output / "topics" / f"{manifest['topics'][0]['id']}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(topic["available_versions"], ["keyan", "survey-机构层补注-中美具身智能路线差异"])
        doc = topic["versions"]["survey-机构层补注-中美具身智能路线差异"]
        self.assertEqual(doc["label"], "机构层补注-中美具身智能路线差异")
        self.assertTrue(doc["survey"])
        self.assertEqual(doc["source_file"], "survey-机构层补注-中美具身智能路线差异.md")
        # Not a style revision: no based_on, so chips render it as a document.
        self.assertNotIn("based_on", doc)

    def test_slide_deck_field_tracks_run_folder(self) -> None:
        """The 汇报展示 manifest field flips on the presence of a compiled
        slide-deck_report.html in the run folder (run-level wiki entry)."""
        evidence = self.root / "evidence"

        def make_run(name: str, with_deck: bool = False) -> Path:
            run = evidence / name
            run.mkdir(parents=True)
            (run / "run.json").write_text(
                json.dumps(
                    {
                        "topic": name,
                        "status": "settled",
                        "style": "scientific-memo",
                        "scope_note": "单风格备忘录交付",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (run / "scientific-memo_keyan.md").write_text(
                f"# {name}\n\n## 结论\n\n备忘录正文，长度足够作为发布内容。\n", encoding="utf-8"
            )
            (run / "evidence-appendix.md").write_text("# 证据附录\n", encoding="utf-8")
            if with_deck:
                (run / "slide-deck_report.html").write_text("<!doctype html><html></html>", encoding="utf-8")
            return run

        with_deck_run = make_run("literature-review-with-deck-20260101", with_deck=True)
        make_run("literature-review-without-deck-20260102")

        manifest = wiki.build_snapshot(evidence, self.output)
        by_topic = {item["topic_key"]: item for item in manifest["topics"]}
        self.assertTrue(by_topic["with-deck"]["slide_deck_available"])
        self.assertFalse(by_topic["without-deck"]["slide_deck_available"])
        topic = json.loads(
            (self.output / "topics" / f"{by_topic['with-deck']['id']}.json").read_text(encoding="utf-8")
        )
        self.assertTrue(topic["slide_deck"]["available"])

    def test_markdown_renderer_escapes_html_and_keeps_external_links(self) -> None:
        rendered, toc = wiki.markdown_to_html(
            "# 标题\n\n<script>alert(1)</script>\n\n## 小节\n\n[论文](https://example.com/paper)\n"
        )

        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn('href="https://example.com/paper"', rendered)
        self.assertEqual([item["label"] for item in toc], ["标题", "小节"])

    def test_markdown_renderer_marks_arxiv_links_only(self) -> None:
        rendered, _toc = wiki.markdown_to_html(
            "[论文](https://arxiv.org/abs/2607.07287) 与 [项目](https://example.com/project)\n"
        )

        self.assertEqual(rendered.count('class="arxiv-icon"'), 1)
        self.assertIn(
            '<span class="arxiv-icon" aria-hidden="true">arXiv</span>'
            '<a href="https://arxiv.org/abs/2607.07287"',
            rendered,
        )
        self.assertIn('<a href="https://example.com/project"', rendered)

    def test_memo_citation_superscripts_link_through_references(self) -> None:
        markdown = (
            "# Memo\n\n"
            "主张一^[1]^，主张二^[2]^，重复引用^[1]^，未注册^[9]^。\n\n"
            "## References\n\n"
            "1. MDE-VIO: Enhancing VIO, Arda et al., 2026, "
            "[arXiv:2602.11323](https://arxiv.org/abs/2602.11323)\n"
            "2. SA-LIVO: Efficient LIVO, Yinong et al., 2026, "
            "[arXiv:2606.25699](https://arxiv.org/abs/2606.25699)\n"
        )
        html, _toc = wiki.markdown_to_html(markdown)
        linked = wiki.link_citation_superscripts(html, wiki._reference_map(markdown))

        self.assertEqual(linked.count('class="citation-link"'), 3)
        self.assertIn('href="/api/reader/2602.11323"', linked)
        self.assertIn('href="/api/reader/2606.25699"', linked)
        self.assertIn("<sup>[9]</sup>", linked)  # unresolvable stays plain

    def test_wiki_home_links_to_github_repository(self) -> None:
        index = (Path(__file__).resolve().parents[1] / "wiki" / "index.html").read_text(encoding="utf-8")

        self.assertIn('href="https://github.com/yuanzh0u/embodied-learning"', index)
        self.assertIn("GitHub 代码仓", index)
        self.assertIn('target="_blank" rel="noopener noreferrer"', index)
        self.assertIn("<title>空间智能研究 Wiki</title>", index)
        self.assertIn("<strong>空间智能研究 Wiki</strong>", index)

    def test_wiki_uses_topbar_actions_and_tree_drawer(self) -> None:
        wiki_root = Path(__file__).resolve().parents[1] / "wiki"
        index = (wiki_root / "index.html").read_text(encoding="utf-8")
        script = (wiki_root / "assets" / "wiki.js").read_text(encoding="utf-8")
        styles = (wiki_root / "assets" / "wiki.css").read_text(encoding="utf-8")
        topbar = index.split('<header class="topbar">', 1)[1].split("</header>", 1)[0]
        sidebar = index.split('<aside class="sidebar"', 1)[1].split("</aside>", 1)[0]

        self.assertIn('href="https://github.com/yuanzh0u/embodied-learning"', topbar)
        self.assertIn('href="knowledge-map/"', topbar)
        self.assertIn('id="refresh-button"', topbar)
        self.assertIn('id="topic-count"', topbar)
        self.assertIn('id="snapshot-time"', topbar)
        self.assertIn('src="assets/github-mark.svg"', topbar)
        self.assertNotIn("github.com", sidebar)
        self.assertNotIn("knowledge-map/", sidebar)
        self.assertNotIn('id="all-research"', sidebar)
        self.assertIn('id="recent-research"', sidebar)
        self.assertIn('aria-hidden="false"', index)
        self.assertIn("function renderFieldTree()", script)
        self.assertIn('class="tree-folder ${expanded ? "is-expanded" : ""}"', script)
        self.assertIn('class="tree-count"', script)
        self.assertIn('class="tree-topic-meta"', script)
        self.assertIn('return `更新于 ${value}`', script)
        self.assertIn("function syncSidebarForViewport()", script)
        self.assertIn("transform: translateX(-105%);", styles)
        self.assertIn('.tree-folder-row[aria-expanded="true"] .folder-icon::after', styles)
        self.assertIn("--paper: #f5f4f0", styles)
        self.assertNotIn("--coral:", styles)
        self.assertIn('--topbar-height: 68px', styles)
        self.assertIn('@media (max-width: 900px)', styles)
        self.assertIn('font-size: clamp(32px, 2.6vw, 38px)', styles)
        self.assertIn('.markdown-body h2 { margin: 40px 0 14px; padding-top: 4px; font-size: 22px; }', styles)
        self.assertIn('nodes.articleTitle.textContent = version.article_title', script)
        self.assertIn('if (repeatedTitle?.tagName === "H1") repeatedTitle.remove()', script)
        self.assertIn('nodes.versionArticleTitle.textContent = `所属话题：${topic.title}`', script)
        self.assertIn('空间智能研究 Wiki', script)
        self.assertIn('data/current.json', script)
        self.assertIn('state.dataBase', script)

    def test_wiki_chat_panel_contract(self) -> None:
        wiki_root = Path(__file__).resolve().parents[1] / "wiki"
        index = (wiki_root / "index.html").read_text(encoding="utf-8")
        script = (wiki_root / "assets" / "wiki.js").read_text(encoding="utf-8")
        styles = (wiki_root / "assets" / "wiki.css").read_text(encoding="utf-8")

        # Triggers: a topbar toggle and an article-level open button.
        topbar = index.split('<header class="topbar">', 1)[1].split("</header>", 1)[0]
        self.assertNotIn('id="chat-toggle"', topbar)  # duplicate trigger removed
        self.assertIn('id="chat-open-button"', index)
        self.assertIn('id="chat-panel"', index)
        self.assertIn('id="chat-messages"', index)
        self.assertIn('id="chat-input"', index)
        self.assertIn('id="chat-stop"', index)
        # JS: localhost-guarded availability, SSE stream reader, topic binding.
        self.assertIn("function streamChat(", script)
        self.assertIn("api/chat", script)
        self.assertIn("data:", script)
        self.assertIn("function syncChatAvailability()", script)
        self.assertIn("chatAvailable()", script)
        self.assertIn("getReader()", script)
        self.assertIn("function renderChatMarkdown(", script)
        # GitHub Pages has no local claude: the triggers must be hidden behind
        # the loopback-hostname guard, and no chat fetch may run there.
        self.assertIn('["localhost", "127.0.0.1", "::1"].includes(location.hostname)', script)
        self.assertIn("nodes.chatOpenButton.hidden = !available;", script)
        self.assertIn("nodes.chatOpenButton.hidden = !available;", script)
        # CSS: overlay panel above the evidence drawer, width token, mobile.
        self.assertIn("--chat-width: 420px", styles)
        self.assertIn(".chat-panel {", styles)
        self.assertIn(".chat-panel.is-open", styles)
        self.assertIn(".chat-msg-user", styles)
        self.assertIn(".chat-msg-assistant", styles)

    def test_wiki_workflow_and_resize_contract(self) -> None:
        wiki_root = Path(__file__).resolve().parents[1] / "wiki"
        index = (wiki_root / "index.html").read_text(encoding="utf-8")
        script = (wiki_root / "assets" / "wiki.js").read_text(encoding="utf-8")
        styles = (wiki_root / "assets" / "wiki.css").read_text(encoding="utf-8")

        # Chat panel resize + focus mode.
        self.assertIn('id="chat-resizer"', index)
        self.assertIn('id="chat-expand"', index)
        self.assertIn("function bindChatResizer(", script)
        self.assertIn("function setChatFocused(", script)
        self.assertIn(".chat-panel.is-focused", styles)
        self.assertIn(".chat-resizer", styles)
        # Homepage workflow hero + interview card.
        self.assertIn('id="home-chat-hero"', index)
        self.assertIn('id="home-chat-input"', index)
        self.assertIn('id="home-chat-form"', index)
        self.assertIn('id="interview-card"', index)
        self.assertIn("function startWorkflow(", script)
        self.assertIn("function showInterviewCard(", script)
        self.assertIn("api/workflow", script)
        self.assertIn("function consumeSSE(", script)
        self.assertIn("function renderTimeline(", script)
        self.assertIn("X-Workflow-Id", script)
        # Stage timeline mirrors the server's stage list.
        self.assertIn('"settle"', script)
        self.assertIn(".chat-timeline", styles)
        self.assertIn(".home-chat-hero", styles)
        self.assertIn(".interview-card", styles)

    def test_wiki_sidebar_toc_contract(self) -> None:
        """The per-page TOC lives under the left research navigation, not as a
        right-hand panel; the JS render targets keep their ids."""
        wiki_root = Path(__file__).resolve().parents[1] / "wiki"
        index = (wiki_root / "index.html").read_text(encoding="utf-8")
        script = (wiki_root / "assets" / "wiki.js").read_text(encoding="utf-8")
        styles = (wiki_root / "assets" / "wiki.css").read_text(encoding="utf-8")

        self.assertNotIn('id="toc-panel"', index)  # right-hand panel removed
        sidebar = index.split('<aside class="sidebar"', 1)[1].split("</aside>", 1)[0]
        self.assertIn('id="sidebar-toc"', sidebar)
        self.assertIn('id="toc-nav"', sidebar)
        self.assertIn('id="reading-progress"', sidebar)
        self.assertIn('tocPanel: el("sidebar-toc")', script)
        self.assertNotIn('el("toc-panel")', script)
        self.assertIn(".sidebar-toc", styles)
        self.assertNotIn(".toc-panel", styles)
        self.assertNotIn("--toc-width", styles)

    def test_wiki_reader_and_selection_quote_contract(self) -> None:
        wiki_root = Path(__file__).resolve().parents[1] / "wiki"
        index = (wiki_root / "index.html").read_text(encoding="utf-8")
        script = (wiki_root / "assets" / "wiki.js").read_text(encoding="utf-8")
        styles = (wiki_root / "assets" / "wiki.css").read_text(encoding="utf-8")

        # Same-page arXiv reader: a view inside #article-view, hash-routed,
        # cached, progressively rendered. Back returns to the topic card.
        self.assertIn('id="reader-view-header"', index)
        self.assertIn('id="reader-back-button"', index)
        self.assertIn('id="reader-open-external"', index)
        self.assertIn('id="reader-progress"', index)
        self.assertIn("function loadPaper(", script)
        self.assertIn("function parsePaperRoute(", script)
        self.assertIn("#/paper/", script)
        self.assertIn("function bindReaderLinks(", script)
        self.assertIn("api/reader/", script)
        self.assertIn("sessionStorage", script)
        self.assertIn(".reader-view-header", styles)
        self.assertIn(".reader-skel-line", styles)
        self.assertIn(".citation-link", styles)
        # Topbar 讨论 trigger sits with the search bar; the conversation stays
        # bound to each topic card.
        topbar = index.split('<header class="topbar">', 1)[1].split("</header>", 1)[0]
        self.assertIn('id="chat-open-button"', topbar)
        self.assertNotIn('id="chat-open-button"', index.split("</header>", 1)[1])
        # Dual chat panes: topic conversation vs workflow conversation.
        self.assertIn('id="chat-show-topic"', index)
        self.assertIn('id="chat-show-workflow"', index)
        # Paper chat: per-arXiv-id conversations over the shared pool.
        self.assertIn('id="chat-show-paper"', index)
        self.assertIn('id="paper-id-form"', index)
        self.assertIn("function loadPaperById(", script)
        self.assertIn("api/paper/chat", script)
        self.assertIn("function switchChatPane(", script)
        self.assertIn("function syncChatPane(", script)
        self.assertIn('state.chat.wsMessages', script)
        self.assertIn(".chat-pane-button", styles)
        # Reader formulas render via KaTeX with a graceful fallback.
        self.assertIn("katex", index)
        self.assertIn("function renderReaderMath(", script)
        # Selection → @-quote context.
        self.assertIn('id="selection-popup"', index)
        self.assertIn('id="selection-cite"', index)
        self.assertIn("function bindSelectionQuote(", script)
        self.assertIn("function composeMessageWithContext(", script)
        self.assertIn("function consumeQuotes(", script)
        self.assertIn("chat-quote-chip", styles)
        self.assertIn(".selection-popup", styles)


if __name__ == "__main__":
    unittest.main()

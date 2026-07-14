#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_kb_links.py"
SPEC = importlib.util.spec_from_file_location("check_kb_links", SCRIPT)
check_kb_links = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(check_kb_links)


def make_repo(tmp: Path) -> Path:
    """Build a minimal knowledge-base fixture inside a real git repo."""
    subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
    (tmp / "knowledge").mkdir()
    (tmp / "knowledge" / "embodied-ai").mkdir(parents=True)
    (tmp / "retired-doc.md").write_text("# Retired\n\n## Section One\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"],
        cwd=tmp,
        check=True,
    )
    ref = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=tmp, check=True, capture_output=True, text=True
    ).stdout.strip()
    (tmp / "retired-doc.md").unlink()
    return Path(ref)


def write_sources(tmp: Path, ref: str, archive_ok: bool = True) -> None:
    target = "retired-doc.md" if archive_ok else "missing-doc.md"
    (tmp / "knowledge" / "sources.md").write_text(
        "# 登记\n\n"
        "## S-TEST\n\n"
        "- 状态：retired\n"
        f"- 存档：`git show {ref}:{target}`\n",
        encoding="utf-8",
    )


def write_card(tmp: Path, ref: str, source_id: str = "S-TEST", locator: str = "§Section One") -> Path:
    card = tmp / "knowledge" / "embodied-ai" / "test-card.md"
    card.write_text(
        "---\n"
        "id: EA-TEST\n"
        "title: Test\n"
        "type: topic-card\n"
        "source:\n"
        f"  - id: {source_id}\n"
        "    status: retired\n"
        f'    archive: "git show {ref}:retired-doc.md"\n'
        f"    locator: {locator}\n"
        "---\n\n# Test\n",
        encoding="utf-8",
    )
    return card


class CheckKbLinksTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.ref = str(make_repo(self.tmp))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_clean_repo_passes(self) -> None:
        write_sources(self.tmp, self.ref)
        write_card(self.tmp, self.ref)
        problems = (
            check_kb_links.check_sources_md(self.tmp)
            + check_kb_links.check_topic_cards(self.tmp)
            + check_kb_links.check_evidence_manifests(self.tmp)
        )
        self.assertEqual(problems, [])

    def test_missing_archive_object_reported(self) -> None:
        write_sources(self.tmp, self.ref, archive_ok=False)
        problems = check_kb_links.check_sources_md(self.tmp)
        self.assertTrue(any("archive object not found" in p for p in problems))

    def test_unregistered_source_id_reported(self) -> None:
        write_sources(self.tmp, self.ref)
        write_card(self.tmp, self.ref, source_id="S-UNKNOWN")
        problems = check_kb_links.check_topic_cards(self.tmp)
        self.assertTrue(any("not registered" in p for p in problems))

    def test_evidence_run_source_is_validated_by_file_not_sources_registry(self) -> None:
        write_sources(self.tmp, self.ref)
        evidence = self.tmp / "evidence" / "literature-review-test-20260714"
        evidence.mkdir(parents=True)
        (evidence / "evidence.jsonl").write_text(
            json.dumps({"event_id": "EA-TEST-2026-0001"}) + "\n", encoding="utf-8"
        )
        card = self.tmp / "knowledge" / "embodied-ai" / "test-card.md"
        card.write_text(
            "---\n"
            "id: EA-TEST\n"
            "title: Test\n"
            "type: topic-card\n"
            "source:\n"
            "  - id: RUN-TEST-20260714\n"
            "    file: ../../evidence/literature-review-test-20260714/evidence.jsonl\n"
            "    locator: EA-TEST-2026-0001\n"
            "---\n\n# Test\n",
            encoding="utf-8",
        )
        self.assertEqual(check_kb_links.check_topic_cards(self.tmp), [])

    def test_missing_evidence_locator_event_reported(self) -> None:
        write_sources(self.tmp, self.ref)
        evidence = self.tmp / "evidence" / "literature-review-test-20260714"
        evidence.mkdir(parents=True)
        (evidence / "evidence.jsonl").write_text(
            json.dumps({"event_id": "EA-TEST-READ-0001"}) + "\n", encoding="utf-8"
        )
        card = self.tmp / "knowledge" / "embodied-ai" / "test-card.md"
        card.write_text(
            "---\n"
            "id: EA-TEST\n"
            "title: Test\n"
            "type: topic-card\n"
            "source:\n"
            "  - id: RUN-TEST-20260714\n"
            "    file: ../../evidence/literature-review-test-20260714/evidence.jsonl\n"
            "    locator: EA-TEST-READ-0001..0002\n"
            "---\n\n# Test\n",
            encoding="utf-8",
        )
        problems = check_kb_links.check_topic_cards(self.tmp)
        self.assertTrue(any("EA-TEST-READ-0002" in problem for problem in problems))

    def test_line_number_locator_reported(self) -> None:
        write_sources(self.tmp, self.ref)
        write_card(self.tmp, self.ref, locator="lines 19-110")
        problems = check_kb_links.check_topic_cards(self.tmp)
        self.assertTrue(any("line-number locator" in p for p in problems))

    def test_broken_index_link_reported(self) -> None:
        (self.tmp / "knowledge" / "index.md").write_text(
            "# Index\n\n[dead](does-not-exist.md)\n", encoding="utf-8"
        )
        problems = check_kb_links.check_index_links(self.tmp)
        self.assertTrue(any("broken link" in p for p in problems))

    def test_evidence_manifest_missing_file_reported(self) -> None:
        run_dir = self.tmp / "evidence" / "literature-review-x-20260101"
        run_dir.mkdir(parents=True)
        (run_dir / "run.json").write_text(
            json.dumps({"files": {"evidence": "evidence.jsonl", "outputs": ["memo.md"]}}),
            encoding="utf-8",
        )
        (run_dir / "evidence.jsonl").write_text("", encoding="utf-8")
        problems = check_kb_links.check_evidence_manifests(self.tmp)
        self.assertEqual(len(problems), 1)
        self.assertIn("memo.md", problems[0])

    def test_manifest_event_prefix_must_match_evidence_ids(self) -> None:
        run_dir = self.tmp / "evidence" / "literature-review-x-20260101-reader-v2"
        run_dir.mkdir(parents=True)
        (run_dir / "evidence.jsonl").write_text(
            json.dumps({"event_id": "EA-WRONG-0001"}) + "\n", encoding="utf-8"
        )
        (run_dir / "run.json").write_text(
            json.dumps(
                {
                    "event_id_prefix": "EA-TEST-READ",
                    "event_count": 1,
                    "files": {"evidence": "evidence.jsonl"},
                }
            ),
            encoding="utf-8",
        )
        problems = check_kb_links.check_evidence_manifests(self.tmp)
        self.assertTrue(any("do not match event_id_prefix" in problem for problem in problems))

    def test_manifest_event_prefix_must_be_unique(self) -> None:
        for name in ("one", "two"):
            run_dir = self.tmp / "evidence" / name
            run_dir.mkdir(parents=True)
            (run_dir / "evidence.jsonl").write_text(
                json.dumps({"event_id": f"EA-TEST-READ-{1 if name == 'one' else 2:04d}"}) + "\n",
                encoding="utf-8",
            )
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "event_id_prefix": "EA-TEST-READ",
                        "event_count": 1,
                        "files": {"evidence": "evidence.jsonl"},
                    }
                ),
                encoding="utf-8",
            )
        problems = check_kb_links.check_evidence_manifests(self.tmp)
        self.assertTrue(any("already owned" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()

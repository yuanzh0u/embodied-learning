#!/usr/bin/env python3
"""Tests for curated-list harvesting (whole-repo scan -> candidates JSON).

The extractor is pure text processing; network helpers are exercised through
mocks (no live GitHub/S2 calls), mirroring the suite's network mocking rule.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


curated_list = load("curated_list_under_test", "embodied_learning/search/curated_list.py")
registry_mod = load("candidate_registry_under_test", "embodied_learning/search/candidate_registry.py")

SAMPLE = """# Awesome Ego Video

Some prose mentioning https://arxiv.org/abs/2000.00001 outside any block.

## 🎬 Video Generation

### Datasets at a glance

| Name | Year | Scale | Key tasks | Paper | Link |
|------|------|-------|-----------|-------|------|
| WorldRover-10M | 2026 | 21.9M frames | World models | [Paper](https://arxiv.org/abs/2608.15659) | N/A |
| Ropedia | 2026 | Large | Ego pretraining | N/A | [HF](https://huggingface.co/x) |

### Entries

- **WorldRover-10M** (2026) — 6,003 synthetic exploration sequences.
  [![arXiv](https://img.shields.io/badge/arXiv-2608.15659-b31b1b.svg)](https://arxiv.org/abs/2608.15659)

- **EgoVid-5M** (2024) — 5M clips for video generation.
  [![arXiv](https://img.shields.io/badge/arXiv-2411.08380-b31b1b.svg)](https://arxiv.org/pdf/2411.08380v2)

- **EPIC-KITCHENS-100** (2022) — the scale-up of EPIC-KITCHENS.
  [![Springer](https://img.shields.io/badge/Springer-blue.svg)](https://link.springer.com/article/10.1007/s11263-022-01642-6)

- **Legacy ID paper** (2013) — old-style arXiv identifier.
  [![arXiv](https://img.shields.io/badge/arXiv-1301.0001.svg)](https://arxiv.org/abs/1301.0001)
"""


class ExtractCandidatesTest(unittest.TestCase):
    def test_bullet_badge_pdf_and_table_rows(self) -> None:
        candidates, unresolved = curated_list.extract_candidates(SAMPLE, "README.md")
        by_id = {item["arxiv_id"]: item for item in candidates}
        self.assertIn("2608.15659", by_id)
        self.assertIn("2411.08380", by_id)
        # pdf link + version suffix normalized; bullet marker kept verbatim
        self.assertEqual(by_id["2411.08380"]["context"].split(" — ")[0], "- **EgoVid-5M** (2024)")
        # bullet context outranks the earlier table-row mention
        self.assertEqual(by_id["2608.15659"]["block_kind"], "bullet")
        self.assertEqual(by_id["2608.15659"]["title"], "WorldRover-10M")
        self.assertEqual(by_id["2608.15659"]["year"], 2026)
        self.assertEqual(by_id["2608.15659"]["section"], "Awesome Ego Video > 🎬 Video Generation > Entries")

    def test_prose_mentions_are_not_entries(self) -> None:
        candidates, _ = curated_list.extract_candidates(SAMPLE, "README.md")
        self.assertNotIn("2000.00001", {item["arxiv_id"] for item in candidates})

    def test_no_arxiv_bullet_is_unresolved_with_link(self) -> None:
        _, unresolved = curated_list.extract_candidates(SAMPLE, "README.md")
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0]["title"], "EPIC-KITCHENS-100")
        self.assertTrue(unresolved[0]["link"].startswith("https://link.springer.com/"))
        self.assertNotIn("shields.io", unresolved[0]["link"])

    def test_dedupe_keeps_single_record_per_id(self) -> None:
        candidates, _ = curated_list.extract_candidates(SAMPLE, "README.md")
        ids = [item["arxiv_id"] for item in candidates]
        self.assertEqual(len(ids), len(set(ids)))


class ResolveUnresolvedTest(unittest.TestCase):
    def test_s2_title_match_attaches_arxiv_id(self) -> None:
        payload = json.dumps({
            "data": [{"title": "EPIC-KITCHENS-100 2022", "externalIds": {"ArXiv": "2204.11120v1"}}]
        }).encode()
        with mock.patch.object(curated_list, "_http_get", return_value=payload) as get, \
             mock.patch.object(curated_list.time, "sleep"):
            resolved, still = curated_list.resolve_unresolved(
                [{"title": "EPIC-KITCHENS-100", "context": "c", "section": "s",
                  "link": "https://link.springer.com/x", "source": "README.md"}]
            )
        self.assertEqual(still, [])
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["arxiv_id"], "2204.11120")
        self.assertIn("query=EPIC-KITCHENS", get.call_args[0][0])

    def test_failure_stays_unresolved(self) -> None:
        with mock.patch.object(curated_list, "_http_get", side_effect=OSError("boom")), \
             mock.patch.object(curated_list.time, "sleep"):
            resolved, still = curated_list.resolve_unresolved(
                [{"title": "No such paper", "context": "c", "section": "s",
                  "link": "https://example.com", "source": "README.md"}]
            )
        self.assertEqual(resolved, [])
        self.assertEqual(len(still), 1)
        self.assertTrue(still[0]["reason"].startswith("s2-resolve-failed"))


class HarvestTest(unittest.TestCase):
    def test_harvest_shape_matches_registry_loader(self) -> None:
        files = [("README.md", SAMPLE), ("CONTRIBUTING.md", "- **Extra** (2025) [arXiv](https://arxiv.org/abs/2501.00001)")]
        with mock.patch.object(curated_list, "fetch_repo_files", return_value=files), \
             mock.patch.object(curated_list, "resolve_unresolved", return_value=([], [])):
            payload = curated_list.harvest("player0718/awesome-ego-video-datasets", resolve_missing=True)
        self.assertEqual(payload["channel_hint"], "curated-list")
        self.assertEqual(payload["files_scanned"], ["README.md", "CONTRIBUTING.md"])  # fetch order kept
        ids = {item["arxiv_id"] for item in payload["candidates"]}
        self.assertEqual(ids, {"2608.15659", "2411.08380", "1301.0001", "2501.00001"})

        # The output must be ingestible by the registry's curated-list channel.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "harvest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            registry_mod.run([], [], [], [], None, Path(tmp) / "registry.json", [path])
            data = json.loads((Path(tmp) / "registry.json").read_text(encoding="utf-8"))
        record = next(item for item in data["candidates"] if item["arxiv_id"] == "2608.15659")
        self.assertEqual(record["discoveries"][0]["channel"], "curated-list")
        self.assertEqual(record["title"], "WorldRover-10M")
        self.assertEqual(record["discovery_context"], "- **WorldRover-10M** (2026) — 6,003 synthetic exploration sequences.")


class ResolveViaSnapshotTest(unittest.TestCase):
    def test_title_match_attaches_snapshot_id(self) -> None:
        db_mod = load("snapshot_db_for_curated_test", "embodied_learning/search/arxiv_snapshot_db.py")
        records = [
            {"id": "2402.14169", "title": "EgoExoLearn: A Dataset for Bridging Asynchronous Ego- and Exo-centric View",
             "abstract": "", "authors": "", "categories": "cs.CV", "versions": [], "update_date": "2024-03-01",
             "comments": "", "journal-ref": ""},
            {"id": "9999.99999", "title": "Unrelated Paper About Motion", "abstract": "", "authors": "",
             "categories": "cs.CV", "versions": [], "update_date": "2024-03-01", "comments": "", "journal-ref": ""},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            jsonl = Path(tmp) / "snap.json"
            jsonl.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")
            db = str(Path(tmp) / "snap.sqlite")  # build_db refuses an existing path
            db_mod.build_db(str(jsonl), db, progress_every=10**9)
            resolved, still = curated_list.resolve_via_snapshot(
                [{"title": "EgoExoLearn: A Dataset for Bridging Asynchronous Ego- and Exo-centric View of Procedural Activities",
                  "context": "c", "section": "s", "link": "https://openaccess.thecvf.com/x", "source": "README.md"}],
                db,
            )
        self.assertEqual(still, [])
        self.assertEqual(len(resolved), 1)
        self.assertEqual(resolved[0]["arxiv_id"], "2402.14169")
        self.assertEqual(resolved[0]["block_kind"], "snapshot-title-resolved")


class CliDispatchTest(unittest.TestCase):
    def test_subcommand_registered(self) -> None:
        search = load("search_cli_under_test", "skills/embodied-ai-literature-hub/scripts/search.py")
        self.assertIn("harvest-curated-list", search._SUBCOMMANDS)
        args = search._harvest_curated_list_parse_args(["--repo", "a/b", "--no-resolve"])
        self.assertEqual(args.repo, "a/b")
        self.assertTrue(args.no_resolve)


if __name__ == "__main__":
    unittest.main()

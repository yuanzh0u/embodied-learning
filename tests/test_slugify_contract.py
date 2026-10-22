#!/usr/bin/env python3
"""Contract tests: the run-folder name `literature-review-<topic>-<date>` has
exactly one slug implementation (wiki.run.manifest) and every caller agrees.

The folder name is an external contract (ADR 0003): catalog rows, evidence/
paths and wiki links all embed it. Two divergent slug copies (init_run vs
build_review_packet) once encoded the CJK range differently — same behavior,
but a future edit to one would silently fork the namespace."""

from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.wiki.run.manifest import (  # noqa: E402
    parse_run_folder_version,
    run_folder_name,
    slugify_topic,
)
from embodied_learning.writer import packet  # noqa: E402


SAMPLES = (
    "UMI data usability",
    "4D 时空推理",
    "单目深度估计 SLAM",
    "LiDAR/SLAM-Calibration: A Survey",
    "  多余   空格  ",
)


class SlugifyContractTest(unittest.TestCase):
    def test_folder_name_shape(self) -> None:
        name = run_folder_name("demo topic", "20260101")
        self.assertEqual(name, "literature-review-demo-topic-20260101")

    def test_packet_and_manifest_agree(self) -> None:
        for topic in SAMPLES:
            self.assertEqual(packet.slugify_topic(topic), slugify_topic(topic), topic)

    def test_slug_is_stable_and_bounded(self) -> None:
        for topic in SAMPLES:
            slug = slugify_topic(topic)
            self.assertLessEqual(len(slug), 72)
            self.assertTrue(slug)
            self.assertNotRegex(slug, r"--")
            self.assertEqual(slug, slug.strip("-._"))

    def test_empty_topic_falls_back(self) -> None:
        self.assertEqual(slugify_topic(""), "review")
        self.assertEqual(slugify_topic("///"), "review")


class RunVersionContractTest(unittest.TestCase):
    """Same topic, repeat production: the version mark is explicit and round-trips
    through the folder name. v1 keeps the bare ADR 0003 name."""

    def test_v1_is_the_bare_contract_name(self) -> None:
        self.assertEqual(run_folder_name("图像分割", "20261012", 1), "literature-review-图像分割-20261012")
        self.assertEqual(run_folder_name("图像分割", "20261012"), "literature-review-图像分割-20261012")

    def test_v2_appends_version_suffix(self) -> None:
        self.assertEqual(run_folder_name("图像分割", "20261012", 2), "literature-review-图像分割-20261012-v2")
        self.assertEqual(run_folder_name("图像分割", "20261012", 12), "literature-review-图像分割-20261012-v12")

    def test_version_round_trips(self) -> None:
        for version in (1, 2, 7, 12):
            name = run_folder_name("人体姿态估计", "20261012", version)
            self.assertEqual(parse_run_folder_version(name), version, name)

    def test_parse_defaults_to_v1(self) -> None:
        self.assertEqual(parse_run_folder_version("literature-review-图像分割-20260101"), 1)
        self.assertEqual(parse_run_folder_version("literature-review-review-20260101"), 1)

    def test_reader_suffix_is_not_a_run_version(self) -> None:
        # -reader-vN is the wiki reader-article rank (snapshot._READER_SUFFIX),
        # not a run-folder version mark — the run name never carries it.
        name = run_folder_name("demo", "20260101", 3)
        self.assertEqual(parse_run_folder_version(name), 3)
        self.assertNotIn("-reader-", name)

    def test_default_project_dir_uses_the_same_version_mark(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            work_dir = Path(tmp)
            first = packet.default_project_dir(work_dir, "图像分割", dt.date(2026, 10, 12))
            self.assertEqual(first.name, "literature-review-图像分割-20261012")
            first.mkdir()
            second = packet.default_project_dir(work_dir, "图像分割", dt.date(2026, 10, 12))
            self.assertEqual(second.name, "literature-review-图像分割-20261012-v2")


if __name__ == "__main__":
    unittest.main()

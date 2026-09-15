#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "src" / "fetch" / "legacy" / "download_arxiv_source.py"
SPEC = importlib.util.spec_from_file_location("download_arxiv_source", SCRIPT_PATH)
das = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(das)


class NoSuchKey(Exception):
    pass


class FakeBody:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def iter_chunks(self, chunk_size: int):
        view = memoryview(self.payload)
        for start in range(0, len(view), chunk_size):
            yield bytes(view[start : start + chunk_size])


class FakeS3Client:
    """Minimal stand-in for the anonymous boto3 client."""

    def __init__(self, objects: dict[str, bytes] | None = None) -> None:
        self.objects = objects or {}
        self.calls: list[tuple[str, str]] = []
        self.exceptions = type("exceptions", (), {"NoSuchKey": NoSuchKey})

    def get_object(self, Bucket: str, Key: str, **kwargs: object):
        self.calls.append((Bucket, Key))
        if Key not in self.objects:
            raise NoSuchKey(Key)
        return {"Body": FakeBody(self.objects[Key])}


def download_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "cache_dir": "/tmp/nonexistent-src-cache",
        "force": False,
        "retries": 2,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def tarball_bytes(members: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name, text in members.items():
            data = text.encode("utf-8")
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


class SourceKeyTest(unittest.TestCase):
    def test_modern_ids_map_to_src_yymm_keys(self) -> None:
        self.assertEqual(das.source_key("2403.12550"), "src/2403/2403.12550.tar.gz")
        self.assertEqual(das.source_key("2607.04127"), "src/2607/2607.04127.tar.gz")

    def test_old_style_and_pre_0704_ids_are_unsupported(self) -> None:
        self.assertIsNone(das.source_key("cat/0501001"))
        self.assertIsNone(das.source_key("0501001"))
        self.assertIsNone(das.source_key("math.GT/0601136"))

    def test_version_suffix_is_stripped_by_normalize(self) -> None:
        self.assertEqual(das.normalize_id("2403.12550v2"), "2403.12550")


class DownloadOneTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.cache = str(Path(self._tmp.name) / "src")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_downloads_tarball_and_reports_state(self) -> None:
        payload = tarball_bytes({"main.tex": "\\begin{document}hi\\end{document}"})
        client = FakeS3Client({"src/2403/2403.12550.tar.gz": payload})
        result = das.download_one("2403.12550", download_args(cache_dir=self.cache), client)
        self.assertEqual(result["state"], "downloaded")
        self.assertEqual(result["bytes"], len(payload))
        self.assertTrue(Path(result["path"]).is_file())

    def test_second_call_hits_cache(self) -> None:
        payload = tarball_bytes({"main.tex": "x"})
        client = FakeS3Client({"src/2403/2403.12550.tar.gz": payload})
        das.download_one("2403.12550", download_args(cache_dir=self.cache), client)
        result = das.download_one("2403.12550", download_args(cache_dir=self.cache), client)
        self.assertEqual(result["state"], "cached")
        self.assertEqual(len(client.calls), 1)

    def test_404_reports_no_source_without_retry_sleep(self) -> None:
        client = FakeS3Client()
        with mock.patch.object(das.time, "sleep") as sleep:
            result = das.download_one("2403.12550", download_args(cache_dir=self.cache), client)
        self.assertEqual(result["state"], "no-source")
        self.assertIn("not found", result["error"])
        sleep.assert_not_called()

    def test_old_style_id_is_no_source_without_network(self) -> None:
        client = FakeS3Client()
        result = das.download_one("cat/0501001", download_args(cache_dir=self.cache), client)
        self.assertEqual(result["state"], "no-source")
        self.assertEqual(client.calls, [])

    def test_transient_error_retries_then_errors(self) -> None:
        class FlakyClient(FakeS3Client):
            def get_object(self, Bucket: str, Key: str, **kwargs: object):
                self.calls.append((Bucket, Key))
                if len(self.calls) < 3:
                    raise OSError("connection reset")
                return super().get_object(Bucket, Key, **kwargs)

        payload = tarball_bytes({"main.tex": "x"})
        client = FlakyClient({"src/2403/2403.12550.tar.gz": payload})
        with mock.patch.object(das.time, "sleep") as sleep:
            result = das.download_one("2403.12550", download_args(cache_dir=self.cache), client)
        self.assertEqual(result["state"], "downloaded")
        self.assertEqual(sleep.call_count, 2)

    def test_force_redownloads_despite_cache(self) -> None:
        payload = tarball_bytes({"main.tex": "x"})
        client = FakeS3Client({"src/2403/2403.12550.tar.gz": payload})
        das.download_one("2403.12550", download_args(cache_dir=self.cache), client)
        result = das.download_one("2403.12550", download_args(cache_dir=self.cache, force=True), client)
        self.assertEqual(result["state"], "downloaded")
        self.assertEqual(len(client.calls), 2)


class RunQueueTest(unittest.TestCase):
    def test_queue_dedupes_and_counts_states(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        try:
            args = download_args(cache_dir=str(Path(tmp.name) / "src"))
            args.paper_id = ["2403.12550", "2403.12550v2"]
            args.paper_id_file = None
            args.workers = 4
            payload = tarball_bytes({"main.tex": "x"})
            client = FakeS3Client({"src/2403/2403.12550.tar.gz": payload})
            summary = das.run_queue(args, client)
            self.assertEqual(summary["paper_count"], 1)
            self.assertEqual(summary["states"], {"downloaded": 1})
        finally:
            tmp.cleanup()

    def test_worker_cap_is_enforced(self) -> None:
        args = download_args()
        args.paper_id = ["2403.12550"]
        args.paper_id_file = None
        args.workers = 999
        client = FakeS3Client()
        summary = das.run_queue(args, client)
        self.assertEqual(summary["workers"], das.MAX_WORKERS)


if __name__ == "__main__":
    unittest.main()

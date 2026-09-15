#!/usr/bin/env python3

from __future__ import annotations

import argparse
import email.message
import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "src" / "search" / "legacy" / "search_semantic_scholar.py"
SPEC = importlib.util.spec_from_file_location("search_semantic_scholar", SCRIPT_PATH)
s2 = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(s2)


class DummyResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def __enter__(self) -> "DummyResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


def base_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "max_results": 2,
        "sort_by": "relevance",
        "sort_order": "descending",
        "sleep_seconds": 0.0,
        "timeout": 1.0,
        "retries": 3,
        "retry_base_seconds": 5.0,
        "retry_max_seconds": 60.0,
        "fail_fast": False,
        "api_key": None,
        "cache_dir": "/tmp/nonexistent-s2-cache",
        "no_cache": True,
        "user_agent": "test-agent",
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = email.message.Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError(s2.API_BASE, code, "error", headers, None)


def search_page(entries: list[dict], next_offset: int | None = None) -> bytes:
    payload: dict = {"total": len(entries), "offset": 0, "data": entries}
    if next_offset is not None:
        payload["next"] = next_offset
    return json.dumps(payload).encode("utf-8")


def entry(arxiv: str | None, published: str = "2026-05-01", title: str = "A Paper") -> dict:
    external: dict = {}
    if arxiv is not None:
        external["ArXiv"] = arxiv
    return {
        "title": title,
        "abstract": "An abstract.",
        "publicationDate": published,
        "authors": [{"name": "Alice"}],
        "externalIds": external,
        "fieldsOfStudy": ["Computer Science"],
        "citationCount": 4,
    }


class ParsePaperTest(unittest.TestCase):
    def test_maps_s2_hit_to_search_arxiv_paper_shape(self) -> None:
        paper = s2.parse_paper(entry("2605.12345"), "q1", "eff")
        assert paper is not None
        self.assertEqual(paper["arxiv_id"], "2605.12345")
        self.assertEqual(paper["published"], "2026-05-01")
        self.assertEqual(paper["pdf_url"], "https://arxiv.org/pdf/2605.12345.pdf")
        self.assertEqual(paper["authors"], ["Alice"])
        self.assertEqual(paper["citation_count"], 4)

    def test_returns_none_without_arxiv_crosswalk(self) -> None:
        self.assertIsNone(s2.parse_paper(entry(None), "q1", "eff"))

    def test_in_window_bounds_are_inclusive_and_blank_dates_rejected(self) -> None:
        self.assertTrue(s2.in_window("2026-01-01", "2026-01-01", "2026-12-31"))
        self.assertTrue(s2.in_window("2026-12-31", "2026-01-01", "2026-12-31"))
        self.assertFalse(s2.in_window("2025-12-31", "2026-01-01", "2026-12-31"))
        self.assertFalse(s2.in_window("", "2026-01-01", "2026-12-31"))


class FetchRetryTest(unittest.TestCase):
    def test_fetch_retries_429_with_retry_after(self) -> None:
        error = http_error(429, retry_after="7")
        with mock.patch.object(s2.urllib.request, "urlopen", side_effect=[error, DummyResponse(b"{}")]) as urlopen:
            with mock.patch.object(s2.time, "sleep") as sleep:
                payload = s2.fetch(s2.build_search_url("robot", 0, 10), base_args())

        self.assertEqual(payload, b"{}")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(7.0)

    def test_fetch_does_not_retry_non_transient_errors(self) -> None:
        with mock.patch.object(s2.urllib.request, "urlopen", side_effect=http_error(400)) as urlopen:
            with mock.patch.object(s2.time, "sleep") as sleep:
                with self.assertRaisesRegex(RuntimeError, "after 1 attempt"):
                    s2.fetch(s2.build_search_url("robot", 0, 10), base_args())
        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()

    def test_api_key_header_sent_from_env(self) -> None:
        captured: dict[str, str] = {}

        def fake_urlopen(request: object, timeout: float) -> DummyResponse:
            captured.update(dict(request.header_items()))  # type: ignore[attr-defined]
            return DummyResponse(b"{}")

        with mock.patch.object(s2.urllib.request, "urlopen", side_effect=fake_urlopen):
            with mock.patch.dict("os.environ", {"S2_API_KEY": "secret-key"}):
                s2.fetch(s2.build_search_url("robot", 0, 10), base_args())
        self.assertEqual(captured.get("X-api-key"), "secret-key")


class CacheTest(unittest.TestCase):
    def test_cache_hit_skips_urlopen(self) -> None:
        url = s2.build_search_url("robot", 0, 10)
        with tempfile.TemporaryDirectory() as tmp:
            s2.write_cache(tmp, url, b'{"data": []}', True)
            with mock.patch.object(s2.urllib.request, "urlopen") as urlopen:
                payload = s2.fetch_cached(url, base_args(cache_dir=tmp, no_cache=False))
            self.assertEqual(payload, b'{"data": []}')
            urlopen.assert_not_called()

    def test_no_cache_bypasses_reads_and_writes(self) -> None:
        url = s2.build_search_url("robot", 0, 10)
        with tempfile.TemporaryDirectory() as tmp:
            args = base_args(cache_dir=tmp, no_cache=True)
            with mock.patch.object(s2.urllib.request, "urlopen", return_value=DummyResponse(b'{"data": []}')):
                s2.fetch_cached(url, args)
            self.assertIsNone(s2.read_cache(tmp, url, True))


class CollectPapersTest(unittest.TestCase):
    def test_collects_paginated_hits_and_counts_crosswalk_exclusions(self) -> None:
        pages = [
            search_page([entry("2605.00001"), entry(None), entry("2605.00002")]),
            search_page([entry("2605.00003", published="2027-01-01")]),  # short page ends pagination
        ]
        with mock.patch.object(s2.urllib.request, "urlopen", side_effect=[DummyResponse(p) for p in pages]):
            papers, excluded = s2.collect_papers("robot", "core", base_args())
        self.assertEqual([p["arxiv_id"] for p in papers], ["2605.00001", "2605.00002"])
        self.assertEqual(excluded, 1)

    def test_pub_date_sort_orders_descending(self) -> None:
        page = search_page([entry("2605.00001", published="2026-02-01"), entry("2605.00002", published="2026-06-01")])
        with mock.patch.object(s2.urllib.request, "urlopen", side_effect=[DummyResponse(page)]):
            papers, _ = s2.collect_papers("robot", "core", base_args(sort_by="pub_date"))
        self.assertEqual([p["arxiv_id"] for p in papers], ["2605.00002", "2605.00001"])


if __name__ == "__main__":
    unittest.main()

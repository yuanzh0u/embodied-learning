#!/usr/bin/env python3

from __future__ import annotations

import argparse
import email.message
import importlib.util
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "embodied_learning" / "search" / "arxiv.py"
SPEC = importlib.util.spec_from_file_location("search_arxiv", SCRIPT_PATH)
search_arxiv = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(search_arxiv)


class DummyResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def __enter__(self) -> "DummyResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


def args_with_retries(retries: int) -> search_arxiv.ArxivSearch:
    return search_arxiv.ArxivSearch(
        start_date="2024-01-01",
        end_date="2024-12-31",
        max_results=1,
        sort_by="submittedDate",
        sort_order="descending",
        timeout=1.0,
        user_agent="test-agent",
        retries=retries,
        retry_base_seconds=5.0,
        retry_max_seconds=60.0,
    )


def args_with_retry_waits(base_seconds: float, max_seconds: float) -> search_arxiv.ArxivSearch:
    searcher = args_with_retries(3)
    searcher.retry_base_seconds = base_seconds
    searcher.retry_max_seconds = max_seconds
    return searcher


def http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = email.message.Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://export.arxiv.org/api/query", code, "error", headers, None)


class SearchArxivRetryTest(unittest.TestCase):
    def test_fetch_retries_429_with_retry_after_and_caps_at_three_retries(self) -> None:
        error = http_error(429, retry_after="7")
        with mock.patch.object(search_arxiv.urllib.request, "urlopen", side_effect=[error, error, error, error]) as urlopen:
            with mock.patch.object(search_arxiv.time, "sleep") as sleep:
                with self.assertRaises(RuntimeError):
                    args_with_retries(99).fetch("all:robot")

        self.assertEqual(urlopen.call_count, 4)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [7.0, 7.0, 7.0])

    def test_fetch_succeeds_after_429_retry(self) -> None:
        with mock.patch.object(
            search_arxiv.urllib.request,
            "urlopen",
            side_effect=[http_error(429, retry_after="2"), DummyResponse(b"<feed />")],
        ) as urlopen:
            with mock.patch.object(search_arxiv.time, "sleep") as sleep:
                payload = args_with_retries(3).fetch("all:robot")

        self.assertEqual(payload, b"<feed />")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(2.0)

    def test_fetch_does_not_retry_non_transient_http_errors(self) -> None:
        with mock.patch.object(search_arxiv.urllib.request, "urlopen", side_effect=http_error(400)) as urlopen:
            with mock.patch.object(search_arxiv.time, "sleep") as sleep:
                with self.assertRaisesRegex(RuntimeError, "after 1 attempt"):
                    args_with_retries(3).fetch("bad-query")

        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()

    def test_retry_wait_is_never_negative(self) -> None:
        self.assertEqual(
            args_with_retry_waits(5, -1).retry_wait_seconds(http_error(429, retry_after="7"), 0),
            0.0,
        )
        self.assertEqual(
            args_with_retry_waits(-5, 60).retry_wait_seconds(TimeoutError("timeout"), 0),
            0.0,
        )


if __name__ == "__main__":
    unittest.main()

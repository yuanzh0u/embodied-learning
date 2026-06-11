#!/usr/bin/env python3

from __future__ import annotations

import argparse
import email.message
import importlib.util
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "search_arxiv.py"
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


def args_with_retries(retries: int) -> argparse.Namespace:
    return argparse.Namespace(
        max_results=1,
        sort_by="submittedDate",
        sort_order="descending",
        timeout=1.0,
        user_agent="test-agent",
        retries=retries,
        retry_base_seconds=5.0,
        retry_max_seconds=60.0,
    )


def args_with_retry_waits(base_seconds: float, max_seconds: float) -> argparse.Namespace:
    args = args_with_retries(3)
    args.retry_base_seconds = base_seconds
    args.retry_max_seconds = max_seconds
    return args


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
                    search_arxiv.fetch("all:robot", args_with_retries(99))

        self.assertEqual(urlopen.call_count, 4)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [7.0, 7.0, 7.0])

    def test_fetch_succeeds_after_429_retry(self) -> None:
        with mock.patch.object(
            search_arxiv.urllib.request,
            "urlopen",
            side_effect=[http_error(429, retry_after="2"), DummyResponse(b"<feed />")],
        ) as urlopen:
            with mock.patch.object(search_arxiv.time, "sleep") as sleep:
                payload = search_arxiv.fetch("all:robot", args_with_retries(3))

        self.assertEqual(payload, b"<feed />")
        self.assertEqual(urlopen.call_count, 2)
        sleep.assert_called_once_with(2.0)

    def test_fetch_does_not_retry_non_transient_http_errors(self) -> None:
        with mock.patch.object(search_arxiv.urllib.request, "urlopen", side_effect=http_error(400)) as urlopen:
            with mock.patch.object(search_arxiv.time, "sleep") as sleep:
                with self.assertRaisesRegex(RuntimeError, "after 1 attempt"):
                    search_arxiv.fetch("bad-query", args_with_retries(3))

        self.assertEqual(urlopen.call_count, 1)
        sleep.assert_not_called()

    def test_retry_wait_is_never_negative(self) -> None:
        self.assertEqual(
            search_arxiv.retry_wait_seconds(http_error(429, retry_after="7"), 0, args_with_retry_waits(5, -1)),
            0.0,
        )
        self.assertEqual(
            search_arxiv.retry_wait_seconds(TimeoutError("timeout"), 0, args_with_retry_waits(-5, 60)),
            0.0,
        )


if __name__ == "__main__":
    unittest.main()

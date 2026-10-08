#!/usr/bin/env python3

from __future__ import annotations

import argparse
import contextlib
import email.message
import importlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from contextlib import nullcontext
from unittest import mock


# Package import: search/arxiv.py does `from .. import ratelimit`, which needs
# package context (a bare spec_from_file_location load breaks).
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
search_arxiv = importlib.import_module("embodied_learning.search.arxiv")


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
    def setUp(self) -> None:
        # These tests exercise the module's own retry/backoff (with time.sleep
        # mocked). Bypass the machine-wide rate-limit gate — its behavior is
        # covered separately in tests/test_ratelimit.py — otherwise the gate's
        # real sleeps pollute the sleep-call assertions.
        patcher = mock.patch.object(search_arxiv.ratelimit, "gate", lambda *a, **k: nullcontext())
        patcher.start()
        self.addCleanup(patcher.stop)

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


class SearchArxivExitCodeTest(unittest.TestCase):
    """Partial-batch exit contract of ArxivSearch.run (shared by all searchers
    via report_partial_batch): failed queries are recorded, hits are kept, and
    the caller sees a non-zero exit plus a stderr WARNING."""

    def run_main(self, fetch_side_effect: list[object]) -> tuple[int, str, dict]:
        queries = [
            {"label": "q-one", "query": "all:alpha"},
            {"label": "q-two", "query": "all:beta"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            output_file = Path(tmp) / "out.json"
            searcher = search_arxiv.ArxivSearch(
                start_date="2026-01-01",
                end_date="2026-06-30",
                output=str(output_file),
            )
            stderr = io.StringIO()
            with mock.patch.object(search_arxiv.ratelimit, "gate", lambda *a, **k: nullcontext()):
                with mock.patch.object(search_arxiv.time, "sleep"):
                    with mock.patch.object(search_arxiv.ArxivSearch, "fetch", side_effect=fetch_side_effect):
                        with contextlib.redirect_stderr(stderr):
                            code = searcher.run(queries)
            return code, stderr.getvalue(), json.loads(output_file.read_text(encoding="utf-8"))

    def test_partial_failure_exits_nonzero_and_warns(self) -> None:
        code, stderr, output = self.run_main([RuntimeError("arXiv request failed: 429"), b"<feed />"])

        self.assertEqual(1, code)
        self.assertIn("1/2 queries failed", stderr)
        self.assertIn("q-one", stderr)
        self.assertIn("429", output["queries"][0]["error"])
        self.assertNotIn("error", output["queries"][1])
        self.assertEqual(0, output["paper_count"])

    def test_all_success_exits_zero_without_warning(self) -> None:
        code, stderr, output = self.run_main([b"<feed />", b"<feed />"])

        self.assertEqual(0, code)
        self.assertEqual("", stderr)
        self.assertEqual(0, output["paper_count"])


if __name__ == "__main__":
    unittest.main()

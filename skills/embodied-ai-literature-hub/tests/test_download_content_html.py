#!/usr/bin/env python3
"""Tests for embodied_learning.fetch.html_queue — extraction step 1 (batch HTML download).

Network is fully mocked at ``html.fetch_html``; the machine-wide ratelimit gate
state is redirected so tests never touch the real shared cache.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

os.environ.setdefault("EMBODIED_RATELIMIT_DIR", tempfile.mkdtemp(prefix="ratelimit-test-"))

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from embodied_learning.fetch import html_queue  # noqa: E402
from embodied_learning.ratelimit import GateTimeout  # noqa: E402


def _opts(tmp: Path, **kwargs) -> html_queue.HtmlDownloadOptions:
    defaults = dict(
        paper_id_file=str(tmp / "ids.txt"),
        html_cache_dir=str(tmp / "html"),
        workers=1,
        timeout=5.0,
        retries=3,
    )
    defaults.update(kwargs)
    return html_queue.HtmlDownloadOptions(**defaults)


class DownloadOneTest(unittest.TestCase):
    def test_cache_hit_short_circuits_without_fetching(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            (tmp / "html" / "2402.10329.html").write_text("<html>hi</html>", encoding="utf-8")
            with mock.patch.object(html_queue.extract_arxiv_html, "fetch_html") as fetch:
                result = html_queue.download_one("2402.10329", _opts(tmp))
            self.assertEqual(result["state"], "cached")
            fetch.assert_not_called()

    def test_clean_404_is_unavailable_and_never_retried(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            with mock.patch.object(
                html_queue.extract_arxiv_html, "fetch_html", return_value=(False, "")
            ) as fetch:
                result = html_queue.download_one("2402.10329", _opts(tmp))
            self.assertEqual(result["state"], "unavailable")
            self.assertEqual(result["attempts"], 1)
            self.assertEqual(result["status"], 404)
            fetch.assert_called_once()

    def test_transient_failure_retries_then_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            boom = urllib.error.URLError("connection reset")
            with mock.patch.object(
                html_queue.extract_arxiv_html,
                "fetch_html",
                side_effect=[boom, boom, (True, "<html>x</html>")],
            ) as fetch, mock.patch.object(html_queue.time, "sleep") as sleep:
                result = html_queue.download_one("2402.10329", _opts(tmp))
            self.assertEqual(result["state"], "downloaded")
            self.assertEqual(result["attempts"], 3)
            self.assertEqual(fetch.call_count, 3)
            self.assertEqual(sleep.call_count, 2)

    def test_persistent_transient_failure_exhausts_retries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            boom = urllib.error.URLError("timed out")
            with mock.patch.object(
                html_queue.extract_arxiv_html, "fetch_html", side_effect=boom
            ) as fetch, mock.patch.object(html_queue.time, "sleep"):
                result = html_queue.download_one("2402.10329", _opts(tmp, retries=2))
            self.assertEqual(result["state"], "failed")
            self.assertEqual(result["attempts"], 3)  # retries+1
            self.assertEqual(fetch.call_count, 3)

    def test_gate_timeout_is_retryable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            with mock.patch.object(
                html_queue.extract_arxiv_html,
                "fetch_html",
                side_effect=[GateTimeout("gate 'arxiv' queue wait exceeded 60s"), (True, "<html>x</html>")],
            ), mock.patch.object(html_queue.time, "sleep"):
                result = html_queue.download_one("2402.10329", _opts(tmp))
            self.assertEqual(result["state"], "downloaded")
            self.assertEqual(result["attempts"], 2)

    def test_non_retryable_http_error_fails_fast(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            boom = urllib.error.HTTPError(
                "https://arxiv.org/html/2402.10329", 403, "Forbidden", None, None
            )
            with mock.patch.object(
                html_queue.extract_arxiv_html, "fetch_html", side_effect=boom
            ) as fetch, mock.patch.object(html_queue.time, "sleep") as sleep:
                result = html_queue.download_one("2402.10329", _opts(tmp))
            self.assertEqual(result["state"], "failed")
            self.assertEqual(result["attempts"], 1)
            fetch.assert_called_once()
            sleep.assert_not_called()

    def test_sticky_unavailable_is_inherited_without_requesting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            with mock.patch.object(html_queue.extract_arxiv_html, "fetch_html") as fetch:
                result = html_queue.download_one(
                    "2402.10329", _opts(tmp), previous_state="unavailable", previous_status=404
                )
            self.assertEqual(result["state"], "unavailable")
            self.assertTrue(result.get("sticky"))
            fetch.assert_not_called()

    def test_force_re_requests_sticky_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            with mock.patch.object(
                html_queue.extract_arxiv_html, "fetch_html", return_value=(True, "<html>x</html>")
            ) as fetch:
                result = html_queue.download_one(
                    "2402.10329",
                    _opts(tmp, force=True),
                    previous_state="unavailable",
                    previous_status=404,
                )
            self.assertEqual(result["state"], "downloaded")
            fetch.assert_called_once()

    def test_tripped_circuit_short_circuits_without_fetching(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            circuit = html_queue._ChannelCircuit(limit=1)
            circuit.record(True)
            with mock.patch.object(html_queue.extract_arxiv_html, "fetch_html") as fetch:
                result = html_queue.download_one("2402.10329", _opts(tmp), circuit)
            self.assertEqual(result["state"], "channel-down")
            fetch.assert_not_called()


class RunDownloadQueueTest(unittest.TestCase):
    def test_manifest_shape_and_wire_states(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            (tmp / "ids.txt").write_text("a\nb\n", encoding="utf-8")
            summary_path = tmp / "html-download.json"

            def fake_fetch(url, target, timeout):
                if url.endswith("/a"):
                    target.write_text("<html>a</html>", encoding="utf-8")
                    return True, "<html>a</html>"
                return False, ""

            import contextlib, io
            buf = io.StringIO()
            with mock.patch.object(html_queue.extract_arxiv_html, "fetch_html", side_effect=fake_fetch), \
                 contextlib.redirect_stdout(buf):
                summary = html_queue.run_download_queue(_opts(tmp, summary_output=str(summary_path)))
            self.assertEqual(summary["paper_count"], 2)
            self.assertEqual(summary["states"], {"downloaded": 1, "unavailable": 1})
            self.assertEqual(len(summary["results"]), 2)
            self.assertTrue(summary_path.is_file())
            on_disk = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(on_disk["states"], summary["states"])
            text = buf.getvalue()
            self.assertIn("DOWNLOADED a (", text)
            self.assertIn("UNAVAILABLE b (", text)

    def test_rerun_inherits_sticky_unavailable_from_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "html").mkdir()
            (tmp / "ids.txt").write_text("a\n", encoding="utf-8")
            summary_path = tmp / "html-download.json"
            summary_path.write_text(json.dumps({"results": [
                {"paper_id": "a", "state": "unavailable", "status": 404},
            ]}), encoding="utf-8")
            with mock.patch.object(html_queue.extract_arxiv_html, "fetch_html") as fetch:
                summary = html_queue.run_download_queue(
                    _opts(tmp, summary_output=str(summary_path))
                )
            self.assertEqual(summary["states"], {"unavailable": 1})
            self.assertTrue(summary["results"][0].get("sticky"))
            fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()

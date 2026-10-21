"""Machine-wide rate-limit gate (embodied_learning/ratelimit.py).

Network is never touched: urlopen is mocked, and the shared state directory is
redirected to a tmp dir via EMBODIED_RATELIMIT_DIR so tests never read or write
the user's real throttle state.
"""

import email.message
import importlib.util
import json
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

_SCRIPT = Path(__file__).resolve().parent.parent / "embodied_learning" / "ratelimit.py"
ratelimit = importlib.import_module("embodied_learning.ratelimit")


def temp_state_dir():
    import tempfile

    return tempfile.TemporaryDirectory()


class GroupForUrlTest(unittest.TestCase):
    def test_arxiv_family_maps_to_one_group(self) -> None:
        for url in (
            "https://export.arxiv.org/api/query?id_list=1",
            "https://arxiv.org/html/2402.10329",
            "https://arxiv.org/pdf/2402.10329",
        ):
            self.assertEqual(ratelimit.group_for_url(url), "arxiv")

    def test_semanticscholar_and_arxiv2md(self) -> None:
        self.assertEqual(ratelimit.group_for_url("https://api.semanticscholar.org/graph/v1/paper/search"), "semanticscholar")
        self.assertEqual(ratelimit.group_for_url("https://arxiv2md.org/api/markdown?url=1"), "arxiv2md")

    def test_unknown_host_is_its_own_group(self) -> None:
        self.assertEqual(ratelimit.group_for_url("https://example.com/x"), "example.com")


class ResolveIntervalTest(unittest.TestCase):
    def test_explicit_argument_wins(self) -> None:
        with mock.patch.dict("os.environ", {"EMBODIED_RATELIMIT_ARXIV_INTERVAL": "9"}, clear=False):
            self.assertEqual(ratelimit.resolve_interval("arxiv", 0.5), 0.5)

    def test_env_override(self) -> None:
        with mock.patch.dict("os.environ", {"EMBODIED_RATELIMIT_ARXIV_INTERVAL": "9"}, clear=False):
            self.assertEqual(ratelimit.resolve_interval("arxiv"), 9.0)

    def test_builtin_default(self) -> None:
        env = {k: v for k, v in __import__("os").environ.items() if not k.startswith("EMBODIED_RATELIMIT_")}
        with mock.patch.dict("os.environ", env, clear=True):
            self.assertEqual(ratelimit.resolve_interval("arxiv"), 3.0)


class GateTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = temp_state_dir()
        self.addCleanup(tmp.cleanup)
        self._dir_patch = mock.patch.dict("os.environ", {"EMBODIED_RATELIMIT_DIR": tmp.name}, clear=False)
        self._dir_patch.start()
        self.addCleanup(self._dir_patch.stop)

    def test_gate_advances_next_ok_ts(self) -> None:
        with ratelimit.gate("arxiv", min_interval=0.05):
            pass
        state = json.loads((Path(ratelimit.state_dir()) / "arxiv.json").read_text())
        self.assertGreater(state["next_ok_ts"], time.time() - 1)

    def test_second_gate_waits_one_interval(self) -> None:
        with ratelimit.gate("arxiv", min_interval=0.15):
            pass
        started = time.time()
        with ratelimit.gate("arxiv", min_interval=0.15):
            pass
        self.assertGreaterEqual(time.time() - started, 0.1)

    def test_report_rejection_extends_cooldown(self) -> None:
        cooldown = ratelimit.report_rejection("arxiv", 0.3)
        self.assertGreaterEqual(cooldown, 0.29)
        started = time.time()
        with ratelimit.gate("arxiv", min_interval=0.01):
            pass
        self.assertGreaterEqual(time.time() - started, 0.25)
        state = json.loads((Path(ratelimit.state_dir()) / "arxiv.json").read_text())
        self.assertNotIn("cooldown_until", state)  # consumed and cleared

    def test_report_rejection_default_when_no_header(self) -> None:
        cooldown = ratelimit.report_rejection("semanticscholar", None)
        self.assertGreater(cooldown, 0)

    def test_max_wait_times_out(self) -> None:
        ratelimit.report_rejection("arxiv", 5.0)
        with self.assertRaises(ratelimit.GateTimeout):
            with ratelimit.gate("arxiv", max_wait=0.2):
                pass

    def test_two_threads_are_serialized(self) -> None:
        stamps: list[float] = []
        lock = threading.Lock()

        def worker() -> None:
            with ratelimit.gate("arxiv", min_interval=0.1):
                with lock:
                    stamps.append(time.time())

        threads = [threading.Thread(target=worker) for _ in range(3)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(stamps), 3)
        gaps = [b - a for a, b in zip(sorted(stamps), sorted(stamps)[1:])]
        for gap in gaps:
            self.assertGreaterEqual(gap, 0.08, "gate failed to serialize concurrent slots")

    def test_lock_is_released_before_the_reserved_slot_is_slept_off(self) -> None:
        """A slow dispatch must not block the next worker's reservation.

        Holding the flock across the spacing sleep and the caller's whole
        body made the extraction queue's four fetch workers effectively
        single-threaded (2026-10-20: 40 min for 109 papers)."""
        started = time.time()

        def worker() -> None:
            with ratelimit.gate("arxiv", min_interval=0.2):
                time.sleep(0.5)  # stand-in for connect + TLS + body read

        threads = [threading.Thread(target=worker) for _ in range(3)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        # Serialized: 3 x (0.2 + 0.5) = 2.1s. Overlapping: ~0.4 + 0.5 = 0.9s.
        self.assertLess(time.time() - started, 1.5)

    def test_cooldown_recorded_while_sleeping_aborts_instead_of_dispatching(self) -> None:
        """A 429 landing while a worker waits out its own reserved slot must
        make the worker fail fast (GateTimeout) rather than dispatch inside
        the machine-wide cooldown."""
        # Burn the first slot so the measured gate has a real spacing sleep.
        with ratelimit.gate("arxiv", min_interval=0.6):
            pass
        # Reserve our slot, then a sibling records a 5s cooldown mid-sleep.
        recorder = threading.Timer(0.1, ratelimit.report_rejection, args=("arxiv", 5.0))
        recorder.start()
        started = time.time()
        with self.assertRaises(ratelimit.GateTimeout):
            with ratelimit.gate("arxiv", min_interval=0.1, max_wait=1.0):
                pass
        recorder.join()
        self.assertLess(time.time() - started, 2.0)


class GatedUrlopenTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = temp_state_dir()
        self.addCleanup(tmp.cleanup)
        self._dir_patch = mock.patch.dict("os.environ", {"EMBODIED_RATELIMIT_DIR": tmp.name}, clear=False)
        self._dir_patch.start()
        self.addCleanup(self._dir_patch.stop)

    @staticmethod
    def _http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
        headers = email.message.Message()
        if retry_after is not None:
            headers["Retry-After"] = retry_after
        return urllib.error.HTTPError("https://export.arxiv.org/api/query", code, "slow down", headers, None)

    def test_success_passes_response_through(self) -> None:
        request = urllib.request.Request("https://export.arxiv.org/api/query")
        response = object()
        with mock.patch.object(urllib.request, "urlopen", return_value=response) as fake:
            result = ratelimit.gated_urlopen(request, timeout=1.0)
        self.assertIs(result, response)
        fake.assert_called_once()

    def test_transient_error_records_cooldown_and_reraises(self) -> None:
        request = urllib.request.Request("https://api.semanticscholar.org/graph/v1/paper/search?query=x")
        error = self._http_error(429, retry_after="7")
        with mock.patch.object(urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(urllib.error.HTTPError):
                ratelimit.gated_urlopen(request, timeout=1.0)
        state = json.loads((Path(ratelimit.state_dir()) / "semanticscholar.json").read_text())
        self.assertGreater(state["cooldown_until"], time.time() + 6)

    def test_non_transient_error_does_not_touch_cooldown(self) -> None:
        request = urllib.request.Request("https://export.arxiv.org/api/query")
        with mock.patch.object(urllib.request, "urlopen", side_effect=self._http_error(404)):
            with self.assertRaises(urllib.error.HTTPError):
                ratelimit.gated_urlopen(request, timeout=1.0)
        state_path = Path(ratelimit.state_dir()) / "arxiv.json"
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        self.assertNotIn("cooldown_until", state)

    def test_group_derived_from_url_when_omitted(self) -> None:
        request = urllib.request.Request("https://arxiv.org/html/2402.10329v1")
        with mock.patch.object(urllib.request, "urlopen", side_effect=self._http_error(503)):
            with self.assertRaises(urllib.error.HTTPError):
                ratelimit.gated_urlopen(request, timeout=1.0)
        self.assertTrue((Path(ratelimit.state_dir()) / "arxiv.json").exists())


if __name__ == "__main__":
    unittest.main()

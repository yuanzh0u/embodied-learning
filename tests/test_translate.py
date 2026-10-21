"""MyMemory translation bootstrap (embodied_learning/utils/translate.py).

Network is never touched: the ratelimit-gated urlopen seam is mocked, so the
assertions are about the request shape and the failure contract (always None,
never an exception).
"""

from __future__ import annotations

import contextlib
import json
import unittest
import urllib.error
import urllib.parse
from unittest import mock

from embodied_learning.config import TRANSLATE_MAX_CHARS
from embodied_learning.utils import translate as translate_mod


def gated_for(payload=None, error=None):
    """Fake ``ratelimit.gated_urlopen``: record the request, yield ``payload``
    (or raise ``error``)."""

    captured: list = []

    @contextlib.contextmanager
    def _fake(request, **kwargs):
        captured.append((request, kwargs))
        if error is not None:
            raise error
        body = json.dumps(payload).encode("utf-8")
        yield mock.Mock(read=lambda: body)

    _fake.captured = captured
    return _fake


class TranslateTest(unittest.TestCase):
    def call(self, text, fake):
        with mock.patch.object(translate_mod.ratelimit, "gated_urlopen", fake):
            return translate_mod.translate(text)

    def test_success_translates_and_sends_langpair(self):
        fake = gated_for({
            "responseData": {"translatedText": "Reinforcement learning"},
            "responseStatus": 200,
        })
        self.assertEqual(self.call("强化学习", fake), "Reinforcement learning")
        request, kwargs = fake.captured[0]
        self.assertEqual(kwargs["group"], "mymemory")
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(request.full_url).query)
        self.assertEqual(query["q"], ["强化学习"])
        self.assertEqual(query["langpair"], ["zh-CN|en"])

    def test_empty_input_short_circuits_without_network(self):
        fake = gated_for({"responseData": {"translatedText": "x"}, "responseStatus": 200})
        self.assertIsNone(self.call("   ", fake))
        self.assertIsNone(self.call("", fake))
        self.assertEqual(fake.captured, [])

    def test_long_input_truncated_to_max_chars(self):
        fake = gated_for({"responseData": {"translatedText": "x"}, "responseStatus": 200})
        self.call("点" * (TRANSLATE_MAX_CHARS + 50), fake)
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(fake.captured[0][0].full_url).query)
        self.assertEqual(len(query["q"][0]), TRANSLATE_MAX_CHARS)

    def test_quota_and_limit_markers_are_failures(self):
        for text in (
            "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY",
            "QUERY LENGTH LIMIT EXCEEDED",
        ):
            fake = gated_for({"responseData": {"translatedText": text}, "responseStatus": 200})
            self.assertIsNone(self.call("强化学习", fake), msg=text)

    def test_quota_finished_flag_and_bad_status_are_failures(self):
        fake = gated_for({
            "responseData": {"translatedText": "x"}, "responseStatus": 200, "quotaFinished": True,
        })
        self.assertIsNone(self.call("强化学习", fake))
        fake = gated_for({"responseData": {"translatedText": "x"}, "responseStatus": 403})
        self.assertIsNone(self.call("强化学习", fake))

    def test_network_and_gate_failures_are_none(self):
        for error in (
            urllib.error.URLError("down"),
            translate_mod.ratelimit.GateTimeout("busy"),
            ValueError("bad json"),  # also covers json.JSONDecodeError
        ):
            fake = gated_for(error=error)
            self.assertIsNone(self.call("强化学习", fake), msg=str(error))

    def test_malformed_payload_is_none(self):
        for payload in (
            {"responseData": None, "responseStatus": 200},
            {"responseData": {"translatedText": ""}, "responseStatus": 200},
            {"responseData": {"translatedText": 42}, "responseStatus": 200},
            "not-a-dict",
        ):
            fake = gated_for(payload)
            self.assertIsNone(self.call("强化学习", fake), msg=repr(payload))


if __name__ == "__main__":
    unittest.main()

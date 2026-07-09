#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "promote_candidates.py"
SPEC = importlib.util.spec_from_file_location("promote_candidates", SCRIPT)
promote_candidates = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(promote_candidates)


API_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2606.03784v2</id>
    <title>Revisiting Embodied Chain-of-Thought</title>
    <published>2026-06-03T00:00:00Z</published>
    <author><name>Jane Doe</name></author>
    <author><name>李四</name></author>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2607.00673v1</id>
    <title>Path Planning in Physically Viable World Models</title>
    <published>2026-07-01T00:00:00Z</published>
    <author><name>John Roe</name></author>
  </entry>
</feed>
"""

LATEXML_HTML = """
<html><body>
<section class="ltx_section" id="S3">
<h2 class="ltx_title ltx_title_section">3 Method</h2>
<div id="S3.p1" class="ltx_para"><p class="ltx_p">Reasoning must ground into executable action guidance.
Chain-of-thought as action prefix causes compounding errors in planning, as shown by prior work <cite class="ltx_cite ltx_citemacro_cite">[<a class="ltx_ref" href="#bib.bib1">1</a>]</cite>.</p></div>
</section>
<section class="ltx_bibliography" id="bib">
<h2 class="ltx_title ltx_title_bibliography">References</h2>
<ul class="ltx_biblist">
<li class="ltx_bibitem" id="bib.bib1"><span class="ltx_bibblock">Prior work. arXiv:2301.00001.</span></li>
</ul>
</section>
</body></html>
"""


class DummyResponse(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):  # type: ignore[no-untyped-def]
        return False


def fake_urlopen(request, timeout=0):  # type: ignore[no-untyped-def]
    url = request.full_url if isinstance(request, urllib.request.Request) else request
    if "export.arxiv.org/api" in url:
        return DummyResponse(API_FEED.encode("utf-8"))
    return DummyResponse(LATEXML_HTML.encode("utf-8"))


class PromoteCandidatesTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_main(self) -> tuple[list[dict], str]:
        skeleton = self.tmp / "skeleton.jsonl"
        digest = self.tmp / "digest.md"
        argv = [
            "promote_candidates.py",
            "--paper-id", "2606.03784",
            "--paper-id", "2607.00673",
            "--topic", "感知误差与认知误差",
            "--topic-id", "EA-MODEL",
            "--id-prefix", "EA-PVC-2026",
            "--start-seq", "3",
            "--terms", "reasoning,planning",
            "--cache-dir", str(self.tmp / "cache"),
            "--output-skeleton", str(skeleton),
            "--output-digest", str(digest),
        ]
        with mock.patch.object(promote_candidates.urllib.request, "urlopen", side_effect=fake_urlopen):
            with mock.patch.object(
                promote_candidates.extract_arxiv_html.urllib.request, "urlopen", side_effect=fake_urlopen
            ):
                with mock.patch.object(promote_candidates.time, "sleep"):
                    with mock.patch.object(promote_candidates.sys, "argv", argv):
                        code = promote_candidates.main()
        self.assertEqual(0, code)
        events = [json.loads(line) for line in skeleton.read_text(encoding="utf-8").splitlines() if line]
        return events, digest.read_text(encoding="utf-8")

    def test_skeleton_prefills_mechanical_fields_and_leaves_todos(self) -> None:
        events, _ = self.run_main()
        self.assertEqual(2, len(events))
        first, second = events
        self.assertEqual("EA-PVC-2026-0003", first["event_id"])
        self.assertEqual("EA-PVC-2026-0004", second["event_id"])
        self.assertEqual("2606.03784", first["paper"]["arxiv_id"])
        self.assertEqual("Revisiting Embodied Chain-of-Thought", first["paper"]["title"])
        self.assertEqual("2026-06-03", first["paper"]["published"])
        self.assertEqual("https://arxiv.org/abs/2606.03784", first["paper"]["url"])
        self.assertEqual(
            [{"name": "Jane Doe", "author_key": "jane-doe", "role": "paper-author", "institutions": []},
             {"name": "李四", "author_key": "unknown-author", "role": "paper-author", "institutions": []}],
            first["authors"],
        )
        # Intellectual fields stay TODO so the validator refuses an unfilled skeleton.
        self.assertTrue(first["claim"].startswith("TODO("))
        self.assertTrue(first["stance"].startswith("TODO("))
        self.assertTrue(first["evidence"]["summary"].startswith("TODO("))
        # Locator prefilled from the top ranked section.
        self.assertEqual("3 Method", first["evidence"]["locator"])

    def test_validator_rejects_unfilled_skeleton(self) -> None:
        events, _ = self.run_main()
        write_spec = importlib.util.spec_from_file_location(
            "write_lit_outputs", ROOT / "scripts" / "write_lit_outputs.py"
        )
        write_lit_outputs = importlib.util.module_from_spec(write_spec)
        assert write_spec and write_spec.loader
        write_spec.loader.exec_module(write_lit_outputs)
        self.assertNotIn(events[0]["stance"], write_lit_outputs.STANCES)

    def test_digest_contains_ranked_sections_and_citations(self) -> None:
        _, digest = self.run_main()
        self.assertIn("## Revisiting Embodied Chain-of-Thought (EA-PVC-2026-0003)", digest)
        self.assertIn("§3 Method", digest)
        self.assertIn("compounding errors", digest)
        self.assertIn("Citation contexts", digest)
        self.assertIn("2301.00001", digest)


if __name__ == "__main__":
    unittest.main()

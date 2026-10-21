"""MyMemory REST translation — bootstrap English queries for pure-Chinese topics.

arXiv is an English corpus: a pure-Chinese topic (e.g. 强化学习) carries no
Latin token the mechanical planner can conjunct, so keyword retrieval has
nothing to run whenever the dynamic-query agent also fails (2026-10-15, plan
fell to 0 queries). One free MyMemory call turns the topic into English
("reinforcement learning") whose Latin tokens feed the same mechanical path an
English topic gets — the conjunctive ``latin-combined`` plan query, screening
terms, and the recall scope clause.

Failure is always ``None``, never an exception: translation is a bootstrap
enrichment, so callers keep their existing fallback when it is unavailable
(network down, quota exhausted, non-200). Requests go through the
machine-wide ratelimit gate like every other outbound call.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request

from embodied_learning import ratelimit
from embodied_learning.config import TRANSLATE_MAX_CHARS, TRANSLATE_TIMEOUT_S

MYMEMORY_ENDPOINT = "https://api.mymemory.translated.net/get"
# MyMemory reports quota/limit problems in-band, with responseStatus 200.
_QUOTA_MARKERS = ("MYMEMORY WARNING", "QUOTA EXCEEDED", "QUERY LENGTH LIMIT")


def translate(
    text: str,
    *,
    source: str = "zh-CN",
    target: str = "en",
    timeout_s: float | None = None,
) -> str | None:
    """Translate ``text`` with the MyMemory REST API; ``None`` on any failure.

    Anonymous MyMemory caps ``q`` at 500 bytes, so the input is truncated to
    ``TRANSLATE_MAX_CHARS`` first — topic phrases are far shorter, the cap is
    a guard, not a feature.
    """

    raw = re.sub(r"\s+", " ", str(text or "")).strip()
    if not raw:
        return None
    query = urllib.parse.urlencode({"q": raw[:TRANSLATE_MAX_CHARS], "langpair": f"{source}|{target}"})
    request = urllib.request.Request(
        f"{MYMEMORY_ENDPOINT}?{query}",
        headers={"User-Agent": "embodied-learning/1.0 (research KB; translate bootstrap)"},
    )
    try:
        with ratelimit.gated_urlopen(
            request, group="mymemory", timeout=timeout_s or TRANSLATE_TIMEOUT_S
        ) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
    except (
        urllib.error.URLError,
        OSError,
        TimeoutError,
        ValueError,
        ratelimit.GateTimeout,
    ):
        return None

    if not isinstance(payload, dict):
        return None
    try:
        status = int(payload.get("responseStatus") or 0)
    except (TypeError, ValueError):
        return None
    if status != 200 or payload.get("quotaFinished"):
        return None
    data = payload.get("responseData")
    translated = data.get("translatedText") if isinstance(data, dict) else None
    if not isinstance(translated, str):
        return None
    translated = translated.strip()
    if not translated:
        return None
    if any(marker in translated.upper() for marker in _QUOTA_MARKERS):
        return None
    return translated

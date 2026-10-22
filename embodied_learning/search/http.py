"""Shared HTTP retry policy for the search layer.

One implementation of the transient-error retry helpers that used to be
copy-pasted across arxiv.py / semantic_scholar.py / citation_expansion.py /
influence.py / problem_relevance.py ("copied from search_arxiv.py").
Request pacing still goes through ``embodied_learning.ratelimit.gated_urlopen``;
this module only decides whether and how long to wait between attempts.
"""

from __future__ import annotations

import urllib.error
from embodied_learning.config import MAX_RETRIES, TRANSIENT_HTTP_CODES



def bounded_retries(value: int) -> int:
    return max(0, min(value, MAX_RETRIES))


def retry_after_seconds(exc: Exception) -> float | None:
    if not isinstance(exc, urllib.error.HTTPError):
        return None
    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    if not retry_after:
        return None
    try:
        parsed = float(retry_after)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in TRANSIENT_HTTP_CODES
    return isinstance(exc, (TimeoutError, urllib.error.URLError, OSError))


def retry_wait_seconds(exc: Exception, attempt: int, retry_base_seconds: float, retry_max_seconds: float) -> float:
    retry_after = retry_after_seconds(exc)
    if retry_after is not None:
        return max(0.0, min(retry_after, retry_max_seconds))
    return max(0.0, min(retry_base_seconds * (2**attempt), retry_max_seconds))

"""Canonical arXiv ID normalization.

One implementation of the ``normalize_arxiv_id`` helpers that were copy-pasted
across the search modules and the single-paper scripts.

Two behaviors behind one name:

- ``normalize_arxiv_id(value)`` — tolerant clean for registry/dedup keys:
  take the last URL path segment, drop ``.pdf``/``.html``, drop ``vN``.
- ``normalize_arxiv_id(value, strict=True)`` — CLI-facing validation: the full
  arXiv ID grammar (via ``knowledge.arxiv_reader.parse_arxiv_id``), raising
  ``ValueError`` with the offending value instead of returning None.
"""

from __future__ import annotations

import re


def normalize_arxiv_id(value: object, *, strict: bool = False) -> str:
    if strict:
        from embodied_learning.knowledge.arxiv_reader import parse_arxiv_id

        raw = re.sub(r"^arxiv:", "", str(value or "").strip(), flags=re.IGNORECASE)
        normalized = parse_arxiv_id(raw)
        if normalized is None:
            raise ValueError(f"无效的 arXiv ID：{value!r}")
        return normalized
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())

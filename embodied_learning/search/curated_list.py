"""Harvest paper candidates from a curated list repository (e.g. an awesome-list).

A curated list (GitHub awesome-list, bibliography file, ...) is a *human-selected*
candidate channel. Every entry is a candidate only — never evidence — and the
discovery channel is recorded truthfully as ``curated-list`` in the candidate
registry (distinct from ``browser`` fallback, which is unplanned web noise).
Downstream deep-read verification decides what becomes evidence, exactly as the
evidence discipline requires for browser results.

Repository scanning is whole-repo, not README-only: the GitHub git-trees API
lists every blob, and all text files (Markdown/TXT/BibTeX below a size cap) are
downloaded and mined, so papers living in CONTRIBUTING.md, docs/*.md, or .bib
files are found too.

Extraction is line-block based and format-agnostic to the specific list:
bullet blocks (``- **Title** (Year) — ...`` plus indented/badge continuation
lines) and Markdown table rows both yield candidates. arXiv IDs are taken from
``arxiv.org/abs|pdf/<id>`` links (modern ``NNNN.NNNNN`` and legacy
``cs/0303012`` forms). Blocks with outbound links but no arXiv link are
reported as ``unresolved`` (with title + first link) so a Semantic Scholar
title lookup (``resolve_unresolved``) can attach arXiv IDs best-effort.

Output JSON intentionally matches the browser-candidates shape
(``{"candidates": [{arxiv_id, title, context, ...}]}``) so
``build-candidate-registry --curated-list-result`` can ingest it directly.
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

GITHUB_API = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
USER_AGENT = "embodied-ai-literature-hub/1.0 (local research workflow)"

TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".bib"}
MAX_FILE_BYTES = 2_000_000

# arxiv.org/abs/2608.15659, .../pdf/2608.15659v2, legacy .../abs/cs.CV/0303012
ARXIV_LINK_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/([a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})(v\d+)?",
    re.IGNORECASE,
)
YEAR_RE = re.compile(r"\((20\d{2})\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
BADGE_RE = re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)")  # [![txt](img)](url)
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
EXTERNAL_LINK_RE = re.compile(r"https?://[^\s\])>\"']+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def normalize_arxiv_id(value: str) -> str:
    """Strip version suffix and scheme noise: ``2608.15659v2`` -> ``2608.15659``."""
    return re.sub(r"v\d+$", "", value.strip().rstrip("/").rstrip("."))


# ---- repository scanning -----------------------------------------------------


def _http_get(url: str, timeout: float) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def list_repo_text_files(repo: str, ref: str, timeout: float) -> list[str]:
    """Every text-suffixed blob path in the repo (whole-tree scan, not README-only)."""
    url = f"{GITHUB_API}/repos/{repo}/git/trees/{ref}?recursive=1"
    payload = json.loads(_http_get(url, timeout).decode("utf-8"))
    paths = []
    for item in payload.get("tree") or []:
        if item.get("type") != "blob":
            continue
        path = str(item.get("path") or "")
        if Path(path).suffix.lower() in TEXT_SUFFIXES and int(item.get("size") or 0) <= MAX_FILE_BYTES:
            paths.append(path)
    return sorted(paths)


def fetch_repo_files(repo: str, ref: str, timeout: float) -> list[tuple[str, str]]:
    """(path, text) for every text file in the repo; unreadable files are skipped."""
    files: list[tuple[str, str]] = []
    for path in list_repo_text_files(repo, ref, timeout):
        url = f"{RAW_BASE}/{repo}/{ref}/{urllib.parse.quote(path)}"
        try:
            files.append((path, _http_get(url, timeout).decode("utf-8")))
        except (OSError, UnicodeDecodeError):
            continue  # a broken/unreadable file must not sink the harvest
    return files


# ---- extraction --------------------------------------------------------------


def _clean_context(line: str) -> str:
    """Badge images and link URLs out, plain text in — the context is for humans."""
    line = BADGE_RE.sub(" ", line)
    line = MD_LINK_RE.sub(lambda m: m.group(1) or m.group(2), line)
    return " ".join(line.split())


def _iter_blocks(text: str):
    """Yield (kind, heading_stack, block_lines) for bullet blocks and table rows.

    A bullet block is the bullet line plus subsequent continuation lines
    (badge links often live on the next line); a table row is a single ``|`` line.
    """
    heading_stack: list[str] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            heading_stack = heading_stack[: level - 1] + [heading.group(2)]
            index += 1
            continue
        if line.startswith("|"):
            yield ("table-row", list(heading_stack), [line])
            index += 1
            continue
        if re.match(r"\s*[-*]\s+\S", line):
            block = [line]
            index += 1
            while index < len(lines):
                follow = lines[index]
                if (
                    not follow.strip()
                    or re.match(r"\s*[-*]\s+\S", follow)
                    or follow.startswith("|")
                    or follow.startswith("#")
                ):
                    break
                block.append(follow)
                index += 1
            yield ("bullet", list(heading_stack), block)
            continue
        index += 1


def _block_title(block: list[str], kind: str) -> str:
    """First bold run wins (list style); fall back to the table's first cell."""
    for line in block:
        match = BOLD_RE.search(line)
        if match:
            return " ".join(match.group(1).split())
    if kind == "table-row":
        cell = block[0].strip().strip("|").split("|")[0]
        return " ".join(cell.replace("**", "").split())
    return ""


def extract_candidates(text: str, source: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Mine one file: returns (candidates with arXiv IDs, unresolved blocks).

    Deduplication is by arXiv ID across the whole file; the first occurrence
    wins but a bullet block outranks a table-row mention (richer context).
    """
    candidates: dict[str, dict[str, Any]] = {}
    unresolved: list[dict[str, Any]] = []
    for kind, headings, block in _iter_blocks(text):
        ids = [normalize_arxiv_id(match.group(1)) for match in ARXIV_LINK_RE.finditer("\n".join(block))]
        section = " > ".join(headings)
        context = _clean_context(block[0])
        title = _block_title(block, kind)
        year_match = YEAR_RE.search(" ".join(block))
        if ids:
            bullet_rank = 1 if kind == "bullet" else 0
            for arxiv_id in dict.fromkeys(ids):  # keep order, dedupe
                existing = candidates.get(arxiv_id)
                if existing is None:
                    record = {
                        "arxiv_id": arxiv_id,
                        "title": title,
                        "context": context,
                        "section": section,
                        "source": source,
                        "block_kind": kind,
                    }
                    if year_match:
                        record["year"] = int(year_match.group(1))
                    candidates[arxiv_id] = record
                elif bullet_rank > (1 if existing.get("block_kind") == "bullet" else 0):
                    # a bullet block appeared after a table row mentioned the same ID
                    existing.update({"title": title, "context": context, "section": section, "block_kind": kind})
                    if year_match and "year" not in existing:
                        existing["year"] = int(year_match.group(1))
        elif kind == "bullet":
            links = [m.group(0) for m in EXTERNAL_LINK_RE.finditer(" ".join(block))]
            links = [link for link in links if "shields.io" not in link and "img.shields" not in link]
            if title and links:
                unresolved.append({
                    "title": title,
                    "context": context,
                    "section": section,
                    "link": links[0],
                    "source": source,
                })
    return list(candidates.values()), unresolved


# ---- unresolved-title resolution (best-effort, Semantic Scholar) --------------


def _normalize_title(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


DOMAIN_TOKENS_RE = re.compile(
    r"\b(ego\w*|first[- ]?person|pov|wearable|hand\w*|gaze|gesture|kitchen|hoi|"
    r"activity|action|manipulation|video|human)\b"
)
SUBMISSION_TITLE_RE = re.compile(r"\b(submission|solution|technical report|place)\b")


def _title_match_score(listed_norm: str, stored_norm: str) -> float:
    """Weighted match score between a listed (nickname) title and a stored title.

    Dataset nicknames ("Assembly101") and subtitle drift make whole-string
    ratio useless; containment of the listed title's tokens in the stored
    title is the real signal. Prefix matches get a bonus. Very short listed
    titles (<=2 tokens) are only trusted with a prefix match — bare "ADL"
    must not resolve onto a different ADL dataset.
    """
    tokens = [token for token in re.findall(r"[a-z0-9]+", listed_norm) if len(token) >= 2]
    if not tokens:
        return 0.0
    contained = sum(1 for token in tokens if token in stored_norm)
    fraction = contained / len(tokens)
    prefix = 0.5 if stored_norm.startswith(listed_norm) or listed_norm.startswith(stored_norm) else 0.0
    if len(tokens) <= 2 and not prefix:
        return 0.0
    if not prefix:
        # A prefix-less containment match onto a paper that never calls
        # itself a dataset/benchmark is usually a methods paper that merely
        # uses the named dataset ("... for EPIC-KITCHENS-100 ...").
        if not re.search(r"\b(datasets?|benchmarks?|corpus|corpora)\b", stored_norm):
            return 0.0
    return fraction + prefix


def resolve_via_snapshot(
    unresolved: list[dict[str, Any]],
    db_path: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Offline title resolution against the local snapshot SQLite/FTS5 database.

    Preferred over the S2 title lookup: instant, no rate limits, and covers
    everything up to the snapshot cutoff. A fuzzy ratio gate (>=0.75) keeps
    wrong-title matches out.
    """
    import sqlite3

    connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        resolved: list[dict[str, Any]] = []
        still: list[dict[str, Any]] = []
        for entry in unresolved:
            phrase = " ".join(re.findall(r"[a-z0-9]+", entry["title"].lower()))
            if not phrase:
                still.append({**entry, "reason": "snapshot-resolve-failed: no latin tokens in title"})
                continue
            # Listed titles drift from stored titles (nicknames like
            # "EPIC-KITCHENS-100" are not in the paper title), so the token
            # AND-count is progressively relaxed (8 -> 5 -> 3 -> 2) and every
            # candidate is gated by fuzzy ratio against the listed title.
            tokens = [token for token in phrase.split() if len(token) >= 3]
            rows: list[tuple[str, str]] = []
            try:
                for count in (8, 5, 3, 2, 1):
                    if count > len(tokens):
                        continue  # relax further: short titles have few tokens
                    # FTS5 column filters bind to a single term, so every
                    # token needs its own `title :` prefix.
                    query = " AND ".join(f"title : {token}" for token in tokens[:count])
                    rows = connection.execute(
                        'SELECT p.id, p.title FROM fts f JOIN papers p ON p.rowid = f.rowid'
                        ' WHERE fts MATCH ? ORDER BY rank LIMIT 5',
                        [query],
                    ).fetchall()
                    if rows:
                        break
            except sqlite3.OperationalError as exc:
                still.append({**entry, "reason": f"snapshot-resolve-failed: {exc}"})
                continue
            match = None
            best_score = 0.0
            for row in rows:
                stored_norm = _normalize_title(row[1])
                # Hard guards: challenge submissions share every dataset
                # keyword but are not the dataset paper; off-domain hits
                # (physics "Homage", chemistry "H2O") share only a nickname.
                if SUBMISSION_TITLE_RE.search(stored_norm) or not DOMAIN_TOKENS_RE.search(stored_norm):
                    continue
                score = _title_match_score(phrase, stored_norm)
                if score >= 0.6 and score > best_score:
                    match, best_score = row, score
            if match is None:
                still.append({**entry, "reason": "snapshot-resolve-failed: no confident title match"})
                continue
            resolved.append({
                "arxiv_id": match[0],
                "title": match[1],
                "context": entry["context"],
                "section": entry["section"],
                "source": entry["source"],
                "block_kind": "snapshot-title-resolved",
                "listed_title": entry["title"],
            })
        return resolved, still
    finally:
        connection.close()


def resolve_unresolved(
    unresolved: list[dict[str, Any]],
    *,
    sleep_seconds: float = 1.0,
    timeout: float = 30.0,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Try to attach an arXiv ID to unresolved entries via S2 title search.

    Best-effort: failures keep the entry in the returned unresolved list with
    ``reason`` filled in — they never block or abort a harvest. Requests go
    through the S2 backend's retry/backoff machinery (429s are common).
    """
    from embodied_learning.search.semantic_scholar import build_search_url, normalize_arxiv_id as s2_normalize

    def _s2_get(url: str, request_timeout: float) -> bytes:
        from embodied_learning.search.semantic_scholar import (
            MAX_RETRIES,
            bounded_retries,
            is_retryable,
            retry_wait_seconds,
        )

        last_error: Exception | None = None
        for attempt in range(bounded_retries(MAX_RETRIES) + 1):
            try:
                return _http_get(url, request_timeout)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if attempt < MAX_RETRIES and is_retryable(exc):
                    time.sleep(retry_wait_seconds(exc, attempt, retry_base_seconds=2.0, retry_max_seconds=60.0))
                    continue
                break
        raise last_error if last_error else RuntimeError("S2 title lookup failed")

    still: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    for index, entry in enumerate(unresolved):
        if index and sleep_seconds:
            time.sleep(sleep_seconds)
        url = build_search_url(entry["title"], offset=0, limit=1)
        try:
            payload = json.loads(_s2_get(url, timeout).decode("utf-8"))
            papers = payload.get("data") or []
            match = papers[0] if papers else None
            arxiv_id = s2_normalize((match or {}).get("externalIds", {}).get("ArXiv"))
            if not (match and arxiv_id):
                raise ValueError("no arXiv external id in S2 result")
        except Exception as exc:  # noqa: BLE001 — any single lookup may fail
            still.append({**entry, "reason": f"s2-resolve-failed: {exc}"})
            continue
        title = str(match.get("title") or entry["title"])
        resolved.append({
            "arxiv_id": arxiv_id,
            "title": title,
            "context": entry["context"],
            "section": entry["section"],
            "source": entry["source"],
            "block_kind": "s2-title-resolved",
            "matched_title": title,
            "listed_title": entry["title"],
        })
    return resolved, still


# ---- orchestration ------------------------------------------------------------


def harvest(
    repo: str,
    *,
    ref: str = "main",
    resolve_missing: bool = True,
    resolve_db: str | None = None,
    sleep_seconds: float = 1.0,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Whole-repo scan -> browser-shaped candidates JSON (channel: curated-list)."""
    files = fetch_repo_files(repo, ref, timeout)
    candidates: dict[str, dict[str, Any]] = {}
    unresolved: list[dict[str, Any]] = []
    scanned: list[str] = []
    for path, text in files:
        scanned.append(path)
        file_candidates, file_unresolved = extract_candidates(text, source=path)
        for record in file_candidates:
            existing = candidates.get(record["arxiv_id"])
            if existing is None:
                candidates[record["arxiv_id"]] = record
            elif record["section"] and record["section"] not in existing.get("sections", []):
                existing.setdefault("sections", [existing.get("section", "")])
                existing["sections"].append(record["section"])
        unresolved.extend(file_unresolved)
    if resolve_missing and unresolved:
        if resolve_db:
            # Offline first (instant, no rate limits); S2 only for the rest.
            resolved, unresolved = resolve_via_snapshot(unresolved, resolve_db)
            for record in resolved:
                candidates.setdefault(record["arxiv_id"], record)
        if unresolved:
            resolved, unresolved = resolve_unresolved(unresolved, sleep_seconds=sleep_seconds, timeout=timeout)
            for record in resolved:
                candidates.setdefault(record["arxiv_id"], record)
    return {
        "batch": f"curated-list:{repo}",
        "source_label": f"curated-list:{repo}",
        "source_url": f"https://github.com/{repo}/tree/{ref}",
        "channel_hint": "curated-list",
        "ref": ref,
        "files_scanned": scanned,
        "candidates": sorted(candidates.values(), key=lambda item: item["arxiv_id"]),
        "unresolved": unresolved,
    }

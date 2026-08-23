#!/usr/bin/env python3
"""Rank papers by problem relevance to open research questions.

Given a review-in-progress (a set of open research questions it has not fully
answered, plus its existing papers as seeds), this script runs a **two-stage
budget funnel** so the expensive steps only ever touch a few papers:

1. **Fetch** -- multi-round citation expansion from the seeds (Semantic Scholar),
   recovering each surviving candidate's *judgment surface* (abstract +
   introduction + related-work sections) from arXiv HTML. No reading happens
   here; it only gathers a corpus.

2. **Retrieve** -- a sparse lexical retriever (BM25) that treats the questions
   as the query and each candidate's judgment surface as a multi-field document,
   then emits the top ``--target-retrieved`` papers *with an explanation* of why
   each one is relevant (which question, which terms, which field, and a snippet).
   This is the "regular method": relevance to the task is shown, not asserted.

The script is deliberately only stages 1--2. Stages 3--4 (rank the ~50 by
reading their surfaces down to ~20, then hand ~10 to ``$embodied-ai-paper-reader``
for full-text reading) are agent-mediated and documented in SKILL.md -- see
``references/retrieval-method.md`` and ``references/problem-relevance-rubric.md``.

BM25 rather than dense embeddings because this repo is stdlib-only; sparse
lexical retrieval is deterministic, explainable, and needs no model weights.

Retry/backoff, arXiv-id normalization, and the citation-neighbor coupling filter
are copied from ``expand_via_citations.py`` / ``rank_influential_papers.py`` so
behavior under rate limiting is identical.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import math
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://api.semanticscholar.org/graph/v1"
NEIGHBOR_FIELDS = "title,abstract,year,publicationDate,authors,externalIds"
MAX_RETRIES = 3
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
WRAPPER_KEY = {"references": "citedPaper", "citations": "citingPaper"}
DEFAULT_SEED_STATUSES = frozenset({"accepted", "full-text-queued", "extracted"})
DEFAULT_CACHE_DIR = os.path.join(tempfile.gettempdir(), "embodied-ai-problem-relevance-ranking", "html")

# BM25 hyper-parameters (standard Okapi defaults).
K1 = 1.5
B = 0.75

FIELD_ORDER = ("title", "abstract", "introduction", "related_work")
DEFAULT_FIELD_WEIGHTS = "title=2.0,abstract=1.0,introduction=1.5,related_work=1.5"

# Function words / question words that carry no topical signal. Content words
# ("camera", "align", "initialize", "third-person", …) are intentionally KEPT.
STOPWORDS = frozenset(
    {
        "the", "a", "an", "and", "or", "but", "if", "then", "else", "of", "to", "in", "on",
        "for", "with", "by", "at", "from", "as", "is", "are", "was", "were", "be", "been",
        "being", "this", "that", "these", "those", "it", "its", "their", "our", "we", "you",
        "your", "my", "his", "her", "they", "them", "can", "could", "may", "might", "will",
        "would", "shall", "should", "not", "no", "do", "does", "did", "has", "have", "had",
        "such", "than", "also", "into", "onto", "over", "under", "between", "among", "across",
        "via", "without", "within", "toward", "towards", "each", "both", "other", "more",
        "most", "some", "any", "all", "per", "during", "after", "before", "while", "how",
        "what", "which", "who", "when", "where", "why", "there", "here", "one", "two",
        "three", "very", "only", "same", "own", "about", "using", "used", "use",
    }
)

TOKEN_RE = re.compile(r"[a-z][a-z0-9\-]{2,}")

_SURVEY_RE = re.compile(r"\b(?:survey|review|roadmap)\b", re.IGNORECASE)
_DATASET_RE = re.compile(r"\b(?:dataset|benchmark|corpus)\b", re.IGNORECASE)

# Related-work section title keywords (matched case-insensitively).
RELATED_WORK_KEYWORDS = (
    "related work",
    "related works",
    "prior work",
    "related studies",
    "related research",
    "related literatur",
    "relation to prior work",
    "background",
)


def _load_extract_arxiv_html():
    """Import the literature-hub's HTML extractor as a library.

    The skill scripts are not importable packages (no ``__init__.py``), so load the
    sibling script by file path -- the same mechanism the tests use.
    """
    path = Path(__file__).resolve().parents[2] / "embodied-ai-literature-hub" / "scripts" / "extract_arxiv_html.py"
    spec = importlib.util.spec_from_file_location("extract_arxiv_html", path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_ARXIV_HTML = _load_extract_arxiv_html()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question", action="append", default=[], help="Open research question. May be repeated.")
    parser.add_argument("--seed-id", action="append", default=[], help="Seed arXiv ID. May be repeated.")
    parser.add_argument("--seed-id-file", help="File with one arXiv ID per line.")
    parser.add_argument("--seed-registry", help="candidate-registry.json to pull seeds from by status.")
    parser.add_argument("--seed-status", action="append", default=[],
                        help="Registry status treated as a seed. May be repeated; default accepted,full-text-queued,extracted.")
    parser.add_argument("--exclude-id-file", action="append", default=[],
                        help="File of arXiv IDs to exclude from results (e.g. papers already read in the review).")
    parser.add_argument("--rounds", type=int, default=2, help="Citation-expansion rounds.")
    parser.add_argument("--direction", choices=["references", "citations", "both"], default="both")
    parser.add_argument("--max-per-seed-per-direction", type=int, default=200, help="Per-request neighbor cap (API max 1000).")
    parser.add_argument("--min-shared-seeds", type=int, default=None,
                        help="Candidates must connect to at least this many seeds. Default: 2 if >=2 seeds, else 1.")
    parser.add_argument("--max-total-candidates", type=int, default=400, help="Cap on the corpus before retrieval.")
    parser.add_argument("--top-k-per-round", type=int, default=20, help="Candidates carried forward as next round's seeds.")
    parser.add_argument("--max-fulltext-per-round", type=int, default=40, help="Cap on arXiv HTML judgment-surface fetches per round.")
    parser.add_argument("--target-retrieved", type=int, default=50, help="How many papers to emit after BM25 retrieval.")
    parser.add_argument("--min-year", type=int, default=None, help="Drop papers published before this year (inclusive).")
    parser.add_argument("--require-terms", default=None,
                        help="Comma-separated terms; keep a candidate only if at least one appears (case-insensitive) in title+abstract.")
    parser.add_argument("--must-terms", default=None,
                        help="Comma-separated terms; a candidate is DROPPED unless at least one appears in title+abstract.")
    parser.add_argument("--field-weights", default=DEFAULT_FIELD_WEIGHTS,
                        help="Comma-separated field=weight for BM25 multi-field scoring.")
    parser.add_argument("--output", help="Retrieved JSON. Defaults to stdout.")
    parser.add_argument("--markdown-output", help="Retrieval table + explanation Markdown.")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Delay between network phases.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0)
    parser.add_argument("--retry-max-seconds", type=float, default=60.0)
    parser.add_argument("--fail-fast", action="store_true", help="Abort on first failed request.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR, help="arXiv HTML cache directory.")
    parser.add_argument("--user-agent", default="embodied-ai-problem-relevance-ranking/1.0 (local research workflow)")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to S2_API_KEY env var.")
    return parser.parse_args()


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_arxiv_id(value: object) -> str:
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())


# ---------------------------------------------------------------------------
# Tokenization (shared by the query and the documents)
# ---------------------------------------------------------------------------


def tokenize(text: str) -> list[str]:
    """Lowercase, keep hyphenated compounds, strip stopwords, drop <3-char tokens.

    A hyphenated compound like ``multi-view`` additionally yields its de-hyphenated
    form ``multiview`` (and ``ego-exo`` -> ``egoexo``) so common spelling variants
    match without a stemmer; the extra form can only add a match, never a penalty.
    """
    out: list[str] = []
    for token in TOKEN_RE.findall((text or "").lower()):
        if token in STOPWORDS:
            continue
        out.append(token)
        if "-" in token:
            out.append(token.replace("-", ""))
    return out


# ---------------------------------------------------------------------------
# Network: retry/backoff copied from search_arxiv.py / expand_via_citations.py
# ---------------------------------------------------------------------------


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


def retry_wait_seconds(exc: Exception, attempt: int, args: argparse.Namespace) -> float:
    retry_after = retry_after_seconds(exc)
    if retry_after is not None:
        return max(0.0, min(retry_after, args.retry_max_seconds))
    return max(0.0, min(args.retry_base_seconds * (2**attempt), args.retry_max_seconds))


def _request(url: str, args: argparse.Namespace, data: bytes | None = None) -> bytes:
    headers = {"User-Agent": args.user_agent}
    if data is not None:
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
    if getattr(args, "api_key", None):
        headers["x-api-key"] = args.api_key
    request = urllib.request.Request(url, data=data, headers=headers)
    last_error: Exception | None = None
    retries = bounded_retries(args.retries)
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                return response.read()
        except Exception as exc:  # pragma: no cover - network dependent
            last_error = exc
            if attempt < retries and is_retryable(exc):
                time.sleep(retry_wait_seconds(exc, attempt, args))
                continue
            break
    raise RuntimeError(f"request to {url} failed: {last_error}") from last_error


def fetch_json(url: str, args: argparse.Namespace, data: bytes | None = None) -> dict:
    raw = _request(url, args, data=data)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:  # pragma: no cover - data dependent
        raise RuntimeError(f"non-JSON response from {url}") from exc


# ---------------------------------------------------------------------------
# Stage 1: citation neighbors + bibliographic coupling
# ---------------------------------------------------------------------------


def neighbor_url(seed_id: str, direction: str, limit: int) -> str:
    endpoint = "references" if direction == "references" else "citations"
    params = {"fields": NEIGHBOR_FIELDS, "limit": str(max(1, min(limit, 1000)))}
    return f"{API_BASE}/paper/ARXIV:{seed_id}/{endpoint}?" + urllib.parse.urlencode(params)


def extract_neighbor_papers(direction: str, raw_json: dict) -> tuple[list[dict], int]:
    """Pull arXiv-identified neighbors out of a references/citations response."""
    wrapper_key = WRAPPER_KEY[direction]
    papers: list[dict] = []
    excluded = 0
    for item in raw_json.get("data", []) or []:
        if not isinstance(item, dict):
            excluded += 1
            continue
        inner = item.get(wrapper_key)
        if not isinstance(inner, dict):
            excluded += 1
            continue
        external_ids = inner.get("externalIds") or {}
        arxiv_raw = external_ids.get("ArXiv") if isinstance(external_ids, dict) else None
        arxiv_id = normalize_arxiv_id(arxiv_raw) if arxiv_raw else ""
        if not arxiv_id:
            excluded += 1
            continue
        authors = [a.get("name") for a in inner.get("authors") or [] if isinstance(a, dict) and a.get("name")]
        published = inner.get("publicationDate") or (str(inner["year"]) if inner.get("year") else "")
        papers.append(
            {
                "arxiv_id": arxiv_id,
                "title": inner.get("title") or "",
                "authors": authors,
                "published": published,
                "abstract": inner.get("abstract") or "",
            }
        )
    return papers, excluded


def year_of(published: object) -> int | None:
    text = str(published or "").strip()
    match = re.match(r"(\d{4})", text)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def passes_field_gates(title: str, abstract: str, args: argparse.Namespace) -> bool:
    """Hard (binary) gates on title+abstract: --require-terms (OR), --must-terms (AND)."""
    require = [t.strip().lower() for t in (args.require_terms or "").split(",") if t.strip()]
    must = [t.strip().lower() for t in (args.must_terms or "").split(",") if t.strip()]
    if not require and not must:
        return True
    text = f"{title} {abstract}".lower()
    if must and not any(t in text for t in must):
        return False
    if require and not any(t in text for t in require):
        return False
    return True


def coupling_scores(
    seed_references: dict[str, set[str]], seed_citations: dict[str, set[str]], seed_ids: set[str]
) -> list[dict]:
    """Score each non-seed neighbor by how many distinct seeds connect to it."""
    entries: dict[str, dict] = {}
    for seed_id, ids in seed_references.items():
        for arxiv_id in ids:
            if arxiv_id in seed_ids:
                continue
            entry = entries.setdefault(arxiv_id, {"shared_seed_count": 0, "connected_seeds": set()})
            entry["shared_seed_count"] += 1
            entry["connected_seeds"].add(seed_id)
    for seed_id, ids in seed_citations.items():
        for arxiv_id in ids:
            if arxiv_id in seed_ids:
                continue
            entry = entries.setdefault(arxiv_id, {"shared_seed_count": 0, "connected_seeds": set()})
            entry["shared_seed_count"] += 1
            entry["connected_seeds"].add(seed_id)
    return [
        {"arxiv_id": arxiv_id, "shared_seed_count": entry["shared_seed_count"],
         "connected_seeds": sorted(entry["connected_seeds"])}
        for arxiv_id, entry in entries.items()
    ]


# ---------------------------------------------------------------------------
# Stage 1: judgment surface (abstract + introduction + related-work) via HTML
# ---------------------------------------------------------------------------


def classify_judgment_section(title: str, kind: str) -> str:
    """Map a LaTeXML section to abstract / introduction / related_work / other."""
    if kind == "ltx_abstract" or (title or "").strip().lower() == "abstract":
        return "abstract"
    lower = (title or "").strip().lower()
    if not lower:
        return "other"
    if "introduction" in lower:
        return "introduction"
    if any(keyword in lower for keyword in RELATED_WORK_KEYWORDS):
        return "related_work"
    return "other"


def extract_judgment_surface(sections: list[dict]) -> dict:
    """Join abstract / introduction / related-work section text from a parsed LaTeXML tree."""
    buckets: dict[str, list[str]] = {"abstract": [], "introduction": [], "related_work": []}
    for section in sections:
        if not isinstance(section, dict):
            continue
        kind = classify_judgment_section(str(section.get("title", "")), str(section.get("kind", "")))
        if kind in buckets:
            text = str(section.get("text", "")).strip()
            if text:
                buckets[kind].append(text)
    surface = {key: "\n\n".join(parts) for key, parts in buckets.items()}
    surface["complete"] = bool(surface["abstract"] or surface["introduction"] or surface["related_work"])
    return surface


def html_cache_path(args: argparse.Namespace, arxiv_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", arxiv_id)
    return Path(args.cache_dir).expanduser() / f"{safe}.html"


def fetch_html(arxiv_id: str, args: argparse.Namespace) -> tuple[bool, str]:
    """Return (available, html) with on-disk caching; 404/410 count as unavailable."""
    target = html_cache_path(args, arxiv_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return True, target.read_text(encoding="utf-8", errors="replace")
    url = f"https://arxiv.org/html/{normalize_arxiv_id(arxiv_id)}"
    try:
        payload = _request(url, args)
    except RuntimeError as exc:  # pragma: no cover - network dependent
        # A 404 raised inside _request surfaces as a RuntimeError here; treat as unavailable.
        if "404" in str(exc) or "410" in str(exc):
            return False, ""
        raise
    text = payload.decode("utf-8", errors="replace")
    target.write_text(text, encoding="utf-8")
    return True, text


def fetch_judgment_surface(arxiv_id: str, args: argparse.Namespace) -> dict | None:
    """Extract the judgment surface from a paper's arXiv HTML, or None if unavailable/flat."""
    try:
        available, html = fetch_html(arxiv_id, args)
    except Exception:  # pragma: no cover - network dependent
        return None
    if not available:
        return None
    structured = _ARXIV_HTML.extract_structured(html)
    if structured is None:
        return None
    return extract_judgment_surface(structured.sections)


# ---------------------------------------------------------------------------
# Stage 2: BM25 sparse retrieval (the "regular method")
# ---------------------------------------------------------------------------


def parse_field_weights(raw: str) -> dict[str, float]:
    weights: dict[str, float] = {}
    for part in raw.split(","):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, val = part.partition("=")
        try:
            weights[key.strip()] = float(val.strip())
        except ValueError:
            continue
    return {field: weights.get(field, 0.0) for field in FIELD_ORDER}


def build_index(docs: list[dict], field_tokens: dict[str, list[str]]) -> dict:
    """Build term document-frequency + per-field average length over the corpus.

    ``field_tokens`` maps arxiv_id -> {field: [tokens]} for the corpus documents.
    """
    field_df: dict[str, dict[str, int]] = {field: {} for field in FIELD_ORDER}
    field_total_len: dict[str, int] = {field: 0 for field in FIELD_ORDER}
    n = 0
    for doc in docs:
        tokens_by_field = field_tokens.get(doc["arxiv_id"], {})
        if not tokens_by_field:
            continue
        n += 1
        for field in FIELD_ORDER:
            tokens = tokens_by_field.get(field, [])
            field_total_len[field] += len(tokens)
            for term in set(tokens):
                field_df[field][term] = field_df[field].get(term, 0) + 1
    avg_len = {
        field: (field_total_len[field] / n) if n else 0.0 for field in FIELD_ORDER
    }
    return {"n": n, "field_df": field_df, "avg_len": avg_len}


def bm25_field(tf: int, df: int, n: int, doc_len: int, avg_len: float) -> float:
    """Okapi BM25 for one term in one field. Monotonic in tf, inverse in df, length-normalized."""
    if tf <= 0 or n <= 0 or avg_len <= 0:
        return 0.0
    idf = math.log((n - df + 0.5) / (df + 0.5) + 1.0)
    norm = tf * (K1 + 1.0) / (tf + K1 * (1.0 - B + B * (doc_len / avg_len)))
    return idf * norm


def _snippet(text: str, term: str, window: int = 120) -> str:
    """A short window around the first occurrence of ``term`` (hyphen-insensitive)."""
    if not text or not term:
        return ""
    lowered = text.lower()
    index = lowered.find(term.lower())
    if index < 0:
        # Fall back to a de-hyphenated search so multi-view/multiview variants match.
        hay = text.replace("-", "")
        index = hay.lower().find(term.replace("-", "").lower())
        if index < 0:
            return ""
        left = max(0, index - window)
        return "…" + " ".join(hay[left : index + len(term) + window].split()) + "…"
    left = max(0, index - window)
    return "…" + " ".join(text[left : index + len(term) + window].split()) + "…"


def score_document(tokens_by_field: dict[str, list[str]], query_terms: list[str], index: dict,
                   field_weights: dict[str, float]) -> dict:
    """Field-weighted BM25 of one document against one question's terms, with an explanation."""
    n = index["n"]
    field_df = index["field_df"]
    avg_len = index["avg_len"]
    total = 0.0
    contributions: list[dict] = []
    matched: set[str] = set()
    for field in FIELD_ORDER:
        weight = field_weights.get(field, 0.0)
        tokens = tokens_by_field.get(field, [])
        doc_len = len(tokens)
        counts: dict[str, int] = {}
        for tok in tokens:
            counts[tok] = counts.get(tok, 0) + 1
        for term in query_terms:
            tf = counts.get(term, 0)
            if tf == 0:
                continue
            df = field_df.get(field, {}).get(term, 0)
            contribution = weight * bm25_field(tf, df, n, doc_len, avg_len.get(field, 0.0))
            if contribution <= 0:
                continue
            total += contribution
            matched.add(term)
            contributions.append({"term": term, "field": field, "contribution": round(contribution, 4)})
    contributions.sort(key=lambda item: (-item["contribution"], item["term"], item["field"]))
    return {"score": total, "matched_terms": sorted(matched), "contributions": contributions}


def retrieve(corpus: list[dict], questions: list[dict], field_weights: dict[str, float],
             target: int) -> tuple[list[dict], int, dict]:
    """BM25 retrieval over the corpus, one query per question; rank by max-over-questions."""
    # Pre-tokenize every document field once.
    field_tokens: dict[str, dict[str, list[str]]] = {}
    for doc in corpus:
        surface = doc.get("judgment_surface") or {}
        field_tokens[doc["arxiv_id"]] = {
            "title": tokenize(doc.get("title", "")),
            "abstract": tokenize(surface.get("abstract") or doc.get("abstract", "")),
            "introduction": tokenize(surface.get("introduction", "")),
            "related_work": tokenize(surface.get("related_work", "")),
        }
    index = build_index(corpus, field_tokens)

    results: list[dict] = []
    for doc in corpus:
        per_question = []
        best = 0.0
        total_sum = 0.0
        for question in questions:
            scored = score_document(field_tokens[doc["arxiv_id"]], question["terms"], index, field_weights)
            per_question.append(
                {
                    "question": question["text"],
                    "bm25": round(scored["score"], 4),
                    "matched_terms": scored["matched_terms"],
                    "contributions": scored["contributions"],
                }
            )
            best = max(best, scored["score"])
            total_sum += scored["score"]
        results.append(
            {
                "arxiv_id": doc["arxiv_id"],
                "title": doc.get("title", ""),
                "published": doc.get("published", ""),
                "connected_seeds": doc.get("connected_seeds", []),
                "round": doc.get("round"),
                "is_survey": bool(_SURVEY_RE.search(doc.get("title", ""))),
                "is_dataset": bool(_DATASET_RE.search(doc.get("title", ""))),
                "surface_complete": bool((doc.get("judgment_surface") or {}).get("complete")),
                "judgment_surface": doc.get("judgment_surface") or {},
                "retrieval_score": round(best, 4),
                "retrieval_score_sum": round(total_sum, 4),
                "per_question": per_question,
            }
        )
    results.sort(key=lambda item: (-item["retrieval_score"], -item["retrieval_score_sum"], item["arxiv_id"]))
    truncated = max(0, len(results) - target)
    kept = results[:target]
    for rank, item in enumerate(kept, start=1):
        item["rank"] = rank
        item["explanation"] = build_explanation(item, field_weights)
    return kept, truncated, index


def build_explanation(item: dict, field_weights: dict[str, float]) -> list[dict]:
    """Shape per-question term contributions into a readable explanation, with snippets.

    Contributions are aggregated **by distinct term** (summing across the fields the term
    matched in) so the explanation surfaces the top *concepts* rather than a noisy list of
    (term × field) pairs. Hyphen variants are merged onto the hyphenated form (``multi-view``
    vs ``multiview``) so one concept is one row. The snippet is pulled from the field with the
    highest contribution, showing *where* in the paper the relevance lives (title vs abstract
    vs introduction vs related-work).
    """
    surface = item.get("judgment_surface") or {}
    field_text = {
        "title": item.get("title", ""),
        "abstract": surface.get("abstract", ""),
        "introduction": surface.get("introduction", ""),
        "related_work": surface.get("related_work", ""),
    }
    explanation: list[dict] = []
    for q in item.get("per_question", []):
        by_term: dict[str, dict] = {}
        for contribution in q.get("contributions", []):
            term = contribution["term"]
            key = term.replace("-", "")
            agg = by_term.setdefault(key, {"display": term, "total": 0.0, "fields": []})
            if "-" in term and "-" not in agg["display"]:
                agg["display"] = term
            agg["total"] += contribution["contribution"]
            agg["fields"].append({"field": contribution["field"], "contribution": contribution["contribution"]})
        ranked = sorted(by_term.values(), key=lambda a: (-a["total"], a["display"]))[:6]
        terms = []
        for agg in ranked:
            agg["fields"].sort(key=lambda f: (-f["contribution"], f["field"]))
            top_field = agg["fields"][0]["field"]
            seen_fields: list[str] = []
            for f in agg["fields"]:
                if f["field"] not in seen_fields:
                    seen_fields.append(f["field"])
            terms.append(
                {
                    "term": agg["display"],
                    "total_contribution": round(agg["total"], 4),
                    "fields": seen_fields,
                    "field_weights": {f: field_weights.get(f, 0.0) for f in seen_fields},
                    "snippet": _snippet(field_text.get(top_field, ""), agg["display"]),
                }
            )
        if terms:
            explanation.append({"question": q.get("question", ""), "bm25": q.get("bm25", 0.0), "terms": terms})
    return explanation


# ---------------------------------------------------------------------------
# CLI orchestration
# ---------------------------------------------------------------------------


def load_ids_from_file(path: str) -> list[str]:
    try:
        return [normalize_arxiv_id(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError:
        return []


def load_seed_ids_from_registry(path: str, statuses: set[str]) -> list[str]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    ids = []
    for candidate in data.get("candidates", []) or []:
        if isinstance(candidate, dict) and candidate.get("status") in statuses:
            arxiv_id = normalize_arxiv_id(candidate.get("arxiv_id"))
            if arxiv_id:
                ids.append(arxiv_id)
    return ids


def collect_seed_ids(args: argparse.Namespace) -> list[str]:
    ids = list(args.seed_id or [])
    if args.seed_id_file:
        ids.extend(load_ids_from_file(args.seed_id_file))
    if args.seed_registry:
        statuses = set(args.seed_status) if args.seed_status else set(DEFAULT_SEED_STATUSES)
        ids.extend(load_seed_ids_from_registry(args.seed_registry, statuses))
    return sorted({normalize_arxiv_id(i) for i in ids if normalize_arxiv_id(i)})


def collect_exclude_ids(args: argparse.Namespace, seed_ids: list[str]) -> set[str]:
    excluded = set(seed_ids)  # seeds are always excluded from results
    for path in args.exclude_id_file:
        excluded.update(load_ids_from_file(path))
    return excluded


def run_round(seed_ids: list[str], args: argparse.Namespace) -> tuple[list[dict], dict[str, dict], int, int]:
    """Fetch neighbors for a seed set and return (scored candidates, paper_meta, excluded, errors)."""
    seed_set = set(seed_ids)
    seed_references: dict[str, set[str]] = {}
    seed_citations: dict[str, set[str]] = {}
    paper_meta: dict[str, dict] = {}
    excluded = 0
    errors = 0
    directions = ["references", "citations"] if args.direction == "both" else [args.direction]
    for seed_id in seed_ids:
        for direction in directions:
            try:
                payload = fetch_json(neighbor_url(seed_id, direction, args.max_per_seed_per_direction), args)
                papers, _excluded = extract_neighbor_papers(direction, payload)
                excluded += _excluded
            except Exception as exc:  # pragma: no cover - network dependent
                if args.fail_fast:
                    raise
                errors += 1
                papers = []
            bucket = seed_references if direction == "references" else seed_citations
            ids = bucket.setdefault(seed_id, set())
            for paper in papers:
                arxiv_id = paper["arxiv_id"]
                ids.add(arxiv_id)
                existing = paper_meta.setdefault(arxiv_id, dict(paper))
                for field in ("title", "abstract", "published", "authors"):
                    if not existing.get(field) and paper.get(field):
                        existing[field] = paper[field]
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)
    scored = coupling_scores(seed_references, seed_citations, seed_set)
    return scored, paper_meta, excluded, errors


def build_corpus_entry(paper_meta: dict, coupling: dict, round_num: int,
                       surface: dict | None) -> dict:
    abstract = paper_meta.get("abstract", "")
    merged = {
        "abstract": surface.get("abstract") if surface else "",
        "introduction": surface.get("introduction") if surface else "",
        "related_work": surface.get("related_work") if surface else "",
        "complete": bool(surface and surface.get("complete")),
    }
    if not merged["abstract"] and abstract:
        merged["abstract"] = abstract
        merged["complete"] = merged["complete"] or bool(abstract)
    return {
        "arxiv_id": coupling["arxiv_id"],
        "title": paper_meta.get("title", ""),
        "abstract": abstract,
        "authors": paper_meta.get("authors", []),
        "published": paper_meta.get("published", ""),
        "connected_seeds": coupling.get("connected_seeds", []),
        "shared_seed_count": coupling.get("shared_seed_count", 0),
        "round": round_num,
        "judgment_surface": merged,
    }


def default_min_shared_seeds(seed_count: int) -> int:
    return 2 if seed_count >= 2 else 1


def markdown_output(questions: list[dict], field_weights: dict[str, float], retrieved: list[dict],
                    truncated: int) -> str:
    lines = [
        "# Problem-relevance retrieval",
        "",
        f"- Method: BM25 (k1={K1}, b={B}) over judgment surface, field weights "
        + ", ".join(f"{k}={v:g}" for k, v in field_weights.items()) + ".",
        f"- Rank by `max` BM25 over the questions; `sum` reported as a secondary signal.",
        "- *Candidate-level discovery only — not accepted evidence.*",
        "",
        "## Questions",
        "",
    ]
    for question in questions:
        lines.append(f"- **{question['text']}** — terms: `{', '.join(question['terms'][:20])}`")
    lines += [
        "",
        "## Retrieved papers",
        "",
        "| # | arXiv | Title | Year | Q1 | Sum | Surf. | Dir/round |",
        "|---:|---|---|---:|---:|---:|:--:|:--:|",
    ]
    for item in retrieved:
        per_q = item.get("per_question", [])
        q1 = per_q[0]["bm25"] if per_q else 0.0
        surf = "✓" if item["surface_complete"] else "~"
        round_label = f"r{item['round']}" if item.get("round") else "—"
        lines.append(
            f"| {item['rank']} | [{item['arxiv_id']}](https://arxiv.org/abs/{item['arxiv_id']}) "
            f"| {item['title']} | {year_of(item.get('published')) or '—'} | {q1} "
            f"| {item['retrieval_score_sum']} | {surf} | {round_label} |"
        )
    if truncated:
        lines += ["", f"_{truncated} papers below the target were truncated._"]
    lines += ["", "## Explanations", ""]
    for item in retrieved:
        lines.append(f"### {item['rank']}. [{item['arxiv_id']}](https://arxiv.org/abs/{item['arxiv_id']}) — {item['title']}")
        for q in item.get("explanation", []):
            lines.append(f"- **{q['question']}** (bm25 {q['bm25']})")
            for term in q["terms"]:
                snip = term["snippet"].replace("\n", " ") if term["snippet"] else "—"
                fields = "+".join(term["fields"])
                lines.append(
                    f"  - `{term['term']}` (contrib {term['total_contribution']}) in [{fields}]: {snip}"
                )
        lines.append("")
    return "\n".join(lines) + "\n"


def write_json(path: str | None, data: dict) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def write_text(path: str | None, text: str) -> None:
    if path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    else:
        print(text)


def build_output(questions: list[dict], field_weights: dict[str, float], retrieved: list[dict],
                 args: argparse.Namespace, corpus_size: int, truncated: int,
                 errors: list[dict]) -> dict:
    return {
        "generated_at": stable_now(),
        "method": "multi-round citation expansion + BM25 sparse retrieval over judgment surface",
        "questions": questions,
        "field_weights": field_weights,
        "k1": K1,
        "b": B,
        "seeds": sorted(collect_seed_ids(args)),
        "rounds": args.rounds,
        "direction": args.direction,
        "min_year": args.min_year,
        "require_terms": args.require_terms,
        "must_terms": args.must_terms,
        "corpus_size": corpus_size,
        "retrieved_count": len(retrieved),
        "truncated_count": truncated,
        "errors": errors,
        "papers": [
            {k: v for k, v in item.items() if k != "explanation"}
            for item in retrieved
        ],
    }


def main() -> int:
    args = parse_args()
    if not args.api_key:
        args.api_key = os.environ.get("S2_API_KEY")

    questions = [q.strip() for q in args.question if q and q.strip()]
    if not questions:
        raise SystemExit("provide at least one --question")
    questions = [{"text": q, "terms": tokenize(q)} for q in questions]

    seed_ids = collect_seed_ids(args)
    if not seed_ids:
        raise SystemExit("provide at least one seed via --seed-id/--seed-id-file/--seed-registry")
    excluded_ids = collect_exclude_ids(args, seed_ids)

    field_weights = parse_field_weights(args.field_weights)

    corpus: list[dict] = []
    seen: set[str] = set(seed_ids) | excluded_ids
    current_seeds = seed_ids
    errors: list[dict] = []

    for round_num in range(1, args.rounds + 1):
        scored, paper_meta, _excluded, _errors = run_round(current_seeds, args)
        if _errors:
            errors.append({"round": round_num, "request_errors": _errors})

        min_shared = args.min_shared_seeds if args.min_shared_seeds is not None else default_min_shared_seeds(len(current_seeds))
        survivors = [s for s in scored if s["shared_seed_count"] >= min_shared]

        # Hard gates + dedup, then cap full-text fetch + carry-forward.
        survivors = [s for s in survivors if s["arxiv_id"] not in seen]
        survivors = [
            s for s in survivors
            if passes_field_gates(paper_meta.get(s["arxiv_id"], {}).get("title", ""),
                                  paper_meta.get(s["arxiv_id"], {}).get("abstract", ""), args)
            and (args.min_year is None or year_of(paper_meta.get(s["arxiv_id"], {}).get("published")) is None
                 or year_of(paper_meta.get(s["arxiv_id"], {}).get("published")) >= args.min_year)
        ]
        # Rank by bibliographic coupling for carry-forward and full-text budget.
        survivors.sort(key=lambda s: (-s["shared_seed_count"], s["arxiv_id"]))

        for coupling in survivors[: args.max_fulltext_per_round]:
            surface = fetch_judgment_surface(coupling["arxiv_id"], args)
            corpus.append(build_corpus_entry(paper_meta.get(coupling["arxiv_id"], {}), coupling, round_num, surface))
            seen.add(coupling["arxiv_id"])
            if args.sleep_seconds > 0:
                time.sleep(args.sleep_seconds)

        if len(corpus) >= args.max_total_candidates:
            break

        # Carry the top coupling-coupled candidates forward as next round's seeds.
        current_seeds = [s["arxiv_id"] for s in survivors[: args.top_k_per_round]]
        if not current_seeds:
            break

    retrieved, truncated, _index = retrieve(corpus, questions, field_weights, args.target_retrieved)
    output = build_output(questions, field_weights, retrieved, args, len(corpus), truncated, errors)
    write_json(args.output, output)
    if args.markdown_output:
        write_text(args.markdown_output, markdown_output(questions, field_weights, retrieved, truncated))

    print(
        f"problem-relevance retrieval from {len(seed_ids)} seed(s) over {args.rounds} round(s): "
        f"{len(corpus)} corpus papers, top {len(retrieved)} retrieved ({truncated} truncated), "
        f"{len(errors)} round error group(s)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

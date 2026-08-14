#!/usr/bin/env python3
"""Expand candidate discovery through citation relationships (Semantic Scholar).

Keyword search alone under-covers a broad topic's sub-themes. This script
chases each seed paper's references (what it cites) and citations (what
cites it) one hop out, then keeps only the neighbors that connect to
*multiple* seeds -- bibliographic coupling (shared references) and
co-citation (shared citing papers), the same signal Connected Papers uses --
instead of naively keeping every 1-hop neighbor, which explodes for
highly-cited seeds. Neighbors below the shared-seed threshold are reported,
not silently dropped. Terms mined from the surviving candidates can be
emitted as a query-planner ``--dynamic-file`` to widen the next keyword
round.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://api.semanticscholar.org/graph/v1"
NEIGHBOR_FIELDS = "title,abstract,year,publicationDate,authors,externalIds"
MAX_RETRIES = 3
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
DEFAULT_SEED_STATUSES = frozenset({"accepted", "full-text-queued", "extracted"})
WRAPPER_KEY = {"references": "citedPaper", "citations": "citingPaper"}

_FUNCTION_STOPWORDS = frozenset(
    {
        "the", "a", "an", "and", "or", "but", "if", "then", "else", "of", "to", "in", "on", "for",
        "with", "by", "at", "from", "as", "is", "are", "was", "were", "be", "been", "being", "this",
        "that", "these", "those", "it", "its", "their", "our", "we", "can", "could", "may", "might",
        "will", "would", "shall", "should", "not", "no", "do", "does", "did", "has", "have", "had",
        "such", "than", "also", "into", "over", "under", "between", "across", "via", "without",
        "within", "toward", "towards", "each", "both", "other", "more", "most", "some", "any", "all",
        "per", "during", "after", "before", "while", "how", "what", "which", "who", "when", "where",
        "there", "here", "one", "two", "three", "very", "only", "same", "own", "about",
    }
)
_GENERIC_DOMAIN_WORDS = frozenset(
    {
        "robot", "robots", "robotic", "robotics", "learning", "model", "models", "modeling", "data",
        "method", "methods", "approach", "approaches", "paper", "task", "tasks", "using", "based",
        "novel", "propose", "proposed", "present", "presented", "results", "result", "show", "shows",
        "showing", "demonstrate", "demonstrates", "demonstrated", "work", "works", "system", "systems",
        "framework", "frameworks", "study", "studies", "new", "recent", "large", "scale", "real",
        "world", "existing", "significant", "significantly", "improve", "improves", "improved",
    }
)
TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9\-]{2,}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-id", action="append", default=[], help="Seed arXiv ID. May be repeated.")
    parser.add_argument("--seed-id-file", help="File with one arXiv ID per line.")
    parser.add_argument("--seed-registry", help="candidate-registry.json to pull seeds from by status.")
    parser.add_argument(
        "--seed-status",
        action="append",
        default=[],
        help="Registry status treated as a seed. May be repeated; default accepted,full-text-queued,extracted.",
    )
    parser.add_argument("--direction", choices=["references", "citations", "both"], default="both")
    parser.add_argument("--max-per-seed-per-direction", type=int, default=200, help="Per-request neighbor cap (API max 1000).")
    parser.add_argument(
        "--min-shared-seeds",
        type=int,
        default=None,
        help="Candidates must connect to at least this many seeds. Default: 2 if >=2 seeds, else 1.",
    )
    parser.add_argument("--max-total-candidates", type=int, default=200, help="Cap after ranking by shared-seed count.")
    parser.add_argument("--include-below-threshold-output", help="Also write candidates below the shared-seed threshold here.")
    parser.add_argument("--start-date", help="Optional YYYY-MM-DD; coarse year-level filter on discovered papers.")
    parser.add_argument("--end-date", help="Optional YYYY-MM-DD; coarse year-level filter on discovered papers.")
    parser.add_argument("--top-terms", type=int, default=20)
    parser.add_argument("--min-doc-frequency", type=int, default=2)
    parser.add_argument("--extra-stopwords-file", help="Extra stopwords, one per line.")
    parser.add_argument("--batch-label", help="Stable round label stored for candidate-registry saturation analysis.")
    parser.add_argument("--output", help="Candidate-registry-compatible JSON. Defaults to stdout.")
    parser.add_argument("--graph-output", help="Citation edges + seed-similarity JSON.")
    parser.add_argument("--dynamic-output", help="query-planner --dynamic-file compatible JSON.")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Delay between seeds.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request after transient failures. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0, help="Base wait before retrying transient failures.")
    parser.add_argument("--retry-max-seconds", type=float, default=60.0, help="Maximum wait before a single retry.")
    parser.add_argument("--fail-fast", action="store_true", help="Abort on the first failed seed/direction request.")
    parser.add_argument(
        "--user-agent",
        default="embodied-ai-literature-hub/1.0 (local research workflow)",
        help="HTTP User-Agent sent to Semantic Scholar.",
    )
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to the S2_API_KEY env var.")
    return parser.parse_args()


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_arxiv_id(value: object) -> str:
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())


# ---------------------------------------------------------------------------
# Network: retry/backoff logic copied verbatim from search_arxiv.py so this
# script behaves identically under rate limiting; only fetch()'s URL/headers
# differ, since the target API is Semantic Scholar, not arXiv.
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


def build_neighbor_url(seed_id: str, direction: str, limit: int) -> str:
    endpoint = "references" if direction == "references" else "citations"
    clamped = max(1, min(limit, 1000))
    params = {"fields": NEIGHBOR_FIELDS, "limit": str(clamped)}
    return f"{API_BASE}/paper/ARXIV:{seed_id}/{endpoint}?" + urllib.parse.urlencode(params)


def fetch(seed_id: str, direction: str, args: argparse.Namespace) -> bytes:
    url = build_neighbor_url(seed_id, direction, args.max_per_seed_per_direction)
    headers = {"User-Agent": args.user_agent}
    if getattr(args, "api_key", None):
        headers["x-api-key"] = args.api_key
    request = urllib.request.Request(url, headers=headers)
    last_error: Exception | None = None
    attempts = 0
    retries = bounded_retries(args.retries)
    for attempt in range(retries + 1):
        attempts = attempt + 1
        try:
            with urllib.request.urlopen(request, timeout=args.timeout) as response:
                return response.read()
        except Exception as exc:  # pragma: no cover - network dependent
            last_error = exc
            if attempt < retries and is_retryable(exc):
                time.sleep(retry_wait_seconds(exc, attempt, args))
                continue
            break
    raise RuntimeError(
        f"Semantic Scholar request for {seed_id} ({direction}) failed after {attempts} attempt(s): {last_error}"
    ) from last_error


# ---------------------------------------------------------------------------
# Pure logic: neighbor extraction, coupling/co-citation scoring, filtering,
# term mining, output shaping. No network access; fully unit-testable.
# ---------------------------------------------------------------------------


def extract_neighbor_papers(direction: str, raw_json: dict) -> tuple[list[dict], int]:
    """Pull arXiv-identified neighbor papers out of a references/citations response.

    Entries without a Semantic Scholar externalIds.ArXiv crosswalk are outside
    this pipeline's arXiv-only scope and are counted as excluded, not dropped
    silently.
    """
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
                "summary": inner.get("abstract") or "",
            }
        )
    return papers, excluded


def within_date_range(published: str, start_date: str | None, end_date: str | None) -> bool:
    if not start_date and not end_date:
        return True
    if not published:
        return True
    try:
        year = int(published[:4])
    except ValueError:
        return True
    if start_date:
        try:
            if year < int(start_date[:4]):
                return False
        except ValueError:
            pass
    if end_date:
        try:
            if year > int(end_date[:4]):
                return False
        except ValueError:
            pass
    return True


def filter_by_date(papers: list[dict], start_date: str | None, end_date: str | None) -> list[dict]:
    if not start_date and not end_date:
        return papers
    return [p for p in papers if within_date_range(str(p.get("published", "")), start_date, end_date)]


def build_seed_neighbor_sets(
    fetched: dict[tuple[str, str], list[dict]]
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, dict]]:
    """Fold per-(seed, direction) fetch results into reference/citation ID sets plus merged metadata."""
    seed_references: dict[str, set[str]] = {}
    seed_citations: dict[str, set[str]] = {}
    paper_by_id: dict[str, dict] = {}
    for (seed_id, direction), papers in fetched.items():
        bucket = seed_references if direction == "references" else seed_citations
        ids = bucket.setdefault(seed_id, set())
        for paper in papers:
            arxiv_id = paper["arxiv_id"]
            ids.add(arxiv_id)
            existing = paper_by_id.setdefault(arxiv_id, dict(paper))
            for field in ("title", "summary", "published"):
                if not existing.get(field) and paper.get(field):
                    existing[field] = paper[field]
            if not existing.get("authors") and paper.get("authors"):
                existing["authors"] = paper["authors"]
    return seed_references, seed_citations, paper_by_id


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def compute_seed_similarity(
    seed_references: dict[str, set[str]], seed_citations: dict[str, set[str]]
) -> list[dict]:
    """Connected-Papers-style pairwise seed similarity: shared references (bibliographic
    coupling) and shared citers (co-citation), both Jaccard-normalized. Seeds with low
    similarity to the rest of the set are a signal of a distinct sub-topic cluster."""
    seeds = sorted(set(seed_references) | set(seed_citations))
    pairs: list[dict] = []
    for i, seed_a in enumerate(seeds):
        for seed_b in seeds[i + 1 :]:
            reference_jaccard = _jaccard(seed_references.get(seed_a, set()), seed_references.get(seed_b, set()))
            citation_jaccard = _jaccard(seed_citations.get(seed_a, set()), seed_citations.get(seed_b, set()))
            pairs.append(
                {
                    "seed_a": seed_a,
                    "seed_b": seed_b,
                    "reference_coupling_jaccard": round(reference_jaccard, 4),
                    "citation_cocitation_jaccard": round(citation_jaccard, 4),
                    "combined_score": round(reference_jaccard + citation_jaccard, 4),
                }
            )
    pairs.sort(key=lambda item: (-item["combined_score"], item["seed_a"], item["seed_b"]))
    return pairs


def default_min_shared_seeds(seed_count: int) -> int:
    return 2 if seed_count >= 2 else 1


def score_candidates(
    seed_references: dict[str, set[str]],
    seed_citations: dict[str, set[str]],
    paper_by_id: dict[str, dict],
    seed_ids: set[str],
) -> list[dict]:
    """Score each non-seed neighbor by how many distinct seeds connect to it.

    A candidate referenced by (or citing) only one seed carries little
    evidence that it belongs to the shared sub-topic; one connected to
    several seeds is bibliographically coupled with (or co-cites) them,
    which is the actual "same sub-topic" signal.
    """
    entries: dict[str, dict] = {}

    def add(arxiv_id: str, seed_id: str, direction: str) -> None:
        if arxiv_id in seed_ids:
            return
        entry = entries.setdefault(
            arxiv_id,
            {"reference_coupling_count": 0, "citation_coupling_count": 0, "connected_seeds": set(), "query_labels": set()},
        )
        if direction == "references":
            entry["reference_coupling_count"] += 1
        else:
            entry["citation_coupling_count"] += 1
        entry["connected_seeds"].add(seed_id)
        entry["query_labels"].add(f"citation:{seed_id}:{direction}")

    for seed_id, ids in seed_references.items():
        for arxiv_id in ids:
            add(arxiv_id, seed_id, "references")
    for seed_id, ids in seed_citations.items():
        for arxiv_id in ids:
            add(arxiv_id, seed_id, "citations")

    results = []
    for arxiv_id, entry in entries.items():
        base = paper_by_id.get(arxiv_id, {})
        results.append(
            {
                "arxiv_id": arxiv_id,
                "title": base.get("title", ""),
                "authors": base.get("authors", []),
                "published": base.get("published", ""),
                "summary": base.get("summary", ""),
                "reference_coupling_count": entry["reference_coupling_count"],
                "citation_coupling_count": entry["citation_coupling_count"],
                "shared_seed_count": len(entry["connected_seeds"]),
                "connected_seeds": sorted(entry["connected_seeds"]),
                "query_label": ",".join(sorted(entry["query_labels"])),
            }
        )
    return results


def select_candidates(
    scored: list[dict], min_shared_seeds: int, max_total: int | None
) -> tuple[list[dict], list[dict], int]:
    """Rank by shared_seed_count, split at the threshold, cap the survivors -- and report
    everything dropped (below-threshold count, truncated count) instead of discarding it
    silently."""
    ranked = sorted(scored, key=lambda item: (-item["shared_seed_count"], item["arxiv_id"]))
    kept = [item for item in ranked if item["shared_seed_count"] >= min_shared_seeds]
    below_threshold = [item for item in ranked if item["shared_seed_count"] < min_shared_seeds]
    truncated_count = 0
    if max_total is not None and len(kept) > max_total:
        truncated_count = len(kept) - max_total
        kept = kept[:max_total]
    return kept, below_threshold, truncated_count


def calibrated_query_from_term(term: str) -> str:
    if " " in term or "-" in term:
        return f'all:"{term}"'
    return f"all:{term}"


def extract_terms(
    papers: list[dict], top_n: int, min_doc_freq: int, extra_stopwords: frozenset[str] = frozenset()
) -> list[dict]:
    """Rank unigrams/bigrams by document frequency across surviving candidates' title+abstract.

    Generic domain words (model, data, robot, ...) are excluded as standalone
    unigrams but still allowed inside a bigram, so phrases like "world model"
    or "data mixture" survive even though "model"/"data" alone would just add
    noise back into every future query.
    """
    doc_freq: dict[str, int] = {}
    example: dict[str, str] = {}
    for paper in papers:
        text_value = f"{paper.get('title', '')} {paper.get('summary', '')}".lower()
        tokens = [t for t in TOKEN_RE.findall(text_value) if t not in _FUNCTION_STOPWORDS and t not in extra_stopwords]
        seen: set[str] = set()
        for i, tok in enumerate(tokens):
            if tok not in _GENERIC_DOMAIN_WORDS:
                seen.add(tok)
            if i + 1 < len(tokens):
                seen.add(f"{tok} {tokens[i + 1]}")
        for term in seen:
            doc_freq[term] = doc_freq.get(term, 0) + 1
            example.setdefault(term, str(paper.get("arxiv_id", "")))
    ranked = sorted(
        ((term, freq) for term, freq in doc_freq.items() if freq >= min_doc_freq),
        key=lambda item: (-item[1], item[0]),
    )
    return [{"term": term, "doc_frequency": freq, "example_arxiv_id": example[term]} for term, freq in ranked[:top_n]]


def build_dynamic_suggestions(terms: list[dict], seeds: list[str], direction: str) -> dict:
    """Shape terms mined from citation-expansion candidates into a query-planner
    ``--dynamic-file`` (see embodied-ai-query-planner/references/dynamic-expansion.md)."""
    queries = []
    for item in terms:
        term = item["term"]
        confidence = "medium" if item["doc_frequency"] >= 3 else "low"
        label = "citation-term-" + re.sub(r"[^a-z0-9]+", "-", term).strip("-")
        queries.append(
            {
                "label": label,
                "tier": "dynamic-association",
                "query": calibrated_query_from_term(term),
                "why": (
                    f"Term co-occurs in {item['doc_frequency']} citation-expansion candidates "
                    f"({direction} of seeds {', '.join(seeds)}); not yet in the static taxonomy."
                ),
                "source": "citation-expansion",
                "confidence": confidence,
            }
        )
    return {
        "sources": [
            {
                "source": "citation-expansion",
                "confidence": "medium",
                "notes": f"Terms mined from {direction} of seeds: {', '.join(seeds)} via Semantic Scholar citation graph.",
            }
        ],
        "knowledge_ids": [],
        "families": [],
        "queries": queries,
        "browser_fallback_queries": [],
        "web_calibration_queries": [],
    }


def build_candidate_output(
    batch_label: str,
    direction: str,
    seed_ids: list[str],
    kept: list[dict],
    below_threshold_count: int,
    truncated_count: int,
    excluded_no_arxiv_id: int,
    errors: list[dict],
) -> dict:
    papers = [
        {
            "arxiv_id": item["arxiv_id"],
            "title": item["title"],
            "authors": item["authors"],
            "published": item["published"],
            "summary": item["summary"],
            "categories": [],
            "query_label": item["query_label"],
            "shared_seed_count": item["shared_seed_count"],
            "connected_seeds": item["connected_seeds"],
        }
        for item in kept
    ]
    return {
        "generated_at": stable_now(),
        "batch": batch_label,
        "source": "semantic-scholar",
        "direction": direction,
        "seeds": sorted(seed_ids),
        "excluded_no_arxiv_id": excluded_no_arxiv_id,
        "below_threshold_count": below_threshold_count,
        "truncated_count": truncated_count,
        "errors": errors,
        "paper_count": len(papers),
        "papers": papers,
    }


def build_graph_output(
    seed_ids: list[str],
    seed_references: dict[str, set[str]],
    seed_citations: dict[str, set[str]],
    seed_similarity: list[dict],
    excluded_no_arxiv_id: int,
) -> dict:
    edges = []
    for seed_id, ids in seed_references.items():
        for target in sorted(ids):
            edges.append({"from": seed_id, "to": target, "direction": "references"})
    for seed_id, ids in seed_citations.items():
        for target in sorted(ids):
            edges.append({"from": target, "to": seed_id, "direction": "citations"})
    return {
        "generated_at": stable_now(),
        "seeds": sorted(seed_ids),
        "edges": edges,
        "seed_similarity": seed_similarity,
        "excluded_no_arxiv_id": excluded_no_arxiv_id,
    }


# ---------------------------------------------------------------------------
# CLI orchestration
# ---------------------------------------------------------------------------


def load_seed_ids_from_registry(path: str, statuses: set[str]) -> list[str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    ids = []
    for candidate in data.get("candidates", []) or []:
        if isinstance(candidate, dict) and candidate.get("status") in statuses:
            arxiv_id = normalize_arxiv_id(candidate.get("arxiv_id"))
            if arxiv_id:
                ids.append(arxiv_id)
    return ids


def collect_seed_ids(args: argparse.Namespace) -> list[str]:
    ids: list[str] = list(args.seed_id or [])
    if args.seed_id_file:
        ids.extend(line.strip() for line in Path(args.seed_id_file).read_text(encoding="utf-8").splitlines() if line.strip())
    if args.seed_registry:
        statuses = set(args.seed_status) if args.seed_status else set(DEFAULT_SEED_STATUSES)
        ids.extend(load_seed_ids_from_registry(args.seed_registry, statuses))
    normalized = [normalize_arxiv_id(i) for i in ids]
    return sorted({i for i in normalized if i})


def load_extra_stopwords(path: str | None) -> frozenset[str]:
    if not path:
        return frozenset()
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return frozenset(line.strip().lower() for line in lines if line.strip())


def write_json(path: str | None, data: dict) -> None:
    rendered = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def main() -> int:
    args = parse_args()
    if not args.api_key:
        args.api_key = os.environ.get("S2_API_KEY")

    seed_ids = collect_seed_ids(args)
    if not seed_ids:
        raise SystemExit("provide at least one seed via --seed-id/--seed-id-file/--seed-registry")

    directions = ["references", "citations"] if args.direction == "both" else [args.direction]
    fetched: dict[tuple[str, str], list[dict]] = {}
    excluded_no_arxiv_id = 0
    errors: list[dict] = []

    for index, seed_id in enumerate(seed_ids):
        for direction in directions:
            try:
                payload = fetch(seed_id, direction, args)
                raw = json.loads(payload)
                papers, excluded = extract_neighbor_papers(direction, raw)
            except Exception as exc:  # pragma: no cover - network dependent
                if args.fail_fast:
                    raise
                errors.append({"seed": seed_id, "direction": direction, "error": str(exc)})
                papers, excluded = [], 0
            excluded_no_arxiv_id += excluded
            fetched[(seed_id, direction)] = filter_by_date(papers, args.start_date, args.end_date)
        if index < len(seed_ids) - 1 and args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    seed_references, seed_citations, paper_by_id = build_seed_neighbor_sets(fetched)
    seed_similarity = compute_seed_similarity(seed_references, seed_citations)
    scored = score_candidates(seed_references, seed_citations, paper_by_id, set(seed_ids))

    min_shared_seeds = args.min_shared_seeds if args.min_shared_seeds is not None else default_min_shared_seeds(len(seed_ids))
    kept, below_threshold, truncated_count = select_candidates(scored, min_shared_seeds, args.max_total_candidates)

    batch_label = args.batch_label or f"citation-{seed_ids[0]}"
    candidate_output = build_candidate_output(
        batch_label, args.direction, seed_ids, kept, len(below_threshold), truncated_count, excluded_no_arxiv_id, errors
    )
    write_json(args.output, candidate_output)

    if args.graph_output:
        write_json(args.graph_output, build_graph_output(seed_ids, seed_references, seed_citations, seed_similarity, excluded_no_arxiv_id))

    if args.dynamic_output:
        extra_stopwords = load_extra_stopwords(args.extra_stopwords_file)
        terms = extract_terms(kept, args.top_terms, args.min_doc_frequency, extra_stopwords)
        write_json(args.dynamic_output, build_dynamic_suggestions(terms, seed_ids, args.direction))

    if args.include_below_threshold_output:
        below_output = build_candidate_output(
            f"{batch_label}-below-threshold", args.direction, seed_ids, below_threshold, 0, 0, 0, []
        )
        write_json(args.include_below_threshold_output, below_output)

    print(
        f"citation expansion from {len(seed_ids)} seed(s): {len(kept)} kept "
        f"(min_shared_seeds={min_shared_seeds}), {len(below_threshold)} below threshold, "
        f"{truncated_count} truncated, {excluded_no_arxiv_id} excluded (no arXiv id), {len(errors)} request error(s)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

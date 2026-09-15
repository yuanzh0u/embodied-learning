#!/usr/bin/env python3
"""Rank the most influential papers in a root paper's citation neighborhood.

Library API: :class:`InfluenceRanking` (discovery, enrichment, scoring, output
shaping) plus the module-level pure helpers (``classify_venue``,
``parse_weights``, ``filter_papers``, ``log_normalize``, ``citations_per_year``,
...). The CLI surface owns argument parsing and lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/rank_influential_papers.py``.

Unlike the citation-expansion library (which de-noises a *multi-seed* citation
graph by bibliographic coupling / co-citation), this library answers a single
question: given one root paper, which of its 1-hop neighbors (what it cites and
what cites it) are the *most influential*?

Influence is a multi-dimensional score, not a raw citation count. For every
neighbor the library assembles four signals and folds them into one weighted
composite in [0, 1]:

* **citation**  -- Semantic Scholar ``citationCount``, log-normalized against
  the largest count in the candidate set (a paper cited 1000x is not 10x more
  influential than one cited 100x).
* **venue**     -- conference/journal mapped to a prestige tier (see
  ``references/scoring-rubric.md``). Preprints score below any peer-reviewed
  venue; an unmappable venue scores neutrally rather than guessing.
* **author**    -- the strongest author's Semantic Scholar ``hIndex`` (default:
  max across authors; ``--author-strategy first-author`` uses the first author).
* **code**      -- whether the paper ships a public code repo / project. This is
  the weakest, most fragile signal (see ``references/scoring-rubric.md``) and is
  scored so that a *missing* confirmation never penalizes a paper: a confirmed
  repo scores 1.0, a confirmed absence 0.0, and "unknown" 0.5.

Raw signals, per-dimension sub-scores, and non-scored context flags (survey /
dataset / benchmark type, citation velocity, direction) are all emitted so the
ranking is auditable. Output is candidate-level only: it is a *discovery*
artifact, never accepted evidence.

Retry/backoff is copied from ``src/search/arxiv.py`` so behavior under rate
limiting is identical; only the target API and URLs differ.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://api.semanticscholar.org/graph/v1"
NEIGHBOR_FIELDS = "title,abstract,year,publicationDate,citationCount,venue,authors,externalIds"
# Full metadata used by the batch endpoint to enrich pre-discovered arXiv IDs
# (e.g. 2-hop expansion from expand_via_citations.py) that lack citationCount/venue.
ENRICH_FIELDS = "title,abstract,year,publicationDate,citationCount,venue,authors.name,authors.hIndex,authors.citationCount,externalIds"
PWC_BASE = "https://paperswithcode.com/api/v1/papers/"
MAX_RETRIES = 3
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}
BATCH_MAX_IDS = 500

# Canonical (lowercased) venue substrings -> (canonical name, tier score).
# Ordered: more specific phrases must precede phrases they contain, e.g.
# "robotics and automation letters" before "robotics and automation".
VENUE_RULES: list[tuple[str, str, float]] = [
    # tier 1
    ("computer vision and pattern recognition", "CVPR", 1.0),
    ("european conference on computer vision", "ECCV", 1.0),
    ("international conference on computer vision", "ICCV", 1.0),
    ("neural information processing systems", "NeurIPS", 1.0),
    ("advances in neural information processing", "NeurIPS", 1.0),
    ("international conference on learning representations", "ICLR", 1.0),
    ("international conference on machine learning", "ICML", 1.0),
    ("transactions on pattern analysis", "TPAMI", 1.0),
    ("international journal of computer vision", "IJCV", 1.0),
    ("robotics: science and systems", "RSS", 1.0),
    ("nature", "Nature/Science", 1.0),
    ("science", "Nature/Science", 1.0),
    # tier 2
    ("transactions on robotics", "T-RO", 0.66),
    ("robotics and automation letters", "RA-L", 0.66),
    ("robotics and automation", "ICRA", 0.66),
    ("intelligent robots and systems", "IROS", 0.66),
    ("conference on robot learning", "CoRL", 0.66),
    ("robot learning", "CoRL", 0.66),
    ("aaai", "AAAI", 0.66),
    ("association for the advancement of artificial intelligence", "AAAI", 0.66),
    ("international joint conference on artificial intelligence", "IJCAI", 0.66),
    ("journal of machine learning research", "JMLR", 0.66),
    ("transactions on machine learning research", "TMLR", 0.66),
    ("acm transactions on graphics", "SIGGRAPH", 0.66),
    ("siggraph", "SIGGRAPH", 0.66),
    # tier 3
    ("winter conference on applications of computer vision", "WACV", 0.33),
    ("asian conference on computer vision", "ACCV", 0.33),
    ("british machine vision conference", "BMVC", 0.33),
    ("international conference on multimedia", "ACMMM", 0.33),
    ("acm multimedia", "ACMMM", 0.33),
]

CODE_MENTION_RE = re.compile(
    r"\b(?:github|open[- ]?source|code(?:base)? (?:is|are) (?:available|released|publicly)|"
    r"we release|we open|reproduc|implementation|source code|demo)\b",
    re.IGNORECASE,
)

_SURVEY_RE = re.compile(r"\b(?:survey|review|roadmap)\b", re.IGNORECASE)
_DATASET_RE = re.compile(r"\b(?:dataset|benchmark|corpus)\b", re.IGNORECASE)


class InfluenceRanking:
    """One influence-ranking run over a set of root (seed) arXiv IDs.

    Options are explicit constructor parameters (the CLI entry translates
    argparse into these); call :meth:`run` with no arguments.
    """

    def __init__(
        self,
        *,
        seed_id: list[str] | None = None,
        direction: str = "both",
        top: int = 10,
        max_per_seed_per_direction: int = 500,
        weights: str = "citation=0.40,venue=0.25,author=0.20,code=0.15",
        author_strategy: str = "max-hindex",
        code_source: str = "abstract",
        min_year: int | None = None,
        require_terms: str | None = None,
        require_title_terms: str | None = None,
        must_terms: str | None = None,
        paper_id_file: list[str] | None = None,
        output: str | None = None,
        markdown_output: str | None = None,
        sleep_seconds: float = 1.0,
        timeout: float = 20.0,
        retries: int = MAX_RETRIES,
        retry_base_seconds: float = 5.0,
        retry_max_seconds: float = 60.0,
        fail_fast: bool = False,
        user_agent: str = "embodied-ai-literature-hub/1.0 (local research workflow)",
        api_key: str | None = None,
    ) -> None:
        self.seed_id = list(seed_id or [])
        self.direction = direction
        self.top = top
        self.max_per_seed_per_direction = max_per_seed_per_direction
        self.weights = weights
        self.author_strategy = author_strategy
        self.code_source = code_source
        self.min_year = min_year
        self.require_terms = require_terms
        self.require_title_terms = require_title_terms
        self.must_terms = must_terms
        self.paper_id_file = list(paper_id_file or [])
        self.output = output
        # Stored separately from the markdown_output() method to avoid shadowing it.
        self.markdown_path = markdown_output
        self.sleep_seconds = sleep_seconds
        self.timeout = timeout
        self.retries = retries
        self.retry_base_seconds = retry_base_seconds
        self.retry_max_seconds = retry_max_seconds
        self.fail_fast = fail_fast
        self.user_agent = user_agent
        self.api_key = api_key

    # -- request plumbing ---------------------------------------------------

    def request_options(self) -> dict[str, object]:
        return {
            "user_agent": self.user_agent,
            "api_key": self.api_key,
            "retries": self.retries,
            "retry_base_seconds": self.retry_base_seconds,
            "retry_max_seconds": self.retry_max_seconds,
            "timeout": self.timeout,
        }

    def fetch_json(self, url: str, data: bytes | None = None) -> dict:
        return fetch_json(url, data=data, **self.request_options())  # type: ignore[arg-type]

    # -- discovery ----------------------------------------------------------

    def discover_neighbors(self, seed_id: str, direction: str) -> tuple[list[dict], int]:
        """Walk the whole neighbor list via the `next` offset, up to the cap."""
        papers: list[dict] = []
        excluded = 0
        offset = 0
        limit = max(1, min(self.max_per_seed_per_direction, 1000))
        while len(papers) < self.max_per_seed_per_direction:
            payload = self.fetch_json(neighbor_url(seed_id, direction, offset, limit))
            data = payload.get("data") or []
            wrapper_key = "citedPaper" if direction == "references" else "citingPaper"
            for item in data:
                if not isinstance(item, dict):
                    excluded += 1
                    continue
                inner = item.get(wrapper_key)
                if not isinstance(inner, dict):
                    excluded += 1
                    continue
                arxiv_id = arxiv_id_of(inner)
                if not arxiv_id:
                    excluded += 1
                    continue
                authors = [a.get("name") for a in inner.get("authors") or [] if isinstance(a, dict) and a.get("name")]
                published = published_value(inner)
                papers.append(
                    {
                        "arxiv_id": arxiv_id,
                        "title": inner.get("title") or "",
                        "abstract": inner.get("abstract") or "",
                        "authors": authors,
                        "published": published,
                        "citation_count": inner.get("citationCount") or 0,
                        "venue": inner.get("venue") or "",
                        "direction": direction,
                        "connected_seeds": [seed_id],
                    }
                )
            next_offset = payload.get("next")
            if not data or next_offset is None or next_offset == offset:
                break
            offset = int(next_offset)
            if self.sleep_seconds > 0:
                time.sleep(self.sleep_seconds)
        return papers, excluded

    def batch_enrichment(self, arxiv_ids: list[str]) -> dict[str, dict]:
        """Fetch full metadata (title/abstract/year/citationCount/venue/authors+hIndex) for many
        arXiv IDs in one batch call (chunked at 500). Used both to add author h-index to
        discovered neighbors and to build full records for pre-discovered ``--paper-id-file`` IDs."""
        out: dict[str, dict] = {}
        unique = sorted({i for i in arxiv_ids if i})
        for start in range(0, len(unique), BATCH_MAX_IDS):
            chunk = unique[start : start + BATCH_MAX_IDS]
            ids = [f"ARXIV:{i}" for i in chunk]
            url = f"{API_BASE}/paper/batch?fields=" + urllib.parse.quote(ENRICH_FIELDS)
            payload = self.fetch_json(url, data=json.dumps({"ids": ids}).encode("utf-8"))
            for paper in payload or []:
                if not isinstance(paper, dict):
                    continue
                arxiv_id = arxiv_id_of(paper)
                if not arxiv_id:
                    continue
                out[arxiv_id] = {
                    "title": paper.get("title") or "",
                    "abstract": paper.get("abstract") or "",
                    "published": published_value(paper),
                    "citation_count": paper.get("citationCount") or 0,
                    "venue": paper.get("venue") or "",
                    "authors": paper.get("authors") or [],
                }
            if self.sleep_seconds > 0 and start + BATCH_MAX_IDS < len(unique):
                time.sleep(self.sleep_seconds)
        return out

    # -- code availability --------------------------------------------------

    def pwc_repo_count(self, arxiv_id: str) -> tuple[int, bool]:
        """Return (num_repos, known). Unknown when PapersWithCode is unreachable/non-JSON."""
        return pwc_repo_count(arxiv_id, **self.request_options())  # type: ignore[arg-type]

    def code_score(self, source: str, arxiv_id: str, text: str) -> dict:
        if source == "none":
            return {"score": 0.5, "known": False, "note": "neutral (code-source none)"}
        if source == "pwc":
            num, known = self.pwc_repo_count(arxiv_id)
            if not known:
                return {"score": 0.5, "known": False, "note": "unknown (PapersWithCode unreachable)"}
            return {"score": 1.0 if num > 0 else 0.0, "known": True, "note": f"{num} repo(s)"}
        # abstract: confirm-only heuristic -- never penalizes an absent mention.
        if code_mention(text):
            return {"score": 1.0, "known": True, "note": "code mention in abstract/title"}
        return {"score": 0.5, "known": False, "note": "no mention (confirm-only)"}

    # -- scoring and ranking ------------------------------------------------

    def score_paper(self, paper: dict, weights: dict, max_velocity: float, author_map: dict) -> dict:
        arxiv_id = paper["arxiv_id"]
        citation = float(paper.get("citation_count") or 0)
        venue = classify_venue(paper.get("venue"))
        text = f"{paper.get('title', '')} {paper.get('abstract', '')}"

        enrich = author_map.get(arxiv_id, {})
        enriched_authors = enrich.get("authors") or []
        if not enriched_authors:
            enriched_authors = paper.get("authors") or []
        h_index, author_known = author_h_index(enriched_authors, self.author_strategy)

        def author_name(a: object) -> str:
            if isinstance(a, dict):
                return a.get("name") or ""
            return str(a or "")

        author_names = [author_name(a) for a in enriched_authors if author_name(a)]

        code = self.code_score(self.code_source, arxiv_id, text)

        velocity = citations_per_year(citation, paper.get("published"))

        sub = {
            # Citation is year-normalized: raw count / age, log-compressed. A 2015 paper with
            # 7000 citations had 10 years to earn them; velocity is the fair, age-aware signal.
            "citation": log_normalize(velocity, max_velocity),
            "venue": venue["score"],
            "author": log_normalize(h_index, 100.0) if author_known else 0.5,
            "code": code["score"],
        }
        composite = sum(weights.get(k, 0.0) * v for k, v in sub.items())
        composite = round(min(1.0, composite), 4)

        year = year_of(paper.get("published")) or 0

        flags = type_flags(paper.get("title", ""))

        return {
            "arxiv_id": arxiv_id,
            "title": paper.get("title") or "",
            "abstract": paper.get("abstract") or "",
            "authors": author_names,
            "published": paper.get("published", ""),
            "year": year,
            "venue": venue["venue"],
            "venue_canonical": venue["canonical"],
            "citation_count": int(citation),
            "citations_per_year": velocity,
            "author_h_index": round(h_index, 1),
            "author_known": author_known,
            "code_known": code["known"],
            "code_note": code["note"],
            "is_survey": flags["is_survey"],
            "is_dataset": flags["is_dataset"],
            "direction": paper.get("direction", ""),
            "connected_seeds": paper.get("connected_seeds", []),
            "sub_scores": {k: round(v, 4) for k, v in sub.items()},
            "composite_score": composite,
        }

    def rank_papers(self, papers: list[dict], weights: dict, author_map: dict, top: int) -> list[dict]:
        max_velocity = max((citations_per_year(float(p.get("citation_count") or 0), p.get("published")) for p in papers), default=0.0)
        scored = [self.score_paper(p, weights, max_velocity, author_map) for p in papers]
        scored.sort(key=lambda item: (-item["composite_score"], -item["citation_count"], item["arxiv_id"]))
        for rank, item in enumerate(scored[:top], start=1):
            item["rank"] = rank
        return scored[:top]

    # -- output shaping -----------------------------------------------------

    def build_output(self, seed_ids: list[str], seed_meta: dict, ranked: list[dict],
                     candidate_count: int, excluded_no_arxiv_id: int, filtered_count: int,
                     truncated_count: int, errors: list[dict]) -> dict:
        return {
            "generated_at": stable_now(),
            "method": "multi-dimensional influence ranking (citation/yr + venue + author + code)",
            "seeds": sorted(seed_ids),
            "seed_meta": seed_meta,
            "direction": self.direction,
            "weights": self.weights,
            "author_strategy": self.author_strategy,
            "code_source": self.code_source,
            "min_year": self.min_year,
            "require_terms": self.require_terms,
            "require_title_terms": self.require_title_terms,
            "must_terms": self.must_terms,
            "candidate_count": candidate_count,
            "top_count": len(ranked),
            "excluded_no_arxiv_id": excluded_no_arxiv_id,
            "filtered_count": filtered_count,
            "truncated_count": truncated_count,
            "errors": errors,
            "papers": ranked,
        }

    def markdown_output(self, seed_ids: list[str], ranked: list[dict]) -> str:
        weights = parse_weights(self.weights)
        method = (
            f"- Method: citation ({weights.get('citation', 0):.2f}, year-normalized = count/age) + "
            f"venue ({weights.get('venue', 0):.2f}) + author h-index ({weights.get('author', 0):.2f}) + "
            f"code ({weights.get('code', 0):.2f}), each normalized to [0,1]."
        )
        lines = [
            f"# Influence ranking: {', '.join(seed_ids)}",
            "",
            method,
            f"- Direction: {self.direction} · Author strategy: {self.author_strategy} · Code source: {self.code_source}.",
            f"- Composite = weighted sum of sub-scores. *Candidate-level only — not accepted evidence.*",
            "",
            "| # | arXiv | Title | Year | Venue | Cit. | Cit/yr | H-idx | Code | Composite | Dir |",
            "|---:|---|---|---:|---|---:|---:|---:|---:|---:|:--:|",
        ]
        for item in ranked:
            code_cell = ("✓" if item["code_known"] and item["sub_scores"]["code"] == 1.0
                         else ("—" if item["code_known"] else "?"))
            lines.append(
                f"| {item['rank']} | [{item['arxiv_id']}](https://arxiv.org/abs/{item['arxiv_id']}) "
                f"| {item['title']} | {item['year'] or '—'} | {item['venue_canonical']} "
                f"| {item['citation_count']} | {item['citations_per_year']} "
                f"| {item['author_h_index'] if item['author_known'] else '—'} "
                f"| {code_cell} | {item['composite_score']} | {item['direction'][:3]} |"
            )
        return "\n".join(lines) + "\n"

    # -- orchestration ------------------------------------------------------

    def run(self) -> int:
        seed_ids = sorted({normalize_arxiv_id(i) for i in self.seed_id if i})
        if not seed_ids:
            raise SystemExit("provide at least one --seed-id")

        directions = ["references", "citations"] if self.direction == "both" else [self.direction]
        papers: list[dict] = []
        excluded_no_arxiv_id = 0
        errors: list[dict] = []

        for seed_id in seed_ids:
            for direction in directions:
                try:
                    discovered, excluded = self.discover_neighbors(seed_id, direction)
                except Exception as exc:  # pragma: no cover - network dependent
                    if self.fail_fast:
                        raise
                    errors.append({"seed": seed_id, "direction": direction, "error": str(exc)})
                    discovered, excluded = [], 0
                excluded_no_arxiv_id += excluded
                papers.extend(discovered)
            if len(seed_ids) > 1 and self.sleep_seconds > 0:
                time.sleep(self.sleep_seconds)

        # Pre-discovered IDs (e.g. 2-hop expansion from expand_via_citations.py) enlarge the pool.
        # They carry only an arXiv id here; full metadata is filled by batch enrichment below.
        extra_ids: set[str] = set()
        for path in self.paper_id_file:
            try:
                extra_ids.update(
                    normalize_arxiv_id(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()
                )
            except OSError as exc:  # pragma: no cover - file handling
                errors.append({"phase": "paper-id-file", "file": path, "error": str(exc)})

        # Deduplicate by arXiv id, keeping the merged direction labels.
        by_id: dict[str, dict] = {}
        for p in papers:
            key = p["arxiv_id"]
            if key in seed_ids:
                continue
            existing = by_id.setdefault(key, dict(p))
            for field in ("title", "abstract", "published", "venue", "citation_count"):
                if not existing.get(field) and p.get(field):
                    existing[field] = p[field]
            if not existing.get("authors") and p.get("authors"):
                existing["authors"] = p["authors"]
            existing["connected_seeds"] = sorted(set(existing.get("connected_seeds", [])) | set(p.get("connected_seeds", [])))
            dirs = set(existing.get("direction", "").split(",")) | {p.get("direction", "")}
            existing["direction"] = ",".join(sorted(d for d in dirs if d))

        all_ids = sorted(set(by_id.keys()) | extra_ids)

        author_map: dict[str, dict] = {}
        try:
            if self.sleep_seconds > 0:
                time.sleep(self.sleep_seconds)
            author_map = self.batch_enrichment(all_ids)
        except Exception as exc:  # pragma: no cover - network dependent
            if self.fail_fast:
                raise
            errors.append({"phase": "enrichment", "error": str(exc)})

        # Build candidate records: discovered papers keep their own metadata, enriched with
        # author h-index; pre-discovered IDs are reconstructed entirely from batch metadata.
        extra_missing = 0
        for arxiv_id in extra_ids:
            if arxiv_id in by_id or arxiv_id in seed_ids:
                continue
            meta = author_map.get(arxiv_id, {})
            if not meta.get("title"):
                extra_missing += 1  # not in Semantic Scholar / failed enrich — reported, not silently dropped
                continue
            by_id[arxiv_id] = {
                "arxiv_id": arxiv_id,
                "title": meta.get("title", ""),
                "abstract": meta.get("abstract", ""),
                "authors": meta.get("authors", []),
                "published": meta.get("published", ""),
                "citation_count": meta.get("citation_count", 0),
                "venue": meta.get("venue", ""),
                "direction": "citation-expansion",
                "connected_seeds": [],
            }

        candidates = list(by_id.values())

        # Apply the field/time scope to the combined pool (1-hop + pre-discovered), so every
        # candidate is gated identically regardless of how it entered the pool.
        candidates, filtered_out = filter_papers(candidates, self.min_year, self.require_terms, self.require_title_terms, self.must_terms)

        weights = parse_weights(self.weights)
        ranked = self.rank_papers(candidates, weights, author_map, self.top)
        truncated_count = max(0, len(candidates) - self.top)

        seed_meta: dict = {}
        try:
            url = f"{API_BASE}/paper/ARXIV:{seed_ids[0]}?fields=" + urllib.parse.quote("title,year,citationCount,venue")
            seed_meta = self.fetch_json(url)
        except Exception as exc:  # pragma: no cover
            errors.append({"phase": "seed-meta", "error": str(exc)})

        output = self.build_output(seed_ids, seed_meta, ranked, len(candidates), excluded_no_arxiv_id, filtered_out, truncated_count, errors)
        write_json(self.output, output)
        if self.markdown_path:
            write_text(self.markdown_path, self.markdown_output(seed_ids, ranked))

        print(
            f"influence ranking from {len(seed_ids)} seed(s): {len(candidates)} candidates, "
            f"top {len(ranked)} emitted, {excluded_no_arxiv_id} excluded (no arXiv id), "
            f"{filtered_out} filtered (min-year / require-terms), "
            f"{extra_missing} extra IDs unenriched, "
            f"{truncated_count} below top, {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 0


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_arxiv_id(value: object) -> str:
    raw = str(value or "").rsplit("/", 1)[-1].removesuffix(".pdf").removesuffix(".html")
    return re.sub(r"v\d+$", "", raw.strip())


def arxiv_id_of(paper: dict) -> str:
    """Return the normalized arXiv ID from a Semantic Scholar paper record, or ""."""
    external_ids = paper.get("externalIds") or {}
    arxiv_raw = external_ids.get("ArXiv") if isinstance(external_ids, dict) else None
    return normalize_arxiv_id(arxiv_raw) if arxiv_raw else ""


def published_value(paper: dict) -> str:
    """Prefer publicationDate, else fall back to the year field."""
    return paper.get("publicationDate") or (str(paper["year"]) if paper.get("year") else "")


def parse_weights(raw: str) -> dict[str, float]:
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
    total = sum(weights.values())
    if total <= 0:
        return {"citation": 0.40, "venue": 0.25, "author": 0.20, "code": 0.15}
    if abs(total - 1.0) > 1e-6:
        weights = {k: v / total for k, v in weights.items()}
    return weights


# ---------------------------------------------------------------------------
# Venue classification
# ---------------------------------------------------------------------------


def classify_venue(venue: object) -> dict:
    """Map a Semantic Scholar venue string to (canonical, score)."""
    text = (venue or "").strip()
    if not text:
        return {"venue": "", "canonical": "preprint", "score": 0.0}
    lowered = re.sub(r"\s+", " ", text.lower())
    for needle, canonical, score in VENUE_RULES:
        if needle in lowered:
            return {"venue": text, "canonical": canonical, "score": score}
    return {"venue": text, "canonical": "unknown", "score": 0.5}


def log_normalize(value: float, max_value: float) -> float:
    if max_value <= 0:
        return 0.0
    return min(1.0, math.log1p(max(0.0, float(value))) / math.log1p(max(0.0, float(max_value))))


def author_h_index(authors: list[dict], strategy: str) -> tuple[float, bool]:
    """Return (h-index, known). Authors lacking an hIndex are skipped."""
    values = []
    for a in authors or []:
        if not isinstance(a, dict):
            continue
        h = a.get("hIndex")
        if isinstance(h, (int, float)) and h is not None:
            values.append(float(h))
    if not values:
        return 0.0, False
    if strategy == "first-author":
        chosen = values[0]
    else:
        chosen = max(values)
    return chosen, True


def code_mention(text: str) -> bool:
    return bool(CODE_MENTION_RE.search(text or ""))


def type_flags(title: str) -> dict:
    title = title or ""
    return {
        "is_survey": bool(_SURVEY_RE.search(title)),
        "is_dataset": bool(_DATASET_RE.search(title)),
    }


def year_of(published: object) -> int | None:
    text = str(published or "").strip()
    match = re.match(r"(\d{4})", text)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def citations_per_year(citation: float, published: object) -> float:
    """Time-normalized citation velocity: raw count / age. Older papers have had more
    time to accumulate citations, so raw count alone over-credits them; velocity is the
    year-aware signal the ranking uses."""
    year = year_of(published)
    if not year:
        return 0.0
    age = max(1, dt.date.today().year - year)
    return round(float(citation) / age, 1)


def filter_papers(
    papers: list[dict],
    min_year: int | None,
    require_terms: str | None,
    require_title_terms: str | None = None,
    must_terms: str | None = None,
) -> tuple[list[dict], int]:
    """Drop neighbors below a publication-year floor and/or outside a topical term set.

    ``require_terms`` matches against title+abstract (recall-oriented);
    ``require_title_terms`` matches against the title only (precision-oriented field gate);
    ``must_terms`` is a hard AND-gate: a paper is dropped unless at least one must-term
    appears in title+abstract (e.g. the third-person/exo side must be present).
    Unknown-year papers are kept (a citing paper already post-dates its cited seed, so
    dropping them would silently discard valid downstream work). Returns (kept, dropped).
    """
    terms = [t.strip().lower() for t in (require_terms or "").split(",") if t.strip()]
    title_terms = [t.strip().lower() for t in (require_title_terms or "").split(",") if t.strip()]
    must = [t.strip().lower() for t in (must_terms or "").split(",") if t.strip()]
    need_text = bool(must or terms)
    kept: list[dict] = []
    dropped = 0
    for paper in papers:
        year = year_of(paper.get("published"))
        if min_year is not None and year is not None and year < min_year:
            dropped += 1
            continue
        if title_terms:
            title = (paper.get("title") or "").lower()
            if not any(term in title for term in title_terms):
                dropped += 1
                continue
        if need_text:
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
            if must and not any(term in text for term in must):
                dropped += 1
                continue
            if terms and not any(term in text for term in terms):
                dropped += 1
                continue
        kept.append(paper)
    return kept, dropped


# ---------------------------------------------------------------------------
# Network: retry/backoff copied from search_arxiv.py (explicit params, no
# option object -- the class methods pass their own values in)
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


def retry_wait_seconds(exc: Exception, attempt: int, retry_base_seconds: float, retry_max_seconds: float) -> float:
    retry_after = retry_after_seconds(exc)
    if retry_after is not None:
        return max(0.0, min(retry_after, retry_max_seconds))
    return max(0.0, min(retry_base_seconds * (2**attempt), retry_max_seconds))


def _request(
    url: str,
    *,
    user_agent: str,
    api_key: str | None = None,
    retries: int = MAX_RETRIES,
    retry_base_seconds: float = 5.0,
    retry_max_seconds: float = 60.0,
    timeout: float = 20.0,
    data: bytes | None = None,
) -> bytes:
    headers = {"User-Agent": user_agent}
    if data is not None:
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
    if api_key:
        headers["x-api-key"] = api_key
    request = urllib.request.Request(url, data=data, headers=headers)
    last_error: Exception | None = None
    attempts = 0
    capped_retries = bounded_retries(retries)
    for attempt in range(capped_retries + 1):
        attempts = attempt + 1
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except Exception as exc:  # pragma: no cover - network dependent
            last_error = exc
            if attempt < capped_retries and is_retryable(exc):
                time.sleep(retry_wait_seconds(exc, attempt, retry_base_seconds, retry_max_seconds))
                continue
            break
    raise RuntimeError(f"request to {url} failed after {attempts} attempt(s): {last_error}") from last_error


def fetch_json(
    url: str,
    *,
    user_agent: str,
    api_key: str | None = None,
    retries: int = MAX_RETRIES,
    retry_base_seconds: float = 5.0,
    retry_max_seconds: float = 60.0,
    timeout: float = 20.0,
    data: bytes | None = None,
) -> dict:
    raw = _request(
        url,
        user_agent=user_agent,
        api_key=api_key,
        retries=retries,
        retry_base_seconds=retry_base_seconds,
        retry_max_seconds=retry_max_seconds,
        timeout=timeout,
        data=data,
    )
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:  # pragma: no cover - data dependent
        raise RuntimeError(f"non-JSON response from {url}") from exc


# ---------------------------------------------------------------------------
# Discovery URL
# ---------------------------------------------------------------------------


def neighbor_url(seed_id: str, direction: str, offset: int, limit: int) -> str:
    endpoint = "references" if direction == "references" else "citations"
    params = {"fields": NEIGHBOR_FIELDS, "limit": str(max(1, min(limit, 1000))), "offset": str(max(0, offset))}
    return f"{API_BASE}/paper/ARXIV:{seed_id}/{endpoint}?" + urllib.parse.urlencode(params)


# ---------------------------------------------------------------------------
# Code availability (module-level so tests can patch it; the class method
# forwards its own request options)
# ---------------------------------------------------------------------------


def pwc_repo_count(
    arxiv_id: str,
    *,
    user_agent: str,
    api_key: str | None = None,
    retries: int = MAX_RETRIES,
    retry_base_seconds: float = 5.0,
    retry_max_seconds: float = 60.0,
    timeout: float = 20.0,
) -> tuple[int, bool]:
    """Return (num_repos, known). Unknown when PapersWithCode is unreachable/non-JSON."""
    url = PWC_BASE + "?" + urllib.parse.urlencode({"arxiv_id": arxiv_id})
    options = dict(
        user_agent=user_agent,
        api_key=api_key,
        retries=retries,
        retry_base_seconds=retry_base_seconds,
        retry_max_seconds=retry_max_seconds,
        timeout=timeout,
    )
    try:
        payload = fetch_json(url, **options)
    except Exception:  # pragma: no cover - network dependent
        return 0, False
    results = payload.get("results") or []
    if not results:
        return 0, True
    first = results[0] if isinstance(results[0], dict) else {}
    num = first.get("num_repositories")
    if isinstance(num, (int, float)):
        return int(num), True
    # Fall back to a repository relation URL, if present.
    repo_url = first.get("repositories")
    if isinstance(repo_url, str) and repo_url:
        try:
            repo_payload = fetch_json(repo_url, **options)
        except Exception:  # pragma: no cover
            return 0, False
        return int(repo_payload.get("count") or len(repo_payload.get("results") or [])), True
    return 0, False


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------


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

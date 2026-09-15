#!/usr/bin/env python3
"""search-layer CLI: one entry, one subcommand per tool.

Each subcommand owns its original flags (per-subcommand parsers, so legacy
flag names never collide); implementation lives in the embodied_learning
search layer. Subcommand names are the old single-purpose scripts
kebab-cased: `build-query-plan` was `scripts/build_query_plan.py`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# ---- build-query-plan (was scripts/build_query_plan.py) ------------------------


import argparse
import json
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from embodied_learning.search.query_plan import (  # noqa: E402
    DEFAULT_MAX_QUERIES,
    FAMILY_PLANS,
    REVIEW_MODES,
    TOPIC_PLANS,
    build_plan,
    render_markdown,
)


def _build_query_plan_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=False, help="Chinese or English embodied-AI topic.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="EA knowledge ID. May be repeated.")
    parser.add_argument("--family", action="append", default=[], help="Specialized query family. May be repeated.")
    parser.add_argument("--start-date", help="Optional YYYY-MM-DD scope metadata.")
    parser.add_argument("--end-date", help="Optional YYYY-MM-DD scope metadata.")
    parser.add_argument("--dynamic-file", action="append", default=[], help="JSON file with LLM/agent dynamic query suggestions. May be repeated.")
    parser.add_argument("--calibration-file", action="append", default=[], help="JSON calibration file. May be repeated.")
    parser.add_argument(
        "--review-mode",
        choices=sorted(REVIEW_MODES),
        default="scoping",
        help="Search-depth contract. Targets are floors, never caps.",
    )
    parser.add_argument("--target-candidates", type=int, help="Override the mode's candidate floor.")
    parser.add_argument("--target-full-text", type=int, help="Override the mode's full-text screening floor.")
    parser.add_argument("--target-evidence", type=int, help="Override the mode's accepted-paper floor.")
    parser.add_argument("--max-queries", type=int, default=DEFAULT_MAX_QUERIES, help="Max arXiv API query entries.")
    parser.add_argument("--output", help="Write JSON plan to this path instead of stdout.")
    parser.add_argument("--markdown-output", help="Write a Markdown review view to this path.")
    parser.add_argument("--list-topics", action="store_true", help="List supported EA topic IDs and exit.")
    parser.add_argument("--list-families", action="store_true", help="List supported specialized families and exit.")
    return parser.parse_args(argv)


def list_and_exit(items: dict[str, Any]) -> int:
    for key in sorted(items):
        print(key)
    return 0


def _build_query_plan_main(argv: list[str] | None = None) -> int:
    args = _build_query_plan_parse_args(argv)
    if args.list_topics:
        return list_and_exit(TOPIC_PLANS)
    if args.list_families:
        return list_and_exit(FAMILY_PLANS)
    if not args.topic:
        raise SystemExit("--topic is required unless --list-topics or --list-families is used.")
    plan = build_plan(
        args.topic,
        knowledge_id=args.knowledge_id,
        family=args.family,
        start_date=args.start_date,
        end_date=args.end_date,
        dynamic_file=args.dynamic_file,
        calibration_file=args.calibration_file,
        review_mode=args.review_mode,
        target_candidates=args.target_candidates,
        target_full_text=args.target_full_text,
        target_evidence=args.target_evidence,
        max_queries=args.max_queries,
    )
    rendered = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if args.markdown_output:
        Path(args.markdown_output).write_text(render_markdown(plan), encoding="utf-8")
    return 0

# ---- search-arxiv (was scripts/search_arxiv.py) ----------------------------

import argparse

from embodied_learning.search.arxiv import MAX_RETRIES, ArxivSearch, load_queries  # noqa: E402


def _search_arxiv_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", action="append", help="Raw arXiv search_query string. May be repeated.")
    parser.add_argument("--query-file", help="JSON file with {'queries': [{'label': str, 'query': str}]}.")
    parser.add_argument("--start-date", required=True, help="Inclusive YYYY-MM-DD submitted date.")
    parser.add_argument("--end-date", required=True, help="Inclusive YYYY-MM-DD submitted date.")
    parser.add_argument("--max-results", type=int, default=25, help="Results per query for this discovery batch.")
    parser.add_argument("--batch-label", help="Stable round label stored for candidate-registry saturation analysis.")
    parser.add_argument("--sort-by", default="submittedDate", choices=["relevance", "lastUpdatedDate", "submittedDate"])
    parser.add_argument("--sort-order", default="descending", choices=["ascending", "descending"])
    parser.add_argument("--sleep-seconds", type=float, default=3.0, help="Delay between multiple API requests.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per query after transient failures. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0, help="Base wait before retrying transient failures.")
    parser.add_argument("--retry-max-seconds", type=float, default=60.0, help="Maximum wait before a single retry.")
    parser.add_argument("--fail-fast", action="store_true", help="Abort on the first failed query.")
    parser.add_argument(
        "--user-agent",
        default="embodied-ai-literature-hub/1.0 (local research workflow)",
        help="HTTP User-Agent sent to arXiv.",
    )
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def _search_arxiv_main(argv: list[str] | None = None) -> int:
    args = _search_arxiv_parse_args(argv)
    search = ArxivSearch(
        start_date=args.start_date,
        end_date=args.end_date,
        max_results=args.max_results,
        batch_label=args.batch_label or "",
        sort_by=args.sort_by,
        sort_order=args.sort_order,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        user_agent=args.user_agent,
        output=args.output,
    )
    return search.run(load_queries(queries=args.query, query_file=args.query_file))

# ---- search-semantic-scholar (was scripts/search_semantic_scholar.py) -----------------

import argparse

from embodied_learning.search.semantic_scholar import DEFAULT_CACHE_DIR, MAX_RETRIES, SemanticScholarSearch, load_queries  # noqa: E402


def _search_semantic_scholar_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", action="append", help="Search query string. May be repeated.")
    parser.add_argument("--query-file",
                        help="JSON file with {'queries': [{'label': str, 'query': str}]}, the planner contract.")
    parser.add_argument("--start-date", required=True, help="Inclusive YYYY-MM-DD publication date.")
    parser.add_argument("--end-date", required=True, help="Inclusive YYYY-MM-DD publication date.")
    parser.add_argument("--max-results", type=int, default=25, help="Results per query for this discovery batch.")
    parser.add_argument("--batch-label", help="Stable round label stored for candidate-registry saturation analysis.")
    parser.add_argument("--sort-by", default="relevance", choices=["relevance", "pub_date"],
                        help="relevance uses S2 ordering; pub_date sorts client-side after fetch.")
    parser.add_argument("--sort-order", default="descending", choices=["ascending", "descending"],
                        help="Only applied with --sort-by pub_date.")
    parser.add_argument("--sleep-seconds", type=float, default=0.1,
                        help="Delay between queries; the S2 pool tolerates small intervals.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request after transient failures. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0, help="Base wait before retrying transient failures.")
    parser.add_argument("--retry-max-seconds", type=float, default=60.0, help="Maximum wait before a single retry.")
    parser.add_argument("--fail-fast", action="store_true", help="Abort on the first failed query.")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to the S2_API_KEY env var.")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR,
                        help="Response cache (shared with expand_via_citations.py).")
    parser.add_argument("--no-cache", action="store_true", help="Bypass the response cache for reads and writes.")
    parser.add_argument("--user-agent",
                        default="embodied-ai-literature-hub/1.0 (local research workflow)",
                        help="HTTP User-Agent sent to Semantic Scholar.")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def _search_semantic_scholar_main(argv: list[str] | None = None) -> int:
    args = _search_semantic_scholar_parse_args(argv)
    search = SemanticScholarSearch(
        start_date=args.start_date,
        end_date=args.end_date,
        max_results=args.max_results,
        batch_label=args.batch_label or "",
        sort_by=args.sort_by,
        sort_order=args.sort_order,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        api_key=args.api_key,
        cache_dir=args.cache_dir,
        no_cache=args.no_cache,
        user_agent=args.user_agent,
        output=args.output,
    )
    return search.run(load_queries(queries=args.query, query_file=args.query_file))

# ---- expand-via-citations (was scripts/expand_via_citations.py) --------------------


import argparse
import os

from embodied_learning.search.citation_expansion import DEFAULT_S2_CACHE_DIR, MAX_RETRIES, CitationExpansion  # noqa: E402


def _expand_via_citations_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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
    parser.add_argument("--sleep-seconds", type=float, default=0.1, help="Delay between seeds.")
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
    parser.add_argument(
        "--cache-dir",
        default=DEFAULT_S2_CACHE_DIR,
        help="Semantic Scholar response cache, shared with search_semantic_scholar.py.",
    )
    parser.add_argument("--no-cache", action="store_true", help="Bypass the response cache for reads and writes.")
    return parser.parse_args(argv)


def _expand_via_citations_main(argv: list[str] | None = None) -> int:
    args = _expand_via_citations_parse_args(argv)
    expansion = CitationExpansion(
        seed_id=args.seed_id,
        seed_id_file=args.seed_id_file,
        seed_registry=args.seed_registry,
        seed_status=args.seed_status,
        direction=args.direction,
        max_per_seed_per_direction=args.max_per_seed_per_direction,
        min_shared_seeds=args.min_shared_seeds,
        max_total_candidates=args.max_total_candidates,
        include_below_threshold_output=args.include_below_threshold_output,
        start_date=args.start_date,
        end_date=args.end_date,
        top_terms=args.top_terms,
        min_doc_frequency=args.min_doc_frequency,
        extra_stopwords_file=args.extra_stopwords_file,
        batch_label=args.batch_label,
        output=args.output,
        graph_output=args.graph_output,
        dynamic_output=args.dynamic_output,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        user_agent=args.user_agent,
        api_key=args.api_key or os.environ.get("S2_API_KEY"),
        cache_dir=args.cache_dir,
        no_cache=args.no_cache,
    )
    return expansion.run()

# ---- build-candidate-registry (was scripts/build_candidate_registry.py) ----------------


import argparse

from embodied_learning.search.candidate_registry import run  # noqa: E402


def _build_candidate_registry_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search-result", action="append", default=[], help="search_arxiv.py JSON; repeat by round.")
    parser.add_argument(
        "--semantic-scholar-result",
        action="append",
        default=[],
        help="search_semantic_scholar.py JSON; repeat by round.",
    )
    parser.add_argument("--browser-result", action="append", default=[], help="parse_browser_candidates.py JSON; repeatable.")
    parser.add_argument("--citation-result", action="append", default=[], help="expand_via_citations.py JSON; repeatable.")
    parser.add_argument("--screening-file", help="Optional JSON candidate/status updates.")
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def _build_candidate_registry_main(argv: list[str] | None = None) -> int:
    args = _build_candidate_registry_parse_args(argv)
    return run(
        [Path(path) for path in args.search_result],
        [Path(path) for path in args.browser_result],
        [Path(path) for path in args.citation_result],
        [Path(path) for path in args.semantic_scholar_result],
        Path(args.screening_file) if args.screening_file else None,
        Path(args.output),
    )

# ---- screen-candidates (was scripts/screen_candidates.py) -----------------------


import argparse

from embodied_learning.search.screening import run  # noqa: E402


def _screen_candidates_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-registry", required=True)
    parser.add_argument("--terms", required=True, help="Comma-separated title/abstract relevance terms.")
    parser.add_argument("--query-label-prefix", action="append", default=[], help="Prefer discoveries whose query label starts with this prefix.")
    parser.add_argument("--seed-evidence-jsonl", action="append", default=[], help="Previously accepted evidence used only as a priority seed.")
    parser.add_argument("--limit", type=int, default=40, help="Number of candidates to queue for full-text recovery.")
    parser.add_argument("--output-screening", required=True)
    parser.add_argument("--output-ids", required=True)
    parser.add_argument("--output-markdown")
    return parser.parse_args(argv)


def _screen_candidates_main(argv: list[str] | None = None) -> int:
    args = _screen_candidates_parse_args(argv)
    return run(
        candidate_registry=args.candidate_registry,
        terms_raw=args.terms,
        query_label_prefixes=args.query_label_prefix,
        seed_evidence_jsonl=args.seed_evidence_jsonl,
        limit=args.limit,
        output_screening=args.output_screening,
        output_ids=args.output_ids,
        output_markdown=args.output_markdown,
    )

# ---- assess-review-coverage (was scripts/assess_review_coverage.py) ------------------


import argparse

from embodied_learning.search.coverage import run  # noqa: E402


def _assess_review_coverage_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-plan", required=True)
    parser.add_argument("--candidate-registry", required=True)
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Accepted evidence; repeatable.")
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def _assess_review_coverage_main(argv: list[str] | None = None) -> int:
    args = _assess_review_coverage_parse_args(argv)
    return run(
        Path(args.query_plan),
        Path(args.candidate_registry),
        [Path(path) for path in args.evidence_jsonl],
        Path(args.output),
    )

# ---- rank-influential-papers (was scripts/rank_influential_papers.py) -----------------


import argparse
import os

from embodied_learning.search.influence import MAX_RETRIES, InfluenceRanking  # noqa: E402


def _rank_influential_papers_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-id", action="append", default=[], help="Root arXiv ID. May be repeated.")
    parser.add_argument("--direction", choices=["references", "citations", "both"], default="both")
    parser.add_argument("--top", type=int, default=10, help="Number of ranked papers to emit.")
    parser.add_argument("--max-per-seed-per-direction", type=int, default=500, help="Neighbor cap per direction (pagination walks the whole list up to this).")
    parser.add_argument(
        "--weights",
        default="citation=0.40,venue=0.25,author=0.20,code=0.15",
        help="Comma-separated dimension=weight. Normalized to sum 1 if not already.",
    )
    parser.add_argument("--author-strategy", choices=["max-hindex", "first-author"], default="max-hindex")
    parser.add_argument("--code-source", choices=["pwc", "abstract", "none"], default="abstract",
                        help="How to detect code availability. 'abstract' is a confirm-only heuristic; 'pwc' hits PapersWithCode; 'none' is neutral.")
    parser.add_argument("--min-year", type=int, default=None,
                        help="Drop neighbors published before this year (inclusive). Unknown-year papers are kept, not dropped.")
    parser.add_argument("--require-terms", default=None,
                        help="Comma-separated terms; keep a neighbor only if at least one term appears (case-insensitive) in its title+abstract.")
    parser.add_argument("--require-title-terms", default=None,
                        help="Comma-separated terms; keep a neighbor only if at least one term appears (case-insensitive) in its TITLE. Tighter field gate than --require-terms.")
    parser.add_argument("--must-terms", default=None,
                        help="Comma-separated terms; a paper is DROPPED unless at least one appears (case-insensitive) in title+abstract. A hard AND-gate on top of --require-terms/--require-title-terms (e.g. require the third-person/exo side).")
    parser.add_argument("--paper-id-file", action="append", default=[],
                        help="File of extra arXiv IDs (one per line) to add to the candidate pool and enrich via the batch endpoint. Repeatable. Use with expand_via_citations.py output to enlarge the pool (e.g. 2-hop downstream).")
    parser.add_argument("--output", help="Ranked JSON. Defaults to stdout.")
    parser.add_argument("--markdown-output", help="Ranking table Markdown.")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Delay between network phases.")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=MAX_RETRIES, help="Retries per request. Capped at 3.")
    parser.add_argument("--retry-base-seconds", type=float, default=5.0)
    parser.add_argument("--retry-max-seconds", type=float, default=60.0)
    parser.add_argument("--fail-fast", action="store_true", help="Abort on first failed request.")
    parser.add_argument("--user-agent", default="embodied-ai-literature-hub/1.0 (local research workflow)")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to S2_API_KEY env var.")
    return parser.parse_args(argv)


def _rank_influential_papers_main(argv: list[str] | None = None) -> int:
    args = _rank_influential_papers_parse_args(argv)
    ranking = InfluenceRanking(
        seed_id=args.seed_id,
        direction=args.direction,
        top=args.top,
        max_per_seed_per_direction=args.max_per_seed_per_direction,
        weights=args.weights,
        author_strategy=args.author_strategy,
        code_source=args.code_source,
        min_year=args.min_year,
        require_terms=args.require_terms,
        require_title_terms=args.require_title_terms,
        must_terms=args.must_terms,
        paper_id_file=args.paper_id_file,
        output=args.output,
        markdown_output=args.markdown_output,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        user_agent=args.user_agent,
        api_key=args.api_key or os.environ.get("S2_API_KEY"),
    )
    return ranking.run()

# ---- rank-problem-relevance (was scripts/rank_problem_relevance.py) ------------------


import argparse
import os

from embodied_learning.search.problem_relevance import (  # noqa: E402
    DEFAULT_CACHE_DIR,
    DEFAULT_FIELD_WEIGHTS,
    MAX_RETRIES,
    ProblemRelevanceRetrieval,
)


def _rank_problem_relevance_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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
    parser.add_argument("--user-agent", default="embodied-ai-literature-hub/1.0 (local research workflow)")
    parser.add_argument("--api-key", default=None, help="Semantic Scholar API key. Falls back to S2_API_KEY env var.")
    return parser.parse_args(argv)


def _rank_problem_relevance_main(argv: list[str] | None = None) -> int:
    args = _rank_problem_relevance_parse_args(argv)
    retrieval = ProblemRelevanceRetrieval(
        question=args.question,
        seed_id=args.seed_id,
        seed_id_file=args.seed_id_file,
        seed_registry=args.seed_registry,
        seed_status=args.seed_status,
        exclude_id_file=args.exclude_id_file,
        rounds=args.rounds,
        direction=args.direction,
        max_per_seed_per_direction=args.max_per_seed_per_direction,
        min_shared_seeds=args.min_shared_seeds,
        max_total_candidates=args.max_total_candidates,
        top_k_per_round=args.top_k_per_round,
        max_fulltext_per_round=args.max_fulltext_per_round,
        target_retrieved=args.target_retrieved,
        min_year=args.min_year,
        require_terms=args.require_terms,
        must_terms=args.must_terms,
        field_weights=args.field_weights,
        output=args.output,
        markdown_output=args.markdown_output,
        sleep_seconds=args.sleep_seconds,
        timeout=args.timeout,
        retries=args.retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        fail_fast=args.fail_fast,
        cache_dir=args.cache_dir,
        user_agent=args.user_agent,
        api_key=args.api_key or os.environ.get("S2_API_KEY"),
    )
    return retrieval.run()

# ---- parse-browser-candidates (was scripts/parse_browser_candidates.py) ----------------


import argparse

from embodied_learning.search.browser_candidates import build_output, read_input  # noqa: E402


def _parse_browser_candidates_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Browser-exported JSON, HTML, text, or '-' for stdin.")
    parser.add_argument("--start-date", help="Inclusive YYYY-MM-DD filter.")
    parser.add_argument("--end-date", help="Inclusive YYYY-MM-DD filter.")
    parser.add_argument("--source-label", default="browser-fallback")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout.")
    return parser.parse_args(argv)


def _parse_browser_candidates_main(argv: list[str] | None = None) -> int:
    import json

    args = _parse_browser_candidates_parse_args(argv)
    payload = read_input(args.input)
    output = build_output(
        payload,
        source_label=args.source_label,
        source_url=args.source_url,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0



_SUBCOMMANDS = {
    "build-query-plan": _build_query_plan_main,
    "search-arxiv": _search_arxiv_main,
    "search-semantic-scholar": _search_semantic_scholar_main,
    "expand-via-citations": _expand_via_citations_main,
    "build-candidate-registry": _build_candidate_registry_main,
    "screen-candidates": _screen_candidates_main,
    "assess-review-coverage": _assess_review_coverage_main,
    "rank-influential-papers": _rank_influential_papers_main,
    "rank-problem-relevance": _rank_problem_relevance_main,
    "parse-browser-candidates": _parse_browser_candidates_main,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch to the tool's own parser: `{layer}.py <subcommand> [flags...]`.

    Each subcommand reuses its original single-purpose parser verbatim, so
    flags, help text, and exit codes are unchanged from the old scripts.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 0
    handler = _SUBCOMMANDS.get(argv[0])
    if handler is None:
        print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 2
    return handler(argv[1:])


if __name__ == "__main__":
    sys.exit(main())

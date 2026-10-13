"""Query-file / CLI-query merging for the search backends.

One implementation of ``load_queries`` (was duplicated in arxiv.py and
semantic_scholar.py). Planner contract: the query file's top-level ``queries``
entries come first (keeping their labels); repeated ``--query`` values follow
as raw strings normalized to ``{"label": "query-N", "query": ...}`` dicts so
``run()`` can index ``item["query"]``.
"""

from __future__ import annotations

import json


def load_queries(queries: list[str] | None = None, query_file: str | None = None) -> list[dict[str, str]]:
    """Merge query-file entries with repeated --query values (CLI-side helper)."""
    queries = list(queries or [])
    if query_file:
        with open(query_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        existing = queries
        queries = []
        for index, item in enumerate(data.get("queries", []), start=1):
            query = item.get("query")
            if query:
                queries.append({"label": item.get("label", f"query-{index}"), "query": query})
        queries.extend(existing)
    # Repeated --query values arrive as raw strings; normalize them to the
    # planner contract shape so run() can index item["query"].
    queries = [
        item if isinstance(item, dict) else {"label": f"query-{index}", "query": item}
        for index, item in enumerate(queries, start=1)
    ]
    if not queries:
        raise SystemExit("Provide --query or --query-file.")
    return queries

#!/usr/bin/env python3
"""SQLite/FTS5 backend for offline arXiv metadata retrieval.

Converts the OAI snapshot JSONL (see :mod:`embodied_learning.search.arxiv_snapshot`)
into a local SQLite database — one-time cost — so every later retrieval round is
SQL-backed instead of a full 5 GB re-scan. Uses only the stdlib ``sqlite3``
module; FTS5 ships with CPython on CPython's Linux/Windows/macOS builds.

Schema:
    papers(id TEXT PRIMARY KEY, rowid-map via INTEGER PRIMARY KEY, title,
           abstract, authors, comments, journal_ref, categories,
           v1_date INTEGER, update_date, authors_parsed)
    fts(title, abstract, authors, comments, journal_ref, categories, id UNINDEXED)
with ``content='papers'`` (external content) and ``fts.rowid == papers.rowid``:
the FTS virtual table stores only the inverted index, and column values are
read live from ``papers`` by column name — the full text lives exactly once,
so the database is roughly half the size of the naive layout while the query
path (index scan + ``papers`` rowid lookup) is unchanged.

Queries run on a small thread pool: each query is an independent read-only
SELECT, ``sqlite3`` releases the GIL while executing, and SQLite tolerates
concurrent readers, so batch wall-clock is the slowest query, not the sum.

Query translation reuses the arXiv-syntax parser from
:mod:`embodied_learning.search.arxiv_snapshot`; nodes map onto FTS5 ``MATCH``
expressions (terms → column-scoped prefix, phrases → quoted token phrases,
AND/OR/ANDNOT pass through). ``submittedDate`` ranges become ``v1_date``
BETWEEN filters and are only supported in conjunctive position (which is how
``with_date_filter`` wraps every query).
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sqlite3
import time
from pathlib import Path
from typing import Any

from embodied_learning.search.arxiv_snapshot import (
    BinaryNode,
    DateRangeNode,
    PhraseNode,
    TermNode,
    parse_query,
    record_to_paper,
    submitted_date,
)

FTS_COLUMNS = {
    # "all" spans every searchable column (id is UNINDEXED, same as before).
    "all": "{title abstract authors comments journal_ref categories}",
    "ti": "title",
    "abs": "abstract",
    "au": "authors",
    "co": "comments",
    "jr": "journal_ref",
    "cat": "categories",
    "id": "id",
}


# ---- one-time conversion ----------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    rowid_alias INTEGER PRIMARY KEY,
    id TEXT NOT NULL UNIQUE,
    title TEXT, abstract TEXT, authors TEXT, comments TEXT,
    journal_ref TEXT, categories TEXT,
    v1_date INTEGER, update_date TEXT, authors_parsed TEXT
);
CREATE INDEX IF NOT EXISTS papers_v1_date ON papers(v1_date);
-- External content: only the inverted index lives here; values are read from
-- ``papers`` by column name at query time. ``rebuild`` builds the index from
-- the content table after the paper rows are inserted.
CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(
    title, abstract, authors, comments, journal_ref, categories,
    id UNINDEXED,
    content='papers', content_rowid='rowid_alias'
);
"""


def build_db(jsonl_path: str, db_path: str, progress_every: int = 500_000) -> int:
    """Stream the snapshot JSONL into a fresh SQLite/FTS5 database.

    Idempotent-ish: refuses to run when ``db_path`` already exists so an
    interrupted build never yields a silently partial database.
    """
    if Path(db_path).exists():
        raise SystemExit(f"refusing to overwrite existing database: {db_path}")
    connection = sqlite3.connect(db_path)
    connection.executescript(_SCHEMA)
    started = time.monotonic()
    scanned = 0
    next_rowid = 0
    seen_ids: set[str] = set()
    paper_rows: list[tuple[Any, ...]] = []

    def flush() -> None:
        connection.executemany(
            "INSERT INTO papers(rowid_alias, id, title, abstract, authors, comments,"
            " journal_ref, categories, v1_date, update_date, authors_parsed)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            paper_rows,
        )
        paper_rows.clear()

    with open(jsonl_path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            scanned += 1
            title = " ".join(str(record.get("title") or "").split())
            abstract = " ".join(str(record.get("abstract") or "").split())
            authors = str(record.get("authors") or "")
            comments = str(record.get("comments") or "")
            journal_ref = str(record.get("journal-ref") or "")
            categories = str(record.get("categories") or "")
            arxiv_id = str(record.get("id") or "")
            if not arxiv_id or arxiv_id in seen_ids:
                continue  # the OAI snapshot contains duplicate ids; keep first
            seen_ids.add(arxiv_id)
            v1 = submitted_date(record)
            v1_date = int(v1.timestamp()) if v1 else None
            update_date = str(record.get("update_date") or "")
            authors_parsed = json.dumps(record.get("authors_parsed") or [], ensure_ascii=False)
            next_rowid += 1
            paper_rows.append((
                next_rowid, arxiv_id, title, abstract, authors, comments, journal_ref,
                categories, v1_date, update_date, authors_parsed,
            ))
            if len(paper_rows) >= 10_000:
                flush()
            if scanned % progress_every == 0:
                print(f"[SNAPSHOT-DB] {scanned} rows, {time.monotonic() - started:.0f}s", flush=True)
    if paper_rows:
        flush()
    connection.commit()
    connection.execute("INSERT INTO fts(fts) VALUES ('rebuild')")
    connection.execute("INSERT INTO fts(fts) VALUES ('optimize')")
    connection.commit()
    connection.close()
    print(f"[SNAPSHOT-DB] done: {scanned} records -> {db_path} in {time.monotonic() - started:.0f}s", flush=True)
    return 0


# ---- query translation ------------------------------------------------------

def _fts_column(field: str) -> str:
    if field not in FTS_COLUMNS:
        raise ValueError(f"unsupported query field: {field}")
    return FTS_COLUMNS[field]


def _quote_phrase(text: str) -> str:
    return '"' + re.sub(r"[^\w]+", " ", text).strip() + '"'


def match_expr(node: Any) -> str:
    """Translate a parsed query tree into an FTS5 MATCH expression.

    Returns ``""`` for an always-true node (date ranges only); callers must
    only drop conjunctive components.
    """
    if isinstance(node, TermNode):
        column = _fts_column(node.field)
        if re.fullmatch(r"\w+", node.term):
            return f"{column} : {node.term}*"
        return f"{column} : {_quote_phrase(node.term)}"  # tokenized, no prefix
    if isinstance(node, PhraseNode):
        return f"{_fts_column(node.field)} : {_quote_phrase(node.phrase)}"
    if isinstance(node, DateRangeNode):
        return ""  # handled as SQL on papers.v1_date
    if isinstance(node, BinaryNode):
        left = match_expr(node.left)
        right = match_expr(node.right)
        if node.op in ("AND", "OR"):
            parts = [part for part in (left, right) if part]
            if not parts:
                return ""
            joiner = " AND " if node.op == "AND" else " OR "
            return joiner.join(parts)
        # ANDNOT: left must stay even when right is pure date (rare; treat
        # empty right as no constraint).
        return f"{left} ANDNOT {right}" if left and right else left
    raise ValueError(f"cannot translate node: {node!r}")


def _split_date_range(node: Any) -> tuple[str, str | None, str | None]:
    """Extract the top-level conjunctive date range; reject nested usage."""
    if isinstance(node, DateRangeNode):
        return "", node.low.isoformat(), node.high.isoformat()
    if isinstance(node, BinaryNode) and node.op in ("AND", "ANDNOT"):
        left_sql, lo1, hi1 = _split_date_range(node.left)
        right_sql, lo2, hi2 = _split_date_range(node.right)
        if lo1 and lo2:
            raise ValueError("more than one submittedDate range is not supported")
        if node.op == "ANDNOT" and (lo2 or hi2):
            raise ValueError("ANDNOT over a submittedDate range is not supported")
        sql = f"{left_sql} ANDNOT {right_sql}" if node.op == "ANDNOT" and left_sql and right_sql else left_sql or right_sql
        return sql, lo1 or lo2, hi1 or hi2
    if isinstance(node, BinaryNode) and node.op == "OR":
        if any(isinstance(child, DateRangeNode) for child in (node.left, node.right)):
            raise ValueError("submittedDate ranges inside OR are not supported")
        left_sql, lo1, hi1 = _split_date_range(node.left)
        right_sql, lo2, hi2 = _split_date_range(node.right)
        if lo1 or lo2:
            raise ValueError("submittedDate ranges inside OR are not supported")
        return f"{left_sql} OR {right_sql}" if left_sql and right_sql else left_sql or right_sql, None, None
    sql = match_expr(node)
    return sql, None, None


# ---- batch search -----------------------------------------------------------

def _ensure_schema(connection: sqlite3.Connection) -> None:
    """Refuse pre-external-content databases (they have the old fts columns)."""
    ddl = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='fts'"
    ).fetchone()
    if ddl and "content='papers'" not in (ddl[0] or ""):
        raise SystemExit(
            "snapshot database uses the old schema (fts stores full text); rebuild it"
            " with `search.py build-snapshot-db --snapshot-jsonl <jsonl> --db <new-path>`"
        )


class SnapshotDbSearch:
    """Same run() contract as :class:`SnapshotArxivSearch`, backed by SQLite.

    Queries execute on a thread pool (one read-only connection per worker);
    results merge in the main thread in original query order, so output is
    identical to serial execution.
    """

    def __init__(
        self,
        *,
        db_path: str,
        start_date: str,
        end_date: str,
        max_results: int = 25,
        batch_label: str = "",
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
        output: str | None = None,
    ) -> None:
        self.db_path = db_path
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = max_results
        self.batch_label = batch_label
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.output = output

    def _run_query(
        self, connection: sqlite3.Connection, item: dict[str, str]
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        from embodied_learning.search.arxiv import with_date_filter  # noqa: E402

        effective = with_date_filter(item["query"], self.start_date, self.end_date)
        node = parse_query(effective)
        try:
            sql_expr, lo_iso, hi_iso = _split_date_range(node)
        except ValueError as exc:
            meta = {"label": item["label"], "query": item["query"], "result_count": 0, "error": str(exc)}
            return meta, []
        sql = "SELECT p.* FROM papers p"
        params: list[Any] = []
        if sql_expr:
            sql += " JOIN fts f ON f.rowid = p.rowid_alias WHERE fts MATCH ?"
            params.append(sql_expr)
        else:
            sql += " WHERE 1=1"
        if lo_iso:
            sql += " AND p.v1_date >= ? AND p.v1_date <= ?"
            low = dt.datetime.fromisoformat(lo_iso).timestamp()
            high = dt.datetime.fromisoformat(hi_iso).timestamp()
            params += [int(low), int(high)]
        sql += " ORDER BY p.v1_date DESC, p.id LIMIT ?"
        params.append(self.max_results)
        try:
            rows = connection.execute(sql, params).fetchall()
        except sqlite3.OperationalError as exc:
            meta = {"label": item["label"], "query": item["query"], "result_count": 0, "error": f"fts match failed: {exc}"}
            return meta, []
        papers = []
        for row in rows:
            record = {
                "id": row["id"],
                "title": row["title"],
                "abstract": row["abstract"],
                "authors": row["authors"],
                "comments": row["comments"],
                "journal-ref": row["journal_ref"],
                "categories": row["categories"],
                "versions": [{"version": "v1", "created": None}],
                "update_date": row["update_date"],
                "authors_parsed": json.loads(row["authors_parsed"] or "[]"),
                "_v1_date": row["v1_date"],
            }
            paper = record_to_paper(record, item["label"], effective)
            papers.append(paper)
        # record_to_paper falls back to update_date when v1 created is None;
        # restore the exact stored v1 timestamp for the published field.
        for paper, row in zip(papers, rows):
            if row["v1_date"]:
                paper["published"] = dt.datetime.fromtimestamp(
                    row["v1_date"], tz=dt.timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
        meta = {"label": item["label"], "query": item["query"], "result_count": len(papers)}
        return meta, papers

    def run(self, queries: list[dict[str, str]], max_workers: int = 8) -> int:
        from concurrent.futures import ThreadPoolExecutor

        probe = sqlite3.connect(self.db_path)
        try:
            _ensure_schema(probe)
        finally:
            probe.close()

        def worker(item: dict[str, str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row
            try:
                return self._run_query(connection, item)
            finally:
                connection.close()

        # sqlite3 releases the GIL during execution, so threads give real
        # parallelism for FTS scans; map() keeps original query order.
        if len(queries) > 1:
            workers = max(1, min(max_workers, len(queries)))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                outcomes = list(pool.map(worker, queries))
        else:
            outcomes = [worker(item) for item in queries]

        papers_by_id: dict[str, dict[str, Any]] = {}
        query_results = []
        for meta, papers in outcomes:
            query_results.append(meta)
            label = meta["label"]
            for paper in papers:
                existing = papers_by_id.setdefault(str(paper["arxiv_id"]), paper)
                if existing is not paper:
                    labels = set(str(existing.get("query_label", "")).split(","))
                    labels.add(label)
                    existing["query_label"] = ",".join(sorted(label for label in labels if label))

        output = {
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "batch": self.batch_label or "",
            "api": f"sqlite:{self.db_path}",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
            "snapshot_backend": "sqlite-fts5",
            "queries": query_results,
            "paper_count": len(papers_by_id),
            "papers": list(papers_by_id.values()),
        }
        rendered = json.dumps(output, ensure_ascii=False, indent=2)
        if self.output:
            with open(self.output, "w", encoding="utf-8") as file_handle:
                file_handle.write(rendered + "\n")
        else:
            print(rendered)
        return 0

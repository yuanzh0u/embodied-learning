#!/usr/bin/env python3
"""Offline arXiv metadata retrieval from a local OAI snapshot (JSONL).

The Kaggle-style ``arxiv-metadata-oai-snapshot.json`` holds one JSON object
per line (``id``, ``title``, ``abstract``, ``authors``, ``categories``,
``comments``, ``journal-ref``, ``versions``, ``update_date``, ...). This module
mirrors the :class:`embodied_learning.search.arxiv.ArxivSearch` contract —
same query syntax, same normalized paper dicts, same batch JSON shape — so
``build-candidate-registry`` and the review driver consume either backend
unchanged. No network access.

Query syntax follows the arXiv Atom API: ``field:term``, quoted phrases,
``AND`` / ``OR`` / ``ANDNOT``, parentheses, and ``submittedDate:[A TO B]``
ranges. ``submittedDate`` maps to the v1 creation date (the API's semantics).
Matching is case-insensitive; bare terms are word-start prefix matches and
quoted phrases are whitespace-normalized substrings.
"""

from __future__ import annotations

import datetime as dt
import email.utils
import heapq
import json
import re
import time
from pathlib import Path
from typing import Any, Callable

KNOWN_FIELDS = {"all", "ti", "abs", "au", "co", "jr", "cat", "id", "submitteddate"}


# ---- query parsing ----------------------------------------------------------

class QueryNode:
    """Compiled predicate over a parsed snapshot record."""

    def evaluate(self, doc: dict[str, str]) -> bool:  # pragma: no cover - interface
        raise NotImplementedError

    def literals(self) -> list[str]:
        """Text literals that must appear in the raw line for any match."""
        return []


def _contains_prefix(text: str, term: str) -> bool:
    """Word-start prefix match, case-insensitive (``ego`` hits ``egocentric``)."""
    return re.search(rf"\b{re.escape(term)}", text) is not None


class TermNode(QueryNode):
    def __init__(self, field: str, term: str) -> None:
        self.field = field
        self.term = term

    def evaluate(self, doc: dict[str, str]) -> bool:
        return _contains_prefix(doc.get(self.field, ""), self.term)

    def literals(self) -> list[str]:
        return [self.term]


class PhraseNode(QueryNode):
    def __init__(self, field: str, phrase: str) -> None:
        self.field = field
        self.phrase = phrase

    def evaluate(self, doc: dict[str, str]) -> bool:
        return self.phrase in doc.get(self.field, "")

    def literals(self) -> list[str]:
        return [self.phrase]


class DateRangeNode(QueryNode):
    def __init__(self, low: str, high: str) -> None:
        self.low = dt.datetime.strptime(low, "%Y%m%d%H%M").replace(tzinfo=dt.timezone.utc)
        self.high = dt.datetime.strptime(high, "%Y%m%d%H%M").replace(tzinfo=dt.timezone.utc)

    def evaluate(self, doc: dict[str, str]) -> bool:
        submitted = doc.get("submitted_dt")
        if submitted is None:
            return False
        return self.low <= submitted <= self.high


class NotNode(QueryNode):
    def __init__(self, child: QueryNode) -> None:
        self.child = child

    def evaluate(self, doc: dict[str, str]) -> bool:
        return not self.child.evaluate(doc)

    def literals(self) -> list[str]:
        return []  # must-not literals can never prefilter


class BinaryNode(QueryNode):
    def __init__(self, op: str, left: QueryNode, right: QueryNode) -> None:
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self, doc: dict[str, str]) -> bool:
        if self.op == "AND":
            return self.left.evaluate(doc) and self.right.evaluate(doc)
        if self.op == "OR":
            return self.left.evaluate(doc) or self.right.evaluate(doc)
        return self.left.evaluate(doc) and not self.right.evaluate(doc)  # ANDNOT

    def literals(self) -> list[str]:
        if self.op in ("AND", "OR"):
            return self.left.literals() + self.right.literals()
        return self.left.literals()  # ANDNOT: must-not side can never prefilter


class QueryParser:
    """Recursive-descent parser for the arXiv search_query mini-language."""

    def __init__(self, query: str) -> None:
        self.tokens = self._tokenize(query)
        self.pos = 0

    @staticmethod
    def _tokenize(query: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        index = 0
        length = len(query)
        while index < length:
            char = query[index]
            if char.isspace():
                index += 1
                continue
            if char == "(":
                tokens.append(("LPAREN", "("))
                index += 1
                continue
            if char == ")":
                tokens.append(("RPAREN", ")"))
                index += 1
                continue
            if char == '"':
                end = query.find('"', index + 1)
                if end < 0:
                    raise ValueError(f"unterminated quoted phrase in query: {query!r}")
                tokens.append(("PHRASE", query[index + 1:end]))
                index = end + 1
                continue
            match = re.match(r"([A-Za-z]+)\s*:", query[index:])
            if match and match.group(1).lower() in KNOWN_FIELDS:
                tokens.append(("FIELD", match.group(1).lower()))
                index += match.end()
                continue
            if char == "[":
                range_match = re.match(
                    r"\[(\d{12})\s+TO\s+(\d{12})\]", query[index:], re.IGNORECASE
                )
                if not range_match:
                    raise ValueError(f"malformed date range in query: {query[index:index + 40]!r}")
                tokens.append(("RANGE", range_match.group(1) + ".." + range_match.group(2)))
                index += range_match.end()
                continue
            word = re.match(r'[^\s()"]+', query[index:])
            if not word:  # pragma: no cover - regex always matches a char
                raise ValueError(f"cannot tokenize query at: {query[index:index + 10]!r}")
            value = word.group(0)
            upper = value.upper()
            if upper in ("AND", "OR", "ANDNOT"):
                tokens.append((upper, value))
            else:
                tokens.append(("TERM", value))
            index += word.end()
        return tokens

    def _peek(self) -> tuple[str, str] | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _next(self) -> tuple[str, str]:
        token = self._peek()
        if token is None:
            raise ValueError("unexpected end of query")
        self.pos += 1
        return token

    def parse(self) -> QueryNode:
        node = self._parse_or()
        if self._peek() is not None:
            raise ValueError(f"unexpected token after query: {self._peek()}")
        return node

    def _parse_or(self) -> QueryNode:
        node = self._parse_and()
        while (token := self._peek()) and token[0] == "OR":
            self._next()
            node = BinaryNode("OR", node, self._parse_and())
        return node

    def _parse_and(self) -> QueryNode:
        node = self._parse_not()
        while True:
            token = self._peek()
            if token is None:
                return node
            if token[0] == "AND":
                self._next()
                node = BinaryNode("AND", node, self._parse_not())
            elif token[0] == "ANDNOT":
                self._next()
                node = BinaryNode("ANDNOT", node, self._parse_not())
            elif token[0] in ("LPAREN", "TERM", "PHRASE", "FIELD"):
                node = BinaryNode("AND", node, self._parse_not())  # implicit AND
            else:
                return node

    def _parse_not(self) -> QueryNode:
        return self._parse_primary()

    def _parse_primary(self) -> QueryNode:
        token = self._next()
        if token[0] == "LPAREN":
            node = self._parse_or()
            closing = self._next()
            if closing[0] != "RPAREN":
                raise ValueError("unbalanced parentheses in query")
            return node
        if token[0] == "FIELD":
            field = token[1]
            value = self._next()
            if field == "submitteddate":
                if value[0] != "RANGE":
                    raise ValueError("submittedDate requires a [A TO B] range")
                low, high = value[1].split("..")
                return DateRangeNode(low, high)
            if value[0] == "PHRASE":
                return PhraseNode(field, _normalize(value[1]))
            if value[0] == "TERM":
                return TermNode(field, value[1].lower())
            raise ValueError(f"field {field!r} expects a term, got {value[0]}")
        if token[0] == "PHRASE":
            return PhraseNode("all", _normalize(token[1]))
        if token[0] == "TERM":
            return TermNode("all", token[1].lower())
        raise ValueError(f"unexpected token {token!r} in query")


def parse_query(query: str) -> QueryNode:
    return QueryParser(query).parse()


def _normalize(text: str) -> str:
    return " ".join(text.split()).lower()


# ---- record handling --------------------------------------------------------

FIELD_SOURCES: dict[str, tuple[str, ...]] = {
    "all": ("title", "abstract", "authors", "comments", "journal_ref", "categories", "id"),
    "ti": ("title",),
    "abs": ("abstract",),
    "au": ("authors",),
    "co": ("comments",),
    "jr": ("journal_ref",),
    "cat": ("categories",),
    "id": ("id",),
}


def record_to_doc(record: dict[str, Any]) -> dict[str, str]:
    """Flatten a snapshot record into normalized field texts for matching."""
    doc: dict[str, str] = {}
    for field, sources in FIELD_SOURCES.items():
        doc[field] = _normalize(" ".join(str(record.get(src) or "") for src in sources))
    doc["submitted_dt"] = submitted_date(record)
    return doc


def submitted_date(record: dict[str, Any]) -> dt.datetime | None:
    """v1 submission date (mirrors the API's submittedDate), UTC-aware."""
    versions = record.get("versions") or []
    if versions:
        created = versions[0].get("created")
        if created:
            try:
                stamp = email.utils.parsedate_to_datetime(created)
                if stamp.tzinfo is None:
                    stamp = stamp.replace(tzinfo=dt.timezone.utc)
                return stamp.astimezone(dt.timezone.utc)
            except (TypeError, ValueError):
                pass
    update_date = record.get("update_date")
    if update_date:
        try:
            return dt.datetime.strptime(update_date, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            return None
    return None


def record_to_paper(record: dict[str, Any], query_label: str, effective_query: str) -> dict[str, Any]:
    """Normalize a snapshot record into the exact paper dict ``parse_feed`` emits."""
    arxiv_id = str(record.get("id") or "")
    created = submitted_date(record)
    published = created.strftime("%Y-%m-%dT%H:%M:%SZ") if created else ""
    update_date = str(record.get("update_date") or "")
    abstract = " ".join(str(record.get("abstract") or "").split())
    title = " ".join(str(record.get("title") or "").split())
    authors = [
        " ".join(part for part in (name[1], name[2] if len(name) > 2 else "", name[0], name[3] if len(name) > 3 else "") if part).strip()
        for name in (record.get("authors_parsed") or [])
        if isinstance(name, (list, tuple)) and name
    ]
    if not authors:
        authors = [name.strip() for name in re.split(r",\s*", str(record.get("authors") or "")) if name.strip()]
    categories = [cat for cat in str(record.get("categories") or "").split() if cat]
    return {
        "arxiv_id": arxiv_id,
        "versioned_id": arxiv_id,  # snapshot has no per-query version info
        "title": title,
        "authors": authors,
        "published": published,
        "updated": f"{update_date}T00:00:00Z" if update_date else "",
        "summary": abstract,
        "categories": categories,
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "query_label": query_label,
        "effective_query": effective_query,
    }


# ---- batch search -----------------------------------------------------------

class SnapshotArxivSearch:
    """One batch of queries over a local snapshot, mirroring ``ArxivSearch``."""

    def __init__(
        self,
        *,
        snapshot_path: str,
        start_date: str,
        end_date: str,
        max_results: int = 25,
        batch_label: str = "",
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
        output: str | None = None,
        prefilter: bool = True,
        progress_every: int = 500_000,
    ) -> None:
        self.snapshot_path = snapshot_path
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = max_results
        self.batch_label = batch_label
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.output = output
        self.prefilter = prefilter
        self.progress_every = progress_every

    def run(self, queries: list[dict[str, str]]) -> int:
        """Single streaming pass; per query keep the newest ``max_results`` hits."""
        from embodied_learning.search.arxiv import with_date_filter  # noqa: E402  # local: avoids import at module load

        compiled: list[dict[str, Any]] = []
        for item in queries:
            effective = with_date_filter(item["query"], self.start_date, self.end_date)
            node = parse_query(effective)
            compiled.append({
                "label": item["label"],
                "query": item["query"],
                "effective": effective,
                "node": node,
                # keep a slack pool of newest candidates before final truncation
                "heap": [],  # min-heap of (sort_key, seq, paper_dict); size <= slack
                "slack": max(self.max_results * 20, 100),
                "seq": 0,  # monotonic tiebreaker: heap tuples must never reach the dict
            })
        literals: list[str] = []
        for entry in compiled:
            literals.extend(entry["node"].literals())
        use_prefilter = (
            self.prefilter
            and literals
            and all(entry["node"].literals() for entry in compiled)
            and all(re.fullmatch(r"[\w][\w .\-/:]*", lit) for lit in literals)
        )

        started = time.monotonic()
        scanned = matched_lines = 0
        with open(self.snapshot_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                scanned += 1
                if scanned % self.progress_every == 0:
                    elapsed = time.monotonic() - started
                    print(
                        f"[SNAPSHOT] scanned {scanned} lines, {matched_lines} prefilter hits, "
                        f"{elapsed:.0f}s elapsed",
                        flush=True,
                    )
                lowered = line.lower() if use_prefilter else ""
                if use_prefilter and not any(lit in lowered for lit in literals):
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                matched_lines += 1
                doc = record_to_doc(record)
                for entry in compiled:
                    if not entry["node"].evaluate(doc):
                        continue
                    paper = record_to_paper(record, entry["label"], entry["effective"])
                    sort_key = _sort_key(paper)
                    item = (sort_key, entry["seq"], paper)
                    entry["seq"] += 1
                    if len(entry["heap"]) < entry["slack"]:
                        heapq.heappush(entry["heap"], item)
                    elif sort_key > entry["heap"][0][0]:
                        heapq.heapreplace(entry["heap"], item)

        papers_by_id: dict[str, dict[str, Any]] = {}
        query_results = []
        for entry in compiled:
            heap = entry["heap"]
            top = sorted(heap, key=lambda item: item[0], reverse=self.sort_order == "descending")
            top = top[: self.max_results]
            query_results.append({
                "label": entry["label"],
                "query": entry["query"],
                "result_count": len(top),
            })
            for _, _, paper in top:
                existing = papers_by_id.setdefault(str(paper["arxiv_id"]), paper)
                if existing is not paper:
                    labels = set(str(existing.get("query_label", "")).split(","))
                    labels.add(entry["label"])
                    existing["query_label"] = ",".join(sorted(label for label in labels if label))

        output = {
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "batch": self.batch_label or "",
            "api": f"snapshot:{self.snapshot_path}",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
            "snapshot_prefilter": use_prefilter,
            "snapshot_lines_scanned": scanned,
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


def _sort_key(paper: dict[str, Any]) -> str:
    """Newest-first ordering key; ISO ``published`` sorts lexicographically."""
    return paper.get("published") or ""


def yyyymmdd_snapshot(value: str) -> str:
    return dt.datetime.strptime(value, "%Y-%m-%d").strftime("%Y%m%d")

#!/usr/bin/env python3
"""Harvest arXiv papers from a Zotero BibTeX file into the shared pool.

Parses ``zotero.bib`` entries that carry an arXiv crosswalk (``arxiv.org/abs``
URL or ``arXiv:<id>`` note), skips papers already deep-read in the pool, and
emits batches of N ids for the deep-read loop. This script only *plans*: it
never runs the extraction or reading pipeline itself — feed the batch file to
``run_review_pipeline``-style extraction plus the workflow's deep-read round.

    python3 scripts/pool_from_zotero.py --stats
    python3 scripts/pool_from_zotero.py --batch-size 10 --out /tmp/batch-1.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root, for the src/ package
from src.knowledge.arxiv_reader import parse_arxiv_id  # noqa: E402

DEFAULT_KB_ROOT = "~/Documents/arxiv"
ENTRY_RE = re.compile(r"^@\w+\{", re.MULTILINE)
FIELD_RE = re.compile(r"^\t(\w+)\s*=\s*(.*)$", re.MULTILINE)
ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([^\s,}]+)", re.IGNORECASE)
ARXIV_NOTE_RE = re.compile(r"arXiv[:\s]*([0-9]{4}\.[0-9]{4,5}|[a-z-]+/[0-9]{7})", re.IGNORECASE)


def strip_braces(value: str) -> str:
    """Strip one trailing comma, then balanced outer brace/quote wrappers.
    Nested-but-sibling braces ({A}-{B}) are preserved: only a single outer
    wrapper whose braces balance at the end is removed."""
    raw = value.strip()
    if raw.endswith(","):
        raw = raw[:-1].rstrip()
    while len(raw) >= 2 and raw[0] in "{\"":
        if raw[0] == '"':
            if raw[-1] == '"':
                raw = raw[1:-1].strip()
            break
        depth = 0
        closes = False
        for index, char in enumerate(raw):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    if index == len(raw) - 1:
                        raw = raw[1:-1].strip()
                        closes = True
                    break
        if not closes:
            break
    return raw


def normalize_id(raw: str) -> str:
    return parse_arxiv_id(raw.strip()) or ""


def parse_entries(bib_text: str) -> list[dict[str, str]]:
    """Split a Zotero BibTeX file into per-entry field dicts.

    Zotero exports are machine-formatted (tab-indented fields, one level of
    brace quoting), so a line-based field scan is sufficient — no full TeX
    parsing required."""
    entries: list[dict[str, str]] = []
    positions = [match.start() for match in ENTRY_RE.finditer(bib_text)] + [len(bib_text)]
    for start, end in zip(positions, positions[1:]):
        block = bib_text[start:end]
        fields = {
            key: strip_braces(value)
            for key, value in FIELD_RE.findall(block)
        }
        citation_key = block.split("{", 1)[1].split(",", 1)[0].strip()
        fields["_key"] = citation_key
        entries.append(fields)
    return entries


def arxiv_id_of(fields: dict[str, str]) -> str:
    for field in ("url", "note"):
        for pattern in (ARXIV_URL_RE, ARXIV_NOTE_RE):
            match = pattern.search(fields.get(field, ""))
            if match:
                return normalize_id(match.group(1))
    return ""


def pool_state(pool_root: Path) -> tuple[set[str], set[str]]:
    """Return (all pooled ids, ids with a passing deep-read note)."""
    pooled: set[str] = set()
    verified: set[str] = set()
    index = pool_root / "index.jsonl"
    if index.is_file():
        import json
        for line in index.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            arxiv_id = str(record.get("arxiv_id") or "")
            if arxiv_id:
                pooled.add(arxiv_id)
                if record.get("audit_status") in {"pass", "needs-review"}:
                    verified.add(arxiv_id)
    return pooled, verified


def _newest_first(arxiv_id: str):
    """Sort key for ``reverse=True``: modern 5-digit-numbering ids first, then
    by year-month descending. Pre-2014 legacy ids (``hep-th/9801001``) sort
    last via the leading 0."""
    match = re.match(r"^(\d{2})(\d{2})\.(\d{4,5})(v\d+)?$", arxiv_id)
    if match:
        year, month = 2000 + int(match.group(1)), int(match.group(2))
        return (1, year * 12 + month, arxiv_id)
    return (0, 0, arxiv_id)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bib", default=None, help="Path to zotero.bib (default <kb-root>/zotero.bib).")
    parser.add_argument("--kb-root", default=DEFAULT_KB_ROOT)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--batches", type=int, default=1, help="How many batches to emit.")
    parser.add_argument("--out-dir", default=None, help="Where batch files are written (default <kb-root>/work).")
    parser.add_argument("--order", choices=["newest", "id", "as-listed"], default="newest",
                        help="newest = recent arXiv ids first (HTML-era papers, best extraction odds).")
    parser.add_argument("--stats", action="store_true", help="Print coverage stats only.")
    args = parser.parse_args(argv)

    kb_root = Path(args.kb_root).expanduser()
    bib_path = Path(args.bib).expanduser() if args.bib else kb_root / "zotero.bib"
    pool_root = kb_root / "pool"
    if not bib_path.is_file():
        print(f"bib file not found: {bib_path}", file=sys.stderr)
        return 2

    entries = parse_entries(bib_path.read_text(encoding="utf-8", errors="replace"))
    harvested: dict[str, dict[str, str]] = {}
    for fields in entries:
        arxiv_id = arxiv_id_of(fields)
        if arxiv_id and arxiv_id not in harvested:
            harvested[arxiv_id] = {
                "title": fields.get("title", ""),
                "year": fields.get("year", ""),
                "key": fields.get("_key", ""),
            }

    pooled, verified = pool_state(pool_root)
    if args.order == "newest":
        ordered = sorted(harvested, key=_newest_first, reverse=True)
    elif args.order == "as-listed":
        ordered = list(harvested)
    else:
        ordered = sorted(harvested)
    todo = [arxiv_id for arxiv_id in ordered if arxiv_id not in verified]
    print(f"bib entries: {len(entries)}, arXiv-harvested: {len(harvested)}, "
          f"pooled: {len(pooled & set(harvested))}, deep-read pass: {len(verified & set(harvested))}, "
          f"todo: {len(todo)}")
    if args.stats:
        return 0

    out_dir = Path(args.out_dir).expanduser() if args.out_dir else kb_root / "work"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    for batch_index in range(args.batches):
        chunk = todo[batch_index * args.batch_size : (batch_index + 1) * args.batch_size]
        if not chunk:
            break
        path = out_dir / f"zotero-batch-{batch_index + 1:02d}.txt"
        path.write_text("\n".join(chunk) + "\n", encoding="utf-8")
        written += 1
        print(f"wrote {path} ({len(chunk)} ids)")
    if not written:
        print("nothing to do: every bib arXiv paper is already deep-read in the pool")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Migrate per-run literature-review artifacts into the shared public pool.

One paper, one pool entry — every downstream consumer (deep reading, the wiki
reader, extraction checkpoints) checks the pool first:

    pool/arxiv-<id>/paper.md         reading-packet / full-text markdown
    pool/arxiv-<id>/extraction.json  unified extraction (tables/figures/text)
    pool/arxiv-<id>/paper.html       cleaned arXiv HTML (reader fast path)
    pool/arxiv-<id>/note.json        paper-reader note (deep-read result)
    pool/arxiv-<id>/note.json.audit.json  claim-support audit when present
    pool/arxiv-<id>/meta.json        manifest; index.jsonl one line per paper

Sources swept (newest wins per file, so a later deep-read refreshes note.json
without downgrading paper.md):
  work/literature-review-*/reading-packets/<id>.md
  work/literature-review-*/extractions/<id>.json
  work/literature-review-*/paper-notes/<id>.json[.audit.json]
  work/reader-cache/<id>.html
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # repo root, for the src/ package
from src.knowledge.legacy.arxiv_reader import parse_arxiv_id  # noqa: E402

DEFAULT_KB_ROOT = "~/Documents/arxiv"


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_id(raw: str) -> str:
    """Canonical id via the shared grammar (folders are keyed by versionless id)."""

    return parse_arxiv_id(raw.strip().removesuffix(".pdf")) or ""


def is_arxiv_id(name: str) -> bool:
    return bool(normalize_id(name))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_index(root: Path) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    index = root / "index.jsonl"
    if index.is_file():
        for line in index.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(record, dict) and record.get("dir_name"):
                    entries[record["dir_name"]] = record
    return entries


def write_index(root: Path, entries: dict[str, dict]) -> None:
    index = root / "index.jsonl"
    lines = [json.dumps(entries[key], ensure_ascii=False, sort_keys=True) for key in sorted(entries)]
    index.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def collect(work_root: Path) -> dict[str, dict[str, Path]]:
    """Map arXiv id -> the newest artifact file of each kind across all runs."""
    papers: dict[str, dict[str, Path]] = {}
    by_id = papers.setdefault

    def offer(paper_id: str, kind: str, path: Path) -> None:
        entry = by_id(paper_id, {})
        current = entry.get(kind)
        if current is None or path.stat().st_mtime > current.stat().st_mtime:
            entry[kind] = path

    for run_dir in sorted(work_root.glob("literature-review-*")):
        if not run_dir.is_dir():
            continue
        for path in (run_dir / "reading-packets").glob("*.md"):
            if is_arxiv_id(path.stem):
                offer(normalize_id(path.stem), "paper_md", path)
        for path in (run_dir / "extractions").glob("*.json"):
            if is_arxiv_id(path.stem):
                offer(normalize_id(path.stem), "extraction", path)
        notes = run_dir / "paper-notes"
        for path in notes.glob("*.json"):
            if path.name.endswith(".audit.json"):
                continue
            if is_arxiv_id(path.stem):
                offer(normalize_id(path.stem), "note", path)
        for path in notes.glob("*.audit.json"):
            stem = path.name.removesuffix(".audit.json")
            if is_arxiv_id(stem):
                offer(normalize_id(stem), "audit", path)

    cache = work_root / "reader-cache"
    if cache.is_dir():
        for path in cache.glob("*.html"):
            if is_arxiv_id(path.stem):
                offer(normalize_id(path.stem), "html", path)
    return papers


def migrate(papers: dict[str, dict[str, Path]], pool_root: Path, *, force: bool) -> tuple[int, int]:
    entries = read_index(pool_root)
    added = refreshed = 0
    for paper_id, kinds in sorted(papers.items()):
        dir_name = f"arxiv-{paper_id}"
        target = pool_root / dir_name
        if target.is_dir() and any(target.iterdir()) and not force:
            refreshed += 1
            continue
        target.mkdir(parents=True, exist_ok=True)
        extraction = None
        if "extraction" in kinds:
            try:
                extraction = load_json(kinds["extraction"])
            except (json.JSONDecodeError, OSError):
                extraction = None
            (target / "extraction.json").write_bytes(kinds["extraction"].read_bytes())
        if "paper_md" in kinds:
            (target / "paper.md").write_bytes(kinds["paper_md"].read_bytes())
        elif extraction is not None and str(extraction.get("text") or "").strip():
            (target / "paper.md").write_text(str(extraction["text"]) + "\n", encoding="utf-8")
        if "html" in kinds:
            (target / "paper.html").write_bytes(kinds["html"].read_bytes())
        if "note" in kinds:
            try:
                note = load_json(kinds["note"])
            except (json.JSONDecodeError, OSError):
                note = None
            if note is not None:
                # Only archive real deep-read notes; template shells carry no cards.
                if note.get("evidence_cards"):
                    (target / "note.json").write_bytes(kinds["note"].read_bytes())
                if "audit" in kinds:
                    (target / "note.json.audit.json").write_bytes(kinds["audit"].read_bytes())
        if extraction is None and (target / "extraction.json").is_file():
            extraction = load_json(target / "extraction.json")
        quality = (extraction or {}).get("quality") or {}
        title = str((extraction or {}).get("title") or "")
        note_status = ""
        if (target / "note.json.audit.json").is_file():
            try:
                note_status = str(load_json(target / "note.json.audit.json").get("status") or "")
            except (json.JSONDecodeError, OSError):
                note_status = ""
        meta = {
            "id_type": "arxiv",
            "key": paper_id,
            "dir_name": dir_name,
            "arxiv_id": paper_id,
            "doi": "",
            "title": title,
            "url": f"https://arxiv.org/abs/{paper_id}",
            "added_at": stable_now(),
            "migrated_from": "work/",
            "extraction_method": str((extraction or {}).get("extraction_method") or ""),
            "source_format": str((extraction or {}).get("source_format") or ""),
            "quality": quality.get("grade") if isinstance(quality, dict) else quality,
            "text_chars": quality.get("text_chars") if isinstance(quality, dict) else 0,
            "deep_read": bool((target / "note.json").is_file()),
            "audit_status": note_status,
            "files": sorted(p.name for p in target.iterdir() if p.is_file()),
        }
        (target / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        entries[dir_name] = meta
        added += 1
    write_index(pool_root, entries)
    return added, refreshed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb-root", default=DEFAULT_KB_ROOT)
    parser.add_argument("--pool-root", default=None, help="Defaults to <kb-root>/pool.")
    parser.add_argument("--dry-run", action="store_true", help="Report what would migrate.")
    parser.add_argument("--force", action="store_true", help="Refresh entries already in the pool.")
    args = parser.parse_args(argv)

    kb_root = Path(args.kb_root).expanduser()
    pool_root = Path(args.pool_root).expanduser() if args.pool_root else kb_root / "pool"
    work_root = kb_root / "work"
    if not work_root.is_dir():
        print(f"no work/ under {kb_root}", file=sys.stderr)
        return 2
    papers = collect(work_root)
    kinds_count: dict[str, int] = {}
    for kinds in papers.values():
        for kind in kinds:
            kinds_count[kind] = kinds_count.get(kind, 0) + 1
    print(f"discovered {len(papers)} papers: {kinds_count}")
    if args.dry_run:
        return 0
    pool_root.mkdir(parents=True, exist_ok=True)
    added, refreshed = migrate(papers, pool_root, force=args.force)
    print(f"pool now: {added} added, {refreshed} already present → {pool_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

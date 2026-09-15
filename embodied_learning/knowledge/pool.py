#!/usr/bin/env python3
"""Manage the local public paper pool: one folder per paper, keyed by unique ID.

The pool is a local (gitignored-by-location) shared store — by default
``~/Documents/arxiv/pool`` next to the knowledge base that
``serve_research_wiki --kb-root`` resolves. Each paper owns a directory named
after its unique ID (``arxiv-2403.12550``, or ``doi-<urlquoted doi>`` when no
arXiv crosswalk exists) holding the converted Markdown, the unified
extraction JSON, an optional reading note, and a ``meta.json`` manifest;
``index.jsonl`` keeps one line per paper for fast lookup.

Source tarballs and HTML are download caches (temp dirs) and are never
archived here — the pool stores extracted artifacts only.

Topic cards cite pool papers with a ``POOL-*`` source entry:

    - id: POOL-arxiv-2403.12550
      file: ~/Documents/arxiv/pool/arxiv-2403.12550/paper.md
      locator: §3 Method ¶ Keyframe Selection

The CLI surface (add | import-existing | list | get) lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/pool_add_paper.py``; this module
is the library API.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any

DEFAULT_POOL_ROOT = "~/Documents/arxiv/pool"


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def paper_identity(extraction: dict[str, Any], metadata: dict[str, Any] | None) -> dict[str, Any]:
    """Resolve the unique ID (arXiv primary, DOI fallback) and display fields."""
    meta = metadata or {}
    paper = meta.get("paper") if isinstance(meta.get("paper"), dict) else meta
    arxiv_id = str(paper.get("arxiv_id") or paper.get("paper_id") or extraction.get("paper_id") or "")
    arxiv_id = re.sub(r"v\d+$", "", arxiv_id.rsplit("/", 1)[-1].removesuffix(".pdf"))
    doi = str(paper.get("doi") or extraction.get("doi") or "")
    if arxiv_id:
        id_type, key = "arxiv", arxiv_id
    elif doi:
        id_type, key = "doi", doi
    else:
        raise SystemExit("no arxiv_id or doi in extraction/metadata; cannot key a pool entry")
    title = str(paper.get("title") or extraction.get("title") or "")
    return {
        "id_type": id_type,
        "key": key,
        "dir_name": f"{id_type}-{urllib.parse.quote(key, safe='')}" if id_type == "doi" else f"arxiv-{key}",
        "arxiv_id": arxiv_id,
        "doi": doi,
        "title": title,
        "published": str(paper.get("published") or ""),
        "authors": paper.get("authors") if isinstance(paper.get("authors"), list) else [],
    }


def pool_dir(pool_root: str) -> Path:
    return Path(pool_root).expanduser()


def index_path(root: Path) -> Path:
    return root / "index.jsonl"


def read_index(root: Path) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    path = index_path(root)
    if not path.is_file():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and record.get("dir_name"):
            entries[str(record["dir_name"])] = record
    return entries


def write_index(root: Path, entries: dict[str, dict[str, Any]]) -> None:
    path = index_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(entries[key], ensure_ascii=False, sort_keys=True) for key in sorted(entries)]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


class PaperPool:
    """Local public paper pool: one folder per paper under a shared root.

    The CLI surface lives in the skill entry (skills/embodied-ai-literature-hub/
    scripts/pool_add_paper.py); this class is the library API.
    """

    def __init__(self, pool_root: str | Path = DEFAULT_POOL_ROOT) -> None:
        self.root = pool_dir(str(pool_root))

    def add(
        self,
        extraction: dict[str, Any],
        metadata: dict[str, Any] | None = None,
        note: str | None = None,
        note_json: dict[str, Any] | None = None,
        html: str | None = None,
        force: bool = False,
    ) -> int:
        """Add or refresh one paper from a unified extraction payload.

        ``note`` is reading-note Markdown text; ``note_json`` is a parsed
        paper-note JSON payload; ``html`` is a path to cleaned/raw paper HTML.
        """
        root = self.root
        identity = paper_identity(extraction, metadata)
        target = root / identity["dir_name"]
        if target.is_dir() and not force:
            print(f"skip {identity['dir_name']}: already in pool (use --force to refresh)")
            return 0
        if not extraction.get("available"):
            raise SystemExit("extraction is not available; refusing to add an unavailable paper")

        markdown = str(extraction.get("text") or "")
        if not markdown.strip():
            raise SystemExit("extraction carries no `text`; rerun with --include-full-text / full-text output")
        target.mkdir(parents=True, exist_ok=True)
        (target / "paper.md").write_text(markdown + "\n", encoding="utf-8")
        (target / "extraction.json").write_text(json.dumps(extraction, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if note:
            (target / "note.md").write_text(note, encoding="utf-8")
        if note_json is not None:
            (target / "note.json").write_text(
                json.dumps(note_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        if html:
            html_path = Path(html).expanduser()
            (target / "paper.html").write_bytes(html_path.read_bytes())

        quality = extraction.get("quality") or {}
        meta = {
            **identity,
            "url": f"https://arxiv.org/abs/{identity['arxiv_id']}" if identity["arxiv_id"] else "",
            "added_at": stable_now(),
            "extraction_method": str(extraction.get("extraction_method") or ""),
            "source_format": str(extraction.get("source_format") or ""),
            "quality": quality.get("grade") if isinstance(quality, dict) else quality,
            "text_chars": quality.get("text_chars") if isinstance(quality, dict) else 0,
            "files": sorted(p.name for p in target.iterdir() if p.is_file()),
        }
        (target / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        entries = read_index(root)
        entries[identity["dir_name"]] = {
            "dir_name": meta["dir_name"],
            "id_type": meta["id_type"],
            "arxiv_id": meta["arxiv_id"],
            "doi": meta["doi"],
            "title": meta["title"],
            "published": meta["published"],
            "quality": meta["quality"],
            "extraction_method": meta["extraction_method"],
            "added_at": meta["added_at"],
        }
        write_index(root, entries)
        print(f"added {identity['dir_name']} -> {target}")
        return 0

    def import_existing(self, force: bool = False) -> int:
        """Migrate legacy flat ``<id>.md`` files into the per-paper layout."""
        root = self.root
        migrated = 0
        for md_file in sorted(root.glob("*.md")):
            match = re.match(r"^(\d{4}\.\d{4,5})(v\d+)?$", md_file.stem)
            if not match:
                continue
            arxiv_id = match.group(1)
            target = root / f"arxiv-{arxiv_id}"
            if target.is_dir() and not force:
                print(f"skip {md_file.name}: {target.name} already exists")
                continue
            target.mkdir(parents=True, exist_ok=True)
            (target / "paper.md").write_text(md_file.read_text(encoding="utf-8"), encoding="utf-8")
            title = ""
            for line in md_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            meta = {
                "id_type": "arxiv",
                "key": arxiv_id,
                "dir_name": f"arxiv-{arxiv_id}",
                "arxiv_id": arxiv_id,
                "doi": "",
                "title": title or arxiv_id,
                "published": "",
                "authors": [],
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "added_at": stable_now(),
                "extraction_method": "html-latexml",
                "source_format": "html",
                "quality": "unknown",
                "text_chars": 0,
                "files": sorted(p.name for p in target.iterdir() if p.is_file()),
                "imported_from": md_file.name,
            }
            (target / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            entries = read_index(root)
            entries[meta["dir_name"]] = {
                "dir_name": meta["dir_name"],
                "id_type": meta["id_type"],
                "arxiv_id": meta["arxiv_id"],
                "doi": "",
                "title": meta["title"],
                "published": "",
                "quality": meta["quality"],
                "extraction_method": meta["extraction_method"],
                "added_at": meta["added_at"],
            }
            write_index(root, entries)
            md_file.unlink()
            migrated += 1
            print(f"migrated {md_file.name} -> {target.name}/")
        print(f"done: {migrated} paper(s) migrated")
        return 0

    def list_papers(self, as_json: bool = False) -> int:
        entries = read_index(self.root)
        if as_json:
            print(json.dumps(list(entries.values()), ensure_ascii=False, indent=2))
            return 0
        print(f"{'dir_name':<40} {'quality':<8} {'method':<14} title")
        for key in sorted(entries):
            record = entries[key]
            print(f"{key:<40} {str(record.get('quality') or ''):<8} {str(record.get('extraction_method') or ''):<14} {str(record.get('title') or '')[:60]}")
        print(f"\n{len(entries)} paper(s) in {self.root}")
        return 0

    def get(self, paper_id: str) -> int:
        root = self.root
        entries = read_index(root)
        requested = paper_id.strip()
        candidates = [requested, f"arxiv-{requested}", f"doi-{urllib.parse.quote(requested, safe='')}"]
        dir_name = next((name for name in candidates if name in entries), None)
        if dir_name is None:
            raise SystemExit(f"paper not found in pool: {requested}")
        meta_file = root / dir_name / "meta.json"
        if not meta_file.is_file():
            raise SystemExit(f"pool entry lacks meta.json: {root / dir_name}")
        print(meta_file.read_text(encoding="utf-8"))
        return 0

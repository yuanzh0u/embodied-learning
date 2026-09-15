#!/usr/bin/env python3
"""knowledge-layer CLI: one entry, one subcommand per tool.

Each subcommand owns its original flags (per-subcommand parsers, so legacy
flag names never collide); implementation lives in the embodied_learning
knowledge layer. Subcommand names are the old single-purpose scripts
kebab-cased: `pool-add-paper` was `scripts/pool_add_paper.py`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# ---- pool-add-paper (was scripts/pool_add_paper.py) --------------------------

import argparse

from embodied_learning.knowledge.pool import DEFAULT_POOL_ROOT, PaperPool, load_json


def _pool_add_paper_parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add", help="Add or refresh a paper from an extraction JSON.")
    add.add_argument("--extraction", required=True, help="Unified extraction JSON (extract_arxiv_content/tex output).")
    add.add_argument("--metadata", help="Optional per-paper metadata JSON (flat or wrapped in `paper`).")
    add.add_argument("--note", help="Optional reading note Markdown to archive as note.md.")
    add.add_argument(
        "--note-json",
        help="Optional paper-note JSON (paper-reader output) to archive as note.json.",
    )
    add.add_argument(
        "--html",
        help="Optional cleaned/raw paper HTML to archive as paper.html (reader fast path).",
    )
    add.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)
    add.add_argument("--force", action="store_true", help="Overwrite an existing pool entry and refresh its index line.")

    import_existing = sub.add_parser("import-existing", help="Migrate legacy flat <id>.md files into the per-paper layout.")
    import_existing.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)
    import_existing.add_argument("--force", action="store_true")

    list_parser = sub.add_parser("list", help="List pool papers.")
    list_parser.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)
    list_parser.add_argument("--format", choices=["table", "json"], default="table")

    get_parser = sub.add_parser("get", help="Print one paper's meta.json.")
    get_parser.add_argument("paper_id", help="arXiv ID or pool directory name.")
    get_parser.add_argument("--pool-root", default=DEFAULT_POOL_ROOT)

    return parser.parse_args(argv)


def _pool_add_paper_main(argv: list[str] | None = None) -> int:
    args = _pool_add_paper_parse_args(argv)
    pool = PaperPool(args.pool_root)
    if args.command == "add":
        metadata = load_json(Path(args.metadata).expanduser()) if args.metadata else None
        note = Path(args.note).expanduser().read_text(encoding="utf-8") if args.note else None
        note_json = load_json(Path(args.note_json).expanduser()) if args.note_json else None
        return pool.add(
            extraction=load_json(Path(args.extraction).expanduser()),
            metadata=metadata,
            note=note,
            note_json=note_json,
            html=args.html,
            force=args.force,
        )
    if args.command == "import-existing":
        return pool.import_existing(force=args.force)
    if args.command == "list":
        return pool.list_papers(as_json=args.format == "json")
    if args.command == "get":
        return pool.get(args.paper_id)
    raise SystemExit("choose a command: add | import-existing | list | get")



_SUBCOMMANDS = {
    "pool-add-paper": _pool_add_paper_main,
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

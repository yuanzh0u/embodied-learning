#!/usr/bin/env python3
"""Optional token-meter helper (audit §6.1).

Enable with ``EMBODIED_TOKEN_METER=1``. Appends one JSONL record to
``work/<run>/token-meter.jsonl`` (or ``--output``). Never blocks the main
pipeline: failures print a warning and return non-zero without raising.

Schema fields:
  run_id, stage, paper_id, round, model,
  prompt_chars, completion_chars, prompt_tokens, completion_tokens,
  files_loaded[{path, bytes}], included_full_text, cache_hit, ts
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENV_FLAG = "EMBODIED_TOKEN_METER"


def enabled() -> bool:
    return os.environ.get(ENV_FLAG, "").strip() not in {"", "0", "false", "False", "no", "NO"}


def append_record(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    files_loaded: list[dict[str, Any]] = []
    for item in args.file or []:
        file_path = Path(item)
        entry: dict[str, Any] = {"path": str(file_path)}
        try:
            entry["bytes"] = file_path.stat().st_size
        except OSError:
            entry["bytes"] = None
        files_loaded.append(entry)
    return {
        "run_id": args.run_id,
        "stage": args.stage,
        "paper_id": args.paper_id,
        "round": args.round,
        "model": args.model,
        "prompt_chars": args.prompt_chars,
        "completion_chars": args.completion_chars,
        "prompt_tokens": args.prompt_tokens,
        "completion_tokens": args.completion_tokens,
        "files_loaded": files_loaded,
        "included_full_text": bool(args.included_full_text),
        "cache_hit": args.cache_hit,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Path to token-meter.jsonl")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--stage", required=True, help="e.g. reader.deep, writer.zhihu, hub.coverage_decide")
    parser.add_argument("--paper-id", default="")
    parser.add_argument("--round", type=int, default=None)
    parser.add_argument("--model", default="")
    parser.add_argument("--prompt-chars", type=int, default=None)
    parser.add_argument("--completion-chars", type=int, default=None)
    parser.add_argument("--prompt-tokens", type=int, default=None)
    parser.add_argument("--completion-tokens", type=int, default=None)
    parser.add_argument("--file", action="append", default=[], help="Loaded file path (repeatable)")
    parser.add_argument("--included-full-text", action="store_true")
    parser.add_argument("--cache-hit", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Write even when EMBODIED_TOKEN_METER is unset.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.force and not enabled():
        print(
            f"token meter idle ({ENV_FLAG} unset); pass --force or export {ENV_FLAG}=1",
            file=sys.stderr,
        )
        return 0
    try:
        record = build_record(args)
        append_record(Path(args.output), record)
    except OSError as exc:
        print(f"token meter warning: {exc}", file=sys.stderr)
        return 1
    print(f"appended token-meter record -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

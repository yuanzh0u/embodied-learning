"""Cache deterministic + LLM-merged query plans by topic/mode/time_range/family.

Cache key = SHA-256 of the normalized tuple
``(topic, review_mode, time_range, family)``. On a hit, reuse the stored plan and
**skip** dynamic-expansion / persona-generation LLM calls. Persona regeneration
after coverage dimension gaps remains allowed (cache does not block that path).

Default root: ``.cache/query-plans/`` (gitignored). Override with
``--cache-root`` or ``EMBODIED_QUERY_PLAN_CACHE``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_CACHE_ROOT = Path(".cache/query-plans")


def normalize_topic(topic: str) -> str:
    return " ".join(str(topic or "").split()).strip().lower()


def normalize_families(families: list[str]) -> list[str]:
    cleaned = sorted({(" ".join(f.split()).strip().lower()) for f in families if f and f.strip()})
    return cleaned


def cache_key(topic: str, review_mode: str, time_range: str, families: list[str]) -> str:
    payload = {
        "topic": normalize_topic(topic),
        "review_mode": str(review_mode or "scoping").strip().lower(),
        "time_range": " ".join(str(time_range or "").split()).strip().lower(),
        "families": normalize_families(families),
    }
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def entry_dir(cache_root: Path, key: str) -> Path:
    return Path(cache_root) / key[:2] / key


def meta_path(directory: Path) -> Path:
    return directory / "meta.json"


def plan_path(directory: Path) -> Path:
    return directory / "query-plan.json"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_key(args: argparse.Namespace) -> int:
    key = cache_key(args.topic, args.review_mode, args.time_range, args.family)
    directory = entry_dir(Path(args.cache_root), key)
    payload = {
        "cache_key": key,
        "cache_dir": str(directory),
        "plan_path": str(plan_path(directory)),
        "hit": plan_path(directory).is_file(),
        "components": {
            "topic": normalize_topic(args.topic),
            "review_mode": args.review_mode,
            "time_range": " ".join(str(args.time_range or "").split()).strip().lower(),
            "families": normalize_families(args.family),
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    key = cache_key(args.topic, args.review_mode, args.time_range, args.family)
    directory = entry_dir(Path(args.cache_root), key)
    plan_file = plan_path(directory)
    hit = plan_file.is_file()
    result: dict[str, Any] = {
        "hit": hit,
        "cache_key": key,
        "cache_dir": str(directory),
        "plan_path": str(plan_file) if hit else None,
        "skip_dynamic_llm": hit,
        "skip_persona_llm": hit,
        "persona_regen_on_coverage_gaps_still_allowed": True,
        "advice": (
            "Cache hit: reuse the plan; skip dynamic/persona LLM. "
            "Still run suggest_persona_regeneration.py only when coverage dimensions fail."
            if hit
            else "Cache miss: run deterministic build_query_plan.py; add dynamic/persona LLM only if needed."
        ),
    }
    if hit and meta_path(directory).is_file():
        result["meta"] = json.loads(meta_path(directory).read_text(encoding="utf-8"))
    if hit and args.output:
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(plan_file, dest)
        result["copied_to"] = str(dest)
    if args.json or args.output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif hit:
        sys.stdout.write(plan_file.read_text(encoding="utf-8"))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    return 0 if hit else 2


def cmd_put(args: argparse.Namespace) -> int:
    key = cache_key(args.topic, args.review_mode, args.time_range, args.family)
    directory = entry_dir(Path(args.cache_root), key)
    plan_file = plan_path(directory)
    if plan_file.exists() and not args.overwrite:
        print(f"error: cache entry exists ({plan_file}); pass --overwrite", file=sys.stderr)
        return 1
    src = Path(args.plan)
    if not src.is_file():
        print(f"error: plan not found: {src}", file=sys.stderr)
        return 1
    # Validate JSON object
    plan = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(plan, dict):
        print("error: plan must be a JSON object", file=sys.stderr)
        return 1
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, plan_file)
    meta = {
        "schema_version": 1,
        "cache_key": key,
        "topic": args.topic,
        "review_mode": args.review_mode,
        "time_range": args.time_range,
        "families": normalize_families(args.family),
        "had_dynamic_llm": bool(args.had_dynamic),
        "had_persona_llm": bool(args.had_persona),
        "stored_at": datetime.now(timezone.utc).isoformat(),
        "source_plan": str(src),
    }
    write_json(meta_path(directory), meta)
    print(json.dumps({"stored": True, "cache_key": key, "plan_path": str(plan_file), "meta": meta}, ensure_ascii=False, indent=2))
    return 0


def cmd_invalidate(args: argparse.Namespace) -> int:
    key = cache_key(args.topic, args.review_mode, args.time_range, args.family)
    directory = entry_dir(Path(args.cache_root), key)
    if directory.exists():
        shutil.rmtree(directory)
        print(json.dumps({"invalidated": True, "cache_key": key}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"invalidated": False, "cache_key": key, "reason": "missing"}, ensure_ascii=False, indent=2))
    return 0


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in the dispatcher."""
    if args.command == "key":
        return cmd_key(args)
    if args.command == "get":
        return cmd_get(args)
    if args.command == "put":
        return cmd_put(args)
    if args.command == "invalidate":
        return cmd_invalidate(args)
    print(f"unknown command: {args.command}", file=sys.stderr)
    return 1

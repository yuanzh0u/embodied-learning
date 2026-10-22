"""Scan evidence/**/evidence.jsonl and report the next available event ID per prefix.

Also reserves prefixes for a run (``--claim-prefix``): a claim file under
``<kb-root>/.claims/event-prefix/`` is an O_EXCL-created permanent reservation,
so two concurrent runs with the same TOPIC8+year cannot both project the same
IDs. Claims are reservations, not locks — they are never garbage-collected.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

from embodied_learning import locks
from embodied_learning.utils.layout import default_kb_root

EVENT_ID = re.compile(r"^(?P<prefix>.+)-(?P<seq>\d{4})$")
CLAIM_KIND = "event-prefix"



def scan(evidence_dir: Path) -> dict[str, int]:
    highest: dict[str, int] = {}
    for jsonl in sorted(evidence_dir.glob("*/evidence.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            match = EVENT_ID.match(str(event.get("event_id") or ""))
            if not match:
                continue
            prefix = match.group("prefix")
            seq = int(match.group("seq"))
            if seq > highest.get(prefix, 0):
                highest[prefix] = seq
    return highest


def _claims_root(kb_root: Path) -> Path:
    return kb_root / locks.CLAIMS_DIRNAME / CLAIM_KIND


def claim_prefix(kb_root: Path, prefix: str, run: str, topic: str = "") -> int:
    """Reserve ``prefix`` for ``run``. Exit 0 = claimed; 4 = already taken."""

    payload = {"prefix": prefix, "run": run, "topic": topic}
    taken = locks.claim(kb_root, f"{CLAIM_KIND}/{prefix}", payload)
    if taken:
        record = locks.read_owner(_claims_root(kb_root) / f"{prefix}.json")
        print(f"claimed {prefix} for run {run} -> {record}")
        return 0
    holder = locks.read_owner(_claims_root(kb_root) / f"{prefix}.json")
    print(
        f"prefix {prefix} already claimed by run {holder.get('run') if holder else '?'}"
        f" (host {holder.get('host') if holder else '?'});"
        f" choose a different prefix or release the claim",
        file=sys.stderr,
    )
    return 4


def release_prefix(kb_root: Path, prefix: str) -> int:
    target = _claims_root(kb_root) / f"{prefix}.json"
    holder = locks.read_owner(target)
    if not holder:
        print(f"no claim found for {prefix}")
        return 0
    locks.release_claim(kb_root, f"{CLAIM_KIND}/{prefix}", claim_id=str(holder.get("claim_id") or ""))
    print(f"released {prefix} (was held by run {holder.get('run')})")
    return 0


def list_claims(kb_root: Path) -> list[dict]:
    root = _claims_root(kb_root)
    if not root.is_dir():
        return []
    claims = []
    for path in sorted(root.glob("*.json")):
        record = locks.read_owner(path)
        if record:
            claims.append(record)
    return claims


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
    evidence_dir = Path(args.evidence_dir)
    if args.kb_root:
        kb_root = Path(args.kb_root).expanduser()
    else:
        kb_root = evidence_dir.parent
    claims = list_claims(kb_root)

    if args.release:
        if not args.claim_prefix:
            print("--release requires --claim-prefix", file=sys.stderr)
            return 2
        return release_prefix(kb_root, args.claim_prefix)

    if args.claim_prefix:
        if not args.run:
            print("--claim-prefix requires --run", file=sys.stderr)
            return 2
        code = claim_prefix(kb_root, args.claim_prefix, args.run, args.topic or "")
        claims = list_claims(kb_root)  # refresh after the claim attempt
        if code:
            return code

    if args.claims:
        if args.json:
            print(json.dumps(claims, ensure_ascii=False, indent=2))
        else:
            if not claims:
                print("no event-prefix claims")
            for record in claims:
                print(
                    f"{record.get('prefix')}: run {record.get('run')}"
                    f" (host {record.get('host')}, claimed {time.strftime('%Y-%m-%d %H:%M', time.localtime(float(record.get('ts') or 0)))})"
                )
        return 0

    highest = scan(evidence_dir)
    claimed_by = {str(record.get("prefix")): record for record in claims}
    if args.prefix:
        used = highest.get(args.prefix, 0)
        report = {args.prefix: {"max_used": used, "next_id": f"{args.prefix}-{used + 1:04d}"}}
        if args.prefix in claimed_by:
            report[args.prefix]["claimed_by_run"] = claimed_by[args.prefix].get("run")
    else:
        report = {
            prefix: {"max_used": used, "next_id": f"{prefix}-{used + 1:04d}"}
            for prefix, used in sorted(highest.items())
        }
        for prefix in claimed_by:
            report.setdefault(prefix, {"max_used": 0, "next_id": f"{prefix}-0001"})
            report[prefix]["claimed_by_run"] = claimed_by[prefix].get("run")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if not report:
            print("no event IDs found")
        for prefix, info in report.items():
            claim_note = f" [claimed by run {info['claimed_by_run']}]" if info.get("claimed_by_run") else ""
            print(f"{prefix}: max used {info['max_used']:04d}, next {info['next_id']}{claim_note}")
    return 0

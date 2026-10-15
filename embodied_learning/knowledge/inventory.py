"""KB inventory: one-shot counts over runs, pool papers, and published topics.

Answers "how many runs ran, how many papers are deep-read, how many have full
text" for one kb-root. Library entry is :func:`kb_stats`; the CLI is
``wiki.py kb-stats``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from typing import Any

from embodied_learning.knowledge.model import KnowledgeBase

SCHEMA_VERSION = 1


def kb_stats(kb: KnowledgeBase, *, include_runs: bool = False) -> dict[str, Any]:
    """Aggregate inventory for ``kb``. ``runs_detail`` appears only when asked."""
    runs = kb.runs()
    papers = kb.papers()
    registered = kb.catalog().run_names()

    by_status: dict[str, int] = {}
    by_mode: dict[str, int] = {}
    total_events = 0
    sum_evidence_papers = 0
    sum_candidate = 0
    sum_full_text = 0
    registered_count = 0
    runs_detail: list[dict[str, Any]] = []

    for run in runs:
        status = run.status or "unknown"
        mode = run.review_mode or "unknown"
        by_status[status] = by_status.get(status, 0) + 1
        by_mode[mode] = by_mode.get(mode, 0) + 1
        manifest = run.manifest
        # event_count is authoritative from run.json; recount from evidence.jsonl
        # lines so a missing file degrades to 0 instead of a stale stamp.
        events = len(run.events())
        total_events += events
        sum_evidence_papers += manifest.evidence_papers or 0
        sum_candidate += manifest.candidate_count or 0
        sum_full_text += manifest.full_text_count or 0
        is_registered = run.name in registered
        registered_count += 1 if is_registered else 0

        summary = run.reading_summary() or {}
        ledger = run.reading_ledger()
        if include_runs:
            runs_detail.append(
                {
                    "run": run.name,
                    "topic": run.topic,
                    "status": run.status,
                    "review_mode": run.review_mode,
                    "event_count": events,
                    "evidence_papers": manifest.evidence_papers,
                    "candidate_count": manifest.candidate_count,
                    "full_text_count": manifest.full_text_count,
                    "ledger_papers": len(ledger),
                    "deep_read_count": summary.get("deep_read_count"),
                    "registered": is_registered,
                    "path": str(run.path),
                }
            )

    full_text = sum(1 for p in papers if p.has_full_text)
    deep_read = sum(1 for p in papers if p.has_deep_read)
    both = sum(1 for p in papers if p.has_full_text and p.has_deep_read)
    not_in_index = sorted(p.dir_name for p in papers if not p.in_index)

    ledger_rows = 0
    accepted_rows = 0
    runs_with_ledger = 0
    runs_with_summary = 0
    sum_deep_read_count = 0
    for run in runs:
        ledger = run.reading_ledger()
        if ledger:
            runs_with_ledger += 1
            ledger_rows += len(ledger)
            accepted_rows += sum(1 for row in ledger if row.get("status") == "accepted")
        summary = run.reading_summary()
        if summary:
            runs_with_summary += 1
            sum_deep_read_count += int(summary.get("deep_read_count") or 0)

    manifest = kb.snapshot_manifest() or {}
    stats = manifest.get("stats") if isinstance(manifest.get("stats"), dict) else {}
    wiki_block: dict[str, Any] = {
        "published_topics": len(kb.wiki_topics()),
        "superseded_versions": int(stats.get("superseded_versions") or 0),
        "snapshot_id": str(manifest.get("snapshot_id") or "")
        or str((_read_current_id(kb)) or ""),
    }

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "kb_root": str(kb.root),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "runs": {
            "total": len(runs),
            "by_status": by_status,
            "by_review_mode": by_mode,
            "registered_in_catalog": registered_count,
            "unregistered": len(runs) - registered_count,
            "total_events": total_events,
            "sum_evidence_papers": sum_evidence_papers,
            "sum_candidate_count": sum_candidate,
            "sum_full_text_count": sum_full_text,
        },
        "pool": {
            "pool_root": str(kb.pool_dir),
            "papers": len(papers),
            "in_index": sum(1 for p in papers if p.in_index),
            "not_in_index": not_in_index,
            "full_text": full_text,
            "deep_read": deep_read,
            "full_text_and_deep_read": both,
            "deep_read_without_full_text": deep_read - both,
        },
        "wiki": wiki_block,
        "reading": {
            "runs_with_ledger": runs_with_ledger,
            "ledger_rows": ledger_rows,
            "accepted_rows": accepted_rows,
            "runs_with_summary": runs_with_summary,
            "sum_deep_read_count": sum_deep_read_count,
        },
    }
    if include_runs:
        payload["runs_detail"] = runs_detail
    return payload


def _read_current_id(kb: KnowledgeBase) -> str:
    try:
        data = json.loads((kb.wiki_data_dir / "current.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(data.get("snapshot_id") or "") if isinstance(data, dict) else ""


def render(payload: dict[str, Any], *, runs_detail: bool = False) -> str:
    runs = payload.get("runs", {})
    pool = payload.get("pool", {})
    wiki = payload.get("wiki", {})
    reading = payload.get("reading", {})
    lines = [
        f"KB 盘点：{payload.get('kb_root', '')}",
        "",
        f"runs（evidence/*/run.json）  {runs.get('total', 0)}"
        f"   settled {runs.get('by_status', {}).get('settled', 0)}"
        f" / 其他 {sum(v for k, v in runs.get('by_status', {}).items() if k != 'settled')}",
    ]
    modes = runs.get("by_review_mode", {})
    if modes:
        lines.append("    按 mode：" + " · ".join(f"{k} {v}" for k, v in sorted(modes.items())))
    lines.append(
        f"    catalog 已登记 {runs.get('registered_in_catalog', 0)}"
        f" · 未登记 {runs.get('unregistered', 0)}"
    )
    lines.append(f"events（evidence.jsonl 行数）  {runs.get('total_events', 0)}")
    lines.append(f"evidence papers（run.json 求和）  {runs.get('sum_evidence_papers', 0)}")
    lines.append("")
    lines.append(f"pool（{pool.get('pool_root', '')}）  {pool.get('papers', 0)} 篇")
    lines.append(
        f"    全文 paper.md   {pool.get('full_text', 0)}"
        f"    深读 note.json   {pool.get('deep_read', 0)}"
        f"    两者兼有   {pool.get('full_text_and_deep_read', 0)}"
    )
    not_in_index = pool.get("not_in_index") or []
    preview = "、".join(not_in_index[:3]) + ("…" if len(not_in_index) > 3 else "")
    lines.append(
        f"    深读无全文   {pool.get('deep_read_without_full_text', 0)}"
        f"    未入 index.json   {len(not_in_index)}"
        + (f"（{preview}）" if preview else "")
    )
    lines.append("")
    lines.append(
        f"wiki 已发布话题   {wiki.get('published_topics', 0)}"
        f"（superseded {wiki.get('superseded_versions', 0)}）"
    )
    lines.append("")
    lines.append(
        f"reading（跨 run 行数，非去重）  ledger 行 {reading.get('ledger_rows', 0)}"
        f" / accepted {reading.get('accepted_rows', 0)}"
        f"（{reading.get('runs_with_ledger', 0)} 个 run 含 ledger）"
    )

    detail = payload.get("runs_detail") or []
    if runs_detail and detail:
        lines.append("")
        lines.append("逐 run：")
        lines.append(f"  {'run':<58} {'mode':<10} {'status':<10} {'events':>6} {'papers':>6} {'dr':>4}")
        for row in detail:
            name = row.get("run", "")
            if len(name) > 58:
                name = name[:55] + "…"
            lines.append(
                f"  {name:<58} {str(row.get('review_mode') or ''):<10}"
                f" {str(row.get('status') or ''):<10}"
                f" {row.get('event_count', 0):>6}"
                f" {str(row.get('evidence_papers') if row.get('evidence_papers') is not None else '—'):>6}"
                f" {str(row.get('deep_read_count') if row.get('deep_read_count') is not None else '—'):>4}"
            )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/wiki.py."""
    kb = KnowledgeBase.open(args.kb_root)
    if not kb.root.is_dir():
        print(f"KB root 不存在：{kb.root}", file=sys.stderr)
        return 1
    try:
        payload = kb_stats(kb, include_runs=bool(getattr(args, "runs_detail", False)))
    except NotADirectoryError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if getattr(args, "json", False):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if not (kb.evidence_dir.is_dir() or kb.pool_dir.is_dir()):
            print("（空 KB：无 evidence/ 或 pool/）")
        print(render(payload, runs_detail=bool(getattr(args, "runs_detail", False))))
    return 0

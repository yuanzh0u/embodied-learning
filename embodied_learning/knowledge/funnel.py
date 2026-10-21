"""The retrieval→evidence funnel as a first-class, publishable artifact.

A review run's most expensive judgment is *which candidate papers matter*:
the driver retrieves a registry, the selector keeps a screening queue, full
text recovery drops some, deep reading keeps fewer, and only audited papers
become citable evidence. Those counts (and the selector's per-paper reasons)
used to live only inside a single ``run.py status`` invocation — nothing
survived ``finalize``, so downstream consumers could not ask "what did this
run actually keep, and why?".

:func:`build_funnel` derives the six layers from the run directory alone and
:func:`write_funnel` stores them as ``funnel.json`` beside ``run.json``;
``finalize`` publishes it with the rest of the bundle. This module also owns
the read side (``kb-stats`` summary + ``wiki.py kb-funnel`` queries), so the
file format has exactly one owner.

Design notes:
- **Layers are derived from disk, never from flags.** ``null`` means the
  source artifact does not exist; a ``--skip-deep-read`` rerun that finds
  earlier notes still reports them.
- Deep read counts *attempts* (notes ∪ ``.failed.json``), not the queue limit:
  a killed run must not report the full budget as read.
- Seeds are forced to the front of the deep-read queue and may sit outside the
  selection, so the funnel is not strictly nested;
  ``detail.seeds_outside_screened`` makes that visible.
- ``abstract`` counts the abstract-tier file (same scope as
  ``run.json.abstract_papers``) and deliberately overlaps ``evidence``; the
  appendix renderer de-duplicates, and a third counting convention would be
  worse than the overlap.
- Keep module-level imports light: ``scripts/wiki.py`` imports every
  ``_MODULES`` entry to build parsers, ``serve`` included.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

from embodied_learning.config import CITED_PAPER_FLOORS, FUNNEL_LAYER_PAPER_CAP

FUNNEL_FILENAME = "funnel.json"
SCHEMA_VERSION = 1
LAYERS = ("registry", "screened", "full_text", "deep_read", "evidence", "abstract")
ABSTRACT_TIER_STEM = "abstract-tier"
# Numeric orderings for run-level rows; ``None`` always sorts last.
SORTS = ("run", "screened", "screen_rate", "evidence_yield")


# ---- readers -----------------------------------------------------------------


def _read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_jsonl(path: Path) -> list[dict]:
    """Malformed lines are skipped: the funnel is a summary, not a validation
    gate (``check-kb-links`` / ``audit-citations`` own integrity)."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out: list[dict] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            out.append(record)
    return out


def _read_ids(path: Path) -> set[str] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    return {line.strip() for line in lines if line.strip()}


def _plain_id(name: str, suffix: str = ".json") -> str:
    """``<id><suffix>`` → ``<id>``; anything that is not a plain id is dropped."""
    if not name.endswith(suffix):
        return ""
    paper_id = name[: -len(suffix)]
    if not paper_id or len(paper_id) > 64 or any(ch in paper_id for ch in "/\\\0"):
        return ""
    return paper_id


def _names(directory: Path) -> list[Path]:
    """``iterdir`` not ``glob``: the driver test harness patches ``Path.glob``."""
    try:
        return sorted(directory.iterdir())
    except OSError:
        return []


# ---- layer derivation --------------------------------------------------------


def _registry_layer(run_dir: Path) -> tuple[list[str], dict[str, dict], int | None]:
    """(ids, metadata by id, stage count). A trimmed bundle may carry only a
    count — then the list is empty but the stage is still known."""
    registry = _read_json(run_dir / "candidate-registry.json")
    if not registry:
        return [], {}, None
    records: dict[str, dict] = {}
    for record in registry.get("candidates") or []:
        if not isinstance(record, dict):
            continue
        paper_id = str(record.get("arxiv_id") or "").strip()
        if paper_id:
            records[paper_id] = record
    count = registry.get("candidate_count")
    if not isinstance(count, int):
        count = len(records) if records else None
    return list(records), records, count


def _extraction(run_dir: Path) -> dict | None:
    path = run_dir / "extraction-summary.json"
    return _read_json(path) if path.is_file() else None


def _full_text_layer(extraction: dict | None, screened: set[str] | None) -> list[str]:
    """Eligible ids, intersected with the selection when one is known: an older
    extraction summary may predate a re-run screening set."""
    if extraction is None:
        return []
    ids: list[str] = []
    for result in extraction.get("results") or []:
        if not isinstance(result, dict) or not result.get("evidence_eligible"):
            continue
        paper_id = str(result.get("paper_id") or "").strip()
        if paper_id and (screened is None or paper_id in screened):
            ids.append(paper_id)
    return list(dict.fromkeys(ids))


def _deep_read_layer(run_dir: Path) -> tuple[list[str] | None, dict[str, int]]:
    """(attempted ids, audit counters). ``None`` = the stage never ran."""
    notes_dir = run_dir / "paper-notes"
    if not notes_dir.is_dir():
        return None, {"pass": 0, "needs_review": 0, "failed": 0}
    attempted: list[str] = []
    statuses: list[str] = []
    failed = 0
    for path in _names(notes_dir):
        name = path.name
        if name.endswith(".audit.json"):
            if _plain_id(name, ".audit.json"):
                statuses.append(str(_read_json(path).get("status") or "?"))
            continue
        if name.endswith(".failed.json"):
            if _plain_id(name, ".failed.json"):
                attempted.append(_plain_id(name, ".failed.json"))
                failed += 1
            continue
        paper_id = _plain_id(name)
        if paper_id:
            attempted.append(paper_id)
    return list(dict.fromkeys(attempted)), {
        "pass": sum(1 for status in statuses if status == "pass"),
        "needs_review": sum(1 for status in statuses if status == "needs-review"),
        "failed": failed,
    }


def _evidence_layer(run_dir: Path) -> tuple[list[str] | None, list[str] | None, int]:
    """(full-text evidence paper ids, abstract ids, full-text event count)."""
    evidence_dir = run_dir / "evidence"
    if not evidence_dir.is_dir():
        return None, None, 0
    full_text: list[str] = []
    events = 0
    for path in _names(evidence_dir):
        if not path.name.endswith(".jsonl") or path.stem == ABSTRACT_TIER_STEM:
            continue
        records = _read_jsonl(path)
        if records:
            full_text.append(path.stem)
            events += len(records)
    abstract: list[str] | None = None
    abstract_path = evidence_dir / f"{ABSTRACT_TIER_STEM}.jsonl"
    if abstract_path.is_file():
        abstract = []
        for record in _read_jsonl(abstract_path):
            paper = record.get("paper") if isinstance(record.get("paper"), dict) else {}
            paper_id = str((paper or {}).get("arxiv_id") or "").strip()
            if paper_id:
                abstract.append(paper_id)
        abstract = list(dict.fromkeys(abstract))
    return full_text, abstract, events


def _selection(run_dir: Path) -> dict:
    screening = _read_json(run_dir / "screening.json")
    rule = screening.get("selection_rule")
    rule = rule if isinstance(rule, dict) else {}
    reasons: dict[str, str] = {}
    for record in screening.get("candidates") or []:
        if not isinstance(record, dict):
            continue
        paper_id = str(record.get("arxiv_id") or "").strip()
        reason = " ".join(str(record.get("selection_reason") or "").split())
        if paper_id and reason:
            reasons[paper_id] = reason
    return {
        "screen_limit": rule.get("limit") if isinstance(rule.get("limit"), int) else None,
        "selection_strategy": str(rule.get("strategy") or "") or None,
        "selection_detail": str(rule.get("detail") or "") or None,
        "reasons": reasons,
    }


def _paper_meta(layers: dict[str, list[str] | None], records: dict[str, dict],
                reasons: dict[str, str]) -> dict[str, dict]:
    """Deduplicated metadata for every id that appears in any layer."""
    papers: dict[str, dict] = {}
    for name in LAYERS:
        for paper_id in layers.get(name) or []:
            if paper_id in papers:
                continue
            record = records.get(paper_id) or {}
            papers[paper_id] = {
                "title": str(record.get("title") or ""),
                "published": str(record.get("published") or ""),
                "reason": reasons.get(paper_id, ""),
            }
    return papers


def _truncate(payload: dict) -> int:
    """Apply ``FUNNEL_LAYER_PAPER_CAP``; returns how many ids were dropped."""
    dropped = 0
    for name in LAYERS:
        ids = payload["layers"].get(name)
        if ids is not None and len(ids) > FUNNEL_LAYER_PAPER_CAP:
            dropped += len(ids) - FUNNEL_LAYER_PAPER_CAP
            payload["layers"][name] = ids[:FUNNEL_LAYER_PAPER_CAP]
    if len(payload["papers"]) > FUNNEL_LAYER_PAPER_CAP:
        dropped += len(payload["papers"]) - FUNNEL_LAYER_PAPER_CAP
        payload["papers"] = dict(list(payload["papers"].items())[:FUNNEL_LAYER_PAPER_CAP])
    payload["truncated"] = dropped > 0
    return dropped


# ---- build / write / read ----------------------------------------------------


def build_funnel(
    run_dir: Path,
    *,
    run: str,
    topic: str,
    review_mode: str,
    summary: dict | None = None,
    skipped: list[str] | None = None,
) -> dict[str, Any]:
    """Derive the funnel from the run directory. Pure read: no writes, no pool
    access, no network. ``skipped`` records stages *this invocation* skipped;
    it never nulls a layer whose artifacts exist (D8)."""
    run_dir = Path(run_dir)
    summary = summary if isinstance(summary, dict) else {}

    registry_ids, registry_records, candidate_count = _registry_layer(run_dir)
    screened = _read_ids(run_dir / "screening-ids.txt")
    extraction = _extraction(run_dir)
    full_text_ids = _full_text_layer(extraction, screened)
    deep_read_ids, audit_counts = _deep_read_layer(run_dir)
    evidence_ids, abstract_ids, evidence_events = _evidence_layer(run_dir)
    selection = _selection(run_dir)

    layers: dict[str, list[str] | None] = {
        "registry": registry_ids,
        "screened": sorted(screened) if screened is not None else None,
        "full_text": full_text_ids if extraction is not None else None,
        "deep_read": deep_read_ids,
        "evidence": evidence_ids,
        "abstract": abstract_ids,
    }
    stages: dict[str, int | None] = {
        "candidates": candidate_count,
        "screened": len(screened) if screened is not None else None,
        "full_text": len(full_text_ids) if extraction is not None else None,
        "deep_read": len(deep_read_ids) if deep_read_ids is not None else None,
        "evidence_papers": len(evidence_ids) if evidence_ids is not None else None,
        "evidence_events": evidence_events if evidence_ids is not None else None,
        "abstract_papers": len(abstract_ids) if abstract_ids is not None else None,
        "abstract_events": None,
    }
    abstract_path = run_dir / "evidence" / f"{ABSTRACT_TIER_STEM}.jsonl"
    if abstract_path.is_file():
        stages["abstract_events"] = len(_read_jsonl(abstract_path))

    # held = selected but no usable full text, split from channel-down skips
    held = channel_down = 0
    if extraction is not None and screened is not None:
        states = {
            str(result.get("paper_id")): str(result.get("state") or "")
            for result in extraction.get("results") or []
            if isinstance(result, dict) and result.get("paper_id")
        }
        eligible = set(full_text_ids)
        for paper_id in screened:
            if paper_id in eligible:
                continue
            if states.get(paper_id) == "channel-down":
                channel_down += 1
            else:
                held += 1

    seeds = {str(seed).strip() for seed in (summary.get("seed_ids") or []) if str(seed).strip()}
    seeds_outside = 0
    if deep_read_ids is not None and screened is not None:
        seeds_outside = len({paper_id for paper_id in deep_read_ids if paper_id in seeds} - screened)

    floor = CITED_PAPER_FLOORS.get(str(review_mode or ""))
    evidence_papers = stages["evidence_papers"]
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run": run,
        "topic": topic,
        "review_mode": review_mode,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "stages": stages,
        "detail": {
            # No cap since 2026-10-20 (selection queues every relevant paper);
            # the key stays for runs settled under the old SCREEN_LIMITS cap,
            # where it records the truncation that produced the queue.
            "screen_limit": selection["screen_limit"],
            "selection_strategy": selection["selection_strategy"],
            "selection_detail": selection["selection_detail"],
            "deep_read_limit": summary.get("deep_read_limit"),
            "deep_read_waitlist": summary.get("deep_read_waitlist"),
            "deep_read_pass": audit_counts["pass"],
            "deep_read_needs_review": audit_counts["needs_review"],
            "deep_read_failed": audit_counts["failed"],
            "held": held,
            "channel_down": channel_down,
            "seeds_outside_screened": seeds_outside,
            "abstract_basis": summary.get("abstract_basis"),
            "abstract_leaked": len(set(abstract_ids or []) - screened) if screened is not None else 0,
            "cited_floor": floor,
            "floor_met": (evidence_papers >= floor)
            if floor is not None and evidence_papers is not None else None,
            "skipped": list(skipped or []),
        },
        "papers": _paper_meta(layers, registry_records, selection["reasons"]),
        "layers": layers,
        "truncated": False,
    }
    _truncate(payload)
    return payload


def write_funnel(payload: dict, run_dir: Path) -> Path:
    """Atomically write ``funnel.json`` into the run directory."""
    from embodied_learning.atomicio import atomic_write_json

    target = Path(run_dir) / FUNNEL_FILENAME
    atomic_write_json(target, payload)
    return target


def read_funnel(run_dir: Path) -> dict | None:
    """The stored funnel, or ``None`` when absent/foreign-schema/unparseable.

    Historical runs (pre-funnel) must degrade to "no data" — never to a guess
    reconstructed from unrelated leftovers."""
    payload = _read_json(Path(run_dir) / FUNNEL_FILENAME)
    if not payload or payload.get("schema_version") != SCHEMA_VERSION:
        return None
    if not isinstance(payload.get("stages"), dict):
        return None
    return payload


# ---- aggregation / query -----------------------------------------------------


def _rate(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or not denominator:
        return None
    return round(numerator / denominator, 4)


def _rates(stages: dict[str, Any]) -> dict[str, float | None]:
    return {
        "screen": _rate(stages.get("screened"), stages.get("candidates")),
        "full_text": _rate(stages.get("full_text"), stages.get("screened")),
        "deep_read": _rate(stages.get("deep_read"), stages.get("full_text")),
        "evidence_yield": _rate(stages.get("evidence_papers"), stages.get("screened")),
    }


def summarize(kb, *, funnels: dict[str, dict | None] | None = None) -> dict[str, Any]:
    """The ``kb-stats`` funnel block: cross-run sums over runs that have data.

    Sums, not distinct papers: the same paper can be selected by two runs and
    the funnel measures *runs*, not the corpus. ``funnels`` lets a caller that
    already read each run's funnel.json pass the map in instead of re-reading."""
    runs = kb.runs()
    sums = {key: 0 for key in (
        "candidates", "screened", "full_text",
        "deep_read", "evidence_papers", "abstract_papers",
    )}
    reported: set[str] = set()
    with_funnel = 0
    for run in runs:
        funnel = funnels.get(run.name) if funnels is not None else read_funnel(run.path)
        if funnel is None:
            continue
        with_funnel += 1
        stages = funnel.get("stages") or {}
        for key in sums:
            value = stages.get(key)
            if isinstance(value, int):
                sums[key] += value
                reported.add(key)
    # A layer no run ever reported stays null instead of reading as 0% (a
    # funnel that never ran deep reading is not a funnel with zero yield).
    rates = {
        "screen": _rate(sums["screened"], sums["candidates"])
        if "screened" in reported else None,
        "full_text": _rate(sums["full_text"], sums["screened"])
        if "full_text" in reported else None,
        "deep_read": _rate(sums["deep_read"], sums["full_text"])
        if "deep_read" in reported else None,
        "evidence_yield": _rate(sums["evidence_papers"], sums["screened"])
        if "evidence_papers" in reported else None,
    }
    return {
        "runs_with_funnel": with_funnel,
        "runs_without_funnel": len(runs) - with_funnel,
        "sums": sums,
        "rates": rates,
        "note": "跨 run 求和口径，非去重；空分母或该层 null 时为 null",
    }


def _matches(run, *, run_name: str | None, topic: str | None, review_mode: str | None) -> bool:
    if run_name and run.name != run_name:
        return False
    if topic and topic.casefold() not in str(run.topic or "").casefold():
        return False
    if review_mode and str(run.review_mode or "") != review_mode:
        return False
    return True


def kb_funnel(
    kb,
    *,
    layer: str | None = None,
    run: str | None = None,
    topic: str | None = None,
    review_mode: str | None = None,
    sort: str = "run",
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Funnel rows. Without ``layer``: one row per matching run (``funnel`` is
    ``None`` for runs that predate the artifact). With ``layer``: one row per
    paper in that layer (``sort`` applies to run-level rows only)."""
    if layer is not None and layer not in LAYERS:
        raise ValueError(f"unknown funnel layer {layer!r}; expected one of {LAYERS}")
    if sort not in SORTS:
        raise ValueError(f"unknown sort {sort!r}; expected one of {SORTS}")

    rows: list[dict[str, Any]] = []
    for review_run in kb.runs():
        if not _matches(review_run, run_name=run, topic=topic, review_mode=review_mode):
            continue
        funnel = read_funnel(review_run.path)
        if layer is None:
            stages = (funnel or {}).get("stages") or {}
            rows.append({
                "run": review_run.name,
                "topic": review_run.topic,
                "review_mode": review_run.review_mode,
                "status": review_run.status,
                "funnel_available": funnel is not None,
                "stages": stages or None,
                "rates": _rates(stages) if funnel is not None else None,
            })
            continue
        if funnel is None:
            continue
        papers = funnel.get("papers") or {}
        for paper_id in (funnel.get("layers") or {}).get(layer) or []:
            meta = papers.get(paper_id) or {}
            rows.append({
                "run": review_run.name,
                "layer": layer,
                "arxiv_id": paper_id,
                "title": meta.get("title") or "",
                "published": meta.get("published") or "",
                "reason": meta.get("reason") or "",
            })

    if layer is None and sort != "run":
        key = {
            "screened": lambda row: (row.get("stages") or {}).get("screened"),
            "screen_rate": lambda row: (row.get("rates") or {}).get("screen"),
            "evidence_yield": lambda row: (row.get("rates") or {}).get("evidence_yield"),
        }[sort]
        # Numeric descending, null last; run name breaks ties for stable output.
        rows.sort(key=lambda row: (key(row) is None, -(key(row) or 0.0), row["run"]))
    return rows[:limit] if limit else rows


def render(rows: list[dict[str, Any]], *, layer: str | None, filters: dict[str, Any]) -> str:
    suffix = "".join(
        f"  {key}={value}" for key, value in filters.items() if value not in (None, "")
    )
    if layer is not None:
        lines = [f"漏斗层：{layer}（{len(rows)} 篇）{suffix}"]
        if not rows:
            lines.append("（无数据：没有匹配的 run，或这些 run 尚无 funnel.json）")
            return "\n".join(lines)
        lines.append(f"  {'run':<46} {'arxiv':<14} {'published':<11} title")
        for row in rows:
            name = row["run"]
            if len(name) > 44:
                name = name[:41] + "…"
            title = row.get("title") or "—"
            if len(title) > 60:
                title = title[:57] + "…"
            lines.append(
                f"  {name:<46} {row.get('arxiv_id', ''):<14}"
                f" {row.get('published', ''):<11} {title}"
            )
            if row.get("reason"):
                lines.append(f"      选文理由：{row['reason']}")
        return "\n".join(lines)

    lines = [f"漏斗（逐 run，{len(rows)} 个 run）{suffix}"]
    if not rows:
        lines.append("（无匹配 run）")
        return "\n".join(lines)
    lines.append(
        f"  {'run':<46} {'mode':<10} {'候选':>5} {'选文':>5} {'全文':>5}"
        f" {'深读':>5} {'证据':>5} {'摘要':>5}  选文率"
    )
    for row in rows:
        name = row["run"]
        if len(name) > 44:
            name = name[:41] + "…"
        if not row.get("funnel_available"):
            lines.append(
                f"  {name:<46} {str(row.get('review_mode') or ''):<10}"
                f"  —  无漏斗数据（旧 run 未生成 funnel.json）"
            )
            continue
        stages = row.get("stages") or {}
        rates = row.get("rates") or {}

        def cell(key: str) -> str:
            value = stages.get(key)
            return "—" if value is None else str(value)

        def pct(value: float | None) -> str:
            return "—" if value is None else f"{value:.0%}"

        lines.append(
            f"  {name:<46} {str(row.get('review_mode') or ''):<10}"
            f" {cell('candidates'):>5} {cell('screened'):>5} {cell('full_text'):>5}"
            f" {cell('deep_read'):>5} {cell('evidence_papers'):>5}"
            f" {cell('abstract_papers'):>5}  {pct(rates.get('screen'))}"
        )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/wiki.py."""
    from embodied_learning.knowledge.model import KnowledgeBase

    kb = KnowledgeBase.open(args.kb_root)
    if not kb.root.is_dir():
        print(f"KB root 不存在：{kb.root}", file=sys.stderr)
        return 1
    layer = getattr(args, "layer", None)
    filters = {
        "run": getattr(args, "run", None),
        "topic": getattr(args, "topic", None),
        "review_mode": getattr(args, "review_mode", None),
    }
    try:
        rows = kb_funnel(
            kb,
            layer=layer,
            run=filters["run"],
            topic=filters["topic"],
            review_mode=filters["review_mode"],
            sort=str(getattr(args, "sort", "run") or "run"),
            limit=int(getattr(args, "limit", 20) or 0),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if getattr(args, "json", False):
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render(rows, layer=layer, filters=filters))
    return 0

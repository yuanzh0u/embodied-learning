#!/usr/bin/env python3
"""Selection strategies: rank a candidate registry into the deep-read queue.

Strategies (``--selection-strategy``):
- ``keywords``: the legacy term-matching scorer (``screening.py``) — kept as
  the mechanical fallback.
- ``bm25``: stdlib BM25 over title+abstract against the topic+focus query.
- ``influence``: registry citation counts (desc), year as tiebreak. Offline
  only — channels without citation metadata degrade honestly (the caller
  falls back to bm25 and reports it).
- ``smart`` (default): abstract evidence for the whole registry + the review
  topic go to ONE one-shot agent that returns the relevant arXiv IDs. The
  count is capped by the mode limit; a shortfall is reported as-is and never
  padded.

Selection replaces the screening stage's role: it produces the same
screening.json / screening-ids.txt artifacts so extraction and deep-read
downstream are unchanged.
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

TOKEN_RE = re.compile(r"[a-z0-9]+")
# One smart-agent call stays inside a comfortable context; larger registries
# are split into full-coverage chunks (every candidate reaches the agent).
SMART_CANDIDATES_PER_CALL = 300
SMART_MAX_ABSTRACT_CHARS = 400


def _tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(str(text or "").lower())


def bm25_scores(registry: dict[str, Any], query: str) -> list[tuple[str, float, dict[str, Any]]]:
    """BM25 (k1=1.5, b=0.75) of registry candidates against ``query``.

    Returns (arxiv_id, score, candidate) for every candidate with a nonzero
    score, best first. Corpus = title + abstract; query = topic (+ focus)."""
    k1, b = 1.5, 0.75
    docs: list[tuple[str, dict[str, Any], Counter, int]] = []
    for candidate in registry.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        arxiv_id = str(candidate.get("arxiv_id") or "").strip()
        if not arxiv_id:
            continue
        tokens = _tokens(
            str(candidate.get("title") or "") + " " + str(candidate.get("summary") or "")
        )
        docs.append((arxiv_id, candidate, Counter(tokens), len(tokens)))
    if not docs:
        return []
    df: Counter = Counter()
    for _, _, counts, _ in docs:
        df.update(counts.keys())
    n_docs = len(docs)
    avgdl = sum(length for _, _, _, length in docs) / n_docs
    query_tokens = _tokens(query)
    scored: list[tuple[str, float, dict[str, Any]]] = []
    for arxiv_id, candidate, counts, length in docs:
        score = 0.0
        for term in query_tokens:
            freq = counts.get(term)
            if not freq:
                continue
            idf = math.log(1 + (n_docs - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * (
                freq * (k1 + 1) / (freq + k1 * (1 - b + b * length / avgdl))
            )
        if score > 0:
            scored.append((arxiv_id, score, candidate))
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored


def bm25_select(registry: dict[str, Any], query: str, limit: int) -> list[dict[str, Any]]:
    return [candidate for _, _, candidate in bm25_scores(registry, query)[: max(0, limit)]]


def influence_select(
    registry: dict[str, Any], limit: int
) -> tuple[list[dict[str, Any]], int]:
    """Citation-count ranking over registry metadata. Returns (selected,
    papers_with_citation_data) — the caller degrades to bm25 when the
    channel carries too little citation signal to fill the queue."""
    with_citations = [
        candidate
        for candidate in registry.get("candidates", [])
        if isinstance(candidate, dict)
        and str(candidate.get("arxiv_id") or "").strip()
        and isinstance(candidate.get("citation_count"), (int, float))
    ]
    with_citations.sort(
        key=lambda c: (-int(c["citation_count"]), str(c.get("published") or ""), str(c.get("arxiv_id")))
    )
    selected = with_citations[: max(0, limit)]
    return selected, len(with_citations)


# ---- smart strategy ---------------------------------------------------------


def _candidate_lines(candidates: list[dict[str, Any]]) -> str:
    lines = []
    for index, candidate in enumerate(candidates, start=1):
        title = " ".join(str(candidate.get("title") or "").split())
        abstract = " ".join(str(candidate.get("summary") or "").split())
        if len(abstract) > SMART_MAX_ABSTRACT_CHARS:
            abstract = abstract[: SMART_MAX_ABSTRACT_CHARS - 1].rstrip() + "…"
        published = str(candidate.get("published") or "")[:10]
        lines.append(f"{index}. [{candidate.get('arxiv_id')}] ({published}) {title} — {abstract}")
    return "\n".join(lines)


SMART_PROMPT_TEMPLATE = (
    "你是综述选题助手。下面是综述话题和候选论文清单（编号 + arXiv ID + 年份 + 标题 + 摘要）。\n"
    "话题：{topic}\n"
    "{focus_line}\n"
    "任务：判断哪些候选与话题真正相关（能进入综述的相关工作或机制讨论，而不是只沾边）。\n"
    "要求：\n"
    "1. 最多输出 {limit} 篇；与话题核心无关的宁缺毋滥。\n"
    "2. 只输出一个 JSON 对象，格式：{{\"relevant\": [{{\"arxiv_id\": \"<id>\", \"reason\": \"<一句话选中理由>\"}}, ...], "
    "\"shortfall_note\": \"<如数量不足，一句话说明为什么其余不相关>\"}}。\n"
    "2b. 每条选中都要给 reason：它与话题哪条主线相关、可贡献什么证据（机制/对比/边界），不要复述标题。\n"
    "3. arXiv ID 必须逐字取自清单方括号内，不要改写。\n"
    "不要输出 JSON 以外的任何内容。\n\n"
    "候选清单：\n{candidates}"
)


def _parse_ids(payload: str, known: set[str]) -> list[str]:
    return [arxiv_id for arxiv_id, _ in _parse_selections(payload, known)]


def _parse_selections(payload: str, known: set[str]) -> list[tuple[str, str]]:
    """(arxiv_id, reason) pairs from the agent JSON. Accepts both the current
    object form ``{"arxiv_id": ..., "reason": ...}`` and the legacy bare-string
    form; unknown IDs are dropped, duplicates keep the first reason."""
    match = re.search(r"\{.*\}", payload, re.DOTALL)
    if not match:
        return []
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return []
    relevant = data.get("relevant") if isinstance(data, dict) else None
    if not isinstance(relevant, list):
        return []
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for item in relevant:
        if isinstance(item, dict):
            arxiv_id = str(item.get("arxiv_id") or item.get("id") or "").strip()
            reason = " ".join(str(item.get("reason") or "").split())
        else:
            arxiv_id = str(item).strip()
            reason = ""
        if arxiv_id in known and arxiv_id not in seen:
            seen.add(arxiv_id)
            out.append((arxiv_id, reason))
    return out


def _salvage_ids(payload: str, known: set[str]) -> list[str]:
    """Last-resort ID recovery from malformed agent output (the model sometimes
    emits code residue inside the JSON array — 20260930 absolute-pose chunk-1
    lost 300 judged papers to this). Bracketed arXiv IDs are extracted and
    filtered against the known set, so hallucinated IDs cannot enter."""
    out: list[str] = []
    for arxiv_id in re.findall(r"\d{4}\.\d{4,5}", payload):
        if arxiv_id in known and arxiv_id not in out:
            out.append(arxiv_id)
    return out


def smart_select(
    registry: dict[str, Any],
    *,
    topic: str,
    focus: str,
    limit: int,
    complete_fn,
    cli: str,
    model: str,
    env: dict[str, str] | None = None,
    cwd=None,
    timeout_s: float = 600.0,
) -> tuple[list[dict[str, Any]], str]:
    """The smart contract: EVERY candidate's abstract reaches the agent.

    Candidates are chunked to context size and each chunk goes to one
    one-shot call with the review topic; the union of relevant IDs is the
    selection. No lexical prefilter may decide what the agent sees — bm25
    cannot tokenize a Chinese topic, and prefiltering by it silently reverts
    smart to the word-matching screen this strategy exists to replace.
    Shortfalls are reported honestly and never padded."""

    candidates = [
        c for c in registry.get("candidates", [])
        if isinstance(c, dict) and str(c.get("arxiv_id") or "").strip()
    ]
    known = {str(c.get("arxiv_id")) for c in candidates}
    if not candidates:
        return [], "empty registry"
    by_id = {str(c.get("arxiv_id")): c for c in candidates}
    focus_line = f"关注重点：{focus}" if focus else ""
    selected: list[tuple[str, str]] = []
    failed_chunks = 0
    salvaged_chunks = 0
    chunks = [
        candidates[i : i + SMART_CANDIDATES_PER_CALL]
        for i in range(0, len(candidates), SMART_CANDIDATES_PER_CALL)
    ]
    for chunk in chunks:
        prompt = SMART_PROMPT_TEMPLATE.format(
            topic=topic, focus_line=focus_line, limit=limit,
            candidates=_candidate_lines(chunk),
        )
        result = complete_fn(
            prompt, timeout_s=timeout_s, cli=cli, model=model,
            cwd=cwd, env=env, label="selection-smart",
        )
        if result.returncode != 0:
            failed_chunks += 1
            continue
        parsed = _parse_selections(result.stdout, known)
        if parsed:
            selected.extend(parsed)
        elif result.stdout.strip():
            # Non-empty output that parses to nothing is NOT an empty verdict:
            # count it as a coverage hole (or salvage IDs) — never let a
            # malformed response silently stand in for "300 papers judged
            # irrelevant" (20260930 absolute-pose chunk-1).
            salvaged = _salvage_ids(result.stdout, known)
            if salvaged:
                selected.extend((arxiv_id, "") for arxiv_id in salvaged)
                salvaged_chunks += 1
            else:
                failed_chunks += 1
    detail_parts = [
        f"smart selected {len(selected)}/{len(candidates)} considered "
        f"({len(chunks)} full-coverage chunk(s))"
    ]
    if salvaged_chunks:
        detail_parts.append(
            f"{salvaged_chunks}/{len(chunks)} chunk(s) malformed — IDs salvaged, reasons lost"
        )
    if failed_chunks:
        detail_parts.append(f"{failed_chunks}/{len(chunks)} chunk(s) failed — coverage incomplete")
    # Dedup, cap, and resolve to candidate records carrying their selection
    # reason (debug surface in screening.json); if fewer than the limit came
    # back relevant, that is the honest answer (never padded).
    ordered = list(dict.fromkeys(selected))[: max(0, limit)]
    out = []
    for arxiv_id, reason in ordered:
        record = dict(by_id[arxiv_id])
        record["selection_reason"] = reason
        out.append(record)
    if len(out) < limit:
        detail_parts.append(f"shortfall: only {len(out)} relevant (limit {limit}), not padded")
    return out, "; ".join(detail_parts)


def to_screening_artifacts(selected: list[dict[str, Any]], detail: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Screening.json entries + id list in the exact shape downstream
    (extraction queue, registry screening updates) expects."""
    rows = []
    ids = []
    for candidate in selected:
        arxiv_id = str(candidate.get("arxiv_id") or "").strip()
        if not arxiv_id:
            continue
        rows.append({
            "arxiv_id": arxiv_id,
            "title": candidate.get("title") or "",
            "status": "full-text-queued",
            "selection_detail": detail,
            "selection_reason": " ".join(str(candidate.get("selection_reason") or "").split()),
        })
        ids.append(arxiv_id)
    return rows, ids


def md_escape_detail(value: str) -> str:
    return " ".join(str(value or "").split()).replace("|", "\\|")


def render_selection_markdown(
    strategy: str, detail: str, selected: list[dict[str, Any]], registry_count: int
) -> str:
    """Screening-queue markdown for the selection strategies (the keywords
    renderer in ``screening.py`` stays the legacy shape's owner)."""
    lines = [
        "# Full-text screening queue",
        "",
        f"- Candidate registry: {registry_count} papers",
        f"- Selection strategy: `{strategy}` ({detail})",
        f"- Queued for full text: {len(selected)} papers",
        "- This is priority screening only; queued papers are not accepted evidence.",
        "",
        "| Rank | arXiv | Score | Title | Selection note |",
        "|---:|---|---|---|---|",
    ]
    for rank, candidate in enumerate(selected, start=1):
        title = " ".join(str(candidate.get("title") or "").split()).replace("|", "\\|")
        note = md_escape_detail(candidate.get("selection_reason") or detail)
        lines.append(
            f"| {rank} | {candidate.get('arxiv_id')} |  | {title} | {note} |"
        )
    return "\n".join(lines) + "\n"


def run_select(
    registry_path: str,
    strategy: str,
    topic: str,
    focus: str,
    limit: int,
    output_screening: str,
    output_ids: str,
    output_markdown: str | None = None,
    terms: str = "",
    *,
    cli: str | None = None,
    model: str | None = None,
    timeout_s: float = 600.0,
    complete_fn=None,
) -> int:
    """CLI driver behind ``search.py select-candidates``: rank the registry with
    one non-keywords strategy and write the same screening artifacts the legacy
    screen-candidates emits, so extraction/deep-read downstream are unchanged.

    Returns the process exit code (0 when candidates were queued, 2 otherwise)."""
    if strategy == "keywords":
        print("keywords 策略走 screen-candidates；select-candidates 不实现词匹配筛选", file=sys.stderr)
        return 2
    from embodied_learning.atomicio import atomic_write_text

    registry = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    # BM25 tokenizes Latin only (abstracts are English); a pure-Chinese topic
    # must be augmented with the run's English terms or every query scores 0.
    query = " ".join(part for part in (topic, focus, terms.replace(",", " ")) if part.strip())
    if strategy == "influence":
        selected, with_data = influence_select(registry, limit)
        parts = [f"influence ranked {with_data} papers with citation data"]
        if len(selected) < limit:
            # Offline honesty: a channel without citation metadata cannot fill
            # the queue by influence alone — bm25 covers the remaining slots
            # and the detail says so (nothing is padded silently).
            chosen = {str(c.get("arxiv_id")) for c in selected}
            selected = selected + [
                candidate
                for _, _, candidate in bm25_scores(registry, query)
                if str(candidate.get("arxiv_id")) not in chosen
            ][: max(0, limit - len(selected))]
            parts.append(f"influence degraded to bm25 (citation data: {with_data} papers)")
        detail = "; ".join(parts)
    elif strategy == "bm25":
        selected = bm25_select(registry, query, limit)
        detail = f"bm25 selected {len(selected)} for topic+focus query"
    elif strategy == "smart":
        from embodied_learning.harness.claude import (
            DRIVER_AGENT_MODEL,
            complete,
            isolated_claude_env,
            resolve_cli,
        )

        cli = cli or resolve_cli()
        if not cli:
            print("claude CLI 不存在，smart 选文无法执行（可改用 --selection-strategy bm25）", file=sys.stderr)
            return 2
        selected, detail = smart_select(
            registry,
            topic=topic,
            focus=focus,
            limit=limit,
            complete_fn=complete_fn or complete,
            cli=cli,
            model=model or DRIVER_AGENT_MODEL,
            env=isolated_claude_env(),
            cwd=None,  # the driver spawns this entry with cwd=kb-root
            timeout_s=timeout_s,
        )
    else:
        print(f"unknown selection strategy: {strategy}", file=sys.stderr)
        return 2
    rows, ids = to_screening_artifacts(selected, detail)
    screening = {
        "version": 1,
        "candidate_registry": registry_path,
        "selection_rule": {"strategy": strategy, "detail": detail, "limit": limit},
        "candidates": rows,
    }
    atomic_write_text(
        Path(output_screening), json.dumps(screening, ensure_ascii=False, indent=2) + "\n"
    )
    atomic_write_text(Path(output_ids), "".join(f"{arxiv_id}\n" for arxiv_id in ids))
    if output_markdown:
        atomic_write_text(
            Path(output_markdown),
            render_selection_markdown(
                strategy, detail, selected, int(registry.get("candidate_count") or 0)
            ),
        )
    print(f"Queued {len(rows)} of {registry.get('candidate_count', 0)} candidates for full-text recovery ({strategy}).")
    return 0 if rows else 2

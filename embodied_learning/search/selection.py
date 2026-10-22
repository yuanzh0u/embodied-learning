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
  topic go to chunked one-shot agent calls that return the relevant arXiv IDs.
  There is no count cap and no relevance score: everything judged relevant is
  queued for full-text recovery, in retrieval order.
- ``smart-jev``: the same full-coverage judgement asked of a decision model
  (System One / jev) instead of the execution model. One typed yes/no question
  per candidate, many questions per request, keep the papers whose probability
  clears ``SMART_JEV_RELEVANCE_THRESHOLD``. Seconds, not minutes, for a
  registry of hundreds — see harness/claude.judge_questions.

Selection produces the screening queue in RETRIEVAL order (the registry's
discovery order), not the agent's output order — the queue's order becomes the
deep-read order, and deep reading is the only stage that truncates.

Selection replaces the screening stage's role: it produces the same
screening.json / screening-ids.txt artifacts so extraction and deep-read
downstream are unchanged.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from embodied_learning.harness.prompt import (
    SMART_JEV_CLAIM,
    SMART_JEV_STATE,
    SMART_SELECTION_PROMPT,
)
from embodied_learning.config import (
    SELECTION_TIMEOUT_S,
    SMART_CANDIDATE_CHARS_PER_CALL,
    SMART_CANDIDATES_PER_CALL,
    SMART_JEV_CHARS_PER_CALL,
    SMART_JEV_QUESTIONS_PER_CALL,
    SMART_JEV_RELEVANCE_THRESHOLD,
    SMART_MAX_ABSTRACT_CHARS,
    SYSTEM_ONE_MODEL,
)

TOKEN_RE = re.compile(r"[a-z0-9]+")
# One smart-agent call stays inside a comfortable context; larger registries
# are split into full-coverage chunks (every candidate reaches the agent).
# Chunk boundaries come from pack_chunks() — rendered size, not fixed count.


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


def bm25_select(
    registry: dict[str, Any], query: str, limit: int | None = None
) -> list[dict[str, Any]]:
    """BM25 order, no cap unless the caller asks for one. Selection does not
    truncate — deep reading is the only stage that does."""
    scored = bm25_scores(registry, query)
    if limit is None:
        return [candidate for _, _, candidate in scored]
    return [candidate for _, _, candidate in scored[: max(0, limit)]]


def influence_select(
    registry: dict[str, Any], limit: int | None = None
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
    selected = with_citations if limit is None else with_citations[: max(0, limit)]
    return selected, len(with_citations)


# ---- smart strategy ---------------------------------------------------------


def _candidate_line(candidate: dict[str, Any]) -> str:
    title = " ".join(str(candidate.get("title") or "").split())
    abstract = " ".join(str(candidate.get("summary") or "").split())
    if len(abstract) > SMART_MAX_ABSTRACT_CHARS:
        abstract = abstract[: SMART_MAX_ABSTRACT_CHARS - 1].rstrip() + "…"
    published = str(candidate.get("published") or "")[:10]
    return f"[{candidate.get('arxiv_id')}] ({published}) {title} — {abstract}"


def _candidate_lines(candidates: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"{index}. {_candidate_line(candidate)}"
        for index, candidate in enumerate(candidates, start=1)
    )


def pack_chunks(
    candidates: list[dict[str, Any]],
    *,
    char_budget: int,
    count_ceiling: int,
) -> list[list[dict[str, Any]]]:
    """Split candidates into agent-call chunks by rendered line size.

    A chunk closes when the next line would overflow ``char_budget`` OR reach
    ``count_ceiling`` — so a registry of long abstracts (the 2026-10-16 强化学习
    run: 300 candidates rendered a 157KB prompt and the completion stream died
    mid-response) packs into short calls, while a registry of tiny lines still
    keeps the candidate count per call bounded. A single line larger than the
    budget becomes its own chunk; candidates are never dropped or split.
    """

    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    for candidate in candidates:
        line_chars = len(_candidate_line(candidate)) + 1  # + newline
        if current and (
            current_chars + line_chars > char_budget or len(current) >= count_ceiling
        ):
            chunks.append(current)
            current = []
            current_chars = 0
        current.append(candidate)
        current_chars += line_chars
    if current:
        chunks.append(current)
    return chunks




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
    complete_fn,
    cli: str,
    model: str,
    env: dict[str, str] | None = None,
    cwd=None,
    timeout_s: float = SELECTION_TIMEOUT_S,
) -> tuple[list[dict[str, Any]], str]:
    """The smart contract: EVERY candidate's abstract reaches the agent.

    Candidates are chunked to context size and each chunk goes to one
    one-shot call with the review topic; the union of relevant IDs is the
    selection. No lexical prefilter may decide what the agent sees — bm25
    cannot tokenize a Chinese topic, and prefiltering by it silently reverts
    smart to the word-matching screen this strategy exists to replace.

    Nothing is truncated here. The queue is emitted in REGISTRY order (the
    retrieval order), not in the agent's reply order: chunk order is a
    coverage device, not a relevance ranking, and the deep-read stage owns the
    only cut in the funnel."""

    candidates = [
        c for c in registry.get("candidates", [])
        if isinstance(c, dict) and str(c.get("arxiv_id") or "").strip()
    ]
    known = {str(c.get("arxiv_id")) for c in candidates}
    if not candidates:
        return [], "empty registry"
    by_id = {str(c.get("arxiv_id")): c for c in candidates}
    focus_line = f"关注重点：{focus}" if focus else ""
    # arxiv_id -> reason. Insertion order is chunk order, which is only
    # meaningful for coverage accounting; the queue itself is re-projected
    # onto registry order below.
    chosen: dict[str, str] = {}
    failed_chunks = 0
    timed_out_chunks = 0
    salvaged_chunks = 0
    chunks = pack_chunks(
        candidates,
        char_budget=SMART_CANDIDATE_CHARS_PER_CALL,
        count_ceiling=SMART_CANDIDATES_PER_CALL,
    )
    for index, chunk in enumerate(chunks, start=1):
        # One agent call per chunk takes minutes; print a plain progress line
        # so the driver can translate it into a wiki progress tick (the
        # 2026-10-13 gap: 13 silent minutes between registry and selection).
        print(f"chunk {index}/{len(chunks)}: judging {len(chunk)} of {len(candidates)} candidates…", flush=True)
        prompt = SMART_SELECTION_PROMPT.format(
            topic=topic, focus_line=focus_line,
            candidates=_candidate_lines(chunk),
        )
        try:
            result = complete_fn(
                prompt, timeout_s=timeout_s, cli=cli, model=model,
                cwd=cwd, env=env, label="selection-smart",
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            # A slow or hung agent call is a FAILED CHUNK, never a run-killing
            # crash — the same contract as a non-zero exit. Every other
            # complete() caller already degrades this way; letting
            # TimeoutExpired escape here aborted the whole fixed workflow
            # (2026-10-08, exit 1 on a single 600s timeout) instead of
            # reporting one visible coverage hole and continuing.
            timed_out_chunks += 1
            failed_chunks += 1
            if isinstance(exc, subprocess.TimeoutExpired):
                print(
                    f"[DRIVER-WARN] 选文 chunk {index}/{len(chunks)} 超时"
                    f"（{timeout_s:.0f}s），{len(chunk)} 篇候选未判定 — 覆盖缺口",
                    flush=True,
                )
            else:
                print(
                    f"[DRIVER-WARN] 选文 chunk {index}/{len(chunks)} 调用失败"
                    f"（{type(exc).__name__}: {exc}），{len(chunk)} 篇候选未判定 — 覆盖缺口",
                    flush=True,
                )
            continue
        if result.returncode != 0:
            failed_chunks += 1
            print(
                f"[DRIVER-WARN] 选文 chunk {index}/{len(chunks)} 返回"
                f" exit {result.returncode}，{len(chunk)} 篇候选未判定 — 覆盖缺口",
                flush=True,
            )
            continue
        parsed = _parse_selections(result.stdout, known)
        if parsed:
            for arxiv_id, reason in parsed:
                chosen.setdefault(arxiv_id, reason)
        elif result.stdout.strip():
            # Non-empty output that parses to nothing is NOT an empty verdict:
            # count it as a coverage hole (or salvage IDs) — never let a
            # malformed response silently stand in for "300 papers judged
            # irrelevant" (20260930 absolute-pose chunk-1).
            salvaged = _salvage_ids(result.stdout, known)
            if salvaged:
                for arxiv_id in salvaged:
                    chosen.setdefault(arxiv_id, "")
                salvaged_chunks += 1
            else:
                failed_chunks += 1
    detail_parts = [
        f"smart selected {len(chosen)}/{len(candidates)} considered "
        f"({len(chunks)} full-coverage chunk(s))"
    ]
    if salvaged_chunks:
        detail_parts.append(
            f"{salvaged_chunks}/{len(chunks)} chunk(s) malformed — IDs salvaged, reasons lost"
        )
    if timed_out_chunks:
        detail_parts.append(
            f"{timed_out_chunks}/{len(chunks)} chunk(s) timed out after {timeout_s:.0f}s — "
            "coverage incomplete (raise --complete-timeout, or re-run this stage)"
        )
    if failed_chunks:
        detail_parts.append(f"{failed_chunks}/{len(chunks)} chunk(s) failed — coverage incomplete")
    # Emit in registry (retrieval) order. The agent's per-chunk reply order is
    # not a global ranking — merging chunk answers by arrival would make the
    # queue's order depend on chunk boundaries and on which chunks happened to
    # fail (2026-10-20 自监督预训练: 120-slot cap + chunk-arrival order put every
    # deep read in 2021-2022). Registry order keeps the retrieval relevance
    # ranking that the search backend produced.
    out = []
    for candidate in candidates:
        arxiv_id = str(candidate.get("arxiv_id"))
        if arxiv_id not in chosen:
            continue
        record = dict(by_id[arxiv_id])
        record["selection_reason"] = chosen[arxiv_id]
        out.append(record)
    return out, "; ".join(detail_parts)


# ---- smart-jev strategy (decision model) ------------------------------------


def _jev_claim(candidate: dict[str, Any]) -> str:
    title = " ".join(str(candidate.get("title") or "").split())
    abstract = " ".join(str(candidate.get("summary") or "").split())
    if len(abstract) > SMART_MAX_ABSTRACT_CHARS:
        abstract = abstract[: SMART_MAX_ABSTRACT_CHARS - 1].rstrip() + "…"
    return SMART_JEV_CLAIM.format(
        arxiv_id=candidate.get("arxiv_id"), title=title, abstract=abstract
    )


def jev_select(
    registry: dict[str, Any],
    *,
    topic: str,
    focus: str = "",
    judge_fn,
    threshold: float = SMART_JEV_RELEVANCE_THRESHOLD,
    model: str = SYSTEM_ONE_MODEL,
    questions_per_call: int = SMART_JEV_QUESTIONS_PER_CALL,
    chars_per_call: int = SMART_JEV_CHARS_PER_CALL,
    workers: int = 4,
    label: str = "selection-smart-jev",
) -> tuple[list[dict[str, Any]], str]:
    """Full-coverage relevance judgement by a decision model.

    Same contract as :func:`smart_select` — every candidate is judged, nothing
    is truncated, the queue comes back in REGISTRY order — but each candidate
    is one typed Noul question in a batched System One request. The union of
    probabilities above ``threshold`` is the selection; a failed batch is a
    reported coverage gap, never a run-killing error.

    ``judge_fn(state, questions, *, model, label)`` is the harness binding
    (``claude.judge_questions``); batching is by rendered claim size and by
    question count, mirroring ``pack_chunks``."""

    candidates = [
        c for c in registry.get("candidates", [])
        if isinstance(c, dict) and str(c.get("arxiv_id") or "").strip()
    ]
    if not candidates:
        return [], "empty registry"
    focus_line = f"关注重点：{focus}\n" if focus else ""
    state = SMART_JEV_STATE.format(topic=topic, focus_line=focus_line)
    chunks = pack_chunks(
        candidates, char_budget=chars_per_call, count_ceiling=questions_per_call
    )
    scores: dict[str, float] = {}
    failed_chunks = 0

    def run_chunk(chunk: list[dict[str, Any]]) -> tuple[dict[str, float], str]:
        questions = {
            str(candidate.get("arxiv_id")): {
                "type": "noul",
                "instructions": _jev_claim(candidate),
            }
            for candidate in chunk
        }
        payload = judge_fn(state, questions, model=model, label=label)
        answers = payload.get("answers") if isinstance(payload, dict) else None
        out: dict[str, float] = {}
        if isinstance(answers, dict):
            for arxiv_id, answer in answers.items():
                if not isinstance(answer, dict):
                    continue
                value = answer.get("noul")
                if isinstance(value, (int, float)):
                    out[str(arxiv_id)] = float(value)
        return out, ""

    print(
        f"jev: judging {len(candidates)} candidates in {len(chunks)} "
        f"System One request(s)…",
        flush=True,
    )
    with ThreadPoolExecutor(max_workers=max(1, min(workers, len(chunks)))) as pool:
        futures = [pool.submit(run_chunk, chunk) for chunk in chunks]
        for index, future in enumerate(futures, start=1):
            try:
                found, _ = future.result()
            except Exception as exc:  # noqa: BLE001 — one batch must not kill the run
                failed_chunks += 1
                print(
                    f"[DRIVER-WARN] 选文(jev) batch {index}/{len(chunks)} 失败"
                    f"（{type(exc).__name__}: {exc}），{len(chunks[index - 1])} 篇候选未判定 — 覆盖缺口",
                    flush=True,
                )
                continue
            scores.update(found)

    known = {str(c.get("arxiv_id")) for c in candidates}
    chosen = {arxiv_id for arxiv_id, score in scores.items()
              if arxiv_id in known and score >= threshold}
    detail_parts = [
        f"smart-jev selected {len(chosen)}/{len(candidates)} considered "
        f"(threshold {threshold:.2f}, {len(chunks)} System One request(s))"
    ]
    unjudged = len(candidates) - len(scores)
    if unjudged:
        detail_parts.append(
            f"{unjudged} candidate(s) unjudged ({failed_chunks} failed batch(es)) — "
            "coverage incomplete"
        )
    out: list[dict[str, Any]] = []
    for candidate in candidates:
        arxiv_id = str(candidate.get("arxiv_id"))
        if arxiv_id not in chosen:
            continue
        record = dict(candidate)
        record["selection_reason"] = (
            f"jev p={scores.get(arxiv_id, 0.0):.2f} ≥ {threshold:.2f}"
        )
        out.append(record)
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
    output_screening: str,
    output_ids: str,
    output_markdown: str | None = None,
    terms: str = "",
    *,
    cli: str | None = None,
    model: str | None = None,
    timeout_s: float = SELECTION_TIMEOUT_S,
    complete_fn=None,
    judge_fn=None,
    threshold: float = SMART_JEV_RELEVANCE_THRESHOLD,
) -> int:
    """CLI driver behind ``search.py select-candidates``: rank the registry with
    one non-keywords strategy and write the same screening artifacts the legacy
    screen-candidates emits, so extraction/deep-read downstream are unchanged.

    No count cap: the queue carries every paper the strategy judges relevant.
    Deep reading is the only funnel stage that truncates.

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
        selected, with_data = influence_select(registry)
        parts = [f"influence ranked {with_data} papers with citation data"]
        if len(selected) < len(registry.get("candidates") or []):
            # Offline honesty: a channel without citation metadata cannot rank
            # every candidate by influence alone — bm25 covers the rest and the
            # detail says so (nothing is dropped silently).
            chosen = {str(c.get("arxiv_id")) for c in selected}
            selected = selected + [
                candidate
                for _, _, candidate in bm25_scores(registry, query)
                if str(candidate.get("arxiv_id")) not in chosen
            ]
            parts.append(f"influence degraded to bm25 (citation data: {with_data} papers)")
        detail = "; ".join(parts)
    elif strategy == "bm25":
        selected = bm25_select(registry, query)
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
            complete_fn=complete_fn or complete,
            cli=cli,
            model=model or DRIVER_AGENT_MODEL,
            env=isolated_claude_env(),
            cwd=None,  # the driver spawns this entry with cwd=kb-root
            timeout_s=timeout_s,
        )
    elif strategy == "smart-jev":
        from embodied_learning.harness.claude import system_one_ready

        if not system_one_ready():
            print(
                "决策模型（System One / jev）未配置：需要 "
                "EMBODIED_SYSTEM_ONE_URL（或 ANTHROPIC_BASE_URL）与 "
                "EMBODIED_SYSTEM_ONE_API_KEY（或 ANTHROPIC_AUTH_TOKEN）。"
                "可改用 --selection-strategy smart（执行模型）。",
                file=sys.stderr,
            )
            return 2
        if judge_fn is None:
            from embodied_learning.harness.claude import judge_questions as judge_fn
        selected, detail = jev_select(
            registry,
            topic=topic,
            focus=focus,
            judge_fn=judge_fn,
            threshold=threshold,
            model=model or SYSTEM_ONE_MODEL,
        )
    else:
        print(f"unknown selection strategy: {strategy}", file=sys.stderr)
        return 2
    rows, ids = to_screening_artifacts(selected, detail)
    screening = {
        "version": 1,
        "candidate_registry": registry_path,
        "selection_rule": {"strategy": strategy, "detail": detail},
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

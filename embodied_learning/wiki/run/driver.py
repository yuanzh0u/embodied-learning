"""Run the fixed mechanical stages of a literature review end to end.

Moves every deterministic stage into this driver so a kickoff no longer
replans search queries, re-reads knowledge routing, or re-learns rate limits
each run:

    plan -> retrieval (arXiv, one process; S2 keyword opt-in via --with-s2) -> registry
         -> screening -> coverage -> extraction -> reading packets
         -> deep read (parallel skeleton agents + local assembly, default on)
         -> evidence projection -> pipeline-summary.json

Deep read + projection run inside the driver too (parallel one-shot claude
skeleton agents); ``--skip-deep-read`` stops after the reading packets so an
external orchestrator can own deep reading instead. Either way, downstream
claude sessions only do the judgment stages: review packet, outline, writing,
audit gates.

Idempotent: a stage whose outputs already exist on disk is skipped, so an
interrupted run resumes for free. Every completed stage prints one
``[DRIVER-STAGE:<name>] ok <detail>`` line; the summary JSON reports stage
durations, counts, coverage status, S2 degradation, and the terms source.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any
import concurrent.futures
from pathlib import Path

from embodied_learning.harness.claude import (
    DRIVER_AGENT_MODEL,
    SessionLog,
    complete,
    open_session_log,
    resolve_cli,
    session_ledger_enabled,
)
from embodied_learning.harness.prompt import (
    DYNAMIC_QUERIES_PROMPT,
    SEED_LINE,
    TERMS_PROMPT,
    build_skeleton_prompt,
    pool_root_for,
    read_skeleton_output,
)
from embodied_learning.knowledge.evidence import consolidate_evidence
from embodied_learning.knowledge.funnel import (
    FUNNEL_FILENAME,
    build_funnel,
    write_funnel,
)
from embodied_learning.utils.layout import default_kb_root, find_roots, kb_cache_dir
from embodied_learning.utils.translate import translate as translate_text
from embodied_learning.search.abstract_evidence import (
    ABSTRACT_FILENAME,
    build_abstract_events,
    max_event_seq,
    read_events,
    write_abstract_tier,
)

_REPO_ROOT, SKILLS_ROOT, SCRIPTS_ROOT = find_roots()
HUB_SCRIPTS = SKILLS_ROOT / "embodied-ai-literature-hub" / "scripts"
PLANNER_SCRIPT = HUB_SCRIPTS / "search.py"
READ_SCRIPT = SKILLS_ROOT / "embodied-ai-paper-reader" / "scripts" / "read.py"
PACKET_SCRIPT = READ_SCRIPT  # subcommand: build-reading-packet
REVIEW_PACKET_SCRIPT = SKILLS_ROOT / "embodied-ai-review-writer" / "scripts" / "write.py"  # subcommand: review-packet

REVIEW_MODES = {"rapid", "scoping", "systematic"}
# Mode tables and agent defaults live in embodied_learning.config (single home).
from embodied_learning.config import (
    # noqa: E402
    AGENT_SESSION_LEDGER_ENV,
    CITATION_EXPANSION_TIMEOUT_S,
    DEEP_READ_LIMITS,
    DEEP_READ_RETRY_PASSES,
    DYNAMIC_AGENT_ATTEMPTS,
    DYNAMIC_AGENT_TIMEOUT_S,
    EVIDENCE_FLOORS,
    EXTRACTION_STAGE_TIMEOUT_S,
    FUNNEL_LAYER_PAPER_CAP,
    REVIEW_MODES,
    S2_BUDGET_S,
    S2_SLEEP_S,
    SEARCH_MAX_RESULTS_PER_QUERY,
    SEARCH_STRATEGIES,
    SELECTION_STRATEGIES,
    SESSION_EVENT_TEXT_MAX_CHARS,
    SKELETON_AGENT_ATTEMPTS,
    TERMS_AGENT_TIMEOUT_S,
)
# Deep-read queue selection: keywords is the legacy term-matching screen
# (screen-candidates); the rest rank the registry by relevance (bm25),
# citations (influence), or one one-shot agent (smart, the default).
# S2 requests run at a 3s pace: the API 429s aggressively, and a degraded S2
# channel costs more (retry rounds, thinner registries) than the seconds saved.
FALLBACK_STOPWORDS = {
    "的", "在", "和", "与", "或", "对", "从", "到", "了", "是",
    "the", "a", "an", "of", "for", "and", "to", "in", "on", "with", "via",
}


# Spawn cwd for stage subprocesses and one-shot agents; main() pins this to
# the KB root so relative defaults and the agents' CLAUDE.md discovery both
# resolve against the KB, never the repo or site-packages.
DRIVER_CWD = Path.cwd()


QUEUE_LINE_RE = re.compile(r"^(OK|HELD) (\S+) \((\d+)/(\d+)\)$")


def extraction_queue_line(line: str) -> None:
    """Translate one extract-content-queue stdout line: per-paper OK/HELD
    becomes a progress tick (HELD additionally notes why it matters); any
    other line (summary, warnings) stays a plain dialog line."""
    match = QUEUE_LINE_RE.match(line.strip())
    if match:
        state, paper_id, done_s, total_s = match.groups()
        log(f"[DRIVER-PROGRESS:extract:{done_s}/{total_s}]")
        if state == "HELD":
            log(f"[PAPER] {paper_id} 全文不满足证据条件（HELD）")
    elif line.strip().startswith("[DRIVER-"):
        log(line.strip())  # already protocol-formatted (e.g. [DRIVER-WARN])
    else:
        log(f"[DRIVER] 全文抽取 {line}")


SELECTION_CHUNK_RE = re.compile(r"^chunk\s+(\d+)/(\d+)\s*[:\-]?\s*(.*)$", re.IGNORECASE)


def selection_line(line: str) -> None:
    """Translate select-candidates' per-chunk stdout into a progress tick so
    the wiki's per-item bar moves during smart selection (one agent call per
    chunk of candidates — minutes each). Other lines stay dialog detail."""
    match = SELECTION_CHUNK_RE.match(line.strip())
    if match:
        done_s, total_s, rest = match.groups()
        log(f"[DRIVER-PROGRESS:select:{done_s}/{total_s}]")
        if rest.strip():
            log(f"[DRIVER] 选文 {rest.strip()}")
    elif line.strip().startswith("[DRIVER-"):
        log(line.strip())  # already protocol-formatted (e.g. [DRIVER-WARN])
    else:
        log(f"[DRIVER] 选文 {line}")


def stage_line(name: str, detail: str = "") -> str:
    """One protocol line per completed stage; the wiki server turns each into
    a timeline event."""
    suffix = f" {detail}" if detail else ""
    return f"[DRIVER-STAGE:{name}] ok{suffix}"


def log(message: str) -> None:
    print(message, flush=True)


def brief(stage: str, title: str, lines: list[str]) -> None:
    """Emit one per-stage results brief — the human-checkable work product of
    that stage (query list, selected papers, deep-read outcomes…).

    The wiki dialog renders it as a collapsible 成果简报 block so a reviewer
    can verify what the stage actually produced and a debugger can replay the
    decision surface without opening the run dir. One JSON payload on the
    stdout line (multi-line briefs survive framing)."""
    payload = json.dumps({"title": title, "lines": lines}, ensure_ascii=False)
    log(f"[DRIVER-BRIEF:{stage}] {payload}")


def run_command(command: list[str], *, timeout: float | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=str(DRIVER_CWD),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def fail(stage: str, message: str) -> "DriverError":
    return DriverError(f"[{stage}] {message}")


class DriverError(RuntimeError):
    pass



def parse_time_range(time_range: str) -> tuple[str, str]:
    match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})", time_range.strip())
    if not match:
        raise ValueError(f"time range must be YYYY-MM-DD..YYYY-MM-DD: {time_range!r}")
    return match.group(1), match.group(2)


def mechanical_terms(topic: str, focus: str) -> list[str]:
    """Fallback terms: split topic + focus, drop stopwords, dedupe, cap at 12.

    Title/abstract matching is substring-based against English papers, so raw
    Chinese words never match — the useful fallback terms are the Latin-word
    runs inside topic/focus (e.g. "3D Gaussian" → "3d", "gaussian"). When the
    text has no Latin tokens at all, fall through to the Chinese tokens."""
    latin: list[str] = []
    cjk: list[str] = []
    for word in re.findall(r"[0-9A-Za-z]+|[一-鿿]+", f"{topic} {focus}"):
        lowered = word.lower()
        if lowered in FALLBACK_STOPWORDS or len(lowered) < 2:
            continue
        target = latin if word.isascii() else cjk
        if lowered not in latin and lowered not in cjk:
            target.append(lowered)
    return (latin or cjk)[:12]



def translation_terms(topic: str, focus: str) -> tuple[list[str], str]:
    """Mechanical terms merged with a MyMemory translation of the topic.

    Pure-Chinese topics carry no Latin token to conjunct — arXiv cannot match
    CJK text (2026-10-15 强化学习), so the mechanical path gets nothing to run.
    One translation call contributes English tokens. Merge, never replace: the
    topic's own tokens stay in the list (call sites filter to Latin where it
    matters), English tokens first so the 12-cap and the recall scope clause
    prefer them. When the topic already has Latin tokens, or translation is
    unavailable, the mechanical result passes through unchanged.

    Returns ``(terms, translated_text)``; ``translated_text`` is "" unless a
    translation actually contributed terms."""

    terms = mechanical_terms(topic, focus)
    if any(term.isascii() for term in terms):
        return terms, ""
    translated = translate_text(f"{topic} {focus}".strip()) or ""
    if not translated:
        return terms, ""
    english = [t for t in mechanical_terms(translated, "") if t.isascii()]
    if not english:
        return terms, ""
    merged = (english + [t for t in terms if t not in english])[:12]
    return merged, translated


def extract_terms_json(text: str) -> list[str] | None:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    terms = payload.get("terms") if isinstance(payload, dict) else None
    if not isinstance(terms, list):
        return None
    cleaned = [str(item).strip() for item in terms if str(item).strip()]
    return cleaned[:12] or None


def agent_terms(
    topic: str, focus: str, timeout_s: float, cli: str | None,
    *, ledger: SessionLog | None = None,
) -> list[str] | None:
    """One-shot claude call for screening terms. Returns None on any failure —
    the caller falls back to mechanical terms. This is a function call with a
    timeout, not a decision-maker."""
    if not cli:
        return None
    try:
        result = complete(
            TERMS_PROMPT.format(topic=topic, focus=focus or "无"), timeout_s=timeout_s, cli=cli,
            label="terms-agent", ledger=ledger,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        if isinstance(exc, subprocess.TimeoutExpired):
            log(f"[DRIVER-WARN] 术语 agent 超时（{timeout_s:.0f}s），回退机械术语")
        else:
            log(f"[DRIVER-WARN] 术语 agent 启动失败：{exc}")
        return None
    if result.returncode:
        return None
    return extract_terms_json(result.stdout)




def parse_seed_ids(raw: str) -> list[str]:
    """Comma/space separated arXiv IDs → normalized list (dedup, version-stripped).
    Per-token normalization delegates to the shared arXiv-ID grammar; a bare
    ``arxiv:`` prefix is stripped first since parse_arxiv_id only knows URLs."""

    from embodied_learning.knowledge.arxiv_reader import parse_arxiv_id

    ids: list[str] = []
    for token in re.split(r"[,\s]+", (raw or "").strip()):
        normalized = parse_arxiv_id(re.sub(r"^arxiv:", "", token, flags=re.IGNORECASE))
        if normalized and normalized not in ids:
            ids.append(normalized)
    return ids


def _dynamic_query_candidates(text: str) -> list[str]:
    """Parse candidates for the agent's JSON payload, cheapest first.

    Includes a head-repair ladder: the completion channel occasionally drops
    the first bytes of the response (2026-10-13/14/15 runs arrived starting at
    ``queries":`` / ``":[`` instead of ``{"queries":``), leaving intact query
    objects under a damaged outer wrapper that a strict parse rejects."""

    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[A-Za-z]*\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    bases = [stripped]
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match and match.group(0) not in bases:
        bases.append(match.group(0))
    candidates: list[str] = []
    for base in bases:
        for prefix in ("", '{"', '{"queries', '{"queries":', '{"queries": [', '{"queries": '):
            candidate = prefix + base
            if candidate not in candidates:
                candidates.append(candidate)
    return candidates


def _load_dynamic_queries(candidate: str) -> dict | None:
    """One candidate string → ``{"queries": [...]}`` or None when unusable."""

    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict):
        queries = payload.get("queries")
    elif isinstance(payload, list):
        queries = payload
    else:
        return None
    if not isinstance(queries, list):
        return None
    cleaned: list[dict] = []
    for item in queries:
        if not isinstance(item, dict) or not str(item.get("query") or "").strip():
            continue
        cleaned.append(
            {
                "label": str(item.get("label") or "dynamic-agent"),
                "tier": str(item.get("tier") or "dynamic-association"),
                "query": str(item["query"]),
                "why": str(item.get("why") or "Agent-generated dynamic query."),
            }
        )
    if not cleaned:
        return None
    return {"queries": cleaned[:20]}


def extract_dynamic_queries_json(text: str) -> dict | None:
    """Parse the dynamic-query agent's JSON payload out of its stdout.

    Tolerates code fences and prose around the object, and repairs a truncated
    response head (see :func:`_dynamic_query_candidates`). Returns None only
    when no candidate yields a non-empty query list."""

    for candidate in _dynamic_query_candidates(text):
        payload = _load_dynamic_queries(candidate)
        if payload is not None:
            return payload
    return None


def agent_dynamic_queries(
    topic: str, focus: str, seed_ids: list[str], timeout_s: float, cli: str | None,
    *,
    attempts: int | None = None,
    ledger: SessionLog | None = None,
) -> dict | None:
    """One-shot claude call generating the run's dynamic arXiv queries.

    This is the stage the failed 2026-09-11 runs were missing: their topics
    matched no taxonomy card, the mechanical latin-term fallback was empty for
    pure-Chinese topics, and retrieval ran 4 off-topic card queries. Returns
    None when every attempt fails — the plan still contains the generic
    fallback (and the driver stops with an actionable empty-plan error when
    that fallback is also empty).

    Parse failures and non-zero exits retry up to ``DYNAMIC_AGENT_ATTEMPTS``
    total tries; a timeout does not retry — that budget is already spent.
    Every failure reason is logged: the silent None of 2026-10-15 made the
    head-truncation outage hard to diagnose."""

    if not cli:
        return None
    total = max(1, int(attempts if attempts is not None else DYNAMIC_AGENT_ATTEMPTS))
    seed_line = SEED_LINE.format(seeds=", ".join(seed_ids)) if seed_ids else ""
    prompt = DYNAMIC_QUERIES_PROMPT.format(topic=topic, focus=focus or "无", seed_line=seed_line)
    for attempt in range(1, total + 1):
        try:
            result = complete(
                prompt, timeout_s=timeout_s, cli=cli, label=f"dynamic-queries:{topic}",
                ledger=ledger,
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            if isinstance(exc, subprocess.TimeoutExpired):
                log(f"[DRIVER-WARN] 动态查询 agent 超时（{timeout_s:.0f}s），回退分类法+通用查询")
            else:
                log(f"[DRIVER-WARN] 动态查询 agent 启动失败：{exc}")
            return None
        if result.returncode:
            log(
                f"[DRIVER-WARN] 动态查询 agent 退出 {result.returncode}（第 {attempt}/{total} 次）："
                f"{(result.stderr or result.stdout or '').strip()[-200:]}"
            )
            continue
        payload = extract_dynamic_queries_json(result.stdout)
        if payload:
            return payload
        head = re.sub(r"\s+", " ", (result.stdout or "").strip())[:100]
        log(f"[DRIVER-WARN] 动态查询 agent 输出无法解析（第 {attempt}/{total} 次）：{head!r}")
    return None


class TermsSelector:
    """Runs the terms selection in a thread so it overlaps retrieval; the main
    flow only blocks on it right before screening.

    ``fallback_terms`` is the precomputed mechanical/translated term list: the
    caller already bootstrapped pure-Chinese topics through translation, and a
    second mechanical pass over the raw Chinese topic would drop back to CJK
    tokens that English titles never match."""

    def __init__(
        self,
        topic: str,
        focus: str,
        *,
        use_agent: bool,
        timeout_s: float,
        cli: str | None,
        fallback_terms: list[str] | None = None,
        ledger: SessionLog | None = None,
    ):
        self._result: list[str] | None = None
        self._source = "mechanical"
        self._thread: threading.Thread | None = None

        def mechanical() -> list[str]:
            return list(fallback_terms) if fallback_terms is not None else mechanical_terms(topic, focus)

        if not use_agent:
            self._result = mechanical()
            return
        def worker() -> None:
            terms = agent_terms(topic, focus, timeout_s, cli, ledger=ledger)
            if terms:
                self._result = terms
                self._source = "agent"
            else:
                self._result = mechanical()
                self._source = "mechanical-fallback"
        self._thread = threading.Thread(target=worker, daemon=True)

    def start(self) -> None:
        if self._thread is not None:
            self._thread.start()

    def join(self) -> tuple[list[str], str]:
        if self._thread is not None:
            self._thread.join()
        assert self._result is not None
        return self._result, self._source


def outputs_exist(*paths: Path) -> bool:
    return all(path.is_file() and path.stat().st_size > 0 for path in paths)


PROJECT_SCRIPT = READ_SCRIPT  # subcommand: project-evidence-events


def build_screening_updates(screening_path: Path, extraction_summary_path: Path) -> list[dict] | None:
    """Merge extraction results into screening statuses for registry rebuild.

    The in-pipeline screening stage emits ``full-text-queued`` statuses that
    predate extraction; ``build-candidate-registry --screening-file`` needs
    ``extracted`` + ``extraction.evidence_eligible`` for the full-text floor to
    count recovered papers. Returns None when either input is missing."""
    if not screening_path.is_file() or not extraction_summary_path.is_file():
        return None
    screening = json.loads(screening_path.read_text(encoding="utf-8"))
    extraction = {
        str(result.get("paper_id")): result
        for result in json.loads(extraction_summary_path.read_text(encoding="utf-8")).get("results", [])
        if isinstance(result, dict) and result.get("paper_id")
    }
    updates = []
    for entry in screening.get("candidates", []):
        result = extraction.get(str(entry.get("arxiv_id")))
        if result and result.get("evidence_eligible"):
            entry = dict(entry)
            entry["status"] = "extracted"
            entry["extraction"] = {"evidence_eligible": True, "path": result.get("path")}
        updates.append(entry)
    return updates


def refresh_coverage_inplace(run_dir: Path, coverage_output: Path) -> None:
    """Recompute coverage-report.json in-process (no subprocess).

    The CLI wrapper (assess-review-coverage) is for stages that want
    run_stage's skip/force semantics; mid-run refreshes just need the numbers
    current. Set operations only — cheap enough to run at every stage end and
    again at finalize."""

    from embodied_learning.search import coverage as coverage_mod

    try:
        plan = json.loads((run_dir / "query-plan.json").read_text(encoding="utf-8"))
        registry = json.loads((run_dir / "candidate-registry.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    evidence_paths = []
    evidence_dir = run_dir / "evidence"
    if evidence_dir.is_dir():
        evidence_paths = [
            path for path in evidence_dir.glob("*.jsonl") if path.name != ABSTRACT_FILENAME
        ]
    report = coverage_mod.assess(plan, registry, evidence_paths)
    coverage_output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def recall_author_queries(papers: list[dict], *, terms: list[str] | str = "", limit: int = 12) -> list[dict]:
    """Author-recall round: ``au:"Name" AND (topic terms)``.

    Discovery rounds (plan/citation) already pulled these authors' obvious
    work, so a term-scoped recall re-finds mostly known papers — low
    new_unique_rate by construction. That makes it a valid saturation TAIL
    (main's author-recall/title-recall rounds). An unscoped ``au:"Name"`` would
    instead harvest every paper the author ever wrote (2026-10-10: 0.92
    new-rate, not a tail). If even a scoped recall lands many new papers, that
    is a real signal the search was incomplete."""

    from collections import Counter

    counts: Counter = Counter()
    for paper in papers:
        for name in paper.get("authors") or []:
            name = str(name).strip()
            # "A. Gopinath" initials are noisy; require a full-looking name.
            if len(name) >= 5 and " " in name and not name.endswith("."):
                counts[name] += 1
    scope = _topic_scope_clause(terms)
    queries = []
    for index, (name, _count) in enumerate(counts.most_common(limit), start=1):
        query = f'au:"{name}"' + scope
        queries.append({"label": f"recall-author-{index}", "query": query})
    return queries


def _topic_scope_clause(terms: list[str] | str, *, limit: int = 4) -> str:
    """`` AND (all:word OR ...)`` from English retrieval terms — keeps a recall
    query from becoming an unbounded author harvest. Accepts the terms list
    (preferred: already Latin-tokenized) or a raw topic string; a pure-Chinese
    topic yields no Latin tokens and must not silently degrade to unscoped
    ``au:"Name"`` (2026-10-10: that re-harvested 253 unrelated papers)."""

    if isinstance(terms, str):
        terms = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", terms)
    tokens = [t for t in terms if t and t.lower() not in _RECALL_STOPWORDS]
    # A merged term list (translated bootstrap, see translation_terms) can mix
    # Latin and CJK tokens — the scope clause wants the English ones.
    latin = [t for t in tokens if t.isascii()]
    tokens = latin or tokens
    if not tokens:
        return ""
    return " AND (" + " OR ".join(f"all:{t}" for t in tokens[:limit]) + ")"


def known_works_queries(papers: list[dict], *, seeds: list[str] | None = None, limit: int = 8) -> list[dict]:
    """Known-works round: exact ``ti:"Full Title"`` for the canon.

    Seeds first, then the earliest/most-central discovered papers. An exact
    title probe re-finds the paper itself and little else — the most reliable
    low-novelty round, the one that lets the saturation judge see a converged
    tail (main's title-recall-5 / browser-fallback were this, both 0.0)."""

    by_id = {}
    for paper in papers:
        arxiv_id = str(paper.get("arxiv_id") or "").split("v")[0]
        if arxiv_id:
            by_id[arxiv_id] = paper
    ordered: list[dict] = []
    for seed in seeds or []:
        paper = by_id.get(str(seed).split("v")[0])
        if paper and paper not in ordered:
            ordered.append(paper)
    for paper in papers:
        if len(ordered) >= limit:
            break
        if paper not in ordered and str(paper.get("title") or "").strip():
            ordered.append(paper)
    queries = []
    seen: set[str] = set()
    for paper in ordered:
        title = str(paper.get("title") or "").strip().replace('"', "")
        if len(title) < 8 or title.lower() in seen:
            continue
        seen.add(title.lower())
        queries.append({"label": f"known-works-{len(queries) + 1}", "query": f'ti:"{title}"'})
        if len(queries) >= limit:
            break
    return queries


def recall_title_queries(papers: list[dict], *, limit: int = 10) -> list[dict]:
    """Title-recall round: ``ti:"..."`` probes on distinctive title phrases.

    Re-finds the papers we already hold — the definitive low-novelty tail
    that lets the saturation judge see a converged search (main's
    title-recall-5 / browser-fallback rounds were exactly this)."""

    seen: set[str] = set()
    queries = []
    for paper in papers:
        title = str(paper.get("title") or "").strip()
        if len(title) < 12:
            continue
        # Distinctive head phrase: drop stopwords, keep the first content words.
        tokens = [t for t in re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", title) if t.lower() not in _RECALL_STOPWORDS]
        phrase = " ".join(tokens[:4])
        if len(phrase) < 8 or phrase.lower() in seen:
            continue
        seen.add(phrase.lower())
        queries.append({"label": f"recall-title-{len(queries) + 1}", "query": f'ti:"{phrase}"'})
        if len(queries) >= limit:
            break
    return queries


_RECALL_STOPWORDS = frozenset(
    "the a an and or of for in on with via using based novel toward towards "
    "from to by at as is are was were we our it its this that these those".split()
)


def write_round_queries(path: Path, queries: list[dict], *, batch_label: str) -> None:
    """Write a search-arxiv --query-file for one retrieval round."""

    payload = {
        "batch": batch_label,
        "queries": queries,
        "start_date": "",
        "end_date": "",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inputs_newer_than(output: Path, inputs: list[Path]) -> bool:
    """True when any input file is newer than the stage output (or the output
    is missing). A registry built from search round r1 must be rebuilt after a
    new recall round lands — "outputs present" alone would silently drop the
    new batch and the saturation judge would never see the tail (2026-10-10)."""

    if not output.is_file():
        return any(path.is_file() for path in inputs)
    try:
        out_mtime = output.stat().st_mtime
    except OSError:
        return True
    for path in inputs:
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime > out_mtime:
                return True
        except OSError:
            return True
    return False


def log_gates(coverage_output: Path, label: str) -> None:
    """Stage-end gate report — cheap set operations, safe to run at every
    stage and again at finalize (2026-10-10: the numbers were computed
    mid-run but only surfaced at settle, after the expensive stages).

    Recoverable failures name their remedy so the operator can fix them at
    the stage that still can, instead of discovering them after writing."""

    try:
        report = json.loads(coverage_output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    checks = (report.get("stop_assessment") or {}).get("checks") or {}
    if not checks:
        return
    targets = report.get("targets") or {}
    observed = report.get("observed") or {}
    obs_key = {
        "candidate_floor": "candidate_count",
        "full_text_floor": "full_text_recovered_count",
        "accepted_paper_floor": "accepted_evidence_paper_count",
    }
    remedy = {
        "full_text_floor": "抽取重试可补",
        "accepted_paper_floor": "深读/候补可补",
        "saturation": "补检索轮次可补",
        "candidate_floor": "需扩检索",
        "coverage_dimensions": "需补维度查询",
    }
    summary = " · ".join(f"{name}={'过' if ok else '未过'}" for name, ok in checks.items())
    log(f"[DRIVER-GATES:{label}] {summary}")
    for name, ok in checks.items():
        if ok:
            continue
        key = obs_key.get(name)
        counts = ""
        if key and name in targets:
            counts = f"（{observed.get(key)}/{targets.get(name)}）"
        log(f"  未过 {name}{counts} — {remedy.get(name, '需人工判断')}")
    kind = report.get("saturation_kind")
    if kind:
        log(f"  saturation_kind={kind}")


def finalize_coverage(run_dir: Path, registry_command: list[str], coverage_output: Path) -> str:
    """Post-deep-read coverage reassessment (idempotent, cheap).

    The in-pipeline coverage stage runs before extraction/deep-read, so its
    full-text and accepted-paper floors are always stale-mid-run. After
    projection: rebuild the registry with extraction statuses merged in, then
    re-run assess-review-coverage with the projected evidence JSONL."""
    evidence_files = sorted(
        path for path in (run_dir / "evidence").glob("*.jsonl")
        if path.name != ABSTRACT_FILENAME  # abstract positioning is not accepted evidence
    )
    if not evidence_files:
        return "skipped (no evidence projected)"
    detail = "ok"
    updates = build_screening_updates(run_dir / "screening.json", run_dir / "extraction-summary.json")
    if updates:
        updates_path = run_dir / "screening-updates.json"
        updates_path.write_text(
            json.dumps({"version": 1, "candidates": updates}, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        result = run_command(list(registry_command) + ["--screening-file", str(updates_path)])
        if result.returncode:
            detail = f"degraded: registry rebuild exit {result.returncode}"
    command = [sys.executable, str(PLANNER_SCRIPT), "assess-review-coverage",
               "--query-plan", str(run_dir / "query-plan.json"),
               "--candidate-registry", str(run_dir / "candidate-registry.json")]
    for evidence_file in evidence_files:
        command += ["--evidence-jsonl", str(evidence_file)]
    command += ["--output", str(coverage_output)]
    result = run_command(command)
    if result.returncode:
        detail = f"degraded: coverage reassessment exit {result.returncode}"
    return detail


def claim_event_prefix(kb_root: Path, run_json_path: Path, manifest: dict) -> str:
    """Reserve this run's event-ID prefix under ``<kb-root>/.claims/``.

    Two concurrent runs with the same TOPIC8+year would both project
    ``EA-<TOPIC8>-<year>-NNNN`` ids (the old run-local counter can't see the
    other run's in-flight events). The claim file is an O_EXCL reservation —
    permanent, never GC'd. On a collision (another run's claim, or legacy
    evidence already using the prefix without a claim) the suffix increments.
    Idempotent: a manifest that already carries ``event_prefix`` keeps it.
    """

    from embodied_learning.wiki.run import events as next_event_id
    from embodied_learning import locks

    existing = manifest.get("event_prefix")
    if isinstance(existing, str) and existing:
        return existing
    year = dt.date.today().strftime("%Y")
    topic = manifest.get("topic") or "REVIEW"
    # TOPIC8 must stay ASCII (EVENT_ID_RE is [A-Z0-9-]), but stripping CJK
    # collapses EVERY Chinese topic to the fallback "REVIEW" — 8 concurrent
    # runs then all fought over EA-REVIEW-2026-N and two of them settled on
    # the same prefix (2026-10-13 race test: 图像内参估计 + 图像拼接 both got
    # EA-REVIEW-2026-8). A short topic digest keeps the namespace per-topic.
    base = re.sub(r"[^0-9A-Za-z]+", "", topic)[:8].upper()
    if len(base) < 3:
        base = "T" + hashlib.sha1(topic.encode("utf-8")).hexdigest()[:6].upper()
    evidence_dir = kb_root / "evidence"
    used = next_event_id.scan(evidence_dir) if evidence_dir.is_dir() else {}
    claimed: dict[str, dict] = {
        str(record.get("prefix")): record for record in next_event_id.list_claims(kb_root)
    }
    # Re-read the claim map inside the loop: the snapshot above is stale the
    # moment a concurrent run reserves something. The O_EXCL in claim() is the
    # real arbiter; the map only saves us from probing taken names.
    for attempt in range(50):
        candidate = f"EA-{base}-{year}" if attempt == 0 else f"EA-{base}-{year}-{attempt + 1}"
        if candidate in used or candidate in claimed:
            continue
        payload = {"prefix": candidate, "run": run_json_path.parent.name, "topic": topic}
        if locks.claim(kb_root, f"event-prefix/{candidate}", payload):
            log(f"[DRIVER] 事件 ID 前缀已预留：{candidate}（{kb_root / '.claims'}）")
            return candidate
        # Lost the race on THIS name — mark it taken locally and keep going.
        claimed[candidate] = {}
    raise RuntimeError(
        f"event-prefix: exhausted 50 candidates for {topic!r} under {kb_root / '.claims'}; "
        "concurrent runs are holding every name in the namespace"
    )


def ensure_event_prefix(kb_root: Path, run_json_path: Path, manifest: dict) -> str:
    """Manifest event_prefix, or a freshly claimed one written back to run.json.

    Shared by the abstract-evidence stage and the deep-read projection: both
    allocate from the same citable ``{prefix}-NNNN`` namespace, so whichever
    runs first reserves the prefix exactly once."""
    existing = manifest.get("event_prefix")
    if isinstance(existing, str) and existing:
        return existing
    prefix = claim_event_prefix(kb_root, run_json_path, manifest)
    write_sync(kb_root, run_json_path, lambda m: m.update({"event_prefix": prefix}))
    return prefix


def _stamp_evidence_scale(kb_root: Path, run_json_path: Path, evidence_dir: Path, events: int) -> None:
    """Write the evidence scale into run.json. check_run_bundle requires
    event_count to match the bundle's evidence; only the driver knows it at
    projection time, so stamp it here instead of leaving the writer agent to
    reverse-engineer the gate and hand-patch the manifest.

    ``events`` is the whole set (abstract tier included). ``evidence_papers``
    counts only full-text-tier papers — the finalize cited-paper floor keeps
    measuring deep-read coverage, which abstract positioning never contributes
    to — and ``abstract_papers`` records the abstract tier separately."""
    full_text_papers = sum(
        1 for path in evidence_dir.glob("*.jsonl")
        if path.name != ABSTRACT_FILENAME
        and any(line.strip() for line in path.read_text(encoding="utf-8").splitlines())
    )
    abstract_papers = {
        str((event.get("paper") or {}).get("arxiv_id") or "")
        for event in read_events(evidence_dir / ABSTRACT_FILENAME)
    } - {""}
    write_sync(kb_root, run_json_path, lambda m: m.update(
        {
            "event_count": events,
            "evidence_papers": full_text_papers,
            "abstract_papers": len(abstract_papers),
        }
    ))


def abstract_evidence_stage(
    kb_root: Path,
    run_dir: Path,
    run_json_path: Path,
    knowledge_ids: list[str],
    args: argparse.Namespace,
    summary_extra: dict,
    screening_ids: Path | None = None,
) -> None:
    """Project *selection-accepted* registry metadata into abstract-tier
    evidence events (stage: abstract-evidence). Abstracts are positioning-only
    material — related-work landscape, never mechanism-level claims. The scope
    is ``screening-ids.txt``: a registry candidate the selector rejected is
    never positioning evidence (2026-10-13 手部姿态估计 leaked 108 rejected
    papers into the appendix at whole-registry scope). Held papers are inside
    the selection set and keep their event.

    Missing ``screening-ids.txt`` skips the stage with a warning — falling
    back to the whole registry would restore that bug. Events share the run's
    event-ID prefix with the deep-read projection (the deep-read start sequence
    is computed after this file exists). Idempotent on the output file."""
    screening_ids = screening_ids or (run_dir / "screening-ids.txt")
    basis = "screened" if screening_ids.is_file() else "skipped"
    summary_extra["abstract_basis"] = basis
    evidence_dir = run_dir / "evidence"
    target = evidence_dir / ABSTRACT_FILENAME
    if not args.force and outputs_exist(target):
        existing = read_events(target)
        summary_extra["abstract_events"] = len(existing)
        log(stage_line("abstract-evidence", f"skipped (outputs present, {len(existing)} events)"))
        return
    if not screening_ids.is_file():
        summary_extra["abstract_events"] = 0
        log("[DRIVER-WARN] 未找到 screening-ids.txt，跳过摘要级（不回退全 registry）")
        return
    include = {
        line.strip()
        for line in screening_ids.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    prefix = ensure_event_prefix(kb_root, run_json_path, manifest)
    registry = json.loads((run_dir / "candidate-registry.json").read_text(encoding="utf-8"))
    # Deep-read evidence does not exist yet at this point, so nothing to exclude:
    # the packet drops abstract events for papers that later deep-read.
    events = build_abstract_events(
        registry,
        topic=args.topic,
        topic_id=knowledge_ids[0] if knowledge_ids else "EA-DATA",
        prefix=prefix,
        start_seq=1,
        include_arxiv_ids=include,
    )
    write_abstract_tier(events, evidence_dir)
    summary_extra["abstract_events"] = len(events)
    log(stage_line(
        "abstract-evidence",
        f"{len(events)} 条摘要级事件（选文通过 {len(include)} 篇，tier: abstract，仅定位用）",
    ))


def project_evidence(kb_root: Path, run_dir: Path, run_json_path: Path, summary_extra: dict) -> None:
    """Project evidence events from every audited paper note.
    Chain: next_event_id → project_evidence_events per paper → merged JSONL.

    Idempotency is per paper: an existing non-empty ``evidence/<paper>.jsonl``
    is kept as-is, so a resume that only owes a few papers does not re-project
    the rest (a run whose evidence directory holds only the abstract tier must
    still project its deep-read events)."""
    notes_dir = run_dir / "paper-notes"
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    id_prefix = ensure_event_prefix(kb_root, run_json_path, manifest)
    # Deep-read events continue the abstract tier's numbering (same citable
    # namespace): the highest allocated ID across every evidence JSONL sets
    # the next sequence.
    existing_events = [
        event
        for path in sorted(evidence_dir.glob("*.jsonl"))
        for event in read_events(path)
    ]
    start_seq = max_event_seq(existing_events) + 1
    projected = 0
    projection_blocked: list[dict[str, str]] = []
    for note_path in sorted(notes_dir.glob("*.json")):
        if note_path.name.endswith(".audit.json"):
            continue
        output = evidence_dir / f"{note_path.stem}.jsonl"
        if output.is_file() and any(
            line.strip() for line in output.read_text(encoding="utf-8").splitlines()
        ):
            continue  # per-paper idempotency: already projected
        audit_path = note_path.with_name(note_path.stem + ".audit.json")
        if not audit_path.is_file():
            continue
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
        pass_cards = [
            str(item.get("card_id") or "")
            for item in audit.get("cards") or []
            if isinstance(item, dict) and item.get("status") == "pass"
        ]
        if not pass_cards:
            # Nothing projectable: structural audit failure (validation /
            # extraction) or every card rejected. The funnel already reports
            # these as audit-reject / deep-read-failed — do not double-count.
            continue
        result = run_command([
            sys.executable, str(PROJECT_SCRIPT), "project-evidence-events",
            "--paper-note", str(note_path),
            "--audit", str(audit_path),
            "--id-prefix", id_prefix,
            "--start-seq", str(start_seq),
            "--output", str(output),
        ])
        if result.returncode:
            # Surface the projector's own reason — the old bare `exit 2` made
            # every shortfall look like a deep-read failure (2026-10-15 纹理映射).
            detail = (result.stderr or result.stdout or "").strip()
            reason = detail.splitlines()[-1] if detail else f"exit {result.returncode}"
            log(f"[DRIVER-WARN] project {note_path.stem}: {reason}")
            projection_blocked.append({"paper_id": note_path.stem, "reason": reason})
            continue
        count = sum(1 for line in output.read_text(encoding="utf-8").splitlines() if line.strip())
        start_seq += count
        projected += count
        log(f"[PAPER] {note_path.stem} 投影 {count} 条证据事件")
        # Partial drops stay visible: cards without a passing audit are now
        # skipped instead of zeroing the paper, but the loss is still a loss.
        note = json.loads(note_path.read_text(encoding="utf-8"))
        note_cards = {
            str(card.get("card_id") or "")
            for card in note.get("evidence_cards") or []
            if isinstance(card, dict)
        }
        dropped = sorted(cid for cid in note_cards if cid and cid not in set(pass_cards))
        if dropped:
            reason = f"{len(dropped)} 张卡未过 claim-support 审计未投影: {', '.join(dropped)}"
            log(f"[DRIVER-WARN] project {note_path.stem}: {reason}")
            projection_blocked.append({"paper_id": note_path.stem, "reason": reason})
    summary_extra["projection_blocked"] = projection_blocked
    # evidence_events stays deep-read-only (the abstract tier is positioning,
    # not accepted evidence); the whole-set total goes into run.json.
    deep_read_events = sum(
        len(read_events(path))
        for path in sorted(evidence_dir.glob("*.jsonl"))
        if path.name != ABSTRACT_FILENAME
    )
    abstract_events = len(read_events(evidence_dir / ABSTRACT_FILENAME))
    summary_extra["evidence_events"] = deep_read_events
    _stamp_evidence_scale(kb_root, run_json_path, evidence_dir, deep_read_events + abstract_events)
    log(stage_line("project", f"{projected} 条深读证据事件（前缀 {id_prefix}，合计 {deep_read_events + abstract_events} 含摘要级）"))
    projection_lines = [
        f"{path.stem}  {len(read_events(path))} 条"
        for path in sorted(evidence_dir.glob("*.jsonl"))
        if path.name != ABSTRACT_FILENAME
    ]
    projection_lines.append(f"（摘要级 {abstract_events} 条，仅定位用）")
    brief(
        "project",
        f"证据投影 · 全文 {deep_read_events} 条 / 摘要 {abstract_events} 条",
        projection_lines,
    )


def review_packet_stage(run_dir: Path, args, summary_extra: dict) -> None:
    """Stage: review-packet — consolidate evidence.jsonl and render
    review-packet / writing-brief / evidence-appendix from the FINAL evidence
    set. build_review_packet is mechanical, so doing it here keeps the
    appendix in lockstep with projected events: a resumed deep-read round
    used to leave the appendix without the new anchors and the writer
    chasing dead ones (20260929 图像粗配准). The writer reads the rendered
    packet; run_status's [next] command remains the manual fallback."""
    evidence_jsonl = consolidate_evidence(run_dir)
    outputs = [
        run_dir / "review-packet.md",
        run_dir / "writing-brief.md",
        run_dir / "evidence-appendix.md",
    ]
    lines = [line for line in evidence_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
    fingerprint = {"events": len(lines)}
    if lines:
        try:
            fingerprint["last_event_id"] = str(json.loads(lines[-1]).get("event_id") or "")
        except json.JSONDecodeError:
            fingerprint["last_event_id"] = ""
    stamp_path = run_dir / ".review-packet.stamp.json"
    if (
        not args.force
        and outputs_exist(*outputs)
        and stamp_path.is_file()
        and json.loads(stamp_path.read_text(encoding="utf-8")) == fingerprint
    ):
        log(stage_line("review-packet", f"skipped (outputs present, evidence unchanged: {fingerprint['events']} events)"))
        return
    command = [
        sys.executable,
        str(REVIEW_PACKET_SCRIPT),
        "review-packet",
        "--run-dir", str(run_dir),
        "--topic", args.topic,
        "--review-mode", args.review_mode,
        "--evidence-jsonl", str(evidence_jsonl),
    ]
    coverage_output = run_dir / "coverage-report.json"
    if coverage_output.is_file():
        command += ["--coverage-report", str(coverage_output)]
    reading_summary = run_dir / "reading-summary.json"
    if reading_summary.is_file():
        command += ["--reading-summary", str(reading_summary)]
    result = run_command(command)
    if result.returncode:
        raise DriverError(f"review packet exit {result.returncode}")
    stamp_path.write_text(json.dumps(fingerprint, ensure_ascii=False) + "\n", encoding="utf-8")
    summary_extra["review_packet_events"] = fingerprint["events"]
    log(stage_line("review-packet", f"{fingerprint['events']} events rendered into packet/brief/appendix"))
    brief(
        "review-packet",
        f"综述包渲染 · {fingerprint['events']} 条证据事件",
        [
            "review-packet.md — 简报（证据面 + 可用图表）",
            "writing-brief.md — 写作合同（必需节/篇幅/链接预算/句长）",
            "evidence-appendix.md — 全量证据附录（锚点）",
        ],
    )


def _audited_note(note_path: Path, audit_path: Path | None = None) -> bool:
    """A note counts as done only when its audit actually passed — reject/failed
    stubs (empty note + status: reject audit) must stay retryable."""
    audit_path = audit_path or note_path.with_name(note_path.stem + ".audit.json")
    if not note_path.is_file() or not audit_path.is_file():
        return False
    try:
        return json.loads(audit_path.read_text(encoding="utf-8")).get("status") in {"pass", "needs-review"}
    except (OSError, ValueError):
        return False


def projection_units(passed: int, needs_review: int) -> int:
    """How many of these deep-read outcomes count toward the evidence floor.

    PROJECTION units, not read units. ``evidence_projection.project()`` now
    emits each passing card even when a sibling card is needs-review
    (2026-10-15), but a needs-review paper is only projectable if at least one
    card passed — unknown at this point — so the floor counter stays
    conservative and counts full-pass papers only. Counting needs-review made
    13 pass + 6 needs-review read as "19 ≥ 15", skipped the 候补 fill, and left
    coverage at 13/15 (2026-10-14 时空智能体). ``needs_review`` is kept in the
    signature only so callers pass it explicitly and the exclusion is visible
    at the call site."""

    return int(passed)


def deep_read_order(screened: list[str], seeds: list[str], limit: int | None) -> list[str]:
    """Deep-read queue: seeds first, then screening order.

    Screening is influence-scored, so a just-published seed paper (few
    citations by construction) ranks below the cut — observed in the 20260924
    单目深度估计 run where the seed never got deep-read. Seeds are the user's
    own framing of the topic: force them to the front.

    ``limit=None`` returns the full scored order (the 候补 waitlist lives past
    the first ``limit``)."""

    seeds = [seed for seed in seeds if seed]
    ordered = seeds + [paper_id for paper_id in screened if paper_id not in seeds]
    if limit is None:
        return ordered
    return ordered[:limit]


def _failure_note_path(notes_dir: Path, paper_id: str) -> Path | None:
    """paper_id becomes a filename: reject anything that is not a plain id
    (a malformed screening line must never become a path)."""
    if not paper_id or len(paper_id) > 64 or any(ch in paper_id for ch in "/\\\0"):
        return None
    return notes_dir / f"{paper_id}.failed.json"


def _record_deep_read_failure(notes_dir: Path, paper_id: str, outcome: str, reason: str) -> None:
    """Persist why a paper stopped: run_status surfaces these reasons (the
    dialog line alone was invisible to later sessions)."""
    path = _failure_note_path(notes_dir, paper_id)
    if path is None:
        return
    path.write_text(
        json.dumps({"outcome": outcome, "reason": reason}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _clear_deep_read_failure(notes_dir: Path, paper_id: str) -> None:
    path = _failure_note_path(notes_dir, paper_id)
    if path is not None:
        path.unlink(missing_ok=True)


def deep_read(run_dir: Path, run_json_path: Path, screening_ids: Path, args, summary_extra: dict,
              ledger: SessionLog | None = None) -> None:
    """Per-paper skeleton agents (parallel one-shot claude) + local assembly.

    Progress is one stdout line per paper event so the wiki dialog shows
    movement instead of a silent wait."""
    cli = resolve_cli()
    if not cli:
        log("[DRIVER] claude CLI 不存在，跳过深读阶段（note 不会生成）")
        return
    pool_root = pool_root_for(args.kb_root)
    limit = args.deep_read_limit or DEEP_READ_LIMITS[args.review_mode]
    # run.json carries no seed_ids (init_run doesn't know them); the retrieval
    # stage already stashed them in summary_extra.
    seeds = [str(s).strip() for s in (summary_extra.get("seed_ids") or []) if str(s).strip()]
    screened = [
        line.strip()
        for line in screening_ids.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    order = deep_read_order(screened, seeds, limit=None)
    waitlist = order[limit:]
    order = order[:limit]
    summary_extra["deep_read_limit"] = limit
    summary_extra["deep_read_waitlist"] = len(waitlist)

    notes_dir = run_dir / "paper-notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    todo = [
        paper_id
        for paper_id in order
        if not (
            _audited_note(notes_dir / f"{paper_id}.json")
            and _audited_note(
                pool_root / f"arxiv-{paper_id}" / "note.json",
                pool_root / f"arxiv-{paper_id}" / "note.json.audit.json",
            )
        )
    ]
    passed = needs_review = failed = 0
    reused = len(order) - len(todo)
    if reused:
        log(f"[DRIVER] 复用池内已有深读笔记 {reused} 篇")
        passed += reused  # reused notes already cleared their per-paper audit
        done = reused
        outcomes = [
            (paper_id, "pass", "复用已有深读笔记")
            for paper_id in order
            if paper_id not in set(todo)
        ]
    else:
        done = 0
        outcomes = []
    log(f"[DRIVER] 深读开始：{len(todo)} 篇并行（每批 {args.agents_parallel}）")
    # Papers whose first pass failed but whose full text is on disk: candidates
    # for the retry pass below (upstream instability under parallel load).
    failed_ids: list[str] = []

    def absorb(
        paper_id: str, outcome: str, deep_reason: str,
        *, note: str = "", failure_prefix: str = "",
    ) -> None:
        """Copy the pooled note (when one was built) and fold one outcome into
        the counters/outcomes. Shared by the first pass, the retry pass and
        the waitlist fill (``note``/``failure_prefix`` label the latter two)."""
        nonlocal passed, needs_review, failed
        pooled_note = pool_root / f"arxiv-{paper_id}" / "note.json"
        pooled_audit = pool_root / f"arxiv-{paper_id}" / "note.json.audit.json"
        if pooled_note.is_file():
            shutil.copyfile(pooled_note, notes_dir / f"{paper_id}.json")
            if pooled_audit.is_file():
                shutil.copyfile(pooled_audit, notes_dir / f"{paper_id}.audit.json")
        # Only exceptions to the norm go to the dialog; steady progress lives
        # on the progress bar. Failure reasons are persisted so run_status can
        # report WHY a paper stopped (log-only reasons were invisible to the
        # writer).
        if outcome == "pass":
            passed += 1
            _clear_deep_read_failure(notes_dir, paper_id)
            outcomes.append((paper_id, "pass", note))
        elif outcome == "needs-review":
            needs_review += 1
            _clear_deep_read_failure(notes_dir, paper_id)
            outcomes.append((
                paper_id, "needs-review",
                f"{note} · 审计 needs-review（可用）" if note else "审计 needs-review（可用）",
            ))
            log(f"[PAPER] {paper_id} 审计 needs-review（可用）")
        else:
            failed += 1
            reason = deep_reason or f"深读失败（{outcome}）"
            if failure_prefix:
                reason = f"{failure_prefix}深读失败（{reason}）"
            _record_deep_read_failure(notes_dir, paper_id, str(outcome), reason)
            outcomes.append((paper_id, "failed", reason))
            log(f"[PAPER] {paper_id} 深读失败（{reason}）")
            if paper_id not in failed_ids:
                failed_ids.append(paper_id)
            return
        if paper_id in failed_ids:
            failed_ids.remove(paper_id)

    def forget_failure(paper_id: str) -> None:
        """Drop a paper's earlier failed row before recording its retry, so one
        recovered paper counts once (as pass/needs-review, not twice)."""
        nonlocal failed
        if paper_id in failed_ids:
            failed -= 1
            failed_ids.remove(paper_id)
        outcomes[:] = [
            item for item in outcomes
            if not (item[0] == paper_id and item[1] == "failed")
        ]

    for batch_start in range(0, len(todo), args.agents_parallel):
        chunk = todo[batch_start : batch_start + args.agents_parallel]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunk)) as executor:
            futures = {}
            for paper_id in chunk:
                if not (pool_root / f"arxiv-{paper_id}" / "extraction.json").is_file():
                    # Say WHY: a 121-byte timeout stub and a full extraction
                    # that failed to pool look identical behind the old
                    # "extraction.json 缺失" wording (2026-10-08).
                    run_extraction = run_dir / "extractions" / f"{paper_id}.json"
                    if not run_extraction.is_file():
                        reason = "全文未恢复（无 extraction 产物）"
                    else:
                        try:
                            payload = json.loads(run_extraction.read_text(encoding="utf-8"))
                        except (OSError, json.JSONDecodeError):
                            payload = {}
                        if str(payload.get("error") or "").strip():
                            reason = f"全文未恢复（{payload['error']}）"
                        elif payload.get("available"):
                            reason = "全文已恢复但未入池（pool-add 失败，见上文日志）"
                        else:
                            reason = "全文未恢复（抽取产物不可用）"
                    futures[paper_id] = None
                    done += 1
                    failed += 1  # consistent with the pre-2026-09 summary semantics
                    _record_deep_read_failure(notes_dir, paper_id, "no-extraction", reason)
                    outcomes.append((paper_id, "failed", reason))
                    log(f"[DRIVER-PROGRESS:deep-read:{done}/{len(order)}]")
                    log(f"[PAPER] {paper_id} {reason}，跳过")
                    continue
                futures[paper_id] = executor.submit(
                    deep_read_paper, paper_id, pool_root, cli,
                    agent_timeout_s=args.agent_timeout,
                    skeleton_path=run_dir / f"skel-{paper_id}.json",
                    ledger=ledger,
                )
            for paper_id, future in futures.items():
                if future is None:
                    continue  # counted when skipped at submission
                try:
                    outcome, deep_reason = future.result()
                except Exception as exc:  # noqa: BLE001 - per-paper isolation
                    outcome = "failed"
                    deep_reason = f"agent 异常：{exc}"
                    log(f"[PAPER] {paper_id} agent 异常：{exc}")
                done += 1
                log(f"[DRIVER-PROGRESS:deep-read:{done}/{len(order)}]")
                absorb(paper_id, outcome, deep_reason)
    # ---- 重试：并发下上游不稳定，失败但全文已恢复的论文再读一遍 ----------
    # The extraction queue already does a HELD second pass for the same reason
    # (rate limits / hard timeouts under load). Deep reads had no such pass:
    # one failed skeleton call wrote <id>.failed.json and the paper was lost
    # for the run even though its full text was on disk. Papers without an
    # extraction are excluded — their bottleneck is the fetch, which this
    # pass cannot fix.
    for retry_round in range(1, DEEP_READ_RETRY_PASSES + 1):
        retry_ids = [
            paper_id for paper_id in failed_ids
            if (pool_root / f"arxiv-{paper_id}" / "extraction.json").is_file()
        ]
        if not retry_ids:
            break
        log(
            f"[DRIVER] 深读重试第 {retry_round}/{DEEP_READ_RETRY_PASSES} 轮："
            f"{len(retry_ids)} 篇（首轮失败且全文已恢复，上游不稳定时一次重试多数能过）"
        )
        for batch_start in range(0, len(retry_ids), args.agents_parallel):
            chunk = retry_ids[batch_start : batch_start + args.agents_parallel]
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(chunk)) as executor:
                futures = {
                    paper_id: executor.submit(
                        deep_read_paper, paper_id, pool_root, cli,
                        agent_timeout_s=args.agent_timeout,
                        skeleton_path=run_dir / f"skel-{paper_id}.json",
                        ledger=ledger,
                    )
                    for paper_id in chunk
                }
                for paper_id, future in futures.items():
                    try:
                        outcome, deep_reason = future.result()
                    except Exception as exc:  # noqa: BLE001 — per-paper isolation
                        outcome = "failed"
                        deep_reason = f"agent 异常：{exc}"
                        log(f"[PAPER] {paper_id} 重试 agent 异常：{exc}")
                    forget_failure(paper_id)
                    absorb(
                        paper_id, outcome, deep_reason,
                        note="重试补读", failure_prefix="重试",
                    )
                    log(f"[DRIVER-RETRY] {paper_id} {outcome}"
                        + (f" · {deep_reason}" if deep_reason else ""))
    # ---- 候补：可投影篇数不足地板时按评分补读 ---------------------------
    # The floor is counted in PROJECTION units, not read units: a needs-review
    # paper is only projectable if at least one card passed, which is unknown
    # here, so it is not counted. Counting it made 13 pass + 6 needs-review
    # read as "19 ≥ 15", skipped the 候补 fill, and left coverage at 13/15 —
    # the exact shape of the 2026-10-14 时空智能体 run that stopped instead of
    # reading on.
    floor = int(EVIDENCE_FLOORS.get(args.review_mode) or 0)
    accepted = projection_units(passed, needs_review)
    filled: list[str] = []
    if floor and accepted < floor and waitlist:
        log(
            f"[DRIVER] 可投影 {accepted} 篇 < 地板 {floor}（另有 needs-review "
            f"{needs_review} 篇不计），从候补按评分补读（缺 {floor - accepted}，"
            f"候补 {len(waitlist)} 篇）"
        )
        for paper_id in waitlist:
            if accepted >= floor:
                break
            # reuse the same per-paper path: skip → agent → copy note → count
            run_extraction = run_dir / "extractions" / f"{paper_id}.json"
            if not (pool_root / f"arxiv-{paper_id}" / "extraction.json").is_file():
                reason = "全文未恢复（无 extraction 产物）"
                if run_extraction.is_file():
                    try:
                        payload = json.loads(run_extraction.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        payload = {}
                    if str(payload.get("error") or "").strip():
                        reason = f"全文未恢复（{payload['error']}）"
                    elif payload.get("available"):
                        reason = "全文已恢复但未入池（pool-add 失败）"
                failed += 1
                filled.append(paper_id)
                _record_deep_read_failure(notes_dir, paper_id, "no-extraction", reason)
                outcomes.append((paper_id, "failed", reason))
                log(f"[PAPER] {paper_id} 候补 {reason}，跳过")
                continue
            try:
                outcome, deep_reason = deep_read_paper(
                    paper_id, pool_root, cli,
                    agent_timeout_s=args.agent_timeout,
                    skeleton_path=run_dir / f"skel-{paper_id}.json",
                    ledger=ledger,
                )
            except Exception as exc:  # noqa: BLE001 — per-paper isolation
                outcome = "failed"
                deep_reason = f"agent 异常：{exc}"
                log(f"[PAPER] {paper_id} agent 异常：{exc}")
            filled.append(paper_id)
            absorb(
                paper_id, outcome, deep_reason,
                note="候补补读", failure_prefix="候补补读",
            )
            accepted = projection_units(passed, needs_review)
            log(f"[PAPER] {paper_id} 候补 {outcome}，累计可投影 {accepted}/{floor}")
        log(f"[DRIVER] 候补补读 {len(filled)} 篇，可投影合计 "
            f"{projection_units(passed, needs_review)} / 地板 {floor}"
            f"（needs-review {needs_review} 篇不计）")
    summary_extra["deep_read"] = {"total": len(order) + len(filled), "pass": passed, "needs_review": needs_review, "failed": failed}
    summary_extra["deep_read_filled"] = filled
    summary_extra["evidence_floor"] = floor
    total = len(order) + len(filled)
    log(stage_line("deep-read", f"{passed} pass / {needs_review} needs-review / {failed} failed（共 {total} 篇）"))
    outcome_rank = {"pass": 0, "needs-review": 1, "failed": 2}
    outcomes.sort(key=lambda item: (outcome_rank.get(item[1], 3), item[0]))
    brief(
        "deep-read",
        f"精读结果 · {passed} pass / {needs_review} needs-review / {failed} failed（共 {total} 篇）",
        [
            f"{paper_id}  [{outcome}]" + (f"  {note}" if note else "")
            for paper_id, outcome, note in outcomes
        ],
    )


def run_skeleton_agent(
    cli: str, paper_id: str, pool_root: Path, timeout_s: float,
    *, attempts: int | None = None, ledger: SessionLog | None = None,
) -> dict | None:
    """One one-shot claude call returning the paper's claim skeleton.

    Non-zero exits, unparseable output AND timeouts retry up to
    ``SKELETON_AGENT_ATTEMPTS`` total tries. Timeouts used to return
    immediately ("the budget is already spent"), but deep reads run several
    agents concurrently and an overloaded upstream surfaces exactly that way:
    the 2026-10-16 强化学习 run lost 20/43 deep reads to skeleton calls that
    died mid-stream. A retried paper costs about one extra read; a lost paper
    costs evidence, so one more timeout budget is the cheaper side. A spawn
    failure (missing CLI) still fails fast on the first try — retrying it only
    burns the wall clock."""
    total = max(1, int(attempts if attempts is not None else SKELETON_AGENT_ATTEMPTS))
    for attempt in range(1, total + 1):
        try:
            result = complete(
                build_skeleton_prompt(paper_id, pool_root), timeout_s=timeout_s, cli=cli,
                cwd=DRIVER_CWD, label=f"skeleton:{paper_id}", ledger=ledger,
            )
        except subprocess.TimeoutExpired:
            log(f"[DRIVER-WARN] {paper_id} 骨架 agent 超时（{timeout_s:.0f}s，"
                f"第 {attempt}/{total} 次）")
            continue
        except OSError as exc:
            log(f"[DRIVER-WARN] {paper_id} 骨架 agent 启动失败：{exc}")
            return None
        if result.returncode:
            reason = (result.stderr or result.stdout or "").strip().splitlines()
            log(f"[DRIVER-WARN] {paper_id} 骨架 agent exit {result.returncode}"
                f"（第 {attempt}/{total} 次）：{reason[-1] if reason else '无输出'}")
            continue
        skeleton = read_skeleton_output(result.stdout)
        if skeleton is not None:
            return skeleton
        head = re.sub(r"\s+", " ", (result.stdout or "").strip())[:100]
        log(f"[DRIVER-WARN] {paper_id} 骨架 agent 输出不可解析（第 {attempt}/{total} 次）：{head!r}")
    return None


def deep_read_paper(
    paper_id: str,
    pool_root: Path,
    cli: str,
    *,
    agent_timeout_s: float = 420.0,
    skeleton_path: Path | None = None,
    ledger: SessionLog | None = None,
) -> tuple[str, str]:
    """Deep-read one pooled paper: skeleton agent → build_paper_note assembly
    + audit. Returns ``(status, reason)`` where status is 'pass' |
    'needs-review' | 'failed' and reason is a human-readable failure cause
    (empty on pass). Shared by the batch driver and the single-paper chat
    preparation (they log differently, so logging stays with the callers)."""

    skeleton = run_skeleton_agent(cli, paper_id, pool_root, agent_timeout_s, ledger=ledger)
    if not skeleton:
        return "failed", "骨架 agent 失败（详见上文 [DRIVER-WARN]）"
    if skeleton_path is None:
        skeleton_path = Path(tempfile.gettempdir()) / f"skel-{paper_id}-{os.getpid()}.json"
    skeleton_path.write_text(json.dumps(skeleton, ensure_ascii=False), encoding="utf-8")
    result = run_command([
        sys.executable, str(READ_SCRIPT),
        "build-paper-note",
        "--arxiv-id", paper_id,
        "--skeleton", str(skeleton_path),
        "--pool-root", str(pool_root.parent),
    ])
    outcome = "unknown"
    try:
        outcome = str(json.loads(result.stdout).get("status") or "unknown")
    except (json.JSONDecodeError, TypeError):
        pass
    if result.returncode == 0 and outcome == "pass":
        return "pass", ""
    if outcome == "needs-review" or (result.returncode == 3 and outcome == "unknown"):
        return "needs-review", ""
    tail = (result.stderr or result.stdout or "").strip().splitlines()
    reason = (
        f"build-paper-note exit {result.returncode}"
        + (f"：{tail[-1]}" if tail else "：无输出")
        if result.returncode
        else f"审计 status={outcome}"
    )
    return "failed", reason


def pool_seed(summary_extra: dict, screening_ids: Path, run_dir: Path, args) -> None:
    """Backfill the shared pool from this run's fresh extractions/HTML so later
    topics (and the wiki reader) answer from the pool instead of re-fetching.
    Also records how many screened papers were already pool-warm."""
    pool_root = pool_root_for(args.kb_root)
    if not screening_ids.is_file():
        return
    warm = cold = held = 0
    add_cmd_base = [
        sys.executable, str(SKILLS_ROOT / "embodied-ai-paper-reader" / "scripts" / "read.py"), "pool-add-paper", "add",
        "--pool-root", str(pool_root),
    ]
    ids = [line.strip() for line in screening_ids.read_text(encoding="utf-8").splitlines() if line.strip()]
    for paper_id in ids:
        pool_dir = pool_root / f"arxiv-{paper_id}"
        if pool_dir.is_dir() and (pool_dir / "extraction.json").is_file():
            warm += 1
            continue  # already pooled
        extraction = run_dir / "extractions" / f"{paper_id}.json"
        if not extraction.is_file():
            continue
        # The extraction FILE existing is not the same as the paper being
        # recovered: a HELD/failed extraction checkpoints a payload with
        # available=False. Only a real recovery is pool-worthy — calling
        # pool-add on the rest produced the self-contradictory
        # "extraction 已恢复但未进 pool：extraction is not available".
        try:
            payload = json.loads(extraction.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        if not payload.get("available"):
            held += 1
            continue
        html_cache = kb_cache_dir(args.kb_root) / "html" / f"{paper_id}.html"
        command = list(add_cmd_base) + ["--extraction", str(extraction), "--force"]
        if html_cache.is_file():
            command += ["--html", str(html_cache)]
        result = run_command(command)
        if result.returncode == 0:
            cold += 1
            continue
        # A failed pool-add must be visible: it used to vanish and resurface
        # later as "未入池（extraction.json 缺失）" with no way to tell a good
        # extraction from a failed one (2026-10-08, 2507.15186).
        reason = (result.stderr or result.stdout or "").strip().splitlines()
        log(
            f"[PAPER] {paper_id} 入池失败（extraction 可用但未进 pool）："
            f"{reason[-1] if reason else f'exit {result.returncode}'}"
        )
    summary_extra["pool_warm"] = warm
    summary_extra["pool_seeded"] = cold
    summary_extra["pool_skipped_held"] = held


def command_label(command: list[str]) -> str:
    """Human label for a spawned command: the script basename plus its
    subcommand (``python3 …/search.py search-arxiv`` → ``search.py search-arxiv``)."""
    for index, item in enumerate(command):
        if item.endswith(".py"):
            label = Path(item).name
            if index + 1 < len(command) and not command[index + 1].startswith("-"):
                label += f" {command[index + 1]}"
            return label
    return Path(command[0]).name if command else "?"


def run_stage(
    name: str,
    outputs: list[Path],
    force: bool,
    command_builder: "callable",
    *,
    timeout: float | None = None,
    stream: bool = False,
    on_line: "callable | None" = None,
    soft_exit_codes: frozenset[int] = frozenset(),
    ledger: "SessionLog | None" = None,
) -> str:
    """Idempotent stage runner: skip when outputs exist, else run the built
    command and verify the outputs landed. ``stream=True`` forwards the child's
    stdout line by line through ``on_line`` so long stages (full-text
    extraction) report per-paper progress into the wiki dialog instead of
    buffering until completion. ``soft_exit_codes`` lists non-zero exits that
    still count as "ran" when the outputs landed (retrieval returns 1 for a
    partial batch: some queries failed, the hits are saved, and the run should
    proceed with the hole visible rather than abort). ``ledger`` receives one
    ``step`` on entry, a ``metric`` with the stage duration on success, and an
    ``error`` line on failure (usage-records-format trace layer)."""
    begun = time.monotonic()
    if not force and outputs_exist(*outputs):
        detail = "skipped (outputs present)"
        if ledger is not None:
            ledger.event(
                level="info", kind="step", text=name,
                stage=name, skipped=True,
            )
        log(stage_line(name, detail))
        return detail
    # Announce BEFORE blocking: a stage that runs for minutes with no output
    # reads as a hang to anyone watching the dialog (2026-10-13: 13 silent
    # minutes between "注册 558 篇去重候选" and "精读候选 29 篇").
    log(f"[DRIVER] {name} 开始…")
    command = command_builder()
    if ledger is not None:
        ledger.step(name, command=command_label(command))
    if stream:
        captured: list[str] = []
        process = subprocess.Popen(
            command, cwd=str(DRIVER_CWD), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        assert process.stdout is not None
        for line in process.stdout:
            stripped = line.rstrip()
            captured.append(stripped)
            if stripped and on_line:
                on_line(stripped)
        try:
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            log(f"[DRIVER-WARN] {name} 阶段超时（{timeout:.0f}s），已 kill；"
                "可 --force 续跑该阶段或加大其超时")
            if ledger is not None:
                ledger.error(
                    f"{name} stage timed out after {timeout:.0f}s",
                    stage=name, timeout_s=timeout,
                    duration_s=round(time.monotonic() - begun, 3),
                )
            process.kill()
            process.wait()
            returncode = -1
        result = subprocess.CompletedProcess(command, returncode, "\n".join(captured[-10:]), "")
    else:
        try:
            result = run_command(command, timeout=timeout)
        except subprocess.TimeoutExpired:
            log(f"[DRIVER-WARN] {name} 阶段超时（{timeout:.0f}s），已中止；"
                "可 --force 续跑该阶段或加大其超时")
            if ledger is not None:
                ledger.error(
                    f"{name} stage timed out after {timeout:.0f}s",
                    stage=name, timeout_s=timeout,
                    duration_s=round(time.monotonic() - begun, 3),
                )
            raise
    if result.returncode and result.returncode not in soft_exit_codes:
        if ledger is not None:
            ledger.error(
                f"{name} stage exit {result.returncode}: "
                f"{(result.stderr or result.stdout or '')[-SESSION_EVENT_TEXT_MAX_CHARS:]}",
                stage=name, exit_code=result.returncode,
                duration_s=round(time.monotonic() - begun, 3),
            )
        raise fail(name, f"exit {result.returncode}: {(result.stderr or result.stdout)[-400:]}")
    missing = [str(path) for path in outputs if not outputs_exist(path)]
    if missing:
        if ledger is not None:
            ledger.error(
                f"{name} stage outputs missing: {', '.join(missing)}",
                stage=name, duration_s=round(time.monotonic() - begun, 3),
            )
        raise fail(name, f"outputs missing after run: {', '.join(missing)}")
    detail = f"ran: {command_label(command)}"
    if result.returncode in soft_exit_codes:
        detail += f" (exit {result.returncode} tolerated: partial batch, hits kept)"
    if ledger is not None:
        ledger.metric(
            name, time.monotonic() - begun,
            returncode=result.returncode, detail=detail,
        )
    log(stage_line(name, detail))
    return detail


SNAPSHOT_BASENAMES = (
    "arxiv-metadata-oai-snapshot.sqlite",  # SQLite/FTS5 (build-snapshot-db) — preferred
    "arxiv-metadata-oai-snapshot.jsonl",   # raw OAI JSONL
)


def autodetect_snapshot(kb_root: Path) -> Path | None:
    """Find a local arXiv metadata snapshot under the KB root. Offline
    retrieval is the default: live arXiv API calls intermittently 406/429, so
    the workflow only goes online when no snapshot exists (and says so)."""
    for basename in SNAPSHOT_BASENAMES:
        candidate = kb_root / basename
        if candidate.is_file():
            return candidate
    return None


def write_sync(kb_root: Path, run_json_path: Path, mutate) -> None:
    """Locked read-modify-write of run.json (atomic replace): concurrent
    writers of the same run (driver + launcher settle flip) cannot lose one
    another's fields. Reentrant with the driver's whole-run lock."""
    from embodied_learning.atomicio import atomic_write_json
    from embodied_learning import locks

    with locks.kb_lock(kb_root, f"run__{run_json_path.parent.name}", stale=21600):
        manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
        mutate(manifest)
        atomic_write_json(run_json_path, manifest)


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/run.py."""
    global DRIVER_CWD
    kb_root = Path(args.kb_root).expanduser().resolve()
    args.kb_root = kb_root
    DRIVER_CWD = kb_root
    try:
        start_date, end_date = parse_time_range(args.time_range)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    run_dir = Path(args.run_dir).resolve()
    if not (run_dir / "run.json").is_file():
        print(f"run.json not found in {run_dir}", file=sys.stderr)
        return 2
    for path in args.external_candidates:
        if not Path(path).is_file():
            print(f"external candidates file not found: {path}", file=sys.stderr)
            return 2
    # smart-jev needs the decision-model endpoint/key. Fail here, before hours
    # of retrieval and extraction, instead of at the screening stage when the
    # registry is already paid for (same fail-fast stance as claude_auth_ready).
    if args.selection_strategy == "smart-jev":
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
    run_json_path = run_dir / "run.json"
    # The manifest's review_mode is the contract the floors/limits are computed
    # from. A caller passing a different --review-mode silently ran the wrong
    # depth (2026-10-09: a rapid request was registered scoping). Refuse rather
    # than let the drift through — the manifest wins, and the caller fixes it.
    if run_json_path.is_file():
        try:
            _existing_mode = str(json.loads(run_json_path.read_text(encoding="utf-8")).get("review_mode") or "")
        except (OSError, json.JSONDecodeError):
            _existing_mode = ""
        if _existing_mode and _existing_mode != args.review_mode:
            raise SystemExit(
                f"review_mode drift: run.json says {_existing_mode!r} but --review-mode "
                f"was {args.review_mode!r}. Fix one of them (run.json `inputs` records "
                "what the user asked for) and re-run; refusing to guess."
            )

    # Whole-run fail-fast mutual exclusion (the duplicate-launcher hazard:
    # two concurrent drivers on one run truncated registries and downgraded
    # coverage). Waiting would only duplicate a running pipeline, so this
    # lock never waits — it reports the holder and exits. The later run.json
    # write_sync acquisitions are reentrant with this one.
    from embodied_learning import locks as _locks

    try:
        _run_lock = _locks.kb_lock(kb_root, f"run__{run_dir.name}", fail_fast=True, stale=21600)
        _run_lock.__enter__()
    except _locks.LockBusy as exc:
        print(str(exc), file=sys.stderr)
        return 4
    try:
        return _main_locked(args, kb_root, run_dir, run_json_path, start_date, end_date)
    finally:
        _run_lock.__exit__(None, None, None)


def _main_locked(
    args: argparse.Namespace,
    kb_root: Path,
    run_dir: Path,
    run_json_path: Path,
    start_date: str,
    end_date: str,
) -> int:
    global DRIVER_CWD
    cache_dir = kb_cache_dir(kb_root)
    log("[DRIVER-PHASE:plan] 查询规划与检索词生成")
    if not args.arxiv_snapshot:
        detected = autodetect_snapshot(kb_root)
        if detected:
            args.arxiv_snapshot = str(detected)
            log(f"[DRIVER] 使用本地 arXiv 快照离线检索：{detected}")
        else:
            log("[DRIVER-WARN] 本地 KB 未找到 arXiv 元数据快照"
                "（arxiv-metadata-oai-snapshot.sqlite/.jsonl），arXiv 检索将直连 API（406/429 风险）。"
                "建议先离线建库：search.py build-snapshot-db")

    started = time.monotonic()
    stage_seconds: dict[str, float] = {}
    summary_extra: dict[str, object] = {}
    cli = resolve_cli()
    # One usage/trace ledger for the whole run (monica usage-records-format):
    # every mechanical stage and every one-shot agent appends here, so a run's
    # trajectory and its token bill are one file. Caller-owned, closed below.
    ledger = open_session_log("pipeline", run_dir.name) if session_ledger_enabled() else None
    # Stage scripts spawn their own agents (smart selection, S2 expansion); the
    # inherited env makes them append to THIS run ledger instead of opening
    # sibling files. Restored in the finally block.
    inherited_ledger = os.environ.get(AGENT_SESSION_LEDGER_ENV)
    if ledger is not None:
        os.environ[AGENT_SESSION_LEDGER_ENV] = str(ledger.path)
        ledger.step(
            "pipeline",
            topic=args.topic,
            review_mode=args.review_mode,
            search_strategy=args.search_strategy,
            selection_strategy=args.selection_strategy,
            kb_root=str(kb_root),
            run_dir=str(run_dir),
        )

    def mark(stage: str, begun: float) -> None:
        stage_seconds[stage] = round(time.monotonic() - begun, 2)

    try:
        # ---- plan -------------------------------------------------------
        begun = time.monotonic()
        plan_outputs = [run_dir / "query-plan.json", run_dir / "query-plan.md"]
        seed_ids = parse_seed_ids(args.seed_arxiv_ids)

        # Bilingual bootstrapping: a pure-Chinese topic produces Chinese-only
        # arXiv queries that match nothing, so the Latin keyword tokens from
        # the mechanical split go into the plan as ONE conjunctive query
        # (all:"a" AND all:"b") — precise like the topic itself. Bare
        # per-word queries ("absolute", "pose", "estimation") flood the
        # registry with off-topic junk (高能物理/量子/NLP on 20260930) and
        # dilute smart selection; never emit those. The file also acts as the
        # merge point for dynamic queries from a prior claude session or the
        # dynamic-query agent: replanning must not silently drop them.
        dynamic_path = run_dir / "dynamic-queries.json"
        # Pure-Chinese topics carry no Latin token to conjunct — arXiv cannot
        # match CJK text, and the plan falls to 0 queries whenever the
        # dynamic-query agent also fails (2026-10-15 强化学习). One MyMemory
        # translation augments the mechanical terms with English tokens so the
        # run keeps an English query channel of its own (merged, not replaced).
        latin_terms, translated_topic = translation_terms(args.topic, args.focus)
        if translated_topic:
            log(
                f"[DRIVER] 纯中文话题无 Latin 检索词，机器翻译自举：{translated_topic} → "
                f"{' / '.join(t for t in latin_terms if t.isascii())}"
            )
        merged_queries: list[dict[str, str]] = []
        existing_dynamic: dict[str, Any] = {}
        if dynamic_path.is_file():
            try:
                existing_dynamic = json.loads(dynamic_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing_dynamic = {}
        merged_queries.extend(
            item
            for item in existing_dynamic.get("queries") or []
            if isinstance(item, dict) and item.get("query")
        )
        ascii_terms = [term for term in latin_terms if term.isascii()]
        if ascii_terms:
            combined = " AND ".join(f'all:"{term}"' for term in ascii_terms)
            if combined not in {str(item.get("query")) for item in merged_queries}:
                merged_queries.append({"label": "latin-combined", "query": combined, "tier": "dynamic-core"})

        # Idempotent resume: decide whether this run will actually rebuild the
        # plan BEFORE spending agent calls. When the plan outputs are present
        # and non-empty and nothing forces a replan, run_stage("plan") skips —
        # the agent's fresh queries would be stranded in dynamic-queries.json
        # outside the plan (2026-10-16 强化学习 resume burned two agent retries
        # before "skipped (outputs present)"). A stale empty plan is the one
        # exception: there the agent's queries are what justify the forced
        # replan (2026-10-15).
        prior_plan: dict[str, Any] = {}
        plan_outputs_present = outputs_exist(*plan_outputs)
        if plan_outputs_present:
            try:
                prior_plan = json.loads((run_dir / "query-plan.json").read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                prior_plan = {}
        prior_plan_empty = not (prior_plan.get("queries") or [])
        plan_will_run = args.force or not plan_outputs_present or prior_plan_empty

        # Smart strategy: one-shot agent generates the topic's own arXiv
        # queries (the stage whose absence sank the pure-Chinese topics on
        # 2026-09-11). Failure is non-fatal — the plan falls back to generic.
        #
        # A pure-Chinese topic has no Latin token to conjunct, so without the
        # agent the plan is left with generic all:"中文" fallbacks that arXiv
        # (an English corpus) can never match — retrieval dies at 0 candidates
        # before any downstream stage runs. There the agent is not an
        # enrichment, it is the only source of English queries: run it
        # regardless of the search strategy and say so in the log.
        dynamic_source = "merged-from-disk"
        needs_agent = args.search_strategy == "smart" or (
            not ascii_terms and not merged_queries and not seed_ids
        )
        if needs_agent and not plan_will_run:
            dynamic_source = "skipped (plan present)"
            log(
                f"[DRIVER] 查询计划已存在（{len(prior_plan.get('queries') or [])} 条查询），"
                "重跑沿用已有计划，跳过动态查询 agent（--force 强制重新规划）"
            )
        elif needs_agent and not args.no_dynamic_agent and not args.external_candidates:
            if args.search_strategy != "smart":
                log(f"[DRIVER] 话题无 Latin 检索词（策略 {args.search_strategy} 无法自举英文查询），"
                    "强制启用动态查询 agent 生成英文检索式")
            agent_payload = agent_dynamic_queries(
                args.topic, args.focus, seed_ids, args.dynamic_timeout, cli,
                ledger=ledger,
            )
            if agent_payload:
                known = {str(item.get("query")) for item in merged_queries}
                fresh = [item for item in agent_payload["queries"] if item["query"] not in known]
                merged_queries.extend(fresh)
                dynamic_source = "agent" if args.search_strategy == "smart" else "agent-forced"
                log(f"[DRIVER] 动态查询 agent 生成 {len(fresh)} 条查询")
            else:
                dynamic_source = "agent-failed"
                log("[DRIVER-WARN] 动态查询 agent 失败，回退分类法+通用查询")
        elif args.search_strategy == "fast":
            dynamic_source = "disabled (fast strategy)"

        dynamic_payload = {"queries": merged_queries}
        dynamic_path.write_text(json.dumps(dynamic_payload, ensure_ascii=False), encoding="utf-8")
        summary_extra["dynamic_source"] = dynamic_source
        summary_extra["seed_ids"] = seed_ids
        summary_extra["search_strategy"] = args.search_strategy
        if args.external_candidates:
            summary_extra["external_candidates"] = args.external_candidates

        def plan_cmd_builder() -> list[str]:  # noqa: E306
            return [
                sys.executable, str(PLANNER_SCRIPT), "build-query-plan",
                "--topic", args.topic,
                "--review-mode", args.review_mode,
                "--start-date", start_date,
                "--end-date", end_date,
                "--dynamic-file", str(dynamic_path),
                "--output", str(run_dir / "query-plan.json"),
                "--markdown-output", str(run_dir / "query-plan.md"),
            ]

        # A stale empty plan must not block replanning: after a dynamic-agent
        # failure the plan stage would skip on its leftover outputs and strand
        # the fresh dynamic-queries.json content outside the plan (2026-10-15
        # 强化学习 resume). Non-empty plans keep the idempotent skip.
        plan_force = args.force
        if not plan_force and merged_queries and plan_outputs_present and prior_plan_empty:
            plan_force = True
            log("[DRIVER] 旧查询计划为空，丢弃后按 dynamic-queries.json 重新规划")
            for stale in plan_outputs:
                stale.unlink(missing_ok=True)

        run_stage("plan", plan_outputs, plan_force, plan_cmd_builder, ledger=ledger)
        mark("plan", begun)
        plan = json.loads((run_dir / "query-plan.json").read_text(encoding="utf-8"))
        knowledge_ids = [str(item) for item in plan.get("knowledge_ids") or []]
        query_count = len(plan.get("queries") or [])
        if knowledge_ids:
            write_sync(kb_root, run_json_path, lambda m: m.update({"knowledge_ids": knowledge_ids}))
        plan_notes = [str(note) for note in plan.get("notes") or []]
        log(f"[DRIVER] 检索计划完成：{query_count} 条查询（策略 {args.search_strategy}）"
            + (f"，知识卡 {','.join(knowledge_ids)}" if knowledge_ids else "，无知识卡匹配"))
        for note in plan_notes[:3]:
            log(f"[DRIVER] 规划提示: {note}")
        query_lines = [
            f"[{str(item.get('tier') or '-')}] {str(item.get('label') or '-')}：{str(item.get('query') or '')}"
            for item in (plan.get("queries") or [])
            if isinstance(item, dict)
        ]
        brief(
            "plan",
            f"查询计划 · {query_count} 条（检索策略 {args.search_strategy}"
            + (f"，知识卡 {','.join(knowledge_ids)}" if knowledge_ids else "")
            + "）",
            query_lines,
        )

        # An empty plan cannot feed search-arxiv: its empty-query guard exits
        # 1, which the partial-batch tolerance then misreports as "outputs
        # missing" (2026-10-15 强化学习). When seeds/external candidates can
        # still feed the registry, skip keyword retrieval and let those
        # channels carry the run; otherwise this is the sanctioned
        # retrieval-failure stop — say what is missing. The empty plan
        # artifacts are dropped so a retry re-runs planning instead of
        # skipping on stale outputs.
        seeds_strategy = args.search_strategy == "seeds"
        external_only = bool(args.external_candidates)
        citation_capable = bool(seed_ids) and args.search_strategy in ("seeds", "smart")
        if query_count == 0 and not (external_only or citation_capable):
            for stale in plan_outputs:
                stale.unlink(missing_ok=True)
            raise fail(
                "plan",
                "检索计划 0 条查询：动态查询 agent 未产出可用英文检索式，话题无 Latin 检索词"
                "（纯中文话题 arXiv 无法匹配）且无种子论文。补充 --seed-arxiv-ids、换用含英文"
                "术语的话题，或把英文检索式写入 dynamic-queries.json 后重试续跑"
                "（空计划已清空，续跑会重新规划）。",
            )

        # ---- terms selection (overlaps retrieval) -----------------------
        selector = TermsSelector(
            args.topic, args.focus,
            use_agent=not args.no_terms_agent and cli is not None,
            timeout_s=args.terms_timeout,
            cli=cli,
            fallback_terms=latin_terms,
            ledger=ledger,
        )
        selector.start()

        # ---- retrieval: arXiv single process (S2 keyword opt-in) --------
        begun = time.monotonic()
        # Open the retrieval block unconditionally (the banner used to fire
        # only under --with-s2, so recall/registry lines before the mining
        # banner piled into the plan or mining node).
        log("[DRIVER-PHASE:retrieval] 开始检索（arXiv 关键词 + 召回扩展）")
        s2_output = run_dir / "search-semantic-scholar.json"
        arxiv_output = run_dir / "search-arxiv.json"
        citation_output = run_dir / "citation-expansion.json"
        s2_detail = "skipped (S2 keyword channel off by default; --with-s2 enables it)"
        s2_process = None
        skip_arxiv = (seeds_strategy and bool(seed_ids)) or external_only or query_count == 0
        if external_only:
            log(f"[DRIVER] 外注候选模式：跳过关键词检索，registry 只收 --external-candidates "
                f"({len(args.external_candidates)} 个文件)")
        if not skip_arxiv:
            if args.with_s2:
                s2_detail = "enabled (--with-s2)"
                s2_cmd = lambda: [  # noqa: E731
                    sys.executable, str(HUB_SCRIPTS / "search.py"), "search-semantic-scholar",
                    "--query-file", str(run_dir / "query-plan.json"),
                    "--start-date", start_date,
                    "--end-date", end_date,
                    "--sleep-seconds", str(S2_SLEEP_S),
                    "--retries", "1",
                    "--retry-max-seconds", "30",
                    "--timeout", "20.0",
                    "--output", str(s2_output),
                ]
                try:
                    s2_process = subprocess.Popen(
                        s2_cmd(), cwd=str(DRIVER_CWD), text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    )
                    try:
                        s2_process.communicate(timeout=args.s2_budget)
                    except subprocess.TimeoutExpired:
                        log(f"[DRIVER-WARN] Semantic Scholar 预算用尽（{args.s2_budget:.0f}s），"
                            "已 kill；引文扩充本轮跳过（可加大 --s2-budget）")
                        s2_process.kill()
                        s2_process.communicate()
                        s2_detail = f"degraded: exceeded {args.s2_budget:.0f}s budget"
                    if s2_process.returncode:
                        s2_detail = f"degraded: exit {s2_process.returncode} (rate limited or unreachable)"
                    elif s2_output.is_file():
                        s2_detail = "ok"
                except OSError as exc:
                    s2_detail = f"degraded: {exc}"
                summary_extra["s2_detail"] = s2_detail
        if not skip_arxiv:
            arxiv_cmd = lambda: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "search-arxiv",
                "--query-file", str(run_dir / "query-plan.json"),
                "--start-date", start_date,
                "--end-date", end_date,
                "--batch-label", "r1",
                # Explicit rather than the CLI default: the per-query cap is a
                # policy knob (SEARCH_MAX_RESULTS_PER_QUERY[review_mode]) and
                # the log quotes it when reporting capped queries.
                "--max-results", str(SEARCH_MAX_RESULTS_PER_QUERY[args.review_mode]),
                # Relevance-ranked discovery (not newest-first): a wide window
                # surfaces seminal and highly-related work, not just the latest
                # submissions. Matches the live API's sortBy=relevance.
                "--sort-by", "relevance",
                *([] if not args.arxiv_snapshot else ["--metadata-snapshot", args.arxiv_snapshot]),
                "--output", str(arxiv_output),
            ]
            # arXiv 429s return exit 0 with zero results; a screening over an empty
            # registry would fail confusingly later. Retry once after a cooldown
            # when a fresh first pass comes back empty (a skipped stage with
            # pre-existing outputs is trusted as-is).
            arxiv_detail = run_stage(
                "retrieval-arxiv", [arxiv_output], args.force, arxiv_cmd,
                # exit 1 = partial batch (some queries failed; hits saved) —
                # proceed with the hole visible, matching the S2 degrade path.
                soft_exit_codes=frozenset({1}),
                ledger=ledger,
            )
            if arxiv_detail.startswith("ran") and arxiv_output.is_file():
                try:
                    # paper_count lives at the top level of both the live and
                    # snapshot outputs (per-query entries only carry
                    # result_count); counting per-query result lists here read
                    # 0 for every successful retrieval and forced a bogus retry.
                    hits = int(json.loads(arxiv_output.read_text(encoding="utf-8")).get("paper_count") or 0)
                except (json.JSONDecodeError, OSError):
                    hits = 0
                if hits == 0:
                    log("[DRIVER-WARN] arXiv returned 0 results (rate limited?) — cooling down 120s and retrying once")
                    time.sleep(120)
                    arxiv_output.unlink(missing_ok=True)
                    arxiv_detail = run_stage(
                        "retrieval-arxiv", [arxiv_output], True, arxiv_cmd,
                        soft_exit_codes=frozenset({1}),
                        ledger=ledger,
                    )
            if arxiv_output.is_file():
                try:
                    arxiv_papers = json.loads(arxiv_output.read_text(encoding="utf-8")).get("paper_count") or 0
                    log(f"[DRIVER] arXiv 关键词检索命中 {arxiv_papers} 篇")
                except (json.JSONDecodeError, OSError):
                    pass
        else:
            if external_only:
                arxiv_detail = "skipped (external candidates replace keyword retrieval)"
            elif query_count == 0:
                arxiv_detail = "skipped (empty query plan; citation/seed channel carries retrieval)"
            else:
                arxiv_detail = "skipped (seeds strategy: citation-graph expansion replaces keyword retrieval)"
            log(stage_line("retrieval-arxiv", arxiv_detail))
        summary_extra["s2_detail"] = s2_detail
        mark("retrieval", begun)

        # ---- citation expansion (seed-driven, smart w/ seeds or seeds) ---
        begun = time.monotonic()
        citation_detail = "skipped (no seeds)"
        if seed_ids and (args.search_strategy in ("seeds", "smart")):
            citation_cmd = lambda: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "expand-via-citations",
                *[item for seed in seed_ids for item in ("--seed-id", seed)],
                "--direction", "both",
                "--batch-label", "citation-seeds",
                "--max-total-candidates", "200",
                "--start-date", start_date,
                "--end-date", end_date,
                "--sleep-seconds", str(S2_SLEEP_S),
                "--graph-output", str(run_dir / "citation-graph.json"),
                "--output", str(citation_output),
            ]
            try:
                citation_result = run_command(
                    citation_cmd(), timeout=CITATION_EXPANSION_TIMEOUT_S)
            except subprocess.TimeoutExpired:
                log(f"[DRIVER-WARN] 引文扩充超时（{CITATION_EXPANSION_TIMEOUT_S:.0f}s），"
                    "本轮跳过（关键词检索候选照常继续）")
                citation_result = subprocess.CompletedProcess(
                    citation_cmd(), returncode=1, stdout="",
                    stderr=f"timeout after {CITATION_EXPANSION_TIMEOUT_S:.0f}s"
                )
            if citation_result.returncode:
                # best-effort: keyword retrieval candidates still proceed
                citation_detail = f"degraded: exit {citation_result.returncode} {(citation_result.stderr or '')[-200:]}"
                log(stage_line("citation-expansion", citation_detail))
            else:
                citation_detail = (citation_result.stderr or "").strip().splitlines()[-1] if (citation_result.stderr or "").strip() else "ok"
                log(stage_line("citation-expansion", citation_detail))
        summary_extra["citation_expansion"] = citation_detail
        mark("citation", begun)

        # ---- recall tail rounds (saturation measurement) ----------------
        # Discovery rounds (plan/citation) can never show diminishing returns
        # — each is 100% new by construction. The saturation judge needs a
        # TAIL of low-novelty rounds to measure. Recall rounds re-query
        # authors/titles already in hand, so they re-find mostly known papers
        # (main's author-recall / title-recall rounds). Cheap against the
        # snapshot; skippable when the pool is too thin to recall from.
        begun = time.monotonic()
        # The scope clause needs English terms; the selector thread has been
        # running since before retrieval and is done by now. A pure-Chinese
        # topic must not silently degrade to unscoped au: harvest.
        recall_terms, _recall_source = selector.join()
        if not any(term.isascii() for term in recall_terms):
            recall_terms = latin_terms or mechanical_terms(args.topic, args.focus)
        recall_outputs: list[Path] = []
        discovery_papers: list[dict] = []
        for source in (arxiv_output, citation_output):
            if not source.is_file():
                continue
            try:
                payload = json.loads(source.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for paper in payload.get("papers") or payload.get("candidates") or []:
                if isinstance(paper, dict):
                    discovery_papers.append(paper)
        recall_specs = (
            (
                "recall-author",
                lambda papers: recall_author_queries(papers, terms=recall_terms),
                "search-recall-author.json",
            ),
            ("recall-title", recall_title_queries, "search-recall-title.json"),
            (
                "known-works",
                lambda papers: known_works_queries(papers, seeds=seed_ids),
                "search-known-works.json",
            ),
        )
        for batch_label, build_queries, filename in recall_specs:
            queries = build_queries(discovery_papers)
            if len(queries) < 3:
                log(f"[DRIVER] {batch_label} 轮跳过（可召回条目不足 3 条）")
                continue
            round_output = run_dir / filename
            round_plan = run_dir / f"query-{batch_label}.json"
            write_round_queries(round_plan, queries, batch_label=batch_label)
            recall_cmd = lambda plan=round_plan, out=round_output, label=batch_label: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "search-arxiv",
                "--query-file", str(plan),
                "--start-date", start_date,
                "--end-date", end_date,
                "--batch-label", label,
                *([] if not args.arxiv_snapshot else ["--metadata-snapshot", args.arxiv_snapshot]),
                "--output", str(out),
            ]
            detail = run_stage(
                batch_label, [round_output], args.force, recall_cmd,
                soft_exit_codes=frozenset({1}),
                ledger=ledger,
            )
            if round_output.is_file():
                recall_outputs.append(round_output)
                try:
                    hits = int(json.loads(round_output.read_text(encoding="utf-8")).get("paper_count") or 0)
                except (OSError, json.JSONDecodeError, ValueError):
                    hits = 0
                log(f"[DRIVER] {batch_label} 轮：{len(queries)} 条召回查询，命中 {hits} 篇（{detail}）")
        summary_extra["recall_rounds"] = [
            {"batch": label, "queries": len(build_queries(discovery_papers)), "file": name}
            for label, build_queries, name in recall_specs
            if (run_dir / name).is_file()
        ]
        mark("recall", begun)

        # ---- registry (retrieval consolidation) --------------------------
        # The registry merge is the tail of retrieval: it fuses the search
        # channels' hits into one deduped candidate set. Keep it BEFORE the
        # mining banner so the 检索命中 brief and its skip lines land under
        # arXiv 检索, not 全文挖掘 (2026-10-16).
        begun = time.monotonic()
        registry_output = run_dir / "candidate-registry.json"
        # Preserve selection/extraction statuses across the rebuild — without
        # --screening-file every candidate resets to "discovered" and the
        # full-text floor reads 0 after a recall-triggered registry refresh
        # (2026-10-10).
        screening_updates_path = run_dir / "screening-updates.json"
        def registry_cmd():
            command = [
                sys.executable, str(HUB_SCRIPTS / "search.py"), "build-candidate-registry",
                "--output", str(registry_output),
            ]
            if not skip_arxiv and arxiv_output.is_file():
                command += ["--search-result", str(arxiv_output)]
            if s2_output.is_file() and s2_process is not None and s2_process.returncode == 0:
                command += ["--semantic-scholar-result", str(s2_output)]
            if citation_output.is_file():
                command += ["--citation-result", str(citation_output)]
            # Recall tail LAST so the saturation judge's tail window lands on
            # the low-novelty rounds (batch order = new_unique_rate order).
            for path in (*recall_outputs, *args.external_candidates):
                kind = "--search-result" if path in recall_outputs else "--curated-list-result"
                command += [kind, str(path)]
            updates = build_screening_updates(
                run_dir / "screening.json", run_dir / "extraction-summary.json")
            if updates is not None:
                screening_updates_path.write_text(
                    json.dumps({"version": 1, "candidates": updates}, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8",
                )
                command += ["--screening-file", str(screening_updates_path)]
            return command
        registry_inputs = [p for p in (arxiv_output, citation_output, *recall_outputs) if p]
        run_stage(
            "registry", [registry_output],
            args.force or inputs_newer_than(registry_output, registry_inputs),
            registry_cmd,
            ledger=ledger,
        )
        mark("registry", begun)
        try:
            registry_size = len(json.loads(registry_output.read_text(encoding="utf-8")).get("candidates") or [])
            log(f"[DRIVER] 候选注册表合并完成：{registry_size} 篇去重候选")
        except (json.JSONDecodeError, OSError):
            registry_size = 0
        retrieval_lines = [
            f"arXiv 关键词：{arxiv_detail if not skip_arxiv else '未跑（seeds/外部候选模式）'}",
            f"Semantic Scholar：{s2_detail or '未启用'}",
            f"引文扩展：{citation_detail}",
        ]
        if not skip_arxiv and arxiv_output.is_file():
            # Surface the sort contract, the cap, and the year spread in the
            # phase brief: "为什么全是 2026" must be answerable from the
            # workflow log. Retrieval is relevance-ranked; the year histogram
            # shows what the relevance cut actually surfaced.
            try:
                batch = json.loads(arxiv_output.read_text(encoding="utf-8"))
                sort_by = str(batch.get("sort_by") or "submittedDate")
                capped = sum(1 for q in batch.get("queries") or [] if q.get("capped"))
                year_counts: dict[str, int] = {}
                for paper in batch.get("papers") or []:
                    year = str(paper.get("published") or "")[:4] or "unknown"
                    year_counts[year] = year_counts.get(year, 0) + 1
                years_desc = sorted(year_counts.items(), key=lambda kv: kv[0], reverse=True)
                year_line = "年份分布：" + "，".join(f"{y}:{n}" for y, n in years_desc[:6])
                if len(years_desc) > 6:
                    year_line += "，…"
                retrieval_lines.append(
                    f"排序：{sort_by}，per-query cap "
                    f"{SEARCH_MAX_RESULTS_PER_QUERY[args.review_mode]}"
                    + (f"（{capped} 条查询触顶）" if capped else "")
                )
                retrieval_lines.append(year_line)
            except (json.JSONDecodeError, OSError, TypeError):
                pass
        if args.external_candidates:
            retrieval_lines.append(f"外部候选：{len(args.external_candidates)} 个清单")
        brief("retrieval", f"检索命中 · 注册 {registry_size} 篇去重候选", retrieval_lines)

        # ---- screening + coverage (joins the terms thread) --------------
        begun = time.monotonic()
        log("[DRIVER-PHASE:mining] 筛选、全文挖掘与深读")
        terms, terms_source = selector.join()
        # Chinese-only screening terms match nothing against English titles —
        # the second half of the 2026-09-11 failure chain. When the fallback
        # terms carry no Latin token, mine English terms from the run's own
        # dynamic queries (the same vocabulary that just retrieved candidates).
        if not any(term.isascii() for term in terms) and dynamic_payload["queries"]:
            mined: list[str] = []
            for item in dynamic_payload["queries"]:
                for token in re.findall(r'"([a-z0-9 \-]+)"', str(item.get("query", "")).lower()):
                    token = token.strip()
                    if 2 <= len(token) <= 40 and token not in mined:
                        mined.append(token)
                if len(mined) >= 12:
                    break
            if mined:
                terms = mined
                terms_source = "dynamic-queries"
        summary_extra["terms"] = terms
        summary_extra["terms_source"] = terms_source
        # No screening cap. Selection decides what is relevant; extraction
        # recovers what selection queued; deep reading (DEEP_READ_LIMITS, with
        # the 候补 fill) is the funnel's only truncation (2026-10-20: the old
        # SCREEN_LIMITS=120 cut stranded 232 of 352 relevant papers).
        screening_output = run_dir / "screening.json"
        screening_ids = run_dir / "screening-ids.txt"
        if args.selection_strategy == "keywords":
            # Legacy term-matching screen: only this strategy consumes the terms
            # thread's output for triage (other strategies still generate terms
            # for the abstract evidence and the reading packets).
            # keywords is the legacy term-match screen (no agent); the timeout
            # knob belongs to select-candidates' smart agent below.
            screening_cmd = lambda: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "screen-candidates",
                "--candidate-registry", str(registry_output),
                "--terms", ",".join(terms),
                "--output-screening", str(screening_output),
                "--output-ids", str(screening_ids),
                "--output-markdown", str(run_dir / "screening.md"),
            ]
        else:
            screening_cmd = lambda: [  # noqa: E731
                sys.executable, str(HUB_SCRIPTS / "search.py"), "select-candidates",
                "--registry", str(registry_output),
                "--strategy", args.selection_strategy,
                "--topic", args.topic,
                "--focus", args.focus or "",
                "--terms", ",".join(terms),
                "--complete-timeout", str(args.selection_timeout),
                *(
                    ["--complete-model", args.selection_model]
                    if args.selection_strategy == "smart"
                    and getattr(args, "selection_model", None) else []
                ),
                *(
                    ["--selection-threshold", str(args.selection_threshold)]
                    if args.selection_strategy == "smart-jev"
                    and getattr(args, "selection_threshold", None) is not None else []
                ),
                "--output-screening", str(screening_output),
                "--output-ids", str(screening_ids),
                "--output-markdown", str(run_dir / "screening.md"),
            ]
        run_stage(
            "screening", [screening_output, screening_ids], args.force, screening_cmd,
            stream=True, on_line=selection_line,
            ledger=ledger,
        )
        summary_extra["selection_strategy"] = args.selection_strategy
        try:
            selection_detail = str(
                (json.loads(screening_output.read_text(encoding="utf-8")).get("selection_rule") or {}).get("detail") or ""
            )
        except (OSError, json.JSONDecodeError):
            selection_detail = ""
        summary_extra["selection_detail"] = selection_detail
        write_sync(kb_root, run_json_path, lambda m: m.update({
            "selection_strategy": args.selection_strategy,
            "selection_model": (
                getattr(args, "selection_model", None)
                or ("jev" if args.selection_strategy == "smart-jev" else "")
            ),
        }))
        screened_ids = [
            line.strip()
            for line in screening_ids.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        summary_extra["screened_count"] = len(screened_ids)
        log(f"[DRIVER] 精读候选 {len(screened_ids)} 篇（screening.md 已写入运行目录）")
        # Selection brief: the deep-read queue with per-paper reasons — the
        # decision surface a reviewer checks ("why these papers?") and the
        # first thing a debugger replays when the queue looks wrong.
        selection_lines: list[str] = []
        try:
            screening_rows = (
                json.loads(screening_output.read_text(encoding="utf-8")).get("candidates") or []
            )
            titles_by_id = {}
            try:
                for record in json.loads(registry_output.read_text(encoding="utf-8")).get("candidates") or []:
                    if isinstance(record, dict) and record.get("arxiv_id"):
                        titles_by_id[str(record["arxiv_id"])] = str(record.get("title") or "")
            except (json.JSONDecodeError, OSError):
                pass
            for row in screening_rows:
                if not isinstance(row, dict):
                    continue
                arxiv_id = str(row.get("arxiv_id") or "")
                title = " ".join((str(row.get("title") or titles_by_id.get(arxiv_id, ""))).split())
                reason = " ".join(str(row.get("selection_reason") or "").split())
                selection_lines.append(
                    f"{arxiv_id}  {title}" + (f"  — {reason}" if reason else "")
                )
        except (json.JSONDecodeError, OSError):
            pass
        if not selection_lines:
            selection_lines = list(screened_ids)
        brief(
            "selection",
            f"精读候选 · {len(screened_ids)} 篇（选文策略 {args.selection_strategy}）",
            selection_lines,
        )
        coverage_output = run_dir / "coverage-report.json"
        coverage_cmd = lambda: [  # noqa: E731
            sys.executable, str(HUB_SCRIPTS / "search.py"), "assess-review-coverage",
            "--query-plan", str(run_dir / "query-plan.json"),
            "--candidate-registry", str(registry_output),
            "--output", str(coverage_output),
        ]
        run_stage(
            "coverage", [coverage_output],
            args.force or inputs_newer_than(coverage_output, [registry_output]),
            coverage_cmd,
            ledger=ledger,
        )
        mark("screening", begun)
        coverage = json.loads(coverage_output.read_text(encoding="utf-8"))
        # Cheap (set ops) — say NOW which floors are already at risk, not at
        # finalize after the deep-read bill is paid.
        log_gates(coverage_output, "检索后")

        # ---- abstract-tier evidence (positioning-only, before extraction) --
        begun = time.monotonic()
        abstract_evidence_stage(
            kb_root, run_dir, run_json_path, knowledge_ids, args, summary_extra,
            screening_ids=screening_ids,
        )
        mark("abstract-evidence", begun)

        # ---- full-text extraction --------------------------------------
        begun = time.monotonic()
        extraction_summary = run_dir / "extraction-summary.json"
        log(f"[DRIVER] 开始全文抽取（HTML→Markdown，阶段上限 {EXTRACTION_STAGE_TIMEOUT_S/60:.0f} 分钟，候选 {len(screened_ids)} 篇）…")
        extraction_cmd = lambda: [  # noqa: E731
            sys.executable, str(HUB_SCRIPTS / "fetch.py"), "extract-content-queue",
            "--paper-timeout", str(args.extraction_timeout),
            "--paper-id-file", str(screening_ids),
            "--terms", ",".join(terms),
            "--output-dir", str(run_dir / "extractions"),
            # Shared KB cache: a paper fetched by an earlier run (or a
            # quick-read) is reused instead of re-downloading from arXiv, and
            # the cache survives /tmp cleanup and is visible to sibling
            # machines on the same KB mount.
            "--html-cache-dir", str(cache_dir / "html"),
            "--pdf-cache-dir", str(cache_dir / "pdfs"),
            "--workers", str(max(1, min(args.workers, 4))),
            "--ocr-mode", "never",
            "--include-full-text",
            "--summary-output", str(extraction_summary),
        ]
        # HELD papers are retryable, not settled: a rerun re-runs the queue so
        # transient fetch failures (rate limiting) get supplemented. The queue
        # itself caches evidence-eligible papers, so only HELD ones re-fetch.
        extraction_force = args.force
        if not extraction_force and extraction_summary.is_file():
            try:
                extraction_force = bool(
                    json.loads(extraction_summary.read_text(encoding="utf-8")).get("held_count"))
            except (OSError, ValueError):
                extraction_force = False
        run_stage(
            "extraction", [extraction_summary], extraction_force, extraction_cmd,
            timeout=EXTRACTION_STAGE_TIMEOUT_S,
            stream=True, on_line=extraction_queue_line,
            ledger=ledger,
        )
        mark("extraction", begun)
        try:
            extraction_payload = json.loads(extraction_summary.read_text(encoding="utf-8"))
            eligible = int(extraction_payload.get("evidence_eligible_count") or 0)
            held = int(extraction_payload.get("held_count") or 0)
            held_ids = [
                str(item.get("paper_id") or "")
                for item in extraction_payload.get("results") or []
                if isinstance(item, dict) and not item.get("evidence_eligible")
            ]
            brief(
                "extraction",
                f"全文恢复 · {eligible} 篇可用 / {held} 篇 HELD（共 {eligible + held} 篇）",
                ([f"HELD  {paper_id}" for paper_id in held_ids if paper_id] or ["无 HELD 篇目"]),
            )
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            pass
        pool_seed(summary_extra, screening_ids, run_dir, args)
        # Refresh coverage in-process so full_text_floor reflects the extraction
        # result — assess() is set operations only (microseconds), no subprocess,
        # and HELD papers are still retryable at this point (2026-10-10).
        refresh_coverage_inplace(run_dir, coverage_output)
        log_gates(coverage_output, "抽取后")

        # ---- reading packets --------------------------------------------
        begun = time.monotonic()
        packets_dir = run_dir / "reading-packets"
        packets_dir.mkdir(parents=True, exist_ok=True)
        packet_count = 0
        extraction_files = sorted((run_dir / "extractions").glob("*.json"))
        if extraction_files:
            log(f"[DRIVER] 生成阅读包（{len(extraction_files)} 篇抽取结果）…")
        for extraction_path in extraction_files:
            paper_id = extraction_path.stem
            packet_output = packets_dir / f"{paper_id}.md"
            if not args.force and packet_output.is_file() and packet_output.stat().st_size > 0:
                packet_count += 1
                log(f"[DRIVER-PROGRESS:packets:{packet_count}/{len(extraction_files)}]")
                continue
            result = run_command([
                sys.executable, str(PACKET_SCRIPT),
                "build-reading-packet",
                "--extraction", str(extraction_path),
                "--review-question", args.topic,
                "--topic-id", *(knowledge_ids or ["EA-DATA"]),
                "--review-mode", args.review_mode,
                "--output", str(packet_output),
            ])
            if result.returncode:
                # One unrecoverable paper must not sink the queue — but the
                # reason must be visible (2026-10-16: 16 bare "exit 2" lines
                # with no way to tell low-quality extraction from a crash).
                reason = (result.stderr or result.stdout or "").strip().splitlines()
                log(f"[DRIVER-WARN] packet {paper_id}: exit {result.returncode}"
                    f"：{reason[-1] if reason else '无输出'}")
            else:
                packet_count += 1
            log(f"[DRIVER-PROGRESS:packets:{packet_count}/{len(extraction_files)}]")
        mark("packets", begun)
        log(stage_line("packets", f"{packet_count}/{len(extraction_files)} packets"))

        # ---- deep read (skeleton agents + local assembly) ---------------
        if not args.skip_deep_read:
            begun = time.monotonic()
            deep_read(run_dir, run_json_path, screening_ids, args, summary_extra, ledger=ledger)
            mark("deep-read", begun)
            begun = time.monotonic()
            project_evidence(kb_root, run_dir, run_json_path, summary_extra)
            mark("project", begun)
            # ---- coverage finalize: statuses + evidence-aware reassessment
            begun = time.monotonic()
            summary_extra["coverage_final"] = finalize_coverage(run_dir, registry_cmd(), coverage_output)
            mark("coverage-final", begun)
            log_gates(coverage_output, "深读后")
            log(stage_line("coverage-final", summary_extra["coverage_final"]))

        # ---- review packet (mechanical refresh over the final evidence set)
        begun = time.monotonic()
        review_packet_stage(run_dir, args, summary_extra)
        mark("review-packet", begun)

        # ---- funnel (publishable retrieval→evidence accounting) ----------
        # Layers come from disk only, so a --skip-deep-read re-entry that finds
        # earlier notes still reports them; `skipped` records what THIS
        # invocation passed over without changing the numbers.
        begun = time.monotonic()
        skipped_stages = ["deep-read"] if args.skip_deep_read else []
        if summary_extra.get("abstract_basis") == "skipped":
            skipped_stages.append("abstract-evidence")
        funnel_payload = build_funnel(
            run_dir,
            run=run_dir.name,
            topic=args.topic,
            review_mode=args.review_mode,
            summary=summary_extra,
            skipped=skipped_stages,
        )
        write_funnel(funnel_payload, run_dir)
        if funnel_payload.get("truncated"):
            log(f"[DRIVER-WARN] funnel.json 层列表超过 {FUNNEL_LAYER_PAPER_CAP} 篇，已截断（truncated: true）")
        leaked = (funnel_payload.get("detail") or {}).get("abstract_leaked") or 0
        if leaked:
            log(f"[DRIVER-WARN] 摘要级含 {leaked} 篇选文外论文（旧产物），可用 --force 重跑 abstract-evidence 收口")
        mark("funnel", begun)

        # ---- summary ----------------------------------------------------
        registry = json.loads(registry_output.read_text(encoding="utf-8"))
        # finalize_coverage (above) rewrote coverage-report.json with the
        # post-deep-read statuses; the `coverage` object in hand is the
        # pre-extraction snapshot and its observed counts are stale (2026-10-12:
        # summary reported full_text_recovered_count 0 while the report on disk
        # said 60 and every floor passed). Re-read the report — summary must
        # describe the same numbers the gates judge on.
        if coverage_output.is_file():
            try:
                coverage = json.loads(coverage_output.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                pass
        observed = coverage.get("observed") or {}
        checks = ((coverage.get("stop_assessment") or {}).get("checks") or {})
        # At driver time only discovery-side floors can pass (full text and
        # accepted papers come later, from deep reading) — report those two
        # honestly instead of expecting ready_to_stop.
        summary = {
            "version": 1,
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "topic": args.topic,
            "review_mode": args.review_mode,
            "time_range": args.time_range,
            "knowledge_ids": knowledge_ids,
            "query_count": query_count,
            "stage_seconds": stage_seconds,
            "candidate_count": int(registry.get("candidate_count") or 0),
            "screened_count": len(screened_ids),
            "full_text_recovered_count": int(observed.get("full_text_recovered_count") or 0),
            "coverage_dimensions_passed": bool(coverage.get("coverage_dimensions")),
            "candidate_floor_passed": bool(checks.get("candidate_floor")),
            "saturation_passed": bool(checks.get("saturation")),
            "packet_count": packet_count,
            # Artifacts a reviewer reads first: the plan, the candidate list,
            # and the screened (deep-read) list.
            "artifacts": {
                "search_plan": "query-plan.md",
                "candidate_registry": "candidate-registry.json",
                "screened_list": "screening.md",
                "citation_graph": "citation-graph.json" if citation_output.is_file() else None,
                "funnel": FUNNEL_FILENAME,
            },
            **summary_extra,
        }
        (run_dir / "pipeline-summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        log(stage_line("summary", f"total {time.monotonic() - started:.0f}s"))
        log(
            f"[DRIVER] 检索计划 query-plan.md · 候选 {summary['candidate_count']} 篇 · "
            f"精读候选 {len(screened_ids)} 篇 · 详情见运行目录 pipeline-summary.json"
        )
        deep_stats = summary_extra.get("deep_read") or {}
        brief(
            "summary",
            f"机械阶段完成 · 候选 {summary['candidate_count']} → 精读 {len(screened_ids)} → 证据 {summary_extra.get('evidence_events', 0)}",
            [
                f"查询 {query_count} 条（{args.search_strategy}）",
                f"全文恢复 {summary['full_text_recovered_count']} 篇 · 阅读包 {packet_count} 篇",
                f"深读 {deep_stats.get('total', 0)} 篇：pass {deep_stats.get('pass', 0)} / "
                f"needs-review {deep_stats.get('needs_review', 0)} / failed {deep_stats.get('failed', 0)}",
                f"证据事件 {summary_extra.get('evidence_events', 0)} 条（全文级）",
                f"覆盖维度 {'过' if summary['coverage_dimensions_passed'] else '未过'} · "
                f"候选地板 {'过' if summary['candidate_floor_passed'] else '未过'} · "
                f"饱和 {'过' if summary['saturation_passed'] else '未过'}",
                "产物：query-plan.md / candidate-registry.json / screening.md / "
                "funnel.json / pipeline-summary.json",
            ],
        )
        return 0
    except DriverError as exc:
        if ledger is not None:
            ledger.error(f"pipeline failed: {exc}", stage="pipeline")
        print(f"pipeline failed: {exc}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        if ledger is not None:
            ledger.error(f"pipeline failed: {exc}", stage="pipeline")
        print(f"pipeline failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if ledger is not None:
            ledger.metric(
                "pipeline", time.monotonic() - started,
                stages=len(stage_seconds),
                stage_seconds=stage_seconds,
            )
            ledger.close()
        if inherited_ledger is None:
            os.environ.pop(AGENT_SESSION_LEDGER_ENV, None)
        else:
            os.environ[AGENT_SESSION_LEDGER_ENV] = inherited_ledger

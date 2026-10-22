#!/usr/bin/env python3
"""Recover arXiv full text for an ID queue with bounded concurrency and per-paper checkpoints.

Library API: the module-level helpers (``load_ids``, ``extraction_args``,
``extract_one``, ``run_queue``) take explicit parameters; the CLI surface owns
argument parsing and lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/extract_content_queue.py``.
"""

from __future__ import annotations

import concurrent.futures
import json
import re
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from embodied_learning.fetch import chain as extract_arxiv_content
from embodied_learning.utils.layout import find_roots
from embodied_learning.config import CHANNEL_DOWN_LIMIT, EXTRACTION_PAPER_TIMEOUT_S

_REPO_ROOT = find_roots()[0] or Path(__file__).resolve().parents[2]
# Per-paper subprocess target: prefer the repo thin entry (dev/CI), fall back to
# running the installed module when skills/ is absent (wheel installs).
_EXTRACT_ENTRY = _REPO_ROOT / "skills" / "embodied-ai-literature-hub" / "scripts" / "fetch.py"
_EXTRACT_CMD = (
    [sys.executable, str(_EXTRACT_ENTRY), "extract-content"] if _EXTRACT_ENTRY.is_file()
    else [sys.executable, "-m", "hub_scripts.fetch", "extract-content"]
)

# Circuit breaker: when the network is dead (arxiv.org connection timeouts)
# every paper waits out its full paper_timeout — 79 papers x 300s on 2026-10-12
# burned the whole extraction window for nothing. A run of consecutive
# connection-level failures means the channel is down, not the papers; stop
# spending per-paper budgets on it. Failures that are clearly per-paper
# (extractor exit with a message, a short HTTP error) do NOT count.


class _ChannelCircuit:
    """Thread-safe consecutive-connection-failure counter. Once tripped,
    extract_one short-circuits and marks the paper CHANNEL_DOWN without
    spawning a subprocess."""

    def __init__(self, limit: int = CHANNEL_DOWN_LIMIT) -> None:
        self.limit = limit
        self._streak = 0
        self._tripped = False
        self._lock = threading.Lock()

    @property
    def tripped(self) -> bool:
        return self._tripped

    def record(self, connection_failure: bool) -> None:
        with self._lock:
            if self._tripped:
                return
            self._streak = self._streak + 1 if connection_failure else 0
            if self._streak >= self.limit:
                self._tripped = True


def _is_connection_failure(error: str) -> bool:
    """Connection-level death (the channel is unreachable) vs a per-paper fail."""
    text = error.lower()
    return any(
        token in text
        for token in (
            "timeout",  # hard timeout after Ns / socket timeout
            "connection",
            "timed out",
            "temporary failure in name resolution",
            "could not resolve",
            "no route to host",
            "network is unreachable",
            "connection reset",
            "broken pipe",
            "ssl",
        )
    )


_HELD_REASON_MAX = 120


def held_reason(
    data: dict[str, Any],
    *,
    manifest_state: str | None = None,
    manifest_status: int | None = None,
    paper_timeout: float | None = None,
) -> str:
    """One-line compact reason a paper came out HELD (`` · ``-joined, ≤120 chars).

    Priority: channel-down → hard timeout → queue-synthesized error →
    unavailable (HTML manifest state + tex/pdf fallback attempts) →
    low quality → raw error tail.
    """
    error = str(data.get("error") or "").strip()
    quality = data.get("quality") if isinstance(data.get("quality"), dict) else {}
    has_quality = bool(quality)

    def short(text: str, limit: int = 60) -> str:
        text = " ".join(text.split())
        return text[:limit]

    if error.startswith("channel down"):
        return "channel-down"
    if error.startswith("hard timeout after"):
        # "hard timeout after 600s: tail" → "timeout 600s"
        match = re.search(r"hard timeout after\s+([0-9]+)s", error)
        if match:
            return f"timeout {match.group(1)}s"
        return f"timeout {int(paper_timeout)}s" if paper_timeout else "timeout"
    if error and not has_quality:
        return f"error {short(error)}"
    if not data.get("available"):
        parts: list[str] = []
        if manifest_state == "unavailable":
            status = manifest_status if manifest_status is not None else 404
            parts.append(f"HTML {status}" if status in {404, 410} else "HTML unavailable")
        elif manifest_state == "failed":
            parts.append("HTML fetch failed")
        elif manifest_state in {"downloaded", "cached"}:
            parts.append("HTML cache missing")
        for attempt in data.get("attempts") or []:
            if not isinstance(attempt, dict):
                continue
            method = str(attempt.get("method") or "")
            if method.startswith("html") or not method:
                continue
            if attempt.get("available"):
                continue
            # Tier vocabulary: arxiv2md / tex-pandoc ride the tex tier;
            # pdf-text / pdf-ocr ride the pdf tier.
            if method.startswith("tex") or method.startswith("arxiv2md"):
                parts.append("tex unavailable")
            elif method.startswith("pdf"):
                err = short(str(attempt.get("error") or ""), 40)
                parts.append(f"pdf: {err}" if err else "pdf unavailable")
            else:
                parts.append(f"{method} unavailable")
        if not parts:
            parts.append("unavailable")
        if error:
            parts.append(short(error, 40))
        reason = " · ".join(parts)
    elif quality.get("grade") not in {"high", "medium"}:
        reason = f"quality {quality.get('grade', 'low')} text={quality.get('text_chars', 0)}"
        if quality.get("structure") and quality.get("structure") != "latexml":
            reason += f" structure={quality['structure']}"
    else:
        reason = f"error {short(error)}" if error else "held"
    return reason[:_HELD_REASON_MAX]


def _write_channel_down(paper_id: str, target: Path, error: str) -> dict[str, Any]:
    data = {
        "paper_id": paper_id,
        "available": False,
        "evidence_eligible": False,
        "error": error,
    }
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "paper_id": paper_id,
        "state": "channel-down",
        "evidence_eligible": False,
        "path": str(target),
        "error": error,
        "held_reason": "channel-down",
    }


class QueueOptions:
    """CLI-option state for one :func:`run_queue` recovery run.

    Explicit constructor parameters (the CLI entry translates argparse into
    these); attribute names mirror the old flag names.
    """

    def __init__(
        self,
        *,
        paper_id_file: str,
        terms: str,
        output_dir: str,
        html_cache_dir: str | None = None,
        pdf_cache_dir: str | None = None,
        workers: int = 2,
        timeout: float = 30.0,
        paper_timeout: float = EXTRACTION_PAPER_TIMEOUT_S,
        top_sections: int = 3,
        ocr_mode: str = "never",
        ocr_language: str = "eng",
        include_full_text: bool = False,
        force: bool = False,
        preferred_source: str = "html",
        tex_transport: str = "arxiv2md",
        curl_timeout: float = 120.0,
        tex_cache_dir: str | None = None,
        summary_output: str | None = None,
        download_manifest: str | None = None,
    ) -> None:
        self.paper_id_file = paper_id_file
        self.terms = terms
        self.output_dir = output_dir
        self.html_cache_dir = html_cache_dir
        self.pdf_cache_dir = pdf_cache_dir
        self.workers = workers
        self.timeout = timeout
        self.paper_timeout = paper_timeout
        self.top_sections = top_sections
        self.ocr_mode = ocr_mode
        self.ocr_language = ocr_language
        self.include_full_text = include_full_text
        self.force = force
        self.preferred_source = preferred_source
        self.tex_transport = tex_transport
        self.curl_timeout = curl_timeout
        self.tex_cache_dir = tex_cache_dir
        self.summary_output = summary_output
        self.download_manifest = download_manifest


def load_ids(path: Path) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.split("#", 1)[0].strip().rsplit("/", 1)[-1].removesuffix(".pdf")
        value = re.sub(r"v\d+$", "", value)
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def extraction_args(paper_id: str, options: QueueOptions) -> extract_arxiv_content.ContentOptions:
    """Per-paper extraction options derived from the queue-level options."""
    return extract_arxiv_content.ContentOptions(
        paper_id=paper_id,
        terms=options.terms,
        html_url=None,
        pdf_url=None,
        pdf_file=None,
        # Explicit queue options win; the /tmp defaults only apply when the
        # caller passed none (lightweight library calls).
        html_cache_dir=options.html_cache_dir
        or extract_arxiv_content.extract_arxiv_html.DEFAULT_CACHE_DIR,
        pdf_cache_dir=options.pdf_cache_dir
        or extract_arxiv_content.extract_arxiv_pdf.DEFAULT_CACHE_DIR,
        timeout=options.timeout,
        top_sections=options.top_sections,
        max_pages=0,
        ocr_mode=options.ocr_mode,
        ocr_language=options.ocr_language,
        ocr_dpi=220,
        min_chars_per_page=180,
        minimum_html_chars=1000,
        force_pdf=False,
        include_selected_text=True,
        include_full_text=options.include_full_text,
    )


def extract_one(
    paper_id: str,
    options: QueueOptions,
    output_dir: Path,
    circuit: _ChannelCircuit | None = None,
    html_cache_only: bool = False,
    manifest_state: str | None = None,
    manifest_status: int | None = None,
) -> dict[str, Any]:
    target = output_dir / f"{paper_id}.json"
    if target.is_file() and not options.force:
        data = json.loads(target.read_text(encoding="utf-8"))
        if data.get("evidence_eligible"):
            return {"paper_id": paper_id, "state": "cached", "evidence_eligible": True, "path": str(target), "held_reason": ""}
        # A previously HELD paper is retryable, not cached: the fetch may have
        # failed transiently (rate limit) and a driver rerun should supplement
        # it instead of skipping it forever. Falls through to a fresh extract;
        # a paper that is genuinely unrecoverable just re-checkpoints as HELD.
    # Download phase already declared the channel down for this paper — do not
    # spawn a subprocess that will only re-discover the same dead network.
    if manifest_state == "channel-down":
        return _write_channel_down(
            paper_id,
            target,
            "channel down: skipped after consecutive connection failures",
        )
    # Channel already declared down by an earlier run of consecutive
    # connection failures — do not spend this paper's full budget on a
    # network that is not answering. The driver rerun retries these.
    if circuit is not None and circuit.tripped:
        return _write_channel_down(
            paper_id,
            target,
            "channel down: skipped after consecutive connection failures",
        )
    temporary = target.with_suffix(".json.tmp")
    command = [
        *_EXTRACT_CMD,
        "--paper-id", paper_id,
        "--terms", options.terms,
        "--timeout", str(options.timeout),
        "--top-sections", str(options.top_sections),
        "--ocr-mode", options.ocr_mode,
        "--ocr-language", options.ocr_language,
        "--include-selected-text",
        "--output", str(temporary),
    ]
    if options.html_cache_dir:
        command.extend(["--html-cache-dir", options.html_cache_dir])
    if options.pdf_cache_dir:
        command.extend(["--pdf-cache-dir", options.pdf_cache_dir])
    if options.tex_cache_dir:
        command.extend(["--tex-cache-dir", options.tex_cache_dir])
    command.extend(["--preferred-source", options.preferred_source])
    command.extend(["--tex-transport", options.tex_transport])
    command.extend(["--curl-timeout", str(options.curl_timeout)])
    if options.include_full_text:
        command.append("--include-full-text")
    if html_cache_only:
        command.append("--html-cache-only")
    tier_lines: list[str] = []
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=max(1.0, options.paper_timeout), check=False)
        # The extract-content subprocess logs tier fallbacks (html→tex→pdf) on
        # stderr so its stdout stays pure JSON; forward them so the driver can
        # show which fallback path recovered (or failed) this paper.
        for line in (completed.stderr or "").splitlines():
            if line.startswith("TIER "):
                tier_lines.append(line.strip())
                print(line.strip(), flush=True)
        data = None
        if temporary.is_file():
            # extract-content writes its full result JSON (quality grade,
            # attempts, fallback_reason, error) to --output before exiting —
            # including exit 2 ("ran but not evidence-eligible"). Reading it
            # on any exit preserves the real failure reason for packet /
            # deep-read / run_status instead of a bare "extractor exit 2: "
            # with an empty tail (2026-10-16).
            try:
                data = json.loads(temporary.read_text(encoding="utf-8"))
                temporary.replace(target)
            except (json.JSONDecodeError, OSError):
                temporary.unlink(missing_ok=True)
        if data is None:
            data = {
                "paper_id": paper_id,
                "available": False,
                "evidence_eligible": False,
                "error": f"extractor exit {completed.returncode}: {(completed.stderr or completed.stdout)[-800:]}",
            }
            target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except subprocess.TimeoutExpired as exc:
        temporary.unlink(missing_ok=True)
        # Keep the tail of what the extractor printed: without it the
        # checkpoint says only "hard timeout", and the cause (a gate cooldown,
        # a dead endpoint, a slow PDF) is unrecoverable after the fact.
        tail = ""
        raw_stderr = exc.stderr
        if raw_stderr:
            tail = raw_stderr.decode("utf-8", "replace") if isinstance(raw_stderr, bytes) else str(raw_stderr)
            tail = tail.strip()[-800:]
        print(
            f"[DRIVER-WARN] {paper_id} 全文抽取硬超时（{options.paper_timeout:.0f}s），记 HELD 待重试"
            + (f"：{tail.splitlines()[-1]}" if tail else ""),
            flush=True,
        )
        data = {
            "paper_id": paper_id,
            "available": False,
            "evidence_eligible": False,
            "error": f"hard timeout after {options.paper_timeout:.0f}s"
            + (f": {tail}" if tail else ""),
        }
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:  # keep the queue moving and checkpoint the failure
        temporary.unlink(missing_ok=True)
        data = {"paper_id": paper_id, "available": False, "evidence_eligible": False, "error": f"{type(exc).__name__}: {exc}"}
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # One record per paper, after the outcome is known: a hard timeout or a
    # connection-flavoured error advances the streak; a real extraction (or a
    # per-paper failure) resets it.
    if circuit is not None:
        circuit.record(_is_connection_failure(str(data.get("error") or "")))
    eligible = bool(data.get("evidence_eligible"))
    return {
        "paper_id": paper_id,
        "state": "extracted",
        "evidence_eligible": eligible,
        "path": str(target),
        "error": data.get("error", ""),
        "held_reason": ""
        if eligible
        else held_reason(
            data,
            manifest_state=manifest_state,
            manifest_status=manifest_status,
            paper_timeout=options.paper_timeout,
        ),
    }


def run_queue(options: QueueOptions) -> dict[str, Any]:
    output_dir = Path(options.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paper_ids = load_ids(Path(options.paper_id_file))
    workers = max(1, min(int(options.workers), 4))
    results: list[dict[str, Any]] = []
    circuit = _ChannelCircuit()
    # Download-phase manifest (step 1): decides html_cache_only and carries the
    # sticky 404 status into held_reason. Missing file = legacy single-step run.
    manifest: dict[str, tuple[str, int | None]] = {}
    if options.download_manifest:
        try:
            payload = json.loads(Path(options.download_manifest).read_text(encoding="utf-8"))
            for item in payload.get("results") or []:
                if isinstance(item, dict) and item.get("paper_id"):
                    manifest[str(item["paper_id"])] = (
                        str(item.get("state") or ""),
                        item.get("status") if isinstance(item.get("status"), int) else None,
                    )
        except (OSError, json.JSONDecodeError):
            manifest = {}

    def _submit(paper_id: str) -> dict[str, Any]:
        state, status = manifest.get(paper_id, (None, None))
        # downloaded/cached/unavailable: HTML already settled in step 1 — parse
        # from cache only. failed: one last network chance inside the chain.
        cache_only = state in {"downloaded", "cached", "unavailable"}
        return extract_one(
            paper_id,
            options,
            output_dir,
            circuit,
            html_cache_only=cache_only,
            manifest_state=state,
            manifest_status=status,
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_submit, paper_id): paper_id for paper_id in paper_ids}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            state = "OK" if result["evidence_eligible"] else ("CHANNEL-DOWN" if result["state"] == "channel-down" else "HELD")
            reason = str(result.get("held_reason") or "")
            suffix = f" {reason}" if state == "HELD" and reason else ""
            print(f"{state} {result['paper_id']} ({len(results)}/{len(paper_ids)}){suffix}", flush=True)
    # Second pass over HELD papers while the channel is still up. Most HELD
    # outcomes are transient (rate-limited HTML fetch, a 600s hard timeout under
    # load, a subprocess that died before writing its result) — on 2026-10-16
    # all 16 HELD papers of the 强化学习 run re-extracted cleanly minutes later.
    # extract_one already re-extracts a non-eligible checkpoint, so this is a
    # plain retry; a genuinely unrecoverable paper just re-checkpoints as HELD.
    held = [item for item in results if not item["evidence_eligible"] and item["state"] != "channel-down"]
    if held and not circuit.tripped:
        print(f"retry: {len(held)} HELD paper(s) get one more attempt", flush=True)
        for item in held:
            result = _submit(str(item["paper_id"]))
            results[results.index(item)] = result
            state = "OK" if result["evidence_eligible"] else ("CHANNEL-DOWN" if result["state"] == "channel-down" else "HELD")
            reason = str(result.get("held_reason") or "")
            suffix = f" {reason}" if state == "HELD" and reason else ""
            print(f"RETRY-{state} {result['paper_id']}{suffix}", flush=True)
            if circuit.tripped:
                print("retry: channel down mid-pass, leaving the rest HELD for a rerun", flush=True)
                break
    results.sort(key=lambda item: paper_ids.index(str(item["paper_id"])))
    skipped = sum(1 for item in results if item["state"] == "channel-down")
    if skipped:
        print(
            f"channel down: skipped {skipped} papers after "
            f"{circuit.limit} consecutive connection failures; rerun to retry them",
            flush=True,
        )
    summary = {
        "version": 1,
        "paper_count": len(paper_ids),
        "evidence_eligible_count": sum(bool(item["evidence_eligible"]) for item in results),
        "held_count": sum(not bool(item["evidence_eligible"]) for item in results),
        "channel_down_count": skipped,
        "workers": workers,
        "ocr_mode": options.ocr_mode,
        "include_full_text": bool(options.include_full_text),
        "results": results,
    }
    if options.summary_output:
        Path(options.summary_output).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary

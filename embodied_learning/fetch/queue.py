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
) -> dict[str, Any]:
    target = output_dir / f"{paper_id}.json"
    if target.is_file() and not options.force:
        data = json.loads(target.read_text(encoding="utf-8"))
        if data.get("evidence_eligible"):
            return {"paper_id": paper_id, "state": "cached", "evidence_eligible": True, "path": str(target)}
        # A previously HELD paper is retryable, not cached: the fetch may have
        # failed transiently (rate limit) and a driver rerun should supplement
        # it instead of skipping it forever. Falls through to a fresh extract;
        # a paper that is genuinely unrecoverable just re-checkpoints as HELD.
    # Channel already declared down by an earlier run of consecutive
    # connection failures — do not spend this paper's full budget on a
    # network that is not answering. The driver rerun retries these.
    if circuit is not None and circuit.tripped:
        data = {
            "paper_id": paper_id,
            "available": False,
            "evidence_eligible": False,
            "error": "channel down: skipped after consecutive connection failures",
        }
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"paper_id": paper_id, "state": "channel-down", "evidence_eligible": False, "path": str(target), "error": data["error"]}
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
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=max(1.0, options.paper_timeout), check=False)
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
    return {"paper_id": paper_id, "state": "extracted", "evidence_eligible": bool(data.get("evidence_eligible")), "path": str(target), "error": data.get("error", "")}


def run_queue(options: QueueOptions) -> dict[str, Any]:
    output_dir = Path(options.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paper_ids = load_ids(Path(options.paper_id_file))
    workers = max(1, min(int(options.workers), 4))
    results: list[dict[str, Any]] = []
    circuit = _ChannelCircuit()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(extract_one, paper_id, options, output_dir, circuit): paper_id
            for paper_id in paper_ids
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            state = "OK" if result["evidence_eligible"] else ("CHANNEL-DOWN" if result["state"] == "channel-down" else "HELD")
            print(f"{state} {result['paper_id']} ({len(results)}/{len(paper_ids)})", flush=True)
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
            result = extract_one(str(item["paper_id"]), options, output_dir, circuit)
            results[results.index(item)] = result
            state = "OK" if result["evidence_eligible"] else ("CHANNEL-DOWN" if result["state"] == "channel-down" else "HELD")
            print(f"RETRY-{state} {result['paper_id']}", flush=True)
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

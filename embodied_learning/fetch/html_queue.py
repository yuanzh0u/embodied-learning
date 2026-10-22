#!/usr/bin/env python3
"""Batch-download arXiv HTML with machine-wide pacing, retries, and a manifest.

Step 1 of the two-step extraction split (2026-10-21): this phase owns the
network for the HTML tier — one request per paper behind the machine-wide
``arxiv`` ratelimit gate, explicit bounded retries for transient failures, and
a sticky ``unavailable`` state for clean 404/410s so reruns do not re-request
papers arXiv does not have as HTML. Step 2 (``extract-content-queue``) reads
the cache with ``--html-cache-only`` and only touches the network for the
tex/pdf fallback tier.

Library API: ``HtmlDownloadOptions`` / ``download_one`` / ``run_download_queue``
take explicit parameters; the CLI surface lives in
``skills/embodied-ai-literature-hub/scripts/fetch.py`` (``download-content-html``).
"""

from __future__ import annotations

import concurrent.futures
import json
import time
import urllib.error
from pathlib import Path
from typing import Any

from embodied_learning.config import (
    DEFAULT_RETRY_CAP_SECONDS,
    HTML_DOWNLOAD_RETRIES,
    HTML_DOWNLOAD_RETRY_BASE_S,
    HTML_DOWNLOAD_TIMEOUT_S,
    MAX_RETRIES,
)
from embodied_learning.fetch import html as extract_arxiv_html
from embodied_learning.fetch.queue import (
    _ChannelCircuit,
    _is_connection_failure,
    load_ids,
)
from embodied_learning.ratelimit import GateTimeout
from embodied_learning.search.http import is_retryable, retry_wait_seconds

# Per-paper stdout protocol consumed by the driver (download_queue_line).
# Keep the state vocabulary stable — the wiki progress bar counts on it.
STATES = ("DOWNLOADED", "CACHED", "UNAVAILABLE", "FAILED", "CHANNEL-DOWN")


class HtmlDownloadOptions:
    """CLI-option state for one :func:`run_download_queue` run."""

    def __init__(
        self,
        *,
        paper_id_file: str,
        html_cache_dir: str | None = None,
        workers: int = 4,
        timeout: float = HTML_DOWNLOAD_TIMEOUT_S,
        retries: int = HTML_DOWNLOAD_RETRIES,
        force: bool = False,
        summary_output: str | None = None,
        manifest_path: str | None = None,
    ) -> None:
        self.paper_id_file = paper_id_file
        self.html_cache_dir = html_cache_dir if html_cache_dir is not None else extract_arxiv_html.DEFAULT_CACHE_DIR
        self.workers = workers
        self.timeout = timeout
        self.retries = max(0, min(int(retries), MAX_RETRIES))
        self.force = force
        self.summary_output = summary_output
        # Previous manifest (same path as summary_output on a rerun): read for
        # sticky-unavailable inheritance before being overwritten.
        self.manifest_path = manifest_path if manifest_path is not None else summary_output


def _load_previous_states(path: str | None) -> dict[str, tuple[str, int | None]]:
    """paper_id -> (state, status) from a prior manifest, {} when unreadable."""
    if not path:
        return {}
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    states: dict[str, tuple[str, int | None]] = {}
    for item in payload.get("results") or []:
        if isinstance(item, dict) and item.get("paper_id"):
            states[str(item["paper_id"])] = (
                str(item.get("state") or ""),
                item.get("status") if isinstance(item.get("status"), int) else None,
            )
    return states


def _retryable(exc: Exception) -> bool:
    # A gate cooldown (machine-wide 429/503 backoff) is transient by
    # definition: the next attempt after the cooldown is likely to succeed.
    return isinstance(exc, GateTimeout) or is_retryable(exc)


def download_one(
    paper_id: str,
    options: HtmlDownloadOptions,
    circuit: _ChannelCircuit | None = None,
    previous_state: str | None = None,
    previous_status: int | None = None,
) -> dict[str, Any]:
    """Download one paper's HTML into the shared cache.

    States: ``cached`` (already on disk), ``downloaded`` (fetched this run),
    ``unavailable`` (clean 404/410 — sticky across reruns unless ``--force``),
    ``failed`` (transient errors exhausted retries), ``channel-down`` (circuit
    tripped, not attempted).
    """
    cache_dir = Path(options.html_cache_dir).expanduser()
    target = cache_dir / f"{paper_id}.html"
    if target.is_file() and target.stat().st_size > 0:
        return {"paper_id": paper_id, "state": "cached", "attempts": 0, "status": 200, "error": "", "path": str(target)}
    # Sticky permanent miss: arXiv has no HTML for this paper (404/410).
    # Re-requesting it every rerun wastes gate slots for papers we can never
    # get; --force (or a new run without the manifest) opts back in.
    if previous_state == "unavailable" and not options.force:
        return {
            "paper_id": paper_id,
            "state": "unavailable",
            "attempts": 0,
            "status": previous_status or 404,
            "error": "",
            "path": str(target),
            "sticky": True,
        }
    if circuit is not None and circuit.tripped:
        return {
            "paper_id": paper_id,
            "state": "channel-down",
            "attempts": 0,
            "status": None,
            "error": "channel down: skipped after consecutive connection failures",
            "path": str(target),
        }

    url = f"https://arxiv.org/html/{paper_id}"
    attempts = 0
    last_error = ""
    last_exc: Exception | None = None
    status: int | None = None
    for attempt in range(options.retries + 1):
        attempts = attempt + 1
        try:
            ok, _payload = extract_arxiv_html.fetch_html(url, target, options.timeout)
            if ok:
                return {"paper_id": paper_id, "state": "downloaded", "attempts": attempts, "status": 200, "error": "", "path": str(target)}
            # fetch_html returns a clean (False, "") only for 404/410 — a
            # permanent miss, never worth retrying.
            status = 404
            return {"paper_id": paper_id, "state": "unavailable", "attempts": attempts, "status": status, "error": "", "path": str(target)}
        except urllib.error.HTTPError as exc:
            status = int(exc.code)
            last_exc = exc
            last_error = f"HTTP {exc.code}: {exc.reason}"
            if not _retryable(exc):
                break
        except Exception as exc:  # URLError / timeout / gate cooldown / OSError
            last_exc = exc
            last_error = f"{type(exc).__name__}: {exc}"
            if not _retryable(exc):
                break
        if attempt < options.retries and last_exc is not None:
            time.sleep(
                retry_wait_seconds(
                    last_exc,
                    attempt,
                    HTML_DOWNLOAD_RETRY_BASE_S,
                    DEFAULT_RETRY_CAP_SECONDS,
                )
            )
    result = {
        "paper_id": paper_id,
        "state": "failed",
        "attempts": attempts,
        "status": status,
        "error": last_error,
        "path": str(target),
    }
    if circuit is not None:
        circuit.record(_is_connection_failure(last_error))
    return result


def run_download_queue(options: HtmlDownloadOptions) -> dict[str, Any]:
    cache_dir = Path(options.html_cache_dir).expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    paper_ids = load_ids(Path(options.paper_id_file))
    previous = _load_previous_states(options.manifest_path)
    workers = max(1, min(int(options.workers), 4))
    results: list[dict[str, Any]] = []
    circuit = _ChannelCircuit()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                download_one,
                paper_id,
                options,
                circuit,
                previous.get(paper_id, (None, None))[0],
                previous.get(paper_id, (None, None))[1],
            ): paper_id
            for paper_id in paper_ids
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            # Protocol vocabulary consumed by the driver's download_queue_line.
            wire = {
                "downloaded": "DOWNLOADED",
                "cached": "CACHED",
                "unavailable": "UNAVAILABLE",
                "failed": "FAILED",
                "channel-down": "CHANNEL-DOWN",
            }.get(str(result["state"]), "FAILED")
            print(f"{wire} {result['paper_id']} ({len(results)}/{len(paper_ids)})", flush=True)
    results.sort(key=lambda item: paper_ids.index(str(item["paper_id"])))
    states: dict[str, int] = {}
    for item in results:
        states[str(item["state"])] = states.get(str(item["state"]), 0) + 1
    summary = {
        "version": 1,
        "paper_count": len(paper_ids),
        "workers": workers,
        "timeout": options.timeout,
        "retries": options.retries,
        "states": states,
        "results": results,
    }
    if options.summary_output:
        Path(options.summary_output).write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return summary

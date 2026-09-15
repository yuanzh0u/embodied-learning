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
from pathlib import Path
from typing import Any

from embodied_learning.fetch import chain as extract_arxiv_content

_REPO_ROOT = Path(__file__).resolve().parents[2]
# Per-paper subprocess target: prefer the repo thin entry (dev/CI), fall back to
# running the installed module when skills/ is absent (wheel installs).
_EXTRACT_ENTRY = _REPO_ROOT / "skills" / "embodied-ai-literature-hub" / "scripts" / "extract_arxiv_content.py"
_EXTRACT_CMD = (
    [sys.executable, str(_EXTRACT_ENTRY)] if _EXTRACT_ENTRY.is_file()
    else [sys.executable, "-m", "hub_scripts.extract_arxiv_content"]
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
        paper_timeout: float = 120.0,
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
        html_cache_dir=extract_arxiv_content.extract_arxiv_html.DEFAULT_CACHE_DIR,
        pdf_cache_dir=extract_arxiv_content.extract_arxiv_pdf.DEFAULT_CACHE_DIR,
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


def extract_one(paper_id: str, options: QueueOptions, output_dir: Path) -> dict[str, Any]:
    target = output_dir / f"{paper_id}.json"
    if target.is_file() and not options.force:
        data = json.loads(target.read_text(encoding="utf-8"))
        return {"paper_id": paper_id, "state": "cached", "evidence_eligible": bool(data.get("evidence_eligible")), "path": str(target)}
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
        if completed.returncode == 0 and temporary.is_file():
            data = json.loads(temporary.read_text(encoding="utf-8"))
            temporary.replace(target)
        else:
            temporary.unlink(missing_ok=True)
            data = {
                "paper_id": paper_id,
                "available": False,
                "evidence_eligible": False,
                "error": f"extractor exit {completed.returncode}: {(completed.stderr or completed.stdout)[-800:]}",
            }
            target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except subprocess.TimeoutExpired:
        temporary.unlink(missing_ok=True)
        data = {
            "paper_id": paper_id,
            "available": False,
            "evidence_eligible": False,
            "error": f"hard timeout after {options.paper_timeout:.0f}s",
        }
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:  # keep the queue moving and checkpoint the failure
        temporary.unlink(missing_ok=True)
        data = {"paper_id": paper_id, "available": False, "evidence_eligible": False, "error": f"{type(exc).__name__}: {exc}"}
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"paper_id": paper_id, "state": "extracted", "evidence_eligible": bool(data.get("evidence_eligible")), "path": str(target), "error": data.get("error", "")}


def run_queue(options: QueueOptions) -> dict[str, Any]:
    output_dir = Path(options.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paper_ids = load_ids(Path(options.paper_id_file))
    workers = max(1, min(int(options.workers), 4))
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(extract_one, paper_id, options, output_dir): paper_id for paper_id in paper_ids}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            state = "OK" if result["evidence_eligible"] else "HELD"
            print(f"{state} {result['paper_id']} ({len(results)}/{len(paper_ids)})", flush=True)
    results.sort(key=lambda item: paper_ids.index(str(item["paper_id"])))
    summary = {
        "version": 1,
        "paper_count": len(paper_ids),
        "evidence_eligible_count": sum(bool(item["evidence_eligible"]) for item in results),
        "held_count": sum(not bool(item["evidence_eligible"]) for item in results),
        "workers": workers,
        "ocr_mode": options.ocr_mode,
        "include_full_text": bool(options.include_full_text),
        "results": results,
    }
    if options.summary_output:
        Path(options.summary_output).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary

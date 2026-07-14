#!/usr/bin/env python3
"""Recover arXiv full text for an ID queue with bounded concurrency and per-paper checkpoints."""

from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("extract_arxiv_content", SCRIPTS_DIR / "extract_arxiv_content.py")
extract_arxiv_content = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(extract_arxiv_content)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id-file", required=True)
    parser.add_argument("--terms", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--workers", type=int, default=2, help="Bounded I/O workers; capped at 4.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--paper-timeout", type=float, default=120.0, help="Hard wall-clock limit per paper subprocess.")
    parser.add_argument("--top-sections", type=int, default=3)
    parser.add_argument("--ocr-mode", choices=["auto", "never", "always"], default="never")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help="Checkpoint complete HTML text/PDF pages for $embodied-ai-paper-reader.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--summary-output")
    return parser.parse_args()


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


def extraction_args(paper_id: str, args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        paper_id=paper_id,
        terms=args.terms,
        html_url=None,
        pdf_url=None,
        pdf_file=None,
        html_cache_dir=extract_arxiv_content.extract_arxiv_html.DEFAULT_CACHE_DIR,
        pdf_cache_dir=extract_arxiv_content.extract_arxiv_pdf.DEFAULT_CACHE_DIR,
        timeout=args.timeout,
        top_sections=args.top_sections,
        max_pages=0,
        ocr_mode=args.ocr_mode,
        ocr_language=args.ocr_language,
        ocr_dpi=220,
        min_chars_per_page=180,
        minimum_html_chars=1000,
        force_pdf=False,
        include_selected_text=True,
        include_full_text=args.include_full_text,
    )


def extract_one(paper_id: str, args: argparse.Namespace, output_dir: Path) -> dict[str, Any]:
    target = output_dir / f"{paper_id}.json"
    if target.is_file() and not args.force:
        data = json.loads(target.read_text(encoding="utf-8"))
        return {"paper_id": paper_id, "state": "cached", "evidence_eligible": bool(data.get("evidence_eligible")), "path": str(target)}
    temporary = target.with_suffix(".json.tmp")
    command = [
        sys.executable,
        str(SCRIPTS_DIR / "extract_arxiv_content.py"),
        "--paper-id", paper_id,
        "--terms", args.terms,
        "--timeout", str(args.timeout),
        "--top-sections", str(args.top_sections),
        "--ocr-mode", args.ocr_mode,
        "--ocr-language", args.ocr_language,
        "--include-selected-text",
        "--output", str(temporary),
    ]
    if args.include_full_text:
        command.append("--include-full-text")
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=max(1.0, args.paper_timeout), check=False)
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
            "error": f"hard timeout after {args.paper_timeout:.0f}s",
        }
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:  # keep the queue moving and checkpoint the failure
        temporary.unlink(missing_ok=True)
        data = {"paper_id": paper_id, "available": False, "evidence_eligible": False, "error": f"{type(exc).__name__}: {exc}"}
        target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"paper_id": paper_id, "state": "extracted", "evidence_eligible": bool(data.get("evidence_eligible")), "path": str(target), "error": data.get("error", "")}


def run_queue(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paper_ids = load_ids(Path(args.paper_id_file))
    workers = max(1, min(int(args.workers), 4))
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(extract_one, paper_id, args, output_dir): paper_id for paper_id in paper_ids}
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
        "ocr_mode": args.ocr_mode,
        "include_full_text": bool(args.include_full_text),
        "results": results,
    }
    if args.summary_output:
        Path(args.summary_output).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    summary = run_queue(parse_args())
    print(f"Recovered {summary['evidence_eligible_count']} of {summary['paper_count']} papers; held {summary['held_count']}.")
    return 0 if summary["evidence_eligible_count"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

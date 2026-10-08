#!/usr/bin/env python3
"""Fetch complete non-OCR full text via alphaxiv (SSR abs page -> versionId -> full-text API).

Emits pipeline-compatible extraction JSON (source_format=pdf, page-wise text layer)
for embodied-ai-paper-reader. arXiv is unreachable from this sandbox; alphaxiv
mirrors the same text layer. Scan-only/garbled papers are marked unavailable.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
TERMS = [
    "SLAM",
    "localization",
    "mapping",
    "embodied",
    "navigation",
    "manipulation",
    "vision-language-action",
    "world model",
    "Gaussian splatting",
    "map-free",
    "mapless",
    "spatial memory",
    "visual odometry",
    "loop closure",
    "teleoperation",
    "pose estimation",
    "3D reconstruction",
    "foundation model",
    "depth estimation",
    "relocalization",
]
MAX_TERM_MATCHES = 120
SNIPPET_CHARS = 160


def http_get(url: str, timeout: float = 30.0, max_attempts: int = 4) -> str:
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": UA, "Accept": "application/json, text/html"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in (429, 500, 502, 503) and attempt < max_attempts:
                time.sleep(2.0 * attempt)
                continue
            raise
        except urllib.error.URLError as e:
            last_error = e
            if attempt < max_attempts:
                time.sleep(2.0 * attempt)
                continue
            raise
    raise RuntimeError(f"unreachable after {max_attempts} attempts: {last_error}")


def normalize_ws(text: str) -> str:
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def fetch_ssr_meta(arxiv_id: str, raw_dir: Path) -> dict:
    cache = raw_dir / f"{arxiv_id}.ssr.html"
    if cache.exists() and cache.stat().st_size > 1000:
        html = cache.read_text(encoding="utf-8", errors="replace")
    else:
        html = http_get(f"https://www.alphaxiv.org/abs/{arxiv_id}")
        cache.write_text(html, encoding="utf-8")
    m = re.search(
        r'versionlessId:"([^"]+)",canonicalId:"([^"]+)",versionId:"([0-9a-f-]+)"', html
    )
    if not m:
        return {"found": False, "ssr_bytes": len(html)}
    title_match = re.search(r"<title>(.*?)</title>", html, re.S)
    title = title_match.group(1).strip() if title_match else ""
    title = re.sub(r"\s*\|\s*alpha.*$", "", title, flags=re.I).strip()
    return {
        "found": True,
        "versionless_id": m.group(1),
        "canonical_id": m.group(2),
        "version_id": m.group(3),
        "title": title,
        "ssr_bytes": len(html),
    }


def fetch_fulltext(version_id: str, arxiv_id: str, raw_dir: Path) -> dict:
    cache = raw_dir / f"{arxiv_id}.fulltext.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    raw = http_get(
        f"https://api.alphaxiv.org/papers/v3/{version_id}/full-text", timeout=45.0
    )
    data = json.loads(raw)
    cache.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def merge_empty_pages(pages: list[dict]) -> list[dict]:
    merged: list[dict] = []
    for page in pages:
        text = str(page.get("text") or "").strip()
        number = page.get("pageNumber") or page.get("page") or (len(merged) + 1)
        if not text:
            if merged:
                merged[-1]["_note_empty_pages"] = (
                    merged[-1].get("_note_empty_pages", []) + [number]
                )
            else:
                merged.append({"page": number, "text": "", "_note_empty_pages": []})
            continue
        merged.append({"page": number, "text": text})
    return [p for p in merged if p["text"].strip()]


def build_term_matches(pages: list[dict]) -> list[dict]:
    matches: list[dict] = []
    for page in pages:
        text = page["text"]
        lowered = text.lower()
        for term in TERMS:
            if len(matches) >= MAX_TERM_MATCHES:
                return matches
            start = 0
            count = 0
            t_low = term.lower()
            while count < 3 and len(matches) < MAX_TERM_MATCHES:
                idx = lowered.find(t_low, start)
                if idx < 0:
                    break
                snippet = text[max(0, idx - 60) : idx + SNIPPET_CHARS]
                matches.append(
                    {
                        "term": term,
                        "locator": f"page {page['page']}",
                        "section_index": page["page"],
                        "char_start": idx,
                        "snippet": " ".join(snippet.split()),
                    }
                )
                start = idx + len(term)
                count += 1
    return matches


def build_extraction(
    arxiv_id: str, meta: dict, fulltext: dict
) -> tuple[dict, str]:
    raw_pages = fulltext.get("pages") or []
    pages = merge_empty_pages(raw_pages)
    total_chars = sum(len(p["text"]) for p in pages)
    status = "ok"
    if len(pages) < 4:
        status = "too_few_pages"
    elif total_chars < 8000:
        status = "too_short"

    text = "\n\n".join(f"## page {p['page']}\n\n{p['text']}" for p in pages)
    empty_notes = sorted(
        {n for p in pages for n in p.get("_note_empty_pages", [])}
    )

    if status == "ok" and total_chars >= 15000 and len(pages) >= 6:
        grade = "high"
    elif status == "ok":
        grade = "medium"
    else:
        grade = "low"

    extraction = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": arxiv_id,
        "title": meta.get("title") or "",
        "alphaxiv": {
            "version_id": meta["version_id"],
            "canonical_id": meta.get("canonical_id"),
            "abs_url": f"https://www.alphaxiv.org/abs/{arxiv_id}",
            "source": "alphaxiv mirror of arXiv text layer (non-OCR)",
        },
        "available": grade in {"high", "medium"},
        "source_format": "pdf",
        "extraction_method": "alphaxiv-fulltext-api",
        "structure": "page-based-text-layer",
        "text_chars": total_chars,
        "page_count": len(pages),
        "pages": [
            {
                "page": p["page"],
                "text": p["text"],
                "extraction_method": "pdf-text",
            }
            for p in pages
        ],
        "text": text,
        "quality": {
            "grade": grade,
            "text_chars": total_chars,
            "structure": "page-based",
            "empty_pages_merged": empty_notes,
        },
        "evidence_eligible": grade in {"high", "medium"},
        "needs_visual_validation": grade == "medium",
        "term_matches": build_term_matches(pages) if grade != "low" else [],
        "attempts": [
            {
                "method": "pdf-text",
                "available": grade in {"high", "medium"},
                "quality": grade,
                "channel": "alphaxiv-fulltext-api",
            }
        ],
        "fallback_reason": "" if grade != "low" else status,
    }
    return extraction, status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids-file", default="extraction-ids.txt")
    parser.add_argument("--out-dir", default="extractions")
    parser.add_argument("--raw-dir", default="alphaxiv-raw")
    parser.add_argument("--status-file", default="extraction-status.json")
    parser.add_argument("--sleep", type=float, default=1.2)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    run_dir = Path(__file__).resolve().parent
    ids: list[str] = []
    for line in (run_dir / args.ids_file).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            ids.append(line)
    if args.limit:
        ids = ids[: args.limit]

    out_dir = run_dir / args.out_dir
    raw_dir = run_dir / args.raw_dir
    out_dir.mkdir(exist_ok=True)
    raw_dir.mkdir(exist_ok=True)

    status: dict[str, dict] = {}
    if (run_dir / args.status_file).exists():
        status = json.loads((run_dir / args.status_file).read_text())

    counts = {"ok_high": 0, "ok_medium": 0, "not_on_alphaxiv": 0, "no_fulltext": 0, "failed": 0, "low": 0}
    for i, arxiv_id in enumerate(ids, 1):
        try:
            meta = fetch_ssr_meta(arxiv_id, raw_dir)
            time.sleep(args.sleep)
            if not meta.get("found"):
                status[arxiv_id] = {"status": "not_on_alphaxiv", "title": ""}
                counts["not_on_alphaxiv"] += 1
                print(f"[{i}/{len(ids)}] {arxiv_id}: not_on_alphaxiv", flush=True)
                continue
            fulltext = fetch_fulltext(meta["version_id"], arxiv_id, raw_dir)
            time.sleep(args.sleep)
            if not fulltext.get("pages"):
                status[arxiv_id] = {
                    "status": "no_fulltext",
                    "title": meta.get("title", ""),
                }
                counts["no_fulltext"] += 1
                print(f"[{i}/{len(ids)}] {arxiv_id}: no_fulltext", flush=True)
                continue
            extraction, st = build_extraction(arxiv_id, meta, fulltext)
            (out_dir / f"{arxiv_id}.json").write_text(
                json.dumps(extraction, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            grade = extraction["quality"]["grade"]
            if grade == "high":
                counts["ok_high"] += 1
            elif grade == "medium":
                counts["ok_medium"] += 1
            else:
                counts["low"] += 1
            status[arxiv_id] = {
                "status": st,
                "grade": grade,
                "title": meta.get("title", ""),
                "pages": extraction["page_count"],
                "chars": extraction["text_chars"],
            }
            print(
                f"[{i}/{len(ids)}] {arxiv_id}: {grade} "
                f"({extraction['page_count']}p, {extraction['text_chars']} chars) {meta.get('title','')[:60]}",
                flush=True,
            )
        except Exception as e:
            counts["failed"] += 1
            status[arxiv_id] = {"status": "failed", "error": str(e)[:200]}
            print(f"[{i}/{len(ids)}] {arxiv_id}: FAILED {e}", flush=True)
        (run_dir / args.status_file).write_text(
            json.dumps(status, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    print("SUMMARY:", json.dumps(counts), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Resolve open-access PDF URLs for candidate arXiv IDs via Semantic Scholar
(batch endpoint) and download them into work/<run>/pdfs/.

Usage:
  python3 s2_fetch_pdfs.py --ids 2604.14089,2510.16205 [--ids-file path.txt]
"""
import argparse
import json
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.semanticscholar.org/graph/v1/paper/batch"
FIELDS = "title,openAccessPdf,externalIds,publicationDate"
CTX = ssl.create_default_context()


def post_batch(ids, max_attempts=8):
    body = json.dumps({"ids": [f"ARXIV:{i}" for i in ids]}).encode("utf-8")
    url = f"{API}?fields={FIELDS}"
    for attempt in range(1, max_attempts + 1):
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": "embodied-lit-review/1.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60, context=CTX) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = min(60.0, 3.0 * attempt)
                print(f"    HTTP {e.code}, backoff {wait:.0f}s (attempt {attempt})", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    return None


def download(url, target: Path, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": "embodied-lit-review/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        payload = resp.read()
    if len(payload) < 20000 or not payload[:5].startswith(b"%PDF"):
        return False, f"not a pdf or too small ({len(payload)} bytes)"
    target.write_bytes(payload)
    return True, f"{len(payload)} bytes"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="")
    ap.add_argument("--ids-file", default="")
    ap.add_argument("--out-dir", default="pdfs")
    ap.add_argument("--manifest", default="pdfs/manifest.json")
    args = ap.parse_args()

    ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    if args.ids_file:
        ids += [line.strip() for line in open(args.ids_file) if line.strip()]
    ids = list(dict.fromkeys(ids))

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {}
    if Path(args.manifest).exists():
        manifest = json.loads(Path(args.manifest).read_text())

    print(f"resolving {len(ids)} ids via S2 batch API ...")
    results = post_batch(ids)
    if results is None:
        print("ERROR: batch API failed after retries", file=sys.stderr)
        return 1

    pending = []
    for pid, rec in zip(ids, results):
        if rec is None:
            manifest[pid] = {"status": "not_found"}
            continue
        oa = rec.get("openAccessPdf") or {}
        url = oa.get("url") if isinstance(oa, dict) else None
        if not url:
            manifest[pid] = {"status": "no_open_access_pdf", "title": rec.get("title", "")}
            continue
        if manifest.get(pid, {}).get("status") == "downloaded":
            pending.append((pid, url))
            continue
        pending.append((pid, url))

    for n, (pid, url) in enumerate(pending, 1):
        target = out / f"{pid}.pdf"
        if target.exists() and target.stat().st_size > 20000:
            manifest[pid] = {"status": "downloaded", "url": url, "file": str(target)}
            continue
        try:
            ok, note = download(url, target)
        except Exception as exc:
            ok, note = False, str(exc)[:200]
        manifest[pid] = {"status": "downloaded" if ok else "download_failed",
                         "url": url, "note": note}
        print(f"[{n}/{len(pending)}] {pid}: {'ok' if ok else 'fail ' + note}")
        time.sleep(1.0)

    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    ok_count = sum(1 for v in manifest.values() if v.get("status") == "downloaded")
    print(f"manifest written: {args.manifest} (downloaded={ok_count})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

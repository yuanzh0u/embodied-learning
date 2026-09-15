#!/usr/bin/env python3
"""Download arXiv TeX source tarballs from the S3 bucket concurrently.

**TODO — not the default path.** Kept functional pending AWS account setup:

1. ``s3://arxiv/`` is a *requester-pays* bucket (arXiv's documented choice):
   the default ``--requester-pays`` mode signs requests with the standard AWS
   credential chain and passes ``RequestPayer='requester'``, so real
   credentials (``~/.aws/credentials`` or env vars) are required — without
   them every call fails with ``NoCredentialsError``. Download bandwidth is
   billed to the bucket owner's payer account, i.e. to us per GB.
2. ``--anonymous`` (botocore ``UNSIGNED``) documents the zero-credential
   intent but the bucket answers ``AccessDenied`` to anonymous requests today.
3. The default full-text path is now the arxiv2md REST API (curl, no
   credentials) — see ``extract_arxiv_tex.py --transport arxiv2md``. Switch
   back here with ``--transport s3-tex`` once AWS credentials exist.

Per-paper objects live at ``src/YYMM/YYMM.NNNNN.tar.gz`` for modern arXiv IDs.
S3 tolerates high concurrency, so threads run with zero sleep between papers;
transient server errors get a small capped retry.

Tarballs are a download cache (same spirit as the HTML cache): they land in a
temp-dir cache, are skipped when already present, and are never archived into
the paper pool or the repository.

Old-style IDs (``cat/0501001``, ``math.GT/0601136``) and pre-2007-04 IDs have
no ``src/YYMM/...`` key and are reported as ``no-source``.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import importlib.util
import json
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any

BUCKET = "arxiv"
REGION = "us-east-1"
DEFAULT_CACHE_DIR = "/tmp/embodied-ai-literature-hub/src"
MAX_WORKERS = 16
MAX_RETRIES = 3
MODERN_ID_RE = re.compile(r"^(\d{2})(\d{2})\.(\d{4,5})$")


def load_boto3():
    """Lazy boto3 import with an actionable message (repo optional extra: s3)."""
    try:
        import boto3  # type: ignore
        from botocore import UNSIGNED  # type: ignore
        from botocore.config import Config  # type: ignore

        return boto3, UNSIGNED, Config
    except ImportError as exc:
        raise SystemExit(
            "boto3 is required for S3 source download. Install it with:\n"
            "  pip install 'embodied-ai-literature-hub[s3]'   (from the repo root)\n"
            "or: pip install boto3"
        ) from exc


def make_client(region: str = REGION, anonymous: bool = False):
    """S3 client: requester-pays default (signed credentials + RequestPayer),
    or explicit anonymous UNSIGNED mode (expected AccessDenied today)."""
    boto3, UNSIGNED, Config = load_boto3()
    if anonymous:
        return boto3.client("s3", region_name=region, config=Config(signature_version=UNSIGNED))
    return boto3.client("s3", region_name=region)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-id", action="append", default=[], help="arXiv ID. May be repeated.")
    parser.add_argument("--paper-id-file", help="UTF-8 file with one arXiv ID per line (# comments allowed).")
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR, help="Tarball cache directory.")
    parser.add_argument("--workers", type=int, default=8, help=f"Bounded I/O workers; capped at {MAX_WORKERS}.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Per-request read timeout in seconds.")
    parser.add_argument("--retries", type=int, default=2, help="Retries per paper after transient S3 errors. Capped at 3.")
    parser.add_argument("--region", default=REGION, help="S3 region of the arXiv bucket.")
    requester = parser.add_mutually_exclusive_group()
    requester.add_argument("--requester-pays", dest="requester_pays", action="store_true", default=True,
                           help="Sign requests with standard AWS credentials and pass RequestPayer=requester "
                                "(default: s3://arxiv/ is a requester-pays bucket).")
    requester.add_argument("--anonymous", dest="requester_pays", action="store_false",
                           help="Use the botocore.UNSIGNED anonymous client (no credentials; the bucket "
                                "currently answers AccessDenied to anonymous requests).")
    parser.add_argument("--force", action="store_true", help="Re-download even when the cache file exists.")
    parser.add_argument("--summary-output", help="Write the run summary JSON here.")
    return parser.parse_args()


def normalize_id(value: str) -> str:
    return re.sub(r"v\d+$", "", str(value or "").strip().rsplit("/", 1)[-1])


def load_ids(path: Path) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        paper_id = normalize_id(line)
        if paper_id and paper_id not in seen:
            seen.add(paper_id)
            ids.append(paper_id)
    return ids


def source_key(paper_id: str) -> str | None:
    """s3://arxiv/ object key for a modern arXiv ID; None when unsupported."""
    match = MODERN_ID_RE.match(paper_id)
    if not match:
        return None
    yymm = f"{match.group(1)}{match.group(2)}"
    return f"src/{yymm}/{paper_id}.tar.gz"


def download_one(paper_id: str, args: argparse.Namespace, client: Any) -> dict[str, Any]:
    """Download one tarball into the cache. Zero sleep; small retry on 5xx."""
    cache_dir = Path(args.cache_dir).expanduser()
    key = source_key(paper_id)
    if key is None:
        return {"paper_id": paper_id, "state": "no-source", "key": "", "path": "", "bytes": 0,
                "error": f"unsupported arXiv ID for s3://arxiv/ (old-style or pre-0704): {paper_id}"}
    target = cache_dir / f"{paper_id}.tar.gz"
    if target.is_file() and target.stat().st_size > 0 and not args.force:
        return {"paper_id": paper_id, "state": "cached", "key": key, "path": str(target),
                "bytes": target.stat().st_size, "error": ""}
    retries = max(0, min(int(args.retries), MAX_RETRIES))
    request_payer = {"RequestPayer": "requester"} if getattr(args, "requester_pays", True) else {}
    last_error = ""
    for attempt in range(retries + 1):
        part = target.with_suffix(".tar.gz.part")
        try:
            response = client.get_object(Bucket=BUCKET, Key=key, **request_payer)
            part.parent.mkdir(parents=True, exist_ok=True)
            written = 0
            with part.open("wb") as handle:
                for chunk in response["Body"].iter_chunks(chunk_size=1 << 20):
                    handle.write(chunk)
                    written += len(chunk)
            part.replace(target)
            return {"paper_id": paper_id, "state": "downloaded", "key": key, "path": str(target),
                    "bytes": written, "error": ""}
        except client.exceptions.NoSuchKey:
            part.unlink(missing_ok=True)
            return {"paper_id": paper_id, "state": "no-source", "key": key, "path": "", "bytes": 0,
                    "error": f"s3://{BUCKET}/{key} not found (submission may be too new for the S3 mirror)"}
        except Exception as exc:  # transient: 5xx ClientError, connection issues, timeouts
            last_error = f"{type(exc).__name__}: {exc}"
            part.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(min(1.0 * (2**attempt), 5.0))
    return {"paper_id": paper_id, "state": "error", "key": key, "path": "", "bytes": 0, "error": last_error}


def run_queue(args: argparse.Namespace, client: Any) -> dict[str, Any]:
    paper_ids: list[str] = []
    seen: set[str] = set()
    for value in args.paper_id:
        normalized = normalize_id(value)
        if normalized and normalized not in seen:
            seen.add(normalized)
            paper_ids.append(normalized)
    if args.paper_id_file:
        for paper_id in load_ids(Path(args.paper_id_file)):
            if paper_id not in seen:
                seen.add(paper_id)
                paper_ids.append(paper_id)
    if not paper_ids:
        raise SystemExit("provide at least one --paper-id or --paper-id-file")
    workers = max(1, min(int(args.workers), MAX_WORKERS))
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(download_one, paper_id, args, client): paper_id for paper_id in paper_ids}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"{result['state'].upper()} {result['paper_id']} ({len(results)}/{len(paper_ids)})", flush=True)
    results.sort(key=lambda item: paper_ids.index(str(item["paper_id"])))
    counts: dict[str, int] = {}
    for result in results:
        counts[result["state"]] = counts.get(result["state"], 0) + 1
    return {
        "version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "bucket": BUCKET,
        "paper_count": len(paper_ids),
        "workers": workers,
        "states": dict(sorted(counts.items())),
        "cache_dir": str(Path(args.cache_dir).expanduser()),
        "results": results,
    }


def main() -> int:
    args = parse_args()
    client = make_client(args.region, anonymous=not getattr(args, "requester_pays", True))
    summary = run_queue(args, client)
    rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.summary_output:
        path = Path(args.summary_output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    ok = summary["states"].get("downloaded", 0) + summary["states"].get("cached", 0)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())

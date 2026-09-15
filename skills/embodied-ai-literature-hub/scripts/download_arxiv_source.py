#!/usr/bin/env python3
"""CLI: download TeX source tarballs from the requester-pays s3://arxiv/ bucket.

Library API lives in src/fetch/s3_source.py (S3DownloadOptions plus the
module-level helpers). This entry owns only argument parsing and dispatch.
"""
import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.fetch.s3_source import (  # noqa: E402
    DEFAULT_CACHE_DIR,
    MAX_WORKERS,
    REGION,
    S3DownloadOptions,
    collect_ids,
    make_client,
    run_queue,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    options = S3DownloadOptions(
        cache_dir=args.cache_dir,
        workers=args.workers,
        timeout=args.timeout,
        retries=args.retries,
        region=args.region,
        requester_pays=args.requester_pays,
        force=args.force,
    )
    paper_ids = collect_ids(args.paper_id, args.paper_id_file)
    client = make_client(options.region, anonymous=not options.requester_pays)
    summary = run_queue(paper_ids, options, client)
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

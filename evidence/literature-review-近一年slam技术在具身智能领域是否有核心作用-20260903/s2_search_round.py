"""Search Semantic Scholar Graph API as the discovery channel when the arXiv API is unreachable.

Reads the run query plan, converts arXiv-API-syntax queries to keyword strings,
searches S2 with rate-limit backoff, keeps only papers with arXiv IDs and
publicationDate inside the review window, and emits search_arxiv.py-compatible
JSON so build_candidate_registry.py --search-result can merge it.
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,externalIds,publicationDate,abstract,fieldsOfStudy,venue"


def convert_query(q: str) -> str:
    q = re.sub(r"\ball:", "", q)
    q = q.replace(" AND ", " ")
    q = q.replace("(", " ").replace(")", " ")
    q = re.sub(r"\s+", " ", q)
    return q.strip()


def s2_search(query: str, year_from: int, year_to: int, limit: int, max_attempts: int = 10):
    params = {
        "query": query,
        "fields": FIELDS,
        "limit": str(limit),
        "year": f"{year_from}-{year_to}",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(1, max_attempts + 1):
        req = urllib.request.Request(url, headers={"User-Agent": "embodied-lit-review/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = 3.0 * attempt
                retry_after = e.headers.get("Retry-After") if e.headers else None
                if retry_after:
                    try:
                        wait = max(wait, float(retry_after))
                    except ValueError:
                        pass
                print(f"    HTTP {e.code}, backoff {wait:.0f}s (attempt {attempt})", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"    network {e}, backoff {5*attempt}s (attempt {attempt})", file=sys.stderr)
            time.sleep(5 * attempt)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--batch-label", default="s2-round")
    ap.add_argument("--from-date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--to-date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--sleep", type=float, default=4.0)
    ap.add_argument("--labels", help="comma-separated subset of query labels to run")
    args = ap.parse_args()

    plan = json.load(open(args.plan))
    only = set(args.labels.split(",")) if args.labels else None

    papers, queries, failed = {}, [], []
    for q in plan["queries"]:
        if only and q["label"] not in only:
            continue
        kw = convert_query(q["query"])
        print(f"[{q['label']}] {kw}", file=sys.stderr)
        data = s2_search(kw, int(args.from_date[:4]), int(args.to_date[:4]), args.limit)
        if data is None:
            failed.append(q["label"])
            queries.append({"label": q["label"], "query": q["query"], "result_count": 0,
                            "error": "S2 exhausted retries"})
            continue
        hits = data.get("data") or []
        kept = 0
        for p in hits:
            arxiv_id = (p.get("externalIds") or {}).get("ArXiv")
            if not arxiv_id:
                continue
            pub = p.get("publicationDate") or ""
            if not (args.from_date <= pub <= args.to_date):
                continue
            key = arxiv_id
            rec = papers.setdefault(key, {
                "arxiv_id": arxiv_id,
                "title": p.get("title") or "",
                "authors": [],
                "published": pub,
                "summary": p.get("abstract") or "",
                "categories": p.get("fieldsOfStudy") or [],
                "query_label": q["label"],
                "matched_queries": [],
            })
            rec["matched_queries"].append(q["label"])
            kept += 1
        queries.append({"label": q["label"], "query": q["query"], "result_count": kept})
        print(f"    kept {kept} in-window arXiv papers", file=sys.stderr)
        time.sleep(args.sleep)

    out = {
        "batch_label": args.batch_label,
        "channel": "semantic-scholar-graph-api",
        "note": "arXiv export API unreachable from this environment; discovery ran via Semantic Scholar Graph API search",
        "date_range": [args.from_date, args.to_date],
        "papers": list(papers.values()),
        "queries": queries,
        "failed_queries": failed,
    }
    json.dump(out, open(args.output, "w"), ensure_ascii=False, indent=1)
    print(f"wrote {args.output}: {len(papers)} unique papers, {len(failed)} failed queries", file=sys.stderr)


if __name__ == "__main__":
    main()

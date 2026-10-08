#!/usr/bin/env python3
"""Build paper-metadata JSON files from cached alphaxiv SSR pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
RAW = RUN_DIR / "alphaxiv-raw"
OUT = RUN_DIR / "paper-metadata"


def norm_date(value: str) -> str:
    m = re.match(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", value.strip())
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return value.strip()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    registry = json.loads((RUN_DIR / "candidate-registry.json").read_text())
    reg_titles = {
        c["arxiv_id"]: c.get("title", "")
        for c in registry.get("candidates", [])
    }
    count = 0
    for ssr in sorted(RAW.glob("*.ssr.html")):
        arxiv_id = ssr.name.removesuffix(".ssr.html")
        html = ssr.read_text(encoding="utf-8", errors="replace")
        authors = re.findall(
            r'<meta name="citation_author" content="([^"]+)"', html
        )
        title_m = re.search(
            r'<meta property="og:title" content="([^"]+)"', html
        ) or re.search(r'<meta name="citation_title" content="([^"]+)"', html)
        title = title_m.group(1).strip() if title_m else reg_titles.get(arxiv_id, "")
        title = re.sub(r"\s*\|\s*alpha.*$", "", title, flags=re.I).strip()
        date_m = re.search(
            r'<meta name="citation_publication_date" content="([^"]+)"', html
        )
        published = norm_date(date_m.group(1)) if date_m else ""
        if not authors:
            jsonld = re.search(r'"author":\[(.*?)\]', html)
            if jsonld:
                authors = re.findall(r'"name":"([^"]+)"', jsonld.group(1))
        meta = {
            "paper": {
                "arxiv_id": arxiv_id,
                "title": title,
                "published": published,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "authors": authors,
            }
        }
        (OUT / f"{arxiv_id}.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        count += 1
    print(f"wrote {count} metadata files to {OUT}")


if __name__ == "__main__":
    main()

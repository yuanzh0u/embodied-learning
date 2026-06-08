# Browser Candidate Fallback

Use this when arXiv API search is rate-limited, times out, returns query-level errors, or produces too small a candidate pool for a named method family.

## Principle

- Browser/web search is only for candidate discovery.
- Accepted evidence still requires arXiv HTML正文 extraction through `scripts/extract_arxiv_html.py`.
- If a candidate has no arXiv HTML正文, keep it as metadata-only and do not mine正文 claims.
- Record fallback source labels so later readers know the paper came from browser discovery rather than API search.

## Browser workflow

1. Open the Browser in the background.
2. Run one or more focused web/arXiv searches from the query plan labels:
   - `site:arxiv.org/abs UMI "Universal Manipulation Interface" robot manipulation after:YYYY-MM-DD before:YYYY-MM-DD`
   - `site:arxiv.org/abs ("UMI-FT" OR "UMI-3D" OR "RealDexUMI" OR "DexUMI") robot after:YYYY-MM-DD before:YYYY-MM-DD`
   - `site:arxiv.org/abs "demonstration quality" "robot learning" gripper after:YYYY-MM-DD before:YYYY-MM-DD`
   - `site:arxiv.org/abs "occlusion" SLAM "data collection" manipulation after:YYYY-MM-DD before:YYYY-MM-DD`
3. Prefer authoritative arXiv result pages over generic snippets:
   - `https://arxiv.org/search/cs?...`
   - `https://arxiv.org/abs/<id>`
   - `https://arxiv.org/html/<id>`
   - If arXiv search pages stall in Browser, use a lightweight web-search result export or direct known `abs/html` pages, then mark the discovery source and continue to HTML正文 validation.
4. Export the visible result page data as JSON or text. Include:
   - page URL
   - page title
   - visible text or DOM snapshot
   - links whose `href` contains `/abs/`, `/html/`, or `/pdf/`
5. Normalize candidates:
   - Run `scripts/parse_browser_candidates.py` on the browser export.
   - Filter to the explicit date range using submitted dates when available.
   - If only the arXiv ID month is known, treat it as a candidate needing abs-page validation.
6. Validate candidates:
   - Open `https://arxiv.org/abs/<id>` or `https://arxiv.org/html/<id>` to confirm title, authors, and submitted date.
   - Run `scripts/extract_arxiv_html.py --paper-id <id>` and promote only if `available=true`.

## Browser export shape

The parser accepts plain text, HTML, or JSON. Recommended JSON:

```json
{
  "source_url": "https://arxiv.org/search/...",
  "title": "Search | arXiv",
  "page_text": "visible text...",
  "links": [
    {"href": "https://arxiv.org/abs/2606.06033", "text": "RealDexUMI"}
  ]
}
```

Keep these exports in `/tmp`, `/private/tmp`, or `work/` test artifacts. Do not store full paper HTML or full extracted正文 in the knowledge base.

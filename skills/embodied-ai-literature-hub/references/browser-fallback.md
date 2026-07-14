# Browser Candidate Fallback

Use this after `search_arxiv.py` has exhausted its API retries, or when API search produces too small a candidate pool for a named method family. The search script waits and retries transient API failures, including HTTP `429`, up to 3 times per query before this fallback is needed.

## Principle

- Browser/web search is only for candidate discovery.
- Accepted evidence still requires locator-backed full text through `scripts/extract_arxiv_content.py`.
- Missing HTML triggers text-layer PDF extraction. Scan-only, unrecoverable, or low-quality papers stay metadata-only; do not run OCR.
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
   - Run `scripts/extract_arxiv_content.py --paper-id <id> --terms <topic terms> --ocr-mode never --include-full-text` and pass complete eligible text to `$embodied-ai-paper-reader`.

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

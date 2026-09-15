# Full-Text Fallback Contract

Use this reference whenever arXiv HTML is missing, incomplete, flat, or below the text-quality gate.

## Decision Chain

1. Request `https://arxiv.org/html/<id>` and parse LaTeXML sections.
2. Accept flat HTML only when it exceeds the minimum text threshold and preserves usable heading locators.
3. Otherwise recover markdown via the markdown tier: `fetch.py extract-arxiv-tex` defaults to the **arxiv2md** transport — a public REST API fetched with curl (`GET https://arxiv2md.org/api/markdown?url=<id>&remove_refs=false&remove_toc=false&remove_citations=false`, no credentials, 30 req/min per IP) returning section-aware markdown with `$...$` math and pipe tables. TeX-derived markdown is authoritative text, so `arxiv2md`/`tex-pandoc` extractions never need visual validation. Papers without arXiv HTML (older or PDF-only, roughly pre-2024-03) answer HTTP 400; treat that as "fall to the PDF tier", not as negative evidence.
   The alternative `s3-tex` transport (`fetch.py extract-arxiv-tex --transport s3-tex` + `fetch.py download-arxiv-source`, boto3 threaded zero-sleep fetch of `src/YYMM/<id>.tar.gz` + pypandoc) is **TODO**: the `s3://arxiv/` bucket is requester-pays, so it needs AWS credentials and bills download bandwidth per GB — pending account setup. Requires `pip install -e ".[s3,tex]"` plus a pandoc binary; missing dependencies skip the tier without failing the chain. Old-style IDs (pre-0704) have no S3 key.
4. Otherwise download/cache `https://arxiv.org/pdf/<id>.pdf` and extract every page with `pypdf`.
   The PDF downloader must honor the gateway's per-request timeout; a slow PDF stays `unavailable` for the current run instead of blocking the rest of a batch.
5. Measure page coverage, median non-space characters, replacement-character rate, and word-like character rate.
6. Run with `--ocr-mode never`. If the PDF lacks a usable text layer, mark it `unavailable`; scan-only papers are outside this project's scope.
7. Rank sections/pages by topic terms and preserve `section path ¶ paragraph`, `path ¶ line-N`, or `page N` locators.
8. For medium-quality text-layer PDF extraction, visually compare every cited page against the PDF before evidence settlement.

Run the gateway, not the individual extractors, during normal recovery:

```bash
python3 skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py \
  --paper-id 2402.10329 \
  --terms UMI,data,teleoperation,limitation \
  --ocr-mode never \
  --include-selected-text \
  --include-full-text \
  --output work/<run>/extraction-2402.10329.json
```

For casual human reading (not evidence work), the same gateway renders markdown directly —
`--terms` is optional, `.md` outputs imply `--format markdown`, and full text is always included:

```bash
python3 skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py 2402.10329 \
  --output paper.md          # or: pip install -e . && extract_arxiv 2402.10329 --output paper.md

# Insert the markdown tier automatically after HTML fails (HTML -> arxiv2md -> PDF):
python3 skills/embodied-ai-literature-hub/scripts/extract_arxiv_content.py 2402.10329 \
  --preferred-source auto --output paper.md
```

## Quality And Promotion

| Result | Candidate status | Evidence action |
|---|---|---|
| high-quality structured/flat HTML | `extracted` | Send complete text to the paper reader |
| high/medium arxiv2md or tex-pandoc Markdown | `extracted` | Send complete text to the paper reader; no visual validation needed |
| high-quality PDF text | `extracted` | Send every page to the paper reader |
| medium-quality PDF text | `extracted` | Visually validate cited pages before evidence projection |
| scan-only/OCR-required PDF | `unavailable` | Keep metadata candidate; do not run OCR or create evidence |
| download/parser failure | `unavailable` | Record attempts and limitation; do not treat as negative evidence |

Store this provenance under `evidence.extraction`:

```json
{
  "source_format": "pdf",
  "method": "pdf-text",
  "quality": "medium",
  "visual_validation": "passed",
  "visual_validation_pages": [3, 7]
}
```

TeX-derived markdown provenance uses `source_format: "tex"` with either
`method: "arxiv2md"` (REST API transport) or `method: "tex-pandoc"` (S3
tarball transport), and `visual_validation: "not-required"`; locators are
markdown section paths with line anchors (`§Path ¶ line-N`).

`$embodied-ai-paper-reader` rejects OCR, incomplete full text, low-quality text,
and medium-quality extraction whose visual validation is not recorded as passed.

## Failure Semantics

- HTML failure means “try the next tier (arxiv2md markdown, then PDF)”, not “paper has no evidence”.
- arxiv2md HTTP 400 (no arXiv HTML for the paper) means “fall to the PDF tier”, not “the paper lacks a relevant claim”.
- TeX-source (`s3-tex`) failure (`no-source`, no S3 key, missing AWS credentials or pandoc) means “fall back to HTML/PDF”, not “the paper lacks a relevant claim”.
- PDF text-layer failure means “full text was not recoverable in this run”, not “the paper lacks a relevant claim”.
- Abstracts may guide screening but cannot supply a locator-backed full-text event.
- Do not copy full PDFs or complete extracted text into `evidence/`; keep caches in `work/` or outside the repository and settle only paper notes and compact evidence records. (The one sanctioned full-text store is the local public paper pool outside the repo — see `knowledge.py pool-add-paper`.)

# Full-Text Fallback Contract

Use this reference whenever arXiv HTML is missing, incomplete, flat, or below the text-quality gate.

## Decision Chain

1. Request `https://arxiv.org/html/<id>` and parse LaTeXML sections.
2. Accept flat HTML only when it exceeds the minimum text threshold and preserves usable heading locators.
3. Otherwise download/cache `https://arxiv.org/pdf/<id>.pdf` and extract every page with `pypdf`.
   The PDF downloader must honor the gateway's per-request timeout; a slow PDF stays `unavailable` for the current run instead of blocking the rest of a batch.
4. Measure page coverage, median non-space characters, replacement-character rate, and word-like character rate.
5. Run with `--ocr-mode never`. If the PDF lacks a usable text layer, mark it `unavailable`; scan-only papers are outside this project's scope.
6. Rank sections/pages by topic terms and preserve `section path ¶ paragraph` or `page N` locators.
7. For medium-quality text-layer PDF extraction, visually compare every cited page against the PDF before evidence settlement.

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

## Quality And Promotion

| Result | Candidate status | Evidence action |
|---|---|---|
| high-quality structured/flat HTML | `extracted` | Send complete text to the paper reader |
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

`$embodied-ai-paper-reader` rejects OCR, incomplete full text, low-quality text,
and medium-quality extraction whose visual validation is not recorded as passed.

## Failure Semantics

- HTML failure means “try PDF”, not “paper has no evidence”.
- PDF text-layer failure means “full text was not recoverable in this run”, not “the paper lacks a relevant claim”.
- Abstracts may guide screening but cannot supply a locator-backed full-text event.
- Do not copy full PDFs or complete extracted text into `evidence/`; keep caches in `work/` or outside the repository and settle only paper notes and compact evidence records.

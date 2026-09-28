# Optional token meter

Minimal instrumentation from the token-optimization audit (§6.1). **Default off.**

## Enable

```bash
export EMBODIED_TOKEN_METER=1
python3 scripts/token_meter.py \
  --output work/<run>/token-meter.jsonl \
  --run-id literature-review-demo-20260928 \
  --stage reader.deep \
  --paper-id 2402.10329 \
  --file work/<run>/reading-packets/2402.10329.md \
  --prompt-chars 12000
```

Without the env flag the script exits 0 and writes nothing (unless `--force`).

## Schema (one JSON object per line)

| Field | Meaning |
|---|---|
| `run_id` / `stage` | e.g. `planner.persona`, `hub.coverage_decide`, `reader.deep`, `writer.zhihu` |
| `paper_id` / `round` | optional |
| `model` | actual model name when known |
| `prompt_chars` / `completion_chars` | local proxies |
| `prompt_tokens` / `completion_tokens` | from API usage when available |
| `files_loaded[]` | `{path, bytes}` — catches registry dumps (H2) and catalog loads (H5) |
| `included_full_text` | bool — catches full-text packet loads (H1) |
| `cache_hit` | prompt-cache hit when known |
| `ts` | UTC timestamp |

## Hooks (optional, non-blocking)

- Paper-reader: after opening a reading packet / extraction, log `stage=reader.*` and `included_full_text`.
- Writer: when loading `writing-brief.md` / `evidence-appendix.md`, log `stage=writer.*`.
- Hub coverage decisions: log `stage=hub.coverage_decide` with only `coverage-report.json` in `files_loaded` — never the full registry.

This helper does **not** wrap `Read` automatically; agents or thin wrappers call it explicitly. A fuller middleware can land in a follow-up PR.

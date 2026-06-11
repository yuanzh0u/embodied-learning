---
name: embodied-ai-query-planner
description: Generate structured paper-search query plans for embodied-AI topics. Use when the user asks for embodied AI paper query generation, arXiv query planning, topic expansion, web calibration, UMI/VLA/Sim2Real/retargeting/tactile query terms, or when another Skill needs a reproducible query plan before literature mining.
---

# Embodied AI Query Planner

## Purpose

Turn a Chinese or English embodied-AI topic into a structured query plan. This Skill plans searches; it does not accept papers as evidence, mine full text, or update topic cards.

Use it upstream of `$embodied-ai-literature-hub` whenever a literature run needs reproducible query strategy.

## Inputs

- Required: `topic`.
- Optional: `knowledge_id` such as `EA-DATA` or `EA-MODEL`.
- Optional: specialized family such as `umi`, `vla`, `sim2real`, `retargeting`, `tactile-force`, or `last-centimeter`.
- Optional: time range. The planner records it but does not filter query strings by date.
- Optional: dynamic suggestions from LLM/agent reasoning.
- Optional: calibration notes from live search.

## Workflow

1. Load local routing if available:
   - `knowledge/index.md`
   - `knowledge/embodied-ai/index.md`
   - relevant topic cards only.
2. Map the topic to `EA-*` IDs and specialized families.
3. Generate the deterministic baseline plan:

```bash
python skills/embodied-ai-query-planner/scripts/build_query_plan.py \
  --topic "UMI 数据可用性" \
  --family umi \
  --knowledge-id EA-DATA \
  --output /tmp/query-plan.json \
  --markdown-output /tmp/query-plan.md
```

4. If the topic needs associative expansion beyond the static taxonomy, create a dynamic suggestion file. See [dynamic-expansion.md](references/dynamic-expansion.md).
5. If the user requested fresh calibration, search arXiv pages, project pages, author pages, Reddit, and X/Twitter for current terms. Save only terms/query hints, not claims. See [web-calibration.md](references/web-calibration.md).
6. Re-run the script with `--dynamic-file` and/or `--calibration-file` to merge dynamic suggestions and calibrated terms.
7. Pass the JSON plan to `$embodied-ai-literature-hub` or `search_arxiv.py --query-file`.

## Output Contract

- `queries`: arXiv API-compatible query entries, preserving compatibility with `search_arxiv.py --query-file`.
- `arxiv_api_queries`: same entries, explicitly channel-labeled.
- `browser_fallback_queries`: web/browser search strings for candidate discovery when the API under-recovers.
- `web_calibration_queries`: search strings for fresh keyword calibration.
- `dynamic_suggestions`: LLM/agent-suggested query additions and adjacent families, separate from static taxonomy.
- `calibration_notes`: source and confidence notes, especially for social calibration.

Each query entry must include `label`, `tier`, `query`, and `why`.

## Rules

- Prefer wide recall plus strong downstream filtering.
- Keep static taxonomy, dynamic suggestions, and web calibration visibly separate.
- Do not hard-filter with `cat:` by default; include suggested categories as metadata.
- Treat Reddit and X/Twitter as low-confidence social calibration only.
- Do not use web or social content as accepted paper evidence.
- Keep topic taxonomy details in [topic-taxonomy.md](references/topic-taxonomy.md).

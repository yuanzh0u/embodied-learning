# Topic Expansion

Deprecated: `embodied-ai-literature-hub` no longer owns topic expansion or query taxonomy.

Use `$embodied-ai-query-planner` before running literature mining. The planner emits JSON with a top-level `queries` array that remains compatible with:

```bash
python skills/embodied-ai-literature-hub/scripts/search_arxiv.py --query-file /tmp/query-plan.json --start-date 2023-01-01 --end-date 2026-06-06
```

This file remains only as a redirect for older workflow references. Do not add new query families here.

# Query Plan Cache

Reuse prior plans for the same topic surface so dynamic / persona LLM steps are not repeated.

## Cache key

```
SHA-256( normalize(topic) + review_mode + normalize(time_range) + sorted(families) )
```

- `topic`: whitespace-collapsed, lowercased.
- `review_mode`: `rapid` | `scoping` | `systematic`.
- `time_range`: optional string (e.g. `近六个月`); empty is a distinct key.
- `family`: specialized families such as `umi`, `vla`, `tactile-force`; order does not matter.

Knowledge IDs are **not** part of the key (they are recoverable from topic/family mapping). If two runs intentionally need different knowledge overlays for the same topic key, invalidate or use a distinct `--cache-root`.

## Location

Default root: **`.cache/query-plans/`** (gitignored). Override with `--cache-root` or env `EMBODIED_QUERY_PLAN_CACHE`. Per-run copies may also live under `work/<run>/` after `--output` on `get`.

Layout:

```
.cache/query-plans/<key[:2]>/<key>/
  query-plan.json
  meta.json          # had_dynamic_llm, had_persona_llm, stored_at, …
```

## Workflow

1. Before dynamic/persona LLM work, probe the cache:

```bash
python3 skills/embodied-ai-query-planner/scripts/query_plan_cache.py get \
  --topic "触觉—力觉联合的动作条件世界模型" \
  --review-mode scoping \
  --time-range "近六个月" \
  --family tactile-force \
  --output work/<run>/query-plan.json \
  --json
```

2. **On hit** (`hit: true`):
   - Reuse the copied plan.
   - **Skip** dynamic-expansion LLM and persona-generation LLM.
   - Deterministic `build_query_plan.py` baseline is already inside the cached plan; do not re-spend LLM tokens regenerating the same expansions.
   - Persona **regeneration** via `suggest_persona_regeneration.py` remains allowed **only when coverage dimensions fail** (or evidence stance skew triggers the reading-phase path). That is an incremental correction, not a cache miss.

3. **On miss**:
   - Run deterministic `build_query_plan.py`.
   - Add dynamic / persona LLM files only when the skill says they are needed.
   - After a reviewed plan is finalized, store it:

```bash
python3 skills/embodied-ai-query-planner/scripts/query_plan_cache.py put \
  --topic "…" --review-mode scoping --time-range "近六个月" --family tactile-force \
  --plan work/<run>/query-plan.json \
  --had-dynamic --had-persona
```

4. Invalidate when taxonomy or intentional strategy changes:

```bash
python3 skills/embodied-ai-query-planner/scripts/query_plan_cache.py invalidate \
  --topic "…" --review-mode scoping --time-range "近六个月" --family tactile-force
```

## Rules

- Cache stores **plans**, not paper evidence. Hitting the cache never skips coverage gates.
- Do not treat a cached plan as fresh web calibration; re-run calibration only when the user asks for live term refresh, then `put` a new entry (or invalidate first).
- Round-capped persona regeneration (default cap 2) is orthogonal: cache hit skips the *initial* persona LLM, not gap-filling regeneration.

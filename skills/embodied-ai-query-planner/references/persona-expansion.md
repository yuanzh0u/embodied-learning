# Persona Expansion

Persona expansion is the perspective layer between the static taxonomy and dynamic expansion. Inspired by STORM's multi-perspective question asking, it generates 3–5 complementary research personas (plus one mandatory safety-net persona) whose domain priors widen query coverage in directions that keyword combinations miss.

Personas widen recall for this run; they never replace the static taxonomy, never relax coverage gates, and never become paper evidence.

## When To Use

- The topic is "pitfall-oriented" or failure-focused (坑、问题、局限、失败), where limit/gap-directed perspectives matter more than breadth.
- Static taxonomy mapping is plausible but the topic benefits from multiple expert viewpoints (e.g. a deployment engineer and a data-quality auditor would ask different questions about the same pipeline).
- A prior run's stance distribution was skewed toward `support` and you want counter-evidence pressure at query-planning time.
- Coverage/saturation rounds exposed a dimension gap that static tier keywords have trouble filling.

## Workflow

Three steps; only step 2 involves an LLM, and its output is a reviewable file.

### Step 1: Extract local reference context (deterministic)

```bash
python skills/embodied-ai-query-planner/scripts/gen_persona_context.py \
  --topic "近半年触觉数据联合训练的坑" \
  --knowledge-id EA-SENSOR \
  --knowledge-id EA-DATA \
  --output work/<run>/persona-context.json
```

The extractor pulls key judgments from matched topic cards and related runs from the literature-review catalog. `--knowledge-id` matching is exact; without it, the topic is fuzzy-matched against card aliases/tags. No network, no LLM, no timestamps — same inputs always produce identical output. This local evidence replaces STORM's Wikipedia-table-of-contents inspiration source and keeps personas calibrated to the project's own knowledge.

### Step 2: Generate the persona file (LLM, one-shot)

Read `persona-context.json` and write a persona file with:

- 3–5 complementary personas, each with a distinct `primary_dimensions` focus; avoid homogeneous perspectives (three "method researchers" add nothing over one).
- Exactly one default safety-net persona (`P-BASIC-FACTS`, focus: broadly covering the basic facts) — the analogue of STORM's default "Basic fact writer". It guarantees baseline coverage even if the other personas skew.
- 2–3 queries per persona. Every persona entry's `inspired_by` MUST point at a real item from the reference context (a key judgment or a related run), never invented.
- Persona queries should stay within roughly 30% of the total query budget.
- Human review before commit: the persona file is the audit artifact that isolates LLM non-reproducibility. Once committed, plan generation stays deterministic.

### Step 3: Merge into the plan

```bash
python skills/embodied-ai-query-planner/scripts/build_query_plan.py \
  --topic "近半年触觉数据联合训练的坑" \
  --knowledge-id EA-SENSOR \
  --knowledge-id EA-DATA \
  --persona-file work/<run>/personas.json \
  --output work/<run>/query-plan.json
```

Persona entries merge after dynamic suggestions and before calibration, enter the same dedupe and `--max-queries` budget as everything else, and each query carries `persona_id`, `persona_source`, and `coverage_dimension`.

## Persona File Shape

```json
{
  "topic": "近半年触觉数据联合训练的坑",
  "generated_by": "llm",
  "reference_context_file": "work/<run>/persona-context.json",
  "personas": [
    {
      "id": "P-FAILURE-HUNTER",
      "name": "失败模式猎手",
      "focus": "专挖联合训练的失败案例：负迁移、模态污染、训练不稳定",
      "primary_dimensions": ["limits-and-counterevidence"],
      "inspired_by": ["EA-SENSOR: 无约束触觉注入污染视觉 dynamics model"]
    },
    {
      "id": "P-BASIC-FACTS",
      "name": "基础事实覆盖者",
      "focus": "广泛覆盖主题基础事实",
      "primary_dimensions": ["direct-topic"],
      "inspired_by": ["STORM 默认角色安全网设计"]
    }
  ],
  "queries": [
    {
      "label": "persona-failure-negative-transfer",
      "tier": "persona-limit",
      "query": "all:\"negative transfer\" AND all:tactile AND all:robot",
      "why": "失败模式猎手：直接搜索负迁移证据",
      "persona": "P-FAILURE-HUNTER"
    }
  ]
}
```

### Field Constraints

| Field | Rule |
|---|---|
| `personas[].id` | Unique across all merged persona files; duplicates are dropped with a note. |
| `personas[].primary_dimensions` | Subset of the six coverage dimensions; drives query tier/dimension inference. |
| `queries[].persona` | Must reference a known persona id; unknown ids are skipped with a note. |
| `queries[].tier` | Use the convention names below (or omit and let the dimension decide). |
| `queries[].coverage_dimension` | Optional explicit override; takes precedence over tier and persona defaults. |
| `queries[].query` | arXiv API syntax, same as all other plan queries. |

## Tier Naming Convention

Tier names must come from this table. They are chosen so `coverage_group()`'s substring fallback ALSO classifies them correctly — with one documented exception.

| Tier | Coverage dimension | `coverage_group()` substring also works? |
|---|---|---|
| `persona-direct` | direct-topic | **No** — "direct" is not a coverage_group keyword; only the explicit table routes it |
| `persona-method` | mechanisms-and-interfaces | Yes ("method") |
| `persona-limit` | limits-and-counterevidence | Yes ("limit") |
| `persona-eval` | evaluation-and-validation | Yes ("eval") |
| `persona-deploy` | deployment-and-operations | Yes ("deploy") |
| `persona-adjacent` | adjacent-and-transfer | Yes (fallback default) |

**Trap**: semantically-natural names like `persona-mechanism` or `persona-deployment` do NOT match coverage_group() keywords (`method`, `deploy`) and would silently misroute to adjacent-and-transfer. Use the table names. When `coverage_dimension` is given explicitly it always wins, so explicit dimensions are the safest choice for unusual cases.

Dimension resolution priority for each query: explicit `coverage_dimension` > query `tier` (convention table) > persona `primary_dimensions[0]` > `coverage_group()` fallback.

## Saturation-Triggered Regeneration

Saturation and dimension gaps are correction signals, not just stop signals. After each literature-hub retrieval round:

```bash
python skills/embodied-ai-query-planner/scripts/suggest_persona_regeneration.py \
  --plan work/<run>/query-plan.json \
  --coverage-report work/<run>/coverage-report.json \
  --output work/<run>/personas-round2.json
```

- Retrieval phase: any coverage dimension with `passed=false` or `unique_candidates < minimum_unique_candidates` requests a targeted gap-filling persona.
- Reading phase (pass `--evidence work/<run>/evidence.jsonl`): if accepted-evidence `limit`+`gap` stance share drops below 20%, request a counter-evidence seeker persona.
- Each regeneration output records `regeneration_round` and `triggered_by` for the audit chain; default round cap is 2 to prevent loops.
- Regenerated persona files re-enter the plan only through `--persona-file` after review — they never bypass coverage gates.

## Promotion Rule

Keep persona queries separate until they prove useful. Promote a pattern into `query_taxonomy.py` only when it repeatedly improves recall across runs and downstream paper-level evidence confirms the adjacent papers contain topic-relevant discussion. Persona queries that never add unique candidates should be retired in the next run, not carried forward.

## Relationship To Other Layers

| Layer | Input | Reproducible | Evidence role |
|---|---|---|---|
| Static taxonomy | `query_taxonomy.py` | Yes | Baseline coverage floor |
| Persona expansion | persona file (LLM, reviewed) | File-level (committed) | Query-planning only |
| Dynamic expansion | dynamic file (LLM/agent) | File-level | Query-planning only |
| Web calibration | calibration file (live search) | No | Term freshness only |

All four layers stay visibly separate in the plan output (`queries[].source_type`, `personas`/`dynamic_suggestions`/`calibration_notes` sections).

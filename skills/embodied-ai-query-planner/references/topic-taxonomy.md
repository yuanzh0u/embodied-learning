---
title: Embodied AI query taxonomy
version: v1
source:
  - docs/prd/embodied-ai-query-planner-skill.md
  - knowledge/embodied-ai/index.md
  - knowledge/embodied-ai/*.md topic cards
---

# Topic Taxonomy

This reference explains the deterministic taxonomy in
`scripts/query_taxonomy.py`. It is the static baseline for query planning; live
web calibration may add terms later, but should not replace these stable keys.

## Query Entry Schema

Each topic or family plan exposes a `queries` list. Every query entry has:

- `label`: stable identifier for logs, query-file output, and deduplication.
- `tier`: reason class for the query, such as `core`, `named-method`,
  `limitation`, `transfer`, `evaluation`, or `deployment`.
- `query`: arXiv API-compatible query text using simple `all:term`, quoted
  phrases, `AND`, `OR`, and parentheses.
- `why`: human-readable rationale for why the query belongs in the plan.
- `suggested_categories`: optional metadata only. These are not hard `cat:`
  filters and should be applied manually only when recall is too noisy.

The existing literature-hub search script reads only `label` and `query`, so
the extra fields are safe metadata for downstream review.

Family plans may also expose `browser_fallback_queries`. These are not arXiv
API strings. They are web/browser search strings, usually with `site:arxiv.org`
syntax, used only when API search is rate-limited or under-recovers. Keep
family-specific named methods, aliases, and limitation language here rather
than in the generic fallback path.

## Tier Semantics

- `core`: direct vocabulary for the topic.
- `named-method` or `named-dataset`: known model, method, dataset, or lineage.
- `named-variant`: specific derivative systems inside a family.
- `quality`: data quality, demonstration quality, or acceptance criteria.
- `collection-setting`: lab, in-the-wild, egocentric, or natural-scene capture.
- `tracking` or `device-language`: hardware wording likely to appear outside
  canonical method names.
- `representation` or `policy-interface`: action spaces, adapters, tokens, or
  interfaces that mediate transfer.
- `validation`, `benchmark`, `evaluation`, or `sim-real`: ways claims are
  tested, including open-loop, closed-loop, simulation, and real-robot checks.
- `limitation` or `system-limitation`: explicit failure, mismatch, latency,
  usability, contact, or deployment-risk language.
- `deployment`, `production`, `production-quality`, `recovery`, or
  `business-adjacent`: industrial rollout, reliability, cycle time, yield,
  recovery, acceptance testing, and ROI-adjacent surfaces.

## EA Topic Coverage

| Key | Knowledge route | Query intent |
|---|---|---|
| `EA-DATA` | data collection and data quality | Demonstration data, in-the-wild collection, dataset curation, and trajectory quality. |
| `EA-SENSOR` | sensors and multimodal perception | RGB/3D/tactile/force observability, sensor fusion, occlusion, and contact cues. |
| `EA-HARDWARE` | collection hardware and device routes | Teleoperation devices, SLAM/tracking, ARKit-like routes, handheld grippers, and collection cost. |
| `EA-XEMBODIMENT` | cross-embodiment transfer | Retargeting, human-to-robot transfer, action representations, dexterous hands, and grippers. |
| `EA-MODEL` | models and pretraining | VLA, robot foundation models, fine-tuning, action tokenization, and transfer value. |
| `EA-EVAL` | evaluation systems and world models | Open-loop vs closed-loop evaluation, benchmarks, world models, and sim-real correlation. |
| `EA-BIZ` | commercialization and deployment | Industrial deployment, reliability, cycle time, failure recovery, and ROI-adjacent constraints. |

## V1 Family Coverage

| Family key | Routes to | Coverage |
|---|---|---|
| `umi` | `EA-DATA`, `EA-HARDWARE`, `EA-XEMBODIMENT` | UMI exact lineage, acronym search, UMI-3D/DexUMI/RealDexUMI variants, force extensions, handheld gripper language, and usability limits. |
| `droid-ego4d` | `EA-DATA`, `EA-HARDWARE`, `EA-MODEL` | DROID robot data, Ego4D/egocentric video, in-the-wild demonstrations, and cross-dataset data mixtures. |
| `teleoperation-demo-quality` | `EA-DATA`, `EA-HARDWARE`, `EA-EVAL` | Teleoperation for imitation learning, demonstration quality, operator burden, latency, and action interfaces. |
| `vla` | `EA-MODEL`, `EA-DATA`, `EA-XEMBODIMENT`, `EA-EVAL` | Vision-language-action models, RT-X/Octo/OpenVLA-style lineages, fine-tuning, data mixtures, and negative transfer. |
| `sim2real` | `EA-MODEL`, `EA-EVAL`, `EA-DATA` | Sim-to-real transfer, real-robot validation, synthetic data, domain randomization, and sim-real correlation. |
| `world-model` | `EA-EVAL`, `EA-MODEL` | Robot world models, video prediction, planning, contact realism, and long-horizon consistency. |
| `retargeting` | `EA-XEMBODIMENT`, `EA-HARDWARE`, `EA-SENSOR` | Human-to-robot mapping, dexterous hand transfer, gripper abstraction, and morphology gaps. |
| `tactile-force` | `EA-SENSOR`, `EA-DATA`, `EA-BIZ` | Tactile sensing, force/torque, slip detection, contact-rich manipulation, and multimodal fusion. |
| `last-centimeter` | `EA-BIZ`, `EA-SENSOR`, `EA-EVAL` | Final approach, visual servoing, force-controlled insertion, recovery, and fixture design. |
| `industrial-deployment` | `EA-BIZ`, `EA-EVAL`, `EA-SENSOR` | Deployment, reliability, cycle time, yield, acceptance testing, and ROI-adjacent search. |

## Deterministic Key Inference

Use `normalize_key(value)` when a caller has one exact user-provided key or
alias. It returns a canonical key when possible and otherwise returns a slug.

Use `infer_keys(topic_text)` for free-form topic text. It scans canonical keys
and aliases, applies explicit associative expansions, then returns matching keys
in stable taxonomy order:

1. All seven `EA-*` topic IDs.
2. All ten specialized family keys.

Alias matching is deliberately simple. It handles English terms such as
`vision-language-action`, `sim-to-real`, and `hand-held gripper`, plus common
Chinese route terms from the local topic cards. It does not perform semantic
expansion, ranking, web lookup, or evidence judgment.

Associative expansion is also deterministic. For example, topics that combine
simulation/synthetic data with limitation, failure, gap, 局限, 限制, or 失效
also include `world-model`, because world-model papers often discuss real-world
data needs and simulated-data failure modes even when their metadata does not
contain simulation keywords.

Topics that combine VLA / vision-language-action / robot foundation model with
data pyramid, data hierarchy, scaling, 数据金字塔, 数据层级, or 数据混合 also include
`droid-ego4d` and `sim2real`. The planner does this because VLA data-pyramid
questions usually need real robot data, human/egocentric video, and
synthetic/simulation data layers, even when papers do not use "pyramid" in
metadata.

## arXiv Compatibility

The taxonomy avoids hard `cat:` filtering because embodied-AI papers often
cross robotics, machine learning, computer vision, systems, and human-computer
interaction categories. Suggested categories are review hints only.

Queries are intentionally conservative API strings:

- fielded terms: `all:robot`, `all:tactile`
- quoted phrases: `all:"robot manipulation"`
- Boolean composition: `AND`, `OR`, and parentheses

Do not put Browser fallback syntax, site search, author-page instructions,
Reddit/X terms, or citation chasing instructions into the arXiv API `queries`.
Family-scoped `browser_fallback_queries` are allowed in this module because
they are part of the deterministic query plan output contract. Keep them
separated from `queries` and never pass them to the arXiv API.

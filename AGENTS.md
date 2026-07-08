# Agent Instructions

This repository is a research knowledge base. Optimize for context efficiency and traceability.

## Loading Order

1. Start with [knowledge/index.md](knowledge/index.md).
2. Load the domain index that matches the task:
   - [knowledge/embodied-ai/index.md](knowledge/embodied-ai/index.md)
   - [knowledge/error-governance/index.md](knowledge/error-governance/index.md)
3. Load only the topic cards listed in `load_when` or `query_routes`.
4. Open raw source documents only when exact wording, detailed evidence, or references are needed.

## Context Rules

- Prefer topic cards over raw long-form materials.
- Preserve frontmatter fields when editing topic cards.
- Add new material through [knowledge/ingestion-guide.md](knowledge/ingestion-guide.md).
- Keep every synthesized claim traceable to a `source` entry or mark it as an inference.
- Use stable IDs such as `EA-DATA`, `EA-EVAL`, and `ERR-PATTERN` when referring to knowledge units.

## Research Workflow

- When researching a topic, first use the project skill `embodied-ai-literature-review`; it orchestrates `embodied-ai-query-planner` and `embodied-ai-literature-hub` for search planning, evidence extraction, and final review drafting.

## Source Of Truth

- `evidence/` is the source of truth for paper-level evidence and finished literature reviews (versioned, append-only per run).
- Retired raw documents remain traceable through their registered git archives in [knowledge/sources.md](knowledge/sources.md) (`git show 081e898:<file>`).
- Topic cards are compressed working memory for agents.
- The master index is the routing layer.
- Candidates and intermediate artifacts live in `work/` (gitignored scratch); accepted assets live in `evidence/`.

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

## Source Of Truth

- Raw source documents are the detailed source of truth.
- Topic cards are compressed working memory for agents.
- The master index is the routing layer.

---
name: embodied-ai-review-writer
description: Write or rewrite publication-ready Chinese embodied-AI literature content from a formal-ready brief and a potentially large evidence reservoir. Use for scientific research memos, 知乎专家解释稿, 小红书洞察帖, full three-style bundles, or when articles are traceable but shallow, packet-like, repetitive, under-cited, or not audience-specific.
---

# Embodied AI Review Writer

## Purpose

Transform a validated `writing-brief.md` into genuinely different reader-facing articles. Keep research provenance intact without exposing audit machinery in the prose. This Skill is the editorial layer after `$embodied-ai-literature-review`; it does not search, promote candidates, or decide whether evidence is accepted.

## Required inputs

- `writing-brief.md` from `$embodied-ai-literature-review`.
- The matching `evidence-appendix.md` and accepted evidence JSONL.
- Requested style: `scientific-memo`, `zhihu-explainer`, `xiaohongshu-post`, or all three.
- Optional audience, publication goal, length, voice, and examples. When absent, use the defaults in the selected style reference.

If no validated brief exists, stop writing and invoke `$embodied-ai-literature-review` first. Candidate lists and raw search results are not writing evidence.
If the brief says `Writing readiness: preliminary` or its coverage gate is blocked, return it to research instead of writing formal articles.

## Load only the selected style guidance

- Scientific research memo: read [scientific-memo.md](references/scientific-memo.md).
- Zhihu expert explainer: read [zhihu-explainer.md](references/zhihu-explainer.md).
- Xiaohongshu insight post: read [xiaohongshu-post.md](references/xiaohongshu-post.md).
- Always read [editorial-quality-rubric.md](references/editorial-quality-rubric.md) and [citation-projection.md](references/citation-projection.md).

For a full bundle, read all three style references, but plan and draft each article independently from the brief. Never derive Zhihu or Xiaohongshu prose by shortening the scientific memo.

## Workflow

1. **Interrogate the evidence reservoir.** Extract one central thesis, 3-5 claim clusters, the strongest counterevidence, mandatory caveats, and the evidence boundary. Separate field size, discovered candidates, extracted full text, accepted papers, and papers selected for each article.
2. **Make three independent editorial plans.** For each style choose the reader question, opening, argument order, examples, excluded details, ending, and representative source subset. Do not reuse an outline or simply cite every accepted paper.
3. **Draft reader-first prose.** Write in natural Chinese. Translate and synthesize English evidence claims; never paste or mechanically translate event claims one by one. Use paper links in body prose where the selected style permits them.
4. **Project provenance.** Keep reader-facing citations compact and put event-level mapping in `trace-map.json` plus `evidence-appendix.md`. Follow [citation-projection.md](references/citation-projection.md).
5. **Edit twice.** First edit for argument, counterevidence, and overclaiming. Second edit for voice, rhythm, jargon, repetition, and platform fit.
6. **Run deterministic gates.** Build the trace map, then audit the three outputs:

```bash
python3 skills/embodied-ai-review-writer/scripts/build_trace_map.py \
  --evidence-jsonl <run>/evidence.jsonl \
  --article <run>/scientific-memo_keyan.md \
  --article <run>/zhihu-explainer_zhihu.md \
  --article <run>/xiaohongshu-post_xiaohongshu.md \
  --output <run>/trace-map.json

python3 skills/embodied-ai-review-writer/scripts/audit_article_quality.py \
  --memo <run>/scientific-memo_keyan.md \
  --zhihu <run>/zhihu-explainer_zhihu.md \
  --xiaohongshu <run>/xiaohongshu-post_xiaohongshu.md
```

7. **Use the existing evidence gates.** Run `scripts/audit_citations.py` and `scripts/check_run_bundle.py` before settlement. Editorial gates complement evidence gates; neither substitutes for the other.

## Migrating an existing three-style bundle

When a paper-reader migration replaces an old evidence set, preserve mature prose only where its cited papers remain accepted. Drop whole unsupported prose blocks, add manually authored replacement arguments from the new brief, rebuild compact references, and regenerate the trace map. The helper below performs the mechanical parts; `article-updates.json` remains a manually written editorial input, not a claim generator:

```bash
python3 skills/embodied-ai-review-writer/scripts/migrate_reader_backed_articles.py \
  --draft-root work/paper-reader-migration/draft-runs \
  --source-root evidence \
  --updates work/paper-reader-migration/article-updates.json
```

After migration, read all three articles again. Removing an unreadable citation is not enough if its unsupported claim remains in plain text. Run `build_trace_map.py`, `audit_article_quality.py`, and `audit_citations.py` on every migrated run.

## Hard rules

- Treat the brief, claim map, stance buckets, and evidence appendix as inputs, never as article body.
- Give each article one explicit central thesis and an evidence-bounded conclusion.
- Preserve `conditional`, `limit`, and `gap` evidence as visible boundaries; do not manufacture consensus.
- Keep event IDs out of body prose. Use arXiv paper links for readers and the trace map for audit.
- Do not leak workflow language such as “formal-ready”, “stance labels”, “output type”, “strong hook is allowed”, or instructions addressed to the writer.
- Do not use topic-agnostic filler or the same opening, paragraph, or conclusion in two styles.
- Do not present untranslated English evidence claims as Chinese articles.
- Use the accepted evidence as a reservoir: scientific memo cites at least 5 representative papers, Zhihu 3-12, and Xiaohongshu 3-5. More evidence should deepen synthesis and counterevidence, not inflate every bibliography.
- Never state or imply that the selected article references equal all papers in the field.
- Keep exact deliverable filenames when writing a literature-review bundle:
  - `scientific-memo_keyan.md`
  - `zhihu-explainer_zhihu.md`
  - `xiaohongshu-post_xiaohongshu.md`

## Completion standard

Finish only when the evidence gates pass, the editorial audit passes, and a manual read confirms that the three outputs sound like three publications for three audiences rather than three views of one database.

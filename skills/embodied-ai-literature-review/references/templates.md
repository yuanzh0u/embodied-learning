# Briefing and Writer Handoff

This Skill does not own reader-facing prose templates. It produces validated writing inputs and hands them to `$embodied-ai-review-writer`.

## Briefing bundle

- `review-packet.md`: audit view of accepted events, stance, confidence, authors, source gaps, and coverage.
- `writing-brief.md`: writer-facing thesis candidates, evidence clusters, mandatory caveats, and paper/event citation pairs.
- `evidence-appendix.md`: complete event-level provenance with locator and short quote.
- Optional consolidated `evidence.jsonl`: the self-contained working evidence set for a synthesis run.
- `candidate-registry.json`: deduplicated discovery and screening history.
- `coverage-report.json`: size, dimension, full-text, accepted-evidence, and saturation checks.

## Handoff contract

Pass the following to `$embodied-ai-review-writer`:

1. `writing-brief.md`
2. `evidence-appendix.md`
3. every accepted evidence JSONL used by the run
4. requested style(s), audience constraints, publication goal, and length if supplied
5. review mode and the passed coverage report

The writer then loads its style-specific reference:

- scientific memo → `embodied-ai-review-writer/references/scientific-memo.md`
- Zhihu explainer → `embodied-ai-review-writer/references/zhihu-explainer.md`
- Xiaohongshu post → `embodied-ai-review-writer/references/xiaohongshu-post.md`

## Non-deliverables

The following remain internal inputs and must never be renamed or presented as final articles:

- Claim Map tables
- stance-bucket lists
- one-event-per-line summaries
- `*.scaffold.md`
- review packet prose

## Gap language passed to the writer

- Use “本轮证据尚未覆盖……” when the run did not inspect enough sources.
- Use “已有论文明确指出……” only when an accepted event has `stance: gap`.
- Use “可以推断……” only with contributing evidence and a falsifier.

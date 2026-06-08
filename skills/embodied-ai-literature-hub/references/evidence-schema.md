# Evidence Schema

Store discussion events as JSONL. One line is one author-attributed stance event about one topic.

## Required fields

```json
{
  "event_id": "EA-DATA-2026-0001",
  "topic_id": "EA-DATA",
  "topic": "UMI data usability",
  "paper": {
    "arxiv_id": "2402.10329",
    "title": "Paper title",
    "published": "2024-02-15",
    "url": "https://arxiv.org/abs/2402.10329"
  },
  "authors": [
    {
      "name": "Author Name",
      "author_key": "author-name",
      "role": "paper-author"
    }
  ],
  "claim": "Precise claim in the agent's words.",
  "stance": "support",
  "evidence": {
    "summary": "Paraphrased evidence.",
    "locator": "page 3, section Method",
    "short_quote": "Optional short quote only.",
    "evidence_type": "experiment"
  },
  "confidence": "direct",
  "core_citations": [
    {
      "title": "Cited paper title",
      "arxiv_id": "2301.00000",
      "reason": "This citation carries the key evidence for the claim."
    }
  ],
  "notes": "Optional uncertainty or extraction caveat."
}
```

## Allowed values

`stance`:

- `support`: paper argues the topic/approach is useful or feasible.
- `limit`: paper highlights weakness, cost, failure mode, negative result, or unsuitable condition.
- `conditional`: paper supports use only under explicit conditions.
- `gap`: paper identifies an unresolved problem, missing benchmark, or open question.

`confidence`:

- `direct`: the paper's authors directly make the claim.
- `citation-supported`: the paper uses another work as support for the claim.
- `inference`: the agent synthesized the claim from evidence; mark this clearly.

## Author keys

- Lowercase ASCII where possible.
- Remove punctuation and collapse whitespace to hyphens.
- Do not merge same-name authors unless there is stronger evidence.

## Promotion rule

A candidate paper enters the evidence layer only if it yields at least one event with a topic-relevant claim and a locator. Metadata-only relevance is not enough.

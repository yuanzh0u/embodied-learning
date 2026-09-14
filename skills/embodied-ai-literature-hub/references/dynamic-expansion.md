# Dynamic Expansion

Dynamic expansion is the LLM/agent layer between the static taxonomy and web calibration.

Use it when the topic uses a new metaphor, product term, or research framing that is not yet encoded in `query_taxonomy.py`. Dynamic suggestions widen recall for this run, but they do not replace the static taxonomy and they are not paper evidence.

## When To Use

- The topic contains an overloaded metaphor such as data pyramid, last centimeter, data flywheel, or foundation-model gap.
- Static mapping is plausible but obviously misses adjacent paper families.
- The user explicitly asks for broader associative query generation.
- A previous arXiv smoke test shows a useful adjacent family that should be tried before permanent taxonomy promotion.

## Suggestion File Shape

```json
{
  "sources": [
    {
      "source": "llm",
      "confidence": "medium",
      "notes": "Agent inferred that VLA data-pyramid questions need human-video and synthetic-data layers."
    }
  ],
  "knowledge_ids": ["EA-DATA", "EA-MODEL", "EA-EVAL"],
  "families": ["droid-ego4d", "sim2real"],
  "queries": [
    {
      "label": "dynamic-vla-human-video-layer",
      "tier": "dynamic-association",
      "query": "all:\"human video\" AND all:\"robot learning\"",
      "why": "Human video can be an upper layer in a VLA data pyramid even when papers do not say data pyramid.",
      "source": "llm",
      "confidence": "medium"
    }
  ],
  "browser_fallback_queries": [
    {
      "label": "dynamic-vla-data-pyramid-browser",
      "query": "\"VLA\" \"data pyramid\" robot learning",
      "why": "Check whether this metaphor appears outside arXiv metadata.",
      "source": "llm",
      "confidence": "medium"
    }
  ],
  "web_calibration_queries": [
    {
      "label": "dynamic-vla-data-pyramid-web",
      "query": "\"vision-language-action\" \"data mixture\"",
      "why": "Calibrate the wording for VLA data-layer discussions.",
      "source": "llm",
      "confidence": "medium"
    }
  ]
}
```

Run:

```bash
python skills/embodied-ai-query-planner/scripts/build_query_plan.py \
  --topic "VLA的数据金字塔" \
  --dynamic-file /tmp/dynamic-vla-data-pyramid.json \
  --output /tmp/query-plan.json
```

## Promotion Rule

Keep dynamic suggestions separate until they prove useful. Promote a pattern into `query_taxonomy.py` only when it repeatedly improves recall and downstream HTML evidence confirms that the adjacent papers contain topic-relevant discussion.

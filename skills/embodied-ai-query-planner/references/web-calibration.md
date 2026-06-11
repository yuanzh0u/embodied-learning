# Web Calibration

Use live search only to improve query wording. Do not promote web, Reddit, or X/Twitter content to literature evidence.

## Source Roles

| Source | Role | Confidence |
|---|---|---|
| arXiv abs/html/search | Find paper vocabulary, IDs, method names, and author spellings | high |
| Project pages | Confirm method names, dataset names, and released variants | medium |
| Author/lab pages | Confirm follow-up names and author-specific terminology | medium |
| Reddit | Discover community aliases and pain points | low |
| X/Twitter | Discover fresh aliases, author announcements, and variant names | low |

## Calibration File Shape

```json
{
  "sources": [
    {
      "source": "x-twitter",
      "url": "https://x.com/example/status/...",
      "confidence": "low",
      "notes": "Researcher thread uses the alias RealDexUMI."
    }
  ],
  "terms": [
    {
      "term": "RealDexUMI",
      "source": "x-twitter",
      "confidence": "low",
      "why": "Fresh alias for a UMI-family dexterous data collection method."
    }
  ],
  "queries": [
    {
      "label": "calibration-realdexumi",
      "query": "all:RealDexUMI OR all:\"RealDex UMI\"",
      "source": "x-twitter",
      "confidence": "low",
      "why": "Search arXiv for the social alias before treating it as a candidate family term."
    }
  ]
}
```

## Rules

- Keep calibration terms traceable to source type.
- Mark Reddit and X/Twitter as `low` confidence.
- Use calibrated terms to search arXiv; do not cite calibration sources as evidence.
- If live search fails, generate the offline baseline plan and add a calibration note.

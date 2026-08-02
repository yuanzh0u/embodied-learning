# Xiaohongshu Insight Post

Use this style for a broad but intelligent audience. Deliver one evidence-grounded surprise in a platform-native, compact form.

## Default shape

- Chinese body length: roughly 500-1,000 Chinese characters, excluding links.
- One cover-ready title and one specific hook.
- Three to five insight cards; each contains one idea, not a compressed paragraph.
- One visible caveat and one compact source note.
- Optional 3-5 relevant hashtags only when the user wants a publish-ready post.

## Recommended form

```md
# <具体、可验证、不过度夸张的标题>

<1-2 句钩子：直接给最强发现和为什么值得关心。>

💡 <洞察 1：一句结论 + 一句解释或场景>（[论文短名](arXiv URL)）

💡 <洞察 2>（[论文短名](arXiv URL)）

💡 <洞察 3-5>

⚠️ <一句明确边界：什么场景下不能外推。>

📚 依据：<3-5 篇代表论文或“完整证据见 appendix”>。
```

## Voice

- Use short paragraphs, concrete nouns, and strong but bounded verbs.
- Prefer a work scene, robot failure, or decision consequence over abstract taxonomy.
- Use emoji as navigation, not decoration.
- Keep Markdown headings such as `## Hook` and internal labels such as `stance` out of the final post.
- Bold labels and the prescribed `💡`/`⚠️`/`📚` markers are platform grammar, not AI residue. Keep them when they improve scanning.
- Hooks may dramatize a supported consequence, but may not invent a field visit, conversation, personal test, customer, or failure episode.
- Compress qualifications into one visible boundary rather than deleting them. Strong wording must remain falsifiable by the cited evidence.

## Citation surface

- Link only the 3-5 papers needed for visible claims.
- Do not print event IDs, confidence labels, or a full bibliography.
- Keep complete provenance in `trace-map.json` and `evidence-appendix.md`.

## Reject the draft when

- The hook is “这个话题不能只看一个结论” or another topic-agnostic sentence.
- Insights are the first five evidence events rather than an editorial selection.
- English claim fragments, ellipsis truncation, or workflow instructions appear.
- References or audit metadata take more space than the post.

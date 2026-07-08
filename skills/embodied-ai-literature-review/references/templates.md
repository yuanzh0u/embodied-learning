# Review Templates

Use these templates when drafting a Chinese embodied-AI literature review or related-work section. The script emits the writing inputs (`review-packet.md` + `writing-brief.md` + `evidence-appendix.md`); **the agent writes the deliverables** in the review project folder under `work/`:

- `scientific-memo_keyan.md`
- `zhihu-explainer_zhihu.md`
- `xiaohongshu-post_xiaohongshu.md`

Link rules for all formal styles (see review-contract.md "Citation and link contract"):

- **Body citations are arXiv paper links**: `[SIEVE](https://arxiv.org/abs/2607.06442)` — 读者在阅读综述时一次点击即达论文。正文不放 `evidence-appendix.md#...` 事件锚点,也不放裸 event ID。
- Event-level provenance lives in `## References` and the appendix: each reference line pairs the paper link with its event anchors, so 溯源不丢、正文不乱。
- **Reference/appendix link targets are relative to the article's own folder.** The appendix sits next to the articles, so the target is always exactly `evidence-appendix.md#<anchor>` — never an invented subdirectory (a real run once linked into a nonexistent `review-bundle/`, producing six dead links in an otherwise good article).
- Only cite papers covered by the loaded evidence set — the audit rejects citations outside it.
- Before settling: `python3 scripts/audit_citations.py --article <each> --appendix evidence-appendix.md --evidence-jsonl <each>` must pass.

## What a deliverable is NOT

A draft with any of these is a packet render, not an article — rewrite it:

- Claim-map tables as body text; one-event-per-line or one-event-per-paragraph enumerations.
- Stance buckets (`### 共识/正向证据` lists) presented as the synthesis.
- The three styles sharing the same canned sentences or differing only in section order.
- Topic-agnostic filler ("不能只看一个漂亮结论""真正值钱的信息藏在证据条件里").

## Scientific memo skeleton (thesis-first)

The proven shape: 中心论点 → 派生矛盾 → 可操作框架 → 最短结论. Each derived tension is a **prose subsection** that names the tension, walks the evidence on both sides, and closes with a one-line takeaway.

```md
# <主题>

## 研究范围

- 时间范围:<resolved range>。证据范围:<n> 篇 paper-level 来源,<m> 条 evidence events。
- 覆盖知识单元:`EA-…`。完整证据条目见 [evidence-appendix.md](evidence-appendix.md)。

## 中心判断

<主题>的主要矛盾是:**<一句话中心论点,直接回答题目>**。

这不是"<常见的浅层归因>"一个问题,而是<把中心论点拆成 N 个层面的一句话预告>。

## <N> 个派生矛盾

### 1. <张力名,例:规模数量 vs 有效结构>

<正方证据的 prose 陈述,带论文链接>([SIEVE](https://arxiv.org/abs/2607.06442))。<反方/条件证据的 prose 陈述>([Lift3D-VLA](https://arxiv.org/abs/2607.06564))。

结论:<一句可操作的 takeaway>。

### 2. <下一个张力>…

## 可操作框架

| 维度 | 核心问题 | 典型指标 |
|---|---|---|
| <维度> | <一句话问题> | <2-4 个指标> |

## 最短结论

<主题>的主要矛盾,不是"<浅层说法>",而是**<中心论点的强化重述>**。解决路径是<一段收束性 prose>。

## References

- [<title>](https://arxiv.org/abs/<id>) (<published>) — 证据: [EA-…-0001](evidence-appendix.md#ea--0001), [EA-…-0002](evidence-appendix.md#ea--0002)
```

## Zhihu expert explainer (misconception-first)

Voice: 懂行的朋友给技术读者拆解。先破一个**具体的**误区(不是"大家都想错了"这种空话),再讲机制,再给边界。可以用比喻,不可以升级 stance。

```md
# <主题>:为什么"<流行的错误说法>"是错的

## TL;DR

<两三句话直接回答:错在哪、真实机制是什么、什么条件下例外。>

## 误区从哪来

很多人以为<具体误区>。这个直觉的来源是<为什么人们会这么想>。但 <SIEVE 式的具体反例>([SIEVE](https://arxiv.org/abs/2607.06442))直接推翻了它:<论文实际发现>。

## 真实机制

<用 2-4 段 prose 讲清楚机制。每段一个机制点,内联论文链接。可以打比方:"就像…"。>

## 什么时候这个结论不成立

<把 conditional/limit 事件转成"边界条款":在<条件>下,<结论会反转/失效>([TACO](https://arxiv.org/abs/2607.02840))。>

## 延伸阅读

<3-5 条,每条一句"为什么值得读"+ 论文链接。>
```

## Xiaohongshu insight post (hook-first)

Voice: 给泛兴趣读者的 5 条反常识卡片。每条 = 一句话洞察 + 一个链接。钩子必须来自证据,不是标题党。

```md
# <一个具体的反常识钩子,例:机器人数据,越多可能越差?>

<一两句展开钩子:最新论文发现<最强的一条反常识证据>。>

💡 <洞察 1 一句话>([论文短名](https://arxiv.org/abs/<id>))
💡 <洞察 2 一句话>([论文短名](https://arxiv.org/abs/<id>))
💡 <洞察 3-5…>

⚠️ 但要注意:<一句 caveat,来自 limit/conditional 事件,不许省略>

📚 依据:<n> 篇 2026 年 arXiv 论文,完整清单见 [evidence-appendix.md](evidence-appendix.md)
```

## Gap language

Use careful language:

- "本轮证据尚未覆盖..." when the run did not inspect enough sources.
- "已有论文明确指出..." only when an evidence event has `stance: gap`.
- "可以推断..." only with `inference` and a short reason.

## Topic-card update suggestion

```md
## Topic Card Update Suggestions

- Add to `<EA-ID>`:
  - <one compact working-memory claim>（source: <event-id/source-id>; confidence: <label>）
- Do not add:
  - single-paper summaries
  - candidate-only findings
  - claims without locator evidence
```

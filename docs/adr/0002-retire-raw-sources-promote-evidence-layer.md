---
title: Retire Raw Sources And Promote A Versioned Evidence Layer
status: accepted
date: 2026-07-08
tags: [adr, knowledge-base, evidence, provenance, context-management]
---

# ADR 0002: Retire Raw Sources And Promote A Versioned Evidence Layer

## Status

Accepted.

## Context

仓库最初的三层记忆模型是:原始材料 = source of truth,`knowledge/` 主题卡 = 压缩工作记忆,`knowledge/index.md` = 路由层。运行一段时间后出现三个结构性问题:

1. 三份原始材料(`具身智能研究问题清单.md`、`测绘误差观与大模型误差治理比较.md`、`项目背景信息.md`)已被手动退役删除,但 `knowledge/sources.md`、9 张主题卡的 frontmatter、`README.md` 与索引仍以文件路径和行号锚定它们,溯源链断裂。
2. 文献 run 的全部产出(accepted evidence JSONL、正式综述成品、source-entry draft)滞留在被 gitignore 的 `work/` 中:不进版本控制、误删无法恢复、对下一次 run 的 Agent 不可见。知识库只出不进。
3. 行号锚点(`locator: lines 19-110`)对任何一次原文编辑都会静默失效,是错误的锚定方式。

## Decision

1. **原始材料正式退役**。git 历史是其唯一存档:`git show 081e898:<文件名>` 可完整恢复。`knowledge/sources.md` 中对应条目标记 `status: retired` 并记录 archive 引用;主题卡 frontmatter 的 `source[].file` 改为 `archive` 引用。退役材料仍可溯源,但不再作为工作树文件维护。
2. **新建顶层 `evidence/` 作为版本化证据层**。规则与管线的 candidate ≠ evidence 纪律同构:**candidate 与中间产物住 `work/`(scratch,gitignored),accepted 资产住 `evidence/`(版本控制)**。每次文献 run 在 `evidence/literature-review-<topic>-<date>/` 归档 accepted evidence JSONL、正式综述成品、source-entry draft、query plan 与 `run.json` manifest。
3. **锚点策略从行号改为语义锚**。sources.md 与主题卡使用章节标题 / Q&A 编号 / 事件 ID 作为 locator;行号锚点全部替换。语义锚在原文编辑后仍可定位,且对 git 存档同样有效。
4. **三层记忆模型语义更新**:
   - `evidence/` 是论文级证据与综述成品的 source of truth(可追加、版本化)。
   - 退役原文经 git 存档仍可溯源,是历史背景材料的 source of truth。
   - 主题卡仍是压缩工作记忆;`knowledge/index.md` 仍是路由层。
5. **完整性可执行化**。新增 `scripts/check_kb_links.py`(校验 sources/主题卡/索引/run manifest 的链路完整性)与 `scripts/next_event_id.py`(事件 ID 分配去心算化),纳入测试套件。

## Consequences

- 溯源链恢复:每张主题卡的 source 引用可被脚本校验;退役不再等于断链。
- 知识积累有了落点:run 产出从"临时文件"升格为"版本化资产",下一次 run 的 Agent 可以加载 `evidence/` 中的既有证据。
- `work/` 语义变纯:只放中间产物与缓存,可随时清理。
- 维护成本:每次 run 结束多一步"结算"(把 accepted 资产拷入 `evidence/` 并写 manifest);由 SKILL.md 工作流固化。
- 上下文预算规则需说明:`evidence/` 中的 JSONL 不适合整读,Agent 应经 run.json 与 brief 选择性加载。

## Roadmap (P3/P4, not yet implemented)

本 ADR 记录后续两阶段路线,供未来实施参考:

- **P3 闭环**:
  - 结算流程:review workflow 末尾显式展示 source-entry draft 与 topic-card update suggestions 并询问合入;`scripts/merge_source_entries.py` 承担合入(默认仍非变异)。
  - 引用审计:`scripts/audit_citations.py` 对 memo+appendix+evidence.jsonl 报告未注册引用、未被引用事件、无引用且无 inference 标记的段落。
  - Query 反馈闭环:run 结束把 "query → 候选数 → 进入证据层的论文数" 写 `evidence/<run>/query-stats.json`;planner 增加第二轮协议(从 `core_citations` 与高频新词生成增量 dynamic-file,连续一轮无新增证据即收敛)。
  - 动态联想升主流程:planner workflow 把"生成 clue model"从可选改为必做。
- **P4 深化**:种子论文锚定、PDF 正式回退位(`pdf-extracted` 置信标记)、planner→search→evidence→packet 全链路 mock 冒烟测试、`work/` 旧平铺文件归档与保留策略。

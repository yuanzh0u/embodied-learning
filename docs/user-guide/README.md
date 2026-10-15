# 使用文档

具身智能证据知识库（Embodied AI Evidence Hub）的使用指南。文档按任务组织，从安装到跑通一条完整综述。

## 目录

| 章节 | 内容 |
|---|---|
| [安装](installation.md) | 环境要求、克隆、可选的 `pip install` 与控制台命令 |
| [快速上手](getting-started.md) | 本地打开 Wiki、跑测试、构建发布站 |
| [综述流水线](review-pipeline.md) | 从研究问题到已发布综述：`run.py launch` / `run.py pipeline` |
| [单篇工具](single-paper.md) | 速读卡、汇报 deck、论文对话 |
| [Wiki 使用](wiki.md) | 本地研究 Wiki：工作流对话、版本切换、修订成稿 |
| [CLI 参考](cli-reference.md) | 六域 dispatcher 与全部子命令 |

## 先读哪一篇

- **只想读综述**：直接打开[在线站点](https://yuanzh0u.github.io/embodied-learning/)，或看[快速上手](getting-started.md)的本地 Wiki 一节。
- **想跑一篇新综述**：[综述流水线](review-pipeline.md)。
- **想精读一篇论文**：[单篇工具](single-paper.md)。
- **想接入 Agent**：[快速上手](getting-started.md)的「交给 AI Agent」一节，以及仓库根的 `AGENTS.md`。

## 文档与代码的边界

- 本目录是**给人看的使用文档**。
- `scripts/README.md` 是运维层脚本地图（含并发锁、harness、能力状态表），面向维护者。
- `CLAUDE.md` / `AGENTS.md` 是 Agent 的上下文加载约定，不是用户手册。
- `docs/adr/` 是架构决策记录，解释「为什么」。
- `docs/seo-geo-release-runbook.md` 是发布后的搜索引擎 / GEO 监测手册。

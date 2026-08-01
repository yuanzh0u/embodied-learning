# 具身学习知识库

> **在线阅读： [打开空间智能研究 Wiki →](https://yuanzh0u.github.io/embodied-learning/)**

这是一个围绕具身智能、数据采集、多模态感知、跨本体迁移、评测体系、商业化落地与误差治理的研究知识库。

## 快速入口

- [空间智能研究 Wiki](https://yuanzh0u.github.io/embodied-learning/)：面向阅读者的研究成果导览，默认提供知乎解释版。
- [项目上下文词表](CONTEXT.md)：项目共享语言与 query-planning 术语。
- [智能体索引](knowledge/index.md)：面向智能体的主索引，优先从这里开始检索。
- [知识库说明](knowledge/README.md)：说明目录结构、索引规则和新增素材方式。
- [证据层说明](evidence/README.md)：文献 run 的 accepted 证据与综述成品归档。
- [术语表](knowledge/glossary.md)：统一核心术语，减少上下文歧义。
- [素材入库规范](knowledge/ingestion-guide.md)：后续新增论文、报告、访谈、项目资料时使用。

## 本地研究 Wiki

双击仓库根目录的 `打开具身智能研究Wiki.command` 即可启动。Wiki 只收录同时具备科研备忘录、知乎解释版和小红书版的完整话题；同一话题只显示最新版本，默认打开知乎解释版。

页面中的“刷新成果”会重新扫描 `work/` 并更新 `wiki/data/` 发布快照。检查确认后提交这些快照文件，GitHub Pages 就会发布下一版。线上页面的“检查更新”只读取已经发布的最新快照，不会访问本地文件。

## 已退役材料（git 存档）

三份初始原始材料已于 2026-07-08 退役（见 [ADR-0002](docs/adr/0002-retire-raw-sources-promote-evidence-layer.md)），唯一存档在 git 历史中，需要完整论述时用以下命令恢复：

```bash
git show 081e898:具身智能研究问题清单.md
git show 081e898:测绘误差观与大模型误差治理比较.md
git show 081e898:项目背景信息.md
```

登记信息与章节锚见 [knowledge/sources.md](knowledge/sources.md)。`knowledge/` 下的主题卡负责压缩、索引和面向智能体加载；论文级证据见 `evidence/`。

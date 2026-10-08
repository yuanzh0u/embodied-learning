# 智驾模型研究 · 体系阅读

以 Mind-Omni 官方总图组织理想专题，提供六个模块、逐层展开的论文与延伸阅读，同时保留原有 30 篇论文、71 位人员和 Tesla / Waymo 工业对照。

## 证据与展示分工

- 论文证据仍以 `evidence/literature-review-智驾模型-vla-驾驶基础模型与关键团队-理想增补-20260927/` 为准；已归档证据未修改。
- `mind-omni-guide.md` 与 `mind-omni.json` 是基于已审计证据的派生阅读结构，不是新一轮论文综述。
- 官方总图属于工业项目披露，来源、日期与原图哈希记录于 `mind-omni-source.json`；不生成论文 evidence event。
- `presentation-audit.json` 记录本次展示、链接及关键推断边界核查，不替代原 run 的论文审计。
- 关系以官方布局、明确方法继承、研究问题延伸分别表述。MindSim 未公开充分证据的部分保留缺项。

## 本地生成

在仓库根目录执行 `python3 scripts/build_mind_omni_reader.py`，会从固定归档版本生成主站子页。正常发布由 `scripts/build_research_site.py` 统一调用，无运行时依赖。

检查 JavaScript 语法：`node --check wiki/guides/mind-omni/reader.js`。本次未运行模型复现实验；未进行未被请求的浏览器视觉测试。

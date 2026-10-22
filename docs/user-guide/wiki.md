# Wiki 使用

本地研究 Wiki 是阅读与触发工作的入口：读综述、翻证据、跑新综述、聊论文。

## 启动

```bash
python3 scripts/wiki.py serve --open          # 打开 http://127.0.0.1:8018
python3 scripts/wiki.py serve --close         # 停止
python3 scripts/wiki.py serve --kb-root ~/Documents/arxiv   # 换知识库
```

默认读本地知识库 `~/Documents/arxiv`。macOS 可双击 `打开具身智能研究Wiki.command`。

对话相关参数（研究助手 / 工作流都走本机 `claude` CLI）：

| 参数 | 说明 |
|---|---|
| `--no-chat` | 禁用对话（纯阅读模式） |
| `--chat-model` / `--workflow-model` | 用哪个模型 |
| `--chat-permission-mode` | `bypassPermissions`（默认）/ `acceptEdits` / `plan` / `default` |
| `--chat-timeout-s` | 单轮超时，默认 900 |
| `--workflow-effort` | `low` / `medium` / `high`，低档更快 |

## 读综述

- **三版本切换**：科研备忘录（keyan）/ 知乎长文（zhihu）/ 小红书帖子（xiaohongshu），同源证据不同文风。
- **证据抽屉**：每条综合判断可展开到证据事件（论文、定位锚、stance、confidence）。
- **全文搜索**：跨专题检索。
- **知识图谱**：主题卡与引用关系的可视化（`wiki.py build-knowledge-map` 生成）。
- **References**：证据附录的引用表（含 arXiv ID、机构等元数据）。

判断的可信度按固定词表标注：`support` / `limit` / `conditional` / `gap`；
`direct` / `citation-supported` / `inference`。**标成 `inference` 的是推断**，不是论文原话。

## 工作流对话（跑新综述）

「工作流」标签页是 STORM 式的综述发起入口：采访式提问 → 生成 topic / focus / knowledge-id →
后台跑无头流水线 → 实时进度 → 产出进 wiki 快照。

- 跑的是 `run.py launch` 同一条链路；进度面板显示阶段与漏斗数字（复用 `run.py status`）。
- **每张阶段卡片只放它自己的动作**：工具行按命令/文件名推断归属（`Write zhihu-explainer_zhihu.md`
  落「成稿撰写」、`run.py check-bundle` 落「审计门」、`run.py finalize` 落「落盘发布」），
  链式命令取第一段；模型没打印 `[STAGE:*]` 也不会串卡。推断不出归属的调用（临时文件写入、
  `find` / 裸 `ls` 之类的探查命令）进中性的「其他动作」卡，**不会**回填到上一个已结束阶段。
- **卡片按首条日志的时间排序**：某阶段的第一条事件来晚了（模型在收尾时才补打 `[STAGE:*]`），
  它的卡片仍插在时间对应的位置，不会挂到列表末尾制造「上一阶段最后一条排在下一阶段第一条前面」。
  收尾消息里重述整条阶段链的标记只是叙述，不会把工作流拨回已完成的阶段。
- **审计门卡片带输出**：`check-bundle` / `audit-citations` / `audit-article-quality` / `finalize`
  的 stdout 以折叠块附在对应工具行下（失败调用无论属哪阶段都保留输出，尾部 1500 字）。
- **开工前查重**：同一主题重复启动会截断 registry。看到已有 in-progress run 就用 `--resume`。
- 长时间静默是正常的（深读/成稿是长任务）；页面保持可见心跳。

也可以直接命令行发起，见[综述流水线](review-pipeline.md)。

## 修订成稿

已 settle 的综述可以做**追加式修订**（不改原始交付物）：

页面「修订成稿」开关 → 选文体 → 生成 `evidence/<run>/revisions/<style>-v<N>.md`
（基底成稿 = v0，首次修订 = v1；版本名机械化递增，版本变迁由研究范围描述承载；`revisions/index.json` 由服务端写 provenance）。

规则：

- 快照构建器把每个修订版本当作独立版本键（`keyan-v1`）排在基底文体之后；
- 基线交付物、`run.json`、`trace-map.json`、`evidence-appendix.md` **永不改写**；
- 修订只用该 run 已有的证据集，不引入新证据。

## 论文对话 / 速读 / 汇报

- **论文对话**：按 arXiv ID 起对话，以深读笔记为上下文（`read.py prepare-chat` 预备）。
- **速读** tab：浏览池内 `quick-read_sudu.md` 卡片，可现场触发新卡（`read.py quick-read`）。
- **汇报放映**：run 级 / 单篇 reveal.js deck（`write.py run-deck` / `paper-deck`），产物生成后重建快照即可见。

细节见[单篇工具](single-paper.md)。

## 多机 / 共享盘

知识库可以放在 CIFS 挂载上多机共用。跨进程协调用 `<kb-root>/.locks/`（O_EXCL 锁文件）
与 `<kb-root>/.claims/`（事件 ID 前缀预留），**不用 flock**。紧急情况可
`EMBODIED_KB_LOCKS_DISABLED=1` 让锁退化为 no-op。

同一 KB 上多机写共享文件（pool index、catalog、run.json、发布、快照重建）是安全的；
但**同一个 run 目录**仍只应由一个 launcher 驱动。

## 常见问题

**页面打不开 / 端口冲突**：换 `--port`，或 `serve --close` 后重启。端口被占时会先问占用者
服务哪个知识库：**同一个库**就复用并提示；**不同的库**直接报错退出（码 2）并给出关闭或换端口两条路
——不会再出现「传了新 `--kb-root`，页面还是旧库」的静默复用。

**新综述没出现在页面上**：跑完 finalize 会重建快照；手动补
`python3 scripts/wiki.py build-wiki --kb-root ~/Documents/arxiv`。

**对话没反应**：确认 `claude` 在 PATH 上、已登录；超时可调大 `--chat-timeout-s`。

**想换知识库**：`--kb-root /path/to/kb`，路径下要有 `knowledge/` 与 `evidence/`。

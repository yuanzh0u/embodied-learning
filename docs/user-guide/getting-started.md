# 快速上手

三分钟把环境跑起来。完整流水线见[综述流水线](review-pipeline.md)。

## 1. 自检

```bash
cd embodied-learning
make test          # 与 CI 相同的四个测试套件
```

全绿即可继续。只跑知识层用 `make test-knowledge`；校验已发布综述用 `make validate`（需完整 git 历史）。

## 2. 本地打开 Wiki

```bash
python3 scripts/wiki.py serve --open
```

浏览器会打开 `http://127.0.0.1:8018`。默认读本地知识库 `~/Documents/arxiv`；换库加 `--kb-root`。

macOS 也可以双击仓库根目录的 `打开具身智能研究Wiki.command`。

停止：`python3 scripts/wiki.py serve --close`，或 Ctrl-C。

Wiki 提供：三版本切换（科研备忘录 / 知乎 / 小红书）、全文搜索、证据抽屉、知识图谱、
工作流对话（跑新综述）、论文对话、速读卡与汇报 deck 入口。细节见 [Wiki 使用](wiki.md)。

## 3. 构建发布站（可选）

从仓库语料构建可抓取的静态研究站：

```bash
python3 scripts/wiki.py build-wiki --output /tmp/wiki-data
python3 scripts/wiki.py build-site \
  --snapshot-root /tmp/wiki-data \
  --wiki-root wiki \
  --output /tmp/wiki-site \
  --base-url https://yuanzh0u.github.io/embodied-learning
```

产出 44 个专题页、`sitemap.xml`、`robots.txt`、`llms.txt` 和 JSON-LD 元数据。
打开 `/tmp/wiki-site/index.html` 即可离线浏览。

> `build-wiki` 不带 `--kb-root` 时取**仓库** catalog + `wiki/site-config.json`，产出 schema v2
> 快照（`build-site` 只接受 v2）。本地 KB 用 `--kb-root`，见 [CLI 参考](cli-reference.md)。

## 4. 交给 AI Agent

支持 `AGENTS.md` 的智能体从 `knowledge/index.md` 开始，只加载与问题匹配的主题卡：

```text
先读取 knowledge/index.md。
围绕“世界模型怎样进入机器人闭环评测”选择相关主题卡，
再从 literature-review-catalog.md 定位当前 review packet；
每条综合判断都保留证据入口，并明确哪些内容属于推断。
```

路由约定（哪个问题加载哪张卡）在 `AGENTS.md`，不要让 Agent 预加载整个目录。

## 5. 跑第一篇综述（可选）

无人值守端到端：

```bash
setsid nohup python3 scripts/run.py launch \
  --topic "近一年触觉世界模型的进展" \
  --review-mode scoping \
  --time-range 2024-01-01..2026-06-06 \
  --focus "接触状态估计、触觉表征、视觉-触觉联合" \
  --knowledge-id EA-SENSOR \
  --kb-root ~/Documents/arxiv \
  > /tmp/launch.log 2>&1 &
```

然后看进度：

```bash
python3 scripts/run.py launch --status --run-dir ~/Documents/arxiv/work/literature-review-近一年触觉世界模型的进展-<日期>
```

细节与断点续跑见[综述流水线](review-pipeline.md)。

## 常见问题

**端口被占用**：`serve --port 8020`，或先 `serve --close`。

**找不到知识库**：显式传 `--kb-root /path/to/kb`。默认 `~/Documents/arxiv`。

**浅克隆校验失败**：`git fetch --unshallow` 后重试。

**`claude` 找不到**：流水线判断阶段需要本机 `claude` CLI；只读 Wiki 不需要。

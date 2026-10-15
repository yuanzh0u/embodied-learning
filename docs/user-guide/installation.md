# 安装

代码是 **stdlib-only Python 3**（≥3.10）：没有必须安装的第三方依赖，没有构建步骤。克隆即可用。

## 标准安装：克隆即用

```bash
git clone https://github.com/yuanzh0u/embodied-learning.git
cd embodied-learning
python3 -m unittest discover -s tests -p 'test_*.py'   # 自检，应全部通过
```

> **需要完整 git 历史**：退役的原始材料只保存在 git 历史里，知识库校验
> （`check-kb-links` / `validate-reviews`）要读历史。不要用 `git clone --depth 1`；
> 已经浅克隆的执行 `git fetch --unshallow`。

所有脚本用 `python3` 调用（`python` 可能不在 PATH）：

```bash
python3 scripts/run.py --help
python3 scripts/wiki.py --help
```

## 可选：`pip install` 注册控制台命令

不需要安装任何东西也能跑；`pip install .`（或 `-e .`）只是把常用入口注册成命令：

```bash
pip install .            # 或 pip install -e .
```

会得到这些命令（与 `scripts/` / `skills/*/scripts/` 下的入口等价）：

| 命令 | 等价于 | 作用 |
|---|---|---|
| `launch_review` | `scripts/run.py launch` | 无头端到端综述 |
| `run_review_pipeline` | `scripts/run.py pipeline` | 机械阶段 driver |
| `serve_research_wiki` | `scripts/wiki.py serve` | 本地研究 Wiki |
| `quick_read_paper` | `skills/embodied-ai-paper-reader/scripts/read.py quick-read` | 单篇速读卡 |
| `paper_slide_deck` | `skills/embodied-ai-review-writer/scripts/write.py paper-deck` | 单篇汇报 deck |
| `run_slide_deck` | `skills/embodied-ai-review-writer/scripts/write.py run-deck` | run 级汇报 deck |
| `extract_arxiv` | `skills/embodied-ai-literature-hub/scripts/fetch.py extract-arxiv-html` | arXiv 全文抽取 |

安装出的 wheel 是**自包含**的：三棵技能树（`SKILL.md` / `references/` / `agents/` / `scripts/`）打成
`wiki_scripts.skills` 包数据，路径解析只走 `embodied_learning.utils.layout`。因此安装环境与仓库
checkout 的行为一致。spawn 出的无头 `claude` 代理使用隔离的 `CLAUDE_CONFIG_DIR`
（`~/.cache/embodied-learning/claude-config`）且 `cwd=<kb-root>`，读不到启动会话的记忆或仓库。

## 可选 extras

HTML 全文路径不需要任何依赖。以下 extras 只在用到对应通道时才需要：

```bash
pip install '.[pdf]'     # pypdf：--force-pdf / PDF 回退抽取
pip install '.[s3]'      # boto3：arXiv TeX 源码 tarball 下载（S3 requester-pays，需凭证）
pip install '.[tex]'     # pypandoc：TeX → Markdown（另需系统 pandoc）
pip install '.[sources]' # 上面 s3 + tex 的合集
```

## 依赖一览

| 场景 | 需要 |
|---|---|
| 读在线/本地 Wiki、跑测试、校验知识库 | 无（stdlib） |
| HTML 全文抽取（默认） | 无（stdlib + 网络） |
| PDF 全文回退 | `pypdf` |
| TeX 源码恢复（非默认） | `boto3` + `pypandoc` + 系统 `pandoc` |
| AI 调用（深读骨架、写作、对话） | 本机 `claude` CLI |
| 离线检索（可选加速） | 无额外依赖；需先建一次 SQLite 快照库 |

## AI 调用前置

流水线的判断阶段（骨架深读、写作成稿、Wiki 对话）通过本机的 `claude` CLI 完成。
请确保：

1. `claude` 在 PATH 上（或用 `--chat-cli` / `--complete-cli` 指定路径）；
2. 已登录一次，凭据可被自动播种到隔离配置目录；
3. 不要在启动会话里手动 spawn `claude`——全部调用走 `embodied_learning/harness/claude.py`。

## 知识库根目录

代码与知识内容分离。工作用的本地知识库默认在 `~/Documents/arxiv`（含自己的
`knowledge/`、`evidence/`、`pool/`、`work/`、`wiki/`）。仓库里的 `knowledge/` 是
公开发布语料。

| 根 | 用途 |
|---|---|
| 仓库 checkout | 公开发布语料、代码、测试 |
| `~/Documents/arxiv` | 本地工作知识库（默认 `--kb-root`） |
| `/mount/TEST/public/wiki` | 局域网共享 KB（多机场景） |

综述、主题卡、论文池等**知识产出进本地 KB**；仓库只记录代码。路径不对时用
`--kb-root` 显式指定。

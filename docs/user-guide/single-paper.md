# 单篇工具

不跑整条综述、只处理一篇论文时用这些。共同点：**精读强制**——没有审计过的深读笔记，不产出卡片或 deck。

## 速读卡（quick-read）

```bash
python3 skills/embodied-ai-paper-reader/scripts/read.py quick-read --arxiv-id 2302.01109
# 或（pip install 后）
quick_read_paper --arxiv-id 2302.01109
```

流水线：pool 检查（幂等补齐抽取）→ **深读**（复用已有笔记，否则现深读）→ 简报（确定性渲染 note+meta）→ 代理成稿（一次，失败重试一次）→ 编辑审计（警告级，不致命）。

产物落在论文池 `~/Documents/arxiv/pool/arxiv-<id>/quick-read_sudu.md`；Wiki 的「速读」tab 直接浏览。

| 参数 | 说明 |
|---|---|
| `--arxiv-id` | arXiv ID（必填） |
| `--kb-root` | 知识库根，默认 `~/Documents/arxiv` |
| `--force` | 忽略缓存，重抽 / 重深读 / 重写 |
| `--skip-agent` | 只出简报（调试），不写卡片 |
| `--no-audit` | 跳过编辑审计 |

退出码：`0` 写成（或缓存命中）；`3` **深读不可用**（不是成功，调用方不要当成功处理）；`1` 硬失败。
最后一行 stdout 是机器可读 JSON。代理写坏了的原文会落到 `quick-read-agent-raw.txt`，便于事后诊断。

## 汇报 deck（slide deck）

### 单篇

```bash
python3 skills/embodied-ai-review-writer/scripts/write.py paper-deck --arxiv-id 2302.01109
```

同 quick-read 的骨架：pool → 深读强制 → 简报 → **代理只写 slide-source DSL** →
`write.py compile-slide-deck` 编译成 reveal.js 单文件 `slide-deck_report.html`。
**禁止手写 HTML**——源文件 `slide-deck_report.md` 才是事实源，改内容改它再编译。

### Run 级

```bash
python3 skills/embodied-ai-review-writer/scripts/write.py run-deck --run-dir <run-dir>
```

从综述 run 的 `writing-brief.md` + `evidence-appendix.md` 生成汇报 deck，产物落在 run 目录
（run 目录无锁）。之后重建 wiki 快照，专题页的「汇报放映」入口即可用。

参数与退出码同 quick-read（`run-deck` 另有退出码 `2` = run 目录不完整 / 无参考文献）。

## 论文对话

Wiki 页面上的「论文对话」标签页，或手动准备：

```bash
python3 skills/embodied-ai-paper-reader/scripts/read.py prepare-chat --arxiv-id 2302.01109
```

确保论文进池 + 深读完成，然后对话代理以深读笔记为上下文回答问题。
注意语义与 quick-read **相反**：`prepare-chat` 在深读不可用时可以降级继续（对话还能聊摘要级内容），
而 `quick-read` / `paper-deck` 的退出码 3 表示失败。

## 论文池

公共论文池在本地 KB 之外的目录（默认 `~/Documents/arxiv/pool`），一文一目录：

```text
pool/arxiv-<id>/
  paper.md          # 全文 Markdown（arxiv2md 或 HTML 恢复）
  extraction.json   # 抽取结果
  note.md / note.json  # 深读笔记
  meta.json         # 元信息
  quick-read_sudu.md
  slide-deck_report.{md,html}
```

常用操作：

```bash
python3 skills/embodied-ai-paper-reader/scripts/read.py pool-add-paper add --extraction /tmp/extraction.json
python3 skills/embodied-ai-paper-reader/scripts/read.py pool-add-paper list
```

主题卡可以用 `POOL-<...>` frontmatter `source` 引用池内论文（绝对 `file:` 路径 + 语义锚 `locator`），
`wiki.py check-kb-links` 校验文件存在，不要求 `sources.md` 登记。

## 相关文档

- [综述流水线](review-pipeline.md)：多论文的完整链路
- [Wiki 使用](wiki.md)：在浏览器里打开速读 / deck / 对话

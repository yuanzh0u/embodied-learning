# SEO / GEO 发布与监测手册

本手册覆盖代码合并后的外部操作。站点生成、页面 metadata、Sitemap、robots、`llms.txt` 和 PR Preview 的自动检查由仓库测试负责；搜索引擎所有权验证、Sitemap 提交和 GEO 抽查必须在生产发布后执行。

## 1. 发布前门禁

在仓库根目录运行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_current_reviews.py --root .
python3 scripts/check_kb_links.py --root .
python3 scripts/build_research_wiki.py --output /tmp/wiki-data
python3 scripts/build_research_site.py \
  --snapshot-root /tmp/wiki-data \
  --wiki-root wiki \
  --output /tmp/wiki-site \
  --base-url https://yuanzh0u.github.io/embodied-learning
```

PR Preview 必须满足：页面含 `noindex,nofollow`，`robots.txt` 为 `Disallow: /`，canonical 仍指向生产地址。

## 2. 生产发布抽查

主分支部署完成后，确认以下地址返回 200：

- `https://yuanzh0u.github.io/embodied-learning/`
- `https://yuanzh0u.github.io/embodied-learning/research/`
- `https://yuanzh0u.github.io/embodied-learning/robots.txt`
- `https://yuanzh0u.github.io/embodied-learning/sitemap.xml`
- `https://yuanzh0u.github.io/embodied-learning/llms.txt`
- Sitemap 中的全部 38 个专题地址

人工关闭 JavaScript，抽查首页及世界模型、VLA、触觉、Ego–Exo、4D 五类页面。正文、论文引用和完整证据附录必须仍可阅读。

查看页面源代码，确认正文与 JSON-LD 已存在于原始 HTML，而不是运行后注入。再使用 Google Rich Results Test 和 Open Graph 调试工具抽查同一批页面。

## 3. 站点所有权验证

使用 HTML 文件方式验证 Google Search Console 与 Bing Webmaster。

1. 从站长工具下载验证文件。
2. 将 Google 文件放入 `wiki/verification/google<token>.html`。
3. 将 Bing 文件命名为 `wiki/verification/BingSiteAuth.xml`。
4. 提交代码并等待主分支发布。
5. 确认验证文件的根地址返回 200，再回到站长工具完成验证。

站点生成器只复制符合上述命名规则的验证文件，避免把其他内部文件发布到站点根目录。

## 4. 提交 Sitemap

在两个站长工具中提交：

```text
https://yuanzh0u.github.io/embodied-learning/sitemap.xml
```

Google Search Console 使用 URL Inspection 抽查首页、专题目录和 5 个代表专题，并在未收录时请求编入索引。Bing Webmaster 使用 Site Scan 检查 canonical、重复 title、抓取错误和结构化数据错误。

## 5. 20 个固定 GEO 问题

每月在 ChatGPT、Perplexity、Google AI 搜索和 Bing Copilot 使用相同问题、相同语言与相同记录格式。只记录公开结果，不使用个性化提示补充仓库信息。

1. 世界模型能否作为机器人闭环评测的真值源？
2. 机器人世界模型最需要哪些训练数据？
3. 世界模型监督训练与纯端到端训练如何取舍？
4. 反应式 VLA 是否会被世界模型取代？
5. VLA 中语言、视觉和连续动作如何对齐？
6. 近年的 VLA 模型有哪些实质性技术突破？
7. 机器人原子技能为什么演进到 VLA？
8. 4D 时空推理需要什么样的数据？
9. 4D 时空推理与普通视频理解有什么区别？
10. 具身智能数据质量最核心的矛盾是什么？
11. 如何识别具身智能训练数据污染？
12. 具身数据怎样保持时空一致性？
13. Egocentric 数据用于机器人训练有什么困难？
14. Ego–Exo 相机如何完成标定与视角对齐？
15. 第三人称视觉表征怎样迁移到第一人称？
16. 视觉与触觉联合训练有哪些主要方法？
17. 触觉世界模型解决了哪些纯视觉无法解决的问题？
18. 具身感知和导航是否已经被解决？
19. 如何区分具身系统的感知误差与认知误差？
20. Loco-Manipulation 的主要进展与开放难题是什么？

每条结果记录：日期、平台、问题、是否出现本站、引用 URL、引用位置、答案是否准确、是否误用结论边界、截图或可复查链接。

## 6. 第 2、4、8 周记录

| 周期 | 已索引专题数 | 非品牌搜索曝光 | 前十查询 | Bing / AI 引用 | Star 增量 | Fork 增量 | 主要问题 |
|---|---:|---:|---|---:|---:|---:|---|
| 第 2 周 |  |  |  |  |  |  |  |
| 第 4 周 |  |  |  |  |  |  |  |
| 第 8 周 |  |  |  |  |  |  |  |

目标是在发布后 8 周内，让 38 个专题全部进入至少一个主流搜索索引。未收录页面按抓取、重复、内容质量和外链四类归因，每次只调整有明确证据的问题。

## 7. 异常排查顺序

1. 抓取：状态码、robots、Sitemap、Pages 部署路径和内部链接是否正确。
2. canonical：是否唯一且指向生产专题页，Preview 是否错误进入索引。
3. 重复：是否出现三文体独立 URL、hash URL 或 alias 页面参与竞争。
4. 内容：正文、证据附录和论文引用是否存在于原始 HTML，description 是否具体。
5. 外链：README、GitHub Homepage、相关专题与公开引用是否指向 canonical。

不要为了 GEO 盲目堆叠关键词、复制三文体页面或添加无法验证的宣传数字。`llms.txt` 只提供机器可读导航，不替代标准抓取协议和可引用内容。

#!/usr/bin/env python3
"""Build the crawlable research site from a validated Wiki schema-v2 snapshot."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from xml.etree import ElementTree


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_research_wiki import (  # noqa: E402
    VERSION_FILES,
    excerpt,
    resolve_snapshot_directory,
    validate_snapshot,
)
from lib.markdown_semantics import render_markdown  # noqa: E402


DEFAULT_SNAPSHOT_ROOT = REPO_ROOT / "wiki" / "data"
DEFAULT_WIKI_ROOT = REPO_ROOT / "wiki"
DEFAULT_OUTPUT = REPO_ROOT / "_site"
DEFAULT_BASE_URL = "https://yuanzh0u.github.io/embodied-learning"
INDEX_DESCRIPTION = (
    "面向 VLA、世界模型、4D 时空推理、多模态感知、机器人数据与闭环评测的具身智能证据知识库。"
    "每项综述连接完整正文、精读论文、正式证据事件与可审计研究边界。"
)
_EXTERNAL_SCHEMES = {"http", "https", "mailto"}
_URL_PATTERN = re.compile(r"^https?://[^\s]+$")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(_read_text(path))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON 文件必须是对象：{path}")
    return value


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _base_url(value: str) -> str:
    value = value.rstrip("/")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError("生产 base URL 必须是有效 HTTPS 地址。")
    return value


def _canonical_url(base_url: str, canonical_path: str) -> str:
    return f"{base_url}{canonical_path}"


def _asset_url(base_url: str, asset_path: str) -> str:
    return f"{base_url}/{asset_path.lstrip('/')}"


def _safe_json_ld(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _without_first_h1(value: str) -> str:
    return re.sub(r"\s*<h1(?:\s[^>]*)?>.*?</h1>\s*", "", value, count=1, flags=re.DOTALL)


def _description(topic: dict[str, object]) -> str:
    title = str(topic["title"])
    short_title = title if len(title) <= 42 else f"{title[:41]}…"
    summary = str(topic.get("excerpt") or "").rstrip("…。.；; ")
    paper_count = int(topic["paper_count"])
    event_count = int(topic["evidence_event_count"])
    suffix = (
        f"本专题基于 {paper_count} 篇精读论文和 {event_count} 条正式证据事件，"
        "提供完整综述、去重论文引用、审计状态、证据边界与可追溯附录。"
    )
    summary_limit = max(28, 154 - len(short_title) - len(suffix) - 2)
    summary = summary[:summary_limit].rstrip("，、；:： ")
    value = f"{short_title}：{summary}。{suffix}"
    if len(value) < 120:
        value += "内容覆盖研究问题、方法差异、失败边界和后续验证方向。"
    return value[:159].rstrip("，、；:： ") + ("" if value[:159].endswith("。") else "。")


def _repo_url(repository_url: str, repo_relative: Path, fragment: str = "") -> str:
    encoded = "/".join(quote(part) for part in repo_relative.as_posix().split("/"))
    suffix = f"#{quote(fragment, safe='-._~:/')}" if fragment else ""
    return f"{repository_url.rstrip('/')}/blob/main/{encoded}{suffix}"


class StaticMarkdownRenderer:
    """Render repository Markdown safely while validating every relative target."""

    def __init__(self, repo_root: Path, source_directory: Path, repository_url: str) -> None:
        self.repo_root = repo_root.resolve()
        self.source_directory = source_directory.resolve()
        self.repository_url = repository_url

    def link(self, label: str, target: str) -> str:
        safe_label = html.escape(label)
        parsed = urlsplit(target)
        if parsed.scheme in _EXTERNAL_SCHEMES:
            return (
                f'<a href="{html.escape(target, quote=True)}" target="_blank" '
                f'rel="noopener noreferrer">{safe_label}</a>'
            )
        if parsed.scheme or parsed.netloc:
            raise RuntimeError(f"不支持的 Markdown 链接：{target}")
        if not parsed.path and parsed.fragment:
            return f'<a href="#{html.escape(parsed.fragment, quote=True)}">{safe_label}</a>'
        normalized_path = unquote(parsed.path)
        if Path(normalized_path).name in {"evidence-appendix.md", "review-packet.md"}:
            return f'<a href="#evidence">{safe_label}</a>'
        if normalized_path.startswith("/"):
            raise RuntimeError(f"仓库内链接必须使用相对路径：{target}")
        destination = (self.source_directory / normalized_path).resolve()
        try:
            repo_relative = destination.relative_to(self.repo_root)
        except ValueError as exc:
            raise RuntimeError(f"仓库链接越界：{target}") from exc
        if not destination.exists():
            raise RuntimeError(f"失效的仓库相对链接：{target}（来自 {self.source_directory}）")
        href = _repo_url(self.repository_url, repo_relative, parsed.fragment)
        return (
            f'<a href="{html.escape(href, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{safe_label}</a>'
        )

    def image(self, alt: str, target: str) -> str:
        safe_alt = html.escape(alt or "研究素材", quote=True)
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https"}:
            return (
                f'<img src="{html.escape(target, quote=True)}" alt="{safe_alt}" loading="lazy">'
            )
        if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
            raise RuntimeError(f"不支持的 Markdown 图片：{target}")
        destination = (self.source_directory / unquote(parsed.path)).resolve()
        try:
            repo_relative = destination.relative_to(self.repo_root)
        except ValueError as exc:
            raise RuntimeError(f"仓库图片越界：{target}") from exc
        if not destination.is_file():
            raise RuntimeError(f"失效的仓库图片：{target}")
        encoded = "/".join(quote(part) for part in repo_relative.as_posix().split("/"))
        src = f"{self.repository_url.rstrip('/')}/raw/main/{encoded}"
        return f'<img src="{html.escape(src, quote=True)}" alt="{safe_alt}" loading="lazy">'

    def render(self, markdown: str) -> str:
        return render_markdown(
            markdown,
            link_renderer=self.link,
            image_renderer=self.image,
            heading_ids=True,
            collect_toc=False,
            table_wrapper_class="table-scroll",
        ).html


def _source_directory(repo_root: Path, topic: dict[str, object]) -> Path:
    raw = topic.get("source_directory")
    if not isinstance(raw, str) or not raw:
        raise RuntimeError(f"专题 {topic.get('id')} 缺少 source_directory。")
    candidate = Path(raw)
    directory = candidate if candidate.is_absolute() else repo_root / candidate
    directory = directory.resolve()
    try:
        directory.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise RuntimeError(f"专题来源目录越过仓库：{raw}") from exc
    if not directory.is_dir():
        raise RuntimeError(f"专题来源目录不存在：{directory}")
    return directory


def _article_bodies(
    repo_root: Path,
    repository_url: str,
    topic: dict[str, object],
) -> tuple[str, str, str]:
    directory = _source_directory(repo_root, topic)
    renderer = StaticMarkdownRenderer(repo_root, directory, repository_url)
    zhihu_path = directory / VERSION_FILES["zhihu"][1]
    if not zhihu_path.is_file():
        raise RuntimeError(f"专题缺少知乎正文：{zhihu_path}")
    raw_zhihu = _read_text(zhihu_path)
    zhihu_html = _without_first_h1(renderer.render(raw_zhihu))

    evidence = topic.get("evidence")
    evidence_name = evidence.get("source_file") if isinstance(evidence, dict) else None
    if not isinstance(evidence_name, str):
        raise RuntimeError(f"专题缺少证据附录：{topic.get('id')}")
    evidence_path = directory / evidence_name
    if not evidence_path.is_file():
        raise RuntimeError(f"专题证据附录不存在：{evidence_path}")
    evidence_html = _without_first_h1(renderer.render(_read_text(evidence_path)))
    conclusion = excerpt(raw_zhihu, limit=260)
    return conclusion, zhihu_html, evidence_html


def _citation_list(citations: list[dict[str, object]]) -> str:
    rows = []
    for citation in citations:
        title = html.escape(str(citation.get("title") or citation.get("url") or "论文"))
        url = html.escape(str(citation.get("url") or ""), quote=True)
        authors = citation.get("authors")
        author_text = ", ".join(str(name) for name in authors[:8]) if isinstance(authors, list) else ""
        if isinstance(authors, list) and len(authors) > 8:
            author_text += " et al."
        year = citation.get("year") or "n.d."
        meta = html.escape(" · ".join(value for value in [author_text, str(year)] if value))
        rows.append(
            f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>'
            f'<span>{meta}</span></li>'
        )
    return "\n".join(rows)


def _related_list(related: list[dict[str, object]]) -> str:
    return "\n".join(
        '<li><a href="{}"><strong>{}</strong><span>{}</span></a></li>'.format(
            html.escape(f"../{item['slug']}/", quote=True),
            html.escape(str(item["title"])),
            html.escape(str(item["title_en"])),
        )
        for item in related
    )


def render_topic_page(
    *,
    topic: dict[str, object],
    related: list[dict[str, object]],
    repo_root: Path,
    site: dict[str, object],
    base_url: str,
    preview: bool,
) -> str:
    repository_url = str(site["repository_url"])
    conclusion, zhihu_html, evidence_html = _article_bodies(repo_root, repository_url, topic)
    citations = topic.get("citations")
    if not isinstance(citations, list) or any(not isinstance(item, dict) for item in citations):
        raise RuntimeError(f"专题 {topic.get('id')} 的引用列表非法。")
    citation_urls = [str(item["url"]) for item in citations]
    canonical = _canonical_url(base_url, str(topic["canonical_path"]))
    social_image = _asset_url(base_url, str(site["social_image"]))
    description = _description(topic)
    keywords = [
        str(topic["title_en"]),
        str(topic["field_en"]),
        "embodied AI",
        "robot learning",
        "literature review",
    ]
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": str(topic["title"]),
        "alternateName": str(topic["title_en"]),
        "datePublished": str(topic["date"]),
        "dateModified": str(topic["date"]),
        "inLanguage": str(site["language"]),
        "publisher": {"@type": str(site["publisher_type"]), "name": str(site["publisher_name"])},
        "keywords": keywords,
        "citation": citation_urls,
        "isPartOf": {"@type": "WebSite", "name": str(site["name"]), "url": f"{base_url}/"},
        "mainEntityOfPage": canonical,
        "image": social_image,
    }
    interactive_base = f"../../#/topic/{quote(str(topic['id']))}"
    noindex = '<meta name="robots" content="noindex,nofollow">' if preview else ""
    knowledge_ids = ", ".join(str(item) for item in topic.get("knowledge_ids", [])) or "未标注"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(str(topic['title']))}｜Embodied AI Evidence Hub</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="keywords" content="{html.escape(', '.join(keywords), quote=True)}">
  {noindex}
  <link rel="canonical" href="{html.escape(canonical, quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(str(topic['title']), quote=True)}｜Embodied AI Evidence Hub">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{html.escape(canonical, quote=True)}">
  <meta property="og:image" content="{html.escape(social_image, quote=True)}">
  <meta property="og:locale" content="zh_CN">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(str(topic['title']), quote=True)}｜Embodied AI Evidence Hub">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{html.escape(social_image, quote=True)}">
  <script type="application/ld+json">{_safe_json_ld(article_schema)}</script>
  <link rel="stylesheet" href="../../assets/research.css">
</head>
<body>
  <header class="site-header">
    <a class="site-brand" href="../../"><strong>Embodied AI Evidence Hub</strong><span>具身智能证据知识库</span></a>
    <nav aria-label="全站导航"><a href="../">专题目录</a><a href="../../knowledge-map/">知识图谱</a><a href="{html.escape(repository_url, quote=True)}">GitHub</a></nav>
  </header>
  <main>
    <article>
      <header class="research-header">
        <p class="eyebrow">{html.escape(str(topic['field']))} · {html.escape(str(topic['field_en']))}</p>
        <h1>{html.escape(str(topic['title']))}</h1>
        <p class="title-en" lang="en">{html.escape(str(topic['title_en']))}</p>
        <p class="updated">更新于 <time datetime="{html.escape(str(topic['date']), quote=True)}">{html.escape(str(topic['date']))}</time></p>
      </header>
      <section class="quick-answer" aria-labelledby="quick-answer-title">
        <p class="eyebrow">30 秒结论</p>
        <h2 id="quick-answer-title">先读这个判断</h2>
        <p>{html.escape(conclusion)}</p>
      </section>
      <dl class="evidence-metrics">
        <div><dt>精读论文</dt><dd>{int(topic['paper_count'])}</dd></div>
        <div><dt>正式证据事件</dt><dd>{int(topic['evidence_event_count'])}</dd></div>
        <div><dt>知识单元</dt><dd>{html.escape(knowledge_ids)}</dd></div>
        <div><dt>审计状态</dt><dd>当前结算 run 已通过仓库校验</dd></div>
      </dl>
      <section class="article-content" aria-labelledby="article-title">
        <p class="eyebrow">知乎解释版 · 完整正文</p>
        <h2 id="article-title">研究综述</h2>
        <div class="markdown-body">{zhihu_html}</div>
      </section>
      <section class="paper-references" aria-labelledby="paper-references-title">
        <p class="eyebrow">Accepted evidence</p>
        <h2 id="paper-references-title">去重论文引用</h2>
        <ol>{_citation_list(citations)}</ol>
      </section>
      <details class="evidence-appendix" id="evidence">
        <summary>完整证据附录（{int(topic['evidence_event_count'])} 条正式证据事件）</summary>
        <div class="markdown-body">{evidence_html}</div>
      </details>
      <section class="reading-versions" aria-labelledby="reading-versions-title">
        <p class="eyebrow">Interactive Wiki</p>
        <h2 id="reading-versions-title">进入交互阅读</h2>
        <p>静态页以知乎解释版承接搜索意图；科研版、知乎版和小红书版在同一交互 Wiki 中切换，不建立相互竞争的索引页。</p>
        <div class="button-row">
          <a class="ai-entry" href="{interactive_base}?version=zhihu&amp;ai=1">用 AI 继续研究</a>
          <a href="{interactive_base}?version=keyan">科研备忘录</a>
          <a href="{interactive_base}?version=zhihu">知乎解释版</a>
          <a href="{interactive_base}?version=xiaohongshu">小红书版</a>
        </div>
      </section>
      <section class="method-note" aria-labelledby="method-note-title">
        <p class="eyebrow">Method and limits</p>
        <h2 id="method-note-title">研究方法、证据边界与引用说明</h2>
        <p>本页由当前结算的证据层自动派生，不改写已结算 run。论文只有在完整非 OCR 全文、结构化论文笔记和 claim-support audit 通过后，才进入接受证据。</p>
        <p>页面结论是对所列论文与研究窗口的综合，不等同于无限外推。引用本专题时，请同时保留本页 canonical 地址、访问日期，并在需要时回溯原论文。</p>
      </section>
      <aside class="related" aria-labelledby="related-title">
        <p class="eyebrow">Related research</p>
        <h2 id="related-title">同领域最新专题</h2>
        <ul>{_related_list(related)}</ul>
      </aside>
    </article>
  </main>
  <footer><p>Research → Audit → Evidence · <a href="../../llms.txt">llms.txt</a></p></footer>
</body>
</html>
"""


def _directory_cards(topics: list[dict[str, object]], href_prefix: str) -> str:
    return "\n".join(
        '<article class="research-card" data-topic-id="{topic_id}"><p>{field}</p><h2><a href="{url}">{title}</a></h2>'
        '<span lang="en">{title_en}</span><small>{papers} 篇精读论文 · {events} 条证据事件</small></article>'.format(
            field=html.escape(str(topic["field"])),
            topic_id=html.escape(str(topic["id"]), quote=True),
            url=html.escape(f"{href_prefix}{topic['slug']}/", quote=True),
            title=html.escape(str(topic["title"])),
            title_en=html.escape(str(topic["title_en"])),
            papers=int(topic["paper_count"]),
            events=int(topic["evidence_event_count"]),
        )
        for topic in topics
    )


def render_research_index(
    topics: list[dict[str, object]], site: dict[str, object], base_url: str, preview: bool
) -> str:
    canonical = f"{base_url}/research/"
    noindex = '<meta name="robots" content="noindex,nofollow">' if preview else ""
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>具身智能研究专题目录｜Embodied AI Evidence Hub</title>
<meta name="description" content="38 个具身智能循证研究专题，覆盖 VLA、世界模型、4D 时空推理、机器人数据、多模态感知与闭环评测。">
{noindex}<link rel="canonical" href="{canonical}"><meta property="og:title" content="具身智能研究专题目录｜Embodied AI Evidence Hub">
<meta property="og:description" content="38 个具身智能循证研究专题及其论文、正式证据事件与审计边界。"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{_asset_url(base_url, str(site['social_image']))}"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="../assets/research.css"></head><body>
<header class="site-header"><a class="site-brand" href="../"><strong>Embodied AI Evidence Hub</strong><span>具身智能证据知识库</span></a><nav><a href="../knowledge-map/">知识图谱</a><a href="{site['repository_url']}">GitHub</a></nav></header>
<main class="directory-page"><p class="eyebrow">Research directory</p><h1>具身智能研究专题</h1><p class="lede">每个地址对应一个可独立抓取、可长期引用的中文专题；正文、论文引用与证据附录无需 JavaScript 即可阅读。</p><div class="research-directory">{_directory_cards(topics, '')}</div></main>
<footer><p>Research → Audit → Evidence · <a href="../llms.txt">llms.txt</a></p></footer></body></html>"""


def _inject_homepage(
    template: str,
    topics: list[dict[str, object]],
    site: dict[str, object],
    base_url: str,
    preview: bool,
) -> str:
    canonical = f"{base_url}/"
    website_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": site["name"], "alternateName": site["name_zh"], "url": canonical, "inLanguage": site["language"]},
            {"@type": "Organization", "name": site["publisher_name"], "url": canonical, "sameAs": [site["repository_url"]]},
        ],
    }
    meta = f"""
    {'<meta name="robots" content="noindex,nofollow">' if preview else ''}
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Embodied AI Evidence Hub｜具身智能证据知识库">
    <meta property="og:description" content="{INDEX_DESCRIPTION}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{_asset_url(base_url, str(site['social_image']))}">
    <meta name="twitter:card" content="summary_large_image">
    <script type="application/ld+json">{_safe_json_ld(website_schema)}</script>"""
    directory = _directory_cards(topics, "research/")
    if "<!-- SITE_HEAD_METADATA -->" not in template or "<!-- STATIC_RESEARCH_DIRECTORY -->" not in template:
        raise RuntimeError("wiki/index.html 缺少静态站注入标记。")
    value = template.replace("<!-- SITE_HEAD_METADATA -->", meta)
    value = value.replace("<!-- STATIC_RESEARCH_DIRECTORY -->", directory)
    value = re.sub(r"<title>.*?</title>", "<title>Embodied AI Evidence Hub｜具身智能证据知识库</title>", value, count=1)
    value = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{INDEX_DESCRIPTION}">',
        value,
        count=1,
    )
    return value


def _sitemap(topics: list[dict[str, object]], base_url: str) -> str:
    urls = [f"{base_url}/", f"{base_url}/research/"] + [
        _canonical_url(base_url, str(topic["canonical_path"])) for topic in topics
    ]
    rows = "\n".join(f"  <url><loc>{html.escape(url)}</loc></url>" for url in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}\n</urlset>\n'


def _robots(base_url: str, preview: bool) -> str:
    if preview:
        return "User-agent: *\nDisallow: /\n"
    return (
        "User-agent: OAI-SearchBot\nAllow: /\n\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )


def _llms(topics: list[dict[str, object]], base_url: str) -> str:
    rows = "\n".join(
        f"- [{topic['title']} / {topic['title_en']}]({_canonical_url(base_url, str(topic['canonical_path']))})"
        for topic in topics
    )
    return f"""# Embodied AI Evidence Hub / 具身智能证据知识库

> Evidence-first Chinese research hub for embodied AI, robot learning, VLA, world models, multimodal sensing, 4D reasoning, data quality, and evaluation.

## Research method

Each public topic is derived from a settled evidence run. Accepted evidence requires complete non-OCR full text, a validated paper note, and a passing claim-support audit. Static pages expose the full Zhihu explainer, deduplicated paper citations, evidence metrics, and an auditable appendix.

## Canonical directory

- [Homepage]({base_url}/)
- [Research directory]({base_url}/research/)
{rows}

## Reuse and citation

Code and research content have separate licenses. Cite the canonical topic URL and the underlying papers; see the repository CITATION.cff and LICENSES.md for details.
"""


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self._in_json_ld = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "meta":
            self.meta.append(values)
        if tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self.json_ld.append(data)


def validate_site(
    output: Path,
    base_url: str,
    *,
    preview: bool,
    require_knowledge_map: bool = False,
) -> None:
    sitemap_path = output / "sitemap.xml"
    robots_path = output / "robots.txt"
    llms_path = output / "llms.txt"
    for required in [output / "index.html", output / "research" / "index.html", sitemap_path, robots_path, llms_path]:
        if not required.is_file():
            raise RuntimeError(f"静态站缺少文件：{required}")
    tree = ElementTree.parse(sitemap_path)
    locations = [node.text for node in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    if len(locations) != 40 or len(locations) != len(set(locations)):
        raise RuntimeError(f"Sitemap 必须包含 40 个唯一 canonical URL，当前为 {len(locations)}。")
    if any("#" in str(url) or "/knowledge-map/" in str(url) or "/data/" in str(url) for url in locations):
        raise RuntimeError("Sitemap 包含 hash、知识图谱或数据快照地址。")
    robots = _read_text(robots_path)
    if preview:
        if "Disallow: /" not in robots:
            raise RuntimeError("Preview robots.txt 必须禁止抓取。")
    elif "User-agent: OAI-SearchBot\nAllow: /" not in robots or f"Sitemap: {base_url}/sitemap.xml" not in robots:
        raise RuntimeError("生产 robots.txt 未允许 OAI-SearchBot 或未指向 Sitemap。")

    topic_pages = sorted((output / "research").glob("*/index.html"))
    if len(topic_pages) != 38:
        raise RuntimeError(f"静态站必须包含 38 个专题页，当前为 {len(topic_pages)}。")
    canonicals: set[str] = set()
    descriptions: list[str] = []
    for page in topic_pages:
        source = _read_text(page)
        required_fragments = ["<h1>", "知乎解释版 · 完整正文", 'id="evidence"', "去重论文引用", "application/ld+json"]
        missing = [fragment for fragment in required_fragments if fragment not in source]
        if missing:
            raise RuntimeError(f"专题页 {page} 缺少：{', '.join(missing)}")
        if "<script>alert" in source:
            raise RuntimeError(f"专题页包含未转义脚本：{page}")
        canonical_match = re.search(r'<link rel="canonical" href="([^"]+)">', source)
        description_match = re.search(r'<meta name="description" content="([^"]+)">', source)
        if canonical_match is None or description_match is None:
            raise RuntimeError(f"专题页缺少 canonical 或 description：{page}")
        canonical = html.unescape(canonical_match.group(1))
        description = html.unescape(description_match.group(1))
        if canonical in canonicals:
            raise RuntimeError(f"专题页 canonical 重复：{canonical}")
        if not 120 <= len(description) <= 160:
            raise RuntimeError(f"专题页 description 长度应为 120–160，当前 {len(description)}：{page}")
        canonicals.add(canonical)
        descriptions.append(description)
        collector = LinkCollector()
        collector.feed(source)
        for payload in collector.json_ld:
            structured = json.loads(payload)
            citations = structured.get("citation", []) if isinstance(structured, dict) else []
            if len(citations) != len(set(citations)):
                raise RuntimeError(f"JSON-LD citation 未去重：{page}")
        if preview and 'name="robots" content="noindex,nofollow"' not in source:
            raise RuntimeError(f"Preview 专题页缺少 noindex：{page}")
        for href in collector.links:
            parsed = urlsplit(href)
            if parsed.scheme in {"http", "https"}:
                if not _URL_PATTERN.fullmatch(href):
                    raise RuntimeError(f"外部 URL 格式非法：{href}")
                if href.startswith(base_url):
                    relative = unquote(parsed.path[len(urlsplit(base_url).path):]).lstrip("/")
                    target = output / relative
                    if parsed.fragment or "/#/" in href:
                        target = output / "index.html"
                    elif parsed.path.endswith("/"):
                        target = target / "index.html"
                    if parsed.path.endswith("/knowledge-map/") and not require_knowledge_map:
                        continue
                    if not target.exists():
                        raise RuntimeError(f"站内链接目标不存在：{href}")
            elif parsed.scheme == "mailto" or (not parsed.path and parsed.fragment):
                continue
            elif parsed.scheme or parsed.netloc:
                raise RuntimeError(f"不支持的站内链接协议：{href}")
            else:
                target = (page.parent / unquote(parsed.path)).resolve()
                try:
                    target.relative_to(output.resolve())
                except ValueError as exc:
                    raise RuntimeError(f"站内链接越过发布目录：{href}") from exc
                if parsed.path.endswith("/") or not parsed.path:
                    target = target / "index.html"
                if (
                    target == (output / "knowledge-map" / "index.html").resolve()
                    and not require_knowledge_map
                ):
                    continue
                if not target.exists():
                    raise RuntimeError(f"站内链接目标不存在：{href}")
    if len(canonicals) != 38:
        raise RuntimeError("专题页 canonical 数量不等于 38。")

    graph = output / "knowledge-map" / "index.html"
    if require_knowledge_map and not graph.is_file():
        raise RuntimeError("静态站缺少知识图谱页面。")
    if graph.is_file() and 'name="robots" content="noindex,follow"' not in _read_text(graph):
        raise RuntimeError("知识图谱页面缺少 noindex,follow。")


def _copy_verification_files(wiki_root: Path, output: Path) -> None:
    verification = wiki_root / "verification"
    if not verification.is_dir():
        return
    for path in verification.iterdir():
        if path.is_file() and (
            re.fullmatch(r"google[0-9a-z]+\.html", path.name, re.IGNORECASE)
            or path.name == "BingSiteAuth.xml"
        ):
            shutil.copy2(path, output / path.name)


def build_site(
    snapshot_root: Path,
    wiki_root: Path,
    output: Path,
    *,
    base_url: str,
    preview: bool,
) -> dict[str, object]:
    base_url = _base_url(base_url)
    snapshot_dir = resolve_snapshot_directory(snapshot_root)
    manifest = validate_snapshot(snapshot_dir)
    if manifest.get("schema_version") != 2:
        raise RuntimeError("静态研究站只接受 schema v2 快照。")
    topics_meta = manifest.get("topics")
    site = manifest.get("site")
    if not isinstance(topics_meta, list) or len(topics_meta) != 38 or not isinstance(site, dict):
        raise RuntimeError("生产静态站要求 38 个 schema v2 专题及完整站点配置。")
    base_url_config = str(site.get("base_url") or "").rstrip("/")
    if base_url != base_url_config:
        raise RuntimeError(f"构建 base URL 与 site-config.json 不一致：{base_url} != {base_url_config}")

    topics: list[dict[str, object]] = []
    for item in topics_meta:
        if not isinstance(item, dict):
            raise RuntimeError("manifest topics 包含非对象条目。")
        topic = _load_json(snapshot_dir / "topics" / f"{item['id']}.json")
        topics.append(topic)
    topics.sort(key=lambda item: (str(item["date"]), str(item["title"])), reverse=True)

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(wiki_root / "assets", output / "assets")
    shutil.copytree(snapshot_root, output / "data")
    repo_root = wiki_root.resolve().parent

    template = _read_text(wiki_root / "index.html")
    _write_text(output / "index.html", _inject_homepage(template, topics, site, base_url, preview))
    _write_text(output / "research" / "index.html", render_research_index(topics, site, base_url, preview))
    for topic in topics:
        related = [item for item in topics if item["id"] != topic["id"] and item["field"] == topic["field"]][:4]
        if len(related) < 4:
            related.extend(
                item for item in topics if item["id"] != topic["id"] and item not in related
            )
            related = related[:4]
        page = render_topic_page(
            topic=topic,
            related=related,
            repo_root=repo_root,
            site=site,
            base_url=base_url,
            preview=preview,
        )
        _write_text(output / "research" / str(topic["slug"]) / "index.html", page)
        for alias in topic.get("aliases", []):
            alias_url = _canonical_url(base_url, f"/research/{alias}/")
            target = _canonical_url(base_url, str(topic["canonical_path"]))
            redirect = (
                '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
                f'<meta name="robots" content="noindex,follow"><link rel="canonical" href="{target}">'
                f'<meta http-equiv="refresh" content="0;url={target}"><title>专题地址已迁移</title></head>'
                f'<body><p><a href="{target}">本专题已迁移到永久地址</a></p><p>{alias_url}</p></body></html>'
            )
            _write_text(output / "research" / str(alias) / "index.html", redirect)

    _write_text(output / "robots.txt", _robots(base_url, preview))
    _write_text(output / "sitemap.xml", _sitemap(topics, base_url))
    _write_text(output / "llms.txt", _llms(topics, base_url))
    _copy_verification_files(wiki_root, output)
    validate_site(output, base_url, preview=preview)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 schema v2 快照构建可抓取的具身智能研究站")
    parser.add_argument("--snapshot-root", type=Path, default=DEFAULT_SNAPSHOT_ROOT)
    parser.add_argument("--wiki-root", type=Path, default=DEFAULT_WIKI_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--preview", action="store_true", help="输出 noindex,nofollow 的 PR Preview")
    parser.add_argument("--check-only", action="store_true", help="仅复查已有站点输出")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.check_only:
            validate_site(
                args.output,
                _base_url(args.base_url),
                preview=args.preview,
                require_knowledge_map=True,
            )
            print("静态研究站校验通过。")
        else:
            manifest = build_site(
                args.snapshot_root,
                args.wiki_root,
                args.output,
                base_url=args.base_url,
                preview=args.preview,
            )
            print(
                f"静态研究站已生成：{len(manifest['topics'])} 个专题，"
                f"构建时间 {datetime.now().astimezone().isoformat(timespec='seconds')}。"
            )
        return 0
    except (FileNotFoundError, RuntimeError, ValueError, KeyError, json.JSONDecodeError, OSError) as exc:
        print(f"构建失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

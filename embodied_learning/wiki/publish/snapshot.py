"""Build and atomically publish the embodied-AI research Wiki snapshot.

Production builds load the current settled runs routed by the literature-review
catalog. Directory scanning remains available for compatibility and isolated tests.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
import time
import unicodedata
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterator


from embodied_learning.utils.jsonio import atomic_write_json
from embodied_learning.utils.layout import default_kb_root, find_roots
from embodied_learning.wiki.publish.markdown import (
    first_heading,
    markdown_to_plain,
    render_markdown,
    strip_frontmatter,
)
from embodied_learning.knowledge import arxiv_reader
from embodied_learning import locks
from embodied_learning.config import STYLE_TO_FILE
from embodied_learning.wiki.run.catalog import (
    catalog_run_paths,
    load_catalog_runs,
    reader_articles,
)

_REPO_ROOT_CHECKOUT, _SKILLS_ROOT, SCRIPT_DIR = find_roots()
# Historical REPO_ROOT semantics: the scripts dir's parent — the repo root on a
# checkout, site-packages in a wheel (path arithmetic must work in both).
REPO_ROOT = SCRIPT_DIR.parent  # REPO_ROOT cosmetic: KB-relative rendering root on a checkout


# Bare-CLI fallbacks. `--kb-root` selects the local KB (knowledge outputs live
# there, never in the package — a wheel install has no knowledge/ to read).
# Without `--kb-root` the defaults follow the REPO checkout: the public
# deploy (CI's `build-wiki --output wiki/data`) builds the repo catalog with
# the repo's branding config, and a wheel install falls back to the local KB.
# The help text on `wiki.py build-wiki` states this contract; keep them aligned.
DEFAULT_SOURCE = default_kb_root() / "knowledge" / "literature-review-catalog.md"
DEFAULT_OUTPUT = default_kb_root() / "wiki" / "data"
# Branding/SEO config is a repo asset (ships with the wheel), not KB content.
DEFAULT_SITE_CONFIG = REPO_ROOT / "wiki" / "site-config.json"

VERSION_FILES = {
    "keyan": ("科研备忘录", "scientific-memo_keyan.md"),
    "zhihu": ("知乎解释版", "zhihu-explainer_zhihu.md"),
    "xiaohongshu": ("小红书版", "xiaohongshu-post_xiaohongshu.md"),
}
FILE_TO_VERSION = {
    filename: (key, label)
    for key, (label, filename) in VERSION_FILES.items()
}
FILE_TO_VERSION["review-packet.md"] = ("keyan", "研究综述")

FIELD_RULES = (
    ("世界模型与评测", ("世界模型", "world-model", "评测", "evaluation", "仿真")),
    ("数据工程与质量", ("数据", "污染", "质量", "时空一致", "采集", "data-quality", "training-data")),
    ("多模态感知", ("触觉", "力觉", "传感器", "感知", "tactile", "sensor", "多模态")),
    ("VLA 与模型", ("vla", "预训练", "对齐", "language-action", "视觉语言", "基础模型")),
    ("空间智能与导航", ("4d", "空间", "定位", "导航", "视觉定位", "bev")),
    ("跨本体与控制", ("跨本体", "loco", "操作", "原子技能", "控制", "灵巧")),
    ("产业与应用", ("产业", "商业", "智能体技术", "物流", "应用")),
)

# A few early runs used English directory names before the current Chinese
# review titles were established. These aliases make those historical runs part
# of the same version line, so the newer dated run wins automatically.
TOPIC_ALIASES = {
    # 时序深度估计是单目深度估计主题线的第二轮综述（20260924 → 20260928），
    # 两轮合并为一个话题：新轮为基底版本，旧轮发布为 第1轮综述。
    "时序深度估计": "单目深度估计",
    "road-marking-extraction": "地面箭头提取",
    "4d-data-requirements": "4d时空推理对数据的需求",
    "data-quality-contradictions": "具身智能数据质量的主要矛盾",
    "embodied-sensor-perception-error": "具身传感器感知误差",
    "language-action-vision-alignment": "sparse-language-dense-vision-and-continuous-action-alignment-in-vla-systems",
    "tactile-world-model": "触觉世界模型",
}

_DATE_COMPACT = re.compile(r"(?<!\d)(20\d{6})(?!\d)")
_DATE_DASHED = re.compile(r"(?<!\d)(20\d{2})-(\d{2})-(\d{2})(?!\d)")
_READER_SUFFIX = re.compile(r"-reader-v(\d+)$", re.IGNORECASE)
# Repeat-production mark on a run folder (literature-review-<topic>-<date>-v<N>,
# see wiki.run.manifest.run_folder_name). Same topic_key either way so the wiki
# groups the versions as one topic with the newest winning; the folder name and
# run.json `run_version` carry which production it is.
_RUN_VERSION_SUFFIX = re.compile(r"-v(\d+)$")
_ARXIV_URL = re.compile(r"^https?://(?:[a-z0-9-]+\.)?arxiv\.org/", re.IGNORECASE)
# Chat-driven revisions live at <run>/revisions/<style>-v<N>.md (style is a
# VERSION_FILES key); the revision flow never touches the base deliverables.
REVISION_FILE_RE = re.compile(r"^(keyan|zhihu|xiaohongshu)-v(\d+)$")
_PUBLIC_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Candidate:
    directory: Path
    topic_key: str
    date: str
    reader_rank: int
    # Same-day runs tie on the extracted date; the run dir's mtime (settle
    # time) breaks the tie so the actually-newer review wins.
    mtime: float = 0.0
    # Same-topic runs this candidate supersedes (newest-wins grouping); the
    # older runs stay reachable as 第N轮综述 version keys instead of being
    # dropped from the wiki.
    superseded_runs: tuple["Candidate", ...] = ()
    article_files: tuple[str, ...] = ()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _revision_index(run_dir: Path) -> dict[str, dict]:
    """version_key -> provenance entry from <run>/revisions/index.json
    (written by the wiki revision flow; the agent itself never writes it)."""
    data = None
    index_path = run_dir / "revisions" / "index.json"
    try:
        data = json.loads(_read_text(index_path))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, list):
        return {}
    return {
        str(entry.get("version_key")): entry
        for entry in data
        if isinstance(entry, dict) and entry.get("version_key")
    }
def _read_json_object(path: Path) -> dict[str, object]:
    value = json.loads(_read_text(path))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON 文件必须是对象：{path}")
    return value


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def extract_date(name: str) -> str:
    matches: list[tuple[int, str]] = []
    for match in _DATE_COMPACT.finditer(name):
        raw = match.group(1)
        matches.append((match.start(), f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"))
    for match in _DATE_DASHED.finditer(name):
        matches.append((match.start(), f"{match.group(1)}-{match.group(2)}-{match.group(3)}"))
    return sorted(matches)[-1][1] if matches else "0000-00-00"


def normalize_topic_key(name: str) -> str:
    value = unicodedata.normalize("NFKC", name).lower().strip()
    value = re.sub(r"^literature-review-", "", value)
    value = _READER_SUFFIX.sub("", value)
    value = _RUN_VERSION_SUFFIX.sub("", value)
    value = _DATE_COMPACT.sub("", value)
    value = _DATE_DASHED.sub("", value)
    value = re.sub(r"[_\s]+", "-", value)
    value = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def read_run_topic(directory: Path) -> str | None:
    run_path = directory / "run.json"
    if not run_path.is_file():
        return None
    try:
        topic = json.loads(_read_text(run_path)).get("topic")
    except (json.JSONDecodeError, OSError):
        return None
    return topic.strip() if isinstance(topic, str) and topic.strip() else None


def read_run_manifest(directory: Path) -> dict | None:
    run_path = directory / "run.json"
    if not run_path.is_file():
        return None
    try:
        manifest = json.loads(_read_text(run_path))
    except (json.JSONDecodeError, OSError):
        return None
    return manifest if isinstance(manifest, dict) else None


# Wiki-publishable subset of check_run_bundle.STYLE_TO_FILE (survey/review-packet
# is a briefing, not a reader article); version keys come from the deliverable
# filename via VERSION_FILES, so the mapping lives in one place.
_FILENAME_TO_VERSION_KEY = {filename: key for key, (_, filename) in VERSION_FILES.items()}
_STYLE_VERSION_KEYS = {
    style: _FILENAME_TO_VERSION_KEY[filename]
    for style, filename in STYLE_TO_FILE.items()
    if filename in _FILENAME_TO_VERSION_KEY
}


def topic_identity(directory: Path) -> str:
    key = normalize_topic_key(read_run_topic(directory) or directory.name)
    return TOPIC_ALIASES.get(key, key)


def topic_id(topic_key: str) -> str:
    digest = hashlib.sha1(topic_key.encode("utf-8")).hexdigest()[:12]
    return f"topic-{digest}"


def discover_topics(source: Path) -> tuple[list[Candidate], dict[str, int]]:
    source = source.resolve()
    catalog_mode = source.is_file()
    if catalog_mode:
        root = source.parent.parent
        runs = load_catalog_runs(root, source)
        all_dirs = [item.directory for item in runs]
        catalog_articles = {
            item.directory: reader_articles(item.manifest_path, item.manifest)
            for item in runs
        }
    elif source.is_dir():
        all_dirs = [path for path in source.iterdir() if path.is_dir()]
    else:
        raise FileNotFoundError(f"成果入口不存在：{source}")

    complete: list[Candidate] = []
    for directory in all_dirs:
        # Deliverable contract: three styles by default; a run.json declaring
        # style+scope_note publishes just its own. reader_articles validates the
        # full manifest shape; historical/flat runs without `files` fall back to
        # the style key alone. The declaration is a required minimum, not a cap:
        # extra on-disk deliverables publish too.
        manifest = read_run_manifest(directory) or {}
        declared_style = str(manifest.get("style") or "")
        try:
            declared_files = reader_articles(directory / "run.json", manifest)
        except ValueError:
            if declared_style in STYLE_TO_FILE:
                declared_files = (STYLE_TO_FILE[declared_style],)
            else:
                declared_files = tuple(filename for _, filename in VERSION_FILES.values())
        article_files = tuple(
            filename
            for filename in dict.fromkeys(
                (*declared_files, *(filename for _, filename in VERSION_FILES.values()))
            )
            if (directory / filename).is_file()
        )
        if not all((directory / filename).is_file() for filename in declared_files):
            if catalog_mode:
                raise RuntimeError(f"目录指定的 run 缺少声明成稿：{directory}")
            continue
        reader_match = _READER_SUFFIX.search(directory.name)
        complete.append(
            Candidate(
                directory=directory,
                topic_key=topic_identity(directory),
                date=extract_date(directory.name),
                reader_rank=int(reader_match.group(1)) if reader_match else 0,
                mtime=directory.stat().st_mtime,
                article_files=article_files,
            )
        )

    grouped: dict[str, list[Candidate]] = {}
    for candidate in complete:
        grouped.setdefault(candidate.topic_key, []).append(candidate)

    selected = []
    for items in grouped.values():
        winner = max(items, key=lambda item: (item.date, item.mtime, item.reader_rank, item.directory.name))
        older = sorted(
            (item for item in items if item is not winner),
            key=lambda item: (item.date, item.directory.name),
        )
        selected.append(replace(winner, superseded_runs=tuple(older)))
    selected.sort(key=lambda item: (item.date, item.directory.name), reverse=True)
    stats = {
        "scanned_directories": len(all_dirs),
        "complete_directories": len(complete),
        "published_topics": len(selected),
        "superseded_versions": len(complete) - len(selected),
        "skipped_incomplete": len(all_dirs) - len(complete),
        "source_mode": "catalog" if catalog_mode else "directory",
    }
    return selected, stats


def load_site_config(path: Path, topic_keys: set[str] | None = None) -> dict[str, object]:
    """Load and validate the public URL/brand contract used by production builds."""

    config = _read_json_object(path)
    if config.get("schema_version") != 1:
        raise RuntimeError("site-config.json 只支持 schema_version 1。")
    site = config.get("site")
    fields = config.get("fields")
    topics = config.get("topics")
    if not isinstance(site, dict) or not isinstance(fields, dict) or not isinstance(topics, dict):
        raise RuntimeError("site-config.json 缺少 site、fields 或 topics 对象。")
    required_site = {
        "name",
        "name_zh",
        "language",
        "base_url",
        "repository_url",
        "publisher_type",
        "publisher_name",
        "social_image",
    }
    missing_site = sorted(required_site - set(site))
    if missing_site:
        raise RuntimeError(f"site-config.json 缺少站点字段：{', '.join(missing_site)}")

    seen_routes: dict[str, str] = {}
    for key, value in topics.items():
        if not isinstance(value, dict):
            raise RuntimeError(f"专题发布配置必须是对象：{key}")
        slug = value.get("slug")
        title_en = value.get("title_en")
        aliases = value.get("aliases")
        if not isinstance(slug, str) or not _PUBLIC_SLUG.fullmatch(slug):
            raise RuntimeError(f"专题 {key} 的 slug 非法：{slug}")
        if not isinstance(title_en, str) or not title_en.strip():
            raise RuntimeError(f"专题 {key} 缺少英文标题。")
        if not isinstance(aliases, list) or any(
            not isinstance(alias, str) or not _PUBLIC_SLUG.fullmatch(alias)
            for alias in aliases
        ):
            raise RuntimeError(f"专题 {key} 的 aliases 必须是合法 slug 列表。")
        for route in [slug, *aliases]:
            previous = seen_routes.get(route)
            if previous is not None:
                raise RuntimeError(f"发布地址重复：{route} 同时属于 {previous} 与 {key}")
            seen_routes[route] = key

    if topic_keys is not None:
        configured = set(topics)
        missing = sorted(topic_keys - configured)
        orphaned = sorted(configured - topic_keys)
        if missing:
            raise RuntimeError(f"以下当前专题缺少发布配置：{', '.join(missing)}")
        if orphaned:
            raise RuntimeError(f"以下发布配置未对应当前专题：{', '.join(orphaned)}")
    return config


def _evidence_paths(directory: Path, run: dict[str, object]) -> list[Path]:
    files = run.get("files")
    if not isinstance(files, dict):
        raise RuntimeError(f"run.json 缺少 files 对象：{directory}")
    raw_paths: list[str] = []
    evidence = files.get("evidence")
    reused = files.get("reused_evidence", [])
    if isinstance(evidence, str):
        raw_paths.append(evidence)
    elif isinstance(evidence, list):
        raw_paths.extend(str(item) for item in evidence)
    if isinstance(reused, list):
        raw_paths.extend(str(item) for item in reused)
    paths = [directory / value for value in raw_paths]
    missing = [str(path) for path in paths if not path.is_file()]
    if not paths or missing:
        detail = ", ".join(missing) if missing else "未声明 evidence 文件"
        raise RuntimeError(f"无法读取专题证据：{directory}（{detail}）")
    return paths


def collect_evidence_metadata(directory: Path) -> dict[str, object]:
    """Return validated counts and URL-deduplicated paper citations for one run."""

    run = _read_json_object(directory / "run.json")
    events: dict[str, dict[str, object]] = {}
    for path in _evidence_paths(directory, run):
        for line_number, line in enumerate(_read_text(path).splitlines(), start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            if not isinstance(event, dict) or not event.get("event_id"):
                raise RuntimeError(f"证据事件缺少 event_id：{path}:{line_number}")
            events.setdefault(str(event["event_id"]), event)

    declared_count = run.get("event_count")
    if not isinstance(declared_count, int) or declared_count != len(events):
        raise RuntimeError(
            f"{directory.name} 的 event_count={declared_count}，"
            f"但证据文件去重后为 {len(events)}。"
        )

    citations_by_url: dict[str, dict[str, object]] = {}
    for event in events.values():
        paper = event.get("paper")
        if not isinstance(paper, dict):
            continue
        url = paper.get("url")
        if not isinstance(url, str) or not re.match(r"^https?://", url):
            continue
        authors = event.get("authors")
        author_names = []
        if isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict) and isinstance(author.get("name"), str):
                    author_names.append(str(author["name"]))
        published = str(paper.get("published") or "")
        citations_by_url.setdefault(
            url,
            {
                "title": str(paper.get("title") or url),
                "authors": author_names,
                "published": published,
                "year": published[:4] if re.match(r"^\d{4}", published) else None,
                "url": url,
            },
        )

    files = run.get("files")
    reading_summary_name = files.get("reading_summary") if isinstance(files, dict) else None
    reading_summary_path = directory / (
        str(reading_summary_name) if isinstance(reading_summary_name, str) else "reading-summary.json"
    )
    paper_count = len(citations_by_url)
    if reading_summary_path.is_file():
        reading_summary = _read_json_object(reading_summary_path)
        accepted_count = reading_summary.get("accepted_evidence_paper_count")
        if not isinstance(accepted_count, int) or accepted_count < 0:
            raise RuntimeError(f"reading-summary.json 缺少有效精读论文数：{directory}")
        paper_count = accepted_count

    knowledge_ids = run.get("knowledge_ids", [])
    if not isinstance(knowledge_ids, list) or any(not isinstance(item, str) for item in knowledge_ids):
        raise RuntimeError(f"run.json 的 knowledge_ids 必须是字符串列表：{directory}")
    return {
        "knowledge_ids": knowledge_ids,
        "paper_count": paper_count,
        "evidence_event_count": len(events),
        "citations": sorted(citations_by_url.values(), key=lambda item: str(item["title"]).lower()),
    }


def excerpt(markdown: str, limit: int = 150) -> str:
    paragraphs = re.split(r"\n\s*\n", strip_frontmatter(markdown))
    for paragraph in paragraphs:
        plain = markdown_to_plain(paragraph)
        if plain and not paragraph.lstrip().startswith("#") and len(plain) >= 24:
            return plain[:limit].rstrip() + ("…" if len(plain) > limit else "")
    plain = markdown_to_plain(markdown)
    return plain[:limit].rstrip() + ("…" if len(plain) > limit else "")


def get_topic_title(directory: Path, default_markdown: str) -> str:
    topic = read_run_topic(directory)
    if topic:
        return topic
    heading = first_heading(default_markdown)
    if heading:
        return heading
    name = re.sub(r"^literature-review-", "", directory.name)
    name = _READER_SUFFIX.sub("", name)
    name = _RUN_VERSION_SUFFIX.sub("", name)
    name = _DATE_COMPACT.sub("", name)
    name = _DATE_DASHED.sub("", name)
    return name.replace("-", " ").strip()


def classify_field(title: str, directory_name: str) -> str:
    haystack = f"{title} {directory_name}".lower()
    scores = [
        (sum(1 for keyword in keywords if keyword.lower() in haystack), field)
        for field, keywords in FIELD_RULES
    ]
    score, field = max(scores, key=lambda item: item[0])
    return field if score else "综合研究"


def _wiki_link(label: str, target: str) -> str:
    safe_label = html.escape(label)
    safe_target = html.escape(target, quote=True)
    if target.startswith(("https://", "http://", "mailto:")):
        link = (
            f'<a href="{safe_target}" target="_blank" '
            f'rel="noopener noreferrer">{safe_label}</a>'
        )
        if _ARXIV_URL.match(target):
            return (
                '<span class="arxiv-reference">'
                '<span class="arxiv-icon" aria-hidden="true">arXiv</span>'
                f"{link}</span>"
            )
        return link
    if target.startswith("#"):
        return f'<a href="{safe_target}">{safe_label}</a>'
    if target.split("#", 1)[0].endswith(("evidence-appendix.md", "review-packet.md")):
        return (
            '<button class="inline-evidence-link" type="button" '
            f'data-open-evidence>{safe_label}</button>'
        )
    return (
        f'<span class="local-ref" title="本地来源：{safe_target}">{safe_label}</span>'
    )


def _wiki_image(alt: str, target: str) -> str:
    safe_alt = html.escape(alt or "本地素材", quote=True)
    if target.startswith(("https://", "http://")):
        return (
            f'<img src="{html.escape(target, quote=True)}" '
            f'alt="{safe_alt}" loading="lazy">'
        )
    return (
        '<span class="local-ref" title="本地图片未随 Wiki 发布">'
        f"〔图片：{safe_alt}〕</span>"
    )


def markdown_to_html(markdown: str) -> tuple[str, list[dict[str, object]]]:
    result = render_markdown(
        markdown,
        link_renderer=_wiki_link,
        image_renderer=_wiki_image,
        heading_ids=True,
        collect_toc=True,
        table_wrapper_class="table-scroll",
    )
    return result.html, result.toc


# Scientific-memo citation markers: ^[1]^ renders to <sup>[1]</sup>. Each
# bracketed number is an individual marker (batch markers like ^[1,2]^ are a
# style violation caught by the writer rubric, not the renderer). Numbers are
# resolved against the document's own References list — every entry carries an
# arXiv link — and rewritten into in-panel reader links.
_RENDERED_SUP_CITATION = re.compile(r"<sup>\[([^\]<]+)\]</sup>")
_REFERENCE_ENTRY = re.compile(
    r"^\s*(\d+)[.)]\s+.*?arxiv\.org/(?:abs|html)/([^\s\]\)#]+)", re.IGNORECASE
)


def _reference_map(markdown: str) -> dict[str, str]:
    """Number → arXiv id from a document's References/参考文献 numbered list."""

    mapping: dict[str, str] = {}
    for line in markdown.splitlines():
        match = _REFERENCE_ENTRY.match(line)
        if match:
            paper_id = arxiv_reader.parse_arxiv_id(match.group(2))
            if paper_id:
                mapping[match.group(1)] = paper_id
    return mapping


def link_citation_superscripts(html_text: str, references: dict[str, str]) -> str:
    """Rewrite <sup>[N]</sup> markers into reader links when N exists in the
    document's reference map. Unresolvable numbers keep plain brackets."""

    def rewrite(match: re.Match) -> str:
        paper_id = references.get(match.group(1).strip())
        if not paper_id:
            return match.group(0)
        return (
            f'<sup class="citation-sup"><a class="citation-link" '
            f'href="/api/reader/{paper_id}" data-arxiv="{html.escape(paper_id, quote=True)}">'
            f"[{match.group(1).strip()}]</a></sup>"
        )

    return _RENDERED_SUP_CITATION.sub(rewrite, html_text)


def build_topic(
    candidate: Candidate,
    publication: dict[str, object] | None = None,
    *,
    field_en: str | None = None,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    # Three styles by default; a run.json declaring a reduced scope publishes
    # only its own deliverable (mirrors check_run_bundle's style gate). The
    # declaration is the required minimum, not a cap: a run may ship extra
    # deliverables (e.g. a memo regenerated alongside an earlier zhihu
    # draft), and every deliverable actually on disk is published.
    manifest = read_run_manifest(candidate.directory) or {}
    declared_style = str(manifest.get("style") or "")

    def version_file(key: str) -> Path:
        return candidate.directory / VERSION_FILES[key][1]

    if declared_style in _STYLE_VERSION_KEYS:
        primary = _STYLE_VERSION_KEYS[declared_style]
        version_keys = [primary] + [
            key for key in VERSION_FILES if key != primary and version_file(key).is_file()
        ]
    else:
        version_keys = [key for key in VERSION_FILES if version_file(key).is_file()] or list(VERSION_FILES)
    markdown_by_version = {
        key: _read_text(candidate.directory / VERSION_FILES[key][1])
        for key in version_keys
    }
    # The declared (primary) style is the reader-facing default; a bare
    # triplet keeps the first on-disk key (zhihu first in VERSION_FILES order
    # only when nothing is declared and all three exist).
    default_version = version_keys[0]
    fallback_markdown = markdown_by_version[default_version]
    title = get_topic_title(candidate.directory, fallback_markdown)
    # When the winner's own topic name needed an alias to reach the canonical
    # line (e.g. an English re-run of a Chinese-titled review), the canonical
    # key is the reader-facing title — the wiki groups by it.
    raw_key = normalize_topic_key(read_run_topic(candidate.directory) or candidate.directory.name)
    if candidate.topic_key and raw_key != candidate.topic_key:
        title = candidate.topic_key
    field = classify_field(title, candidate.directory.name)
    identifier = topic_id(candidate.topic_key)
    versions: dict[str, object] = {}
    search_versions: dict[str, object] = {}

    for key in version_keys:
        label, filename = VERSION_FILES[key]
        markdown = markdown_by_version[key]
        rendered, toc = markdown_to_html(markdown)
        if key == "keyan":
            # Memo citation markers resolve against this document's own
            # References list (number → arXiv id) into in-panel reader links.
            rendered = link_citation_superscripts(rendered, _reference_map(markdown))
        plain = markdown_to_plain(markdown)
        versions[key] = {
            "label": label,
            "article_title": first_heading(markdown) or title,
            "html": rendered,
            # Raw source kept alongside the render so the reader page can
            # export the selected style as Markdown without server support.
            "markdown": markdown,
            "toc": toc,
            "characters": len(plain),
            "source_file": filename,
        }
        search_versions[key] = {
            "label": label,
            "article_title": first_heading(markdown) or title,
            "text": plain,
        }

    # Chat-driven revisions (versions feature): the wiki revision flow writes
    # additive `revisions/<style>-v<N>.md` files into the published run and
    # never touches the base deliverables, so every version stays viewable.
    # Revisions are published as version keys of their own ("keyan-v2"),
    # ordered directly after their base style.
    revision_entries: list[tuple[str, int, Path]] = []
    revisions_dir = candidate.directory / "revisions"
    if revisions_dir.is_dir():
        for path in revisions_dir.glob("*.md"):
            match = REVISION_FILE_RE.match(path.stem)
            if match:
                revision_entries.append((match.group(1), int(match.group(2)), path))
    if revision_entries:
        style_order = {key: index for index, key in enumerate(version_keys)}
        revision_entries.sort(key=lambda item: (style_order.get(item[0], len(style_order)), item[1]))
        revision_meta = _revision_index(candidate.directory)
        for style, number, path in revision_entries:
            key = path.stem
            markdown = _read_text(path)
            rendered, toc = markdown_to_html(markdown)
            if style == "keyan":
                rendered = link_citation_superscripts(rendered, _reference_map(markdown))
            plain = markdown_to_plain(markdown)
            base_label = VERSION_FILES[style][0] if style in VERSION_FILES else style
            meta = revision_meta.get(key) or {}
            versions[key] = {
                "label": f"{base_label} · 修订v{number}",
                "article_title": first_heading(markdown) or title,
                "html": rendered,
                "markdown": markdown,
                "toc": toc,
                "characters": len(plain),
                "source_file": f"revisions/{path.name}",
                "revision": number,
                "based_on": style,
                "request": str(meta.get("request") or ""),
                "created_at": str(meta.get("created_at") or ""),
            }
            search_versions[key] = {
                "label": versions[key]["label"],
                "article_title": versions[key]["article_title"],
                "text": plain,
            }
        ordered: list[str] = []
        for key in version_keys:
            ordered.append(key)
            ordered.extend(path.stem for style, _, path in revision_entries if style == key)
        ordered.extend(
            path.stem for style, _, path in revision_entries if style not in style_order
        )
        version_keys = ordered

    # Superseded same-topic runs (a re-run of the whole review — e.g. the same
    # topic submitted under an English name) become 第N轮综述 versions instead
    # of being dropped by the newest-wins collapse. Numbering is chronological:
    # the oldest superseded run is 第1轮, the winner carries no round suffix.
    for round_index, old in enumerate(candidate.superseded_runs, start=1):
        old_manifest = read_run_manifest(old.directory) or {}
        old_declared = str(old_manifest.get("style") or "")
        if old_declared in _STYLE_VERSION_KEYS:
            old_styles = [_STYLE_VERSION_KEYS[old_declared]]
        else:
            old_styles = [
                key for key in VERSION_FILES if (old.directory / VERSION_FILES[key][1]).is_file()
            ]
        for style in old_styles:
            key = f"{style}-r{round_index}"
            if key in versions:
                continue
            markdown = _read_text(old.directory / VERSION_FILES[style][1])
            rendered, toc = markdown_to_html(markdown)
            if style == "keyan":
                rendered = link_citation_superscripts(rendered, _reference_map(markdown))
            plain = markdown_to_plain(markdown)
            base_label = VERSION_FILES[style][0]
            versions[key] = {
                "label": f"{base_label} · 第{round_index}轮综述",
                "article_title": first_heading(markdown) or title,
                "html": rendered,
                "markdown": markdown,
                "toc": toc,
                "characters": len(plain),
                "source_file": VERSION_FILES[style][1],
                "revision": round_index,
                "based_on": style,
                "cross_run": True,
                "request": f"第{round_index}轮综述 · run {old.directory.name}",
                "run_directory": _relative(old.directory),
            }
            search_versions[key] = {
                "label": versions[key]["label"],
                "article_title": versions[key]["article_title"],
                "text": plain,
            }
            version_keys.append(key)

    # Chat draft documents: the topic chat's survey-*.md convention used to be
    # write-only; each draft now publishes as its own version key so a
    # manually written or agent-drafted 补注/讨论稿 is versioned and switchable.
    for path in sorted(candidate.directory.glob("survey-*.md")):
        key = path.stem
        if key in versions:
            continue
        markdown = _read_text(path)
        rendered, toc = markdown_to_html(markdown)
        # Survey drafts may carry the memo citation contract; harmless when
        # the reference map is empty.
        rendered = link_citation_superscripts(rendered, _reference_map(markdown))
        plain = markdown_to_plain(markdown)
        versions[key] = {
            "label": key.removeprefix("survey-") or key,
            "article_title": first_heading(markdown) or title,
            "html": rendered,
            "markdown": markdown,
            "toc": toc,
            "characters": len(plain),
            "source_file": path.name,
            "survey": True,
        }
        search_versions[key] = {
            "label": versions[key]["label"],
            "article_title": versions[key]["article_title"],
            "text": plain,
        }
        version_keys.append(key)

    evidence_path = candidate.directory / "evidence-appendix.md"
    evidence_kind = "证据附录"
    if not evidence_path.is_file():
        evidence_path = candidate.directory / "review-packet.md"
        evidence_kind = "研究证据包"
    evidence_html = ""
    evidence_toc: list[dict[str, object]] = []
    if evidence_path.is_file():
        evidence_html, evidence_toc = markdown_to_html(_read_text(evidence_path))

    # Run-level slide deck (汇报展示): a compiled reveal.js single file sitting
    # in the run folder. The wiki links to it; the server serves the file.
    deck_available = (candidate.directory / "slide-deck_report.html").is_file()
    public_metadata: dict[str, object] = {}
    if publication is not None:
        public_metadata = collect_evidence_metadata(candidate.directory)
        public_metadata.update(
            {
                "slug": publication["slug"],
                "aliases": publication["aliases"],
                "canonical_path": f"/research/{publication['slug']}/",
                "title_en": publication["title_en"],
                "field_en": field_en or "Embodied AI Research",
            }
        )

    topic = {
        "id": identifier,
        "topic_key": candidate.topic_key,
        "title": title,
        "field": field,
        "date": candidate.date,
        "excerpt": excerpt(fallback_markdown),
        "default_version": default_version,
        "source_directory": _relative(candidate.directory),
        "versions": versions,
        "available_versions": version_keys,
        "slide_deck": {"available": deck_available},
        "evidence": {
            "available": bool(evidence_html),
            "label": evidence_kind,
            "html": evidence_html,
            "toc": evidence_toc,
            "source_file": evidence_path.name if evidence_path.is_file() else None,
        },
        **public_metadata,
    }
    manifest_item = {
        "id": identifier,
        "topic_key": candidate.topic_key,
        "title": title,
        "field": field,
        "date": candidate.date,
        "excerpt": topic["excerpt"],
        "default_version": default_version,
        "available_versions": list(version_keys),
        "evidence_available": bool(evidence_html),
        "slide_deck_available": deck_available,
        **{
            key: public_metadata[key]
            for key in (
                "slug",
                "aliases",
                "canonical_path",
                "title_en",
                "field_en",
                "knowledge_ids",
                "paper_count",
                "evidence_event_count",
            )
            if key in public_metadata
        },
    }
    search_item = {
        "id": identifier,
        "title": title,
        "field": field,
        "date": candidate.date,
        "versions": search_versions,
        **{
            key: public_metadata[key]
            for key in ("title_en", "canonical_path")
            if key in public_metadata
        },
    }
    return topic, manifest_item, search_item


def write_json(path: Path, value: object, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":") if compact else None,
        indent=None if compact else 2,
    )
    path.write_text(payload + "\n", encoding="utf-8")


def build_snapshot(
    source: Path,
    output: Path,
    *,
    site_config: Path | None = None,
) -> dict[str, object]:
    selected, stats = discover_topics(source)
    empty_library = False
    if not selected:
        routed = (
            catalog_run_paths(source.parent.parent, source)
            if source.is_file()
            else [path for path in source.iterdir() if path.is_dir()]
        )
        if routed:
            # Runs exist but none publishes (incomplete triplets): keep the
            # previous snapshot rather than wiping it with an empty one.
            raise RuntimeError("没有发现同时包含三种成稿的完整话题，保留现有快照。")
        # First-run shape: a catalog that routes zero runs publishes a real
        # empty index so a cold-start wiki serves a valid snapshot.
        empty_library = True
    publication_config = (
        load_site_config(site_config, {candidate.topic_key for candidate in selected})
        if site_config is not None
        else None
    )
    configured_topics = publication_config["topics"] if publication_config is not None else {}
    configured_fields = publication_config["fields"] if publication_config is not None else {}

    topics_dir = output / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)
    expected_files: set[str] = set()
    manifest_topics: list[dict[str, object]] = []
    search_topics: list[dict[str, object]] = []

    for candidate in selected:
        publication = configured_topics.get(candidate.topic_key)
        if publication_config is not None and not isinstance(publication, dict):
            raise RuntimeError(f"专题缺少发布配置：{candidate.topic_key}")
        default_file = (
            VERSION_FILES["zhihu"][1]
            if VERSION_FILES["zhihu"][1] in candidate.article_files
            else candidate.article_files[0]
        )
        title_for_field = get_topic_title(candidate.directory, _read_text(candidate.directory / default_file))
        field = classify_field(title_for_field, candidate.directory.name)
        field_en = configured_fields.get(field) if isinstance(configured_fields, dict) else None
        topic, manifest_item, search_item = build_topic(
            candidate,
            publication,
            field_en=str(field_en) if isinstance(field_en, str) else None,
        )
        filename = f"{topic['id']}.json"
        expected_files.add(filename)
        write_json(topics_dir / filename, topic, compact=True)
        manifest_topics.append(manifest_item)
        search_topics.append(search_item)

    for stale in topics_dir.glob("topic-*.json"):
        if stale.name not in expected_files:
            stale.unlink()

    fields: dict[str, int] = {}
    for item in manifest_topics:
        field = str(item["field"])
        fields[field] = fields.get(field, 0) + 1

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    legacy_site = {
        "title": "空间智能研究 Wiki",
        "subtitle": "从科研备忘录到公众解释",
        "default_version": "zhihu",
    }
    public_site = dict(publication_config["site"]) if publication_config is not None else legacy_site
    public_site.update(
        {
            "title": (
                f"{public_site['name']}｜{public_site['name_zh']}"
                if publication_config is not None
                else legacy_site["title"]
            ),
            "subtitle": "Research → Audit → Evidence" if publication_config is not None else legacy_site["subtitle"],
            "default_version": "zhihu",
        }
    )
    manifest = {
        **({"schema_version": 2} if publication_config is not None else {}),
        "site": public_site,
        "generated_at": generated_at,
        "source": _relative(source),
        "stats": stats,
        "fields": [{"name": name, "count": count} for name, count in sorted(fields.items())],
        "topics": manifest_topics,
    }
    if empty_library:
        # Sentinel: validate_snapshot tolerates zero topics only for this
        # first-run shape; a normal publish that loses its topics still fails.
        manifest["empty_library"] = True
    search_index = {"generated_at": generated_at, "topics": search_topics}
    write_json(output / "manifest.json", manifest)
    write_json(output / "search-index.json", search_index, compact=True)
    return manifest


def validate_snapshot(output: Path) -> dict[str, object]:
    manifest_path = output / "manifest.json"
    if not manifest_path.is_file():
        raise RuntimeError(f"缺少发布索引：{manifest_path}")
    manifest = json.loads(_read_text(manifest_path))
    schema_version = manifest.get("schema_version", 1)
    if schema_version not in (1, 2):
        raise RuntimeError(f"不支持的 Wiki 快照 schema_version：{schema_version}")
    topics = manifest.get("topics")
    if not isinstance(topics, list):
        raise RuntimeError("发布索引中没有话题。")
    if not topics and not manifest.get("empty_library"):
        raise RuntimeError("发布索引中没有话题。")
    seen_keys: set[str] = set()
    seen_slugs: set[str] = set()
    expected_topic_files: set[str] = set()
    manifest_ids: list[str] = []
    for item in topics:
        if not isinstance(item, dict):
            raise RuntimeError("发布索引包含非对象话题。")
        identifier = item.get("id")
        key = item.get("topic_key")
        if not identifier or not key:
            raise RuntimeError("发布索引包含缺少 id 或 topic_key 的话题。")
        if key in seen_keys:
            raise RuntimeError(f"发现重复话题版本：{key}")
        seen_keys.add(key)
        if schema_version == 2:
            required = {
                "slug",
                "aliases",
                "canonical_path",
                "title_en",
                "field_en",
                "knowledge_ids",
                "paper_count",
                "evidence_event_count",
                "default_version",
                "available_versions",
            }
            missing = sorted(required - set(item))
            if missing:
                raise RuntimeError(f"{identifier} 缺少 schema v2 字段：{', '.join(missing)}")
            slug = item.get("slug")
            aliases = item.get("aliases")
            if not isinstance(slug, str) or not _PUBLIC_SLUG.fullmatch(slug):
                raise RuntimeError(f"{identifier} 的 slug 非法。")
            if item.get("canonical_path") != f"/research/{slug}/":
                raise RuntimeError(f"{identifier} 的 canonical_path 与 slug 不一致。")
            if slug in seen_slugs:
                raise RuntimeError(f"发布快照包含重复 slug：{slug}")
            seen_slugs.add(slug)
            if not isinstance(aliases, list):
                raise RuntimeError(f"{identifier} 的 aliases 必须是列表。")
            for alias in aliases:
                if not isinstance(alias, str) or not _PUBLIC_SLUG.fullmatch(alias):
                    raise RuntimeError(f"{identifier} 包含非法历史 slug。")
                if alias in seen_slugs:
                    raise RuntimeError(f"发布快照包含重复地址：{alias}")
                seen_slugs.add(alias)
            if not isinstance(item.get("paper_count"), int) or int(item["paper_count"]) < 0:
                raise RuntimeError(f"{identifier} 的 paper_count 非法。")
            if (
                not isinstance(item.get("evidence_event_count"), int)
                or int(item["evidence_event_count"]) < 0
            ):
                raise RuntimeError(f"{identifier} 的 evidence_event_count 非法。")
        topic_path = output / "topics" / f"{identifier}.json"
        if not topic_path.is_file():
            raise RuntimeError(f"专题正文不存在：{topic_path}")
        topic = _read_json_object(topic_path)
        versions = topic.get("versions")
        default_version = item.get("default_version")
        available_versions = item.get("available_versions")
        if not isinstance(versions, dict) or not versions:
            raise RuntimeError(f"{identifier} 没有可发布版本。")
        if default_version not in versions:
            raise RuntimeError(f"{identifier} 的默认版本不存在。")
        if available_versions != list(versions):
            raise RuntimeError(f"{identifier} 的可用版本声明不一致。")
        manifest_ids.append(str(identifier))
        expected_topic_files.add(f"{identifier}.json")
        topic_path = output / "topics" / f"{identifier}.json"
        topic = json.loads(_read_text(topic_path))
        if topic.get("id") != identifier or topic.get("topic_key") != key:
            raise RuntimeError(f"{identifier} 的话题文件与发布索引不一致。")
        versions = topic.get("versions", {})
        available = topic.get("available_versions") or list(VERSION_FILES)
        missing = [key for key in available if key not in versions]
        if missing:
            raise RuntimeError(f"{identifier} 缺少版本：{', '.join(missing)}")
        if schema_version == 2:
            for field in (
                "slug",
                "aliases",
                "canonical_path",
                "title_en",
                "field_en",
                "knowledge_ids",
                "paper_count",
                "evidence_event_count",
                "default_version",
                "available_versions",
            ):
                if topic.get(field) != item.get(field):
                    raise RuntimeError(f"{identifier} 的 {field} 与发布索引不一致。")
            citations = topic.get("citations")
            if not isinstance(citations, list):
                raise RuntimeError(f"{identifier} 缺少论文引用列表。")
            citation_urls = [citation.get("url") for citation in citations if isinstance(citation, dict)]
            if len(citation_urls) != len(citations) or len(citation_urls) != len(set(citation_urls)):
                raise RuntimeError(f"{identifier} 的论文引用 URL 未去重。")
    actual_topic_files = {
        path.name for path in (output / "topics").glob("topic-*.json") if path.is_file()
    }
    if actual_topic_files != expected_topic_files:
        raise RuntimeError("发布索引与话题文件集合不一致。")
    search_path = output / "search-index.json"
    if not search_path.is_file():
        raise RuntimeError("缺少全文搜索索引。")
    search = json.loads(_read_text(search_path))
    search_topics = search.get("topics")
    if not isinstance(search_topics, list):
        raise RuntimeError("全文搜索索引缺少话题列表。")
    search_ids = [str(item.get("id")) for item in search_topics if isinstance(item, dict)]
    if search_ids != manifest_ids:
        raise RuntimeError("全文搜索索引与发布索引的话题顺序或集合不一致。")
    if search.get("generated_at") != manifest.get("generated_at"):
        raise RuntimeError("全文搜索索引与发布索引来自不同快照。")
    return manifest


@contextmanager
def publication_lock(output: Path) -> Iterator[None]:
    """Serialize Wiki snapshot publishers across machines and processes.

    The lock file lives inside the output dir (``<output>/.locks/``) so it is
    shared on the same CIFS mount — the previous /tmp + flock scheme was
    machine-local and let two machines publish simultaneously. O_EXCL
    acquisition, brief bounded wait, stale-steal (see embodied_learning.locks).
    """

    output.mkdir(parents=True, exist_ok=True)
    try:
        wait = float(os.environ.get("EMBODIED_KB_LOCK_WAIT") or 600)
    except ValueError:
        wait = 600.0
    with locks.kb_lock(output, "wiki-publish", wait=wait, stale=1800.0):
        yield


def _snapshot_pointer(output: Path) -> dict[str, object] | None:
    pointer_path = output / "current.json"
    if not pointer_path.is_file():
        return None
    pointer = json.loads(_read_text(pointer_path))
    if not isinstance(pointer, dict):
        raise RuntimeError("Wiki 快照指针必须是 JSON 对象。")
    snapshot_id = pointer.get("snapshot_id")
    base_path = pointer.get("base_path")
    expected = f"snapshots/{snapshot_id}"
    if not isinstance(snapshot_id, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", snapshot_id):
        raise RuntimeError("Wiki 快照指针包含非法 snapshot_id。")
    if base_path != expected:
        raise RuntimeError("Wiki 快照指针的 base_path 与 snapshot_id 不一致。")
    return pointer


def resolve_snapshot_directory(output: Path) -> Path:
    """Resolve the active immutable snapshot, with legacy in-place fallback."""

    output = output.resolve()
    pointer = _snapshot_pointer(output)
    if pointer is None:
        return output
    target = (output / str(pointer["base_path"])).resolve()
    snapshots_root = (output / "snapshots").resolve()
    try:
        target.relative_to(snapshots_root)
    except ValueError as exc:
        raise RuntimeError("Wiki 快照指针越过 snapshots 目录。") from exc
    if not target.is_dir():
        raise RuntimeError(f"Wiki 当前快照不存在：{target}")
    return target


def validate_published_snapshot(output: Path) -> dict[str, object]:
    return validate_snapshot(resolve_snapshot_directory(output))


def activate_snapshot(output: Path, snapshot_id: str) -> dict[str, object]:
    """Validate and atomically switch the public pointer to one snapshot."""

    if not re.fullmatch(r"[A-Za-z0-9._-]+", snapshot_id):
        raise RuntimeError("非法 snapshot_id。")
    snapshot_dir = output / "snapshots" / snapshot_id
    manifest = validate_snapshot(snapshot_dir)
    pointer = {
        "schema_version": 1,
        "snapshot_id": snapshot_id,
        "base_path": f"snapshots/{snapshot_id}",
        "published_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "generated_at": manifest.get("generated_at"),
        "topic_count": len(manifest["topics"]),
    }
    atomic_write_json(output / "current.json", pointer)
    return manifest


def prune_snapshots(output: Path, *, retain: int = 2) -> None:
    """Keep the active snapshot and at least one rollback snapshot.

    A minimum-age floor guards against deleting a snapshot that a Wiki reader
    resolved moments ago (the server re-reads current.json per request but a
    slow request may still be mid-serve): anything younger than the floor
    survives this round and becomes deletable on a later prune.
    """

    try:
        min_age = float(os.environ.get("EMBODIED_KB_PRUNE_MIN_AGE_S") or 600)
    except ValueError:
        min_age = 600
    now = time.time()
    pointer = _snapshot_pointer(output)
    active = str(pointer["snapshot_id"]) if pointer else None
    snapshots_root = output / "snapshots"
    if not snapshots_root.is_dir():
        return
    directories = sorted(
        (path for path in snapshots_root.iterdir() if path.is_dir()),
        key=lambda path: path.name,
        reverse=True,
    )
    keep_count = max(2, retain)
    keep = {path.name for path in directories[:keep_count]}
    if active:
        keep.add(active)
    for directory in directories:
        if directory.name in keep:
            continue
        try:
            age = now - directory.stat().st_mtime
        except OSError:
            continue
        if age < min_age:
            continue  # too fresh to prune safely; a later run removes it
        shutil.rmtree(directory)


def publish_snapshot(
    source: Path,
    output: Path,
    *,
    site_config: Path | None = None,
    retain: int = 2,
    before_activate: Callable[[Path], None] | None = None,
) -> dict[str, object]:
    """Build, validate, and atomically activate a new immutable Wiki snapshot."""

    source = source.resolve()
    output = output.resolve()
    with publication_lock(output):
        snapshots_root = output / "snapshots"
        snapshots_root.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix=".staging-", dir=output))
        final: Path | None = None
        activated = False
        try:
            manifest = build_snapshot(source, stage, site_config=site_config)
            validate_snapshot(stage)
            digest = hashlib.sha256(
                (stage / "manifest.json").read_bytes()
                + (stage / "search-index.json").read_bytes()
            ).hexdigest()[:10]
            timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%f")
            # The uuid suffix rules out cross-machine id collisions (two
            # publishers building identical content in the same microsecond
            # would otherwise fight over one os.replace target).
            snapshot_id = f"{timestamp}-{digest}-{uuid.uuid4().hex[:8]}"
            final = snapshots_root / snapshot_id
            os.replace(stage, final)
            if before_activate:
                before_activate(final)
            activate_snapshot(output, snapshot_id)
            activated = True
            prune_snapshots(output, retain=retain)
            return manifest
        finally:
            if stage.exists():
                shutil.rmtree(stage)
            if final is not None and final.exists() and not activated:
                shutil.rmtree(final)


def resolve_io_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    """Resolve --source/--output per the `wiki.py build-wiki` help contract.

    Explicit flags win. ``--kb-root`` selects the local KB. With neither,
    the repo checkout is the corpus (CI's public deploy); a wheel install
    without a checkout falls back to the local KB.
    """

    kb_root = Path(args.kb_root).resolve() if args.kb_root else None
    if args.source is not None:
        source = args.source
    elif kb_root is not None:
        source = kb_root / "knowledge" / "literature-review-catalog.md"
    else:
        repo_catalog = REPO_ROOT / "knowledge" / "literature-review-catalog.md"
        source = repo_catalog if repo_catalog.is_file() else DEFAULT_SOURCE
    output = args.output or (kb_root / "wiki" / "data" if kb_root else DEFAULT_OUTPUT)
    return source, output


def resolve_site_config(args: argparse.Namespace) -> Path | None:
    """Resolve --site-config per the `wiki.py build-wiki` help contract.

    Explicit flags win. ``--kb-root`` uses that KB's config (a private KB
    publishes schema v1 — no public URL branding — when it has none). With no
    ``--kb-root`` the repo's branding config is the default so the public
    deploy produces a schema v2 snapshot that ``build-site`` accepts.
    """

    if args.site_config is not None:
        return args.site_config
    if args.kb_root is not None:
        candidate = Path(args.kb_root).resolve() / "wiki" / "site-config.json"
        return candidate if candidate.is_file() else None
    return DEFAULT_SITE_CONFIG if DEFAULT_SITE_CONFIG.is_file() else None


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in the dispatcher."""
    try:
        if args.check:
            manifest = validate_published_snapshot(args.output or DEFAULT_OUTPUT)
            print(f"Wiki 快照有效：{len(manifest['topics'])} 个最新完整话题。")
        elif args.activate:
            with publication_lock(args.output or DEFAULT_OUTPUT):
                manifest = activate_snapshot(args.output or DEFAULT_OUTPUT, args.activate)
            print(f"Wiki 已切换到快照 {args.activate}：{len(manifest['topics'])} 个话题。")
        else:
            source, output = resolve_io_paths(args)
            manifest = publish_snapshot(
                source,
                output,
                site_config=resolve_site_config(args),
                retain=args.retain,
            )
            stats = manifest["stats"]
            print(
                "Wiki 已原子发布："
                f"加载 {stats['scanned_directories']} 个 run，"
                f"发布 {stats['published_topics']} 个最新完整话题，"
                f"跳过 {stats['skipped_incomplete']} 个不完整目录。"
            )
        return 0
    except (RuntimeError, ValueError) as exc:
        print(f"构建失败：{exc}", file=sys.stderr)
        # Exit code 3 = "nothing publishable yet" (empty/first-run corpus), so
        # callers (serve_research_wiki) can distinguish it from real failures.
        if "没有发现同时包含三种成稿" in str(exc) or "no run manifests routed" in str(exc):
            return 3
        return 1
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        print(f"构建失败：{exc}", file=sys.stderr)
        return 1

#!/usr/bin/env python3
"""Build and atomically publish the embodied-AI research Wiki snapshot.

Production builds load the current settled runs routed by the literature-review
catalog. Directory scanning remains available for compatibility and isolated tests.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.markdown_semantics import (  # noqa: E402
    first_heading,
    markdown_to_plain,
    render_markdown,
    strip_frontmatter,
)
from lib.review_runs import load_catalog_runs  # noqa: E402


DEFAULT_SOURCE = REPO_ROOT / "knowledge" / "literature-review-catalog.md"
DEFAULT_OUTPUT = REPO_ROOT / "wiki" / "data"
DEFAULT_SITE_CONFIG = REPO_ROOT / "wiki" / "site-config.json"

VERSION_FILES = {
    "keyan": ("科研备忘录", "scientific-memo_keyan.md"),
    "zhihu": ("知乎解释版", "zhihu-explainer_zhihu.md"),
    "xiaohongshu": ("小红书版", "xiaohongshu-post_xiaohongshu.md"),
}

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
    "4d-data-requirements": "4d时空推理对数据的需求",
    "data-quality-contradictions": "具身智能数据质量的主要矛盾",
    "embodied-sensor-perception-error": "具身传感器感知误差",
    "language-action-vision-alignment": "sparse-language-dense-vision-and-continuous-action-alignment-in-vla-systems",
    "tactile-world-model": "触觉世界模型",
}

_DATE_COMPACT = re.compile(r"(?<!\d)(20\d{6})(?!\d)")
_DATE_DASHED = re.compile(r"(?<!\d)(20\d{2})-(\d{2})-(\d{2})(?!\d)")
_READER_SUFFIX = re.compile(r"-reader-v(\d+)$", re.IGNORECASE)
_ARXIV_URL = re.compile(r"^https?://(?:[a-z0-9-]+\.)?arxiv\.org/", re.IGNORECASE)
_PUBLIC_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class Candidate:
    directory: Path
    topic_key: str
    date: str
    reader_rank: int


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        all_dirs = [item.directory for item in load_catalog_runs(root, source)]
    elif source.is_dir():
        all_dirs = [path for path in source.iterdir() if path.is_dir()]
    else:
        raise FileNotFoundError(f"成果入口不存在：{source}")

    complete: list[Candidate] = []
    for directory in all_dirs:
        if not all((directory / filename).is_file() for _, filename in VERSION_FILES.values()):
            if catalog_mode:
                raise RuntimeError(f"目录指定的 run 缺少三种成稿：{directory}")
            continue
        reader_match = _READER_SUFFIX.search(directory.name)
        complete.append(
            Candidate(
                directory=directory,
                topic_key=topic_identity(directory),
                date=extract_date(directory.name),
                reader_rank=int(reader_match.group(1)) if reader_match else 0,
            )
        )

    grouped: dict[str, list[Candidate]] = {}
    for candidate in complete:
        grouped.setdefault(candidate.topic_key, []).append(candidate)

    selected = [
        max(items, key=lambda item: (item.date, item.reader_rank, item.directory.name))
        for items in grouped.values()
    ]
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


def get_topic_title(directory: Path, zhihu_markdown: str) -> str:
    topic = read_run_topic(directory)
    if topic:
        return topic
    heading = first_heading(zhihu_markdown)
    if heading:
        return heading
    name = re.sub(r"^literature-review-", "", directory.name)
    name = _READER_SUFFIX.sub("", name)
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


def build_topic(
    candidate: Candidate,
    publication: dict[str, object] | None = None,
    *,
    field_en: str | None = None,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    markdown_by_version = {
        key: _read_text(candidate.directory / filename)
        for key, (_, filename) in VERSION_FILES.items()
    }
    title = get_topic_title(candidate.directory, markdown_by_version["zhihu"])
    field = classify_field(title, candidate.directory.name)
    identifier = topic_id(candidate.topic_key)
    versions: dict[str, object] = {}
    search_versions: dict[str, object] = {}

    for key, (label, filename) in VERSION_FILES.items():
        markdown = markdown_by_version[key]
        rendered, toc = markdown_to_html(markdown)
        plain = markdown_to_plain(markdown)
        versions[key] = {
            "label": label,
            "article_title": first_heading(markdown) or title,
            "html": rendered,
            "toc": toc,
            "characters": len(plain),
            "source_file": filename,
        }
        search_versions[key] = {
            "label": label,
            "article_title": first_heading(markdown) or title,
            "text": plain,
        }

    evidence_path = candidate.directory / "evidence-appendix.md"
    evidence_kind = "证据附录"
    if not evidence_path.is_file():
        evidence_path = candidate.directory / "review-packet.md"
        evidence_kind = "研究证据包"
    evidence_html = ""
    evidence_toc: list[dict[str, object]] = []
    if evidence_path.is_file():
        evidence_html, evidence_toc = markdown_to_html(_read_text(evidence_path))

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
        "excerpt": excerpt(markdown_by_version["zhihu"]),
        "source_directory": _relative(candidate.directory),
        "versions": versions,
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
        "default_version": "zhihu",
        "evidence_available": bool(evidence_html),
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
    if not selected:
        raise RuntimeError("没有发现同时包含三种成稿的完整话题，保留现有快照。")
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
        title_for_field = get_topic_title(
            candidate.directory,
            _read_text(candidate.directory / VERSION_FILES["zhihu"][1]),
        )
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
    if not isinstance(topics, list) or not topics:
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
        manifest_ids.append(str(identifier))
        expected_topic_files.add(f"{identifier}.json")
        topic_path = output / "topics" / f"{identifier}.json"
        topic = json.loads(_read_text(topic_path))
        if topic.get("id") != identifier or topic.get("topic_key") != key:
            raise RuntimeError(f"{identifier} 的话题文件与发布索引不一致。")
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
            ):
                if topic.get(field) != item.get(field):
                    raise RuntimeError(f"{identifier} 的 {field} 与发布索引不一致。")
            citations = topic.get("citations")
            if not isinstance(citations, list):
                raise RuntimeError(f"{identifier} 缺少论文引用列表。")
            citation_urls = [citation.get("url") for citation in citations if isinstance(citation, dict)]
            if len(citation_urls) != len(citations) or len(citation_urls) != len(set(citation_urls)):
                raise RuntimeError(f"{identifier} 的论文引用 URL 未去重。")
        versions = topic.get("versions", {})
        missing = [key for key in VERSION_FILES if key not in versions]
        if missing:
            raise RuntimeError(f"{identifier} 缺少版本：{', '.join(missing)}")
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
    """Prevent concurrent publishers without leaving a stale process lock."""

    output.mkdir(parents=True, exist_ok=True)
    lock_key = hashlib.sha256(str(output.resolve()).encode("utf-8")).hexdigest()[:20]
    lock_path = Path(tempfile.gettempdir()) / f"research-wiki-publish-{lock_key}.lock"
    handle = lock_path.open("a+", encoding="utf-8")
    locked = False
    try:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            locked = True
        except BlockingIOError as exc:
            raise RuntimeError("已有 Wiki 快照发布正在进行。") from exc
        handle.seek(0)
        handle.truncate()
        handle.write(str(os.getpid()))
        handle.flush()
        yield
    finally:
        if locked:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


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


def _atomic_write_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


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
    _atomic_write_json(output / "current.json", pointer)
    return manifest


def prune_snapshots(output: Path, *, retain: int = 2) -> None:
    """Keep the active snapshot and at least one rollback snapshot."""

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
        if directory.name not in keep:
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
            snapshot_id = f"{timestamp}-{digest}"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="构建空间智能研究 Wiki 的静态内容快照")
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="成果目录 Markdown；也兼容直接扫描目录",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="静态数据输出目录")
    parser.add_argument(
        "--site-config",
        type=Path,
        default=DEFAULT_SITE_CONFIG,
        help="品牌、英文标题与永久 URL 配置",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="只校验当前原子快照")
    action.add_argument("--activate", metavar="SNAPSHOT_ID", help="回滚或切换到已验证快照")
    parser.add_argument("--retain", type=int, default=2, help="至少保留的快照数，默认 2")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.check:
            manifest = validate_published_snapshot(args.output)
            print(f"Wiki 快照有效：{len(manifest['topics'])} 个最新完整话题。")
        elif args.activate:
            with publication_lock(args.output):
                manifest = activate_snapshot(args.output, args.activate)
            print(f"Wiki 已切换到快照 {args.activate}：{len(manifest['topics'])} 个话题。")
        else:
            manifest = publish_snapshot(
                args.source,
                args.output,
                site_config=args.site_config,
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
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError, OSError) as exc:
        print(f"构建失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

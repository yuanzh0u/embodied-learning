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


@dataclass(frozen=True)
class Candidate:
    directory: Path
    topic_key: str
    date: str
    reader_rank: int


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def build_topic(candidate: Candidate) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
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
    }
    search_item = {
        "id": identifier,
        "title": title,
        "field": field,
        "date": candidate.date,
        "versions": search_versions,
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


def build_snapshot(source: Path, output: Path) -> dict[str, object]:
    selected, stats = discover_topics(source)
    if not selected:
        raise RuntimeError("没有发现同时包含三种成稿的完整话题，保留现有快照。")

    topics_dir = output / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)
    expected_files: set[str] = set()
    manifest_topics: list[dict[str, object]] = []
    search_topics: list[dict[str, object]] = []

    for candidate in selected:
        topic, manifest_item, search_item = build_topic(candidate)
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
    manifest = {
        "site": {
            "title": "空间智能研究 Wiki",
            "subtitle": "从科研备忘录到公众解释",
            "default_version": "zhihu",
        },
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
    topics = manifest.get("topics")
    if not isinstance(topics, list) or not topics:
        raise RuntimeError("发布索引中没有话题。")
    seen_keys: set[str] = set()
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
        manifest_ids.append(str(identifier))
        expected_topic_files.add(f"{identifier}.json")
        topic_path = output / "topics" / f"{identifier}.json"
        topic = json.loads(_read_text(topic_path))
        if topic.get("id") != identifier or topic.get("topic_key") != key:
            raise RuntimeError(f"{identifier} 的话题文件与发布索引不一致。")
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
            manifest = build_snapshot(source, stage)
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
            manifest = publish_snapshot(args.source, args.output, retain=args.retain)
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

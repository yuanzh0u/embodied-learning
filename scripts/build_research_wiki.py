#!/usr/bin/env python3
"""Build the static content snapshot for the embodied-AI research Wiki.

The scanner deliberately reads finished writing artifacts only. A topic enters the
snapshot when all three reader versions are present. When multiple directories
represent the same normalized topic, only the newest dated version is published.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "work"
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
_HEADER = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_HR = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})$")
_UL_ITEM = re.compile(r"^[-*+]\s+(.+)$")
_OL_ITEM = re.compile(r"^\d+[.)]\s+(.+)$")
_BLOCKQUOTE = re.compile(r"^>\s?(.*)$")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}.*\|")
_INLINE_LINK = re.compile(r"(?<!!)\[([^\]]+)]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
_INLINE_IMAGE = re.compile(r"!\[([^\]]*)]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
_INLINE_CODE = re.compile(r"`([^`]+)`")
_INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")
_INLINE_STRIKE = re.compile(r"~~(.+?)~~")
_INLINE_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
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
    if not source.is_dir():
        raise FileNotFoundError(f"成果目录不存在：{source}")

    complete: list[Candidate] = []
    all_dirs = [path for path in source.iterdir() if path.is_dir()]
    for directory in all_dirs:
        if not all((directory / filename).is_file() for _, filename in VERSION_FILES.values()):
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
    }
    return selected, stats


def strip_frontmatter(markdown: str) -> str:
    if not markdown.startswith("---\n"):
        return markdown
    end = markdown.find("\n---\n", 4)
    return markdown[end + 5 :] if end >= 0 else markdown


def first_heading(markdown: str) -> str | None:
    for line in strip_frontmatter(markdown).splitlines():
        match = _HEADER.match(line.strip())
        if match:
            return re.sub(r"[*_`]+", "", match.group(2)).strip()
    return None


def markdown_to_plain(markdown: str) -> str:
    text = strip_frontmatter(markdown)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = _INLINE_IMAGE.sub(r"\1", text)
    text = _INLINE_LINK.sub(r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[>*+-]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+[.)]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`~|]", "", text)
    return re.sub(r"\s+", " ", text).strip()


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


def _heading_slug(text: str, used: set[str]) -> str:
    plain = markdown_to_plain(text).lower()
    base = re.sub(r"[^\w\u4e00-\u9fff]+", "-", plain).strip("-") or "section"
    slug = base
    number = 2
    while slug in used:
        slug = f"{base}-{number}"
        number += 1
    used.add(slug)
    return slug


def _inline(text: str) -> str:
    escaped = html.escape(text, quote=True)
    code_tokens: dict[str, str] = {}

    def stash_code(match: re.Match[str]) -> str:
        token = f"@@CODE{len(code_tokens)}@@"
        code_tokens[token] = f"<code>{html.escape(match.group(1))}</code>"
        return token

    escaped = _INLINE_CODE.sub(stash_code, escaped)

    def image_sub(match: re.Match[str]) -> str:
        alt, target = match.group(1), html.unescape(match.group(2))
        if target.startswith(("https://", "http://", "data:image/")):
            return f'<img src="{html.escape(target, quote=True)}" alt="{alt}" loading="lazy">'
        return f'<span class="local-ref" title="本地图片未随 Wiki 发布">〔图片：{alt or "本地素材"}〕</span>'

    def link_sub(match: re.Match[str]) -> str:
        label, target = match.group(1), html.unescape(match.group(2))
        if target.startswith(("https://", "http://", "mailto:")):
            link = f'<a href="{html.escape(target, quote=True)}" target="_blank" rel="noopener noreferrer">{label}</a>'
            if _ARXIV_URL.match(target):
                return f'<span class="arxiv-reference"><span class="arxiv-icon" aria-hidden="true">arXiv</span>{link}</span>'
            return link
        if target.startswith("#"):
            return f'<a href="{html.escape(target, quote=True)}">{label}</a>'
        if target.split("#", 1)[0].endswith(("evidence-appendix.md", "review-packet.md")):
            return f'<button class="inline-evidence-link" type="button" data-open-evidence>{label}</button>'
        return f'<span class="local-ref" title="本地来源：{html.escape(target, quote=True)}">{label}</span>'

    escaped = _INLINE_IMAGE.sub(image_sub, escaped)
    escaped = _INLINE_LINK.sub(link_sub, escaped)
    escaped = _INLINE_BOLD.sub(lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", escaped)
    escaped = _INLINE_STRIKE.sub(r"<del>\1</del>", escaped)
    escaped = _INLINE_ITALIC.sub(r"<em>\1</em>", escaped)
    for token, rendered in code_tokens.items():
        escaped = escaped.replace(token, rendered)
    return escaped


def markdown_to_html(markdown: str) -> tuple[str, list[dict[str, object]]]:
    lines = strip_frontmatter(markdown).splitlines()
    out: list[str] = []
    toc: list[dict[str, object]] = []
    used_slugs: set[str] = set()
    paragraph: list[str] = []
    in_ul = False
    in_ol = False
    index = 0

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_paragraph() -> None:
        if paragraph:
            value = " ".join(part.strip() for part in paragraph).strip()
            if value:
                out.append(f"<p>{_inline(value)}</p>")
            paragraph.clear()

    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists()
            language = stripped[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            language_attr = f' class="language-{html.escape(language, quote=True)}"' if language else ""
            out.append(f"<pre><code{language_attr}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        header = _HEADER.match(stripped)
        if header:
            flush_paragraph()
            close_lists()
            level = len(header.group(1))
            label = header.group(2)
            slug = _heading_slug(label, used_slugs)
            out.append(f'<h{level} id="{slug}">{_inline(label)}</h{level}>')
            if level <= 3:
                toc.append({"id": slug, "label": markdown_to_plain(label), "level": level})
            index += 1
            continue

        if _HR.match(stripped):
            flush_paragraph()
            close_lists()
            out.append("<hr>")
            index += 1
            continue

        if "|" in stripped and index + 1 < len(lines) and _TABLE_SEP.match(lines[index + 1]):
            flush_paragraph()
            close_lists()
            headers = [cell.strip() for cell in stripped.strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            out.append('<div class="table-scroll"><table><thead><tr>')
            out.extend(f"<th>{_inline(cell)}</th>" for cell in headers)
            out.append("</tr></thead><tbody>")
            for row in rows:
                cells = row + [""] * max(0, len(headers) - len(row))
                out.append("<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in cells[: len(headers)]) + "</tr>")
            out.append("</tbody></table></div>")
            continue

        ul_match = _UL_ITEM.match(stripped)
        if ul_match:
            flush_paragraph()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{_inline(ul_match.group(1))}</li>")
            index += 1
            continue

        ol_match = _OL_ITEM.match(stripped)
        if ol_match:
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{_inline(ol_match.group(1))}</li>")
            index += 1
            continue

        quote_match = _BLOCKQUOTE.match(stripped)
        if quote_match:
            flush_paragraph()
            close_lists()
            quote_lines = [quote_match.group(1)]
            index += 1
            while index < len(lines):
                next_match = _BLOCKQUOTE.match(lines[index].strip())
                if not next_match:
                    break
                quote_lines.append(next_match.group(1))
                index += 1
            out.append(f"<blockquote>{_inline(' '.join(quote_lines))}</blockquote>")
            continue

        if not stripped:
            flush_paragraph()
            close_lists()
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    close_lists()
    return "\n".join(out), toc


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
            "title": "具身智能研究 Wiki",
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
    for item in topics:
        identifier = item.get("id")
        key = item.get("topic_key")
        if not identifier or not key:
            raise RuntimeError("发布索引包含缺少 id 或 topic_key 的话题。")
        if key in seen_keys:
            raise RuntimeError(f"发现重复话题版本：{key}")
        seen_keys.add(key)
        topic_path = output / "topics" / f"{identifier}.json"
        topic = json.loads(_read_text(topic_path))
        versions = topic.get("versions", {})
        missing = [key for key in VERSION_FILES if key not in versions]
        if missing:
            raise RuntimeError(f"{identifier} 缺少版本：{', '.join(missing)}")
    search_path = output / "search-index.json"
    if not search_path.is_file():
        raise RuntimeError("缺少全文搜索索引。")
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="构建具身智能研究 Wiki 的静态内容快照")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="成果扫描目录")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="静态数据输出目录")
    parser.add_argument("--check", action="store_true", help="只校验现有发布快照")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.check:
            manifest = validate_snapshot(args.output)
            print(f"Wiki 快照有效：{len(manifest['topics'])} 个最新完整话题。")
        else:
            manifest = build_snapshot(args.source, args.output)
            stats = manifest["stats"]
            print(
                "Wiki 已刷新："
                f"扫描 {stats['scanned_directories']} 个目录，"
                f"发布 {stats['published_topics']} 个最新完整话题，"
                f"跳过 {stats['skipped_incomplete']} 个不完整目录。"
            )
        return 0
    except (FileNotFoundError, RuntimeError, json.JSONDecodeError, OSError) as exc:
        print(f"构建失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

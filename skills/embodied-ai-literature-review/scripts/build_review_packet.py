#!/usr/bin/env python3
"""Build the review packet, evidence appendix, and writing brief from accepted evidence.

This script is a briefing generator, not an author: it renders the audit
packet, the citation-anchor appendix, and a writing brief. The three prose
deliverables (scientific-memo_keyan.md / zhihu-explainer_zhihu.md /
xiaohongshu-post_xiaohongshu.md) are written by the agent from these inputs
and must never be mechanical dumps of the claim map.
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
STANCE_ORDER = ["support", "conditional", "limit", "gap"]
FORMAL_SOURCE_THRESHOLD = 5
DEFAULT_LOOKBACK_MONTHS = 6
STANCE_ZH = {
    "support": "支持",
    "conditional": "条件成立",
    "limit": "限制/负面",
    "gap": "缺口",
}

STYLE_OUTLINES_ZH = {
    "survey": [
        "研究边界与证据范围",
        "概念与问题结构",
        "主要共识",
        "条件、限制与分歧",
        "未解决问题",
        "对后续研究/项目的启发",
    ],
    "related-work": [
        "本地问题定义",
        "相邻工作脉络",
        "已有工作的关键限制",
        "本文/项目的定位",
    ],
    "positioning": [
        "核心主张",
        "现有证据支持什么",
        "现有证据不足在哪里",
        "可验证假设与风险",
    ],
}

DEFAULT_OUTPUT_STYLES = ["scientific-memo", "expert-explainer", "kol-thread"]
STYLE_FILENAME_MAP = {
    "scientific-memo": "scientific-memo_keyan.md",
    "expert-explainer": "zhihu-explainer_zhihu.md",
    "kol-thread": "xiaohongshu-post_xiaohongshu.md",
    "survey": "review-packet.md",
}
STYLE_CHOICES = sorted(set(STYLE_OUTLINES_ZH) | set(DEFAULT_OUTPUT_STYLES) | {"all"})
APPENDIX_FILENAME = "evidence-appendix.md"
BRIEF_FILENAME = "writing-brief.md"
FORMAL_STYLES = set(DEFAULT_OUTPUT_STYLES)
SCAFFOLD_BANNER = (
    "<!-- SCAFFOLD: 机械渲染的证据脚手架,非成稿。 -->\n"
    "> **警告:本文件不是综述成稿。** 它是 claim map 与 stance 分桶的机械渲染,\n"
    "> 仅供对照检查。成稿必须由 LLM 依 `writing-brief.md` 撰写为按论证组织的 prose,\n"
    "> 并保存为不带 `.scaffold` 后缀的正式文件名。\n\n"
)


def scaffold_filename(style: str) -> str:
    base = artifact_filename(style)
    return base[: -len(".md")] + ".scaffold.md" if base.endswith(".md") else base + ".scaffold"


def shift_months(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 + months
    year = month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def default_time_range(today: date | None = None) -> str:
    end = today or date.today()
    start = shift_months(end, -DEFAULT_LOOKBACK_MONTHS)
    return f"{start.isoformat()}..{end.isoformat()}"


def slugify_topic(topic: str) -> str:
    slug = re.sub(r"\s+", "-", topic.strip().lower())
    slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-._")
    return slug[:72] or "review"


def artifact_filename(style: str) -> str:
    return STYLE_FILENAME_MAP.get(style, f"{slugify_topic(style)}.md")


def default_project_dir(work_dir: Path, topic: str, today: date | None = None) -> Path:
    project_day = (today or date.today()).strftime("%Y%m%d")
    base_name = f"literature-review-{slugify_topic(topic)}-{project_day}"
    candidate = work_dir / base_name
    suffix = 2
    while candidate.exists():
        candidate = work_dir / f"{base_name}-{suffix}"
        suffix += 1
    return candidate


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text.replace("|", r"\|")


def truncate(value: Any, limit: int = 180) -> str:
    text = md_escape(value)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def load_events(paths: list[Path]) -> list[dict[str, Any]]:
    """Load and concatenate evidence JSONL from one or more runs.

    De-duplicates by `event_id` so combining several runs' evidence.jsonl does
    not double-count an event that appears in more than one file. The first
    occurrence wins; later duplicates are dropped.
    """
    events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{lineno}: invalid JSONL: {exc}") from exc
                if not isinstance(event, dict):
                    raise ValueError(f"{path}:{lineno}: expected a JSON object")
                event_id = str(event.get("event_id") or "")
                if event_id and event_id in seen_ids:
                    continue
                if event_id:
                    seen_ids.add(event_id)
                event["_input_file"] = str(path)
                event["_input_line"] = lineno
                events.append(event)
    return events


def load_fallback_sources(paths: list[Path]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"{path}: expected a JSON list of fallback source records")
        for index, item in enumerate(data, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"{path}:{index}: expected a JSON object")
            sources.append(item)
    return sources


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    frontmatter = text[4:end]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def extract_section(text: str, heading_fragment: str) -> str:
    lines = text.splitlines()
    capture = False
    captured: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if capture:
                break
            capture = heading_fragment in line
            continue
        if capture:
            captured.append(line)
    return "\n".join(captured).strip()


def bullet_items(section: str, limit: int = 5) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
        elif stripped and not items:
            items.append(stripped)
        if len(items) >= limit:
            break
    return items


def load_topic_cards(paths: list[Path]) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        summary = extract_section(text, "30 秒摘要")
        judgments = bullet_items(extract_section(text, "关键判断"))
        cards.append(
            {
                "path": str(path),
                "id": frontmatter.get("id", path.stem),
                "title": frontmatter.get("title", path.stem),
                "summary": truncate(summary, 360),
                "judgments": [truncate(item, 160) for item in judgments],
            }
        )
    return cards


def load_source_ids(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return []
    ids: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^##\s+(S-[A-Za-z0-9-]+)", line.strip())
        if match:
            ids.append(match.group(1))
    return ids


def authors_summary(event: dict[str, Any], limit: int = 3) -> str:
    authors = event.get("authors") or []
    names: list[str] = []
    if isinstance(authors, list):
        for author in authors[:limit]:
            if isinstance(author, dict):
                names.append(str(author.get("author_key") or author.get("name") or "unknown-author"))
            else:
                names.append(str(author))
    if isinstance(authors, list) and len(authors) > limit:
        names.append("et al.")
    return "; ".join(names) if names else "unlisted"


def institution_summary(event: dict[str, Any]) -> str:
    seen: list[str] = []
    authors = event.get("authors") or []
    if not isinstance(authors, list):
        return "unlisted"
    for author in authors:
        if not isinstance(author, dict):
            continue
        institutions = author.get("institutions") or []
        if not isinstance(institutions, list):
            continue
        for institution in institutions:
            if isinstance(institution, dict):
                name = str(institution.get("name") or "").strip()
                if name and name not in seen:
                    seen.append(name)
    return "; ".join(seen) if seen else "unlisted"


def paper_info(event: dict[str, Any]) -> dict[str, Any]:
    paper = event.get("paper") or {}
    return paper if isinstance(paper, dict) else {}


def paper_key(event: dict[str, Any]) -> str:
    paper = paper_info(event)
    return str(paper.get("arxiv_id") or paper.get("url") or paper.get("title") or event.get("event_id") or "")


def paper_url(paper: dict[str, Any]) -> str:
    """Canonical paper URL: derive from arxiv_id so link label and target stay consistent."""
    arxiv_id = str(paper.get("arxiv_id") or "").strip()
    if arxiv_id:
        return f"https://arxiv.org/abs/{arxiv_id}"
    return str(paper.get("url") or "").strip()


def paper_link(event: dict[str, Any]) -> str:
    """Markdown link for a paper: `[arxiv_id](url)`, degrading to plain text without a URL."""
    paper = paper_info(event)
    label = md_escape(paper.get("arxiv_id") or paper.get("title") or "unknown-paper")
    url = paper_url(paper)
    return f"[{label}]({url})" if url else label


def event_anchor(event_id: str) -> str:
    """GitHub-style anchor for an `### <event_id>` heading in the appendix."""
    return re.sub(r"[^0-9a-z一-鿿-]", "", event_id.lower().replace(" ", "-"))


def event_link(event_id: str) -> str:
    """Markdown link from an in-text event ID to its appendix entry."""
    safe_id = md_escape(event_id)
    return f"[{safe_id}]({APPENDIX_FILENAME}#{event_anchor(event_id)})"


def citation_pair(event: dict[str, Any]) -> str:
    """Brief-facing citation: arXiv paper link first (what articles cite in body text),
    appendix event link second (locator for the writer)."""
    event_id = str(event.get("event_id") or "missing-event-id")
    return f"{paper_link(event)} / {event_link(event_id)}"


def count_paper_level_sources(events: list[dict[str, Any]], fallback_sources: list[dict[str, Any]] | None = None) -> int:
    keys = {paper_key(event) for event in events if paper_key(event)}
    for source in fallback_sources or []:
        if str(source.get("tier") or "") == "paper-level":
            key = str(source.get("url") or source.get("title") or "")
            if key:
                keys.add(key)
    return len(keys)


def render_evidence_sufficiency(events: list[dict[str, Any]], fallback_sources: list[dict[str, Any]] | None = None) -> str:
    count = count_paper_level_sources(events, fallback_sources)
    status = "formal-ready" if events and count >= FORMAL_SOURCE_THRESHOLD else "preliminary"
    lines = [
        f"- Evidence sufficiency: {status}",
        f"- Paper-level sources: {count} / {FORMAL_SOURCE_THRESHOLD}",
    ]
    if status == "preliminary":
        lines.append(f"- Formal outputs are blocked until at least {FORMAL_SOURCE_THRESHOLD} paper-level sources are available.")
    else:
        lines.append("- Formal scientific, expert-explainer, and KOL outputs are allowed by the source-count gate.")
    return "\n".join(lines) + "\n"


def event_sort_key(event: dict[str, Any]) -> tuple[str, int, str, str]:
    stance = str(event.get("stance") or "")
    stance_idx = STANCE_ORDER.index(stance) if stance in STANCE_ORDER else len(STANCE_ORDER)
    paper = paper_info(event)
    return (
        str(event.get("topic_id") or ""),
        stance_idx,
        str(paper.get("published") or ""),
        str(event.get("event_id") or ""),
    )


def render_topic_cards(cards: list[dict[str, Any]]) -> str:
    if not cards:
        return "- No topic cards provided.\n"
    chunks: list[str] = []
    for card in cards:
        chunks.append(f"- `{md_escape(card['id'])}` {md_escape(card['title'])}: {card['summary']}")
        for item in card["judgments"]:
            chunks.append(f"  - {item}")
    return "\n".join(chunks) + "\n"


def render_stance_distribution(events: list[dict[str, Any]]) -> str:
    if not events:
        return "- No evidence events provided.\n"
    counts = Counter(str(event.get("stance") or "unknown") for event in events)
    lines = ["| Stance | Meaning | Events |", "|---|---|---|"]
    for stance in STANCE_ORDER + sorted(set(counts) - set(STANCE_ORDER)):
        if counts.get(stance, 0):
            lines.append(f"| `{stance}` | {STANCE_ZH.get(stance, 'unknown')} | {counts[stance]} |")
    return "\n".join(lines) + "\n"


def render_evidence_core(events: list[dict[str, Any]], source_ids: list[str], linked: bool = False) -> str:
    if not events:
        return "\n".join(
            [
                "- Accepted events: 0",
                "- Stance labels: none",
                "- Confidence labels: none",
                "- Trace IDs: none",
                "- Registered sources: " + (", ".join(f"`{item}`" for item in source_ids[:12]) if source_ids else "not loaded"),
            ]
        ) + "\n"
    stances = sorted({str(event.get("stance") or "unknown") for event in events})
    confidences = sorted({str(event.get("confidence") or "unknown") for event in events})
    trace_ids = [str(event.get("event_id") or "missing-event-id") for event in sorted(events, key=event_sort_key)]
    trace_rendered = (
        ", ".join(event_link(item) for item in trace_ids[:12])
        if linked
        else ", ".join(f"`{item}`" for item in trace_ids[:12])
    )
    lines = [
        f"- Accepted events: {len(events)}",
        "- Stance labels: " + ", ".join(f"`{item}`" for item in stances),
        "- Confidence labels: " + ", ".join(f"`{item}`" for item in confidences),
        "- Trace IDs: " + trace_rendered,
        "- Registered sources: " + (", ".join(f"`{item}`" for item in source_ids[:12]) if source_ids else "not loaded"),
    ]
    return "\n".join(lines) + "\n"


def render_source_gaps(events: list[dict[str, Any]], source_ids: list[str]) -> str:
    gaps: list[str] = []
    if not source_ids:
        gaps.append("- No registered source file was loaded; cite event IDs and mark source-entry gaps before final knowledge-base updates.")
    if not events:
        gaps.append("- No accepted evidence events were loaded; paper-level claims must remain preliminary.")
    if not gaps:
        gaps.append("- No immediate source gaps detected from loaded packet inputs.")
    return "\n".join(gaps) + "\n"


def render_source_tiers(fallback_sources: list[dict[str, Any]]) -> str:
    if not fallback_sources:
        return "- No fallback source-tier records provided.\n"
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source in fallback_sources:
        grouped[str(source.get("tier") or "web-context")].append(source)
    tier_order = ["paper-level", "official-context", "web-context", "social-calibration"]
    chunks = ["- Fallback sources are review-packet context, not Hub evidence JSONL."]
    for tier in tier_order + sorted(set(grouped) - set(tier_order)):
        if tier not in grouped:
            continue
        chunks.append("")
        chunks.append(f"### {tier}")
        for source in grouped[tier]:
            title = md_escape(source.get("title") or "Untitled source")
            url = md_escape(source.get("url") or "")
            chunks.append(f"- {title}" + (f" - {url}" if url else ""))
    return "\n".join(chunks) + "\n"


def render_claim_map(events: list[dict[str, Any]], linked: bool = False) -> str:
    if not events:
        return "- No evidence events provided. Use topic-card claims only as background, or run `$embodied-ai-literature-hub` first.\n"
    lines = [
        "| Event | Topic | Stance | Confidence | Claim | Evidence | Authors | Paper |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for event in sorted(events, key=event_sort_key):
        evidence = event.get("evidence") or {}
        if not isinstance(evidence, dict):
            evidence = {}
        locator = evidence.get("locator")
        summary = evidence.get("summary") or ""
        evidence_cell = truncate(f"{summary} ({locator})" if locator else summary, 220)
        event_id = str(event.get("event_id") or "missing-event-id")
        if linked:
            event_cell = event_link(event_id)
            paper_cell = paper_link(event)
        else:
            event_cell = md_escape(event_id)
            paper = paper_info(event)
            paper_cell = md_escape(paper.get("arxiv_id") or paper.get("title") or "unknown-paper")
        lines.append(
            "| {event_id} | {topic} | `{stance}` | `{confidence}` | {claim} | {evidence} | {authors} | {paper} |".format(
                event_id=event_cell,
                topic=md_escape(event.get("topic_id") or event.get("topic") or "unknown-topic"),
                stance=md_escape(event.get("stance") or "unknown"),
                confidence=md_escape(event.get("confidence") or "unknown"),
                claim=truncate(event.get("claim"), 180),
                evidence=evidence_cell,
                authors=md_escape(authors_summary(event)),
                paper=paper_cell,
            )
        )
    return "\n".join(lines) + "\n"


def render_paper_inventory(events: list[dict[str, Any]]) -> str:
    if not events:
        return "- No accepted paper evidence provided.\n"
    papers: dict[str, dict[str, Any]] = {}
    for event in events:
        paper = paper_info(event)
        key = str(paper.get("arxiv_id") or paper.get("title") or event.get("event_id"))
        record = papers.setdefault(
            key,
            {
                "title": paper.get("title") or "Untitled",
                "published": paper.get("published") or "unknown-date",
                "events": [],
                "stances": set(),
            },
        )
        record["events"].append(str(event.get("event_id") or "missing-event-id"))
        record["stances"].add(str(event.get("stance") or "unknown"))
    lines = ["| Paper | Published | Stances | Events |", "|---|---|---|---|"]
    for key in sorted(papers):
        record = papers[key]
        lines.append(
            f"| {md_escape(key)}: {truncate(record['title'], 120)} | {md_escape(record['published'])} | "
            f"{md_escape(', '.join(sorted(record['stances'])))} | {md_escape('; '.join(record['events']))} |"
        )
    return "\n".join(lines) + "\n"


def render_author_events(events: list[dict[str, Any]]) -> str:
    if not events:
        return "- No author stance events provided.\n"
    lines = ["| Event | Authors | Institutions | Stance | Claim |", "|---|---|---|---|---|"]
    for event in sorted(events, key=event_sort_key):
        lines.append(
            "| {event_id} | {authors} | {institutions} | `{stance}` | {claim} |".format(
                event_id=md_escape(event.get("event_id") or "missing-event-id"),
                authors=md_escape(authors_summary(event)),
                institutions=md_escape(institution_summary(event)),
                stance=md_escape(event.get("stance") or "unknown"),
                claim=truncate(event.get("claim"), 160),
            )
        )
    return "\n".join(lines) + "\n"


def render_synthesis_slots(events: list[dict[str, Any]], linked: bool = False) -> str:
    if not events:
        return "- Draft from topic cards only, and mark paper-level claims as missing evidence.\n"
    by_stance: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in sorted(events, key=event_sort_key):
        by_stance[str(event.get("stance") or "unknown")].append(event)
    labels = {
        "support": "共识/正向证据",
        "conditional": "条件成立",
        "limit": "限制与失败模式",
        "gap": "开放问题",
    }

    def event_ref(event: dict[str, Any]) -> str:
        event_id = str(event.get("event_id") or "missing-event-id")
        return event_link(event_id) if linked else f"`{md_escape(event_id)}`"

    chunks: list[str] = []
    for stance in STANCE_ORDER:
        stance_events = by_stance.get(stance, [])
        if not stance_events:
            continue
        chunks.append(f"### {labels[stance]}")
        for event in stance_events[:8]:
            chunks.append(f"- {event_ref(event)}: {truncate(event.get('claim'), 220)}")
    unknown = [event for stance, values in by_stance.items() if stance not in STANCE_ORDER for event in values]
    if unknown:
        chunks.append("### Unlabeled stance")
        for event in unknown[:8]:
            chunks.append(f"- {event_ref(event)}: {truncate(event.get('claim'), 220)}")
    return "\n".join(chunks) + "\n"


def top_claims(events: list[dict[str, Any]], limit: int = 3) -> list[str]:
    claims: list[str] = []
    for event in sorted(events, key=event_sort_key):
        event_id = str(event.get("event_id") or "missing-event-id")
        claims.append(f"`{md_escape(event_id)}` {truncate(event.get('claim'), 150)}")
        if len(claims) >= limit:
            break
    return claims


def recommend_style(events: list[dict[str, Any]]) -> str:
    if len(events) >= FORMAL_SOURCE_THRESHOLD:
        return "all"
    return "preliminary-packet"


def render_references(events: list[dict[str, Any]]) -> str:
    """Deduplicated reference list with inline Markdown links, sorted by arXiv ID/title."""
    papers: dict[str, dict[str, Any]] = {}
    for event in events:
        paper = paper_info(event)
        key = paper_key(event)
        if key and key not in papers:
            papers[key] = paper
    if not papers:
        return "- No paper-level sources loaded.\n"
    lines = []
    for key in sorted(papers):
        paper = papers[key]
        title = md_escape(paper.get("title") or "Untitled")
        label = md_escape(paper.get("arxiv_id") or key)
        url = paper_url(paper)
        published = md_escape(paper.get("published") or "")
        suffix = f"({published})" if published else ""
        if url:
            lines.append(f"- `{label}` [{title}]({url}) {suffix}".rstrip())
        else:
            lines.append(f"- `{label}` {title} {suffix}".rstrip())
    return "\n".join(lines) + "\n"


def tension_pairs(events: list[dict[str, Any]], limit: int = 8) -> list[str]:
    """Surface support-vs-limit/conditional tensions inside each topic group.

    These pairs are thesis candidates: a real review's central argument usually
    lives where the literature pushes in both directions at once.
    """
    by_topic: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for event in events:
        topic_id = str(event.get("topic_id") or "unknown")
        by_topic[topic_id][str(event.get("stance") or "unknown")].append(event)
    pairs: list[str] = []
    for topic_id in sorted(by_topic):
        stances = by_topic[topic_id]
        positives = stances.get("support", [])
        negatives = stances.get("limit", []) + stances.get("conditional", [])
        for pos in positives:
            if not negatives:
                break
            neg = negatives[len(pairs) % len(negatives)]
            pairs.append(
                f"- `{topic_id}`: {truncate(pos.get('claim'), 120)} ({citation_pair(pos)}) "
                f"⟷ {truncate(neg.get('claim'), 120)} ({citation_pair(neg)})"
            )
            if len(pairs) >= limit:
                return pairs
    return pairs


def render_writing_brief(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    source_ids: list[str],
    time_range: str | None = None,
    fallback_sources: list[dict[str, Any]] | None = None,
) -> str:
    """The writer-facing brief: raw material organized for prose, not for audit."""
    count = count_paper_level_sources(events, fallback_sources)
    caveats = [
        event
        for event in sorted(events, key=event_sort_key)
        if str(event.get("stance")) in {"limit", "conditional", "gap"}
    ]
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in sorted(events, key=event_sort_key):
        by_topic[str(event.get("topic_id") or "unknown")].append(event)
    lines = [
        f"# Writing Brief: {topic}",
        "",
        "> 本文件是写作输入,不是交付物。三篇成稿由 LLM 依此撰写:",
        "> 正文必须是按论证组织的连续 prose;禁止把 claim map 表格当正文;",
        "> 禁止一事件一行/一段;三种风格必须是三个真实读者声音。",
        "> 正文引用一律用 arXiv 论文链接(读者点开即达论文);事件锚点只用于 References/appendix 溯源。",
        "",
        "## 范围",
        "",
        f"- Topic: {topic}",
        f"- Time range: {time_range or 'not provided'}",
        f"- Knowledge IDs: {', '.join(f'`{item}`' for item in knowledge_ids) if knowledge_ids else 'unlisted'}",
        f"- Paper-level sources: {count} / {FORMAL_SOURCE_THRESHOLD}"
        + (" (formal-ready)" if count >= FORMAL_SOURCE_THRESHOLD else " (preliminary — 不足以支撑正式综述)"),
        f"- Accepted events: {len(events)}",
        "",
        "## 中心论点候选(从张力对中提炼,不要照抄)",
        "",
        "综述的中心论点应回答:这批证据合在一起说明了什么矛盾/机制/转变?",
        "以下 support ⟷ limit/conditional 张力对是论点候选的原料:",
        "",
    ]
    pairs = tension_pairs(events)
    lines.extend(pairs if pairs else ["- 证据中没有明显的 stance 张力;考虑以共识+边界作为组织轴。"])
    lines.extend(["", "## 按主题聚类的证据(写作时按论证重组,不要按此顺序罗列)", ""])
    for topic_id in sorted(by_topic):
        group = by_topic[topic_id]
        lines.append(f"### {topic_id} ({len(group)} events)")
        for event in group:
            stance = str(event.get("stance") or "unknown")
            lines.append(f"- [`{stance}`] {truncate(event.get('claim'), 200)} ({citation_pair(event)})")
        lines.append("")
    lines.extend(
        [
            "## 必须保留的 caveat(任何风格都不得丢失或升级)",
            "",
        ]
    )
    if caveats:
        for event in caveats:
            lines.append(
                f"- `{md_escape(event.get('stance'))}` {truncate(event.get('claim'), 200)} ({citation_pair(event)})"
            )
    else:
        lines.append("- 无 limit/conditional/gap 事件;声明证据一致性本身即是 caveat。")
    lines.extend(
        [
            "",
            "## 三种风格的读者与语气",
            "",
            "- `scientific-memo_keyan.md` 研究者读:中心论点 → 派生矛盾/机制(prose 小节) → 可操作框架 → 最短结论。引用密集,每个实质论断带论文链接。",
            "- `zhihu-explainer_zhihu.md` 技术公众读:先破一个具体误区 → 讲机制(用比喻可以,升级 stance 不可以) → 给适用边界 → 延伸阅读。",
            "- `xiaohongshu-post_xiaohongshu.md` 泛兴趣读者:一个钩子 → 3-5 条反常识洞察(每条一句话+论文链接) → 一句可见的 caveat → 一行来源说明。",
            "",
            "## 引用速查",
            "",
            "- **正文引用 = arXiv 论文链接**:`[2606.13877](https://arxiv.org/abs/2606.13877)` 或 `[SIEVE](https://arxiv.org/abs/2607.06442)`。读者点开即达论文。",
            f"- 事件级溯源留给 appendix:成稿正文不放 `{APPENDIX_FILENAME}#...` 事件锚点;需要精确定位(章节/立场/置信)时,读者从 References 或 appendix 查。",
            "- 本简报中每条证据给出 `论文链接 / 事件链接` 对:写作时**取前者入正文**,后者供你核对 locator 与 stance。",
            "- 成稿末尾必须有 `## References` 节(去重论文清单,含链接);"
            + f"完整证据条目在 [{APPENDIX_FILENAME}]({APPENDIX_FILENAME})。",
            "- Registered sources: "
            + (", ".join(f"`{item}`" for item in source_ids[:12]) if source_ids else "not loaded"),
            "",
        ]
    )
    return "\n".join(lines)


def render_evidence_appendix(topic: str, events: list[dict[str, Any]], time_range: str | None = None) -> str:
    """Per-event appendix; each `### <event_id>` heading is the anchor target for in-text event links."""
    lines = [
        f"# Evidence Appendix: {topic}",
        "",
        f"- Time range: {time_range or 'not provided'}",
        f"- Events: {len(events)}",
        "- 每个事件一节,标题即锚点;正文中的 event ID 链接跳转到这里。",
        "",
    ]
    for event in sorted(events, key=event_sort_key):
        event_id = str(event.get("event_id") or "missing-event-id")
        evidence = event.get("evidence") or {}
        if not isinstance(evidence, dict):
            evidence = {}
        lines.extend(
            [
                f"### {event_id}",
                "",
                f"- Claim: {md_escape(event.get('claim'))}",
                f"- Stance: `{md_escape(event.get('stance') or 'unknown')}` | Confidence: `{md_escape(event.get('confidence') or 'unknown')}`",
                f"- Paper: {paper_link(event)} {md_escape(paper_info(event).get('title') or '')}".rstrip(),
                f"- Locator: {md_escape(evidence.get('locator') or 'not recorded')}",
                f"- Evidence: {md_escape(evidence.get('summary') or '')}",
            ]
        )
        quote = str(evidence.get("short_quote") or "").strip()
        if quote:
            lines.append(f"- Quote: “{md_escape(quote)}”")
        authors = authors_summary(event)
        if authors:
            lines.append(f"- Authors: {md_escape(authors)}")
        lines.append("")
    lines.extend(["## References", "", render_references(events).rstrip(), ""])
    return "\n".join(lines)


def render_style_menu(topic: str, events: list[dict[str, Any]], fallback_sources: list[dict[str, Any]] | None = None) -> str:
    count = count_paper_level_sources(events, fallback_sources)
    status = "formal-ready" if events and count >= FORMAL_SOURCE_THRESHOLD else "preliminary"
    claims = top_claims(events)
    lines = [
        f"- Evidence sufficiency: {status}",
        f"- Paper-level sources: {count} / {FORMAL_SOURCE_THRESHOLD}",
        f"- Recommended default: {recommend_style(events)}",
        "- Core claims:",
    ]
    if claims:
        lines.extend(f"  - {claim}" for claim in claims)
    else:
        lines.append("  - No accepted claims loaded yet.")
    lines.extend(
        [
            f"- Scientific memo preview: 《{topic}》研究备忘录: evidence scope, claim map, disagreements, and gaps.",
            f"- Expert explainer preview: TL;DR: {topic} 的关键不在单点结论，而在证据条件和误区拆解。",
            f"- KOL thread preview: {topic}: 先看证据边界，再谈一个可传播的反常识洞察。",
        ]
    )
    return "\n".join(lines) + "\n"


def render_scientific_memo(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    topic_cards: list[dict[str, Any]],
    source_ids: list[str],
    fallback_sources: list[dict[str, Any]] | None = None,
    time_range: str | None = None,
) -> str:
    count = count_paper_level_sources(events)
    if count < FORMAL_SOURCE_THRESHOLD:
        return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, "scientific-memo", fallback_sources, time_range)
    knowledge = ", ".join(f"`{item}`" for item in knowledge_ids) if knowledge_ids else "unlisted"
    lines = [
        f"# {topic}研究备忘录",
        "",
        "## 研究边界与证据范围",
        "",
        f"- Topic: {topic}",
        f"- Time range: {time_range or 'not provided'}",
        f"- Knowledge IDs: {knowledge}",
        f"- Paper-level sources: {count} / {FORMAL_SOURCE_THRESHOLD}",
        "- Output type: scientific-memo",
        "",
        "## Evidence Core",
        "",
        render_evidence_core(events, source_ids, linked=True).rstrip(),
        "",
        "## Claim Map",
        "",
        render_claim_map(events, linked=True).rstrip(),
        "",
        "## 主要综合",
        "",
        render_synthesis_slots(events, linked=True).rstrip(),
        "",
        "## Source Gaps",
        "",
        render_source_gaps(events, source_ids).rstrip(),
        "",
        "## References",
        "",
        render_references(events).rstrip(),
        "",
        f"完整证据条目见 [{APPENDIX_FILENAME}]({APPENDIX_FILENAME})。",
        "",
        "## 研究启发与开放问题",
        "",
        "- Treat support, conditional, limit, and gap events as separate signals before writing topic-card updates.",
        "- Mark cross-event synthesis as `inference` unless a claim is directly backed by an event/source ID.",
        "- Use topic-card update suggestions only after checking source gaps.",
        "",
    ]
    return "\n".join(lines)


def render_expert_explainer(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    topic_cards: list[dict[str, Any]],
    source_ids: list[str],
    fallback_sources: list[dict[str, Any]] | None = None,
    time_range: str | None = None,
) -> str:
    count = count_paper_level_sources(events)
    if count < FORMAL_SOURCE_THRESHOLD:
        return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, "expert-explainer", fallback_sources, time_range)
    lines = [
        f"# {topic}：专家解释帖",
        "",
        "## TL;DR",
        "",
        f"{topic} 不能只看一个漂亮结论，要先看论文级证据、适用条件和失败模式。",
        "",
        "## 检索范围",
        "",
        f"- Time range: {time_range or 'not provided'}",
        f"- Paper-level sources: {count} / {FORMAL_SOURCE_THRESHOLD}",
        "- Output type: expert-explainer",
        "",
        "## 常见误区或争议",
        "",
        "- 把候选论文、项目页或社交讨论当成正文级证据，会高估结论强度。",
        "- 把 `conditional`、`limit`、`gap` 写成共识，会让综述失真。",
        "",
        "## 证据与限制",
        "",
        render_synthesis_slots(events, linked=True).rstrip(),
        "",
        "## Claim Map",
        "",
        render_claim_map(events, linked=True).rstrip(),
        "",
        "## 延伸阅读与可信度",
        "",
        render_evidence_sufficiency(events).rstrip(),
        "",
        render_source_gaps(events, source_ids).rstrip(),
        "",
        "## References",
        "",
        render_references(events).rstrip(),
        "",
        f"完整证据条目见 [{APPENDIX_FILENAME}]({APPENDIX_FILENAME})。",
        "",
    ]
    return "\n".join(lines)


def render_kol_thread(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    topic_cards: list[dict[str, Any]],
    source_ids: list[str],
    fallback_sources: list[dict[str, Any]] | None = None,
    time_range: str | None = None,
) -> str:
    count = count_paper_level_sources(events)
    if count < FORMAL_SOURCE_THRESHOLD:
        return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, "kol-thread", fallback_sources, time_range)
    insight_lines: list[str] = []
    for index, event in enumerate(sorted(events, key=event_sort_key)[:5], start=1):
        event_id = str(event.get("event_id") or "missing-event-id")
        stance = str(event.get("stance") or "unknown")
        insight_lines.append(f"{index}. {truncate(event.get('claim'), 180)} ({event_link(event_id)}; stance: `{stance}`)")
    lines = [
        f"# {topic}：洞察短串",
        "",
        "## Hook",
        "",
        f"{topic} 最容易被讲成一句口号，但真正值钱的信息藏在证据条件里。",
        "",
        "## 证据约束洞察",
        "",
        *insight_lines,
        "",
        "## 边界提醒",
        "",
        "- Strong hook is allowed; stance/confidence cannot be upgraded.",
        "- Any `conditional`, `limit`, or `gap` claim must stay visible in the thread.",
        "",
        "## 依据来源",
        "",
        f"- Time range: {time_range or 'not provided'}",
        "",
        render_evidence_sufficiency(events).rstrip(),
        "",
        render_source_gaps(events, source_ids).rstrip(),
        "",
        "## References",
        "",
        render_references(events).rstrip(),
        "",
        f"完整证据条目见 [{APPENDIX_FILENAME}]({APPENDIX_FILENAME})。",
        "",
    ]
    return "\n".join(lines)


def render_final_output(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    topic_cards: list[dict[str, Any]],
    source_ids: list[str],
    style: str,
    fallback_sources: list[dict[str, Any]] | None = None,
    time_range: str | None = None,
) -> str:
    fallback_sources = fallback_sources or []
    if style == "scientific-memo":
        return render_scientific_memo(topic, knowledge_ids, events, topic_cards, source_ids, fallback_sources, time_range)
    if style == "expert-explainer":
        return render_expert_explainer(topic, knowledge_ids, events, topic_cards, source_ids, fallback_sources, time_range)
    if style == "kol-thread":
        return render_kol_thread(topic, knowledge_ids, events, topic_cards, source_ids, fallback_sources, time_range)
    return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, style, fallback_sources, time_range)


def render_output_artifacts(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    topic_cards: list[dict[str, Any]],
    source_ids: list[str],
    style: str,
    fallback_sources: list[dict[str, Any]] | None = None,
    time_range: str | None = None,
    emit_scaffold: bool = False,
) -> dict[str, str]:
    """Assemble the briefing bundle.

    Default (`style == "all"`): review-packet.md + writing-brief.md +
    evidence-appendix.md — writing inputs, not deliverables. The three prose
    articles are written by the agent from the brief. Mechanical style renders
    are only available as clearly-bannered `*.scaffold.md` files, either via
    emit_scaffold or by requesting a formal style explicitly.
    """

    def brief() -> str:
        return render_writing_brief(topic, knowledge_ids, events, source_ids, time_range, fallback_sources)

    def scaffold(output_style: str) -> str:
        rendered = render_final_output(
            topic, knowledge_ids, events, topic_cards, source_ids, output_style, fallback_sources, time_range
        )
        return SCAFFOLD_BANNER + rendered

    artifacts: dict[str, str] = {}
    if style == "all":
        artifacts["review-packet.md"] = render_packet(
            topic, knowledge_ids, events, topic_cards, source_ids, "survey", fallback_sources, time_range
        )
        artifacts[BRIEF_FILENAME] = brief()
        if events:
            artifacts[APPENDIX_FILENAME] = render_evidence_appendix(topic, events, time_range)
        if emit_scaffold:
            for output_style in DEFAULT_OUTPUT_STYLES:
                artifacts[scaffold_filename(output_style)] = scaffold(output_style)
    elif style in FORMAL_STYLES:
        # Explicit formal style: never emit a file that looks like a finished article.
        artifacts[scaffold_filename(style)] = scaffold(style)
        artifacts[BRIEF_FILENAME] = brief()
        if events:
            artifacts[APPENDIX_FILENAME] = render_evidence_appendix(topic, events, time_range)
    else:
        # survey / related-work / positioning keep their packet-flavored artifact.
        artifacts[artifact_filename(style)] = render_final_output(
            topic, knowledge_ids, events, topic_cards, source_ids, style, fallback_sources, time_range
        )
    return artifacts


def render_outline(style: str) -> str:
    sections = STYLE_OUTLINES_ZH.get(style, STYLE_OUTLINES_ZH["survey"])
    return "\n".join(f"{idx}. {section}" for idx, section in enumerate(sections, start=1)) + "\n"


def render_packet(
    topic: str,
    knowledge_ids: list[str],
    events: list[dict[str, Any]],
    topic_cards: list[dict[str, Any]],
    source_ids: list[str],
    style: str,
    fallback_sources: list[dict[str, Any]] | None = None,
    time_range: str | None = None,
) -> str:
    fallback_sources = fallback_sources or []
    event_topics = sorted({str(event.get("topic_id")) for event in events if event.get("topic_id")})
    knowledge = knowledge_ids or event_topics or [str(card["id"]) for card in topic_cards]
    lines = [
        f"# Review Packet: {topic}",
        "",
        "## Scope",
        "",
        f"- Topic: {topic}",
        f"- Time range: {time_range or 'not provided'}",
        f"- Review style: `{style}`",
        f"- Knowledge IDs: {', '.join(f'`{item}`' for item in knowledge) if knowledge else 'unlisted'}",
        f"- Evidence events: {len(events)}",
        f"- Topic cards: {len(topic_cards)}",
        f"- Registered source IDs available: {', '.join(f'`{item}`' for item in source_ids[:12]) if source_ids else 'not loaded'}",
        "",
        "## Orchestration Contract",
        "",
        "- Main path: planner -> hub -> review packet -> style menu.",
        "- Use `$embodied-ai-query-planner` for topic mapping and query planning.",
        "- Use `$embodied-ai-literature-hub` for retrieval, HTML mining, and evidence promotion.",
        "- This review packet is not a replacement for either upstream Skill.",
        "",
        "## Evidence Core",
        "",
        render_evidence_core(events, source_ids).rstrip(),
        "",
        "## Evidence Sufficiency",
        "",
        render_evidence_sufficiency(events, fallback_sources).rstrip(),
        "",
        "## Source Tiers",
        "",
        render_source_tiers(fallback_sources).rstrip(),
        "",
        "## Topic Card Context",
        "",
        render_topic_cards(topic_cards).rstrip(),
        "",
        "## Stance Distribution",
        "",
        render_stance_distribution(events).rstrip(),
        "",
        "## Accepted Paper Inventory",
        "",
        render_paper_inventory(events).rstrip(),
        "",
        "## Claim Map",
        "",
        render_claim_map(events).rstrip(),
        "",
        "## Author Stance Events",
        "",
        render_author_events(events).rstrip(),
        "",
        "## Synthesis Slots",
        "",
        render_synthesis_slots(events).rstrip(),
        "",
        "## Source Gaps",
        "",
        render_source_gaps(events, source_ids).rstrip(),
        "",
        "## Style Menu",
        "",
        render_style_menu(topic, events, fallback_sources).rstrip(),
        "",
        "## Draft Outline",
        "",
        render_outline(style).rstrip(),
        "",
        "## Traceability Checklist",
        "",
        "- Cite event IDs for paper-specific claims.",
        "- Cite stable source IDs for topic-card background.",
        "- Mark cross-event synthesis as `inference` with a short reason.",
        "- Do not cite candidate-only papers as accepted evidence.",
        "- Open raw sources before using exact wording.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Review topic or question.")
    parser.add_argument("--time-range", help="Review/search time range. Defaults to the most recent six months.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="Knowledge ID such as EA-DATA. Repeatable.")
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Evidence JSONL file. Repeatable.")
    parser.add_argument("--fallback-source-json", action="append", default=[], help="Fallback source-tier JSON file. Repeatable.")
    parser.add_argument("--topic-card", action="append", default=[], help="Topic card Markdown file. Repeatable.")
    parser.add_argument("--source-file", help="Optional knowledge/sources.md file for source ID inventory.")
    parser.add_argument(
        "--style",
        choices=STYLE_CHOICES,
        default="all",
        help=(
            "Review shape. Default 'all' emits the briefing bundle "
            "(review-packet.md + writing-brief.md + evidence-appendix.md); "
            "formal styles emit a *.scaffold.md render, never a finished article."
        ),
    )
    parser.add_argument(
        "--emit-scaffold",
        action="store_true",
        help="With --style all, additionally emit *.scaffold.md mechanical renders of the three formal styles.",
    )
    parser.add_argument("--work-dir", default=str(REPO_ROOT / "work"), help="Directory for default review project folders.")
    parser.add_argument("--output", help="Write Markdown artifact to this path. Use '-' for stdout. Defaults to work/<project>/ when omitted.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    time_range = args.time_range or default_time_range()
    events = load_events([Path(path) for path in args.evidence_jsonl])
    fallback_sources = load_fallback_sources([Path(path) for path in args.fallback_source_json])
    cards = load_topic_cards([Path(path) for path in args.topic_card])
    source_ids = load_source_ids(Path(args.source_file)) if args.source_file else []
    artifacts = render_output_artifacts(
        args.topic,
        args.knowledge_id,
        events,
        cards,
        source_ids,
        args.style,
        fallback_sources,
        time_range,
        emit_scaffold=args.emit_scaffold,
    )

    if args.output == "-":
        if len(artifacts) == 1:
            sys.stdout.write(next(iter(artifacts.values())))
        else:
            for filename, content in artifacts.items():
                sys.stdout.write(f"<!-- {filename} -->\n\n{content}\n\n")
    elif args.output:
        output = Path(args.output)
        if len(artifacts) == 1:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(next(iter(artifacts.values())), encoding="utf-8")
        else:
            output.mkdir(parents=True, exist_ok=True)
            for filename, content in artifacts.items():
                (output / filename).write_text(content, encoding="utf-8")
    else:
        project_dir = default_project_dir(Path(args.work_dir), args.topic)
        project_dir.mkdir(parents=True, exist_ok=True)
        outputs: list[Path] = []
        for filename, content in artifacts.items():
            output = project_dir / filename
            output.write_text(content, encoding="utf-8")
            outputs.append(output)
        if len(outputs) == 1:
            sys.stdout.write(f"Wrote Markdown artifact: {outputs[0]}\n")
        else:
            sys.stdout.write("Wrote Markdown artifacts:\n")
            for output in outputs:
                sys.stdout.write(f"- {output}\n")
        if args.style == "all":
            sys.stdout.write(
                "NEXT: 这些是写作输入,不是综述成稿。请依 writing-brief.md 撰写三篇 prose:\n"
                "scientific-memo_keyan.md / zhihu-explainer_zhihu.md / xiaohongshu-post_xiaohongshu.md\n"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

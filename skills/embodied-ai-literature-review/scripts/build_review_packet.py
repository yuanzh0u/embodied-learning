#!/usr/bin/env python3
"""Build a traceable review packet from embodied-AI evidence artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


STANCE_ORDER = ["support", "conditional", "limit", "gap"]
FORMAL_SOURCE_THRESHOLD = 5
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

STYLE_CHOICES = sorted(set(STYLE_OUTLINES_ZH) | {"scientific-memo", "expert-explainer", "kol-thread"})


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
    events: list[dict[str, Any]] = []
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


def render_evidence_core(events: list[dict[str, Any]], source_ids: list[str]) -> str:
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
    lines = [
        f"- Accepted events: {len(events)}",
        "- Stance labels: " + ", ".join(f"`{item}`" for item in stances),
        "- Confidence labels: " + ", ".join(f"`{item}`" for item in confidences),
        "- Trace IDs: " + ", ".join(f"`{item}`" for item in trace_ids[:12]),
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


def render_claim_map(events: list[dict[str, Any]]) -> str:
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
        paper = paper_info(event)
        paper_cell = paper.get("arxiv_id") or paper.get("title") or "unknown-paper"
        lines.append(
            "| {event_id} | {topic} | `{stance}` | `{confidence}` | {claim} | {evidence} | {authors} | {paper} |".format(
                event_id=md_escape(event.get("event_id") or "missing-event-id"),
                topic=md_escape(event.get("topic_id") or event.get("topic") or "unknown-topic"),
                stance=md_escape(event.get("stance") or "unknown"),
                confidence=md_escape(event.get("confidence") or "unknown"),
                claim=truncate(event.get("claim"), 180),
                evidence=evidence_cell,
                authors=md_escape(authors_summary(event)),
                paper=md_escape(paper_cell),
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


def render_synthesis_slots(events: list[dict[str, Any]]) -> str:
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
    chunks: list[str] = []
    for stance in STANCE_ORDER:
        stance_events = by_stance.get(stance, [])
        if not stance_events:
            continue
        chunks.append(f"### {labels[stance]}")
        for event in stance_events[:8]:
            chunks.append(
                f"- `{md_escape(event.get('event_id') or 'missing-event-id')}`: {truncate(event.get('claim'), 220)}"
            )
    unknown = [event for stance, values in by_stance.items() if stance not in STANCE_ORDER for event in values]
    if unknown:
        chunks.append("### Unlabeled stance")
        for event in unknown[:8]:
            chunks.append(f"- `{md_escape(event.get('event_id') or 'missing-event-id')}`: {truncate(event.get('claim'), 220)}")
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
    stances = {str(event.get("stance") or "") for event in events}
    if {"limit", "conditional", "gap"} & stances:
        return "scientific-memo"
    if len(events) >= FORMAL_SOURCE_THRESHOLD:
        return "scientific-memo"
    return "preliminary-packet"


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
) -> str:
    count = count_paper_level_sources(events)
    if count < FORMAL_SOURCE_THRESHOLD:
        return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, "scientific-memo", fallback_sources)
    knowledge = ", ".join(f"`{item}`" for item in knowledge_ids) if knowledge_ids else "unlisted"
    lines = [
        f"# {topic}研究备忘录",
        "",
        "## 研究边界与证据范围",
        "",
        f"- Topic: {topic}",
        f"- Knowledge IDs: {knowledge}",
        f"- Paper-level sources: {count} / {FORMAL_SOURCE_THRESHOLD}",
        "- Output type: scientific-memo",
        "",
        "## Evidence Core",
        "",
        render_evidence_core(events, source_ids).rstrip(),
        "",
        "## Claim Map",
        "",
        render_claim_map(events).rstrip(),
        "",
        "## 主要综合",
        "",
        render_synthesis_slots(events).rstrip(),
        "",
        "## Source Gaps",
        "",
        render_source_gaps(events, source_ids).rstrip(),
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
) -> str:
    count = count_paper_level_sources(events)
    if count < FORMAL_SOURCE_THRESHOLD:
        return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, "expert-explainer", fallback_sources)
    lines = [
        f"# {topic}：专家解释帖",
        "",
        "## TL;DR",
        "",
        f"{topic} 不能只看一个漂亮结论，要先看论文级证据、适用条件和失败模式。",
        "",
        "## 常见误区或争议",
        "",
        "- 把候选论文、项目页或社交讨论当成正文级证据，会高估结论强度。",
        "- 把 `conditional`、`limit`、`gap` 写成共识，会让综述失真。",
        "",
        "## 证据与限制",
        "",
        render_synthesis_slots(events).rstrip(),
        "",
        "## Claim Map",
        "",
        render_claim_map(events).rstrip(),
        "",
        "## 延伸阅读与可信度",
        "",
        render_evidence_sufficiency(events).rstrip(),
        "",
        render_source_gaps(events, source_ids).rstrip(),
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
) -> str:
    count = count_paper_level_sources(events)
    if count < FORMAL_SOURCE_THRESHOLD:
        return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, "kol-thread", fallback_sources)
    insight_lines: list[str] = []
    for index, event in enumerate(sorted(events, key=event_sort_key)[:5], start=1):
        event_id = str(event.get("event_id") or "missing-event-id")
        stance = str(event.get("stance") or "unknown")
        insight_lines.append(f"{index}. {truncate(event.get('claim'), 180)} (`{event_id}`; stance: `{stance}`)")
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
        render_evidence_sufficiency(events).rstrip(),
        "",
        render_source_gaps(events, source_ids).rstrip(),
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
        return render_scientific_memo(topic, knowledge_ids, events, topic_cards, source_ids, fallback_sources)
    if style == "expert-explainer":
        return render_expert_explainer(topic, knowledge_ids, events, topic_cards, source_ids, fallback_sources)
    if style == "kol-thread":
        return render_kol_thread(topic, knowledge_ids, events, topic_cards, source_ids, fallback_sources)
    return render_packet(topic, knowledge_ids, events, topic_cards, source_ids, style, fallback_sources, time_range)


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
    parser.add_argument("--time-range", help="Required when fallback sources represent new paper discovery.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="Knowledge ID such as EA-DATA. Repeatable.")
    parser.add_argument("--evidence-jsonl", action="append", default=[], help="Evidence JSONL file. Repeatable.")
    parser.add_argument("--fallback-source-json", action="append", default=[], help="Fallback source-tier JSON file. Repeatable.")
    parser.add_argument("--topic-card", action="append", default=[], help="Topic card Markdown file. Repeatable.")
    parser.add_argument("--source-file", help="Optional knowledge/sources.md file for source ID inventory.")
    parser.add_argument("--style", choices=STYLE_CHOICES, default="survey", help="Review shape.")
    parser.add_argument("--output", help="Write Markdown packet to this path; stdout if omitted.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.fallback_source_json and not args.time_range:
        parser.error("--time-range is required when using --fallback-source-json")
    events = load_events([Path(path) for path in args.evidence_jsonl])
    fallback_sources = load_fallback_sources([Path(path) for path in args.fallback_source_json])
    cards = load_topic_cards([Path(path) for path in args.topic_card])
    source_ids = load_source_ids(Path(args.source_file)) if args.source_file else []
    packet = render_final_output(args.topic, args.knowledge_id, events, cards, source_ids, args.style, fallback_sources, args.time_range)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(packet, encoding="utf-8")
    else:
        sys.stdout.write(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

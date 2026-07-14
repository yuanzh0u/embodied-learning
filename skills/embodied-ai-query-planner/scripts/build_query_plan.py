#!/usr/bin/env python3
"""Build structured arXiv query plans for embodied-AI literature discovery."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import sys
from typing import Any

try:
    from query_taxonomy import ALIASES, FAMILY_PLANS, TOPIC_PLANS, infer_keys, normalize_key
except ImportError as exc:  # pragma: no cover - import path failure is surfaced by CLI
    raise SystemExit(f"Unable to import query taxonomy: {exc}") from exc


SOCIAL_SOURCES = {"reddit", "x", "twitter", "x-twitter", "x/twitter"}
DEFAULT_MAX_QUERIES = 50
REVIEW_MODES: dict[str, dict[str, object]] = {
    "rapid": {
        "candidate_floor": 30,
        "full_text_floor": 12,
        "evidence_floor": 8,
        "query_multiplier": 2,
        "minimum_batches": 2,
        "saturation_rounds": 1,
        "max_new_unique_rate": 0.10,
        "minimum_per_dimension": 1,
    },
    "scoping": {
        "candidate_floor": 100,
        "full_text_floor": 35,
        "evidence_floor": 15,
        "query_multiplier": 4,
        "minimum_batches": 3,
        "saturation_rounds": 2,
        "max_new_unique_rate": 0.10,
        "minimum_per_dimension": 3,
    },
    "systematic": {
        "candidate_floor": 200,
        "full_text_floor": 80,
        "evidence_floor": 30,
        "query_multiplier": 6,
        "minimum_batches": 4,
        "saturation_rounds": 2,
        "max_new_unique_rate": 0.05,
        "minimum_per_dimension": 5,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=False, help="Chinese or English embodied-AI topic.")
    parser.add_argument("--knowledge-id", action="append", default=[], help="EA knowledge ID. May be repeated.")
    parser.add_argument("--family", action="append", default=[], help="Specialized query family. May be repeated.")
    parser.add_argument("--start-date", help="Optional YYYY-MM-DD scope metadata.")
    parser.add_argument("--end-date", help="Optional YYYY-MM-DD scope metadata.")
    parser.add_argument("--dynamic-file", action="append", default=[], help="JSON file with LLM/agent dynamic query suggestions. May be repeated.")
    parser.add_argument("--calibration-file", action="append", default=[], help="JSON calibration file. May be repeated.")
    parser.add_argument(
        "--review-mode",
        choices=sorted(REVIEW_MODES),
        default="scoping",
        help="Search-depth contract. Targets are floors, never caps.",
    )
    parser.add_argument("--target-candidates", type=int, help="Override the mode's candidate floor.")
    parser.add_argument("--target-full-text", type=int, help="Override the mode's full-text screening floor.")
    parser.add_argument("--target-evidence", type=int, help="Override the mode's accepted-paper floor.")
    parser.add_argument("--max-queries", type=int, default=DEFAULT_MAX_QUERIES, help="Max arXiv API query entries.")
    parser.add_argument("--output", help="Write JSON plan to this path instead of stdout.")
    parser.add_argument("--markdown-output", help="Write a Markdown review view to this path.")
    parser.add_argument("--list-topics", action="store_true", help="List supported EA topic IDs and exit.")
    parser.add_argument("--list-families", action="store_true", help="List supported specialized families and exit.")
    return parser.parse_args()


def stable_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def list_and_exit(items: dict[str, Any]) -> int:
    for key in sorted(items):
        print(key)
    return 0


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def normalize_requested(value: str) -> str:
    normalized = normalize_key(value)
    if normalized in TOPIC_PLANS or normalized in FAMILY_PLANS:
        return normalized
    alias_value = ALIASES.get(normalized)
    if isinstance(alias_value, tuple) and alias_value:
        return alias_value[0]
    return normalized


def unpack_inferred(value: Any) -> tuple[list[str], list[str], list[str]]:
    """Accept a few taxonomy return shapes so the taxonomy module can stay simple."""
    topics: list[str] = []
    families: list[str] = []
    notes: list[str] = []
    if isinstance(value, dict):
        topics = [str(item) for item in as_list(value.get("knowledge_ids") or value.get("topics"))]
        families = [str(item) for item in as_list(value.get("families"))]
        notes = [str(item) for item in as_list(value.get("notes"))]
    elif isinstance(value, tuple) and len(value) >= 2:
        topics = [str(item) for item in as_list(value[0])]
        families = [str(item) for item in as_list(value[1])]
        if len(value) > 2:
            notes = [str(item) for item in as_list(value[2])]
    else:
        for item in as_list(value):
            key = str(item)
            if key.startswith("EA-"):
                topics.append(key)
            else:
                families.append(key)
    return topics, families, notes


def unique_valid(keys: list[str], valid: set[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for raw in keys:
        key = normalize_requested(raw)
        if key in valid and key not in seen:
            seen.add(key)
            result.append(key)
    return result


def query_entry(raw: dict[str, Any], source_key: str, source_type: str) -> dict[str, Any]:
    entry = {
        "label": str(raw["label"]),
        "tier": str(raw.get("tier", "baseline")),
        "query": str(raw["query"]),
        "why": str(raw.get("why", "")),
        "source_key": source_key,
        "source_type": source_type,
        "channel": "arxiv_api",
    }
    for optional in (
        "suggested_categories",
        "calibration_source",
        "calibration_confidence",
        "dynamic_source",
        "dynamic_confidence",
        "evidence_role",
    ):
        if optional in raw:
            entry[optional] = raw[optional]
    return entry


def browser_query(label: str, query: str, why: str, source_key: str) -> dict[str, str]:
    return {
        "label": label,
        "query": query,
        "why": why,
        "source_key": source_key,
        "channel": "browser_fallback",
    }


def web_query(label: str, query: str, why: str, source_key: str, source_type: str = "web") -> dict[str, str]:
    return {
        "label": label,
        "query": query,
        "why": why,
        "source_key": source_key,
        "source_type": source_type,
        "channel": "web_calibration",
    }


def dedupe_queries(entries: list[dict[str, Any]], max_queries: int) -> list[dict[str, Any]]:
    by_query: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for entry in entries:
        query = str(entry["query"])
        if query not in by_query:
            by_query[query] = dict(entry)
            by_query[query]["merged_labels"] = [entry["label"]]
            order.append(query)
            continue
        existing = by_query[query]
        labels = existing.setdefault("merged_labels", [])
        if entry["label"] not in labels:
            labels.append(entry["label"])
        if entry.get("source_key") and entry["source_key"] not in str(existing.get("source_key", "")).split(","):
            existing["source_key"] = ",".join(filter(None, [str(existing.get("source_key", "")), str(entry["source_key"])]))
    return [by_query[query] for query in order[:max_queries]]


def coverage_group(tier: str) -> str:
    """Collapse query tiers into review-level coverage dimensions."""
    normalized = normalize_key(tier)
    if any(token in normalized for token in ("limit", "failure", "gap", "risk", "burden", "latency")):
        return "limits-and-counterevidence"
    if any(token in normalized for token in ("eval", "benchmark", "validation", "sim-real", "closed-loop")):
        return "evaluation-and-validation"
    if any(token in normalized for token in ("deploy", "production", "recovery", "industrial", "business")):
        return "deployment-and-operations"
    if any(token in normalized for token in ("core", "exact", "named", "quality")):
        return "direct-topic"
    if any(token in normalized for token in ("method", "representation", "interface", "tracking", "sensor")):
        return "mechanisms-and-interfaces"
    return "adjacent-and-transfer"


def build_coverage_dimensions(queries: list[dict[str, Any]], minimum_per_dimension: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[str]] = {}
    for item in queries:
        group = coverage_group(str(item.get("tier") or "baseline"))
        grouped.setdefault(group, []).append(str(item["label"]))
    return [
        {
            "dimension": dimension,
            "query_labels": labels,
            "minimum_unique_candidates": minimum_per_dimension,
        }
        for dimension, labels in grouped.items()
    ]


def search_targets(args: argparse.Namespace, query_count: int) -> dict[str, int]:
    mode = REVIEW_MODES[args.review_mode]
    candidate_floor = max(
        int(mode["candidate_floor"]),
        query_count * int(mode["query_multiplier"]),
    )
    return {
        "candidate_floor": max(1, args.target_candidates or candidate_floor),
        "full_text_floor": max(1, args.target_full_text or int(mode["full_text_floor"])),
        "accepted_paper_floor": max(1, args.target_evidence or int(mode["evidence_floor"])),
    }


def suggested_categories(topic_keys: list[str], family_keys: list[str]) -> list[str]:
    categories: set[str] = set()
    for key in topic_keys:
        for category in TOPIC_PLANS.get(key, {}).get("suggested_categories", []):
            categories.add(str(category))
        for item in TOPIC_PLANS.get(key, {}).get("queries", []):
            for category in item.get("suggested_categories", []):
                categories.add(str(category))
    for key in family_keys:
        for category in FAMILY_PLANS.get(key, {}).get("suggested_categories", []):
            categories.add(str(category))
        for item in FAMILY_PLANS.get(key, {}).get("queries", []):
            for category in item.get("suggested_categories", []):
                categories.add(str(category))
    return sorted(categories)


def load_calibration(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        return {"_error": f"{path}: {exc}"}
    if isinstance(data, list):
        return {"terms": data}
    if isinstance(data, dict):
        return data
    return {"_error": f"{path}: expected JSON object or list"}


def load_json_file(path: str, list_key: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        return {"_error": f"{path}: {exc}"}
    if isinstance(data, list):
        return {list_key: data}
    if isinstance(data, dict):
        return data
    return {"_error": f"{path}: expected JSON object or list"}


def source_confidence(source: str, provided: str | None = None) -> str:
    if provided:
        return provided
    if normalize_key(source) in SOCIAL_SOURCES:
        return "low"
    if normalize_key(source) in {"arxiv", "arxiv-search", "arxiv-html", "arxiv-abs"}:
        return "high"
    if source:
        return "medium"
    return "unknown"


def calibrated_query_from_term(term: str) -> str:
    if " " in term or "-" in term:
        return f'all:"{term}"'
    return f"all:{term}"


def source_label(source: str, default: str) -> str:
    return source or default


def dynamic_confidence(source: str, provided: str | None = None) -> str:
    if provided:
        return provided
    normalized = normalize_key(source)
    if normalized in {"llm", "agent", "model", "assistant"}:
        return "medium"
    if normalized in SOCIAL_SOURCES:
        return "low"
    return "medium"


def merge_dynamic(paths: list[str]) -> tuple[list[str], list[str], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[str], list[dict[str, Any]]]:
    topic_keys: list[str] = []
    family_keys: list[str] = []
    arxiv_entries: list[dict[str, Any]] = []
    browser_entries: list[dict[str, Any]] = []
    web_entries: list[dict[str, Any]] = []
    notes: list[str] = []
    suggestions: list[dict[str, Any]] = []

    for path in paths:
        data = load_json_file(path, "queries")
        if data.get("_error"):
            notes.append(f"Dynamic suggestions unavailable: {data['_error']}")
            continue

        for source in as_list(data.get("sources")):
            if not isinstance(source, dict):
                continue
            src = source_label(str(source.get("source", "")), "llm")
            confidence = dynamic_confidence(src, source.get("confidence"))
            notes.append(f"{src} dynamic expansion ({confidence}): {source.get('notes') or path}")

        topic_keys.extend(str(item) for item in as_list(data.get("knowledge_ids") or data.get("topics")))
        family_keys.extend(str(item) for item in as_list(data.get("families")))

        for index, query_item in enumerate(as_list(data.get("queries")), start=1):
            if not isinstance(query_item, dict) or not query_item.get("query"):
                continue
            source = source_label(str(query_item.get("source", "")), "llm")
            confidence = dynamic_confidence(source, query_item.get("confidence"))
            label = str(query_item.get("label") or f"dynamic-query-{index}")
            entry = {
                "label": label,
                "tier": str(query_item.get("tier", "dynamic-association")),
                "query": str(query_item["query"]),
                "why": str(query_item.get("why", "LLM/agent suggested this adjacent query for broader recall.")),
                "dynamic_source": source,
                "dynamic_confidence": confidence,
                "evidence_role": "query-planning-only",
            }
            arxiv_entries.append(entry)
            suggestions.append(
                {
                    "label": label,
                    "channel": "arxiv_api",
                    "source": source,
                    "confidence": confidence,
                    "query": entry["query"],
                    "why": entry["why"],
                }
            )

        for index, item in enumerate(as_list(data.get("browser_fallback_queries")), start=1):
            if not isinstance(item, dict) or not item.get("query"):
                continue
            label = str(item.get("label") or f"dynamic-browser-{index}")
            source = source_label(str(item.get("source", "")), "llm")
            browser_entries.append(browser_query(label, str(item["query"]), str(item.get("why", "")), "dynamic"))
            suggestions.append(
                {
                    "label": label,
                    "channel": "browser_fallback",
                    "source": source,
                    "confidence": dynamic_confidence(source, item.get("confidence")),
                    "query": str(item["query"]),
                    "why": str(item.get("why", "")),
                }
            )

        for index, item in enumerate(as_list(data.get("web_calibration_queries")), start=1):
            if not isinstance(item, dict) or not item.get("query"):
                continue
            label = str(item.get("label") or f"dynamic-web-calibration-{index}")
            source = source_label(str(item.get("source", "")), "llm")
            web_entries.append(web_query(label, str(item["query"]), str(item.get("why", "")), "dynamic", source))
            suggestions.append(
                {
                    "label": label,
                    "channel": "web_calibration",
                    "source": source,
                    "confidence": dynamic_confidence(source, item.get("confidence")),
                    "query": str(item["query"]),
                    "why": str(item.get("why", "")),
                }
            )

    if paths and not suggestions and not topic_keys and not family_keys:
        notes.append("Dynamic files were provided but contained no usable keys or query suggestions.")
    return topic_keys, family_keys, arxiv_entries, browser_entries, web_entries, notes, suggestions


def merge_calibration(paths: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    arxiv_entries: list[dict[str, Any]] = []
    web_entries: list[dict[str, Any]] = []
    notes: list[str] = []
    for path in paths:
        data = load_calibration(path)
        if data.get("_error"):
            notes.append(f"Calibration unavailable: {data['_error']}")
            continue
        for source in as_list(data.get("sources")):
            if not isinstance(source, dict):
                continue
            src = str(source.get("source", "web"))
            confidence = source_confidence(src, source.get("confidence"))
            notes.append(f"{src} calibration ({confidence}): {source.get('notes') or source.get('url') or path}")
        for term_item in as_list(data.get("terms")):
            if isinstance(term_item, str):
                term_item = {"term": term_item, "source": "manual"}
            if not isinstance(term_item, dict) or not term_item.get("term"):
                continue
            term = str(term_item["term"])
            source = str(term_item.get("source", "manual"))
            confidence = source_confidence(source, term_item.get("confidence"))
            label_term = normalize_key(term).replace("_", "-")
            arxiv_entries.append(
                {
                    "label": f"calibrated-{label_term}",
                    "tier": "calibrated-term",
                    "query": calibrated_query_from_term(term),
                    "why": str(term_item.get("why", f"Search arXiv for calibrated term: {term}.")),
                    "calibration_source": source,
                    "calibration_confidence": confidence,
                    "evidence_role": "query-calibration-only",
                }
            )
            web_entries.append(
                web_query(
                    f"web-calibrated-{label_term}",
                    f'"{term}" robot manipulation arxiv',
                    f"Check whether calibrated term appears in paper-facing web surfaces: {term}.",
                    "calibration",
                    source,
                )
            )
        for query_item in as_list(data.get("queries")):
            if not isinstance(query_item, dict) or not query_item.get("query"):
                continue
            source = str(query_item.get("source", "manual"))
            confidence = source_confidence(source, query_item.get("confidence"))
            arxiv_entries.append(
                {
                    "label": str(query_item.get("label", "calibrated-query")),
                    "tier": str(query_item.get("tier", "calibrated-query")),
                    "query": str(query_item["query"]),
                    "why": str(query_item.get("why", "Search arXiv with an Agent-supplied calibrated query.")),
                    "calibration_source": source,
                    "calibration_confidence": confidence,
                    "evidence_role": "query-calibration-only",
                }
            )
    if paths and not notes:
        notes.append("Calibration files were provided but contained no usable sources, terms, or queries.")
    if not paths:
        notes.append("No live web calibration was provided; generated offline baseline query plan.")
    return arxiv_entries, web_entries, notes


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    topic = args.topic or ""
    inferred_topics, inferred_families, inference_notes = unpack_inferred(infer_keys(topic))
    dynamic_topics, dynamic_families, dynamic_arxiv, dynamic_browser, dynamic_web, dynamic_notes, dynamic_suggestions = merge_dynamic(args.dynamic_file)
    topic_keys = unique_valid([*args.knowledge_id, *inferred_topics, *dynamic_topics], set(TOPIC_PLANS))
    family_keys = unique_valid([*args.family, *inferred_families, *dynamic_families], set(FAMILY_PLANS))

    plan_notes = [*inference_notes, *dynamic_notes]
    if not topic_keys and not family_keys:
        plan_notes.append("No EA topic or specialized family matched; emitted generic embodied-AI topic queries.")

    raw_queries: list[dict[str, Any]] = []
    browser_queries: list[dict[str, Any]] = []
    web_queries: list[dict[str, Any]] = []

    raw_queries.extend(query_entry(item, "dynamic", "dynamic-suggestion") for item in dynamic_arxiv)
    browser_queries.extend(dynamic_browser)
    web_queries.extend(dynamic_web)

    calibrated_arxiv, calibrated_web, calibration_notes = merge_calibration(args.calibration_file)
    raw_queries.extend(query_entry(item, "calibration", "web-calibration") for item in calibrated_arxiv)
    web_queries.extend(calibrated_web)

    for key in family_keys:
        plan = FAMILY_PLANS[key]
        raw_queries.extend(query_entry(item, key, "specialized-family") for item in plan.get("queries", []))
        for item in plan.get("browser_fallback_queries", []):
            browser_queries.append(browser_query(item["label"], item["query"], item.get("why", ""), key))
        for item in plan.get("web_calibration_queries", []):
            web_queries.append(web_query(item["label"], item["query"], item.get("why", ""), key))

    for key in topic_keys:
        plan = TOPIC_PLANS[key]
        raw_queries.extend(query_entry(item, key, "knowledge-topic") for item in plan.get("queries", []))
        for item in plan.get("browser_fallback_queries", []):
            browser_queries.append(browser_query(item["label"], item["query"], item.get("why", ""), key))
        for item in plan.get("web_calibration_queries", []):
            web_queries.append(web_query(item["label"], item["query"], item.get("why", ""), key))

    if not raw_queries and topic:
        raw_queries.append(
            query_entry(
                {
                    "label": "generic-topic",
                    "tier": "generic",
                    "query": f'all:"{topic}" AND all:robot',
                    "why": "Fallback query for a topic that did not match the embodied-AI taxonomy.",
                },
                "generic",
                "fallback",
            )
        )
        web_queries.append(web_query("web-generic-topic", f'"{topic}" robot learning arxiv', "Calibrate an unmatched topic.", "generic"))

    arxiv_queries = dedupe_queries(raw_queries, args.max_queries)
    query_text = topic or "embodied AI"
    if not browser_queries:
        browser_queries.append(
            browser_query(
                "browser-topic-arxiv",
                f'site:arxiv.org/abs "{query_text}" "robot"',
                "Fallback candidate discovery on arXiv pages when API metadata search under-recovers.",
                "generic",
            )
        )
    if not web_queries:
        web_queries.append(
            web_query(
                "web-topic-calibration",
                f'"{query_text}" "robot" "arXiv"',
                "Find paper-facing terminology for the requested topic.",
                "generic",
            )
        )

    mode = REVIEW_MODES[args.review_mode]
    targets = search_targets(args, len(arxiv_queries))
    coverage_dimensions = build_coverage_dimensions(
        arxiv_queries,
        int(mode["minimum_per_dimension"]),
    )

    return {
        "generated_at": stable_now(),
        "planner": "embodied-ai-query-planner",
        "topic": topic,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "knowledge_ids": topic_keys,
        "families": family_keys,
        "suggested_categories": suggested_categories(topic_keys, family_keys),
        "query_budget": args.max_queries,
        "review_mode": args.review_mode,
        "search_targets": targets,
        # Compatibility field for older Hub callers. This is a floor, never a stopping cap.
        "minimum_candidate_count": targets["candidate_floor"],
        "coverage_dimensions": coverage_dimensions,
        "stopping_rule": {
            "minimum_batches": int(mode["minimum_batches"]),
            "saturation_rounds": int(mode["saturation_rounds"]),
            "max_new_unique_rate": float(mode["max_new_unique_rate"]),
            "requires_candidate_floor": True,
            "requires_full_text_floor": True,
            "requires_accepted_paper_floor": True,
            "requires_all_coverage_dimensions": True,
            "note": "Stop only when every requirement passes; source-count floors alone never establish coverage.",
        },
        "notes": plan_notes,
        "dynamic_suggestions": dynamic_suggestions,
        "calibration_notes": calibration_notes,
        "queries": arxiv_queries,
        "arxiv_api_queries": arxiv_queries,
        "browser_fallback_queries": browser_queries,
        "web_calibration_queries": web_queries,
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# Query Plan: {plan['topic'] or 'embodied AI'}",
        "",
        "## Scope",
        "",
        f"- Knowledge IDs: {', '.join(plan['knowledge_ids']) or 'none'}",
        f"- Families: {', '.join(plan['families']) or 'none'}",
        f"- Suggested categories: {', '.join(plan['suggested_categories']) or 'none'}",
        f"- Review mode: {plan['review_mode']}",
        f"- Candidate floor (not a cap): {plan['search_targets']['candidate_floor']}",
        f"- Full-text floor: {plan['search_targets']['full_text_floor']}",
        f"- Accepted-paper floor: {plan['search_targets']['accepted_paper_floor']}",
        "",
        "## arXiv API Queries",
        "",
        "| Label | Tier | Query | Why |",
        "|---|---|---|---|",
    ]
    for item in plan["arxiv_api_queries"]:
        lines.append(f"| {item['label']} | {item['tier']} | `{item['query']}` | {item.get('why', '')} |")
    lines.extend(["", "## Coverage Dimensions", "", "| Dimension | Minimum candidates | Query labels |", "|---|---:|---|"])
    for item in plan["coverage_dimensions"]:
        lines.append(
            f"| {item['dimension']} | {item['minimum_unique_candidates']} | {', '.join(item['query_labels'])} |"
        )
    rule = plan["stopping_rule"]
    lines.extend(
        [
            "",
            "## Stopping Rule",
            "",
            f"- Minimum batches: {rule['minimum_batches']}",
            f"- Consecutive saturation rounds: {rule['saturation_rounds']}",
            f"- Maximum new-unique rate at saturation: {rule['max_new_unique_rate']:.0%}",
            "- Candidate, full-text, accepted-paper, and dimension floors must all pass.",
        ]
    )
    lines.extend(["", "## Browser Fallback Queries", "", "| Label | Query | Why |", "|---|---|---|"])
    for item in plan["browser_fallback_queries"]:
        lines.append(f"| {item['label']} | `{item['query']}` | {item.get('why', '')} |")
    lines.extend(["", "## Web Calibration Queries", "", "| Label | Source | Query | Why |", "|---|---|---|---|"])
    for item in plan["web_calibration_queries"]:
        lines.append(f"| {item['label']} | {item.get('source_type', 'web')} | `{item['query']}` | {item.get('why', '')} |")
    if plan["dynamic_suggestions"]:
        lines.extend(["", "## Dynamic Suggestions", "", "| Label | Channel | Source | Confidence | Query | Why |", "|---|---|---|---|---|---|"])
        for item in plan["dynamic_suggestions"]:
            lines.append(
                f"| {item['label']} | {item['channel']} | {item.get('source', '')} | {item.get('confidence', '')} | `{item['query']}` | {item.get('why', '')} |"
            )
    lines.extend(["", "## Calibration Notes", ""])
    for note in plan["calibration_notes"]:
        lines.append(f"- {note}")
    if plan["notes"]:
        lines.extend(["", "## Planner Notes", ""])
        for note in plan["notes"]:
            lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    if args.list_topics:
        return list_and_exit(TOPIC_PLANS)
    if args.list_families:
        return list_and_exit(FAMILY_PLANS)
    if not args.topic:
        raise SystemExit("--topic is required unless --list-topics or --list-families is used.")
    plan = build_plan(args)
    rendered = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    if args.markdown_output:
        Path(args.markdown_output).write_text(render_markdown(plan), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

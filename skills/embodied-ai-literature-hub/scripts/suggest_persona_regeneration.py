#!/usr/bin/env python3
"""Suggest saturation-triggered persona regeneration for a literature run.

Reads the current query plan plus a coverage report (retrieval phase) and/or an
evidence event log (reading phase), detects dimension gaps or stance skew, and
emits a draft persona file for the next round. Pure judgment plus templates:
the draft focus texts and starter queries are meant to be refined by an
agent/LLM and reviewed before re-entering the plan via --persona-file.

Refusal rule: regeneration stops once the plan already carries personas from
the maximum round (default 2), preventing regeneration loops.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

STANCE_SHARE_THRESHOLD = 0.20
MIN_EVENTS_FOR_STANCE_TRIGGER = 10

DIMENSION_PERSONA_TEMPLATES: dict[str, tuple[str, str, str]] = {
    "direct-topic": ("P-DIRECT", "主题事实补全者", "围绕主题核心概念补齐直接证据与基础事实"),
    "mechanisms-and-interfaces": ("P-METHOD", "机制与接口补缺者", "从方法、表征、接口与传感器机制角度补齐该维度的证据缺口"),
    "limits-and-counterevidence": ("P-LIMIT", "限制与反面证据猎手", "专搜失败案例、负迁移、局限与反例证据"),
    "evaluation-and-validation": ("P-EVAL", "评测验证补缺者", "从 benchmark、闭环验证与 sim-real 差距角度补齐证据"),
    "deployment-and-operations": ("P-DEPLOY", "部署运维补缺者", "从真实部署、产线运维与失败恢复角度补齐证据"),
    "adjacent-and-transfer": ("P-ADJACENT", "邻接迁移补缺者", "从相邻任务与跨域迁移角度补齐证据"),
}
DIMENSION_QUERY_MODIFIERS: dict[str, list[str]] = {
    "direct-topic": ["survey", "overview"],
    "mechanisms-and-interfaces": ["representation", "architecture"],
    "limits-and-counterevidence": ["failure", "limitation"],
    "evaluation-and-validation": ["benchmark", "evaluation"],
    "deployment-and-operations": ["deployment", "real-world"],
    "adjacent-and-transfer": ["transfer", "cross-domain"],
}
COUNTER_EVIDENCE_PERSONA = (
    "P-COUNTER-EVIDENCE",
    "反面证据搜寻者",
    "当已接纳证据的 limit/gap 占比过低时，主动搜寻限制、失败与反面证据以平衡证据池",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, help="Current query-plan.json.")
    parser.add_argument("--coverage-report", help="Coverage report from the literature hub retrieval round.")
    parser.add_argument("--evidence", help="evidence.jsonl with accepted evidence events (reading phase).")
    parser.add_argument("--max-rounds", type=int, default=2, help="Maximum regeneration rounds allowed.")
    parser.add_argument("--output", help="Write the draft persona file to this path instead of stdout.")
    return parser.parse_args()


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a JSON object")
    return data


def current_regeneration_round(plan: dict[str, Any]) -> int:
    rounds = [
        int(item["regeneration_round"])
        for item in plan.get("queries", [])
        if isinstance(item, dict) and item.get("regeneration_round") is not None
    ]
    return (max(rounds) if rounds else 0) + 1


def detect_dimension_gaps(coverage_report: dict[str, Any]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for entry in coverage_report.get("coverage_dimensions", []):
        if not isinstance(entry, dict):
            continue
        passed = bool(entry.get("passed", True))
        unique = int(entry.get("unique_candidates") or 0)
        minimum = int(entry.get("minimum_unique_candidates") or 0)
        if not passed or unique < minimum:
            gaps.append(
                {
                    "dimension": str(entry.get("dimension", "")),
                    "unique_candidates": unique,
                    "minimum_unique_candidates": minimum,
                    "passed": passed,
                }
            )
    return gaps


def detect_stance_skew(evidence_path: str) -> dict[str, Any] | None:
    stances: dict[str, int] = {}
    total = 0
    with open(evidence_path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            stance = str(event.get("stance") or "")
            if stance:
                stances[stance] = stances.get(stance, 0) + 1
                total += 1
    if total < MIN_EVENTS_FOR_STANCE_TRIGGER:
        return {
            "triggered": False,
            "reason": f"only {total} stance-labeled events (< {MIN_EVENTS_FOR_STANCE_TRIGGER}); too few to judge balance",
            "total": total,
            "stances": stances,
        }
    counter = stances.get("limit", 0) + stances.get("gap", 0)
    share = counter / total
    return {
        "triggered": share < STANCE_SHARE_THRESHOLD,
        "reason": f"limit+gap stance share {share:.0%} ({counter}/{total}) vs threshold {STANCE_SHARE_THRESHOLD:.0%}",
        "total": total,
        "stances": stances,
    }


def anchor_terms_for_dimension(plan: dict[str, Any], dimension: str) -> list[str]:
    """Extract English anchor phrases from the plan's existing queries in a dimension."""
    terms: dict[str, int] = {}
    for item in plan.get("queries", []):
        if str(item.get("coverage_dimension") or "") != dimension:
            continue
        query = str(item.get("query", ""))
        for phrase in re.findall(r'"([^"]{3,})"', query):
            terms[phrase] = terms.get(phrase, 0) + 1
        for word in re.findall(r"all:([\w-]{4,})", query):
            if word.lower() not in {"robot", "robotics", "learning"}:
                terms[word] = terms.get(word, 0) + 1
    ranked = sorted(terms.items(), key=lambda pair: (-pair[1], pair[0]))
    return [term for term, _ in ranked[:2]]


def starter_queries(dimension: str, anchors: list[str], round_number: int, index_offset: int) -> list[dict[str, Any]]:
    modifiers = DIMENSION_QUERY_MODIFIERS.get(dimension, ["robot"])
    queries: list[dict[str, Any]] = []
    for index, modifier in enumerate(modifiers, start=index_offset):
        if anchors:
            query = f'all:"{anchors[0]}" AND all:{modifier}'
            why = f"Gap-filling starter query for {dimension}; refine the anchor term before use."
        else:
            query = f"all:{modifier} AND all:robot"
            why = f"Generic starter query for {dimension}; no anchor term found in the plan, replace with topic-specific terms."
        queries.append(
            {
                "label": f"persona-reg-r{round_number}-{dimension}-{index}",
                "query": query,
                "why": why,
                "tier": None,
                "coverage_dimension": dimension,
            }
        )
    return queries


def build_draft(
    plan: dict[str, Any],
    round_number: int,
    max_rounds: int,
    gaps: list[dict[str, Any]],
    stance: dict[str, Any] | None,
) -> dict[str, Any]:
    triggered_by: list[str] = []
    personas: list[dict[str, Any]] = []
    queries: list[dict[str, Any]] = []

    for gap in gaps:
        dimension = gap["dimension"]
        template = DIMENSION_PERSONA_TEMPLATES.get(dimension)
        if template is None:
            continue
        short, name, focus = template
        persona_id = f"{short}-REG-R{round_number}"
        trigger = (
            f"coverage-report: dimension {dimension} has unique_candidates={gap['unique_candidates']} "
            f"< minimum={gap['minimum_unique_candidates']} (passed={str(gap['passed']).lower()})"
        )
        triggered_by.append(trigger)
        personas.append(
            {
                "id": persona_id,
                "name": name,
                "focus": focus,
                "primary_dimensions": [dimension],
                "inspired_by": [trigger],
                "regeneration_round": round_number,
                "triggered_by": trigger,
            }
        )
        # A gap dimension often has few or weak queries (that is why it is a
        # gap), so fall back to direct-topic anchors to keep starter queries
        # topic-specific — same fallback the stance-skew branch uses.
        anchors = anchor_terms_for_dimension(plan, dimension) or anchor_terms_for_dimension(plan, "direct-topic")
        for query in starter_queries(dimension, anchors, round_number, 1):
            query["persona"] = persona_id
            query["regeneration_round"] = round_number
            queries.append(query)

    if stance and stance.get("triggered"):
        persona_id = f"{COUNTER_EVIDENCE_PERSONA[0]}-REG-R{round_number}"
        trigger = f"evidence.jsonl: {stance['reason']}"
        triggered_by.append(trigger)
        personas.append(
            {
                "id": persona_id,
                "name": COUNTER_EVIDENCE_PERSONA[1],
                "focus": COUNTER_EVIDENCE_PERSONA[2],
                "primary_dimensions": ["limits-and-counterevidence"],
                "inspired_by": [trigger],
                "regeneration_round": round_number,
                "triggered_by": trigger,
            }
        )
        anchors = anchor_terms_for_dimension(plan, "direct-topic") or anchor_terms_for_dimension(plan, "limits-and-counterevidence")
        for query in starter_queries("limits-and-counterevidence", anchors, round_number, 1):
            query["persona"] = persona_id
            query["regeneration_round"] = round_number
            queries.append(query)

    for query in queries:
        query.pop("tier", None)

    return {
        "topic": plan.get("topic", ""),
        "status": "draft-needs-review",
        "regeneration_round": round_number,
        "max_regeneration_rounds": max_rounds,
        "triggered_by": triggered_by,
        "personas": personas,
        "queries": queries,
        "notes": [
            "Draft personas and starter queries are templates; refine focus text and queries before merging via --persona-file.",
            "Regeneration never bypasses coverage gates; it only adds queries for the next retrieval round.",
        ],
    }


def main() -> int:
    args = parse_args()
    plan = load_json(args.plan)

    round_number = current_regeneration_round(plan)
    if round_number > args.max_rounds:
        draft = {
            "topic": plan.get("topic", ""),
            "status": "refused",
            "regeneration_round": round_number,
            "max_regeneration_rounds": args.max_rounds,
            "reason": (
                f"Plan already carries regeneration round {round_number - 1} personas; "
                f"round {round_number} exceeds the cap of {args.max_rounds}. "
                "Accept the coverage gap or raise --max-rounds explicitly."
            ),
        }
        rendered = json.dumps(draft, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)
        return 0

    if not args.coverage_report and not args.evidence:
        raise SystemExit("Provide --coverage-report and/or --evidence; there is nothing to judge otherwise.")

    gaps = detect_dimension_gaps(load_json(args.coverage_report)) if args.coverage_report else []
    stance = detect_stance_skew(args.evidence) if args.evidence else None

    draft = build_draft(plan, round_number, args.max_rounds, gaps, stance)
    if stance and not stance.get("triggered"):
        draft["notes"].append(f"Stance check not triggered: {stance['reason']}.")
    if args.coverage_report and not gaps:
        draft["notes"].append("Coverage report shows no dimension gaps; no retrieval-phase persona was added.")

    rendered = json.dumps(draft, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())

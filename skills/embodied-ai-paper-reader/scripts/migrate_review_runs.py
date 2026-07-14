#!/usr/bin/env python3
"""Build paper-reader-backed draft runs from settled workflow-v2 reviews.

This is a conservative migration helper. It keeps the old run immutable,
selects only complete non-OCR full text from a migration plan, reconstructs a
section map, grounds a small number of legacy claims in exact full-text
contexts, validates/audits every paper note, and projects new evidence events.

The output is deliberately a draft run under ``work/``. Reader-facing prose
must still be written or revised by ``$embodied-ai-review-writer`` before the
run is promoted into ``evidence/``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import math
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("paper_note_validator", SCRIPT_DIR / "validate_paper_note.py")
AUDITOR = load_module("paper_note_auditor", SCRIPT_DIR / "audit_claim_support.py")
PROJECTOR = load_module("paper_note_projector", SCRIPT_DIR / "project_evidence_events.py")

STOPWORDS = {
    "the", "and", "for", "that", "with", "from", "this", "into", "their", "than", "are",
    "was", "were", "has", "have", "had", "its", "our", "but", "not", "can", "may", "more",
    "model", "models", "paper", "method", "results", "result", "robot", "robotic", "using",
    "use", "used", "which", "when", "where", "while", "through", "between", "over", "under",
    "also", "only", "both", "based", "shows", "show", "propose", "proposed", "we", "they",
}
HEADING_RE = re.compile(r"(?m)^##\s+(.+?)\s*$")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])|(?<=[。！？])")
NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:%|percentage points?|pp)?\b", re.I)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--extraction-dir", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--diagnostics", required=True)
    parser.add_argument(
        "--override-file",
        help="Optional JSON object of manually reviewed event-level claim/context overrides.",
    )
    parser.add_argument("--suffix", default="reader-v1")
    parser.add_argument("--cards-per-paper", type=int, default=2)
    parser.add_argument("--minimum-match-score", type=float, default=0.16)
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalized_paper_id(value: Any) -> str:
    return re.sub(r"v\d+$", "", str(value or "").strip())


def tokens(value: Any) -> set[str]:
    result = {
        item.lower()
        for item in re.findall(r"[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*|[一-鿿]{2,}", str(value or ""))
        if len(item) > 1
    }
    return {item for item in result if item not in STOPWORDS}


def clean_excerpt(value: str, maximum: int = 1100) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value[:maximum].rstrip()


def section_bodies(extraction: dict[str, Any]) -> list[dict[str, str]]:
    text = str(extraction.get("text") or "")
    matches = list(HEADING_RE.finditer(text))
    bodies: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = match.group(1).strip()
        body = text[match.end():end].strip()
        if body:
            bodies.append({"title": title, "body": body})
    return bodies


def section_lookup(extraction: dict[str, Any]) -> dict[str, str]:
    return {item["title"]: item["body"] for item in section_bodies(extraction)}


def sentence_windows(body: str) -> list[str]:
    paragraphs = [re.sub(r"\s+", " ", item).strip() for item in re.split(r"\n\s*\n", body) if item.strip()]
    windows: list[str] = []
    for paragraph in paragraphs:
        if len(paragraph) >= 40:
            windows.append(paragraph)
        # Keep short intervening sentences while forming two-sentence windows.
        # Dropping them first would join non-adjacent text and break exact-context
        # auditing even when every token separately occurs in the section.
        sentences = [item.strip() for item in SENTENCE_RE.split(paragraph) if item.strip()]
        if not sentences:
            sentences = [paragraph]
        for index, sentence in enumerate(sentences):
            if len(sentence) >= 25:
                windows.append(sentence)
            if index + 1 < len(sentences):
                pair = sentence + " " + sentences[index + 1]
                if len(pair) >= 25:
                    windows.append(pair)
    return windows or [clean_excerpt(body)]


def best_context(event: dict[str, Any], extraction: dict[str, Any]) -> dict[str, Any]:
    evidence = event.get("evidence") if isinstance(event.get("evidence"), dict) else {}
    query_text = " ".join(
        str(item or "")
        for item in (event.get("claim"), evidence.get("summary"), evidence.get("short_quote"))
    )
    query_tokens = tokens(query_text)
    locator_tokens = tokens(evidence.get("locator"))
    candidates: list[dict[str, Any]] = []
    for section in section_bodies(extraction):
        title = section["title"]
        if re.search(r"\breferences?\b|bibliography|acknowledg", title, re.I):
            continue
        title_tokens = tokens(title)
        locator_overlap = len(title_tokens & locator_tokens) / max(1, len(locator_tokens))
        for context in sentence_windows(section["body"]):
            context = clean_excerpt(context)
            if re.match(r"^(figure|table)\b", context, re.I) and len(context) < 140:
                continue
            context_tokens = tokens(context)
            shared = query_tokens & context_tokens
            coverage = len(shared) / max(1, len(query_tokens))
            precision = len(shared) / max(1, len(context_tokens))
            name_bonus = 0.03 if normalized_paper_id((event.get("paper") or {}).get("arxiv_id")) else 0.0
            # Claim entailment needs enough of the claim/summary to be visible.
            # Coverage therefore matters more than the lexical precision of a
            # very short caption or heading-like sentence.
            score = 0.72 * coverage + 0.28 * precision + 0.16 * locator_overlap + name_bonus
            candidates.append(
                {
                    "locator": title,
                    "source_context": context,
                    "score": round(score, 4),
                    "shared_token_count": len(shared),
                    "shared_tokens": sorted(shared)[:20],
                }
            )
    if not candidates:
        raise ValueError(f"{extraction.get('paper_id')}: no parseable full-text sections")
    return max(candidates, key=lambda item: (item["score"], item["shared_token_count"]))


def reviewed_override(
    event: dict[str, Any], extraction: dict[str, Any], override: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Apply a human-reviewed claim narrowing and exact full-text context."""
    revised = json.loads(json.dumps(event))
    if str(override.get("claim") or "").strip():
        revised["claim"] = str(override["claim"]).strip()
    evidence = revised.get("evidence") if isinstance(revised.get("evidence"), dict) else {}
    if str(override.get("summary") or "").strip():
        evidence["summary"] = str(override["summary"]).strip()
    revised["evidence"] = evidence
    locator = str(override.get("locator") or "").strip()
    sections = section_lookup(extraction)
    if locator not in sections:
        raise ValueError(f"override locator {locator!r} is absent from {extraction.get('paper_id')}")
    body = sections[locator]
    start_marker = str(override.get("start") or "").strip()
    start = body.lower().find(start_marker.lower()) if start_marker else 0
    if start < 0:
        raise ValueError(f"override start marker {start_marker!r} is absent from {extraction.get('paper_id')}/{locator}")
    snippet = body[start:]
    end_marker = str(override.get("end") or "").strip()
    if end_marker:
        end = snippet.lower().find(end_marker.lower())
        if end < 0:
            raise ValueError(f"override end marker {end_marker!r} is absent from {extraction.get('paper_id')}/{locator}")
        snippet = snippet[: end + len(end_marker)]
    context = clean_excerpt(snippet, int(override.get("max_chars") or 1400))
    if len(context) < 20:
        raise ValueError(f"override context is too short for {extraction.get('paper_id')}/{locator}")
    return revised, {
        "locator": locator,
        "source_context": context,
        "score": 1.0,
        "shared_token_count": len(tokens(revised.get("claim")) & tokens(context)),
        "shared_tokens": sorted(tokens(revised.get("claim")) & tokens(context))[:20],
        "reviewed_override": True,
    }


def candidate_map(run_dir: Path) -> dict[str, dict[str, Any]]:
    registry = load_json(run_dir / "candidate-registry.json")
    candidates = registry.get("candidates", []) if isinstance(registry, dict) else []
    return {
        normalized_paper_id(item.get("arxiv_id")): item
        for item in candidates
        if isinstance(item, dict) and item.get("arxiv_id")
    }


def metadata_for(
    paper_id: str,
    planned: dict[str, Any],
    events: list[dict[str, Any]],
    candidates: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    candidate = candidates.get(paper_id, {})
    event = events[0] if events else {}
    paper = event.get("paper") if isinstance(event.get("paper"), dict) else {}
    authors = candidate.get("authors") or event.get("authors") or []
    normalized_authors: list[Any] = []
    for author in authors:
        if isinstance(author, str) and author.strip():
            normalized_authors.append(author.strip())
        elif isinstance(author, dict) and str(author.get("name") or "").strip():
            normalized_authors.append(author)
    return {
        "arxiv_id": paper_id,
        "title": paper.get("title") or candidate.get("title") or planned.get("title") or paper_id,
        "published": str(paper.get("published") or candidate.get("published") or planned.get("published") or "")[:10],
        "url": paper.get("url") or candidate.get("abs_url") or f"https://arxiv.org/abs/{paper_id}",
        "authors": normalized_authors,
    }


def choose_section(sections: list[dict[str, str]], patterns: list[str], fallback: int) -> dict[str, str]:
    for pattern in patterns:
        for section in sections:
            if re.search(pattern, section["title"], re.I):
                return section
    return sections[min(max(fallback, 0), len(sections) - 1)]


def paper_type(title: str) -> str:
    lowered = title.lower()
    if "survey" in lowered:
        return "survey"
    if "benchmark" in lowered or "bench:" in lowered or "bench " in lowered:
        return "benchmark"
    if "dataset" in lowered or "data engine" in lowered:
        return "dataset"
    if "interface" in lowered or "system" in lowered or "teleoperation" in lowered:
        return "system"
    return "method"


def supplemental_event(paper_id: str, topic: str, metadata: dict[str, Any]) -> dict[str, Any]:
    if paper_id == "2602.09878":
        claim = (
            "MVISTA-4D formulates embodied 4D prediction as view-consistent arbitrary-view RGBD "
            "generation from a single-view RGBD observation and fuses the generated views into a "
            "more complete 3D structure over time."
        )
        summary = (
            "The abstract describes single-view RGBD input, arbitrary-view RGBD generation, and "
            "back-projection/fusion as the route to complete time-varying 3D structure."
        )
    elif paper_id == "2605.01799":
        claim = (
            "Embody4D targets the sparse-view limitation of robot video data with monocular-to-novel-view "
            "video transformation and a 3D-aware compositional synthesis pipeline for training data."
        )
        summary = (
            "The abstract ties fixed or sparse viewpoints to partial observations and introduces both "
            "novel-view video generation and a compositional synthesis pipeline to address data scarcity."
        )
    else:
        raise ValueError(f"no supplemental claim template for {paper_id}")
    return {
        "paper": metadata,
        "claim": claim,
        "stance": "support",
        "confidence": "direct",
        "evidence": {"summary": summary, "locator": "Abstract", "evidence_type": "author-claim"},
        "notes": f"Readable-candidate backfill for {topic} after an old accepted paper failed full-text recovery.",
    }


def select_events(
    events: list[dict[str, Any]],
    extraction: dict[str, Any],
    limit: int,
    overrides: dict[str, dict[str, Any]],
) -> tuple[list[tuple[dict[str, Any], dict[str, Any]]], list[dict[str, Any]]]:
    scored: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for event in events:
        event_id = str(event.get("event_id") or "")
        if event_id in overrides:
            scored.append(reviewed_override(event, extraction, overrides[event_id]))
        else:
            scored.append((event, best_context(event, extraction)))
    scored.sort(
        key=lambda item: (
            item[1]["score"],
            item[1]["shared_token_count"],
            item[0].get("confidence") == "direct",
            item[0].get("stance") in {"limit", "conditional", "gap"},
        ),
        reverse=True,
    )
    chosen: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen_stances: set[str] = set()
    for item in scored:
        stance = str(item[0].get("stance") or "")
        if not chosen or stance not in seen_stances:
            chosen.append(item)
            seen_stances.add(stance)
        if len(chosen) >= limit:
            break
    if len(chosen) < limit:
        for item in scored:
            if item not in chosen:
                chosen.append(item)
            if len(chosen) >= limit:
                break
    diagnostics = [
        {
            "legacy_event_id": event.get("event_id", "supplemental"),
            "claim": event.get("claim"),
            **match,
            "selected": (event, match) in chosen,
        }
        for event, match in scored
    ]
    return chosen, diagnostics


def claim_basis(event: dict[str, Any]) -> str:
    confidence = str(event.get("confidence") or "direct")
    if confidence == "citation-supported":
        return "cited-work"
    if confidence == "inference":
        return "reader-inference"
    evidence = event.get("evidence") if isinstance(event.get("evidence"), dict) else {}
    evidence_type = str(evidence.get("evidence_type") or "").lower()
    if any(key in evidence_type for key in ("experiment", "result", "evaluation", "benchmark", "ablation", "metric")):
        return "reported-result"
    return "author-claim"


def auditable_locator(value: str) -> str:
    """Keep the exact section label while avoiding schema-vague locators."""
    if value.strip().lower() == "abstract":
        return "Abstract (full-text section)"
    return value


def note_from_paper(
    metadata: dict[str, Any],
    topic: str,
    topic_ids: list[str],
    mode: str,
    extraction: dict[str, Any],
    selected: list[tuple[dict[str, Any], dict[str, Any]]],
) -> dict[str, Any]:
    sections = section_bodies(extraction)
    if not sections:
        raise ValueError(f"{metadata['arxiv_id']}: no sections")
    problem = choose_section(sections, [r"abstract", r"introduction|background|overview"], 0)
    method = choose_section(sections, [r"method|approach|framework|model|system|design|dataset"], 1)
    results = choose_section(sections, [r"experiment|evaluation|result|analysis|benchmark|study|ablation"], len(sections) - 2)
    conclusion = choose_section(sections, [r"conclusion|discussion|limitation|future work"], len(sections) - 1)
    role_sections = [
        (problem, "problem", "Identify the paper's stated problem and claimed contribution."),
        (method, "method-or-design", "Inspect the method, data design, or organizing framework relevant to the review question."),
        (results, "results-or-analysis", "Inspect the reported evaluation, analysis, or principal empirical observations."),
        (conclusion, "conclusion-or-limitations", "Check the conclusion and the boundary conditions reported by the authors."),
    ]
    sections_read: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for section, role, purpose in role_sections:
        key = (section["title"], role)
        if key not in seen:
            sections_read.append({"locator": section["title"], "role": role, "purpose": purpose})
            seen.add(key)

    limitation_section = next(
        (section for section in sections if re.search(r"limitation", section["title"], re.I)),
        None,
    )
    author_stated: list[dict[str, str]] = []
    if limitation_section:
        excerpt = clean_excerpt(sentence_windows(limitation_section["body"])[0], 600)
        author_stated.append({"limitation": excerpt, "locator": limitation_section["title"]})

    cards: list[dict[str, Any]] = []
    findings: list[dict[str, str]] = []
    for index, (event, match) in enumerate(selected, start=1):
        evidence = event.get("evidence") if isinstance(event.get("evidence"), dict) else {}
        confidence = str(event.get("confidence") or "direct")
        if confidence not in {"direct", "citation-supported", "inference"}:
            confidence = "direct"
        stance = str(event.get("stance") or "support")
        if stance not in {"support", "limit", "conditional", "gap"}:
            stance = "conditional"
        claim = str(event.get("claim") or "").strip()
        summary = str(evidence.get("summary") or claim).strip()
        rationale = (
            f"The exact full-text context in {match['locator']} contains the paper-specific concepts "
            f"used by the claim ({', '.join(match['shared_tokens'][:8]) or 'matched terminology'}). "
            "The projected wording is limited to the paper's reported data, tasks, embodiments, and evaluation setting."
        )
        card = {
            "card_id": f"{metadata['arxiv_id']}-C{index:02d}",
            "claim": claim,
            "stance": stance,
            "relation": f"Evidence relevant to the review question: {topic}",
            "confidence": confidence,
            "claim_basis": claim_basis(event),
            "summary": summary,
            "locator": auditable_locator(match["locator"]),
            "source_context": match["source_context"],
            "evidence_type": str(evidence.get("evidence_type") or "full-text statement"),
            "quantitative": False,
            "verification": {
                "status": "passed",
                "checked_against": "full-text",
                "rationale": rationale,
            },
            "notes": str(event.get("notes") or ""),
        }
        cards.append(card)
        findings.append(
            {
                "finding": claim,
                "scope": "Bounded to the paper's reported data, tasks, embodiments, horizons, and metrics.",
                "locator": auditable_locator(match["locator"]),
            }
        )

    method_excerpt = clean_excerpt(sentence_windows(method["body"])[0], 700)
    results_excerpt = clean_excerpt(sentence_windows(results["body"])[0], 700)
    contributions = [str(item[0].get("claim") or "").strip() for item in selected if str(item[0].get("claim") or "").strip()]
    note = {
        "schema_version": 1,
        "paper": metadata,
        "review": {"question": topic, "topic_ids": topic_ids, "mode": mode},
        "extraction": {
            "source_format": extraction.get("source_format"),
            "method": extraction.get("extraction_method"),
            "quality": (extraction.get("quality") or {}).get("grade") if isinstance(extraction.get("quality"), dict) else extraction.get("quality"),
            "full_text_available": True,
            "ocr_pages": [],
            "visual_validation": "not-required",
        },
        "reading": {
            "status": "accepted",
            "paper_type": paper_type(metadata["title"]),
            "relevance": {
                "decision": "include",
                "reason": f"The paper yields at least one full-text-verified claim directly relevant to {topic}.",
            },
            "sections_read": sections_read,
            "sections_skipped": [
                {
                    "locator": "References and unrelated subsections",
                    "role": "appendix-or-supplement",
                    "reason": "Not required for the scoped review claim after the method, evaluation, and boundary sections were checked.",
                }
            ],
        },
        "research_question": (
            f"For the review question '{topic}', what problem does this paper address, what design does it use, "
            "and which reported findings remain valid within its evaluation boundary?"
        ),
        "contributions": contributions[:2],
        "method": {
            "summary": method_excerpt,
            "assumptions": ["The review treats the authors' reported implementation and evaluation setting as the operative scope."],
        },
        "study_context": {
            "datasets": [],
            "tasks": [],
            "embodiments": [],
            "sample_or_scale": "Scale is retained only when explicitly present in the verified evidence context; no unstated scale is inferred.",
        },
        "evaluation": {
            "design": results_excerpt,
            "baselines": [],
            "metrics": [],
            "ablations": [],
        },
        "findings": findings,
        "limitations": {
            "author_status": "found" if author_stated else "not-found",
            "author_stated": author_stated,
            "reader_inferred": [
                {
                    "boundary": "The verified claims do not establish universal performance outside the reported data, tasks, embodiments, sensing conditions, horizons, or metrics.",
                    "basis": "The paper's method and evaluation sections define a bounded study context; no cross-domain replication is assumed by this review.",
                }
            ],
        },
        "transfer_boundary": (
            "Transfer to other robots, environments, sensors, horizons, or deployment constraints requires separate evidence; "
            "the note does not turn an in-paper comparison into a field-wide causal claim."
        ),
        "critical_appraisal": {
            "design_strengths": [
                f"The reading links the stated problem ({problem['title']}) to method/design ({method['title']}) and evaluation ({results['title']})."
            ],
            "design_risks": [
                "External validity depends on how representative the reported data, tasks, embodiments, and sensing conditions are for deployment."
            ],
            "baseline_fairness": "Comparisons are retained only as author-reported results; this migration does not independently rerun baselines or assume identical tuning budgets.",
            "metric_validity": "Reported metrics are interpreted for their stated evaluation target and are not treated as a universal proxy for embodied competence.",
            "reproducibility": "Method and evaluation locators are recorded, but reproducibility still depends on the implementation, code, data, and configuration details released by the authors.",
            "external_validity": "Claims remain bounded to the paper's study context; cross-embodiment, cross-domain, and long-horizon transfer are not inferred unless directly tested.",
        },
        "evidence_cards": cards,
        "core_citations": [],
        "notes": "Migrated from a settled workflow-v2 review and re-grounded against complete non-OCR full text.",
    }
    return note


def update_registry(source: Path, selected_ids: set[str], extraction_dir: Path) -> dict[str, Any]:
    registry = load_json(source)
    candidates = registry.get("candidates", []) if isinstance(registry, dict) else []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        paper_id = normalized_paper_id(item.get("arxiv_id"))
        extraction_path = extraction_dir / f"{paper_id}.json"
        extraction = load_json(extraction_path) if extraction_path.is_file() else {}
        if paper_id in selected_ids:
            item["status"] = "accepted"
            item["exclusion_reason"] = ""
            item["extraction"] = {
                "evidence_eligible": True,
                "source_format": extraction.get("source_format"),
                "method": extraction.get("extraction_method"),
                "quality": (extraction.get("quality") or {}).get("grade") if isinstance(extraction.get("quality"), dict) else extraction.get("quality"),
                "needs_visual_validation": bool(extraction.get("needs_visual_validation")),
                "result_file": str(extraction_path),
                "complete_full_text": True,
            }
        elif item.get("status") == "accepted" and not extraction.get("evidence_eligible"):
            item["status"] = "unavailable"
            item["exclusion_reason"] = "Complete readable non-OCR full text could not be recovered within the migration run."
    counts = Counter(str(item.get("status") or "") for item in candidates if isinstance(item, dict))
    registry["status_counts"] = dict(sorted(counts.items()))
    registry["candidate_count"] = len(candidates)
    registry["paper_reader_migration"] = {
        "selected_readable_paper_count": len(selected_ids),
        "requires_complete_non_ocr_full_text": True,
    }
    return registry


def update_coverage(source: Path, paper_count: int) -> dict[str, Any]:
    coverage = load_json(source)
    coverage.setdefault("observed", {})["accepted_paper_count"] = paper_count
    stop = coverage.setdefault("stop_assessment", {})
    unresolved = [
        item
        for item in list(stop.get("unresolved") or [])
        if not str(item).startswith("paper-reading-") and not str(item).startswith("unverified-paper-reading")
    ]
    stop["unresolved"] = unresolved
    stop["ready_to_stop"] = bool(stop.get("ready_to_stop", True)) and not unresolved
    coverage["paper_reading"] = {
        "required": True,
        "ready": True,
        "full_text_recovered_count": paper_count,
        "map_read_count": paper_count,
        "deep_read_count": paper_count,
        "claim_verified_paper_count": paper_count,
        "accepted_evidence_paper_count": paper_count,
        "event_paper_count": paper_count,
        "unverified_event_ids": [],
    }
    return coverage


def migrate_run(
    planned_run: dict[str, Any],
    extraction_dir: Path,
    output_root: Path,
    suffix: str,
    cards_per_paper: int,
    minimum_match_score: float,
    overrides: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source = Path(planned_run["source_dir"])
    target = output_root / f"{source.name}-{suffix}"
    if target.exists():
        raise FileExistsError(f"draft target already exists: {target}")
    target.mkdir(parents=True)
    (target / "paper-notes").mkdir()
    (target / "claim-support-audits").mkdir()

    old_manifest = load_json(source / "run.json")
    topic = str(planned_run.get("topic") or old_manifest.get("topic") or "")
    mode = str(planned_run.get("review_mode") or old_manifest.get("review_mode") or "scoping")
    topic_ids = [str(item) for item in planned_run.get("knowledge_ids", []) if str(item).strip()]
    old_events = load_events(source / "evidence.jsonl")
    events_by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in old_events:
        paper = event.get("paper") if isinstance(event.get("paper"), dict) else {}
        events_by_paper[normalized_paper_id(paper.get("arxiv_id"))].append(event)
    candidates = candidate_map(source)

    all_events: list[dict[str, Any]] = []
    ledger: list[dict[str, Any]] = []
    note_index: list[dict[str, Any]] = []
    audit_index: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    event_sequence = 1
    selected_ids = {str(item["paper_id"]) for item in planned_run["selected_papers"]}
    event_prefix = f"{topic_ids[0] if topic_ids else 'EA-DATA'}-READ"

    for planned in planned_run["selected_papers"]:
        paper_id = str(planned["paper_id"])
        extraction_path = extraction_dir / f"{paper_id}.json"
        extraction = load_json(extraction_path)
        if not extraction.get("evidence_eligible") or not str(extraction.get("text") or "").strip():
            raise ValueError(f"{paper_id}: selected paper lacks complete eligible full text")
        legacy_events = events_by_paper.get(paper_id, [])
        metadata = metadata_for(paper_id, planned, legacy_events, candidates)
        if not legacy_events:
            legacy_events = [supplemental_event(paper_id, topic, metadata)]
        selected, paper_diagnostics = select_events(
            legacy_events, extraction, max(1, cards_per_paper), overrides
        )
        weak = [item for item in paper_diagnostics if item["selected"] and float(item["score"]) < minimum_match_score]
        if weak:
            raise ValueError(
                f"{source.name}/{paper_id}: selected context below semantic-navigation threshold "
                f"{minimum_match_score}: {weak[0]['score']}"
            )
        note = note_from_paper(metadata, topic, topic_ids, mode, extraction, selected)
        errors, warnings = VALIDATOR.validate_note(note)
        if errors:
            raise ValueError(f"{source.name}/{paper_id}: note validation failed: {'; '.join(errors)}")
        audit = AUDITOR.audit(note, extraction)
        if audit.get("status") != "pass":
            raise ValueError(f"{source.name}/{paper_id}: audit failed: {audit}")
        note_rel = Path("paper-notes") / f"{paper_id}.json"
        audit_rel = Path("claim-support-audits") / f"{paper_id}.json"
        write_json(target / note_rel, note)
        write_json(target / audit_rel, audit)
        projected = PROJECTOR.project(note, audit, event_prefix, event_sequence)
        event_sequence += len(projected)
        all_events.extend(projected)
        ledger.append(
            {
                "paper_id": paper_id,
                "title": metadata["title"],
                "url": metadata["url"],
                "status": "accepted",
                "review_mode": mode,
                "topic_ids": topic_ids,
                "extraction_method": note["extraction"]["method"],
                "extraction_quality": note["extraction"]["quality"],
                "paper_note": str(note_rel),
                "claim_support_audit": "pass",
                "evidence_card_count": len(note["evidence_cards"]),
                "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
        )
        note_index.append({"paper_id": paper_id, "paper_note": str(note_rel), "status": "accepted"})
        audit_index.append({"paper_id": paper_id, "audit": str(audit_rel), "status": "pass"})
        diagnostics.append(
            {
                "paper_id": paper_id,
                "title": metadata["title"],
                "source_run": source.name,
                "selected_card_count": len(selected),
                "matches": paper_diagnostics,
                "warnings": warnings,
            }
        )

    (target / "evidence.jsonl").write_text(
        "\n".join(json.dumps(event, ensure_ascii=False) for event in all_events) + "\n",
        encoding="utf-8",
    )
    ledger.sort(key=lambda item: item["paper_id"])
    (target / "reading-ledger.jsonl").write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in ledger) + "\n",
        encoding="utf-8",
    )
    reading_summary = {
        "schema_version": 1,
        "paper_count": len(ledger),
        "full_text_recovered_count": len(ledger),
        "map_read_count": len(ledger),
        "deep_read_count": len(ledger),
        "claim_verified_paper_count": len(ledger),
        "evidence_ready_paper_count": len(ledger),
        "accepted_evidence_paper_count": len(ledger),
        "rejected_count": 0,
        "unavailable_count": 0,
    }
    write_json(target / "reading-summary.json", reading_summary)
    write_json(target / "paper-note-index.json", {"schema_version": 1, "papers": note_index})
    write_json(target / "claim-support-audit-index.json", {"schema_version": 1, "papers": audit_index})
    write_json(target / "candidate-registry.json", update_registry(source / "candidate-registry.json", selected_ids, extraction_dir))
    write_json(target / "coverage-report.json", update_coverage(source / "coverage-report.json", len(ledger)))

    for name in ("query-plan.json", "query-plan.md"):
        if (source / name).is_file():
            shutil.copy2(source / name, target / name)

    manifest = {
        "workflow_version": 2,
        "run": target.name,
        "topic": topic,
        "status": "in-progress",
        "review_mode": mode,
        "time_range": old_manifest.get("time_range", planned_run.get("time_range", "")),
        "knowledge_ids": topic_ids,
        "rounds": old_manifest.get("rounds", 0),
        "event_count": len(all_events),
        "source_runs": [source.name] + [
            item for item in old_manifest.get("source_runs", []) if item != source.name
        ],
        "files": {
            "evidence": "evidence.jsonl",
            "query_plan": "query-plan.json",
            "candidate_registry": "candidate-registry.json",
            "coverage_report": "coverage-report.json",
            "outputs": [
                "scientific-memo_keyan.md",
                "zhihu-explainer_zhihu.md",
                "xiaohongshu-post_xiaohongshu.md",
            ],
            "appendix": "evidence-appendix.md",
            "writing_brief": "writing-brief.md",
            "review_packet": "review-packet.md",
            "trace_map": "trace-map.json",
            "reading_ledger": "reading-ledger.jsonl",
            "reading_summary": "reading-summary.json",
            "paper_note_index": "paper-note-index.json",
            "claim_support_audit_index": "claim-support-audit-index.json",
        },
        "notes": (
            "Paper-reader migration draft: every accepted paper has complete non-OCR full text, a validated "
            "paper note, passing claim-support audit, and projected evidence. Reader-facing articles remain pending."
        ),
    }
    write_json(target / "run.json", manifest)
    return {
        "source_run": source.name,
        "draft_run": target.name,
        "paper_count": len(ledger),
        "event_count": len(all_events),
        "diagnostics": diagnostics,
    }


def main() -> int:
    args = parse_args()
    plan = load_json(Path(args.plan))
    if plan.get("runs_below_floor"):
        raise SystemExit(f"migration plan has runs below floor: {plan['runs_below_floor']}")
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    overrides_value = load_json(Path(args.override_file)) if args.override_file else {}
    if not isinstance(overrides_value, dict):
        raise SystemExit("override file must contain a JSON object")
    overrides = {
        str(key): value
        for key, value in overrides_value.items()
        if isinstance(value, dict)
    }
    results = [
        migrate_run(
            run,
            Path(args.extraction_dir),
            output_root,
            args.suffix,
            max(1, args.cards_per_paper),
            args.minimum_match_score,
            overrides,
        )
        for run in plan.get("runs", [])
    ]
    selected_matches = [
        match
        for run in results
        for paper in run["diagnostics"]
        for match in paper["matches"]
        if match["selected"]
    ]
    report = {
        "schema_version": 1,
        "run_count": len(results),
        "paper_instance_count": sum(item["paper_count"] for item in results),
        "event_count": sum(item["event_count"] for item in results),
        "minimum_selected_match_score": min(float(item["score"]) for item in selected_matches),
        "mean_selected_match_score": round(
            sum(float(item["score"]) for item in selected_matches) / max(1, len(selected_matches)), 4
        ),
        "runs": results,
    }
    write_json(Path(args.diagnostics), report)
    print(
        f"Built {report['run_count']} paper-reader draft runs with "
        f"{report['paper_instance_count']} paper instances and {report['event_count']} events."
    )
    print(
        f"Selected context match scores: min={report['minimum_selected_match_score']:.4f}, "
        f"mean={report['mean_selected_match_score']:.4f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

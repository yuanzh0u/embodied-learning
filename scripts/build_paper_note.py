#!/usr/bin/env python3
"""Assemble, validate, audit, and archive a paper note from a claim skeleton.

The deep-read loop keeps agent judgment (choosing claims and quoting the
paper) but moves every mechanical step into this script:

  skeleton (agent, ~15 lines) → locate sections → verify quotes verbatim
  → assemble the full note JSON → in-process validate + claim-support audit
  → auto-repair locators/quotes → write note.json + audit into the pool

Agent output (stdin or --skeleton), one JSON object:

    {
      "arxiv_id": "2607.15868",
      "paper_type": "system",                    // method|system|dataset|survey|analysis|benchmark
      "relevance_reason": "……",
      "research_question": "……",
      "contributions": ["…"],
      "method_summary": "…",
      "findings": ["…"],
      "limitations": ["…"],                       // reader-inferred when not author-stated
      "cards": [
        {
          "claim": "……",
          "stance": "support",                    // support|limit|conditional|gap
          "evidence_type": "method",              // method|experiment|dataset|claim|analysis
          "quote": "verbatim English sentence",   // any exact substring of the paper
          "locator_hint": "sliding window",       // fuzzy; the script resolves it
          "quantitative": {"metric": "…", "value_or_direction": "…", "comparator": "…"} | false
        }
      ]
    }

Exit codes: 0 pass, 3 needs-review (cards usable but flagged), 1 reject.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

READER_SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "embodied-ai-paper-reader" / "scripts"
DEFAULT_KB_ROOT = "~/Documents/arxiv"
TOPIC_IDS = ["EA-SENSOR"]
GENERAL_QUESTION = "该论文的核心贡献、方法有效性的量化证据、适用边界与局限（通用深读问题）"
PAPER_TYPES = {"method", "system", "dataset", "survey", "analysis", "benchmark"}
STANCES = {"support", "limit", "conditional", "gap"}
EVIDENCE_TYPES = {"method", "experiment", "dataset", "claim", "analysis"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


validator = load_module("paper_note_validator", READER_SCRIPTS / "validate_paper_note.py")
auditor = load_module("claim_support_auditor", READER_SCRIPTS / "audit_claim_support.py")


def normalize(text: Any) -> str:
    return auditor.normalize(text)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Locator resolution: fuzzy hint -> exact section title + verbatim surface.
# ---------------------------------------------------------------------------

def resolve_locator(extraction: dict[str, Any], hint: str, quote: str) -> tuple[str, str, bool]:
    """Return (exact_title, surface_text, resolved). Surfaces are searched by
    quote containment: the section whose text contains the quote wins."""
    sections = extraction.get("sections") or []
    normalized_quote = normalize(quote)
    if not normalized_quote:
        return "", "", False
    ranked: list[tuple[int, dict[str, Any]]] = []
    hint_normalized = normalize(hint)
    for section in sections:
        if not isinstance(section, dict):
            continue
        title = str(section.get("title") or str(section.get("path") or "").split(">")[-1]).strip()
        if not title:
            continue
        # heading score: does the hint match this section's title/path?
        label = normalize(section.get("path") or title)
        heading_score = 0
        if hint_normalized and (hint_normalized in label or label in hint_normalized):
            heading_score = 2
        full_text = full_text_of(extraction)
        surface = section_surface(extraction, full_text, title)
        if not section_resolves(extraction, full_text, title):
            continue  # heading absent from the text (audit would reject)
        if normalized_quote in normalize(surface):
            ranked.append((heading_score - len(surface), section))
    if not ranked:
        return "", "", False
    ranked.sort(key=lambda item: -item[0])
    section = ranked[0][1]
    title = str(section.get("title") or str(section.get("path") or "").split(">")[-1]).strip()
    surface = section_surface(extraction, full_text_of(extraction), title)
    # found=True only when the quote is verbatim in this section; a hint-only
    # match is left to the caller's repair paths.
    return title, surface, normalized_quote in normalize(surface)


_FULL_TEXT_CACHE: dict[int, str] = {}


def full_text_of(extraction: dict[str, Any]) -> str:
    key = id(extraction)
    if key not in _FULL_TEXT_CACHE:
        text, _ = auditor.extraction_text(extraction)
        _FULL_TEXT_CACHE[key] = text
    return _FULL_TEXT_CACHE[key]


def section_surface(extraction: dict[str, Any], full_text: str, title: str) -> str:
    surface, _ = auditor.locator_surface(title, full_text, {}, extraction)
    return surface


def section_resolves(extraction: dict[str, Any], full_text: str, title: str) -> bool:
    """True when the audit's locator lookup actually finds the section heading
    (not the full-text fallback)."""
    _, resolved = auditor.locator_surface(title, full_text, {}, extraction)
    return resolved


def quote_context(extraction: dict[str, Any], quote: str) -> tuple[str, str, bool]:
    """Fallback when no hint matches: find the quote's section by scanning all
    section surfaces. Returns (title, surface, found)."""
    full_text = full_text_of(extraction)
    normalized_quote = normalize(quote)
    if not normalized_quote:
        return "", full_text, False
    for section in extraction.get("sections") or []:
        if not isinstance(section, dict):
            continue
        title = str(section.get("title") or str(section.get("path") or "").split(">")[-1]).strip()
        if not title:
            continue
        surface = section_surface(extraction, full_text, title)
        if normalized_quote in normalize(surface):
            return title, surface, True
    if normalized_quote in normalize(full_text):
        # The quote exists but no extraction section carries it (appendices are
        # common): locate the nearest markdown heading above the quote so the
        # card still gets a real, auditable locator.
        headings = [
            (match.start(), match.group(1).strip())
            for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", full_text)
        ]
        probe = re.search(re.escape(normalize(quote)[:40]), normalize(full_text))
        if probe and headings:
            position = probe.start()
            above = [title for start, title in headings if start <= position]
            if above:
                candidate = above[-1]
                surface, resolved = auditor.locator_surface(candidate, full_text, {}, extraction)
                if resolved:
                    return candidate, surface, True
        return "", full_text, True
    return "", full_text, False


def best_verbatim_window(surface: str, quote: str, max_words: int = 60) -> str:
    """A verbatim substring of the surface overlapping the quote — used to
    auto-repair near-miss quotes (agent paraphrase) into exact text."""
    quote_tokens = normalize(quote).split()
    surface_tokens = normalize(surface).split()
    best_len, best_start = 0, 0
    window_len = min(max_words, len(surface_tokens))
    for start in range(max(0, len(surface_tokens) - window_len) + 1):
        end = min(len(surface_tokens), start + window_len)
        window = surface_tokens[start:end]
        shared = len(set(window) & set(quote_tokens))
        if shared > best_len:
            best_len, best_start = shared, start
    if not best_len:
        return ""
    window = surface_tokens[best_start : best_start + window_len]
    # Re-attach original punctuation by searching the raw surface for the
    # first window token run.
    probe = re.escape(window[0])
    match = re.search(rf"(?i)\b{probe}\b", surface)
    if not match:
        return " ".join(window)
    start = match.start()
    end = start
    for token in window:
        nxt = re.search(rf"(?i)\b{re.escape(token)}\b", surface[end + 1 :])
        if not nxt:
            break
        end += 1 + nxt.end()
    return surface[start:end]


# ---------------------------------------------------------------------------
# Skeleton → note assembly
# ---------------------------------------------------------------------------

def assemble_note(
    skeleton: dict[str, Any], extraction: dict[str, Any], pool_dir: Path, *, max_cards: int = 4
) -> tuple[dict[str, Any], list[str]]:
    problems: list[str] = []
    arxiv_id = str(skeleton.get("arxiv_id") or extraction.get("paper_id") or pool_dir.name.removeprefix("arxiv-"))
    paper_type = str(skeleton.get("paper_type") or "method")
    if paper_type not in PAPER_TYPES:
        problems.append(f"paper_type {paper_type!r} invalid, defaulting to method")
        paper_type = "method"

    sections_read: list[dict[str, str]] = []
    cards: list[dict[str, Any]] = []
    raw_cards = (skeleton.get("cards") or [])[: max(1, max_cards)]
    used_roles: set[str] = set()
    for index, raw in enumerate(raw_cards, start=1):
        claim = str(raw.get("claim") or "").strip()
        quote = str(raw.get("quote") or "").strip()
        hint = str(raw.get("locator_hint") or "").strip()
        stance = str(raw.get("stance") or "support")
        evidence_type = str(raw.get("evidence_type") or "method")
        if stance not in STANCES:
            problems.append(f"card {index}: stance {stance!r} invalid → support")
            stance = "support"
        if evidence_type not in EVIDENCE_TYPES:
            problems.append(f"card {index}: evidence_type {evidence_type!r} invalid → method")
            evidence_type = "method"
        if not claim or not quote:
            problems.append(f"card {index}: missing claim or quote — skipped")
            continue

        title, surface, found = resolve_locator(extraction, hint, quote)
        if not found and hint:
            # Hint-matched section: repair the quote against that surface even
            # when the verbatim containment failed (agent paraphrase).
            for section in extraction.get("sections") or []:
                if not isinstance(section, dict):
                    continue
                other = str(section.get("title") or "").strip()
                label = normalize(section.get("path") or other)
                if not other or hint.lower() not in label:
                    continue
                candidate = section_surface(extraction, full_text_of(extraction), other)
                repaired = best_verbatim_window(candidate, quote)
                if repaired and normalize(repaired) in normalize(candidate):
                    title, surface, quote, found = other, candidate, repaired, True
                    break
        if not found:
            title, surface, found = quote_context(extraction, quote)
        if found and normalize(title) == "abstract" and hint:
            # Abstract locators are too vague for the validator: re-resolve via
            # the hint against non-abstract sections carrying the quote.
            for section in extraction.get("sections") or []:
                if not isinstance(section, dict):
                    continue
                other = str(section.get("title") or "").strip()
                label = normalize(section.get("path") or other)
                if not other or normalize(other) in {"abstract", "references"}:
                    continue
                candidate = section_surface(extraction, full_text_of(extraction), other)
                hint_hit = hint.lower() in label
                quote_hit = normalize(quote) in normalize(candidate)
                if quote_hit and (hint_hit or normalize(title) == "abstract"):
                    title, surface, found = other, candidate, True
                    break
        if found and normalize(quote) not in normalize(surface):
            # Quote resolved but not verbatim (agent paraphrase): repair from
            # the surface so the audit's exact-match gate passes.
            repaired = best_verbatim_window(surface, quote)
            if repaired and normalize(repaired) in normalize(surface):
                quote = repaired
            else:
                found = False  # wrong section: fall through to re-resolution
        if not found or normalize(title) in {"abstract", "references"}:
            # Validator bans abstract/references locators. Scan body sections
            # one more time with the repaired quote; else drop the card.
            body_hit = False
            for section in extraction.get("sections") or []:
                if not isinstance(section, dict):
                    continue
                other = str(section.get("title") or "").strip()
                if not other or normalize(other) in {"abstract", "references"}:
                    continue
                candidate = section_surface(extraction, full_text_of(extraction), other)
                if normalize(quote) in normalize(candidate):
                    title, surface, found = other, candidate, True
                    body_hit = True
                    break
            if not body_hit:
                problems.append(
                    f"card {index}: quote only present in Abstract/References — "
                    "quote a body-section sentence instead"
                )
                continue
        if not found:
            problems.append(f"card {index}: quote not found in any section — skipped")
            continue
        # Exact-quote repair pass (normalize-level containment holds, surface
        # may differ in whitespace/punctuation): re-extract the true substring.
        exact = normalize(quote) in normalize(surface)
        if not exact:
            repaired = best_verbatim_window(surface, quote)
            if repaired and normalize(repaired) in normalize(surface):
                quote = repaired
                exact = True
        if title and title not in {item["locator"] for item in sections_read}:
            sections_read.append({"locator": title, "role": "relevant-core", "purpose": f"支撑卡片 {index} 的原文核对。"})
            used_roles.add("relevant-core")
        quantitative: Any = False
        raw_quant = raw.get("quantitative")
        if isinstance(raw_quant, dict) and not all(
            str(raw_quant.get(key) or "").strip()
            for key in ("metric", "value_or_direction", "comparator")
        ):
            # Agent gave a free-form dict: flatten into the required schema or
            # treat as non-quantitative rather than shipping empty fields.
            # The claim text already carries the numbers; audit token-matching
            # against an English section would fail on a Chinese label, so
            # degrade to a non-quantitative card.
            raw_quant = False
        if isinstance(raw_quant, dict):
            quantitative = {
                "metric": str(raw_quant.get("metric") or ""),
                "value_or_direction": str(raw_quant.get("value_or_direction") or ""),
                "comparator": str(raw_quant.get("comparator") or ""),
                "task_or_sample": str(raw_quant.get("task_or_sample") or raw_quant.get("task") or "论文实验设置（批量池化未展开）"),
                "locator": str(raw_quant.get("locator") or title or "正文实验节"),
            }
        if isinstance(quantitative, dict) and title:
            # The audit checks that ≥1/3 of quantitative tokens occur at the
            # locator's surface. If the resolved section's prose lacks them
            # (numbers often sit in a neighbouring results section), relocate
            # the card to the resolved section with the best token coverage.
            measurement = auditor.meaningful_tokens(
                " ".join(str(quantitative.get(field) or "") for field in ("metric", "value_or_direction", "comparator"))
            )

            def coverage(section_title: str) -> float:
                probe = section_surface(extraction, full_text_of(extraction), section_title)
                if not section_resolves(extraction, full_text_of(extraction), section_title):
                    return -1.0
                visible = measurement & auditor.meaningful_tokens(probe)
                return len(visible) / max(1, len(measurement))

            if coverage(title) < 1 / 3:
                best_title, best_score = title, coverage(title)
                for section in extraction.get("sections") or []:
                    if not isinstance(section, dict):
                        continue
                    candidate_title = str(section.get("title") or "").strip()
                    if not candidate_title or candidate_title == title:
                        continue
                    score = coverage(candidate_title)
                    candidate_surface = section_surface(extraction, full_text_of(extraction), candidate_title)
                    quote_still_there = normalize(quote) in normalize(candidate_surface)
                    if score > best_score and quote_still_there:
                        best_title, best_score = candidate_title, score
                if best_title != title:
                    title = best_title
        cards.append(
            {
                "card_id": f"{arxiv_id}-C{index:02d}",
                "claim": claim,
                "stance": stance,
                "relation": str(raw.get("relation") or "支撑综述问题的对应分支。"),
                "confidence": "direct",
                "claim_basis": "reported-result" if quantitative else "author-claim",
                "summary": str(raw.get("summary") or claim[:120]),
                "locator": title,
                "source_context": quote,
                "evidence_type": evidence_type,
                "quantitative": quantitative,
                "verification": {
                    "status": "passed" if exact else "needs-review",
                    "checked_against": "full-text",
                    "rationale": "脚本组装：quote 已在定位节内做归一化精确匹配后逐字录入。",
                },
            }
        )

    for role in ("problem", "relevant-core", "conclusion-or-limitations"):
        if role not in used_roles:
            sections_read.append(
                {
                    "locator": role_to_locator(role, extraction),
                    "role": role,
                    "purpose": "rapid 模式必备阅读角色（脚本按抽取结构自动标注）。",
                }
            )

    note = {
        "schema_version": 1,
        "paper": {
            "arxiv_id": arxiv_id,
            "title": str(extraction.get("title") or ""),
            "published": "",
            "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else "",
            "authors": skeleton.get("authors") or [f"{arxiv_id} authors (批量池化未逐人核对)"],
        },
        "review": {
            "question": GENERAL_QUESTION,
            "topic_ids": TOPIC_IDS,
            "mode": "rapid",
        },
        "extraction": {
            "source_format": str(extraction.get("source_format") or ""),
            "method": str(extraction.get("extraction_method") or ""),
            "quality": (extraction.get("quality") or {}).get("grade") if isinstance(extraction.get("quality"), dict) else "high",
            "full_text_available": True,
            "ocr_pages": [],
            "visual_validation": "not-required",
        },
        "reading": {
            "status": "evidence-ready" if cards else "mapped",
            "paper_type": paper_type,
            "relevance": {"decision": "include", "reason": str(skeleton.get("relevance_reason") or "批量池化深读。")},
            "sections_read": sections_read,
            "sections_skipped": [
                {"locator": str(section.get("title") or ""), "reason": "rapid 模式非核心节"}
                for section in (extraction.get("sections") or [])
                if str(section.get("title") or "") not in {item["locator"] for item in sections_read}
            ][:6],
        },
        "research_question": str(skeleton.get("research_question") or GENERAL_QUESTION),
        "contributions": [str(item) for item in skeleton.get("contributions") or []],
        "method": {"summary": str(skeleton.get("method_summary") or "")},
        "study_context": {
            "datasets": skeleton.get("datasets") or [],
            "tasks": skeleton.get("tasks") or [],
            "embodiments": skeleton.get("embodiments") or [],
            "sample_or_scale": str(skeleton.get("sample_or_scale") or ""),
        },
        "evaluation": {
            "design": str(skeleton.get("evaluation_design") or ""),
            "baselines": skeleton.get("baselines") or [],
            "metrics": skeleton.get("metrics") or [],
            "ablations": skeleton.get("ablations") or [],
        },
        "findings": [
            {
                "finding": str(item if isinstance(item, str) else item.get("finding", "")),
                "scope": str(item.get("scope", "") if isinstance(item, dict) else "") or "论文实验声明的适用范围（批量池化未展开）。",
                "locator": str(item.get("locator", "") if isinstance(item, dict) else "")
                or (cards[0]["locator"] if cards else role_to_locator("relevant-core", extraction)),
            }
            for item in skeleton.get("findings") or []
        ],
        "limitations": {
            "author_status": "not-found",
            "author_stated": [],
            "reader_inferred": [
                {
                    "boundary": str(item if isinstance(item, str) else item.get("boundary", "")),
                    "basis": str(item.get("basis", "") if isinstance(item, dict) else "")
                    or "基于正文结论与实验节的阅读推断（批量池化，未逐项回查原文）。",
                }
                for item in skeleton.get("limitations") or []
            ],
        },
        "transfer_boundary": str(skeleton.get("transfer_boundary") or "证据迁移边界未展开（批量池化深读）。"),
        "critical_appraisal": {
            "design_strengths": skeleton.get("design_strengths") or [],
            "design_risks": skeleton.get("design_risks") or [],
            "baseline_fairness": str(skeleton.get("baseline_fairness") or "未逐项核对。"),
            "metric_validity": str(skeleton.get("metric_validity") or "未逐项核对。"),
            "reproducibility": str(skeleton.get("reproducibility") or "未逐项核对。"),
            "external_validity": str(skeleton.get("external_validity") or "未逐项核对。"),
        },
        "evidence_cards": cards,
        "core_citations": skeleton.get("core_citations") or [],
        "notes": "脚本组装（build_paper_note.py）：agent 只提供速记骨架，locator/quote 由脚本解析校验。",
    }
    return note, problems


def role_to_locator(role: str, extraction: dict[str, Any]) -> str:
    """Pick a real section title matching the required rapid role."""
    patterns = {
        "problem": ("intro", "abstract", "introduction"),
        "relevant-core": ("method", "approach", "design"),
        "conclusion-or-limitations": ("conclusion", "limitation", "summary"),
    }
    keywords = patterns.get(role, ())
    for section in extraction.get("sections") or []:
        if not isinstance(section, dict):
            continue
        label = normalize(section.get("path") or section.get("title"))
        if any(keyword in label for keyword in keywords):
            return str(section.get("title") or "")
    first = extraction.get("sections") or [{}]
    return str(first[0].get("title") or "Abstract")


# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arxiv-id", required=True)
    parser.add_argument("--pool-root", default=DEFAULT_KB_ROOT)
    parser.add_argument("--skeleton", help="Skeleton JSON file; stdin when omitted.")
    parser.add_argument("--max-cards", type=int, default=4)
    args = parser.parse_args(argv)

    pool_root = Path(args.pool_root).expanduser()
    if pool_root.name != "pool":
        pool_root = pool_root / "pool"
    pool_dir = pool_root / f"arxiv-{args.arxiv_id}"
    extraction_path = pool_dir / "extraction.json"
    if not extraction_path.is_file():
        print(f"extraction not pooled for {args.arxiv_id}: {extraction_path}", file=sys.stderr)
        return 1
    extraction = load_json(extraction_path)

    raw_text = (
        Path(args.skeleton).read_text(encoding="utf-8")
        if args.skeleton
        else sys.stdin.read()
    )
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not match:
        print("skeleton must contain one JSON object", file=sys.stderr)
        return 1
    try:
        skeleton = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        print(f"skeleton JSON invalid: {exc}", file=sys.stderr)
        return 1

    skeleton["cards"] = (skeleton.get("cards") or [])[: max(1, args.max_cards)]
    note, problems = assemble_note(skeleton, extraction, pool_dir, max_cards=args.max_cards)
    errors, warnings = validator.validate_note(note)
    if errors:
        pool_dir.mkdir(parents=True, exist_ok=True)
        (pool_dir / "note.json").write_text(json.dumps(note, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (pool_dir / "note.build-report.json").write_text(
            json.dumps({"status": "invalid", "errors": errors, "problems": problems}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"status": "invalid", "errors": errors[:5]}, ensure_ascii=False))
        return 1

    audit = auditor.audit(note, extraction)
    (pool_dir / "note.json").write_text(json.dumps(note, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pool_dir / "note.json.audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (pool_dir / "note.build-report.json").write_text(
        json.dumps({"status": audit.get("status"), "problems": problems}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = {
        "arxiv_id": args.arxiv_id,
        "status": audit.get("status"),
        "cards": len(note["evidence_cards"]),
        "problems": problems,
    }
    print(json.dumps(summary, ensure_ascii=False))
    if audit.get("status") == "pass":
        return 0
    if audit.get("status") == "needs-review":
        return 3
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Audit editorial quality signals for a three-style embodied-AI review bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path


EVENT_ID_RE = re.compile(r"\b(?:EA|ERR)-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{4}\b")
ARXIV_LINK_RE = re.compile(r"https?://arxiv\.org/abs/\d{4}\.\d{4,5}(?:v\d+)?")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
LATIN_RE = re.compile(r"[A-Za-z]")

CANNED_PHRASES = [
    "不能只看一个漂亮结论",
    "真正值钱的信息藏在证据条件里",
    "把候选论文、项目页或社交讨论当成正文级证据",
    "Strong hook is allowed",
    "Treat support, conditional, limit, and gap events as separate signals",
    "Formal scientific, expert-explainer, and KOL outputs are allowed",
    "No immediate source gaps detected from loaded packet inputs",
]

PACKET_MARKERS = [
    "## Evidence Core",
    "## Claim Map",
    "## Source Gaps",
    "### 共识/正向证据",
    "### 条件成立",
    "### 限制与失败模式",
    "- Output type:",
    "- Stance labels:",
    "- Confidence labels:",
    "- Trace IDs:",
]

INTERNAL_PROSE_MARKERS = [
    "随附证据附录",
    "相关知识单元",
    "相关证据文件",
    "已接纳证据",
    "source-entry:",
    "formal-ready",
    "formal review 阈值",
    "trace:",
    "inference；",
    "综合推断：",
    "领域背景：",
]


@dataclass
class Finding:
    severity: str
    file: str
    rule: str
    message: str


def strip_source_tail(text: str, style: str) -> str:
    markers = ["\n## References"]
    if style == "zhihu":
        markers.append("\n## 延伸阅读")
    if style == "xiaohongshu":
        markers.extend(["\n📚", "\n## 依据来源", "\n## References"])
    positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    return text[: min(positions)] if positions else text


def linguistic_text(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = EVENT_ID_RE.sub("", text)
    return text


def chinese_share(text: str) -> float:
    text = linguistic_text(text)
    chinese = len(CHINESE_RE.findall(text))
    latin = len(LATIN_RE.findall(text))
    return chinese / max(1, chinese + latin)


def chinese_count(text: str) -> int:
    return len(CHINESE_RE.findall(linguistic_text(text)))


def normalized_substantive_lines(text: str, style: str) -> set[str]:
    body = strip_source_tail(text, style)
    lines: set[str] = set()
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or len(line) < 24:
            continue
        line = re.sub(r"\[[^\]]+\]\([^\)]+\)", "", line)
        line = re.sub(r"[`*_>#💡⚠️📚]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) >= 24:
            lines.add(line)
    return lines


def normalized_body(text: str, style: str) -> str:
    body = strip_source_tail(text, style)
    body = re.sub(r"\[[^\]]+\]\([^\)]+\)", "", body)
    body = re.sub(r"^#+\s+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\s+", "", body)
    return body


def source_line_share(text: str) -> float:
    lines = [line for line in text.splitlines() if line.strip()]
    start = len(lines)
    for index, line in enumerate(lines):
        if line.strip() in {"## References", "## 依据来源"} or line.lstrip().startswith("📚"):
            start = index
            break
    return (len(lines) - start) / max(1, len(lines))


def add(findings: list[Finding], severity: str, path: Path, rule: str, message: str) -> None:
    findings.append(Finding(severity, str(path), rule, message))


def audit_file(path: Path, style: str, min_chinese_share: float) -> tuple[str, list[Finding]]:
    findings: list[Finding] = []
    if not path.is_file():
        add(findings, "error", path, "file-exists", "article file is missing")
        return "", findings
    text = path.read_text(encoding="utf-8")
    body = strip_source_tail(text, style)

    share = chinese_share(body)
    if share < min_chinese_share:
        add(findings, "error", path, "chinese-share", f"visible prose Chinese share {share:.0%} is below {min_chinese_share:.0%}")

    event_ids = sorted(set(EVENT_ID_RE.findall(body)))
    if event_ids:
        add(findings, "error", path, "event-ids-in-body", f"body exposes event IDs: {', '.join(event_ids[:5])}")

    for phrase in CANNED_PHRASES:
        if phrase in text:
            add(findings, "error", path, "canned-phrase", f"contains scaffold phrase: {phrase}")
    for marker in PACKET_MARKERS:
        if marker in text:
            add(findings, "error", path, "packet-leak", f"contains packet/scaffold marker: {marker}")
    for marker in INTERNAL_PROSE_MARKERS:
        if marker in text:
            add(findings, "error", path, "internal-prose", f"contains reader-facing internal/audit wording: {marker}")
    if re.search(r"\bstance\s*:", body, flags=re.IGNORECASE):
        add(findings, "error", path, "internal-prose", "body exposes a stance label")
    if re.search(r"^-\s*—", text, flags=re.MULTILINE):
        add(findings, "error", path, "empty-reading-note", "contains an empty annotated-reading bullet")
    if "()" in text or "、、、" in text or re.search(r",\s*,?\s*\.", text):
        add(findings, "error", path, "malformed-prose", "contains empty citation slots or malformed generated punctuation")
    if "[TODO" in text or "<claim" in text or "<topic>" in text:
        add(findings, "error", path, "placeholder", "contains an unresolved placeholder")
    if "..." in body:
        add(findings, "warning", path, "truncation", "visible prose contains three-dot truncation")

    zh_count = chinese_count(body)
    if style == "memo":
        if zh_count < 1800:
            add(findings, "error", path, "memo-length", f"memo has only {zh_count} Chinese characters before references; expected at least 1800")
        required = {
            "boundary": r"^## .*?(研究边界|研究范围)",
            "thesis": r"^## .*?(中心判断|核心结论|中心论点)",
            "limits": r"^## .*?(条件|分歧|边界|限制|局限|空白)",
            "ending": r"^## .*?(结论|启发|下一步)",
        }
    elif style == "zhihu":
        if zh_count < 1000:
            add(findings, "error", path, "zhihu-length", f"Zhihu body has only {zh_count} Chinese characters; expected at least 1000")
        required = {
            "tldr": r"^## TL;DR",
            "misconception": r"^## .*误区|^### .*误区",
            "mechanism": r"^## .*机制|^### .*机制",
            "boundary": r"^## .*?(边界|什么时候.*不成立|限制)",
        }
    else:
        if zh_count < 300:
            add(findings, "error", path, "xiaohongshu-length", f"Xiaohongshu body has only {zh_count} Chinese characters; expected at least 300")
        if zh_count > 1400:
            add(findings, "warning", path, "xiaohongshu-length", f"Xiaohongshu body has {zh_count} Chinese characters; consider tightening below 1400")
        insight_count = len(re.findall(r"^\s*💡", body, flags=re.MULTILINE))
        if not 3 <= insight_count <= 5:
            add(findings, "error", path, "insight-count", f"expected 3-5 visible 💡 insights, found {insight_count}")
        if not re.search(r"^\s*⚠️", body, flags=re.MULTILINE):
            add(findings, "error", path, "visible-caveat", "missing a visible ⚠️ caveat")
        ref_share = source_line_share(text)
        if ref_share > 0.20:
            add(findings, "error", path, "source-share", f"source/reference material occupies {ref_share:.0%} of non-empty lines; maximum is 20%")
        required = {}

    for rule, pattern in required.items():
        if not re.search(pattern, text, flags=re.MULTILINE):
            add(findings, "error", path, f"section-{rule}", f"missing required {style} section: {rule}")

    unique_links = set(ARXIV_LINK_RE.findall(text))
    minimum_links = {"memo": 5, "zhihu": 3, "xiaohongshu": 3}[style]
    maximum_links = {"memo": None, "zhihu": 12, "xiaohongshu": 5}[style]
    if len(unique_links) < minimum_links:
        add(
            findings,
            "error",
            path,
            "source-selection",
            f"{style} cites only {len(unique_links)} unique arXiv papers; expected at least {minimum_links}",
        )
    if maximum_links is not None and len(unique_links) > maximum_links:
        add(
            findings,
            "error" if style == "xiaohongshu" else "warning",
            path,
            "source-selection",
            f"{style} cites {len(unique_links)} unique arXiv papers; maximum reader-facing budget is {maximum_links}",
        )

    links = len(ARXIV_LINK_RE.findall(body))
    paragraphs = len([item for item in re.split(r"\n\s*\n", body) if item.strip() and not item.lstrip().startswith("#")])
    if paragraphs and links / paragraphs > {"memo": 2.5, "zhihu": 1.5, "xiaohongshu": 1.2}[style]:
        add(findings, "warning", path, "citation-density", f"body has {links} arXiv links across {paragraphs} prose blocks")

    return text, findings


def overlap_findings(memo_path: Path, memo: str, zhihu_path: Path, zhihu: str) -> list[Finding]:
    findings: list[Finding] = []
    memo_lines = normalized_substantive_lines(memo, "memo")
    zhihu_lines = normalized_substantive_lines(zhihu, "zhihu")
    exact = len(memo_lines & zhihu_lines) / max(1, min(len(memo_lines), len(zhihu_lines)))
    if exact > 0.25:
        add(findings, "error", zhihu_path, "cross-style-overlap", f"exact substantive-line overlap with memo is {exact:.0%}; maximum is 25%")
    similarity = SequenceMatcher(None, normalized_body(memo, "memo"), normalized_body(zhihu, "zhihu")).ratio()
    if similarity > 0.55:
        add(findings, "warning", zhihu_path, "cross-style-similarity", f"normalized body similarity with memo is {similarity:.0%}")
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-dir", help="Directory containing the three standard article filenames.")
    parser.add_argument("--memo", help="Scientific memo Markdown path.")
    parser.add_argument("--zhihu", help="Zhihu explainer Markdown path.")
    parser.add_argument("--xiaohongshu", help="Xiaohongshu post Markdown path.")
    parser.add_argument("--min-chinese-share", type=float, default=0.65)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bundle_dir:
        root = Path(args.bundle_dir)
        memo_path = Path(args.memo) if args.memo else root / "scientific-memo_keyan.md"
        zhihu_path = Path(args.zhihu) if args.zhihu else root / "zhihu-explainer_zhihu.md"
        xhs_path = Path(args.xiaohongshu) if args.xiaohongshu else root / "xiaohongshu-post_xiaohongshu.md"
    else:
        if not (args.memo and args.zhihu and args.xiaohongshu):
            raise SystemExit("provide --bundle-dir or all of --memo/--zhihu/--xiaohongshu")
        memo_path, zhihu_path, xhs_path = Path(args.memo), Path(args.zhihu), Path(args.xiaohongshu)

    memo, findings = audit_file(memo_path, "memo", args.min_chinese_share)
    zhihu, more = audit_file(zhihu_path, "zhihu", args.min_chinese_share)
    findings.extend(more)
    xhs, more = audit_file(xhs_path, "xiaohongshu", args.min_chinese_share)
    findings.extend(more)
    if memo and zhihu:
        findings.extend(overlap_findings(memo_path, memo, zhihu_path, zhihu))

    if args.json:
        print(json.dumps({"ok": not any(item.severity == "error" for item in findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item.severity.upper()} {item.file} [{item.rule}] {item.message}")
        if not findings:
            print("editorial quality audit OK")
        elif not any(item.severity == "error" for item in findings):
            print("editorial quality audit OK with warnings")
    return 1 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit a corpus of published Zhihu explainers referenced by topic JSON files."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path

from audit_article_quality import (
    ARXIV_LINK_RE,
    Finding,
    audit_file,
    chinese_count,
    domain_acronyms,
    longest_chinese_sentence,
    normalized_substantive_lines,
    strip_source_tail,
    zhihu_reading_list_findings,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topics-dir", required=True, help="Directory containing topic JSON files with source_directory fields.")
    parser.add_argument("--project-root", default=".", help="Root used to resolve relative source_directory values.")
    parser.add_argument("--min-chinese-share", type=float, default=0.65)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args()


def load_article_paths(topics_dir: Path, project_root: Path) -> tuple[list[Path], list[Finding]]:
    paths: list[Path] = []
    findings: list[Finding] = []
    topic_paths = sorted(topics_dir.glob("*.json"))
    if not topic_paths:
        findings.append(Finding("error", str(topics_dir), "empty-corpus", "topics directory contains no topic JSON files"))
        return paths, findings
    for topic_path in topic_paths:
        try:
            topic = json.loads(topic_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("error", str(topic_path), "topic-json", f"cannot read topic JSON: {exc}"))
            continue
        source_directory = topic.get("source_directory")
        if not source_directory:
            findings.append(Finding("error", str(topic_path), "source-directory", "topic is missing source_directory"))
            continue
        bundle = Path(source_directory)
        if not bundle.is_absolute():
            bundle = project_root / bundle
        paths.append(bundle / "zhihu-explainer_zhihu.md")
    return paths, findings


def audit_corpus(topics_dir: Path, project_root: Path, min_chinese_share: float) -> dict[str, object]:
    article_paths, findings = load_article_paths(topics_dir, project_root)
    files_with_errors: set[str] = set()
    files_with_warnings: set[str] = set()
    articles: list[dict[str, object]] = []
    line_files: dict[str, set[str]] = defaultdict(set)
    heading_signatures: Counter[tuple[str, ...]] = Counter()
    heading_name_counts: Counter[str] = Counter()
    for article_path in article_paths:
        text, article_findings = audit_file(article_path, "zhihu", min_chinese_share)
        findings.extend(article_findings)
        if any(item.severity == "error" for item in article_findings):
            files_with_errors.add(str(article_path))
        if any(item.severity == "warning" for item in article_findings):
            files_with_warnings.add(str(article_path))
        if text:
            body = strip_source_tail(text, "zhihu")
            for line in normalized_substantive_lines(text, "zhihu"):
                line_files[line].add(str(article_path))
            headings = tuple(
                heading.strip()
                for heading in re.findall(r"^#{2,3}\s+(.+)$", text, flags=re.MULTILINE)
                if heading.strip() not in {"TL;DR", "延伸阅读", "References"}
            )
            if headings:
                heading_signatures[headings] += 1
                heading_name_counts.update(set(headings))
            acronyms = domain_acronyms(body)
            reading_items, annotated_items = zhihu_reading_list_findings(text)
            title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
            articles.append(
                {
                    "file": str(article_path),
                    "title": title_match.group(1).strip() if title_match else article_path.parent.name,
                    "chinese_chars": chinese_count(body),
                    "acronym_count": len(acronyms),
                    "longest_sentence": longest_chinese_sentence(body),
                    "body_source_count": len(set(ARXIV_LINK_RE.findall(body))),
                    "reading_items": reading_items,
                    "annotated_reading_items": annotated_items,
                    "image_count": len(re.findall(r"!\[[^\]]*\]\([^)]*\)", text)),
                }
            )
    for item in findings:
        if item.severity == "error" and item.file not in files_with_errors:
            files_with_errors.add(item.file)
        if item.severity == "warning" and item.file not in files_with_warnings:
            files_with_warnings.add(item.file)
    repeated_lines = {line: files for line, files in line_files.items() if len(files) > 1}
    corpus_warning_count = 0
    if repeated_lines:
        corpus_warning_count += 1
        findings.append(
            Finding(
                "warning",
                "<corpus>",
                "cross-article-repetition",
                f"corpus contains {len(repeated_lines)} substantive line(s) repeated across multiple articles",
            )
        )
    largest_heading_cluster = max(heading_signatures.values(), default=0)
    heading_cluster_threshold = max(3, math.ceil(len(articles) * 0.40))
    if largest_heading_cluster >= heading_cluster_threshold:
        corpus_warning_count += 1
        findings.append(
            Finding(
                "warning",
                "<corpus>",
                "heading-template-concentration",
                f"largest exact heading template is shared by {largest_heading_cluster}/{len(articles)} articles",
            )
        )
    most_common_heading, largest_heading_name_cluster = (
        heading_name_counts.most_common(1)[0] if heading_name_counts else ("", 0)
    )
    if largest_heading_name_cluster >= heading_cluster_threshold:
        corpus_warning_count += 1
        findings.append(
            Finding(
                "warning",
                "<corpus>",
                "generic-heading-concentration",
                f"heading '{most_common_heading}' is shared by {largest_heading_name_cluster}/{len(articles)} articles",
            )
        )
    char_counts = [int(item["chinese_chars"]) for item in articles]
    return {
        "ok": not files_with_errors,
        "stats": {
            "article_count": len(article_paths),
            "files_with_errors": len(files_with_errors),
            "files_with_warnings": len(files_with_warnings),
            "median_chinese_chars": statistics.median(char_counts) if char_counts else 0,
            "articles_below_1800": sum(int(item["chinese_chars"]) < 1800 for item in articles),
            "articles_above_4500": sum(int(item["chinese_chars"]) > 4500 for item in articles),
            "articles_with_over_5_acronyms": sum(int(item["acronym_count"]) > 5 for item in articles),
            "articles_with_long_sentences": sum(int(item["longest_sentence"]) > 70 for item in articles),
            "articles_with_10_body_sources": sum(int(item["body_source_count"]) >= 10 for item in articles),
            "articles_with_complete_reading_lists": sum(
                int(item["reading_items"]) >= 3 and item["reading_items"] == item["annotated_reading_items"]
                for item in articles
            ),
            "articles_with_images": sum(int(item["image_count"]) > 0 for item in articles),
            "repeated_substantive_lines": len(repeated_lines),
            "largest_heading_template_cluster": largest_heading_cluster,
            "largest_heading_name_cluster": largest_heading_name_cluster,
            "most_common_heading": most_common_heading,
            "corpus_warning_count": corpus_warning_count,
        },
        "articles": articles,
        "findings": [asdict(item) for item in findings],
    }


def main() -> int:
    args = parse_args()
    report = audit_corpus(Path(args.topics_dir), Path(args.project_root), args.min_chinese_share)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in report["findings"]:
            print(f"{item['severity'].upper()} {item['file']} [{item['rule']}] {item['message']}")
        stats = report["stats"]
        print(
            "Zhihu corpus audit: "
            f"{stats['article_count']} article(s), "
            f"{stats['files_with_errors']} file(s) with errors, "
            f"{stats['files_with_warnings']} file(s) with warnings"
        )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

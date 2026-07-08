#!/usr/bin/env python3
"""Check knowledge-base link integrity: sources, topic cards, indexes, evidence manifests."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
ARCHIVE_CMD = re.compile(r"git show ([0-9a-f]{7,40}):(.+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root to check.")
    return parser.parse_args()


def parse_frontmatter(text: str) -> dict[str, object]:
    """Minimal YAML-subset frontmatter parser for topic cards."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    data: dict[str, object] = {}
    sources: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_source = False
    for line in text[3:end].splitlines():
        if not line.strip():
            continue
        if not line.startswith(" "):
            in_source = line.strip() == "source:"
            current = None
            if ":" in line and not in_source:
                key, _, value = line.partition(":")
                data[key.strip()] = value.strip()
            continue
        if in_source:
            stripped = line.strip()
            if stripped.startswith("- "):
                current = {}
                sources.append(current)
                stripped = stripped[2:]
            if current is not None and ":" in stripped:
                key, _, value = stripped.partition(":")
                current[key.strip()] = value.strip().strip('"')
    if sources:
        data["source"] = sources
    return data


def git_object_exists(root: Path, ref: str, path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        cwd=root,
        capture_output=True,
    )
    return result.returncode == 0


def registered_source_ids(sources_md: Path) -> set[str]:
    if not sources_md.is_file():
        return set()
    return set(re.findall(r"^## (S-[A-Z0-9-]+)", sources_md.read_text(encoding="utf-8"), flags=re.MULTILINE))


def check_markdown_links(md_file: Path, root: Path) -> list[str]:
    problems = []
    text = md_file.read_text(encoding="utf-8")
    for target in MD_LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (md_file.parent / target).resolve()
        if not resolved.exists():
            problems.append(f"{md_file.relative_to(root)}: broken link -> {target}")
    return problems


def check_sources_md(root: Path) -> list[str]:
    problems = []
    sources_md = root / "knowledge" / "sources.md"
    if not sources_md.is_file():
        return [f"missing file: {sources_md.relative_to(root)}"]
    text = sources_md.read_text(encoding="utf-8")
    for entry_match in re.finditer(r"^## (S-[A-Z0-9-]+)\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL):
        source_id, body = entry_match.group(1), entry_match.group(2)
        retired = "retired" in body
        archive = ARCHIVE_CMD.search(body)
        if retired:
            if not archive:
                problems.append(f"sources.md {source_id}: retired but no `git show <ref>:<file>` archive registered")
            elif not git_object_exists(root, archive.group(1), archive.group(2).strip("`").strip()):
                problems.append(
                    f"sources.md {source_id}: archive object not found: {archive.group(1)}:{archive.group(2)}"
                )
        else:
            file_match = re.search(r"文件：\[[^\]]*\]\(([^)]+)\)", body)
            if file_match:
                resolved = (sources_md.parent / file_match.group(1)).resolve()
                if not resolved.exists():
                    problems.append(f"sources.md {source_id}: active entry file missing -> {file_match.group(1)}")
    return problems


def check_topic_cards(root: Path) -> list[str]:
    problems = []
    known_ids = registered_source_ids(root / "knowledge" / "sources.md")
    for card in sorted(root.glob("knowledge/*/*.md")):
        if card.name == "index.md" or "templates" in card.parts:
            continue
        front = parse_frontmatter(card.read_text(encoding="utf-8"))
        for source in front.get("source", []) or []:
            sid = source.get("id", "")
            rel = card.relative_to(root)
            if sid and sid not in known_ids:
                problems.append(f"{rel}: source id `{sid}` not registered in sources.md")
            archive = source.get("archive", "")
            if source.get("status") == "retired":
                match = ARCHIVE_CMD.search(archive)
                if not match:
                    problems.append(f"{rel}: retired source `{sid}` missing archive `git show <ref>:<file>`")
                elif not git_object_exists(root, match.group(1), match.group(2).strip()):
                    problems.append(f"{rel}: archive object not found: {archive}")
            elif source.get("file"):
                resolved = (card.parent / source["file"]).resolve()
                if not resolved.exists():
                    problems.append(f"{rel}: source file missing -> {source['file']}")
            if re.match(r"lines \d", str(source.get("locator", ""))):
                problems.append(f"{rel}: line-number locator (use semantic anchors per ADR-0002)")
    return problems


def check_evidence_manifests(root: Path) -> list[str]:
    problems = []
    for manifest in sorted(root.glob("evidence/*/run.json")):
        run_dir = manifest.parent
        rel = manifest.relative_to(root)
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{rel}: invalid JSON ({exc})")
            continue
        files = data.get("files", {})
        listed: list[str] = []
        for value in files.values():
            if isinstance(value, str):
                listed.append(value)
            elif isinstance(value, list):
                listed.extend(item for item in value if isinstance(item, str))
        for name in listed:
            if not (run_dir / name).is_file():
                problems.append(f"{rel}: listed file missing -> {name}")
    return problems


def check_index_links(root: Path) -> list[str]:
    problems = []
    for index in [
        root / "knowledge" / "index.md",
        root / "knowledge" / "README.md",
        root / "knowledge" / "embodied-ai" / "index.md",
        root / "knowledge" / "error-governance" / "index.md",
        root / "README.md",
        root / "AGENTS.md",
    ]:
        if index.is_file():
            problems.extend(check_markdown_links(index, root))
    return problems


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    problems = (
        check_sources_md(root)
        + check_topic_cards(root)
        + check_index_links(root)
        + check_evidence_manifests(root)
    )
    if problems:
        print(f"{len(problems)} problem(s):")
        for item in problems:
            print(f"- {item}")
        return 1
    print("knowledge-base links OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

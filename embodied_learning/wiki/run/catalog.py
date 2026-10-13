"""Catalog routing and run-bundle registration (split out of scripts/lib/review_runs.py)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# Route markers for a CURRENT run manifest. Catalogs label the link either
# `[run](...)` or `[run.json](...)` depending on the authoring path; both mean
# "this is the run to publish". Prose labels — 历史版本 / 兼容归档 run /
# 补沉淀 run — mark rows that must NOT be routed into the wiki.
CATALOG_RUN_LINK = re.compile(
    r"\[(?:run|run\.json)\]\((\.\./evidence/[^)\s]+/run\.json)\)"
)
# Contract constants live in embodied_learning.config (single home).
from embodied_learning.config import (
    CITED_PAPER_FLOORS,
    STANDARD_ARTICLES,
    STYLE_TO_ARTICLE,
    STYLE_TO_FILE,
)



def build_trace_map(run_dir: Path, skills_root: Path) -> tuple[bool, list[str]]:
    """Mechanically build ``trace-map.json`` from the deliverables + evidence.

    Pure script work the writer used to do by hand (the file is published in
    finalize_run.PUBLISH_FILES yet nothing built it). Always rebuilt — cheap
    and deterministic. Returns ``(ok, problem_lines)``; ``UNCOVERED`` lines
    name papers the deliverables cite without evidence backing, a
    fix-and-rerun condition for the writer, never a stop."""
    import subprocess
    import sys

    builder = skills_root / "embodied-ai-review-writer" / "scripts" / "write.py"
    evidence = run_dir / "evidence.jsonl"
    if not evidence.is_file():
        return False, [f"trace-map 输入缺失：{evidence}（先跑驱动/consolidate 生成 evidence.jsonl）"]
    if not builder.is_file():
        return False, [f"trace-map 构建器缺失：{builder}"]
    articles = [name for name in STANDARD_ARTICLES if (run_dir / name).is_file()]
    if not articles:
        return True, []  # writer 未写成稿：无物可映射
    command = [sys.executable, str(builder), "build-trace-map", "--evidence-jsonl", str(evidence)]
    for name in articles:
        command += ["--article", str(run_dir / name)]
    command += ["--output", str(run_dir / "trace-map.json")]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        lines = [line.strip() for line in (result.stdout or "").splitlines() if line.strip()]
        return False, lines or [f"build-trace-map exit {result.returncode}：{(result.stderr or '')[-200:]}"]
    return True, []


@dataclass(frozen=True)
class ReviewRun:
    """A settled, minimally complete review selected by the current catalog."""

    manifest_path: Path
    manifest: dict[str, object]

    @property
    def directory(self) -> Path:
        return self.manifest_path.parent

    @property
    def topic(self) -> str:
        return str(self.manifest["topic"])


def _under(path: Path, ancestor: Path) -> bool:
    try:
        path.resolve().relative_to(ancestor.resolve())
        return True
    except ValueError:
        return False


def catalog_run_paths(root: Path, catalog_path: Path | None = None) -> list[Path]:
    """Return the unique run manifests explicitly routed by the current catalog."""

    root = root.resolve()
    catalog = (catalog_path or root / "knowledge" / "literature-review-catalog.md").resolve()
    if not _under(catalog, root):
        raise ValueError(f"catalog escapes repository root: {catalog}")
    if not catalog.is_file():
        raise ValueError(f"catalog not found: {catalog}")

    relative_links = CATALOG_RUN_LINK.findall(catalog.read_text(encoding="utf-8"))
    if not relative_links:
        # An empty catalog is a valid first-run shape: it routes zero runs and
        # the wiki publishes an empty index instead of failing.
        return []

    evidence_root = (root / "evidence").resolve()
    paths: set[Path] = set()
    for link in relative_links:
        path = (catalog.parent / link).resolve()
        if not _under(path, evidence_root):
            raise ValueError(f"catalog run escapes evidence root: {link}")
        if path.name != "run.json":
            raise ValueError(f"catalog target is not a run manifest: {link}")
        paths.add(path)
    return sorted(paths, key=lambda item: item.relative_to(root).as_posix())


def evidence_paths(
    run_json: Path,
    manifest: dict[str, object],
    *,
    require_files: bool = True,
) -> list[Path]:
    """Resolve the self-contained evidence files declared by one run."""

    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError(f"{run_json}: files must be an object")

    names: list[str] = []
    evidence = files.get("evidence")
    if isinstance(evidence, str):
        names.append(evidence)
    reused = files.get("reused_evidence")
    if isinstance(reused, list):
        names.extend(item for item in reused if isinstance(item, str))
    if not names:
        raise ValueError(f"{run_json}: no local evidence file is declared")

    run_dir = run_json.parent.resolve()
    resolved: list[Path] = []
    for name in names:
        path = (run_dir / name).resolve()
        if not _under(path, run_dir):
            raise ValueError(f"{run_json}: evidence path escapes run directory: {name}")
        if require_files and not path.is_file():
            raise ValueError(f"{run_json}: declared evidence file is missing: {name}")
        resolved.append(path)
    return resolved


def reader_articles(
    run_json: Path,
    manifest: dict[str, object],
    *,
    require_files: bool = True,
) -> tuple[str, ...]:
    """Return the declared reader-facing articles for a settled run.

    Three articles remain the default contract. A run may intentionally publish
    one supported style only when both ``style`` and ``scope_note`` are present,
    matching ``run.py check-bundle``.
    """

    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError(f"{run_json}: files must be an object")
    outputs = files.get("outputs")
    if outputs is not None and (
        not isinstance(outputs, list) or any(not isinstance(item, str) for item in outputs)
    ):
        raise ValueError(f"{run_json}: files.outputs must be a string list")

    style = manifest.get("style")
    if style is None:
        articles = STANDARD_ARTICLES
    else:
        if not isinstance(style, str) or style not in STYLE_TO_ARTICLE:
            supported = ", ".join(sorted(STYLE_TO_ARTICLE))
            raise ValueError(f"{run_json}: unsupported reduced-scope style {style!r}; use {supported}")
        if not str(manifest.get("scope_note") or "").strip():
            raise ValueError(f"{run_json}: reduced-scope style requires scope_note")
        if outputs is None:
            raise ValueError(f"{run_json}: reduced-scope style requires files.outputs")
        articles = (STYLE_TO_ARTICLE[style],)

    for name in articles:
        if isinstance(outputs, list) and name not in outputs:
            raise ValueError(f"{run_json}: reader-facing article is not listed in files.outputs: {name}")
        if require_files and not (run_json.parent / name).is_file():
            raise ValueError(f"{run_json}: missing reader-facing article: {name}")
    return articles


def load_catalog_runs(
    root: Path,
    catalog_path: Path | None = None,
    *,
    require_settled: bool = True,
    require_complete: bool = True,
) -> list[ReviewRun]:
    """Load catalog-selected runs through one shared minimal trust boundary.

    Deep evidence, citation, and editorial gates remain the responsibility of
    ``validate_current_reviews.py``. This loader guarantees that every consumer
    starts from the same current version and never sees an incomplete triplet.
    """

    runs: list[ReviewRun] = []
    for run_json in catalog_run_paths(root, catalog_path):
        if not run_json.is_file():
            raise ValueError(f"catalog run manifest is missing: {run_json}")
        try:
            manifest = json.loads(run_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid run manifest JSON: {run_json}: {exc}") from exc
        if not isinstance(manifest, dict):
            raise ValueError(f"run manifest must be an object: {run_json}")
        topic = manifest.get("topic")
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError(f"catalog run has no topic: {run_json}")
        if require_settled and manifest.get("status") != "settled":
            raise ValueError(f"catalog routes to non-settled run: {run_json}")
        evidence_paths(run_json, manifest, require_files=require_complete)
        if require_complete:
            reader_articles(run_json, manifest)
        runs.append(ReviewRun(run_json, manifest))
    return runs


def event_consistency_problems(run_paths: Iterable[Path]) -> list[str]:
    """Allow exact event reuse while rejecting ID collisions or local duplicates."""

    owners: dict[str, tuple[str, str]] = {}
    problems: list[str] = []
    for run_json in run_paths:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
        for evidence_path in evidence_paths(run_json, manifest):
            local_ids: set[str] = set()
            for line_number, line in enumerate(
                evidence_path.read_text(encoding="utf-8").splitlines(), 1
            ):
                if not line.strip():
                    continue
                event = json.loads(line)
                event_id = str(event.get("event_id") or "")
                if not event_id:
                    problems.append(f"{evidence_path}:{line_number}: missing event_id")
                    continue
                if event_id in local_ids:
                    problems.append(f"{evidence_path}:{line_number}: duplicate event_id {event_id}")
                    continue
                local_ids.add(event_id)

                canonical = json.dumps(
                    event, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                )
                prior = owners.get(event_id)
                location = f"{evidence_path}:{line_number}"
                if prior is None:
                    owners[event_id] = (canonical, location)
                elif prior[0] != canonical:
                    problems.append(
                        f"event_id {event_id} differs between {prior[1]} and {location}"
                    )
    return problems


def _catalog_row_from_manifest(run_json: Path, manifest: dict) -> str:
    """A minimal but truthful 成果索引 row; the agent may enrich it later.

    规模 = 候选池 / 可读全文 / 精读并接纳论文数 (column semantics per the
    catalog header). run.py finalize stamps candidate_count / full_text_count
    / evidence_papers into run.json from pipeline-summary.json + the evidence
    set, so the row carries the real triple instead of "— / — / N".
    """

    topic = str(manifest.get("topic") or run_json.parent.name)
    knowledge_ids = manifest.get("knowledge_ids")
    cards = "、".join(knowledge_ids) if isinstance(knowledge_ids, list) and knowledge_ids else ""

    def fmt(value: object) -> str:
        return str(value) if isinstance(value, int) and value > 0 else "—"

    scale = " / ".join(
        fmt(manifest.get(key))
        for key in ("candidate_count", "full_text_count", "evidence_papers")
    )
    run_rel = f"../evidence/{run_json.parent.name}/run.json"
    return f"| LR-{topic[:24]} | {topic} | {cards} | {scale} | [run]({run_rel}) |"


def register_run_in_catalog(
    kb_root: Path,
    run_json_path: Path,
    row: str | None = None,
    *,
    catalog_path: Path | None = None,
) -> bool:
    """Append one 成果索引 row for a settled run; returns False when already
    registered (idempotent — safe to call from both launch_review and the
    agent-settle path).

    Concurrency: the read→append→write round trip runs under the KB-shared
    ``catalog`` lock (two machines settling at once would otherwise lose one
    row), and the write itself is atomic. The link check keys on
    ``../evidence/<run>/run.json`` — the same anchor the routing layer parses.
    """

    from embodied_learning.atomicio import atomic_write_text
    from embodied_learning import locks

    kb_root = kb_root.resolve()
    catalog = (catalog_path or kb_root / "knowledge" / "literature-review-catalog.md").resolve()
    run_json_path = run_json_path.resolve()
    manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
    row = row or _catalog_row_from_manifest(run_json_path, manifest)
    link = f"../evidence/{run_json_path.parent.name}/run.json"

    with locks.kb_lock(kb_root, "catalog"):
        if catalog.is_file() and link in catalog.read_text(encoding="utf-8"):
            return False
        content = catalog.read_text(encoding="utf-8") if catalog.is_file() else ""
        lines = content.splitlines()
        # Join the last existing evidence-link table row; append at end when
        # the catalog has no table yet.
        insert_at = None
        for index in range(len(lines) - 1, -1, -1):
            if "](../evidence/" in lines[index] and lines[index].lstrip().startswith("|"):
                insert_at = index + 1
                break
        if insert_at is None:
            if content and not content.endswith("\n"):
                content += "\n"
            content += row + "\n"
        else:
            lines.insert(insert_at, row)
            content = "\n".join(lines) + "\n"
        catalog.parent.mkdir(parents=True, exist_ok=True)
        atomic_write_text(catalog, content)
    return True

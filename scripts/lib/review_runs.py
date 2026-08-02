"""Canonical loading helpers for catalog-routed literature-review runs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CATALOG_RUN_LINK = re.compile(r"\]\((\.\./evidence/[^)\s]+/run\.json)\)")
STANDARD_ARTICLES = (
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
)


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
        raise ValueError(f"no run manifests routed by {catalog.relative_to(root)}")

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
            missing = [name for name in STANDARD_ARTICLES if not (run_json.parent / name).is_file()]
            if missing:
                raise ValueError(f"{run_json}: missing reader-facing articles: {', '.join(missing)}")
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

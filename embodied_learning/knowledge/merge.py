"""KB merge: fold runs, pool papers, topic cards, and site slugs from source roots into a target KB.

Newer-wins by default (``prefer="newer"``): runs compare ``run.json`` mtime,
pool papers compare ``meta.json.added_at``, cards compare file mtime. Shared
files (``pool/index.jsonl``, the catalog, ``wiki/site-config.json``) are
rewritten under the KB locks; per-run copies are lock-free.

Library entry is :func:`kb_merge`; the CLI is ``wiki.py kb-merge``. Always
``--dry-run`` first against a CIFS root — stat caches make mtimes unreliable
there (``prefer="target"`` / ``"source"`` are the escape hatches).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from embodied_learning import locks
from embodied_learning.atomicio import atomic_write_json, atomic_write_text
from embodied_learning.knowledge.model import KnowledgeBase
from embodied_learning.knowledge.pool import read_index, write_index

SCHEMA_VERSION = 1
WHAT = ("runs", "pool", "cards", "slugs")
DEFAULT_WHAT = frozenset({"runs", "pool", "cards"})  # slugs are opt-in (--what slugs)
PREFER = ("newer", "target", "source")
CARD_DIRS = ("embodied-ai", "error-governance")


# ---- freshness ---------------------------------------------------------------


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def _run_freshness(run_dir: Path) -> float:
    return _mtime(run_dir / "run.json")


def _pool_freshness(paper_dir: Path) -> tuple[str, float]:
    """Return (added_at ISO, mtime fallback) — ISO compares lexicographically."""
    meta_path = paper_dir / "meta.json"
    added_at = ""
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if isinstance(meta, dict):
            added_at = str(meta.get("added_at") or "")
    except (OSError, json.JSONDecodeError):
        pass
    return added_at, _mtime(meta_path or paper_dir)


def _source_wins(src_key: tuple[str, float], dst_key: tuple[str, float], prefer: str) -> bool:
    """True when the source copy should replace the target copy."""
    if prefer == "source":
        return True
    if prefer == "target":
        return False
    src_iso, src_mt = src_key
    dst_iso, dst_mt = dst_key
    if src_iso and dst_iso:
        return src_iso > dst_iso
    return src_mt > dst_mt


def _file_wins(src: Path, dst: Path, prefer: str) -> bool:
    return _source_wins((_mtime_as_iso(src), _mtime(src)), (_mtime_as_iso(dst), _mtime(dst)), prefer)


def _mtime_as_iso(path: Path) -> str:
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat()
    except OSError:
        return ""


# ---- copy helpers ------------------------------------------------------------


def _dir_bytes(path: Path) -> int:
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
            except OSError:
                pass
    return total


def _copy_tree(src: Path, dst: Path) -> int:
    """Replace ``dst`` with a copy of ``src``. Returns bytes copied."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return _dir_bytes(dst)


# ---- shared-file merges ------------------------------------------------------


def _merge_pool_index(target: KnowledgeBase, pending: dict[str, dict[str, Any]], *, dry_run: bool) -> int:
    """Fold ``pending`` entries into ``pool/index.jsonl`` under the pool lock."""
    if not pending or dry_run:
        return 0
    with locks.kb_lock(target.root, "pool-index"):
        entries = read_index(target.pool_dir) if (target.pool_dir / "index.jsonl").is_file() else {}
        added = 0
        for key, value in pending.items():
            if key not in entries:
                added += 1
            entries[key] = value
        write_index(target.pool_dir, entries)
    return added


def _catalog_row(run_json: Path, manifest: dict[str, Any]) -> str:
    from embodied_learning.wiki.run.catalog import _catalog_row_from_manifest

    return _catalog_row_from_manifest(run_json, manifest)


def _register_catalog_row(target: KnowledgeBase, run_name: str, *, dry_run: bool) -> str:
    """Append (or keep) the catalog row for a freshly copied run.

    Returns ``added`` | ``present`` | ``skipped``.
    """
    if dry_run:
        return "skipped"
    from embodied_learning.wiki.run.catalog import register_run_in_catalog

    run_json = target.evidence_dir / run_name / "run.json"
    if not run_json.is_file():
        return "skipped"
    added = register_run_in_catalog(target.root, run_json)
    return "added" if added else "present"


def _replace_catalog_row(target: KnowledgeBase, run_name: str, *, dry_run: bool) -> str:
    """Rewrite the catalog row of an overwritten run from its new run.json."""
    if dry_run:
        return "skipped"
    from embodied_learning.wiki.run.catalog import _catalog_row_from_manifest

    run_json = target.evidence_dir / run_name / "run.json"
    catalog = target.knowledge_dir / "literature-review-catalog.md"
    if not run_json.is_file() or not catalog.is_file():
        return "skipped"
    try:
        manifest = json.loads(run_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "skipped"
    row = _catalog_row_from_manifest(run_json, manifest)
    link = f"../evidence/{run_name}/run.json"
    with locks.kb_lock(target.root, "catalog"):
        lines = catalog.read_text(encoding="utf-8").splitlines()
        replaced = False
        for index, line in enumerate(lines):
            if line.lstrip().startswith("|") and link in line:
                lines[index] = row
                replaced = True
                break
        if replaced:
            atomic_write_text(catalog, "\n".join(lines) + "\n")
    return "replaced" if replaced else "skipped"


def _merge_site_slugs(
    target: KnowledgeBase,
    source: KnowledgeBase,
    *,
    prefer: str,
    dry_run: bool,
) -> tuple[int, int]:
    """Fold ``wiki/site-config.json`` topic slug/aliases into the target config.

    Site metadata (``site``/``fields``) is taken from the source when the
    target has none. Returns (added, overwritten).
    """
    src_cfg_path = source.site_config
    if not src_cfg_path.is_file():
        return 0, 0
    try:
        src_cfg = json.loads(src_cfg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0, 0
    if not isinstance(src_cfg, dict):
        return 0, 0
    src_topics = src_cfg.get("topics") if isinstance(src_cfg.get("topics"), dict) else {}

    dst_cfg: dict[str, Any] = {}
    if target.site_config.is_file():
        try:
            loaded = json.loads(target.site_config.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                dst_cfg = loaded
        except (OSError, json.JSONDecodeError):
            dst_cfg = {}
    dst_topics = dst_cfg.get("topics") if isinstance(dst_cfg.get("topics"), dict) else {}

    added = 0
    overwritten = 0
    for key, value in src_topics.items():
        if key not in dst_topics:
            dst_topics[key] = value
            added += 1
        elif _file_wins(src_cfg_path, target.site_config, prefer):
            dst_topics[key] = value
            overwritten += 1

    if (added or overwritten) and not dry_run:
        if "schema_version" not in dst_cfg:
            dst_cfg["schema_version"] = 1
        if "site" not in dst_cfg and isinstance(src_cfg.get("site"), dict):
            dst_cfg["site"] = src_cfg["site"]
        if "fields" not in dst_cfg and isinstance(src_cfg.get("fields"), dict):
            dst_cfg["fields"] = src_cfg["fields"]
        dst_cfg["topics"] = dst_topics
        with locks.kb_lock(target.root, "site-config"):
            atomic_write_json(target.site_config, dst_cfg)
    return added, overwritten


# ---- wiki rebuild ------------------------------------------------------------


def _rebuild_wiki(target: KnowledgeBase) -> dict[str, Any]:
    """Republish the target's wiki snapshot. Private-KB fallback when the
    site-config does not exactly cover the current topics (its validator
    rejects both missing and orphaned slug entries)."""
    from embodied_learning.wiki.publish import snapshot as snap

    source = target.knowledge_dir / "literature-review-catalog.md"
    output = target.wiki_data_dir
    config = target.site_config if target.site_config.is_file() else None
    attempts: list[Path | None] = [config, None] if config is not None else [None]
    last_error = ""
    for site_config in attempts:
        try:
            manifest = snap.publish_snapshot(source, output, site_config=site_config, retain=2)
            stats = manifest.get("stats") if isinstance(manifest.get("stats"), dict) else {}
            return {
                "rebuilt": True,
                "site_config": str(site_config) if site_config else None,
                "published_topics": int(stats.get("published_topics") or 0),
                "snapshot_id": str(manifest.get("snapshot_id") or ""),
            }
        except (RuntimeError, ValueError, OSError) as exc:
            last_error = str(exc)
            continue
    return {"rebuilt": False, "error": last_error, "published_topics": 0, "snapshot_id": ""}


# ---- the merge ---------------------------------------------------------------


def kb_merge(
    target: KnowledgeBase,
    sources: list[KnowledgeBase],
    *,
    what: frozenset[str] = DEFAULT_WHAT,
    prefer: str = "newer",
    dry_run: bool = False,
    rebuild_wiki: bool = True,
) -> dict[str, Any]:
    """Fold every source into ``target``. Pure report — side effects unless ``dry_run``."""
    if prefer not in PREFER:
        raise ValueError(f"unknown prefer {prefer!r}; expected one of {PREFER}")
    unknown = sorted(what - set(WHAT))
    if unknown:
        raise ValueError(f"unknown what {unknown!r}; expected subset of {WHAT}")

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "target": str(target.root),
        "sources": [str(src.root) for src in sources],
        "dry_run": dry_run,
        "prefer": prefer,
        "what": sorted(what),
        "runs": {"copied": 0, "overwritten": 0, "skipped_target_newer": 0, "errors": []},
        "pool": {"copied": 0, "overwritten": 0, "skipped_target_newer": 0, "index_merged": 0},
        "cards": {"copied": 0, "overwritten": 0, "skipped_target_newer": 0, "unrouted_ids": []},
        "slugs": {"added": 0, "overwritten": 0},
        "catalog": {"rows_added": 0, "rows_replaced": 0},
        "wiki": {"rebuilt": False, "published_topics": 0, "snapshot_id": ""},
        "bytes_copied": 0,
    }

    pending_index: dict[str, dict[str, Any]] = {}
    new_card_ids: list[str] = []
    routed = _routed_card_ids(target)

    for source in sources:
        if "runs" in what:
            _merge_runs(source, target, prefer=prefer, dry_run=dry_run, report=report)
        if "pool" in what:
            _merge_pool(source, target, prefer=prefer, dry_run=dry_run, report=report, pending_index=pending_index)
        if "cards" in what:
            _merge_cards(source, target, prefer=prefer, dry_run=dry_run, report=report, new_card_ids=new_card_ids)
        if "slugs" in what:
            added, overwritten = _merge_site_slugs(target, source, prefer=prefer, dry_run=dry_run)
            report["slugs"]["added"] += added
            report["slugs"]["overwritten"] += overwritten

    if pending_index:
        report["pool"]["index_merged"] = _merge_pool_index(target, pending_index, dry_run=dry_run)

    report["cards"]["unrouted_ids"] = sorted(set(new_card_ids) - routed)

    if rebuild_wiki and not dry_run:
        report["wiki"] = _rebuild_wiki(target)
    return report


def _routed_card_ids(target: KnowledgeBase) -> set[str]:
    index = target.knowledge_dir / "index.md"
    if not index.is_file():
        return set()
    try:
        text = index.read_text(encoding="utf-8")
    except OSError:
        return set()
    return {card.card_id for card in target.cards() if card.card_id in text}


def _merge_runs(
    source: KnowledgeBase,
    target: KnowledgeBase,
    *,
    prefer: str,
    dry_run: bool,
    report: dict[str, Any],
) -> None:
    for src_run in source.runs():
        name = src_run.name
        src_dir = source.evidence_dir / name
        dst_dir = target.evidence_dir / name
        try:
            if dst_dir.is_dir():
                if not _source_wins(
                    ("", _run_freshness(src_dir)),
                    ("", _run_freshness(dst_dir)),
                    prefer,
                ):
                    report["runs"]["skipped_target_newer"] += 1
                    continue
                if not dry_run:
                    report["bytes_copied"] += _copy_tree(src_dir, dst_dir)
                    outcome = _replace_catalog_row(target, name, dry_run=dry_run)
                    if outcome == "replaced":
                        report["catalog"]["rows_replaced"] += 1
                report["runs"]["overwritten"] += 1
            else:
                if not dry_run:
                    dst_dir.parent.mkdir(parents=True, exist_ok=True)
                    report["bytes_copied"] += _copy_tree(src_dir, dst_dir)
                    outcome = _register_catalog_row(target, name, dry_run=dry_run)
                    if outcome == "added":
                        report["catalog"]["rows_added"] += 1
                else:
                    report["catalog"]["rows_added"] += 1
                report["runs"]["copied"] += 1
        except OSError as exc:
            report["runs"]["errors"].append(f"{name}: {exc}")


def _merge_pool(
    source: KnowledgeBase,
    target: KnowledgeBase,
    *,
    prefer: str,
    dry_run: bool,
    report: dict[str, Any],
    pending_index: dict[str, dict[str, Any]],
) -> None:
    src_index = read_index(source.pool_dir) if (source.pool_dir / "index.jsonl").is_file() else {}
    for paper in source.papers():
        src_dir = paper.path
        dst_dir = target.pool_dir / paper.dir_name
        src_key = _pool_freshness(src_dir)
        if dst_dir.is_dir():
            if not _source_wins(src_key, _pool_freshness(dst_dir), prefer):
                report["pool"]["skipped_target_newer"] += 1
                continue
            if not dry_run:
                report["bytes_copied"] += _copy_tree(src_dir, dst_dir)
            report["pool"]["overwritten"] += 1
        else:
            if not dry_run:
                dst_dir.parent.mkdir(parents=True, exist_ok=True)
                report["bytes_copied"] += _copy_tree(src_dir, dst_dir)
            report["pool"]["copied"] += 1
        if paper.dir_name in src_index:
            pending_index[paper.dir_name] = src_index[paper.dir_name]


def _merge_cards(
    source: KnowledgeBase,
    target: KnowledgeBase,
    *,
    prefer: str,
    dry_run: bool,
    report: dict[str, Any],
    new_card_ids: list[str],
) -> None:
    for card in source.cards():
        rel = card.path.relative_to(source.knowledge_dir)
        dst = target.knowledge_dir / rel
        if dst.is_file():
            if not _file_wins(card.path, dst, prefer):
                report["cards"]["skipped_target_newer"] += 1
                continue
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(card.path, dst)
            report["cards"]["overwritten"] += 1
        else:
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(card.path, dst)
            report["cards"]["copied"] += 1
            new_card_ids.append(card.card_id)


# ---- presentation ------------------------------------------------------------


def render(report: dict[str, Any]) -> str:
    lines = [
        f"KB 合并 → {report.get('target', '')}"
        + ("（dry-run，未落盘）" if report.get("dry_run") else ""),
        f"  来源：{', '.join(report.get('sources') or [])}",
        f"  范围：{', '.join(report.get('what') or [])}   prefer={report.get('prefer')}",
        "",
    ]
    runs = report.get("runs", {})
    lines.append(
        f"runs    拷入 {runs.get('copied', 0)} · 覆盖 {runs.get('overwritten', 0)}"
        f" · 跳过（目标更新） {runs.get('skipped_target_newer', 0)}"
    )
    if runs.get("errors"):
        for err in runs["errors"][:5]:
            lines.append(f"        错误：{err}")
    pool = report.get("pool", {})
    lines.append(
        f"pool    拷入 {pool.get('copied', 0)} · 覆盖 {pool.get('overwritten', 0)}"
        f" · 跳过（目标更新） {pool.get('skipped_target_newer', 0)}"
        f" · index 合并 {pool.get('index_merged', 0)}"
    )
    cards = report.get("cards", {})
    lines.append(
        f"cards   拷入 {cards.get('copied', 0)} · 覆盖 {cards.get('overwritten', 0)}"
        f" · 跳过（目标更新） {cards.get('skipped_target_newer', 0)}"
    )
    unrouted = cards.get("unrouted_ids") or []
    if unrouted:
        preview = "、".join(unrouted[:5]) + ("…" if len(unrouted) > 5 else "")
        lines.append(f"        未入 index.md 路由 {len(unrouted)} 张（{preview}）")
    slugs = report.get("slugs", {})
    lines.append(f"slugs   新增 {slugs.get('added', 0)} · 覆盖 {slugs.get('overwritten', 0)}")
    catalog = report.get("catalog", {})
    lines.append(f"catalog 行新增 {catalog.get('rows_added', 0)} · 重写 {catalog.get('rows_replaced', 0)}")
    wiki = report.get("wiki", {})
    if wiki.get("rebuilt"):
        lines.append(
            f"wiki    快照已重建：{wiki.get('published_topics', 0)} 个话题"
            f"（site-config: {wiki.get('site_config') or '无（私有模式）'}）"
        )
    elif report.get("dry_run"):
        lines.append("wiki    dry-run 未重建")
    else:
        lines.append(f"wiki    重建失败：{wiki.get('error', '')}")
    lines.append(f"字节    {report.get('bytes_copied', 0)}")
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in scripts/wiki.py."""
    target = KnowledgeBase.open(args.kb_root)
    if not target.root.is_dir():
        print(f"KB root 不存在：{target.root}", file=sys.stderr)
        return 1
    sources: list[KnowledgeBase] = []
    for raw in args.source or []:
        src = KnowledgeBase.open(raw)
        if not src.root.is_dir():
            print(f"来源 KB root 不存在：{src.root}", file=sys.stderr)
            return 1
        sources.append(src)
    if not sources:
        print("至少需要一个 --source", file=sys.stderr)
        return 2

    what_raw = getattr(args, "what", None) or list(DEFAULT_WHAT)
    try:
        report = kb_merge(
            target,
            sources,
            what=frozenset(what_raw),
            prefer=str(getattr(args, "prefer", "newer") or "newer"),
            dry_run=bool(getattr(args, "dry_run", False)),
            rebuild_wiki=not bool(getattr(args, "no_wiki", False)),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if getattr(args, "json", False):
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render(report))
    return 0

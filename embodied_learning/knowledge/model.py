"""Domain model for a knowledge-base root — the wiki's data structure lives here.

Layout::

    <kb-root>/
        evidence/<run>/     run.json + evidence.jsonl + deliverables + revisions/
        pool/<dir>/         meta.json + extraction.json + paper.md + note.json
        knowledge/          literature-review-catalog.md + {embodied-ai,error-governance}/*.md
        wiki/data/          snapshots/<id>/{manifest.json,topics/*.json}

Roles: ``knowledge/`` owns the data structures and downstream consumption of
results (stats / search / merge); ``wiki/run/`` is the single-review
generation workflow that writes these structures; ``wiki/publish/`` is
display/reading that renders them.

Reading is tolerant: corrupt JSON records are skipped, absent files read as
empty. Meaning invariants — full text = ``paper.md`` exists, deep read =
``note.json`` exists (presence, not audit-passed), event ids accept both the
current ``event_id`` and the legacy ``id`` key.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from embodied_learning.config import STYLE_TO_FILE
from embodied_learning.knowledge.pool import read_index
from embodied_learning.utils.jsonio import load_json

# Deliverable styles a reader can view (the wiki version keys). Survey/review-
# packet is a briefing, not a reader article — same split as snapshot.VERSION_FILES.
VERSION_FILES: dict[str, tuple[str, str]] = {
    "keyan": ("科研备忘录", "scientific-memo_keyan.md"),
    "zhihu": ("知乎解释版", "zhihu-explainer_zhihu.md"),
    "xiaohongshu": ("小红书版", "xiaohongshu-post_xiaohongshu.md"),
}
REVISION_FILE_RE = re.compile(r"^(keyan|zhihu|xiaohongshu)-v(\d+)$")

CARD_DIRS: tuple[str, ...] = ("embodied-ai", "error-governance")
CATALOG_RUN_LINK = re.compile(r"\[(?:run|run\.json)\]\(\.\./evidence/([^)\s]+)/run\.json\)")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _read_json(path: Path) -> Any:
    try:
        return load_json(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _int_or_none(value: Any) -> int | None:
    return value if isinstance(value, int) else None


# ---- atomic types ------------------------------------------------------------


@dataclass(frozen=True)
class EvidenceEvent:
    """One evidence record from a run's ``evidence.jsonl``."""

    event_id: str
    topic_id: str
    claim: str
    stance: str
    confidence: str
    paper_id: str
    paper_title: str
    run_name: str
    raw: dict[str, Any] = field(repr=False)

    @classmethod
    def from_record(cls, record: dict[str, Any], *, run_name: str) -> "EvidenceEvent":
        paper = record.get("paper") if isinstance(record.get("paper"), dict) else {}
        event_id = str(record.get("event_id") or record.get("id") or "")
        return cls(
            event_id=event_id,
            topic_id=str(record.get("topic_id") or ""),
            claim=str(record.get("claim") or ""),
            stance=str(record.get("stance") or ""),
            confidence=str(record.get("confidence") or ""),
            paper_id=str(paper.get("arxiv_id") or record.get("paper_id") or ""),
            paper_title=str(paper.get("title") or record.get("title") or ""),
            run_name=run_name,
            raw=record,
        )


@dataclass(frozen=True)
class Deliverable:
    """A prose face of a run — the base triplet or an additive revision."""

    style: str
    label: str
    path: Path
    revision: int | None = None
    based_on: str | None = None


@dataclass(frozen=True)
class RunManifest:
    """``run.json`` with the fields downstream consumers care about."""

    run_name: str
    topic: str
    status: str
    review_mode: str
    time_range: str
    knowledge_ids: tuple[str, ...]
    event_count: int
    candidate_count: int | None
    full_text_count: int | None
    evidence_papers: int | None
    style: str | None
    notes: str
    raw: dict[str, Any] = field(repr=False)

    @classmethod
    def from_json(cls, payload: Any, *, run_name: str) -> "RunManifest | None":
        if not isinstance(payload, dict):
            return None
        ids = payload.get("knowledge_ids")
        return cls(
            run_name=str(payload.get("run") or run_name),
            topic=str(payload.get("topic") or run_name),
            status=str(payload.get("status") or ""),
            review_mode=str(payload.get("review_mode") or ""),
            time_range=str(payload.get("time_range") or ""),
            knowledge_ids=tuple(str(x) for x in ids) if isinstance(ids, list) else (),
            event_count=payload.get("event_count") if isinstance(payload.get("event_count"), int) else 0,
            candidate_count=_int_or_none(payload.get("candidate_count")),
            full_text_count=_int_or_none(payload.get("full_text_count")),
            evidence_papers=_int_or_none(payload.get("evidence_papers")),
            style=str(payload["style"]) if payload.get("style") else None,
            notes=str(payload.get("notes") or ""),
            raw=payload,
        )


@dataclass(frozen=True)
class PoolPaper:
    """One paper folder under ``pool/``."""

    dir_name: str
    arxiv_id: str
    doi: str
    title: str
    quality: str | None
    extraction_method: str
    added_at: str
    has_full_text: bool
    has_deep_read: bool
    in_index: bool
    path: Path
    meta: dict[str, Any] = field(repr=False, default_factory=dict)


@dataclass(frozen=True)
class TopicCard:
    """A routing card under ``knowledge/{embodied-ai,error-governance}/``."""

    path: Path
    card_id: str
    title: str
    tags: tuple[str, ...]
    load_when: str
    source: str


@dataclass(frozen=True)
class TopicVersion:
    """One style/revision of a published topic."""

    style: str
    label: str
    article_title: str
    source_file: str
    characters: int
    revision: int | None = None
    based_on: str | None = None


@dataclass(frozen=True)
class WikiTopic:
    """One published topic — the wiki's display unit."""

    id: str
    topic_key: str
    title: str
    field: str
    date: str
    excerpt: str
    default_version: str
    versions: dict[str, TopicVersion]
    source_directory: str | None = None
    slide_deck: dict[str, Any] | None = None
    evidence: dict[str, Any] | None = None

    @classmethod
    def from_snapshot(cls, payload: Any) -> "WikiTopic | None":
        if not isinstance(payload, dict):
            return None
        raw_versions = payload.get("versions")
        versions: dict[str, TopicVersion] = {}
        if isinstance(raw_versions, dict):
            for key, value in raw_versions.items():
                if not isinstance(value, dict):
                    continue
                versions[str(key)] = TopicVersion(
                    style=str(key),
                    label=str(value.get("label") or ""),
                    article_title=str(value.get("article_title") or ""),
                    source_file=str(value.get("source_file") or ""),
                    characters=int(value.get("characters") or 0),
                    revision=_int_or_none(value.get("revision")),
                    based_on=str(value["based_on"]) if value.get("based_on") else None,
                )
        return cls(
            id=str(payload.get("id") or ""),
            topic_key=str(payload.get("topic_key") or ""),
            title=str(payload.get("title") or ""),
            field=str(payload.get("field") or ""),
            date=str(payload.get("date") or ""),
            excerpt=str(payload.get("excerpt") or ""),
            default_version=str(payload.get("default_version") or ""),
            versions=versions,
            source_directory=str(payload["source_directory"]) if payload.get("source_directory") else None,
            slide_deck=payload.get("slide_deck") if isinstance(payload.get("slide_deck"), dict) else None,
            evidence=payload.get("evidence") if isinstance(payload.get("evidence"), dict) else None,
        )


@dataclass(frozen=True)
class CatalogEntry:
    """One 成果索引 row in ``knowledge/literature-review-catalog.md``."""

    row: str
    run_link: str
    run_name: str
    topic: str
    knowledge_ids: str
    scale: str


# ---- aggregates --------------------------------------------------------------


class ReviewRun:
    """One ``evidence/<run>/`` folder — the unit a review settles into."""

    def __init__(self, path: Path, manifest: RunManifest) -> None:
        self.path = path
        self.manifest = manifest

    @classmethod
    def open(cls, run_json: Path) -> "ReviewRun | None":
        payload = _read_json(run_json)
        manifest = RunManifest.from_json(payload, run_name=run_json.parent.name)
        return cls(run_json.parent, manifest) if manifest else None

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def topic(self) -> str:
        return self.manifest.topic

    @property
    def status(self) -> str:
        return self.manifest.status

    @property
    def review_mode(self) -> str:
        return self.manifest.review_mode

    @property
    def run_json(self) -> Path:
        return self.path / "run.json"

    def events(self) -> list[EvidenceEvent]:
        out: list[EvidenceEvent] = []
        for line in _read_text(self.path / "evidence.jsonl").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                out.append(EvidenceEvent.from_record(record, run_name=self.name))
        return out

    def deliverables(self) -> list[Deliverable]:
        """Base prose faces (config.STYLE_TO_FILE) plus ``revisions/<style>-v<N>.md``."""
        out: list[Deliverable] = []
        for style, filename in STYLE_TO_FILE.items():
            path = self.path / filename
            if path.is_file():
                label = VERSION_FILES.get(style, (style, filename))[0]
                out.append(Deliverable(style=style, label=label, path=path))
        revisions = self.path / "revisions"
        if revisions.is_dir():
            for path in sorted(revisions.glob("*.md")):
                match = REVISION_FILE_RE.match(path.stem)
                if not match:
                    continue
                base, number = match.group(1), int(match.group(2))
                base_label = VERSION_FILES.get(base, (base, base))[0]
                out.append(
                    Deliverable(
                        style=path.stem,
                        label=f"{base_label} · 修订v{number}",
                        path=path,
                        revision=number,
                        based_on=base,
                    )
                )
        return out

    def reading_summary(self) -> dict[str, Any] | None:
        payload = _read_json(self.path / "reading-summary.json")
        return payload if isinstance(payload, dict) else None

    def reading_ledger(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for line in _read_text(self.path / "reading-ledger.jsonl").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                out.append(record)
        return out

    def is_registered(self, catalog: "Catalog") -> bool:
        return self.name in catalog.run_names()


class Catalog:
    """``knowledge/literature-review-catalog.md`` — the routing table to runs."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def entries(self) -> list[CatalogEntry]:
        out: list[CatalogEntry] = []
        for line in _read_text(self.path).splitlines():
            if not line.startswith("|"):
                continue
            match = CATALOG_RUN_LINK.search(line)
            if not match:
                continue
            run_name = match.group(1)
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            out.append(
                CatalogEntry(
                    row=line,
                    run_link=match.group(0),
                    run_name=run_name,
                    topic=cells[1] if len(cells) > 1 else run_name,
                    knowledge_ids=cells[2] if len(cells) > 2 else "",
                    scale=cells[3] if len(cells) > 3 else "",
                )
            )
        return out

    def run_names(self) -> set[str]:
        return {entry.run_name for entry in self.entries()}


class KnowledgeBase:
    """A kb-root — the aggregate root for runs, papers, cards, and wiki topics."""

    def __init__(self, root: Path) -> None:
        self.root = root

    @classmethod
    def open(cls, root: str | Path) -> "KnowledgeBase":
        return cls(Path(root).expanduser())

    # ---- layout ----

    @property
    def evidence_dir(self) -> Path:
        return self.root / "evidence"

    @property
    def pool_dir(self) -> Path:
        return self.root / "pool"

    @property
    def knowledge_dir(self) -> Path:
        return self.root / "knowledge"

    @property
    def wiki_data_dir(self) -> Path:
        return self.root / "wiki" / "data"

    @property
    def site_config(self) -> Path:
        return self.root / "wiki" / "site-config.json"

    # ---- collections ----

    def runs(self) -> list[ReviewRun]:
        """Every ``evidence/*/run.json``, catalog-free (unregistered runs included)."""
        out: list[ReviewRun] = []
        for run_json in sorted(self.evidence_dir.glob("*/run.json")):
            run = ReviewRun.open(run_json)
            if run is not None:
                out.append(run)
        return out

    def papers(self) -> list[PoolPaper]:
        """Every ``pool/<dir>/`` — hidden entries (``.locks``) skipped."""
        index = read_index(self.pool_dir) if (self.pool_dir / "index.jsonl").is_file() else {}
        out: list[PoolPaper] = []
        if not self.pool_dir.is_dir():
            return out
        for entry in sorted(self.pool_dir.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            meta = _read_json(entry / "meta.json")
            meta = meta if isinstance(meta, dict) else {}
            arxiv_id = str(meta.get("arxiv_id") or "")
            if not arxiv_id and entry.name.startswith("arxiv-"):
                arxiv_id = entry.name.removeprefix("arxiv-")
            out.append(
                PoolPaper(
                    dir_name=entry.name,
                    arxiv_id=arxiv_id,
                    doi=str(meta.get("doi") or ""),
                    title=str(meta.get("title") or ""),
                    quality=str(meta["quality"]) if meta.get("quality") else None,
                    extraction_method=str(meta.get("extraction_method") or ""),
                    added_at=str(meta.get("added_at") or ""),
                    has_full_text=(entry / "paper.md").is_file(),
                    has_deep_read=(entry / "note.json").is_file(),
                    in_index=entry.name in index,
                    path=entry,
                    meta=meta,
                )
            )
        return out

    def cards(self) -> list[TopicCard]:
        out: list[TopicCard] = []
        for sub in CARD_DIRS:
            folder = self.knowledge_dir / sub
            if not folder.is_dir():
                continue
            for path in sorted(folder.glob("*.md")):
                out.append(self._read_card(path))
        return out

    @staticmethod
    def _read_card(path: Path) -> TopicCard:
        text = _read_text(path)
        meta: dict[str, str] = {}
        if text.startswith("---"):
            for line in text.splitlines()[1:]:
                if line.strip() == "---":
                    break
                if ":" in line and not line.startswith((" ", "\t", "-")):
                    key, _, value = line.partition(":")
                    meta[key.strip()] = value.strip()
        tags_raw = meta.get("tags", "")
        tags = tuple(t.strip() for t in tags_raw.strip("[]").split(",") if t.strip())
        return TopicCard(
            path=path,
            card_id=meta.get("id") or path.stem,
            title=meta.get("title") or path.stem,
            tags=tags,
            load_when=meta.get("load_when") or "",
            source=meta.get("source") or "",
        )

    def catalog(self) -> Catalog:
        return Catalog(self.knowledge_dir / "literature-review-catalog.md")

    def wiki_topics(self) -> list[WikiTopic]:
        """Published topics from the current wiki snapshot (display cache)."""
        current = _read_json(self.wiki_data_dir / "current.json")
        if not isinstance(current, dict) or not current.get("base_path"):
            return []
        # current.json's base_path is wiki/data-relative ("snapshots/<id>")
        topics_dir = self.wiki_data_dir / str(current["base_path"]) / "topics"
        if not topics_dir.is_dir():
            return []
        out: list[WikiTopic] = []
        for path in sorted(topics_dir.glob("*.json")):
            topic = WikiTopic.from_snapshot(_read_json(path))
            if topic is not None:
                out.append(topic)
        return out

    def snapshot_manifest(self) -> dict[str, Any] | None:
        current = _read_json(self.wiki_data_dir / "current.json")
        if not isinstance(current, dict) or not current.get("base_path"):
            return None
        payload = _read_json(self.wiki_data_dir / str(current["base_path"]) / "manifest.json")
        return payload if isinstance(payload, dict) else None

    def iter_events(self) -> Iterator[EvidenceEvent]:
        """Stream every evidence record across runs (bounded memory)."""
        for run_json in sorted(self.evidence_dir.glob("*/evidence.jsonl")):
            run_name = run_json.parent.name
            for line in _read_text(run_json).splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(record, dict):
                    yield EvidenceEvent.from_record(record, run_name=run_name)

    # ---- downstream consumption (delegates to knowledge.{inventory,query,merge}) ----

    def stats(self, *, include_runs: bool = False) -> dict[str, Any]:
        from embodied_learning.knowledge.inventory import kb_stats

        return kb_stats(self, include_runs=include_runs)

    def search(self, query: str, *, scope: str = "all", limit: int = 20) -> list[dict[str, Any]]:
        from embodied_learning.knowledge.query import kb_search

        return kb_search(self, query, scope=scope, limit=limit)

    def funnel(
        self,
        *,
        layer: str | None = None,
        run: str | None = None,
        topic: str | None = None,
        review_mode: str | None = None,
        sort: str = "run",
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        from embodied_learning.knowledge.funnel import kb_funnel

        return kb_funnel(
            self,
            layer=layer,
            run=run,
            topic=topic,
            review_mode=review_mode,
            sort=sort,
            limit=limit,
        )

    def merge_from(
        self,
        source: "KnowledgeBase | str | Path",
        *,
        what: frozenset[str] | None = None,
        prefer: str = "newer",
        dry_run: bool = False,
    ) -> dict[str, Any]:
        from embodied_learning.knowledge.merge import WHAT, kb_merge

        src = source if isinstance(source, KnowledgeBase) else KnowledgeBase.open(source)
        return kb_merge(
            self,
            [src],
            what=what if what is not None else frozenset(WHAT),
            prefer=prefer,
            dry_run=dry_run,
        )

#!/usr/bin/env python3
"""Build the Mind-Omni guided reader from its settled evidence bundle."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
import sys
from pathlib import Path
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.markdown_semantics import render_markdown  # noqa: E402


DEFAULT_RUN_NAME = "literature-review-智驾模型-vla-驾驶基础模型与关键团队-理想增补-20260927"
DEFAULT_RUN = REPO_ROOT / "evidence" / DEFAULT_RUN_NAME
DEFAULT_SOURCE = REPO_ROOT / "wiki" / "guides" / "mind-omni"
DEFAULT_OUTPUT = REPO_ROOT / "_site" / "research" / "autonomous-driving-vla-models-teams" / "mind-omni"
DEFAULT_CANONICAL_URL = (
    "https://yuanzh0u.github.io/embodied-learning/"
    "research/autonomous-driving-vla-models-teams/mind-omni/"
)
SITE_METADATA_MARKER = "<!-- SITE_METADATA -->"


def _load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON source must be an object: {path}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _verify_source_assets(source: Path, overview: dict[str, object]) -> None:
    provenance = _load_object(source / "figure-sources.json")
    figures = provenance.get("figures")
    if not isinstance(figures, list):
        raise RuntimeError("figure-sources.json must contain a figures list")
    expected = {
        str(item["asset"]): str(item["sha256"])
        for item in figures
        if isinstance(item, dict) and "asset" in item and "sha256" in item
    }
    overview_figures = overview.get("figures")
    if not isinstance(overview_figures, list):
        raise RuntimeError("overview.json must contain a figures list")
    for figure in overview_figures:
        if not isinstance(figure, dict):
            raise RuntimeError("overview.json contains an invalid figure")
        asset = str(figure.get("asset") or "")
        source_asset = source / asset
        if asset not in expected or not source_asset.is_file():
            raise RuntimeError(f"figure asset lacks provenance: {asset}")
        actual = _sha256(source_asset)
        if actual != expected[asset]:
            raise RuntimeError(f"figure checksum mismatch: {asset}")
        figure["sha256"] = actual

    map_source = _load_object(source / "mind-omni-source.json")
    map_asset = str(map_source.get("asset") or "")
    map_path = source / map_asset
    if not map_path.is_file() or _sha256(map_path) != map_source.get("sha256"):
        raise RuntimeError(f"Mind-Omni overview checksum mismatch: {map_asset}")


def build_reader(
    run: Path,
    source: Path,
    output: Path,
    *,
    canonical_url: str = DEFAULT_CANONICAL_URL,
    preview: bool = False,
) -> dict[str, object]:
    """Build one self-contained reader without changing the evidence source."""

    run = run.resolve()
    source = source.resolve()
    output = output.resolve()
    manifest = _load_object(run / "run.json")
    if manifest.get("status") != "settled":
        raise RuntimeError("Mind-Omni reader requires a settled source run")
    if run.name != DEFAULT_RUN_NAME:
        raise RuntimeError(f"unexpected Mind-Omni source run: {run.name}")
    parsed = urlsplit(canonical_url)
    if parsed.scheme != "https" or not parsed.netloc or not canonical_url.endswith("/"):
        raise RuntimeError("Mind-Omni canonical URL must be an absolute HTTPS directory URL")

    overview = _load_object(source / "overview.json")
    _verify_source_assets(source, overview)
    data = dict(overview)
    data["source_run"] = run.name
    data["system"] = _load_object(source / "mind-omni.json")

    notes = {
        path.stem: _load_object(path)
        for path in sorted((run / "paper-notes").glob("*.json"))
    }
    data["papers"] = {}
    papers = data["papers"]
    assert isinstance(papers, dict)
    shorts = overview.get("shorts")
    if not isinstance(shorts, dict):
        raise RuntimeError("overview.json must contain paper shorts")
    for paper_id, note in notes.items():
        paper = note["paper"]
        review_display = note["review_display"]
        papers[paper_id] = {
            "id": paper_id,
            "name": review_display["name"],
            "short": shorts.get(paper_id, note["research_question"]),
            "published": paper["published"],
            "version": paper["versioned_id"],
            "url": f"https://arxiv.org/abs/{paper['versioned_id']}",
            "method": note["method"]["summary"],
            "evaluation": note["evaluation"]["design"],
            "boundary": note["transfer_boundary"],
        }

    groups = data.get("groups")
    if not isinstance(groups, list):
        raise RuntimeError("overview.json must contain paper groups")
    used = [str(paper_id) for group in groups for paper_id in group["ids"]]
    if len(used) != len(set(used)) or set(used) != set(notes):
        raise RuntimeError("Mind-Omni paper-group coverage drift")

    source_records: dict[str, dict[str, object]] = {}
    for filename in ("publication-identities.json", "supplement-sources.json"):
        records = _load_object(run / filename).get("sources")
        if not isinstance(records, list):
            raise RuntimeError(f"{filename} must contain a sources list")
        for record in records:
            if isinstance(record, dict):
                source_records[str(record["source_id"])] = record

    liauto_paper_ids = {
        "2402.12289",
        "2605.12624",
        "2605.12622",
        "2605.12625",
        "2603.01441",
        "2509.20109",
        "2507.00603",
        "2411.11252",
        "2605.26113",
        "2607.01586",
        "2609.24526",
    }
    data["people"] = []
    people = _load_object(run / "organization-people.json").get("people")
    if not isinstance(people, list):
        raise RuntimeError("organization-people.json must contain a people list")
    for person in people:
        refs = [
            {
                "url": source_records[str(source_id)]["url"],
                "label": source_records[str(source_id)].get("title", "作者/贡献表"),
            }
            for source_id in person["sources"]
        ]
        data["people"].append(
            {
                "name": person["name"],
                "direction": person["team_or_direction"],
                "works": "、".join(
                    str(papers.get(paper_id, {}).get("name", paper_id))
                    for paper_id in person["paper_or_system_ids"]
                ),
                "affiliation": person["publication_affiliation"],
                "role": person["explicit_role"],
                "current": person["current_public_role"],
                "checked": person["checked_at"],
                "sources": refs,
                "liauto": bool(liauto_paper_ids & set(person["paper_or_system_ids"])),
            }
        )

    if output.exists():
        shutil.rmtree(output)
    (output / "assets").mkdir(parents=True)
    (output / "reports").mkdir()
    for asset in sorted((source / "assets").iterdir()):
        if asset.is_file():
            shutil.copy2(asset, output / "assets" / asset.name)

    report_specs = {
        "mind-omni-guide.md": {
            "label": "Mind-Omni 体系分析",
            "description": "以官方总图为骨干：六个模块、U1 的定位与图外延伸。",
        },
        **overview["reportSpecs"],
    }
    data["reports"] = {}
    data["reportOrder"] = list(report_specs)

    def link(label: str, target: str) -> str:
        safe_target = html.escape(target, quote=True)
        if target in report_specs:
            return f'<a href="#reports" data-report="{safe_target}">{label}</a>'
        if target.startswith(("https://", "http://")):
            return f'<a href="{safe_target}" target="_blank" rel="noopener">{label}</a>'
        relative = target.split("#", 1)[0]
        path = (run / relative).resolve()
        if path.is_file() and _inside(path, run):
            destination = output / "reports" / path.relative_to(run)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            return f'<a href="reports/{safe_target}" target="_blank" rel="noopener">{label}</a>'
        return label

    for filename, spec in report_specs.items():
        markdown_path = source / filename if filename == "mind-omni-guide.md" else run / filename
        markdown = markdown_path.read_text(encoding="utf-8")
        rendered = render_markdown(
            markdown,
            link_renderer=link,
            table_wrapper_class="table-scroll",
        ).html
        data["reports"][filename] = {**spec, "html": rendered}
        (output / "reports" / filename).write_text(markdown, encoding="utf-8")

    data.pop("shorts", None)
    data.pop("reportSpecs", None)
    for figure in data["figures"]:
        paper_id = str(figure["id"])
        if figure["version"] != notes[paper_id]["paper"]["versioned_id"]:
            raise RuntimeError(f"figure version drift: {paper_id}")

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (output / "assets" / "research-data.js").write_text(
        f"window.RESEARCH_DATA = {payload};\n", encoding="utf-8"
    )
    shutil.copy2(source / "reader.css", output / "assets" / "reader.css")
    shutil.copy2(source / "reader.js", output / "assets" / "reader.js")
    for filename in ("mind-omni-source.json", "figure-sources.json", "presentation-audit.json"):
        shutil.copy2(source / filename, output / filename)

    template = (source / "index.html").read_text(encoding="utf-8")
    if SITE_METADATA_MARKER not in template:
        raise RuntimeError("Mind-Omni template lacks the site metadata marker")
    metadata = (
        f'<link rel="canonical" href="{html.escape(canonical_url, quote=True)}">'
        f'<meta property="og:url" content="{html.escape(canonical_url, quote=True)}">'
        + ('<meta name="robots" content="noindex,nofollow">' if preview else "")
    )
    (output / "index.html").write_text(
        template.replace(SITE_METADATA_MARKER, metadata), encoding="utf-8"
    )
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--canonical-url", default=DEFAULT_CANONICAL_URL)
    parser.add_argument("--preview", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = build_reader(
            args.run,
            args.source,
            args.output,
            canonical_url=args.canonical_url,
            preview=args.preview,
        )
    except (OSError, KeyError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"Mind-Omni build failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"Built Mind-Omni reader: {len(data['papers'])} papers, "
        f"{len(data['people'])} people, {len(data['figures'])} paper figures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Render knowledge/index.md as a browsable doc-site: a directory tree on the
left (mirroring the routing structure) and a rendered-Markdown pane on the
right. Walks markdown links plus frontmatter `source.file` references
starting from knowledge/index.md, expanding only inside knowledge/ so
evidence/ runs and archived docs show up as leaf entries instead of blowing
up the tree. Everything is static HTML/CSS/vanilla JS -- no network access
and no third-party JS is required to view it.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import webbrowser
from collections import deque
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.markdown_semantics import (  # noqa: E402
    render_markdown,
    strip_frontmatter,
)

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
FRONTMATTER_BOUNDS = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

TYPE_COLORS = {
    "index": "#2563eb",
    "domain-index": "#0891b2",
    "topic-card": "#16a34a",
    "source-index": "#d97706",
    "workflow": "#7c3aed",
    "evidence-jsonl": "#059669",
    "evidence-json": "#0d9488",
    "doc": "#6b7280",
}
DEFAULT_COLOR = "#6b7280"
BODY_PREVIEW_LIMIT = 20000
MAX_JSONL_RECORDS = 200
LEGEND_LABELS = {
    "index": "index",
    "domain-index": "domain-index",
    "topic-card": "topic-card",
    "source-index": "source-index",
    "workflow": "workflow",
    "evidence-jsonl": "evidence .jsonl",
    "evidence-json": "run.json / manifest",
    "doc": "其它文档",
}


def parse_frontmatter(text: str) -> dict[str, object]:
    """Minimal YAML-subset frontmatter parser: scalar keys plus a `source:` list."""
    match = FRONTMATTER_BOUNDS.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    sources: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_source = False
    for line in match.group(1).splitlines():
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


def extract_links(text: str) -> list[str]:
    links = []
    for target in MD_LINK.findall(text):
        target = target.strip()
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if target.endswith(".md"):
            links.append(target)
    return links


def _is_under(path: Path, ancestor: Path) -> bool:
    try:
        path.resolve().relative_to(ancestor.resolve())
        return True
    except ValueError:
        return False


def build_graph(root: Path, start: Path, max_nodes: int = 400):
    """BFS from `start`; expand any .md file under knowledge/, treat the rest as leaves.

    Returns (nodes, edges, children_map, root_rel, truncated):
      - nodes: rel_path -> {id, title, type, path, body}
      - edges: set of (from_rel, to_rel, kind), kind in {"link", "source"}; every
        discovered reference, including repeats of an already-placed node.
      - children_map: rel_path -> [(child_rel, kind), ...] in first-discovery order.
        This is the spanning tree used for the sidebar (cross-references still
        appear in `edges` but do not create a second tree slot).
      - root_rel: rel_path of `start`.
      - truncated: True if max_nodes was hit before the queue drained.
    """
    knowledge_dir = root / "knowledge"
    start = start.resolve()
    root_rel = start.relative_to(root.resolve()).as_posix()

    nodes: dict[str, dict[str, object]] = {}
    edges: set[tuple[str, str, str]] = set()
    children_map: dict[str, list[tuple[str, str]]] = {}
    discovered = {root_rel}
    queue: deque[Path] = deque([start])
    truncated = False

    while queue:
        path = queue.popleft()
        rel = path.relative_to(root.resolve()).as_posix()
        if rel in nodes:
            continue
        if len(nodes) >= max_nodes:
            truncated = True
            break

        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        is_markdown = path.suffix == ".md"
        front = parse_frontmatter(text) if (text and is_markdown) else {}
        if is_markdown:
            node_id = str(front.get("id") or path.stem)
            node_title = str(front.get("title") or path.stem)
            node_type = str(front.get("type") or "doc")
        else:
            node_id = path.name
            node_title = f"{path.parent.name}/{path.name}"
            node_type = {".jsonl": "evidence-jsonl", ".json": "evidence-json"}.get(path.suffix, "doc")
        nodes[rel] = {
            "id": node_id,
            "title": node_title,
            "type": node_type,
            "path": rel,
            "body": strip_frontmatter(text) if is_markdown else text,
        }

        can_expand = path.is_file() and path.suffix == ".md" and _is_under(path, knowledge_dir)
        if not can_expand:
            continue

        targets: list[tuple[str, str]] = [(t, "link") for t in extract_links(text)]
        for src in front.get("source", []) or []:
            file_field = src.get("file", "")
            if file_field and not file_field.startswith(("http://", "https://")):
                targets.append((file_field, "source"))

        for target, kind in targets:
            target_path = (path.parent / target).resolve()
            if not target_path.is_file():
                continue
            trel = target_path.relative_to(root.resolve()).as_posix()
            edges.add((rel, trel, kind))
            if trel not in discovered:
                discovered.add(trel)
                children_map.setdefault(rel, []).append((trel, kind))
                queue.append(target_path)

    return nodes, edges, children_map, root_rel, truncated


def make_link_resolver(root: Path, source_dir: Path, ids: dict[str, str]):
    """Build a resolver that turns a raw markdown link target into render info.

    Internal targets (files that ended up as nodes) become in-app navigation;
    other real files get a corrected absolute file:// href; anything that
    does not resolve to a real file on disk is flagged broken instead of
    silently producing a dead relative link against the *generated* HTML's
    own location.
    """
    root = root.resolve()

    def resolve(target: str) -> dict[str, object]:
        if target.startswith(("http://", "https://", "mailto:")) or target.startswith("#"):
            return {"href": target, "internal_id": None, "broken": False}
        clean = target.split("#", 1)[0]
        if not clean:
            return {"href": target, "internal_id": None, "broken": False}
        try:
            resolved = (source_dir / clean).resolve()
        except OSError:
            return {"href": target, "internal_id": None, "broken": True}
        if not resolved.is_file():
            return {"href": target, "internal_id": None, "broken": True}
        try:
            rel = resolved.relative_to(root).as_posix()
        except ValueError:
            rel = None
        node_id = ids.get(rel) if rel else None
        return {"href": resolved.as_uri(), "internal_id": node_id, "broken": False}

    return resolve


def markdown_to_html(body: str, resolve=None) -> str:
    if resolve is None:
        resolve = lambda target: {  # noqa: E731
            "href": target,
            "internal_id": None,
            "broken": not target.startswith(("http://", "https://", "mailto:", "#")),
        }

    def render_link(label: str, target: str) -> str:
        info = resolve(target)
        safe_label = html.escape(label)
        if info["internal_id"]:
            return (
                '<a href="#" class="internal-link" '
                f'data-goto="{html.escape(str(info["internal_id"]), quote=True)}">'
                f"{safe_label}</a>"
            )
        if info["broken"]:
            title = html.escape("文件未找到: " + target, quote=True)
            return f'<span class="broken-link" title="{title}">{safe_label}</span>'
        href = html.escape(str(info["href"]), quote=True)
        return f'<a href="{href}" target="_blank" rel="noopener">{safe_label}</a>'

    return render_markdown(body, link_renderer=render_link).html


def render_markdown_preview(body: str, resolve) -> str:
    truncated = len(body) > BODY_PREVIEW_LIMIT
    snippet = body[:BODY_PREVIEW_LIMIT]
    rendered = markdown_to_html(snippet, resolve)
    if truncated:
        rendered += '<p class="truncated-note">内容较长，已截断预览 — 点击上方"打开原始文件"查看完整内容。</p>'
    return rendered or "<p><em>(空文件)</em></p>"


# ---------------------------------------------------------------------------
# JSON / JSONL preview (evidence.jsonl event streams, run.json manifests).
# ---------------------------------------------------------------------------


def json_value_to_html(value: object) -> str:
    if isinstance(value, dict):
        if not value:
            return "<em>{}</em>"
        rows = "".join(
            f"<tr><th>{html.escape(str(k))}</th><td>{json_value_to_html(v)}</td></tr>" for k, v in value.items()
        )
        return f'<table class="json-table">{rows}</table>'
    if isinstance(value, list):
        if not value:
            return "<em>[]</em>"
        items = "".join(f"<li>{json_value_to_html(v)}</li>" for v in value)
        return f'<ul class="json-list">{items}</ul>'
    if value is None:
        return "<em>null</em>"
    if isinstance(value, bool):
        return f"<code>{str(value).lower()}</code>"
    if isinstance(value, (int, float)):
        return f"<code>{html.escape(str(value))}</code>"
    return html.escape(str(value))


def render_json_preview(body: str) -> str:
    try:
        data = json.loads(body) if body.strip() else {}
    except json.JSONDecodeError as exc:
        snippet = html.escape(body[:BODY_PREVIEW_LIMIT])
        return f'<p class="truncated-note">JSON 解析失败：{html.escape(str(exc))}</p><pre>{snippet}</pre>'
    return json_value_to_html(data)


def render_jsonl_preview(body: str) -> str:
    lines = [ln for ln in body.splitlines() if ln.strip()]
    total = len(lines)
    records: list[object] = []
    errors = 0
    for ln in lines[:MAX_JSONL_RECORDS]:
        try:
            records.append(json.loads(ln))
        except json.JSONDecodeError:
            errors += 1
    summary = f"共 {total} 条记录"
    if total > MAX_JSONL_RECORDS:
        summary += f"，仅预览前 {MAX_JSONL_RECORDS} 条"
    if errors:
        summary += f"，{errors} 条解析失败"
    parts = [f'<p class="jsonl-summary">{html.escape(summary)}</p>']
    for idx, record in enumerate(records):
        label = None
        if isinstance(record, dict):
            label = record.get("event_id") or record.get("id")
        label = html.escape(str(label or f"记录 {idx + 1}"))
        parts.append(f'<details class="json-record"><summary>{label}</summary>{json_value_to_html(record)}</details>')
    return "".join(parts) if records else '<p><em>(无记录)</em></p>'


def render_plain_preview(body: str) -> str:
    truncated = len(body) > BODY_PREVIEW_LIMIT
    out = f"<pre>{html.escape(body[:BODY_PREVIEW_LIMIT])}</pre>"
    if truncated:
        out += '<p class="truncated-note">内容较长，已截断预览。</p>'
    return out


def render_preview_for(rel: str, body: str, resolve) -> str:
    suffix = Path(rel).suffix
    if suffix == ".md":
        return render_markdown_preview(body, resolve)
    if suffix == ".jsonl":
        return render_jsonl_preview(body)
    if suffix == ".json":
        return render_json_preview(body)
    return render_plain_preview(body)


def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_tree(nodes: dict, children_map: dict, rel: str, ids: dict, kind: str | None = None, depth: int = 0) -> str:
    info = nodes[rel]
    node_id = ids[rel]
    color = TYPE_COLORS.get(info["type"], DEFAULT_COLOR)
    badge = '<span class="kind-badge">source</span>' if kind == "source" else ""
    search_key = html.escape(f"{info['id']} {info['title']} {rel}".lower())
    row = (
        f'<div class="tree-row" data-id="{node_id}" data-search="{search_key}">'
        f'<span class="dot" style="background:{color}"></span>'
        f'<span class="tree-label">{html.escape(_truncate(str(info["id"]), 26))}</span>'
        f'<span class="tree-sub">{html.escape(_truncate(str(info["title"]), 22))}</span>'
        f"{badge}"
        f"</div>"
    )
    children = children_map.get(rel, [])
    if not children:
        return f"<li>{row}</li>"
    inner = "".join(render_tree(nodes, children_map, c, ids, k, depth + 1) for c, k in children)
    open_attr = " open data-default-open" if depth < 2 else ""
    return f"<li><details{open_attr}><summary>{row}</summary><ul>{inner}</ul></details></li>"


def render_html(root: Path, nodes: dict, edges: set, children_map: dict, root_rel: str, truncated: bool) -> str:
    root = root.resolve()
    ids = {rel: f"n{i}" for i, rel in enumerate(sorted(nodes))}

    parent_of = {c: p for p, kids in children_map.items() for c, _k in kids}
    backlinks: dict[str, list[str]] = {}
    for a, b, _kind in edges:
        if a in ids and b in ids and a != parent_of.get(b):
            backlinks.setdefault(ids[b], []).append(ids[a])

    node_info = {
        ids[rel]: {
            "id": info["id"],
            "title": info["title"],
            "type": info["type"],
            "path": info["path"],
            "file_uri": (root / rel).resolve().as_uri(),
        }
        for rel, info in nodes.items()
    }
    content_map = {
        ids[rel]: render_preview_for(rel, str(info["body"]), make_link_resolver(root, (root / rel).parent, ids))
        for rel, info in nodes.items()
    }

    tree_html = f'<ul class="tree-root">{render_tree(nodes, children_map, root_rel, ids)}</ul>'
    legend_items = "".join(
        f'<div class="legend-item"><span class="dot" style="background:{color}"></span>{html.escape(LEGEND_LABELS.get(t, t))}</div>'
        for t, color in TYPE_COLORS.items()
    )
    warning = (
        '<div class="warning">节点数达到上限，部分文件未展开（可用 --max-nodes 提高上限）。</div>'
        if truncated
        else ""
    )

    def _json_for_script(data: object) -> str:
        return json.dumps(data, ensure_ascii=False).replace("</script>", "<\\/script>")

    node_info_json = _json_for_script(node_info)
    content_json = _json_for_script(content_map)
    backlinks_json = _json_for_script({k: sorted(set(v)) for k, v in backlinks.items()})
    root_id = ids[root_rel]

    return f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<title>知识库路由浏览器 — knowledge/index.md</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; color: #0f172a; }}
  #app {{ display: flex; height: 100vh; }}
  #sidebar {{ width: 340px; flex: 0 0 340px; border-right: 1px solid #e2e8f0; background: #f8fafc; display: flex; flex-direction: column; }}
  #sidebar header {{ padding: 12px 14px; border-bottom: 1px solid #e2e8f0; background: white; }}
  #sidebar header h1 {{ font-size: 14px; margin: 0 0 8px; }}
  #search {{ width: 100%; padding: 6px 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 13px; }}
  .legend {{ display: flex; flex-wrap: wrap; gap: 8px; font-size: 11px; color: #64748b; margin-top: 8px; }}
  .legend-item {{ display: flex; align-items: center; gap: 4px; }}
  .warning {{ margin: 8px 14px 0; background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 6px; font-size: 12px; }}
  .dot {{ width: 9px; height: 9px; border-radius: 50%; display: inline-block; flex: 0 0 auto; }}
  #tree-wrap {{ overflow-y: auto; flex: 1 1 auto; padding: 6px 4px 20px; }}
  #tree-wrap ul {{ list-style: none; margin: 0; padding-left: 16px; }}
  #tree-wrap ul.tree-root {{ padding-left: 4px; }}
  #tree-wrap li {{ margin: 1px 0; }}
  #tree-wrap summary {{ list-style: none; cursor: pointer; }}
  #tree-wrap summary::-webkit-details-marker {{ display: none; }}
  #tree-wrap summary::before {{ content: '▸'; display: inline-block; width: 14px; color: #94a3b8; font-size: 10px; }}
  #tree-wrap details[open] > summary::before {{ content: '▾'; }}
  .tree-row {{ display: flex; align-items: center; gap: 6px; padding: 4px 6px; border-radius: 6px; cursor: pointer; font-size: 12.5px; }}
  .tree-row:hover {{ background: #e2e8f0; }}
  .tree-row.active {{ background: #dbeafe; }}
  .tree-label {{ font-weight: 600; white-space: nowrap; }}
  .tree-sub {{ color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .kind-badge {{ font-size: 9px; color: #d97706; border: 1px solid #d97706; border-radius: 4px; padding: 0 4px; }}
  #content {{ flex: 1 1 auto; overflow-y: auto; padding: 28px 40px; }}
  #pane-title {{ font-size: 20px; margin: 0 0 4px; }}
  #pane-meta {{ font-size: 12.5px; color: #64748b; margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid #e2e8f0; }}
  #pane-meta a {{ color: #2563eb; }}
  #pane-body {{ max-width: 860px; line-height: 1.65; font-size: 15px; }}
  #pane-body h1, #pane-body h2, #pane-body h3 {{ margin-top: 1.6em; }}
  #pane-body table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13.5px; }}
  #pane-body th, #pane-body td {{ border: 1px solid #e2e8f0; padding: 6px 10px; text-align: left; vertical-align: top; }}
  #pane-body th {{ background: #f1f5f9; }}
  #pane-body code {{ background: #f1f5f9; padding: 1px 5px; border-radius: 4px; font-size: 90%; }}
  #pane-body pre {{ background: #0f172a; color: #e2e8f0; padding: 12px 14px; border-radius: 8px; overflow-x: auto; }}
  #pane-body pre code {{ background: none; padding: 0; color: inherit; }}
  #pane-body blockquote {{ margin: 0; padding: 4px 14px; border-left: 3px solid #cbd5e1; color: #475569; }}
  #pane-body a {{ color: #2563eb; }}
  .truncated-note {{ color: #92400e; font-style: italic; }}
  #pane-body .internal-link {{ color: #2563eb; cursor: pointer; }}
  #pane-body .broken-link {{ color: #b91c1c; text-decoration: line-through dotted; cursor: help; }}
  #pane-body .jsonl-summary {{ color: #64748b; font-size: 13px; margin-bottom: 14px; }}
  #pane-body details.json-record {{ border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 8px; padding: 4px 10px; }}
  #pane-body details.json-record summary {{ cursor: pointer; font-weight: 600; padding: 6px 0; }}
  #pane-body table.json-table {{ border-collapse: collapse; margin: 4px 0; }}
  #pane-body table.json-table th {{ background: #f1f5f9; text-align: left; white-space: nowrap; }}
  #pane-body table.json-table th, #pane-body table.json-table td {{ border: 1px solid #e2e8f0; padding: 4px 8px; vertical-align: top; font-size: 13px; }}
  #pane-body ul.json-list {{ margin: 4px 0; padding-left: 20px; }}
  #backlinks {{ margin-top: 28px; padding-top: 14px; border-top: 1px solid #e2e8f0; font-size: 13px; }}
  #backlinks .chip {{ display: inline-block; margin: 3px 6px 3px 0; padding: 3px 10px; border: 1px solid #cbd5e1; border-radius: 999px; cursor: pointer; font-size: 12px; }}
  #backlinks .chip:hover {{ background: #e2e8f0; }}
</style>
</head>
<body>
<div id="app">
  <div id="sidebar">
    <header>
      <h1>知识库路由 · {len(nodes)} 节点</h1>
      <input id="search" type="text" placeholder="搜索 id / 标题 / 路径…">
      <div class="legend">{legend_items}</div>
    </header>
    {warning}
    <div id="tree-wrap">{tree_html}</div>
  </div>
  <div id="content">
    <h2 id="pane-title"></h2>
    <div id="pane-meta"></div>
    <div id="pane-body"></div>
    <div id="backlinks"></div>
  </div>
</div>
<script>
  var NODE_INFO = {node_info_json};
  var CONTENT = {content_json};
  var BACKLINKS = {backlinks_json};
  var ROOT_ID = "{root_id}";

  function selectNode(id) {{
    var info = NODE_INFO[id];
    if (!info) return;
    document.querySelectorAll('.tree-row.active').forEach(function (r) {{ r.classList.remove('active'); }});
    var row = document.querySelector('.tree-row[data-id="' + id + '"]');
    if (row) row.classList.add('active');
    document.getElementById('pane-title').textContent = info.id + ' · ' + info.title;
    document.getElementById('pane-meta').innerHTML =
      '路径: ' + info.path + ' &nbsp;·&nbsp; 类型: ' + info.type +
      ' &nbsp;·&nbsp; <a href="' + info.file_uri + '" target="_blank" rel="noopener">在编辑器/文件系统打开原始文件</a>';
    document.getElementById('pane-body').innerHTML = CONTENT[id] || '<p><em>无内容</em></p>';
    var back = BACKLINKS[id] || [];
    var backEl = document.getElementById('backlinks');
    if (back.length) {{
      backEl.innerHTML = '被以下文件引用：' + back.map(function (bid) {{
        var b = NODE_INFO[bid];
        return '<span class="chip" data-id="' + bid + '">' + (b ? b.id : bid) + '</span>';
      }}).join('');
      backEl.querySelectorAll('.chip').forEach(function (chip) {{
        chip.addEventListener('click', function () {{ selectNode(chip.getAttribute('data-id')); }});
      }});
    }} else {{
      backEl.innerHTML = '';
    }}
    document.getElementById('content').scrollTop = 0;
  }}

  document.querySelectorAll('.tree-row').forEach(function (row) {{
    row.addEventListener('click', function () {{ selectNode(row.getAttribute('data-id')); }});
  }});

  document.getElementById('pane-body').addEventListener('click', function (e) {{
    var link = e.target.closest('.internal-link');
    if (!link) return;
    e.preventDefault();
    selectNode(link.getAttribute('data-goto'));
  }});

  function markVisible(li, query) {{
    var ownRow = null;
    for (var i = 0; i < li.children.length; i++) {{
      var el = li.children[i];
      if (el.classList && el.classList.contains('tree-row')) {{ ownRow = el; break; }}
      if (el.tagName === 'DETAILS') {{
        var summary = el.querySelector(':scope > summary > .tree-row');
        if (summary) ownRow = summary;
      }}
    }}
    var selfMatch = ownRow && (ownRow.getAttribute('data-search') || '').indexOf(query) !== -1;
    var childLis = li.querySelectorAll(':scope > details > ul > li, :scope > ul.tree-root > li');
    var anyChildVisible = false;
    childLis.forEach(function (childLi) {{
      if (markVisible(childLi, query)) anyChildVisible = true;
    }});
    var visible = selfMatch || anyChildVisible;
    li.style.display = visible ? '' : 'none';
    var details = li.querySelector(':scope > details');
    if (details && anyChildVisible) details.open = true;
    return visible;
  }}

  document.getElementById('search').addEventListener('input', function (e) {{
    var query = e.target.value.trim().toLowerCase();
    var topLis = document.querySelectorAll('#tree-wrap > ul.tree-root > li');
    if (!query) {{
      document.querySelectorAll('#tree-wrap li').forEach(function (li) {{ li.style.display = ''; }});
      document.querySelectorAll('#tree-wrap details').forEach(function (d) {{
        d.open = d.hasAttribute('data-default-open');
      }});
      return;
    }}
    topLis.forEach(function (li) {{ markVisible(li, query); }});
  }});

  selectNode(ROOT_ID);
</script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(REPO_ROOT), help="Repository root.")
    parser.add_argument(
        "--start", default="knowledge/index.md", help="Entry markdown file, relative to --root."
    )
    parser.add_argument(
        "--output",
        default="work/kb-graph/index.html",
        help="Output HTML path, relative to --root unless absolute.",
    )
    parser.add_argument("--max-nodes", type=int, default=400, help="BFS node cap.")
    parser.add_argument("--no-open", action="store_true", help="Write the file but skip opening a browser.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    start = (root / args.start).resolve()
    if not start.is_file():
        print(f"start file not found: {start}", file=sys.stderr)
        return 1

    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)

    nodes, edges, children_map, root_rel, truncated = build_graph(root, start, max_nodes=args.max_nodes)
    doc = render_html(root, nodes, edges, children_map, root_rel, truncated)
    output.write_text(doc, encoding="utf-8")

    print(f"wrote {output} ({len(nodes)} nodes, {len(edges)} edges)")
    if truncated:
        print("warning: max-nodes cap reached, tree is incomplete", file=sys.stderr)
    if not args.no_open:
        webbrowser.open(output.resolve().as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

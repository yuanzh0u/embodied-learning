#!/usr/bin/env python3
"""Compile slide-deck_report.md (slide-source DSL) into a single-file reveal.js deck.

汇报展示风格（slide-deck）的确定性编译器。代理只写受限 DSL 的 slide-source，
永不手写 HTML——base64 内联、div 配平、引文编号都由本脚本结构性保证。

slide-source 格式
-----------------
文档头（第一个 ``---`` 之前）是 ``# key: value`` 元数据行::

    # title: EGO-EXO 数据采集方案
    # subtitle: 测绘级底图模式
    # date: 2026-09-23
    # refs: refs.json          # 引文键 -> {title, url}（键 -> 编号由编译器分配）
    # end: 谢谢 · Q&A          # 可选，生成结尾页

正文用 ``---`` 分页。每页由若干 ``key: value`` 头字段 + 正文块组成::

    ---
    kicker: 空间配准
    title: 底图时效性是第一退化源
    class: cover               # 可选：cover / end，仅特殊页使用
    verdict: 页底金色结论条，支持 **强调** 与 {{citekey}}

    - 列表项，支持 **bold**、`code` 与 {{citekey}}
    1. 有序项自动渲染为步骤条（.steps）

    @stat 0.30→0.71 | EgoScale 千小时→万小时        # 多个 @stat 合成一行数字卡
    @bars EgoScale 千时 0.30 ; EgoScale 万时 0.71 ; *我们 0.85
                                                   # `*` 前缀=ours 高亮，`!`=risk 红条
    @card 标题 | 正文一句话                         # 单卡；@cards A | x ;; B | y 为并排卡组
    @tier 语义级 > 时间窗级 > *帧级+空间配准        # `*` 标热层
    @fix 已核验项一 ; 已核验项二                    # 对勾清单
    @care 风险/注意一句话
    @fig /abs/or/relative/path.png | 图注
    | 列一 | 列二 |                                 # 连续竖线行渲染为表格

校验（违规即非零退出，stdout 打 JSON 摘要）：未知指令、每页 >7 个列表项、
>2 张图、>1 张表、>4 张数字卡、无 title 的内容页、未解析的 {{citekey}}、
图路径不存在。

CLI::

    build_slide_deck.py --source slide-deck_report.md --output slide-deck_report.html \
        [--refs refs.json] [--qa /tmp/deck-qa]

``--qa`` 逐页 headless Chrome 截图（reveal ``#/N`` hash 直达），供视觉 QA。
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from html import escape
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
REVEAL_DIR = ASSETS_DIR / "reveal"
THEME_CSS = ASSETS_DIR / "deck-theme.css"

MAX_BULLETS = 7
MAX_FIGS = 2
MAX_TABLES = 1
MAX_STATS = 4
REFS_PER_PAGE = 27

# Keys may be arXiv IDs (digit-leading, e.g. {{2505.11709}}) or word keys.
_CITE_RE = re.compile(r"\{\{([A-Za-z0-9][A-Za-z0-9_.-]*)\}\}")
_META_RE = re.compile(r"^#\s*([a-z][a-z_-]*):\s*(.*)$")
_HEAD_RE = re.compile(r"^([a-z][a-z_-]*):\s*(.*)$")


class CompileError(Exception):
    """slide-source 违规；message 面向写稿代理，带页码定位。"""


# ---------------------------------------------------------------- parsing

def split_slides(text: str, errors: list[str]) -> tuple[dict[str, str], list[dict]]:
    """Split on bare ``---`` lines. First chunk is doc metadata."""
    chunks = re.split(r"(?m)^---\s*$", text)
    meta: dict[str, str] = {}
    rest = chunks
    # Guard on the first line only: `$` without re.M never crosses newlines.
    first_line = chunks[0].lstrip().split("\n", 1)[0].strip() if chunks else ""
    if _META_RE.match(first_line):
        for line in chunks[0].splitlines():
            m = _META_RE.match(line.strip())
            if m:
                meta[m.group(1)] = m.group(2).strip()
        rest = chunks[1:]
    slides = []
    for idx, chunk in enumerate(rest, 1):
        head: dict[str, str] = {}
        lines = chunk.splitlines()
        i = 0
        while i < len(lines) and not lines[i].strip():  # separator newline after ---
            i += 1
        while i < len(lines):
            m = _HEAD_RE.match(lines[i].strip())
            if not m:
                break
            head[m.group(1)] = m.group(2).strip()
            i += 1
        body = "\n".join(lines[i:]).strip("\n")
        if not head.get("title") and "cover" not in head.get("class", ""):
            errors.append(f"slide {idx}: 缺少 title 头字段")
        slides.append({"idx": idx, "head": head, "body": body})
    return meta, slides


def assign_citation_numbers(slides: list[dict], refs: dict) -> dict[str, int]:
    """Number {{citekey}}s by first appearance across slides (1-based)."""
    keymap: dict[str, int] = {}
    for slide in slides:
        for m in _CITE_RE.finditer(slide["body"] + "\n" + slide["head"].get("verdict", "")):
            key = m.group(1)
            if key not in refs:
                raise CompileError(
                    f"slide {slide['idx']}: 引文键 {{{{{key}}}}} 不在 refs 表中")
            if key not in keymap:
                keymap[key] = len(keymap) + 1
    return keymap


# ---------------------------------------------------------------- rendering

def _inline(text: str, keymap: dict[str, int], idx: int) -> str:
    s = escape(text, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)

    def _code(m: re.Match) -> str:
        return "<code>" + m.group(1) + "</code>"

    s = re.sub(r"`([^`]+)`", _code, s)

    def _cite(m: re.Match) -> str:
        return f'<span class="cite">[{keymap[m.group(1)]}]</span>'

    return _CITE_RE.sub(_cite, s)


def _bars_html(arg: str, idx: int) -> str:
    rows = []
    for item in [p.strip() for p in arg.split(";") if p.strip()]:
        cls = ""
        label = item
        if label.startswith("*"):
            cls, label = "ours", label[1:].strip()
        elif label.startswith("!"):
            cls, label = "risk", label[1:].strip()
        parts = label.rsplit(None, 1)
        if len(parts) != 2:
            raise CompileError(f"slide {idx}: @bars 项缺少数值：{item!r}")
        name, val = parts
        num = re.sub(r"[^0-9.]", "", val)
        try:
            f = float(num)
        except ValueError as exc:
            raise CompileError(f"slide {idx}: @bars 数值无法解析：{val!r}") from exc
        # Numbers <=1 are fractions (x100); larger numbers are already
        # percentages and clamp at 100.
        width = min(100.0, f * 100 if f <= 1 else f)
        rows.append(
            f'<div class="row {cls}"><div class="lbl">{escape(name, quote=False)}</div>'
            f'<div class="track"><div class="fill" style="width:{width:.1f}%"></div></div>'
            f'<div class="bval">{escape(val, quote=False)}</div></div>')
    return '<div class="bars">' + "".join(rows) + "</div>"


def _fig_html(arg: str, src_dir: Path, idx: int) -> str:
    path_str, _, caption = arg.partition("|")
    path = Path(path_str.strip())
    if not path.is_absolute():
        path = src_dir / path
    if not path.is_file():
        raise CompileError(f"slide {idx}: @fig 图片不存在：{path}")
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp"}.get(
                path.suffix.lower())
    if mime is None:
        raise CompileError(f"slide {idx}: @fig 不支持的图片格式：{path.suffix}")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    cap = f'<div class="cap">{escape(caption.strip(), quote=False)}</div>' if caption.strip() else ""
    return (f'<div class="fig"><img src="data:{mime};base64,{data}" alt="figure">'
            f"{cap}</div>")


def _table_html(lines: list[str], keymap: dict, idx: int) -> str:
    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    rows = [cells(l) for l in lines]
    head, body = rows[0], rows[1:]
    if body and all(re.fullmatch(r":?-{3,}:?", c) for c in body[0]):
        body = body[1:]
    html = ["<table><thead><tr>"]
    html += [f"<th>{_inline(c, keymap, idx)}</th>" for c in head]
    html.append("</tr></thead><tbody>")
    for row in body:
        html.append("<tr>" + "".join(
            f"<td>{_inline(c, keymap, idx)}</td>" for c in row) + "</tr>")
    html.append("</tbody></table>")
    return "".join(html)


def render_body(body: str, keymap: dict, idx: int, src_dir: Path,
                errors: list[str]) -> str:
    """Render one slide body: bullets / steps / paragraphs / directives / table."""
    out: list[str] = []
    figs = tables = stats = 0
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            tables += 1
            if tables > MAX_TABLES:
                errors.append(f"slide {idx}: 表格超过每页 {MAX_TABLES} 张")
            out.append(_table_html(tbl, keymap, idx))
            continue
        m = re.match(r"@([a-z]+)\s*(.*)$", stripped)
        if m:
            name, arg = m.group(1), m.group(2).strip()
            if name == "stat":
                v, _, k = arg.partition("|")
                stats += 1
                if stats > MAX_STATS:
                    errors.append(f"slide {idx}: 数字卡超过每页 {MAX_STATS} 张")
                card = (f'<div class="stat"><div class="v">{_inline(v.strip(), keymap, idx)}</div>'
                        f'<div class="k">{_inline(k.strip(), keymap, idx)}</div></div>')
                if out and out[-1].startswith('<div class="statrow">'):
                    out[-1] = out[-1][:-len("</div>")] + card + "</div>"
                else:
                    out.append(f'<div class="statrow">{card}</div>')
            elif name == "bars":
                out.append(_bars_html(arg, idx))
            elif name == "card":
                t, _, c = arg.partition("|")
                out.append(f'<div class="card"><span class="t">{_inline(t.strip(), keymap, idx)}</span>'
                           f"{_inline(c.strip(), keymap, idx)}</div>")
            elif name == "cards":
                cells = []
                for item in [p.strip() for p in arg.split(";;") if p.strip()]:
                    t, _, c = item.partition("|")
                    cells.append(f'<div class="card"><span class="t">{_inline(t.strip(), keymap, idx)}</span>'
                                 f"{_inline(c.strip(), keymap, idx)}</div>")
                out.append('<div class="cardrow">' + "".join(cells) + "</div>")
            elif name == "tier":
                items = []
                for item in [p.strip() for p in arg.split(">") if p.strip()]:
                    hot = item.startswith("*")
                    label = item[1:].strip() if hot else item
                    items.append(f'<div class="t{" hot" if hot else ""}">'
                                 f"{_inline(label, keymap, idx)}</div>")
                out.append('<div class="tier">'
                           + '<div class="arrow">→</div>'.join(items) + "</div>")
            elif name == "fix":
                lis = "".join(f"<li>{_inline(p.strip(), keymap, idx)}</li>"
                              for p in arg.split(";") if p.strip())
                out.append(f'<ul class="fix">{lis}</ul>')
            elif name == "care":
                out.append(f'<div class="care">{_inline(arg, keymap, idx)}</div>')
            elif name == "fig":
                figs += 1
                if figs > MAX_FIGS:
                    errors.append(f"slide {idx}: 图片超过每页 {MAX_FIGS} 张")
                out.append(_fig_html(arg, src_dir, idx))
            else:
                errors.append(f"slide {idx}: 未知指令 @{name}（支持 stat/bars/card/cards/tier/fix/care/fig）")
            i += 1
            continue
        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            if len(items) > MAX_BULLETS:
                errors.append(f"slide {idx}: 列表 {len(items)} 项，超过每页 {MAX_BULLETS} 项上限")
            out.append("<ul>" + "".join(
                f"<li>{_inline(t, keymap, idx)}</li>" for t in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append('<ol class="steps">' + "".join(
                f"<li>{_inline(t, keymap, idx)}</li>" for t in items) + "</ol>")
            continue
        out.append(f"<p>{_inline(stripped, keymap, idx)}</p>")
        i += 1
    return "\n".join(out)


def render_slide(slide: dict, keymap: dict, src_dir: Path,
                 errors: list[str], meta: dict | None = None) -> str:
    head, idx = slide["head"], slide["idx"]
    classes = ["slide"]
    if head.get("class"):
        classes.append(head["class"])
    meta = meta or {}
    if "cover" in classes:
        # Cover pulls its content from the doc metadata when not overridden.
        title = head.get("title") or meta.get("title") or ""
        sub = " · ".join(
            part for part in (meta.get("subtitle", ""), meta.get("date", "")) if part)
        inner = [f'<h1>{_inline(title, keymap, idx)}</h1>',
                 f'<div class="sub">{escape(sub, quote=False)}</div>']
    else:
        inner = [f'<p class="kicker">{escape(head["kicker"], quote=False)}</p>'
                 if head.get("kicker") else ""]
        if head.get("title"):
            inner.append(f"<h2>{_inline(head['title'], keymap, idx)}</h2>")
        inner.append(render_body(slide["body"], keymap, idx, src_dir, errors))
    if head.get("verdict") and "cover" not in classes:
        inner.append(f'<div class="verdict">{_inline(head["verdict"], keymap, idx)}</div>')
    attr = f' id="slide-{idx}"' if head.get("class") not in ("cover", "end") else ""
    return f'<section class="{" ".join(classes)}"{attr}>\n' + "\n".join(
        part for part in inner if part) + "\n</section>"


def render_refs_pages(keymap: dict, refs: dict) -> list[str]:
    entries = sorted(keymap.items(), key=lambda kv: kv[1])
    pages = []
    for start in range(0, len(entries), REFS_PER_PAGE):
        chunk = entries[start:start + REFS_PER_PAGE]
        lis = []
        for key, n in chunk:
            info = refs[key] or {}
            title = escape(str(info.get("title") or key), quote=False)
            url = str(info.get("url") or "").strip()
            tail = f' <a href="{escape(url)}">{escape(url)}</a>' if url else ""
            lis.append(f'<div><span class="n">[{n}]</span> {title}{tail}</div>')
        pages.append(
            '<section class="slide"><p class="kicker">References</p>'
            f"<h2>参考文献 {start + 1}–{start + len(chunk)}</h2>"
            f'<div class="refs">{"".join(lis)}</div></section>')
    return pages


def compile_deck(source: Path, refs_override: Path | None,
                 errors: list[str]) -> tuple[str, dict]:
    text = source.read_text(encoding="utf-8")
    meta, slides = split_slides(text, errors)
    refs_path = refs_override or (source.parent / meta["refs"]) if (
        refs_override or meta.get("refs")) else None
    refs: dict = {}
    if refs_path:
        refs = json.loads(Path(refs_path).read_text(encoding="utf-8"))
    keymap = assign_citation_numbers(slides, refs)

    src_dir = source.parent
    body_slides = [render_slide(s, keymap, src_dir, errors, meta) for s in slides]
    body_slides += render_refs_pages(keymap, refs)
    if meta.get("end"):
        body_slides.append(
            f'<section class="slide end"><h1>{escape(meta["end"], quote=False)}</h1>'
            f'<div class="sub">{escape(meta.get("subtitle", ""), quote=False)}</div></section>')

    reset_css = (REVEAL_DIR / "reset.min.css").read_text(encoding="utf-8")
    reveal_css = (REVEAL_DIR / "reveal.min.css").read_text(encoding="utf-8")
    theme_css = THEME_CSS.read_text(encoding="utf-8")
    reveal_js = (REVEAL_DIR / "reveal.min.js").read_text(encoding="utf-8")
    title = meta.get("title") or source.stem
    head_parts = [f"<title>{escape(title, quote=False)}</title>",
                  f"<style>{reset_css}</style>", f"<style>{reveal_css}</style>",
                  f"<style>{theme_css}</style>"]
    html = (
        "<!doctype html>\n<html lang=\"zh\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        + "\n".join(head_parts) +
        "\n</head>\n<body>\n"
        '<div class="reveal"><div class="slides">\n'
        + "\n".join(body_slides) +
        "\n</div></div>\n"
        "<script>" + reveal_js + "</script>\n"
        "<script>Reveal.initialize({hash:true,width:1280,height:720,margin:0.04,"
        "center:false,progress:true,slideNumber:'c/t',controls:true,keyboard:true,"
        "overview:true,transition:'none'});</script>\n"
        "</body>\n</html>\n")
    summary = {"pages": len(body_slides), "citations": len(keymap),
               "refs_available": len(refs), "title": title}
    return html, summary


# ---------------------------------------------------------------- QA

def qa_screenshots(html_path: Path, out_dir: Path, pages: int) -> list[str]:
    """Per-slide headless Chrome screenshots (reveal #/N hash navigation)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for i in range(pages):
        png = out_dir / f"slide-{i + 1:02d}.png"
        url = f"file://{html_path.resolve()}#/{i}"
        subprocess.run(
            ["google-chrome", "--headless", "--disable-gpu", "--hide-scrollbars",
             "--window-size=1600,900", f"--screenshot={png}", url],
            check=True, capture_output=True, timeout=60)
        written.append(str(png))
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--source", required=True, help="slide-source DSL markdown")
    parser.add_argument("--output", required=True, help="single-file reveal.js HTML")
    parser.add_argument("--refs", help="citation key -> {title,url} JSON (overrides # refs:)")
    parser.add_argument("--qa", help="screenshot every slide into this directory")
    args = parser.parse_args(argv)

    source, output = Path(args.source), Path(args.output)
    errors: list[str] = []
    try:
        html, summary = compile_deck(source, Path(args.refs) if args.refs else None, errors)
    except CompileError as exc:
        print(f"COMPILE ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for err in errors:
            print(f"VALIDATION: {err}", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    summary["output"] = str(output)
    if args.qa:
        summary["screenshots"] = qa_screenshots(output, Path(args.qa), summary["pages"])
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

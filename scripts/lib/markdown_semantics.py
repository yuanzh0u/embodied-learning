"""Shared safe Markdown semantics for Wiki and knowledge-map renderers.

This intentionally implements the repository's supported Markdown subset. It
is not a full CommonMark parser; it centralizes the meaning and escaping rules
while allowing callers to customize link behavior and presentation wrappers.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Callable


LinkRenderer = Callable[[str, str], str]
ImageRenderer = Callable[[str, str], str]

FRONTMATTER_BOUNDS = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
HEADER = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
HR = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})$")
UL_ITEM = re.compile(r"^[-*+]\s+(.+)$")
OL_ITEM = re.compile(r"^\d+[.)]\s+(.+)$")
BLOCKQUOTE = re.compile(r"^>\s?(.*)$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}.*\|")
INLINE_LINK = re.compile(r"(?<!!)\[([^\]]+)]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
INLINE_IMAGE = re.compile(r"!\[([^\]]*)]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
INLINE_CODE = re.compile(r"`([^`]+)`")
INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")
INLINE_STRIKE = re.compile(r"~~(.+?)~~")
INLINE_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


@dataclass(frozen=True)
class MarkdownResult:
    html: str
    toc: list[dict[str, object]]


def strip_frontmatter(markdown: str) -> str:
    match = FRONTMATTER_BOUNDS.match(markdown)
    return markdown[match.end() :] if match else markdown


def first_heading(markdown: str) -> str | None:
    for line in strip_frontmatter(markdown).splitlines():
        match = HEADER.match(line.strip())
        if match:
            return re.sub(r"[*_`]+", "", match.group(2)).strip()
    return None


def markdown_to_plain(markdown: str) -> str:
    text = strip_frontmatter(markdown)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = INLINE_IMAGE.sub(r"\1", text)
    text = INLINE_LINK.sub(r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[>*+-]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+[.)]\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`~|]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _default_link(label: str, target: str) -> str:
    if not target.startswith(("https://", "http://", "mailto:", "#")):
        return (
            f'<span class="local-ref" title="本地来源：{html.escape(target, quote=True)}">'
            f"{html.escape(label)}</span>"
        )
    return (
        f'<a href="{html.escape(target, quote=True)}" target="_blank" '
        f'rel="noopener noreferrer">{html.escape(label)}</a>'
    )


def _default_image(alt: str, target: str) -> str:
    if target.startswith(("https://", "http://")):
        return (
            f'<img src="{html.escape(target, quote=True)}" '
            f'alt="{html.escape(alt, quote=True)}" loading="lazy">'
        )
    return f'<span class="local-ref">〔图片：{html.escape(alt or "本地素材")}〕</span>'


def _inline(
    text: str,
    link_renderer: LinkRenderer,
    image_renderer: ImageRenderer,
) -> str:
    tokens: dict[str, str] = {}

    def stash(rendered: str) -> str:
        token = f"@@MDTOKEN{len(tokens)}@@"
        tokens[token] = rendered
        return token

    text = INLINE_CODE.sub(lambda match: stash(f"<code>{html.escape(match.group(1))}</code>"), text)
    text = INLINE_IMAGE.sub(
        lambda match: stash(image_renderer(match.group(1), match.group(2))), text
    )
    text = INLINE_LINK.sub(
        lambda match: stash(link_renderer(match.group(1), match.group(2))), text
    )
    rendered = html.escape(text, quote=True)
    rendered = INLINE_BOLD.sub(
        lambda match: f"<strong>{match.group(1) or match.group(2)}</strong>", rendered
    )
    rendered = INLINE_STRIKE.sub(r"<del>\1</del>", rendered)
    rendered = INLINE_ITALIC.sub(r"<em>\1</em>", rendered)
    for token, value in tokens.items():
        rendered = rendered.replace(token, value)
    return rendered


def _heading_slug(text: str, used: set[str]) -> str:
    plain = markdown_to_plain(text).lower()
    base = re.sub(r"[^\w\u4e00-\u9fff]+", "-", plain).strip("-") or "section"
    slug = base
    number = 2
    while slug in used:
        slug = f"{base}-{number}"
        number += 1
    used.add(slug)
    return slug


def render_markdown(
    markdown: str,
    *,
    link_renderer: LinkRenderer | None = None,
    image_renderer: ImageRenderer | None = None,
    heading_ids: bool = False,
    collect_toc: bool = False,
    toc_max_level: int = 3,
    table_wrapper_class: str | None = None,
    code_language_class: bool = True,
) -> MarkdownResult:
    """Render the supported Markdown subset with a single escaping policy."""

    render_link = link_renderer or _default_link
    render_image = image_renderer or _default_image
    lines = strip_frontmatter(markdown).splitlines()
    out: list[str] = []
    toc: list[dict[str, object]] = []
    used_slugs: set[str] = set()
    paragraph: list[str] = []
    in_ul = False
    in_ol = False
    index = 0

    def inline(value: str) -> str:
        return _inline(value, render_link, render_image)

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_paragraph() -> None:
        if paragraph:
            value = " ".join(part.strip() for part in paragraph).strip()
            if value:
                out.append(f"<p>{inline(value)}</p>")
            paragraph.clear()

    while index < len(lines):
        stripped = lines[index].strip()

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists()
            language = stripped[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            language_attr = (
                f' class="language-{html.escape(language, quote=True)}"'
                if language and code_language_class
                else ""
            )
            out.append(
                f"<pre><code{language_attr}>{html.escape(chr(10).join(code_lines))}</code></pre>"
            )
            continue

        header = HEADER.match(stripped)
        if header:
            flush_paragraph()
            close_lists()
            level = len(header.group(1))
            label = header.group(2)
            slug = _heading_slug(label, used_slugs) if heading_ids or collect_toc else ""
            id_attr = f' id="{slug}"' if slug else ""
            out.append(f"<h{level}{id_attr}>{inline(label)}</h{level}>")
            if collect_toc and level <= toc_max_level:
                toc.append({"id": slug, "label": markdown_to_plain(label), "level": level})
            index += 1
            continue

        if HR.match(stripped):
            flush_paragraph()
            close_lists()
            out.append("<hr>")
            index += 1
            continue

        if "|" in stripped and index + 1 < len(lines) and TABLE_SEP.match(lines[index + 1]):
            flush_paragraph()
            close_lists()
            headers = [cell.strip() for cell in stripped.strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            if table_wrapper_class:
                out.append(f'<div class="{html.escape(table_wrapper_class, quote=True)}">')
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(cell)}</th>" for cell in headers) + "</tr></thead><tbody>")
            for row in rows:
                cells = row + [""] * max(0, len(headers) - len(row))
                out.append(
                    "<tr>"
                    + "".join(f"<td>{inline(cell)}</td>" for cell in cells[: len(headers)])
                    + "</tr>"
                )
            out.append("</tbody></table>")
            if table_wrapper_class:
                out.append("</div>")
            continue

        ul_match = UL_ITEM.match(stripped)
        if ul_match:
            flush_paragraph()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(ul_match.group(1))}</li>")
            index += 1
            continue

        ol_match = OL_ITEM.match(stripped)
        if ol_match:
            flush_paragraph()
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline(ol_match.group(1))}</li>")
            index += 1
            continue

        quote_match = BLOCKQUOTE.match(stripped)
        if quote_match:
            flush_paragraph()
            close_lists()
            quote_lines = [quote_match.group(1)]
            index += 1
            while index < len(lines):
                next_match = BLOCKQUOTE.match(lines[index].strip())
                if not next_match:
                    break
                quote_lines.append(next_match.group(1))
                index += 1
            out.append(f"<blockquote>{inline(' '.join(quote_lines))}</blockquote>")
            continue

        if not stripped:
            flush_paragraph()
            close_lists()
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    close_lists()
    return MarkdownResult("\n".join(out), toc)

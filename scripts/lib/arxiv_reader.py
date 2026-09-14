#!/usr/bin/env python3
"""Inline arXiv paper reader for the research Wiki.

Fetches a paper's HTML rendering (arXiv's experimental LaTeXML build, with
ar5iv as the fallback for papers that predate it), strips it down to readable
article markup, and serves it inside the Wiki's reader panel so users can read
the paper beside the chat. Documents are cached on disk under
``<kb-root>/work/reader-cache/`` (scratch, never served statically).

stdlib-only: urllib for fetching, ``re`` + ``html`` for cleaning (no
BeautifulSoup / lxml).
"""

from __future__ import annotations

import html as htmllib
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

FETCH_TIMEOUT_S = 45.0
MAX_HTML_BYTES = 12_000_000  # sanity cap — LaTeXML pages are ≤ ~3 MB today

# Accepts new-style ids (2402.10329, optional v2 suffix) and old-style ids
# (cs/0301012, astro-ph.EP/9912004). Version suffixes are stripped for the
# canonical cache key.
ARXIV_ID_RE = re.compile(
    r"^(?:[a-z-]+(?:\.[A-Za-z]{2})?/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?$",
    re.IGNORECASE,
)

ARXIV_PATH_RE = re.compile(r"/(?:abs|html|pdf|doi)/(.+?)(?:\.pdf)?/?$")

_HARVEST_TEMPLATE = "Mozilla/5.0 (compatible; research-wiki-reader/1.0)"
_FETCH_URLS = (
    "https://arxiv.org/html/{paper_id}",
    "https://ar5iv.labs.arxiv.org/html/{paper_id}",
)


def parse_arxiv_id(value: str) -> str | None:
    """Extract a canonical arXiv id from a bare id or an abs/html/pdf URL.

    Returns the versionless id, or None when the input does not name an arXiv
    paper (plain links fall through to normal navigation)."""

    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if candidate.lower().startswith(("http://", "https://")):
        match = re.match(r"^https?://(?:[a-z0-9-]+\.)*arxiv\.org", candidate, re.IGNORECASE)
        if not match:
            return None
        path_match = ARXIV_PATH_RE.search(candidate)
        if not path_match:
            return None
        candidate = path_match.group(1)
    candidate = candidate.removesuffix(".html").strip("/")
    if not ARXIV_ID_RE.match(candidate):
        return None
    return re.sub(r"v\d+$", "", candidate, flags=re.IGNORECASE)


def cache_path(cache_dir: Path, paper_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", paper_id)
    return Path(cache_dir) / f"{safe}.html"


def fetch_paper(paper_id: str, cache_dir: Path, *, timeout: float = FETCH_TIMEOUT_S) -> dict:
    """Return ``{"ok", "paper_id", "html", "source", "error"}`` for a paper.

    The cleaned document is cached on disk; a warm cache answers without any
    network traffic. Network/parse failures degrade to ``ok: False`` plus an
    error string — the caller serves a friendly unavailable page."""

    paper_id = paper_id.strip()
    if not ARXIV_ID_RE.match(paper_id):
        return {"ok": False, "paper_id": paper_id, "html": "", "source": "", "error": "无效的 arXiv ID"}
    target = cache_path(cache_dir, paper_id)
    if target.is_file() and target.stat().st_size > 0:
        try:
            return {
                "ok": True,
                "paper_id": paper_id,
                "html": target.read_text(encoding="utf-8", errors="replace"),
                "source": "cache",
                "error": "",
            }
        except OSError:
            pass  # unreadable cache — refetch below

    errors: list[str] = []
    for url_template in _FETCH_URLS:
        url = url_template.format(paper_id=paper_id)
        try:
            request = urllib.request.Request(url, headers={"User-Agent": _HARVEST_TEMPLATE})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = getattr(response, "status", 200)
                final_url = response.geturl() or url
                if status >= 400:
                    errors.append(f"{url} → HTTP {status}")
                    continue
                payload = response.read(MAX_HTML_BYTES + 1)
            if len(payload) > MAX_HTML_BYTES:
                errors.append(f"{url} → 页面过大")
                continue
            html_text = payload.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            if exc.code in {404, 410}:
                errors.append(f"{url} → 无 HTML 版本（HTTP {exc.code}）")
                continue
            errors.append(f"{url} → HTTP {exc.code}")
            continue
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append(f"{url} → {exc}")
            continue

        cleaned = build_document(paper_id, html_text, base_url=final_url)
        if not cleaned:
            errors.append(f"{url} → 未找到正文（可能没有 HTML 版本）")
            continue
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(cleaned, encoding="utf-8")
        except OSError:
            pass  # cache write is best-effort
        return {"ok": True, "paper_id": paper_id, "html": cleaned, "source": url, "error": ""}

    return {"ok": False, "paper_id": paper_id, "html": "", "source": "", "error": "；".join(errors)}


# ---- document assembly ----------------------------------------------------

_DROP_TAGS_RE = re.compile(
    r"<(script|style|svg|head|nav|footer|dialog|iframe|noscript|button|form|input|select|textarea)\b"
    r"[^>]*>.*?</\1\s*>",
    re.IGNORECASE | re.DOTALL,
)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_MATH_RE = re.compile(r"<math\b[^>]*\balttext=\"([^\"]*)\"[^>]*>.*?</math\s*>", re.IGNORECASE | re.DOTALL)
_MATH_BARE_RE = re.compile(r"<math\b.*?</math\s*>", re.IGNORECASE | re.DOTALL)
_IMG_RE = re.compile(r"<img\b[^>]*\bsrc=\"([^\"]*)\"", re.IGNORECASE)
_ABS_RE = re.compile(r"<a\s[^>]*>", re.IGNORECASE)
_TITLE_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1\s*>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")

READER_CSS = """
:root { color-scheme: light; }
body {
  margin: 0 auto; max-width: 880px; padding: 30px 30px 90px;
  background: #fafaf8; color: #252a27;
  font: 16px/1.78 Georgia, "Songti SC", "Noto Serif CJK SC", serif;
  word-break: break-word;
}
h1, h2, h3, h4 { font-family: Inter, "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.4; }
h1.ltx_title { font-size: 1.55em; margin: 0 0 0.7em; }
h2 { font-size: 1.32em; margin: 1.6em 0 0.6em; border-bottom: 1px solid #e7e9e5; padding-bottom: 5px; }
h3 { font-size: 1.12em; margin: 1.3em 0 0.5em; }
::selection { background: #e2ebe6; }
a { color: #2f5d50; }
img { max-width: 100%; height: auto; margin: 18px auto; display: block; border-radius: 6px; }
figure { margin: 22px 0; }
figcaption { text-align: center; color: #68706b; font-size: 0.82em; margin-top: 8px; }
.ltx_tabular, table { max-width: 100%; display: block; overflow-x: auto; border-collapse: collapse; font-size: 0.86em; }
td, th { padding: 5px 9px; border-bottom: 1px solid #e7e9e5; vertical-align: top; }
.math-inline { font-family: Consolas, monospace; font-size: 0.84em; background: rgba(37,42,39,0.055); padding: 0.1em 0.3em; border-radius: 4px; }
.ltx_bibliography { font-size: 0.88em; line-height: 1.6; }
.ltx_bibitem { margin: 7px 0; }
.reader-ext { color: #68706b; }
"""


def _strip_to_article(raw: str) -> str:
    """Isolate the LaTeXML <article>; fall back to <body> when absent."""

    match = re.search(r"<article\b[^>]*>", raw, re.IGNORECASE)
    if match:
        end = raw.find("</article", match.end())
        if end != -1:
            return raw[match.end():end]
    body = re.search(r"<body\b[^>]*>(.*)</body\s*>", raw, re.IGNORECASE | re.DOTALL)
    return body.group(1) if body else raw


def _neutralize_anchors(html_text: str, base_url: str) -> str:
    """Links must not navigate inside the sandboxed panel. Fragment anchors
    stay (in-document navigation is safe and useful); arXiv paper links become
    reader refs carrying the parsed id (the frontend opens them in-panel);
    everything else degrades to inert text with the absolute URL in title."""

    out: list[str] = []
    pos = 0
    for match in _ABS_RE.finditer(html_text):
        out.append(html_text[pos:match.start()])
        tag = match.group(0)
        href_match = re.search(r'\bhref="([^"]*)"', tag)
        href = href_match.group(1) if href_match else ""
        if href.startswith("#"):
            out.append(tag)
        else:
            paper = parse_arxiv_id(urljoin(base_url, href)) or ""
            if paper:
                out.append(f'<a class="reader-ref" data-arxiv="{htmllib.escape(paper, quote=True)}" href="#">')
            else:
                url = htmllib.escape(urljoin(base_url, href)[:200], quote=True)
                out.append(f'<a class="reader-ext" href="#" title="{url}">')
        pos = match.end()
    out.append(html_text[pos:])
    return "".join(out)


def build_document(paper_id: str, raw: str, *, base_url: str) -> str | None:
    """Clean a fetched LaTeXML page into a standalone styled article document.

    Returns None when the page carries no article (e.g. arXiv's "no HTML"
    placeholder), which the caller reports as unavailable."""

    body = _strip_to_article(raw)
    body = _COMMENT_RE.sub("", body)
    body = _DROP_TAGS_RE.sub("", body)
    if not _TAG_RE.sub("", body).strip():
        return None

    # Math: keep the LaTeX source as inline code — readable without MathML.
    body = _MATH_RE.sub(lambda m: f'<code class="math-inline">{htmllib.escape(htmllib.unescape(m.group(1)))}</code>', body)
    body = _MATH_BARE_RE.sub("", body)

    # Images: absolutize against the final fetch URL.
    body = _IMG_RE.sub(
        lambda m: f'<img src="{htmllib.escape(urljoin(base_url, htmllib.unescape(m.group(1))), quote=True)}"',
        body,
    )

    body = _neutralize_anchors(body, base_url=base_url)

    title_match = _TITLE_RE.search(body)
    title = ""
    if title_match:
        title = re.sub(r"\s+", " ", htmllib.unescape(_TAG_RE.sub(" ", title_match.group(1)))).strip()
        title = title[:300]

    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{htmllib.escape(title or f'arXiv:{paper_id}')}</title>\n"
        f"<style>{READER_CSS}</style>\n"
        "</head>\n"
        f'<body data-reader-doc="ok" data-paper-id="{htmllib.escape(paper_id, quote=True)}">\n'
        f"{body}\n</body>\n</html>\n"
    )


def unavailable_page(paper_id: str, error: str) -> str:
    """A styled placeholder for papers without an HTML rendering."""

    detail = f'<p class="reader-error-detail">{htmllib.escape(error[:400])}</p>' if error else ""
    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        f"<title>arXiv:{htmllib.escape(paper_id)} 暂无 HTML 版本</title>\n"
        f"<style>{READER_CSS}\n"
        ".reader-unavailable { max-width: 460px; margin: 14vh auto; text-align: center;"
        ' font-family: Inter, "PingFang SC", sans-serif; }\n'
        ".reader-unavailable h1 { font-size: 20px; }\n"
        ".reader-unavailable p { color: #68706b; font-size: 14px; line-height: 1.7; }\n"
        ".reader-unavailable a { color: #2f5d50; }\n"
        ".reader-error-detail { word-break: break-all; font-size: 11px; color: #929893; }\n"
        "</style>\n</head>\n"
        '<body data-reader-doc="unavailable">\n'
        '<div class="reader-unavailable">\n'
        "<h1>这篇论文暂无可用的 HTML 版本</h1>\n"
        f"<p>arXiv:{htmllib.escape(paper_id)} 没有实验性 HTML 渲染（较老的投稿常见）。</p>\n"
        f'<p>可以在 arXiv 摘要页获取 PDF：<br><a href="https://arxiv.org/abs/{htmllib.escape(paper_id, quote=True)}" target="_blank">arxiv.org/abs/{htmllib.escape(paper_id)}</a></p>\n'
        f"{detail}\n"
        "</div>\n</body>\n</html>\n"
    )

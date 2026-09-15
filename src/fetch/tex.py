#!/usr/bin/env python3
"""Fetch a paper's full text as Markdown and emit the unified extraction JSON.

Two transports, selected by ``--transport``:

- ``arxiv2md`` (default): curl the public arxiv2md REST API
  (https://github.com/timf34/arxiv2md — ``GET /api/markdown?url=<id>``).
  Zero dependencies, no credentials, returns section-aware markdown with
  LaTeX math. Works for papers with arXiv HTML (roughly 2024-03 onward;
  older/PDF-only IDs answer HTTP 400).
- ``s3-tex`` (TODO): download the TeX source tarball from ``s3://arxiv/`` via
  boto3 and convert the main ``.tex`` with pypandoc. The bucket is
  requester-pays (needs AWS credentials), and pandoc must be installed —
  kept functional but pending account setup; see download_arxiv_source.py.

Both paths produce the same unified extraction JSON
(``extraction_method: "tex-pandoc"`` for s3-tex, ``"arxiv2md"`` for the API,
both with ``source_format: "tex"``-style markdown semantics: authoritative
text, no visual validation) plus a markdown sidecar.

Library API: :class:`TexExtraction` (one CLI-configured extraction run) plus
the module-level helpers (tarball safety, main-Tex discovery, quality
assessment, arxiv2md transport). The CLI surface owns argument parsing and
lives in the skill entry
``skills/embodied-ai-literature-hub/scripts/extract_arxiv_tex.py``.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any

# The S3 downloader's top-level imports are stdlib-only (boto3 stays lazy inside it),
# so a module-level import is safe and mock-patchable.
from src.fetch import s3_source as download_arxiv_source

DEFAULT_SOURCE_CACHE_DIR = "/tmp/embodied-ai-literature-hub/src"
DEFAULT_TO = "markdown+tex_math_dollars"  # plain $...$ math; gfm would render $`...`$ backtick math
MAX_EXTRACT_BYTES = 512 * 1024 * 1024
MAX_MEMBERS = 20000
ALLOWED_SUFFIXES = {".tex", ".bib", ".bbl", ".sty", ".cls"}
MAX_TERM_MATCHES = 120

ARXIV2MD_API = "https://arxiv2md.org/api/markdown"
ARXIV2MD_JSON_API = "https://arxiv2md.org/api/json"
ARXIV2MD_PARAMS = "remove_refs=false&remove_toc=false&remove_citations=false"

MATH_TOKEN_RE = re.compile(r"\$[^$\n]+\$|\\\(|\\\[|\$\$")
TABLE_SEPARATOR_RE = re.compile(r"^\|?[\s:|-]+\|[\s:|-]*$")



def import_pypandoc():
    try:
        import pypandoc  # type: ignore

        return pypandoc
    except ImportError as exc:
        raise SystemExit(
            "pypandoc is required for TeX source conversion. Install it with:\n"
            "  pip install 'embodied-ai-literature-hub[tex]'   (from the repo root)\n"
            "or: pip install pypandoc\n"
            "A pandoc binary is also needed: apt install pandoc, or pip install pypandoc-binary."
        ) from exc


def normalize_id(value: str) -> str:
    return re.sub(r"v\d+$", "", str(value or "").strip().rsplit("/", 1)[-1])


def _member_is_safe(member: tarfile.TarInfo) -> bool:
    if member.isdir():
        return True
    if not member.isfile():
        return False  # symlinks/hardlinks/devices are refused outright
    path = Path(member.name)
    if path.is_absolute() or ".." in path.parts:
        return False
    return path.suffix.lower() in ALLOWED_SUFFIXES


def safe_extract(tar_path: Path, dest: Path) -> list[str]:
    """Extract only text-bearing TeX members, guarding paths and total size."""
    extracted: list[str] = []
    total = 0
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_path, "r:gz") as archive:
        members = archive.getmembers()
        if len(members) > MAX_MEMBERS:
            raise ValueError(f"tarball has {len(members)} members (limit {MAX_MEMBERS})")
        for member in members:
            if not _member_is_safe(member):
                continue
            total += int(member.size)
            if total > MAX_EXTRACT_BYTES:
                raise ValueError(f"tarball exceeds the {MAX_EXTRACT_BYTES} byte extraction cap")
            archive.extract(member, dest, filter="data")
            extracted.append(member.name)
    return extracted


def find_main_tex(names: list[str], forced: str | None = None, root: Path | None = None) -> str | None:
    """Pick the .tex containing \\begin{document}; largest wins, --main-tex overrides."""
    base = root or Path(".")
    if forced:
        for name in names:
            if name == forced:
                return name
        return None
    best: tuple[int, str] | None = None
    for name in names:
        if not name.lower().endswith(".tex"):
            continue
        try:
            text = (base / name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "\\begin{document}" not in text:
            continue
        if best is None or len(text) > best[0]:
            best = (len(text), name)
    return best[1] if best else None


def convert_to_markdown(pypandoc: Any, main_tex: Path, to: str) -> str:
    return pypandoc.convert_file(
        str(main_tex),
        to,
        format="latex",
        extra_args=["--resource-path", str(main_tex.parent), "--wrap=none"],
    )


def markdown_sections(text: str) -> list[dict[str, Any]]:
    """Mine ATX headings into the extraction `sections` shape (locator anchors)."""
    sections: list[dict[str, Any]] = []
    lines = text.splitlines()
    open_stack: list[tuple[int, dict[str, Any], int]] = []  # (level, section, start_line)
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        # close every section at a deeper-or-equal level
        while open_stack and open_stack[-1][0] >= level:
            _, section, start = open_stack.pop()
            section["char_count"] = sum(len(line) for line in lines[start:index])
        section = {
            "index": len(sections),
            "id": "",
            "kind": "section",
            "title": title,
            "path": " > ".join([s[1]["title"] for s in open_stack if s[0] < level] + [title]),
            "level": level,
            "char_count": 0,
        }
        sections.append(section)
        open_stack.append((level, section, index))
    while open_stack:
        _, section, start = open_stack.pop()
        section["char_count"] = sum(len(line) for line in lines[start:])
    return sections


def markdown_term_matches(text: str, terms: list[str], window: int = 260) -> list[dict[str, Any]]:
    sections = markdown_sections(text)
    matches: list[dict[str, Any]] = []
    lowered = text.lower()
    lines = text.splitlines()
    for raw_term in terms:
        term = raw_term.lower()
        start = 0
        while True:
            index = lowered.find(term, start)
            if index < 0 or len(matches) >= MAX_TERM_MATCHES:
                return matches
            locator_path = "Markdown body"
            for section in sections:
                heading_offset = _section_heading_offset(lines, section["index"])
                if 0 <= heading_offset <= index:
                    locator_path = str(section["path"])
            line_no = text[:index].count("\n") + 1
            left = max(0, index - window)
            right = min(len(text), index + len(term) + window)
            matches.append(
                {
                    "term": raw_term,
                    "locator": f"{locator_path} ¶ line-{line_no}",
                    "char_start": index,
                    "snippet": " ".join(text[left:right].split()),
                }
            )
            start = index + len(term)
    return matches


def _section_heading_offset(lines: list[str], section_index: int) -> int:
    """Char offset of a section's heading line (sections are in document order)."""
    seen = 0
    counted = 0
    for line in lines:
        match = re.match(r"^(#{1,6})\s+", line)
        if match and counted == section_index:
            return seen
        if match:
            counted += 1
        seen += len(line) + 1
    return -1


def assess_quality(text: str, minimum_chars: int) -> dict[str, Any]:
    chars = len(re.sub(r"\s+", "", text))
    section_count = len(markdown_sections(text))
    math_preserved = bool(MATH_TOKEN_RE.search(text))
    table_count = sum(
        1
        for index, line in enumerate(text.splitlines())
        if "|" in line and index + 1 < len(text.splitlines()) and TABLE_SEPARATOR_RE.match(text.splitlines()[index + 1])
    )
    if chars >= 2 * minimum_chars and section_count >= 3:
        grade = "high"
    elif chars >= minimum_chars:
        grade = "medium"
    else:
        grade = "low"
    return {
        "grade": grade,
        "text_chars": chars,
        "structure": "markdown",
        "section_count": section_count,
        "math_preserved": math_preserved,
        "table_count": table_count,
    }


def document_title(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1)
    # arxiv2md markdown starts at `##`; the first heading is the paper title
    # (a `## Contents` TOC line means the title follows it after the TOC block).
    skip_until_content = False
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if not match:
            continue
        title = match.group(1).strip()
        if title.lower() == "contents":
            skip_until_content = True
            continue
        if skip_until_content and not line.startswith("-"):
            return title
        if not skip_until_content:
            return title
    return ""


def latex_title(main_tex_text: str) -> str:
    """Pull \\title{...} from the TeX source (pandoc's first h1 is usually §1)."""
    match = re.search(r"\\title\s*(?:\[[^\]]*\])?\s*\{", main_tex_text)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for index in range(start, len(main_tex_text)):
        char = main_tex_text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                inner = main_tex_text[start + 1 : index]
                # drop nested commands, keep the words
                inner = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?", " ", inner)
                inner = re.sub(r"[{}]", "", inner)
                return " ".join(inner.split())
    return ""


def build_output(
    markdown: str,
    main_tex: str,
    cache_file: str,
    *,
    paper_id: str = "",
    terms: str | None = None,
    minimum_chars: int = 1000,
    tex_title: str = "",
    method: str = "tex-pandoc",
) -> dict[str, Any]:
    """Build the unified extraction payload; option values are explicit kwargs."""
    terms_list = [term.strip() for term in (terms or "").split(",") if term.strip()]
    quality = assess_quality(markdown, minimum_chars)
    available = quality["grade"] in {"high", "medium"}
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(paper_id),
        "available": available,
        "cache_file": cache_file,
        "structure": "markdown",
        "text_chars": quality["text_chars"],
        "source_format": "tex",
        "extraction_method": method,
        "main_tex": main_tex,
        "title": tex_title or document_title(markdown),
        "sections": markdown_sections(markdown),
        "term_matches": markdown_term_matches(markdown, terms_list) if terms_list else [],
        "selected_passages": [],
        "reference_hints": [],
        "text": markdown,
        "quality": quality,
        "evidence_eligible": bool(available),
        "needs_visual_validation": False,
        "visual_validation": "not-required",
        "attempts": [{"method": method, "available": bool(available), "quality": quality["grade"]}],
        "fallback_reason": "" if available else "TeX conversion below the minimum quality gate.",
    }


def unavailable_output(paper_id: str, method: str, error: str) -> dict[str, Any]:
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "paper_id": normalize_id(paper_id),
        "available": False,
        "source_format": "tex",
        "extraction_method": method,
        "structure": "markdown",
        "text_chars": 0,
        "quality": {"grade": "low", "text_chars": 0, "structure": "markdown", "math_preserved": False, "table_count": 0},
        "evidence_eligible": False,
        "needs_visual_validation": False,
        "text": "",
        "sections": [],
        "term_matches": [],
        "selected_passages": [],
        "reference_hints": [],
        "attempts": [{"method": method, "available": False, "quality": "low", "error": error}],
        "fallback_reason": f"Full text not recoverable via {method}: {error}",
    }


def fetch_arxiv2md(paper_id: str, curl_timeout: float) -> tuple[str, str]:
    """Fetch paper markdown from the public arxiv2md REST API via curl.

    The API accepts arXiv IDs/URLs and returns section-aware markdown with
    LaTeX math. Papers without arXiv HTML (older or PDF-only) answer HTTP 400.
    Public rate limit: 30 requests/minute per IP.

    Returns (markdown, title). The title comes from the JSON endpoint
    (the markdown itself starts at the Contents/Abstract level, not the title).
    """
    url = f"{ARXIV2MD_API}?url={paper_id}&{ARXIV2MD_PARAMS}"
    markdown, code = _curl_get(url, curl_timeout)
    if code == "400":
        raise RuntimeError(f"arxiv2md has no HTML for {paper_id} (HTTP 400): {markdown[:300]}")
    if code != "200":
        raise RuntimeError(f"arxiv2md answered HTTP {code} for {paper_id}: {markdown[:200]}")
    if not markdown:
        raise RuntimeError(f"arxiv2md returned an empty body for {paper_id}")
    title = ""
    try:
        meta, meta_code = _curl_get(f"{ARXIV2MD_JSON_API}?url={paper_id}", curl_timeout)
        if meta_code == "200":
            title = str(json.loads(meta).get("title") or "")
    except (RuntimeError, json.JSONDecodeError):
        pass  # markdown still usable; title falls back to the first content heading
    return markdown, (title or document_title(markdown))


def _curl_get(url: str, curl_timeout: float) -> tuple[str, str]:
    completed = subprocess.run(
        ["curl", "-sS", "--max-time", str(max(1.0, curl_timeout)), "-w", "\n%{http_code}", url],
        capture_output=True,
        text=True,
        check=False,
    )
    body, _, code = completed.stdout.rpartition("\n")
    if completed.returncode != 0:
        raise RuntimeError(f"curl failed (rc={completed.returncode}): {completed.stderr.strip()[:300]}")
    return body.strip(), code.strip()


class TexExtraction:
    """One CLI-configured Markdown-tier extraction run for a single paper.

    Options are explicit constructor parameters (the CLI entry translates
    argparse into these); call :meth:`run` to fetch/convert and emit the JSON
    payload. The parameter names mirror the old CLI flag names.
    """

    def __init__(
        self,
        *,
        paper_id: str = "",
        transport: str = "arxiv2md",
        source: str | None = None,
        source_cache_dir: str = DEFAULT_SOURCE_CACHE_DIR,
        main_tex: str | None = None,
        terms: str | None = None,
        minimum_chars: int = 1000,
        to: str = DEFAULT_TO,
        pandoc_timeout: float = 60.0,
        curl_timeout: float = 120.0,
        output: str | None = None,
        markdown_output: str | None = None,
    ) -> None:
        self.paper_id = paper_id
        self.transport = transport
        self.source = source
        self.source_cache_dir = source_cache_dir
        self.main_tex = main_tex
        self.terms = terms
        self.minimum_chars = minimum_chars
        self.to = to
        self.pandoc_timeout = pandoc_timeout
        self.curl_timeout = curl_timeout
        self.output = output
        self.markdown_output = markdown_output

    def run(self) -> dict[str, Any]:
        """Fetch markdown (arxiv2md) or convert TeX (s3-tex) and build the payload."""
        if self.transport == "arxiv2md":
            if not self.paper_id:
                raise SystemExit("--transport arxiv2md requires --paper-id")
            paper_id = normalize_id(self.paper_id)
            try:
                markdown, title = fetch_arxiv2md(paper_id, self.curl_timeout)
            except RuntimeError as exc:
                return unavailable_output(self.paper_id, "arxiv2md", str(exc))
            return build_output(
                markdown,
                "",
                f"{ARXIV2MD_API}?url={paper_id}",
                paper_id=self.paper_id,
                terms=self.terms,
                minimum_chars=self.minimum_chars,
                tex_title=title,
                method="arxiv2md",
            )
        # s3-tex transport: requester-pays S3 tarball + pandoc conversion (TODO: needs AWS credentials)
        return self.run_s3_tex()

    def run_s3_tex(self) -> dict[str, Any]:
        """S3 TeX transport: tarball -> safe extract -> pandoc -> unified payload."""
        pypandoc = import_pypandoc()
        if self.source:
            tar_path = Path(self.source).expanduser()
        elif self.paper_id:
            paper_id = normalize_id(self.paper_id)
            download_options = download_arxiv_source.S3DownloadOptions(
                cache_dir=self.source_cache_dir,
                workers=1,
                timeout=60.0,
                retries=2,
                region=download_arxiv_source.REGION,
                force=False,
            )
            client = download_arxiv_source.make_client(download_options.region)
            result = download_arxiv_source.download_one(paper_id, download_options, client)
            if result["state"] not in {"downloaded", "cached"}:
                return unavailable_output(self.paper_id, "tex-pandoc", result["error"])
            tar_path = Path(result["path"])
        else:
            raise SystemExit("provide --paper-id or --source")

        with tempfile.TemporaryDirectory(prefix="arxiv-tex-") as tmp:
            tmp_dir = Path(tmp)
            extracted = safe_extract(tar_path, tmp_dir)
            main_tex = find_main_tex(extracted, self.main_tex, root=tmp_dir)
            if main_tex is None:
                raise ValueError("no .tex member with \\begin{document}; use --main-tex to point at one")
            main_tex_text = (tmp_dir / main_tex).read_text(encoding="utf-8", errors="replace")
            markdown = convert_to_markdown(pypandoc, tmp_dir / main_tex, self.to).strip()
            return build_output(
                markdown,
                main_tex,
                str(tar_path),
                paper_id=self.paper_id,
                terms=self.terms,
                minimum_chars=self.minimum_chars,
                tex_title=latex_title(main_tex_text),
                method="tex-pandoc",
            )


def write_markdown_sidecar(output_path: str | None, markdown: str, explicit: str | None) -> None:
    target = explicit
    if target is None and output_path:
        target = re.sub(r"\.json$", "", output_path) + ".md"
    if not target:
        return
    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown + "\n", encoding="utf-8")


def emit(output: dict[str, Any], output_path: str | None, markdown_output: str | None) -> None:
    """Write/print the extraction JSON and its Markdown sidecar (CLI-side)."""
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
        write_markdown_sidecar(output_path, str(output.get("text") or ""), markdown_output)
    else:
        print(rendered)

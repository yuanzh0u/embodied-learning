#!/usr/bin/env python3
"""audit-slide-deck: 汇报展示（slide-deck）交付物的内容审计.

检查 slide-deck_report.md（slide-source DSL）与可选的已编译 HTML：
页数边界、每页密度、verdict 覆盖率、引文完整性（{{key}} 必须全部落在 refs 表，
refs 表未被引用的键给 warning）、图文件存在性、HTML 的 div 配平/外部资源/引文编号。

用法::

    writing_audit.py audit-slide-deck --source slide-deck_report.md \
        [--refs refs.json] [--html slide-deck_report.html] [--json]

退出码：0 无 error（warning 不算失败）；1 有 error；2 参数/文件错误。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:  # sibling import works under any loader
    sys.path.insert(0, str(_SCRIPTS_DIR))
import build_slide_deck as bsd  # noqa: E402  (sibling module, same directory)

MIN_PAGES, WARN_PAGES, MAX_PAGES = 5, 10, 60


def _load_refs(path: Path | None, meta: dict, base_dir: Path) -> dict:
    refs_path = path or (meta.get("refs") and Path(meta["refs"]))
    if not refs_path:
        return {}
    refs_path = Path(refs_path)
    if not refs_path.is_absolute():
        refs_path = base_dir / refs_path
    return json.loads(refs_path.read_text(encoding="utf-8"))


def audit_source(source: Path, refs_override: Path | None) -> tuple[list[dict], dict]:
    findings: list[dict] = []
    text = source.read_text(encoding="utf-8")
    errors: list[str] = []
    meta, slides = bsd.split_slides(text, errors)
    for err in errors:
        findings.append({"severity": "error", "check": "parse", "message": err})

    n_content = [s for s in slides if s["head"].get("class") not in ("cover", "end")]
    if len(slides) < MIN_PAGES:
        findings.append({"severity": "error", "check": "page-count",
                         "message": f"全册仅 {len(slides)} 页，少于 {MIN_PAGES} 页下限"})
    elif len(slides) < WARN_PAGES:
        findings.append({"severity": "warning", "check": "page-count",
                         "message": f"全册 {len(slides)} 页偏少（建议 ≥{WARN_PAGES} 页）"})
    if len(slides) > MAX_PAGES:
        findings.append({"severity": "warning", "check": "page-count",
                         "message": f"全册 {len(slides)} 页超出 {MAX_PAGES} 页上限，考虑分册"})

    no_verdict = [s["idx"] for s in n_content if not s["head"].get("verdict")]
    if n_content and len(no_verdict) / len(n_content) > 0.4:
        findings.append({"severity": "warning", "check": "verdict-coverage",
                         "message": f"{len(no_verdict)}/{len(n_content)} 内容页缺 verdict 结论条"
                                    f"（超过 40%）：页 " + ", ".join(map(str, no_verdict[:8]))})

    refs = _load_refs(refs_override, meta, source.parent)
    cited: dict[str, int] = {}
    for slide in slides:
        blob = slide["body"] + "\n" + slide["head"].get("verdict", "")
        for m in bsd._CITE_RE.finditer(blob):
            key = m.group(1)
            cited[key] = cited.get(key, 0) + 1
            if refs and key not in refs:
                findings.append({"severity": "error", "check": "citation-resolve",
                                 "message": f"slide {slide['idx']}: 引文键 {{{{{key}}}}} 不在 refs 表"})
    if refs:
        for key in refs:
            if key not in cited:
                findings.append({"severity": "warning", "check": "refs-unused",
                                 "message": f"refs 表键 {key} 未被任何页引用"})

    for slide in slides:
        src_dir = source.parent
        body = slide["body"]
        try:
            bsd.render_body(body, {k: 1 for k in cited} or {}, slide["idx"],
                            src_dir, errors)
        except bsd.CompileError as exc:
            findings.append({"severity": "error", "check": "render",
                             "message": f"slide {slide['idx']}: {exc}"})
        for m in re.finditer(r"@fig\s+([^|\n]+)", body):
            path = Path(m.group(1).strip())
            if not path.is_absolute():
                path = src_dir / path
            if not path.is_file():
                findings.append({"severity": "error", "check": "figure-exists",
                                 "message": f"slide {slide['idx']}: 图不存在 {path}"})
    for err in errors:
        if "未知指令" in err or "超过每页" in err:
            findings.append({"severity": "error", "check": "density", "message": err})
        elif err not in {f["message"] for f in findings}:
            findings.append({"severity": "warning", "check": "render", "message": err})

    stats = {"pages": len(slides), "content_pages": len(n_content),
             "citations": len(cited), "refs_available": len(refs)}
    # The compiler appends References pages (chunked) and an optional end page,
    # so the compiled HTML has more sections than the source has slides.
    import math
    stats["expected_sections"] = (
        len(slides)
        + (math.ceil(len(cited) / bsd.REFS_PER_PAGE) if cited else 0)
        + (1 if meta.get("end") else 0))
    return findings, stats


def audit_html(html_path: Path, pages: int) -> tuple[list[dict], dict]:
    findings: list[dict] = []
    html = html_path.read_text(encoding="utf-8")
    body = re.sub(r"<script>.*?</script>", "", html[html.index("<body>"):], flags=re.S)
    secs = re.findall(r"<section.*?</section>", body, flags=re.S)
    if pages and len(secs) != pages:
        findings.append({"severity": "error", "check": "html-sections",
                         "message": f"HTML {len(secs)} 个 section 与 source {pages} 页不一致"})
    for i, sec in enumerate(secs, 1):
        if sec.count("<div") != sec.count("</div>"):
            findings.append({"severity": "error", "check": "html-balance",
                             "message": f"slide {i}: div 不配平"})
    if re.search(r'<img src="(?!data:)', body):
        findings.append({"severity": "error", "check": "html-offline",
                         "message": "存在非 base64 内联的图片（离线放映会破图）"})
    return findings, {"html_sections": len(secs)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="audit-slide-deck", description=__doc__)
    parser.add_argument("--source", required=True, help="slide-deck_report.md")
    parser.add_argument("--refs", help="引文键表 JSON（默认读 source 头的 # refs:）")
    parser.add_argument("--html", help="已编译的 slide-deck_report.html")
    parser.add_argument("--json", action="store_true", help="stdout 输出 JSON")
    args = parser.parse_args(argv)

    source = Path(args.source)
    if not source.is_file():
        print(f"source not found: {source}", file=sys.stderr)
        return 2
    findings, stats = audit_source(source, Path(args.refs) if args.refs else None)
    if args.html:
        html_path = Path(args.html)
        if not html_path.is_file():
            print(f"html not found: {html_path}", file=sys.stderr)
            return 2
        h_findings, h_stats = audit_html(html_path, stats["expected_sections"])
        findings += h_findings
        stats.update(h_stats)

    errors = [f for f in findings if f["severity"] == "error"]
    if args.json:
        print(json.dumps({"findings": findings, **stats}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f"[{f['severity'].upper()}] {f['check']}: {f['message']}")
        print(f"pages={stats['pages']} citations={stats['citations']} "
              f"errors={len(errors)} warnings={len(findings) - len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

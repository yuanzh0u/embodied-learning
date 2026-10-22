"""Extraction-output plumbing shared by the fetch chain and the TeX tier.

One home for the "render JSON/markdown and write to file-or-stdout" helpers
that were duplicated as two different ``emit()`` implementations
(``fetch/chain.py`` and ``fetch/tex.py``). The tier-specific emit functions
stay as thin wrappers with their original signatures.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def dump_json(output: dict[str, Any]) -> str:
    return json.dumps(output, ensure_ascii=False, indent=2)


def write_json_output(output: dict[str, Any], output_path: str | None) -> None:
    """Write pretty JSON to ``output_path``, or print it when no path is given."""

    rendered = dump_json(output)
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def write_text_output(rendered: str, output_path: str | None) -> None:
    """Write a rendered document to ``output_path``, or print it when absent."""

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def write_markdown_sidecar(output_path: str | None, markdown: str, explicit: str | None) -> None:
    """Write the Markdown sidecar next to a JSON extraction (``.json`` -> ``.md``)."""

    target = explicit
    if target is None and output_path:
        target = re.sub(r"\.json$", "", output_path) + ".md"
    if not target:
        return
    path = Path(target)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown + "\n", encoding="utf-8")

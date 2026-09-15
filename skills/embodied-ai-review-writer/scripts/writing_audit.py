#!/usr/bin/env python3
"""CLI: writer-side audit tools — trace maps and editorial quality gates.

One entry, three subcommands (the old single-purpose scripts, kebab-cased):
build-trace-map | audit-article-quality | audit-zhihu-corpus. Each
subcommand reuses its original parser verbatim (sys.argv slice), so flags,
help text, and exit codes are unchanged.
"""
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import _article_quality  # noqa: E402  (sibling modules, same directory)
import _trace_map  # noqa: E402
import _zhihu_corpus  # noqa: E402

_SUBCOMMANDS = {
    "build-trace-map": _trace_map,
    "audit-article-quality": _article_quality,
    "audit-zhihu-corpus": _zhihu_corpus,
}


def main(argv: list[str] | None = None) -> int:
    """Dispatch to the tool's own parser; flags and exit codes unchanged."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("\nsubcommands: " + ", ".join(_SUBCOMMANDS))
        return 0
    module = _SUBCOMMANDS.get(argv[0])
    if module is None:
        print(f"unknown subcommand: {argv[0]}", file=sys.stderr)
        print("subcommands: " + ", ".join(_SUBCOMMANDS), file=sys.stderr)
        return 2
    saved = sys.argv
    try:
        sys.argv = [f"writing_audit.py {argv[0]}"] + argv[1:]
        return module.main()
    finally:
        sys.argv = saved


if __name__ == "__main__":
    sys.exit(main())

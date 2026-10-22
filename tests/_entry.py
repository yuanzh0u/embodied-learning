"""Test helper: invoke a library entry the way the dispatchers do.

The library exposes ``run(args) -> int`` (no argparse, no ``main``); the
dispatcher owns the flag table. Tests that used to call ``mod.main([...])``
call :func:`invoke` instead — same argv, same exit code, and the module
globals stay patchable via ``mock.patch.object(mod, ...)``.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_entry(entry_path: Path):
    """Load a dispatcher module by path (works for scripts/ and skills/*/scripts/)."""
    name = "entry_" + entry_path.stem + "_" + str(abs(hash(entry_path.as_posix())))
    spec = importlib.util.spec_from_file_location(name, entry_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def invoke(entry: str, subcommand: str, argv: list[str]) -> int:
    """Run one subcommand through its dispatcher's parser and library ``run()``.

    ``entry`` is the dispatcher file name, e.g. ``"run.py"`` (resolved under
    ``scripts/`` first, then each ``skills/*/scripts/``).
    """
    candidates = [_REPO_ROOT / "scripts" / entry]
    candidates += sorted((_REPO_ROOT / "skills").glob(f"*/scripts/{entry}"))
    path = next((p for p in candidates if p.is_file()), None)
    if path is None:
        raise FileNotFoundError(entry)
    module = _load_entry(path)
    parser = module._parser_for(subcommand) if hasattr(module, "_parser_for") else None
    if parser is None:
        # dispatchers that build parsers inline (search/fetch/read/write)
        if hasattr(module, "dispatch"):
            return int(module.dispatch([subcommand, *argv]) or 0)
        return int(module.main([subcommand, *argv]) or 0)
    parser.prog = subcommand
    args = parser.parse_args(argv)
    impl = __import__(module._MODULES[subcommand], fromlist=["run"])
    return int(impl.run(args) or 0)


def parse(entry: str, subcommand: str, argv: list[str]):
    """Build the subcommand's argparse Namespace without running anything."""
    candidates = [_REPO_ROOT / "scripts" / entry]
    candidates += sorted((_REPO_ROOT / "skills").glob(f"*/scripts/{entry}"))
    path = next(p for p in candidates if p.is_file())
    module = _load_entry(path)
    parser = module._parser_for(subcommand)
    parser.prog = subcommand
    return parser.parse_args(argv)

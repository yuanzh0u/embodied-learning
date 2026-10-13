"""Install-layout resolution: repo checkout vs wheel install.

The distribution maps repo trees into import packages (see pyproject.toml):

- repo checkout: this file lives at <repo>/embodied_learning/utils/layout.py,
  the skills tree at <repo>/skills, the top-level scripts at <repo>/scripts.
- wheel install: this file lives at <site-packages>/embodied_learning/utils/
  layout.py; pyproject maps the skills/ tree in as `wiki_scripts.skills`
  package data, so the installed `wiki_scripts` directory is layout-complete —
  it IS the scripts root and contains skills/ beside the script modules.

Callers use `find_roots()` instead of `Path(__file__).parent.parent`-style
bootstrapping, which silently points into site-packages when installed.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

# Local-KB-first convention: knowledge outputs live under the local KB, never
# in the package. (Same default as serve_research_wiki.DEFAULT_KB_ROOT.)
DEFAULT_KB_ROOT = Path.home() / "Documents" / "arxiv"


def _wiki_scripts_dir() -> Path | None:
    """Directory of the installed ``wiki_scripts`` package (None in a checkout
    where it is not importable as a package)."""

    spec = importlib.util.find_spec("wiki_scripts")
    if spec and spec.submodule_search_locations:
        return Path(next(iter(spec.submodule_search_locations)))
    return None


def find_roots() -> tuple[Path | None, Path, Path]:
    """Return (repo_root_or_None, skills_root, scripts_root).

    Repo checkout is detected by the pyproject.toml two levels up from this
    file (embodied_learning/utils/layout.py). Editable installs resolve here
    too, which is correct — they run against the checkout. Anything else is a
    wheel install where the wiki_scripts package dir holds both the scripts
    and the bundled skills tree.
    """
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    if (repo_root / "pyproject.toml").is_file():
        return repo_root, repo_root / "skills", repo_root / "scripts"
    pkg_dir = _wiki_scripts_dir()
    if pkg_dir is None:  # pragma: no cover - defensive: installed without wiki_scripts
        pkg_dir = here.parents[1]
    return None, pkg_dir / "skills", pkg_dir


def default_kb_root() -> Path:
    """Canonical local KB root for new environments (override per-call with
    --kb-root; serve_research_wiki keeps its own DEFAULT_KB_ROOT constant)."""
    return DEFAULT_KB_ROOT


def infer_kb_root(run_dir: Path) -> Path | None:
    """Owning KB root of a run directory, from its birth layout.

    run.py init places runs at ``<kb-root>/work/<run>/``, so the root is the
    grandparent of a run that lives under ``work/``. Returns None for any
    other layout (callers fall back to an explicit --kb-root or the default).

    This is the guard against silent cross-KB publish: run.py finalize must
    never copy a run into a KB that does not own its work/ directory (the
    2026-09-30 absolute-pose run published into ~/Documents/arxiv while the
    run lived under the /mount/TEST wiki KB — the writer omitted --kb-root and
    the default swallowed it)."""
    resolved = Path(run_dir).expanduser().resolve()
    if resolved.parent.name == "work":
        return resolved.parent.parent
    return None


def resolve_pipeline_layout(pipeline_root: Path) -> tuple[Path, Path]:
    """Given the pipeline root, return (skills_root, scripts_root).

    The wiki chat/prompt layer asks for this by pipeline root; it is path
    resolution and therefore lives here, not in the prompt layer.

    Three shapes: repo checkout (``<root>/skills`` + ``<root>/scripts``), wheel
    install where the root IS the scripts package dir (contains ``run.py init``
    and the bundled ``skills/``), and a bare skills/ root (the wheel's
    ``wiki_scripts/skills`` — its parent holds the scripts)."""

    skills_root = pipeline_root if pipeline_root.name == "skills" else pipeline_root / "skills"
    if (pipeline_root / "scripts" / "run.py").is_file():
        scripts_root = pipeline_root / "scripts"
    elif (pipeline_root / "run.py").is_file():
        scripts_root = pipeline_root  # installed: the wiki_scripts dir itself
    elif pipeline_root.name == "skills" and (pipeline_root.parent / "run.py").is_file():
        scripts_root = pipeline_root.parent  # installed: wiki_scripts/skills shape
    else:
        scripts_root = pipeline_root.parent / "scripts"
    return skills_root, scripts_root

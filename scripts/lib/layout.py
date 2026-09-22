"""Install-layout resolution: repo checkout vs wheel install.

The distribution maps repo trees into import packages (see pyproject.toml):

- repo checkout: this file lives at <repo>/scripts/lib/layout.py, the skills
  tree at <repo>/skills, the top-level scripts at <repo>/scripts.
- wheel install: this file lives at <site-packages>/wiki_scripts/lib/layout.py;
  pyproject maps the skills/ tree in as `wiki_scripts.skills` package data, so
  the installed `wiki_scripts` directory is layout-complete — it IS the
  scripts root and contains skills/ beside the script modules.

Callers use `find_roots()` instead of `Path(__file__).parent.parent`-style
bootstrapping, which silently points into site-packages when installed.
"""

from __future__ import annotations

from pathlib import Path

# Local-KB-first convention: knowledge outputs live under the local KB, never
# in the package. (Same default as serve_research_wiki.DEFAULT_KB_ROOT.)
DEFAULT_KB_ROOT = Path.home() / "Documents" / "arxiv"


def find_roots() -> tuple[Path | None, Path, Path]:
    """Return (repo_root_or_None, skills_root, scripts_root).

    Repo checkout is detected by the pyproject.toml two levels up from this
    file (scripts/lib/layout.py). Editable installs resolve here too, which is
    correct — they run against the checkout. Anything else is a wheel install
    where the wiki_scripts package dir holds both the scripts and the bundled
    skills tree.
    """
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    if (repo_root / "pyproject.toml").is_file():
        return repo_root, repo_root / "skills", repo_root / "scripts"
    pkg_dir = here.parents[1]
    return None, pkg_dir / "skills", pkg_dir


def default_kb_root() -> Path:
    """Canonical local KB root for new environments (override per-call with
    --kb-root; serve_research_wiki keeps its own DEFAULT_KB_ROOT constant)."""
    return DEFAULT_KB_ROOT

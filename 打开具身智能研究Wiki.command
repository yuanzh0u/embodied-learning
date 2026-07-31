#!/bin/zsh
cd -- "$(dirname -- "$0")" || exit 1
exec python3 scripts/serve_research_wiki.py --open

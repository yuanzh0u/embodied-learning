# Local mirrors of CI unittest discovery (see .github/workflows/research-validation.yml).
# Stdlib-only: no install step. Run from the repository root.

PYTHON ?= python3

TEST_SUITES := \
	tests \
	skills/embodied-ai-query-planner/tests \
	skills/embodied-ai-literature-hub/tests \
	skills/embodied-ai-paper-reader/tests \
	skills/embodied-ai-literature-review/tests \
	skills/embodied-ai-review-writer/tests

.PHONY: help test test-knowledge validate

help:
	@echo "Targets:"
	@echo "  make test           - run the same unittest suites as research-validation CI"
	@echo "  make test-knowledge - run top-level tests/ only"
	@echo "  make validate       - run scripts/validate_current_reviews.py (needs full git history)"

test:
	@set -euo pipefail; \
	for suite in $(TEST_SUITES); do \
		echo "==> $(PYTHON) -m unittest discover -s $$suite -v"; \
		$(PYTHON) -m unittest discover -s $$suite -v; \
	done

test-knowledge:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) scripts/validate_current_reviews.py --root .

"""Central constants and review-mode default parameters.

Single home for the fixed vocabularies, mode tables and TUNABLE POLICY KNOBS
that used to be copy-pasted across modules (floors, stance caps, style
contracts, screen / deep-read limits, agent timeouts, extraction caps, lock
and retry budgets). Import from here — do not re-declare.

What belongs here: a number or table an operator would adjust (limits,
timeouts, thresholds, caps, budgets, pacing). What does NOT: compiled regexes,
tag sets, lookup tables that document structure, and path derivations — those
stay next to the code that interprets them.

Evidence discipline note: the floor numbers are part of the review contract
(rapid/scoping/systematic). Changing a value here changes every gate that
counts against it, so treat edits as contract changes (see docs/adr/0002).
"""

from __future__ import annotations

# ---- review modes ------------------------------------------------------------

REVIEW_MODES: tuple[str, ...] = ("rapid", "scoping", "systematic")

# Retrieval-strategy vocabulary (driver --search-strategy).
SEARCH_STRATEGIES: tuple[str, ...] = ("smart", "fast", "seeds")

# Deep-read queue selection vocabulary (driver --selection-strategy).
# ``keywords`` keeps the legacy term-matching screen-candidates path.
SELECTION_STRATEGIES: tuple[str, ...] = ("keywords", "influence", "bm25", "smart")

# Accepted-evidence floor per review mode (deep-read / evidence sufficiency).
EVIDENCE_FLOORS: dict[str, int] = {"rapid": 8, "scoping": 15, "systematic": 30}

# Distinct cited-paper floor per review mode (finalize gate).
CITED_PAPER_FLOORS: dict[str, int] = {"rapid": 6, "scoping": 10, "systematic": 15}

# Registry screen budget per review mode (driver screening stage). A
# runaway guard on extraction cost only — it must not cut a quality shortlist
# (2026-10-10: smart picked 68, cap 48, 20 never even reached extraction).
SCREEN_LIMITS: dict[str, int] = {"rapid": 80, "scoping": 120, "systematic": 200}

# Deep-read queue limit per review mode (driver deep-read stage). Deep-read
# throughput is the real review breadth (screening only triages). Sized so
# BOTH paper floors clear at the observed ~70% skeleton-audit pass rate:
# the cited-paper floor AND the evidence floor. When audited passes still
# fall short, the driver pulls 候补 from the scored extraction pool until the
# evidence floor is met.
DEEP_READ_LIMITS: dict[str, int] = {"rapid": 12, "scoping": 22, "systematic": 43}

# Soft deep-read budget offset above the evidence floor (check-deep-read-budget).
DEEP_READ_BUDGET_OFFSET: int = 10

# ---- writer contract ---------------------------------------------------------

# Settled-scope style -> deliverable file (the reduced-scope settle contract;
# mirrors check_run_bundle). `slide-deck` ships the compiled HTML; `survey` is
# the packet-only scope.
STYLE_TO_FILE: dict[str, str] = {
    "scientific-memo": "scientific-memo_keyan.md",
    "expert-explainer": "zhihu-explainer_zhihu.md",
    "kol-thread": "xiaohongshu-post_xiaohongshu.md",
    "slide-deck": "slide-deck_report.html",
    "survey": "review-packet.md",
}
STYLE_TO_ARTICLE: dict[str, str] = STYLE_TO_FILE

# The standard review triplet every full bundle ships (three prose faces).
STANDARD_ARTICLES: tuple[str, ...] = (
    "scientific-memo_keyan.md",
    "zhihu-explainer_zhihu.md",
    "xiaohongshu-post_xiaohongshu.md",
)

# Writer stance caps: max events per stance in the brief/appendix.
DEFAULT_WRITER_STANCE_CAPS: dict[str, int] = {
    "support": 8,
    "limit": 6,
    "conditional": 6,
    "gap": 4,
}

# ---- agent / network defaults -----------------------------------------------

TERMS_AGENT_TIMEOUT_S: float = 180.0
DYNAMIC_AGENT_TIMEOUT_S: float = 480.0
S2_BUDGET_S: float = 480.0
DEFAULT_AGENT_TIMEOUT_S: float = 900.0
DEFAULT_AGENTS_PARALLEL: int = 5
DEFAULT_EXTRACTION_WORKERS: int = 4
# One smart-selection chunk is ONE agent call judging up to
# SMART_CANDIDATES_PER_CALL abstracts; the 2026-10-14 时空智能体 run lost its
# whole older half (2024-01..2026-08) to a 900s chunk timeout, which then
# starved the full-text and accepted-paper floors. Keep this generous.
SELECTION_TIMEOUT_S: float = 3600.0

# ---- network: retry, pacing, circuit breaking -------------------------------

# Codes that extend the machine-wide cooldown (gated_urlopen).
TRANSIENT_HTTP_CODES: frozenset[int] = frozenset({429, 500, 502, 503, 504})

# Policy groups: one shared slot/cooldown file per group. arXiv's official
# politeness rate is 1 request / 3 s for API+export; S2 429s aggressively
# without an API key; arxiv2md publishes 30 req/min per IP.
DEFAULT_INTERVALS: dict[str, float] = {
    "arxiv": 3.0,
    "semanticscholar": 1.0,
    "arxiv2md": 2.0,
}

# S2 request pacing passed to expand-via-citations (driver --sleep-seconds).
S2_SLEEP_S: float = 3.0

DEFAULT_RETRY_BASE_SECONDS: float = 20.0
DEFAULT_RETRY_CAP_SECONDS: float = 600.0
MAX_RETRIES: int = 3
LOCK_POLL_SECONDS: float = 0.05

# Consecutive connection-level failures before the extraction queue gives up
# on a dead channel instead of spending every paper's full budget on it.
CHANNEL_DOWN_LIMIT: int = 6

# ---- extraction caps ---------------------------------------------------------

MAX_TERM_MATCHES: int = 120
MAX_CITATION_CONTEXTS: int = 200
MAX_REFERENCE_HINTS: int = 80
MAX_EXTRACT_BYTES: int = 512 * 1024 * 1024
MAX_MEMBERS: int = 20000
MAX_WORKERS: int = 16
FETCH_TIMEOUT_S: float = 45.0
MAX_HTML_BYTES: int = 12_000_000
MAX_FILE_BYTES: int = 2_000_000
MAX_EXCERPT_CHARS: int = 300
DEFAULT_MAX_SECTION_CHARS: int = 4000

# ---- agent / chat timeouts ---------------------------------------------------

STOP_GRACE_S: float = 5.0
# Tool-call detail caps for the harness event stream (dialog journal + UI).
# ``command`` is the audit trail for "did the agent pass the right flags?" —
# 120 chars used to cut audit-citations invocations mid-flag and hide real
# flag-guessing retries (2026-10-15). Keep commands whole; path/URL-ish keys
# stay compact so the live status spinner remains readable.
TOOL_DETAIL_MAX_CHARS: int = 120
TOOL_COMMAND_DETAIL_MAX_CHARS: int = 2000
SKELETON_TIMEOUT_S: float = 900.0
ARTICLE_TIMEOUT_S: float = 600.0
SOURCE_TIMEOUT_S: float = 900.0
DEFAULT_CHAT_TIMEOUT_S: int = 1800
FIRST_EVENT_TIMEOUT_S: float = 240.0
MAX_HISTORY_MESSAGES: int = 40
MAX_PROMPT_CONTEXT_FILES: int = 40
WORKFLOW_AUTO_CONTINUE_ROUNDS: int = 2
WORKFLOW_MIN_TIMEOUT_S: float = 5400.0
WORKFLOW_DRIVER_TIMEOUT_S: float = 10800.0
# Subprocess budgets the wiki server wraps around its skill scripts (速读卡 /
# 汇报 deck / 论文对话准备). A timeout there kills the child and surfaces an
# error to the pane, so they are generous but bounded.
QUICKREAD_TIMEOUT_S: float = 1800.0
RUN_DECK_TIMEOUT_S: float = 1800.0
PAPER_DECK_TIMEOUT_S: float = 3600.0
PAPER_PREP_TIMEOUT_S: float = 2400.0
REFRESH_TIMEOUT_S: float = 300.0
INIT_RUN_TIMEOUT_S: float = 120.0
# Hard per-paper full-text extraction budget (queue entry point).
EXTRACTION_PAPER_TIMEOUT_S: float = 600.0
# Whole extraction-queue stage budget (the driver wraps it in one run_stage).
EXTRACTION_STAGE_TIMEOUT_S: float = 5400.0
# Citation-expansion (S2) round budget inside the driver.
CITATION_EXPANSION_TIMEOUT_S: float = 900.0

# ---- ranking / scoring knobs -------------------------------------------------

STANCE_SHARE_THRESHOLD: float = 0.20
MIN_EVENTS_FOR_STANCE_TRIGGER: int = 10
K1: float = 1.5  # BM25 term-frequency saturation
B: float = 0.75  # BM25 length normalisation
DEFAULT_FIELD_WEIGHTS: str = "title=2.0,abstract=1.0,introduction=1.5,related_work=1.5"
SMART_CANDIDATES_PER_CALL: int = 300
SMART_MAX_ABSTRACT_CHARS: int = 400
BATCH_MAX_IDS: int = 500
PAGE_SIZE: int = 100
DEFAULT_MAX_QUERIES: int = 50

# ---- writing budgets and caps -----------------------------------------------

FORMAL_SOURCE_THRESHOLD: int = 5
DEFAULT_LOOKBACK_MONTHS: int = 6
DEFAULT_MAX_CLAIM: int = 400
DEFAULT_MAX_SUMMARY: int = 320
DEFAULT_MAX_QUOTE: int = 220
# Per-style prose floors / hard warning ceilings / (min,max) link budgets.
LENGTH_FLOORS: dict[str, int] = {"memo": 1800, "zhihu": 1000, "quickread": 300, "xiaohongshu": 300}
LENGTH_CEILINGS: dict[str, int] = {"zhihu": 4500, "quickread": 1400, "xiaohongshu": 1400}
LINK_BUDGETS: dict[str, tuple[int, int | None]] = {
    "memo": (5, None),
    "zhihu": (3, 12),
    "xiaohongshu": (3, 5),
    "quickread": (1, 1),
}

# ---- slide / reader rendering caps ------------------------------------------

MIN_SLIDES: int = 5
MAX_BULLETS: int = 7
MAX_FIGS: int = 2
MAX_TABLES: int = 1
MAX_STATS: int = 4
REFS_PER_PAGE: int = 27
BODY_PREVIEW_LIMIT: int = 20000
MAX_JSONL_RECORDS: int = 200

# ---- shared-KB lock policy ---------------------------------------------------
# The KB may live on a flaky CIFS share; these are the O_EXCL lock's patience
# knobs (see scripts/README.md 「共享知识库的并发与锁」).
STEAL_MARKER_MAX_AGE: float = 60.0
PROGRESS_EVERY: float = 10.0
DEFAULT_WAIT: float = 120.0
DEFAULT_STALE: float = 900.0
DEFAULT_POLL: float = 1.0

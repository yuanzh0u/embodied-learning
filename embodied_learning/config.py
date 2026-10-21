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
# ``smart`` and ``smart-jev`` are the two model-driven variants: the first uses
# the execution model of the run (claude one-shot), the second a decision model
# (System One / jev) through the harness's second binding.
SELECTION_STRATEGIES: tuple[str, ...] = ("keywords", "influence", "bm25", "smart", "smart-jev")

# Default deep-read queue selection. ``smart-jev`` is the decision model: it
# answers one typed per-paper question in seconds instead of spending minutes
# on an execution-model pass, and the strict "core contribution" wording keeps
# precision at ~80% at threshold 0.60 (2026-10-20 A/B, 455 candidates).
# It fails fast when the System One channel is unconfigured; ``smart`` (the
# execution model) stays available as the explicit fallback.
DEFAULT_SELECTION_STRATEGY: str = "smart-jev"

# Accepted-evidence floor per review mode (deep-read / evidence sufficiency).
EVIDENCE_FLOORS: dict[str, int] = {"rapid": 8, "scoping": 15, "systematic": 30}

# Distinct cited-paper floor per review mode (finalize gate).
CITED_PAPER_FLOORS: dict[str, int] = {"rapid": 6, "scoping": 10, "systematic": 15}

# Deep-read queue limit per review mode (driver deep-read stage). This is the
# ONLY truncation in the funnel: selection queues every paper the strategy
# judges relevant and extraction recovers all of them (2026-10-20: the old
# SCREEN_LIMITS cap duplicated this cut and stranded 232 of 352 relevant
# papers before extraction). Deep-read throughput is the real review breadth
# (screening only triages). Sized so BOTH paper floors clear at the observed
# ~70% skeleton-audit pass rate: the cited-paper floor AND the evidence floor.
# It is a FIRST-PASS budget, not the stopping rule — when audited passes fall
# short, the driver pulls 候补 from the rest of the extracted queue until the
# evidence floor is met.
DEEP_READ_LIMITS: dict[str, int] = {"rapid": 12, "scoping": 22, "systematic": 43}

# Soft deep-read budget offset above the evidence floor (check-deep-read-budget).
DEEP_READ_BUDGET_OFFSET: int = 10

# Per-layer paper-id cap in funnel.json (runaway guard for a pathological
# registry). Truncation is recorded (``truncated: true``) and logged, never
# silent; normal runs sit far below it (largest observed registry: 308).
FUNNEL_LAYER_PAPER_CAP: int = 5000

# Per-query retrieval cap by review mode (search-arxiv --max-results, driver
# passes the mode's value). This is a *discovery* budget, not a corpus census:
# n_queries x this value is why every topic's initial retrieval lands near a
# few hundred papers. Retrieval is relevance-ranked (not newest-first), so a
# wider window surfaces seminal and highly-related work instead of just the
# latest submissions — raise the mode's value for a wider pool rather than
# piling on more queries.
SEARCH_MAX_RESULTS_PER_QUERY: dict[str, int] = {"rapid": 25, "scoping": 35, "systematic": 45}

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
# Total tries for the dynamic-query agent on parse/exit failures (a timeout
# does not retry: that budget is already spent). The completion channel
# occasionally truncates the response head or drops JSON quoting
# (2026-10-13/14/15 runs); a second call almost always lands.
DYNAMIC_AGENT_ATTEMPTS: int = 2
# Total tries for the deep-read skeleton agent on parse/exit failures AND
# timeouts. Deep reads run several agents concurrently, so an upstream stall
# under load frequently surfaces as a timeout rather than a clean error; the
# 2026-10-16 强化学习 run lost 20/43 deep reads to skeleton calls that died on
# truncated streams. One extra timeout budget per paper is the cheaper side of
# that trade (a retried paper costs ~2x one read; a lost paper costs evidence).
SKELETON_AGENT_ATTEMPTS: int = 2
# Whole-queue retry passes after the first deep-read pass: papers that still
# failed but DO have full text are re-read once more (transient upstream
# failures dominate under parallel load). Papers without an extraction are
# never retried here — the bottleneck is the fetch, not the model.
DEEP_READ_RETRY_PASSES: int = 1
S2_BUDGET_S: float = 480.0
DEFAULT_AGENT_TIMEOUT_S: float = 900.0
DEFAULT_AGENTS_PARALLEL: int = 5
DEFAULT_EXTRACTION_WORKERS: int = 4
# One smart-selection chunk is ONE agent call; chunks are packed by rendered
# candidate length (SMART_CANDIDATE_CHARS_PER_CALL). The 2026-10-14 时空智能体
# run lost its whole older half (2024-01..2026-08) to a 900s chunk timeout, which
# then starved the full-text and accepted-paper floors. Keep this generous.
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
    "mymemory": 1.0,
    # Decision-model (System One) traffic: 1200 req/min upstream, so a light
    # machine-wide spacing is plenty and keeps sibling runs from stampeding.
    "systemone": 0.25,
}

# S2 request pacing passed to expand-via-citations (driver --sleep-seconds).
S2_SLEEP_S: float = 3.0

# MyMemory bootstrap translation (pure-Chinese topic → English query terms).
TRANSLATE_TIMEOUT_S: float = 15.0
# Anonymous MyMemory requests cap q at 500 bytes; stay well under.
TRANSLATE_MAX_CHARS: int = 400

DEFAULT_RETRY_BASE_SECONDS: float = 20.0
# Cap on a 429/503 cooldown recorded machine-wide. Deliberately far below
# EXTRACTION_PAPER_TIMEOUT_S (600s): when both were 600 a single long
# ``Retry-After`` turned into a full per-paper hard timeout — every fetch
# worker blocked in the gate until the subprocess was killed (2026-10-20
# 视频流式重建 run: 5 papers x 600s, 4 of them recovered instantly on retry).
DEFAULT_RETRY_CAP_SECONDS: float = 120.0
MAX_RETRIES: int = 3
LOCK_POLL_SECONDS: float = 0.05

# How long one fetch may block in the machine-wide gate before giving up and
# letting the extraction queue's retry pass try again. Must stay below the
# per-paper extraction budget so a cooldown becomes a fast HELD (seconds),
# not a burned subprocess slot.
FETCH_GATE_MAX_WAIT_S: float = 60.0

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
# Why the agent made a mutating call (Edit/Write/...): the stream-json
# tool_use block carries no reason, so the harness attaches the narration
# text that preceded it. Without this the dialog journal shows "Edit：<path>"
# with no way to tell a style fix from a citation fix (2026-10-20 审计门).
TOOL_REASON_MAX_CHARS: int = 300
# Usage/trace ledger (monica usage-records-format): set to 0/false to disable.
# Every claude invocation writes one JSONL session file directly under the
# machine-local conversation store (``usage-<kind>-*.jsonl``). A parent process
# can point spawned stage scripts at its own run ledger with the env below, so
# subprocess agents append to the same file instead of opening a sibling.
AGENT_SESSION_LOG_ENV: str = "EMBODIED_AGENT_SESSION_LOG"
AGENT_SESSION_LEDGER_ENV: str = "EMBODIED_AGENT_LEDGER"
# Diagnostic event text cap in the ledger (no prompt/response bodies — D9).
SESSION_EVENT_TEXT_MAX_CHARS: int = 300
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
# Smart-selection chunk packing: bound ONE agent call by the rendered
# candidate-block size (primary) and by candidate count (secondary ceiling).
# Fixed-count chunks ignored how long abstracts actually run — the 2026-10-16
# 强化学习 run's two chunks (300 / 150 papers) rendered 157KB / 78KB prompts and
# BOTH lost their completion stream mid-response (upstream EOF after 44660 /
# 30074 frames). With SMART_MAX_ABSTRACT_CHARS applied a line runs ~500 chars,
# so 24k ≈ 45 papers: one call's prompt and generation stay short enough to
# land. The count ceiling only bites when lines are tiny (empty abstracts).
SMART_CANDIDATE_CHARS_PER_CALL: int = 24_000
SMART_CANDIDATES_PER_CALL: int = 60
SMART_MAX_ABSTRACT_CHARS: int = 400

# ---- decision model (System One / jev) selection ---------------------------
#
# ``smart-jev`` asks a decision model one typed yes/no question per candidate
# and keeps the papers whose probability clears a threshold. It is NOT a claude
# call: jev speaks TypeSafe's System One protocol, so the harness owns a second
# binding (harness/claude.system_one) beside complete(). One request carries
# many questions (the model answers them in one forward pass), which is why the
# whole registry fits in a handful of calls.
SYSTEM_ONE_MODEL: str = "jev-1.14.0"
# Endpoint is ``<base>/v1/systemone``; the base URL and the key are read from
# the environment ONLY (never written to config): the repo's own vars first,
# then the gateway vars the claude CLI already uses.
SYSTEM_ONE_ENDPOINT_SUFFIX: str = "/v1/systemone"
SYSTEM_ONE_URL_ENV: str = "EMBODIED_SYSTEM_ONE_URL"
SYSTEM_ONE_KEY_ENV: str = "EMBODIED_SYSTEM_ONE_API_KEY"
SYSTEM_ONE_URL_FALLBACK_ENVS: tuple[str, ...] = ("ANTHROPIC_BASE_URL",)
SYSTEM_ONE_KEY_FALLBACK_ENVS: tuple[str, ...] = ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY")
# One request carries up to SMART_JEV_QUESTIONS_PER_CALL questions; the char
# budget below keeps the request body inside System One's 32k state+question cap.
SMART_JEV_QUESTIONS_PER_CALL: int = 60
SMART_JEV_CHARS_PER_CALL: int = 24_000
# Keep a candidate when the Noul probability clears this. 0.60 measured
# precision 0.88 / recall 0.73 against the smart (glm) baseline on the 455-
# candidate 视频流式重建 registry (2026-10-20); lower = more recall, more drift.
SMART_JEV_RELEVANCE_THRESHOLD: float = 0.60
SYSTEM_ONE_TIMEOUT_S: float = 120.0
SYSTEM_ONE_RETRIES: int = 2
SYSTEM_ONE_BACKOFF_BASE: float = 1.5
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
# Zhihu long-sentence gate. The audit reports EVERY sentence over the limit in
# one pass (longest first): reporting only the single longest made the writer
# whack one mole per round — fix the 93-char sentence and the 76-char one takes
# its place, five audit rounds later the draft still had one at 72 (2026-10-20
# 视频流式重建). The cap keeps one audit message readable; the message names
# how many it withheld.
LONG_SENTENCE_MAX_CHARS: int = 70
LONG_SENTENCE_REPORT_LIMIT: int = 8

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

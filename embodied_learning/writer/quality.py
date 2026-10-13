"""Audit editorial quality signals for an embodied-AI review bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
from pathlib import Path
from embodied_learning.config import LENGTH_CEILINGS, LENGTH_FLOORS, LINK_BUDGETS


EVENT_ID_RE = re.compile(r"\b(?:EA|ERR)-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{4}\b")
ARXIV_LINK_RE = re.compile(r"https?://arxiv\.org/abs/\d{4}\.\d{4,5}(?:v\d+)?")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
LATIN_RE = re.compile(r"[A-Za-z]")
ACRONYM_RE = re.compile(r"(?<![A-Za-z])[A-Z][A-Z0-9-]{1,}(?![A-Za-z])")

# Single source of the per-style required-section contract: style ->
# {rule: (heading regex, human-readable hint)}. audit_file enforces it (the
# failure message carries the hint so a failing draft names its own fix), and
# build_review_packet renders it into the writing brief so the writer's FIRST
# draft can satisfy the gate instead of learning it by failing.
REQUIRED_SECTIONS: dict[str, dict[str, tuple[str, str]]] = {
    "memo": {
        "boundary": (r"^## .*?(研究边界|研究范围)", '以 "## 研究边界…" 或 "## 研究范围…" 开头的节'),
        "thesis": (r"^## .*?(中心判断|核心结论|中心论点)", '标题含 中心判断/核心结论/中心论点 的 "##" 节'),
        "limits": (r"^## .*?(条件|分歧|边界|限制|局限|空白)", '标题含 条件/分歧/边界/限制/局限/空白 的 "##" 节'),
        "ending": (r"^## .*?(结论|启发|下一步)", '标题含 结论/启发/下一步 的 "##" 节'),
    },
    "zhihu": {
        "tldr": (r"^## TL;DR", '以 "## TL;DR" 开头的节'),
        "misconception": (
            r"^#{2,3}\s+.*(?:误区|直觉.*(?:失灵|误判)|为什么.*(?:容易|会).*误判|问题从哪来)",
            '标题含 误区/直觉失灵/为什么容易误判/问题从哪来 的 "##"/"###" 节',
        ),
        "mechanism": (
            r"^#{2,3}\s+.*(?:机制|问题.*(?:出在哪|在哪里)|为什么.*(?:失败|失效)|因果链|真正发生)",
            '标题含 机制/问题出在哪/为什么失效/因果链/真正发生 的 "##"/"###" 节',
        ),
        "boundary": (r"^## .*?(边界|什么时候.*不成立|限制)", '标题含 边界/什么时候不成立/限制 的 "##" 节'),
    },
    "quickread": {
        "positioning": (r"^## .*?一句话定位", '以 "## …一句话定位" 开头的节'),
        "method": (r"^## .*?方法步骤", '以 "## …方法步骤" 开头的节'),
        "limits": (r"^## .*?局限与边界", '以 "## …局限与边界" 开头的节'),
    },
    "xiaohongshu": {},  # 结构门替代必需节：💡×3-5 + ⚠️ caveat（见 STRUCTURE_GATES）
}

# Styles with no required heading sections but hard structural gates, as
# human-readable hints for the brief. audit_file enforces these inline per style.
STRUCTURE_GATES: dict[str, tuple[str, ...]] = {
    "xiaohongshu": ("3-5 个行首 💡 洞察行", "至少一个行首 ⚠️ 注意事项行"),
}

# Chinese-character floors/ceilings and arXiv-link budgets per style: shared
# by audit_file and build_review_packet's writing-brief contract section.
# ---- rule registry: the single source of truth --------------------------
# Every audit rule registers here with the contract line the WRITER is shown.
# audit_file() emits findings tagged with these ids; render_style_contract()
# renders the same registry into the writing brief. One edit propagates to
# both — the point of this table.
#
# It exists because the two used to be hand-maintained apart: a newly added
# error gate (chinese-share) was enforced by the audit but never rendered into
# the brief, so the writer optimized for the seven rules it could see and then
# failed on the one it could not (2026-10-09, first-draft churn). A rule id
# emitted by audit_file() that is missing here, or an error rule here that the
# contract render skips, is a test failure.
#
# `spec` is the Chinese contract line, written as an instruction (not a
# restatement of the regex): the writer must be able to comply without
# reverse-engineering the gate. Keep thresholds in sync with the checks below.


class RuleSpec:
    __slots__ = ("id", "severity", "scope", "spec")

    def __init__(self, rule_id: str, severity: str, scope: tuple[str, ...], spec: str):
        self.id = rule_id
        self.severity = severity          # "error" | "warning"
        self.scope = scope                # ("all",) or style keys: memo/zhihu/xiaohongshu/quickread
        self.spec = spec                  # contract line shown to the writer

    def applies_to(self, style_key: str) -> bool:
        return "all" in self.scope or style_key in self.scope


def _r(rule_id: str, severity: str, scope: tuple[str, ...], spec: str) -> RuleSpec:
    return RuleSpec(rule_id, severity, scope, spec)


_ALL = ("all",)
_MEMO = ("memo",)
_ZHIHU = ("zhihu",)
_XHS = ("xiaohongshu",)
_QR = ("quickread",)

RULE_SPECS: dict[str, RuleSpec] = {
    spec.id: spec
    for spec in (
        # ---- language / provenance (every style) ----
        _r("file-exists", "error", _ALL, "成稿文件必须真实写入运行目录根（不是草稿区、不是 .scaffold.md）。"),
        _r(
            "chinese-share", "error", _ALL,
            "可见散文的中文占比至少 65%（按字数；论文标题、arXiv 链接、事件 ID 已从计数中剔除）。"
            "英文术语首次出现给一句中文释义后改用中文说法，别让专有名词和英文短句把占比拉下去——"
            "写完自己数一遍再交，这是一票否决。",
        ),
        _r("event-ids-in-body", "error", _ALL, "正文不得出现 EA-*/ERR-* 事件 ID；事件锚点只存在于 trace-map 与 evidence-appendix。"),
        _r("canned-phrase", "error", _ALL, "不得使用脚手架套话（如「本文综述了」「随着…的发展」这类模板句）。"),
        _r("packet-leak", "error", _ALL, "不得泄入 review-packet / writing-brief / scaffold 的标记、栏目名或内部标题。"),
        _r("internal-prose", "error", _ALL, "不得出现面向审计/写作过程的内部措辞、stance 标签（support/limit/…）或「证据锚点」这类词。"),
        _r("internal-reasoning-label", "error", _ALL, "不得留下推理标签（如「论点」「证据」「反例」这类自述式小标题）。"),
        _r("missing-citation-subject", "error", _ALL, "每处引用必须点明论文主体（谁做的、什么方法），不能只给链接或只给编号。"),
        _r("generic-citation-anchor", "error", _ALL, "不得用「某研究表明」「相关工作显示」这类无主语引用。"),
        _r("chatbot-artifact", "error", _ALL, "不得留下对话残留（「好的」「以下是」「希望这对你有帮助」）。"),
        _r("duplicate-prose", "error", _ALL, "不得整段重复同一句实质性散文；三种风格是三个声音，不是同一份稿子复制。"),
        _r("empty-reading-note", "error", _ALL, "注释式书目每条都要有一句读者价值注记，不得留空。"),
        _r("malformed-prose", "error", _ALL, "不得有空引文槽、连续标点（。。，，）或生成残缺的句读。"),
        _r("placeholder", "error", _ALL, "不得留未替换占位符（TBD、XXX、<待填>、TODO）。"),
        # ---- memo ----
        _r("memo-length", "error", _MEMO, "科研备忘录正文至少 1800 个中文字符。"),
        _r("memo-grouped-citation", "error", _MEMO, "严禁 ^[1,2]^ 这类合并上标；多条引用逐条并列 ^[1]^ ^[2]^。"),
        _r("memo-inline-arxiv-link", "warning", _MEMO, "正文用上标 ^[n]^ 而非内联 arXiv 链接；arXiv 链接只在文末 References。"),
        _r("memo-superscript-citations", "warning", _MEMO, "正文至少 5 处上标 ^[n]^ 引用标记（每处一条引用）。"),
        # ---- zhihu ----
        _r("zhihu-length", "error", _ZHIHU, "知乎科普正文至少 1000 个中文字符（地板不是上限；过短=过度压缩）。"),
        _r("unannotated-reading-list", "error", _ZHIHU, "「延伸阅读」每条链接都要附一句读者价值注记，不能是纯书目堆砌。"),
        _r("acronym-load", "warning", _ZHIHU, "正文领域缩写不超过 5 个，首次出现给一句人话解释。"),
        _r("long-sentence", "warning", _ZHIHU, "单句不超过 70 个中文字符（长句拆从句，降推断负载）。"),
        _r("body-citation-load", "warning", _ZHIHU, "正文内嵌引用控制在 3–12 篇；支撑性覆盖挪进「延伸阅读」注记。"),
        # ---- xiaohongshu ----
        _r("xiaohongshu-length", "error", _XHS, "小红书正文至少 300 个中文字符，至多 1400。"),
        _r("insight-count", "error", _XHS, "3–5 个行首 💡 洞察行，且至少一个行首 ⚠️ 注意事项行。"),
        _r("visible-caveat", "error", _XHS, "至少一条限制/反证必须在正文可见（不能只藏在附录）。"),
        # ---- quick-read card ----
        _r("quickread-length", "error", _QR, "速读卡正文至少 300 个中文字符，至多 1400。"),
        _r("quickread-table", "warning", _QR, "速读卡允许一张要点表，但正文仍须是连贯散文。"),
        # ---- cross-style / provenance ----
        _r("source-share", "error", _ALL, "来源行（References/出处行）占比受控：正文必须是论证散文，不是引文清单。"),
        _r("source-selection", "error", _ALL, "引用源须经选择（代表工作 + 反例），不是把证据集全部罗列。"),
        _r("citation-density", "warning", _ALL, "引用密度与篇幅匹配；避免一两句一引或通篇无引。"),
        _r("figures-available", "warning", _ALL, "证据带图而正文未落图时给出解释；可用图表见 brief 的「可用图表」段。"),
        # ---- tone warnings ----
        _r("generic-uplift", "warning", _ALL, "不得使用空泛正向断言（「具有重要意义」「前景广阔」）。"),
        _r("vague-attribution", "warning", _ALL, "不得用「有学者认为」「业内普遍」这类无名权威。"),
        _r("promotional-prose", "warning", _ALL, "不得使用推广腔（「强烈推荐」「值得关注」）。"),
        _r("truncation", "warning", _ALL, "可见散文不得出现三点式截断（…）表示未写完。"),
    )
}

CANNED_PHRASES = [
    "不能只看一个漂亮结论",
    "真正值钱的信息藏在证据条件里",
    "把候选论文、项目页或社交讨论当成正文级证据",
    "Strong hook is allowed",
    "Treat support, conditional, limit, and gap events as separate signals",
    "Formal scientific, expert-explainer, and KOL outputs are allowed",
    "No immediate source gaps detected from loaded packet inputs",
]

CHATBOT_ARTIFACTS = [
    "希望这对你有帮助",
    "希望这对您有帮助",
    "如果你想让我",
    "如果您想让我",
    "如果需要我可以继续",
    "您说得完全正确",
    "你说得完全正确",
    "下面让我们",
    "接下来让我们",
    "让我们深入探讨",
]

GENERIC_UPLIFT_PATTERNS = [
    re.compile(r"未来(?:看起来)?(?:一片)?光明"),
    re.compile(r"前景(?:十分|非常|依然|仍然)?可期"),
    re.compile(r"激动人心的(?:时代|时刻)"),
    re.compile(r"(?:迈出|迈出了).{0,8}(?:重要|关键)一步"),
    re.compile(r"继续(?:踏上|追求).{0,8}(?:卓越|旅程)"),
    re.compile(r"让我们(?:拭目以待|共同期待)"),
]

INTERNAL_PROSE_MARKERS = [
    "随附证据附录",
    "相关知识单元",
    "相关证据文件",
    "已接纳证据",
    "source-entry:",
    "formal-ready",
    "formal review 阈值",
    "trace:",
    "inference；",
    "综合推断：",
    "领域背景：",
]

INTERNAL_REASONING_LABEL_RE = re.compile(
    r"(?:[（(]\s*inference\s*[）)])|(?:\binference\s*[:：;；])|(?:synthesized from evidence events)",
    flags=re.IGNORECASE,
)

MALFORMED_PUNCTUATION_RE = re.compile(r"。。|，，|；；|：：|[.,，]\s*。|。\s*[.,]")

MISSING_CITATION_SUBJECT_RE = re.compile(
    r"(?:但|而|与|和)\s+的\s+(?:(?:[A-Za-z][A-Za-z0-9-]*)\s+)?(?:实验|研究|结论|方法|架构|论文)"
)

PACKET_MARKERS = [
    "## Evidence Core",
    "## Claim Map",
    "## Source Gaps",
    "### 共识/正向证据",
    "### 条件成立",
    "### 限制与失败模式",
    "- Output type:",
    "- Stance labels:",
    "- Confidence labels:",
    "- Trace IDs:",
]

PROMOTIONAL_PATTERNS = [
    re.compile(r"令人叹为观止"),
    re.compile(r"充满活力的"),
    re.compile(r"无缝(?:衔接|体验)"),
    re.compile(r"不断演变的.{0,12}格局"),
    re.compile(r"持久的证明"),
]

VAGUE_ATTRIBUTION_PATTERNS = [
    re.compile(r"(?:行业专家|业内人士|专家们?|观察者|多位专家)(?:普遍)?(?:认为|指出|表示)"),
    re.compile(r"有观点认为"),
]

# Every id audit_file() can emit must be registered above. Kept as a flat
# tuple so a source-level drift test can compare cheaply.
RULE_IDS: tuple[str, ...] = tuple(RULE_SPECS)

# The three prose deliverables this audit covers: filename -> the audit style
# its rules run under.
STANDARD_TARGETS: tuple[tuple[str, str], ...] = (
    ("scientific-memo_keyan.md", "memo"),
    ("zhihu-explainer_zhihu.md", "zhihu"),
    ("xiaohongshu-post_xiaohongshu.md", "xiaohongshu"),
)

# Reduced-scope settle contract (run.json `style`) -> the one prose file this
# audit covers for it. slide-deck / survey ship non-prose artifacts (compiled
# HTML, the mechanical packet) and are outside the editorial audit.
REDUCED_STYLE_TARGETS: dict[str, tuple[str, str]] = {
    "scientific-memo": ("scientific-memo_keyan.md", "memo"),
    "expert-explainer": ("zhihu-explainer_zhihu.md", "zhihu"),
    "kol-thread": ("xiaohongshu-post_xiaohongshu.md", "xiaohongshu"),
}




@dataclass
class Finding:
    severity: str
    file: str
    rule: str
    message: str


def strip_source_tail(text: str, style: str) -> str:
    markers = ["\n## References"]
    if style == "zhihu":
        markers.append("\n## 延伸阅读")
    if style == "xiaohongshu":
        markers.extend(["\n📚", "\n## 依据来源", "\n## References"])
    positions = [text.find(marker) for marker in markers if text.find(marker) >= 0]
    return text[: min(positions)] if positions else text


def linguistic_text(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"https?://\S+", "", text)
    text = EVENT_ID_RE.sub("", text)
    return text


def chinese_share(text: str) -> float:
    # Paper titles are citation metadata rather than narrative prose. Counting
    # long English titles against a Chinese article makes the language gate
    # depend on citation style instead of the language used by the author.
    text = re.sub(r"\[[^\]]+\]\([^\)]+\)", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = EVENT_ID_RE.sub("", text)
    chinese = len(CHINESE_RE.findall(text))
    latin = len(LATIN_RE.findall(text))
    return chinese / max(1, chinese + latin)


def chinese_count(text: str) -> int:
    return len(CHINESE_RE.findall(linguistic_text(text)))


def longest_chinese_sentence(text: str) -> int:
    sentences = re.split(r"[。！？!?；;\n]+", linguistic_text(text))
    return max((len(CHINESE_RE.findall(sentence)) for sentence in sentences), default=0)


def longest_chinese_sentence_text(text: str) -> str:
    """The longest Chinese sentence itself (trimmed), so the long-sentence
    warning names the exact text the writer must Edit — no inline-python
    sentence hunt (2026-09-30 absolute-pose burned ~8 calls finding it)."""
    sentences = re.split(r"[。！？!?；;\n]+", linguistic_text(text))
    if not sentences:
        return ""
    longest = max(sentences, key=lambda s: len(CHINESE_RE.findall(s)))
    return " ".join(longest.split())


def domain_acronyms(text: str) -> list[str]:
    return sorted(set(ACRONYM_RE.findall(linguistic_text(text))) - {"TL", "DR"})


def normalized_substantive_lines(text: str, style: str) -> set[str]:
    body = strip_source_tail(text, style)
    lines: set[str] = set()
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or len(line) < 24:
            continue
        line = re.sub(r"\[[^\]]+\]\([^\)]+\)", "", line)
        line = re.sub(r"[`*_>#💡⚠️📚]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) >= 24:
            lines.add(line)
    return lines


def normalized_body(text: str, style: str) -> str:
    body = strip_source_tail(text, style)
    body = re.sub(r"\[[^\]]+\]\([^\)]+\)", "", body)
    body = re.sub(r"^#+\s+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\s+", "", body)
    return body


def duplicate_prose_blocks(text: str) -> list[str]:
    normalized: list[str] = []
    for raw in re.split(r"\n\s*\n", text):
        block = raw.strip()
        if not block or block.startswith("#"):
            continue
        block = linguistic_text(block)
        block = re.sub(r"[`*_>#💡⚠️📚|•-]", "", block)
        block = re.sub(r"\s+", "", block)
        if len(block) >= 40:
            normalized.append(block)
    counts = Counter(normalized)
    return [block for block, count in counts.items() if count > 1]


def source_line_share(text: str) -> float:
    lines = [line for line in text.splitlines() if line.strip()]
    start = len(lines)
    for index, line in enumerate(lines):
        if line.strip() in {"## References", "## 依据来源"} or line.lstrip().startswith("📚"):
            start = index
            break
    return (len(lines) - start) / max(1, len(lines))


def zhihu_reading_list_findings(text: str) -> tuple[int, int]:
    heading = re.search(r"^##\s+(?:延伸阅读|References)\s*$", text, flags=re.MULTILINE)
    if not heading:
        return 0, 0
    tail = text[heading.end() :]
    linked_bullets = [
        line.strip()
        for line in tail.splitlines()
        if re.match(r"^[-*]\s+", line.strip()) and ARXIV_LINK_RE.search(line)
    ]
    annotated = [
        line
        for line in linked_bullets
        if re.search(r"\]\([^)]*\)\s*[：:]\s*\S", line)
    ]
    return len(linked_bullets), len(annotated)


def add(findings: list[Finding], severity: str, path: Path, rule: str, message: str) -> None:
    findings.append(Finding(severity, str(path), rule, message))


def audit_file(path: Path, style: str, min_chinese_share: float) -> tuple[str, list[Finding]]:
    findings: list[Finding] = []
    if not path.is_file():
        add(findings, "error", path, "file-exists", "article file is missing")
        return "", findings
    text = path.read_text(encoding="utf-8")
    body = strip_source_tail(text, style)

    share = chinese_share(body)
    if share < min_chinese_share:
        add(findings, "error", path, "chinese-share", f"visible prose Chinese share {share:.0%} is below {min_chinese_share:.0%}")

    event_ids = sorted(set(EVENT_ID_RE.findall(body)))
    if event_ids:
        add(findings, "error", path, "event-ids-in-body", f"body exposes event IDs: {', '.join(event_ids[:5])}")

    for phrase in CANNED_PHRASES:
        if phrase in text:
            add(findings, "error", path, "canned-phrase", f"contains scaffold phrase: {phrase}")
    for marker in PACKET_MARKERS:
        if marker in text:
            add(findings, "error", path, "packet-leak", f"contains packet/scaffold marker: {marker}")
    for marker in INTERNAL_PROSE_MARKERS:
        if marker in text:
            add(findings, "error", path, "internal-prose", f"contains reader-facing internal/audit wording: {marker}")
    generic_citations = len(re.findall(r"相关研究", body))
    if generic_citations:
        add(
            findings,
            "error",
            path,
            "generic-citation-anchor",
            f"body contains {generic_citations} unresolved generic citation anchor(s): 相关研究",
        )
    reasoning_label = INTERNAL_REASONING_LABEL_RE.search(body)
    if reasoning_label:
        add(
            findings,
            "error",
            path,
            "internal-reasoning-label",
            f"body exposes an internal reasoning label: {reasoning_label.group(0)}",
        )
    missing_subject = MISSING_CITATION_SUBJECT_RE.search(body)
    if missing_subject:
        add(
            findings,
            "error",
            path,
            "missing-citation-subject",
            f"body contains a high-confidence missing citation subject: {missing_subject.group(0)}",
        )
    for phrase in CHATBOT_ARTIFACTS:
        if phrase in body:
            add(findings, "error", path, "chatbot-artifact", f"contains conversational assistant residue: {phrase}")
    for pattern in GENERIC_UPLIFT_PATTERNS:
        match = pattern.search(body)
        if match:
            add(findings, "warning", path, "generic-uplift", f"contains a generic positive claim: {match.group(0)}")
    for pattern in VAGUE_ATTRIBUTION_PATTERNS:
        match = pattern.search(body)
        if match:
            add(findings, "warning", path, "vague-attribution", f"contains an unnamed authority claim: {match.group(0)}")
    for pattern in PROMOTIONAL_PATTERNS:
        match = pattern.search(body)
        if match:
            add(findings, "warning", path, "promotional-prose", f"contains promotional wording: {match.group(0)}")
    duplicates = duplicate_prose_blocks(body)
    if duplicates:
        add(findings, "error", path, "duplicate-prose", f"contains {len(duplicates)} exactly repeated substantive prose block(s)")
    if re.search(r"\bstance\s*:", body, flags=re.IGNORECASE):
        add(findings, "error", path, "internal-prose", "body exposes a stance label")
    if re.search(r"^-\s*—", text, flags=re.MULTILINE):
        add(findings, "error", path, "empty-reading-note", "contains an empty annotated-reading bullet")
    if "()" in text or "、、、" in text or re.search(r",\s*,?\s*\.", text) or MALFORMED_PUNCTUATION_RE.search(text):
        add(findings, "error", path, "malformed-prose", "contains empty citation slots or malformed generated punctuation")
    if "[TODO" in text or "<claim" in text or "<topic>" in text:
        add(findings, "error", path, "placeholder", "contains an unresolved placeholder")
    if "..." in body:
        add(findings, "warning", path, "truncation", "visible prose contains three-dot truncation")

    zh_count = chinese_count(body)
    if style == "memo":
        if zh_count < LENGTH_FLOORS["memo"]:
            add(findings, "error", path, "memo-length", f"memo has only {zh_count} Chinese characters before references; expected at least {LENGTH_FLOORS['memo']}")
        # Citation format contract: the wiki renders ^[n]^ superscripts into
        # clickable reading links via the References list — inline arXiv links
        # in the body break that rendering (2026-09-18 regression on both
        # headless ego runs). Severity stays "warning" here so pre-contract
        # settled runs still pass validate_current_reviews; the launcher gate
        # upgrades these rule IDs to hard failures for newly written runs.
        inline_arxiv = ARXIV_LINK_RE.findall(body)
        if inline_arxiv:
            add(
                findings,
                "warning",
                path,
                "memo-inline-arxiv-link",
                f"memo body has {len(inline_arxiv)} inline arXiv link(s); cite with superscript markers ^[1]^"
                " (one marker per citation, never ^[1,2]^) and list arXiv links only under References",
            )
        superscripts = len(re.findall(r"\^\[\d+\]\^", body))
        if superscripts < 5:
            add(
                findings,
                "warning",
                path,
                "memo-superscript-citations",
                f"memo body has only {superscripts} superscript citation marker(s) ^[n]^; expected at least 5"
                " (each citation carries its own bracketed marker)",
            )
        grouped = [marker for marker in re.findall(r"\^\[[\d,\s]+\]\^", body) if "," in marker]
        if grouped:
            add(
                findings,
                "error",
                path,
                "memo-grouped-citation",
                f"memo body groups multiple numbers into one marker ({', '.join(grouped[:3])});"
                " write consecutive markers ^[1]^ ^[2]^ instead of ^[1,2]^",
            )
    elif style == "zhihu":
        if zh_count < LENGTH_FLOORS["zhihu"]:
            add(findings, "error", path, "zhihu-length", f"Zhihu body has only {zh_count} Chinese characters; expected at least {LENGTH_FLOORS['zhihu']}")
        elif zh_count < 1800:
            add(
                findings,
                "warning",
                path,
                "zhihu-length",
                f"Zhihu body has {zh_count} Chinese characters; review for over-compression against the 1800-character explanation target",
            )
        elif zh_count > LENGTH_CEILINGS["zhihu"]:
            add(
                findings,
                "warning",
                path,
                "zhihu-length",
                f"Zhihu body has {zh_count} Chinese characters; review whether the explanation can stay below {LENGTH_CEILINGS['zhihu']}",
            )
        acronyms = domain_acronyms(body)
        if len(acronyms) > 5:
            add(
                findings,
                "warning",
                path,
                "acronym-load",
                f"Zhihu body uses {len(acronyms)} domain acronyms; review first-use explanations and reader memory load: {', '.join(acronyms[:10])}",
            )
        longest_sentence = longest_chinese_sentence(body)
        if longest_sentence > 70:
            offender = longest_chinese_sentence_text(body)
            add(
                findings,
                "warning",
                path,
                "long-sentence",
                f"Zhihu body contains a sentence with {longest_sentence} Chinese characters; review clauses and inference load above 70"
                + (f" — 待修句：{offender}" if offender else ""),
            )
        body_sources = set(ARXIV_LINK_RE.findall(body))
        if len(body_sources) >= 10:
            add(
                findings,
                "warning",
                path,
                "body-citation-load",
                f"Zhihu body cites {len(body_sources)} unique papers; review whether supporting coverage belongs in annotated further reading",
            )
        reading_items, annotated_items = zhihu_reading_list_findings(text)
        if reading_items < 3 or annotated_items != reading_items:
            add(
                findings,
                "error",
                path,
                "unannotated-reading-list",
                f"Zhihu further reading has {reading_items} linked bullet(s), {annotated_items} with reader-value annotations; expected at least 3 and every item annotated",
            )
    elif style == "quickread":
        if zh_count < LENGTH_FLOORS["quickread"]:
            add(findings, "error", path, "quickread-length", f"Quick-read card has only {zh_count} Chinese characters; expected at least {LENGTH_FLOORS['quickread']}")
        elif zh_count > LENGTH_CEILINGS["quickread"]:
            add(findings, "warning", path, "quickread-length", f"Quick-read card has {zh_count} Chinese characters; consider tightening below {LENGTH_CEILINGS['quickread']}")
        if re.search(r"^\|.*\|", text, flags=re.MULTILINE):
            add(findings, "warning", path, "quickread-table", "card contains a table row; the wiki inline reader cannot render tables")
    else:
        if zh_count < LENGTH_FLOORS["xiaohongshu"]:
            add(findings, "error", path, "xiaohongshu-length", f"Xiaohongshu body has only {zh_count} Chinese characters; expected at least {LENGTH_FLOORS['xiaohongshu']}")
        if zh_count > LENGTH_CEILINGS["xiaohongshu"]:
            add(findings, "warning", path, "xiaohongshu-length", f"Xiaohongshu body has {zh_count} Chinese characters; consider tightening below {LENGTH_CEILINGS['xiaohongshu']}")
        insight_count = len(re.findall(r"^\s*💡", body, flags=re.MULTILINE))
        if not 3 <= insight_count <= 5:
            add(findings, "error", path, "insight-count", f"expected 3-5 visible 💡 insights, found {insight_count}")
        if not re.search(r"^\s*⚠️", body, flags=re.MULTILINE):
            add(findings, "error", path, "visible-caveat", "missing a visible ⚠️ caveat")
        ref_share = source_line_share(text)
        if ref_share > 0.20:
            add(findings, "error", path, "source-share", f"source/reference material occupies {ref_share:.0%} of non-empty lines; maximum is 20%")

    for rule, (pattern, hint) in REQUIRED_SECTIONS.get(style, {}).items():
        if not re.search(pattern, text, flags=re.MULTILINE):
            add(findings, "error", path, f"section-{rule}", f"missing required {style} section: {rule}（{hint}）")

    unique_links = set(ARXIV_LINK_RE.findall(text))
    minimum_links, maximum_links = LINK_BUDGETS[style]
    if len(unique_links) < minimum_links:
        add(
            findings,
            "error",
            path,
            "source-selection",
            f"{style} cites only {len(unique_links)} unique arXiv papers; expected at least {minimum_links}",
        )
    if maximum_links is not None and len(unique_links) > maximum_links:
        add(
            findings,
            "error" if style in {"xiaohongshu", "quickread"} else "warning",
            path,
            "source-selection",
            f"{style} cites {len(unique_links)} unique arXiv papers; maximum reader-facing budget is {maximum_links}",
        )

    links = len(ARXIV_LINK_RE.findall(body))
    paragraphs = len([item for item in re.split(r"\n\s*\n", body) if item.strip() and not item.lstrip().startswith("#")])
    if paragraphs and links / paragraphs > {"memo": 2.5, "zhihu": 1.5, "xiaohongshu": 1.2, "quickread": 1.0}[style]:
        add(findings, "warning", path, "citation-density", f"body has {links} arXiv links across {paragraphs} prose blocks")

    return text, findings


def overlap_findings(memo_path: Path, memo: str, zhihu_path: Path, zhihu: str) -> list[Finding]:
    findings: list[Finding] = []
    memo_lines = normalized_substantive_lines(memo, "memo")
    zhihu_lines = normalized_substantive_lines(zhihu, "zhihu")
    exact = len(memo_lines & zhihu_lines) / max(1, min(len(memo_lines), len(zhihu_lines)))
    if exact > 0.25:
        add(findings, "error", zhihu_path, "cross-style-overlap", f"exact substantive-line overlap with memo is {exact:.0%}; maximum is 25%")
    similarity = SequenceMatcher(None, normalized_body(memo, "memo"), normalized_body(zhihu, "zhihu")).ratio()
    if similarity > 0.55:
        add(findings, "warning", zhihu_path, "cross-style-similarity", f"normalized body similarity with memo is {similarity:.0%}")
    return findings


def evidence_visual_event_count(path: str | None) -> int:
    """Number of evidence events carrying figures[]/tables[]."""
    if not path:
        return 0
    count = 0
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                evidence = event.get("evidence") or {}
                if not isinstance(evidence, dict):
                    continue
                if any(isinstance(evidence.get(key), list) and evidence.get(key) for key in ("figures", "tables")):
                    count += 1
    except OSError:
        return 0
    return count


def figures_available_findings(
    labeled: list[tuple[str, Path, str]], visual_events: int, findings: list[Finding]
) -> None:
    """Warning (never error): the evidence carries figures but a style draft
    embeds none — expressiveness gap, not a correctness failure (some topics
    legitimately have no usable figures)."""
    if visual_events == 0:
        return
    for style, path, text in labeled:
        if "![" not in text:
            add(
                findings,
                "warning",
                path,
                "figures-available",
                f"evidence carries figures ({visual_events} events) but the {style} draft embeds none; "
                "use the writing-brief 可用图表 blocks",
            )


def bundle_targets(root: Path) -> tuple[tuple[Path, str], ...]:
    """Resolve the editorial outputs declared by a bundle manifest.

    Historical bundles without a manifest style retain the standard three-file
    contract. A reduced bundle must name a supported style and explain its
    scope, matching the repository's publication contract.
    """

    run_json = root / "run.json"
    if not run_json.is_file():
        return tuple((root / name, style) for name, style in STANDARD_TARGETS)

    manifest = json.loads(run_json.read_text(encoding="utf-8"))
    style = manifest.get("style")
    if style is None:
        return tuple((root / name, audit_style) for name, audit_style in STANDARD_TARGETS)
    if not isinstance(style, str) or style not in REDUCED_STYLE_TARGETS:
        supported = ", ".join(sorted(REDUCED_STYLE_TARGETS))
        raise ValueError(f"unsupported reduced-scope style {style!r}; use {supported}")
    if not str(manifest.get("scope_note") or "").strip():
        raise ValueError("reduced-scope style requires scope_note")

    name, audit_style = REDUCED_STYLE_TARGETS[style]
    files = manifest.get("files")
    outputs = files.get("outputs") if isinstance(files, dict) else None
    if not isinstance(outputs, list) or name not in outputs:
        raise ValueError(f"reduced-scope article is not listed in files.outputs: {name}")
    return ((root / name, audit_style),)


def run(args: argparse.Namespace) -> int:
    """Business entry — ``args`` comes from the CLI parser in the dispatcher."""
    if args.quickread:
        if args.bundle_dir or args.memo or args.zhihu or args.xiaohongshu:
            raise SystemExit("--quickread audits a single-paper card and cannot be combined with bundle flags")
        findings = audit_file(Path(args.quickread), "quickread", args.min_chinese_share)[1]
    elif args.memo and not (args.bundle_dir or args.zhihu or args.xiaohongshu):
        # Single-style runs declare style+scope_note and may ship the memo
        # alone — auditing it must not require the full triplet.
        memo_text, findings = audit_file(Path(args.memo), "memo", args.min_chinese_share)
        figures_available_findings(
            [("memo", Path(args.memo), memo_text)], evidence_visual_event_count(args.evidence_jsonl), findings
        )
    else:
        contents: dict[str, tuple[Path, str]] = {}
        findings = []
        if args.bundle_dir:
            root = Path(args.bundle_dir)
            if args.memo or args.zhihu or args.xiaohongshu:
                targets = (
                    (Path(args.memo) if args.memo else root / "scientific-memo_keyan.md", "memo"),
                    (Path(args.zhihu) if args.zhihu else root / "zhihu-explainer_zhihu.md", "zhihu"),
                    (
                        Path(args.xiaohongshu)
                        if args.xiaohongshu
                        else root / "xiaohongshu-post_xiaohongshu.md",
                        "xiaohongshu",
                    ),
                )
            else:
                try:
                    targets = bundle_targets(root)
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    print(f"ERROR {root} [bundle-contract] {exc}")
                    return 1
        else:
            if not (args.memo and args.zhihu and args.xiaohongshu):
                raise SystemExit("provide --bundle-dir, --quickread, or all of --memo/--zhihu/--xiaohongshu")
            targets = (
                (Path(args.memo), "memo"),
                (Path(args.zhihu), "zhihu"),
                (Path(args.xiaohongshu), "xiaohongshu"),
            )

        for path, style in targets:
            content, more = audit_file(path, style, args.min_chinese_share)
            findings.extend(more)
            if content:
                contents[style] = (path, content)
        figures_available_findings(
            [(style, path, content) for style, (path, content) in contents.items()],
            evidence_visual_event_count(args.evidence_jsonl),
            findings,
        )
        if "memo" in contents and "zhihu" in contents:
            memo_path, memo = contents["memo"]
            zhihu_path, zhihu = contents["zhihu"]
            findings.extend(overlap_findings(memo_path, memo, zhihu_path, zhihu))

    if args.json:
        print(json.dumps({"ok": not any(item.severity == "error" for item in findings), "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item.severity.upper()} {item.file} [{item.rule}] {item.message}")
        if not findings:
            print("editorial quality audit OK")
        elif not any(item.severity == "error" for item in findings):
            print("editorial quality audit OK with warnings")
    return 1 if any(item.severity == "error" for item in findings) else 0

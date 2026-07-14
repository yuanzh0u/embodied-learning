#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills" / "embodied-ai-review-writer" / "scripts" / "audit_article_quality.py"


class AuditArticleQualityTests(unittest.TestCase):
    def write_good_bundle(self, root: Path) -> None:
        memo_mechanism = (
            "机器人数据质量不是数据文件的固定属性，而是样本、目标任务、动作接口和闭环收益之间的关系。"
            "多篇研究从轨迹筛选、任务覆盖、恢复片段和跨本体适配给出互补证据。"
            "这些结果共同支持以目标效用为中心的判断，但不同任务对质量信号的排序并不相同。"
        )
        memo = f"""# 具身数据质量研究备忘录

## 研究范围

本文讨论近一年机器人示教与策略训练中的数据质量问题，并明确区分论文直接结果与综合判断。

## 中心判断

高质量数据的核心不是表面干净，而是能否在目标任务上形成可验证的闭环收益。

## 核心机制

{memo_mechanism * 16}

## 条件与分歧

这一判断不能外推到所有任务。开放空间抓放、接触丰富装配和跨本体迁移依赖不同的质量信号，统一分数可能掩盖覆盖损失。

## 研究空白与下一步

下一步应比较片段价值、任务覆盖和真实闭环收益，并设计能推翻中心判断的对照实验。

## 结论

研究重点应从多采数据转向证明哪些数据在什么条件下真正有用。

## References

- [代表论文](https://arxiv.org/abs/2603.09056)
- [代表论文二](https://arxiv.org/abs/2606.16208)
- [代表论文三](https://arxiv.org/abs/2606.28320)
- [代表论文四](https://arxiv.org/abs/2602.01001)
- [代表论文五](https://arxiv.org/abs/2602.01002)
"""
        zhihu_mechanism = (
            "可以把机器人学习想成教新员工做装配。录像数量很多并不代表示范清楚；如果动作绕路、关键接触没记录，学到的只是重复失误。"
            "论文真正改变的判断，是把数据价值放回具体任务和执行结果中衡量。"
        )
        zhihu = f"""# 机器人数据越多越好吗？

## TL;DR

不一定。数据只有在目标任务上能被机器人正确理解和执行，才真正有价值。

## 误区从哪来

大家容易把数据规模等同于模型能力，因为图像和语言模型确实常从规模中获益。但机器人还要面对动作、接触和控制接口。

## 真实机制

{zhihu_mechanism * 11}

## 什么时候这个结论不成立

如果任务简单、动作接口统一、失败代价很低，扩大数据规模仍可能是最有效的选择。复杂接触任务才更需要精细质量治理。

## 结论

真正应该追问的不是有多少条轨迹，而是哪一条轨迹改变了机器人在真实任务中的表现。

## 延伸阅读

- [数据筛选研究](https://arxiv.org/abs/2603.09056)
- [覆盖与多样性](https://arxiv.org/abs/2606.16208)
- [失败与恢复](https://arxiv.org/abs/2606.28320)
"""
        xhs = """# 机器人数据，真的不是越多越好

最新研究把问题说得很直接：一条成功轨迹，也可能充满停顿、绕路和无效纠正。对机器人来说，数据看起来完整，不代表它真的能学到正确动作。真正的问题是，这些轨迹能不能转化成稳定、可执行、可恢复的行为。

💡 好数据先看任务价值。能帮助目标策略完成任务，比看起来平滑更重要；同一条轨迹换一个机器人或任务，价值可能完全不同。（[研究一](https://arxiv.org/abs/2603.09056)）

💡 多样性也有代价。只追求场景更多，可能让关键任务反而被稀释；数据筛选必须同时守住长尾覆盖和目标任务收益。（[研究二](https://arxiv.org/abs/2606.16208)）

💡 失败片段不一定该删除。一次纠错动作，可能比整条成功轨迹更有训练价值，因为它告诉模型偏离之后怎样重新回到正确状态。（[研究三](https://arxiv.org/abs/2606.28320)）

⚠️ 但别反过来迷信质量分数：不同任务需要的几何、接触和控制信息并不一样。开放空间抓放与精密装配不能用同一把尺子验收。

📚 依据：近一年机器人数据筛选与示教研究，完整证据见附录。
"""
        (root / "scientific-memo_keyan.md").write_text(memo, encoding="utf-8")
        (root / "zhihu-explainer_zhihu.md").write_text(zhihu, encoding="utf-8")
        (root / "xiaohongshu-post_xiaohongshu.md").write_text(xhs, encoding="utf-8")

    def test_good_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_good_bundle(root)
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle-dir", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("editorial quality audit OK", completed.stdout)

    def test_packet_dump_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            bad = """# Review

## Evidence Core

- Output type: scientific-memo
- Strong hook is allowed; stance/confidence cannot be upgraded.
- EA-DATA-2026-0001: English evidence claim...

## Claim Map

| Claim | Stance |
|---|---|
| raw event | support |
"""
            for name in ["scientific-memo_keyan.md", "zhihu-explainer_zhihu.md", "xiaohongshu-post_xiaohongshu.md"]:
                (root / name).write_text(bad, encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle-dir", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("packet-leak", completed.stdout)
        self.assertIn("event-ids-in-body", completed.stdout)

    def test_internal_reader_leaks_and_empty_reading_notes_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.write_good_bundle(root)
            zhihu = root / "zhihu-explainer_zhihu.md"
            zhihu.write_text(
                zhihu.read_text(encoding="utf-8")
                + "\n-  — [论文](https://arxiv.org/abs/2607.00001)\n完整定位见 随附证据附录。\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--bundle-dir", str(root)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("empty-reading-note", completed.stdout)
        self.assertIn("internal-prose", completed.stdout)


if __name__ == "__main__":
    unittest.main()

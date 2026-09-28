#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "lib" / "git_history.py"
SPEC = importlib.util.spec_from_file_location("git_history", SCRIPT)
git_history = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(git_history)


def init_repo(tmp: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp, check=True)
    (tmp / "README").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"],
        cwd=tmp,
        check=True,
    )


class GitHistoryTest(unittest.TestCase):
    def test_full_clone_is_not_shallow(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            init_repo(tmp)
            self.assertFalse(git_history.is_shallow_repository(tmp))
            git_history.require_full_history(tmp)  # does not raise

    def test_shallow_clone_detected_and_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            src = Path(raw) / "src"
            dst = Path(raw) / "shallow"
            src.mkdir()
            init_repo(src)
            # Second commit so --depth 1 actually truncates history.
            (src / "README").write_text("y\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=src, check=True)
            subprocess.run(
                ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "second"],
                cwd=src,
                check=True,
            )
            subprocess.run(
                ["git", "clone", "--depth", "1", f"file://{src}", str(dst)],
                check=True,
                capture_output=True,
            )
            self.assertTrue(git_history.is_shallow_repository(dst))
            with self.assertRaises(SystemExit) as ctx:
                git_history.require_full_history(dst)
            self.assertIn("shallow clone detected", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Layout resolution (repo checkout vs wheel install) and spawned-agent
isolation guarantees."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
import embodied_learning.utils.layout as layout
import embodied_learning.harness.claude as agent_invoke
from embodied_learning.wiki.publish import chat as wiki_chat
agent_invoke.run_one_shot_agent = agent_invoke.complete  # historical alias


def make_installed_pkg(tmp: Path) -> Path:
    """Synthesize the wheel layout: site-packages/{wiki_scripts,embodied_learning}
    where wiki_scripts holds run.py + the bundled skills tree. Returns the
    wiki_scripts dir."""
    pkg = tmp / "site-packages" / "wiki_scripts"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("# stub\n", encoding="utf-8")
    (pkg / "run.py").write_text("# stub\n", encoding="utf-8")
    skill = pkg / "skills" / "embodied-ai-review-writer"
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\n---\n", encoding="utf-8")
    shutil.copytree(
        REPO / "embodied_learning", pkg.parent / "embodied_learning",
        dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return pkg


class FindRootsTest(unittest.TestCase):
    def test_repo_checkout_layout(self) -> None:
        repo_root, skills_root, scripts_root = layout.find_roots()
        self.assertEqual(repo_root, REPO)
        self.assertEqual(skills_root, REPO / "skills")
        self.assertEqual(scripts_root, REPO / "scripts")

    def test_installed_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_installed_pkg(Path(tmp))
            env = dict(__import__("os").environ, PYTHONPATH=str(pkg.parent))
            probe = subprocess.run(
                [sys.executable, "-c",
                 "from embodied_learning.utils.layout import find_roots; "
                 "r, s, c = find_roots(); print(r or ''); print(s); print(c)"],
                capture_output=True, text=True, timeout=60, cwd=str(pkg), env=env,
            )
            self.assertEqual(probe.returncode, 0, probe.stderr)
            repo_root, skills_root, scripts_root = probe.stdout.splitlines()
            self.assertEqual(repo_root, "")
            self.assertEqual(Path(skills_root), pkg / "skills")
            self.assertEqual(Path(scripts_root), pkg)


class KbCacheDirTest(unittest.TestCase):
    def test_cache_lives_under_the_kb_root(self) -> None:
        """Full text is reused across runs and machines, so the cache hangs
        off the KB root (next to pool/) instead of /tmp."""
        self.assertEqual(layout.kb_cache_dir("/kb"), Path("/kb/.cache"))
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(layout.kb_cache_dir(tmp), Path(tmp) / ".cache")


class ResolvePipelineLayoutTest(unittest.TestCase):
    def test_repo_shape(self) -> None:
        skills_root, scripts_root = wiki_chat.resolve_pipeline_layout(REPO)
        self.assertEqual(skills_root, REPO / "skills")
        self.assertEqual(scripts_root, REPO / "scripts")

    def test_installed_scripts_dir_shape(self) -> None:
        # pipeline_root IS the wiki_scripts dir (contains run.py + skills/)
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_installed_pkg(Path(tmp))
            skills_root, scripts_root = wiki_chat.resolve_pipeline_layout(pkg)
            self.assertEqual(skills_root, pkg / "skills")
            self.assertEqual(scripts_root, pkg)

    def test_installed_skills_dir_shape(self) -> None:
        # pipeline_root arrives as the bundled skills/ dir itself
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_installed_pkg(Path(tmp))
            skills_root, scripts_root = wiki_chat.resolve_pipeline_layout(pkg / "skills")
            self.assertEqual(skills_root, pkg / "skills")
            self.assertEqual(scripts_root, pkg)


class IsolatedClaudeEnvTest(unittest.TestCase):
    def setUp(self) -> None:
        # The env helpers live in the harness module now; patch there (never
        # the shim's re-exports) so tests cannot touch real credentials.
        import embodied_learning.harness.claude as harness_claude

        self._harness = harness_claude
        self._orig = (harness_claude.ISOLATED_CONFIG_DIR, harness_claude.CREDENTIALS_FILE)

    def tearDown(self) -> None:
        self._harness.ISOLATED_CONFIG_DIR, self._harness.CREDENTIALS_FILE = self._orig

    def test_strips_nested_markers_and_sets_config_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = Path(tmp) / "claude-config"
            self._harness.ISOLATED_CONFIG_DIR = config_dir
            env = agent_invoke.isolated_claude_env({
                "CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli",
                "CLAUDE_CODE_SSE_PORT": "1234", "PATH": "/usr/bin",
            })
            self.assertNotIn("CLAUDECODE", env)
            self.assertNotIn("CLAUDE_CODE_ENTRYPOINT", env)
            self.assertNotIn("CLAUDE_CODE_SSE_PORT", env)
            self.assertEqual(env["CLAUDE_CONFIG_DIR"], str(config_dir))
            self.assertTrue(config_dir.is_dir())

    def test_copies_credentials_readonly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            config_dir = tmp / "claude-config"
            credentials = tmp / "home-credentials.json"
            credentials.write_text("{}", encoding="utf-8")
            self._harness.ISOLATED_CONFIG_DIR = config_dir
            self._harness.CREDENTIALS_FILE = credentials
            self._harness.prepare_claude_config_dir(config_dir)
            copied = config_dir / ".credentials.json"
            self.assertTrue(copied.is_file())
            self.assertEqual(copied.stat().st_mode & 0o777, 0o600)
            # idempotent: second call keeps the existing copy
            credentials.write_text("{\"x\":1}", encoding="utf-8")
            self._harness.prepare_claude_config_dir(config_dir)
            self.assertEqual(copied.read_text(encoding="utf-8"), "{}")

    def test_auth_ready_messages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = Path(tmp) / "claude-config"
            config_dir.mkdir()
            env = {"CLAUDE_CONFIG_DIR": str(config_dir)}
            self.assertIsNotNone(agent_invoke.claude_auth_ready(env))
            env["ANTHROPIC_API_KEY"] = "sk-test"
            self.assertIsNone(agent_invoke.claude_auth_ready(env))
            del env["ANTHROPIC_API_KEY"]
            (config_dir / ".credentials.json").write_text("{}", encoding="utf-8")
            self.assertIsNone(agent_invoke.claude_auth_ready(env))


class RunOneShotAgentIsolationTest(unittest.TestCase):
    def test_passes_cwd_and_isolated_env(self) -> None:
        captured: dict = {}

        def fake_run(command, **kwargs):
            captured["command"] = command
            captured.update(kwargs)
            return subprocess.CompletedProcess(command, 0, "", "")

        import embodied_learning.harness.claude as harness_claude

        orig_run = harness_claude.subprocess.run
        harness_claude.subprocess.run = fake_run
        try:
            with tempfile.TemporaryDirectory() as tmp, \
                    mock.patch.dict(os.environ,
                                    {"EMBODIED_CONVERSATION_STORE": str(Path(tmp) / "store")}):
                harness_claude.ISOLATED_CONFIG_DIR = Path(tmp) / "cfg"
                agent_invoke.run_one_shot_agent("prompt", timeout_s=1.0, cli="claude", cwd=Path(tmp))
        finally:
            harness_claude.subprocess.run = orig_run
        self.assertEqual(captured["command"], ["claude", "-p", "--model", agent_invoke.DRIVER_AGENT_MODEL,
                                               "--output-format", "json",
                                               "--permission-mode", "bypassPermissions"])
        self.assertIn("cwd", captured)
        self.assertIn("CLAUDE_CONFIG_DIR", captured["env"])


class InstalledLayoutSmokeTest(unittest.TestCase):
    """Load the real pipeline scripts from a synthesized wheel layout and
    check their path constants resolve inside the package (the exact failure
    mode of the previous parent.parent bootstrapping). Runs in subprocesses so
    the `lib` package does not leak between layouts in this process."""

    SCRIPT_NAMES = ("run.py", "wiki.py")

    def test_scripts_resolve_inside_pkg(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = make_installed_pkg(Path(tmp))
            shutil.copy2(REPO / "scripts" / "__init__.py", pkg / "__init__.py")
            for name in self.SCRIPT_NAMES:
                shutil.copy2(REPO / "scripts" / name, pkg / name)
            # The wheel layout: BOTH packages sit in site-packages so
            # embodied_learning.utils.layout takes its wheel branch
            # (find_spec("wiki_scripts")) instead of probing a repo checkout.
            site_packages = pkg.parent
            shutil.copytree(
                REPO / "embodied_learning",
                site_packages / "embodied_learning",
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            env = dict(__import__("os").environ, PYTHONPATH=str(site_packages))
            for name in self.SCRIPT_NAMES:
                probe = subprocess.run(
                    [sys.executable, "-c",
                     "import importlib.util, sys\n"
                     "spec = importlib.util.spec_from_file_location('m', sys.argv[1])\n"
                     "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
                     "print(m.SCRIPTS_ROOT)\n",
                     str(pkg / name)],
                    capture_output=True, text=True, timeout=60,
                    cwd=str(pkg), env=env,  # no repo on sys.path via cwd
                )
                self.assertEqual(probe.returncode, 0, f"{name}: {probe.stderr}")
                self.assertEqual(probe.stdout.strip(), str(pkg), name)

            # entry-point style invocation (--help) works for the dispatchers
            for name, sub in (("run.py", "pipeline"), ("run.py", "finalize"), ("wiki.py", "serve")):
                help_run = subprocess.run(
                    [sys.executable, str(pkg / name), sub, "--help"],
                    capture_output=True, text=True, timeout=60, cwd=str(pkg), env=env,
                )
                self.assertEqual(help_run.returncode, 0, f"{name} {sub}: {help_run.stderr}")


if __name__ == "__main__":
    unittest.main()

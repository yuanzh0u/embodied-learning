"""Spawn-environment hygiene for lib.agent_invoke (scripts/lib/agent_invoke.py)."""

import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "lib" / "agent_invoke.py"
_spec = importlib.util.spec_from_file_location("agent_invoke_test_module", _SCRIPT)
agent_invoke = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(agent_invoke)


class IsolatedClaudeEnvTest(unittest.TestCase):
    def test_strips_subagent_model_override(self) -> None:
        """A shell-profile CLAUDE_CODE_SUBAGENT_MODEL must not leak into spawned
        sessions: on CLI < 2.1.251 it outranks per-call model choices, so Task
        subagents would all land on that model instead of inheriting the
        session's pinned --model."""
        with mock.patch.dict(
            "os.environ",
            {"CLAUDE_CODE_SUBAGENT_MODEL": "glm-5.3-flash-cc", "PATH": os.environ["PATH"]},
            clear=True,
        ):
            env = agent_invoke.isolated_claude_env()
        self.assertNotIn("CLAUDE_CODE_SUBAGENT_MODEL", env)

    def test_strips_nested_session_markers(self) -> None:
        with mock.patch.dict(
            "os.environ",
            {
                "CLAUDECODE": "1",
                "CLAUDE_CODE_ENTRYPOINT": "cli",
                "CLAUDE_CODE_SSE_PORT": "1234",
                "PATH": os.environ["PATH"],
            },
            clear=True,
        ):
            env = agent_invoke.isolated_claude_env()
        for key in agent_invoke.NESTED_CLAUDE_ENV_KEYS:
            self.assertNotIn(key, env)

    def test_explicit_env_argument_is_stripped_too(self) -> None:
        env = agent_invoke.isolated_claude_env({"CLAUDE_CODE_SUBAGENT_MODEL": "glm-5.3-flash-cc"})
        self.assertNotIn("CLAUDE_CODE_SUBAGENT_MODEL", env)


if __name__ == "__main__":
    unittest.main()

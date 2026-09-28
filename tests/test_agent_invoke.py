"""Spawn-environment hygiene for lib.agent_invoke (scripts/lib/agent_invoke.py)."""

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "lib" / "agent_invoke.py"
_spec = importlib.util.spec_from_file_location("agent_invoke_test_module", _SCRIPT)
agent_invoke = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(agent_invoke)
# complete()'s globals live in the harness module, not the shim.
import embodied_learning.harness.claude as harness_claude  # noqa: E402


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


class ConversationStoreTest(unittest.TestCase):
    """Every claude invocation is archived machine-locally under
    ~/.claude/projects/embodied-learning-work (env-overridable for tests)."""

    def setUp(self) -> None:
        import tempfile

        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._env = mock.patch.dict(
            os.environ, {"EMBODIED_CONVERSATION_STORE": self._tmp.name}
        )
        self._env.start()
        self.addCleanup(self._env.stop)

    def test_conversation_store_default_and_override(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("EMBODIED_CONVERSATION_STORE", None)
            self.assertEqual(
                agent_invoke.conversation_store(),
                Path.home() / ".claude" / "projects" / "embodied-learning-work",
            )
        # setUp's override is still active for this test process.
        self.assertNotEqual(agent_invoke.conversation_store(), Path.home())

    def test_record_agent_invocation_writes_folder_and_index(self) -> None:
        folder = agent_invoke.record_agent_invocation(
            kind="one-shot",
            label="2302.01109 速读",
            prompt="PROMPT",
            stdout="OUT",
            stderr="warn",
            returncode=0,
            cwd="/tmp/kb",
            model="glm-5.3-flash",
            duration_s=1.5,
        )
        self.assertIsNotNone(folder)
        self.assertEqual((folder / "prompt.md").read_text(encoding="utf-8"), "PROMPT")
        self.assertEqual((folder / "output.txt").read_text(encoding="utf-8"), "OUT")
        self.assertIn("warn", (folder / "stderr.txt").read_text(encoding="utf-8"))
        index = json.loads(
            (folder.parent.parent / "invocations.jsonl").read_text(encoding="utf-8").splitlines()[-1]
        )
        self.assertEqual(index["kind"], "one-shot")
        self.assertEqual(index["returncode"], 0)
        self.assertIn("2302.01109", index["label"])
        self.assertEqual(index["folder"], str(folder.relative_to(folder.parent.parent)))

    def test_run_one_shot_agent_records_invocation(self) -> None:
        completed = subprocess.CompletedProcess(["claude"], 0, stdout="RESULT", stderr="")
        with mock.patch.object(harness_claude.subprocess, "run", return_value=completed) as run:
            result = agent_invoke.run_one_shot_agent(
                "do things",
                timeout_s=10,
                cli="/fake/claude",
                cwd="/tmp/kb",
                label="paper-1234",
            )
        self.assertEqual(result.stdout, "RESULT")
        recorded = json.loads(
            (Path(self._tmp.name) / "invocations.jsonl").read_text(encoding="utf-8").splitlines()[-1]
        )
        self.assertEqual(recorded["kind"], "one-shot")
        self.assertEqual(recorded["label"], "paper-1234")
        self.assertEqual(recorded["returncode"], 0)
        self.assertEqual(run.call_args.kwargs["input"], "do things")

    def test_run_one_shot_agent_records_timeout(self) -> None:
        with mock.patch.object(
            harness_claude.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(cmd=["claude"], timeout=1),
        ):
            with self.assertRaises(subprocess.TimeoutExpired):
                agent_invoke.run_one_shot_agent(
                    "slow", timeout_s=1, cli="/fake/claude", label="timeout-case"
                )
        recorded = json.loads(
            (Path(self._tmp.name) / "invocations.jsonl").read_text(encoding="utf-8").splitlines()[-1]
        )
        self.assertIsNone(recorded["returncode"])

    def test_storage_failure_never_breaks_the_call(self) -> None:
        completed = subprocess.CompletedProcess(["claude"], 0, stdout="ok", stderr="")
        with mock.patch.object(
            harness_claude, "conversation_store", side_effect=OSError("no space")
        ), mock.patch.object(harness_claude.subprocess, "run", return_value=completed):
            result = agent_invoke.run_one_shot_agent(
                "p", timeout_s=5, cli="/fake/claude", label="x"
            )
        self.assertEqual(result.stdout, "ok")

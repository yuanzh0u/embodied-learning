"""The harness binding surface (embodied_learning/harness/claude.py).

Loads the module via importlib (wheel-layout parity with a repo checkout) and
asserts the contract that matters architecturally: this module is the ONLY
place that spawns claude, so it must be self-contained (no wiki_chat /
scripts imports) and expose the complete invocation surface.
"""

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "embodied_learning" / "harness" / "claude.py"
claude = importlib.import_module("embodied_learning.harness.claude")


class SurfaceContractTest(unittest.TestCase):
    """The binding layer's public surface and its independence guarantees."""

    def test_exposes_full_invocation_surface(self) -> None:
        for name in (
            "resolve_cli", "isolated_claude_env", "strip_nested_claude_env",
            "prepare_claude_config_dir", "claude_auth_ready", "complete",
            "ChatTurn", "build_claude_command", "parse_stream_line",
            "is_resume_failure", "conversation_store", "record_agent_invocation",
            "DRIVER_AGENT_MODEL", "DEFAULT_PERMISSION_MODE", "FALLBACK_CLI",
        ):
            self.assertTrue(hasattr(claude, name), f"harness surface missing {name}")

    def test_no_scripts_layer_imports(self) -> None:
        """The binding must not depend on the scripts/wiki layer — callers
        depend on the harness, never the reverse (pybind direction)."""

        import ast

        tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imported.add(node.module.split(".")[0])
        self.assertEqual(imported & {"lib", "wiki_scripts", "wiki_chat"}, set())


class CompleteCommandShapeTest(unittest.TestCase):
    """complete() keeps the plain-text one-shot command; stream=True switches
    to stream-json. The two shapes must never blur — dozens of callers parse
    stdout by exact contract."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._env = mock.patch.dict(
            os.environ, {"EMBODIED_CONVERSATION_STORE": self._tmp.name}
        )
        self._env.start()
        self.addCleanup(self._env.stop)

    def _capture(self, **kwargs):
        captured: dict = {}

        def fake_run(command, **run_kwargs):
            captured["command"] = command
            captured.update(run_kwargs)
            return subprocess.CompletedProcess(command, 0, "OUT", "")

        with mock.patch.object(claude.subprocess, "run", side_effect=fake_run):
            result = claude.complete("prompt text", timeout_s=5, cli="claude", **kwargs)
        self.assertEqual(result.stdout, "OUT")
        return captured

    def test_plain_text_shape(self) -> None:
        captured = self._capture(cwd="/tmp/kb", label="paper-1")
        self.assertEqual(
            captured["command"],
            ["claude", "-p", "--model", claude.DRIVER_AGENT_MODEL,
             "--permission-mode", "bypassPermissions"],
        )
        self.assertTrue(captured["capture_output"])
        self.assertEqual(captured["input"], "prompt text")
        self.assertEqual(captured["cwd"], "/tmp/kb")

    def test_stream_shape_and_file_sink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sink = Path(tmp) / "writer.log"
            with open(sink, "w", encoding="utf-8") as handle:
                captured = self._capture(stream=True, stream_to=handle, label="writer-run")
            self.assertEqual(captured["command"][:6],
                             ["claude", "-p", "--output-format", "stream-json", "--verbose",
                              "--permission-mode"])
            self.assertFalse(captured["capture_output"])
            self.assertIs(captured["stdout"], handle)
            self.assertEqual(sink.read_text(encoding="utf-8"), "")  # fake run wrote nothing

    def test_invocation_recorded_with_label(self) -> None:
        self._capture(cwd="/tmp/kb", label="slide-2302.01109")
        index = json.loads(
            (Path(self._tmp.name) / "invocations.jsonl").read_text(encoding="utf-8").splitlines()[-1]
        )
        self.assertEqual(index["label"], "slide-2302.01109")
        self.assertEqual(index["output_chars"], 3)


class ChatTurnInHarnessTest(unittest.TestCase):
    """ChatTurn streams, archives, and stops exactly as wiki_chat's original —
    the move to the harness must not change its external contract."""

    def test_events_and_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["EMBODIED_CONVERSATION_STORE"] = tmp
            try:
                # ChatTurn feeds the prompt via stdin and closes it; /bin/cat
                # echoes it back, so the prompt IS the stream-json transcript.
                stream = (
                    json.dumps({"type": "system", "subtype": "init",
                                "session_id": "s-1", "model": "m"}) + "\n"
                    + json.dumps({"type": "result", "session_id": "s-1",
                                  "is_error": False, "result": "done"}) + "\n"
                )
                turn = claude.ChatTurn(
                    cli="claude", prompt=stream, cwd=Path(tmp), model="m",
                    system_prompt="SYS",
                )

                def fake_popen(command, **kwargs):
                    captured_command.append(command)
                    return real_popen(
                        ["/bin/cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=True,
                    )

                captured_command: list = []
                real_popen = claude.subprocess.Popen  # capture before patching
                with mock.patch.object(claude.subprocess, "Popen", side_effect=fake_popen):
                    turn.start()
                events = list(turn.events())
                self.assertEqual(events[0]["type"], "session")
                self.assertEqual(events[-1]["type"], "done")
                argv = captured_command[0]
                self.assertEqual(argv[argv.index("--append-system-prompt") + 1], "SYS")
                self.assertEqual(argv[argv.index("--model") + 1], "m")
                index = json.loads(
                    (Path(tmp) / "invocations.jsonl").read_text(encoding="utf-8").splitlines()[-1]
                )
                self.assertEqual(index["kind"], "chat")
                self.assertEqual(index["returncode"], 0)
            finally:
                os.environ.pop("EMBODIED_CONVERSATION_STORE", None)


if __name__ == "__main__":
    unittest.main()

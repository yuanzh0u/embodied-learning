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
            "session_log_path", "open_session_log", "session_ledger_enabled",
            "parse_result_envelope", "is_stream_truncation",
            "DRIVER_AGENT_MODEL", "DEFAULT_PERMISSION_MODE", "FALLBACK_CLI",
            "STREAM_FALLBACK_MODEL", "STREAM_TRUNCATION_KEYWORDS",
            "judge_questions", "system_one_ready", "resolve_system_one_endpoint",
            "resolve_system_one_key", "SystemOneError", "SYSTEM_ONE_MODEL",
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
             "--output-format", "json",
             "--permission-mode", "bypassPermissions"],
        )
        self.assertTrue(captured["capture_output"])
        self.assertEqual(captured["input"], "prompt text")
        self.assertEqual(captured["cwd"], "/tmp/kb")

    def test_json_envelope_is_unwrapped_to_plain_text(self) -> None:
        """Callers keep their plain-text stdout contract even though the CLI
        now answers with a JSON envelope (usage recording needs it)."""

        envelope = json.dumps({
            "type": "result", "subtype": "success", "is_error": False,
            "result": "PAYLOAD", "session_id": "s-1", "num_turns": 2,
            "total_cost_usd": 0.02,
            "usage": {"input_tokens": 10, "output_tokens": 3,
                      "cache_read_input_tokens": 4, "cache_creation_input_tokens": 0},
        })
        with mock.patch.object(
            claude.subprocess, "run",
            return_value=subprocess.CompletedProcess(["claude"], 0, envelope, ""),
        ):
            result = claude.complete("p", timeout_s=5, cli="claude", label="env")
        self.assertEqual(result.stdout, "PAYLOAD")

    def test_envelope_warning_preamble_is_tolerated(self) -> None:
        envelope = json.dumps({"type": "result", "result": "OK", "is_error": False})
        self.assertEqual(
            claude.parse_result_envelope("Warning: no stdin data\n" + envelope + "\n"),
            json.loads(envelope),
        )
        self.assertIsNone(claude.parse_result_envelope("plain text"))

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


class CompleteFallbackRetryTest(unittest.TestCase):
    """Stream truncation switches to the fallback model and retries (2026-10-20,
    mirrors monica's harness). The dmxapi glm upstream cut is a LINK problem —
    same-model retry is a coin flip, switching ``--model`` on the same gateway
    is the escape (probe: deepseek-v4.1-flash-1017 landed 6/6 while glm died
    5/6). The error wording must stay byte-identical: problem-card fingerprints
    hash it."""

    TRUNCATION = (
        "API Error: upstream stream ended without a terminal frame "
        "(no message_delta, no message_stop); the response is truncated "
        "and incomplete; received 7 frames; reason=eof"
    )

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._env = mock.patch.dict(
            os.environ, {"EMBODIED_CONVERSATION_STORE": self._tmp.name}
        )
        self._env.start()
        self.addCleanup(self._env.stop)
        sleep_patch = mock.patch.object(claude.time, "sleep")  # skip the backoff
        sleep_patch.start()
        self.addCleanup(sleep_patch.stop)

    def _envelope(self, *, is_error: bool, result: str) -> str:
        return json.dumps({
            "type": "result", "is_error": is_error, "result": result,
            "usage": {"input_tokens": 5, "output_tokens": 2},
        })

    def _complete(self, outcomes: list[tuple[int, str]], **kwargs):
        """Run complete() against a fake subprocess.run; outcomes is one
        (returncode, stdout) per expected call. Returns (result, commands)."""
        captured: list[list[str]] = []
        remaining = list(outcomes)

        def fake_run(command, **run_kwargs):
            captured.append(list(command))
            code, out = remaining.pop(0)
            return subprocess.CompletedProcess(command, code, out, "")

        with mock.patch.object(claude.subprocess, "run", side_effect=fake_run):
            result = claude.complete("prompt text", timeout_s=5, cli="claude", **kwargs)
        self.assertEqual(remaining, [])  # every prepared outcome was consumed
        return result, captured

    @staticmethod
    def _model_of(command: list[str]) -> str:
        return command[command.index("--model") + 1]

    def test_switches_to_fallback_and_recovers(self) -> None:
        result, commands = self._complete([
            (1, self._envelope(is_error=True, result=self.TRUNCATION)),
            (0, self._envelope(is_error=False, result="RECOVERED")),
        ])
        self.assertEqual(result.stdout, "RECOVERED")
        self.assertEqual(len(commands), 2)  # 首跑 + 1 次重试
        self.assertEqual(self._model_of(commands[0]), claude.DRIVER_AGENT_MODEL)
        self.assertEqual(self._model_of(commands[1]), claude.STREAM_FALLBACK_MODEL)

    def test_fallback_name_is_configurable(self) -> None:
        _, commands = self._complete([
            (1, self._envelope(is_error=True, result=self.TRUNCATION)),
            (0, self._envelope(is_error=False, result="OK")),
        ], fallback_model="my-backup")
        self.assertEqual(self._model_of(commands[1]), "my-backup")

    def test_disabled_fallback_keeps_same_model(self) -> None:
        result, commands = self._complete([
            (1, self._envelope(is_error=True, result=self.TRUNCATION)),
            (0, self._envelope(is_error=False, result="OK")),
        ], fallback_model="")
        self.assertEqual(result.stdout, "OK")
        self.assertEqual(len(commands), 2)
        self.assertTrue(
            all(self._model_of(c) == claude.DRIVER_AGENT_MODEL for c in commands)
        )

    def test_plain_error_is_not_retried(self) -> None:
        """Non-truncation failures die once — retry only heals this one fault."""
        result, commands = self._complete([
            (1, self._envelope(is_error=True, result="模型内部错误")),
        ])
        self.assertEqual(result.stdout, "模型内部错误")
        self.assertEqual(len(commands), 1)

    def test_exhausted_retries_stay_on_fallback(self) -> None:
        result, commands = self._complete([
            (1, self._envelope(is_error=True, result=self.TRUNCATION)),
            (1, self._envelope(is_error=True, result=self.TRUNCATION)),
            (1, self._envelope(is_error=True, result=self.TRUNCATION)),
        ])
        self.assertEqual(len(commands), 3)  # 首跑 + 2 次重试
        self.assertEqual(self._model_of(commands[0]), claude.DRIVER_AGENT_MODEL)
        self.assertTrue(
            all(self._model_of(c) == claude.STREAM_FALLBACK_MODEL for c in commands[1:])
        )
        self.assertIn("upstream stream ended", result.stdout)  # 报错原文不动


class ChatTurnFallbackRetryTest(unittest.TestCase):
    """ChatTurn respawns with the fallback model on a stream truncation: the
    held truncation-done is dropped and the retry's stream supplies the real
    one (2026-10-20, same semantic as complete())."""

    TRUNCATION = CompleteFallbackRetryTest.TRUNCATION

    def _turn_stream(self, *, is_error: bool, result: str) -> str:
        return (
            json.dumps({"type": "system", "subtype": "init",
                        "session_id": "s-1", "model": "m"}) + "\n"
            + json.dumps({"type": "result", "session_id": "s-1",
                          "is_error": is_error, "result": result}) + "\n"
        )

    def test_switches_to_fallback_and_recovers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["EMBODIED_CONVERSATION_STORE"] = tmp
            try:
                streams = [
                    self._turn_stream(is_error=True, result=self.TRUNCATION),
                    self._turn_stream(is_error=False, result="RECOVERED"),
                ]
                captured_command: list = []
                real_popen = claude.subprocess.Popen  # capture before patching

                def fake_popen(command, **kwargs):
                    captured_command.append(list(command))
                    code = "import sys; sys.stdin.read(); sys.stdout.write(%r)" % streams.pop(0)
                    return real_popen(
                        ["/usr/bin/python3", "-c", code],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=True,
                    )

                turn = claude.ChatTurn(
                    cli="claude", prompt="hi", cwd=Path(tmp), model="glm-5.3-flash",
                    fallback_model="deepseek-v4.1-flash-1017",
                )
                with mock.patch.object(claude.subprocess, "Popen", side_effect=fake_popen), \
                        mock.patch.object(claude.time, "sleep"):
                    turn.start()
                    events = list(turn.events())
                self.assertEqual(len(captured_command), 2)  # 首跑 + 1 次重试
                first = captured_command[0]
                second = captured_command[1]
                self.assertEqual(first[first.index("--model") + 1], "glm-5.3-flash")
                self.assertEqual(
                    second[second.index("--model") + 1], "deepseek-v4.1-flash-1017")
                # The held truncation-done never reaches the consumer — the only
                # done event is the retry's success.
                dones = [e for e in events if e.get("type") == "done"]
                self.assertEqual(len(dones), 1)
                self.assertFalse(dones[0].get("is_error"))
                retries = [e for e in events if e.get("stage") == "retry"]
                self.assertEqual(len(retries), 1)
                self.assertIn("deepseek-v4.1-flash-1017", retries[0]["detail"])
            finally:
                os.environ.pop("EMBODIED_CONVERSATION_STORE", None)

    def test_plain_error_is_not_retried(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["EMBODIED_CONVERSATION_STORE"] = tmp
            try:
                captured_command: list = []
                real_popen = claude.subprocess.Popen
                stream = self._turn_stream(is_error=True, result="模型内部错误")

                def fake_popen(command, **kwargs):
                    captured_command.append(list(command))
                    code = "import sys; sys.stdin.read(); sys.stdout.write(%r)" % stream
                    return real_popen(
                        ["/usr/bin/python3", "-c", code],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, text=True,
                    )

                turn = claude.ChatTurn(
                    cli="claude", prompt="hi", cwd=Path(tmp), model="glm-5.3-flash",
                )
                with mock.patch.object(claude.subprocess, "Popen", side_effect=fake_popen):
                    turn.start()
                    events = list(turn.events())
                self.assertEqual(len(captured_command), 1)  # 一次判死
                dones = [e for e in events if e.get("type") == "done"]
                self.assertEqual(len(dones), 1)
                self.assertTrue(dones[0].get("is_error"))
            finally:
                os.environ.pop("EMBODIED_CONVERSATION_STORE", None)


class ToolDetailTest(unittest.TestCase):
    """``_tool_detail`` feeds the dialog journal — the audit trail for
    "did the agent pass the right flags?". A 120-char cut used to truncate
    audit-citations invocations mid-flag and hide real wrong-flag retries
    (2026-10-15). Commands stay whole; path-ish keys stay compact."""

    def _detail(self, payload: dict) -> str:
        line = json.dumps({
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": "Bash", "input": payload}]},
        })
        events = claude.parse_stream_line(line)
        tool_events = [e for e in events if e.get("stage") == "tool"]
        self.assertEqual(len(tool_events), 1)
        return tool_events[0]["detail"]

    def test_command_is_not_cut_at_120(self) -> None:
        command = (
            "python3 scripts/run.py audit-citations "
            "--article work/literature-review-纹理映射-20261013/scientific-memo_keyan.md "
            "--appendix work/literature-review-纹理映射-20261013/evidence-appendix.md "
            "--evidence-jsonl work/literature-review-纹理映射-20261013/evidence.jsonl "
            "--run-json work/literature-review-纹理映射-20261013/run.json"
        )
        self.assertGreater(len(command), 120)
        self.assertEqual(self._detail({"command": command}), command)

    def test_command_still_capped_at_config_limit(self) -> None:
        huge = "x" * (claude.TOOL_COMMAND_DETAIL_MAX_CHARS + 50)
        detail = self._detail({"command": huge})
        self.assertEqual(len(detail), claude.TOOL_COMMAND_DETAIL_MAX_CHARS)

    def test_file_path_stays_compact(self) -> None:
        path = "/tmp/" + "a" * 400
        detail = self._detail({"file_path": path})
        self.assertEqual(len(detail), claude.TOOL_DETAIL_MAX_CHARS)

    def test_non_string_and_missing_input(self) -> None:
        self.assertEqual(self._detail({"command": 42}), "")
        self.assertEqual(claude._tool_detail({"input": "not-a-dict"}), "")


class ToolReasonTest(unittest.TestCase):
    """A path-only Edit line says which file, not why it changed. The journal
    is the debugging surface for the audit gates, so the tool event carries
    the agent's stated motive (2026-10-20 自监督预训练 audit loop)."""

    def _events(self, content: list[dict], prior_text: str = "") -> list[dict]:
        line = json.dumps({"type": "assistant", "message": {"content": content}})
        return claude.parse_stream_line(line, prior_text=prior_text)

    def test_reason_comes_from_the_same_message_narration(self) -> None:
        events = self._events([
            {"type": "text", "text": "把英文表题改中文，修中文占比不足。"},
            {"type": "tool_use", "name": "Edit", "input": {"file_path": "/run/memo.md"}},
        ])
        tool = next(e for e in events if e.get("stage") == "tool")
        self.assertEqual(tool["reason"], "把英文表题改中文，修中文占比不足。")

    def test_reason_falls_back_to_prior_narration(self) -> None:
        events = self._events(
            [{"type": "tool_use", "name": "Edit", "input": {"file_path": "/run/memo.md"}}],
            prior_text="行内 arXiv 链接触发审计门，改为上标引用。",
        )
        self.assertEqual(
            next(e for e in events if e.get("stage") == "tool")["reason"],
            "行内 arXiv 链接触发审计门，改为上标引用。",
        )

    def test_reason_source_distinguishes_inline_from_carried(self) -> None:
        """A tool-only message repeats the previous narration; the journal must
        say so, otherwise a long run of edits reads as the same motive
        fifteen times (2026-10-20 视频流式重建 audit loop)."""

        inline = self._events([
            {"type": "text", "text": "拆长句。"},
            {"type": "tool_use", "name": "Edit", "input": {"file_path": "/run/zhihu.md"}},
        ])
        self.assertEqual(
            next(e for e in inline if e.get("stage") == "tool")["reason_source"], "inline"
        )

        carried = self._events(
            [{"type": "tool_use", "name": "Edit", "input": {"file_path": "/run/zhihu.md"}}],
            prior_text="拆长句。",
        )
        self.assertEqual(
            next(e for e in carried if e.get("stage") == "tool")["reason_source"], "carried"
        )

        bare = self._events([{"type": "tool_use", "name": "Edit", "input": {"file_path": "/x"}}])
        tool = next(e for e in bare if e.get("stage") == "tool")
        self.assertEqual((tool["reason"], tool["reason_source"]), ("", "none"))

    def test_reason_is_capped_and_whitespace_collapsed(self) -> None:
        long_text = "  修\n 门禁" + "字" * (claude.TOOL_REASON_MAX_CHARS + 50)
        events = self._events([{"type": "tool_use", "name": "Write", "input": {"file_path": "/x"}}],
                              prior_text=long_text)
        reason = next(e for e in events if e.get("stage") == "tool")["reason"]
        self.assertLessEqual(len(reason), claude.TOOL_REASON_MAX_CHARS + 1)  # + the "…" prefix
        self.assertNotIn("\n", reason)
        self.assertTrue(reason.startswith("…"))

    def test_tool_without_narration_has_empty_reason(self) -> None:
        events = self._events([{"type": "tool_use", "name": "Edit", "input": {"file_path": "/x"}}])
        self.assertEqual(next(e for e in events if e.get("stage") == "tool")["reason"], "")


class SystemOneBindingTest(unittest.TestCase):
    """The decision-model binding (jev / System One): environment-only config,
    ``state`` + typed ``questions`` wire shape, transient retry, and the same
    ledger contract as complete() (2026-10-20 smart-jev selection)."""

    ENV = {
        "EMBODIED_SYSTEM_ONE_URL": "https://gw.example/v1/systemone",
        "EMBODIED_SYSTEM_ONE_API_KEY": "test-key",
        "EMBODIED_CONVERSATION_STORE": "",
        "EMBODIED_AGENT_SESSION_LOG": "0",
    }

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        env = dict(self.ENV, EMBODIED_CONVERSATION_STORE=self._tmp.name)
        patcher = mock.patch.dict(os.environ, env, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)
        for key in ("EMBODIED_AGENT_SESSION_LOG",):
            os.environ.pop(key, None)
        sleep_patch = mock.patch.object(claude.time, "sleep")
        sleep_patch.start()
        self.addCleanup(sleep_patch.stop)

    @staticmethod
    def _response(payload: dict, status: int = 200):
        body = mock.MagicMock()
        body.read.return_value = json.dumps(payload).encode("utf-8")
        body.__enter__ = mock.Mock(return_value=body)
        body.__exit__ = mock.Mock(return_value=False)
        return body

    def test_resolves_endpoint_from_gateway_base(self) -> None:
        env = {"ANTHROPIC_BASE_URL": "https://gw.example"}
        self.assertEqual(
            claude.resolve_system_one_endpoint(env),
            "https://gw.example/v1/systemone",
        )

    def test_explicit_endpoint_is_used_verbatim(self) -> None:
        env = {
            "EMBODIED_SYSTEM_ONE_URL": "https://other.example/custom",
            "ANTHROPIC_BASE_URL": "https://gw.example",
        }
        self.assertEqual(
            claude.resolve_system_one_endpoint(env), "https://other.example/custom"
        )

    def test_unconfigured_call_fails_before_any_request(self) -> None:
        with mock.patch.object(claude.ratelimit, "gated_urlopen") as gated:
            with self.assertRaises(claude.SystemOneError):
                claude.judge_questions(
                    "state", {"a": {"type": "noul", "instructions": "x"}},
                    env={"EMBODIED_SYSTEM_ONE_URL": "", "EMBODIED_SYSTEM_ONE_API_KEY": ""},
                )
        gated.assert_not_called()

    def test_posts_state_and_questions_and_returns_answers(self) -> None:
        questions = {"2601.00001": {"type": "noul", "instructions": "claim"}}
        with mock.patch.object(
            claude.ratelimit, "gated_urlopen",
            return_value=self._response({
                "answers": {"2601.00001": {"noul": 0.91, "type": "noul"}},
                "model": "jev-1.14.0",
                "usage": {"input_tokens": 12, "output_tokens": 3},
            }),
        ) as gated:
            payload = claude.judge_questions("综述话题：X", questions, label="t")

        self.assertEqual(payload["answers"]["2601.00001"]["noul"], 0.91)
        request = gated.call_args.args[0]
        self.assertEqual(gated.call_args.kwargs["group"], "systemone")
        self.assertEqual(
            json.loads(request.data.decode("utf-8")),
            {"model": "jev-1.14.0", "state": "综述话题：X", "questions": questions},
        )
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")

    def test_transient_rejection_is_retried(self) -> None:
        reject = claude.urllib.error.HTTPError(
            "https://gw.example", 503, "unavailable", {}, None
        )
        ok = self._response({"answers": {"a": {"noul": 0.7}}, "usage": {}})
        with mock.patch.object(
            claude.ratelimit, "gated_urlopen", side_effect=[reject, ok]
        ) as gated:
            payload = claude.judge_questions(
                "s", {"a": {"type": "noul", "instructions": "c"}}
            )
        self.assertEqual(payload["answers"]["a"]["noul"], 0.7)
        self.assertEqual(gated.call_count, 2)

    def test_non_transient_rejection_is_not_retried(self) -> None:
        reject = claude.urllib.error.HTTPError(
            "https://gw.example", 400, "bad request", {}, None
        )
        with mock.patch.object(
            claude.ratelimit, "gated_urlopen", side_effect=reject
        ) as gated:
            with self.assertRaises(claude.SystemOneError):
                claude.judge_questions(
                    "s", {"a": {"type": "noul", "instructions": "c"}}
                )
        self.assertEqual(gated.call_count, 1)

    def test_usage_lands_in_the_inherited_ledger(self) -> None:
        ledger_path = Path(self._tmp.name) / "usage.jsonl"
        with mock.patch.dict(os.environ, {"EMBODIED_AGENT_LEDGER": str(ledger_path)}):
            with mock.patch.object(
                claude.ratelimit, "gated_urlopen",
                return_value=self._response({
                    "answers": {"a": {"noul": 0.7}},
                    "model": "jev-1.14.0",
                    "usage": {"input_tokens": 9, "output_tokens": 2},
                }),
            ):
                claude.judge_questions(
                    "s", {"a": {"type": "noul", "instructions": "c"}}, label="sel"
                )
        records = [
            json.loads(line)
            for line in ledger_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        usage = [r for r in records if r.get("type") == "assistant"]
        self.assertEqual(len(usage), 1)
        self.assertEqual(usage[0]["attrs"]["stage"], "sel")


if __name__ == "__main__":
    unittest.main()

"""Cross-process KB locks (embodied_learning/locks.py).

The lock is an append-only journal: one JSON line per acquire/release, the
holder reconstructed by replaying it. Never delete/create/rename — the three
operations a flaky CIFS share answers with ghost dentries. Tests run on a
plain temp dir (appends work the same as on a share). No flock anywhere; no
sub-millisecond race windows are asserted. Multi-process behavior is
exercised with real subprocesses since the point is cross-*process* exclusion.
"""

import importlib.util
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _REPO_ROOT / "embodied_learning" / "locks.py"
locks = importlib.import_module("embodied_learning.locks")


def _env(tmp: str) -> dict[str, str]:
    return {**os.environ, "EMBODIED_KB_LOCK_DIR": str(Path(tmp) / ".locks")}


def _seed_journal(path: Path, *records: dict) -> None:
    """Append legacy-style owner records (no ``op`` = a lone acquire)."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


class AcquireReleaseTest(unittest.TestCase):
    def test_round_trip_journals_acquire_then_release(self) -> None:
        """Release appends a release line and the holder goes away — the
        journal file itself is never deleted (that is the whole point)."""

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                with locks.kb_lock(tmp, "pool-index", detail="run-a"):
                    lock_file = Path(tmp) / ".locks" / "pool-index.lock"
                    record = locks.read_owner(lock_file)
                    self.assertEqual(record["name"], "pool-index")
                    self.assertEqual(record["pid"], os.getpid())
                    self.assertTrue(record["host"])
                    self.assertTrue(record["claim_id"])
                    self.assertEqual(record["detail"], "run-a")
                self.assertTrue(lock_file.exists())  # journal survives
                self.assertIsNone(locks.read_owner(lock_file))  # but unheld
                ops = [r.get("op") for r in locks._journal_events(lock_file)]
                self.assertEqual(ops, ["acquire", "release"])

    def test_second_thread_is_excluded_and_times_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                started = threading.Event()
                done = threading.Event()
                errors: list[Exception] = []

                def holder() -> None:
                    try:
                        with locks.kb_lock(tmp, "catalog"):
                            started.set()
                            done.wait(timeout=5)
                    except Exception as exc:  # noqa: BLE001
                        errors.append(exc)

                thread = threading.Thread(target=holder)
                thread.start()
                self.assertTrue(started.wait(timeout=5))
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "catalog", wait=0.3, poll=0.05):
                        pass
                done.set()
                thread.join(timeout=5)
                self.assertEqual(errors, [])

    def test_fail_fast_raises_lockbusy_with_owner_info(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                started = threading.Event()
                done = threading.Event()

                def holder() -> None:
                    with locks.kb_lock(tmp, "run__demo"):
                        started.set()
                        done.wait(timeout=5)

                thread = threading.Thread(target=holder)
                thread.start()
                self.assertTrue(started.wait(timeout=5))
                with self.assertRaises(locks.LockBusy) as ctx:
                    with locks.kb_lock(tmp, "run__demo", fail_fast=True):
                        pass
                self.assertIn("run__demo", str(ctx.exception))
                done.set()
                thread.join(timeout=5)

    def test_reentrant_same_thread_does_not_deadlock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                with locks.kb_lock(tmp, "pool-index"):
                    with locks.kb_lock(tmp, "pool-index"):  # nested: no self-deadlock
                        self.assertEqual(
                            locks.read_owner(Path(tmp) / ".locks" / "pool-index.lock")["pid"],
                            os.getpid(),
                        )
                self.assertIsNone(locks.read_owner(Path(tmp) / ".locks" / "pool-index.lock"))

    def test_sibling_thread_still_serializes_on_reentrant_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                started = threading.Event()
                done = threading.Event()
                errors: list[Exception] = []

                def sibling() -> None:
                    try:
                        with locks.kb_lock(tmp, "pool-index", wait=0.3, poll=0.05):
                            errors.append(AssertionError("sibling took the lock"))
                    except locks.LockTimeout:
                        pass
                    except Exception as exc:  # noqa: BLE001
                        errors.append(exc)

                with locks.kb_lock(tmp, "pool-index"):
                    with locks.kb_lock(tmp, "pool-index"):
                        thread = threading.Thread(target=sibling)
                        thread.start()
                        thread.join(timeout=5)
                self.assertEqual(errors, [])


class JournalStaleStealTest(unittest.TestCase):
    """A stale holder is superseded by appending a new acquire — never by
    unlinking the journal."""

    def _seed_stale(self, tmp: str, name: str, age: float) -> Path:
        lock_file = Path(tmp) / ".locks" / f"{name}.lock"
        _seed_journal(
            lock_file,
            {"name": name, "host": "ghost", "pid": 1, "ts": time.time() - age, "claim_id": "old"},
        )
        return lock_file

    def test_waiter_steals_stale_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = self._seed_stale(tmp, "pool-index", age=3600)
                with locks.kb_lock(tmp, "pool-index", stale=900, poll=0.05):
                    record = locks.read_owner(lock_file)
                    self.assertNotEqual(record["claim_id"], "old")
                # journal keeps the full trail — nothing is ever deleted
                events = locks._journal_events(lock_file)
                self.assertGreaterEqual(len(events), 3)  # old + our acquire + release

    def test_fresh_lock_is_not_stolen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                self._seed_stale(tmp, "pool-index", age=1.0)
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "pool-index", wait=0.3, stale=900, poll=0.05):
                        pass

    def test_dead_local_pid_steals_instantly_regardless_of_ttl(self) -> None:
        """A same-host holder whose pid is verifiably gone is a leftover lock:
        the waiter must not sit out the stale TTL."""

        exited = subprocess.Popen(["true"])
        exited.wait()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "wiki-publish.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "wiki-publish",
                        "host": socket.gethostname(),
                        "pid": exited.pid,
                        "ts": time.time(),  # brand new: TTL path must not apply
                        "claim_id": "dead-holder",
                    },
                )
                with locks.kb_lock(tmp, "wiki-publish", wait=1.0, stale=1800, poll=0.05):
                    record = locks.read_owner(lock_file)
                    self.assertNotEqual(record["claim_id"], "dead-holder")

    def test_alive_local_pid_is_not_stolen(self) -> None:
        alive = subprocess.Popen(["sleep", "30"])
        self.addCleanup(alive.kill)
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "x.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "x",
                        "host": socket.gethostname(),
                        "pid": alive.pid,
                        "ts": time.time(),
                        "claim_id": "live-holder",
                    },
                )
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "x", wait=0.3, stale=1800, poll=0.05):
                        pass

    def test_dead_pid_steals_even_fail_fast(self) -> None:
        """A crashed driver's run-lock must not block its own rerun for the
        full TTL: fail-fast still steals when the holder pid is dead."""

        exited = subprocess.Popen(["true"])
        exited.wait()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "run__demo.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "run__demo",
                        "host": socket.gethostname(),
                        "pid": exited.pid,
                        "ts": time.time(),
                        "claim_id": "dead-holder",
                    },
                )
                with locks.kb_lock(tmp, "run__demo", fail_fast=True, stale=1800):
                    record = locks.read_owner(lock_file)
                    self.assertNotEqual(record["claim_id"], "dead-holder")

    def test_remote_host_dead_pid_not_stolen(self) -> None:
        """Cross-machine holders cannot be probed — they age out via TTL only."""

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "x.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "x",
                        "host": "other-machine",
                        "pid": 999999,
                        "ts": time.time(),
                        "claim_id": "remote-holder",
                    },
                )
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "x", wait=0.3, stale=1800, poll=0.05):
                        pass

    def test_own_leftover_lock_is_stolen_instantly(self) -> None:
        """Release's append can fail on a flaky share; a leftover acquire with
        our own live pid must be reclaimable immediately (not wait out TTL)."""

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "pool-index.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "pool-index",
                        "host": socket.gethostname(),
                        "pid": os.getpid(),
                        "ts": time.time() - 3600,
                        "claim_id": "own-leftover",
                    },
                )
                with locks.kb_lock(tmp, "pool-index", wait=1.0, stale=1800, poll=0.05):
                    record = locks.read_owner(lock_file)
                    self.assertNotEqual(record["claim_id"], "own-leftover")

    def test_own_leftover_stolen_even_fail_fast(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "run__demo.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "run__demo",
                        "host": socket.gethostname(),
                        "pid": os.getpid(),
                        "ts": time.time() - 3600,
                        "claim_id": "own-leftover",
                    },
                )
                with locks.kb_lock(tmp, "run__demo", fail_fast=True, stale=1800):
                    record = locks.read_owner(lock_file)
                    self.assertNotEqual(record["claim_id"], "own-leftover")

    def test_release_journal_failure_is_reclaimed_on_next_take(self) -> None:
        """A failed release append leaves an unmatched acquire; our own pid
        makes it a leftover the next take reclaims instantly."""

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "pool-index.lock"
                _seed_journal(
                    lock_file,
                    {
                        "name": "pool-index",
                        "host": socket.gethostname(),
                        "pid": os.getpid(),
                        "ts": time.time(),
                        "claim_id": "leaked",
                    },
                )
                with locks.kb_lock(tmp, "pool-index", wait=1.0, stale=1800, poll=0.05):
                    record = locks.read_owner(lock_file)
                    self.assertNotEqual(record["claim_id"], "leaked")

    def test_empty_journal_is_free(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "wiki-chat-sessions.lock"
                lock_file.parent.mkdir(parents=True)
                lock_file.write_text("", encoding="utf-8")
                with locks.kb_lock(tmp, "wiki-chat-sessions", wait=1.5, poll=0.05):
                    record = locks.read_owner(lock_file)
                    self.assertTrue(record["claim_id"])


class JournalInternalsTest(unittest.TestCase):
    def test_journal_replay_resolves_holder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lock_file = Path(tmp) / "x.lock"
            _seed_journal(
                lock_file,
                {"op": "acquire", "claim_id": "a", "ts": 1.0, "host": "h", "pid": 1},
                {"op": "release", "claim_id": "a", "ts": 2.0, "host": "h", "pid": 1},
                {"op": "acquire", "claim_id": "b", "ts": 3.0, "host": "h", "pid": 2},
            )
            holder = locks.read_owner(lock_file)
            self.assertEqual(holder["claim_id"], "b")

    def test_legacy_single_object_reads_as_acquire(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lock_file = Path(tmp) / "x.lock"
            lock_file.write_text(json.dumps({"claim_id": "legacy", "ts": 1.0}), encoding="utf-8")
            holder = locks.read_owner(lock_file)
            self.assertEqual(holder["claim_id"], "legacy")

    def test_torn_trailing_line_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lock_file = Path(tmp) / "x.lock"
            _seed_journal(lock_file, {"op": "acquire", "claim_id": "ok", "ts": 1.0})
            with lock_file.open("a", encoding="utf-8") as handle:
                handle.write('{"op": "acquire", "clai')  # torn write
            holder = locks.read_owner(lock_file)
            self.assertEqual(holder["claim_id"], "ok")

    def test_journal_file_is_never_deleted(self) -> None:
        """The design invariant: release appends, it does not unlink."""
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "pool-index.lock"
                for _ in range(3):
                    with locks.kb_lock(tmp, "pool-index", poll=0.01):
                        self.assertTrue(lock_file.exists())
                self.assertTrue(lock_file.exists())
                events = locks._journal_events(lock_file)
                self.assertEqual([r.get("op") for r in events], ["acquire", "release"] * 3)


class MultiProcessTest(unittest.TestCase):
    """Real cross-process exclusion — the whole reason this exists."""

    def test_two_processes_serialize(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = {**os.environ, **_env(tmp), "PYTHONPATH": str(_REPO_ROOT)}
            script = (
                "import sys, time, os\n"
                f"sys.path.insert(0, {str(_REPO_ROOT)!r})\n"
                "from embodied_learning import locks\n"
                f"with locks.kb_lock({tmp!r}, 'shared', wait=10, poll=0.05):\n"
                f"    with open(os.path.join({tmp!r}, 'log.txt'), 'a') as f:\n"
                "        f.write('enter %d\\n' % os.getpid())\n"
                "        time.sleep(0.3)\n"
                "        f.write('exit %d\\n' % os.getpid())\n"
            )
            procs = [
                subprocess.Popen([sys.executable, "-c", script], env=env)
                for _ in range(2)
            ]
            for proc in procs:
                self.assertEqual(proc.wait(timeout=20), 0)
            lines = Path(tmp, "log.txt").read_text().splitlines()
            self.assertEqual(len(lines), 4)
            # enter/exit must nest, never interleave
            self.assertEqual(lines[0].split()[0], "enter")
            self.assertEqual(lines[1].split()[0], "exit")
            self.assertEqual(lines[2].split()[0], "enter")
            self.assertEqual(lines[3].split()[0], "exit")
            self.assertEqual(lines[0].split()[1], lines[1].split()[1])
            self.assertEqual(lines[2].split()[1], lines[3].split()[1])
            self.assertNotEqual(lines[0].split()[1], lines[2].split()[1])


if __name__ == "__main__":
    unittest.main()

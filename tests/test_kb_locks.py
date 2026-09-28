"""Cross-process KB locks (embodied_learning/locks.py).

The primitives rely only on O_EXCL creation and same-directory unlink, which
tmpfs honors with the same server-side semantics as a CIFS share — so tests
run on a plain temp dir. No flock anywhere; no sub-millisecond race windows
are asserted (CIFS round trips are milliseconds). Multi-process behavior is
exercised with real subprocesses since the point is cross-*process* exclusion.
"""

import importlib.util
import json
import os
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
_spec = importlib.util.spec_from_file_location("locks_test_module", _SCRIPT)
locks = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(locks)


def _env(tmp: str) -> dict[str, str]:
    return {**os.environ, "EMBODIED_KB_LOCK_DIR": str(Path(tmp) / ".locks")}


def _utime(path: Path, ts: float) -> None:
    os.utime(path, (ts, ts))


def _touch_owner(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record), encoding="utf-8")


class AcquireReleaseTest(unittest.TestCase):
    def test_round_trip_writes_and_removes_owner_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                with locks.kb_lock(tmp, "pool-index", detail="run-a"):
                    lock_file = Path(tmp) / ".locks" / "pool-index.lock"
                    record = json.loads(lock_file.read_text(encoding="utf-8"))
                    self.assertEqual(record["name"], "pool-index")
                    self.assertEqual(record["pid"], os.getpid())
                    self.assertTrue(record["host"])
                    self.assertTrue(record["claim_id"])
                    self.assertEqual(record["detail"], "run-a")
                self.assertFalse(lock_file.exists())

    def test_second_thread_is_excluded_and_times_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                started = threading.Event()
                release = threading.Event()

                def holder() -> None:
                    with locks.kb_lock(tmp, "catalog"):
                        started.set()
                        release.wait(10)

                thread = threading.Thread(target=holder)
                thread.start()
                self.assertTrue(started.wait(10))
                try:
                    with self.assertRaises(locks.LockTimeout):
                        with locks.kb_lock(tmp, "catalog", wait=0.3, poll=0.05):
                            pass
                finally:
                    release.set()
                    thread.join(10)

    def test_fail_fast_raises_lockbusy_with_owner_info(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                started = threading.Event()
                release = threading.Event()

                def holder() -> None:
                    with locks.kb_lock(tmp, "run__demo"):
                        started.set()
                        release.wait(10)

                thread = threading.Thread(target=holder)
                thread.start()
                self.assertTrue(started.wait(10))
                try:
                    with self.assertRaises(locks.LockBusy) as ctx:
                        with locks.kb_lock(tmp, "run__demo", fail_fast=True):
                            pass
                    self.assertIn(str(os.getpid()), str(ctx.exception))
                    self.assertIn("重复启动", str(ctx.exception))
                finally:
                    release.set()
                    thread.join(10)

    def test_reentrant_same_thread_does_not_deadlock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                with locks.kb_lock(tmp, "pool-index"):
                    with locks.kb_lock(tmp, "pool-index"):  # nested: no self-deadlock
                        pass
                self.assertFalse((Path(tmp) / ".locks" / "pool-index.lock").exists())

    def test_sibling_thread_still_serializes_on_reentrant_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                depth_seen: list[int] = []
                started = threading.Event()
                release = threading.Event()

                def holder() -> None:
                    with locks.kb_lock(tmp, "pool-index"):
                        with locks.kb_lock(tmp, "pool-index"):
                            depth_seen.append(2)
                            started.set()
                            release.wait(10)

                thread = threading.Thread(target=holder)
                thread.start()
                self.assertTrue(started.wait(10))
                try:
                    with self.assertRaises(locks.LockTimeout):
                        with locks.kb_lock(tmp, "pool-index", wait=0.2, poll=0.05):
                            pass
                finally:
                    release.set()
                    thread.join(10)
                self.assertEqual(depth_seen, [2])


class StaleStealTest(unittest.TestCase):
    def _write_stale_lock(self, tmp: str, name: str, age: float) -> Path:
        lock_file = Path(tmp) / ".locks" / f"{name}.lock"
        _touch_owner(
            lock_file,
            {"name": name, "host": "ghost", "pid": 1, "ts": time.time() - age, "claim_id": "old"},
        )
        _utime(lock_file, time.time() - age)
        return lock_file

    def test_waiter_steals_stale_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = self._write_stale_lock(tmp, "pool-index", age=3600)
                with locks.kb_lock(tmp, "pool-index", stale=900, poll=0.05):
                    record = json.loads(lock_file.read_text(encoding="utf-8"))
                    self.assertNotEqual(record["claim_id"], "old")

    def test_fresh_lock_is_not_stolen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                self._write_stale_lock(tmp, "pool-index", age=1.0)
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "pool-index", wait=0.3, stale=900, poll=0.05):
                        pass

    def test_fresh_steal_marker_prevents_double_steal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = self._write_stale_lock(tmp, "pool-index", age=3600)
                marker = lock_file.with_name(lock_file.name + locks.STEAL_SUFFIX)
                marker.write_text("", encoding="utf-8")
                _utime(marker, time.time())  # fresh marker: another waiter is mid-steal
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "pool-index", wait=0.3, stale=900, poll=0.05):
                        pass

    def test_stale_steal_marker_is_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = self._write_stale_lock(tmp, "pool-index", age=3600)
                marker = lock_file.with_name(lock_file.name + locks.STEAL_SUFFIX)
                marker.write_text("", encoding="utf-8")
                _utime(marker, time.time() - 3600)  # its creator died mid-steal
                with locks.kb_lock(tmp, "pool-index", stale=900, poll=0.05):
                    pass
                self.assertFalse(marker.exists())
                self.assertFalse(lock_file.exists())

    def test_unreadable_record_stolen_after_grace(self) -> None:
        """0-byte / corrupt owner record (crash between O_EXCL create and
        record-write, or CIFS leftover): reclaim after the grace period —
        this is the only path a '未知持有者' lock ever clears."""
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "wiki-chat-sessions.lock"
                lock_file.parent.mkdir(parents=True)
                lock_file.write_text("", encoding="utf-8")  # 0 bytes, no record
                _utime(lock_file, time.time() - 120)
                with locks.kb_lock(tmp, "wiki-chat-sessions", wait=1.0, stale=900, poll=0.05):
                    record = json.loads(lock_file.read_text(encoding="utf-8"))
                    self.assertTrue(record["claim_id"])

    def test_garbage_record_stolen_after_grace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "x.lock"
                lock_file.parent.mkdir(parents=True)
                lock_file.write_bytes(b'\x00\x01 {"truncated": not-json')  # corrupt record
                _utime(lock_file, time.time() - 120)
                with locks.kb_lock(tmp, "x", wait=1.0, stale=900, poll=0.05):
                    pass

    def test_unreadable_streak_clears_cache_lie_without_ghost_marker(self) -> None:
        """The NAS lies in more shapes than nlink=0: stat may say ENOENT or
        report nlink=1 for an entry that cannot be opened. After a short
        streak of unreadable records past EEXIST, the waiter unlinks
        unconditionally — a live holder (record written in ms) never
        accumulates the streak, so this cannot steal a real lock."""
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "x.lock"
                lock_file.parent.mkdir(parents=True)
                lock_file.write_text("garbage", encoding="utf-8")
                os.chmod(lock_file, 0o000)  # unreadable like the ghost's ENOENT
                self.addCleanup(lambda: os.chmod(lock_file, 0o644) if lock_file.exists() else None)
                with mock.patch.object(locks, "_is_ghost_dentry", return_value=False):
                    with locks.kb_lock(tmp, "x", wait=5, poll=0.05):
                        record = json.loads(lock_file.read_text(encoding="utf-8"))
                        self.assertTrue(record["claim_id"])

    def test_ghost_dentry_is_cleared_and_retry_hits_server(self) -> None:
        """Flaky-NAS ghost: O_EXCL keeps answering EEXIST from the client
        cache while reads say ENOENT (record unreadable → holder None), and
        st_nlink==0 marks the dying inode. The waiter must unlink (dropping
        the cached dentry) and immediately retry — not wait out any grace.
        tmpfs cannot produce nlink=0, so the judge is mocked; the unreadable
        record stands in for the ENOENT read, and the wiring (clear →
        immediate retry → acquire) runs for real."""

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "wiki-chat-sessions.lock"
                lock_file.parent.mkdir(parents=True)
                lock_file.write_text("would-be-record", encoding="utf-8")
                os.chmod(lock_file, 0o000)  # read fails like the ghost's ENOENT
                self.addCleanup(lambda: os.chmod(lock_file, 0o644) if lock_file.exists() else None)
                with mock.patch.object(locks, "_is_ghost_dentry", side_effect=[True, False]):
                    with locks.kb_lock(tmp, "wiki-chat-sessions", wait=5, poll=0.05):
                        # The ghost was cleared; we own a fresh, readable lock.
                        record = json.loads(lock_file.read_text(encoding="utf-8"))
                        self.assertTrue(record["claim_id"])

    def test_is_ghost_dentry_false_for_real_and_missing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / "real.lock"
            real.write_text("x", encoding="utf-8")
            self.assertFalse(locks._is_ghost_dentry(real))
            self.assertFalse(locks._is_ghost_dentry(Path(tmp) / "missing.lock"))

    def test_unreadable_grace_is_bounded_by_caller_wait(self) -> None:
        """The reclaim must fire BEFORE the waiter's own timeout — the exact
        trap that bit wiki-publish (wait 600 < stale 1800) and chat-sessions
        (wait 30 < grace 60)."""
        self.assertEqual(locks._unreadable_grace(30, 900, 1.0), 30)  # wait-bound
        self.assertEqual(locks._unreadable_grace(600, 1800, 1.0), 60)  # grace-capped
        self.assertEqual(locks._unreadable_grace(120, 900, 1.0), 60)
        self.assertEqual(locks._unreadable_grace(0.5, 900, 0.05), 0.5)
        self.assertEqual(locks._unreadable_grace(0.01, 900, 0.05), 0.1)  # 2-poll floor

    def test_unreadable_record_reclaimed_before_wait_expiry(self) -> None:
        """A brand-new unreadable record (fresh 0-byte leftover / ghost dentry)
        is reclaimed within the caller's wait, not after a fixed grace."""
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "wiki-chat-sessions.lock"
                lock_file.parent.mkdir(parents=True)
                lock_file.write_text("", encoding="utf-8")
                with locks.kb_lock(tmp, "wiki-chat-sessions", wait=1.5, poll=0.05):
                    record = json.loads(lock_file.read_text(encoding="utf-8"))
                    self.assertTrue(record["claim_id"])

    def test_dead_local_pid_steals_instantly_regardless_of_ttl(self) -> None:
        """A same-host holder whose pid is verifiably gone is a leftover lock:
        the waiter must not sit out the stale TTL (the wiki-publish incident:
        wait 600s < stale 1800s timed out before the steal could fire)."""
        import socket

        # A real exited process: its pid is guaranteed not to come back.
        exited = subprocess.Popen(["true"])
        exited.wait()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "wiki-publish.lock"
                _touch_owner(
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
                    record = json.loads(lock_file.read_text(encoding="utf-8"))
                    self.assertNotEqual(record["claim_id"], "dead-holder")

    def test_alive_local_pid_is_not_stolen(self) -> None:
        import socket

        alive = subprocess.Popen(["sleep", "30"])
        self.addCleanup(alive.kill)
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "x.lock"
                _touch_owner(
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
        full 6h TTL: fail-fast still steals when the holder pid is dead."""
        import socket

        exited = subprocess.Popen(["true"])
        exited.wait()
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "run__demo.lock"
                _touch_owner(
                    lock_file,
                    {
                        "name": "run__demo",
                        "host": socket.gethostname(),
                        "pid": exited.pid,
                        "ts": time.time(),
                        "claim_id": "dead-driver",
                    },
                )
                with locks.kb_lock(tmp, "run__demo", fail_fast=True, stale=21600):
                    record = json.loads(lock_file.read_text(encoding="utf-8"))
                    self.assertNotEqual(record["claim_id"], "dead-driver")

    def test_remote_host_dead_pid_not_stolen(self) -> None:
        """Cross-machine holders cannot be probed: same pid value but a
        foreign host must wait for the TTL."""
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                lock_file = Path(tmp) / ".locks" / "x.lock"
                _touch_owner(
                    lock_file,
                    {"name": "x", "host": "some-other-machine", "pid": 999999999, "ts": time.time()},
                )
                _utime(lock_file, time.time())
                with self.assertRaises(locks.LockTimeout):
                    with locks.kb_lock(tmp, "x", wait=0.3, stale=1800, poll=0.05):
                        pass

    def test_release_with_foreign_claim_id_does_not_unlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lock_file = Path(tmp) / ".locks" / "pool-index.lock"
            _touch_owner(lock_file, {"claim_id": "someone-else", "ts": time.time()})
            entry = locks._Entry()
            entry.claim_id = "mine"
            locks._release(lock_file, entry)
            self.assertTrue(lock_file.exists())

    def test_release_without_claim_id_never_unlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lock_file = Path(tmp) / ".locks" / "pool-index.lock"
            _touch_owner(lock_file, {"claim_id": "someone-else"})
            entry = locks._Entry()
            locks._release(lock_file, entry)  # failed-acquisition path
            self.assertTrue(lock_file.exists())


class ClaimTest(unittest.TestCase):
    def test_first_wins_second_loses_then_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                self.assertTrue(locks.claim(tmp, "event-prefix/EA-DEMO-2026", {"run": "run-a"}))
                self.assertFalse(locks.claim(tmp, "event-prefix/EA-DEMO-2026", {"run": "run-b"}))
                claim_file = Path(tmp) / ".claims" / "event-prefix" / "EA-DEMO-2026.json"
                record = json.loads(claim_file.read_text(encoding="utf-8"))
                self.assertEqual(record["run"], "run-a")
                self.assertTrue(record["claim_id"])
                locks.release_claim(tmp, "event-prefix/EA-DEMO-2026", claim_id=record["claim_id"])
                self.assertFalse(claim_file.exists())
                self.assertTrue(locks.claim(tmp, "event-prefix/EA-DEMO-2026", {"run": "run-b"}))

    def test_release_refuses_mismatched_claim_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                locks.claim(tmp, "event-prefix/P", {"run": "run-a"})
                locks.release_claim(tmp, "event-prefix/P", claim_id="not-mine")
                self.assertTrue((Path(tmp) / ".claims" / "event-prefix" / "P.json").exists())

    def test_ttl_takeover_of_stale_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict("os.environ", _env(tmp)):
                claim_file = Path(tmp) / ".claims" / "event-prefix" / "OLD.json"
                old = time.time() - 7200
                _touch_owner(claim_file, {"run": "ghost", "ts": old, "claim_id": "old-id"})
                _utime(claim_file, old)
                self.assertTrue(locks.claim(tmp, "event-prefix/OLD", {"run": "new"}, ttl=3600))
                self.assertEqual(json.loads(claim_file.read_text(encoding="utf-8"))["run"], "new")


class EnvKnobsTest(unittest.TestCase):
    def test_lock_dir_redirect(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            custom = Path(tmp) / "elsewhere"
            with mock.patch.dict("os.environ", {"EMBODIED_KB_LOCK_DIR": str(custom)}):
                self.assertEqual(locks.locks_dir("/any/root"), custom)
                with locks.kb_lock("/any/root", "x"):
                    self.assertTrue((custom / "x.lock").exists())

    def test_disabled_is_full_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(_env(tmp), EMBODIED_KB_LOCKS_DISABLED="1")
            with mock.patch.dict("os.environ", env):
                with locks.kb_lock(tmp, "x"):
                    pass
                lock_dir = Path(tmp) / ".locks"
                self.assertFalse(lock_dir.exists() and list(lock_dir.glob("*")))
                self.assertTrue(locks.claim(tmp, "y", {}))


class MultiProcessTest(unittest.TestCase):
    """Real subprocess contention: the whole point is cross-process exclusion."""

    HELPER_HOLD = """
import sys, time
sys.path.insert(0, {repo_root!r})
from embodied_learning import locks
root, name = sys.argv[1], sys.argv[2]
with locks.kb_lock(root, name, detail="child"):
    print("HELD", flush=True)
    time.sleep(float(sys.argv[3]))
print("DONE", flush=True)
"""

    def _spawn_holder(self, root: str, name: str, hold: float, env: dict) -> subprocess.Popen:
        return subprocess.Popen(
            [
                sys.executable,
                "-c",
                self.HELPER_HOLD.format(repo_root=str(_REPO_ROOT)),
                root,
                name,
                str(hold),
            ],
            stdout=subprocess.PIPE,
            text=True,
            env=env,
        )

    def test_parent_waits_for_child_then_acquires(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = _env(tmp)
            child = self._spawn_holder(tmp, "pool-index", 1.5, env)
            try:
                self.assertEqual(child.stdout.readline().strip(), "HELD")
                begin = time.monotonic()
                with mock.patch.dict("os.environ", env):
                    with locks.kb_lock(tmp, "pool-index", wait=30, poll=0.1):
                        self.assertGreaterEqual(time.monotonic() - begin, 1.0)
            finally:
                child.wait(60)

    def test_fail_fast_errors_while_child_holds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = _env(tmp)
            holder = self._spawn_holder(tmp, "run__demo", 1.2, env)
            try:
                self.assertEqual(holder.stdout.readline().strip(), "HELD")
                with mock.patch.dict("os.environ", env):
                    with self.assertRaises(locks.LockBusy):
                        with locks.kb_lock(tmp, "run__demo", fail_fast=True):
                            pass
            finally:
                holder.wait(60)


if __name__ == "__main__":
    unittest.main()

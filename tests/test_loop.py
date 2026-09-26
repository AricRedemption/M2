"""tests/test_loop.py -- loop system: goal_check router, marathon_guard, direction_gate.

The loop scripts (scripts/goal_check, scripts/marathon_guard,
scripts/direction_gate) operate on the repo root by default but accept an
M2_LOOP_ROOT override; every test fabricates a minimal loop workspace in a
tmp dir and drives the real scripts end-to-end through subprocess.
"""
import json
import os
import subprocess
import sys
import time

import pytest

SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))

GOAL_CHECK = os.path.join(SCRIPTS, "goal_check")
MARATHON_GUARD = os.path.join(SCRIPTS, "marathon_guard")
DIRECTION_GATE = os.path.join(SCRIPTS, "direction_gate")

GOALS_TEMPLATE = """# GOALS.md — 程序计数器

```yaml
state: RUNNING
mode: {mode}
current_action: test
```

```yaml
goal_queue:
{queue}
```
"""


def make_root(tmp_path, queue, mode="ON"):
    root = tmp_path / "repo"
    loop = root / "docs" / "loop"
    loop.mkdir(parents=True)
    (loop / "GOALS.md").write_text(GOALS_TEMPLATE.format(mode=mode, queue=queue), encoding="utf-8")
    return root


def run(script, root, *args):
    env = dict(os.environ, M2_LOOP_ROOT=str(root))
    return subprocess.run(
        [sys.executable, script, *args], env=env,
        capture_output=True, text=True, timeout=60,
    )


def read_goals(root):
    return (root / "docs" / "loop" / "GOALS.md").read_text(encoding="utf-8")


def entry(id_, check_cmd, status="todo"):
    return (
        f"  - id: {id_}\n"
        f"    goal: {id_} goal\n"
        f"    done_condition: {id_} done\n"
        f"    check_cmd: {check_cmd}\n"
        f"    status: {status}\n"
    )


class TestGoalCheckRouter:
    def test_not_achieved_keeps_queue(self, tmp_path):
        root = make_root(tmp_path, entry("a", "false") + entry("b", "true"))
        r = run(GOAL_CHECK, root)
        assert r.returncode == 1
        assert "NOT-Achieved" in r.stdout
        assert "- id: a" in read_goals(root) and "- id: b" in read_goals(root)

    def test_achieved_pops_first_and_promotes(self, tmp_path):
        root = make_root(tmp_path, entry("a", "true") + entry("b", "false"))
        r = run(GOAL_CHECK, root)
        assert r.returncode == 0
        assert "ACHIEVED" in r.stdout and "b" in r.stdout
        body = read_goals(root)
        assert "- id: a" not in body
        assert "- id: b" in body
        assert "```yaml" in body and "state: RUNNING" in body

    def test_achieved_on_single_entry_empties_queue(self, tmp_path):
        root = make_root(tmp_path, entry("only", "true"))
        r = run(GOAL_CHECK, root)
        assert r.returncode == 0
        assert "- id:" not in read_goals(root)

    def test_queue_empty(self, tmp_path):
        root = make_root(tmp_path, "")
        r = run(GOAL_CHECK, root)
        assert r.returncode == 2
        assert "QUEUE-EMPTY" in r.stdout

    def test_mode_off_refuses(self, tmp_path):
        root = make_root(tmp_path, entry("a", "true"), mode="OFF")
        r = run(GOAL_CHECK, root)
        assert r.returncode == 5
        assert "MODE-OFF" in r.stdout

    def test_heartbeat_touches_lock(self, tmp_path):
        root = make_root(tmp_path, entry("a", "false"))
        assert not (root / ".loop-lock").exists()
        run(GOAL_CHECK, root)
        assert (root / ".loop-lock").exists()


class TestGoalCheckAudit:
    def test_healthy_queue(self, tmp_path):
        root = make_root(tmp_path, entry("a", "true") + entry("b", "false"))
        r = run(GOAL_CHECK, root, "--audit")
        assert r.returncode == 0
        assert "2 条目全部健康" in r.stdout

    def test_duplicate_id_detected(self, tmp_path):
        root = make_root(tmp_path, entry("a", "true") + entry("a", "false"))
        r = run(GOAL_CHECK, root, "--audit")
        assert r.returncode == 1
        assert "重复条目 id" in r.stdout

    def test_missing_check_cmd_detected(self, tmp_path):
        queue = "  - id: a\n    goal: a\n    status: todo\n"
        root = make_root(tmp_path, queue)
        r = run(GOAL_CHECK, root, "--audit")
        assert r.returncode == 1
        assert "check_cmd 缺失/空" in r.stdout

    def test_missing_queue_block_detected(self, tmp_path):
        root = tmp_path / "repo"
        loop = root / "docs" / "loop"
        loop.mkdir(parents=True)
        (loop / "GOALS.md").write_text("# no queue here\n", encoding="utf-8")
        r = run(GOAL_CHECK, root, "--audit")
        assert r.returncode == 1
        assert "未找到 goal_queue" in r.stdout


class TestMarathonGuard:
    def test_no_lock_is_clear(self, tmp_path):
        root = make_root(tmp_path, "")
        r = run(MARATHON_GUARD, root)
        assert r.returncode == 0

    def test_fresh_lock_is_busy(self, tmp_path):
        root = make_root(tmp_path, "")
        (root / ".loop-lock").write_text(str(int(time.time())))
        r = run(MARATHON_GUARD, root)
        assert r.returncode == 1
        assert "BUSY" in r.stdout

    def test_expired_lock_is_clear(self, tmp_path):
        root = make_root(tmp_path, "")
        lock = root / ".loop-lock"
        lock.write_text("0")
        old = time.time() - 200 * 60
        os.utime(lock, (old, old))
        r = run(MARATHON_GUARD, root)
        assert r.returncode == 0
        assert "自过期" in r.stdout


class TestDirectionGate:
    def test_add_then_check_round_passes(self, tmp_path):
        root = make_root(tmp_path, "")
        r = run(DIRECTION_GATE, root, "--add", "--round", "3",
                "--direction", "四轴耦合: reasoning", "--evidence", "tests 全绿")
        assert r.returncode == 0
        r = run(DIRECTION_GATE, root, "--check-round", "3")
        assert r.returncode == 0
        lines = (root / "docs" / "loop" / "direction-gate.jsonl").read_text().strip().splitlines()
        assert json.loads(lines[-1])["round"] == 3

    def test_check_round_mismatch_fails(self, tmp_path):
        root = make_root(tmp_path, "")
        run(DIRECTION_GATE, root, "--add", "--round", "2",
            "--direction", "d", "--evidence", "e")
        r = run(DIRECTION_GATE, root, "--check-round", "3")
        assert r.returncode == 1
        assert "轮号" in r.stdout

    def test_check_round_on_empty_ledger_fails(self, tmp_path):
        root = make_root(tmp_path, "")
        r = run(DIRECTION_GATE, root, "--check-round", "1")
        assert r.returncode == 1

    def test_add_requires_all_fields(self, tmp_path):
        root = make_root(tmp_path, "")
        r = run(DIRECTION_GATE, root, "--add", "--round", "1",
                "--direction", "", "--evidence", "e")
        assert r.returncode != 0

    def test_drift_streak_warns(self, tmp_path):
        root = make_root(tmp_path, "")
        for i in range(2):
            run(DIRECTION_GATE, root, "--add", "--round", str(i + 1),
                "--direction", "DRIFT", "--evidence", "e")
        r = run(DIRECTION_GATE, root, "--add", "--round", "3",
                "--direction", "DRIFT", "--evidence", "e")
        assert r.returncode == 0
        assert "BLOCKED-HUMAN" in r.stdout


@pytest.mark.parametrize("script", [GOAL_CHECK, MARATHON_GUARD, DIRECTION_GATE])
def test_scripts_are_executable(script):
    assert os.access(script, os.X_OK), f"{script} 缺少可执行位"

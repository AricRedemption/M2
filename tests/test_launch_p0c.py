"""tests/test_launch_p0c.py — launch_p0c.sh 控制流门(2026-09-28 事故工程硬化)

不跑真实训练(桩进程模拟 runner 写 canonical 行),钉住 launcher 三重卫生中
可自动验证的两条:
  1. 幂等重入:canonical jsonl 已有 (tag, seed) 行 ⇒ 重跑跳过该 seed;
  2. 双开防护:pidfile 指向活进程 ⇒ 拒绝点火(退出码 1)。
caffeinate 包装与 MPS 真实训练属人工验收项,不在本文件。
canonical jsonl 是真实实验数据:测试行带专用 tag,fixture 前后清理。
"""

import json
import os
import subprocess

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LAUNCHER = os.path.join(ROOT, "scripts", "launch_p0c.sh")
STUB = os.path.join(ROOT, "tests", "fixtures", "fake_p0c_runner.py")
RESULTS = os.path.join(ROOT, "benchmarks", "results", "reasoning_depth.jsonl")
TAG = "t_launch_p0c_test"


def _lines():
    if not os.path.exists(RESULTS):
        return []
    return [ln for ln in open(RESULTS, encoding="utf-8").read().splitlines()
            if ln.strip()]


def _purge_test_rows():
    """只删本测试写入的行;不可解析的行原样保留(数据纪律:不动他人数据)。"""
    if not os.path.exists(RESULTS):
        return
    keep = []
    for ln in _lines():
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            keep.append(ln)
            continue
        if r.get("tag") != TAG:
            keep.append(ln)
    with open(RESULTS, "w", encoding="utf-8") as f:
        f.write("".join(l + "\n" for l in keep))


@pytest.fixture(autouse=True)
def _clean_canonical():
    _purge_test_rows()
    yield
    _purge_test_rows()


def _env(tmp_path):
    return {**os.environ,
            "P0C_PYTHON": STUB,
            "P0C_TAG": TAG,
            "P0C_LOG": str(tmp_path / "launcher.log"),
            "P0C_PIDFILE": str(tmp_path / "launcher.pid")}


def _tag_rows():
    return [json.loads(ln) for ln in _lines()
            if json.loads(ln).get("tag") == TAG]


def test_rerun_skips_completed_seeds(tmp_path):
    """首跑写 2 行;重跑全跳过,不再新增(中断后重跑=免费续跑)。"""
    env = _env(tmp_path)
    r1 = subprocess.run([LAUNCHER, "0", "1"], env=env,
                        capture_output=True, text=True, cwd=ROOT)
    assert r1.returncode == 0, r1.stderr
    rows = _tag_rows()
    assert sorted(r["seed"] for r in rows) == [0, 1]
    assert all(r.get("stub") for r in rows)
    # pidfile 收尾清理
    assert not os.path.exists(env["P0C_PIDFILE"])
    log1 = open(env["P0C_LOG"], encoding="utf-8").read()
    assert log1.count("start") == 2 and "rc=0" in log1

    r2 = subprocess.run([LAUNCHER, "0", "1"], env=env,
                        capture_output=True, text=True, cwd=ROOT)
    assert r2.returncode == 0, r2.stderr
    assert len(_tag_rows()) == 2, "重跑必须跳过已有 canonical 行的 seed"
    log2 = open(env["P0C_LOG"], encoding="utf-8").read()
    assert log2.count("跳过") == 2


def test_refuses_double_launch(tmp_path):
    """活 pid 在 ⇒ 拒绝点火(2026-09-28 之后不再允许双开踩踏)。"""
    env = _env(tmp_path)
    pidfile = env["P0C_PIDFILE"]
    os.makedirs(os.path.dirname(pidfile), exist_ok=True)
    with open(pidfile, "w") as f:
        f.write(str(os.getpid()))  # pytest 进程本身=活进程
    try:
        r = subprocess.run([LAUNCHER, "0"], env=env,
                           capture_output=True, text=True, cwd=ROOT)
        assert r.returncode == 1
        assert "不双开" in (r.stdout + r.stderr)
        assert _tag_rows() == [], "拒绝点火时不得写入任何行"
    finally:
        os.remove(pidfile)

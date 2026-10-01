"""tests/test_reasoning_depth_incremental.py — 增量落盘回归门（2026-09-28 事故）

事故形态:P0-C′ 训练腿 18.5h 被杀,3 个已完成 depth-run 的 eval 只存在于
stdout 日志——canonical jsonl 只在进程退出时批量写,零机器可读数据落盘。
本文件钉住两件事:
  1. 每个 depth-run / transformer eval 完成即写 partial 台账(fsync);
  2. 每个 seed 完成即写 canonical 行;中途死亡最多丢“当前进行中的
     depth-run”的信息,已完成的一律在盘。
"""

import json

import pytest

torch = pytest.importorskip("torch")

import benchmarks.reasoning_depth as rd  # noqa: E402


def _paths(tmp_path):
    results = tmp_path / "reasoning_depth.jsonl"
    partials = tmp_path / "reasoning_depth.partial.jsonl"
    monkey_target = pytest.MonkeyPatch()
    monkey_target.setattr(rd, "RESULTS", str(results))
    monkey_target.setattr(rd, "PARTIALS", str(partials))
    return results, partials, monkey_target


def _read(path):
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text().splitlines() if ln.strip()]


def test_happy_path_flushes_partial_then_canonical(tmp_path):
    """整跑完成:partials 每 depth 一行 + canonical 每 seed 一行。"""
    results, partials, mp = _paths(tmp_path)
    try:
        rd.run_fixed_sweep(
            "pointer_chase", difficulty=2, n_values=8, seeds=[0],
            steps=3, batch=8, lr=3e-4, depths=[1, 2], device="cpu",
            tag="test_incr", skip_transformer=True, mix=True)
    finally:
        mp.undo()

    prows = _read(partials)
    depths_seen = sorted(r["depth"] for r in prows
                         if r["kind"] == "depth_run_partial")
    assert depths_seen == [1, 2], "每个 depth-run 评估完成必须立即落 partial"
    for r in prows:
        assert r["tag"] == "test_incr" and r["seed"] == 0
        assert "acc" in r and "ts" in r

    crows = _read(results)
    assert len(crows) == 1, "seed 完成即写 canonical 行"
    assert crows[0]["tag"] == "test_incr"
    assert set(crows[0]["mtlnn_acc_by_depth"].keys()) == {"1", "2"}
    assert crows[0]["transformer_acc"] is None  # skip_transformer=True


def test_kill_mid_depth_2_keeps_depth_1(tmp_path):
    """2026-09-28 事故回归:depth 2 训练中死亡,depth 1 的 eval 必须在盘,
    canonical 行(按 seed 粒度)正确地尚未写出。"""
    results, partials, mp = _paths(tmp_path)
    orig_train = rd.train_model
    calls = {"n": 0}

    def train_then_die(*a, **kw):
        calls["n"] += 1
        if calls["n"] >= 2:
            raise RuntimeError("simulated kill (2026-09-28 incident)")
        return orig_train(*a, **kw)

    try:
        with pytest.raises(RuntimeError):
            mp.setattr(rd, "train_model", train_then_die)
            rd.run_fixed_sweep(
                "pointer_chase", difficulty=2, n_values=8, seeds=[0],
                steps=3, batch=8, lr=3e-4, depths=[1, 2], device="cpu",
                tag="test_kill", skip_transformer=True, mix=True)
    finally:
        mp.undo()

    prows = _read(partials)
    assert [r["depth"] for r in prows] == [1], \
        "死亡前的 depth-run 评估必须已在 partial 台账"
    assert not results.exists(), \
        "seed 未完成,canonical 行不得提前写出(口径纯净性)"

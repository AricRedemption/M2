#!/usr/bin/env bash
# launch_p0c.sh — P0-C′ 训练腿发射器(2026-10-01 轮 6 工程硬化)
#
# 背景:2026-09-28 事故——18.5h 训练随机器关机全损,无 checkpoint、无增量
# 落盘、无点火排程,循环静默停摆 3.5 天。本脚本三重卫生:
#   1. caffeinate 防睡眠:机器睡眠/关机=进程死,事故根因之一;
#   2. 每 seed 一次调用:预注册 protocol.runner 本意(单点死亡只损失一条腿,
#      不再是整个 3-seed sweep);
#   3. 幂等重入:canonical jsonl 已有 (tag=p0c_prime, seed=S) 行即跳过该
#      seed——任何中断后直接重跑本脚本即可续跑缺失的腿。
#   依赖:reasoning_depth.py 增量落盘(每个 depth-run eval 完成即写
#   partial 台账,死亡最多丢"进行中"的那一个 depth-run)。
#
# 测试/干跑旋钮(默认=预注册协议原样):
#   P0C_DEVICE=cpu P0C_STEPS=2 P0C_DEPTHS="1 2" P0C_TAG=p0c_smoke_test \
#     ./scripts/launch_p0c.sh 0
set -uo pipefail
cd "$(dirname "$0")/.."

PY=${P0C_PYTHON:-.venv/bin/python}
DEVICE=${P0C_DEVICE:-mps}
STEPS=${P0C_STEPS:-30000}
DEPTHS=${P0C_DEPTHS:-1 2 4 8}
TAG=${P0C_TAG:-p0c_prime}
RESULTS=benchmarks/results/reasoning_depth.jsonl
PIDFILE=${P0C_PIDFILE:-benchmarks/results/p0c_prime_run.pid}
LOG=${P0C_LOG:-benchmarks/results/p0c_prime_run.log}

# 双开防护:活 pid 不双开(死 pid 视为陈旧,直接接管)
if [[ -f $PIDFILE ]]; then
  oldpid=$(cat "$PIDFILE" 2>/dev/null || true)
  if [[ -n $oldpid ]] && kill -0 "$oldpid" 2>/dev/null; then
    echo "已有活训练进程 pid=$oldpid,不双开。查进度: tail -f $LOG" >&2
    exit 1
  fi
fi

seeds=("$@")
[[ ${#seeds[@]} -eq 0 ]] && seeds=(0 1 2)

seed_done() {  # seed_done S TAG: canonical jsonl 已有 (TAG, S) 行 ⇒ 退出码 0
  # 纯 bash 行级 AND:先按 "seed": S,(json.dumps 定宽格式)筛行,再按 tag 过滤。
  # 不依赖 python——launcher 的控制流(跳过/双开)可被桩进程完整测试。
  [[ -f $RESULTS ]] || return 1
  grep -E "\"seed\": $1(,|})" "$RESULTS" 2>/dev/null \
    | grep -qF "\"tag\": \"$2\""
}

for seed in "${seeds[@]}"; do
  if seed_done "$seed" "$TAG"; then
    echo "=== $TAG seed $seed 已有 canonical 行,跳过 ($(date '+%F %T')) ===" | tee -a "$LOG"
    continue
  fi
  echo "=== $TAG seed $seed start $(date '+%F %T') ===" | tee -a "$LOG"
  CAFFEINATE=$(command -v caffeinate 2>/dev/null || true)
  if [[ -n $CAFFEINATE ]]; then
    "$CAFFEINATE" -is "$PY" -m benchmarks.reasoning_depth \
      --task pointer_chase --difficulty 16 --n_values 16 \
      --mode fixed --seeds "$seed" --steps "$STEPS" \
      --eval_depths $DEPTHS --mix --full_mha --n_global_heads 2 \
      --beta2 0.999 --clip 0 --device "$DEVICE" --tag "$TAG" \
      >> "$LOG" 2>&1 &
  else
    "$PY" -m benchmarks.reasoning_depth \
      --task pointer_chase --difficulty 16 --n_values 16 \
      --mode fixed --seeds "$seed" --steps "$STEPS" \
      --eval_depths $DEPTHS --mix --full_mha --n_global_heads 2 \
      --beta2 0.999 --clip 0 --device "$DEVICE" --tag "$TAG" \
      >> "$LOG" 2>&1 &
  fi
  pid=$!
  echo "$pid" > "$PIDFILE"
  echo "pid=$pid 已记录($PIDFILE),等待该 seed 完成..." >&2
  wait "$pid"
  rc=$?
  echo "=== $TAG seed $seed end rc=$rc $(date '+%F %T') ===" | tee -a "$LOG"
done
rm -f "$PIDFILE"
echo "全部 seed 处理完毕。" >&2

#!/usr/bin/env bash
# ignite — 跨 Agent 点火器(v1,移植自 AwareLiquid-Physic AMM-020;Ralph 式,
# 机器级 cron/launchd 驱动,与具体 Agent 软件解耦)。
#
# AMM-003(2026-10-01):本脚本降级为**可选后备**点火器——驱动主路径=
# 用户 Desktop Go 模式拉式点火(禁 cron/launchd/心跳排程)。仅用户显式
# 要求时启用;默认不安装任何排程。
#
# 语义:锁新鲜(<100min)=马拉松活着 ⇒ 退出;mode=OFF 或 state≠RUNNING ⇒ 退出;
# 否则用 docs/loop/agent-cmd.conf 配置的命令把 GOAL-PROMPT-M2 正文
# (```text 围栏)喂给任意 agent CLI。
#
# agent-cmd.conf 格式(一行模板,{PROMPT} 占位符被替换为 prompt 正文):
#   zcode -p {PROMPT}
#   claude -p {PROMPT}
#
# 安装(macOS launchd/cron 例,每 30 分钟):
#   */30 * * * * /Users/aricredemption/Projects/M2/scripts/ignite.sh >> /tmp/ignite-m2.log 2>&1
set -uo pipefail
cd "$(dirname "$0")/.."
LOG=/tmp/ignite-m2.log
now() { date '+%F %T'; }

CONF=docs/loop/agent-cmd.conf
[[ -f $CONF ]] || { echo "$(now) 未配置 $CONF(AGENT_CMD 模板)" >> $LOG; exit 1; }

# 有活马拉松(锁龄 <100min)⇒ 不点火
if [[ -f .loop-lock ]] && [[ -n $(find .loop-lock -mmin -100 2>/dev/null) ]]; then
  exit 0
fi
# 停机条件:mode=OFF 或 state≠RUNNING(PARKED/BLOCKED-HUMAN)⇒ 不点火
grep -q "^mode: ON" docs/loop/GOALS.md || { echo "$(now) mode=OFF,不点火" >> $LOG; exit 0; }
grep -q "^state: RUNNING" docs/loop/GOALS.md || { echo "$(now) state 非 RUNNING,不点火(重入口=用户指令)" >> $LOG; exit 0; }

PROMPT=$(awk '/^```text$/{f=1;next}/^```$/{f=0}f' docs/loop/GOAL-PROMPT-M2.md)
[[ -n $PROMPT ]] || { echo "$(now) 未从 GOAL-PROMPT-M2.md 提取到 text 围栏" >> $LOG; exit 1; }

AGENT_CMD=$(grep -v '^\s*#' "$CONF" | grep -v '^\s*$' | head -1)
[[ -n $AGENT_CMD ]] || { echo "$(now) $CONF 无有效模板行" >> $LOG; exit 1; }

echo "$(now) 点火: $AGENT_CMD" >> $LOG
printf -v FULL_CMD "$AGENT_CMD" "$PROMPT"
eval "$FULL_CMD" >> $LOG 2>&1

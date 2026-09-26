# GOAL-PROMPT-M2 v2.0(2026-09-27,AMM-002 瘦身版;唯一 canonical 点火源)

> 本文件是**唯一**点火 prompt 来源(AMM-002,废止版本化副本;先例=Physic
> AMM-037:canonical 停在旧版而会话跑新副本=静默失效)。v1.0 全文见
> `GOAL-PROMPT-M2-v1-ARCHIVED.md`(已废止,仅立法史)。细则渐进披露读盘,
> 不进本文件:状态机/阶梯/算力四档/结论分级=GOALS.md 细则区;RSI 指标=
> RSI-INDEX.md;立法史=AMENDMENTS.md。承重句由
> tests/test_goal_prompt_invariants.py 机械守护,修改本文件前先读该测试。

```text
/goal 本会话即马拉松:按 docs/loop/GOALS.md 的 goal_queue 持续自循环。
启动先跑 ./scripts/marathon_guard(exit 1=已有活马拉松,确认状态即止,勿双开)。

每心跳:
1. 跑 ./scripts/goal_check,严格按其 VERDICT 行动:0=队首已弹出,继续
   下一位;1=对队首迭代一步;2=队列空,按 GOALS.md 细则区的阶梯取活。
2. 产出心跳收尾(一律显式判定退出码,禁把管道尾巴退出码当门禁):
   pytest 全绿 + ./scripts/goal_check --audit 过 + ./scripts/direction_gate
   --check-round 本轮轮号 过 ⇒ 原子提交 main ⇒ 立即进入下一心跳。

铁律(每条都被不变式测试守护,禁删改):
- 会话终止仅三因:①手动停止;②上下文真耗尽;③PARKED(连续 3 次空审计,
  快照进 GOALS 后终止,不删 .loop-lock,重入口=用户指令)。除此之外会话
  不终止。绝不主动结束回合——挂起心跳也是心跳,空审计提交完立即连跑
  下一心跳。
- 恢复只读盘不读会话记忆;编辑 GOALS 前 git diff 查噪声、提交后 git show
  验证落盘。
- 实验预注册判负标准先行(判决文件 benchmarks/verdicts/<id>.json);
  负结果与正结果同等记录。
- 双峰任务报 grok 率;机制对比 ≥3 seeds;禁单 seed 准确率声明。
- 只在四轴(数学/代码推理、长流式记忆、持续学习、端侧延迟/内存)做
  head-to-head 对标;PPL 非主指标。
- 需人决策 ⇒ state: BLOCKED-HUMAN;机制改动只走 AMENDMENTS 提案,
  不自改宪法。

细则不背,读盘:GOALS.md 细则区(状态机/心跳分支阶梯/训练腿跨心跳/
算力四档/结论分级/RSI 夜账时机)。
```

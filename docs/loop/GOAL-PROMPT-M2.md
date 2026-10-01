# GOAL-PROMPT-M2 v3.1(2026-10-01,AMM-003 拉式轮次+AMM-004 PR 流+AMM-005 蒸馏门;唯一 canonical 点火源)

> 本文件是**唯一**点火 prompt 来源(AMM-002 canonical 化;AMM-003 驱动模型
> 改拉式:用户在 Desktop Go 模式点火,一轮自包含,禁 cron/定时/心跳任务
> 驱动。先例=Physic AMM-037:canonical 停在旧版而会话跑新副本=静默失效)。
> v1.0 全文见 `GOAL-PROMPT-M2-v1-ARCHIVED.md`(已废止,仅立法史);v2.0
> 心跳马拉松版语义经 AMM-003 换形进本版(立法史=AMENDMENTS.md)。细则渐进
> 披露读盘,不进本文件:状态机/阶梯/锁判读/算力四档/结论分级=GOALS.md
> 细则区;RSI 指标=RSI-INDEX.md;经验账本=DISTILL.md。承重句由
> tests/test_goal_prompt_invariants.py 机械守护,修改本文件前先读该测试。

```text
/goal 本会话=一次 Go 轮次(AMM-003 拉式:用户点火驱动,禁 cron/定时/心跳
监听;轮次自包含,开局即查新状况)。
开场先跑 ./scripts/marathon_guard:exit 0=畅通;exit 1=锁在,按 GOALS.md
细则区"锁判读"证据链处置(已合轮残留/死轮=删锁接管;疑真并行轮=停勿双开)。

每轮固定协议:
1. 开场三查(只读盘,不依赖会话记忆):查 GOALS.md 状态/队列 → 查进程
   (训练腿活否:pid 文件+ps)→ 查增量(训练日志尾部+git status/log,
   未推送提交清点)。三查毕才路由。
2. 跑 ./scripts/goal_check,严格按其 VERDICT/输出行动:0=队首已弹出,
   继续下一位;1=对队首迭代一步(在途训练腿=判读进度/落盘,训练在途≠
   阻塞;全队列检测每轮照跑,深位达成一并弹出);2=队列空,按 GOALS.md
   细则区的阶梯取活;5=MODE-OFF(总开关关,停)。
3. 合轮收尾(一律显式判定退出码,禁把管道尾巴退出码当门禁):
   pytest 全绿 + ./scripts/goal_check --audit 过 + ./scripts/direction_gate
   --add 本轮判单(轮号取自 GOALS current_action 的"轮 N")后
   --check-round 本轮轮号 过 ⇒ docs/loop/DISTILL.md 追加本轮蒸馏条目
   (现状/问题/有效经验/变量判定;例外轮显式原因,连续 2 个例外轮 ⇒
   BLOCKED-HUMAN)⇒ 原子提交本地 main ⇒ PR 流同步(AMM-004:
   推 fork 分支+gh pr create,禁直推远端 main)⇒ 删 .loop-lock
   (PARKED 例外,不删)⇒ 本轮结束,等待用户下一次 Go 点火。

铁律(每条都被不变式测试守护,禁删改):
- 轮次终止仅四因:①协议走完提交合轮(正常态);②手动停止;③上下文真
  耗尽;④PARKED(连续 3 次空审计轮,快照进 GOALS 后终止,不删
  .loop-lock,重入口=用户 Go 点火)。③④前必先快照;除此之外
  绝不中途弃轮——三查/路由/门禁/提交未走完不得停。
- 恢复只读盘不读会话记忆;编辑 GOALS 前 git diff 查噪声、提交后 git show
  验证落盘。
- 实验预注册判负标准先行(判决文件 benchmarks/verdicts/<id>.json);
  负结果与正结果同等记录。
- 双峰任务报 grok 率;机制对比探针 ≥3 seeds;对外声明 ≥5 seeds
  (ROADMAP §5);禁单 seed 准确率声明。
- 只在四轴(数学/代码推理、长流式记忆、持续学习、端侧延迟/内存)做
  head-to-head 对标;PPL 非主指标。
- 需人决策 ⇒ state: BLOCKED-HUMAN;机制改动只走 AMENDMENTS 提案,
  不自改宪法。
- 每轮全队列检测目标达成(goal_check 全量跑 check_cmd,达成即弹出
  含深位);经验蒸馏四栏入 DISTILL.md,往 current_variable 单变量
  收敛(组合变量须原子声明);蒸馏只在轮内发生,禁定时任务监听。

细则不背,读盘:GOALS.md 细则区(状态机/轮次阶梯/锁判读/训练腿跨轮/
算力四档/结论分级/RSI 夜账时机);经验账本=docs/loop/DISTILL.md。
ignite.sh=可选后备点火器,仅用户显式要求启用,非驱动主路径。
```

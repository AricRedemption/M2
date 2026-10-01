# AMENDMENTS — M2 循环治理提案账本

> 机制改动只走本文件提案,不自改宪法(GOAL-PROMPT-M2.md)。
> 状态:PROPOSED → ADOPTED(附依据)/ REJECTED(附理由)。
> 需长期停放的不可行动项登记「停车场」,阶梯②逐轮三问审计
> (T1/T2 可动?可逆?无预注册门槛?)。

## 提案

### AMM-003 拉式驱动模型(Go 轮次制)— ADOPTED(2026-10-01)
- 提案:驱动模型自"cron/心跳马拉松会话"改为**用户 Go 点火的拉式自包含
  轮次**(Desktop Go 模式):每轮=开场三查(状态/进程/增量,只读盘)→
  goal_check 路由与在途判读 → 队列推进 → 门禁全绿 → 原子提交(+push)→
  删锁合轮。**禁 cron/launchd/定时任务/心跳监听**,调度工具一律不创建;
  ignite.sh 降级为可选后备(仅用户显式要求时启用),非驱动主路径。
- 铁律修订(本提案唯一动的一条):"绝不主动结束回合"(马拉松连续会话
  语义;Physic 轮 409/410/AMM-036 挂起停摆事故)→"**绝不中途弃轮**"
  (拉式换形:轮次可以且应当结束——提交即合轮;但三查/路由/门禁/提交
  未走完不得停)。挂起停摆防护语义经换形保全:从"会话永续"改为
  "轮内协议完整性"。不变式测试同提交更新(fragment 换形,其余 16 条
  零改动)。
- .loop-lock 语义变更:心跳存活信号 → **轮内互斥锁**(goal_check 轮内
  touch;合轮显式删除;PARKED 例外保留作墓碑,100min 自过期)。
  marathon_guard 脚本零改动,exit 码语义不变;BUSY 时的锁判读证据链
  (已合轮残留/死轮残留=删锁接管;疑真并行轮=停勿双开)下沉 GOALS.md
  细则区。
- 根因:2026-09-28 事故实证点火链三重死亡(ignite.sh 从未被排程+其
  agent CLI zcode 本机不存在+无人监听锁龄),P0-C′ 18.5h 训练随关机
  全损且循环停摆 3.5 天零自愈——推式链路在本机从未活过。用户裁定改
  拉式(会话 2026-10-01):"我不想用心跳任务的方式去做,我希望是用
  Goal Prompt 用 Desktop 的那个 Go 模式去驱动,然后每一轮去检查新的
  状况"。
- 语义保全:马拉松模型全部承重语义经换形保留——程序计数器/goal_check
  路由/audit 数数锚/判单门/其余 16 条铁律(预注册/负结果/seed 纪律/
  四轴对标/BLOCKED-HUMAN/AMENDMENTS)零语义变化;仅"心跳单元"→
  "轮次单元"术语同步(GOALS.md 细则区同提交改订)。
- 与 Physic 的差异:Physic AMM-020 cron 点火(Ralph 式推式)依赖机器级
  排程存活;M2 实证该链路死亡后转拉式,属 M2 特有演化,非回退。

### AMM-002 Goal Prompt 瘦身 canonical 化 — ADOPTED(2026-09-27)
- 提案:v2 精简版(~20 行,指针+铁律式)升为**唯一** canonical 点火源;
  v1 全文(110 行)降级 `GOAL-PROMPT-M2-v1-ARCHIVED.md`(带废止横幅,
  仅立法史);承重铁律建立机械门禁 `tests/test_goal_prompt_invariants.py`
  (17 条,每条对应一次真实事故);细则(状态机/阶梯/四档/分级)下沉
  GOALS.md 细则区渐进披露。
- 根因:用户质询"太复杂了";Physic AMM-037 同型先例(prompt 太细=
  人工 Reflexion,canonical 停旧版=静默失效;v9.0 60 行→20 行,
  27 条承重句不变式零改动)。
- 语义保全:v1 的全部机制语义经三条路径无损保留——铁律进 v2 正文、
  细节进 GOALS.md 细则区、立法史进本文件;invariants 测试守护回归。

### AMM-001 采纳循环体系(GOAL-PROMPT-M2 v1.0)— ADOPTED(2026-09-27)
- 提案:移植 AwareLiquid-Physic 循环体系(GOAL-PROMPT-v8,AMM-035 优化版
  语义)至 M2:程序计数器 GOALS.md+goal_check 心跳路由器+marathon_guard
  锁检+direction_gate 判单门+RSI-INDEX 指数账本+ignite 跨 agent 点火。
- 依据:用户指令"列一个优先级清单,完整执行"(会话 2026-09-27);
  动机=M2 已有预注册/多 seed/负结果照记的文化纪律,但缺机械化的程序
  计数器与门禁,接续依赖散文 HANDOFF,长训练腿期间状态易失焦。
- 与源版本的差异(细节见 GOAL-PROMPT-M2.md 差异清单):无 PR 层
  (main 直接提交)、训练腿跨心跳(status: doing)、退出码 0/1/2/5
  起步(MINING-FROZEN/DEBT-FIRST 门后补)、判单加四轴耦合声明。

## 停车场(阶梯②每轮三问审计;解停须逐条记录依据)

- T2 服务器完整 nchain(5 seeds×5 tasks)/genreplay 结果判读 — 在途,
  等服务器返回,非解停项(队列执行段)。
- μP 缩放迁移(ROADMAP P1,50M→350M)— 需云预算与用户指令(T2/T3 资源)。
- 2B 混合架构注意力配比(ROADMAP P2)— 需融资/算力到位(用户资源)。
- GRPO 可验证奖励后训练(ROADMAP P2)— 前置=dpo-grpo-wiring 出队。

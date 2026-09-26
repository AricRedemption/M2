# AMENDMENTS — M2 循环治理提案账本

> 机制改动只走本文件提案,不自改宪法(GOAL-PROMPT-M2.md)。
> 状态:PROPOSED → ADOPTED(附依据)/ REJECTED(附理由)。
> 需长期停放的不可行动项登记「停车场」,阶梯②逐轮三问审计
> (T1/T2 可动?可逆?无预注册门槛?)。

## 提案

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

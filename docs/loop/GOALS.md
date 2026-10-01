# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 任何会话(人/cron/agent CLI)打开 M2 工作区:读这里 → 执行 current_action →
> 完成后推进状态并原子提交。规则:一次只有一个 current_action;达成条件
> 必须可机械验证(check_cmd 退出码,禁散文);研究内容不进本文件,
> 详情指针指向对应文档。更新本文件 = 推进程序计数器。
> 编辑前 git diff 查格式化器噪声;提交后 git show 验证落盘;
> 每轮提交前必跑 ./scripts/goal_check --audit(数数锚:条目数=check_cmd 数)。

## 循环细则(AMM-002 自 prompt 下沉,AMM-003 轮次化改订;agent 每轮开场读本区,不靠会话记忆)

- **驱动模型(AMM-003,拉式;AMM-004 PR 流)**:用户在 Desktop Go 模式点火,
  一轮自包含:开场三查(状态/进程/增量)→ goal_check 路由 → 门禁全绿 →
  原子提交(+推 fork 分支/PR 同步,禁直推远端 main)→ 删锁合轮。
  **禁 cron/launchd/定时任务/心跳监听**,调度工具
  一律不创建;ignite.sh=可选后备(仅用户显式要求时启用)。
- **锁判读(marathon_guard exit 1 时)**:最后提交晚于锁 mtime(锁后已
  提交=已合轮残留)或 锁龄≥30min+锁后零提交+零活进程(死轮残留)
  ⇒ 删锁接管;锁龄<30min+锁后零提交+有活进程迹象 ⇒ 疑真并行轮,
  停勿双开,报告用户。合轮删锁;PARKED 例外保留(墓碑,100min 自过期)。
- **状态机**:RUNNING(默认)/ PARKED(唯一非手动自停态:连续 3 次空审计
  轮触发;处置=RSI 夜账补账+快照进本文件+提交合轮,不删 .loop-lock,
  100min 自过期;重入口=用户 Go 点火:读 PARKED 快照+复述停摆原因进
  本轮报告+置回 RUNNING)/ BLOCKED-HUMAN(需人决策)。
- **轮次单元(训练腿跨轮)**:≤30min 可出判读的=当轮发起当轮判读;
  训练腿(小时级)=发起后条目 status 置 doing,后续每轮=查进度/判读/
  落盘,训练在途≠阻塞。blocked_on 禁列在途训练项。长训练腿一律走
  scripts/launch_p0c.sh 式幂等发射器(逐 seed 判重+caffeinate 防睡+
  pidfile 双开拒+逐深度增量落盘;2026-09-28 事故教训:18.5h 随关机
  全损,jsonl 零落盘)。
- **轮次分支阶梯(QUEUE-EMPTY 时依序取活,产出清零空审计计数)**:
  ① 判读后续池迭代(RESULTS/ROADMAP 明示可迭代点;段内同族 ≤2);
  ② 停车场三问解停审计(AMENDMENTS 停车场逐条过"T1/T2 可动?可逆?
     无预注册门槛?",逐项记录依据);
  ③ 写作登记(RESULTS/ROADMAP/HANDOFF 回填);
  ④ 工程硬化(工具缺口/测试加固/**RSI 夜账到期检查**——累计 ≥10 产出
     轮次未入账即属此项有活,防夜账断喂式静默失效);
  ⑤ 全空 ⇒ **空审计**:四项逐项审计依据写进 current_action 后提交,
     合轮等待下次点火;连续 3 次(跨轮)⇒ PARKED。
- **算力四档**:T0 本地 CPU / T1 本地加速器(本机 MPS / RTX 5060 8GB,
  视所在机器) / T2 服务器 / T3 Kaggle;T2/T3 发起需用户预先授权;
  资源红线=护机优先,异常即中止。
- **结论分级**:[A]构造保证 / [B]本机实测 / [C]终局声明(须 T3 或跨机
  复现);meta 带 exec_tier 与 seed 数。
- **判单门**:每产出轮次提交前 direction_gate --add --round N
  --direction(四轴耦合) --evidence,再 --check-round N;连续 2 条
  DRIFT ⇒ BLOCKED-HUMAN。
- **蒸馏门(AMM-005)**:GOALS meta 的 current_variable=当前唯一研究
  变量(单变量;组合变量须在其预注册原子声明,如 γ配额K=2+full_mha
  修复包);goal_check 每轮**全队列**检测达成(深位达成即弹出,不排
  队首)+回显锚点+--audit 校验非空;每个产出轮合轮前在
  docs/loop/DISTILL.md 追加四栏条目(现状/问题/有效经验/变量判定),
  例外轮显式声明原因,**连续 2 个例外轮 ⇒ BLOCKED-HUMAN**;蒸馏只在
  轮内发生,禁定时任务写入;换变量须旧变量判读落盘(或显式弃置+原因)
  后留痕切换。

```yaml
state: RUNNING            # RUNNING | PARKED | BLOCKED-HUMAN(PARKED 不删 .loop-lock,100min 自过期)
mode: ON                  # 循环总开关(OFF ⇒ goal_check/ignite 均不动作)
current_goal: >-
  M2 循环 v1(AMM-003 拉式):训练腿跨轮的 Go 轮次循环(轮次协议/阶梯/
  纪律唯一源=docs/loop/GOAL-PROMPT-M2.md,本文件不复述)。
current_variable: p0c-prime-depth(思考深度→能力;组合变量=γ配额K=2+full_mha 原子修复包,其余冻结;判据=verdicts/p0c_prime.prereg.v2.json,沿用 v1,no_posthoc_move)
current_action: >-
  轮 1(2026-09-27)循环体系 bootstrap:移植 Physic 循环体系
  (GOAL-PROMPT-v8 语义),落地 goal_check/marathon_guard/direction_gate/
  ignite.sh 四脚本+docs/loop/ 文档+21 测试,初始队列 4 条(见下)。
  轮 1.5 验收修复:pop_first 隔条删除 bug(≥3 条队列吞第 3 条)+
  ignite 漏检 PARKED+RSI T+ 计数勘误,回归测试入库(207 passed)。
  轮 2(AMM-002)prompt 瘦身 canonical 化:v2 精简版(指针+铁律式,
  ~20 行)升唯一点火源,v1 全文降级 ARCHIVED 存档;承重句不变式
  门禁建立(tests/test_goal_prompt_invariants.py,17 条铁律);细则
  (状态机/阶梯/四档/分级)自 prompt 下沉本文件细则区;阶梯④ 新增
  RSI 夜账到期检查(防 Physic 夜账断喂 91 轮式静默失效);根因=用
  户"太复杂了"质询+Physic AMM-037 先例(60 行→20 行,人工 Reflexion
  治理)。轮 2 验收修复(粘贴前终检):心跳步骤 2 补回 --add 判单步
  (v2 瘦身时误删,照字面执行会卡死在 --check-round 轮号不符)+
  退出码 5=MODE-OFF 显式化+seed 纪律对齐 ROADMAP §5(探针 ≥3/
  对外声明 ≥5);生命周期沙箱复验(guard→NOT-Achieved→ACHIEVED
  弹出→audit 3=3)全通。
  轮 3(2026-09-27)P0-C′ 发起:接管孤儿锁(前会话建锁即死,证据链=
  锁 mtime==最后提交 mtime+零提交+零活进程)后按队列迭代——预注册
  判负标准先行落盘(benchmarks/verdicts/p0c_prime.prereg.json:A 绝对
  增益≥0.02 ∧ B≥2σ 配对 ∧ C grok 率非降,判负诊断四选一,k=16 退化桶
  剔除主指标)+ reasoning_depth.py 补 --device(auto>cuda>mps>cpu)
  + fixed-depth sweep 训练腿发射(pointer_chase 单环 mix d16/n16,
  γ 配额 n_global_heads=2+full_mha,深度{1,2,4,8}×3 seeds×30k 步,
  beta2=0.999/clip=0 grokking 卫生配方,T1 MPS,ETA≈69h,按 seed
  分段落盘 jsonl,PID 记 benchmarks/results/p0c_prime_run.pid)。
  轮 4(2026-09-27)episodic-stream:队首+次位均训练腿在途(P0-C′
  本地 MPS / 2b-120k 服务器),按细则"训练在途≠阻塞"推进队列下一位
  可执行项——m2_training/episodic_stream.py 落地(DATA_FORMS §2 规格:
  Step/EventSegment/Episode 三时标层级+to_episode_stream 守门入口,
  时间戳一等公民+单调不减校验=反模式3 的 shuffle 拒绝+SHA-256 内容
  身份沿用 text_data.Corpus 纪律,dump/load 往返强校验防静默篡改),
  8 测试入库(总 235 绿)。check_cmd 待该条升到队首时自然 ACHIEVED
  弹出。下一步心跳:查 P0-C′ 进度(seed 0 d=1 在途);seed 边界=
  判读点。
  轮 5(2026-09-27)dpo-grpo-wiring:队首在途期间推进队列下一位——
  DPO/GRPO 对齐损失接入真实训练:Recipe.rl_mode(默认 ""=SFT 主线
  逐位不变;"dpo"/"grpo" 实验路径,禁 text 语料),TrainingRun 冻结
  参考模型(init 快照)+ rl 单步路径(DPO: 答案位 chosen/错答 rejected
  序列 logprob;GRPO: 答案位 G=4 采样 bandit+组优势+k3 KL+比率裁剪),
  checkpoint 增量存 rl_ref_model+restore 强校验;集成测试 7 项真实
  执行训练步(非纯数学单测),总 242 绿。check_cmd 待升队首自然弹出。
  队列全部可执行项清空,此后心跳=P0-C′ 进度判读循环(seed 边界+
  全落盘判决),若无产出心跳则按空审计阶梯计数。
  轮 6(2026-10-01)事故响应+拉式驱动改造(AMM-003):登记 2026-09-28
  训练腿死亡事故——P0-C′ 18.5h 随关机全损(seed0 深度 1/2/4 各 30k 步
  完成+深度 8 至 23200 步,jsonl 零落盘=进程退出才批量写;点火链三重
  死亡=ignite 从未排程+zcode CLI 本机不存在+无人监听,停摆 3.5 天零
  自愈)。修复三件:P0-2 崩溃安全(reasoning_depth.py 逐深度/逐 seed
  fsync 增量落盘,partial+canonical 分流,kill 中途保留已完成深度,
  +2 测试);P0-3 发射卫生(scripts/launch_p0c.sh 逐 seed 幂等重发+
  caffeinate -is 防睡+pidfile 双开拒,+2 测试);AMM-003 拉式驱动
  (GOAL-PROMPT-M2 v3.0 Go 轮次制:开场三查+合轮删锁+"绝不中途弃轮"
  换形"绝不主动结束回合",锁语义=轮内互斥,ignite 降可选后备,不变式
  测试同步改订;GOALS 细则区轮次化)。RSI 夜账补账轮 2-6。事故判读:
  死亡训练腿 eval 全部 chance 平台期(M≈0.065-0.069 vs 0.0625,k16=
  1.000 管道自洽,loss≈2.71≈15/16·ln16),初判 budget_wall 方向,
  待 transformer 对照终判。待用户裁决二项:①git push 403(AwareLiquid/
  M2 远端拒绝 AricRedemption 账号,本地 8 提交未推);②P0-C′ 重发方案
  (chance 平台期早停条款+transformer 对照先行;签收前不动 GPU)。
  轮 7(2026-10-01)两裁定落地+对照先行发射:①PR 流(AMM-004,ADOPTED):
  实测主仓 push:false ⇒ fork(AricRedemption/M2)分支 round-6-amm003 +
  PR AwareLiquid/M2#1,轮 3-6 共 8 提交进入可备份可评审态,merge 待主仓
  维护者;②P0-C′ 对照先行(prereg v2=p0c_prime.prereg.v2.json:hypothesis/
  metrics/判据/诊断逐字沿用 v1,执行改 phase1 对照单发→readout→phase2
  全量重发|phase3 复核→budget_wall;死亡腿 log 降级 exploratory 不入指标;
  mid-eval 10k/20k 只写 partial 不早停)。设施:reasoning_depth.py
  +--transformer_only/--mid_eval,launcher +P0C_MODE=control|sweep+
  P0C_SKIP_TRANSFORMER 省预算旋钮,+5 测试(总 250 绿)。MPS 实测对照
  300 步/19s ⇒ phase_1 ETA≈30min(6h/depth 为 MT-LNN 腿扫描速度,对照
  臂成本塌缩,当轮可判读)。对照腿已发射 T1 MPS:launcher pid 96600/
  训练 pid 96611,tag=p0c_prime_v2_control,caffeinate+pidfile+增量落盘。
  判读规则(预注册 v2 readout_rule):对照 grok(M≥0.90)⇒ phase_2 全量
  重发(sweep+skip_transformer,tag=p0c_prime,ETA≈45-66h);对照 chance ⇒
  phase_3 复核(1 seed×{1,8},ETA≈12h),仍 chance ⇒ budget_wall 判负登记。
  轮 7 后段(2026-10-01 16:24 接力;前段会话判单 --add 后猝死,锁判读=
  死轮残留[锁龄 30min49s+锁后零提交+零轮会话写入 31min,仅 detached
  训练腿],删锁接管):①phase_1 对照判读——transformer 30k 步+grokking
  卫生配方 M(k1..15)≈0.064=全 chance(<0.90)⇒ 按 readout_rule 机械进
  phase_3 复核腿(MT-LNN seed0×深度{1,8},tag=p0c_prime_v2_recheck,
  T1 MPS 发射,≈12h,复核仍 chance ⇒ budget_wall 判负);②AMM-005
  蒸馏门落地——goal_check v2 每轮全队列达成检测(达成即弹出含深位,
  首跑弹出滞留 2 轮的 episodic-stream/dpo-grpo-wiring)+current_variable
  锚点回显+audit 校验+DISTILL.md 四栏经验账本(轮 1-6 补账+轮 7 起按轮
  记账)+GOAL-PROMPT v3.1(承重句 17→19);③dpo-grpo-wiring check_cmd
  钉死 .venv/bin/python(系统 python3 无 pytest,原命令在本机永不弹)。
  前段勘误:叙事"总 250 绿"实为 251。
  轮 8(2026-10-01)研究登记轮:体系优化校验(GOAL-PROMPT v3.1 承重句
  19/19 绿+四文档交叉引用齐+RSI 夜账节奏未到期[距上账 1 产出轮])+
  外部 RSI 体系对标检索(8 体系)→ docs/loop/RSI-HORIZON.md:已具备 5
  (验证后改/追加账本/评估器门禁/git 存档/负结果+预注册)、缺口 2 ⇒
  AMM-006(ExpeL 式经验检索-精炼闭环)+AMM-007(宪法变动率仪表)均
  PROPOSED 待用户点火、条件触发 1(Dream-RSI 重放=进 agent 训练线后)、
  拒 1(并行变体探索,与单变量收敛冲突);RSI-INDEX 头部补定性/定量
  账本指针。phase_3 复核在途判读(d1 至 10k 步 mid-eval 全 chance,
  mid_eval_discipline 禁中途判)。
blocked_on: >-
  服务器后台训练(nchain 完整 5 seeds/genreplay)=队列执行段在途,
  非人工阻塞(blocked_on 禁列在途训练项);无其他人工阻塞。
next_trigger_hint: goal_check ⇒ 路由(挂起/阶梯/状态机语义见本文件细则区)
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX,DISTILL,RSI-HORIZON}.md
updated: 2026-10-01 (轮 8 研究登记:RSI-HORIZON 对标 8 体系+AMM-006/007 PROPOSED;phase_3 复核在途)
```

```yaml
goal_queue:
  - id: p0c-prime-depth-retest
    goal: P0-C′ 思考深度命题复测(ROADMAP §4 P0-C 结论 3 待办)——γ 全局头配额
      + full MHA 修复注意力后的 MT-LNN 上做 fixed-depth sweep(深度 1/2/4/8
      各训全新模型),任务用更难配置(更多跳数/更大图,pointer_chase d16/
      parity 线);预注册判负标准先行落盘,结果登记 ROADMAP P0 实验日志;
      多 seed 纪律(双峰任务报 grok 率,禁单 seed 声明)。
    done_condition: 判决文件 benchmarks/verdicts/p0c_prime.json 存在且含
      h_supported 字段(预注册格式),ROADMAP 已登记判决条目。
    check_cmd: python3 -c "import json; d=json.load(open('benchmarks/verdicts/p0c_prime.json')); assert 'h_supported' in d"
    status: doing
  - id: 2b-120k-leg
    goal: 2B 训练下一腿——60K 步(val PPL 2.556)后继续至 120K 步并登记
      val PPL;附上下文平坦 PPL 判读(128:2.72/256:2.72/512:2.68,长上下文
      无增益,判读数据侧 vs 架构侧归因并给出下一腿决策)。
    done_condition: docs/RESULTS_2B_120K.md 存在且登记 val PPL + 上下文
      PPL 判读 + 下一腿决策。
    check_cmd: test -f docs/RESULTS_2B_120K.md
    status: todo
```

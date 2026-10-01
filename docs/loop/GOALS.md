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
  **禁 cron/launchd/定时任务/心跳监听**,调度工具一律不创建
  (ignite.sh+agent-cmd.conf 已于轮 11 归档删除,git 可逆)。
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
- **蒸馏门(AMM-005;纪律正文=GOAL-PROMPT v4.0,本区只留 GOALS 特有)**:
  current_variable=当前唯一研究变量(单变量;组合变量须在其预注册原子
  声明);换变量须旧变量判读落盘(或显式弃置+原因)后留痕切换。
  例外轮计数(轮 12 补):只认全例外(主判定=例外);半例外(推进为主+
  机制为辅)不断连击;用户明示续作机制工作 ⇒ 重置连击(明示=人裁,
  留痕于当轮 DISTILL);阈值 2 与后果不动。
- **社区蒸馏门(AMM-008)**:问表四栏+颗粒度对齐纪律+触发条件(例行=
  十轮节拍③,定义=RSI-INDEX)+入账四分法=RSI-HORIZON.md 协议区,不在
  本区复述;采纳走 AMENDMENTS。
- **程序计数器瘦身(AMM-009)**:current_action 仅近 2 轮全文+更早轮
  单行索引(全文=git log,永不丢);块高 ≤48 行由测试守护。

```yaml
state: RUNNING            # 轮 12 用户问询例外轮机制=明示授权,连击重置(计数语义见细则区蒸馏门 bullet);下轮=phase_3 d=8 读数回研究主线
mode: ON                  # 循环总开关(OFF ⇒ goal_check 不动作)
current_goal: >-
  M2 循环 v1(AMM-003 拉式):训练腿跨轮的 Go 轮次循环(轮次协议/阶梯/
  纪律唯一源=docs/loop/GOAL-PROMPT-M2.md,本文件不复述)。
current_variable: p0c-prime-depth(思考深度→能力;组合变量=γ配额K=2+full_mha 原子修复包,其余冻结;判据=verdicts/p0c_prime.prereg.v2.json,沿用 v1,no_posthoc_move)
current_action: >-
  [轮次索引:更早轮单行,全文=git log(AMM-009 瘦身,永不丢)]
  轮 1(09-27)循环 bootstrap+验收修复(pop_first 隔条删除 bug)。
  轮 2(09-27)AMM-002 prompt 瘦身 canonical 化+17 条不变式测试。
  轮 3(09-27)P0-C′ 发射:预注册 v1+fixed sweep(T1 MPS)。
  轮 4(09-27)episodic-stream 落地(DATA_FORMS §2)。
  轮 5(09-27)dpo-grpo-wiring 接线(rl 单步路径,默认关)。
  轮 6(10-01)AMM-003 拉式驱动+09-28 事故响应(fsync 增量+幂等发射)。
  轮 7(10-01)AMM-004 PR 流(fork+PR#1)+AMM-005 蒸馏门(goal_check
  全队列+current_variable+DISTILL)+P0-C′ 对照先行(phase_1 chance ⇒
  phase_3 复核发射;前段会话猝死,锁判读取证后接力收编)。
  轮 8(10-01)研究登记:RSI-HORIZON 对标 8 体系(已具备 5/缺口 2)。
  轮 9(10-01)AMM-008 社区蒸馏门(问表四栏)+社区先验(多跳结构性
  障碍+grokking 量级 10^5-10^6 步)喂 P0-C′ 判读链。
  轮 10(10-01)AMM-009 大道至简:GOAL-PROMPT v4.0 蒸馏门全量进宪法
  (承重句 19→21)+程序计数器瘦身(≤48 行测试守护)+变动率一行仪表。phase_3 复核在途:d=1 完成(终评 k1-15 全 chance,
  partial 已落盘),d=8 训练中(≈6h 后终评;readout_rule:仍 chance ⇒
  budget_wall 判负,加预算量级参照社区先验 10^5-10^6 步)。
  轮 11(10-01)清理轮(审计处方打包,零承重句变动):①十轮节拍四钟
  合一(夜账/HORIZON 复检/社区例行/变动率窗口→唯一定义处=RSI-INDEX);
  ②死件归档(ignite.sh+agent-cmd.conf 删除,git 可逆);③HORIZON
  AMM-006/007 章节各压一行;④goal_check 队列空提示语对齐;⑤DISTILL/
  RSI-INDEX 头部去重。**例外轮连击(轮 10+11=2)⇒ 铁律转 BLOCKED-HUMAN**
  (体系正确叫停"连续改体系"):待用户裁决——下一轮回研究主线(phase_3
  d=8 读数,readout_rule 终判)即解除,或明示继续机制工作/改锚。
  轮 12(10-01)例外轮计数补丁(BLOCKED-HUMAN 下用户问询=明示授权):
  ①半例外(推进为主+机制为辅,轮 7/9 已用)不计入连击——用法先于
  定义,账本已记不改;②用户明示续作机制工作 ⇒ 重置连击。补丁 3 行,
  阈值/后果零改动;state 回 RUNNING,连击归零。phase_3 d=8 在途
  (2k/30k 步);下轮=d=8 读数(readout_rule 终判)回研究主线。
blocked_on: >-
  服务器后台训练(nchain 完整 5 seeds/genreplay)=队列执行段在途,
  非人工阻塞(blocked_on 禁列在途训练项);无其他人工阻塞。
next_trigger_hint: goal_check ⇒ 路由(挂起/阶梯/状态机语义见本文件细则区)
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX,DISTILL,RSI-HORIZON}.md
updated: 2026-10-01 (轮 12 例外轮计数补丁,用户明示授权重置连击,回 RUNNING;phase_3 d8 在途)
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

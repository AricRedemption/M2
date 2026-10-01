# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 任何会话(人/cron/agent CLI)打开 M2 工作区:读这里 → 执行 current_action →
> 完成后推进状态并原子提交。规则:一次只有一个 current_action;达成条件
> 必须可机械验证(check_cmd 退出码,禁散文);研究内容不进本文件,
> 详情指针指向对应文档。更新本文件 = 推进程序计数器。
> 编辑前 git diff 查格式化器噪声;提交后 git show 验证落盘;
> 每轮提交前必跑 ./scripts/goal_check --audit(数数锚:条目数=check_cmd 数)。

## 循环细则(AMM-002 自 prompt 下沉,AMM-003 轮次化改订;agent 每轮开场读本区,不靠会话记忆)

- **驱动模型(AMM-003 拉式点火;AMM-004 PR 流;AMM-010 连续循环)**:
  用户点火一次=一个连续循环,循环内由 goal 校验驱动连续轮次(单目标
  =goal_queue 清空或推进至 BLOCKED-HUMAN,点火时可改指),达成或合法
  终止方停。**禁 cron/launchd/定时任务/心跳监听**不变,调度工具一律
  不创建(ignite.sh+agent-cmd.conf 已于轮 11 归档删除,git 可逆);
  循环锁=.loop-lock 每轮合轮 touch 刷新,循环终止删(PARKED 墓碑例外)。
- **锁判读(marathon_guard exit 1 时)**:最后提交晚于锁 mtime(锁后已
  提交=已合轮残留)或 锁龄≥30min+锁后零提交+零活进程(死轮残留)
  ⇒ 删锁接管;锁龄<30min+锁后零提交+有活进程迹象 ⇒ 疑真并行轮,
  停勿双开,报告用户。连续循环内:锁 mtime=每轮合轮 touch 刷新,活循环
  的锁恒新鲜;循环终止删锁;PARKED 例外保留(墓碑,100min 自过期)。
- **状态机**:RUNNING(默认)/ PARKED(唯一非手动自停态:连续 3 次空审计
  轮触发;处置=RSI 夜账补账+快照进本文件+提交合轮,不删 .loop-lock,
  100min 自过期;重入口=用户 Go 点火:读 PARKED 快照+复述停摆原因进
  本轮报告+置回 RUNNING)/ BLOCKED-HUMAN(需人决策;含 exit 6 阶梯全空
  =队列余项待人裁,AMM-011)。
- **轮次单元(训练腿跨轮)**:≤30min 可出判读的=当轮发起当轮判读;
  训练腿(小时级)=发起后条目 status 置 doing,后续每轮=查进度/判读/
  落盘,训练在途≠阻塞。blocked_on 禁列在途训练项。长训练腿一律走
  scripts/launch_p0c.sh 式幂等发射器(逐 seed 判重+caffeinate 防睡+
  pidfile 双开拒+逐深度增量落盘;2026-09-28 事故教训:18.5h 随关机
  全损,jsonl 零落盘)。
- **轮次分支阶梯(无可执行项时依序取活——exit 2 队列空,或 exit 6
  余条目均人门控(AMM-011);产出清零空审计计数)**:
  ① 判读后续池迭代(RESULTS/ROADMAP 明示可迭代点;段内同族 ≤2);
  ② 停车场三问解停审计(AMENDMENTS 停车场逐条过"T1/T2 可动?可逆?
     无预注册门槛?",逐项记录依据);
  ③ 写作登记(RESULTS/ROADMAP/HANDOFF 回填);
  ④ 工程硬化(工具缺口/测试加固/**RSI 夜账到期检查**——累计 ≥10 产出
     轮次未入账即属此项有活,防夜账断喂式静默失效);
  ⑤ 全空 ⇒ **空审计**:四项逐项审计依据写进 current_action 后提交,
     合轮(连续循环内由 goal 校验驱动下一轮);连续 3 次(跨轮)⇒ PARKED。
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
state: RUNNING            # 轮 26 在途跟进轮:mid_eval 预测已立待核;d=8 臂(pid 40268)6600/30000,判据预载,出数即终判
mode: ON                  # 循环总开关(OFF ⇒ goal_check 不动作;AMM-011 维护停后恢复)
current_goal: >-
  M2 循环 v2(AMM-010 单目标连续循环):goal 校验驱动的连续轮次循环,
  单目标=队列清空或推进至 BLOCKED-HUMAN(协议/阶梯/纪律唯一源=
  docs/loop/GOAL-PROMPT-M2.md,本文件不复述)。
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
  轮 10(10-01)AMM-009 大道至简(GOAL-PROMPT v4.0 承重句 19→21+程序计数器
  瘦身+变动率一行仪表);phase_3 d=1 终评 chance 落盘,d=8 在途。
  轮 11(10-01)清理轮(审计处方打包,零承重句变动);例外连击(10+11)
  触发 BLOCKED-HUMAN,轮 12 用户问询=明示授权解除(半例外不计连击+
  明示续作重置连击,阈值/后果零改动)。
  轮 13(10-01)判读+事故响应:d=1 终评 chance;双腿死于 20:22 重启,
  幂等重发 pid 40268,M(1,·) 取 18:31 冻结 partial 留痕。
  轮 14(10-01)工程硬化:launcher 双开防护扩同目录 *.pid+UNBUFFERED=1,
  +2 测试;并行轮遗留锁证据链接管删除。
  轮 15(10-01)社区蒸馏门(用户点名):三路检索入 HORIZON #3,喂终判
  分叉(d8 chance⇒双归因,加预算=人裁,换任务=排序类)。非例外。
  轮 16(10-01)AMM-010 单目标连续循环 ADOPTED(用户明示点火=修宪授权,
  v4.0→v4.1 三处改订;21 fragment 零改动;例外轮连击重置)。
  轮 17(10-01)AMM-010 验收轮(用户点名):全仓一致性扫描修 3 处旧驱动
  模型残留(阶梯⑤/current_goal/HANDOFF);21 fragment 复验绿,交付 v4.1。
  轮 18(10-01)十轮节拍轮:夜账轮 7-17 补账(K=0 待 d8/A 累计 10/8/EXP 23%)+复检+例行推迟留痕+变动率 +4≤6 ✓;分支+PR#2 开成。
  轮 19(10-01)在途跟进:自家锁三证据判例(mtime/HEAD/腿 pid);推送 443 欠账=2。
  轮 20(10-01)工程硬化轮(例外轮,连击=1):三查发现 jsonl mtime 被测试
  套件推走→定位 test_launch_p0c 写穿规范账本(purge 撞 fsync=吞行竞争)
  →修复=P0C_RESULTS_DIR env 三方同旋钮+零接触回归门;验收 269 绿全等。
  轮 21(10-01)在途跟进:自家锁判例照用;隔离修复轮内首验;推送 force-
  with-lease 清偿欠账归 0(非快进拒=防御正常,先 fetch 再 lease)。
  非例外轮,连击归 0。
  轮 22(10-01)在途跟进:5800+/30000 禁中途判;隔离二次验;清偿后快进首验。
  轮 23(10-01)在途跟进轮:6000/30000 禁中途判;partial 冻结预测验证
  (18:31 未动=未到 mid_eval 旁证,与步速互证 ETA)。非例外轮,连击=0。
  轮 24(10-02)终判预演:prereg v2 判据装填+落账路径+登记位确认(出数即机械核对)。
  轮 25-27(10-02)在途跟进×3:6400→6600 禁中途判;PR #2 MERGEABLE 实测;立 mid_eval 预测并前置核对成立(约 01:53)。
  轮 28-35(10-02)在途跟进×8:6800→7600 步稳态平台 2.74;欠账清偿。
  轮 36-83(10-02)在途跟进×48:7800→12800 步;轮 36 崩落观察轮 37 证伪
  (周期伪影),38 回平台,47 预测复现@9200,57 mid_eval 三项兑现+中点
  读数 chance(记录非判定);推送欠账 1 笔(443 长断延续);终评约 09:45。
  轮 84(10-02)MODE-OFF 终止轮:用户 02:47:54 手动停,删锁报告;腿 40268 保留,AMM-011 修复落地后 mode ON 恢复待点火。
  轮 85(10-02)重启点火轮:锁判读接管(锁后已提交残留,腿活≠并行);d=8 臂 14000/30000 chance 平台;推送欠账 3 笔 443;终评约 09:45。
blocked_on: >-
  服务器后台训练(nchain 完整 5 seeds/genreplay)=队列执行段在途,
  非人工阻塞(blocked_on 禁列在途训练项);无其他人工阻塞。
next_trigger_hint: goal_check ⇒ 路由(挂起/阶梯/状态机语义见本文件细则区)
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX,DISTILL,RSI-HORIZON}.md
updated: 2026-10-02 (轮 27 在途跟进:mid_eval 预测待事件落地核;d=8 在途)
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
      [AMM-011:T2 服务器腿,算力四档需用户预授权 ⇒ status=blocked-human
      人门控:goal_check 路由跳过、不计数为有活;授权后改回 todo 即入队]
    done_condition: docs/RESULTS_2B_120K.md 存在且登记 val PPL + 上下文
      PPL 判读 + 下一腿决策。
    check_cmd: test -f docs/RESULTS_2B_120K.md
    status: blocked-human
```

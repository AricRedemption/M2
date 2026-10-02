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
state: BLOCKED-HUMAN       # 轮 340 置入(轮 341 纠偏补写):exit 6 阶梯全空,待授权项菜单四选已报;循环已合法终止(单目标达成,锁已删)
mode: ON                  # 循环总开关(OFF ⇒ goal_check 不动作;AMM-012 维护停后恢复)
current_goal: >-
  M2 循环 v2(AMM-010 单目标连续循环):goal 校验驱动的连续轮次循环,
  单目标=队列清空或推进至 BLOCKED-HUMAN(协议/阶梯/纪律唯一源=
  docs/loop/GOAL-PROMPT-M2.md,本文件不复述)。
current_variable: p0c-prime-depth(思考深度→能力;判读已落盘=判负 budget_wall,verdicts/p0c_prime.json h_supported=false;换向待人裁:加预算/换任务/2b 三选,判据=prereg.v2.json no_posthoc_move)
current_action: >-
  [轮次索引:更早轮单行,全文=git log(AMM-009 瘦身,永不丢)]
  轮 1-105(09-27~10-02)前循环:bootstrap/AMM-002~010 修宪链/P0-C′
  发射与事故链/两轮 MODE-OFF/loop_closer 立项(详见 git log 与
  DISTILL 轮 1-105)。
  轮 106(10-02)新循环点火首轮:closer 账实结类=add -A 全仓+测试;
  AMM-012 首轮 D=3/N=3;腿 17000/30000。
  轮 107-133(10-02)在途跟进×22+节拍×2(113/123)+方向动作×2(108 停车
  场/113 判读准备)+推送 443 判例成标准动作(111/116):腿 17000→18800
  chance 平台;判读预案五件开建(118 分支表/123 mid_eval 预案/128
  verdict schema)。
  轮 134-138(10-02)跟进+135 观察轮(19400 崩落)/136 证伪(伪影判例二
  兑现,判读程序收敛两步动作)/137-138:腿 18800→19800;137 起程序计数
  器链断(账实不符第五击,轮 341 结类)。
  轮 139-163(10-02)跟进×20+节拍×2(143/153)+方向动作×3(143 计算干跑
  known-good/148 数据链字段级终检/158 2b 菜单做实):腿 19800→29400 前
  段;23600/24400 伪影两现两证伪。
  轮 164-213(10-02)跟进×45+节拍×5(173/183/193/203/213)+方向动作×5
  (168/178/188/198/208 留痕):腿 23400 前后稳态;25800 伪影第四现证伪
  (254)。
  轮 214-263(10-02)跟进×45+节拍×5(223/233/243/253/263)+方向动作×5
  (218/228/238/248/259 留痕):腿 23400→26400;队列头判据在途。
  轮 264-313(10-02)跟进×45+节拍×5(273/283/293/303/313)+方向动作×5
  (268/278/288/298/308 留痕):腿 26400→28800 稳态守望。
  轮 314-338(10-02)跟进×22+节拍×2(323/333)+方向动作×2(318/328 留痕
  /338 终评在即):腿 28800→29800;终评倒计时。
  轮 339(10-02)终评判读轮:腿 rc=0 完成(30000 步 12.6h),M(8,0)=0.0656
  ≈M(1,0)=0.0660 均 chance,gain=−0.0004 ⇒ h_supported=false 诊断
  budget_wall(非 thesis 反证);verdicts/p0c_prime.json+ROADMAP §4.5
  第七轮登记+夜账终入账(K+1 首事件);队首机械弹出;预案五件全链兑现
  零临场发挥。
  轮 340(10-02)exit 6 阶梯走查全空(空审计)⇒ 置 BLOCKED-HUMAN;待人
  授权项菜单四选录 blocked_on 并报告用户;循环单目标达成待终止。
  轮 341(10-02)终止后账实纠偏:程序计数器链断 137 起结类(轮 107
  old_string 跨行拼接错配静默 no-op,235 轮继承),本块全量重建
  (107-341 单行索引,全文=git log/DISTILL/gate jsonl 无损);state 行
  补写 BLOCKED-HUMAN;循环保持终止。
blocked_on: >-
blocked_on: >-
  【待人裁菜单(轮 340 报告,裁决权在用户)】(a) d8 fork·加预算:T1 腿
  10^5 步≈2 天/臂(新预注册+换变量留痕;HORIZON #3 sizing);(b) d8
  fork·加预算 T2/T3(需预授权);(c) d8 fork·换任务排序类(T1 可跑,
  新预注册);(d) 2b-120k-leg 三选[专荐改判据:用户线 RESULTS_2B_30K.md
  已含 200K 收官 PPL 2.4106 收敛饱和,见 DISTILL 轮 158];另:EXP 窗口
  重置待人裁确认(AMM-012);腿 40268 已 rc=0 收官,无在途训练。
next_trigger_hint: goal_check ⇒ 路由;下轮预期 exit 6(队列=[2b-120k-leg blocked-human]):阶梯取活后向用户报告待授权项菜单=(a) T1 加预算腿 10^5 步≈2 天/臂(新预注册+换变量留痕)(b) T2/T3 加预算(需预授权)(c) 换任务排序类新预注册(T1 可跑)(d) 2b-120k-leg 三选[专荐改判据:用户线 RESULTS_2B_30K.md 已含 200K 收官 PPL 2.4106,详见 DISTILL 轮 158]——菜单裁决权在用户,人裁毕走 AMENDMENTS/队列变更;需人决策 ⇒ BLOCKED-HUMAN(单目标达成=合法终止因①,终止删锁报告);EXP 窗口重置待人裁确认(AMM-012)
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX,DISTILL,RSI-HORIZON}.md
updated: 2026-10-02 (轮 341 终止后纠偏:程序计数器链断结类全量重建+state 补写;循环保持终止)
```

```yaml
goal_queue:
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

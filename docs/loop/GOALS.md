# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 任何会话(人/cron/agent CLI)打开 M2 工作区:读这里 → 执行 current_action →
> 完成后推进状态并原子提交。规则:一次只有一个 current_action;达成条件
> 必须可机械验证(check_cmd 退出码,禁散文);研究内容不进本文件,
> 详情指针指向对应文档。更新本文件 = 推进程序计数器。
> 编辑前 git diff 查格式化器噪声;提交后 git show 验证落盘;
> 每轮提交前必跑 ./scripts/goal_check --audit(数数锚:条目数=check_cmd 数)。

## 循环细则(AMM-002 自 prompt 下沉,AMM-003 轮次化改订;agent 每轮开场读本区,不靠会话记忆)

- **驱动模型(AMM-003 拉式点火;AMM-004 PR 流;AMM-010 连续循环;
  AMM-014 蒸馏续向)**:用户点火一次=一个连续循环,循环内由 goal
  校验驱动连续轮次(单目标=goal_queue 清空=续向蒸馏无可推导,点火时
  可改指),达成或合法终止方停。队首弹出后按续向蒸馏自动推导下一
  方向(四栏:现状/问题/目标/训练结论 ⇒ 新条目+预注册+发射,换变量
  留痕切换),人不在方向环;资源红线不可解/手动停 ⇒ BLOCKED-HUMAN。**禁 cron/launchd/定时任务/心跳监听**不变,调度工具一律
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
  本轮报告+置回 RUNNING)/ BLOCKED-HUMAN(资源红线不可解[T3 不可用]/手动停;exit 6 且续向
  蒸馏推导不出 ⇒ 队列余项待人裁,AMM-011/014)。
- **轮次单元(训练腿跨轮)**:≤30min 可出判读的=当轮发起当轮判读;
  训练腿(小时级)=发起后条目 status 置 doing,后续每轮=查进度/判读/
  落盘,训练在途≠阻塞。blocked_on 禁列在途训练项。长训练腿一律走
  scripts/launch_p0c.sh 式幂等发射器(逐 seed 判重+caffeinate 防睡+
  pidfile 双开拒+逐深度增量落盘;2026-09-28 事故教训:18.5h 随关机
  全损,jsonl 零落盘)。
- **轮次分支阶梯(无可执行项时依序取活——exit 2 队列空,或 exit 6
  余条目均人门控(AMM-011);产出清零空审计计数)**:
  ① 续向蒸馏(AMM-014:四栏推导下一方向 ⇒ 立新预注册+发射新腿,
     换变量留痕切换;次选 RESULTS/ROADMAP 明示可迭代点;段内同族 ≤2);
  ② 停车场三问解停审计(AMENDMENTS 停车场逐条过"T1/T2 可动?可逆?
     无预注册门槛?",逐项记录依据);
  ③ 写作登记(RESULTS/ROADMAP/HANDOFF 回填);
  ④ 工程硬化(工具缺口/测试加固/**RSI 夜账到期检查**——累计 ≥10 产出
     轮次未入账即属此项有活,防夜账断喂式静默失效);
  ⑤ 全空 ⇒ **空审计**:四项逐项审计依据写进 current_action 后提交,
     合轮(连续循环内由 goal 校验驱动下一轮);连续 3 次(跨轮)⇒ PARKED。
- **算力四档(AMM-017 资源=蒸馏约束,非停车条件)**:本机(T0 CPU/
  T1 MPS)探针腿 ≤30min/腿=唯一执行档;T2 服务器/T3 Kaggle=外置资源,
  一律**愿望登记**(非阻塞,到位由用户点火改指入队);异常即中止。
- **结论分级**:[A]构造保证 / [B]本机实测 / [C]终局声明(须 T3 或跨机
  复现);meta 带 exec_tier 与 seed 数。
- **判单门**:每产出轮次提交前 direction_gate --add --round N
  --direction(四轴耦合) --evidence,再 --check-round N;连续 2 条
  DRIFT ⇒ BLOCKED-HUMAN。
- **合轮收尾与 VERDICT 语义(AMM-016 自围栏下沉;机械化=scripts 头注)**:
  VERDICT 退出码=scripts/goal_check 头注(0=队首弹出续位/1=对队首迭代
  一步/2=队列空/6=无可执行项走阶梯①续向蒸馏/5=MODE-OFF);合轮门禁链
  =pytest 全绿+goal_check --audit 过+direction_gate --add --check-round
  本轮过+DISTILL.md 四栏(现状/问题/有效经验/变量判定,另带节拍距/
  方向距行「距上次十轮节拍已 N 产出轮;守望段方向距 D(非守望记
  D=—)」;例外轮显式原因,连续 2 个例外轮 ⇒ BLOCKED-HUMAN)⇒ 原子
  提交 main ⇒ 推 fork 分支+PR ⇒ touch .loop-lock;红即 ABORT。
- **续向蒸馏细则(AMM-017)**:推导前提=本机 ≤30min 探针可执行
  (预算反推进预注册:步数/规模按 30min 实测速度定,等墙钟预算设计);
  超预算推导(外置资源依赖)→ 愿望登记(blocked_on 区+DISTILL 留痕),
  不入队不停车;多 seed=每条发射 ≤30min,3 seeds 分三次发射;BLOCKED-
  HUMAN=仅用户手动停。
- **蒸馏门(AMM-005;纪律=IRON-LAWS.md,本区只留 GOALS 特有)**:
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
state: RUNNING            # 轮 359 判决轮(阶段 2 判决+弹出):3 seeds M(1)_ds=0.6421(=d1 无 ds 水平,ds 无害性✓)vs M(8)_ds=0.1249,gain=−0.5172±0.0229 三 seed 全负 ⇒ h_supported=false 诊断 depth_hurts(预判如实兑现);verdicts/p0c_sort_ds_depth.json+ROADMAP §4.5 第十一轮=深度命题探针级五连负收官;弹出队列空;阶梯①推导=S5 词问题探针(NC¹ 完全分离+looped 文献正先验=深度链唯一剩余正先验角落)入队 todo
mode: ON                  # 循环总开关(OFF ⇒ goal_check 不动作;AMM-012 维护停后恢复)
current_goal: >-
  M2 循环 v2(AMM-010/014 蒸馏续向连续循环):goal 校验驱动的连续
  轮次循环,单目标=队列清空(队列由续向蒸馏续填,人不在方向环;协议/
  阶梯/纪律唯一源=docs/loop/GOAL-PROMPT-M2.md v4.5,本文件不复述)。
current_variable: p0c-sort-depth(排序类多步比较链上思考深度→能力;判读落盘=verdicts/p0c_sort_ds_depth.json h_supported=false 诊断 depth_hurts,轮 359——ds 平面上深度单调伤,探针级五连负收官;换向推导=S5 词问题探针(正先验角落),预注册时留痕切换或延续)
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
  轮 339-349(10-02)终评判读+终止+立法链:腿 40268 判负 budget_wall
  (M(8,0)=0.0656≈chance,verdicts/p0c_prime.json+§4.5 第七轮);exit 6
  空审计置 BLOCKED-HUMAN+程序计数器链断全量重建;AMM-013/014(蒸馏续向
  v4.5 队列播种 p0c-sort-relay)/015(铁律下沉+distill_inject v4.6)/
  016(围栏 17 行 v4.7)/017(资源=蒸馏约束 v4.8:只推导≤30min 可执行,
  超预算愿望登记不停车)+社区门#5+版本表。
  轮 350-358(10-03)深度命题探针链前段:bubble_trace 实现+预注册
  先行 0c7fbf1/fefc67b/9d897be+launcher 参数化(P0C_TASK/STACK/DS)+
  接线(deep_supervision 进 fixed);core 3 seeds 判负 **flat_
  iterations_ignored**(§4.5 第八轮)/stack 3 seeds 判负 **budget_
  wall=深堆叠不训练**(第九轮)/ds 变体 3 seeds 判负 **direction_
  but_underpowered=部分救活**(第十轮,ds 使深堆叠从不训练变部分
  训练);裸 & 腿中断受管重发恢复;节拍四事(N=10)。
  轮 359(10-03)阶段 2 判决轮:d1+ds 三短腿(3min/腿,判据先行
  3f88b4a)M(1)_ds=0.6421(=d1 无 ds 水平,ds 无害性✓)/M(8)_ds=
  0.1249 在盘,gain=−0.5172±0.0229 三 seed 全负 ⇒ A/B/C 全败
  h_supported=false,**depth_hurts**(轮 358 预判如实兑现);
  verdicts/p0c_sort_ds_depth.json+§4.5 第十一轮=深度命题探针级
  五连负收官(全路径无非 thesis 终局反证,升级预算=愿望登记);
  弹出队列空;阶梯①推导=S5 词问题探针(NC¹ 分离+looped 正先验=
  深度链唯一剩余正先验角落)入队 todo。
blocked_on: >-
  愿望登记(AMM-017 非阻塞,不停车):t3-kaggle-launcher(Kaggle 发射
  器,凭证到位由用户点火改指入队)/30k 步级终判预算(排序腿升级);
  另:EXP 窗口重置仍待人裁确认(AMM-012);腿 40268 已 rc=0 收官,
  无在途训练。
next_trigger_hint: goal_check ⇒ 路由;下轮预期 VERDICT=1(队首
  p0c-s5-depth todo):S5 预注册先行(p0c_s5_depth.prereg.json:任务
  =gen_s5_word 现成 NC¹ 完全分离,k=8 固定(T=11 极短,腿~3min),
  stack+ds d={1,8} 同腿配对 3 seeds;判据=深度方向 A/B/C+负诊断
  三选一,正先验=HORIZON #3 looped 文献)→中程提交→发射;判决后
  续向蒸馏:若 s5 亦负=深度链全路径收官,换轴推导或单目标达成候选;
  EXP 窗口重置待人裁确认(AMM-012);点火=v4.8 围栏
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX,DISTILL,RSI-HORIZON}.md
updated: 2026-10-03 (轮 359 阶段 2 判决:depth_hurts 五连负收官,S5 正先验角落推导入队)
```

```yaml
goal_queue:
  - id: p0c-s5-depth
    goal: S5 词问题深度探针(轮 359 立项,深度链最后一条可推导路径)
      ——gen_s5_word 现成(NC¹ 完全分离,Barrington:固定浅层必败,
      权重共享迭代可解;looped 文献正先验=HORIZON #3),k=8 固定
      T=11,stack+ds,d={1,8} 同腿配对 ×3 seeds;单变量=深度。
    done_condition: 判决文件 benchmarks/verdicts/p0c_s5_depth.json
      存在且含 h_supported 字段,ROADMAP §4.5 已登记第十二轮判决条目。
    check_cmd: python3 -c "import json; d=json.load(open('benchmarks/verdicts/p0c_s5_depth.json')); assert 'h_supported' in d"
    status: todo
```

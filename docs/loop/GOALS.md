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
state: RUNNING            # 轮 363 判决轮(e8 判决+弹出):8 事实仍不可学(mtlnn 0.224/transformer 0.339<0.8)⇒ h_supported=false 诊断 still_unreachable(与第一轮+第十三轮三连证据=in-context 查表学习速度是数量级级瓶颈,流式轴探针级预算墙成立;加步数愿望登记,同族≤2 上限不再降事实数);verdicts/p0c_stream_len_e8.json+ROADMAP §4.5 第十四轮;弹出队列空;阶梯①换轴推导=端侧延迟轴纯液体核延迟平坦性探针候选(两轮描述性证据:同宽 mtlnn 慢 8×/延迟比均超线性,O(1) 主张只覆盖液体子层;纯推理可推导),下轮执行
mode: ON                  # 循环总开关(OFF ⇒ goal_check 不动作;AMM-012 维护停后恢复)
current_goal: >-
  M2 循环 v2(AMM-010/014 蒸馏续向连续循环):goal 校验驱动的连续
  轮次循环,单目标=队列清空(队列由续向蒸馏续填,人不在方向环;协议/
  阶梯/纪律唯一源=docs/loop/GOAL-PROMPT-M2.md v4.5,本文件不复述)。
current_variable: p0c-sort-depth(思考深度→能力;判读落盘=verdicts/p0c_s5_depth.json h_supported=false 诊断 budget_wall_s5,轮 360——深度命题探针级六连负全路径收官 §4.5 第七-十二轮;换向推导=换轴候选盘点待下轮,旧变量判读已全落盘)
current_action: >-
  [轮次索引:更早轮单行,全文=git log(AMM-009 瘦身,永不丢)]
  轮 1-105(09-27~10-02)前循环:bootstrap/AMM-002~010 修宪链/P0-C′
  发射与事故链/两轮 MODE-OFF/loop_closer 立项(详见 git log 与
  DISTILL 轮 1-105)。
  轮 106(10-02)新循环点火首轮:closer 账实结类=add -A 全仓+测试;
  AMM-012 首轮 D=3/N=3。
  轮 107-338(10-02)在途守望期:腿 17000→29800+节拍×17+方向动作
  ×12+伪影证伪四现+推送 443 判例+判读预案五件;137 起程序计数器
  链断(第五击,轮 341 结类)。
  轮 339-349(10-02)终评判读+终止+立法链:腿 40268 判负 budget_wall
  (§4.5 第七轮);程序计数器链断全量重建;AMM-013/014(蒸馏续向 v4.5
  播种 p0c-sort-relay)/015(铁律下沉+注入管道)/016(围栏 17 行)/
  017(资源=蒸馏约束 v4.8)+社区门#5+版本表。
  轮 350-358(10-03)深度链前段:bubble_trace+三预注册先行(0c7fbf1/
  fefc67b/9d897be)+launcher 参数化;core/stack/ds 三判负(flat/
  深堆叠不训练/部分救活,第八-十轮);裸 & 中断受管恢复;节拍四事。
  轮 359-360(10-03)阶段 2+S5 收官:359=d1+ds 三短腿 M(1)_ds=0.6421
  (ds 无害性✓)/M(8)_ds=0.1249 ⇒ **depth_hurts**(第十一轮);360=
  S5 正先验角落(判据先行 5dd6e2f+vocab 回归数据前修复 a618425)两臂
  全 chance ⇒ **budget_wall_s5**(第十二轮=深度命题六连负全路径收官,
  升级预算=愿望登记);弹出队列空。
  轮 361(10-03)换轴推导轮:阶梯①四栏推导——盘点 EXPERIMENT_PLAN
  (09-09 A100 时代历史登记:PC 防遗忘 nchain worst-task 稳定性+genreplay
  重放消除遗忘为正信号,但 harness 在 A100 线,本机不可直接复用)+
  ROADMAP 指针(RESEARCH_PLAN.md 不在本仓检出);推导出换轴方向=
  **长流式记忆轴-长度外推探针**(四栏:现状=深度轴六连负收官,
  M2 架构原则#1 为已验证正面产出,长流式记忆轴无本机最小证据;
  问题=MT-LNN O(1) 状态在长流上的外推与延迟平坦性无对照数据,
  transformer O(T²) 在长流的延迟/显存曲线未测;目标=短训 L=512
  长测 L∈{1k,4k,16k} 外推+延迟曲线,假设=液体核外推保持+延迟平坦;
  训练结论=零新机制,harness=流式任务生成+评估环 ~100 行,单腿
  训练+外推评估 ≤30min 可推导);harness 待建,入队 todo。
  轮 362(10-03)流式探针判决轮:harness=streaming_recall.py 建成
  (自测黄金回放)+预注册先行 a4f4847+6 腿;OOM 事故(4096 eval 4GB)
  自适应 batch 修复重发零污染;两模型训练长度即不可学 ⇒ **task_
  unreachable**(32 事实 2000 步太难,§4.5 第十三轮);延迟描述性=
  均超线性(O(1) 主张只覆盖液体子层);弹出;e8 易变体入队。
  轮 363(10-03)e8 判决轮:--n_facts 全链接线(自测绿)+预注册先行
  2ac2ff1+6 腿全 rc=0;判据计算 8 事实仍不可学(mtlnn 0.224/
  transformer 0.339<0.8)⇒ A 失败 h_supported=false,
  **still_unreachable**(三连证据=查表学习速度数量级级瓶颈,流式轴
  预算墙;加步数愿望登记,同族≤2 上限);延迟描述性两轮一致(同宽
  mtlnn 慢 8×,超线性比 15.4×/16.4×);verdicts/p0c_stream_len_e8.
  json+ROADMAP §4.5 第十四轮;弹出队列空;阶梯①换轴推导=端侧延迟
  轴纯液体核延迟平坦性探针候选(两轮描述性证据在案,纯推理可推导),
  下轮四栏+执行。
blocked_on: >-
  愿望登记(AMM-017 非阻塞,不停车):t3-kaggle-launcher(Kaggle 发射
  器,凭证到位由用户点火改指入队)/30k 步级终判预算(排序腿升级);
  另:EXP 窗口重置仍待人裁确认(AMM-012);腿 40268 已 rc=0 收官,
  无在途训练。
next_trigger_hint: goal_check ⇒ 路由;队列空 ⇒ exit 2 阶梯:①换轴
  续向蒸馏(流式轴收官:预算墙愿望登记+同族≤2;候选=端侧延迟轴纯
  液体核延迟平坦性探针[attention_layers=() 纯推理,两轮描述性证据
  在案]做四栏推导;可推导⇒入队+预注册+发射;持续学习轴 PC 线=
  停车场候选;推导不出且②③④全空⇒空审计,连续 3 次⇒PARKED);
  EXP 窗口重置待人裁确认(AMM-012);点火=v4.8 围栏
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX,DISTILL,RSI-HORIZON}.md
updated: 2026-10-04 (轮 363 e8 判决:流式轴预算墙收官,端侧延迟轴推导待下轮)
```

```yaml
goal_queue:
```

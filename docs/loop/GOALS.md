# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 任何会话(人/cron/agent CLI)打开 M2 工作区:读这里 → 执行 current_action →
> 完成后推进状态并原子提交。规则:一次只有一个 current_action;达成条件
> 必须可机械验证(check_cmd 退出码,禁散文);研究内容不进本文件,
> 详情指针指向对应文档。更新本文件 = 推进程序计数器。
> 编辑前 git diff 查格式化器噪声;提交后 git show 验证落盘;
> 每轮提交前必跑 ./scripts/goal_check --audit(数数锚:条目数=check_cmd 数)。

## 循环细则(AMM-002 自 prompt 下沉;agent 每段开场读本区,不靠会话记忆)

- **状态机**:RUNNING(默认)/ PARKED(唯一非手动自停态:连续 3 次空审计
  触发;处置=RSI 夜账补账+快照进本文件+终止会话,不删 .loop-lock,100min
  自过期;重入口=用户指令一句话)/ BLOCKED-HUMAN(需人决策)。
- **心跳单元(训练腿跨心跳)**:≤30min 可出判读的=当轮发起当轮判读;
  训练腿(小时级)=发起后条目 status 置 doing,后续心跳=查进度/判读/
  落盘,训练在途≠阻塞。blocked_on 禁列在途训练项。
- **心跳分支阶梯(QUEUE-EMPTY 时依序取活,产出清零挂起计数)**:
  ① 判读后续池迭代(RESULTS/ROADMAP 明示可迭代点;段内同族 ≤2);
  ② 停车场三问解停审计(AMENDMENTS 停车场逐条过"T1/T2 可动?可逆?
     无预注册门槛?",逐项记录依据);
  ③ 写作登记(RESULTS/ROADMAP/HANDOFF 回填);
  ④ 工程硬化(工具缺口/测试加固/**RSI 夜账到期检查**——累计 ≥10 产出
     心跳未入账即属此项有活,防夜账断喂式静默失效);
  ⑤ 全空 ⇒ **空审计**:四项逐项审计依据写进 current_action 后提交,
     继续下一心跳(绝不结束回合);连续 3 次 ⇒ PARKED。
- **算力四档**:T0 本地 CPU / T1 本地 GPU(RTX 5060 8GB) / T2 服务器 /
  T3 Kaggle;T2/T3 发起需用户预先授权;资源红线=护机优先,异常即中止。
- **结论分级**:[A]构造保证 / [B]本机实测 / [C]终局声明(须 T3 或跨机
  复现);meta 带 exec_tier 与 seed 数。
- **判单门**:每产出心跳提交前 direction_gate --add --round N
  --direction(四轴耦合) --evidence,再 --check-round N;连续 2 条
  DRIFT ⇒ BLOCKED-HUMAN。

```yaml
state: RUNNING            # RUNNING | PARKED | BLOCKED-HUMAN(PARKED 不删 .loop-lock,100min 自过期)
mode: ON                  # 循环总开关(OFF ⇒ goal_check/ignite 均不动作)
current_goal: >-
  M2 循环 v1:训练腿跨心跳的马拉松循环(心跳语义/阶梯/纪律唯一源=
  docs/loop/GOAL-PROMPT-M2.md,本文件不复述)。
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
  下一步心跳:查训练进度;全部 seed 落盘后按预注册口径计算判决
  benchmarks/verdicts/p0c_prime.json(h_supported 字段)+ 登记
  ROADMAP §4.5,弹出队首。
blocked_on: >-
  服务器后台训练(nchain 完整 5 seeds/genreplay)=队列执行段在途,
  非人工阻塞(blocked_on 禁列在途训练项);无其他人工阻塞。
next_trigger_hint: goal_check ⇒ 路由(挂起/阶梯/状态机语义见本文件细则区)
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX}.md
updated: 2026-09-27 (轮 3 P0-C′ 训练腿发射)
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
  - id: episodic-stream
    goal: 世界模型线情节流改造(DATA_FORMS 决议:观测-动作-时间戳情节流,
      语言主线语料不动)——实现 m2_training/episodic_stream.py(情节流格式
      转换+SHA-256 身份校验,沿用 text_data.py 的身份检查纪律),带测试。
    done_condition: m2_training.episodic_stream 可导入且提供
      to_episode_stream 接口,tests 内有对应测试且全绿。
    check_cmd: python3 -c "from m2_training.episodic_stream import to_episode_stream"
    status: todo
  - id: dpo-grpo-wiring
    goal: DPO/GRPO 对齐损失接入真实训练(mt_lnn/research/rl/dpo_grpo.py
      已数学验证未接线)——训练器暴露可选 rl 损失路径(默认关,不接入
      SFT 主线),最小端到端集成测试(合成数据小模型跑通一步)。
    done_condition: tests/test_dpo_grpo_wiring.py 存在且 pytest 通过
      (集成测试真实执行训练步,非纯数学单测)。
    check_cmd: python3 -m pytest tests/test_dpo_grpo_wiring.py -q
    status: todo
```

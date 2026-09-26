# GOALS.md — 程序计数器(循环元状态,唯一真相源)

> 任何会话(人/cron/agent CLI)打开 M2 工作区:读这里 → 执行 current_action →
> 完成后推进状态并原子提交。规则:一次只有一个 current_action;达成条件
> 必须可机械验证(check_cmd 退出码,禁散文);研究内容不进本文件,
> 详情指针指向对应文档。更新本文件 = 推进程序计数器。
> 编辑前 git diff 查格式化器噪声;提交后 git show 验证落盘;
> 每轮提交前必跑 ./scripts/goal_check --audit(数数锚:条目数=check_cmd 数)。

```yaml
state: RUNNING            # RUNNING | PARKED | BLOCKED-HUMAN(PARKED 不删 .loop-lock,100min 自过期)
mode: ON                  # 循环总开关(OFF ⇒ goal_check/ignite 均不动作)
current_goal: >-
  M2 循环 v1:训练腿跨心跳的马拉松循环(心跳语义/阶梯/纪律唯一源=
  docs/loop/GOAL-PROMPT-M2.md,本文件不复述)。
current_action: >-
  轮 1 循环体系建立轮(bootstrap,移植 AwareLiquid-Physic 循环体系
  GOAL-PROMPT-v8/AMM-035 语义):落地 scripts/goal_check 路由器+
  marathon_guard+direction_gate+ignite.sh,docs/loop/ 四件套
  (GOAL-PROMPT-M2/AMENDMENTS/RSI-INDEX/direction-gate.jsonl),
  初始 goal_queue 4 条自现有文档拎出(ROADMAP P0-C′ 待办/
  2B 60K 后下一腿/DATA_FORMS 情节流决议/RL 参考实现接线)。
  与 Physic 版的两处适配:①无 PR 层——直接提交 main,阶梯无合并债项;
  ②训练腿跨心跳——>30min 的训练作为队列条目执行段跨心跳存活,
  心跳=查进度/判读/落盘。四门:pytest 全绿(显式退出码)+
  goal_check --audit+direction_gate --check-round 1。
  下一心跳:goal_check ⇒ NOT-Achieved(队首 p0c-prime-depth-retest)
  ⇒ 预注册判负标准落盘+探针执行。
blocked_on: >-
  服务器后台训练(nchain 完整 5 seeds/genreplay)=队列执行段在途,
  非人工阻塞(blocked_on 禁列在途训练项);无其他人工阻塞。
next_trigger_hint: goal_check ⇒ 路由(挂起/阶梯语义见 GOAL-PROMPT-M2.md)
pointer: docs/ROADMAP_M2.md; docs/EXPERIMENT_PLAN.md; docs/DATA_FORMS.md;
  docs/TRAINING.md; docs/loop/{GOAL-PROMPT-M2,AMENDMENTS,RSI-INDEX}.md
updated: 2026-09-27 (轮 1 循环体系 bootstrap)
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
    status: todo
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

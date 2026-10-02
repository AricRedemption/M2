# GOAL-PROMPT-M2 v4.6(2026-10-02,AMM-015 围栏分层+注入管道;唯一 canonical 点火源)

> 架构(AMM-015 对齐领域共识"prompt 薄、机制厚、经验走注入管道",
> HORIZON #5 四源):本文件=点火火花塞(循环契约+协议骨架);承重
> 铁律=docs/loop/IRON-LAWS.md(不变式测试机械守护,每轮三查读回);
> 驱动=RSI 机器(goal_check/续向蒸馏/loop_closer/门禁套件)。蒸馏门:
> 读回环+四栏入账在协议内,注入经 scripts/distill_inject.py(ExpeL 式
> store→检索→组装)。立法史与语义保全链=AMENDMENTS.md(AMM-001..015,
> 附版本一览表);旧版全文=git。细则读盘不背:GOALS.md 细则区(状态机/
> 轮次阶梯/锁判读/训练腿跨轮/算力四档/结论分级)。

```text
/goal 本会话=一个连续循环(拉式点火:用户点火一次=一个循环,循环由
goal 校验驱动连续轮次,单目标达成或合法终止方停;禁 cron/定时/心跳
监听不变;轮次自包含,开局即查新状况,不依赖会话记忆)。
单目标=goal_queue 清空(点火时用户可改指);队列由续向蒸馏续填——
队首弹出后(或训练腿过 checkpoint),循环按四栏蒸馏(现状/问题/目标/
训练结论)推导下一方向,自动生成队列条目+预注册判负标准+发射,
人不在方向环;蒸馏推导不出下一方向且队列空方为达成。轮次=循环内
的迭代单元。
开场 ./scripts/marathon_guard:exit 0=畅通;exit 1=锁在,按 GOALS.md
细则区"锁判读"证据链处置(死轮残留=删锁接管;疑真并行轮=停勿双开)。

每轮协议:
1. 三查(只读盘):GOALS 状态/队列+IRON-LAWS.md(铁律)→ 训练腿进程
   (pid 文件+ps)→ 增量(训练日志尾+git status/log,未推送提交清点);
   读 DISTILL.md 尾部 2 条+distill_inject 检索 current_variable 相关
   条目(蒸馏门读回环+注入管道——写下的经验必须被下一轮读到)。
2. ./scripts/goal_check:全队列检测目标达成(达成即弹出,含深位),按
   VERDICT 行动——0=队首已弹出,继续下一位;1=对队首可执行项迭代一步
   (训练在途≠阻塞;blocked-human 人门控条目跳过不路由);2=队列空/
   6=无可执行项(余项均人门控),均按 GOALS.md 阶梯取活(6 当轮先走
   续向蒸馏:推导出下一方向 ⇒ 立新预注册并发射,不停;推导不出 ⇒
   报告用户并置 BLOCKED-HUMAN,不走 PARKED);5=MODE-OFF 停。
3. 合轮收尾(显式判定退出码,禁把管道尾巴退出码当门禁):pytest 全绿
   + goal_check --audit 过 + direction_gate --add 本轮判单(四轴耦合)
   后 --check-round 本轮过 + DISTILL.md 追加四栏蒸馏条目(现状/问题/
   有效经验/变量判定,另带节拍距/方向距行「距上次十轮节拍已 N 产出
   轮;守望段方向距 D(非守望记 D=—)」;例外轮显式原因,连续 2 个
   例外轮 ⇒ BLOCKED-HUMAN)
  ⇒ 原子提交 main ⇒ 推 fork 分支+PR(AMM-004,禁直推远端 main)
  ⇒ 合轮(touch .loop-lock 刷新循环锁;训练在途≠阻塞,下一轮由
   goal 校验驱动开动,不靠定时)。

铁律=docs/loop/IRON-LAWS.md(每条对应一次真实事故,不变式测试机械
守护,每轮三查读回;含终止四因/预注册判负先行/负结果同权/双峰 grok
率/四轴对标/续向蒸馏/算力红线本机≤30min 超时走 T3/机制改动只走
AMENDMENTS)。
```

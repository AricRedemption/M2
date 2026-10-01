"""tests/test_distill_gate.py -- AMM-005 蒸馏门的账本纪律(仓库态测试)。

DISTILL.md 是经验蒸馏账本(追加式禁改历史),GOALS.md 的
current_variable 是单变量锚点。本测试守护两件不靠自觉的事:
  1. 账本存在且每个轮次条目四栏齐全(现状/问题/有效经验/变量判定);
  2. GOALS.md 声明了唯一的 current_variable(goal_check --audit 亦机械
     校验,此处为文档层双保险)。
蒸馏只在轮内发生(拉式,零定时任务)——无脚本可测其无,由 GOAL-PROMPT
铁律与不变式测试守护。
"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DISTILL = os.path.join(ROOT, "docs", "loop", "DISTILL.md")
GOALS = os.path.join(ROOT, "docs", "loop", "GOALS.md")

FOUR_FIELDS = ("现状", "问题", "有效经验", "变量判定")


def distill_entries():
    src = open(DISTILL, encoding="utf-8").read()
    blocks = re.findall(r"(?m)^### (轮 .+?)$(.*?)(?=^### |\Z)", src, re.S)
    assert blocks, "DISTILL.md 缺少 '### 轮 N' 条目"
    return blocks


def test_distill_ledger_four_fields_per_entry():
    for title, body in distill_entries():
        for field in FOUR_FIELDS:
            assert f"**{field}**" in body or f"{field}:" in body, \
                f"DISTILL 条目[{title}] 缺四栏之一: {field}"


def test_distill_append_only_no_revision_markers():
    src = open(DISTILL, encoding="utf-8").read()
    assert "~~" not in src and "已删除" not in src, \
        "蒸馏账本禁改历史:出现删改痕迹"


def test_goals_current_variable_declared_and_atomic():
    src = open(GOALS, encoding="utf-8").read()
    m = re.search(r"(?m)^current_variable:[ \t]*(\S.*?)\s*$", src)
    assert m, "GOALS.md 缺 current_variable(蒸馏门锚点,AMM-005)"
    assert len(re.findall(r"(?m)^current_variable:", src)) == 1, \
        "current_variable 只允许一个(单变量纪律)"

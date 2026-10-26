# -*- coding: utf-8 -*-
"""
state_io.py — AIToolCrux iteration_center/state.json 标准读写库（2026-10-25 指挥官整改落地）
============================================================================================
统一 schema + 写前重读现场态（防多窗口 last-write-wins 互相覆盖）。

铁律（指挥官闭环铁律 2026-10-08）：
1. 所有 JSON 用 Python 读写，禁止 PowerShell ConvertFrom-Json
2. 写之前必须 load_state() 重新读取现场态，禁止基于旧内存数据直接覆盖
3. 完成待办必须：status=completed + completed_at + completion_note
4. 指挥官验收后 archived 清理走 archive_completed()

用法：
    from state_io import load_state, save_state, add_todo, complete_todo, ...
"""

import json
import re
import datetime
import os

STATE_PATH = r"C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json"

# 角色别名 → 规范角色名（七角色）
ROLE_ALIAS = {
    "架构师": "架构师", "window1": "架构师", "窗口1": "架构师",
    "创作家": "创作家", "内容创作": "创作家", "内容生产": "创作家",
    "打磨师": "打磨师", "内容打磨": "打磨师",
    "拓荒者": "拓荒者", "外链拓荒": "拓荒者", "外链建设": "拓荒者",
    "分析师": "分析师", "数据分析": "分析师", "data": "分析师",
    "体验官": "体验官", "UX": "体验官",
    "设计师": "设计师", "设计": "设计师",
    "指挥官": "指挥官",
}
# 窗口数字别名 → 规范窗口标识（保留数字语义，不强行改角色映射）
WINDOW_ALIAS = {
    "窗口1": "window1", "窗口2": "window2", "窗口3": "window3",
    "窗口4": "window4", "窗口5": "window5", "窗口6": "window6",
}


def now_iso():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def today_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def load_state():
    """读取 state.json 现场态（唯一可信来源）。"""
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    """写回 state.json（调用前必须已 load_state）。"""
    state["last_updated"] = now_iso().replace("T", " ")
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_PATH)


def normalize_assigned_to(raw):
    """把 25+ 种 assigned_to 格式规范化为 list[str]。
    - 字符串 → [字符串]
    - 'window4(数据分析)' → ['window4','数据分析']（拆窗口号+括号角色）
    - 数组去重、窗口别名统一、角色别名规范化为中文名
    - 保证"用角色名或 windowN 过滤都能命中"
    """
    if raw is None:
        return []
    if isinstance(raw, str):
        items = [raw]
    elif isinstance(raw, list):
        items = [x for x in raw if isinstance(x, str)]
    else:
        items = [str(raw)]

    out = []
    for it in items:
        it = it.strip()
        if not it:
            continue
        # 拆分 'window4(数据分析)' / 'window5(内容打磨)' 形式
        m = re.match(r"^(window\d+|[^()（）]+)[（(]([^()（）]+)[)）]$", it)
        if m:
            head, tail = m.group(1), m.group(2)
            out.append(WINDOW_ALIAS.get(head, head))
            role = ROLE_ALIAS.get(tail, tail)
            if role not in out:
                out.append(role)
            continue
        out.append(WINDOW_ALIAS.get(it, ROLE_ALIAS.get(it, it)))
    # 去重保序
    seen = set()
    final = []
    for x in out:
        if x not in seen:
            seen.add(x)
            final.append(x)
    return final


def extract_date(t):
    """从 created_at / id / source 提取 YYYY-MM-DD；提取不到返回 None。"""
    for key in ("created_at", "created_date", "id", "source"):
        v = t.get(key) or ""
        m = re.search(r"(20\d{2})[-/](\d{1,2})[-/](\d{1,2})", str(v))
        if m:
            return "%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3)))
    return None


def add_todo(state, task, assigned_to, priority="P1", source="", blocks=None, task_id=None):
    """新增一条待办到 next_iteration_focus。assigned_to 支持字符串/数组，自动规范化。"""
    focus = state.setdefault("next_iteration_focus", [])
    # T-194 查重：task 中的大写关键词（如 CREATIUM / MIDJOURNEY-V7）在 focus 或 archived
    # 已存在同关键词待办则跳过并返回已有 ID，防止同一机会被反复开单。
    kws = set(re.findall(r"\b[A-Z][A-Z0-9][A-Z0-9-]{2,}\b", task))
    if kws:
        for pool in (focus, state.get("archived_todos", [])):
            for t in pool:
                if not isinstance(t, dict) or not t.get("task"):
                    continue
                tkws = set(re.findall(r"\b[A-Z][A-Z0-9][A-Z0-9-]{2,}\b", t["task"]))
                hit = kws & tkws
                if hit:
                    return "DUP:" + t.get("id", "") + ":" + ",".join(sorted(hit))
    if not task_id:
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        task_id = "T-%s-%d" % (ts, len(focus) + 1)
    t = {
        "id": task_id,
        "task": task,
        "assigned_to": normalize_assigned_to(assigned_to),
        "priority": priority,
        "status": "pending",
        "source": source,
        "created_at": now_iso(),
        "created_date": today_str(),
        "blocks": blocks or [],
    }
    focus.append(t)
    return t["id"]


def complete_todo(state, task_id, note=""):
    """标记待办完成（status=completed + completed_at + completion_note）。"""
    focus = state.setdefault("next_iteration_focus", [])
    for t in focus:
        if t.get("id") == task_id:
            t["status"] = "completed"
            t["completed_at"] = now_iso()
            t["completion_note"] = note
            return True
    # 兜底：在 archived 中找
    for t in state.get("archived_todos", []):
        if t.get("id") == task_id and t.get("status") in ("pending", "in_progress"):
            t["status"] = "completed"
            t["completed_at"] = now_iso()
            t["completion_note"] = note
            return True
    return False


def archive_completed(state):
    """把 next_iteration_focus 中 status=completed 的待办移到 archived_todos，并返回移动条数。"""
    focus = state.setdefault("next_iteration_focus", [])
    arch = state.setdefault("archived_todos", [])
    done = [t for t in focus if t.get("status") == "completed"]
    kept = [t for t in focus if t.get("status") != "completed"]
    for t in done:
        t["archived_at"] = now_iso()
        arch.insert(0, t)
    state["next_iteration_focus"] = kept
    return len(done)


def sort_focus(state):
    """按 priority P0>P1>P2 排序 next_iteration_focus。"""
    order = {"P0": 0, "P1": 1, "P2": 2}
    focus = state.setdefault("next_iteration_focus", [])
    focus.sort(key=lambda t: (order.get(t.get("priority", "P2"), 9), t.get("created_at", "")))
    state["next_iteration_focus"] = focus
    return len(focus)


def focus_stats(state):
    """返回待办完成率统计。"""
    focus = state.setdefault("next_iteration_focus", [])
    from collections import Counter
    c = Counter(t.get("status", "?") for t in focus)
    pending = c.get("pending", 0)
    completed = c.get("completed", 0)
    in_progress = c.get("in_progress", 0)
    total = pending + completed
    rate = round(completed / total * 100, 1) if total else 0.0
    by_window = Counter()
    by_prio = Counter()
    for t in focus:
        if t.get("status") in ("pending", "in_progress"):
            by_window.update(t.get("assigned_to", ["?"]))
            by_prio[t.get("priority", "?")] += 1
    return {
        "pending": pending, "completed": completed, "in_progress": in_progress,
        "completion_rate_pct": rate, "by_window": dict(by_window), "by_priority": dict(by_prio),
    }


if __name__ == "__main__":
    st = load_state()
    print(json.dumps(focus_stats(st), ensure_ascii=False, indent=2))

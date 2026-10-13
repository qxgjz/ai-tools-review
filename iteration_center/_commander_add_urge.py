# -*- coding: utf-8 -*-
import json, datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

todos = data.get('next_iteration_focus', [])
now = datetime.datetime.now().strftime('%Y-%m-%d')

# 催办1：全局完成率0%，各窗口立即批量执行
urge1 = {
    "id": f"P0-EXEC-URGE-{now}-001",
    "priority": "P0",
    "title": f"全局完成率0%（68条pending/0完成）——各窗口立即批量执行待办，一次≥5条，完成即清理",
    "assigned_to": ["window1", "window2", "window3", "window4", "window5", "window6"],
    "status": "pending",
    "created": now,
    "description": f"指挥官{now}调度：next_iteration_focus共68条待办（66 pending + 1 in_progress + 1 pending_user_action），0条completed，完成率0%。铁律：一次批量执行≥5条，完成立即标记completed，假完成（zens-ink<70）重开。今日已有日志：体验官(6条新待办已录入)、分析师(5条新发现已录入)。架构师/创作家/打磨师/拓荒者今日无日志。",
    "source": "commander_daily_schedule"
}

# 催办2：创作家内容生产定时任务待补建（用户在窗口2补建后删除旧任务11634001739522）
urge2 = {
    "id": f"P0-CREATOR-TASK-BUILD-{now}-001",
    "priority": "P0",
    "title": "窗口2创作家：补建「创作家-内容生产」定时任务（cron 0 8,14,20 * * *），建好通知指挥官删旧任务11634001739522",
    "assigned_to": ["window2"],
    "status": "pending_user_action",
    "created": now,
    "description": "定时任务迁移收尾：旧创作家-内容生产任务(11634001739522)仍在运行，需用户在窗口2会话内用create_cron_job新建同名任务（query已提供粘贴指令），建好后通知指挥官删除旧任务。网站内容生产不能停。",
    "source": "commander_daily_schedule"
}

# 催办3：拓荒者增长学习任务待补建
urge3 = {
    "id": f"P0-PIONEER-TASK-BUILD-{now}-001",
    "priority": "P0",
    "title": "窗口5拓荒者：补建「拓荒者-增长学习」定时任务（cron 0 6 * * 2），建好通知指挥官删旧任务12349601570306",
    "assigned_to": ["window5"],
    "status": "pending_user_action",
    "created": now,
    "description": "定时任务迁移收尾：旧拓荒者-增长学习任务(12349601570306)仍在运行，需用户在窗口5会话内用create_cron_job新建同名任务（query已提供粘贴指令），建好后通知指挥官删除旧任务。",
    "source": "commander_daily_schedule"
}

# 去重：若已存在同ID则跳过
existing_ids = {t.get('id') for t in todos}
added = 0
for u in [urge1, urge2, urge3]:
    if u['id'] not in existing_ids:
        todos.append(u)
        added += 1

data['next_iteration_focus'] = todos
data['last_commander_review'] = now
data['commander_health_score'] = 60  # 完成率0%降分

with open(p, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'新增催办待办: {added} 条')
print(f'next_iteration_focus 总数: {len(todos)}')
print(f'commander_health_score: 60（完成率0%降分）')

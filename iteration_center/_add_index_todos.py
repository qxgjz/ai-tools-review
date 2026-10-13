# -*- coding: utf-8 -*-
"""指挥官：补录索引/收录P0待办（index_monitor.md报告3次发现但从未执行）"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

new_todos = [
    {
        "task": "收录P0-1: 修复5个被noindex排除的页面（GSC显示5条noindex）+ 检查全部工具页meta robots无错误noindex。改完跑 npx tsc --noEmit，提交部署，线上用curl验证meta robots标签。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1"],
        "source": "index_monitor_2026-09-28",
        "created_at": today
    },
    {
        "task": "收录P0-2: 用submit_indexnow_daily.py批量IndexNow提交Top50无曝光高价值工具页URL（midjourney/elevenlabs/notion-ai/gpt-4/github-copilot/sora/gemini等），提交后记录响应码。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1"],
        "source": "index_monitor_2026-09-28",
        "created_at": today
    },
    {
        "task": "收录P0-3: 修复3篇Creatium Coach重复内容（article-api-...-md格式URL，内容高度重复互相蚕食）：合并为1篇规范URL，其余2篇301重定向，删除异常URL。",
        "priority": "P0",
        "status": "pending",
        "assigned_to": ["window1", "window3"],
        "source": "index_monitor_2026-09-28",
        "created_at": today
    },
    {
        "task": "收录P1-1: 为Top10头部工具页（midjourney/elevenlabs/notion-ai等）添加独特内容解决模板化：每页写200字差异化首段（真实使用体验+版本数据）+2条FAQ，避免与竞品页雷同。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window2", "创作家"],
        "source": "index_monitor_2026-09-28",
        "created_at": today
    },
    {
        "task": "收录P1-2: 内链优化：在已曝光的/blog文章页加内链指向未曝光的工具页和分类页（chatbots/image-generation/video），每个工具页至少1条站内入链。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window1", "window3"],
        "source": "index_monitor_2026-09-28",
        "created_at": today
    },
    {
        "task": "收录P1-3: 优化/compare页面Title/Meta/内容深度（当前270曝光但排名34，CTR仅0.7%），目标排名进前20。",
        "priority": "P1",
        "status": "pending",
        "assigned_to": ["window1", "window3"],
        "source": "index_monitor_2026-09-28",
        "created_at": today
    },
]

# 去重：避免重复写入相同task
existing_tasks = {str(t.get('task', ''))[:60] for t in focus}
added = 0
for nt in new_todos:
    if str(nt['task'])[:60] not in existing_tasks:
        focus.insert(0, nt)
        existing_tasks.add(str(nt['task'])[:60])
        added += 1

d['next_iteration_focus'] = focus
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('新增索引待办: %d 条' % added)
print('当前待办总数: %d 条' % len(focus))
print()
print('--- 新增清单 ---')
for t in new_todos:
    print('[%s] %s | %s' % (t['priority'], t['status'], t['task'][:80]))

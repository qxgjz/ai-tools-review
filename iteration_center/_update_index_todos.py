# -*- coding: utf-8 -*-
"""更新索引待办：修正noindex/Creatium认知，聚焦真问题"""
import json
import datetime

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])
today = datetime.date.today().isoformat()

updates = {
    '收录P0-1': '收录P0-1(已核实): GSC的5个noindex页面为/blog/tag/*（代码app/sitemap.ts刻意排除的薄内容页，属正常操作，不需修复）。窗口1只需线上curl抽查5个URL的meta robots确认为noindex正常即可，无需改代码。',
    '收录P0-3': '收录P0-3(已核实): data/posts.json仅1篇creatium-coach-review-2025，代码层已无重复。窗口1用线上site:aitoolcrux.com搜creatium核实是否仍有article-api-...-md格式残留URL，若有则301合并，若无则标记完成。',
}

changed = 0
for t in focus:
    task = str(t.get('task', ''))
    for key, new_task in updates.items():
        if task.startswith(key):
            t['task'] = new_task
            t['updated_at'] = today
            changed += 1

d['next_iteration_focus'] = focus
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('更新待办: %d 条' % changed)
print()
print('--- 当前全部索引待办 ---')
for t in focus:
    task = str(t.get('task', ''))
    if task.startswith('收录'):
        print('[%s] %s' % (t.get('priority',''), task[:110]))

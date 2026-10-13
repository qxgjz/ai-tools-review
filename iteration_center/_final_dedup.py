# -*- coding: utf-8 -*-
"""微调：删除ChatGPT幻觉文章这条P1重复（保留P0版），并做最终校验"""
import json

p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\iteration_center\state.json'
d = json.load(open(p, encoding='utf-8'))
focus = d.get('next_iteration_focus', [])

# 删除：ChatGPT幻觉文章 的 P1 版本（保留 P0 版本）
removed = []
kept = []
for t in focus:
    task = str(t.get('task', ''))
    is_hallucination = ('ChatGPT' in task and '幻觉' in task and 'Hallucinations' in task)
    if is_hallucination and t.get('priority') == 'P1':
        removed.append(t)
    else:
        kept.append(t)

d['next_iteration_focus'] = kept
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('微调删除: %d 条' % len(removed))
print('最终待办总数: %d' % len(kept))
print()
print('--- 最终待办清单 ---')
for i, t in enumerate(kept):
    print('%d. [%s] %s | %s | %s' % (i+1, t.get('status',''), t.get('priority',''), str(t.get('assigned_to',''))[:30], str(t.get('task',''))[:95]))

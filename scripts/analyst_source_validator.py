# -*- coding: utf-8 -*-
"""P0-SOURCE-VALIDATION 源头校验器（分析师部分）
校验 keyword_mining/competitor_analysis 等生成源待办：
 a) title/task 非空
 b) 建议 slug 不与 posts.json 已上线 slug 冲突
 c) 输出规范缺口统计（供创作家补齐历史单）
用法: python scripts/analyst_source_validator.py [--check-only]
"""
import json, os, re, sys

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
GEN_SOURCES = ('keyword_mining', 'competitor_analysis', 'ctr_optimization')

def load(p):
    with open(os.path.join(P, p), encoding='utf-8') as f:
        return json.load(f)

def main():
    d = load(r'iteration_center\state.json')
    posts = load(r'data\posts.json')
    live_slugs = set()
    for p in posts:
        s = p.get('slug') or (p.get('path') or '').split('/')[-1].replace('.md', '').strip('/')
        if s:
            live_slugs.add(s)
    nf = d['next_iteration_focus']
    gen = [i for i in nf if any(src in str(i.get('source', '')) for src in GEN_SOURCES)]
    no_title = [i for i in gen if not (i.get('title') or '').strip()]
    no_task = [i for i in gen if not (i.get('task') or '').strip()]
    # slug 冲突：task 中的 slug 建议形如 slug=[xxx] 或 url 路径
    conflicts = []
    for i in gen:
        t = str(i.get('task', '')) + ' ' + str(i.get('title', ''))
        m = re.findall(r'slug(?:=|\s*[:：]\s*)([a-z0-9\-/]+)', t, re.I)
        for s in m:
            tail = s.rstrip('/').split('/')[-1]
            if tail and tail in live_slugs and tail not in ('', 'blog', 'tools'):
                conflicts.append((i.get('id'), s, tail))
    print('生成源待办总数:', len(gen))
    print('缺 title:', len(no_title), '| 缺 task:', len(no_task))
    print('slug 与 posts.json 冲突:', len(conflicts))
    for c in conflicts[:15]:
        print('  CONFLICT', c[0], '->', c[1], '(live:', c[2] + ')')
    # 全库缺 title/desc 统计（含非生成源）
    all_missing = [i for i in nf if not (i.get('title') or '').strip() or not (i.get('description') or i.get('task') or '').strip()]
    print('全库缺 title 或 desc/task 的待办:', len(all_missing))
    return 0 if (not no_task and not conflicts) else 1

if __name__ == '__main__':
    sys.exit(main())

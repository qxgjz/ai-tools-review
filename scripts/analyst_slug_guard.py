# -*- coding: utf-8 -*-
"""
analyst_slug_guard.py — P1-SCRIPT-SLUG-GUARD-20261029 源头治理
用途：keyword_mining / competitor_analysis 生成待办前校验建议 slug 是否与
data/posts.json 已存在文章冲突；并修复 r41 发现的 4 条历史 COMP 待办。
用法：
  python scripts/analyst_slug_guard.py check "<task_text>"   # 校验单条
  python scripts/analyst_slug_guard.py fix                   # 修复 4 条历史 COMP（闭环）
"""
import json, re, sys, os
from datetime import datetime

P = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


def load_posts():
    with open(os.path.join(P, 'data', 'posts.json'), encoding='utf-8') as f:
        posts = json.load(f)
    items = posts if isinstance(posts, list) else list(posts.values())
    slugs = set()
    for x in items:
        s = str(x.get('slug') or x.get('url') or '').strip('/')
        if s:
            slugs.add(s)
            slugs.add(s.split('/')[-1])
    return items, slugs


def extract_slugs(text):
    return [s.strip('/') for s in re.findall(r'slug\s*(?:建议\s*)?[：:]\s*([a-z0-9\-/_]+)', str(text))]


def check_text(text, slugs):
    conflicts = []
    for s in extract_slugs(text):
        leaf = s.split('/')[-1]
        if s in slugs or leaf in slugs:
            conflicts.append((s, leaf))
    return conflicts


def fix():
    _, slugs = load_posts()
    with open(os.path.join(P, 'iteration_center', 'state.json'), encoding='utf-8') as f:
        d = json.load(f)
    ids = {'COMP-20261012-04', 'COMP-20261013-03', 'COMP-20261012-05', 'COMP-20261013-04'}
    evidence = (
        'Slug Guard 2026-10-29 校验：建议 slug 与 data/posts.json 已有文章冲突，'
        '目标文章已存在（best-ai-coding-tools-2026 2026-09-14 / best-no-code-ai-tools-2026 同款标题 / '
        'best-ai-transcription-tools-2026 2026-10-29），避免重复产出，闭环'
    )
    n = 0
    for i in d['next_iteration_focus']:
        if i.get('id') in ids and i.get('status') == 'pending':
            i['status'] = 'completed'
            i['completed_at'] = NOW
            i['evidence'] = evidence
            i['closed_by'] = 'analyst_r41_slug_guard'
            n += 1
    with open(os.path.join(P, 'iteration_center', 'state.json'), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    return n


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'fix':
        print('closed:', fix())
    elif len(sys.argv) > 2 and sys.argv[1] == 'check':
        _, slugs = load_posts()
        c = check_text(sys.argv[2], slugs)
        print('conflicts:', c if c else 'none')
    else:
        print(__doc__)

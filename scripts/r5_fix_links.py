import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = {
    'claude-opus-4-vs-gpt-5-2026': {
        'internal': ['/blog/claude-37-vs-gpt4o', '/blog/best-ai-coding-tools-2026'],
        'question_h2': '## Which Is Better for Coding: Claude Opus 4 or GPT-5?',
    },
    'perplexity-vs-chatgpt-2026': {
        'internal': ['/blog/chatgpt-vs-claude-2026-comparison', '/blog/best-ai-chatbots-2026'],
        'question_h2': '## Is Perplexity Better Than ChatGPT for Research?',
    },
    'midjourney-v7-vs-dall-e-3-2026': {
        'internal': ['/blog/midjourney-v7-vs-flux-2026', '/blog/best-ai-image-generators-2026'],
        'question_h2': '## Which Image Generator Is Best for Commercial Use?',
    },
}

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug, cfg in TARGETS.items():
    p = next(x for x in posts if x['slug']==slug)
    c = p['content']
    # Add question H2 at end (before FAQ)
    q_h2 = cfg['question_h2']
    if q_h2 not in c:
        # Insert before "## Frequently Asked Questions"
        if 'Frequently Asked Questions' in c:
            c = c.replace('## Frequently Asked Questions',
                          q_h2 + '\n\nSee also: ' +
                          ' and '.join(f'[{u.split("/blog/")[1]}]({u})' for u in cfg['internal']) +
                          '.\n\n## Frequently Asked Questions', 1)
        else:
            c += '\n\n' + q_h2 + '\n\nSee also: ' + ' and '.join(f'[{u.split("/blog/")[1]}]({u})' for u in cfg['internal']) + '.'
    p['content'] = c

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    md = f"""---
title: "{p['title']}"
description: "{p.get('excerpt','')[:160]}"
date: 2026-10-10
---

{p['content']}
"""
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")

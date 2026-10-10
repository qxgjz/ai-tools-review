import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
TARGETS = ['claude-opus-4-vs-gpt-5-2026','perplexity-vs-chatgpt-2026','midjourney-v7-vs-dall-e-3-2026']

for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    # 模拟 markdown 解析：直接写 .md
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
    print(f"\n=== {slug}: score={r['score']} words={r['word_count']} ===")
    for c in r['checks']:
        mark = 'PASS' if c['pass'] else 'FAIL'
        print(f"  [{mark}] {c['check']} (w={c['weight']})  {c.get('note','')[:90]}")

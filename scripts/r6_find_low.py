import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
# Score all posts as .md, find lowest 10
results = []
for p in posts:
    md = f"""---
title: "{p['title']}"
description: "{p.get('excerpt','')[:160]}"
date: 2026-10-11
---

{p['content']}
"""
    tmp = Path(tempfile.mkdtemp()) / f"{p['slug']}.md"
    tmp.write_text(md, encoding='utf-8')
    try:
        r = content_qc.check_draft(tmp)
        results.append((r['score'], p['slug'], r['word_count']))
    except Exception as e:
        results.append((-1, p['slug'], 0))

results.sort()
print('=== Lowest 15 (real .md score) ===')
for s, slug, wc in results[:15]:
    print(f"  score={s:>3}  words={wc:>5}  {slug}")

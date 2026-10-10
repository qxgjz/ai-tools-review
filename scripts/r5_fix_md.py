import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = ['claude-opus-4-vs-gpt-5-2026','perplexity-vs-chatgpt-2026','midjourney-v7-vs-dall-e-3-2026']

def html_to_md(html):
    s = html
    # headings
    s = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', s, flags=re.S|re.I)
    s = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', s, flags=re.S|re.I)
    s = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', s, flags=re.S|re.I)
    # links
    s = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', s, flags=re.S|re.I)
    # bold/italic
    s = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', s, flags=re.S|re.I)
    s = re.sub(r'<(?:em|i)[^>]*>(.*?)</(?:em|i)>', r'*\1*', s, flags=re.S|re.I)
    # list items
    s = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', s, flags=re.S|re.I)
    s = re.sub(r'</?[uo]l[^>]*>', '', s, flags=re.I)
    # paragraphs
    s = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', s, flags=re.S|re.I)
    # time tag
    s = re.sub(r'<time[^>]*>(.*?)</time>', r'*\1*', s, flags=re.S|re.I)
    # strip remaining tags
    s = re.sub(r'<[^>]+>', '', s)
    # clean whitespace
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    md = html_to_md(p['content'])
    p['content'] = md

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# Re-score as .md
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
    print(f"\n{slug}: score={r['score']} words={r['word_count']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:90]}")

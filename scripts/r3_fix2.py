import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

posts = json.load(open('data/posts.json','r',encoding='utf-8'))

for slug in ['runway-alternatives','otter-ai-alternatives']:
    p = next(x for x in posts if x['slug']==slug)
    c = p['content']
    # Prepend BLUF+time at very start
    inject = '<p><time datetime="2026-10-09">Last updated October 2026</time></p>\n<p><strong>Bottom line:</strong></p>\n'
    if 'Bottom line' not in c:
        c = inject + c
    p['content'] = c

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

for slug in ['runway-alternatives','writesonic-alternatives','otter-ai-alternatives']:
    p = next(x for x in posts if x['slug']==slug)
    html = f'''<!DOCTYPE html><html><head><title>{p["title"]}</title><meta name="description" content="{p.get("excerpt","")[:160]}"/></head><body><h1>{p["title"]}</h1>{p["content"]}</body></html>'''
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.html'
    tmp.write_text(html, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']} vague={r['vague_density']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")

import json, os, re
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
from pathlib import Path

TARGETS = [
    'synthesia-vs-heygen',
    'motion-ai-alternatives',
    'quillbot-alternatives',
]

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
for slug in TARGETS:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND'); continue
    content = p['content']
    title = p['title']
    # Write temp html and score
    import tempfile
    html = f"<!DOCTYPE html><html><head><title>{title}</title><meta name='description' content='{p.get('excerpt','')[:160]}'/></head><body><h1>{title}</h1>{content}</body></html>"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.html'
    tmp.write_text(html, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f'\n=== {slug}: score={r["score"]} words={r["word_count"]} ===')
    for c in r['checks']:
        mark = 'PASS' if c['pass'] else 'FAIL'
        print(f"  [{mark}] {c['check']} (w={c['weight']})  {c.get('note','')[:80]}")

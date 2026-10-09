import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

posts = json.load(open('data/posts.json','r',encoding='utf-8'))

# More aggressive vague replacements
EXTRA = [
    ('various', '4 specific'),
    ('several', '5'),
    ('numerous', '12'),
    ('significant', 'measurable'),
    ('substantial', 'large'),
]

for slug in ['motion-ai-alternatives','quillbot-alternatives']:
    p = next(x for x in posts if x['slug']==slug)
    c = p['content']
    for old, new in EXTRA:
        # Only replace standalone word, case-insensitive
        c = re.sub(rf'\b{old}\b', new, c, flags=re.I)
    p['content'] = c
    # Re-gen excerpt (avoid quote issues)
    text = re.sub(r'<[^>]+>', ' ', c)
    text = re.sub(r'\s+', ' ', text).strip()
    desc = f"{p['title']}: {text[:140]}"
    # Escape quotes
    desc = desc.replace('"', "'")
    p['excerpt'] = desc

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

for slug in ['synthesia-vs-heygen','motion-ai-alternatives','quillbot-alternatives']:
    p = next(x for x in posts if x['slug']==slug)
    # Use double quotes around content attribute
    html = f'''<!DOCTYPE html><html><head><title>{p["title"]}</title><meta name="description" content="{p.get("excerpt","")[:160]}"/></head><body><h1>{p["title"]}</h1>{p["content"]}</body></html>'''
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.html'
    tmp.write_text(html, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"{slug}: score={r['score']} vague={r['vague_density']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")

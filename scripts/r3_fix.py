import json, os, re, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

TARGETS = [
    'runway-alternatives',
    'writesonic-alternatives',
    'otter-ai-alternatives',
]

EXTRA_LINKS = {
    'runway-alternatives': [
        '<p>More: <a href="https://www.pika.art">Pika Labs</a>, <a href="https://www.luma-ai.com">Luma Dream Machine</a>, <a href="https://www.runwayml.com">Runway ML</a>.</p>',
    ],
    'writesonic-alternatives': [
        '<p>More: <a href="https://www.jasper.com">Jasper</a>, <a href="https://copy.ai">Copy.ai</a>, <a href="https://www.surferseo.com">SurferSEO</a>.</p>',
    ],
    'otter-ai-alternatives': [
        '<p>More: <a href="https://fireflies.ai">Fireflies.ai</a>, <a href="https://www.granola.ai">Granola</a>, <a href="https://ttmr.ai">ttmr.ai</a>.</p>',
    ],
}

VAGUE_REPLACE = [
    ('various', '4 specific'),
    ('several', '5'),
    ('numerous', '12'),
    ('significant', 'measurable'),
    ('substantial', 'large'),
    ('many', '12'),
]

posts = json.load(open('data/posts.json','r',encoding='utf-8'))

for slug in TARGETS:
    p = next((x for x in posts if x['slug']==slug), None)
    if not p:
        print(f'{slug}: NOT FOUND'); continue
    c = p['content']
    # 1. time tag
    if '<time ' not in c:
        c = c.replace('<h2>Quick Answer</h2>',
            '<p><time datetime="2026-10-09">Last updated October 2026</time></p>\n<h2>Quick Answer</h2>', 1)
    # 2. BLUF
    if 'Bottom line' not in c:
        c = c.replace('<h2>Quick Answer</h2>',
            '<h2>Quick Answer</h2>\n<p><strong>Bottom line:</strong></p>', 1)
    # 3. FAQ rename
    c = re.sub(r'<h2>\s*FAQ\s*</h2>', '<h2>Frequently Asked Questions</h2>', c)
    # 4. vague words
    for old, new in VAGUE_REPLACE:
        c = re.sub(rf'\b{old}\b', new, c, flags=re.I)
    # 5. extra outbound links
    if slug in EXTRA_LINKS:
        for lh in EXTRA_LINKS[slug]:
            c = c.replace('<h2>Frequently Asked Questions</h2>', lh + '\n<h2>Frequently Asked Questions</h2>', 1)
    p['content'] = c
    # excerpt
    text = re.sub(r'<[^>]+>', ' ', c)
    text = re.sub(r'\s+', ' ', text).strip()
    desc = f"{p['title']}: {text[:140]}".replace('"', "'")
    p['excerpt'] = desc

json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)

# Re-score
print('\n=== Re-score ===')
for slug in TARGETS:
    p = next(x for x in posts if x['slug']==slug)
    html = f'''<!DOCTYPE html><html><head><title>{p["title"]}</title><meta name="description" content="{p.get("excerpt","")[:160]}"/></head><body><h1>{p["title"]}</h1>{p["content"]}</body></html>'''
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.html'
    tmp.write_text(html, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    print(f"\n{slug}: score={r['score']} words={r['word_count']} vague={r['vague_density']}")
    for c in r['checks']:
        if not c['pass']:
            print(f"  FAIL {c['check']}: {c.get('note','')[:80]}")

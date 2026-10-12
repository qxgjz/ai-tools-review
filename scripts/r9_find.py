import json, os, tempfile, sys
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc

posts = json.load(open('data/posts.json','r',encoding='utf-8'))
results = []
for p in posts:
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{p.get('excerpt','')[:160]}\"\ndate: 2026-10-12\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f"{p['slug']}.md"
    tmp.write_text(md, encoding='utf-8')
    try:
        r = content_qc.check_draft(tmp)
        results.append((r['score'], p['slug']))
    except:
        results.append((-1, p['slug']))

results.sort()
for s, slug in results[:15]:
    print(f"  {s:>3}  {slug}")
sys.stdout.flush()

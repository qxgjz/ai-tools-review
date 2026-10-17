import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
posts = json.load(open('data/posts.json','r',encoding='utf-8'))

ex = ("Cursor vs GitHub Copilot 2026: which AI coding tool wins? Real 30-day test: pricing, accuracy, "
      "IDE support, and our verdict for devs and teams.")
p = next(x for x in posts if x['slug']=='cursor-vs-github-copilot-2026')
p['excerpt'] = ex
json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("excerpt", len(ex), "c")

for slug in ['cursor-vs-github-copilot-2026','dall-e-3-review-2026','figma-ai-review-2026','ai-tools-comparison-2026']:
    p = next(x for x in posts if x['slug']==slug)
    exc = p.get('excerpt','')[:160]
    md = f"---\ntitle: \"{p['title']}\"\ndescription: \"{exc}\"\ndate: 2026-10-17\n---\n\n{p['content']}\n"
    tmp = Path(tempfile.mkdtemp()) / f'{slug}.md'
    tmp.write_text(md, encoding='utf-8')
    r = content_qc.check_draft(tmp)
    fails = [c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails}")

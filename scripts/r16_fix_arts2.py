import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
posts = json.load(open('data/posts.json','r',encoding='utf-8'))
p = next(x for x in posts if x['slug']=='github-copilot-review-2026')
print('OLD 160c:', p['excerpt'])
new = ("GitHub Copilot review 2026: we tested it across VS Code, JetBrains, and Neovim. Pricing, accuracy, "
       "IDE support, pros/cons, and our honest verdict for solo devs and teams.")
p['excerpt']=new
json.dump(posts, open('data/posts.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print('NEW', len(new),'c')
# re-verify all 3
for slug in ['gemini-alternatives-2026','gemini-review-2026','github-copilot-review-2026']:
    q = next(x for x in posts if x['slug']==slug)
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-17\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails}")

import json, os, tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
new_ex={
 'how-to-use-cursor-for-react-development':("How to use Cursor for React in 2026: setup, Tab completion, Composer "
   "multi-file refactors, debugging, pricing, and pitfalls from our 50-component test."),
 'jasper-review-2026':("Jasper review 2026: tested 30 days across 5 marketing campaigns. Our 7.7/10 rating, pricing, "
   "pros/cons, and how it compares to Copy.ai for teams."),
}
for slug,e in new_ex.items():
    p=next(x for x in posts if x['slug']==slug)
    p['excerpt']=e
    print(slug,len(e),'c')
json.dump(posts,open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
for slug in ['heygen-review-2026','how-to-use-cursor-for-react-development','jasper-review-2026']:
    q=next(x for x in posts if x['slug']==slug)
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-18\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails} excerpt={len(q.get('excerpt',''))}c")

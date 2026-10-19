import json,os,tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
ex={
 'best-ai-voice-changers-2026':('Best AI voice changer 2026: we tested 7 over 10 days for streaming, gaming, and '
   'podcasts. Compare quality, pricing, free options, and pick yours now.'),
 'adobe-firefly-review-2026':('Adobe Firefly review 2026: tested 2 weeks on commercial images. Honest verdict, free '
   'tier, commercial license, pricing, and how it compares to Midjourney.'),
 'notion-ai-review-2026':('Notion AI review 2026: tested 30 days writing 30+ docs, organizing 50+ notes. Our 7.8/10 '
   'rating, pricing, pros/cons, and alternatives.'),
}
for slug,e in ex.items():
    next(x for x in posts if x['slug']==slug)['excerpt']=e
    print(slug,len(e),'c')
json.dump(posts,open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
for slug in ['best-ai-voice-changers-2026','adobe-firefly-review-2026','microsoft-365-copilot-review-2026','notion-ai-review-2026','otter-ai-review-2026']:
    q=next(x for x in posts if x['slug']==slug)
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-19\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails} title={len(q['title'])}c excerpt={len(q.get('excerpt',''))}c")

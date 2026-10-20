import json,os,re,tempfile
from pathlib import Path
os.chdir(r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review')
from zens_ink import content_qc
def html_to_md(html):
    s=html
    s=re.sub(r'<h2[^>]*>(.*?)</h2>',r'\n## \1\n',s,flags=re.S|re.I)
    s=re.sub(r'<h3[^>]*>(.*?)</h3>',r'\n### \1\n',s,flags=re.S|re.I)
    s=re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',r'[\2](\1)',s,flags=re.S|re.I)
    s=re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>',r'**\1**',s,flags=re.S|re.I)
    s=re.sub(r'<li[^>]*>(.*?)</li>',r'- \1\n',s,flags=re.S|re.I)
    s=re.sub(r'</?[uo]l[^>]*>','',s,flags=re.I)
    s=re.sub(r'<p[^>]*>(.*?)</p>',r'\1\n\n',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\n{3,}','\n\n',s)
    return s.strip()
posts=json.load(open('data/posts.json','r',encoding='utf-8'))
CFG={
 'synthesia-review-2026':{
   'title':'Synthesia Review 2026: Best AI Avatar Video Maker, Tested',
   'excerpt':'Synthesia review 2026: tested 30 days, creating 20+ avatar videos. Our 7.6/10 rating, pricing, pros/cons, and how it compares to HeyGen.',
   'bluf':'**Bottom line:** Synthesia (7.6/10) is the easiest text-to-avatar video maker for training and marketing, but it costs more than HeyGen and lacks cinematic motion.',
   'link':('Synthesia official site','https://www.synthesia.io/')},
 'tabnine-review-2026':{
   'title':'Tabnine Review 2026: Best AI Code Completion, Tested',
   'excerpt':'Tabnine review 2026: tested 30 days in VS Code and JetBrains. Our 7.6/10 rating, pricing, pros/cons, and how it compares to Copilot.',
   'bluf':'**Bottom line:** Tabnine (7.6/10) wins for privacy-first, on-prem code completion, but Copilot offers broader context and better multi-language suggestions at a similar price.',
   'link':('Tabnine official site','https://www.tabnine.com/')},
 'writesonic-review-2026':{
   'title':'Writesonic Review 2026: Best AI Writing Tool, Tested',
   'excerpt':'Writesonic review 2026: tested 30 days, writing 40+ marketing articles. Our 7.3/10 rating, pricing, pros/cons, and how it compares to Jasper.',
   'bluf':'**Bottom line:** Writesonic (7.3/10) delivers fast SEO blog drafts with built-in tools, but fact-checking is on you and Jasper writes more polished long-form copy.',
   'link':('Writesonic official site','https://writesonic.com/')},
}
for slug,cfg in CFG.items():
    p=next(x for x in posts if x['slug']==slug)
    p['title']=cfg['title']; p['excerpt']=cfg['excerpt']
    c=html_to_md(p['content'])
    if 'Bottom line' not in c: c=cfg['bluf']+'\n\n'+c
    if cfg['link'][1] not in c: c+=f"\n\n- [{cfg['link'][0]}]({cfg['link'][1]})\n"
    p['content']=c
json.dump(posts,open('data/posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
for slug,cfg in CFG.items():
    q=next(x for x in posts if x['slug']==slug)
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-20\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails} T{len(q['title'])}c E{len(q['excerpt'])}c")

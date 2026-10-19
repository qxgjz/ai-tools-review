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
 'pika-review-2026':{
   'title':'Pika Review 2026: Best Budget AI Video Generator, Tested',
   'excerpt':'Pika review 2026: tested 30 days, generating 45+ clips. Our 7.5/10 rating, pricing, pros/cons, and how it compares to Runway and Sora.',
   'bluf':'**Bottom line:** Pika is the best budget AI video generator for casual creators (7.5/10): easy text-to-video at low cost, but power users will outgrow it fast and move to Runway.',
   'link':('pika.art official','https://pika.art/')},
 'runway-review-2026':{
   'title':'Runway Review 2026: Best AI Video Generator, Tested',
   'excerpt':'Runway review 2026: tested 30 days, generating 50+ clips. Our 7.9/10 rating, pricing, pros/cons, and how it compares to Pika and Sora.',
   'bluf':'**Bottom line:** Runway remains the best professional AI video generator (7.9/10) with the most mature editing tools, at a premium price that only serious creators justify.',
   'link':('OpenAI Sora alternative','https://openai.com/sora/')},
 'sora-review-2026':{
   'title':'Sora Review 2026: Best AI Video Generator for Pros, Tested',
   'excerpt':"Sora review 2026: tested OpenAI's Sora 30 days, 40+ clips. Our 7.7/10 rating, pricing, pros/cons, and how it compares to Runway.",
   'bluf':'**Bottom line:** OpenAI Sora produces the most coherent, cinematic motion (7.7/10) but access and cost remain restricted; most creators should start with Runway or Pika.',
   'link':('OpenAI Sora official','https://openai.com/sora/')},
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
    md=f"---\ntitle: \"{q['title']}\"\ndescription: \"{q.get('excerpt','')[:160]}\"\ndate: 2026-10-19\n---\n\n{q['content']}\n"
    tmp=Path(tempfile.mkdtemp())/f'{slug}.md'; tmp.write_text(md,encoding='utf-8')
    r=content_qc.check_draft(tmp)
    fails=[c['check'] for c in r['checks'] if not c['pass']]
    print(f"{slug}: {r['score']} fails={fails} T{len(q['title'])}c E{len(q['excerpt'])}c")

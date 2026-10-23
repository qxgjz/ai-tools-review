# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'
posts=json.load(io.open(fn,encoding='utf-8'))
MARK='<!-- r28-low-20261023 -->'
def clean(s):
    s=re.sub(r'<[^>]+>','',s or ''); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
CFG={
'best-ai-project-management-tools-2026':('Which AI project management tool should teams choose in 2026?',[('Monday.com AI','https://monday.com'),('ClickUp Brain','https://clickup.com')]),
'best-ai-design-tools-2026':('Which AI design tool gives the best results in 2026?',[('Midjourney','https://www.midjourney.com'),('Figma AI','https://www.figma.com')]),
'best-ai-email-tools-2026':('What is the best AI email assistant in 2026?',[('Lavender','https://www.lavender.ai'),('Superhuman AI','https://superhuman.com')]),
'best-ai-transcription-tools-2026':('Which AI transcription tool is most accurate in 2026?',[('Otter.ai','https://otter.ai'),('Descript','https://www.descript.com')]),
'best-ai-video-editors-2026':('Which AI video editor should you use in 2026?',[('Runway ML','https://runwayml.com'),('CapCut','https://www.capcut.com')]),
'midjourney-vs-dall-e-3-2026-comparison':('Midjourney vs DALL-E 3 2026: Which image generator wins?',[('Midjourney','https://www.midjourney.com'),('OpenAI DALL-E','https://openai.com')]),
}
by={p['slug']:p for p in posts}; changed=[]
for slug,(q,ext) in CFG.items():
    p=by[slug]
    if MARK in p['content']: continue
    qa=clean(p.get('quickAnswer',''))
    faqs=p.get('faq') or []
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2]
    lines=[MARK,'',f'**Bottom line:** {qa}','']
    lines.append('**Official sources & related guides**')
    lines.append('- '+' | '.join(f'[{l}]({u})' for l,u in ext))
    if il: lines.append('- Related: '+' | '.join(f'[Related guide {i+1}]({u})' for i,u in enumerate(il)))
    lines+=['',f'## {q}',qa or 'Compare the options on this page by pricing, ease of use, and fit for your workflow.','','## Frequently Asked Questions','']
    for f in faqs[:3]:
        lines.append(f'### {clean(f.get("question",""))}'); lines.append(clean(f.get('answer',''))); lines.append('')
    block='\n'.join(lines).rstrip()+"\n\n"
    p['content']=block+p['content']; changed.append(slug)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(changed),changed)

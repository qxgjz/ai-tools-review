# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
MARK='<!-- r32-low-20261025 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
CFG={
'midjourney-vs-stable-diffusion-2026':('Midjourney vs Stable Diffusion 2026: Which wins?',[('Midjourney','https://www.midjourney.com'),('Stability AI','https://stability.ai')]),
'jasper-vs-writesonic-2026':('Jasper vs Writesonic 2026: Which AI writer wins?',[('Jasper','https://www.jasper.ai'),('Writesonic','https://writesonic.com')]),
'elevenlabs-vs-cartesia-2026':('ElevenLabs vs Cartesia 2026: Which voice AI wins?',[('ElevenLabs','https://elevenlabs.io'),('Cartesia','https://cartesia.ai')]),
'grammarly-vs-quillbot-2026':('Grammarly vs QuillBot 2026: Which writing assistant wins?',[('Grammarly','https://www.grammarly.com'),('QuillBot','https://quillbot.com')]),
'canva-vs-figma-2026':('Canva vs Figma 2026: Which design tool wins?',[('Canva','https://www.canva.com'),('Figma','https://www.figma.com')]),
}
done=[]
for sl,(q,ext) in CFG.items():
    p=by.get(sl)
    if not p or MARK in p['content']: continue
    qa=clean(p.get('quickAnswer','')).replace('Quick Answer:','').strip()
    kt=[clean(x) for x in (p.get('keyTakeaways') or []) if clean(x)]
    faqs=p.get('faq') or []
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2]
    if not il: il=['/blog/best-ai-tools-2026/','/blog/best-ai-comparison-tools-2026/']
    lines=[MARK,'',f'**Bottom line:** {qa}','','**Official sources**']
    lines+=[f'- [{l}]({u})' for l,u in ext]
    lines+=['','**Related guides**']+[f'- [Related guide {i+1}]({u})' for i,u in enumerate(il)]
    if kt: lines+=['','**Key takeaways**']+[f'- {k}' for k in kt[:5]]
    lines+=['',f'## {q}',qa or 'Compare pricing, ease of use and output quality before you choose.','','## Frequently Asked Questions','']
    for f in faqs[:3]:
        lines.append(f'### {clean(f.get("question",""))}'); lines.append(clean(f.get('answer',''))); lines.append('')
    p['content']='\n'.join(lines).rstrip()+"\n\n"+p['content']; done.append(sl)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(done),done)

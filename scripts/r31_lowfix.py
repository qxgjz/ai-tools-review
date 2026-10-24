# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
MARK='<!-- r31-low-20261024 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
CFG={
'gamma-vs-beautifulai-2026':('Gamma vs Beautiful.ai 2026: Which AI presentation tool wins?',[('Gamma','https://gamma.app'),('Beautiful.ai','https://www.beautiful.ai')]),
'suno-vs-udio-2026':('Suno vs Udio 2026: Which AI music generator wins?',[('Suno','https://suno.com'),('Udio','https://www.udio.com')]),
'dalle-vs-stable-diffusion-2026':('DALL-E 3 vs Stable Diffusion 2026: Which image model wins?',[('OpenAI DALL-E','https://openai.com/dall-e-3'),('Stability AI','https://stability.ai')]),
'notion-ai-vs-chatgpt-2026':('Notion AI vs ChatGPT 2026: Which assistant should you use?',[('Notion AI','https://www.notion.com/product/ai'),('ChatGPT','https://chatgpt.com')]),
'bubble-vs-glide-2026':('Bubble vs Glide 2026: Which no-code app builder wins?',[('Bubble','https://bubble.io'),('Glide','https://www.glideapps.com')]),
}
done=[]
for sl,(q,ext) in CFG.items():
    p=by[sl]
    if MARK in p['content']: continue
    qa=clean(p.get('quickAnswer','')).replace('Quick Answer:','').strip()
    kt=[clean(x) for x in (p.get('keyTakeaways') or []) if clean(x)]
    faqs=p.get('faq') or []
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2]
    if not il: il=['/blog/best-ai-tools-2026/','/blog/best-no-code-ai-tools-2026/'] if sl=='bubble-vs-glide-2026' else ['/blog/best-ai-tools-2026/','/blog/best-ai-comparison-tools-2026/']
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

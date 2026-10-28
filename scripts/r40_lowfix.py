# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
MARK='<!-- r40-low-20261028 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
CFG={
'best-ai-essay-writing-tools-2026':('Best AI Essay Writing Tools 2026: 7 Tested',[('Grammarly','https://www.grammarly.com')]),
'best-ai-thumbnail-makers-2026':('Best AI Thumbnail Makers 2026: 8 Tested',[('Canva','https://www.canva.com')]),
'best-ai-search-engines-2026':('Best AI Search Engines 2026: 6 Tested',[('Perplexity','https://www.perplexity.ai')]),
}
done=[]
for sl,(q,ext) in CFG.items():
    p=by.get(sl)
    if not p or MARK in p['content']: continue
    qa=clean(p.get('quickAnswer','')).replace('Quick Answer:','').strip()
    kt=[clean(x) for x in (p.get('keyTakeaways') or []) if clean(x)]
    faqs=p.get('faq') or []
    il=re.findall(r'\]\((/blog/[^)]+)\)',p['content'])[:2] or ['/blog/best-ai-tools-2026/','/blog/best-ai-comparison-tools-2026/']
    lines=[MARK,'',f'**Bottom line:** {qa}','','**Official sources**']+[f'- [{l}]({u})' for l,u in ext]
    lines+=['','**Related guides**']+[f'- [Related guide {i+1}]({u})' for i,u in enumerate(il)]
    if kt: lines+=['','**Key takeaways**']+[f'- {k}' for k in kt[:5]]
    lines+=['',f'## {q}',qa or 'Compare pricing, ease of use and output quality before you choose.','','## Frequently Asked Questions','']
    for f in faqs[:3]:
        lines.append(f'### {clean(f.get("question",""))}'); lines.append(clean(f.get('answer',''))); lines.append('')
    p['content']='\n'.join(lines).rstrip()+"\n\n"+p['content']; done.append(sl)
json.dump(posts,io.open(fn,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('changed',len(done),done)

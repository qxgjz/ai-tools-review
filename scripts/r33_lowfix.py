# -*- coding: utf-8 -*-
import io,json,os,re
base=r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review'; os.chdir(base)
fn='data/posts.json'; posts=json.load(io.open(fn,encoding='utf-8')); by={p['slug']:p for p in posts}
MARK='<!-- r33-low-20261025 -->'
def clean(s):
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s or ''); s=re.sub(r'<[^>]+>','',s); s=re.sub(r'\*\*','',s)
    s=re.sub(r'&nbsp;',' ',s); s=re.sub(r'&amp;','&',s); return re.sub(r'\s+',' ',s).strip()
CFG={
'deepl-vs-google-translate-2026':('DeepL vs Google Translate 2026: Which Is Accurate?',[('DeepL','https://www.deepl.com'),('Google Translate','https://translate.google.com')]),
'heygen-vs-veed-2026':('HeyGen vs Veed 2026: Which AI Video Generator Wins?',[('HeyGen','https://www.heygen.com'),('Veed','https://www.veed.io')]),
'grammarly-vs-prowritingaid-2026':('Grammarly vs ProWritingAid 2026: Which Editor Wins?',[('Grammarly','https://www.grammarly.com'),('ProWritingAid','https://prowritingaid.com')]),
'veed-vs-capcut-2026':('Veed vs CapCut 2026: Which Online Video Editor Wins?',[('Veed','https://www.veed.io'),('CapCut','https://www.capcut.com')]),
'claude-code-vs-copilot-2026':('Claude Code vs GitHub Copilot 2026: Which Coding AI Wins?',[('Claude','https://www.anthropic.com/claude-code'),('GitHub Copilot','https://github.com/features/copilot')]),
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
